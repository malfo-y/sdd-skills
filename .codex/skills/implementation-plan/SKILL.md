---
name: implementation-plan
description: Use this skill when the user asks to "create an implementation plan", "plan the implementation", "break down this spec", "create a development roadmap", "analyze requirements and create tasks", "create a parallel implementation plan", "plan parallel implementation", "병렬 구현 계획", or wants a structured implementation plan with task-level Target Files for conflict-aware parallel execution.
---

# Implementation Plan Creation (Parallel-Ready)

Create a structured, actionable implementation plan where every task declares `Target Files`.
Use this skill when planning is needed separately from `feature-draft`.

Keep this file concise and rely on `references/` for detailed patterns.

## Workflow Position

Standalone planning path:

```
spec -> implementation-plan (this) -> implementation -> spec-update-done
```

If the user also needs requirement clarification + spec patch drafting in one run, prefer `feature-draft`.

## Hard Rule

- Read spec as input, but never modify files under `_sdd/spec/`.
- If spec changes are needed, capture them as open questions and hand off to `spec-update-todo`.

## Language

- Default output language: Korean.

## Inputs

- user request in chat
- `_sdd/implementation/user_input.md` (if present)
- current spec files under `_sdd/spec/` (read-only)
- repository structure and conventions

If input is unclear and no usable context exists, ask the user directly before planning.

## Output

Default path:

- `<project_root>/_sdd/implementation/IMPLEMENTATION_PLAN.md`

Optional archive when replacing:

- `<project_root>/_sdd/implementation/prev/PREV_IMPLEMENTATION_PLAN_<timestamp>.md`

Split output option for large plans:

- `IMPLEMENTATION_PLAN.md` as index
- `IMPLEMENTATION_PLAN_PHASE_<n>.md` files per phase

## Plan Contract

Include these sections:

1. Overview
2. Scope (In/Out)
3. Components
4. Implementation Phases
5. Task Details
6. Parallel Execution Summary
7. Risks & Mitigations
8. Open Questions

Each task in Task Details must include:

- `Component`, `Priority`, `Type`
- `Description`
- `Acceptance Criteria`
- `Target Files` with `[C]/[M]/[D]` markers
- `Technical Notes`
- `Dependencies`

## Workflow

### 1) Analyze specification

Extract requirements, constraints, scope boundaries, and success criteria.

### 2) Identify components

Break work into modules/services and integration points.

### 3) Define tasks with Target Files

- Make tasks granular and executable.
- Assign exact file-level `Target Files`.
- Include both implementation files and tests.

### 4) Map dependencies and parallel potential

- mark blocking dependencies explicitly
- identify non-overlapping tasks that can run in parallel
- call out file conflicts that force sequential order

### 5) Produce plan

Generate final markdown and summarize:

- phase ordering
- critical path
- expected parallel efficiency

## Quality Gates

Before finalizing:

- every task has `Target Files`
- no directory-level paths or wildcard-only paths
- dependencies form a valid order
- conflicts in shared files are explicitly documented
- semantic conflict risks (shared schema/config/API contracts) are explicitly documented
- open questions are explicit (do not guess)

## When to Ask the User

Ask directly when:

- requirements are ambiguous
- technical stack/constraints are missing
- target file paths are uncertain
- multiple scope interpretations are equally valid

## Integration

- Upstream: `spec-create`, `spec-draft`, `feature-draft` (optional)
- Downstream: `implementation` (preferred), `implementation-sequential` (sequential fallback)

## References

- `references/target-files-spec.md` for `Target Files` grammar and conflict policy
- `references/advanced-patterns.md` for decomposition/risk/dependency patterns
- `examples/sample-plan-parallel.md` for a complete sample plan
