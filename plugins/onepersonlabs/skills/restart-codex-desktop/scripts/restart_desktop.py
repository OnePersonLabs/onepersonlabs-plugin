#!/usr/bin/env python3
"""Restart Windows Desktop from an independent helper, then optionally continue."""

from __future__ import annotations

import argparse
import ctypes
from ctypes import wintypes
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time
import uuid
import xml.etree.ElementTree as ET


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
from windows_ui import QuitInputError, inspect_quit_target, request_quit

DEFAULT_CONTINUATION = "Continue the authorized work from its last checkpoint. Verify the restarted app's loaded configuration before proceeding."


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


def restart(args: argparse.Namespace, inspect=inspect_desktop, launch=subprocess.Popen,
            quit_app=None, report=lambda **values: None, target=None) -> dict:
    if target:
        # Renderer processes can change during the short arming delay. The original
        # main-window identity must still exist; refresh its dependent process set.
        selected = target["quit_window"]
        current = inspect()
        if (current["executable"] != target["executable"]
                or (selected["pid"], selected["started"]) not in identities(current)):
            raise RuntimeError("Desktop changed after preparation; no Quit input was sent")
        target = current
    else:
        target = inspect()
    cli = prepare_continuation(target, args)
    report(state="requesting_quit")
    try:
        quit_result = (quit_app or request_quit)(target)
    except QuitInputError as error:
        # Ctrl+Q may already have reached the app before input delivery became
        # uncertain. Never send it again; actual exit decides whether to reopen.
        quit_result = error.details
    report(state="waiting_for_exit", quit_result=quit_result)
    wait_for_exit(target, args.timeout_seconds, inspect=inspect)
    report(state="old_processes_exited")
    command = [target["executable"]]
    if args.thread:
        command.append(f"codex://threads/{args.thread}")
    environment = os.environ.copy()
    if args.codex_home:
        environment["CODEX_HOME"] = str(Path(args.codex_home).resolve())
    launch(command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
           stderr=subprocess.DEVNULL, env=environment)
    wait_for_start(target, inspect=inspect)
    # A process launch is observable; UI readiness and loaded configuration are not.
    result = {"state": "new_process_observed", "executable": target["executable"],
              "thread": args.thread, "ui_ready": False, "quit_result": quit_result}
    if cli:
        report(state="submitting_continuation")
        message = args.message
        if getattr(args, "receipt", None):
            message += f"\n\nRestart receipt: {args.receipt}. Reconcile the result and delete this receipt and its matching .claimed file once no recovery remains."
        result["continuation"] = queue_once(cli, Path(args.codex_home).resolve(), args.thread, message)
    return result


LAUNCH_HELPER = r"""
$ErrorActionPreference = 'Stop'
$spec = [Console]::In.ReadToEnd() | ConvertFrom-Json
$startup = New-CimInstance -ClassName Win32_ProcessStartup -ClientOnly -Property @{
    ShowWindow = [uint16]0; CreateFlags = [uint32]16777216
}
$result = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{
    CommandLine = $spec.commandLine; CurrentDirectory = $spec.cwd; ProcessStartupInformation = $startup
}
$result | Select-Object ReturnValue,ProcessId | ConvertTo-Json -Compress
"""


def independent_process() -> bool:
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    kernel.IsProcessInJob.argtypes = [wintypes.HANDLE, wintypes.HANDLE, ctypes.POINTER(wintypes.BOOL)]
    inside = wintypes.BOOL()
    if not kernel.IsProcessInJob(kernel.GetCurrentProcess(), None, ctypes.byref(inside)):
        raise ctypes.WinError(ctypes.get_last_error())
    return not inside.value


def write_receipt(path: Path, record: dict) -> None:
    temporary = path.with_suffix(".writing")
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(record, stream, indent=2)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def worker(receipt: Path) -> dict:
    # An exclusive claim prevents a repeated internal worker invocation from quitting twice.
    claim = receipt.with_suffix(".claimed")
    with claim.open("x", encoding="utf-8") as stream:
        stream.write(str(os.getpid()))
    record = json.loads(receipt.read_text(encoding="utf-8"))

    def report(**values):
        record.update(values, updated_at=time.time())
        write_receipt(receipt, record)

    try:
        if not independent_process():
            raise RuntimeError("Restart helper remains in a parent job; Desktop was not closed")
        args = argparse.Namespace(**record["request"])
        args.receipt = str(receipt)
        report(state="armed", helper_pid=os.getpid(), independent=True)
        delay = record["not_before"] - time.time()
        if delay > 0:
            time.sleep(delay)
        if time.time() > record["not_before"] + 30:
            raise RuntimeError("Restart launch expired; Desktop was not closed")
        result = restart(args, report=report, target=record["target"])
        report(state="finished", result=result)
        return result
    except Exception as error:
        report(state="failed", error=str(error), details=getattr(error, "details", None))
        raise


def arm_restart(args: argparse.Namespace, inspect=inspect_desktop) -> dict:
    target = inspect()
    if not identities(target):
        raise RuntimeError("Desktop is not running")
    target["quit_window"] = inspect_quit_target(target)
    prepare_continuation(target, args)
    directory = Path(args.codex_home) / "onepersonlabs" / "desktop-restarts"
    directory.mkdir(parents=True, exist_ok=True)
    receipt = directory / f"{uuid.uuid4()}.json"
    record = {"state": "prepared", "created_at": time.time(),
              "not_before": time.time() + args.delay_seconds,
              "target": target, "request": vars(args),
              "disposal": "Remove this receipt and matching claim after the resumed owner reconciles the result. Preserve unresolved continuation state."}
    write_receipt(receipt, record)
    command = subprocess.list2cmdline([sys.executable, "-B", str(Path(__file__).resolve()),
                                      "worker", "--receipt", str(receipt)])
    try:
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", LAUNCH_HELPER],
            input=json.dumps({"commandLine": command, "cwd": str(SCRIPT_DIR)}),
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=20,
            creationflags=subprocess.CREATE_NO_WINDOW, check=True)
        started = json.loads(result.stdout)
        if started["ReturnValue"] != 0:
            raise RuntimeError(f"Windows helper launch failed: {started['ReturnValue']}")
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            current = json.loads(receipt.read_text(encoding="utf-8"))
            if current["state"] == "failed":
                raise RuntimeError(current["error"])
            if current.get("independent"):
                return {"state": "armed", "helper_pid": started["ProcessId"],
                        "receipt": str(receipt), "not_before": record["not_before"]}
            time.sleep(0.1)
        raise RuntimeError("Helper readiness is uncertain; inspect the receipt instead of launching another")
    except Exception as error:
        # A process may already exist. Do not overwrite its state or retry the launch.
        raise RuntimeError(f"{error}; restart receipt: {receipt}") from error


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
    parser.add_argument("mode", choices=["inspect", "restart", "worker", "status"])
    parser.add_argument("--thread", type=thread_id)
    parser.add_argument("--message", help="explicitly authorized continuation; queued once after launch")
    parser.add_argument("--codex-home", help="native Windows Codex home owning the destination thread")
    parser.add_argument("--timeout-seconds", type=positive_timeout, default=60)
    parser.add_argument("--delay-seconds", type=positive_timeout, default=10)
    parser.add_argument("--receipt", type=Path, help="existing restart receipt for status/internal worker")
    args = parser.parse_args()
    try:
        if args.mode == "inspect":
            if args.message or args.thread or args.codex_home:
                raise ValueError("inspect does not accept continuation arguments")
            result = inspect_desktop()
        elif args.mode in {"worker", "status"}:
            if not args.receipt:
                raise ValueError("--receipt is required")
            result = worker(args.receipt) if args.mode == "worker" else json.loads(args.receipt.read_text(encoding="utf-8"))
        else:
            args.codex_home = str(Path(args.codex_home or os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))).resolve(strict=True))
            if args.thread and not args.message:
                args.message = DEFAULT_CONTINUATION
            # The worker receives JSON-only arguments and never a shell command.
            args.receipt = None
            result = arm_restart(args)
        print(json.dumps(result, indent=2))
        return 0 if result.get("continuation", {}).get("state", "accepted") == "accepted" else 2
    except (OSError, ValueError, RuntimeError, ET.ParseError, subprocess.SubprocessError) as error:
        print(json.dumps({"state": "failed", "error": str(error)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
