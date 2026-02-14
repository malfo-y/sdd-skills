---
name: pr-review
description: This skill should be used when the user asks to "review PR", "PR review", "review PR against spec", "PR 리뷰", "PR 검증", "스펙 기반 PR 리뷰", "PR 승인 검토", or wants to verify a pull request's implementation against the specification and spec patch draft.
---

# PR Review (Spec-Based)

Review PR implementation against the current spec and spec patch draft, then issue a structured verdict.

Always output the report as documented under "## Output" section below.

## Hard Rule

- Do not modify `_sdd/spec/` in this skill.
- Record needed spec changes as review findings only.
- Actual spec updates are performed later via `spec-update-todo`.

## Language

- Default report language: Korean.

## Inputs

- Baseline spec (`_sdd/spec/` index + linked files)
- Spec patch draft (`_sdd/pr/spec_patch_draft.md`, if available)
- PR metadata and diff
- Test evidence (CI results, local test output when available)

## Output

- `_sdd/pr/PR_REVIEW.md`

## Review Workflow

### 1) Collect Review Baseline

- Confirm target PR.
- Load baseline spec and patch draft.
- Gather changed files and key commits.

### 2) Validate Against Acceptance Intent

For each significant change, determine:

- Expected behavior from spec
- Implemented behavior from code/diff
- Whether behavior matches, diverges, or is missing

### 3) Evaluate Quality and Risk

Check:

- Functional correctness
- Regression risk
- Test sufficiency
- Security/performance impacts (if relevant)
- Backward compatibility concerns

### 4) Build Gap Analysis

Classify findings:

- Spec mismatch
- Missing requirement coverage
- Extra undocumented behavior
- Test/evidence gap

### 5) Issue Verdict

Use one verdict:

- `APPROVE`: no blocking issues
- `REQUEST_CHANGES`: at least one blocking issue
- `NEEDS_DISCUSSION`: major ambiguity or trade-off decision required

## Report Contract

Keep report sections fixed:

1. Verdict and rationale
2. Metrics summary (files, tests, major gaps)
3. Acceptance/spec compliance check
4. Gap analysis with severity
5. Recommended next actions
6. Reviewer notes and assumptions

## Edge Cases

- No spec file: perform limited PR-only review and explicitly mark baseline missing.
- Multiple spec candidates: ask user which is authoritative.
- Missing patch draft: continue review, then recommend running `pr-spec-patch`.

## Integration

- Patch drafting: `pr-spec-patch`
- Spec sync after merge: `spec-update-todo` or `spec-update-done`

## References

- `references/review-checklist.md` for detailed checklist.
- `examples/sample-review.md` for full report style.
