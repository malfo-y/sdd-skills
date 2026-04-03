# Feature Draft: Implementation Inline Orchestration

**Date**: 2026-04-01
**Author**: hyunjoonlee
**Target Spec**: `_sdd/spec/main.md`
**Status**: Draft

---

<!-- spec-update-todo-input-start -->
# Part 1: Spec Patch Draft

> This patch can be copy-pasted into the corresponding spec section,
> or used as input for the `spec-update-todo` skill.

# Spec Update Input

**Date**: 2026-04-01
**Author**: hyunjoonlee
**Target Spec**: `_sdd/spec/main.md`

## Background & Motivation Updates

### Background Update: Inline Orchestration 도입 배경

**Target Section**: `_sdd/spec/main.md` > `Core Design > Key Idea`

**Proposed**:

v3.8.0에서 implementation agent를 iteration orchestrator로 전환하면서 ac-plan, tdd-execute를 내부 sub-agent로 분리하였다. 이 구조는 **context dilution 방지**(sub-agent가 독립 컨텍스트에서 실행)에 효과적이지만, **실행 가시성(visibility) 저하** 문제를 수반한다. sub-agent 단위가 크고 실행 시간이 길어 사용자에게 진행 상황이 보이지 않는 시간이 길다.

v3.11에서 이 trade-off를 해소하기 위해 **Inline Orchestration 패턴**을 도입한다. implementation 오케스트레이터가 sub-agent를 spawn하는 대신 sub-step 지시 파일을 Read하여 inline으로 실행하고, **Re-anchor 패턴**과 **State Externalization 패턴**으로 context dilution을 억제한다. 이를 통해:
- 사용자에게 전체 실행 과정이 실시간으로 보임 (가시성 확보)
- 핵심 지시가 매 단계 갱신되어 dilution에 의한 지시 망각 방지 (품질 유지)
- 중간 결과가 파일로 기록되어 대화 컨텍스트를 오염시키지 않음 (noise 감소)

## Design Changes

### Design Change: Inline Orchestration Pattern 추가

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Core Design > Design Patterns`

**Description**:

**Inline Orchestration 패턴**: implementation 오케스트레이터에서 사용한다. sub-agent spawn 대신 sub-step 지시 파일을 `Read` 도구로 로드하여 현재 컨텍스트에서 inline으로 실행한다. Agent Wrapper 패턴의 가시성 한계를 해결하면서, Re-anchor 패턴과 State Externalization 패턴으로 context dilution을 억제한다.

```
# 기존: Agent 기반 (visibility 낮음, dilution 없음)
implementation orchestrator
  → Agent(subagent_type="ac-plan")        # 격리 실행, 출력 안 보임
  → Agent(subagent_type="tdd-execute")    # 격리 실행, 출력 안 보임
  → Agent(subagent_type="implementation-review")  # 격리 실행, 출력 안 보임

# 신규: Inline Orchestration (visibility 높음, dilution 억제)
implementation orchestrator
  → Read(ac-plan 지시) → inline 실행 → state 기록 → re-anchor
  → Read(tdd-execute 지시) → inline 실행 → state 기록 → re-anchor
  → Read(implementation-review 지시) → inline 실행 → state 기록 → re-anchor
```

주요 제약:
- inline 실행 시 sub-step의 tool 제한이 사라짐 (ac-plan의 Read-only 제한 등). 대신 지시 파일에 "이 단계에서는 분석만 수행하고 코드를 수정하지 않는다" 등의 행동 제약을 명시한다.
- tdd-execute 내부의 task sub-agent spawn은 유지한다 (task 단위는 작아서 가시성 문제 없음).

### Design Change: Re-anchor Pattern 추가

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Core Design > Design Patterns`

**Description**:

**Re-anchor 패턴**: Inline Orchestration 패턴과 함께 사용한다. 각 sub-step 지시 파일에 10줄 이내의 `## Re-anchor` 섹션을 포함하며, 매 단계 전환 시 이 섹션을 Re-read하여 핵심 지시를 "최신 컨텍스트"로 끌어올린다. context dilution에서 instruction signal이 noise에 묻히는 문제를 해결한다.

```markdown
## Re-anchor
<!-- 매 iteration 시작 시 Read하여 핵심 지시를 갱신한다 -->
- AC 목록과 상태는 반드시 iteration_state.md에서 읽는다
- 코드 변경 후 반드시 테스트를 재실행한다
- Spec 파일은 읽기 전용이다
- 파일당 하나의 concern만 수정한다
- 이전 단계 결과는 iteration_state.md에 기록되어 있다
```

이 패턴의 핵심 원리: **signal-to-noise ratio** 유지. 컨텍스트의 총량이 아니라 "지금 따라야 할 지시"가 "이전 단계의 잔해(tool output, 중간 결과)"에 묻히지 않도록 하는 것이 목적이다. Re-anchor를 통해 instruction signal을 최신 위치에 재주입한다.

### Design Change: State Externalization Pattern 추가

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Core Design > Design Patterns`

**Description**:

**State Externalization 패턴**: Inline Orchestration 패턴과 함께 사용한다. iteration loop의 중간 결과(AC 상태, 단계별 결과 요약, 이슈 목록)를 대화 컨텍스트에 누적하지 않고 외부 파일에 기록한다. 다음 단계 시작 시 필요한 부분만 파일에서 읽어 컨텍스트를 lean하게 유지한다.

```
_sdd/implementation/iteration_state.md
├── ## AC Status           # 전역 AC 상태 맵 (PENDING/MET/NOT_MET/UNTESTED)
├── ## Current Phase       # 현재 Phase 번호 + iteration 번호
├── ## Latest Step Result  # 가장 최근 단계 결과 요약 (1-3줄)
├── ## Iteration History   # 누적 iteration 이력 테이블
└── ## Active Issues       # 현재 미해결 critical/high 이슈 목록
```

대화에는 "Step 2 완료, 결과는 iteration_state.md에 기록" 수준의 요약만 남긴다. 이를 통해:
- Tool output의 긴 결과가 컨텍스트를 오염시키지 않음
- 다음 단계에서 필요한 정보를 파일에서 정확히 읽을 수 있음
- iteration 간 상태 전달이 명시적이고 추적 가능

### Design Change: Mirror 패턴 → Inline Orchestration 전환

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Core Design > Design Patterns`

**Description**:

implementation 스킬에 한해 **Mirror 패턴을 폐기**하고 **Inline Orchestration 패턴으로 전환**한다.

- 기존: `.claude/skills/implementation/SKILL.md`가 `.claude/agents/implementation.md`의 Mirror(전체 복사) → agent가 sub-agent를 spawn
- 변경: `.claude/skills/implementation/SKILL.md`가 Inline Orchestration 오케스트레이터로 전환 → sub-step 지시 파일을 Read하여 inline 실행

`.claude/agents/implementation.md` agent 파일은 sdd-autopilot 등 agent spawn이 필요한 호출 경로를 위해 유지하되, SKILL.md와는 독립적으로 관리한다. (Mirror 동기화 의무 해제)

### Design Change: Agent Depth 3 → Depth 2로 축소

**Priority**: Medium
**Target Section**: `_sdd/spec/main.md` > `Core Design > Design Rationale`

**Description**:

기존: implementation(depth 1) → tdd-execute(depth 2) → task sub-agents(depth 3). Inline Orchestration 전환으로:
- ac-plan: agent spawn → inline 실행 (depth 감소)
- tdd-execute: agent spawn → inline 실행 (depth 감소), 내부 task sub-agent만 Agent()로 spawn
- implementation-review: agent spawn → inline 실행 (depth 감소)

결과: 최대 depth가 3 → 2로 축소 (implementation → task sub-agents). 단, implementation 자체가 agent로 호출되는 경우(sdd-autopilot) depth 2 → task sub-agents는 depth 3이 될 수 있어, agent 경로에서는 기존과 동일.

| 호출 경로 | 최대 depth |
|-----------|-----------|
| 사용자 `/implementation` (inline) | 2 (main → task sub-agents) |
| sdd-autopilot → Agent(implementation) | 3 (autopilot → implementation → task sub-agents) |

## Improvements

### Improvement: implementation 오케스트레이터 Inline 전환

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Component Details > implementation`

**Current State**: implementation SKILL.md는 agent.md의 Mirror. Step 4에서 `Agent(subagent_type="ac-plan")`, `Agent(subagent_type="tdd-execute")`, `Agent(subagent_type="implementation-review")`를 spawn.

**Proposed**: implementation SKILL.md를 Inline Orchestration 오케스트레이터로 전환. Step 4에서 sub-step 지시 파일을 Read하여 inline 실행. Re-anchor 패턴 + State Externalization 패턴 적용.

**Reason**: Agent 기반 실행의 가시성 저하 해결. 사용자가 전체 실행 과정을 실시간으로 확인 가능.

### Improvement: ac-plan에 Re-anchor 섹션 추가

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Component Details > ac-plan`

**Current State**: ac-plan.md에 Re-anchor 섹션 없음. Agent로만 호출됨.

**Proposed**: `## Re-anchor` 섹션을 추가하여 inline 실행 시 매 iteration 경계에서 핵심 지시를 재주입할 수 있도록 한다. 또한 "이 단계에서는 분석만 수행하고 코드를 수정하지 않는다" 행동 제약을 Hard Rules에 명시.

**Reason**: Inline Orchestration 전환 시 tool 제한이 사라지므로 행동 제약으로 보완 필요.

### Improvement: tdd-execute에 Re-anchor 섹션 추가

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Component Details > tdd-execute`

**Current State**: tdd-execute.md에 Re-anchor 섹션 없음. Agent로만 호출됨.

**Proposed**: `## Re-anchor` 섹션 추가. 내부 task sub-agent spawn은 유지 (task 단위는 작아서 가시성 문제 없음). State Externalization으로 구현 결과를 iteration_state.md에 기록하는 절차 추가.

**Reason**: Inline Orchestration 전환 지원.

### Improvement: implementation-review에 Re-anchor 섹션 추가

**Priority**: Medium
**Target Section**: `_sdd/spec/main.md` > `Component Details > implementation-review`

**Current State**: implementation-review SKILL.md/agent.md에 Re-anchor 섹션 없음.

**Proposed**: `## Re-anchor` 섹션 추가. 검증 결과를 iteration_state.md에 기록하는 절차 추가.

**Reason**: Inline Orchestration 전환 지원.

### Improvement: implementation iteration_state.md artifact 추가

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Architecture Overview > _sdd/ Artifact Map`

**Current State**: iteration 상태가 대화 컨텍스트에만 존재.

**Proposed**: `_sdd/implementation/iteration_state.md`를 Artifact Map에 추가. 생성 스킬: implementation. 설명: iteration loop 상태 (AC 상태, Phase 정보, 단계별 결과, 이슈 목록).

**Reason**: State Externalization 패턴의 저장소.

### Improvement: 스펙 Key Features / Success Criteria 갱신

**Priority**: Low
**Target Section**: `_sdd/spec/main.md` > `Background & Motivation > Key Features`, `Success Criteria`

**Current State**: "implementation 내부 sub-agent (2개) ─── ac-plan, tdd-execute"로 기술. Agent 12개로 카운트.

**Proposed**: Inline Orchestration 전환 반영. ac-plan, tdd-execute는 "implementation 내부 inline instruction (2개)"로 변경. Agent 카운트는 10개(12-2)로 조정하되, agent 파일 자체는 sdd-autopilot 경로용으로 유지됨을 명시.

**Reason**: 아키텍처 변경 반영.

## Failure Modes

| 시나리오 | 실패 시 | 사용자 가시성 | 처리 방안 |
|---------|---------|-------------|----------|
| Inline 실행 중 context dilution으로 이전 지시 망각 | AC 누락/잘못된 구현 | 사용자가 비정상 행동 관찰 | Re-anchor 섹션 재설계 (더 강한 지시, 빈도 증가) |
| iteration_state.md 파싱 실패 | 이전 iteration 결과 유실 | 에러 메시지 출력 | 파일 재생성 + 코드베이스에서 상태 재추론 |
| ac-plan inline 실행 시 코드 수정 시도 | 스케줄링 단계에서 의도치 않은 변경 | 의도치 않은 파일 변경 관찰 | Hard Rules 행동 제약 강화, git diff로 사전 상태 스냅샷 |
| tdd-execute inline 실행 시 task sub-agent depth 초과 | task sub-agent 실행 실패 | 에러 로그 | task sub-agent 대신 순차 inline 실행으로 fallback |
| Re-anchor 섹션이 너무 길어 역효과 | Re-anchor 자체가 noise가 됨 | 느린 응답/반복적 출력 | Re-anchor 10줄 상한 엄격 적용 |

## Notes

- 이 변경은 Claude Code 플랫폼에만 적용. Codex는 별도 후속 작업.
- `.claude/agents/implementation.md` agent 파일은 sdd-autopilot 호출 경로를 위해 유지. 단, agent 파일도 동일한 inline 패턴을 적용할 수 있으며, 이는 사용자 판단에 따라 후속 작업으로 진행.
- 기존 `_sdd/implementation/IMPLEMENTATION_REPORT.md`와 `iteration_state.md`는 별개 파일. REPORT는 최종 산출물, state는 실행 중 임시 상태.

<!-- spec-update-todo-input-end -->

---

# Part 2: Implementation Plan

## Overview

implementation 오케스트레이터의 sub-step 실행 방식을 Agent spawn에서 inline Read + 실행으로 전환한다. Re-anchor 패턴과 State Externalization 패턴을 적용하여 context dilution을 억제하면서 가시성을 확보한다.

## Scope

### In Scope
- ac-plan.md, tdd-execute.md, implementation-review.md/SKILL.md에 Re-anchor 섹션 추가
- iteration_state.md 형식 정의 및 State Externalization 로직 설계
- implementation SKILL.md를 Inline Orchestration 오케스트레이터로 재작성
- implementation agent.md에서 Mirror Notice 제거 및 독립 관리 선언

### Out of Scope
- Codex 측 변경 (`.codex/` 하위)
- sdd-autopilot 오케스트레이터 변경 (implementation agent 호출 방식 유지)
- 다른 스킬/에이전트의 Inline Orchestration 전환

## Components

1. **Re-anchor Sections**: ac-plan, tdd-execute, implementation-review 지시 파일에 추가할 compact 핵심 지시 섹션
2. **State Externalization**: iteration_state.md 형식 + 읽기/쓰기 절차
3. **Inline Orchestrator**: implementation SKILL.md의 새로운 오케스트레이션 로직
4. **Agent File Decoupling**: implementation agent.md의 Mirror 해제

## Implementation Phases

### Phase 1: Sub-step 지시 파일 준비

| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| T1 | ac-plan.md Re-anchor 섹션 + 행동 제약 추가 | P1-High | - | Re-anchor |
| T2 | tdd-execute.md Re-anchor 섹션 + state 기록 절차 추가 | P1-High | - | Re-anchor |
| T3 | implementation-review.md Re-anchor 섹션 + state 기록 절차 추가 | P1-High | - | Re-anchor |

### Phase 2: State Externalization 설계

| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| T4 | iteration_state.md 형식 정의 + 읽기/쓰기 규약 설계 | P0-Critical | - | State Externalization |

### Phase 3: Implementation 오케스트레이터 재작성

| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| T5 | implementation SKILL.md Inline Orchestration 재작성 | P0-Critical | T1, T2, T3, T4 | Inline Orchestrator |
| T6 | implementation agent.md Mirror 해제 + 독립 관리 선언 | P2-Medium | T5 | Agent File Decoupling |

### Phase 4: 스펙 동기화

| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| T7 | 스펙 main.md 업데이트 (패턴 3개 추가 + Component Details + Artifact Map + 카운트 조정) | P1-High | T5 | Spec Sync |

## Task Details

### Task T1: ac-plan.md Re-anchor 섹션 + 행동 제약 추가

**Component**: Re-anchor
**Priority**: P1-High
**Type**: Refactor

**Description**: `.claude/agents/ac-plan.md`에 `## Re-anchor` 섹션을 추가한다. 이 섹션은 implementation 오케스트레이터가 inline 실행 전에 Read하여 핵심 지시를 컨텍스트에 재주입하는 데 사용된다. 또한 inline 실행 시 tool 제한이 사라지므로, Hard Rules에 "이 단계에서는 분석/읽기만 수행하고 코드를 생성/수정/삭제하지 않는다"는 행동 제약을 추가한다.

**Acceptance Criteria**:
- [ ] `## Re-anchor` 섹션이 10줄 이내로 추가됨
- [ ] Re-anchor에 "AC 상태는 iteration_state.md에서 읽는다" 지시 포함
- [ ] Re-anchor에 "이 단계는 읽기 전용 — 코드 수정 금지" 지시 포함
- [ ] Hard Rules에 inline 실행 시 행동 제약 명시
- [ ] 기존 agent spawn 경로에서도 정상 동작 유지 (하위 호환)

**Target Files**:
- [M] `.claude/agents/ac-plan.md` -- Re-anchor 섹션 + 행동 제약 추가

**Technical Notes**: Re-anchor 섹션은 `## Re-anchor` 헤더 아래 HTML 주석(`<!-- ... -->`)으로 용도 설명을 포함한다. agent spawn 경로에서는 이 섹션이 무해하게 존재한다 (단순 추가 지시일 뿐).
**Dependencies**: -

---

### Task T2: tdd-execute.md Re-anchor 섹션 + state 기록 절차 추가

**Component**: Re-anchor
**Priority**: P1-High
**Type**: Refactor

**Description**: `.claude/agents/tdd-execute.md`에 `## Re-anchor` 섹션을 추가한다. 또한 Step 4 (Integrate & Verify) 이후에 결과를 `iteration_state.md`에 기록하는 절차를 Output Format 또는 Process에 추가한다. 내부 task sub-agent spawn은 유지한다.

**Acceptance Criteria**:
- [ ] `## Re-anchor` 섹션이 10줄 이내로 추가됨
- [ ] Re-anchor에 "TDD 필수: RED → GREEN → REFACTOR" 핵심 지시 포함
- [ ] Re-anchor에 "결과는 iteration_state.md에 기록" 지시 포함
- [ ] Re-anchor에 "Spec 파일 불가침" 지시 포함
- [ ] Process에 iteration_state.md 기록 절차 추가
- [ ] 기존 agent spawn 경로에서도 정상 동작 유지

**Target Files**:
- [M] `.claude/agents/tdd-execute.md` -- Re-anchor 섹션 + state 기록 절차 추가

**Technical Notes**: tdd-execute는 내부에서 task sub-agent를 spawn한다. 이 부분은 변경하지 않는다 (task 단위는 작아서 가시성 문제 없음).
**Dependencies**: -

---

### Task T3: implementation-review.md Re-anchor 섹션 + state 기록 절차 추가

**Component**: Re-anchor
**Priority**: P1-High
**Type**: Refactor

**Description**: `.claude/agents/implementation-review.md`에 `## Re-anchor` 섹션을 추가한다. Step 5 (Summary) 이후에 이슈 요약을 `iteration_state.md`에 기록하는 절차를 추가한다. `.claude/skills/implementation-review/SKILL.md`도 동일하게 업데이트한다 (Mirror 동기화).

**Acceptance Criteria**:
- [ ] agent.md와 SKILL.md 모두에 `## Re-anchor` 섹션이 10줄 이내로 추가됨
- [ ] Re-anchor에 "Skeptical Evaluator Posture" 핵심 지시 포함
- [ ] Re-anchor에 "결과는 iteration_state.md에 기록" 지시 포함
- [ ] Re-anchor에 "Spec 파일 수정 금지" 지시 포함
- [ ] Process에 iteration_state.md 기록 절차 추가
- [ ] 기존 agent spawn 경로에서도 정상 동작 유지

**Target Files**:
- [M] `.claude/agents/implementation-review.md` -- Re-anchor 섹션 + state 기록 절차 추가
- [M] `.claude/skills/implementation-review/SKILL.md` -- Mirror 동기화

**Technical Notes**: implementation-review는 이미 SKILL.md가 존재하는 Mirror 패턴. 두 파일 동시 수정 필요.
**Dependencies**: -

---

### Task T4: iteration_state.md 형식 정의 + 읽기/쓰기 규약 설계

**Component**: State Externalization
**Priority**: P0-Critical
**Type**: Infrastructure

**Description**: `_sdd/implementation/iteration_state.md`의 형식과 읽기/쓰기 규약을 설계한다. 이 파일은 implementation iteration loop의 중간 상태를 저장하며, 각 sub-step이 결과를 기록하고 다음 sub-step이 필요한 부분만 읽는 데 사용된다.

**Acceptance Criteria**:
- [ ] iteration_state.md의 섹션 구조가 정의됨 (AC Status, Current Phase, Latest Step Result, Iteration History, Active Issues)
- [ ] 각 sub-step별 "무엇을 쓰는가" 규약이 정의됨:
  - ac-plan → AC Status 갱신 (subset 선택), Latest Step Result 갱신
  - tdd-execute → AC Status 갱신 (MET/NOT_MET/UNTESTED), Latest Step Result 갱신, 파일 변경 목록
  - implementation-review → Active Issues 갱신, AC Status 보정 (NOT_MET), Latest Step Result 갱신
  - orchestrator → Current Phase 갱신, Iteration History 추가
- [ ] 각 sub-step별 "무엇을 읽는가" 규약이 정의됨:
  - ac-plan → AC Status (전체), Iteration History, Active Issues
  - tdd-execute → AC Status (subset만), Latest Step Result (ac-plan 결과)
  - implementation-review → AC Status (전체), Latest Step Result (tdd-execute 결과)
  - orchestrator → AC Status, Active Issues (종료 판단)
- [ ] 파일 초기화 시점과 아카이브 규칙이 정의됨
- [ ] 형식 문서가 implementation SKILL.md 또는 별도 참조 파일에 포함됨

**Target Files**:
- [C] `_sdd/implementation/iteration_state_format.md` -- 형식 정의 + 읽기/쓰기 규약 문서 (implementation SKILL.md에서 참조)

**Technical Notes**: iteration_state.md는 런타임 파일이므로 git에 커밋되지 않는다 (.gitignore 추가 고려). 형식 정의 문서는 implementation SKILL.md에 인라인하거나 별도 참조로 둘 수 있다. 컨텍스트 효율을 위해 인라인 테이블 형태로 SKILL.md에 포함하는 것을 권장.
**Dependencies**: -

---

### Task T5: implementation SKILL.md Inline Orchestration 재작성

**Component**: Inline Orchestrator
**Priority**: P0-Critical
**Type**: Refactor

**Description**: `.claude/skills/implementation/SKILL.md`를 agent Mirror에서 Inline Orchestration 오케스트레이터로 전면 재작성한다. Step 4 (Iteration Loop)에서 `Agent()` 호출을 `Read()` + inline 실행으로 전환하고, Re-anchor 패턴과 State Externalization 패턴을 적용한다.

**Acceptance Criteria**:
- [ ] Step 4.1: `Read(".claude/agents/ac-plan.md")` → ac-plan 지시에 따라 inline 실행 → 결과를 iteration_state.md에 기록
- [ ] Step 4.1 후: `Read(".claude/agents/ac-plan.md", re-anchor 섹션만)` 또는 orchestrator 자체 re-anchor 수행
- [ ] Step 4.2: `Read(".claude/agents/tdd-execute.md")` → tdd-execute 지시에 따라 inline 실행 (task sub-agent spawn은 유지) → 결과를 iteration_state.md에 기록
- [ ] Step 4.2 후: re-anchor 수행
- [ ] Step 4.3: `Read(".claude/skills/implementation-review/SKILL.md")` 또는 `Read(".claude/agents/implementation-review.md")` → inline 실행 → 결과를 iteration_state.md에 기록
- [ ] Step 4.3 후: re-anchor 수행
- [ ] Step 4.4: `Read("_sdd/implementation/iteration_state.md")` → 종료 판단
- [ ] Mirror Notice 제거 (더 이상 agent의 Mirror가 아님)
- [ ] Orchestrator 자체 Re-anchor 섹션이 SKILL.md에 포함됨 (매 iteration 시작 시 자기 참조)
- [ ] iteration_state.md 초기화/아카이브 로직 포함
- [ ] 기존 AC (AC1~AC4) 모두 유지
- [ ] 대화에는 단계별 요약만 출력, 상세는 iteration_state.md에 기록

**Target Files**:
- [M] `.claude/skills/implementation/SKILL.md` -- Inline Orchestration 오케스트레이터로 전면 재작성

**Technical Notes**:

핵심 설계 결정:

1. **Re-anchor 위치**: SKILL.md 자체에 `## Re-anchor` 섹션을 두고, 매 iteration 시작 시 자기 자신의 이 섹션을 Read한다. 이는 sub-step 지시 파일의 Re-anchor와는 별개로, 오케스트레이터 수준의 핵심 지시를 갱신한다.

2. **Sub-step 지시 읽기 방식**: 각 sub-step의 전체 파일을 Read하는 것이 아니라, Process 섹션만 선택적으로 읽는 것을 권장. 다만 파일이 크지 않으면 전체 Read도 무방.

3. **Inline 실행의 의미**: Read한 지시를 "따르라"는 것이지, 별도 프로세스를 시작하는 것이 아님. 현재 컨텍스트에서 해당 지시의 Step들을 순차 실행하고, 완료 시 결과를 state에 기록.

4. **tdd-execute의 task sub-agent**: tdd-execute 지시를 inline으로 따르되, 그 안에서 task sub-agent를 Agent()로 spawn하는 것은 유지. 이 부분만 agent 격리가 남음. task sub-agent는 단일 AC + 소수 파일 대상이므로 실행 시간이 짧고 가시성 문제가 적음.

5. **출력 규칙**: 각 sub-step 완료 시 대화에 1-3줄 요약만 출력. 상세 결과는 iteration_state.md에. 이를 통해 사용자에게 진행 상황을 실시간으로 보여주면서도 컨텍스트를 lean하게 유지.

**Dependencies**: T1, T2, T3, T4

---

### Task T6: implementation agent.md Mirror 해제

**Component**: Agent File Decoupling
**Priority**: P2-Medium
**Type**: Refactor

**Description**: `.claude/agents/implementation.md`에서 Mirror 관계를 해제한다. SKILL.md가 독립적으로 변경되었으므로, agent.md는 sdd-autopilot 등 agent spawn 경로를 위한 독립 파일로 유지한다.

**Acceptance Criteria**:
- [ ] agent.md 하단의 Mirror Notice 관련 참조가 제거됨 (agent 파일에는 원래 Mirror Notice 없음 — SKILL.md에 있었음)
- [ ] agent.md의 Process Step 4에서 Agent() 호출 방식 유지 (agent 경로에서는 기존대로 동작)
- [ ] agent.md 상단에 "Inline Orchestration은 SKILL.md에서 수행. 이 파일은 agent spawn 경로(sdd-autopilot)용" 주석 추가

**Target Files**:
- [M] `.claude/agents/implementation.md` -- Mirror 해제 주석 + 독립 관리 선언

**Technical Notes**: agent.md도 향후 inline 패턴으로 전환할 수 있으나, 이번 scope에서는 기존 동작을 유지한다.
**Dependencies**: T5

---

### Task T7: 스펙 main.md 업데이트

**Component**: Spec Sync
**Priority**: P1-High
**Type**: Infrastructure

**Description**: `_sdd/spec/main.md`에 Part 1의 spec patch 내용을 반영한다. 이 태스크는 `spec-update-todo` 스킬을 사용하여 수행하거나 수동으로 반영한다.

**Acceptance Criteria**:
- [ ] Core Design > Design Patterns에 Inline Orchestration, Re-anchor, State Externalization 패턴 추가
- [ ] Core Design > Design Rationale에 Inline Orchestration 전환 근거 추가
- [ ] Architecture Overview > System Diagram에 inline instruction 반영
- [ ] Architecture Overview > _sdd/ Artifact Map에 iteration_state.md 추가
- [ ] Component Details > implementation 설명 업데이트
- [ ] Component Details > ac-plan, tdd-execute 설명에 "inline instruction으로도 사용됨" 추가
- [ ] Background & Motivation > Key Features, Agent 카운트 조정

**Target Files**:
- [M] `_sdd/spec/main.md` -- Inline Orchestration 반영

**Technical Notes**: `spec-update-todo` 스킬에 Part 1을 입력으로 전달하여 자동 반영 권장.
**Dependencies**: T5

## Parallel Execution Summary

| Phase | Total Tasks | Max Parallel | Sequential (conflicts) |
|-------|-------------|--------------|----------------------|
| Phase 1 | 3 (T1, T2, T3) | 3 | 없음 — 각각 다른 파일 수정 |
| Phase 2 | 1 (T4) | 1 | - |
| Phase 3 | 2 (T5, T6) | 1 | T6은 T5 완료 후 |
| Phase 4 | 1 (T7) | 1 | - |

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Re-anchor가 context dilution을 충분히 억제하지 못함 | 구현 품질 저하 | Re-anchor 빈도를 높이거나 (매 sub-step 전/후), orchestrator 자체 re-anchor를 더 강하게 설계 |
| iteration_state.md 파싱이 불안정 | 상태 유실 | 간단한 markdown 테이블 형식 사용, 파싱 실패 시 코드베이스에서 재추론하는 fallback |
| tdd-execute inline 실행 시 컨텍스트 과부하 | tdd-execute 자체의 지시가 길어 dilution 가속 | tdd-execute 지시의 핵심 부분만 선택적 Read, Process 섹션만 로드 |
| sdd-autopilot 경로와 skill 직접 호출 경로의 동작 차이 | 유지보수 부담 | agent.md와 SKILL.md의 core logic(AC, 종료 조건)은 동일하게 유지, 실행 방식만 다르게 |
| agent.md와 SKILL.md의 독립 관리로 인한 drift | 불일치 | SKILL.md를 primary로, agent.md는 필요 시만 갱신. 향후 agent.md도 inline으로 전환 검토 |

## Open Questions

- [ ] agent.md도 이번에 inline으로 전환할지, 아니면 sdd-autopilot 호출 경로를 위해 기존 Agent() 방식을 유지할지? (이 draft에서는 유지로 가정)
- [ ] iteration_state.md를 .gitignore에 추가할지? (런타임 파일이므로 추가 권장, 단 디버깅 시 유용할 수 있음)
- [ ] Re-anchor를 오케스트레이터만 할지, 각 sub-step 지시 파일도 자체 re-anchor를 가질지? (이 draft에서는 둘 다 보유)
- [ ] tdd-execute의 task sub-agent도 향후 inline으로 전환할지? (이번 scope에서는 유지)

## Model Recommendation

- **Phase 1 (T1-T3)**: 병렬 실행 가능. 각각 독립 파일 수정. Sonnet으로 충분.
- **Phase 2 (T4)**: 형식 설계. Opus 권장 (state 구조의 설계 품질이 전체 시스템에 영향).
- **Phase 3 (T5)**: 핵심 태스크. Opus 필수 (SKILL.md 전면 재작성, 설계 결정 다수).
- **Phase 3 (T6)**: 간단한 주석/notice 변경. Sonnet으로 충분.
- **Phase 4 (T7)**: spec-update-todo 활용. Sonnet으로 충분.

---

## Next Steps

### Apply Spec Patch
- **Method A (automatic)**: Run `spec-update-todo` -> Part 1을 입력으로 사용
- **Method B (manual)**: Part 1의 각 항목을 Target Section에 복사

### Execute Implementation
- **Parallel**: Run `implementation` skill -> Part 2를 계획으로 사용
- **Sequential**: Phase 순서대로 태스크를 순차 실행
