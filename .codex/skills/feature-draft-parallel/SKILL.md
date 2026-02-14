---
name: feature-draft-parallel
description: Use this skill when the user asks for "feature draft parallel", "parallel feature draft", "parallel feature plan", "병렬 기능 초안", "병렬 기능 계획", or wants requirement clarification + spec patch draft + implementation planning in one workflow with Target Files for parallel execution.
---

# Feature Draft (Parallel)

Create one draft file that includes:

- Part 1: spec patch input (compatible with `spec-update-todo`)
- Part 2: parallel-ready implementation plan (task-level `Target Files` required)

Keep this skill body concise. Use `references/` for detailed templates and rules.

## Simplified Workflow

This skill is **Step 2 of 4** in the parallel SDD flow:

```
spec -> feature-draft-parallel (this) -> implementation-parallel -> spec-update-done
```

| Step | Skill | Purpose |
|------|-------|---------|
| 1 | spec-create | Create the initial spec document |
| **2** | **feature-draft-parallel** | Draft spec patch + parallel-ready implementation plan |
| 3 | implementation-parallel | Execute plan with conflict-aware parallel groups |
| 4 | spec-update-done | Sync spec with actual code |

## Hard Rules

- Do not modify files under `_sdd/spec/` directly.
- Save output only under `_sdd/drafts/`.
- Keep Part 1 in strict `Spec Update Input` structure.
- Include `Target Files` in **every** task in Part 2.
- If multiple features are detected, ask whether to combine into one file or split.

## Language

- Default output language: Korean.
- Keep section headings and schema stable for downstream skills.

## Inputs

Primary:

- Current chat requirements

Optional context:

- `_sdd/spec/user_draft.md`
- `_sdd/spec/user_spec.md`
- `_sdd/implementation/user_input.md`
- repository changes (`git diff`)
- `_sdd/spec/DECISION_LOG.md`
- current spec index and linked sub-spec files

## Output

- `_sdd/drafts/feature_draft_<feature_name>.md`

Optional archive when replacing same filename:

- `_sdd/drafts/prev/prev_feature_draft_<name>_<timestamp>.md`

## Downstream Compatibility Contract

Keep these exact top-level headings:

- `# Part 1: Spec Patch Draft`
- `# Spec Update Input`
- `# Part 2: Implementation Plan`

For Part 2 task details, include:

- `Component`, `Priority`, `Type`, `Description`, `Acceptance Criteria`
- `Target Files` (`[C]`, `[M]`, `[D]` markers)
- `Technical Notes`, `Dependencies`

Downstream consumers:

- `implementation-parallel`: executes Part 2 with conflict-aware grouping
- `implementation`: can execute Part 2 sequentially (ignores Target Files)
- `spec-update-todo` / `spec-update-done`: consume Part 1 for spec sync

## Workflow

### 1) Analyze input completeness

Classify request as HIGH/MEDIUM/LOW and minimize unnecessary questions.
Use `references/adaptive-questions.md`.

### 2) Gather read-only context

- Locate main spec and linked spec files.
- Build section map for `Target Section` annotations.
- Check decision log for constraints.
- Explore codebase structure to plan realistic `Target Files`.

### 3) Clarify only missing fields

Ask concise questions for missing priority, acceptance criteria, scope boundaries, or technical constraints.

### 4) Design changes and map Target Files

- Classify requested changes (feature/improvement/bug/component/config).
- Map each item to a concrete spec `Target Section`.
- Define implementation tasks and assign exact file-level `Target Files`.
- Minimize file overlap across tasks to maximize parallelizability.

### 5) Generate Part 1 (Spec Patch Draft)

Produce `Spec Update Input` compatible content with explicit `Target Section` annotations.

### 6) Generate Part 2 (Parallel-ready Implementation Plan)

Produce phase-based plan with:

- scope and components
- phase tables (`ID`, `Task`, `Priority`, `Dependencies`, `Component`)
- task details with `Target Files`
- `Parallel Execution Summary` (conflicts + max parallel)
- risks and open questions

### 7) Verify and save

Before finalizing:

- every task has valid `Target Files`
- file paths are plausible for the repository
- expected conflict points are explicitly called out
- semantic conflict points (shared schema/config/API contracts) are explicitly called out
- required headings match compatibility contract

Then save and summarize next steps.

## Quality Gates

- Part 1 is parseable as `Spec Update Input`.
- Part 2 tasks are executable and dependency-aware.
- `Target Files` are file-level (not directory-level).
- no direct edits under `_sdd/spec/` were made.
- unresolved ambiguity is listed under Open Questions.

## Integration

- Parallel flow: `spec -> feature-draft-parallel -> implementation-parallel -> spec-update-done`
- Sequential fallback: `feature-draft-parallel -> implementation`

## References

- `references/adaptive-questions.md` for completeness-based questioning
- `references/output-format.md` for exact output schema
- `references/target-files-spec.md` for `Target Files` grammar and conflict rules
- `examples/feature_draft_parallel.md` for a complete sample output
