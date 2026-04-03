# Spec Format Reference (Current Canonical Model)

Checklist-style reference for the expected section structure and preservation rules. This is not a generation template. It defines what the current SDD global spec model expects after migration.

---

## Global Spec Core

| Order | Section | Purpose | Required |
|------|---------|---------|----------|
| 1 | Background & High-Level Concept | 문제, 개념, 대안 대비 선택 이유 | Yes |
| 2 | Scope / Non-goals / Guardrails | 책임 범위와 경계 고정 | Yes |
| 3 | Core Design & Key Decisions | 유지해야 할 설계 구조와 핵심 결정 | Yes |
| 4 | Contract / Invariants / Verifiability | 계약, 불변조건, 검증 연결 | Yes |
| 5 | Usage Guide & Expected Results | 시나리오와 기대 결과 | Yes |
| 6 | Decision-Bearing Structure | 시스템 경계, ownership, cross-component contract 등 | Yes |
| 7 | Reference Information | 데이터 모델, API, 환경 및 설정 | If useful |
| A | Strategic Code Map | selective navigation hint | Optional appendix |
| B | Related Docs & Code References | 관련 문서 / citation index | Optional appendix |

## Temporary Spec Reference

Temporary spec은 global spec과 다른 shape를 가진다.

| Order | Section | Required |
|------|---------|----------|
| 1 | Change Summary | Yes |
| 2 | Scope Delta | Yes |
| 3 | Contract/Invariant Delta | Yes |
| 4 | Touchpoints | Yes |
| 5 | Implementation Plan | Yes |
| 6 | Validation Plan | Yes |
| 7 | Risks / Open Questions | Yes |

## CIV Canonical Shape

### Contract

| ID | Subject | Inputs/Outputs | Preconditions | Postconditions | Failure Guarantees |
|----|---------|----------------|---------------|----------------|--------------------|

### Invariants

| ID | Scope | Invariant | Why It Matters |
|----|-------|-----------|----------------|

### Verifiability

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|

`Verification Method` enum:

- `test`
- `review`
- `runtime-check`
- `manual-check`

## Preservation Rules

These elements must be preserved or explicitly reconstructed during migration.

### Must Preserve

- 문제 정의와 high-level concept
- scope와 non-goals 경계
- 유지해야 할 핵심 설계 결정
- 실제로 중요한 contract와 invariant
- 사용 시나리오와 기대 결과

### Must Reconstruct If Missing

- `Contract / Invariants / Verifiability`
- explicit scope / non-goals / guardrails
- decision-bearing structure

### Must Not Be Treated As Mandatory Main-Body Structure

- exhaustive architecture inventory
- exhaustive component inventory
- class/function list copied from code
- implementation details that do not carry decisions

### Strategic Code Map Rule

- appendix-level hint로만 유지
- manual curated가 기본값
- entrypoint / invariant hotspot / extension point / change hotspot 위주
- 단순 파일 나열은 금지
