# Spec Rewrite Plan

## Rewrite Context

- **Target Document**: `_sdd/spec/apify_ig.md`
- **Execution Date**: 2026-04-02
- **Goal**: improve structure and findability without inventing missing whitepaper narrative

## Diagnosis Summary

- **Primary Pain**: `main` mixes architecture, operations, and historical logs, so component boundaries are hard to follow
- **Lowest Metrics**:
  - `Usage Completeness`: `1` -- representative scenario lacks expected result
  - `Ambiguity Control`: `1` -- several promises are non-measurable
  - `Architecture Clarity`: `2` -- queue/retry ownership is scattered
- **Whitepaper Risk**: §2 narrative exists but is buried under reference-heavy sections

## Keep in Main

- Background / scope / non-goals
- Architecture snapshot and core flow
- Component index with direct links
- Primary usage entry point
- Open questions that affect implementation or review

## Move / Prune / Appendix

- Move long batch execution logs to appendix
- Collapse duplicate API response tables into one canonical table
- Prune low-value historical commentary after preserving the rationale in `DECISION_LOG.md`

## Split Map

```text
_sdd/spec/
├── apify_ig.md
└── apify_ig/
    ├── overview.md
    ├── architecture.md
    ├── components.md
    ├── interfaces.md
    ├── operations.md
    └── appendix.md
```

## Metric Improvement Rationale

- `Component Separation`: move operations and interfaces into dedicated files
- `Findability`: turn `main` into a link-first hub so core topics stay within two hops
- `Repo Purpose Clarity`: keep project purpose and usage path in `main`
- `Why/Decision Preservation`: move only low-value bulk text and preserve rationale in-line or in `DECISION_LOG.md`

## Ambiguities / Risks / Unresolved Decisions

- Rate limit is inconsistent across two source sections (`20/min` vs `30/min`)
- Alert ownership is still undefined
- Missing quantitative done criteria for sync reliability

## Whitepaper Warnings

- Do not author missing inline citations automatically
- If §5 expected results are absent, warn in the report instead of inventing them

## Execution Order

1. Rewrite `main` as the index hub
2. Create split files and move existing content
3. Validate links and citation headers
4. Write `REWRITE_REPORT.md` with any deviations from this plan

## Approval Status

- **Approval Required**: yes
- **Approval Reason**: new subdirectory split and section relocation
- **Status**: pending
