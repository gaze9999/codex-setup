"""Focused Jev protocol, fallback, credential and portability checks; no live API."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock
from urllib import error

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "jev-evaluation" / "scripts" / "jev.py"
SPEC = importlib.util.spec_from_file_location("jev", SCRIPT)
j = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(j)


def response(values):
    return {"model": "jev-1.13.0", "answers": values, "usage": {"input_tokens": 12, "output_tokens": 4}}


class JevTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.environment = mock.patch.dict(os.environ, {"CODEX_HOME": str(self.root), "TYPESAFE_API_KEY": "test-key", "TYPESAFE_MODEL": "jev-latest"}, clear=True)
        self.environment.start()
        self.addCleanup(self.environment.stop)

    def input_file(self, value):
        path = self.root / "input with space.json"
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8-sig")
        return str(path)

    def main_result(self, arguments):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = j.main(arguments)
        return code, json.loads(output.getvalue())

    def test_all_three_answer_types_and_usage(self):
        questions = {
            "yes": {"type": "noul", "instructions": "Is it relevant?"},
            "kind": {"type": "choice", "instructions": "Which?", "criteria": {"a": None, "b": "Other"}},
            "level": {"type": "score", "instructions": "How much?", "criteria": ["Low", "High"]},
        }
        values = {
            "yes": {"type": "noul", "noul": 0.8},
            "kind": {"type": "choice", "choice": "a", "probabilities": {"a": 0.8, "b": 0.2}, "confidence": 0.6},
            "level": {"type": "score", "score": 0.2, "legend": {"0": "Low", "1": "High"}, "probabilities": {"0": 0.8, "1": 0.2}, "confidence": 0.6},
        }
        prepared = j.payload({"state": "text", "questions": questions}, "jev-latest")
        found = j.answers(response(values), prepared["questions"])
        self.assertEqual(found["answers"], values)
        self.assertEqual(found["usage"]["input_tokens"], 12)

    def test_invalid_request_types_and_criteria(self):
        invalid = [
            {"type": "unknown", "instructions": "Question"},
            {"type": "choice", "instructions": "Question", "criteria": []},
            {"type": "score", "instructions": "Question", "criteria": ["Only"]},
            {"type": "noul", "instructions": "Question", "criteria": {"maybe": "No"}},
            {"type": "noul", "instructions": "Question", "extra": "not supported"},
        ]
        for question in invalid:
            with self.subTest(question=question), self.assertRaises(j.Problem):
                j.payload({"state": "text", "questions": {"q": question}}, "jev-latest")

    def test_invalid_answers_and_invented_confidence(self):
        question = {"q": {"type": "noul", "instructions": "Question"}}
        for value in (True, float("nan"), -0.1, 1.1, "0.8"):
            with self.subTest(value=value), self.assertRaises(j.Problem):
                j.answers(response({"q": {"type": "noul", "noul": value}}), question)
        found = j.answers(response({"q": {"type": "noul", "noul": 0.8, "confidence": 0.99}}), question)
        self.assertNotIn("confidence", found["answers"]["q"])
        with self.assertRaises(j.Problem):
            j.answers(response({}), question)

    def test_choice_outside_rubric_and_missing_confidence_rejected(self):
        question = {"q": {"type": "choice", "instructions": "Which?", "criteria": {"a": None, "b": None}}}
        value = {"type": "choice", "choice": "other", "probabilities": {"a": 0.8, "b": 0.2}, "confidence": 0.6}
        with self.assertRaises(j.Problem):
            j.answers(response({"q": value}), question)
        value["choice"] = "a"
        del value["confidence"]
        with self.assertRaises(j.Problem):
            j.answers(response({"q": value}), question)

    def test_rank_retains_required_without_transmitting_it(self):
        data = {"query": "Validation", "candidates": [{"id": "must", "required": True, "text": "private governing material"}, {"id": "b", "text": "Theme"}, {"id": "a", "text": "Validation"}]}
        prepared, items = j.rank_request(data)
        self.assertNotIn("private governing material", json.dumps(prepared))
        result = j.rank_items(items, {"candidate_0": {"noul": 0.1}, "candidate_1": {"noul": 0.9}})
        self.assertEqual([item["id"] for item in result], ["must", "a", "b"])
        self.assertIsNone(result[0]["probability"])
        self.assertEqual([item["id"] for item in j.rank_items(items)], ["must", "b", "a"])

    def test_rank_rejects_duplicate_ids(self):
        with self.assertRaises(j.Problem):
            j.rank_request({"query": "Q", "candidates": [{"id": "a", "text": "one"}, {"id": "a", "text": "two"}]})

    def test_all_required_skips_credential_and_network(self):
        path = self.input_file({"query": "Q", "candidates": [{"id": "a", "required": True}]})
        with mock.patch.object(j, "load_key") as key, mock.patch.object(j, "call_api") as call:
            code, result = self.main_result(["rank", "--input", path])
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "skipped")
        key.assert_not_called()
        call.assert_not_called()

    def test_missing_credentials_preserves_ranked_candidate_ids(self):
        path = self.input_file({"query": "Q", "candidates": [{"id": "b", "text": "one"}, {"id": "a", "text": "two"}]})
        with mock.patch.object(j, "load_key", side_effect=j.Problem("missing_credential")), mock.patch.object(j, "call_api") as call:
            code, result = self.main_result(["rank", "--input", path])
        self.assertEqual(code, 1)
        self.assertEqual(result["status"], "fallback")
        self.assertEqual([item["id"] for item in result["candidates"]], ["b", "a"])
        self.assertTrue(all(item["probability"] is None for item in result["candidates"]))
        call.assert_not_called()

    def test_dry_run_accepts_utf8_bom_without_echoing_inputs(self):
        path = self.input_file({"query": "欄位驗證", "candidates": [{"id": "a", "text": "only approved excerpt"}]})
        with mock.patch.object(j, "load_key") as key, mock.patch.object(j, "call_api") as call:
            code, result = self.main_result(["rank", "--input", path, "--dry-run"])
        self.assertEqual(code, 0)
        self.assertNotIn("only approved excerpt", json.dumps(result))
        key.assert_not_called()
        call.assert_not_called()

    def test_authenticated_transport_uses_utf8_and_fixed_origin(self):
        raw = io.BytesIO(json.dumps(response({"q": {"type": "noul", "noul": 0.9}})).encode())
        opener = mock.Mock()
        opener.open.return_value = raw
        with mock.patch.object(j.request, "build_opener", return_value=opener):
            j.call_api("systemone", "test-key", {"state": "繁體中文"}, 8, 1)
        req = opener.open.call_args.args[0]
        self.assertEqual(req.full_url, j.API + "systemone")
        self.assertEqual(req.get_header("Authorization"), "Bearer test-key")
        self.assertEqual(json.loads(req.data)["state"], "繁體中文")
        self.assertIsNone(j.NoRedirect().redirect_request(None, None, 302, "", {}, "https://other.invalid"))

    def test_401_never_retries_or_prints_response_body(self):
        body = io.BytesIO(b"test-key private response body")
        failure = error.HTTPError(j.API, 401, "unauthorized", {}, body)
        opener = mock.Mock()
        opener.open.side_effect = failure
        path = self.input_file({"state": "public", "questions": {"q": {"type": "noul", "instructions": "Q"}}})
        with mock.patch.object(j.request, "build_opener", return_value=opener):
            code, result = self.main_result(["evaluate", "--input", path])
        self.assertEqual((code, result["reason"]), (1, "http_401"))
        self.assertEqual(opener.open.call_count, 1)
        self.assertNotIn("test-key", json.dumps(result))
        self.assertTrue(body.closed)

    def test_transient_retry_is_bounded_and_honors_short_retry_after(self):
        opener = mock.Mock()
        opener.open.side_effect = [error.HTTPError(j.API, 429, "limit", {"Retry-After": "1"}, io.BytesIO()), io.BytesIO(b'{"models":[]}')]
        with mock.patch.object(j.request, "build_opener", return_value=opener), mock.patch.object(j.time, "sleep") as sleep:
            self.assertEqual(j.call_api("models", "test-key", None, 8, 1), {"models": []})
        self.assertEqual(opener.open.call_count, 2)
        sleep.assert_called_once_with(1)

    def test_long_retry_after_returns_control_without_waiting(self):
        opener = mock.Mock()
        opener.open.side_effect = error.HTTPError(j.API, 529, "busy", {"Retry-After": "120"}, io.BytesIO())
        with mock.patch.object(j.request, "build_opener", return_value=opener), mock.patch.object(j.time, "sleep") as sleep, self.assertRaisesRegex(j.Problem, "http_529"):
            j.call_api("models", "test-key", None, 8, 1)
        self.assertEqual(opener.open.call_count, 1)
        sleep.assert_not_called()

    def test_network_and_malformed_response_fallback(self):
        for failure in (TimeoutError(), error.URLError("offline")):
            opener = mock.Mock()
            opener.open.side_effect = failure
            with mock.patch.object(j.request, "build_opener", return_value=opener), mock.patch.object(j.time, "sleep"), self.assertRaises(j.Problem):
                j.call_api("models", "test-key", None, 8, 1)
            self.assertEqual(opener.open.call_count, 2)
        opener.open.side_effect = None
        opener.open.return_value = io.BytesIO(b'{"bad":NaN}')
        with mock.patch.object(j.request, "build_opener", return_value=opener), self.assertRaisesRegex(j.Problem, "invalid_response"):
            j.call_api("models", "test-key", None, 8, 1)

    def test_key_file_resolution_and_refuse_repository_storage(self):
        path = j.key_path()
        self.assertEqual(path, self.root / "credentials" / "jev.key")
        j.save_key(path, "file-key")
        with mock.patch.dict(os.environ, {"TYPESAFE_API_KEY": ""}), mock.patch.object(j.sys, "platform", "darwin"):
            self.assertEqual(j.load_key(path), ("file-key", "key_file"))
        with self.assertRaisesRegex(j.Problem, "credential_exists"):
            j.save_key(path, "new-key")
        j.save_key(path, "new-key", replace=True)
        checkout = self.root / "checkout"
        (checkout / ".git").mkdir(parents=True)
        with self.assertRaisesRegex(j.Problem, "credential_inside_repository"):
            j.save_key(checkout / "secret.key", "test-key")

    def test_posix_private_file_permissions_required(self):
        path = mock.Mock()
        path.is_file.return_value = True
        path.stat.return_value = SimpleNamespace(st_mode=0o100644, st_size=8)
        with mock.patch.object(j, "os", SimpleNamespace(name="posix", environ={})), mock.patch.object(j.sys, "platform", "darwin"), mock.patch.object(j, "key_path", return_value=path), self.assertRaisesRegex(j.Problem, "credential_file_permissions"):
            j.load_key()

    def test_unreadable_key_path_is_not_missing_credential(self):
        path = mock.Mock()
        path.stat.side_effect = PermissionError("private diagnostic canary")
        with mock.patch.object(j, "os", SimpleNamespace(name="posix", environ={})), mock.patch.object(j.sys, "platform", "darwin"), mock.patch.object(j, "key_path", return_value=path), self.assertRaisesRegex(j.Problem, "^credential_file_unreadable$"):
            j.load_key()

    def test_setup_key_requires_interactive_terminal_and_hides_key(self):
        with mock.patch.object(j.sys.stdin, "isatty", return_value=False), mock.patch.object(j.getpass, "getpass") as prompt:
            code, result = self.main_result(["setup-key"])
        self.assertEqual((code, result["reason"]), (1, "interactive_terminal_required"))
        prompt.assert_not_called()
        with mock.patch.object(j.sys.stdin, "isatty", return_value=True), mock.patch.object(j.getpass, "getpass", return_value="setup-test-key"):
            code, result = self.main_result(["setup-key"])
        self.assertEqual(code, 0)
        self.assertNotIn("setup-test-key", json.dumps(result))

    def test_relocated_script_runs_from_unrelated_project(self):
        installed = self.root / "Mac compatible folder 空白" / "jev-evaluation"
        shutil.copytree(SCRIPT.parents[1], installed)
        project = self.root / "other project"
        project.mkdir()
        run = subprocess.run([sys.executable, "-B", str(installed / "scripts" / "jev.py"), "doctor"], cwd=project, capture_output=True, env=os.environ.copy(), check=False)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertTrue(json.loads(run.stdout)["credential_available"])
        self.assertNotIn(b"test-key", run.stdout)

    def test_invalid_or_oversized_input_and_timeout_do_not_call_api(self):
        path = self.root / "large.json"
        path.write_bytes(b" " * (j.MAX_BYTES + 1))
        with mock.patch.object(j, "call_api") as call:
            self.assertEqual(self.main_result(["evaluate", "--input", str(path)])[1]["reason"], "input_too_large")
            self.assertEqual(self.main_result(["doctor", "--timeout", "nan"])[1]["reason"], "invalid_timeout")
            call.assert_not_called()

    def test_unsupported_python_stops_before_credential_or_api_access(self):
        with mock.patch.object(j.sys, "version_info", (3, 9)), mock.patch.object(j, "load_key") as key, mock.patch.object(j, "call_api") as call:
            code, result = self.main_result(["doctor", "--online"])
        self.assertEqual((code, result["reason"]), (1, "python_3_10_required"))
        key.assert_not_called()
        call.assert_not_called()


if __name__ == "__main__":
    unittest.main()
