"""Invoke the installed Desktop's native Ctrl+Q Quit accelerator on Windows."""

from __future__ import annotations

import ctypes
from ctypes import wintypes
import ntpath
import os


CONTROL = 0x11
Q = 0x51
QUIT_KEYS = [(CONTROL, False), (Q, False), (Q, True), (CONTROL, True)]
FILETIME_TO_DATETIME_TICKS = 504911232000000000


class QuitInputError(RuntimeError):
    """A refused or uncertain input operation, with metadata for the caller."""

    def __init__(self, message: str, details: dict):
        super().__init__(message)
        self.details = details


class _KEYBDINPUT(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_uint16), ("wScan", ctypes.c_uint16),
                ("dwFlags", ctypes.c_uint32), ("time", ctypes.c_uint32),
                ("dwExtraInfo", ctypes.c_size_t)]


class _MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_int32), ("dy", ctypes.c_int32),
                ("mouseData", ctypes.c_uint32), ("dwFlags", ctypes.c_uint32),
                ("time", ctypes.c_uint32), ("dwExtraInfo", ctypes.c_size_t)]


class _INPUTUNION(ctypes.Union):
    _fields_ = [("ki", _KEYBDINPUT), ("mi", _MOUSEINPUT)]


class _INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.c_uint32), ("data", _INPUTUNION)]


class _WindowsApi:
    def __init__(self):
        if os.name != "nt":
            raise RuntimeError("Desktop Quit input is supported only on native Windows")
        self.user = ctypes.WinDLL("user32", use_last_error=True)
        self.kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        self.callback_type = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
        signatures = {
            "EnumWindows": ([self.callback_type, wintypes.LPARAM], wintypes.BOOL),
            "IsWindowVisible": ([wintypes.HWND], wintypes.BOOL),
            "IsWindowEnabled": ([wintypes.HWND], wintypes.BOOL),
            "IsIconic": ([wintypes.HWND], wintypes.BOOL),
            "GetWindow": ([wintypes.HWND, wintypes.UINT], wintypes.HWND),
            "GetWindowThreadProcessId": ([wintypes.HWND, ctypes.POINTER(wintypes.DWORD)], wintypes.DWORD),
            "GetForegroundWindow": ([], wintypes.HWND),
            "SetForegroundWindow": ([wintypes.HWND], wintypes.BOOL),
            "ShowWindow": ([wintypes.HWND, ctypes.c_int], wintypes.BOOL),
            "GetAsyncKeyState": ([ctypes.c_int], ctypes.c_short),
            "SendInput": ([wintypes.UINT, ctypes.POINTER(_INPUT), ctypes.c_int], wintypes.UINT),
        }
        for name, (arguments, result) in signatures.items():
            function = getattr(self.user, name)
            function.argtypes, function.restype = arguments, result
        self.kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        self.kernel.OpenProcess.restype = wintypes.HANDLE
        self.kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        self.kernel.CloseHandle.restype = wintypes.BOOL
        self.kernel.QueryFullProcessImageNameW.argtypes = [
            wintypes.HANDLE, wintypes.DWORD, wintypes.LPWSTR, ctypes.POINTER(wintypes.DWORD)]
        self.kernel.QueryFullProcessImageNameW.restype = wintypes.BOOL
        self.kernel.GetProcessTimes.argtypes = [wintypes.HANDLE, *[ctypes.POINTER(wintypes.FILETIME)] * 4]
        self.kernel.GetProcessTimes.restype = wintypes.BOOL

    def windows(self) -> list[int]:
        handles = []

        @self.callback_type
        def visit(hwnd, _):
            # Owned windows include modal dialogs; never target their disabled parent.
            if (self.user.IsWindowVisible(hwnd) and self.user.IsWindowEnabled(hwnd)
                    and not self.user.GetWindow(hwnd, 4)):  # GW_OWNER
                handles.append(int(hwnd))
            return True

        if not self.user.EnumWindows(visit, 0):
            raise ctypes.WinError(ctypes.get_last_error())
        return handles

    def window_pid(self, hwnd: int) -> int:
        pid = wintypes.DWORD()
        if not self.user.GetWindowThreadProcessId(hwnd, ctypes.byref(pid)):
            raise ctypes.WinError(ctypes.get_last_error())
        return pid.value

    def process_identity(self, pid: int) -> dict:
        handle = self.kernel.OpenProcess(0x1000, False, pid)  # PROCESS_QUERY_LIMITED_INFORMATION
        if not handle:
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            buffer = ctypes.create_unicode_buffer(32768)
            length = wintypes.DWORD(len(buffer))
            if not self.kernel.QueryFullProcessImageNameW(handle, 0, buffer, ctypes.byref(length)):
                raise ctypes.WinError(ctypes.get_last_error())
            created, exited, kernel, user = (wintypes.FILETIME() for _ in range(4))
            if not self.kernel.GetProcessTimes(handle, ctypes.byref(created), ctypes.byref(exited),
                                               ctypes.byref(kernel), ctypes.byref(user)):
                raise ctypes.WinError(ctypes.get_last_error())
            ticks = (created.dwHighDateTime << 32) | created.dwLowDateTime
            return {"executable": buffer.value, "started": str(ticks + FILETIME_TO_DATETIME_TICKS)}
        finally:
            self.kernel.CloseHandle(handle)

    def foreground(self) -> int:
        return int(self.user.GetForegroundWindow() or 0)

    def activate(self, hwnd: int) -> bool:
        if self.user.IsIconic(hwnd):
            self.user.ShowWindow(hwnd, 9)  # SW_RESTORE
        return bool(self.user.SetForegroundWindow(hwnd))

    def held_keys(self) -> list[int]:
        return [key for key in range(1, 256) if self.user.GetAsyncKeyState(key) & 0x8000]

    def send(self, keys: list[tuple[int, bool]]) -> int:
        inputs = (_INPUT * len(keys))()
        for item, (key, released) in zip(inputs, keys):
            item.type = 1  # INPUT_KEYBOARD
            item.data.ki = _KEYBDINPUT(key, 0, 2 if released else 0, 0, 0)
        return int(self.user.SendInput(len(inputs), inputs, ctypes.sizeof(_INPUT)))


def _path(value: str) -> str:
    return ntpath.normcase(ntpath.normpath(value))


def _verify(api, target: dict, hwnd: int, pid: int, started: str) -> None:
    if api.window_pid(hwnd) != pid:
        raise RuntimeError("Desktop window owner changed; no Quit input was sent")
    identity = api.process_identity(pid)
    if (str(identity["started"]) != started
            or _path(identity["executable"]) != _path(target["executable"])):
        raise RuntimeError("Desktop process identity changed; no Quit input was sent")


def _select(api, target: dict) -> dict:
    expected = {int(item["pid"]): str(item["started"]) for item in target["processes"]}
    candidates = []
    for hwnd in api.windows():
        pid = api.window_pid(hwnd)
        if pid not in expected:
            continue
        _verify(api, target, hwnd, pid, expected[pid])
        candidates.append({"hwnd": hwnd, "pid": pid, "started": expected[pid]})
    foreground = api.foreground()
    focused = [item for item in candidates if item["hwnd"] == foreground]
    if focused:
        return focused[0]
    if len(candidates) == 1:
        return candidates[0]
    if not candidates:
        raise RuntimeError("No enabled visible Desktop main window was found; restore it before restarting")
    raise RuntimeError("Multiple Desktop windows are visible; focus the intended Desktop window before restarting")


def inspect_quit_target(target: dict) -> dict:
    """Read the target window and process identity without focus or input changes."""
    return _select(_WindowsApi(), target)


def request_quit(target: dict) -> dict:
    """Submit native Quit once; the caller must separately verify app process exit."""
    api = _WindowsApi()
    selected = _select(api, target)
    hwnd, pid, started = selected["hwnd"], selected["pid"], selected["started"]
    if api.held_keys():
        raise RuntimeError("Keys or mouse buttons are held; release them before restarting Desktop")
    if api.foreground() != hwnd and not api.activate(hwnd):
        raise RuntimeError("Windows refused Desktop foreground activation; focus Desktop before retrying")
    _verify(api, target, hwnd, pid, started)
    if api.held_keys():
        raise RuntimeError("Keyboard state changed before Quit; release held keys before restarting Desktop")
    if api.foreground() != hwnd:
        raise RuntimeError("Desktop lost foreground focus; no Quit input was sent")
    sent = api.send(QUIT_KEYS)
    result = {"state": "quit_input_sent", **selected, "events_sent": sent,
              "events_expected": len(QUIT_KEYS), "exit_confirmed": False}
    if sent != len(QUIT_KEYS):
        held = []
        for key, released in QUIT_KEYS[:max(0, min(sent, len(QUIT_KEYS)))]:
            if released:
                held.remove(key)
            else:
                held.append(key)
        cleanup = [(key, True) for key in reversed(held)]
        result.update(state="quit_input_uncertain", cleanup_expected=len(cleanup), cleanup_sent=0)
        try:
            result["cleanup_sent"] = api.send(cleanup) if cleanup else 0
        except OSError as error:
            result["cleanup_error"] = str(error)
        raise QuitInputError(
            f"Quit input delivery is uncertain ({sent}/4 events); no retry was attempted", result)
    return result
