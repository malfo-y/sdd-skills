# Spec Rewrite Report — Scoped Guardrails Legibility Polish

**Date**: 2026-06-12
**Target**: `_sdd/spec/main.md` §2 Scope / Non-goals / Guardrails (Guardrails bullet legibility only)
**Type**: scoped polish (NOT full rewrite)
**Plan**: `_sdd/spec/logs/spec-rewrite-plan.md`

## Diagnosis Summary (Step 1)
직전 review→update-done→upgrade로 spec은 이미 thin·canonical 정합. 4 공통축 + rewrite 고유 4축 모두 PASS. 유일 결함은 §2 Guardrails 일부 bullet이 한 문장에 다중 결정을 담은 run-on이라 legibility만 저하. → full rewrite 회피, scoped polish만 수행 (Error Handling "잘 구조화된 spec" 경로).

## Metric Scorecard

| 축 | Before | After | 비고 |
|----|--------|-------|------|
| Thinness | PASS | PASS | bullet 수·내용 동일, 줄바꿈만 추가. 비대화 없음 |
| Decision-bearing truth | PASS | PASS | 모든 절 §2 body 잔류. log 이동 0 |
| Anti-duplication | PASS | PASS | 신규 중복 0 |
| Navigation + surface fit | PASS | PASS | 동일 surface 내 가독성만 ↑ |
| Component Separation | PASS | PASS | 미변경 |
| Findability | PASS | PASS | 미변경 |
| Boundary Clarity | PASS | PASS | 미변경 |
| Canonical Fit | PASS | PASS+ | run-on 6개 → lead+sub 구조로 결정 경계 명료화 |

## Canonical-fit 평가
global spec은 여전히 `개념 + 경계 + 결정` thin 문서. polish는 결정의 가독성만 높였고 feature-level usage/contract/inventory 유입 없음. Hard Rule 5(재비대화 금지) 준수 — 총 정보량 동일, 표현 구조만 개선.

## Pruning / Move / Split 결과
- Pruning: 없음 (내용 삭제 0)
- Move(body→log): 없음 (rationale 전량 body 잔류, Hard Rule 1 비해당)
- Split: 6개 run-on bullet을 lead 문장 + nested sub-bullet으로 분할
  - L59 → lead + 3 sub (orchestrator형 / wrapper형 / producer orchestrator)
  - L62(현 L65) → lead + 2 sub (thin entrypoint / 대화입력 forwarding)
  - L63(현 L68) → lead + 3 sub (producer 자체소유 / 공통 loop 정책 / fix=재dispatch)
  - L64(현 L72) → lead + 1 sub (미통과 reject/regenerate)
  - L65(현 L74) → lead + 2 sub (kebab-case canonical / legacy alias reject)
  - L68(현 L79) → lead + 3 sub (Checkpoint boundary / adaptive final review / missing=schema violation)

## Rationale Preservation
원본 절 ↔ 결과 sub-bullet 1:1 대조 검증 통과. `code` span(`feature-draft`, `Checkpoint`, `critical=high=medium=0`, agent 이름 등)·inline 링크·`orchestrator-contract.md §6` citation 전부 유지. component-level `Why`/`Source`는 §2 대상 아님(미변경).

## Body vs Log Placement
이 작업은 legibility 재배치이지 pruning이 아니므로 decision-bearing 내용 전량 §2 body 잔류가 의도된 결과. log/report로 내린 rationale 없음. 메타 메모(scorecard/deviation)만 본 report에 기록.

## 링크/경로 유효성
§2 내 링크 미변경(`docs/SDD_SPEC_DEFINITION.md`, `docs/SDD_WORKFLOW.md`, `../env.md`) — edit 대상 bullet 밖이라 깨짐 없음.

## Plan 대비 Deviation
- 계획된 6개 bullet만 수정, 그 외 §2/§3/타 파일 무수정 — 계획 일치.
- Minor: L68→현 L81 분할 시 "처리한다 (1개" 앞 공백 1칸 제거("처리한다(1개")로 정규화. 의미 무관 표기 정리.
- 그 외 deviation 없음.

## Unresolved Warning
- 없음. missing canonical core 없음(자동 생성 비해당). ambiguity 없음.
