# Spec Review Checklist (Strict)

Use this checklist for review-only spec validation.  
This checklist does not authorize direct spec edits.

## 1) Scope Setup

- [ ] Main spec index identified (`_sdd/spec/<project>.md` or `_sdd/spec/main.md`)
- [ ] Linked sub-spec files identified
- [ ] Generated/backup files excluded (`SUMMARY.md`, `prev/PREV_*.md`)
- [ ] Review scope declared (Spec-only or Spec+Code)

## 2) Spec-Only Quality Checks

- [ ] Goals and scope are explicit and non-conflicting
- [ ] Acceptance criteria are present and measurable
- [ ] Terms and abbreviations are defined
- [ ] No contradictory statements across sections/files
- [ ] Component responsibilities and ownership boundaries are clear
- [ ] Section flow is navigable and links are valid

## 3) Code-Linked Drift Checks

- [ ] Architecture claims match current code structure
- [ ] Feature behavior claims match implementation
- [ ] API endpoints/methods/schemas match runtime behavior
- [ ] Config/env/dependency claims match actual project state
- [ ] Issue status in spec reflects implementation/test reality

## 4) Evidence Quality

- [ ] Each high/medium finding has concrete evidence (`path:line`, test, diff, commit)
- [ ] Unknowns are explicitly marked as unknown
- [ ] Inference vs direct evidence is clearly distinguished

## 5) Decision Rule

Choose one:

- [ ] `SPEC_OK`
  - No high findings
  - No unresolved medium findings that block planning/release

- [ ] `SYNC_REQUIRED`
  - At least one high finding, or multiple medium findings requiring spec correction

- [ ] `NEEDS_DISCUSSION`
  - Core ambiguity/trade-off unresolved by available evidence

## 6) Report Completeness

- [ ] Executive summary included
- [ ] Findings grouped by severity
- [ ] Spec-only quality notes included
- [ ] Spec-to-code drift notes included
- [ ] Open questions included
- [ ] Prioritized next actions included
- [ ] Handoff instructions included when `SYNC_REQUIRED`

## 7) Strict Mode Validation

- [ ] No spec file under `_sdd/spec/` was edited (other than report file)
- [ ] Report saved to `_sdd/spec/SPEC_REVIEW_REPORT.md`
- [ ] Existing report archived as `_sdd/spec/prev/PREV_SPEC_REVIEW_REPORT_<timestamp>.md` if overwritten
