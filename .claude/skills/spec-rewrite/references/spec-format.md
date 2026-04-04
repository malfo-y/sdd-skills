# Spec Format Reference

## Global Spec Core

| Order | Section | Required |
|------|---------|----------|
| 1 | Background & High-Level Concept | Yes |
| 2 | Scope / Non-goals / Guardrails | Yes |
| 3 | Core Design & Key Decisions | Yes |

Optional support layers:

- reference information
- appendix-level code map
- guide links
- repo-wide invariant wording embedded in guardrails or key decisions

Global anti-patterns:

- feature-level usage guide in main body
- feature-level contract/validation in main body
- exhaustive architecture/component inventory as default structure
- code-obvious explanation copied into the spec

## Temporary Spec Reference

| Order | Section | Required |
|------|---------|----------|
| 1 | Change Summary | Yes |
| 2 | Scope Delta | Yes |
| 3 | Contract/Invariant Delta | Yes |
| 4 | Touchpoints | Yes |
| 5 | Implementation Plan | Yes |
| 6 | Validation Plan | Yes |
| 7 | Risks / Open Questions | Yes |
