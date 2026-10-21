import importlib.util
from contextlib import closing
import json
import os
from pathlib import Path
import sqlite3
import tempfile
import tomllib
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[3]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


migration = load_module("onepersonlabs_identity_migration", ROOT / "plugins/onepersonlabs/scripts/migrate_identity.py")
application = load_module("onepersonlabs_harness_application", ROOT / "plugins/onepersonlabs/skills/configure-harness/scripts/application.py")


class IdentityMigration(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.home = self.root / "home"
        self.home.mkdir()
        self.backups = self.root / "recovery"
        self.backups.mkdir()
        (self.home / "config.toml").write_text('model = "gpt-6.1-sol"\n', encoding="utf-8")
        self.old_runtime = self.root / "runtime" / "opl" / "human-inbox"
        self.new_runtime = self.root / "runtime" / "onepersonlabs" / "human-inbox"
        self.runtime_paths = patch.object(migration, "runtime_paths", return_value=(self.old_runtime, self.new_runtime))
        self.runtime_paths.start()
        self.addCleanup(self.runtime_paths.stop)

    def migrate(self, root_mappings=()):
        return migration.migrate_home(self.home, self.backups, root_mappings)

    def test_catalog_workspace_identity_path_and_pause_state_survive(self):
        old_workspace = self.root / "projects" / "opl"
        new_workspace = self.root / "projects" / "onepersonlabs"
        old_workspace.mkdir(parents=True)
        self.old_runtime.mkdir(parents=True)
        with closing(sqlite3.connect(self.old_runtime / "catalog.sqlite3")) as database:
            database.execute("CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
            database.execute("CREATE TABLE workspaces (id TEXT PRIMARY KEY, path TEXT NOT NULL UNIQUE)")
            database.execute("INSERT INTO meta VALUES ('id', 'catalog-identity-123')")
            database.execute("INSERT INTO workspaces VALUES ('workspace-identity-456', ?)", (str(old_workspace),))
            database.commit()
        refresh_state = {"version": 1, "workspace": str(old_workspace), "was_running": True,
                         "host": "127.0.0.1", "port": 43871, "allow_lan": False, "wake_root": True}
        service_receipt = {"catalog_id": "catalog-identity-123", "workspace": str(old_workspace), "pid": 9134}
        (self.old_runtime / "refresh-state.json").write_text(json.dumps(refresh_state), encoding="utf-8")
        (self.old_runtime / "service.json").write_text(json.dumps(service_receipt), encoding="utf-8")

        self.migrate([(old_workspace, new_workspace)])

        self.assertFalse(self.old_runtime.exists())
        with closing(sqlite3.connect(self.new_runtime / "catalog.sqlite3")) as database:
            self.assertEqual(database.execute("SELECT value FROM meta WHERE key='id'").fetchone()[0], "catalog-identity-123")
            self.assertEqual(database.execute("SELECT id,path FROM workspaces").fetchone(),
                             ("workspace-identity-456", str(new_workspace)))
        self.assertEqual(json.loads((self.new_runtime / "refresh-state.json").read_text()),
                         {**refresh_state, "workspace": str(new_workspace)})
        self.assertEqual(json.loads((self.new_runtime / "service.json").read_text()),
                         {**service_receipt, "workspace": str(new_workspace)})

    def test_preserves_custom_config_and_retires_only_manifest_owned_role(self):
        old_cache = self.home / "plugins" / "cache" / "opl" / "opl"
        old_plugin = old_cache / "0.3.0"
        agents = old_plugin / "agents"
        agents.mkdir(parents=True)
        (old_plugin / ".codex-plugin").mkdir()
        (old_plugin / ".codex-plugin" / "plugin.json").write_text(json.dumps({"name": "opl"}), encoding="utf-8")
        owned_profile = agents / "opl-reviewer.toml"
        owned_profile.write_text("model = 'gpt-6-luna'\n", encoding="utf-8")
        custom_profile = self.root / "custom" / "opl-personal.toml"
        custom_profile.parent.mkdir()
        custom_profile.write_text("model = 'gpt-6.1-sol'\n", encoding="utf-8")
        disabled_path = old_cache / "0.3.0" / "skills" / "adhd"
        config = (
            f"[agents.opl-reviewer]\nconfig_file = {json.dumps(str(owned_profile))}\n\n"
            f"[agents.opl-personal]\nconfig_file = {json.dumps(str(custom_profile))}\n\n"
            "[skills]\nconfig = [\n"
            "  { name = 'opl:adhd', enabled = false },\n"
            f"  {{ path = {json.dumps(str(disabled_path))}, enabled = false }},\n"
            "]\n"
        )
        (self.home / "config.toml").write_text(config, encoding="utf-8")

        self.migrate()

        migrated = (self.home / "config.toml").read_text(encoding="utf-8")
        self.assertNotIn("[agents.opl-reviewer]", migrated)
        self.assertIn(f"[agents.opl-personal]\nconfig_file = {json.dumps(str(custom_profile))}", migrated)
        self.assertIn("{ name = 'opl:adhd', enabled = false }", migrated)
        skill_path = Path(tomllib.loads(migrated)["skills"]["config"][1]["path"])
        self.assertEqual(skill_path, self.home / "plugins" / "cache" / "onepersonlabs" / "onepersonlabs" / "0.3.1" / "skills" / "adhd")
        self.assertTrue((self.home / "plugins" / "cache" / "opl" / "opl" / "0.3.0" / "agents" / "opl-reviewer.toml").is_file())

    def test_harness_receipt_and_exact_backup_remain_usable_after_move(self):
        policy = self.home / "onepersonlabs" / "harness" / "policies" / "managed.md"
        original = b"Original policy bytes\r\n"
        policy.parent.mkdir(parents=True)
        policy.write_bytes(original)
        candidate = self.root / "candidate.md"
        candidate.write_bytes(b"Updated policy bytes\n")
        plan = application.prepare(self.home, [{"target": str(policy), "candidate": str(candidate)}])
        applied = application.apply(self.home, plan)
        old_owned_state = self.home / "opl"
        (self.home / "onepersonlabs").rename(old_owned_state)
        old_transaction_root = old_owned_state / "harness" / "transactions"
        for receipt_path in old_transaction_root.glob("*/receipt.json"):
            text = receipt_path.read_text(encoding="utf-8")
            text = text.replace(str(self.home / "onepersonlabs"), str(old_owned_state))
            receipt_path.write_text(text, encoding="utf-8")
        old_receipt = Path(applied["receipt"]).as_posix().replace(
            (self.home / "onepersonlabs").as_posix(), old_owned_state.as_posix())

        self.migrate()

        receipt = Path(old_receipt.replace(old_owned_state.as_posix(), (self.home / "onepersonlabs").as_posix()))
        self.assertTrue(receipt.is_file())
        record = json.loads(receipt.read_text(encoding="utf-8"))
        self.assertEqual(Path(record["files"][0]["backup"]).read_bytes(), original)
        self.assertEqual(application.rollback(self.home, receipt)["restored"], 1)
        self.assertEqual(policy.read_bytes(), original)

    def test_destination_collision_refuses_without_changing_state_or_config(self):
        old = self.home / "opl"
        new = self.home / "onepersonlabs"
        old.mkdir()
        new.mkdir()
        (old / "owned.json").write_text('{"path":"old"}', encoding="utf-8")
        (new / "owned.json").write_text('{"path":"new"}', encoding="utf-8")
        before_config = (self.home / "config.toml").read_bytes()
        before_old = (old / "owned.json").read_bytes()
        before_new = (new / "owned.json").read_bytes()

        with self.assertRaisesRegex(ValueError, "destination already exists"):
            self.migrate()

        self.assertEqual((self.home / "config.toml").read_bytes(), before_config)
        self.assertEqual((old / "owned.json").read_bytes(), before_old)
        self.assertEqual((new / "owned.json").read_bytes(), before_new)
        self.assertFalse((self.backups / "progress.json").exists())
        self.assertFalse((self.backups / "config.before-identity.toml").exists())

    def test_conflicting_old_skill_versions_require_a_decision_before_writes(self):
        cache = self.home / 'plugins/cache/opl/opl'
        entries = [f'{{path={json.dumps(str(cache / version / "skills/adhd"))}, enabled={enabled}}}'
                   for version, enabled in [('0.2.0', 'true'), ('0.3.0', 'false')]]
        original = ('[skills]\nconfig=[' + ','.join(entries) + ']\n').encode()
        (self.home / 'config.toml').write_bytes(original)
        with self.assertRaisesRegex(ValueError, 'conflicting skills.config destination'):
            self.migrate()
        self.assertEqual((self.home / 'config.toml').read_bytes(), original)
        self.assertEqual(list(self.backups.iterdir()), [])

    def test_custom_runtime_locations_and_in_place_transfer(self):
        custom = self.root / 'custom-runtime'
        environment = {'OPL_HUMAN_RUNTIME': str(custom), 'ONEPERSONLABS_HUMAN_RUNTIME': str(custom)}
        self.runtime_paths.stop()
        with patch.dict(os.environ, environment):
            self.assertEqual(migration.runtime_paths(self.home), (custom, custom))
            custom.mkdir()
            previous = self.root / 'old-project'
            current = self.root / 'renamed-project'
            (custom / 'refresh-state.json').write_text(json.dumps({'workspace': str(previous), 'was_running': False}))
            self.migrate([(previous, current)])
            self.assertEqual(json.loads((custom / 'refresh-state.json').read_text())['workspace'], str(current))
            self.assertTrue((self.backups / 'state-1/refresh-state.json').is_file())
        self.runtime_paths.start()


if __name__ == "__main__":
    unittest.main(verbosity=2)
