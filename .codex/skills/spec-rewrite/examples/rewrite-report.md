## Rewrite Summary

- **Target Document**: `_sdd/spec/apify_ig.md`
- **Execution Date**: 2026-04-04
- **Goal**: improve canonical fit and readability while preserving rationale and documenting unresolved gaps
- **Plan Artifact**: `_sdd/spec/logs/spec-rewrite-plan.md`

## What Was Pruned or Moved

1. Moved exhaustive file-by-file inventories into reference sections
2. Compressed duplicate setup/config notes
3. Reduced appendix code map to entrypoint / invariant hotspot / change hotspot rows only

## File Split Map

```text
_sdd/spec/
├── apify_ig.md
├── api-reference.md
├── environment.md
└── appendix.md
```

## Main Index Changes

- rewrote `apify_ig.md` as the shortest path to problem, scope, CIV, and usage
- kept rationale inline where it carries design meaning
- moved low-value reference detail out of the main path

## Metric Scorecard

- **Component Separation**: improved
- **Findability**: improved
- **Repo Purpose Clarity**: improved
- **Architecture Clarity**: improved
- **Usage Completeness**: partial
- **Environment Reproducibility**: partial
- **Ambiguity Control**: partial
- **Why/Decision Preservation**: strong
- **Canonical Fit**: improved

## Canonical Fit Assessment

- **Global core visibility**: improved
- **CIV visibility**: improved
- **Decision-bearing structure**: improved
- **Reference/main-body balance**: improved
- **Warnings left unresolved**: CIV detail still thin in two areas; not auto-authored

## Warnings Left Unresolved

- missing quantitative done criteria in one usage scenario
- incomplete verification mapping for one contract

## Plan Deviations

- kept one operational section inline because moving it would have weakened the usage path

## Validation Result

- link check: pass
- broken citation count: 0
- canonical-fit warnings left: 2
