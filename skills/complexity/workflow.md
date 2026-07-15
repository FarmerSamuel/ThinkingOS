# Complexity Workflow

1. Validate required inputs and registered dependencies.
2. Normalize Component, Interaction, Dependency, UncertaintyDriver, FeedbackLoop without adding unsupported facts.
3. Apply the skill-specific relationship and classification rules.
4. Test ambiguity, contradiction, alternatives, and failure conditions.
5. Evaluate InteractionCoverage, DependencyQuality, Uncertainty, Adaptation, ExplanatoryPower using the shared 0–4 rubric.
6. Generate universal output, update conversation state, and recommend a dependency-safe transition.

Execution loops to clarification when a blocking gap appears. It exits only with schema-compatible output or an explicit needs-clarification result.
