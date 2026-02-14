# Output Format Specification

`feature-draft` outputs one combined markdown file with two parts.

## File Path

- `_sdd/drafts/feature_draft_<feature_name>.md`
- If existing file is replaced, archive to `_sdd/drafts/prev/`

## File Skeleton

```markdown
# Feature Draft: <Feature Name>

**Date**: YYYY-MM-DD
**Author**: <author>
**Target Spec**: <spec filename>
**Status**: Draft

---

# Part 1: Spec Patch Draft

# Spec Update Input

**Date**: YYYY-MM-DD
**Author**: <author>
**Target Spec**: <spec filename>

## New Features
...

## Improvements
...

## Bug Reports
...

## Component Changes
...

## Configuration Changes
...

## Notes
...

---

# Part 2: Implementation Plan

# Implementation Plan: <Feature Name>

## Overview
...

## Scope
### In Scope
...
### Out of Scope
...

## Components
...

## Implementation Phases
### Phase 1
| ID | Task | Priority | Dependencies | Component |

## Task Details
### Task 1
**Acceptance Criteria**:
- [ ] ...

## Risks & Mitigations
...

## Open Questions
- [ ] ...

---

## Next Steps
1. Apply Part 1 via `spec-update-todo`
2. Execute Part 2 via `implementation`
```

## Part 1 Rules

- Must remain `Spec Update Input` compatible.
- Add `Target Section` annotations to each major item.
- Keep items concise but actionable.
- Use checklist acceptance criteria for implementable changes.

## Part 2 Rules

- Tasks must be actionable and dependency-aware.
- Include at least one testing task when feature behavior changes.
- Include risk section even if short.

## Naming Rules

- Use lowercase snake case for `<feature_name>`.
- Multi-feature draft names should use a neutral group name (for example `v2_features`).

## Large Plan Split (Optional)

If task count is very large (for example >25):

- keep main file as index + Part 1
- move phase details to `feature_draft_<name>_phase_<n>.md`
- link phase files from the main file
