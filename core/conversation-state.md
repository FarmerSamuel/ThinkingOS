# Conversation State

ThinkingOS maintains an explicit, reusable state so reasoning can continue across turns, skills, or compatible AI systems without relying on hidden conversational memory.

## State fields

- **Current Skill:** The active thinking capability and its version or identifier.
- **Current Goal:** The validated outcome the user is trying to achieve.
- **Collected Inputs:** Relevant facts, claims, evidence, constraints, preferences, assumptions, and their provenance when available.
- **Pending Questions:** Unresolved questions, ordered by their impact on the goal or decision.
- **Next Skill:** The recommended follow-on capability, including why and when it should run.

## State behavior

State is updated after validation and after every material conclusion. New information should augment or explicitly supersede earlier entries rather than silently rewriting them. Facts, user statements, and system-generated assumptions must remain distinguishable.

Future implementations should be able to serialize, restore, inspect, and pass this state between skills. Only goal-relevant context should be retained, and sensitive information should be minimized according to the host system's privacy rules.
