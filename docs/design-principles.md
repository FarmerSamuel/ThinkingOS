# ThinkingOS Skill Design Principles

## One skill, one thinking habit

Each skill develops or applies one primary thinking habit. A clear cognitive unit makes the skill understandable, testable, and reusable.

## One skill, one thinking problem

A skill should solve only one defined thinking problem. If a specification requires unrelated goals or evaluation methods, divide it into composable skills.

## Composable by contract

Skills exchange validated state and structured outputs through shared schemas. Composition must use explicit transition conditions rather than hidden orchestration assumptions.

## Non-overlapping responsibilities

Every skill owns a distinct purpose and decision boundary. Shared behavior belongs in the core framework or shared schemas, not duplicated across skills.

## Reusable logic

Logic rules should be explicit, deterministic where possible, and independent of presentation. Repeated reasoning operations should become shared framework capabilities.

## Reusable knowledge

Knowledge assets should be referenced rather than embedded repeatedly. Logic and knowledge remain separate so either can evolve without rewriting the other.

## Platform independence

Skills must not depend on a specific LLM, vendor, API, message format, tool protocol, or user interface. Platform-specific behavior belongs in adapters.

## Validation before evaluation

No skill should evaluate or recommend before checking input sufficiency, ambiguity, and logical consistency. Unknowns must be surfaced rather than silently completed.

## Transparent reasoning

Outputs distinguish facts, assumptions, evaluation, reasoning, and confidence. Authority, fluency, or certainty must not substitute for evidence.

## Testable specifications

Every rule and boundary should support a conformance test. Examples explain expected behavior; tests verify it.
