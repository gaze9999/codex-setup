from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


REPOSITORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY / "mcp_servers" / "workspace_inspection"))
sys.path.insert(0, str(REPOSITORY.parent / "my-py-tools" / "packages" / "workspace_core"))

from workspace_inspection_mcp.install import main as install_main
from workspace_inspection_mcp.service import WorkspaceInspectionService


class WorkspaceInspectionTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.source = self.root / "source"
        self.target = self.root / "target"
        self.source.mkdir()
        self.target.mkdir()
        self.service = WorkspaceInspectionService([self.root])

    def test_compare_and_validation_are_read_only_and_bounded(self) -> None:
        (self.source / "value.txt").write_text("before", encoding="utf-8")
        (self.target / "value.txt").write_text("after", encoding="utf-8")
        run = self.root / "runs" / "run-001"
        run.mkdir(parents=True)
        run.joinpath("results.json").write_text(json.dumps({"results": [{"name": "test", "status": "passed"}]}), encoding="utf-8")

        comparison = self.service.compare_environment(str(self.source), str(self.target))
        evidence = self.service.validation_evidence(str(self.root / "runs"))

        self.assertEqual(comparison["changed"][0]["path"], "value.txt")
        self.assertEqual(evidence["runs"][0]["results"][0]["status"], "passed")
        with self.assertRaisesRegex(ValueError, "roots"):
            self.service.validation_evidence(str(self.root.parent))

    def test_installer_preview_and_apply_preserve_other_settings(self) -> None:
        config = self.root / "config.toml"
        config.write_text('[features]\nkeep = true\n', encoding="utf-8")
        args = ["--python", sys.executable, "--config", str(config), "--read-root", str(self.root)]
        with patch("workspace_inspection_mcp.install.subprocess.run"):
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                self.assertEqual(install_main(args), 0)
            self.assertEqual(json.loads(stream.getvalue())["status"], "preview")
            self.assertEqual(config.read_text(encoding="utf-8"), '[features]\nkeep = true\n')

            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                self.assertEqual(install_main(args + ["--apply"]), 0)
            result = json.loads(stream.getvalue())
            self.assertEqual(result["status"], "installed")
            self.assertIn("[mcp_servers.workspace_inspection]", config.read_text(encoding="utf-8"))
            self.assertTrue(Path(result["backup"]).is_file())


if __name__ == "__main__":
    unittest.main()
