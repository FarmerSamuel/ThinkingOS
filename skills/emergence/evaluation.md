# Emergence Evaluation

Score each dimension from 0 to 4:

- **PatternEvidence Score:** Evaluates patternevidence.
- **InteractionBasis Score:** Evaluates interactionbasis.
- **LevelDistinction Score:** Evaluates leveldistinction.
- **AlternativeTesting Score:** Evaluates alternativetesting.
- **PredictiveUse Score:** Evaluates predictiveuse.

The overall score is the rounded mean, capped at 2 when a blocking input, dependency, contradiction, or core logic failure remains. Map it to `evaluation.score`; include observations supporting every dimension in `reasoning`.

Confidence reflects evidence quality, input completeness, and alternative testing—not fluency or agreement.
