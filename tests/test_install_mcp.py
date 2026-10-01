from pathlib import Path
import contextlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/install_mcp.py"
spec = importlib.util.spec_from_file_location("setup_mcp_installer", SCRIPT)
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallMcpTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.config = self.root / "config.toml"
        self.config.write_bytes(b'[mcp_servers.other]\ncommand = "keep"\n')
        self.args = ["local_documents", "--python", sys.executable, "--config", str(self.config), "--read-root", str(self.root)]

    def wheel(self, name):
        path = self.root / (name + ".whl")
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr(name + "-0.1.0.dist-info/METADATA", "Name: " + name + "\nVersion: 0.1.0\n")
        return path

    def test_preview_needs_no_repo_or_process_and_defaults_read_only(self):
        before = self.config.read_bytes()
        stream = io.StringIO()
        with patch.object(installer.subprocess, "run") as run, contextlib.redirect_stdout(stream):
            self.assertEqual(installer.main(self.args + ["--verify"]), 0)
        run.assert_not_called()
        result = json.loads(stream.getvalue())
        self.assertEqual(result["write_roots"], [])
        self.assertNotIn("source", result)
        self.assertEqual(self.config.read_bytes(), before)

    def test_apply_uses_installed_module_in_isolated_python(self):
        with patch.object(installer.subprocess, "run") as run:
            self.assertEqual(installer.main(self.args + ["--apply", "--verify", "--write-root", str(self.root)]), 0)
        commands = [call.args[0] for call in run.call_args_list]
        self.assertEqual(len(commands), 3)
        self.assertEqual(commands[1][1:5], ["-I", "-B", "-m", "mcp_servers.local_documents.install_document_mcp"])
        self.assertIn("--write-root", commands[1])
        self.assertEqual(commands[2][-1], "mcp_servers.local_documents.verify_document_mcp")

    def test_failed_pip_check_prevents_registration(self):
        with patch.object(installer.subprocess, "run", side_effect=subprocess.CalledProcessError(7, ["pip", "check"])) as run, contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(installer.main(self.args + ["--apply"]), 1)
        self.assertEqual(run.call_count, 1)

    def test_wrong_wheel_distribution_is_rejected_before_installation(self):
        wheel = self.wheel("unrelated")
        with patch.object(installer.subprocess, "run") as run, contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(installer.main(self.args + ["--core-wheel", str(wheel), "--apply"]), 1)
        run.assert_not_called()

    def test_wheel_hash_is_reported_without_installing(self):
        wheel = self.wheel("my-py-document-core")
        with patch.object(installer.subprocess, "run") as run, contextlib.redirect_stdout(io.StringIO()) as stream:
            self.assertEqual(installer.main(self.args + ["--core-wheel", str(wheel)]), 0)
        self.assertEqual(len(json.loads(stream.getvalue())["wheels"][0]["sha256"]), 64)
        run.assert_not_called()

    def test_new_runtime_requires_both_wheels_and_preserves_existing_user_folder(self):
        base = ["local_documents", "--config", str(self.config), "--read-root", str(self.root)]
        with patch.object(installer.venv, "EnvBuilder") as builder, contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(installer.main(base + ["--runtime", str(self.root / "new-runtime"), "--apply"]), 1)
            self.assertEqual(installer.main(base + ["--runtime", str(self.root), "--apply"]), 1)
        builder.assert_not_called()

    def test_install_failure_stops_before_registration(self):
        wheel = self.wheel("my-py-document-core")
        with patch.object(installer.subprocess, "run", side_effect=subprocess.CalledProcessError(3, ["pip", "install"])) as run, contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(installer.main(self.args + ["--core-wheel", str(wheel), "--apply"]), 1)
        self.assertEqual(run.call_count, 1)

    def test_jev_defaults_to_preview_and_preserves_options(self):
        with patch.object(installer.subprocess, "run", return_value=subprocess.CompletedProcess([], 0)) as run:
            self.assertEqual(installer.main(["jev", "--replace"]), 0)
        self.assertIn("--dry-run", run.call_args.args[0])
        with patch.object(installer.subprocess, "run", return_value=subprocess.CompletedProcess([], 8)) as run:
            self.assertEqual(installer.main(["jev", "--apply", "--verify-online"]), 8)
        self.assertNotIn("--dry-run", run.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
