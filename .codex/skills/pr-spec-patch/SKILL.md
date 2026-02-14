---
name: pr-spec-patch
description: This skill should be used when the user asks to "create spec patch from PR", "PR spec patch", "compare PR with spec", "PR to spec", "PR 스펙 패치", "PR 리뷰 준비", "스펙 패치 생성", "PR 변경사항 스펙 반영", or wants to generate a spec patch document by comparing a pull request against the current specification.
---

# PR Spec Patch

Create a spec patch draft by comparing PR changes against the current spec.

## Hard Rule

- Do not edit files under `_sdd/spec/` in this skill.
- Only produce/update `_sdd/pr/spec_patch_draft.md`.
- Final spec application is handled later by `spec-update-todo`.

## Prerequisites

- `gh` CLI is authenticated.
- PR number is provided or discoverable from current branch.
- A baseline spec exists (recommended). If missing, continue with explicit `baseline missing` note only when user agrees.

## Inputs

- Current spec index and linked sub-specs (`_sdd/spec/`)
- PR metadata/diff from GitHub
- Existing draft (`_sdd/pr/spec_patch_draft.md`) if present
- User clarifications in conversation

## Output

- `_sdd/pr/spec_patch_draft.md`

## Modes

### Mode A: Create New Draft

1. Validate prerequisites and pick target spec file(s).
2. Collect PR metadata and changed files.
3. Map code changes to spec sections/components.
4. Draft patch content in `Spec Update Input` compatible structure.
5. Record unresolved questions and assumptions.

### Mode B: Update Existing Draft

1. Load existing draft.
2. Confirm whether current request matches the same PR.
3. Apply edits requested in conversation (add/remove/refine items).
4. Update metadata and unresolved-question status.

## Patch Mapping Rules

Classify PR changes into:

- New Features
- Improvements
- Bug Fixes
- Component/API Changes
- Configuration/Operational Changes

For each item include:

- What changed
- Why spec update is needed
- Evidence pointer (file/path level)
- Acceptance criteria impact (if any)

## Draft Contract

Keep draft sections fixed:

1. PR Summary
2. Spec Patch Content (`Spec Update Input` compatible)
3. Open Questions / Proposals
4. Metadata (PR number, date, status)

## Edge Cases

- Multiple spec files: ask user which should be baseline index.
- Very large PR: summarize by component first, then detail high-impact changes.
- Existing draft for different PR: ask user whether to archive and regenerate.

## Integration

- Generate patch: `pr-spec-patch`
- Validate implementation vs spec: `pr-review`
- Apply spec updates: `spec-update-todo`

## References

- `references/gh-commands.md` for PR data collection commands.
- `examples/spec_patch_draft.md` for expected draft format.
