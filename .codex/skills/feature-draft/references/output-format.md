# Output Format Specification

Output format for `feature-draft`.

The draft has two parts:
- **Part 1**: planned spec changes in a format that `spec-update-todo` can consume
- **Part 2**: implementation plan with `Target Files`

Part 1 should reflect the exploration-first spec philosophy:
- user-visible value goes to `Goal`
- boundary/flow changes go to `Architecture Overview`
- ownership/contracts go to `Component Details`
- run/test/change guidance goes to `Usage Examples`
- uncertainty goes to `Open Questions`
- optional sections appear only when they materially help

## File Structure Overview

~~~markdown
# Feature Draft: [Feature Name]

**Date**: YYYY-MM-DD
**Author**: [author]
**Target Spec**: [target spec filename]
**Status**: Draft

---

# Part 1: Spec Patch Draft
[Spec Update Input format]

---

# Part 2: Implementation Plan
[Implementation plan with Target Files]

---

## Next Steps
[Next steps]
~~~

## Part 1: Spec Patch Draft

### Format Principles

1. `spec-update-todo` compatible
2. each item has a `**Target Section**`
3. change intent is explicit
4. affected components/paths are visible when possible
5. low-confidence items are collected in `Open Questions`
6. include `**Spec Update Classification**`
7. omit empty optional sections and compress repeated prose
8. when behavior or design intent changes matter, target `Component Details > Overview`

### Full Structure

~~~markdown
# Part 1: Spec Patch Draft

> 이 패치는 `spec-update-todo` 입력으로 사용할 수 있습니다.

# Spec Update Input

**Date**: YYYY-MM-DD
**Author**: [author]
**Target Spec**: [target spec filename]
**Spec Update Classification**: MUST update | NO update | CONSIDER

## New Features
[feature items...]

## Improvements
[improvement items...]

## Bug Reports
[bug items...]

## Component Changes
[component items...]

## Environment & Dependency Changes
[environment/dependency/config items...]

## Notes
[context and constraints...]

## Open Questions
[unknowns and low-confidence assumptions...]
~~~

### Minimal Structure for `NO update`

~~~markdown
# Part 1: Spec Patch Draft

> 이 패치는 `spec-update-todo` 입력으로 사용할 수 있습니다.

# Spec Update Input

**Date**: YYYY-MM-DD
**Author**: [author]
**Target Spec**: [target spec filename]
**Spec Update Classification**: NO update

## Notes

### No Spec Change Reason
- 내부 리팩터링만 수행되며 사용자 동작, 경계, 계약, 변경 시작점이 바뀌지 않음

## Open Questions
- [필요 시]
~~~

### New Features

~~~markdown
## New Features

### Feature: [feature name]
**Priority**: High/Medium/Low
**Target Section**: `_sdd/spec/xxx.md` > `Goal > Key Features`
**Affected Components**: [component names]
**Related Paths**: `src/...`, `tests/...`

**Description**:
[user-visible behavior]

**Acceptance Criteria**:
- [ ] criterion 1
- [ ] criterion 2

**Spec Impact**:
- Goal: [what becomes newly true for users]
- Architecture/Flow: [if relevant]
- Usage/Change Paths: [if relevant]
- Tests/Observability: [if relevant]

**Risks / Invariants**:
- [what must remain true]

**Dependencies**:
- [dependency or "-"]
~~~

### Improvements

~~~markdown
## Improvements

### Improvement: [name]
**Priority**: High/Medium/Low
**Target Section**: `_sdd/spec/xxx.md` > `Identified Issues & Improvements`
**Affected Components**: [components]

**Current State**:
[current pain point]

**Proposed**:
[planned improvement]

**Reason**:
[why it matters]

**Related Paths**:
- `src/...`
~~~

### Bug Reports

~~~markdown
## Bug Reports

### Bug: [bug name]
**Severity**: High/Medium/Low
**Target Section**: `_sdd/spec/xxx.md` > `Identified Issues & Improvements`
**Affected Components**: [components]
**Location**: `path/to/file.py:123`

**Description**:
[symptom]

**Expected Behavior**:
[expected behavior]

**Risks / Invariants**:
- [blast radius or contract risk]
~~~

### Component Changes

~~~markdown
## Component Changes

### New Component: [component name]
**Target Section**: `_sdd/spec/xxx.md` > `Component Details`
**Owned Paths**:
- `src/...`
- `tests/...`

**Responsibility**:
- [what it does]

**Overview**:
- 동작 개요: [how the component works]
- 설계 의도: [why this structure exists]

**Interfaces / Contracts**:
- Inputs: ...
- Outputs: ...

**Change Recipes**:
- [where future edits would begin]

### Update Component: [component name]
**Target Section**: `_sdd/spec/xxx.md` > `Component Details`
**Change Type**: Enhancement / Refactor / Fix

**Changes**:
- [change 1]
- [change 2]

**Overview Update**:
- 동작 개요: [updated behavior summary]
- 설계 의도: [updated rationale if relevant]

**Risks / Invariants**:
- [notes]
~~~

### Environment & Dependency Changes

~~~markdown
## Environment & Dependency Changes

### Change: [name]
**Target Section**: `_sdd/spec/xxx.md` > `Environment & Dependencies`
**Type**: Dependency / Environment Variable / Runtime / Tooling / Setup Command

**Description**:
[what changes]

**Impact**:
- [setup/test/runtime impact]
~~~

### Notes / Open Questions

~~~markdown
## Notes

### Context
[context]

### Constraints
[constraints]

### Decision-Log Candidates
- [if any]

### References
[references]

## Open Questions
- [low-confidence assumption]
- [needs confirmation]
~~~

### Target Section Annotation Rules

| Planned Change | Preferred Target Section |
|----------------|--------------------------|
| New user-visible capability | `Goal > Key Features` |
| Boundary or integration scope change | `Architecture Overview > System Boundary` |
| Runtime/data/event flow change | `Architecture Overview > Runtime Map` |
| Component behavior/design intent change | `Component Details > Overview` |
| Component ownership/contract change | `Component Details` |
| Config/dependency/runtime change | `Environment & Dependencies` |
| Operational or debugging entry point | `Usage Examples > Common Change Paths` or `Common Operations` |
| Planned risk/debt | `Identified Issues & Improvements` |
| Uncertainty or unresolved dependency | `Open Questions` |

## Part 2: Implementation Plan

~~~markdown
# Part 2: Implementation Plan

## Overview
[summary including user-facing flow and design intent when useful]

## Scope

### In Scope
- [...]

### Out of Scope
- [...]

## Components
1. **[component]**: ...
2. **[component]**: ...

## Implementation Phases

### Phase 1: [name]
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 1  | ...  | P0       | -            | ...       |

## Task Details

### Task 1: [title]
**Component**: [component]
**Priority**: P0/P1/P2/P3
**Type**: Feature/Bug/Refactor/Research/Infrastructure/Test

**Description**:
[description]

**Acceptance Criteria**:
- [ ] criterion 1
- [ ] criterion 2

**Target Files**:
- [C] `src/path/to/file.py` -- 설명
- [M] `src/path/to/existing.py` -- 설명
- [C] `tests/test_file.py` -- 설명

**Technical Notes**:
- [implementation hints]

**Dependencies**: [task IDs or "-"]

## Parallel Execution Summary
| Phase | Total Tasks | Max Parallel | File Conflicts |
|-------|-------------|--------------|----------------|
| 1     | N           | N            | None           |

## Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|

## Open Questions
- [question]

## Model Recommendation
[recommendation]
~~~

## Next Steps

~~~markdown
## Next Steps

### Apply Spec Patch
- Run `spec-update-todo` with Part 1

### Execute Implementation
- Run `implementation` with Part 2

### Sync After Completion
- Run `spec-update-done`
~~~
