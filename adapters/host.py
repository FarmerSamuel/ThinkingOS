"""Shared mapping for editor and assistant hosts that consume MCP tools."""

from typing import Any, Mapping

from adapters.base import AdapterRequest, AdapterResponse, BaseAdapter, ProviderRequest
from adapters.mcp import MCPAdapter


class MCPHostAdapter(BaseAdapter):
    """Labels MCP requests for a specific host without changing the protocol."""

    def __init__(self, provider: str, tool_name: str = "thinkingos_run") -> None:
        self.provider = provider
        self._mcp = MCPAdapter(tool_name)

    @property
    def capabilities(self) -> frozenset[str]:
        return self._mcp.capabilities

    def build_request(self, request: AdapterRequest, **options: Any) -> ProviderRequest:
        mapped = self._mcp.build_request(request, **options)
        return ProviderRequest(self.provider, mapped.operation, mapped.payload)

    def parse_response(self, payload: Mapping[str, Any]) -> AdapterResponse:
        parsed = self._mcp.parse_response(payload)
        return AdapterResponse(parsed.output, self.provider, parsed.provider_metadata)
