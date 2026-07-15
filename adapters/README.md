# ThinkingOS Adapters

Adapters translate the provider-neutral ThinkingOS execution contract into a
model API or host protocol. They do not contain thinking logic, make network
requests, select models, or manage credentials.

## Contract

1. Construct an `AdapterRequest` from a validated skill and conversation state.
2. Call `build_request` to obtain a serializable `ProviderRequest`.
3. Send that payload using an application-owned client.
4. Pass the provider response to `parse_response`.
5. Validate the normalized output against `schemas/output.schema.json`.

The separation keeps retries, authentication, transport, observability, and
data-retention decisions in the host application. See
[`adapter-protocol.md`](adapter-protocol.md) for invariants and extension rules.

## Supported integrations

| Adapter | Integration surface |
| --- | --- |
| OpenAI | Responses API |
| Claude | Messages API |
| Gemini | GenerateContent API |
| Cursor | MCP host bridge |
| Copilot | MCP host bridge |
| MCP | JSON-RPC tool server |

Provider capabilities change over time. Callers must explicitly supply model
identifiers and remain responsible for checking provider availability.
