---
name: feature-draft-sequential
description: Use this skill when the user asks for "feature draft sequential", "sequential feature draft", "legacy feature draft", "순차 기능 초안", "레거시 기능 계획", or explicitly wants a sequential feature-draft workflow without Target Files.
---

# Feature Draft

Create a single draft file that contains both:

- Part 1: spec patch input (compatible with `spec-update-todo`)
- Part 2: implementation plan (phase/task based)

which is saved as documented under "## Output" section below.

## Simplified Workflow

This skill is **Step 2 of 4** in the simplified SDD workflow:

```
spec -> feature-draft-sequential (this) -> implementation-sequential -> spec-update-done
```

| Step | Skill | Purpose |
|------|-------|---------|
| 1 | spec-create | Create the initial spec document |
| **2** | **feature-draft-sequential** | Draft feature spec patch + implementation plan |
| 3 | implementation-sequential | Execute the implementation plan (TDD + built-in review) |
| 4 | spec-update-done | Sync spec with actual code |

> **Previous workflow** (7 steps): spec -> spec-draft -> spec-update-todo -> implementation-plan-sequential -> implementation-sequential -> implementation-review -> spec-update-done
> **New workflow** (4 steps): spec -> feature-draft-sequential -> implementation-sequential -> spec-update-done

This skill compresses a 3-step flow into one run:
`spec-draft -> spec-update-todo -> implementation-plan-sequential`.

## Hard Rules

- Never modify `_sdd/spec/` files directly in this skill.
- Write output under `_sdd/drafts/` only.
- If multiple features are detected, ask the user whether to keep one combined file or split files.
- Keep Part 1 in strict `Spec Update Input` structure so it can be consumed by `spec-update-todo`.

## Inputs

Primary:

- Current chat requirements

Optional supporting inputs:

- `_sdd/spec/user_draft.md`
- `_sdd/spec/user_spec.md`
- `_sdd/implementation/user_input.md`
- repo changes (`git diff`)
- `_sdd/spec/DECISION_LOG.md`
- current spec index and linked sub-spec files

## Output

- `_sdd/drafts/feature_draft_<feature_name>.md`

Optional archive when file already exists:

- `_sdd/drafts/prev/prev_feature_draft_<name>_<timestamp>.md`

## Downstream Compatibility Contract

Use stable headings and structure so downstream skills can consume this file:

- `# Part 1: Spec Patch Draft`
- `# Spec Update Input`
- `# Part 2: Implementation Plan`

Downstream consumers:

- `implementation-sequential`: reads Part 2 as an executable plan
- `implementation-review`: audits Part 2 against code/tests and generated reports
- `spec-update-done`: uses Part 1 and implementation artifacts to sync spec

## Workflow

### 1) Analyze Input Completeness

Classify user input as:

- HIGH: objective, priority, and acceptance criteria already clear
- MEDIUM: some key fields missing
- LOW: idea-level request only

Use adaptive questioning from `references/adaptive-questions.md`.

### 2) Gather Read-Only Context

- Locate primary spec (`_sdd/spec/<project>.md` or `_sdd/spec/main.md`)
- Follow links if spec is split
- Capture current section map to target patch locations
- Check decision log for constraints and prior rationale

### 3) Clarify Only What Is Missing

Ask targeted questions for missing fields:

- priority/severity
- measurable acceptance criteria
- scope boundaries
- component or config impact

### 4) Design Feature Changes

Categorize requested changes into:

- New Features
- Improvements
- Bug Reports
- Component Changes
- Configuration Changes

Map each item to `Target Section` in existing spec.

### 5) Generate Part 1 (Spec Patch Draft)

Produce `Spec Update Input` compatible content with:

- metadata (`Date`, `Author`, `Target Spec`)
- sectioned change items
- `Target Section` annotations
- acceptance criteria checklists where applicable

### 6) Generate Part 2 (Implementation Plan)

Produce phase-based implementation plan with:

- in-scope / out-of-scope
- components
- phase tables (`ID`, `Task`, `Priority`, `Dependencies`, `Component`)
- task details with acceptance criteria
- risks and open questions

### 7) Save and Summarize

- Save combined draft file
- Report what was included in Part 1 and Part 2
- Recommend next execution path:
  - apply patch with `spec-update-todo`
  - execute plan with `implementation-sequential`

## Quality Gates

Before finalizing:

- Part 1 is parseable as `Spec Update Input`
- Part 2 tasks are actionable and dependency-aware
- no direct spec file edits were made
- unresolved ambiguity is listed explicitly
- section headers follow the downstream compatibility contract

## Integration

Simplified standard flow:

`spec -> feature-draft-sequential -> implementation-sequential -> spec-update-done`

Legacy-compatible path (optional):

`feature-draft-sequential -> spec-update-todo -> implementation-sequential -> implementation-review -> spec-update-done`

## References

- `references/adaptive-questions.md` for completeness-based questioning
- `references/output-format.md` for exact output contract
- `examples/feature_draft.md` for a full sample output
