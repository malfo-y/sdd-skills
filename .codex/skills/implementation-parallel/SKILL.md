---
name: implementation-parallel
description: Use this skill when the user asks to "implement in parallel", "parallel implementation", "implement the plan in parallel", "병렬 구현", or wants conflict-aware concurrent execution of an implementation plan using task-level Target Files.
---

# Implementation Execution (Parallel TDD + Built-in Review)

Execute implementation plans with dependency-aware TDD and conflict-aware parallel groups.
Use this skill when maximizing safe concurrency matters.

Keep this body concise. Use `references/` for full scheduling and review details.

## Simplified Workflow

This skill is **Step 3 of 4** in the parallel flow:

```
spec -> feature-draft-parallel / implementation-plan-parallel -> implementation-parallel (this) -> spec-update-done
```

## Hard Rules

- Do not create/edit/delete files under `_sdd/spec/`.
- If spec drift is discovered, report it and hand off to `spec-update-todo` or `spec-update-done`.
- Before tests/runtime commands, apply `_sdd/env.md` setup if present.
- If runtime setup is unknown and `_sdd/env.md` is missing, ask user instead of guessing.

## Inputs

Plan sources:

- `_sdd/implementation/IMPLEMENTATION_PLAN.md`
- `_sdd/implementation/IMPLEMENTATION_PLAN_PHASE_<n>.md`
- `_sdd/drafts/feature_draft_<feature_name>.md` (use Part 2)

Supporting context:

- `_sdd/implementation/IMPLEMENTATION_PROGRESS*.md` (if present)
- repository test/code conventions

If multiple plan sources conflict, ask the user which one to execute.

## Output

- `_sdd/implementation/IMPLEMENTATION_PROGRESS.md`
- `_sdd/implementation/IMPLEMENTATION_PROGRESS_PHASE_<n>.md` (optional)
- `_sdd/implementation/IMPLEMENTATION_REPORT_PHASE_<n>.md`
- `_sdd/implementation/IMPLEMENTATION_REPORT.md`
- in-session progress state via `update_plan`

## Execution Contract

- Keep plan task IDs as canonical IDs.
- Respect dependencies first, then priority (`P0` -> `P3`).
- Use `Target Files` plus semantic dependency checks (shared schema/config/API contracts) to form safe parallel groups.
- Execute edits to the same file sequentially.
- Require test evidence for every completed criterion.

## Workflow

### 1) Load plan and environment

Parse phases, tasks, dependencies, acceptance criteria, and `Target Files`.
Load test/runtime setup from `_sdd/env.md`.

### 2) Determine parallel readiness

- If tasks include `Target Files`, use full parallel grouping.
- If missing for some tasks, infer cautiously and confirm with user when uncertain.
- If reliable grouping is impossible, fall back to sequential execution for that scope.

### 3) Build conflict-aware groups

Within each phase:

- select unblocked tasks
- detect file overlap conflicts from `Target Files`
- detect semantic conflicts even when file paths do not overlap
- group non-conflicting tasks for concurrent execution
- keep conflicting tasks in later/serial groups

Use detailed algorithm in `references/parallel-execution.md`.

### 4) Execute with TDD

For each task criterion:

1. RED: add/adjust failing test
2. GREEN: minimal code to pass
3. REFACTOR: clean while keeping tests green

Run independent group work concurrently where safe. Merge/verify group results before moving on.

### 5) Post-group verification

After each group:

- run relevant test suites (and full suite at checkpoints)
- detect regressions and integration issues
- handle unplanned dependencies
- verify file-boundary compliance (`Target Files`)

### 6) Phase review

Apply cross-cutting checks (security, error handling, performance, test quality, integration).
Fix critical issues before proceeding.

### 7) Final review and report

Run cross-phase review and generate combined report with:

- completion status
- test status
- parallel execution stats
- findings by severity
- readiness verdict (`READY` / `NEEDS_WORK` / `BLOCKED`)

## Progress Report Contract

Each progress update should include:

1. Phase/task scope covered
2. Files changed
3. Tests added/updated and result
4. Parallel groups executed (or sequential fallback reason)
5. Blockers and next tasks

## When to Pause and Ask

Ask user directly when:

- target file boundaries are ambiguous
- plan scope is conflicting or out-of-date
- unresolved dependency blocks all available work
- multiple valid technical choices have meaningful trade-offs

## Integration

- Upstream plans: `feature-draft-parallel` (Part 2), `implementation-plan-parallel`
- Legacy compatibility: can execute non-parallel plans via sequential fallback
- Downstream spec sync: `spec-update-done`

## References

- `references/parallel-execution.md` for grouping/conflict algorithm
- `references/best-practices.md` for TDD execution patterns
- `references/review-checklist.md` for phase/final review gates
- `examples/sample-parallel-session.md` for end-to-end sample run
