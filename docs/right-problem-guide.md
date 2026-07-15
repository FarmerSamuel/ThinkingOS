# Right Problem Guide

`#RightProblem` helps determine whether the stated problem is the problem worth solving. Use it before solution generation, especially when a request begins with a preferred tool, an unsupported cause, a broad judgment, or an unclear success definition.

## The habit

Separate the frame into five parts:

1. **Current condition:** What is observed, for whom, and over what period?
2. **Goal:** What outcome should improve?
3. **Obstacle:** What condition plausibly explains the gap?
4. **Constraint:** What boundary governs the feasible space?
5. **Evidence and assumptions:** What is known, inferred, disputed, or missing?

The result is `Valid`, `Invalid`, or `Incomplete`. A fluent explanation does not make a frame valid.

## When to use it

- Before approving a project, product, policy, or major decision.
- When a team disagrees about causes or priorities.
- When repeated solutions do not improve the outcome.
- Before asking an AI system to recommend solutions.
- When a problem statement describes people rather than observable behavior or results.

## Practical techniques

### Clarify material ambiguity

Ask for a number, boundary, timeframe, owner, or condition when different interpretations would change the decision. Do not block harmless informal wording.

### Define observable success

Replace “launch the system” with the result the system is expected to improve. Given/When/Then may help describe operational scenarios, but ThinkingOS does not require a specific documentation syntax.

### Distinguish obstacle from constraint

Ask whether more resources, authority, time, or evidence would remove the condition. Treat the answer as a diagnostic hypothesis, not proof.

### Test alternative explanations

Ask what else could produce the same observation and what evidence would distinguish the explanations. Five Whys may deepen inquiry, but every causal link still requires validation.

### Reframe deliberately

Try inversion, scope, stakeholder, or timeframe lenses. Compare each alternative with the same evidence and stop when reframing no longer changes the decision.

## One-question conversation

ThinkingOS asks one high-impact question at a time. A useful opening is:

> What observable outcome should improve if this problem is solved?

The next question targets the unknown most likely to invalidate or materially reshape the frame.

## Common failure modes

- A solution is written as the problem: “We need a new CRM.”
- A symptom is repeated as its own cause.
- A goal describes activity rather than an outcome.
- A people judgment is used without observable evidence.
- Every boundary is treated as fixed.
- A checklist or causal chain is treated as proof.
- A downstream skill is started while the frame remains incomplete.

## Self-check

- Is the goal observable and independent of a preferred solution?
- Is the affected stakeholder and scope clear enough for this decision?
- Does evidence support the obstacle, or is it only plausible?
- Are obstacles, constraints, and assumptions separated?
- Has at least one credible alternative explanation been considered?
- Is the next step clarification, evidence collection, or another eligible skill?

## Related ThinkingOS resources

- [Problem-framing knowledge](https://github.com/FarmerSamuel/ThinkingOS/blob/main/knowledge/problem-framing.md)
- [Skill specification](skill-specification.md)
- [Evaluation model](evaluation-model.md)
- [Thinking graph](thinking-graph.md)

## Source notes

ThinkingOS uses cross-disciplinary thinking habits without claiming `#RightProblem` as an official Minerva habit. Minerva's current overview describes Habits of Mind and Foundational Concepts as transferable cognitive tools, and its published introduction notes that the catalog changes over time. The Five Whys is used here as an inquiry heuristic associated with Taiichi Ohno, not as automatic root-cause proof.

- [Minerva pedagogy](https://www.minerva.edu/pedagogy/)
- [Minerva HCs introduction](https://www.minerva.edu/public/media/enrollment-center/Minerva-HCs-Intro.pdf)
- [Institute for Healthcare Improvement: Five Whys](https://www.ihi.org/library/tools/5-whys-finding-root-cause)
