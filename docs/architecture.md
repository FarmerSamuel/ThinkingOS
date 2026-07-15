# ThinkingOS Architecture

## Overview

ThinkingOS uses a layered architecture so reasoning behavior remains reusable, testable, and independent from AI providers or interfaces.

```text
Core
  ↓
Engine
  ↓
Specification
  ↓
Skill
  ↓
Knowledge
  ↓
Adapters
```

The diagram shows dependency direction: lower layers use contracts established above them. Cross-layer access should occur only through explicit interfaces and schemas.

## Layers

### Core

Defines the universal persona, philosophy, principles, validation expectations, logic contract, output format, workflow, questioning style, and conversation state. Core establishes behavior shared by all ThinkingOS implementations.

Core must not contain skill-specific methods, domain knowledge, or platform integration.

### Engine

Executes the shared reasoning pipeline. It coordinates input collection, validation, missing-information detection, element evaluation, logic rules, reasoning evaluation, output generation, and skill transition recommendations.

The Engine controls execution order but does not invent a skill's rules or domain facts.

### Specification

Defines the formal contracts for skills, evaluations, outputs, and ThinkingOS Language. Schemas and documentation make conformance testable across implementations.

The Specification describes what valid components contain, not how a particular runtime implements them.

### Skill

Encapsulates one thinking habit and one thinking problem. A skill declares its inputs, validation rules, logic rules, evaluation criteria, conversation rules, output contract, tests, and allowed transitions.

Skills compose through shared state and schemas and must not duplicate Core or Engine responsibilities.

### Knowledge

Provides reusable evidence, concepts, taxonomies, and reference material that skills may consult. Knowledge is versioned and traceable, and remains separate from logic so either can evolve independently.

Knowledge must not silently override validation or determine conclusions without an applicable skill rule.

### Adapters

Connect ThinkingOS to LLMs, APIs, storage, user interfaces, tools, and other execution environments. Adapters translate platform formats into shared contracts and translate structured results back to the host platform.

Provider credentials, model settings, transport details, and interface behavior belong only in this layer.

## Architectural constraints

- Dependencies flow through documented contracts; platform details do not leak upward.
- Core and Specification remain AI-agnostic.
- The Engine invokes skill-declared behavior but does not embed domain-specific logic.
- Skills reference knowledge rather than copying it.
- Adapters may vary without changing skill semantics.
- Every layer is independently versionable and testable.
