#!/usr/bin/env python3
"""Arm an independent Windows Desktop exit watcher, then reopen and optionally continue."""

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
$processes = @(Get-CimInstance Win32_Process | Where-Object { $_.ExecutablePath -eq $exe } | ForEach-Object {
    $processId = $_.ProcessId
    $native = Get-Process -Id $processId -ErrorAction SilentlyContinue
    if (-not $native) { return }
    try {
        if (-not $_.CommandLine) { throw 'Cannot identify Desktop process role' }
        @{ pid = $_.ProcessId; started = $native.StartTime.ToUniversalTime().Ticks.ToString()
       parent_pid = $_.ParentProcessId
       kind = $(if ($_.CommandLine -match '(?:^|\s)--type(?:=|\s)') { 'child' } else { 'main' })
       hwnd = $native.MainWindowHandle.ToInt64(); title = $native.MainWindowTitle }
    } catch {
        # A renderer or the original main can exit while this read-only snapshot is built.
        if (-not (Get-Process -Id $processId -ErrorAction SilentlyContinue)) { return }
        throw
    }
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


def identity(process: dict) -> tuple[int, str]:
    return int(process["pid"]), str(process["started"])


def main_processes(state: dict) -> list[dict]:
    # Electron renderer/utility turnover is normal. Only its browser/main process
    # owns the app lifetime; command-line type and exact-image parents distinguish it.
    processes = state["processes"]
    pids = {int(item["pid"]) for item in processes}
    mains = [item for item in processes if item["kind"] == "main"]
    if any(int(item["parent_pid"]) in pids for item in mains):
        raise RuntimeError("ambiguous Desktop main-process ancestry; reconcile before restarting")
    return mains


def check_installation(target: dict, current: dict) -> None:
    if current["executable"] != target["executable"] or current["root"] != target["root"]:
        raise RuntimeError("installed Desktop changed; no launch or continuation was attempted")


def original_main_running(target: dict, current: dict) -> bool:
    check_installation(target, current)
    mains = main_processes(current)
    if any(identity(item) != identity(target["main_process"]) for item in mains):
        raise RuntimeError("new Desktop main process appeared; reconcile a possible external restart")
    return bool(mains)


def wait_for_exit(target: dict, timeout: float, inspect=inspect_desktop,
                  clock=time.monotonic, sleep=time.sleep) -> None:
    deadline = clock() + timeout
    while True:
        if not original_main_running(target, inspect()):
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
                   clock=time.monotonic, sleep=time.sleep) -> dict:
    deadline = clock() + 30
    while True:
        current = inspect()
        check_installation(target, current)
        mains = main_processes(current)
        if len(mains) > 1 or any(identity(item) == identity(target["main_process"]) for item in mains):
            raise RuntimeError("ambiguous Desktop launch; no continuation was attempted")
        if mains:
            return mains[0]
        if clock() >= deadline:
            raise TimeoutError("no new Desktop main process was observed; no continuation was attempted")
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


def watch_and_relaunch(args: argparse.Namespace, target: dict, inspect=inspect_desktop,
                       launch=subprocess.Popen, report=lambda **values: None) -> dict:
    cli = prepare_continuation(target, args)
    # Readiness precedes the agent's GUI Quit. The app may already be gone when
    # the first observation runs, so never require it to remain alive afterward.
    report(state="waiting_for_exit", exit_deadline=time.time() + args.timeout_seconds)
    wait_for_exit(target, args.timeout_seconds, inspect=inspect)
    report(state="original_main_exited")
    command = [target["executable"]]
    if args.thread:
        command.append(f"codex://threads/{args.thread}")
    environment = os.environ.copy()
    if args.codex_home:
        environment["CODEX_HOME"] = str(Path(args.codex_home).resolve())
    # Recheck immediately before our one launch, including replacement-main refusal.
    if original_main_running(target, inspect()):
        raise RuntimeError("original Desktop main reappeared; reconcile before reopening")
    report(state="launching", launch_attempted=True)
    launch(command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
           stderr=subprocess.DEVNULL, env=environment)
    new_main = wait_for_start(target, inspect=inspect)
    # Process observation does not establish UI readiness or loaded configuration.
    result = {"state": "new_process_observed", "executable": target["executable"],
              "main_process": new_main, "thread": args.thread, "ui_ready": False}
    if cli:
        report(state="submitting_continuation", continuation_attempted=True)
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
    # An exclusive claim prevents a repeated internal worker invocation from launching or queuing twice.
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
        if time.time() > record["created_at"] + 30:
            raise RuntimeError("Watcher preparation expired; no launch or continuation was attempted")
        args = argparse.Namespace(**record["request"])
        args.receipt = str(receipt)
        target = record["target"]
        if not original_main_running(target, inspect_desktop()):
            raise RuntimeError("original Desktop main exited before watcher readiness; no launch was attempted")
        report(state="starting", helper_pid=os.getpid(), independent=True)
        result = watch_and_relaunch(args, target, report=report)
        report(state="finished", result=result)
        return result
    except Exception as error:
        report(state="failed", error=str(error), details=getattr(error, "details", None))
        raise


def arm_restart(args: argparse.Namespace, inspect=inspect_desktop) -> dict:
    target = inspect()
    mains = main_processes(target)
    if len(mains) != 1:
        raise RuntimeError("Expected exactly one running Desktop main process")
    if not mains[0]["hwnd"]:
        raise RuntimeError("No visible Desktop main window was found; restore it before arming")
    target["main_process"] = mains[0]
    prepare_continuation(target, args)
    directory = Path(args.codex_home) / "onepersonlabs" / "desktop-restarts"
    directory.mkdir(parents=True, exist_ok=True)
    # Serialize competing arm requests; every receipt, even finished, belongs to
    # an owner who must reconcile it before another launch can be authorized.
    lock = directory / "arming.lock"
    try:
        guard = lock.open("x", encoding="utf-8")
    except FileExistsError as error:
        raise RuntimeError(f"Another arm is active or unresolved; reconcile {lock}") from error
    try:
        with guard:
            existing = list(directory.glob("*.json"))
            if existing:
                raise RuntimeError(f"Reconcile the existing restart receipt before another arm: {existing[0]}")
            receipt = directory / f"{uuid.uuid4()}.json"
            record = {"state": "prepared", "created_at": time.time(),
                      "target": target, "request": vars(args),
                      "disposal": "Remove this receipt and matching claim after the resumed owner reconciles the result. Preserve unresolved continuation state."}
            write_receipt(receipt, record)
    finally:
        lock.unlink()
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
            if current["state"] == "waiting_for_exit" and current.get("independent"):
                return {"state": "armed", "helper_pid": current["helper_pid"],
                        "receipt": str(receipt), "target": {
                            "executable": target["executable"], "main_process": target["main_process"]},
                        "exit_deadline": current["exit_deadline"]}
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
    parser.add_argument("mode", choices=["inspect", "arm", "worker", "status"])
    parser.add_argument("--thread", type=thread_id)
    parser.add_argument("--message", help="explicitly authorized continuation; queued once after launch")
    parser.add_argument("--codex-home", help="native Windows Codex home owning the destination thread")
    parser.add_argument("--timeout-seconds", type=positive_timeout, default=60)
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
