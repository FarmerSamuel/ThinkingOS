# ThinkingOS Skill Specification

## Status and scope

This document defines the platform-independent contract for every ThinkingOS Skill. A skill is a reusable thinking capability that develops or applies one thinking habit. It is not a model prompt, user interface, provider integration, or collection of domain answers.

Conforming skills must define every section below. A section may explicitly state that no items apply, but it must not be silently omitted.

## Standard skill structure

### 1. Metadata

Provides stable identity and lifecycle information: name, version, description, status, authorship, tags, and compatibility information. Metadata enables discovery, versioning, validation, and composition without interpreting prose.

### 2. Purpose

Defines the single thinking problem the skill addresses, the outcome it enables, and its scope boundaries. The purpose must explain when the skill should and should not be used.

### 3. Thinking Habit

Names the reusable cognitive behavior the skill develops or applies. One skill must represent one primary thinking habit.

### 4. Thinking Elements

Lists the concepts or units of thought the skill examines, such as claims, assumptions, evidence, constraints, alternatives, criteria, or consequences. Elements describe what is reasoned about, not how a platform stores it.

### 5. Required Inputs

Declares the information necessary to run the skill, including type, meaning, necessity, and accepted constraints. Inputs must not depend on a particular LLM message format.

### 6. Validation Rules

Defines checks applied before analysis: presence, format, relevance, ambiguity, sufficiency, and consistency. Each rule must identify its failure condition and whether it blocks evaluation or permits a disclosed assumption.

### 7. Logic Rules

Defines the ordered, testable reasoning operations used by the skill. Rules must be explicit enough to reproduce across compatible implementations and must not rely on hidden model behavior.

### 8. Evaluation Criteria

Defines how the quality of the user's thinking or supplied material is assessed. Criteria should map to observable evidence and the shared evaluation model rather than reward agreement with the system.

### 9. Conversation Rules

Defines interaction behavior, including question order, clarification thresholds, turn size, and when to pause. Questions should be decision-relevant, neutral, and limited to what materially improves the evaluation.

### 10. Output Schema

Declares the structured result produced by the skill. Outputs must conform to `schemas/output.schema.json`; skill-specific additions must be documented and must preserve the universal fields.

### 11. Never Rules

Lists prohibited behavior and invalid conclusions specific to the skill, in addition to the ThinkingOS core principles. Never Rules create enforceable safety and scope boundaries.

### 12. Next Skill

Defines optional transitions to other skills, the conditions for each transition, and the reason the transition advances the current goal. A skill must not invoke a follow-on skill merely to extend the interaction.

### 13. References

Identifies standards, research, frameworks, or internal specifications that inform the skill. References must include enough provenance to distinguish external evidence from project conventions.

### 14. Examples

Provides representative, platform-neutral input and expected-output cases. Examples illustrate the contract but do not replace validation rules or tests.

### 15. Tests

Defines conformance cases for valid inputs, invalid inputs, ambiguity, boundary conditions, logic rules, output structure, and Never Rules. Tests should be deterministic wherever the contract permits.

## Conformance requirements

A conforming skill must:

1. Validate against `schemas/skill.schema.json`.
2. Follow the core validation and logic-engine contracts.
3. Produce an output compatible with `schemas/output.schema.json`.
4. Use the shared evaluation model and `schemas/evaluation.schema.json` when evaluating user thinking.
5. Keep provider adapters, model settings, and interface behavior outside the skill definition.
6. Declare extensions explicitly and preserve backward compatibility within a major version.
