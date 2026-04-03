# Specification Summary Template

This template shows the structure and placeholders for generating summaries under the current SDD canonical model.

## Kind Detection

Before writing, classify the target as one of:

- `Global Spec`
- `Temporary Spec`

Use dominant purpose when signals are mixed.

## Global Spec Summary Template

```markdown
# [Project Name] - Specification Summary

**Generated**: [YYYY-MM-DD HH:MM]
**Spec Type**: Global Spec
**Spec Version**: [X.Y.Z or N/A]

## Executive Summary
[1-2 paragraph overview]

## Problem & High-Level Concept
- Problem: ...
- Concept: ...

## Scope Snapshot
### In Scope
- ...
### Non-goals
- ...
### Guardrails
- ...

## CIV Snapshot
### Key Contracts
- `C1`: ...
### Key Invariants
- `I1`: ...
### Verification
- `V1`: ...

## Decision-Bearing Structure
- System boundary: ...
- Ownership: ...
- Cross-component contract: ...
- Extension point: ...

## Usage & Expected Results
- Scenario: ...
- Expected result: ...

## Status / Risks / Next Steps
- Current status: ...
- Risks: ...
- Next steps: ...
```

## Temporary Spec Summary Template

```markdown
# [Change Name] - Temporary Spec Summary

**Generated**: [YYYY-MM-DD HH:MM]
**Spec Type**: Temporary Spec

## Executive Summary
[1 paragraph overview]

## Change Summary
- ...

## Scope Delta
- ...

## Contract / Invariant Delta Snapshot
- `C1`: ...
- `I1`: ...

## Touchpoints
- `path/to/file`

## Implementation / Validation Snapshot
- Plan: ...
- Validation: ...

## Risks / Open Questions
- ...
```

## README Snapshot Template

README block stays concise even if the summary file is longer.

```markdown
<!-- spec-summary:start -->
## Project Snapshot

- Type: Global Spec | Temporary Spec
- Current status: ...
- Key focus: ...
- Summary: `_sdd/spec/summary.md`
<!-- spec-summary:end -->
```
