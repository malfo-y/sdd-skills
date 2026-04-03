# Spec Rewrite Plan

## Rewrite Context

- **Target Document**: `_sdd/spec/apify_ig.md`
- **Execution Date**: 2026-04-04
- **Goal**: improve canonical fit and findability without inventing missing CIV or missing temporary-spec detail

## Diagnosis Summary

- **Primary Pain**: `main` mixes global rationale, operational notes, and implementation inventory, so the canonical shape is hard to see
- **Lowest Metrics**:
  - `Canonical Fit`: weak — CIV and decision-bearing structure are buried
  - `Findability`: weak — key sections are harder to locate than necessary
  - `Ambiguity Control`: weak — scope and ownership boundaries are vague

## Keep in Main

- problem / concept / scope / guardrails
- key design decisions
- CIV
- usage and expected results
- decision-bearing structure

## Move / Prune / Appendix

- move long file-by-file inventories to reference sections
- compress duplicate setup notes
- keep only selective navigation hints in strategic code map appendix

## Split Map

```text
_sdd/spec/
├── apify_ig.md
├── api-reference.md
├── environment.md
└── appendix.md
```

## Metric Improvement Rationale

- `Canonical Fit`: expose global spec core directly
- `Findability`: make `main` the shortest path to concept, CIV, and usage
- `Why/Decision Preservation`: keep rationale inline instead of burying it in appendices

## Ambiguities / Risks / Unresolved Decisions

- rate-limit contract appears in two inconsistent places
- ownership for failure alerting is still unclear
- some config notes may need their own reference file

## Canonical Warnings

- missing or weak CIV must be flagged, not authored from scratch
- if usage outcomes remain vague, leave explicit warnings in `rewrite_report.md`

## Execution Order

1. Rewrite `main` to expose global core
2. Move inventory-heavy detail to reference files
3. Validate links and citations
4. Write `rewrite_report.md` with deviations
