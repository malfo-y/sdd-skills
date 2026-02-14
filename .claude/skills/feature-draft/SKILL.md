---
name: feature-draft
description: This skill should be used when the user asks to "feature draft", "draft feature", "feature plan", "plan feature", "기능 초안", "기능 계획", "초안과 계획", "draft and plan", "feature spec and plan", or wants to combine requirements gathering, spec patch drafting, and implementation planning into a single workflow.
version: 1.0.0
---

# Feature Draft - Unified Spec Patch + Implementation Plan Skill

Collects requirements through conversation with the user, then outputs a spec patch draft and implementation plan as a **single file**.

## Simplified Workflow

This skill is **Step 2 of 4** in the simplified SDD workflow:

```
spec → feature-draft (this) → implementation → spec-update-done
```

| Step | Skill | Purpose |
|------|-------|---------|
| 1 | spec-create | Create the initial spec document |
| **2** | **feature-draft** | Draft feature spec patch + implementation plan |
| 3 | implementation | Execute the implementation plan (TDD) |
| 4 | spec-update-done | Sync spec with actual code |

> **Previous workflow** (7 steps): spec → spec-draft → spec-update-todo → implementation-plan → implementation → implementation-review → spec-update-done
> **New workflow** (4 steps): spec → feature-draft → implementation → spec-update-done

## Overview

This skill integrates the functionality of three skills: `spec-draft` + `spec-update-todo` + `implementation-plan`.
In a single conversation, it collects requirements and simultaneously generates a spec patch draft (Part 1) and an implementation plan (Part 2).

**Previous workflow**: `spec-draft` → `spec-update-todo` → `implementation-plan` (3 invocations, 3x tokens)
**This skill**: `feature-draft` (1 invocation, shared context)

## When to Use This Skill

- When you want to plan a new feature and create an implementation plan all at once
- When you want to write a spec patch and implementation plan simultaneously
- When you want to save tokens while getting both a spec patch and implementation plan
- When you want to collapse the `spec-draft` → `spec-update-todo` → `implementation-plan` chain into one step

## Hard Rules

1. **No spec file modifications**: Files under `_sdd/spec/` are **read-only**. Never modify them.
2. **Output location**: Save to `_sdd/drafts/` directory.
3. **Write in Korean**: Output file content must be written in Korean.
4. **Multiple features supported**: Multiple features can be included in one file, but always confirm with the user first.
5. **spec-update-todo compatible**: Part 1 must follow the "Spec Update Input" format so it can be directly used as input for `spec-update-todo`.

## Input Sources

1. **User conversation (current session)**: Real-time requirements collection (primary)
2. **Existing draft files**: `_sdd/spec/user_draft.md` or `_sdd/spec/user_spec.md`
3. **Existing implementation input**: `_sdd/implementation/user_input.md`
4. **User-modified code**: Analyze changes via git diff etc.
5. **Other user-specified files**: Reference documents or notes
6. **Existing decision log**: `_sdd/spec/DECISION_LOG.md` (if present)

## Output

**File location**: `_sdd/drafts/feature_draft_<feature_name>.md`

**File structure** (single file, 2 parts):
- **Part 1**: Spec patch draft ("Spec Update Input" format + Target Section annotations)
- **Part 2**: Implementation plan (per-phase tasks, details, risks)

**Optional output**: `_sdd/spec/DECISION_LOG.md` (only when new decisions/trade-offs arise)

## Process

### Step 1: Input Analysis

```
1. Review user conversation content
2. Check for existing files:
   - `_sdd/spec/user_draft.md` (created by spec-draft)
   - `_sdd/spec/user_spec.md` (user-authored)
   - `_sdd/implementation/user_input.md` (implementation input)
3. Check code changes (git diff etc.)
4. Consolidate requirements from all sources
5. Determine input completeness level (see references/adaptive-questions.md):
   - HIGH: Feature name + description + acceptance criteria + priority all present
   - MEDIUM: Feature name + description present but acceptance criteria or priority missing
   - LOW: Vague idea level
```

### Step 2: Context Gathering

```
1. Read existing spec (read-only):
   - Find `_sdd/spec/<project>.md` or `main.md`
   - If spec is split, follow links from the index
2. Understand spec structure:
   - Section list (to determine where patches go)
   - Component list (to understand relationships with existing components)
   - Existing feature list (to prevent duplication)
   - Verify spec language/style (so patches match existing style)
3. Check `_sdd/spec/DECISION_LOG.md` (if present):
   - Review existing decisions/rationale
   - Ensure new feature doesn't conflict with existing decisions
```

### Step 3: Adaptive Clarification

Apply different question strategies based on input completeness level:

**HIGH (detailed input)**: Proceed directly without questions. Only confirm collected information.

**MEDIUM (partial input)**: Ask only 1-3 key questions:
- Priority (High/Medium/Low)
- Acceptance Criteria
- Technical constraints

**LOW (vague input)**: Confirm type first, then ask required questions:
1. Confirm requirement type (new feature/improvement/bug/component/configuration)
2. Type-specific required questions (see references/adaptive-questions.md)
3. Use AskUserQuestion tool

**Multiple features check**:
- If multiple features are detected in user input:
  - Use AskUserQuestion to confirm: "It seems like multiple features are included. Would you like to include them all in one file, or separate them into individual files?"
  - Proceed based on user's choice

### Step 4: Feature Design

```
1. Classify requirements by type:
   - New Features
   - Improvements
   - Bug Reports
   - Component Changes
   - Configuration Changes

2. Map each item to target spec section:
   | Type | Target Section |
   |------|----------------|
   | New Feature (Core) | Goal > Key Features |
   | New Feature (Component) | Component Details |
   | Improvement | Issues > Improvements |
   | Bug Fix | Issues > Bugs |
   | Performance | Issues > Performance |
   | Security | Security Considerations |
   | Configuration | Configuration |
   | Dependency | Environment & Dependencies |
   | API Change | API Reference |
   | Test Addition | Testing |

3. Identify implementation components:
   - Group related features into modules
   - Identify shared utilities/common patterns
   - Check external dependencies and integration points
   - Consider data model/storage requirements
```

### Step 5: Spec Patch Generation = Part 1

Part 1 follows the "Spec Update Input" format with `**Target Section**` annotations added to each item.

**Format rules**:
- Full compliance with "Spec Update Input" format (spec-update-todo compatible)
- Add `**Target Section**` to each item (manual copy-paste location guide)
- Use status marker: 📋 Planned
- Match existing spec style/language
- See `references/output-format.md` for detailed format

```markdown
# Part 1: Spec Patch Draft

> This patch can be copy-pasted into the corresponding spec section,
> or used as input for the `spec-update-todo` skill.

# Spec Update Input

**Date**: YYYY-MM-DD
**Author**: [author]
**Target Spec**: [target spec file]

## New Features

### Feature: [feature name]
**Priority**: High/Medium/Low
**Category**: [category]
**Target Component**: [target component]
**Target Section**: `_sdd/spec/xxx.md` > `Goal > Key Features`

**Description**:
[feature description]

**Acceptance Criteria**:
- [ ] criterion 1
- [ ] criterion 2

**Technical Notes**:
[technical notes]

**Dependencies**:
[dependencies]

---

## Improvements

### Improvement: [improvement name]
**Priority**: High/Medium/Low
**Target Section**: `_sdd/spec/xxx.md` > `Issues > Improvements`
**Current State**: [current state]
**Proposed**: [proposed change]
**Reason**: [reason for improvement]

---

## Bug Reports

### Bug: [bug name]
**Severity**: High/Medium/Low
**Target Section**: `_sdd/spec/xxx.md` > `Issues > Bugs`
**Location**: [file:line]
**Description**: [bug description]
**Reproduction**: [reproduction steps]
**Expected Behavior**: [expected behavior]

---

## Component Changes

### New Component: [component name]
**Target Section**: `_sdd/spec/xxx.md` > `Component Details`
**Purpose**: [purpose]
**Input**: [input]
**Output**: [output]
**Planned Methods**:
- `method_name()` - description

---

## Configuration Changes

### New Config: [config name]
**Target Section**: `_sdd/spec/xxx.md` > `Configuration`
**Type**: Environment Variable / Config File
**Required**: Yes/No
**Default**: [default value]
**Description**: [description]

---

## Notes

### Context
[additional context]

### Constraints
[constraints]
```

### Step 6: Implementation Plan Generation = Part 2

Reuse the components and analysis results from Step 4 to create the implementation plan.

**Implementation plan structure**:

```markdown
# Part 2: Implementation Plan

## Overview
[summary of what to implement]

## Scope
### In Scope
- [included items]

### Out of Scope
- [excluded items]

## Components
1. **[component name]**: description
2. **[component name]**: description

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

### Task 1: [clear, action-oriented title]
**Component**: [parent component]
**Priority**: [P0-Critical | P1-High | P2-Medium | P3-Low]
**Type**: [Feature | Bug | Refactor | Research | Infrastructure | Test]

**Description**:
[detailed description of work to be done]

**Acceptance Criteria**:
- [ ] [specific, measurable criterion]
- [ ] [additional criterion]

**Technical Notes**:
- [implementation hints, patterns to use, files to modify]

**Dependencies**: [blocking task ID list]

## Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| ...  | ...    | ...        |

## Open Questions
- [ ] [question needing clarification]

## Model Recommendation
[model recommendation based on implementation complexity]
```

**Task definition rules**:
- Each task should be completable in a single work session
- Split into subtasks if too large
- Include infrastructure/setup tasks (CI/CD, environment configuration, etc.)
- Include test tasks (unit, integration, E2E)
- Include documentation tasks

**Dependency mapping**:
- **Blocks**: Tasks that cannot start until this task is complete
- **Related**: Shares context but no blocking relationship
- **Parallel**: Can be worked on concurrently

**Phase strategy** (choose based on complexity):
- **MVP-First**: Foundation → MVP → Core → Nice-to-Have
- **Risk-First**: High-risk items → Core → Low-risk items
- **Dependency-Driven**: Foundation → Services → Integration → Polish

**Model recommendation**:
Estimate implementation scale and complexity to recommend an appropriate model.
See "Model aliases" at https://code.claude.com/docs/en/model-config.

### Step 7: Review & Confirm

```
1. Show generated draft to user (Part 1 + Part 2)
2. Incorporate modifications
3. Check if there's anything else to add

4. Save file:
   a. Create `_sdd/drafts/` directory (if it doesn't exist)
   b. Archive existing file (if a file with the same name exists):
      - `_sdd/drafts/prev/prev_feature_draft_<name>_<timestamp>.md`
   c. Save: `_sdd/drafts/feature_draft_<feature_name>.md`

5. Process input files (if used):
   - `user_draft.md` → `_processed_user_draft.md`
   - `user_spec.md` → `_processed_user_spec.md`
   - `user_input.md` → `_processed_user_input.md`
   Add processing metadata:
   <!-- Processed: YYYY-MM-DD -->
   <!-- Applied to: feature_draft_<name>.md -->

6. Update Decision Log (optional):
   - Only when significant decisions/trade-offs were made
   - Add brief entry to `_sdd/spec/DECISION_LOG.md`

7. Provide next steps guidance:
```

**Completion message template**:

```markdown
## Feature Draft Complete

**File**: `_sdd/drafts/feature_draft_<name>.md`
**Date**: YYYY-MM-DD

### Contents
| Part | Content | Item Count |
|------|---------|------------|
| Part 1 | Spec patch draft | N items |
| Part 2 | Implementation plan | N tasks (M phases) |

### Input Files Processed
- [x] `user_draft.md` → `_processed_user_draft.md` (if used)
- [x] `user_spec.md` → `_processed_user_spec.md` (if used)

### Next Steps
Apply spec patch (choose one):
- **Method A (automatic)**: Run `spec-update-todo` → use Part 1 as input
- **Method B (manual)**: Copy-paste each patch from Part 1 to the target section

Execute implementation:
- Run `implementation` skill → use Part 2 as implementation plan

### Model Recommendation
[model recommendation for implementation]
```

## File Management Rules

### Output Filename
- Format: `feature_draft_<feature_name>.md`
- `<feature_name>`: lowercase English, underscore-separated (e.g., `real_time_notification`)
- For multiple features: use representative feature name or group name (e.g., `feature_draft_v2_features.md`)

### Archive
- Location: `_sdd/drafts/prev/`
- Format: `prev_feature_draft_<name>_<timestamp>.md`
- Archive only when a file with the same name already exists

### File Size Management
- When exceeding 25 tasks, suggest per-phase split option to user:
  - Main file: `feature_draft_<name>.md` (index + Part 1)
  - Phase files: `feature_draft_<name>_phase_1.md`, `feature_draft_<name>_phase_2.md`, ...

## Best Practices

### Effective Requirements Gathering
- **Be specific**: Provide clear criteria rather than vague expressions
- **Include examples**: Collect concrete usage examples when possible
- **Specify priority**: Assign priority to all items
- **Explain context**: Record why something is needed

### Spec Patch Quality
- **Style consistency**: Match the existing spec's language/format
- **Section accuracy**: Target Section annotations must match the actual spec structure
- **Status markers**: Use 📋 Planned marker
- **Compatibility**: Full compliance with spec-update-todo input format

### Implementation Plan Quality
- **Specific tasks**: Vague tasks cause scope creep
- **Include infrastructure**: CI/CD, environment configuration, tool setup
- **Include tests**: Unit, integration, E2E test tasks
- **Consider operations**: Monitoring, logging, deployment procedures
- **Document decisions**: Record reasons for choosing specific approaches
- **Identify MVP**: Mark tasks essential for initial release

## Error Handling

| Situation | Response |
|-----------|----------|
| `_sdd/spec/` directory missing | Recommend running `spec-create` first |
| Spec file missing | Can generate Part 2 only without spec (Part 1 requires spec) |
| `_sdd/drafts/` directory missing | Create automatically |
| Existing feature_draft file | Archive to `prev/` then create new |
| Incomplete information | Supplement with adaptive questions |
| User interrupts | Save content gathered so far |
| Multiple features detected in input | Confirm with user (single file vs separate) |

## Workflow Integration

```
Previous chain (3 skills):
  spec-draft → spec-update-todo → implementation-plan

Unified skill (1 skill):
  feature-draft
       ↓
  _sdd/drafts/feature_draft_<name>.md
                            ↓
       ↓    manual copy-paste or spec-update-todo
                            ↓
  implementation ←──────────┘
       ↓
  implementation-review
       ↓
  spec-update-done
```

## Additional Resources

### Reference Files
- **`references/adaptive-questions.md`** - Adaptive mode question guide (completeness level assessment + type-specific questions)
- **`references/output-format.md`** - Output file detailed format specification

### Example Files
- **`examples/feature_draft.md`** - Completed output example file
