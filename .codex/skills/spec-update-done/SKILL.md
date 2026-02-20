---
name: spec-update-done
description: This skill should be used when the user asks to "review spec", "update spec from code", "sync spec with implementation", "spec drift check", "verify spec accuracy", "refresh spec document", "spec needs update", or mentions spec document maintenance, code-to-spec synchronization, or implementation log analysis.
---

# Spec Update from Implemented State

Synchronize `_sdd/spec/` with implementation evidence and review artifacts.

## Simplified Workflow

This skill is **Step 4 of 4** in the simplified SDD workflow:

```
spec -> feature-draft -> implementation -> spec-update-done (this)
```

| Step | Skill | Purpose |
|------|-------|---------|
| 1 | spec-create | Create the initial spec document |
| 2 | feature-draft | Draft feature spec patch + implementation plan |
| 3 | implementation | Execute the implementation plan (TDD + built-in review) |
| **4** | **spec-update-done** | Sync spec with actual code |

> **Previous workflow** (7 steps): spec -> spec-draft -> spec-update-todo -> implementation-plan -> implementation -> implementation-review -> spec-update-done
> **New workflow** (4 steps): spec -> feature-draft -> implementation -> spec-update-done

## Purpose

- Reduce drift between implementation and spec.
- Keep changes traceable to concrete evidence.
- Preserve rationale in `DECISION_LOG.md` when decisions changed.

## Inputs

- Spec documents:
  - `_sdd/spec/<project>.md` or `_sdd/spec/main.md` (+ linked sub-specs)
- Implementation artifacts:
  - `_sdd/implementation/IMPLEMENTATION_PLAN.md`
  - `_sdd/implementation/IMPLEMENTATION_PROGRESS*.md`
  - `_sdd/implementation/IMPLEMENTATION_REVIEW.md`
  - `_sdd/implementation/IMPLEMENTATION_REPORT.md`
  - `_sdd/implementation/IMPLEMENTATION_REPORT_PHASE_<n>.md`
- Feature draft artifacts:
  - `_sdd/drafts/feature_draft_<name>.md` (Part 1 patch draft + Part 2 plan)
- Code evidence:
  - git diff, recent commits, current workspace
- Conversation feedback and corrections
- Optional:
  - `_sdd/spec/DECISION_LOG.md`
  - `_sdd/env.md`
  - `_sdd/implementation/IMPLEMENTATION_INDEX.md` (if present)

## Outputs

- Updated `_sdd/spec/*.md`
- Backups: `_sdd/spec/prev/PREV_<file>_<timestamp>.md`
- Optional decision-log updates: `_sdd/spec/DECISION_LOG.md`
- Feature archive copies: `_sdd/implementation/features/<feature_id>/...`
- Updated artifact index: `_sdd/implementation/IMPLEMENTATION_INDEX.md`

## Workflow

### 1) Identify Scope

1. Identify main/index spec.
2. Include linked sub-spec files.
3. Determine `feature_id` for this sync:
   - use user-provided `feature_id` if explicitly given
   - else derive from `feature_draft_<name>.md` when a matching draft exists (`<name>` -> `feature_id`)
   - else derive from current implementation plan/report title if unambiguous
   - else ask user before archiving
4. Exclude generated backups (`SUMMARY.md`, `prev/PREV_*`).

### 2) Collect Evidence and Detect Drift

Compare:

- spec claims
- actual code behavior
- implementation progress/review/report claims
- feature-draft intent (Part 1/Part 2), when present

Classify drift:

- Feature drift
- API/interface drift
- Config/runtime drift
- Status drift (planned/in-progress/completed)
- Report drift (generated report claims vs real state)

### 3) Choose Update Strategy

Choose based on scope:

- Quick Sync: localized updates
- Section Update: feature/component-level updates
- Full Refresh: broad or structural drift

Use `references/update-strategies.md` for detailed patterns.

### 4) Backup and Apply Updates

For each spec file to edit:

1. create `prev/PREV_*` backup
2. patch only relevant sections
3. preserve links/cross-references
4. update status markers (`✅/🚧/📋/⏸️`)

### 5) Update Decision Log and Changelog

If rationale changed, append/update `DECISION_LOG.md`.
Refresh version/date/change notes in spec.

### 6) Validate and Summarize

Validate before finishing:

- links resolve
- no duplicated/conflicting statements
- no statement contradicts verified code

Publish summary:

- changed files
- key synced sections
- unresolved questions

### 7) Archive Implementation Artifacts by Feature (Copy-only)

After spec sync is complete, archive implementation artifacts for the resolved `feature_id`.

Rules:

1. Never move/delete root artifacts under `_sdd/implementation/`; copy only.
2. Create feature directory if missing:
   - `_sdd/implementation/features/<feature_id>/`
3. Collect and copy existing files (if present):
   - `IMPLEMENTATION_PLAN*.md`
   - `IMPLEMENTATION_PROGRESS*.md`
   - `IMPLEMENTATION_REVIEW.md`
   - `IMPLEMENTATION_REPORT*.md`
   - `TEST_SUMMARY.md`
4. Use timestamped destination filenames to prevent overwrite:
   - `_sdd/implementation/features/<feature_id>/SYNC_<YYYYMMDD_HHMMSS>_<original_filename>`
5. Create/update `_sdd/implementation/IMPLEMENTATION_INDEX.md`:
   - keep one section per `feature_id`
   - append a new sync record with:
     - `synced_at` (UTC)
     - copied file list (`destination <- source`)
     - optional note (e.g., spec files updated in this run)
6. If `feature_id` cannot be determined reliably, ask user and skip archive step until confirmed.

## Spec Split Guidance

If the main spec is too large, ask user whether to split.
When splitting:

- keep main file as index/overview
- move detailed topics to linked sub-spec files
- keep consistent suffixes (`_API`, `_DATA_MODEL`, `_COMPONENTS`, etc.)

## Quality Gates

- every edited file has backup
- each major change is traceable to evidence
- rationale changes are recorded
- uncertainty is labeled explicitly (no silent assumptions)
- feature archive step is copy-only and `IMPLEMENTATION_INDEX.md` is updated when archive runs

## When to Ask User

Ask user when:

- code/log/requirements conflict
- intent is ambiguous with multiple valid interpretations
- breaking-change reflection is uncertain
- spec split/restructure decision is needed

## Integration

Recommended flows:

`feature-draft` -> `implementation` -> `spec-update-done`

Optional standalone audit path:

`implementation-review` -> `spec-update-done` -> `spec-summary`

## References

- `references/drift-patterns.md`: drift diagnosis patterns
- `references/update-strategies.md`: update strategy and conflict handling
- `examples/review-report.md`: update report example
