import json
import unittest

from adapters import AdapterError, AdapterRequest
from adapters.claude import ClaudeAdapter
from adapters.copilot import CopilotAdapter
from adapters.cursor import CursorAdapter
from adapters.gemini import GeminiAdapter
from adapters.mcp import MCPAdapter
from adapters.openai import OpenAIAdapter


OUTPUT = {"type": "object", "required": ["summary"], "properties": {"summary": {"type": "string"}}}


def request() -> AdapterRequest:
    return AdapterRequest(
        skill_id="right-problem",
        instructions="Validate before evaluating.",
        inputs={"goal": "Ship safely"},
        state={"currentGoal": "Ship safely"},
        output_schema=OUTPUT,
    )


class RequestTests(unittest.TestCase):
    def test_rejects_empty_skill(self) -> None:
        with self.assertRaises(AdapterError):
            AdapterRequest("", "instructions", {}).validate()

    def test_rejects_empty_instructions(self) -> None:
        with self.assertRaises(AdapterError):
            AdapterRequest("skill", "", {}).validate()


class ProviderMappingTests(unittest.TestCase):
    def test_openai_mapping(self) -> None:
        mapped = OpenAIAdapter().build_request(request(), model="deployment-model")
        self.assertEqual(mapped.operation, "responses.create")
        self.assertEqual(mapped.payload["text"]["format"]["type"], "json_schema")

    def test_openai_requires_model(self) -> None:
        with self.assertRaises(AdapterError):
            OpenAIAdapter().build_request(request())

    def test_openai_parses_nested_output(self) -> None:
        response = OpenAIAdapter().parse_response(
            {"output": [{"content": [{"type": "output_text", "text": '{"summary":"ok"}'}]}]}
        )
        self.assertEqual(response.output["summary"], "ok")

    def test_claude_mapping(self) -> None:
        mapped = ClaudeAdapter().build_request(request(), model="deployment-model", max_tokens=512)
        self.assertEqual(mapped.payload["messages"][0]["role"], "user")
        self.assertEqual(mapped.payload["max_tokens"], 512)

    def test_claude_rejects_invalid_max_tokens(self) -> None:
        with self.assertRaises(AdapterError):
            ClaudeAdapter().build_request(request(), model="deployment-model", max_tokens=0)

    def test_claude_parses_text_blocks(self) -> None:
        response = ClaudeAdapter().parse_response(
            {"content": [{"type": "text", "text": '{"summary":"ok"}'}]}
        )
        self.assertEqual(response.output["summary"], "ok")

    def test_gemini_mapping(self) -> None:
        mapped = GeminiAdapter().build_request(request(), model="deployment-model")
        self.assertEqual(mapped.operation, "models/deployment-model:generateContent")
        self.assertEqual(mapped.payload["generationConfig"]["responseMimeType"], "application/json")

    def test_gemini_reports_blocked_prompt(self) -> None:
        with self.assertRaisesRegex(AdapterError, "SAFETY"):
            GeminiAdapter().parse_response({"promptFeedback": {"blockReason": "SAFETY"}})


class MCPTests(unittest.TestCase):
    def test_mcp_mapping(self) -> None:
        mapped = MCPAdapter().build_request(request(), request_id="abc")
        self.assertEqual(mapped.payload["method"], "tools/call")
        self.assertEqual(mapped.payload["params"]["name"], "thinkingos_run")

    def test_mcp_parses_structured_content(self) -> None:
        response = MCPAdapter().parse_response(
            {"jsonrpc": "2.0", "id": 1, "result": {"structuredContent": {"summary": "ok"}}}
        )
        self.assertEqual(response.output, {"summary": "ok"})

    def test_mcp_parses_text_fallback(self) -> None:
        response = MCPAdapter().parse_response(
            {"result": {"content": [{"type": "text", "text": json.dumps({"summary": "ok"})}]}}
        )
        self.assertEqual(response.output["summary"], "ok")

    def test_mcp_rejects_protocol_error(self) -> None:
        with self.assertRaisesRegex(AdapterError, "bad request"):
            MCPAdapter().parse_response({"error": {"message": "bad request"}})

    def test_tool_definition_uses_custom_name(self) -> None:
        definition = MCPAdapter("custom_run").tool_definition({"type": "object"}, OUTPUT)
        self.assertEqual(definition["name"], "custom_run")

    def test_cursor_preserves_host_provenance(self) -> None:
        mapped = CursorAdapter().build_request(request())
        self.assertEqual(mapped.provider, "cursor")

    def test_copilot_preserves_host_provenance(self) -> None:
        parsed = CopilotAdapter().parse_response(
            {"result": {"structuredContent": {"summary": "ok"}}}
        )
        self.assertEqual(parsed.provider, "copilot")


class OutputSafetyTests(unittest.TestCase):
    def test_rejects_non_json_output(self) -> None:
        with self.assertRaises(AdapterError):
            OpenAIAdapter().parse_response({"output_text": "not-json"})

    def test_rejects_json_array_output(self) -> None:
        with self.assertRaises(AdapterError):
            OpenAIAdapter().parse_response({"output_text": "[]"})


if __name__ == "__main__":
    unittest.main()
