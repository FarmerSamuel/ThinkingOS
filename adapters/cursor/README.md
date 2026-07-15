# Cursor Adapter

Cursor is treated as an MCP host, not as a model provider. This adapter emits
the same standards-based `tools/call` request as the MCP adapter while retaining
`cursor` as provenance in normalized responses. Configure the ThinkingOS MCP
server in Cursor and let the host own model selection and user authorization.

See Cursor's official [MCP documentation](https://docs.cursor.com/context/model-context-protocol).
