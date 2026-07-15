"""GitHub Copilot MCP host adapter."""

from adapters.host import MCPHostAdapter


class CopilotAdapter(MCPHostAdapter):
    def __init__(self, tool_name: str = "thinkingos_run") -> None:
        super().__init__("copilot", tool_name)
