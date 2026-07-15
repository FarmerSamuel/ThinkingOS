# ThinkingOS Reasoning Engine

## Purpose

The ThinkingOS Engine is the shared, AI-agnostic execution contract for every Thinking Skill. It coordinates validation, logic, evaluation, output, and skill transitions without embedding domain knowledge, provider behavior, or skill-specific rules.

## Generic execution pipeline

```text
Collect Inputs
  ↓
Validate Inputs
  ↓
Detect Missing Information
  ↓
Evaluate Thinking Elements
  ↓
Run Logic Rules
  ↓
Evaluate Reasoning
  ↓
Generate Evaluation
  ↓
Generate Output
  ↓
Recommend Next Skill
```

### 1. Collect Inputs

Capture the current goal, skill inputs, relevant conversation state, evidence, assumptions, constraints, and context. Preserve provenance and distinguish user-provided information from system-derived assumptions.

**Exit condition:** Inputs are normalized into the active skill's declared input contract.

### 2. Validate Inputs

Apply the skill's validation rules and the shared validation framework. Check type, presence, relevance, ambiguity, internal consistency, and scope compatibility before analysis begins.

**Exit condition:** Validation is classified as ready, ready with disclosed assumptions, or needs clarification.

### 3. Detect Missing Information

Identify unknowns that could materially affect the evaluation or conclusion. Separate blocking gaps from non-blocking limitations and prioritize the smallest decision-relevant question.

**Exit condition:** Blocking gaps produce a clarification request; non-blocking gaps are recorded for the output.

### 4. Evaluate Thinking Elements

Inspect the elements declared by the active skill, such as goals, claims, assumptions, evidence, obstacles, constraints, criteria, or alternatives. Maintain the semantic boundaries defined by the skill.

**Exit condition:** Each required element has an evidence-backed observation or an explicit unknown status.

### 5. Run Logic Rules

Apply the skill's ordered logic rules to the validated elements. Record dependencies, rule outcomes, exceptions, and disclosed assumptions. Rules must be reproducible and must not rely on hidden provider behavior.

**Exit condition:** Every applicable rule has a recorded result or a documented reason it could not run.

### 6. Evaluate Reasoning

Assess input quality, logic quality, completeness, consistency, and actionability using the shared evaluation model. Detect unsupported inference, contradiction, weak causality, or untested alternatives.

**Exit condition:** Dimension-level findings and confidence factors are available.

### 7. Generate Evaluation

Transform the reasoning findings into the universal evaluation structure: score, strengths, weaknesses, missing information, logical issues, recommendation, and confidence.

**Exit condition:** The evaluation conforms to `schemas/evaluation.schema.json`.

### 8. Generate Output

Produce a concise, transparent result containing the summary, evaluation, reasoning, assumptions, missing information, questions, next step, and confidence.

**Exit condition:** The result conforms to `schemas/output.schema.json` and preserves material uncertainty.

### 9. Recommend Next Skill

Evaluate the active skill's declared transition conditions. Recommend at most the most useful next skill when it materially advances the current goal; otherwise recommend a direct action, clarification, or no transition.

**Exit condition:** Conversation state records the next skill or explicitly records that no skill transition is needed.

## Execution rules

- A later stage must not bypass an unresolved blocking result from an earlier stage.
- Validation and missing-information detection may return execution to input collection.
- Logic or reasoning failures may return execution to element evaluation.
- Every stage updates reusable conversation state without silently rewriting prior facts.
- Implementations may optimize execution, but observable behavior must preserve this pipeline's ordering and guarantees.
