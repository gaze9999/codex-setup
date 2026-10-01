from pathlib import Path
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills/jev-evaluation/scripts"))
try:
    from mcp import Client
except ModuleNotFoundError as exc:
    if exc.name != "mcp":
        raise
    Client = None
if Client is not None:
    import mcp_server as server


@unittest.skipIf(Client is None, "Run MCP tests with the isolated SDK runtime")
class MCPTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.env = mock.patch.dict(os.environ, {"TYPESAFE_API_KEY": "test-key", "TYPESAFE_MODEL": "jev-latest"})
        self.env.start()
        self.addCleanup(self.env.stop)

    async def call(self, name, arguments):
        async with Client(server.build_server()) as client:
            result = await client.call_tool(name, arguments)
            return result

    async def test_discovery_exposes_only_bounded_tools_without_credential_arguments(self):
        async with Client(server.build_server()) as client:
            tools = (await client.list_tools()).tools
        self.assertEqual(sorted(tool.name for tool in tools), ["jev_evaluate", "jev_rank", "jev_status"])
        for tool in tools:
            self.assertNotIn("key", tool.input_schema["properties"])
            self.assertTrue(tool.annotations.read_only_hint)

    async def test_required_candidates_do_not_read_key_or_call_provider(self):
        with mock.patch.object(server.jev, "load_key") as key, mock.patch.object(server.jev, "call_api") as api:
            result = await self.call("jev_rank", {"query": "Q", "candidates": [{"id": "must", "required": True}]})
        self.assertFalse(result.is_error)
        self.assertEqual(result.structured_content["status"], "skipped")
        key.assert_not_called()
        api.assert_not_called()

    async def test_rank_preserves_all_ids_and_omits_required_text_from_api(self):
        response = {"model": "jev-test", "answers": {"candidate_0": {"type": "noul", "noul": 0.1}, "candidate_1": {"type": "noul", "noul": 0.9}}, "usage": {"input_tokens": 20, "output_tokens": 2}}
        with mock.patch.object(server.jev, "call_api", return_value=response) as api:
            result = await self.call("jev_rank", {"query": "Q", "candidates": [{"id": "must", "required": True, "text": "private canary"}, {"id": "b", "text": "B"}, {"id": "a", "text": "A"}]})
        self.assertEqual([item["id"] for item in result.structured_content["candidates"]], ["must", "a", "b"])
        self.assertNotIn("private canary", str(api.call_args))
        self.assertNotIn("test-key", str(result.structured_content))

    async def test_missing_key_returns_original_order(self):
        with mock.patch.object(server.jev, "load_key", side_effect=server.jev.Problem("missing_credential")):
            result = await self.call("jev_rank", {"query": "Q", "candidates": [{"id": "b", "text": "B"}, {"id": "a", "text": "A"}]})
        self.assertEqual(result.structured_content["reason"], "missing_credential")
        self.assertEqual([item["id"] for item in result.structured_content["candidates"]], ["b", "a"])

    async def test_typed_evaluation_uses_same_validated_provider_result(self):
        response = {"model": "jev-test", "answers": {"q": {"type": "choice", "choice": "a", "probabilities": {"a": 0.9, "b": 0.1}, "confidence": 0.7}}, "usage": {"input_tokens": 20, "output_tokens": 2}}
        with mock.patch.object(server.jev, "call_api", return_value=response):
            result = await self.call("jev_evaluate", {"state": "Public", "questions": {"q": {"type": "choice", "instructions": "Q", "criteria": {"a": "A", "b": "B"}}}})
        self.assertEqual(result.structured_content["answers"]["q"]["choice"], "a")

    async def test_invalid_model_and_duplicate_ids_do_not_call_provider(self):
        with mock.patch.object(server.jev, "call_api") as api:
            result = await self.call("jev_rank", {"query": "Q", "model": "other", "candidates": [{"id": "a", "text": "A"}]})
            duplicate = await self.call("jev_rank", {"query": "Q", "candidates": [{"id": "a", "text": "A"}, {"id": "a", "text": "B"}]})
        self.assertEqual(result.structured_content["reason"], "invalid_model")
        self.assertEqual(duplicate.structured_content["reason"], "invalid_rank_input")
        api.assert_not_called()

    async def test_invalid_required_boolean_is_rejected_by_tool_schema(self):
        with mock.patch.object(server.jev, "call_api") as api:
            result = await self.call("jev_rank", {"query": "Q", "candidates": [{"id": "a", "required": "true"}]})
        self.assertTrue(result.is_error)
        api.assert_not_called()

    async def test_local_status_never_calls_provider(self):
        with mock.patch.object(server.jev, "call_api") as api:
            result = await self.call("jev_status", {})
        self.assertTrue(result.structured_content["credential_available"])
        self.assertNotIn("test-key", str(result.structured_content))
        api.assert_not_called()


if __name__ == "__main__":
    unittest.main()
