# Spec Rewrite Plan — Scoped Guardrails Legibility Polish

**Date**: 2026-06-12
**Scope**: `_sdd/spec/main.md` §2 Scope / Non-goals / Guardrails — Guardrails bullet legibility만
**Type**: scoped polish (NOT full rewrite). 직전 review→update-done→upgrade로 spec은 이미 thin·canonical 정합.
**Canonical-fit rationale**: 구조/분할/경계 모두 PASS 상태. 유일 결함은 일부 Guardrail bullet이 한 문장에 다중 결정을 담은 run-on이라 legibility만 저하. 구조 재편·파일 분할·내용 이동 없음.

## 4-Core Axis Pre-judgment (무엇을 줄이고 무엇을 보존)
- `Thinness`: 유지 — bullet 수·총량 동일. 분할은 줄바꿈만 추가, 본문 비대화 아님 (Hard Rule 5 준수).
- `Decision-bearing truth`: 100% 보존 — 모든 절(clause)·`code`·링크·rationale를 sub-bullet로 옮기되 surface(§2 body) 그대로 유지. body→log 이동 없음.
- `Anti-duplication`: 변화 없음 — 새 중복 생성 안 함.
- `Navigation + surface fit`: 변화 없음 — 같은 §2 surface 내 가독성만 개선.

## Body / Log Placement Rule
- 이 작업은 **legibility 재배치**이지 rationale pruning이 아니다. 따라서 decision-bearing 내용은 전부 §2 body에 잔류. `decision_log`/`rewrite_report`로 내리는 rationale 없음 (Hard Rule 1 비해당).
- 메타 메모(이 polish의 deviation/scorecard)만 `rewrite_report.md`에 기록.

## Split Map (대상 bullet, 모두 lead 문장 + nested sub-bullet 구조로)
대상 = 3절 이상 또는 rule+exception 구조의 run-on bullet. 절은 1:1 보존, 추가/삭제 없음.

1. **L59** skill/agent layer + nesting + orchestrator/wrapper 형태 + producer orchestrator → lead(layer+nesting) + sub(orchestrator형 / wrapper형 / producer orchestrator) 3 sub-bullet
2. **L62** wrapper-backed skill 계약 → lead(entrypoint/artifact 유지+흉내 금지) + sub(thin entrypoint·agent 단일소스 / 대화입력 forwarding) 2 sub-bullet
3. **L63** review/validation workflow loop → lead(review-only 금지) + sub(producer 자체 소유 / 공통 loop 정책 차용 / fix=재dispatch·단일작성자) 3 sub-bullet
4. **L64** autopilot plan-review gate → lead(gate 통과 필수) + sub(미통과 시 reject/regenerate) 1 sub-bullet
5. **L65** canonical agent invocation → lead(canonical 이름만) + sub(kebab-case canonical / legacy alias reject) 2 sub-bullet
6. **L68** multi-phase execution gate → lead(execution gate) + sub(Checkpoint group boundary / adaptive final review / missing Checkpoint=schema violation) 3 sub-bullet

비대상(이미 단문·가독): L58, L60, L61, L66, L67, L69, L70, L71, L72, L73 — 손대지 않음.

## Ambiguity / Risk / Unresolved
- Risk: nested bullet은 본 문서가 주로 flat bullet/table 스타일이나, §2 run-on에 한해 가독성 이득이 명확. 표준 마크다운이라 렌더 안전.
- Risk: 절 분할 시 의미 누락 위험 → 검증 단계에서 원본 대비 절 단위 대조.
- Unresolved: 없음.

## Target Files
- `_sdd/spec/main.md` (§2 Guardrails만)

## 실행 순서 / Deviation 규칙
1. 이 plan 저장 (현재 단계)
2. main.md §2 6개 bullet in-place 분할 edit
3. 절 보존 검증 (원본 절 ↔ 결과 sub-bullet 1:1)
4. `rewrite_report.md` 작성 (scorecard + deviation)
- Deviation 발생 시 report에 기록. 계획 외 bullet/섹션은 건드리지 않음.
