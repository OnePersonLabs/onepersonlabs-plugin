import importlib.util
import hashlib
import json
import os
import re
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location("instructions", ROOT / "plugins/onepersonlabs/skills/update-instructions/scripts/instructions.py")
instructions = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(instructions)


def content(number, text="Use my browser."):
    return f"<!-- onepersonlabs-instructions-version: {number} -->\n\n{text}\n".encode()


def legacy_content(number, text="Use my browser."):
    return f"<!-- opl-instructions-version: {number} -->\n\n{text}\n".encode()


class InstructionUpdates(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="OnePersonLabs é ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.home = self.root / "home"
        self.plugin = self.root / "plugin"
        self.home.mkdir()
        self.plugin.mkdir()
        (self.plugin / "AGENTS.md").write_bytes(content(3, "Installed OnePersonLabs defaults."))
        self.target = self.home / "AGENTS.md"

    def apply(self, expected):
        bundled = (self.plugin / "AGENTS.md").read_bytes()
        return instructions.apply_installed(self.home, self.plugin, expected, str(self.target),
                                            hashlib.sha256(bundled).hexdigest())

    def test_versions_and_override(self):
        for data, state in [(content(3), "current"), (content(1), "update"), (content(4), "newer"),
                            (legacy_content(2), "update"), (b"Personal", "setup"),
                            (content(1) + content(2), "invalid"),
                            (content(1) + legacy_content(2), "invalid")]:
            self.target.write_bytes(data)
            self.assertEqual(instructions.snapshot(self.home, self.plugin)["status"], state)
        override = self.home / "AGENTS.override.md"
        override.write_bytes(content(3))
        self.assertEqual(instructions.snapshot(self.home, self.plugin)["target"], str(override))
        override.write_bytes(b"")
        self.assertEqual(instructions.effective_target(self.home), self.target)

    def test_legacy_marker_migrates_without_downgrade(self):
        original = legacy_content(2, "Legacy instructions.")
        self.target.write_bytes(original)
        inspected = instructions.snapshot(self.home, self.plugin)
        self.assertEqual(inspected["status"], "update")
        result = self.apply(hashlib.sha256(original).hexdigest())
        self.assertTrue(result["changed"])
        self.assertEqual(self.target.read_bytes(), (self.plugin / "AGENTS.md").read_bytes())
        self.assertIn(b"onepersonlabs-instructions-version: 3", self.target.read_bytes())
        self.assertNotIn(b"opl-instructions-version", self.target.read_bytes())
        backups_before_newer_check = sorted(self.home.glob("AGENTS.md.onepersonlabs-backup-*"))

        newer = legacy_content(999, "Newer legacy instructions.")
        self.target.write_bytes(newer)
        inspected = instructions.snapshot(self.home, self.plugin)
        self.assertEqual(inspected["status"], "newer")
        with self.assertRaisesRegex(ValueError, "downgrade"):
            self.apply(hashlib.sha256(newer).hexdigest())
        self.assertEqual(self.target.read_bytes(), newer)
        self.assertEqual(sorted(self.home.glob("AGENTS.md.onepersonlabs-backup-*")), backups_before_newer_check)

    def test_backup_is_exact_and_same_content_is_noop(self):
        original = b"\xef\xbb\xbf" + content(1).replace(b"\n", b"\r\n")
        self.target.write_bytes(original)
        result = self.apply(hashlib.sha256(original).hexdigest())
        self.assertEqual(Path(result["backup"]).read_bytes(), original)
        self.assertRegex(Path(result["backup"]).name, r"^AGENTS\.md\.onepersonlabs-backup-\d{8}-001\.expires-\d+$")
        self.assertEqual(self.target.read_bytes(), (self.plugin / "AGENTS.md").read_bytes())
        again = self.apply(result["sha256"])
        self.assertFalse(again["changed"])

    def test_ambiguous_version_refuses_replacement_and_keeps_original(self):
        original = legacy_content(999, 'Newer legacy instructions.') + content(3)
        self.target.write_bytes(original)
        with self.assertRaisesRegex(ValueError, 'invalid version'):
            self.apply(hashlib.sha256(original).hexdigest())
        self.assertEqual(self.target.read_bytes(), original)
        self.assertEqual(list(self.home.glob('AGENTS.md.onepersonlabs-backup-*')), [])

    def test_dated_backup_sequence_never_overwrites_existing_backup(self):
        original = content(1, "First version")
        self.target.write_bytes(original)
        first = self.apply(hashlib.sha256(original).hexdigest())
        first_backup = Path(first["backup"])
        self.assertTrue(re.fullmatch(r"AGENTS\.md\.onepersonlabs-backup-\d{8}-001\.expires-\d+", first_backup.name))

        second_original = self.target.read_bytes()
        (self.plugin / "AGENTS.md").write_bytes(content(4, "Second installed version."))
        second = self.apply(hashlib.sha256(second_original).hexdigest())
        second_backup = Path(second["backup"])
        self.assertRegex(second_backup.name, r"\.onepersonlabs-backup-\d{8}-002\.expires-\d+$")
        self.assertEqual(first_backup.read_bytes(), original)
        self.assertEqual(second_backup.read_bytes(), second_original)

    def test_concurrent_edit_and_downgrade_rejected(self):
        self.target.write_bytes(content(1))
        with self.assertRaisesRegex(ValueError, "changed after inspection"):
            self.apply("old hash")
        self.target.write_bytes(content(4))
        with self.assertRaisesRegex(ValueError, "downgrade"):
            self.apply(hashlib.sha256(content(4)).hexdigest())

    def test_missing_target_is_created_without_backup(self):
        result = self.apply("missing")
        self.assertIsNone(result["backup"])
        self.assertEqual(self.target.read_bytes(), (self.plugin / "AGENTS.md").read_bytes())

    def test_cleanup_removes_only_expired_owned_backups_and_supports_preview(self):
        now = time.time()
        old = self.home / f"AGENTS.md.onepersonlabs-backup-20200101-001.expires-{int(now - 1)}"
        recent = self.home / f"AGENTS.md.onepersonlabs-backup-20200101-002.expires-{int(now + 100)}"
        unrelated = self.home / "other-backup-20200101"
        for path in (old, recent, unrelated):
            path.write_bytes(b"backup")
        now = time.time()
        preview = instructions.cleanup_backups(self.home, now=now, preview=True)
        self.assertEqual(preview["deleted"], [])
        self.assertEqual(preview["would_delete"], [str(old)])
        self.assertTrue(old.exists())
        result = instructions.cleanup_backups(self.home, now=now)
        self.assertEqual(result["deleted"], [str(old)])
        self.assertFalse(old.exists())
        self.assertTrue(recent.exists())
        self.assertTrue(unrelated.exists())

    def test_failed_update_keeps_unresolved_recovery_backup_until_reconciled(self):
        original = content(1)
        self.target.write_bytes(original)
        real_replace = instructions.os.replace
        calls = 0

        def replace_then_fail(source, target):
            nonlocal calls
            calls += 1
            real_replace(source, target)
            if calls == 1:
                raise OSError("readback interruption")

        with patch.object(instructions.os, "replace", side_effect=replace_then_fail):
            with self.assertRaisesRegex(OSError, "readback interruption"):
                self.apply(hashlib.sha256(original).hexdigest())
        backups = [path for path in self.home.glob("AGENTS.md.onepersonlabs-backup-*")
                   if instructions._BACKUP_NAME.fullmatch(path.name)]
        self.assertEqual(len(backups), 1)
        backup = backups[0]
        self.assertEqual(backup.read_bytes(), original)
        self.assertTrue(backup.name.endswith(".pending"))
        cleanup = instructions.cleanup_backups(self.home, now=time.time() + 60 * 60 * 24 * 30)
        self.assertEqual(cleanup["deleted"], [])
        self.assertTrue(backup.exists())

    def test_successful_update_starts_fixed_retention_only_after_verified_readback(self):
        original = content(1)
        self.target.write_bytes(original)
        result = self.apply(hashlib.sha256(original).hexdigest())
        backup = Path(result["backup"])
        expiry = int(backup.name.rsplit(".expires-", 1)[1])
        self.assertGreaterEqual(expiry, time.time() + instructions.BACKUP_RETENTION_SECONDS - 2)

    def test_legacy_opl_backup_is_only_reconciled_after_later_version_is_active(self):
        legacy = self.home / "AGENTS.md.opl-backup-20200101-001"
        legacy.write_bytes(content(1, "old"))
        active = content(3, "current")
        self.target.write_bytes(active)
        old = time.time() - instructions.BACKUP_RETENTION_SECONDS - 10
        os.utime(legacy, (old, old))
        result = instructions.cleanup_backups(self.home)
        self.assertEqual(result["deleted"], [str(legacy)])
        self.assertFalse(legacy.exists())

    def test_legacy_uuid_backup_name_is_scoped_and_reconciled(self):
        legacy = self.home / "AGENTS.md.opl-backup-0cddb0f5eae24572af294b78b580ab12"
        legacy.write_bytes(content(1, "old"))
        self.target.write_bytes(content(3, "current"))
        old = time.time() - instructions.BACKUP_RETENTION_SECONDS - 10
        os.utime(legacy, (old, old))
        result = instructions.cleanup_backups(self.home)
        self.assertEqual(result["deleted"], [str(legacy)])

    def test_changed_override_during_apply_is_rejected(self):
        original = content(1)
        self.target.write_bytes(original)
        real_snapshot = instructions.snapshot
        calls = 0

        def changed(home, root):
            nonlocal calls
            calls += 1
            if calls == 2:
                (home / "AGENTS.override.md").write_bytes(content(2))
            return real_snapshot(home, root)

        with patch.object(instructions, "snapshot", side_effect=changed):
            with self.assertRaisesRegex(ValueError, "during application"):
                self.apply(hashlib.sha256(original).hexdigest())
        self.assertEqual(self.target.read_bytes(), original)

    def test_failed_atomic_replace_preserves_original(self):
        original = content(1)
        self.target.write_bytes(original)
        with patch.object(instructions.os, "replace", side_effect=OSError("locked")):
            with self.assertRaisesRegex(OSError, "locked"):
                self.apply(hashlib.sha256(original).hexdigest())
        self.assertEqual(self.target.read_bytes(), original)
        self.assertEqual(list(self.home.glob(".onepersonlabs-instructions-*")), [])

    def test_changed_installed_instructions_after_inspection_are_rejected(self):
        original = content(1)
        self.target.write_bytes(original)
        inspected = instructions.snapshot(self.home, self.plugin)
        (self.plugin / "AGENTS.md").write_bytes(content(3, "Changed installed defaults."))
        with self.assertRaisesRegex(ValueError, "changed after inspection"):
            instructions.apply_installed(self.home, self.plugin, inspected["sha256"], inspected["target"],
                                         inspected["bundled_sha256"])
        self.assertEqual(self.target.read_bytes(), original)

    def test_changed_installed_instructions_during_apply_are_rejected(self):
        original = content(1)
        self.target.write_bytes(original)
        real_snapshot = instructions.snapshot
        calls = 0

        def changed(home, root):
            nonlocal calls
            calls += 1
            if calls == 2:
                (root / "AGENTS.md").write_bytes(content(3, "Changed installed defaults."))
            return real_snapshot(home, root)

        with patch.object(instructions, "snapshot", side_effect=changed):
            with self.assertRaisesRegex(ValueError, "during application"):
                self.apply(hashlib.sha256(original).hexdigest())
        self.assertEqual(self.target.read_bytes(), original)
        self.assertEqual(list(self.home.glob(".onepersonlabs-instructions-*")), [])


if __name__ == "__main__":
    unittest.main()
