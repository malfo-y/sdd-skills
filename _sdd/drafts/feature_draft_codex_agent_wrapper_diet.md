# Feature Draft: Codex Agent Self-Containment + Wrapper Diet

**날짜**: 2026-03-19
**요청 배경**: Claude Code 쪽 pipeline wrapper/agent를 concise하게 정리한 흐름을 Codex에도 적용하고자 한다. 참고 문서인 `feature_draft_agent_self_containment.md`, `feature_draft_agent_self_containment_phase2.md`, `feature_draft_full_skills_ac_first.md`의 원칙을 Codex custom agent + wrapper 구조에 맞게 재해석한다.

<!-- spec-update-todo-input-start -->

# Part 1: Spec Patch Draft

> 이 패치는 `_sdd/spec/main.md`의 대응 섹션에 반영하거나, `spec-update-todo` 입력으로 그대로 사용할 수 있다.

# Spec Update Input

**Date**: 2026-03-19
**Author**: feature-draft
**Target Spec**: `_sdd/spec/main.md`
**Spec Update Classification**: SHOULD update

## Background & Motivation Updates

### Background Update: Codex custom agent도 self-contained + concise 원칙을 따른다
**Target Section**: `_sdd/spec/main.md` > `Core Design > Key Idea`
**Change Type**: Motivation / Architecture Clarification

**Current**:
현재 스펙은 Codex가 `.codex/agents/*.toml` custom agent와 `.codex/skills/*/SKILL.md` wrapper 구조를 사용한다고 정의하지만, 실제 Codex agent 다수는 `../skills/.../references/*.md` 및 `examples/*`를 핵심 실행 지침으로 참조한다. 또한 일부 agent는 400~800줄 수준으로 비대해져 핵심 decision gate와 hard rule이 장문 설명에 묻히고 있다.

**Proposed**:
Codex custom agent 레이어에도 Claude와 동일한 방향의 정제 원칙을 명시한다.

1. **AC-First**: agent 목적에 맞는 Acceptance Criteria를 먼저 정의하고 이를 만족시키는 최소 구조로 재작성한다.
2. **Self-Contained**: 실행에 필수인 규칙, decision gate, output contract, error handling은 agent TOML 내부에 인라인한다.
3. **Concise**: Context Management, References, Examples, Best Practices 중 런타임 필수가 아닌 장문 설명은 축약하거나 선택형 문서로 내린다.
4. **Wrapper Minimalism**: wrapper skill은 얇은 진입점으로 유지하되, trigger scope, output contract, delegation contract는 명시한다.

**Reason**:
1. custom agent 실행 단위는 reference/example 파일이 없어도 동작해야 안정적이다.
2. plugin/symlink/copy 혼합 설치 환경에서 상대경로 reference 의존은 취약하다.
3. 비대한 TOML은 Codex custom agent 컨텍스트를 과소비해 핵심 규칙 회수율을 떨어뜨린다.
4. Claude에서 검증된 concise wrapper + self-contained agent 패턴을 Codex에도 맞추면 dual-platform 유지보수 비용이 줄어든다.

---

## Design Changes

### Design Change: Codex custom agent의 핵심 실행 계약을 TOML 내부로 수렴
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Core Design > SKILL.md / Agent 정의 공통 구조`
**Change Type**: Prompt Architecture / Agent Contract

**Description**:
Codex custom agent는 `developer_instructions` 내부에 다음 요소를 자체 포함해야 한다.

- Acceptance Criteria
- Hard Rules
- Process / Step sequence
- Output location or output contract
- Decision gates and failure handling
- Platform-specific parallelization rules가 핵심 기능이면 해당 규칙의 압축판

`references/`와 `examples/`는 선택적 human-facing 보조 문서로 남길 수 있으나, agent가 이를 읽지 못해도 정상 동작해야 한다.

**Impact**:
- `.codex/agents/*.toml`의 구조가 짧고 직접 실행 가능한 형태로 바뀐다.
- `feature-draft`, `implementation`, `implementation-review`, `spec-update-done` 같이 현재 장문 reference 의존이 큰 agent가 우선 정리 대상이 된다.
- Codex-specific capability(병렬 worker dispatch, progress artifact, strict review-only 규칙)는 삭제하지 않고 agent 내부 핵심 계약으로 승격된다.

---

### Design Change: Codex wrapper skill을 concise contract 템플릿으로 통일
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Core Design > Design Patterns > Agent Wrapper 패턴`
**Change Type**: Wrapper Contract

**Description**:
Codex wrapper skill은 아래 4요소만 유지하는 표준 템플릿으로 통일한다.

1. trigger description
2. delegation statement
3. hard rules 3개 내외
4. output contract + execution clause

wrapper는 장문 workflow를 반복하지 않으며, 실행 로직은 custom agent가 책임진다. 단, trigger drift를 막기 위해 wrapper description/skill.json/agent description 사이 의미 불일치를 허용하지 않는다.

**Impact**:
- `.codex/skills/<name>/SKILL.md`가 Claude의 concise wrapper와 구조적으로 수렴한다.
- generated orchestrator와 사용자 직접 호출 모두 동일한 contract를 보게 된다.
- wrapper 수정 시 agent 책임 범위와 output artifact가 함께 검증 대상이 된다.

---

## New Features

### Feature: Codex self-contained execution layer
**Priority**: High
**Category**: Core Feature
**Target Component**: `.codex/agents/`
**Target Section**: `_sdd/spec/main.md` > `Goal > Key Features`

**Description**:
Codex custom agent 9개를 self-contained execution layer로 정제한다. 각 agent는 reference/example 파일이 없어도 핵심 프로세스를 수행할 수 있어야 하며, `_sdd/` artifact handoff 계약을 명시적으로 보존한다.

**Acceptance Criteria**:
- [ ] `feature-draft`, `implementation-plan`, `implementation`, `implementation-review`, `spec-review`, `spec-update-done`, `spec-update-todo`, `ralph-loop-init`, `write-phased`의 핵심 실행 규칙이 TOML 내부에 존재한다.
- [ ] 각 agent는 현재 사용하는 `_sdd/` 산출물 경로를 유지한다.
- [ ] 외부 reference/example 문서는 선택적 참고 자료로만 남고, 런타임 필수 의존이 아니다.
- [ ] Codex-specific execution model(예: parallel worker dispatch, review lane, generated orchestrator handoff)은 유지된다.

**Technical Notes**:
- `implementation-review`의 parallel lane, `implementation`의 progress tracking, `spec-review`의 strict review-only, `write-phased`의 2-phase generation은 삭제 대상이 아니다.
- 정제 시 Claude 문서를 그대로 복사하지 않고 Codex 도구/실행 모델 차이를 보존해야 한다.

**Dependencies**:
- `.codex/agents/feature-draft.toml`
- `.codex/agents/implementation-plan.toml`
- `.codex/agents/implementation.toml`
- `.codex/agents/implementation-review.toml`
- `.codex/agents/spec-review.toml`
- `.codex/agents/spec-update-done.toml`
- `.codex/agents/spec-update-todo.toml`
- `.codex/agents/ralph-loop-init.toml`
- `.codex/agents/write-phased.toml`

---

### Feature: Codex concise wrapper parity
**Priority**: High
**Category**: Enhancement
**Target Component**: `.codex/skills/`
**Target Section**: `_sdd/spec/main.md` > `Core Design > Design Patterns > Agent Wrapper 패턴`

**Description**:
Codex wrapper skill을 Claude의 concise wrapper 수준으로 정제하되, Codex custom agent naming과 output contract를 유지한다. wrapper는 얇아지지만 trigger scope와 artifact handoff는 더 엄격히 맞춘다.

**Acceptance Criteria**:
- [ ] 9개 pipeline wrapper가 공통 concise 템플릿을 따른다.
- [ ] `SKILL.md`와 `skill.json`의 description이 agent responsibility와 충돌하지 않는다.
- [ ] wrapper는 direct user entry와 generated orchestrator handoff 모두를 설명할 수 있다.
- [ ] wrapper의 output contract가 agent output과 일치한다.

**Technical Notes**:
- wrapper에서 장문 workflow를 제거해도 output contract는 유지한다.
- agent 이름 표기(`feature_draft`, `implementation_review` 등 underscore style)는 Codex custom agent naming을 따른다.

**Dependencies**:
- `.codex/skills/feature-draft/SKILL.md`
- `.codex/skills/implementation-plan/SKILL.md`
- `.codex/skills/implementation/SKILL.md`
- `.codex/skills/implementation-review/SKILL.md`
- `.codex/skills/spec-review/SKILL.md`
- `.codex/skills/spec-update-done/SKILL.md`
- `.codex/skills/spec-update-todo/SKILL.md`
- `.codex/skills/ralph-loop-init/SKILL.md`
- `.codex/skills/write-phased/SKILL.md`

---

## Improvements

### Improvement: Codex agent의 reference/example 런타임 의존 제거
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Core Design > Key Idea`
**Current State**:
현재 여러 Codex agent가 `../skills/.../references/*.md` 또는 `examples/*`를 직접 읽거나, 해당 문서의 존재를 핵심 알고리즘의 전제로 둔다. 대표적으로 `feature-draft`, `implementation-plan`, `implementation`, `spec-update-todo`, `spec-update-done`, `spec-review`, `ralph-loop-init`이 여기에 해당한다.

**Proposed**:
핵심 로직은 agent TOML에 인라인하고, reference/example는 선택형 보조 자료로 격하한다. 남는 reference는 human documentation 또는 회귀 검증 샘플에 한정한다.

**Reason**:
Codex agent가 독립 실행 단위로 동작하려면 설치 형태와 무관하게 핵심 규칙 회수가 가능해야 한다.

---

### Improvement: Codex agent line budget 및 섹션 구조 표준화
**Priority**: Medium
**Target Section**: `_sdd/spec/main.md` > `Core Design > SKILL.md / Agent 정의 공통 구조`
**Current State**:
현재 Codex agent는 `implementation-review` 835줄, `implementation` 695줄, `feature-draft` 680줄, `spec-update-done` 527줄 등 편차가 크고, `Context Management`, `Integration`, `References`, `Examples` 섹션이 핵심 프로세스보다 과도하게 길다.

**Proposed**:
다음 표준을 추가한다.

- wrapper-backed custom agent는 우선 150~450줄 범위를 목표로 정제한다.
- 필수 섹션은 Acceptance Criteria, Hard Rules, Process, Output/Artifacts, Error Handling 중심으로 재구성한다.
- 선택 섹션은 필요한 agent만 유지하고, 반복 표/예시는 과감히 압축한다.

**Reason**:
LLM이 핵심 제약과 산출물 계약을 안정적으로 회수하게 하려면 prompt surface를 줄여야 한다.

---

## Notes

### Context
- 이 draft는 Claude 쪽 concise wrapper/agent 정제를 Codex에 적용하기 위한 계획이다.
- 기존 draft `feature_draft_agent_self_containment*.md`는 Claude agent 중심, `feature_draft_full_skills_ac_first.md`는 full skill 정제 중심이다.
- 이번 draft는 Codex custom agent + wrapper에만 초점을 둔다.

### Constraints
- `.codex/agents/*.toml`의 custom agent naming과 Codex-specific execution model은 유지한다.
- `_sdd/` artifact handoff 경로를 바꾸지 않는다.
- full skill(`spec-create`, `spec-summary`, `discussion`, `pr-review` 등) 정제는 이번 scope에서 제외한다.

### Decision-Log Candidates
- Codex custom agent는 runtime-critical 규칙을 외부 reference에 의존하지 않는다.
- Codex wrapper는 concise contract를 유지하되 output contract를 반드시 포함한다.

## Recommended Decisions

- **Line budget 정책**: hard limit 대신 권장 범위 정책을 사용한다. wrapper-backed custom agent는 우선 150~450줄을 목표로 하되, 500줄 초과 시 축약 검토, 650줄 초과 시 예외 사유를 남긴다.
- **reference/example 정책**: 완전 삭제하지 않고 optional docs + 회귀 비교용 fixture로 유지한다. 단, runtime-critical 규칙은 agent TOML 내부에 존재해야 한다.
- **압축 기준선**: `implementation-review`와 `implementation`은 line count가 아니라 contract preservation 기준으로 압축한다. parallel lane, progress artifact, verification, review-only, final report contract는 필수 보존 항목으로 본다.

<!-- spec-update-todo-input-end -->

# Part 2: Implementation Plan

## Overview
Codex custom agent 9개와 대응 wrapper 9개를 대상으로, Claude에서 검증된 concise wrapper + self-contained agent 원칙을 Codex 실행 모델에 맞게 적용한다. 핵심 목표는 외부 reference 의존 제거, runtime-critical contract 인라인, wrapper/agent/metadata 정합성 확보이다.

## Scope

### In Scope
- `.codex/agents/*.toml` 9개 self-contained 재작성
- 대응 `.codex/skills/*/SKILL.md` wrapper 정제
- 관련 `skill.json` description/trigger 정합성 점검
- runtime-critical reference 내용을 agent 내부로 흡수하거나 축약
- `_sdd/` artifact contract 유지 검증

### Out of Scope
- `.claude/` 문서 추가 정리
- full skill(`spec-create`, `spec-summary`, `discussion`, `guide-create`, `pr-review` 등) 정제
- autopilot/generated orchestrator의 구조 개편
- custom agent 개수나 이름 체계 변경

## Components
1. **Core Delivery Agents**: `feature-draft`, `implementation-plan`, `implementation`, `implementation-review`
2. **Spec Sync/Review Agents**: `spec-update-done`, `spec-update-todo`, `spec-review`
3. **Utility Agents**: `write-phased`, `ralph-loop-init`
4. **Wrapper Contracts**: `.codex/skills/*/SKILL.md`, `skill.json`
5. **Reference Decomposition**: 기존 `references/`, `examples/`의 runtime-critical 내용 추출/축약

## Implementation Phases

### Phase 1: Core Delivery Agent Diet
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 1 | Core delivery agent self-contained 재작성 | P0 | - | Core Delivery Agents |
| 2 | Core wrapper concise parity 정리 | P1 | 1 | Wrapper Contracts |

### Phase 2: Spec Lifecycle Agent Diet
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 3 | Spec sync/review agent self-contained 재작성 | P0 | - | Spec Sync/Review Agents |
| 4 | Spec lifecycle wrapper/metadata 정리 | P1 | 3 | Wrapper Contracts |

### Phase 3: Utility + Verification
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 5 | Utility agent 정리 (`write-phased`, `ralph-loop-init`) | P1 | - | Utility Agents |
| 6 | Reference decomposition + parity verification | P0 | 1,2,3,4,5 | Reference Decomposition |

## Task Details

### Task 1: Core delivery agent self-contained 재작성
**Component**: Core Delivery Agents
**Priority**: P0
**Type**: Refactor

**Description**:
Codex의 핵심 delivery agent 4개를 self-contained + AC-first 구조로 재작성한다. 각 agent는 core rules, decision gate, output artifact, failure handling을 TOML 내부에 직접 포함해야 한다.

**Acceptance Criteria**:
- [ ] `feature-draft.toml`이 `adaptive-questions`, `output-format`, `target-files-spec`, `tool-and-gates` reference 없이도 핵심 draft 생성이 가능하다.
- [ ] `implementation-plan.toml`이 target-files 규격과 phase planning 핵심 규칙을 자체 포함한다.
- [ ] `implementation.toml`이 parallel execution, progress artifact, verification contract를 자체 포함한다.
- [ ] `implementation-review.toml`이 review-only contract와 parallel lane 핵심 규칙을 자체 포함한다.

**Target Files**:
- [M] `.codex/agents/feature-draft.toml` -- reference-heavy draft generation 규칙을 self-contained로 재작성
- [M] `.codex/agents/implementation-plan.toml` -- planning contract를 concise하게 재구성
- [M] `.codex/agents/implementation.toml` -- parallel/TDD/progress contract를 압축 유지
- [M] `.codex/agents/implementation-review.toml` -- review-only + lane contract를 압축 유지

**Technical Notes**:
- Claude agent의 concise화 원칙을 참고하되, Codex-specific worker/lane orchestration은 삭제하지 않는다.
- 각 agent는 외부 문서 없이도 “최소한 올바른 결과물”을 낼 수 있어야 한다.
- 구현 착수 순서는 `feature-draft` + `implementation-review`를 pilot으로 우선 적용한 뒤, 나머지 core agent로 확장하는 것을 기본 전략으로 한다.

**Dependencies**: -

### Task 2: Core wrapper concise parity 정리
**Component**: Wrapper Contracts
**Priority**: P1
**Type**: Refactor

**Description**:
Core delivery wrapper 4개와 metadata를 concise contract 템플릿으로 정리한다. wrapper는 trigger, delegation, output contract만 유지하고 장문 설명은 agent로 내린다.

**Acceptance Criteria**:
- [ ] `feature-draft`, `implementation-plan`, `implementation`, `implementation-review` wrapper가 공통 concise template을 따른다.
- [ ] `SKILL.md`와 `skill.json` description이 agent responsibility와 일치한다.
- [ ] output contract가 실제 `_sdd/` artifact와 맞는다.

**Target Files**:
- [M] `.codex/skills/feature-draft/SKILL.md` -- concise wrapper template 정렬
- [M] `.codex/skills/feature-draft/skill.json` -- trigger/description 정합성 점검
- [M] `.codex/skills/implementation-plan/SKILL.md` -- concise wrapper template 정렬
- [M] `.codex/skills/implementation-plan/skill.json` -- description 정합성 점검
- [M] `.codex/skills/implementation/SKILL.md` -- concise wrapper template 정렬
- [M] `.codex/skills/implementation/skill.json` -- description 정합성 점검
- [M] `.codex/skills/implementation-review/SKILL.md` -- concise wrapper template 정렬
- [M] `.codex/skills/implementation-review/skill.json` -- description 정합성 점검

**Technical Notes**:
- wrapper는 얇아지지만 output contract는 유지한다.
- direct user entry와 generated orchestrator handoff 문구를 동시에 수용하되, orchestrator 언급은 `Execution` 1줄 수준으로 최소화한다.

**Dependencies**: 1

### Task 3: Spec sync/review agent self-contained 재작성
**Component**: Spec Sync/Review Agents
**Priority**: P0
**Type**: Refactor

**Description**:
Spec lifecycle 관련 agent 3개를 self-contained + concise 구조로 재작성한다. drift detection, section mapping, strict review checklist의 핵심 규칙을 TOML 내부로 가져오고, reference 문서는 선택형으로 낮춘다.

**Acceptance Criteria**:
- [ ] `spec-update-done.toml`이 drift pattern과 update strategy의 핵심 규칙을 자체 포함한다.
- [ ] `spec-update-todo.toml`이 input 분류와 section mapping 핵심 규칙을 자체 포함한다.
- [ ] `spec-review.toml`이 strict review-only checklist와 severity decision 규칙을 자체 포함한다.
- [ ] 세 agent 모두 `_sdd/spec/*` 산출물 계약을 유지한다.

**Target Files**:
- [M] `.codex/agents/spec-update-done.toml` -- drift/update rules self-contained 재작성
- [M] `.codex/agents/spec-update-todo.toml` -- section mapping/input parsing self-contained 재작성
- [M] `.codex/agents/spec-review.toml` -- strict review checklist self-contained 재작성

**Technical Notes**:
- `spec-update-done`와 `spec-review`의 trigger scope는 혼선이 없어야 한다.
- review-only와 mutate-after-report의 경계는 문서 수준에서 명확히 고정한다.

**Dependencies**: -

### Task 4: Spec lifecycle wrapper/metadata 정리
**Component**: Wrapper Contracts
**Priority**: P1
**Type**: Refactor

**Description**:
Spec lifecycle wrapper 3개와 metadata를 concise contract로 맞춘다. 특히 `spec-review`와 `spec-update-done`의 trigger drift를 방지한다.

**Acceptance Criteria**:
- [ ] `spec-review`는 strict review-only 의미를 wrapper와 metadata 모두에서 유지한다.
- [ ] `spec-update-done`는 implementation-to-spec sync 요청으로만 한정된다.
- [ ] `spec-update-todo`는 user-input-to-spec update 요청 범위를 명확히 유지한다.

**Target Files**:
- [M] `.codex/skills/spec-review/SKILL.md` -- concise wrapper + strict review-only title 유지
- [M] `.codex/skills/spec-review/skill.json` -- review-only trigger 정합성 점검
- [M] `.codex/skills/spec-update-done/SKILL.md` -- concise wrapper + sync-only trigger 정렬
- [M] `.codex/skills/spec-update-done/skill.json` -- sync-only metadata 정렬
- [M] `.codex/skills/spec-update-todo/SKILL.md` -- concise wrapper template 정렬
- [M] `.codex/skills/spec-update-todo/skill.json` -- description 정합성 점검

**Technical Notes**:
- Claude 쪽에서 겪었던 trigger drift를 Codex에서 선제 차단한다.

**Dependencies**: 3

### Task 5: Utility agent 정리 (`write-phased`, `ralph-loop-init`)
**Component**: Utility Agents
**Priority**: P1
**Type**: Refactor

**Description**:
Utility agent 2개를 self-contained로 정리한다. `write-phased`는 2-phase generation 규칙을 짧고 안정적으로 유지하고, `ralph-loop-init`은 reference/example fallback을 optional docs로 내린다.

**Acceptance Criteria**:
- [ ] `write-phased.toml`은 skeleton → fill 규칙, in-place patch 원칙, finalize 규칙만으로 충분히 동작한다.
- [ ] `ralph-loop-init.toml`은 `ralph-loop-concept`나 example shell/state 파일 없이도 기본 workspace를 생성할 수 있다.
- [ ] utility wrapper도 output contract를 유지한다.

**Target Files**:
- [M] `.codex/agents/write-phased.toml` -- concise self-contained 2-phase agent 유지/정리
- [M] `.codex/agents/ralph-loop-init.toml` -- fallback-heavy 구조를 self-contained로 정리
- [M] `.codex/skills/write-phased/SKILL.md` -- concise wrapper contract 정렬
- [M] `.codex/skills/write-phased/skill.json` -- description 정합성 점검
- [M] `.codex/skills/ralph-loop-init/SKILL.md` -- concise wrapper contract 정렬
- [M] `.codex/skills/ralph-loop-init/skill.json` -- description 정합성 점검

**Technical Notes**:
- `ralph-loop-init`는 Codex-specific long-running process setup 책임을 유지해야 한다.

**Dependencies**: -

### Task 6: Reference decomposition + parity verification
**Component**: Reference Decomposition
**Priority**: P0
**Type**: Verification

**Description**:
모든 wrapper-backed Codex agent에 대해 runtime-critical reference 의존이 제거되었는지 검증하고, dual-platform parity를 점검한다.

**Acceptance Criteria**:
- [ ] `.codex/agents/*.toml`에서 runtime-critical `../skills/.../references` 의존이 제거되거나 optional note 수준으로 축소된다.
- [ ] wrapper/skill.json/agent description 사이 trigger drift가 없다.
- [ ] `_sdd/` artifact contract가 기존 spec과 일치한다.
- [ ] Claude와 Codex가 구조는 달라도 책임 경계(wrapper vs agent)는 동일하게 유지된다.
- [ ] 각 agent는 외부 reference/example 없이도 최소 입력으로 expected `_sdd/` artifact를 생성하거나 올바른 review 결과를 산출하는 smoke check를 통과한다.

**Target Files**:
- [M] `.codex/agents/feature-draft.toml` -- final dependency pruning
- [M] `.codex/agents/implementation-plan.toml` -- final dependency pruning
- [M] `.codex/agents/implementation.toml` -- final dependency pruning
- [M] `.codex/agents/implementation-review.toml` -- final dependency pruning
- [M] `.codex/agents/spec-update-done.toml` -- final dependency pruning
- [M] `.codex/agents/spec-update-todo.toml` -- final dependency pruning
- [M] `.codex/agents/spec-review.toml` -- final dependency pruning
- [M] `.codex/agents/ralph-loop-init.toml` -- final dependency pruning
- [M] `.codex/agents/write-phased.toml` -- final dependency pruning
- [M] `.codex/skills/feature-draft/SKILL.md` -- parity verification 후 contract 점검
- [M] `.codex/skills/implementation-plan/SKILL.md` -- parity verification 후 contract 점검
- [M] `.codex/skills/implementation/SKILL.md` -- parity verification 후 contract 점검
- [M] `.codex/skills/implementation-review/SKILL.md` -- parity verification 후 contract 점검
- [M] `.codex/skills/spec-review/SKILL.md` -- parity verification 후 contract 점검
- [M] `.codex/skills/spec-update-done/SKILL.md` -- parity verification 후 contract 점검
- [M] `.codex/skills/spec-update-todo/SKILL.md` -- parity verification 후 contract 점검
- [M] `.codex/skills/write-phased/SKILL.md` -- parity verification 후 contract 점검
- [M] `.codex/skills/ralph-loop-init/SKILL.md` -- parity verification 후 contract 점검

**Technical Notes**:
- optional human-facing docs는 남겨도 되지만, agent correctness를 좌우하면 안 된다.
- verification 결과는 wrapper 얇아짐과 agent 자급자족 두 축을 동시에 확인해야 한다.

**Dependencies**: 1, 2, 3, 4, 5

## Parallel Execution Summary
| Phase | Total Tasks | Max Parallel | Sequential (conflicts) |
|-------|-------------|--------------|------------------------|
| Phase 1 | 2 | 1 | Task 2는 Task 1 이후 |
| Phase 2 | 2 | 1 | Task 4는 Task 3 이후 |
| Phase 3 | 2 | 1 | Task 6은 Task 5 및 이전 phase 이후 |

## Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| Codex-specific 병렬 규칙이 과도하게 삭제됨 | 기능 회귀 | self-contained화 시 runtime-critical contract 목록을 먼저 고정 |
| wrapper와 agent trigger drift | 잘못된 라우팅 | `SKILL.md`/`skill.json`/agent description 동시 점검 |
| reference 제거 후 예시/체크리스트 품질 저하 | 출력 품질 하락 | optional docs로 유지하되 핵심 규칙만 agent에 인라인 |
| dual-platform parity를 무리하게 동일화 | 플랫폼 강점 손실 | 구조 원칙만 공유하고 실행 세부는 플랫폼별로 유지 |

## Recommended Decisions
- **Wrapper execution 문구**: Codex에서도 Claude처럼 wrapper를 더 줄이되, `generated orchestrator` 언급은 `Execution` 1줄로 유지한다.
- **Optional docs 처리**: optional docs는 완전히 제거하지 않고, human-facing docs 및 regression fixture로 유지한다.
- **길이 축약 기준**: `implementation-review`와 `implementation`은 contract preservation을 기준으로 축약하며, line budget은 참고값일 뿐 통과 기준이 아니다.

## Model Recommendation
`feature-draft`, `implementation`, `implementation-review`, `spec-update-done`는 구조 보존과 대규모 압축이 함께 필요하므로 고성능 reasoning 모델 우선이 적합하다. wrapper/metadata 정리는 중간급 모델로도 가능하지만, final parity verification은 다시 상위 모델 검토가 바람직하다.
