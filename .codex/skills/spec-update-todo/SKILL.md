---
name: spec-update-todo
description: This skill should be used when the user asks to "update spec with features", "add features to spec", "update spec from input", "add requirements to spec", "spec update", "expand spec", "add to-do to spec", "add to-implement to spec", or mentions adding new features, requirements, or planned improvements to an existing specification document.
---

# Spec Update from Planned Inputs

Update spec documents with newly requested features, improvements, and planned work.

## Purpose

- Capture new scope in `_sdd/spec/` before implementation.
- Keep spec structure maintainable as scope grows.
- Preserve rationale in `DECISION_LOG.md` when important decisions change.

## Inputs

### Conversation Inputs

- User-provided requirements directly in chat.

### File Inputs

- `_sdd/spec/user_spec.md`
- `_sdd/spec/user_draft.md`

If both files exist, ask the user which one to apply first.

### Optional Context

- `_sdd/spec/DECISION_LOG.md`
- Existing split spec files linked from index/main spec

## Output

- Updated spec files under `_sdd/spec/`
- Optional decision-log entry updates
- Processed input file rename:
  - `user_spec.md` -> `_processed_user_spec.md`
  - `user_draft.md` -> `_processed_user_draft.md`

## Workflow

### 1) Select Target Spec Scope

- Identify main/index spec file (`_sdd/spec/<project>.md` preferred, `main.md` fallback).
- If multiple candidates exist, ask the user directly.
- If spec is split, follow index links and update the right file(s).

### 2) Check Maintainability

If spec is becoming too large (for example >500 lines or poor navigation), ask whether to split.
If splitting is approved:

- Keep index spec as overview
- Move large topics to linked sub-specs with consistent names

### 3) Backup Before Edit

For each file to be edited:

- Create `_sdd/spec/prev/PREV_<filename>_<timestamp>.md`

### 4) Map Inputs to Spec Sections

Map each requested item to the right section type:

- New Features
- Improvements
- Bug/Issue Updates
- Component/API/Config Changes

Use section mapping guidance from `references/section-mapping.md`.

### 5) Apply Structured Updates

- Add clear descriptions and measurable acceptance criteria.
- Mark status as planned (`📋`) unless user specifies otherwise.
- Keep wording testable and avoid ambiguous adjectives.

### 6) Update Decision Log (When Needed)

If update introduces a meaningful architectural/product decision, append concise rationale to `_sdd/spec/DECISION_LOG.md`.

### 7) Mark Input Files as Processed

After successful application, rename processed input files and append lightweight processing metadata comments.

### 8) Publish Update Summary

Summarize:

- Files changed
- Features/improvements added
- Open questions
- Recommended next skill (`implementation-plan` or `implementation`)

## Update Quality Gates

Before finishing:

- No conflicting statements across split spec files
- Acceptance criteria are present for material additions
- Links from index to sub-spec files are valid
- Backups were created for all modified files

## Error Handling

- Missing `_sdd/spec/`: create directory and ask user for target spec filename.
- Ambiguous input text: ask targeted clarifying questions.
- Conflicting requests: present options and ask user to choose one.

## Integration

Typical sequence:

`spec-draft` -> `spec-update-todo` -> `implementation-plan` -> `implementation` -> `spec-update-done`

## References

- `references/input-format.md` for detailed input schema.
- `references/section-mapping.md` for section placement rules.
- `examples/user_spec.md` and `examples/update-summary.md` for examples.
