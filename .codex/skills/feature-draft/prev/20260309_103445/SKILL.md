---
name: feature-draft
description: This skill should be used when the user asks to "feature draft", "draft feature", "feature plan", "plan feature", "draft and plan", "feature draft parallel", "parallel feature draft", "병렬 기능 초안", "parallel feature plan", or wants to combine requirements gathering, spec patch drafting, and implementation planning with Target Files for parallel execution support.
version: 1.1.0
---

# Feature Draft - Exploration-First Spec Patch + Implementation Plan

Collect requirements from conversation/files/code context, then output:
- **Part 1**: a spec patch draft that fits the exploration-first SDD spec shape
- **Part 2**: an implementation plan with `Target Files` for parallel execution

This skill does not edit `_sdd/spec/` directly. It produces a draft artifact for later application by `spec-update-todo` and later synchronization by `spec-update-done`.

## Simplified Workflow

This skill is **Step 2 of 4** in the SDD workflow:

```
spec -> feature-draft (this) -> implementation -> spec-update-done
```

| Step | Skill | Purpose |
|------|-------|---------|
| 1 | spec-create | Create the initial index-first spec |
| **2** | **feature-draft** | Draft planned spec changes + implementation plan |
| 3 | implementation | Execute the plan |
| 4 | spec-update-done | Sync actual implementation back to spec |

## Overview

The spec philosophy used here:
- `Goal` explains user-visible value and scope
- `Architecture Overview` shows boundaries, repository/runtime maps, and invariants
- `Component Details` shows component ownership, paths, and contracts
- `Usage Examples` includes common operations and common change paths
- `Open Questions` makes uncertainty explicit

Part 1 must preserve that shape. Do not generate patch drafts that depend on old default sections such as `Security Considerations`, `API Reference`, `Testing`, or generic `Configuration` unless the existing spec already uses them and they are materially relevant.

## When to Use This Skill

- When you want to plan a feature and draft the corresponding spec changes together
- When you want a patch draft that points to the right spec sections before implementation
- When you want a parallel-ready implementation plan with `Target Files`
- When the feature spans multiple components and you need explicit change boundaries

## Hard Rules

1. **No spec file modifications**: Files under `_sdd/spec/` are read-only in this skill.
2. **Output location**: Save to `_sdd/drafts/`.
3. **Write in Korean**: Output file content must be written in Korean.
4. **spec-update-todo compatible**: Part 1 must follow the `Spec Update Input` format defined in `references/output-format.md`.
5. **Target Files required**: Every task in Part 2 must include a `**Target Files**` field.
6. **Anchor-aware drafting**: Part 1 should target stable spec anchors such as `Goal`, `Architecture Overview`, `Component Details`, `Environment & Dependencies`, `Identified Issues & Improvements`, `Usage Examples`, `Open Questions`.
7. **Change-oriented output**: Part 1 must help later readers understand what changes, where it changes, and what risks or invariants matter.
8. **Actual paths first**: Use real or strongly inferred components/paths whenever possible.
9. **Unknowns are explicit**: Low-confidence assumptions belong in `Open Questions`.
10. **Multiple features allowed**: Multiple features may share one draft only when the grouping is coherent; record grouping rationale in `Open Questions` if needed.

## Input Sources

1. User conversation (primary)
2. Existing draft files: `_sdd/spec/user_draft.md`, `_sdd/spec/user_spec.md`
3. Existing implementation input: `_sdd/implementation/user_input.md`
4. Current spec documents in `_sdd/spec/`
5. Codebase context and changed files
6. `_sdd/spec/DECISION_LOG.md` (if present)

## Output

**File location**: `_sdd/drafts/feature_draft_<feature_name>.md`

**File structure**:
- **Part 1**: Spec patch draft (`Spec Update Input` format)
- **Part 2**: Implementation plan with `Target Files`

**Optional output**:
- `_sdd/spec/DECISION_LOG.md` only if a new non-obvious decision must be preserved separately

## Process

### Step 1: Input Analysis

**Tools**: `Read`, `Glob`, `Bash (git diff)`

Collect:
1. user-stated feature intent
2. existing draft/input files
3. changed files from the working tree
4. constraints, priorities, and acceptance criteria if available

Completeness rubric:
- **High**: feature name, desired behavior, acceptance criteria, and likely scope all present
- **Medium**: feature and behavior present, but criteria or constraints are partial
- **Low**: idea-level request only

**Decision Gate 1->2**:
```
spec_exists = project spec file exists under _sdd/spec/ (excluding user_* and DECISION_LOG)

IF spec_exists -> Step 2
ELSE -> deterministic defaults:
  - recommend running spec-create first
  - or proceed in Part 2 only mode if the user clearly wants implementation planning without spec patching
```

### Step 2: Context Gathering

**Tools**: `rg`, `Glob`, `Read`, `Bash`

Read the existing spec as a map, not just as prose.

Prioritize extracting:
- `Goal > Project Snapshot / Key Features / Non-Goals`
- `Architecture Overview > System Boundary / Repository Map / Runtime Map / Cross-Cutting Invariants`
- `Component Details > Component Index`
- `Usage Examples > Common Change Paths`
- `Open Questions`

Also gather:
- related component docs if the spec is already split
- relevant decision-log entries
- code paths and symbols that will likely be touched
- existing conventions for naming, tests, and configuration

### Step 3: Adaptive Completion (Non-Interactive)

**Tools**: deterministic defaults (non-interactive)

Apply deterministic completion based on input quality.

Required completion checklist:
- feature name and objective
- requirement type
- affected components
- target spec areas
- acceptance criteria
- risks / invariants
- likely target files
- unresolved assumptions

For medium/low-confidence inferences:
- keep the draft deterministic
- record assumptions in `Open Questions`

### Step 4: Feature Design

**Tools**: `rg`, `Glob`, `Read`, `Bash`

Classify the planned change and map it to spec impact.

| Change Type | Preferred Target Section |
|-------------|--------------------------|
| User-visible feature | `Goal > Key Features` |
| Scope/boundary change | `Architecture Overview > System Boundary` |
| Flow/integration change | `Architecture Overview > Runtime Map` |
| New or changed component | `Component Details` or component spec file |
| Config/dependency/runtime change | `Environment & Dependencies` |
| Operational/debug path change | `Usage Examples > Common Change Paths` or `Common Operations` |
| Risk/technical debt | `Identified Issues & Improvements` |
| Uncertainty | `Open Questions` |

For each feature item, identify:
- affected components
- likely paths/symbols
- required spec impact
- user-visible acceptance criteria
- risks, invariants, and observability needs

For Part 2, map `Target Files` per task and minimize file overlap across tasks.

### Step 5: Generate Part 1 (Spec Patch Draft)

**Tools**: none

Part 1 follows the `Spec Update Input` format from `references/output-format.md`.

Minimum expectations:
- every item includes `**Target Section**`
- every meaningful item states affected components or paths
- behavior changes include acceptance criteria
- risky changes include `Risks / Invariants`
- unresolved assumptions are collected in `Open Questions`

### Step 5.5: Internal Validation

**Tools**: deterministic defaults (non-interactive)

Check that Part 1 answers:
- what changes
- where it changes in the spec
- which components are affected
- what must not break
- what remains uncertain

If not, repair Part 1 before continuing.

### Step 6: Generate Part 2 (Implementation Plan)

**Tools**: none

Create an implementation plan with:
- concise overview
- in-scope / out-of-scope
- affected components
- phased tasks
- detailed tasks with `Target Files`
- risks and mitigations
- open questions
- model recommendation

Task rules:
- each task should be completable in one focused work session
- include tests and required setup when relevant
- minimize file overlap to preserve parallelizability
- when file overlap is unavoidable, call it out in the parallel summary

See `references/output-format.md` and `references/target-files-spec.md`.

### Step 7: Review, Save, and Finalize

**Tools**: `Write`, `Bash (mkdir/mv)`, `Glob`

Before saving:
1. verify every task has `Target Files`
2. verify `[M]` files exist or adjust markers
3. verify `[C]` files are not already present or adjust markers
4. detect overlaps and reflect them in the parallel summary
5. ensure Part 1 and Part 2 are consistent

Save rules:
- create `_sdd/drafts/` if missing
- archive existing same-name draft to `_sdd/drafts/prev/prev_feature_draft_<name>_<timestamp>.md`
- save new file as `_sdd/drafts/feature_draft_<feature_name>.md`

If input files were used, mark them as processed:
- `_sdd/spec/user_draft.md` -> `_sdd/spec/_processed_user_draft.md`
- `_sdd/spec/user_spec.md` -> `_sdd/spec/_processed_user_spec.md`
- `_sdd/implementation/user_input.md` -> `_sdd/implementation/_processed_user_input.md`

## Output Summary

Completion output should summarize:
- feature scope
- planned spec impact
- number of phases / tasks
- major file conflict areas
- open questions
- next step: `spec-update-todo` then `implementation`

## Context Management

| 스펙 크기 | 전략 |
|-----------|------|
| < 200줄 | 전체 읽기 |
| 200-500줄 | 전체 읽기 가능 |
| 500-1000줄 | TOC 먼저, 관련 섹션만 읽기 |
| > 1000줄 | 인덱스와 타겟 섹션 우선 |

| 코드베이스 크기 | 전략 |
|----------------|------|
| < 50 파일 | `Glob` + `Read` 자유 탐색 |
| 50-200 파일 | `rg`, `Glob`, `Read`, `Bash` + 타겟 `Read` |
| > 200 파일 | `rg`, `Glob`, `Bash` 위주, 최소 `Read` |

## Additional Resources

### Reference Files
- `references/output-format.md` - Part 1 / Part 2 output shape
- `references/target-files-spec.md` - exact `Target Files` rules
- `references/tool-and-gates.md` - tool mapping and gates
- `references/adaptive-questions.md` - deterministic completion rules

### Example Files
- `examples/feature_draft_parallel.md` - sample feature draft output

## Integration with Other Skills

- `spec-create` defines the spec shape Part 1 should target
- `spec-update-todo` applies planned items to `_sdd/spec/`
- `implementation` executes Part 2
- `spec-update-done` syncs actual implementation back to spec
