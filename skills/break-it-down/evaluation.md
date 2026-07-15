# Break It Down Evaluation

Score each dimension from 0 to 4 using `rubric.md`.

- **Coverage Score:** How fully the components represent the in-scope problem.
- **Distinctness Score:** How clearly sibling responsibilities are separated.
- **Tractability Score:** Whether leaf units are small enough for reliable analysis without becoming trivial.
- **Dependency Score:** Whether sequencing, coupling, and shared inputs are preserved.
- **Goal Alignment Score:** Whether the decomposition remains connected to the validated goal.

The **Overall Decomposition Score** is the rounded mean, capped at 2 if Coverage or Goal Alignment is below 2, or if a blocking dependency is omitted. Map the overall score to `evaluation.score`; report dimension scores as labeled reasoning entries.

Confidence is high only when the problem boundary, decomposition basis, and dependencies are supported by reliable inputs.
