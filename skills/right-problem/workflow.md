# Right Problem Workflow

## Entry condition

Run the skill when a user presents a problem, asks for a solution, or needs to determine whether an apparent problem is correctly framed.

## Flow

### 1. Collect the frame

Capture the problem statement, desired goal, supporting context, evidence, known constraints, stakeholders, and prior attempts. Do not reinterpret them yet.

### 2. Validate required inputs

Confirm that the problem statement and goal are present, meaningful, and distinguishable. Apply `validation.md` before any evaluation.

### 3. Isolate thinking elements

Separate:

- **Goal:** The desired outcome.
- **Obstacle:** The condition preventing or limiting the goal.
- **Constraint:** A boundary governing what can change.
- **Assumption:** A claim accepted without sufficient validation.
- **Evidence:** Information supporting or challenging the frame.

### 4. Test the problem relationship

Evaluate whether the stated obstacle plausibly explains the gap between the current condition and goal. Look for symptoms mistaken for causes, circular definitions, hidden solution assumptions, and contradictions.

### 5. Generate clarification

If a blocking gap or ambiguity exists, ask the single question most likely to change the problem frame. Remain in `%CollectingInputs` or `%Validating` until the answer permits evaluation.

### 6. Evaluate the frame

Apply the Goal, Obstacle, Constraint, and Logic rubrics. Derive the Overall Thinking Score without allowing a strong dimension to hide a blocking weakness.

### 7. Classify the result

- `!Valid`: The problem frame is sufficiently clear, relevant, and logically supported.
- `!Invalid`: Evidence or logic materially contradicts the frame.
- `!Incomplete`: Material information is missing or ambiguous.

### 8. Produce output

Return the universal output schema with the skill-specific score extension, assumptions, missing information, one prioritized question when required, confidence, and next step.

### 9. Recommend a transition

Recommend `#Constraints`, `#BreakItDown`, or `#GapAnalysis` only when its transition condition is satisfied. Otherwise recommend clarification, evidence collection, reframing, or no next skill.

## Exit conditions

The skill exits when it has produced a schema-compatible output and updated conversation state with the current goal, collected inputs, pending questions, and optional next skill.
