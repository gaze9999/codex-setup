from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/prepare_release.py"
if not SCRIPT.is_file():
    SCRIPT = Path(__file__).with_name("prepare_release.py")
spec = importlib.util.spec_from_file_location("prepare_release", SCRIPT)
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


class PrepareReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary.name)
        self.output = self.repo / "dist"

    def tearDown(self):
        self.temporary.cleanup()

    def skill(self, name, version="v1.2.3", metadata=True, crlf=False):
        root = self.repo / "skills" / name
        root.mkdir(parents=True)
        header = f"---\nname: {name}\ndescription: A focused test skill\n"
        if metadata:
            header += f'metadata:\n  custom: "keep"\n  version: "{version}" # retain comment\n  author: "example"\n  repository: "https://github.com/example/skills"\n'
        text = header + "license: MIT\n---\n\n# Instructions\n\nKeep the body unchanged\n"
        (root / "SKILL.md").write_bytes(text.replace("\n", "\r\n").encode() if crlf else text.encode())
        (root / "assets").mkdir()
        (root / "assets/data.txt").write_text("asset payload", encoding="utf-8")
        return root

    def test_auto_patch_and_combined_archive_layout(self):
        self.skill("alpha", crlf=True)
        self.skill("beta")
        result = release.prepare(self.repo, None, self.output)
        self.assertEqual((result["tag"], result["skills"], result["zip_count"]), ("v1.2.4", 2, 1))
        folder = Path(result["output"])
        with zipfile.ZipFile(folder / "all-skills-v1.2.4.zip") as archive:
            self.assertEqual(set(name.split("/")[0] for name in archive.namelist()), {"alpha", "beta"})
            self.assertFalse(any(name.endswith(".zip") or name.startswith("skills/") for name in archive.namelist()))
            self.assertEqual(archive.read("alpha/assets/data.txt"), b"asset payload")
            self.assertEqual(archive.read("alpha/SKILL.md"), (self.repo / "skills/alpha/SKILL.md").read_bytes())
        self.assertEqual({p.name for p in folder.glob("*.zip")}, {"all-skills-v1.2.4.zip"})
        text = (self.repo / "skills/alpha/SKILL.md").read_bytes()
        self.assertIn(b'version: "v1.2.4" # retain comment\r\n', text)
        self.assertIn(b'custom: "keep"\r\n', text)
        self.assertIn(b"license: MIT\r\n---\r\n", text)
        self.assertNotIn(b"\n", text.replace(b"\r\n", b""))

    def test_regeneration_removes_managed_legacy_individual_archives(self):
        self.skill("alpha")
        result = release.prepare(self.repo, "2.0.0", self.output)
        folder = Path(result["output"])
        old = folder / "alpha.zip"
        old.write_bytes((folder / "all-skills-v2.0.0.zip").read_bytes())
        marker = folder / release.MANIFEST
        manifest = json.loads(marker.read_text(encoding="utf-8"))
        manifest["assets"].append({"name": old.name, "size": old.stat().st_size, "sha256": release.digest(old.read_bytes())})
        marker.write_text(json.dumps(manifest), encoding="utf-8")
        release.prepare(self.repo, "2.0.0", self.output)
        self.assertFalse(old.exists())
        self.assertEqual([a["name"] for a in json.loads(marker.read_text(encoding="utf-8"))["assets"]], ["all-skills-v2.0.0.zip"])

    def test_manual_version_and_missing_metadata(self):
        self.skill("alpha")
        self.skill("beta", metadata=False)
        result = release.prepare(self.repo, "2.0.0", self.output)
        self.assertEqual(result["tag"], "v2.0.0")
        text = (self.repo / "skills/beta/SKILL.md").read_text(encoding="utf-8")
        self.assertIn('version: "v2.0.0"', text)
        self.assertIn('author: "example"', text)
        self.assertIn('repository: "https://github.com/example/skills"', text)
        self.assertEqual(text.split("---", 2)[2], "\n\n# Instructions\n\nKeep the body unchanged\n")

    def test_added_renamed_deleted_skills_refresh_same_output(self):
        alpha = self.skill("alpha")
        beta = self.skill("beta")
        release.prepare(self.repo, "3.0.0", self.output)
        renamed = alpha.with_name("renamed")
        alpha.rename(renamed)
        path = renamed / "SKILL.md"
        path.write_text(path.read_text(encoding="utf-8").replace("name: alpha", "name: renamed"), encoding="utf-8")
        self.assertTrue(beta.resolve().is_relative_to(self.repo.resolve()))
        shutil.rmtree(beta)
        self.skill("new-skill", metadata=False)
        result = release.prepare(self.repo, "v3.0.0", self.output)
        folder = Path(result["output"])
        self.assertEqual({path.name for path in folder.glob("*.zip")}, {"all-skills-v3.0.0.zip"})
        with zipfile.ZipFile(folder / "all-skills-v3.0.0.zip") as archive:
            self.assertEqual({name.split("/")[0] for name in archive.namelist()}, {"renamed", "new-skill"})
        manifest = json.loads((folder / release.MANIFEST).read_text(encoding="utf-8"))
        self.assertEqual(manifest["skills"], ["new-skill", "renamed"])

    def test_dry_run_and_local_tags(self):
        root = self.skill("alpha")
        original = (root / "SKILL.md").read_bytes()
        with patch.object(release, "git_output", side_effect=lambda repo, *args: "v4.5.6\nnot-a-version\n" if args[0] == "tag" else None):
            result = release.prepare(self.repo, None, self.output, dry_run=True)
        self.assertEqual(result["tag"], "v4.5.7")
        self.assertEqual((root / "SKILL.md").read_bytes(), original)
        self.assertFalse(self.output.exists())

    def test_unmanaged_output_is_preserved_before_version_write(self):
        root = self.skill("alpha")
        original = (root / "SKILL.md").read_bytes()
        output = self.output / "v2.0.0"
        output.mkdir(parents=True)
        (output / "someone-else.txt").write_text("keep", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unmanaged"):
            release.prepare(self.repo, "2.0.0", self.output)
        self.assertEqual((root / "SKILL.md").read_bytes(), original)
        self.assertEqual((output / "someone-else.txt").read_text(encoding="utf-8"), "keep")

    def test_caches_and_secrets_are_excluded(self):
        root = self.skill("alpha")
        (root / "__pycache__").mkdir()
        (root / "__pycache__/cache.pyc").write_bytes(b"cache")
        for name in ("build", "dist", "package.egg-info"):
            (root / name).mkdir()
            (root / name / "generated.txt").write_text("excluded", encoding="utf-8")
        for name in (".env", ".env.local", "run.log", "private.key", "notes.tmp"):
            (root / name).write_text("excluded", encoding="utf-8")
        (root / ".env.example").write_text("EXAMPLE=", encoding="utf-8")
        result = release.prepare(self.repo, "2.0.0", self.output)
        with zipfile.ZipFile(Path(result["output"]) / "all-skills-v2.0.0.zip") as archive:
            self.assertEqual(set(archive.namelist()), {"alpha/SKILL.md", "alpha/assets/data.txt", "alpha/.env.example"})

    def test_invalid_version_and_output_inside_skills(self):
        root = self.skill("alpha")
        original = (root / "SKILL.md").read_bytes()
        for version, output in (("bad-version", self.output), ("2.0.0", root / "generated")):
            with self.assertRaises(ValueError):
                release.prepare(self.repo, version, output)
        self.assertEqual((root / "SKILL.md").read_bytes(), original)

    def test_metadata_rolls_back_if_version_write_fails(self):
        roots = [self.skill("alpha"), self.skill("beta")]
        originals = {root / "SKILL.md": (root / "SKILL.md").read_bytes() for root in roots}
        write = release.atomic_write
        calls = 0

        def fail_once(path, data):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("simulated write failure")
            write(path, data)

        with patch.object(release, "atomic_write", side_effect=fail_once):
            with self.assertRaisesRegex(OSError, "simulated"):
                release.prepare(self.repo, "2.0.0", self.output)
        for path, data in originals.items():
            self.assertEqual(path.read_bytes(), data)
        self.assertFalse((self.output / "v2.0.0").exists())

    @unittest.skipUnless(shutil.which("git"), "Git is unavailable")
    def test_git_ignored_files_and_working_tree_rename(self):
        root = self.skill("alpha")
        subprocess.run(["git", "init", "--quiet", str(self.repo)], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(self.repo), "add", "skills"], check=True, capture_output=True)
        (self.repo / ".gitignore").write_text("skills/*/assets/ignored.dat\n", encoding="utf-8")
        (root / "assets/ignored.dat").write_text("ignored", encoding="utf-8")
        release.prepare(self.repo, "2.0.0", self.output)
        renamed = root.with_name("renamed")
        root.rename(renamed)
        path = renamed / "SKILL.md"
        path.write_text(path.read_text(encoding="utf-8").replace("name: alpha", "name: renamed"), encoding="utf-8")
        result = release.prepare(self.repo, "2.0.0", self.output)
        folder = Path(result["output"])
        self.assertFalse((folder / "alpha.zip").exists())
        with zipfile.ZipFile(folder / "all-skills-v2.0.0.zip") as archive:
            self.assertEqual(set(archive.namelist()), {"renamed/SKILL.md", "renamed/assets/data.txt"})

    def test_malformed_output_manifest_preserves_skill_version(self):
        root = self.skill("alpha")
        original = (root / "SKILL.md").read_bytes()
        output = self.output / "v2.0.0"
        output.mkdir(parents=True)
        (output / release.MANIFEST).write_text(json.dumps({"producer": release.PRODUCER, "tag": "v2.0.0"}), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Invalid output manifest"):
            release.prepare(self.repo, "2.0.0", self.output)
        self.assertEqual((root / "SKILL.md").read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
