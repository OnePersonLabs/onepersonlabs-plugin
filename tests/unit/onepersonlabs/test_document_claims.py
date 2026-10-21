"""Focused behavior tests for the handoff evidence checker."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "plugins/onepersonlabs/skills/handoff/scripts/validate-doc-claims.py"


class DocumentClaimTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        self.root.mkdir()
        self.git("init", "-q")
        self.git("config", "user.name", "Test User")
        self.git("config", "user.email", "test@example.invalid")

    def git(self, *args):
        return subprocess.run(
            ["git", *args], cwd=self.root, check=True, capture_output=True,
            text=True, encoding="utf-8",
        )

    def commit_files(self):
        self.git("add", "--all")
        self.git("commit", "-q", "-m", "fixture")

    def validate(self, document, *, repo_root=None):
        command = [sys.executable, "-B", str(SCRIPT), str(document)]
        if repo_root is not None:
            command.extend(["--repo-root", str(repo_root)])
        return subprocess.run(
            command, cwd=self.root, capture_output=True, text=True,
            encoding="utf-8", errors="replace",
        )

    def test_false_path_and_fabricated_commit_citation_are_flags(self):
        document = self.root / "handoff.md"
        document.write_text(
            "The commit deadbeef1 fixed this issue. Check `src/café.py`.\n",
            encoding="utf-8",
        )
        self.commit_files()

        result = self.validate(document)

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("FLAG sha deadbeef1", result.stdout)
        self.assertIn("FLAG path `src/café.py`", result.stdout)
        self.assertIn("2 flags", result.stdout)

    def test_deleted_historical_path_is_distinguished_for_adjudication(self):
        old_file = self.root / "old" / "module.py"
        old_file.parent.mkdir()
        old_file.write_text("old implementation\n", encoding="utf-8")
        self.commit_files()
        old_file.unlink()
        document = self.root / "handoff.md"
        document.write_text(
            "The pre-fix implementation in `old/module.py` was removed.\n",
            encoding="utf-8",
        )

        result = self.validate(document)

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("tracked at HEAD but missing from the working tree", result.stdout)
        self.assertIn("deleted or uncommitted removal", result.stdout)
        self.assertIn("Annotate as historical", result.stdout)

    def test_relative_links_resolve_from_handoff_directory_outside_repo(self):
        document_dir = Path(self.temp.name) / "handoff"
        document_dir.mkdir()
        (document_dir / "near.md").write_text("target\n", encoding="utf-8")
        document = document_dir / "handoff.md"
        document.write_text(
            "[near](near.md) [missing](nested/missing.md)\n", encoding="utf-8"
        )
        (self.root / "source.txt").write_text("fixture\n", encoding="utf-8")
        self.commit_files()

        result = self.validate(document, repo_root=self.root)

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("FLAG link (nested/missing.md)", result.stdout)
        self.assertNotIn("FLAG link (near.md)", result.stdout)
        self.assertIn("2 links; 1 flags", result.stdout)


if __name__ == "__main__":
    unittest.main()
