# Claude Adapter

Maps ThinkingOS requests to Anthropic's Messages API. Instructions are placed in
the top-level `system` field and the serialized skill context becomes one user
message. The caller supplies the model, transport, and credentials.

See the official [Messages API reference](https://platform.claude.com/docs/en/api/messages).
