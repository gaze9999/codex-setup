"""Focused CLI checks for task-guide creation and preservation boundaries."""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1] / "skills" / "task-guide"
SCRIPT = SKILL / "scripts" / "create_task_guide.py"


class TaskGuideTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "另一個專案 with spaces"
        self.root.mkdir()
        self.source = self.root / "input.json"
        self.output = self.root / ".codex" / "agent-guidance" / "orders.md"
        self.data = {
            "title": "訂單 task rules",
            "scope": ["僅修改已授權畫面", "保留既有 state\n不得建立第二個 owner"],
            "read_by_task": [{"need": "欄位 | mapping", "evidence": "`specs/order.md`\n確認空值語意"}],
            "source_authority": ["業務規則由 `specs/order.md` 決定; API 保留 `orderId`"],
        }
        self.write_input()

    def tearDown(self):
        self.temporary.cleanup()

    def write_input(self):
        self.source.write_text(json.dumps(self.data, ensure_ascii=False), encoding="utf-8-sig")

    def run_cli(self, *args, script=SCRIPT):
        return subprocess.run([sys.executable, "-B", str(script), str(self.source), *map(str, args)],
                              cwd=self.root, capture_output=True, encoding="utf-8", check=False)

    def test_create_preserves_unicode_sources_and_table_content(self):
        result = self.run_cli("--output", self.output)
        self.assertEqual(result.returncode, 0, result.stderr)
        text = self.output.read_text(encoding="utf-8")
        self.assertIn("欄位 \\| mapping", text)
        self.assertIn("`specs/order.md`<br>確認空值語意", text)
        self.assertIn(self.data["source_authority"][0], text)
        self.assertIn("- 保留既有 state\n  不得建立第二個 owner", text)
        self.assertNotIn(b"\r\n", self.output.read_bytes())

    def test_preview_and_check_do_not_create_parent_directories(self):
        for mode in ("--dry-run", "--check"):
            with self.subTest(mode=mode):
                result = self.run_cli(mode, "--output", self.output)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertFalse(self.output.parent.exists())
        self.assertIn(self.data["source_authority"][0], self.run_cli("--dry-run").stdout)
        self.assertNotIn("orderId", self.run_cli("--check").stdout)

    def test_existing_guide_is_preserved(self):
        self.output.parent.mkdir(parents=True)
        original = b"existing concurrent work\n"
        self.output.write_bytes(original)
        result = self.run_cli("--output", self.output)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.output.read_bytes(), original)

    def test_invalid_schema_never_writes_output(self):
        invalid = [
            {key: value for key, value in self.data.items() if key != "source_authority"},
            {**self.data, "scope": "not a list"},
            {**self.data, "read_by_task": [{"need": "API", "evidence": "source", "lost": "decision"}]},
            {**self.data, "open_items": [None]},
            {**self.data, "undocumented_decisions": ["must not be discarded"]},
            {**self.data, "title": "title\nnew heading"},
            {**self.data, "source_authority": []},
        ]
        for index, data in enumerate(invalid):
            with self.subTest(case=index):
                self.source.write_text(json.dumps(data), encoding="utf-8")
                result = self.run_cli("--output", self.output)
                self.assertEqual(result.returncode, 2, result.stdout)
                self.assertFalse(self.output.parent.exists())

    def test_duplicate_properties_and_invalid_encoding_are_rejected(self):
        duplicate = json.dumps(self.data)[:-1] + ', "title": "overwritten"}'
        for content in (duplicate.encode("utf-8"), b"\xff\xfeinvalid"):
            with self.subTest(content=content[:12]):
                self.source.write_bytes(content)
                result = self.run_cli("--output", self.output)
                self.assertEqual(result.returncode, 2)
                self.assertFalse(self.output.parent.exists())

    def test_input_file_is_never_replaced(self):
        self.source = self.root / "existing.md"
        self.write_input()
        original = self.source.read_bytes()
        result = self.run_cli("--output", self.source)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.source.read_bytes(), original)

    def test_copied_skill_runs_without_repository_or_dependencies(self):
        copied = self.root / "installed skill"
        shutil.copytree(SKILL, copied)
        self.source = copied / "assets" / "task-guide.example.json"
        result = self.run_cli("--output", self.output, script=copied / "scripts" / SCRIPT.name)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("ASK USER", self.output.read_text(encoding="utf-8"))

    def scheme(self):
        return {
            "registry": "docs/progress.md", "separator": "-", "digits": 2,
            "groups": [{"prefix": "UI", "meaning": "畫面"}, {"prefix": "API", "meaning": "介面"}],
            "reserved": ["UI-01", "UI-04", "API-02", "UI-01", "~~UI-07~~"],
            "items": [
                {"key": "new", "prefix": "UI", "title": "新增查詢"},
                {"key": "old", "prefix": "UI", "title": "名稱已改", "id": "UI-07"},
                {"key": "api", "prefix": "API", "title": "介面驗證"},
            ],
        }

    def test_id_allocation_preserves_existing_ids_and_skips_historical_gaps(self):
        self.data["work_item_ids"] = self.scheme()
        self.write_input()
        original = self.source.read_bytes()
        result = self.run_cli("--allocate-ids", "--output", self.output)
        self.assertEqual(result.returncode, 0, result.stderr)
        allocations = json.loads(result.stdout)
        self.assertEqual(allocations["status"], "proposed")
        self.assertEqual({item["key"]: item["id"] for item in allocations["items"]},
                         {"new": "UI-08", "old": "UI-07", "api": "API-03"})
        self.assertFalse(self.output.parent.exists())
        self.assertEqual(self.source.read_bytes(), original)

    def test_id_style_retains_existing_spelling_and_serials_can_grow(self):
        self.data["work_item_ids"] = {
            "registry": "docs/items.md", "separator": "", "digits": 2,
            "groups": [{"prefix": "TASK", "meaning": "工作"}], "reserved": ["TASK099"],
            "items": [{"key": "new", "prefix": "TASK", "title": "新增"},
                      {"key": "old", "prefix": "TASK", "title": "既有", "id": "TASK099"}],
        }
        self.write_input()
        result = self.run_cli("--allocate-ids")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([item["id"] for item in json.loads(result.stdout)["items"]], ["TASK100", "TASK099"])

    def test_corrected_id_is_reserved_even_when_no_longer_an_active_item(self):
        scheme = self.scheme()
        scheme["items"] = [scheme["items"][0]]
        self.data["work_item_ids"] = scheme
        self.write_input()
        result = self.run_cli("--allocate-ids")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["items"][0]["id"], "UI-08")

    def test_conflicting_id_claims_are_rejected_without_writes(self):
        scheme = self.scheme()
        invalid = [
            {**scheme, "digits": True},
            {**scheme, "reserved": ["UI-01", "UI-1"]},
            {**scheme, "items": [scheme["items"][1], {**scheme["items"][1], "key": "another"}]},
            {**scheme, "items": [scheme["items"][0], scheme["items"][0]]},
            {**scheme, "reserved": ["UNKNOWN-01"]},
            {**scheme, "items": [{"key": "bad", "prefix": "API", "title": "不符分類", "id": "UI-07"}]},
        ]
        for index, value in enumerate(invalid):
            with self.subTest(case=index):
                self.data["work_item_ids"] = value
                self.write_input()
                result = self.run_cli("--allocate-ids", "--output", self.output)
                self.assertEqual(result.returncode, 2, result.stdout)
                self.assertFalse(self.output.parent.exists())

    def test_heading_priority_keeps_important_prose_before_tables_and_details_after(self):
        self.data.update({
            "section_order": ["open_items", "source_authority", "read_by_task", "documentation"],
            "open_items": ["關鍵規格尚未確認"], "verification": ["既有 focused check"],
            "documentation": ["詳細紀錄維護方式"],
            "documentation_triggers": [{"trigger": "交付", "result": "更新受影響紀錄"}],
        })
        self.write_input()
        result = self.run_cli("--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        text = result.stdout
        self.assertLess(text.index("## 未確認事項"), text.index("## 依任務讀取"))
        self.assertLess(text.index("## 來源優先序"), text.index("## 依任務讀取"))
        self.assertLess(text.index("| 交付 |"), text.index("- 詳細紀錄維護方式"))
        self.assertIn("既有 focused check", text)
        self.assertIn(self.data["scope"][0], text)


if __name__ == "__main__":
    unittest.main()
