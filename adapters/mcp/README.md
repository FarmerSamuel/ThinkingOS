# MCP Adapter

Exposes a ThinkingOS execution as an MCP `tools/call` JSON-RPC request and
normalizes `structuredContent` or the compatible text fallback. A host can use
`tool_definition` to advertise the execution tool with input and output JSON
Schemas.

Production servers must validate inputs, enforce access control and rate limits,
sanitize outputs, request confirmation for sensitive operations, and retain
auditable tool-call records. These requirements follow the official
[MCP tools specification](https://modelcontextprotocol.io/specification/2025-06-18/server/tools).
