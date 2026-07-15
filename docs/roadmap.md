# ThinkingOS Roadmap

ThinkingOS v1.0 completes the original five-phase roadmap. Future work follows
the compatibility policy and priorities in [Future Work](future-work.md).

## v1.0 milestone status

| Phase | Outcome | Status |
| --- | --- | --- |
| 1. Framework | Core, Engine, specifications, schemas, language, and graph | Complete |
| 2. Core Skills | Thirteen conforming, tested Thinking Skills | Complete |
| 3. Knowledge Engine | Reusable, cited knowledge separated from Skill logic | Complete |
| 4. Multi-AI Adapters | OpenAI, Claude, Gemini, Cursor, Copilot, and MCP mappings | Complete |
| 5. ThinkingOS SDK | Registry, graph, Skill validation, state, tests, and packaging | Complete |

## Phase 1 - Framework

Delivered the universal persona, philosophy, principles, conversation state,
validation model, reasoning Engine, Skill lifecycle, Thinking Language, JSON
Schemas, Registry, and directed Thinking Graph.

## Phase 2 - Core Skills

Delivered Right Problem, Break It Down, Constraints, Gap Analysis, Analogy,
Heuristic, Deep Processing, Make Association, Learning Triangle, Mind Map,
Boundary, Complexity, and Emergence. Each package follows the official Skill
Specification and has versioned tests and evaluation criteria.

## Phase 3 - Knowledge Engine

Delivered reusable foundations for critical thinking, problem solving, decision
making, and systems thinking, plus a shared glossary and source policy. Knowledge
remains replaceable without changing Skill logic.

## Phase 4 - Multi-AI Adapters

Delivered a provider-neutral adapter contract, fail-closed response parsing,
model API mappings, and MCP host bridges. Credentials, network I/O, model choice,
and provider lifecycle remain outside the reasoning framework.

## Phase 5 - ThinkingOS SDK

Delivered a Python 3.11+ SDK for Registry loading, deterministic graph traversal,
Skill discovery and JSON Schema validation, reusable conversation state, and
provider payload adapters. CI verifies tests and distributable package builds.

## Release policy

Roadmap completion does not eliminate lifecycle governance. New work moves
through `planned`, `draft`, `review`, `testing`, `released`, and `deprecated`.
Released public contracts follow Semantic Versioning and require migration notes
for breaking changes.
