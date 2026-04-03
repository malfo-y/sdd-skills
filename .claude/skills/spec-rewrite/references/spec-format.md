# Spec Rewrite Format Reference (Current Canonical Model)

Validation and preservation reference aligned with `docs/SDD_SPEC_DEFINITION.md`.
This is not a generation template. It defines what structure and explanation quality the rewrite should preserve or improve.

---

## Global Spec Canonical Shape

| Order | Section | Required |
|------|---------|----------|
| 1 | Background & High-Level Concept | Yes |
| 2 | Scope / Non-goals / Guardrails | Yes |
| 3 | Core Design & Key Decisions | Yes |
| 4 | Contract / Invariants / Verifiability | Yes |
| 5 | Usage Guide & Expected Results | Yes |
| 6 | Decision-Bearing Structure | Yes |
| 7 | Reference Information | If useful |
| A | Strategic Code Map | Optional appendix |

## Temporary Spec Canonical Shape

| Order | Section | Required |
|------|---------|----------|
| 1 | Change Summary | Yes |
| 2 | Scope Delta | Yes |
| 3 | Contract/Invariant Delta | Yes |
| 4 | Touchpoints | Yes |
| 5 | Implementation Plan | Yes |
| 6 | Validation Plan | Yes |
| 7 | Risks / Open Questions | Yes |

## Explanation Quality Checks

### Global Spec

- 문제와 high-level concept가 보이는가
- scope와 non-goals가 경계 역할을 하는가
- CIV가 명시되어 있는가
- decision-bearing structure가 inventory보다 앞서는가
- usage와 expected result가 있는가

### Temporary Spec

- 이번 변경의 목적과 delta가 명확한가
- contract/invariant delta와 validation linkage가 보이는가
- touchpoints와 implementation plan이 실행 가능성을 주는가

## Preservation Rules

- inline citation과 code excerpt header는 보존한다.
- component-level `Why`는 사라지면 안 된다.
- existing rationale는 appendix 이동 시에도 보존 위치를 남긴다.
- strategic code map은 selective appendix로 유지한다.

## Rewrite Boundary

`spec-rewrite` should:

- preserve existing valuable content
- improve clarity, structure, findability, and canonical fit
- compress or relocate low-value inventory
- warn when canonical core is missing

`spec-rewrite` should not:

- invent missing CIV or missing temporary delta out of thin air
- silently upgrade a weak spec into a richer one
- treat inventory-heavy detail as mandatory main-body structure
