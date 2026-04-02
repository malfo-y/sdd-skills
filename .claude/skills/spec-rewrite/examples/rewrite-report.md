## Rewrite Summary

- **Target Document**: `_sdd/spec/apify_ig.md`
- **Execution Date**: 2026-04-02
- **Goal**: improve structure and readability while preserving whitepaper qualities and documenting unresolved gaps
- **Plan Artifact**: `_sdd/spec/logs/spec-rewrite-plan.md`

## What Was Pruned or Moved

1. Moved 3 batch execution log sections to `_sdd/spec/apify_ig/appendix.md`
2. Consolidated 2 duplicate API response tables into 1 canonical table and replaced the rest with links
3. Moved long historical decision-review paragraphs to appendix while preserving rationale in `decision_log.md`

## File Split Map

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

## Main Index Changes

- Rewrote `apify_ig.md` as a link-first index hub
- Kept only core sections that help the reader orient quickly:
  - Background / Scope / Non-Goals
  - Architecture Snapshot
  - Component Index
  - Usage Entry Point
  - Open Questions

## Metric Scorecard

- **Component Separation**: `2` -- major components now map to dedicated files, but operations and interfaces still partially overlap
- **Findability**: `3` -- all core topics are reachable from `main` within two hops
- **Repo Purpose Clarity**: `2` -- main explains what the project does, but motivation is still thin
- **Architecture Clarity**: `2` -- core flow is visible, but retry/queue ownership remains hard to follow
- **Usage Completeness**: `1` -- examples exist, but representative setup/action/result flow is incomplete
- **Environment Reproducibility**: `2` -- dependencies and config are listed, but test/runtime prerequisites need tightening
- **Ambiguity Control**: `1` -- several non-measurable phrases remain and some ownership is undefined
- **Why/Decision Preservation**: `3` -- component `Why` fields and moved rationale were preserved

## Ambiguities and Issues

### [High] Missing Acceptance Criteria
- **Issue**: No clear done criteria for the data synchronization feature
- **Impact**: No reliable completion signal for implementation/review
- **Recommended Action**: Add quantitative limits for latency, failure rate, and retry boundaries

### [High] Conflicting Statements
- **Issue**: One document states "30 requests/minute" while another states "20 requests/minute"
- **Impact**: Risk of production misconfiguration for rate limits
- **Recommended Action**: Define a single source of truth and normalize values

### [Medium] Undefined Ownership
- **Issue**: Alert-response ownership is not specified
- **Impact**: Slower incident response
- **Recommended Action**: Define owner team and on-call escalation path

### [Low] Ambiguous Requirement
- **Issue**: Multiple non-measurable phrases such as "sync as quickly as possible"
- **Impact**: High implementation variance
- **Recommended Action**: Replace wording with numeric SLA/SLO targets

## Whitepaper Fit Assessment

- **Background & Motivation**: partial -- problem statement is present, but the reason this approach was chosen is still weak
- **Core Design Narrative**: partial -- architecture exists, but the main logic is still more tabular than narrative
- **Code Grounding / Citation**: weak -- no inline citations were found and the code reference index is missing
- **Usage Guide & Expected Results**: weak -- usage examples exist, but expected results are not explicit
- **Reference Balance**: partial -- reference sections are strong, but they still dominate the narrative sections

## Warnings Left Unresolved

- Missing §2-quality design narrative was flagged but not auto-generated
- Missing inline citations were flagged but not synthesized
- Weak usage outcome descriptions were flagged for follow-up via `spec-create` or `spec-upgrade`

## Plan Deviations

- Added `operations.md` only after link validation showed the original interfaces split still mixed runtime procedures
- Kept one short historical rationale paragraph in `main` because moving it would have weakened the §1 motivation narrative

> **Recommendation**: Use `spec-create` or `spec-upgrade` if the project needs missing whitepaper narrative to be authored, not just preserved.

## Validation Result

- Link check: pass (0 broken links)
- Duplicate sections: reduced from 6 to 1
- Main document length: reduced from 1200 lines to 310 lines
- Component `Why` fields: preserved inline
- Deferred warning count: 3
