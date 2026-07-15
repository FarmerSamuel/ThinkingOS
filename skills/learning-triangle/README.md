# Learning Triangle

`#LearningTriangle` is a platform-independent ThinkingOS Skill. Balance explanation, practice, and feedback into a testable learning loop.

## Purpose

Convert understanding gaps into cycles of explanation, application, and correction. This skill does not generate unvalidated solutions or contain provider-specific behavior.

## Inputs

- `elaboratedConcepts` — ElaboratedConcepts input.
- `understandingGaps` — UnderstandingGaps input.
- `learningGoal` — LearningGoal input.

## Outputs

- `LearningPlan`
- `PracticeLoop`
- `FeedbackCriteria`

## Workflow

Validate inputs → identify elements → apply logic rules → evaluate reasoning → generate output → recommend a valid next skill.

## Evaluation

The skill evaluates GoalAlignment, Balance, PracticeQuality, FeedbackQuality, Adaptability on a 0–4 scale. Overall score maps to `evaluation.score`; dimension scores are labeled reasoning entries.

## Usage

Invoke only when dependencies (deep-processing) are satisfied by registered outputs or validated equivalents. See `workflow.md` and `examples.md`.
