"""Focused checks for minute timestamps and append-only history evidence."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "skills" / "task-guide" / "scripts" / "record_history.py"


class TaskHistoryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "歷史快照 with spaces"
        self.root.mkdir()
        self.source = self.root / "entry.json"
        self.output = self.root / "docs" / "history.md"
        self.data = {"timestamp": "2026-10-01 09:30", "title": "工作項目盤點",
                     "summary": "保留既有 ID 並追加待辦", "checks": ["僅文件核對, 未執行 Build"]}
        self.write_input()

    def tearDown(self):
        self.temporary.cleanup()

    def write_input(self):
        self.source.write_text(json.dumps(self.data, ensure_ascii=False), encoding="utf-8-sig")

    def run_cli(self, *args):
        return subprocess.run([sys.executable, "-B", str(SCRIPT), str(self.source), *map(str, args)],
                              cwd=self.root, capture_output=True, encoding="utf-8", check=False)

    def test_create_without_commit_omits_git_line(self):
        result = self.run_cli("--output", self.output)
        self.assertEqual(result.returncode, 0, result.stderr)
        text = self.output.read_text(encoding="utf-8")
        self.assertIn("## 2026-10-01 09:30 工作項目盤點", text)
        self.assertNotIn("Git:", text)
        self.assertIn(self.data["summary"], text)
        self.assertIn("未執行 Build", text)

    def test_append_preserves_existing_bytes_and_distinguishes_uncommitted_changes(self):
        self.output.parent.mkdir()
        original = b"\xef\xbb\xbf# existing history\r\n\r\nold evidence\r\n"
        self.output.write_bytes(original)
        self.data.update({"commit": "abcdef1234", "repository": "example", "uncommitted": True})
        self.write_input()
        result = self.run_cli("--output", self.output)
        self.assertEqual(result.returncode, 0, result.stderr)
        contents = self.output.read_bytes()
        self.assertTrue(contents.startswith(original))
        self.assertIn("Git: example@abcdef1234 + 未提交變更", contents.decode("utf-8-sig"))
        self.assertIn(self.data["summary"], contents.decode("utf-8-sig"))
        self.assertNotIn(b"\n", contents[len(original):].replace(b"\r\n", b""))

    def test_repeated_entry_is_rejected_without_changing_history(self):
        self.assertEqual(self.run_cli("--output", self.output).returncode, 0)
        original = self.output.read_bytes()
        result = self.run_cli("--output", self.output)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.output.read_bytes(), original)

    def test_invalid_time_or_commit_never_creates_output(self):
        invalid = [
            {**self.data, "timestamp": "2026-10-01 09:30:00"},
            {**self.data, "timestamp": "2026-10-01 9:30"},
            {**self.data, "timestamp": "2026-02-30 09:30"},
            {**self.data, "commit": "not-a-sha"},
            {**self.data, "commit": "a" * 40},
            {**self.data, "uncommitted": "false"},
            {**self.data, "checks": "passed"},
            {key: value for key, value in {**self.data, "commit": "abcdef12"}.items() if key != "summary"},
        ]
        for index, data in enumerate(invalid):
            with self.subTest(case=index):
                self.source.write_text(json.dumps(data), encoding="utf-8")
                result = self.run_cli("--output", self.output)
                self.assertEqual(result.returncode, 2)
                self.assertFalse(self.output.parent.exists())

    def test_preview_and_check_do_not_create_files(self):
        for mode in ("--dry-run", "--check"):
            with self.subTest(mode=mode):
                result = self.run_cli(mode, "--output", self.output)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertFalse(self.output.parent.exists())

    def test_input_cannot_be_used_as_history_output(self):
        self.source = self.root / "source.md"
        self.write_input()
        original = self.source.read_bytes()
        result = self.run_cli("--output", self.source)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.source.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
