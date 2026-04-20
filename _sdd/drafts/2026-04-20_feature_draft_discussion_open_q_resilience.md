# Feature Draft: discussion 스킬 미결 질문 잔존 방지 (open-q resilience)

**Source Discussion**: [`_sdd/discussion/2026-04-20_discussion_skill_open_q_root_cause.md`](../discussion/2026-04-20_discussion_skill_open_q_root_cause.md)

<!-- spec-update-todo-input-start -->
# Part 1: Temporary Spec Draft

## Change Summary

토론 종료 후에도 in-scope 미결 질문이 남는 현상을 줄이기 위해 `discussion` 스킬의 세 지점을 보강한다.

1. **상류 차단 (Soft 모드)**: 사용자가 묵시적 deferral("나중에 보죠")로 답할 때, AI가 내부적으로 `(a) 지금 답 가능 / (b) 토론 외부 사유 deferred / (c) 다른 미결 의존`으로 분류하고, (a)면 한 가지로 좁힌 1회 재질문, (b/c)면 조용히 기록만 한다. 메타-분류 질문을 사용자 표면에 노출하지 않는다 (fatigue 방지).
2. **수렴 가드**: `수렴 신호 감지 (3.5)`와 `Stagnation Fallback (3.5.1)`가 in-scope `open_questions > 0`일 때 종료 권유를 자동 보류한다.
3. **Gate 3→4 강화**: "그대로 정리(미결로 기록)" 선택 시 각 미결 질문에 카테고리 라벨(`out-of-scope` / `needs-data` / `deferred-deliberately` / `blocked-by:<id>`)을 강제 기록한다. 카테고리 없는 미결은 통과하지 않는다.

근거: `_sdd/discussion/` 산출물 7건 분석에서 잔존 미결 2건 모두 (a) 묵시적 deferral 또는 (b) 미탐지 의존성 체인이 원인. 추가로 사용자가 "토론 길어지면 빠르게 수렴하려는 fatigue" 패턴을 인정 — 이는 스킬의 수렴 메커니즘이 fatigue를 보상하기 때문.

## Scope Delta

### In Scope
- `.claude/skills/discussion/SKILL.md` Process 섹션 3.2.2 / 3.5 / 3.5.1 / Gate 3→4 수정
- `.codex/skills/discussion/SKILL.md` 동일 수정 (플랫폼 동등성 유지)
- 토론 요약 출력 형식의 `미결 질문` 섹션에 카테고리 라벨 추가
- 변경 후 1-2주 산출물 추적 액션 (운영 액션, 코드 변경 아님)

### Out of Scope
- Gate 3→4에 "추가 논의" 강제 (B 대안) — 사용자가 우회할 위험으로 채택하지 않음
- 의존성 체인 자동 그래프 검출 (LLM 추론 기반 Soft 모드로 충분, 별도 데이터 구조 도입 불필요)
- 다른 스킬 (`feature-draft`, `spec-create` 등) 수정
- discussion examples / references 문서 갱신 (별도 follow-up)

### Guardrail Delta
- 사용자에게 메타-분류 질문 (`이거 (a/b/c) 중 뭐죠?`)을 직접 노출하지 않는다. 분류는 AI 내부 추론으로만 수행한다.
- 수렴 가드는 in-scope 항목만 카운트한다. `out-of-scope` / `deferred-deliberately`로 분류된 미결은 카운트에서 제외해 무한 루프를 방지한다.

## Contract/Invariant Delta

| ID | Type | Change | Why |
|----|------|--------|-----|
| C1 | Add | Process 3.2.2에 "묵시적 deferral 감지 시 AI 내부 (a/b/c) 분류 → (a)면 좁힌 재질문 1회, 그 외 조용히 기록" 규칙 명시 | 미결이 쌓이는 상류 메커니즘 차단, fatigue 회피 |
| C2 | Modify | Process 3.5 수렴 신호와 3.5.1 stagnation fallback에 "in-scope `open_questions` > 0이면 종료 권유 보류" 가드 추가 | 수렴 압력이 fatigue를 타고 조기 종료를 보상하는 패턴 차단 |
| C3 | Modify | Gate 3→4의 "그대로 정리(미결로 기록)" 옵션에 카테고리 라벨 강제 (`out-of-scope` / `needs-data` / `deferred-deliberately` / `blocked-by:<id>`) | followup 추적성 확보, 의존성 체인 가시화 |
| C4 | Modify | Step 4 출력 형식 "미결 질문" 섹션에 카테고리 라벨 컬럼 추가 | 산출물 단계에서 카테고리 영속 보장 |
| I1 | Add | in-scope 미결 질문이 남은 상태로는 Gate 3→4 외 어떤 경로로도 토론이 종료되지 않는다 | 우회 종료 차단 (수렴 신호 / stagnation 둘 다 가드 적용) |
| I2 | Add | 토론 요약의 모든 미결 질문 항목은 카테고리 라벨을 포함한다 | C3/C4 invariant 보강 |

## Touchpoints

| 영역 | 위치 | 변경 의도 |
|------|------|-----------|
| 분류 로직 추가 | `.claude/skills/discussion/SKILL.md` 3.2.2 끝부분 | Soft 모드 deferral 분류 규칙 삽입 |
| 수렴 가드 | `.claude/skills/discussion/SKILL.md` 3.5 본문 + 3.5.1 본문 | "in-scope open_q > 0이면 보류" 가드 명시 |
| 게이트 라벨 | `.claude/skills/discussion/SKILL.md` Gate 3→4 부근 | 카테고리 라벨 강제 |
| 출력 형식 | `.claude/skills/discussion/SKILL.md` Step 4 요약 템플릿 | "미결 질문" 섹션에 카테고리 컬럼 |
| Codex 미러 | `.codex/skills/discussion/SKILL.md` 동일 4지점 | 플랫폼 동등성 유지 |

## Implementation Plan

1. `.claude/skills/discussion/SKILL.md`에 4지점 변경을 한 번에 적용 (논리적으로 묶여 있으므로 단일 task).
2. `.codex/skills/discussion/SKILL.md`에 동일 변경을 미러링. 두 파일은 독립 관리 원칙이지만 contract 의미는 동일하게 유지.
3. (운영) 변경 후 1-2주 신규 `_sdd/discussion/*.md` 산출물의 미결 질문 발생률 / followup 파일 생성률 추적.

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, I1 | 시뮬레이션 리뷰 — 가짜 deferral 답변 시나리오 | "나중에 보죠" 입력 시 AI가 (a)면 좁힌 재질문, (b/c)면 조용히 기록. 메타-분류 질문 표면 노출 없음 확인 |
| V2 | C2, I1 | 시뮬레이션 리뷰 — in-scope open_q 1건 + 수렴 신호 충족 상태 | 종료 권유가 발화되지 않고 미결 해결을 유도하는지 확인 (3.5와 3.5.1 모두) |
| V3 | C3, C4, I2 | 시뮬레이션 + 산출물 검증 | Gate 3→4 "그대로 정리" 선택 시 카테고리 라벨 입력 강제, 저장된 요약 파일에 카테고리 컬럼 존재 확인 |
| V4 | C1-C4 (운영 검증) | 1-2주 후 `_sdd/discussion/` 신규 산출물 비교 | 미결 질문 발생률 감소, followup 파일 생성률 감소를 baseline(2/7) 대비 비교 |

## Risks / Open Questions

- **R1**: Soft 모드의 (a) 분류 정확도가 LLM 추론에 전적으로 의존한다. 분류가 보수적으로 (b/c)에 치우치면 미결이 다시 쌓일 수 있다. → 운영 추적(V4)으로 감지하고 필요 시 분류 가이드 강화.
- **R2**: 수렴 가드(C2)가 너무 보수적으로 작동하면 정당한 수렴도 보류돼 토론이 끝없이 늘어질 수 있다. `out-of-scope`/`deferred-deliberately` 분류로 카운트 제외 가능하지만, 사용자가 카테고리 입력에 부담을 느낄 가능성. → V3와 V4에서 함께 모니터링.
- **R3**: `.claude`와 `.codex` 미러가 독립 관리 원칙이라 wording이 미세하게 분기될 수 있음. → contract 의미만 동일하게 유지하면 OK (memory `feedback_platform_parity`).
- **OQ1**: `blocked-by:<id>` 라벨이 가리키는 ID 체계 — 동일 토론 내 다른 미결 질문 번호 vs. 외부 토론 파일 슬러그 — 어느 쪽으로 통일할지 구현 시 결정 필요.

<!-- spec-update-todo-input-end -->

# Part 2: Implementation Plan

## Overview

discussion 스킬의 SKILL.md 본문을 4개 지점에서 패치한다. 변경은 코드가 아닌 마크다운 본문 수정이며, Claude/Codex 두 미러를 동일 contract로 유지한다.

## Scope

- 수정 대상: `.claude/skills/discussion/SKILL.md`, `.codex/skills/discussion/SKILL.md`
- 신규 파일: 없음
- 삭제 파일: 없음
- 코드 변경: 없음 (markdown only)

## Components

- `discussion` skill (Claude 진입점): `.claude/skills/discussion/SKILL.md`
- `discussion` skill (Codex 미러): `.codex/skills/discussion/SKILL.md`

## Contract/Invariant Delta Coverage

| Delta ID | Covered By Tasks |
|----------|------------------|
| C1 | T1, T2 |
| C2 | T1, T2 |
| C3 | T1, T2 |
| C4 | T1, T2 |
| I1 | T1, T2 (V1, V2 검증) |
| I2 | T1, T2 (V3 검증) |

## Implementation Phases

### Phase 1: Skill 본문 패치 (Claude + Codex 동시)

- T1과 T2는 서로 다른 파일이라 파일 충돌은 없으나, 동일 contract를 동일하게 표현해야 하는 의미적 결합이 있다. 같은 phase 내에서 동시에 진행하되 wording 일치를 검토한다.

### Phase 2: 자체 시뮬레이션 검증

- T3: V1/V2/V3 시나리오를 머릿속/리뷰로 walk-through하고 본문 wording이 의도대로 작동할지 확인.

### Phase 3 (운영, 별도 트래킹)

- T4: 1-2주 후 `_sdd/discussion/` 신규 산출물 분석 (V4). 코드 변경 없으므로 implementation 외 task로 분리.

## Task Details

### Task T1: `.claude/skills/discussion/SKILL.md` 4지점 패치

**Component**: `.claude/skills/discussion/`
**Priority**: P1
**Type**: Refactor (skill behavior)

**Description**:
다음 4지점을 본문에 명시한다.

1. **3.2.2 비판적 개입 끝부분**에 "Soft Deferral Handling" 서브섹션 추가:
   - AI는 사용자 답변에서 묵시적 deferral 신호("나중에", "그건 보고", "지금은 모르겠어요" 등)를 감지하면 내부적으로 다음 분류를 수행한다.
     - (a) 지금 토론 내에서 한 가지 구체 질문으로 좁히면 답할 수 있다 → 좁힌 1회 재질문
     - (b) 토론 외부 사유로 진짜 deferred (다른 작업/외부 데이터/명확한 분리 필요) → `open_questions`에 카테고리 `deferred-deliberately` 또는 `needs-data`로 조용히 기록
     - (c) 다른 미결 질문에 의존 → `blocked-by:<id>`로 기록하고 의존하는 Q를 다음 라운드 우선 주제로 채택
   - 메타-분류 질문(예: "이거 (a)/(b)/(c) 중 뭐죠?")을 **사용자 표면에 노출하지 않는다** (fatigue 방지).

2. **3.5 수렴 신호 감지 및 종료 유도**에 가드 한 줄 추가:
   - "단, in-scope `open_questions` (즉 카테고리가 `out-of-scope` / `deferred-deliberately`가 아닌 항목) 가 1건 이상이면 수렴 신호가 충족돼도 종료 권유를 발화하지 않고 해당 미결을 다음 라운드 주제로 채택한다."

3. **3.5.1 Stagnation Fallback** 동일 가드 적용:
   - "in-scope `open_questions` > 0이면 stagnation 감지 시에도 강제 종료 옵션을 제시하지 않고, '남은 미결 1개만 더 논의'를 기본 옵션으로 둔다."

4. **Gate 3→4의 "그대로 정리(미결로 기록)" 옵션** 강화:
   - 선택 시, 각 미결 질문에 대해 사용자에게 카테고리 라벨(`out-of-scope` / `needs-data` / `deferred-deliberately` / `blocked-by:<id>`)을 다중 선택으로 한 번만 묻고, 미입력 항목이 있으면 통과 불가.
   - **Step 4 요약 출력 형식**의 `## 미결 질문 (Open Questions)` 템플릿을 다음으로 변경:
     ```markdown
     ## 미결 질문 (Open Questions)
     | # | 질문 | 카테고리 | 맥락 / 의존 |
     |---|------|----------|-------------|
     | 1 | ... | needs-data | ... |
     ```

또한 Hard Rules에 다음 한 줄 추가:
- "in-scope 미결 질문이 남은 상태로는 Gate 3→4 외 경로로 토론을 종료하지 않는다."

**Acceptance Criteria**:
- [ ] 3.2.2 끝부분에 Soft Deferral Handling 서브섹션이 추가됐다.
- [ ] 3.5와 3.5.1 본문에 in-scope open_q 가드 문장이 추가됐다.
- [ ] Gate 3→4 설명이 카테고리 라벨 강제를 반영했다.
- [ ] Step 4 요약 템플릿의 "미결 질문" 섹션에 카테고리 컬럼이 추가됐다.
- [ ] Hard Rules에 종료 경로 제한 규칙이 추가됐다.

**Target Files**:
- [M] `.claude/skills/discussion/SKILL.md` -- 4지점 본문 수정 + Hard Rules 1줄 추가

**Technical Notes**: Covers C1, C2, C3, C4, I1, I2; validated by V1, V2, V3.
**Dependencies**: 없음

### Task T2: `.codex/skills/discussion/SKILL.md` 동일 패치 미러링

**Component**: `.codex/skills/discussion/`
**Priority**: P1
**Type**: Refactor (skill behavior)

**Description**:
T1과 동일한 4지점 + Hard Rules 변경을 Codex 미러에 적용한다. wording은 동일 contract를 표현하면 되며, 미러 간 자구 일치를 강제하지 않는다 (memory `feedback_platform_parity`). 단, 카테고리 라벨 어휘(`out-of-scope` / `needs-data` / `deferred-deliberately` / `blocked-by:<id>`)와 출력 템플릿 컬럼명은 두 미러가 동일하게 유지해 산출물 형식 호환성을 보장한다.

**Acceptance Criteria**:
- [ ] T1과 동일한 4지점 변경이 .codex 미러에 반영됐다.
- [ ] 카테고리 라벨 어휘와 출력 템플릿 컬럼명이 두 파일에서 일치한다.
- [ ] Hard Rules에 종료 경로 제한 규칙이 추가됐다.

**Target Files**:
- [M] `.codex/skills/discussion/SKILL.md` -- T1과 동일 4지점 + Hard Rules

**Technical Notes**: Covers C1, C2, C3, C4, I1, I2; validated by V1, V2, V3.
**Dependencies**: T1과 같은 phase. 파일 충돌 없으나 의미 결합 — 같이 검토.

### Task T3: 시뮬레이션 자체 검증

**Component**: review
**Priority**: P1
**Type**: Test (manual walk-through)

**Description**:
T1/T2 적용 후 다음 시나리오를 머릿속으로 시뮬레이션해 본문이 의도대로 동작하는지 확인한다.

- 시나리오 V1: 사용자가 "나중에 보죠"로 답 → AI가 좁힌 재질문 또는 조용한 기록. 메타-분류 질문 노출 없음.
- 시나리오 V2: in-scope open_q 1건 있는 상태에서 수렴 신호 충족 → 종료 권유 발화 없음, 해당 미결을 다음 라운드 주제로 채택.
- 시나리오 V3: Gate 3→4 "그대로 정리" 선택 → 카테고리 라벨 입력 강제, 출력 파일에 카테고리 컬럼 존재.

본문 wording이 모호해 시나리오가 분기되면 T1/T2로 돌아가 보강한다.

**Acceptance Criteria**:
- [ ] 세 시나리오 모두 본문 wording만으로 의도된 동작을 일관되게 추론할 수 있다.
- [ ] 모호한 지점은 T1/T2 본문에서 보강 완료.

**Target Files**:
- [TBD] 시뮬레이션 walk-through 결과는 별도 파일로 저장하지 않음 — 검토 단계의 in-conversation 활동.

**Technical Notes**: V1, V2, V3 sign-off.
**Dependencies**: T1, T2 완료 후.

### Task T4 (운영, 별도 트래킹): 1-2주 후 산출물 추적

**Component**: ops review
**Priority**: P2
**Type**: Test (operational)

**Description**:
2026-04-20 이후 1-2주간 `_sdd/discussion/` 신규 산출물에서 다음 지표를 baseline(7건 중 2건 미결, 1건 followup 생성)과 비교.

- 미결 질문 발생률
- followup 파일 (`*_open_questions*` / `*_followup*`) 생성률
- 미결 카테고리 분포 (in-scope vs out-of-scope vs deferred-deliberately)

지표가 개선되지 않으면 R1/R2 가설로 돌아가 분류 가이드를 보강하거나 가드 강도를 조정한다.

**Acceptance Criteria**:
- [ ] 신규 산출물 5건 이상 누적 시 baseline 대비 비교 리포트 작성.
- [ ] 결과를 `_sdd/discussion/` 또는 `_sdd/spec/logs/`에 기록.

**Target Files**:
- [TBD] 운영 추적 결과 저장 위치 -- baseline 누적 후 결정 (예: `_sdd/spec/logs/discussion_open_q_resilience_followup_<date>.md`)

**Technical Notes**: V4. 코드 변경 없음.
**Dependencies**: T1, T2, T3 완료 + 시간 경과.

## Parallel Execution Summary

| Phase | Tasks | Parallelism | 이유 |
|-------|-------|-------------|------|
| 1 | T1, T2 | 병렬 가능 | 다른 파일이라 파일 충돌 없음. 의미 결합은 같은 phase 내에서 검토로 흡수. |
| 2 | T3 | 단독 | T1/T2 양쪽 결과를 함께 검토. |
| 3 | T4 | 시간 분리 | 산출물 누적 후. |

## Risks and Mitigations

| Risk ID | 내용 | Mitigation |
|---------|------|------------|
| R1 | Soft 모드 (a/b/c) 분류 정확도가 LLM에 의존 | V4 운영 추적, 필요 시 분류 가이드/예시 보강 |
| R2 | 수렴 가드가 보수적으로 작동해 토론 무한 루프 | `out-of-scope`/`deferred-deliberately` 카운트 제외, V3/V4 모니터링 |
| R3 | Claude/Codex 미러 wording 분기 | contract 어휘(카테고리 라벨, 컬럼명)만 강제 일치, 자구는 자유 |
| R4 | 카테고리 라벨 입력이 새로운 fatigue 유발 | 다중 선택 1회만 묻고, 미입력 시 가장 일반적 라벨 자동 제안 (구현 시 wording 결정) |

## Open Questions

- OQ1: `blocked-by:<id>`의 ID 체계 — 동일 토론 내 미결 번호 vs 외부 토론 파일 슬러그. T1 구현 wording 시 결정.
- OQ2: 카테고리 라벨 미입력 시 fallback 동작 — "강제 차단" vs "기본값 자동 적용 후 경고". 사용성 vs 엄격성 트레이드오프, T1 구현 시 결정.
