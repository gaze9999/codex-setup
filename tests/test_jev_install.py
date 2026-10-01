from pathlib import Path
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
try:
    import tomllib
except ImportError:
    import tomli as tomllib
import unittest
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "skills/jev-evaluation/scripts/install_mcp.py"
spec = importlib.util.spec_from_file_location("jev_installer", SCRIPT)
i = importlib.util.module_from_spec(spec)
spec.loader.exec_module(i)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source"
        self.source.mkdir()
        (self.source / "SKILL.md").write_text("Skill", encoding="utf-8")
        (self.source / "scripts").mkdir()
        (self.source / "scripts/mcp_server.py").write_text("server", encoding="utf-8")
        self.target = self.root / "installed" / i.NAME
        self.config = self.root / "config.toml"
        self.runtime = self.root / "runtime"

    def install(self, replace=False):
        return i.install(self.source, self.target, self.config, self.runtime, replace)

    def test_config_preserves_existing_settings_and_never_embeds_key(self):
        original = '[mcp_servers.other]\ncommand = "other"\n# retained comment\n[preferences]\nvalue = 2\n'
        updated = i.update_config(original, Path("python"), Path("server 空白.py"))
        self.assertTrue(updated.startswith(original))
        parsed = tomllib.loads(updated)
        self.assertEqual(parsed["preferences"]["value"], 2)
        self.assertFalse(parsed["mcp_servers"]["jev"]["required"])
        self.assertNotIn("env", parsed["mcp_servers"]["jev"])

    def test_managed_update_is_idempotent_and_replaces_only_own_block(self):
        first = i.update_config('model = "unchanged"\n', Path("python"), Path("old.py"))
        same = i.update_config(first, Path("python"), Path("old.py"))
        self.assertEqual(first, same)
        new = i.update_config(first, Path("python"), Path("new.py"))
        self.assertEqual(new.count("[mcp_servers.jev]"), 1)
        self.assertNotIn("old.py", new)

    def test_unmanaged_server_conflict_preserves_files(self):
        original = '[mcp_servers.jev]\ncommand = "user-owned"\n'
        self.config.write_text(original, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "existing_jev_server_not_managed"):
            self.install()
        self.assertFalse(self.target.exists())
        self.assertEqual(self.config.read_text(encoding="utf-8"), original)

    def test_invalid_toml_fails_before_skill_write(self):
        self.config.write_text("[invalid", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.install()
        self.assertFalse(self.target.exists())

    def test_first_install_matches_source_and_registers_absolute_paths(self):
        result = self.install()
        self.assertEqual(i.files(self.source), i.files(self.target))
        settings = tomllib.loads(self.config.read_text(encoding="utf-8"))["mcp_servers"]["jev"]
        self.assertEqual(settings["args"][1], str(self.target.resolve() / "scripts/mcp_server.py"))
        self.assertEqual(result["status"], "ok")

    def test_replacement_requires_flag_and_backs_up_previous_files(self):
        self.install()
        (self.source / "SKILL.md").write_text("new", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "existing_skill_use_replace"):
            self.install()
        result = self.install(True)
        self.assertEqual((Path(result["backup"]) / i.NAME / "SKILL.md").read_text(encoding="utf-8"), "Skill")
        self.assertEqual((self.target / "SKILL.md").read_text(encoding="utf-8"), "new")

    def test_unexpected_installed_files_are_preserved(self):
        self.install()
        (self.target / "local.md").write_text("user work", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unexpected_installed_files"):
            self.install(True)
        self.assertEqual((self.target / "local.md").read_text(encoding="utf-8"), "user work")

    def test_changed_config_is_not_overwritten(self):
        self.config.write_text('value = "original"\n', encoding="utf-8")
        prepare = i.update_config
        def change(original, python, server):
            result = prepare(original, python, server)
            self.config.write_text('value = "concurrent"\n', encoding="utf-8")
            return result
        with mock.patch.object(i, "update_config", side_effect=change), self.assertRaisesRegex(ValueError, "config_changed_during_install"):
            self.install()
        self.assertFalse(self.target.exists())
        self.assertIn("concurrent", self.config.read_text(encoding="utf-8"))

    def test_source_credentials_are_refused(self):
        (self.source / "private.key").write_text("not-a-real-key", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "skill_contains_private"):
            self.install()
        self.assertFalse(self.target.exists())

    def test_json_output_is_utf8_even_when_windows_encoding_is_cp950(self):
        destination = self.root / "中文 空白 路徑"
        env = dict(os.environ, PYTHONIOENCODING="cp950")
        run = subprocess.run([sys.executable, "-B", str(SCRIPT), "--dry-run", "--skill-root", str(destination)], env=env, capture_output=True, check=False)
        self.assertEqual(run.returncode, 0, run.stderr)
        data = json.loads(run.stdout.decode("utf-8"))
        self.assertEqual(data["skill"], str(destination / i.NAME))
        self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
