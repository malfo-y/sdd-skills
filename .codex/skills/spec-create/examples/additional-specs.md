# Additional Spec Examples

Supplementary examples for the current SDD canonical model.

---

## Example 1: Supporting Reference File Split

대규모 프로젝트에서는 글로벌 스펙 본문을 얇게 유지하고, 참조 정보만 supporting file로 분리할 수 있다.

```markdown
_sdd/spec/
├── main.md                  # global spec core
├── api-reference.md         # reference information
├── data-models.md           # reference information
└── environment.md           # environment & dependencies
```

이때 `main.md`에는 아래 core만 유지한다.

1. 배경 및 high-level concept
2. Scope / Non-goals / Guardrails
3. 핵심 설계와 주요 결정
4. Contract / Invariants / Verifiability
5. 사용 가이드 & 기대 결과
6. Decision-bearing structure

---

## Example 2: Temporary Spec Skeleton

temporary spec은 글로벌 스펙과 다른 목적을 가진 실행 청사진이다.

```markdown
# Inventory Reservation Retry Temporary Spec

## 1. Change Summary
[이번 변경의 요약]

## 2. Scope Delta
- retry window를 30초에서 2분으로 늘린다
- reservation timeout metric을 추가한다

## 3. Contract/Invariant Delta

| ID | Type | Change |
|----|------|--------|
| C1 | Modify | reservation timeout은 2분까지 유지된다 |
| I1 | Preserve | oversell 방지 invariant는 유지된다 |

## 4. Touchpoints
- `services/inventory/src/application/reserve.py`
- `services/inventory/src/config.py`
- `services/inventory/tests/test_reserve.py`

## 5. Implementation Plan
- timeout config를 분리한다
- reservation state transition을 수정한다

## 6. Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, I1 | test, review | retry timeout과 oversell regression 확인 |

## 7. Risks / Open Questions
- long retry window가 UX에 미치는 영향 재확인 필요
```

핵심은 `Contract/Invariant Delta`와 `Validation Plan` 사이의 ID 연결을 유지하는 것이다.

---

## Example 3: Strategic Code Map Should Stay Selective

좋은 strategic code map:

```markdown
## Appendix A. Strategic Code Map

| Kind | Path / Symbol | Why It Matters |
|------|----------------|----------------|
| Entrypoint | `src/main.py:create_app` | 전체 API wiring 진입점 |
| Invariant Hotspot | `src/order/confirm.py:confirm_order` | confirmed order invariant 핵심 |
| Extension Point | `src/search/query_builder.py:build_query` | 필터 확장 지점 |
```

나쁜 strategic code map:

```markdown
- `src/a.py`
- `src/b.py`
- `src/c.py`
- `src/d.py`
```

전수형 파일 목록은 code map이 아니라 inventory다.
