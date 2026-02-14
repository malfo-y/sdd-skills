---
name: implementation-review
description: Use this skill to review implementation progress against the plan, verify acceptance criteria, identify issues, and determine next steps. Triggered by "review implementation", "check progress", "verify implementation", "what's done", "implementation status", or "audit the code".
---

# Implementation Review

> **Simplified Workflow Note**: This skill is part of the **legacy workflow**.
> In the simplified 4-step workflow (`spec -> feature-draft -> implementation -> spec-update-done`),
> the `implementation` skill already includes in-phase and final reviews.
> Use this skill as an optional standalone audit path.

Run an independent audit of implementation status and report readiness with evidence.

Always output the report as documented under "## Output" section below.

## Hard Rule

- Do not modify files under `_sdd/spec/`.
- If spec changes are needed, report them as follow-up actions and hand off to `spec-update-todo` or `spec-update-done`.

## Language

- Default report language: Korean.
- Keep labels and evidence precise and technical.

## Inputs

- Plan artifacts:
  - `_sdd/implementation/IMPLEMENTATION_PLAN*.md`
  - `_sdd/drafts/feature_draft_<feature_name>.md` (use Part 2 as plan baseline when relevant)
- Progress and review artifacts:
  - `_sdd/implementation/IMPLEMENTATION_PROGRESS*.md`
  - `_sdd/implementation/IMPLEMENTATION_REPORT.md`
  - `_sdd/implementation/IMPLEMENTATION_REPORT_PHASE_<n>.md`
- Code and tests in repository
- Optional: `_sdd/implementation/IMPLEMENTATION_REVIEW.md` (previous report)
- Optional runtime setup: `_sdd/env.md`

If multiple phase files exist and user does not specify scope:

- default to latest phase review
- ask user if they want all phases reviewed

## Output

- `_sdd/implementation/IMPLEMENTATION_REVIEW.md`
- If overwriting, archive previous report under `_sdd/implementation/prev/PREV_IMPLEMENTATION_REVIEW_<timestamp>.md`

## Review Dimensions

1. Task completion versus plan
2. Acceptance-criteria satisfaction
3. Test evidence quality (coverage, pass/fail, risk)
4. Defects, regressions, and technical debt
5. Release readiness and next actions
6. Consistency between generated reports and real code state

## Workflow

### 1) Select Baseline and Build Inventory

- Select baseline plan source (`IMPLEMENTATION_PLAN*` or feature draft Part 2).
- Enumerate planned tasks and criteria.
- Record dependencies and priorities.
- Mark scope expected for the current phase.

### 2) Verify Implemented State

- Map tasks to actual code changes and artifacts.
- Confirm whether each criterion is implemented, partial, or missing.
- Verify claims in progress logs with file-level evidence.

### 3) Evaluate Test Evidence

- Confirm tests exist for critical behavior and edge cases.
- Check failing tests and flaky patterns.
- Identify untested high-risk paths.

### 4) Cross-check Generated Reports (If Present)

When `IMPLEMENTATION_REPORT*` exists:

- validate that report claims match code/tests
- flag any mismatch between report status and real state
- capture drift between phase reports and final report

### 5) Classify Findings

Use severity levels:

- Critical: incorrect behavior, security risk, or release blocker
- High: significant acceptance gap or regression risk
- Medium: quality or maintainability risk
- Low: polish and non-blocking improvements

### 6) Produce Verdict and Actions

- Summarize readiness (`READY`, `PARTIAL`, `NOT_READY`).
- Provide prioritized next actions with explicit owners/scope when possible.
- Include open questions that block closure.

## Report Contract

Keep report sections concise and fixed:

1. Progress Overview (tasks/criteria completion)
2. Findings by severity
3. Test Status and blind spots
4. Recommended Next Steps
5. Final readiness verdict

For quick checks, allow an abbreviated report with the same fields.

## When to Escalate

Ask the user directly when:

- A criterion is ambiguous and evidence is inconclusive.
- Multiple valid remediations have meaningful trade-offs.
- Environment limitations prevent reliable verification.
- Multiple plan baselines conflict and cannot be reconciled.

## Integration

- Source of truth for expected work: `implementation-plan`, `feature-draft` (Part 2)
- Execution remediation: `implementation` (which now includes built-in phase/final reviews)
- Spec sync follow-up: `spec-update-done`

## References

- `references/review-checklist.md` for full checklist.
- `examples/sample-review.md` for full report style.
