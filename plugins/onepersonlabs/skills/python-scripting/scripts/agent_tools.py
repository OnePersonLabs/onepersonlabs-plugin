#!/usr/bin/env python3
"""Discover, run, and retire disposable Python tools in the active Codex home."""

from __future__ import annotations

import argparse
import errno
import io
import json
import os
from pathlib import Path
import re
import runpy
import stat
import sys
import time
import tokenize


DEFAULTS = {
    "hot_age_days": 60,
    "hot_count": 100,
    "cold_age_days": 180,
    "cold_count": 400,
    "temp_age_days": 14,
}
TIERS = ("hot", "cold", "temp")
HEADER_BYTES = 8192
FIND_BYTES = 16 * 1024
TOOL_NAME = re.compile(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*\.py")
# One descriptor per process matters: POSIX record locks are lost when ANY
# descriptor for the same inode closes. Keep this descriptor until OS exit;
# a runpy finally block would release the execution guard before shutdown work.
_LOCK = None


class ToolError(Exception):
    """A store operation could not safely complete."""


def inspect_path(path: Path, directory: bool = False):
    """Reject redirection, including Windows junctions and other reparse points."""
    try:
        info = path.lstat()
    except FileNotFoundError:
        return None
    if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
        raise ToolError(f"redirected path is not allowed: {path}")
    expected = stat.S_ISDIR if directory else stat.S_ISREG
    if not expected(info.st_mode):
        raise ToolError(f"expected {'directory' if directory else 'regular file'}: {path}")
    return info


def identity(info):
    return info.st_dev, info.st_ino


def unchanged(path: Path, previous):
    current = inspect_path(path)
    if current is None or (
        identity(current), current.st_mtime_ns, current.st_size, current.st_nlink
    ) != (identity(previous), previous.st_mtime_ns, previous.st_size, previous.st_nlink):
        raise ToolError(f"file changed during operation; preserved: {path}")
    return current


def nofollow_options(operation):
    # Windows Python can lack follow_symlinks support for utime and link. On
    # that platform use the native regular-path operation after the caller's
    # lstat/reparse/identity checks. This is cooperative safety, not protection
    # against an adversary replacing the path between validation and operation.
    return {"follow_symlinks": False} if operation in os.supports_follow_symlinks else {}


class Store:
    def __init__(self):
        self.home = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex").expanduser().resolve()
        self.root = self.home / "agent-tools"

    def validate(self):
        exists = inspect_path(self.root, directory=True) is not None
        if exists:
            for tier in TIERS:
                inspect_path(self.root / tier, directory=True)
            inspect_path(self.root / ".lock")
        return exists

    def config(self):
        values = dict(DEFAULTS)
        if not self.validate():
            return values
        path = self.root / "config.json"
        before = inspect_path(path)
        if before is None:
            return values
        try:
            with path.open("r", encoding="utf-8") as stream:
                supplied = json.load(stream)
        except (ValueError, UnicodeError) as error:
            raise ToolError(f"invalid config.json: {error}") from error
        unchanged(path, before)
        if not isinstance(supplied, dict):
            raise ToolError("config.json must contain an object")
        unknown = supplied.keys() - DEFAULTS.keys()
        if unknown:
            raise ToolError(f"unknown config.json keys: {', '.join(sorted(unknown))}")
        for key, value in supplied.items():
            if type(value) is not int or value < 0:
                raise ToolError(f"config.json {key} must be a finite nonnegative integer")
        values.update(supplied)
        return values

    def create(self):
        # Validate the whole optional configuration before even creating .lock.
        self.config()
        self.home.mkdir(parents=True, exist_ok=True)
        self.root.mkdir(exist_ok=True)
        self.validate()
        for tier in TIERS:
            (self.root / tier).mkdir(exist_ok=True)
        self.validate()

    def entries(self, tier, warnings):
        self.validate()
        folder = self.root / tier
        if inspect_path(folder, directory=True) is None:
            return []
        entries = []
        for path in folder.iterdir():
            if path.suffix != ".py":
                continue
            try:
                info = inspect_path(path)
                if info is not None:
                    entries.append((path, info))
            except ToolError as error:
                warnings.append(str(error))
        return sorted(entries, key=lambda item: (item[1].st_mtime_ns, item[0].name))


class StoreLock:
    def __init__(self, store):
        global _LOCK
        if _LOCK is not None:
            raise ToolError("manager accepts one operation per process")
        store.validate()
        path = store.root / ".lock"
        before = inspect_path(path)
        flags = os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_BINARY", 0)
        self.fd = os.open(path, flags, 0o600)
        # Retain even on failure: never reopen this inode in this process.
        _LOCK = self
        after = inspect_path(path)
        opened = os.fstat(self.fd)
        if after is None or identity(after) != identity(opened) or (before and identity(before) != identity(after)):
            raise ToolError("lock path changed while opening")
        if opened.st_nlink != 1:
            raise ToolError(".lock must have exactly one filesystem link")
        self.held = set()
        if os.name == "nt":
            self._windows_setup()

    def _windows_setup(self):
        import ctypes
        from ctypes import wintypes
        import msvcrt

        class OVERLAPPED(ctypes.Structure):
            _fields_ = [("Internal", ctypes.c_size_t), ("InternalHigh", ctypes.c_size_t),
                        ("Offset", wintypes.DWORD), ("OffsetHigh", wintypes.DWORD),
                        ("hEvent", wintypes.HANDLE)]

        self.ctypes = ctypes
        self.overlapped = OVERLAPPED
        self.handle = wintypes.HANDLE(msvcrt.get_osfhandle(self.fd))
        self.kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        self.kernel.LockFileEx.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.DWORD,
                                         wintypes.DWORD, wintypes.DWORD, ctypes.POINTER(OVERLAPPED)]
        self.kernel.LockFileEx.restype = wintypes.BOOL
        self.kernel.UnlockFileEx.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.DWORD,
                                           wintypes.DWORD, ctypes.POINTER(OVERLAPPED)]
        self.kernel.UnlockFileEx.restype = wintypes.BOOL

    def acquire(self, byte, shared=False, blocking=False):
        if os.name == "nt":
            overlapped = self.overlapped(Offset=byte)
            flags = (0 if shared else 2) | (0 if blocking else 1)
            if not self.kernel.LockFileEx(self.handle, flags, 0, 1, 0, self.ctypes.byref(overlapped)):
                code = self.ctypes.get_last_error()
                if not blocking and code in (32, 33):
                    return False
                raise self.ctypes.WinError(code)
        else:
            import fcntl
            flags = fcntl.LOCK_SH if shared else fcntl.LOCK_EX
            if not blocking:
                flags |= fcntl.LOCK_NB
            try:
                fcntl.lockf(self.fd, flags, 1, byte, os.SEEK_SET)
            except OSError as error:
                if not blocking and error.errno in (errno.EACCES, errno.EAGAIN):
                    return False
                raise
        self.held.add(byte)
        return True

    def release(self, byte):
        if byte not in self.held:
            return
        if os.name == "nt":
            overlapped = self.overlapped(Offset=byte)
            if not self.kernel.UnlockFileEx(self.handle, 0, 1, 0, self.ctypes.byref(overlapped)):
                raise self.ctypes.WinError(self.ctypes.get_last_error())
        else:
            import fcntl
            fcntl.lockf(self.fd, fcntl.LOCK_UN, 1, byte, os.SEEK_SET)
        self.held.remove(byte)


def header(path, info):
    with path.open("rb") as stream:
        content = stream.read(HEADER_BYTES + 1)
    prefix = content[:HEADER_BYTES]
    unchanged(path, info)
    try:
        encoding, _ = tokenize.detect_encoding(io.BytesIO(prefix).readline)
        # Decode only required header lines. A bounded read can end inside a
        # multibyte character in later code; that must not invalidate metadata.
        raw = prefix.removeprefix(b"\xef\xbb\xbf").splitlines(keepends=True)
        index = 1 if raw and raw[0].startswith(b"#!") else 0
        if index < len(raw) and re.match(rb"^#.*coding[:=]\s*[-\w.]+", raw[index]):
            index += 1
        if len(raw) <= index + 1:
            raise ToolError(f"invalid header in {path.name}: missing metadata")
        if len(content) > HEADER_BYTES and index + 1 == len(raw) - 1 and not raw[index + 1].endswith((b"\n", b"\r")):
            raise ToolError(f"invalid header in {path.name}: metadata exceeds bounded prefix")
        lines = b"".join(raw[:index + 2]).decode(encoding, errors="strict").splitlines()
    except (SyntaxError, LookupError, UnicodeError) as error:
        raise ToolError(f"invalid header in {path.name}: {error}") from error
    if len(lines) <= index + 1 or not lines[index].startswith("# Description: ") or not lines[index + 1].startswith("# Keywords: "):
        raise ToolError(f"invalid header in {path.name}: expected adjacent Description and Keywords comments")
    description = lines[index][len("# Description: "):].strip()
    keywords = [part.strip() for part in lines[index + 1][len("# Keywords: "):].split(",")]
    if not description or not all(keywords):
        raise ToolError(f"invalid header in {path.name}: description and keywords must be nonempty")
    return description, keywords


def eligible(store, path, info):
    """Use the same selection rules for discovery and execution."""
    if not TOOL_NAME.fullmatch(path.name):
        raise ToolError(f"ineligible filename; use snake_case.py: {path.name}")
    paired = False
    if path.parent.name in ("hot", "cold"):
        paired = reconcile_pair(store, store.root / "hot" / path.name,
                                store.root / "cold" / path.name, dry_run=True)
    if info.st_nlink != 1 and not (paired and info.st_nlink == 2):
        raise ToolError(f"unexpected filesystem links; preserved: {path}")
    return paired


def bounded_find(matches, warnings, limit):
    """Bound the whole serialized response, including escapes and diagnostics."""
    result = {"matches": [], "omitted_matches": len(matches), "metadata_truncated": 0,
              "warnings": [], "omitted_warnings": len(warnings), "warnings_truncated": 0}

    def fits():
        # Reserve CRLF as well as the exact JSON form printed by main().
        return len(json.dumps(result, ensure_ascii=True).encode("utf-8")) + 2 <= FIND_BYTES

    for original in matches[:limit]:
        candidate = dict(original)
        added = False
        for text_limit, keyword_count, keyword_limit in ((512, 8, 64), (128, 3, 32), (48, 1, 24)):
            candidate["description"] = original["description"][:text_limit]
            candidate["keywords"] = [word[:keyword_limit] for word in original["keywords"][:keyword_count]]
            shortened = candidate != original
            result["matches"].append(candidate)
            result["omitted_matches"] -= 1
            result["metadata_truncated"] += int(shortened)
            if fits():
                added = True
                break
            result["matches"].pop()
            result["omitted_matches"] += 1
            result["metadata_truncated"] -= int(shortened)
        if not added:
            continue
    for original in warnings:
        warning = original[:256]
        shortened = warning != original
        result["warnings"].append(warning)
        result["omitted_warnings"] -= 1
        result["warnings_truncated"] += int(shortened)
        if not fits():
            result["warnings"].pop()
            result["omitted_warnings"] += 1
            result["warnings_truncated"] -= int(shortened)
    return result


def find(store, terms, limit):
    store.config()
    warnings, matches = [], []
    for tier in ("hot", "cold"):
        for path, info in sorted(store.entries(tier, warnings), key=lambda item: item[0].name):
            try:
                paired = eligible(store, path, info)
                if paired and tier == "cold":
                    continue
                description, keywords = header(path, info)
            except ToolError as error:
                warnings.append(str(error))
                continue
            text = " ".join((path.name, description, *keywords)).casefold()
            if all(term.casefold() in text for term in terms):
                matches.append({"tier": tier, "name": path.name, "description": description,
                                "keywords": keywords, "path": str(path)})
    return bounded_find(matches, warnings, limit)


def reconcile_pair(store, hot, cold, dry_run=False):
    hot_info, cold_info = inspect_path(hot), inspect_path(cold)
    if hot_info and cold_info:
        if identity(hot_info) == identity(cold_info) and hot_info.st_nlink == cold_info.st_nlink == 2:
            if not dry_run:
                store.validate()
                unchanged(hot, hot_info)
                unchanged(cold, cold_info)
                cold.unlink()
            return True
        raise ToolError(f"conflicting basename; both files preserved: {hot.name}")
    return False


def move(store, source, info, target):
    store.validate()
    unchanged(source, info)
    if inspect_path(target) is not None:
        raise ToolError(f"destination exists; both files preserved: {target.name}")
    if info.st_nlink != 1:
        raise ToolError(f"unexpected filesystem links; preserved: {source}")
    # Refresh BEFORE the no-clobber link/unlink move. An interrupted move leaves
    # an identifiable two-link pair with the destination's full retention life.
    os.utime(source, None, **nofollow_options(os.utime))
    refreshed = inspect_path(source)
    if refreshed is None or identity(refreshed) != identity(info):
        raise ToolError(f"file changed before move; preserved: {source}")
    unchanged(source, refreshed)
    try:
        os.link(source, target, **nofollow_options(os.link))
    except OSError as error:
        raise ToolError(f"no-clobber move failed; source preserved: {source}: {error}") from error
    linked = inspect_path(target)
    current = inspect_path(source)
    if not linked or not current or identity(linked) != identity(refreshed) or identity(current) != identity(refreshed) or current.st_nlink != 2:
        raise ToolError(f"move interrupted by filesystem changes; inspect both paths: {source}, {target}")
    store.validate()
    unchanged(source, current)
    unchanged(target, linked)
    source.unlink()


def maintain(store, dry_run=False):
    config = store.config()
    if not store.validate():
        return {"actions": [], "warnings": []}
    if not dry_run:
        lock = StoreLock(store)
        if not lock.acquire(0):
            return {"skipped": "another store operation is active"}
        if not lock.acquire(1):
            lock.release(0)
            return {"skipped": "a tool is running"}
        config = store.config()
    warnings, actions = [], []
    reconciled = set()
    conflicts = set()
    demoted = 0
    # Only exact same-inode interrupted moves are recoverable automatically.
    for cold, _info in store.entries("cold", warnings):
        hot = store.root / "hot" / cold.name
        try:
            if reconcile_pair(store, hot, cold, dry_run):
                actions.append({"action": "reconcile", "name": cold.name})
                reconciled.add(cold.name)
        except ToolError as error:
            warnings.append(str(error))
            conflicts.add(cold.name)
    now = time.time()
    for tier in TIERS:
        entries = store.entries(tier, warnings)
        if dry_run and tier == "cold":
            entries = [(path, info) for path, info in entries if path.name not in reconciled]
        virtual_count = demoted if dry_run and tier == "cold" else 0
        excess = max(0, len(entries) + virtual_count - config.get(tier + "_count", 0))
        for path, info in entries:
            if tier != "temp" and excess == 0:
                break
            if now - info.st_mtime < config[tier + "_age_days"] * 86400:
                continue
            if tier != "temp" and path.name in conflicts:
                continue
            action = "demote" if tier == "hot" else "delete"
            try:
                if info.st_nlink != 1 and not (dry_run and path.name in reconciled and info.st_nlink == 2):
                    raise ToolError(f"unexpected filesystem links; preserved: {path}")
                if tier == "hot":
                    target = store.root / "cold" / path.name
                    if inspect_path(target) is not None and not (dry_run and path.name in reconciled):
                        raise ToolError(f"destination exists; both files preserved: {path.name}")
                    if not dry_run:
                        move(store, path, info, target)
                    demoted += 1
                elif not dry_run:
                    store.validate()
                    unchanged(path, info)
                    if info.st_nlink != 1:
                        raise ToolError(f"unexpected filesystem links; preserved: {path}")
                    path.unlink()
                actions.append({"action": action, "tier": tier, "name": path.name})
                excess -= 1
            except (ToolError, OSError) as error:
                warnings.append(str(error))
    return {"actions": actions, "warnings": warnings, "dry_run": dry_run}


def run(store, name, temporary, arguments):
    if Path(name).name != name or not TOOL_NAME.fullmatch(name):
        raise ToolError("NAME must be an exact snake_case.py basename without path components")
    store.config()
    if not store.validate():
        raise ToolError(f"tool store does not exist: {store.root}")
    lock = StoreLock(store)
    lock.acquire(0, blocking=True)
    lock.acquire(1, shared=True, blocking=True)
    store.config()
    if temporary:
        path = store.root / "temp" / name
    else:
        path, cold = store.root / "hot" / name, store.root / "cold" / name
        selected = path if inspect_path(path) is not None else cold
        selected_info = inspect_path(selected)
        if selected_info is None:
            raise ToolError(f"tool not found: {name}")
        eligible(store, selected, selected_info)
        if reconcile_pair(store, path, cold):
            print(f"Reconciled interrupted move for {name}; retained hot copy.", file=sys.stderr)
        if inspect_path(path) is None and inspect_path(cold) is not None:
            info = inspect_path(cold)
            header(cold, info)
            move(store, cold, info, path)
    info = inspect_path(path)
    if info is None:
        raise ToolError(f"tool not found: {name}")
    eligible(store, path, info)
    header(path, info)
    store.validate()
    unchanged(path, info)
    if info.st_nlink != 1:
        raise ToolError(f"unexpected filesystem links; preserved: {path}")
    os.utime(path, None, **nofollow_options(os.utime))
    lock.release(0)
    sys.argv = [str(path), *arguments]
    sys.path.insert(0, str(path.parent))
    # cwd and stdio are inherited. The OS releases byte 1 at process exit,
    # including SystemExit, exceptions, and interpreter shutdown callbacks.
    runpy.run_path(str(path), run_name="__main__")


def hook(store):
    try:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict) or payload.get("hook_event_name") != "SessionStart":
            raise ToolError("expected a SessionStart hook object")
        if "source" in payload and payload["source"] not in ("startup", "resume", "clear", "compact"):
            raise ToolError("unsupported SessionStart source")
        result = maintain(store)
        if result.get("warnings"):
            messages = result["warnings"]
            suffix = f"; {len(messages) - 5} more failures" if len(messages) > 5 else ""
            return {"systemMessage": "Agent-tool cleanup: " + "; ".join(message[:500] for message in messages[:5]) + suffix}
        return {}
    except (ToolError, OSError, ValueError) as error:
        return {"systemMessage": f"Agent-tool cleanup failed: {error}"}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    paths = commands.add_parser("paths", help="show storage paths; optionally create tiers")
    paths.add_argument("--create", action="store_true")
    search = commands.add_parser("find", help="match names and bounded metadata headers")
    search.add_argument("terms", nargs="*")
    search.add_argument("--limit", type=int, default=20)
    execute = commands.add_parser("run", help="run NAME [--temp] -- script arguments")
    execute.add_argument("name")
    execute.add_argument("--temp", action="store_true")
    cleanup = commands.add_parser("maintain", help="apply retention; dry-run is an advisory snapshot")
    cleanup.add_argument("--dry-run", action="store_true")
    commands.add_parser("hook", help="read native SessionStart JSON from stdin")
    arguments = list(sys.argv[1:] if argv is None else argv)
    script_arguments = []
    if arguments[:1] == ["run"] and "--" in arguments:
        separator = arguments.index("--")
        arguments, script_arguments = arguments[:separator], arguments[separator + 1:]
    args = parser.parse_args(arguments)
    store = Store()
    try:
        if args.command == "hook":
            result = hook(store)
        elif args.command == "paths":
            store.config()
            if args.create:
                store.create()
            result = {"root": str(store.root), **{tier: str(store.root / tier) for tier in TIERS}}
        elif args.command == "find":
            if args.limit < 0:
                raise ToolError("--limit must be nonnegative")
            result = find(store, args.terms, args.limit)
        elif args.command == "maintain":
            result = maintain(store, args.dry_run)
        else:
            run(store, args.name, args.temp, script_arguments)
            return 0
        print(json.dumps(result, ensure_ascii=True))
        return 1 if args.command == "maintain" and result.get("warnings") else 0
    except (ToolError, OSError) as error:
        print(f"agent-tools: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
