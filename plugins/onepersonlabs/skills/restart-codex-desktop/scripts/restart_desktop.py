#!/usr/bin/env python3
"""Wait for a manual Windows Desktop Quit, reopen it, and optionally queue once."""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time
import uuid
import xml.etree.ElementTree as ET


DISCOVER = r"""
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)
$packages = @(Get-AppxPackage -Name OpenAI.Codex)
if ($packages.Count -ne 1) { throw 'Expected exactly one installed OpenAI.Codex package' }
$package = $packages[0]
[xml]$manifest = Get-Content -LiteralPath (Join-Path $package.InstallLocation 'AppxManifest.xml')
$apps = @($manifest.SelectNodes('/*[local-name()="Package"]/*[local-name()="Applications"]/*[local-name()="Application"][@Id="App"]'))
if ($apps.Count -ne 1) { throw 'Expected one manifest App entrypoint' }
$exe = [IO.Path]::GetFullPath((Join-Path $package.InstallLocation $apps[0].Executable))
$processes = @(Get-Process | Where-Object { $_.Path -and $_.Path -eq $exe } | ForEach-Object {
    @{ pid = $_.Id; started = $_.StartTime.ToUniversalTime().Ticks.ToString() }
})
@{ root = $package.InstallLocation; processes = $processes } | ConvertTo-Json -Depth 4 -Compress
"""


def desktop_executable(root: Path) -> Path:
    """Use the package entrypoint, never a similarly named bundled CLI runner."""
    root = root.resolve(strict=True)
    manifest = ET.parse(root / "AppxManifest.xml")
    apps = [app for app in manifest.findall("{*}Applications/{*}Application")
            if app.attrib.get("Id") == "App"]
    if len(apps) != 1:
        raise ValueError("expected one manifest App entrypoint")
    executable = (root / apps[0].attrib["Executable"]).resolve(strict=True)
    if executable.parent != root / "app" or executable.name.lower() not in {"codex.exe", "chatgpt.exe"}:
        raise ValueError("manifest entrypoint is not a recognized Desktop UI executable")
    if not (executable.parent / "resources" / "app.asar").is_file():
        raise ValueError("Desktop application resources are missing")
    return executable


def inspect_desktop() -> dict:
    if os.name != "nt":
        raise RuntimeError("this helper supports native Windows Appx installations only")
    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", DISCOVER],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=20, check=False,
        creationflags=subprocess.CREATE_NO_WINDOW,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Desktop inspection failed: {result.stderr.strip() or result.stdout.strip()}")
    state = json.loads(result.stdout)
    state["executable"] = str(desktop_executable(Path(state["root"])))
    return state


def identities(state: dict) -> set[tuple[int, str]]:
    return {(int(item["pid"]), str(item["started"])) for item in state["processes"]}


def wait_for_exit(target: dict, timeout: float, inspect=inspect_desktop,
                  clock=time.monotonic, sleep=time.sleep) -> None:
    original = identities(target)
    if not original:
        raise RuntimeError("Desktop is not running; this restart helper will not launch an unobserved target")
    deadline = clock() + timeout
    while True:
        current = inspect()
        if current["executable"] != target["executable"]:
            raise RuntimeError("installed Desktop changed while waiting; inspect again before reopening")
        running = identities(current)
        if running - original:
            raise RuntimeError("new Desktop processes appeared; reconcile a possible external restart")
        if not running:
            return
        if clock() >= deadline:
            raise TimeoutError("Desktop did not exit before the timeout; no launch or continuation was attempted")
        sleep(min(0.5, max(0, deadline - clock())))


def queue_once(cli: Path, home: Path, thread: str, message: str) -> dict:
    environment = os.environ.copy()
    environment["CODEX_HOME"] = str(home)
    try:
        result = subprocess.run(
            [str(cli), "queue", "--thread", thread, "--message", message, "--resume"],
            stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=30,
            encoding="utf-8", errors="replace", env=environment,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        # The server might have accepted the prompt before the client failed.
        return {"state": "unknown", "error": str(error), "retry": False}
    return {
        "state": "accepted" if result.returncode == 0 else "unknown",
        "exit_code": result.returncode,
        "stdout": result.stdout.strip(), "stderr": result.stderr.strip(),
        "resume_confirmed": False, "retry": False,
    }


def wait_for_start(target: dict, inspect=inspect_desktop,
                   clock=time.monotonic, sleep=time.sleep) -> None:
    deadline = clock() + 30
    while True:
        current = inspect()
        if current["executable"] != target["executable"]:
            raise RuntimeError("Desktop installation changed during launch; no continuation was attempted")
        if identities(current):
            return
        if clock() >= deadline:
            raise TimeoutError("no new Desktop process was observed; no continuation was attempted")
        sleep(0.5)


def prepare_continuation(target: dict, args: argparse.Namespace) -> Path | None:
    if args.codex_home and not args.message:
        raise ValueError("--codex-home requires --message")
    if not args.message:
        return None
    if not args.thread or not args.codex_home:
        raise ValueError("--message requires --thread and --codex-home")
    home = Path(args.codex_home).resolve(strict=True)
    if not home.is_dir():
        raise ValueError("--codex-home must be a directory")
    cli = Path(target["executable"]).parent / "resources" / "codex.exe"
    if not cli.is_file():
        raise RuntimeError("the package's native CLI runner is missing")
    help_result = subprocess.run([str(cli), "queue", "--help"], capture_output=True,
                                 text=True, encoding="utf-8", errors="replace", timeout=20, check=True)
    if "--resume" not in help_result.stdout:
        raise RuntimeError("this installed CLI does not support queue --resume")
    return cli


def restart(args: argparse.Namespace, inspect=inspect_desktop, launch=subprocess.Popen) -> dict:
    target = inspect()
    cli = prepare_continuation(target, args)
    print(json.dumps({"state": "waiting_for_manual_quit", "executable": target["executable"],
                      "processes": target["processes"], "timeout_seconds": args.timeout_seconds}), flush=True)
    wait_for_exit(target, args.timeout_seconds, inspect=inspect)
    command = [target["executable"]]
    if args.thread:
        command.append(f"codex://threads/{args.thread}")
    launch(command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    wait_for_start(target, inspect=inspect)
    # A process launch is observable; UI readiness and loaded configuration are not.
    result = {"state": "new_process_observed", "executable": target["executable"],
              "thread": args.thread, "ui_ready": False}
    if cli:
        result["continuation"] = queue_once(cli, Path(args.codex_home).resolve(), args.thread, args.message)
    return result


def positive_timeout(value: str) -> float:
    number = float(value)
    if not math.isfinite(number) or not 1 <= number <= 300:
        raise argparse.ArgumentTypeError("timeout must be between 1 and 300 seconds")
    return number


def thread_id(value: str) -> str:
    try:
        return str(uuid.UUID(value))
    except ValueError as error:
        raise argparse.ArgumentTypeError("thread must be an exact UUID") from error


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["inspect", "wait-and-reopen"])
    parser.add_argument("--thread", type=thread_id)
    parser.add_argument("--message", help="explicitly authorized continuation; queued once after launch")
    parser.add_argument("--codex-home", help="native Windows Codex home owning the destination thread")
    parser.add_argument("--timeout-seconds", type=positive_timeout, default=60)
    args = parser.parse_args()
    try:
        if args.mode == "inspect":
            if args.message or args.thread or args.codex_home:
                raise ValueError("inspect does not accept continuation arguments")
            result = inspect_desktop()
        else:
            result = restart(args)
        print(json.dumps(result, indent=2))
        return 0 if result.get("continuation", {}).get("state", "accepted") == "accepted" else 2
    except (OSError, ValueError, RuntimeError, ET.ParseError, subprocess.SubprocessError) as error:
        print(json.dumps({"state": "failed", "error": str(error)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
