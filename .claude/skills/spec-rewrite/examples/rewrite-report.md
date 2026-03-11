## Rewrite Summary

- **Target Document**: `_sdd/spec/apify_ig.md`
- **Execution Date**: 2026-02-07
- **Goal**: simplify a long spec, split it hierarchically, and document ambiguities explicitly

## What Was Pruned or Moved

1. Moved 3 batch execution log sections to `_sdd/spec/apify_ig/appendix.md`
2. Consolidated 2 duplicate API response tables into 1 canonical table and replaced the rest with links
3. Moved long historical decision-review paragraphs to appendix

## File Split Map

```text
_sdd/spec/
├── apify_ig.md
└── apify_ig/
    ├── 01-overview.md
    ├── 02-architecture.md
    ├── 03-components.md
    ├── 04-interfaces.md
    ├── 05-operational-guides.md
    └── appendix.md
```

## Main Index Changes

- Rewrote `apify_ig.md` as a link-first index hub
- Kept only core sections:
  - Goal / Scope / Non-Goals
  - Architecture Snapshot
  - Component Index
  - Open Questions

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

## Validation Result

- Link check: pass (0 broken links)
- Duplicate sections: reduced from 6 to 1
- Main document length: reduced from 1200 lines to 280 lines
- Component Why fields: all preserved inline (not moved to appendix or DECISION_LOG)
