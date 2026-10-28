#!/usr/bin/env python3
"""Inspect and update the global OnePersonLabs instructions."""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
import time
import uuid
from contextlib import contextmanager

MARKERS = (
    ("onepersonlabs-instructions-version", re.compile(r"^<!-- onepersonlabs-instructions-version: ([1-9][0-9]*) -->$", re.MULTILINE)),
    ("opl-instructions-version", re.compile(r"^<!-- opl-instructions-version: ([1-9][0-9]*) -->$", re.MULTILINE)),
)
BACKUP_RETENTION_SECONDS = 7 * 24 * 60 * 60
_BACKUP_NAME = re.compile(
    r"^(?:AGENTS\.md|AGENTS\.override\.md)"
    r"(?:\.onepersonlabs-backup-[0-9]{8}-[0-9]{3,}(?:\.pending|\.expires-[0-9]+)?"
    r"|\.opl-backup-(?:[0-9a-f]{32}|[0-9]{8}-(?:[0-9]{3}|confidence-[0-9]{3}|discard-[0-9]{3}|oververification-[0-9]{3})))$"
)


def normalized(data: bytes) -> str:
    return data.decode("utf-8-sig").replace("\r\n", "\n")


def version(data: bytes, *, optional=False) -> int | None:
    text = normalized(data)
    matches = [(name, marker.findall(text)) for name, marker in MARKERS]
    marker_names = [name for name, _ in matches if name in text]
    valid = [(name, values[0]) for name, values in matches if len(values) == 1]
    if not marker_names and optional:
        return None
    if len(marker_names) != 1 or len(valid) != 1 or marker_names[0] != valid[0][0] or text.count(marker_names[0]) != 1:
        raise ValueError("expected exactly one valid instructions version marker (canonical or legacy)")
    return int(valid[0][1])


def home_path(value=None) -> Path:
    return Path(value or os.environ.get("CODEX_HOME") or Path.home() / ".codex").expanduser().resolve()


def effective_target(home: Path) -> Path:
    override = home / "AGENTS.override.md"
    if override.exists() and override.read_bytes().strip():
        return override
    return home / "AGENTS.md"


def plugin_path(value=None) -> Path:
    return Path(value or os.environ.get("PLUGIN_ROOT") or Path(__file__).resolve().parents[3]).resolve()


def snapshot(home: Path, root: Path) -> dict:
    target = effective_target(home)
    data = target.read_bytes() if target.exists() else None
    error = None
    try:
        previous = version(data, optional=True) if data is not None else None
    except (ValueError, UnicodeError) as exc:
        previous, error = None, str(exc)
    bundled = (root / "AGENTS.md").read_bytes()
    current = version(bundled)
    state = "invalid" if error else "setup" if previous is None else "current" if previous == current else "update" if previous < current else "newer"
    return {
        "home": str(home),
        "target": str(target),
        "sha256": hashlib.sha256(data).hexdigest() if data is not None else "missing",
        "user_version": previous,
        "bundled_version": current,
        "status": state,
        "error": error,
        "bundled_path": str(root / "AGENTS.md"),
        "bundled_sha256": hashlib.sha256(bundled).hexdigest(),
    }


def _backup_path(target: Path) -> Path:
    date = datetime.now().strftime("%Y%m%d")
    sequence = 1
    while True:
        base = target.with_name(f"{target.name}.onepersonlabs-backup-{date}-{sequence:03d}")
        candidate = base.with_name(base.name + ".pending")
        if (not candidate.exists() and not candidate.is_symlink()
                and not base.exists() and not list(target.parent.glob(base.name + ".expires-*"))):
            return candidate
        sequence += 1


@contextmanager
def _writer_lock(home: Path):
    """Share configure-harness's per-home write lock while pruning/applying."""
    home = Path(home).expanduser()
    if home.is_symlink():
        raise ValueError("Codex home must be a non-symlink directory")
    home = home.resolve(strict=True)
    if not home.is_dir():
        raise ValueError("Codex home must be a non-symlink directory")
    lock_root = home / "onepersonlabs" / "harness"
    lock_root.mkdir(parents=True, exist_ok=True)
    lock_path = lock_root / ".write-lock"
    try:
        descriptor = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise ValueError(f"another Codex home write owns {lock_path}; inspect before retrying") from None
    os.close(descriptor)
    try:
        yield home
    finally:
        lock_path.unlink()


def _cleanup_backups_unlocked(home: Path, *, now: float | None = None, preview: bool = False) -> dict:
    """Remove only expired backups created by this helper in this Codex home."""
    home = Path(home).expanduser().resolve(strict=True)
    cutoff = (time.time() if now is None else now) - BACKUP_RETENTION_SECONDS
    deleted, pending = [], []
    for candidate in home.iterdir():
        if not _BACKUP_NAME.fullmatch(candidate.name):
            continue
        if candidate.is_symlink() or not candidate.is_file():
            pending.append({"path": str(candidate), "reason": "not a regular backup file"})
            continue
        expiry = re.search(r"\.expires-([0-9]+)$", candidate.name)
        if expiry:
            if int(expiry.group(1)) > (time.time() if now is None else now):
                continue
            if not preview:
                candidate.unlink()
            deleted.append(str(candidate))
            continue
        if candidate.name.endswith(".pending"):
            pending.append({"path": str(candidate), "reason": "update verification or recovery is unresolved"})
            continue
        # Legacy backups expire only when the active target proves a later
        # version was installed, using the original file timestamp.
        target = home / re.split(r"\.(?:onepersonlabs-backup|opl-backup)-", candidate.name, maxsplit=1)[0]
        try:
            saved_version = version(candidate.read_bytes(), optional=True)
            active_version = version(target.read_bytes()) if target.is_file() and not target.is_symlink() else None
        except (OSError, ValueError, UnicodeError):
            saved_version = active_version = None
        expired = (saved_version is not None and active_version is not None
                   and active_version > saved_version and candidate.stat().st_mtime <= cutoff)
        if expired:
            if not preview:
                candidate.unlink()
            deleted.append(str(candidate))
        else:
            pending.append({"path": str(candidate), "reason": "legacy backup lacks proof of a later verified replacement"})
    return {"deleted": [] if preview else deleted, "would_delete": deleted if preview else [], "pending": pending}


def cleanup_backups(home: Path, *, now: float | None = None, preview: bool = False) -> dict:
    with _writer_lock(home) as resolved:
        return _cleanup_backups_unlocked(resolved, now=now, preview=preview)


def _apply_installed(home: Path, root: Path, expected: str, expected_target: str, expected_bundled: str) -> dict:
    before = snapshot(home, root)
    if before["error"]:
        raise ValueError(f"cannot replace instructions with an invalid version: {before['error']}")
    target = Path(before["target"])
    if (before["sha256"] != expected or target != Path(expected_target).resolve()
            or before["bundled_sha256"] != expected_bundled):
        raise ValueError("user instructions changed after inspection; inspect again before updating")
    if target.is_symlink():
        raise ValueError("instruction target is a symlink; reconcile its destination explicitly")

    source = root / "AGENTS.md"
    replacement = source.read_bytes()
    installed_version = version(replacement)
    if installed_version != before["bundled_version"]:
        raise ValueError("installed OnePersonLabs instructions have an inconsistent version")
    if before["user_version"] is not None and before["user_version"] > installed_version:
        raise ValueError("refusing to downgrade a newer user instruction version")
    if source.resolve() == target.resolve():
        raise ValueError("installed instructions and effective target resolve to the same file")

    cleanup = _cleanup_backups_unlocked(home)

    original = target.read_bytes() if target.exists() else None
    if original == replacement:
        return {"target": str(target), "changed": False, "backup": None}

    home.mkdir(parents=True, exist_ok=True)
    backup = None
    temporary = None
    try:
        if original is not None:
            while True:
                backup = _backup_path(target)
                try:
                    with backup.open("xb") as stream:
                        stream.write(original)
                        stream.flush()
                        os.fsync(stream.fileno())
                    break
                except FileExistsError:
                    continue
                except OSError:
                    backup.unlink(missing_ok=True)
                    raise
            backup.chmod(stat.S_IMODE(target.stat().st_mode))

        with tempfile.NamedTemporaryFile(dir=home, prefix=".onepersonlabs-instructions-", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(replacement)
            stream.flush()
            os.fsync(stream.fileno())
        if original is not None:
            temporary.chmod(stat.S_IMODE(target.stat().st_mode))

        final = snapshot(home, root)
        if (final["target"] != str(target) or final["sha256"] != expected
                or final["bundled_sha256"] != expected_bundled):
            raise ValueError("instructions changed during application; update stopped")
        os.replace(temporary, target)
        temporary = None
        if target.read_bytes() != replacement:
            raise OSError("replacement readback did not match; inspect the retained backup")
        if backup is not None:
            verified_at = time.time()
            expires_at = int(verified_at + BACKUP_RETENTION_SECONDS)
            verified_backup = backup.with_name(
                backup.name.removesuffix(".pending") + f".expires-{expires_at}"
            )
            backup.rename(verified_backup)
            backup = verified_backup
    except BaseException:
        # A failed write with the original still present needs no recovery copy.
        # Keep the pending backup when the target changed and recovery may depend on it.
        if (backup is not None and original is not None and target.is_file()
                and hashlib.sha256(target.read_bytes()).hexdigest() == hashlib.sha256(original).hexdigest()):
            backup.unlink(missing_ok=True)
        raise
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)

    return {
        "target": str(target),
        "changed": True,
        "backup": str(backup) if backup else None,
        "version": installed_version,
        "sha256": hashlib.sha256(replacement).hexdigest(),
        "cleanup": cleanup,
    }


def apply_installed(home: Path, root: Path, expected: str, expected_target: str, expected_bundled: str) -> dict:
    with _writer_lock(home) as resolved:
        return _apply_installed(resolved, root, expected, expected_target, expected_bundled)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("inspect", "apply", "cleanup"):
        child = commands.add_parser(command)
        child.add_argument("--home")
        child.add_argument("--plugin-root")
        if command == "apply":
            child.add_argument("--expected-sha256", required=True)
            child.add_argument("--expected-target", required=True)
            child.add_argument("--expected-bundled-sha256", required=True)
        if command == "cleanup":
            child.add_argument("--preview", action="store_true")
    args = parser.parse_args()
    home = home_path(args.home)
    root = plugin_path(args.plugin_root)
    if args.command == "inspect":
        result = snapshot(home, root)
    elif args.command == "cleanup":
        result = cleanup_backups(home, preview=args.preview)
    else:
        result = apply_installed(home, root, args.expected_sha256, args.expected_target,
                                 args.expected_bundled_sha256)
    print(json.dumps(result))


if __name__ == "__main__":
    try:
        main()
    except (OSError, UnicodeError, ValueError) as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        sys.exit(1)
