# Adapter Protocol

## Boundary

An adapter is a deterministic translation boundary around the ThinkingOS
engine. It receives a skill identifier, compiled instructions, validated inputs,
reusable conversation state, and an optional output schema. It returns a
provider payload or normalizes a provider response.

## Invariants

- Thinking logic remains in `core/` and `skills/`.
- Model selection is explicit; adapters never silently choose a model.
- Credentials, authorization headers, and secrets are never accepted or stored.
- Network I/O, retry policy, rate limiting, and telemetry belong to the caller.
- Provider output is untrusted until parsed and schema-validated.
- Unknown or malformed response shapes fail closed with `AdapterError`.
- Provider-specific metadata must not be copied into conversation state
  implicitly.

## Capability labels

Capabilities describe the mapping, not a guarantee about every provider model:

- `structured-output`: maps the universal output schema when supported.
- `conversation-state`: supplies serialized ThinkingOS state to the provider.
- `system-instructions`: separates engine instructions from user inputs.
- `tool-protocol`: exposes ThinkingOS through a callable host protocol.

Applications must intersect adapter capabilities with the selected model or
host capabilities before execution.

## Error model

Invalid neutral requests, missing required routing options, malformed provider
responses, and non-object JSON outputs raise `AdapterError`. Transport and
provider HTTP errors are outside this package and should be converted by the
calling application into its own observable error types.

## Adding an adapter

Subclass `BaseAdapter`, publish immutable capabilities, keep mapping functions
side-effect free, document the official integration surface, and add contract
tests for successful mappings and malformed responses. Do not duplicate skill
validation or evaluation rules.
