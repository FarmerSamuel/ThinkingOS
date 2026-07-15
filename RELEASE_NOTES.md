# ThinkingOS 1.0.0

ThinkingOS v1.0 is the first stable release of an AI-agnostic framework for
reusable, validation-first thinking. It establishes durable contracts from the
Core and Engine through Skills, Knowledge, SDK, and provider adapters.

## Highlights

- Thirteen released Thinking Skills cover problem framing, decomposition,
  constraints, gaps, analogy, heuristics, deep learning, association, learning
  planning, concept mapping, boundaries, complexity, and emergence.
- Every Skill ships with metadata, a schema-conforming definition, workflow,
  validation, evaluation, rubric, examples, at least ten cases, references, and
  its own changelog.
- The Python SDK discovers Skills, validates contracts, traverses dependencies,
  and serializes reusable conversation state.
- Deterministic adapters support OpenAI, Claude, Gemini, Cursor, GitHub Copilot,
  and MCP without embedding credentials, transport logic, or model choices.
- Automated validation covers JSON Schema, YAML, graph integrity, docs links,
  unit contracts, package builds, Markdown, and strict MkDocs output.

## Compatibility

Public SDK APIs and released framework contracts now follow Semantic Versioning.
Model identifiers and provider availability are deliberately not frozen by this
release. Applications must choose models explicitly and validate normalized
outputs against the universal Output Schema.

## Upgrade notes

This is the first stable release. Draft Skill packages at `0.1.0` are promoted
to `1.0.0` without changing their validation-first semantics. Consumers should
pin the framework version and consult individual Skill changelogs for future
contract changes.

## Known operational requirement

Repository administrators must select **GitHub Actions** as the Pages source in
repository settings before the documentation deployment job can publish. The
workflow safely skips deployment until that one-time setting is enabled.
