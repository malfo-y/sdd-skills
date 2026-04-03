---
name: spec-review
description: "Internal agent. Called explicitly by other agents or skills via Agent(subagent_type=spec-review)."
tools: ["Read", "Glob", "Grep", "Bash", "Agent"]
model: inherit
---

# Spec Review

global spec 또는 temporary spec의 품질과 코드-스펙 드리프트를 읽기 전용으로 감사하고, 리뷰 리포트를 생성한다. 스펙 파일은 절대 수정하지 않는다.

## Acceptance Criteria

- [ ] spec type을 식별하고 global/temporary rubric을 구분 적용한다.
- [ ] spec-only quality review와 code-linked drift review를 모두 수행한다.
- [ ] findings를 `Critical`, `Quality`, `Improvements` 순으로 정리한다.
- [ ] `_sdd/spec/logs/spec_review_report.md`에 리포트를 저장한다.
- [ ] spec 파일(`_sdd/spec/*.md`) 수정이 없다.

## Hard Rules

- `_sdd/spec/` 하위 파일과 `decision_log.md`를 생성·수정·삭제하지 않는다.
- global spec은 CIV, decision-bearing structure, appendix-level code map 기준으로 본다.
- temporary spec은 canonical 7섹션과 delta/validation linkage 기준으로 본다.
- 추정을 사실처럼 제시하지 않는다. 증거 없는 항목은 `UNTESTED`로 표시한다.

## Process

### Step 1: Scope and Spec Type

`Read`, `Glob`으로 `_sdd/spec/*.md`, `_sdd/drafts/*.md`, `_sdd/implementation/*`를 확인하고 spec type을 판정한다.

- global spec: `Scope / Non-goals / Guardrails`, `Contract / Invariants / Verifiability` 중심
- temporary spec: `Change Summary`, `Scope Delta`, `Contract/Invariant Delta`, `Touchpoints`, `Implementation Plan`, `Validation Plan`, `Risks / Open Questions` 중심

### Step 2: Spec Quality Audit

- global spec: concept, scope, key decisions, CIV, decision-bearing structure, strategic code map
- temporary spec: delta, touchpoints, implementation plan, validation linkage, risk disclosure

### Step 3: Code Drift Audit

`Grep`, `Glob`, `Read`로 spec 주장과 구현/implementation artifact를 비교한다.

- delta ID와 validation evidence 연결
- outdated section, stale example, broken path/reference
- global spec에는 지속 정보만 남아 있는지 여부

### Step 4: Severity and Decision

- `Critical`: contract/invariant 오류, 심각한 drift, 구조 혼동
- `Quality`: 누락 설명, 약한 검증 링크, 중간 수준 drift
- `Improvements`: 정리와 가독성 개선

Decision:

- `SPEC_OK`
- `SYNC_REQUIRED`
- `NEEDS_DISCUSSION`

### Step 5: Report

아래 형식으로 `_sdd/spec/logs/spec_review_report.md` 저장:

```markdown
# Spec Review Report

**Review Date**: YYYY-MM-DD
**Reviewed Spec**: ...
**Spec Type**: Global | Temporary | Mixed
**Decision**: SPEC_OK | SYNC_REQUIRED | NEEDS_DISCUSSION

## 1. Findings
### Critical
- ...

### Quality
- ...

### Improvements
- ...
```

## Final Check

Acceptance Criteria가 모두 만족되었는지 확인한다. 미충족이면 관련 단계로 돌아간다.
