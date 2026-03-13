# Output Format Specification

Detailed format specification for the `feature-draft` skill's output files.
Output format specification for feature-draft, with **Target Files** fields in Part 2.

---

## File Structure Overview

```markdown
# Feature Draft: [Feature Name]

[Header metadata]

---

# Part 1: Spec Patch Draft
[Spec Update Input format]

---

# Part 2: Implementation Plan
[Implementation Plan format with Target Files]

---

## Next Steps
[Next Steps]
```

---

## Header Metadata

```markdown
# Feature Draft: [Feature Name]

**Date**: YYYY-MM-DD
**Author**: [author]
**Target Spec**: [target spec filename, e.g.: project.md]
**Status**: Draft
```

For multiple features:
```markdown
# Feature Draft: [Group name or representative feature name]

**Date**: YYYY-MM-DD
**Author**: [author]
**Target Spec**: [target spec filename]
**Status**: Draft
**Features**: [feature 1], [feature 2], [feature 3]
```

---

## Part 1: Spec Patch Draft

### Format Principles

1. **"Spec Update Input" format compliance**: Can be directly used as input for `spec-update-todo` skill
2. **Target Section annotations**: Manual copy-paste location guide for each item
3. **Status marker**: Use 📋 Planned
4. **Match existing style**: Conform to the spec's language/format

### Full Structure

```markdown
<!-- spec-update-todo-input-start -->
# Part 1: Spec Patch Draft

> This patch can be copy-pasted into the corresponding spec section,
> or used as input for the `spec-update-todo` skill.

# Spec Update Input

**Date**: YYYY-MM-DD
**Author**: [author]
**Target Spec**: [target spec filename]

## Background & Motivation Updates
[background/motivation changes — maps to §1...]

## Design Changes
[core design/algorithm changes — maps to §2...]

## New Features
[feature items...]

## Improvements
[improvement items...]

## Bug Reports
[bug items...]

## Component Changes
[component items...]

## Configuration Changes
[configuration items...]

## Usage Scenarios
[new usage scenarios and expected results — maps to §5...]

## Notes
[additional context...]
<!-- spec-update-todo-input-end -->
```

### Per-Section Detailed Format

#### Background & Motivation Updates

```markdown
## Background & Motivation Updates

### Background Update: [title]
**Target Section**: `_sdd/spec/xxx.md` > `배경 및 동기 (§1)`
**Change Type**: Problem Statement / Motivation / Alternative Comparison

**Current**: [current description in spec, if any]
**Proposed**: [proposed update]
**Reason**: [why this update is needed]
```

Minimal format:
```markdown
### Background Update: [title]
**Target Section**: `_sdd/spec/xxx.md` > `배경 및 동기 (§1)`

**Proposed**: [proposed update]
```

#### Design Changes

```markdown
## Design Changes

### Design Change: [title]
**Priority**: High/Medium/Low
**Target Section**: `_sdd/spec/xxx.md` > `핵심 설계 (§2)`
**Change Type**: Algorithm / Logic Flow / Design Rationale

**Description**:
[what design aspect is changing and why]

**Code Reference**: `[filepath:functionName]`

**Impact**:
[what other parts of the system are affected]
```

Minimal format:
```markdown
### Design Change: [title]
**Priority**: High/Medium/Low
**Target Section**: `_sdd/spec/xxx.md` > `핵심 설계 (§2)`

**Description**:
[what design aspect is changing and why]
```

#### New Features

```markdown
## New Features

### Feature: [feature name]
**Priority**: High/Medium/Low
**Category**: [Core Feature/Enhancement/Performance/Security/UI/UX]
**Target Component**: [target component or file]
**Target Section**: `_sdd/spec/xxx.md` > `Goal > Key Features`

**Description**:
[feature description - describe behavior from user's perspective]

**Acceptance Criteria**:
- [ ] criterion 1
- [ ] criterion 2
- [ ] criterion 3

**Technical Notes**:
[technical notes - libraries to use, architecture constraints, etc.]

**Dependencies**:
[prerequisites or required conditions]
```

Minimal format (required fields only):
```markdown
### Feature: [feature name]
**Priority**: High/Medium/Low
**Target Section**: `_sdd/spec/xxx.md` > `Goal > Key Features`

**Description**:
[feature description]
```

#### Improvements

```markdown
## Improvements

### Improvement: [improvement name]
**Priority**: High/Medium/Low
**Target Section**: `_sdd/spec/xxx.md` > `Issues > Improvements`
**Current State**: [current state]
**Proposed**: [proposed change]
**Reason**: [reason for improvement]
```

Simple format:
```markdown
## Improvements

- **High**: [improvement description] → Target: `xxx.md` > `Issues > Improvements`
- **Medium**: [improvement description] → Target: `xxx.md` > `Issues > Improvements`
```

#### Bug Reports

```markdown
## Bug Reports

### Bug: [bug name]
**Severity**: High/Medium/Low
**Target Section**: `_sdd/spec/xxx.md` > `Issues > Bugs`
**Location**: [file:line]

**Description**:
[bug description]

**Reproduction**:
1. Step 1
2. Step 2

**Expected Behavior**:
[expected behavior]

**Workaround**:
[workaround if available]
```

#### Component Changes

```markdown
## Component Changes

### New Component: [component name]
**Target Section**: `_sdd/spec/xxx.md` > `Component Details`
**Purpose**: [purpose]
**Input**: [input]
**Output**: [output]

**Planned Methods**:
- `method_name(params)` - description

### Update Component: [component name]
**Target Section**: `_sdd/spec/xxx.md` > `Component Details > [component name]`
**Change Type**: Enhancement/Refactor/Fix

**Changes**:
- change 1
- change 2
```

#### Configuration Changes

```markdown
## Configuration Changes

### New Config: [config name]
**Target Section**: `_sdd/spec/xxx.md` > `Configuration`
**Type**: Environment Variable / Config File / CLI Argument
**Required**: Yes/No
**Default**: [default value]
**Description**: [description]
```

#### Notes

```markdown
## Notes

### Context
[additional context]

### Constraints
[constraints]

### References
[reference links]
```

#### Usage Scenarios

```markdown
## Usage Scenarios

### Scenario: [scenario name]
**Target Section**: `_sdd/spec/xxx.md` > `사용 가이드 & 기대 결과 (§5)`

**Setup**:
[preconditions or setup steps]

**Action**:
[what the user does]

**Expected Result**:
[what should happen — observable behavior, output, side effects]
```

Minimal format:
```markdown
### Scenario: [scenario name]
**Target Section**: `_sdd/spec/xxx.md` > `사용 가이드 & 기대 결과 (§5)`

**Action**: [what the user does]
**Expected Result**: [what should happen]
```

### Target Section Annotation Rules

| Input Type | Target Section Value |
|------------|---------------------|
| Background/Motivation Update | `_sdd/spec/xxx.md` > `배경 및 동기 (§1)` |
| Design Change / Algorithm | `_sdd/spec/xxx.md` > `핵심 설계 (§2)` |
| New Feature (Core) | `_sdd/spec/xxx.md` > `Goal > Key Features` |
| New Feature (Component) | `_sdd/spec/xxx.md` > `Component Details (§4)` |
| Improvement | `_sdd/spec/xxx.md` > `Issues > Improvements` |
| Bug Report | `_sdd/spec/xxx.md` > `Issues > Bugs` |
| Performance | `_sdd/spec/xxx.md` > `Issues > Performance` |
| Security | `_sdd/spec/xxx.md` > `Security Considerations` |
| Usage Scenario / Expected Result | `_sdd/spec/xxx.md` > `사용 가이드 & 기대 결과 (§5)` |
| Configuration | `_sdd/spec/xxx.md` > `Configuration (§8)` |
| Dependency | `_sdd/spec/xxx.md` > `Environment & Dependencies (§8)` |
| API Change | `_sdd/spec/xxx.md` > `API Reference (§7)` |
| Test Addition | `_sdd/spec/xxx.md` > `Testing` |
| Code Reference | `_sdd/spec/xxx.md` > `부록: 코드 레퍼런스 목록` |

For split specs, use actual filenames:
- `_sdd/spec/project_API.md` > `API Reference`
- `_sdd/spec/project_COMPONENTS.md` > `Component Details`

---

## Part 2: Implementation Plan (with Target Files)

### Full Structure

```markdown
# Part 2: Implementation Plan

## Overview
[summary of what to implement - 1-3 sentences]

## Scope

### In Scope
- [included item 1]
- [included item 2]

### Out of Scope
- [excluded item 1]
- [excluded item 2]

## Components
1. **[component name]**: brief description
2. **[component name]**: brief description

## Implementation Phases

### Phase 1: [phase name]
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 1  | ...  | P0       | -            | ...       |

### Phase 2: [phase name]
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 2  | ...  | P1       | 1            | ...       |

## Task Details

### Task 1: [title]
**Component**: [parent component]
**Priority**: P0/P1/P2/P3
**Type**: Feature/Bug/Refactor/Research/Infrastructure/Test

**Description**:
[detailed description]

**Acceptance Criteria**:
- [ ] criterion 1
- [ ] criterion 2

**Target Files**:
- [C] `src/path/to/file.py` -- 설명
- [M] `src/path/to/existing.py` -- 변경 설명
- [C] `tests/test_file.py` -- 테스트

**Technical Notes**:
- [implementation hints]

**Dependencies**: [blocking task IDs]

---

## Parallel Execution Summary
| Phase | Total Tasks | Max Parallel | Sequential (conflicts) |
|-------|-------------|--------------|----------------------|
| 1     | N           | N            | None           |
| 2     | N           | N            | file.py (Task X, Y) |

## Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|

## Open Questions
- [ ] [question]

## Model Recommendation
[model recommendation]
```

### Task Structure Details (with Target Files)

```markdown
### Task [ID]: [clear, action-oriented title]
**Component**: [parent component/module]
**Priority**: [P0-Critical | P1-High | P2-Medium | P3-Low]
**Type**: [Feature | Bug | Refactor | Research | Infrastructure | Test]

**Description**:
[detailed description of work to be done]

**Acceptance Criteria**:
- [ ] [specific, measurable criterion]
- [ ] [additional criterion]

**Target Files**:
- [C/M/D] `path/to/file` -- 변경 설명

**Technical Notes**:
- [implementation hints, patterns to use]

**Dependencies**: [blocking task ID list, or "-" if none]
```

### Target Files Markers

| Marker | Meaning | Description |
|--------|---------|-------------|
| `[C]` | Create | New file to be created |
| `[M]` | Modify | Existing file to be modified |
| `[D]` | Delete | File to be deleted |

See `references/target-files-spec.md` for the full specification.

### Priority Definitions

| Priority | Description |
|----------|-------------|
| P0-Critical | Needs immediate attention, prerequisite for other tasks |
| P1-High | Core functionality, must complete in current phase |
| P2-Medium | Important but can be deferred |
| P3-Low | Nice to have but not essential |

### Phase Strategies

**MVP-First** (default):
```
Phase 1: Foundation (base setup, tasks with no dependencies)
Phase 2: Core (core features, MVP)
Phase 3: Enhancement (additional features, improvements)
Phase 4: Polish (testing, documentation, optimization)
```

**Risk-First** (when uncertainty is high):
```
Phase 1: Spike (validate high-risk items)
Phase 2: Core (core features)
Phase 3: Remaining (low-risk items)
```

---

## Next Steps Section

```markdown
---

## Next Steps

### Apply Spec Patch (choose one)
- **Method A (automatic)**: Run `spec-update-todo` → use Part 1 from this file as input
- **Method B (manual)**: Copy-paste each item from Part 1 to its Target Section

### Execute Implementation
- **Parallel**: Run `implementation` skill → use Part 2 as implementation plan
- **Sequential**: Execute tasks sequentially (Target Files ignored)

### Model Recommendation
- [model recommendation for implementation]
```

---

## File Management Rules

### Filename
- Format: `feature_draft_<feature_name>.md`
- `<feature_name>`: lowercase English, underscore-separated
- Example: `feature_draft_real_time_notification.md`
- Multiple features: `feature_draft_v2_features.md`, `feature_draft_batch_improvements.md`

### Archive
- Location: `_sdd/drafts/prev/`
- Format: `prev_feature_draft_<name>_<timestamp>.md`
- `<timestamp>` format: `YYYYMMDD_HHMMSS`
- Example: `prev_feature_draft_notification_20260214_143000.md`

### File Size Management
Split option when exceeding 25 tasks:

```
_sdd/drafts/
├── feature_draft_<name>.md           # Index + Part 1
├── feature_draft_<name>_phase_1.md   # Phase 1 task details
├── feature_draft_<name>_phase_2.md   # Phase 2 task details
└── feature_draft_<name>_phase_3.md   # Phase 3 task details
```

Link phase files from index file:
```markdown
## Implementation Phases

### Phase 1: Foundation
[Details: feature_draft_<name>_phase_1.md](./feature_draft_<name>_phase_1.md)

| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 1  | ...  | P0       | -            | ...       |
```

### Input File Processing

Used input files are marked as processed:

| Original | After Processing |
|----------|-----------------|
| `_sdd/spec/user_draft.md` | `_sdd/spec/_processed_user_draft.md` |
| `_sdd/spec/user_spec.md` | `_sdd/spec/_processed_user_spec.md` |
| `_sdd/implementation/user_input.md` | `_sdd/implementation/_processed_user_input.md` |

Processing metadata added:
```markdown
<!-- Processed: YYYY-MM-DD -->
<!-- Applied to: feature_draft_<name>.md -->
```
