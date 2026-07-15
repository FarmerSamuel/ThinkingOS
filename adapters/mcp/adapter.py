"""MCP tools/call mapping for the ThinkingOS execution contract."""

from typing import Any, Mapping

from adapters.base import AdapterError, AdapterRequest, AdapterResponse, BaseAdapter, ProviderRequest


class MCPAdapter(BaseAdapter):
    provider = "mcp"

    def __init__(self, tool_name: str = "thinkingos_run") -> None:
        if not tool_name.strip():
            raise AdapterError("tool_name must not be empty")
        self.tool_name = tool_name

    @property
    def capabilities(self) -> frozenset[str]:
        return frozenset({"structured-output", "conversation-state", "tool-protocol"})

    def build_request(self, request: AdapterRequest, **options: Any) -> ProviderRequest:
        request.validate()
        arguments = request.context()
        arguments["instructions"] = request.instructions
        if request.output_schema is not None:
            arguments["outputSchema"] = dict(request.output_schema)
        payload = {
            "jsonrpc": "2.0",
            "id": options.get("request_id", 1),
            "method": "tools/call",
            "params": {"name": self.tool_name, "arguments": arguments},
        }
        return ProviderRequest(self.provider, "tools/call", payload)

    def parse_response(self, payload: Mapping[str, Any]) -> AdapterResponse:
        if "error" in payload:
            error = payload["error"]
            message = error.get("message", "unknown protocol error") if isinstance(error, Mapping) else str(error)
            raise AdapterError(f"MCP protocol error: {message}")
        result = payload.get("result")
        if not isinstance(result, Mapping):
            raise AdapterError("MCP response contains no result")
        if result.get("isError"):
            raise AdapterError("MCP tool execution failed")
        structured = result.get("structuredContent")
        if structured is None:
            text_parts = [
                item.get("text", "")
                for item in result.get("content", [])
                if isinstance(item, Mapping) and item.get("type") == "text"
            ]
            structured = "".join(text_parts)
        return AdapterResponse(self.decode_json(structured), self.provider, {"requestId": payload.get("id")})

    def tool_definition(self, input_schema: Mapping[str, Any], output_schema: Mapping[str, Any]) -> dict[str, Any]:
        return {
            "name": self.tool_name,
            "title": "Run a ThinkingOS Skill",
            "description": "Validate and execute one registered ThinkingOS thinking skill.",
            "inputSchema": dict(input_schema),
            "outputSchema": dict(output_schema),
        }
