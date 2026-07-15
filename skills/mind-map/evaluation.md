# Mind Map Evaluation

Score each dimension from 0 to 4:

- **Coverage Score:** Evaluates coverage.
- **Hierarchy Score:** Evaluates hierarchy.
- **LinkValidity Score:** Evaluates linkvalidity.
- **Readability Score:** Evaluates readability.
- **GoalAlignment Score:** Evaluates goalalignment.

The overall score is the rounded mean, capped at 2 when a blocking input, dependency, contradiction, or core logic failure remains. Map it to `evaluation.score`; include observations supporting every dimension in `reasoning`.

Confidence reflects evidence quality, input completeness, and alternative testing—not fluency or agreement.
