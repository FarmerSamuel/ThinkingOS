"""Cursor MCP host adapter."""

from adapters.host import MCPHostAdapter


class CursorAdapter(MCPHostAdapter):
    def __init__(self, tool_name: str = "thinkingos_run") -> None:
        super().__init__("cursor", tool_name)
