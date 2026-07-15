# ThinkingOS Roadmap

## Guiding principles

The roadmap prioritizes stable contracts before capabilities and capabilities before integrations. Dates are intentionally omitted: phases advance when their exit criteria are met, not when an arbitrary schedule expires.

All planned work remains AI-agnostic at the Core, Engine, Specification, Skill, and Knowledge layers.

## Phase 1 — Framework

Establish the durable foundations of ThinkingOS.

### Scope

- Core persona, philosophy, principles, validation, logic, output, and conversation state.
- Shared reasoning Engine and architecture.
- Skill, evaluation, output, and Thinking Language specifications.
- Skill Registry, dependency graph, lifecycle, and governance documentation.

### Exit criteria

- Core contracts are internally consistent and versioned.
- Schemas validate representative fixtures.
- Registry dependencies are complete, acyclic, and reviewable.

## Phase 2 — Core Skills

Implement and validate the initial set of reusable thinking habits.

### Scope

- Problem framing, decomposition, constraints, and gap analysis.
- Analogy, heuristics, deep processing, and association.
- Learning, mapping, boundary, complexity, and emergence skills.
- Skill-specific examples, tests, evaluations, and lifecycle metadata.

### Exit criteria

- Each released skill conforms to the Skill Specification.
- Cross-skill inputs and outputs pass integration tests.
- No skill duplicates another skill's primary responsibility.

## Phase 3 — Knowledge Engine

Create reusable, traceable knowledge infrastructure separate from skill logic.

### Scope

- Knowledge asset format, provenance, versioning, and quality criteria.
- Retrieval and relevance contracts independent of a specific model or database.
- Knowledge-to-skill interfaces and citation requirements.

### Exit criteria

- Knowledge can be updated without changing skill logic.
- Skills can validate source provenance, relevance, and compatibility.
- Reference fixtures support deterministic conformance tests.

## Phase 4 — Multi-AI Adapters

Connect ThinkingOS to multiple AI and non-AI execution environments without changing framework semantics.

### Scope

- Adapter interface and capability negotiation.
- Provider-neutral state, tool, error, and output mappings.
- Conformance suites for representative platforms.

### Exit criteria

- At least two independent adapters produce schema-compatible behavior.
- Platform limitations are explicit and do not leak into skill definitions.
- Credentials and provider configuration remain isolated in adapters.

## Phase 5 — ThinkingOS SDK

Package the framework for application developers and integrators.

### Scope

- Registry discovery, schema validation, graph traversal, and state management APIs.
- Skill authoring, testing, packaging, and migration tools.
- Reference runtime, documentation, and integration examples.

### Exit criteria

- Developers can build, validate, compose, and run skills through stable APIs.
- The SDK enforces version, dependency, and output contracts.
- A documented compatibility policy supports independent ecosystem development.

## Status model

Roadmap items move through `planned`, `draft`, `review`, `testing`, `released`, and `deprecated` according to the Skill Lifecycle. Inclusion in this roadmap or the Registry does not imply implementation or release.
