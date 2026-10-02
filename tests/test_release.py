"""Focused checks for the release asset gate."""

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import prepare_release  # noqa: E402

spec = importlib.util.spec_from_file_location("release_flow", SCRIPTS / "release.py")
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        skill = self.repo / "skills" / "sample"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("---\nname: sample\ndescription: Example\n---\nContent\n", encoding="utf-8")
        self.result = prepare_release.prepare(self.repo, "1.0.0", self.repo / "dist")
        self.patch = patch.object(release, "REPO", self.repo)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def test_prepared_assets_match_source(self):
        assets = release.verify("v1.0.0")
        self.assertEqual({path.name for path in assets}, {"all-skills-v1.0.0.zip"})

    def test_stale_individual_asset_is_rejected(self):
        (self.repo / "dist/v1.0.0/sample.zip").write_bytes(b"stale")
        with self.assertRaisesRegex(ValueError, "unexpected"):
            release.verify("v1.0.0")

    def test_modified_source_or_asset_is_rejected(self):
        skill = self.repo / "skills" / "sample" / "SKILL.md"
        skill.write_text(skill.read_text(encoding="utf-8") + "changed\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "does not match"):
            release.verify("v1.0.0")
        skill.write_text(skill.read_text(encoding="utf-8").replace("changed\n", ""), encoding="utf-8")
        asset = self.repo / "dist" / "v1.0.0" / "all-skills-v1.0.0.zip"
        asset.write_bytes(asset.read_bytes() + b"changed")
        with self.assertRaisesRegex(ValueError, "asset changed"):
            release.verify("v1.0.0")


if __name__ == "__main__":
    unittest.main()
