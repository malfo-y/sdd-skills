---
name: spec-review
description: This skill should be used when the user asks to "review spec", "spec drift check", "verify spec accuracy", "audit spec quality", "review spec against code", "refresh spec review", "스펙 리뷰", "스펙 검토", "스펙 드리프트 점검", or wants a review-only analysis of spec quality and code-to-spec alignment without directly editing spec files.
version: 1.0.0
---

# Spec Review (Strict, Review-Only)

Review SDD spec quality and spec-to-code alignment in strict review-only mode.  
This skill generates findings and recommendations, but does not edit `_sdd/spec/*.md`.

## Hard Rule: No Spec Edits

- This skill performs review and reporting only.
- Never create, modify, rename, or delete spec files under `_sdd/spec/` (except the review report file defined below).
- If spec changes are needed, record them as actionable recommendations and hand off to `/spec-update-done` for actual edits.

## Overview

This skill evaluates two dimensions:

1. **Spec-only quality review**  
- Clarity, completeness, internal consistency, measurable acceptance criteria, structure quality.

2. **Code-linked drift review**  
- Whether implementation, tests, and runtime-facing behavior still match what the spec claims.

## When to Use This Skill

- Before implementation planning to validate spec quality
- After implementation/review cycles to detect drift
- During periodic documentation governance
- When a team wants findings first, and spec edits only after approval

## Inputs

### Primary
- `_sdd/spec/<project>.md` or `_sdd/spec/main.md`
- Linked sub-spec files (if split spec structure exists)

### Secondary
- `_sdd/implementation/IMPLEMENTATION_PLAN.md`
- `_sdd/implementation/IMPLEMENTATION_PROGRESS.md`
- `_sdd/implementation/IMPLEMENTATION_REVIEW.md`
- Recent code changes (`git diff`, `git log`, current workspace state)
- Test artifacts (when available)

## Review Process

### Step 1: Scope and Source Selection

1. Identify main spec index file.
2. Enumerate linked sub-spec files.
3. Exclude generated/backup files (`SUMMARY.md`, `prev/PREV_*.md`) from primary analysis.
4. Define review scope:
   - Spec-only
   - Spec + code alignment (default)

### Step 2: Spec-Only Quality Audit

Assess the spec as a standalone design artifact:

- **Clarity**: ambiguous wording, undefined terms
- **Completeness**: missing requirements, missing acceptance criteria
- **Consistency**: conflicting statements across sections/files
- **Testability**: whether requirements can be objectively verified
- **Navigability**: structure, section discoverability, cross-links
- **Ownership**: responsibility boundaries and decision ownership

### Step 3: Code-Linked Drift Audit

Compare spec claims to implementation evidence:

- **Architecture drift**: undocumented/new/removed components
- **Feature drift**: planned vs implemented vs documented behavior
- **API drift**: endpoint/method/schema changes
- **Config drift**: env vars/defaults/dependency versions
- **Issue drift**: resolved issues still open in spec, or new issues undocumented

Require concrete evidence wherever possible:
- `path:line` references
- test names/status
- commit or diff references

### Step 4: Severity and Decision

Classify findings:
- `High`: architecture breaks, security/reliability risks, contradictory spec claims
- `Medium`: behavior mismatch, missing acceptance criteria, important doc gaps
- `Low`: style/organization/non-blocking documentation quality issues

Assign one overall decision:
- `SPEC_OK`: no material drift or quality blockers
- `SYNC_REQUIRED`: spec updates are needed before next planning/release step
- `NEEDS_DISCUSSION`: key ambiguities/trade-offs require product/architecture decisions

### Step 5: Report and Handoff

1. Create/update strict review report.
2. Do not edit actual spec content.
3. If decision is `SYNC_REQUIRED`, include a ready-to-apply update checklist and recommend running `/spec-update-done`.

## Output

### Report File

- Default path: `_sdd/spec/SPEC_REVIEW_REPORT.md`
- If the file already exists, archive it first:
  - `_sdd/spec/prev/PREV_SPEC_REVIEW_REPORT_<timestamp>.md` (create `_sdd/spec/prev/` if missing)

### Report Format

```markdown
# Spec Review Report (Strict)

**Date**: YYYY-MM-DD
**Reviewer**: Claude
**Scope**: Spec-only | Spec+Code
**Spec Files**: [list]
**Code State**: <commit hash or workspace summary>
**Decision**: SPEC_OK | SYNC_REQUIRED | NEEDS_DISCUSSION

## Executive Summary
- <one-paragraph summary>

## Findings by Severity

### High
1. <finding>
   - Evidence: `path:line`, tests, diff references
   - Impact:
   - Recommendation:

### Medium
...

### Low
...

## Spec-Only Quality Notes
- Clarity:
- Completeness:
- Consistency:
- Testability:
- Structure:

## Spec-to-Code Drift Notes
- Architecture:
- Features:
- API:
- Configuration:
- Issues/Technical debt:

## Open Questions
1. <question requiring decision>

## Suggested Next Actions
1. <action>
2. <action>

## Handoff for Spec Updates (if SYNC_REQUIRED)
- Recommended command: `/spec-update-done`
- Update priorities:
  - P1:
  - P2:
  - P3:
```

## Guardrails

- Do not present assumptions as facts; label unknowns clearly.
- Prefer evidence-backed findings over broad statements.
- Separate objective drift findings from subjective design suggestions.
- Keep recommendations actionable and ordered by risk/impact.

## Integration with Other Skills

- **spec-update-done**: apply approved spec updates after this review
- **spec-update-todo**: add planned requirements before implementation
- **implementation-review**: verify plan/task completion against acceptance criteria
- **spec-summary**: regenerate summary after approved updates are applied

## Additional Resources

### Reference Files
- `references/review-checklist.md` - strict review checklist and decision rules

### Example Files
- `examples/spec-review-report.md` - sample strict review report output
