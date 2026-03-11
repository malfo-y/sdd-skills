# Spec Review Checklist (Strict) / 스펙 리뷰 체크리스트 (Strict)

Use this checklist for review-only spec validation.
This checklist does not authorize direct spec edits.

## 1) Scope Setup / 범위 설정

- [ ] Main spec index identified (`_sdd/spec/<project>.md` or `_sdd/spec/main.md`)
- [ ] Linked sub-spec files identified
- [ ] Generated/backup files excluded (`SUMMARY.md`, `prev/PREV_*.md`)
- [ ] `_sdd/spec/DECISION_LOG.md` loaded if present
- [ ] Review scope declared (Spec-only or Spec+Code)
- [ ] If local runtime/test checks are planned, `_sdd/env.md` is checked and setup is applied first

## 2) Spec-Only Quality Checks / 스펙 품질 검증

- [ ] Goals and scope are explicit and non-conflicting
- [ ] Acceptance criteria are present and measurable
- [ ] Terms and abbreviations are defined
- [ ] No contradictory statements across sections/files
- [ ] Component responsibilities and ownership boundaries are clear
- [ ] Each component explains _why_ it exists (design motivation, problem solved), not just _what_ it does — flag components with only Purpose but no Why/rationale
- [ ] Section flow is navigable and links are valid

## 3) Code-Linked Drift Checks / 코드 연동 드리프트 검증

- [ ] Architecture claims match current code structure
- [ ] Feature behavior claims match implementation
- [ ] API endpoints/methods/schemas match runtime behavior
- [ ] Config/env/dependency claims match actual project state
- [ ] Issue status in spec reflects implementation/test reality
- [ ] Decision-log assumptions/rationale still match implementation behavior

## 3.5) Drift Summary Presentation / 드리프트 요약 제시

- [ ] Drift findings summarized in category x severity table before proceeding to severity classification
- [ ] Table covers: Architecture, Feature, API, Config, Issue, Decision-log drift categories

## 4) Evidence Quality / 근거 품질

- [ ] Each high/medium finding has concrete evidence (`path:line`, test, diff, commit)
- [ ] Unknowns are explicitly marked as unknown
- [ ] Inference vs direct evidence is clearly distinguished

## 5) Decision Rule / 판정 기준

Choose one:

- [ ] `SPEC_OK`
  - No high findings
  - No unresolved medium findings that block planning/release

- [ ] `SYNC_REQUIRED`
  - At least one high finding, or multiple medium findings requiring spec correction

- [ ] `NEEDS_DISCUSSION`
  - Core ambiguity/trade-off unresolved by available evidence

## 6) Report Completeness / 리포트 완성도

- [ ] Executive summary included
- [ ] Findings grouped by severity
- [ ] Spec-only quality notes included
- [ ] Spec-to-code drift notes included
- [ ] Open questions included
- [ ] Prioritized next actions included
- [ ] Decision-log follow-up proposals included when rationale drift is found
- [ ] Handoff instructions included when `SYNC_REQUIRED`

## 7) Strict Mode Validation / Strict 모드 검증

- [ ] No spec file under `_sdd/spec/` was edited (other than report file)
- [ ] `_sdd/spec/DECISION_LOG.md` was not edited directly in this skill
- [ ] Report saved to `_sdd/spec/SPEC_REVIEW_REPORT.md`
- [ ] Existing report archived as `_sdd/spec/prev/PREV_SPEC_REVIEW_REPORT_<timestamp>.md` if overwritten
