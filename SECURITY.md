# Security Policy

## Supported versions

Security fixes are provided for the latest stable major release. Before v1.0, fixes target the current `main` branch and the most recent pre-release when practical.

## Report a vulnerability

Do not open a public issue. Use [GitHub private vulnerability reporting](https://github.com/FarmerSamuel/ThinkingOS/security/advisories/new) and include:

- Affected version or commit.
- A concise impact statement.
- Reproduction steps or a minimal proof of concept.
- Any known mitigations.
- Whether the report contains sensitive data.

Maintainers will acknowledge a complete report, investigate impact, coordinate remediation, and publish an advisory when appropriate. Please avoid accessing data you do not own, disrupting services, or publicly disclosing details before a fix is available.

## Scope

Relevant issues include unsafe adapter credential handling, workflow privilege escalation, malicious schema or knowledge ingestion, and defects that cause protected data to be retained or exposed contrary to documented contracts.

General reasoning quality disagreements without a security impact belong in the issue tracker.
