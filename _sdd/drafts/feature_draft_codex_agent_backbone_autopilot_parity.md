# Feature Draft: Codex Agent Backbone + Autopilot Spawn Parity

**Date**: 2026-03-17
**Author**: Codex
**Target Spec**: main.md
**Status**: Draft
**Features**: Codex custom agent layer, wrapper parity, autopilot agent spawn, write-phased nested parity

---

<!-- spec-update-todo-input-start -->
# Part 1: Spec Patch Draft

> 이 패치는 해당 스펙 섹션에 copy-paste하거나,
> `spec-update-todo` 스킬의 입력으로 사용할 수 있습니다.

# Spec Update Input

**Date**: 2026-03-17
**Author**: Codex
**Target Spec**: `_sdd/spec/main.md`
**Spec Update Classification**: MUST update

## Background & Motivation Updates

### Background Update: Codex autopilot 실행 모델 공백 해소
**Target Section**: `_sdd/spec/main.md` > `배경 및 동기 (§1)`
**Change Type**: Problem Statement / Motivation / Alternative Comparison

**Current**:
현재 Codex 쪽 스펙과 스킬 문서는 `sdd-autopilot`, generated orchestration skill, execution unit 재사용을 설명하지만, 실제로 오케스트레이터가 spawn하여 사용할 repo-local custom agent 레이어는 없다. 이 상태에서는 "파이프라인을 생성한다"는 설명은 존재하지만, Claude Code의 `autopilot -> orchestrator -> agent`에 대응하는 실행 backbone은 비어 있다.

**Proposed**:
Codex에도 `.codex/agents/` 기반 custom agent 레이어를 도입한다. 단, 새 비즈니스 역할을 발명하지 않고 기존 SDD 역할(feature-draft, implementation-plan, implementation, implementation-review, spec-update-done, spec-update-todo, spec-review, ralph-loop-init, write-phased)만 custom agent로 정의한다. 기존 `.codex/skills/*`는 사용자 진입점과 문서화 surface를 유지하는 wrapper로 남긴다.

**Reason**:
Codex autopilot이 실제로 end-to-end 파이프라인을 실행하려면, generated orchestrator가 호출할 실체가 필요하다. wrapper skill만으로는 skill 자체를 subagent처럼 spawn할 수 없으므로, custom agent 레이어를 명시적으로 도입해야 한다.

### Background Update: write-phased 중첩 전략의 Codex parity 필요
**Target Section**: `_sdd/spec/main.md` > `배경 및 동기 (§1)`
**Change Type**: Problem Statement / Motivation / Alternative Comparison

**Current**:
Codex의 `write-phased`는 공용 long-form utility로 문서화되었지만, 실제로 어떤 핵심 실행 단위가 이를 nested subagent로 사용하는지는 정의되지 않았다. 특히 장문 산출물이 핵심인 planning/review 계열에서 Claude parity가 깨져 있다.

**Proposed**:
Codex에서도 장문 산출물 중심의 핵심 agent(`feature-draft`, `implementation-plan`, `implementation-review`, `spec-review`)가 `write-phased`를 nested custom agent로 사용하도록 정의한다. `implementation`, `spec-update-done`, `spec-update-todo`는 1차 범위에서 제외하고 필요 시 후속 최적화로 다룬다.

**Reason**:
긴 스펙 패치, 구현 계획, 리뷰 리포트는 skeleton -> fill 2단계 작성 전략의 수혜가 가장 크다. write-phased를 utility로만 설명하고 nested usage를 생략하면 품질 패턴이 반쯤만 이식된다.

---

## Design Changes

### Design Change: Codex custom agent layer 추가
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `핵심 설계 (§2)`
**Change Type**: Logic Flow / Design Rationale

**Description**:
Codex 아키텍처에 `.codex/agents/*.toml` custom agent 레이어를 추가한다. 각 agent 파일은 기존 SDD skill의 역할과 동일한 이름/책임을 가지되, 서브에이전트로 spawn될 수 있는 실행 단위로 정의된다.

권장 agent 집합:
- `feature_draft`
- `implementation_plan`
- `implementation`
- `implementation_review`
- `spec_update_todo`
- `spec_update_done`
- `spec_review`
- `ralph_loop_init`
- `write_phased`

**Impact**:
- Codex의 실제 실행 backbone이 생긴다.
- generated orchestrator가 "skill 설명"이 아니라 "spawn 가능한 agent 이름"을 기준으로 설계된다.
- skill과 agent의 역할 분리가 명확해진다.

### Design Change: Wrapper Skill + Custom Agent parity 도입
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `핵심 설계 (§2)` > `Design Patterns`
**Change Type**: Logic Flow / Design Rationale

**Description**:
Codex에도 Claude와 대응되는 wrapper pattern을 도입한다. 다만 구현 수단은 `.claude/agents/*.md`가 아니라 `.codex/agents/*.toml` 기반 custom agent다.

구조:
- custom agent: `.codex/agents/<name>.toml`
- wrapper skill: `.codex/skills/<name>/SKILL.md`
- skill metadata: `.codex/skills/<name>/skill.json`

wrapper skill의 역할:
1. 사용자 직접 호출 진입점 유지
2. custom agent에게 사용자 원문 요청과 관련 artifact 경로를 전달
3. standalone 호출과 orchestrator 하위 호출 모두 동일한 결과 계약 유지

**Impact**:
- 사용자는 기존처럼 `$feature-draft`, `$implementation` 등을 직접 사용할 수 있다.
- autopilot/orchestrator는 wrapper skill이 아니라 custom agent를 직접 spawn한다.
- skill 본문과 agent 동작의 책임 경계가 명확해진다.

### Design Change: Generated orchestration skill은 custom agent만 spawn
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `핵심 설계 (§2)`
**Change Type**: Logic Flow / Design Rationale

**Description**:
Codex의 generated orchestration skill은 skill 이름을 직접 실행 단위로 취급하지 않는다. 대신 `.codex/agents/`에 정의된 custom agent 이름을 명시적으로 사용하여 파이프라인을 실행한다.

예시:
- `feature_draft`
- `implementation_plan`
- `implementation`
- `implementation_review`
- `spec_update_done`

오케스트레이터 규약:
- 각 step은 사용할 agent 이름과 입력 artifact 경로를 명시한다.
- resume 시에는 `_sdd/pipeline/log_*.md`의 Status를 읽고 첫 미완료 step의 agent부터 재개한다.
- review 포함 시 `implementation_review -> implementation -> implementation_review` 루프를 최대 3회 강제한다.

**Impact**:
- "skill을 subagent처럼 쓴다"는 오해를 제거한다.
- Codex subagent 모델과 repo 설계를 일치시킨다.
- generated orchestrator 품질 검증 기준이 선명해진다.

### Design Change: Codex pre-flight에 `.codex/config.toml`과 `_sdd/env.md` 포함
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `핵심 설계 (§2)`
**Change Type**: Algorithm / Design Rationale

**Description**:
Codex `sdd-autopilot`의 Pre-flight Check는 `_sdd/env.md`뿐 아니라 `.codex/config.toml`도 함께 읽는다. 최소 확인 항목은 다음과 같다.

- `_sdd/env.md`: 외부 서비스, 환경 변수, 테스트 방법, 빌드/배포 요구
- `.codex/config.toml`:
  - `agents.max_threads`
  - `agents.max_depth`
  - optional agent runtime defaults

기본 정책:
- `autopilot -> custom agent -> write_phased` 중첩을 지원하려면 `agents.max_depth >= 2`
- 병렬 review/exploration을 허용하려면 `agents.max_threads`가 파이프라인 요구치를 충족해야 함
- 갭이 있으면 승인 전에 사용자에게 리스크로 제시

**Impact**:
- nested subagent 호출이 설정 부족으로 실패하는 상황을 미리 방지한다.
- autopilot 승인 단계가 실제 실행 가능성까지 검증하는 checkpoint가 된다.

### Design Change: write-phased nested parity for long-form agents
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `핵심 설계 (§2)`
**Change Type**: Algorithm / Design Rationale

**Description**:
다음 Codex custom agent는 장문 산출물이 필요할 때 `write_phased` agent를 nested spawn하여 skeleton -> fill 전략을 사용한다.

- `feature_draft`
- `implementation_plan`
- `implementation_review`
- `spec_review`

규칙:
- nested 호출은 output generation 단계에서만 수행
- 상위 agent는 `write_phased`에 전체 output format과 필요한 맥락을 그대로 넘긴다
- 중첩이 불필요하게 깊어지면 orchestration layer 직적용 대신 해당 agent 내부에서만 한 번 중첩한다

**Impact**:
- Codex 장문 산출물의 구조적 일관성과 품질이 개선된다.
- Claude Code와 동일한 long-form writing 패턴을 확보한다.

---

## New Features

### Feature: Codex custom agent backbone
**Priority**: High
**Category**: Core Feature
**Target Component**: `.codex/agents/`
**Target Section**: `_sdd/spec/main.md` > `Goal > Key Features`

**Description**:
Codex용 custom agent backbone을 도입하여, 기존 SDD 핵심 역할들을 실제로 spawn 가능한 단위로 만든다. 이 계층은 wrapper skill 아래에서 작동하며, autopilot/generated orchestrator가 직접 사용하는 실행 레이어가 된다.

**Acceptance Criteria**:
- [ ] `.codex/agents/` 디렉토리가 생성된다.
- [ ] 기존 SDD 핵심 역할 8개 + `write_phased`가 custom agent로 정의된다.
- [ ] 각 agent는 name, description, developer_instructions를 가진 TOML 형식을 따른다.
- [ ] 각 agent는 대응 wrapper skill 또는 orchestrator에서 참조 가능한 안정적인 이름을 갖는다.

**Technical Notes**:
- agent 이름은 skill 이름과 구분하기 위해 underscore 스타일을 기본으로 사용한다.
- business/domain agent를 추가하지 않고 기존 SDD 역할만 옮긴다.
- developer_instructions는 대응 skill 문서를 source-of-truth workflow로 참조하도록 설계할 수 있다.

**Dependencies**:
- `.codex/config.toml`
- `.codex/skills/feature-draft/`
- `.codex/skills/implementation-plan/`
- `.codex/skills/implementation/`
- `.codex/skills/implementation-review/`
- `.codex/skills/spec-update-done/`
- `.codex/skills/spec-update-todo/`
- `.codex/skills/spec-review/`
- `.codex/skills/ralph-loop-init/`
- `.codex/skills/write-phased/`

### Feature: Wrapper parity for user entry points
**Priority**: High
**Category**: Enhancement
**Target Component**: Codex pipeline skills
**Target Section**: `_sdd/spec/main.md` > `Goal > Key Features`

**Description**:
기존 Codex pipeline skill들을 wrapper skill로 재정렬하여, 사용자는 기존 호출 인터페이스를 유지하면서도 내부적으로는 custom agent 실행 경로를 사용하게 한다.

**Acceptance Criteria**:
- [ ] `feature-draft`, `implementation-plan`, `implementation`, `implementation-review`, `spec-update-done`, `spec-update-todo`, `spec-review`, `ralph-loop-init`가 wrapper 역할을 명시한다.
- [ ] wrapper skill은 standalone direct use와 autopilot 하위 실행 모두 지원한다.
- [ ] discussion은 full interactive skill로 유지된다.
- [ ] `write-phased`는 direct skill + custom agent 양쪽 용도를 모두 가진다.

**Technical Notes**:
- wrapper skill은 전체 업무 로직을 중복 구현하지 않고 agent handoff와 결과 계약을 우선 설명한다.
- standalone 호출에서도 입력/출력 형식은 기존과 호환되어야 한다.

**Dependencies**:
- `.codex/agents/`
- `.codex/skills/discussion/`

### Feature: Autopilot agent-spawn execution model
**Priority**: High
**Category**: Core Feature
**Target Component**: `sdd-autopilot`
**Target Section**: `_sdd/spec/main.md` > `Goal > Key Features`

**Description**:
Codex `sdd-autopilot`은 generated orchestration skill을 만들고, 그 orchestrator가 custom agent를 명시적으로 spawn하는 실행 모델을 사용한다. generated orchestrator는 step별로 agent 이름, 입력 artifact, 출력 artifact, resume 상태, review-fix 규칙을 기록한다.

**Acceptance Criteria**:
- [ ] `sdd-autopilot` 문서가 skill 직접 실행이 아니라 custom agent spawn 모델을 명시한다.
- [ ] generated orchestration skill 예시가 custom agent 이름을 사용한다.
- [ ] 오케스트레이터는 skill 이름을 하위 실행 단위처럼 취급하지 않는다.
- [ ] review-fix 루프가 `implementation_review` 중심으로 정의된다.
- [ ] active orchestrator / archived orchestrator / pipeline log 계약이 새 실행 모델에도 그대로 유지된다.

**Technical Notes**:
- small/medium/large 파이프라인마다 어떤 agent가 필요한지 명시적 매핑 테이블이 필요하다.
- resume는 `_sdd/pipeline/log_*.md`의 Status 기반으로 동작한다.

**Dependencies**:
- `.codex/skills/sdd-autopilot/`
- `.codex/skills/sdd-autopilot/references/pipeline-templates.md`
- `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md`
- `.codex/agents/`

### Feature: write-phased nested parity for long-form producers
**Priority**: Medium
**Category**: Enhancement
**Target Component**: `write-phased`
**Target Section**: `_sdd/spec/main.md` > `Goal > Key Features`

**Description**:
Codex custom agent 중 장문 산출물이 핵심인 planning/review 계열은 `write_phased` custom agent를 nested spawn하여 최종 문서를 작성한다.

**Acceptance Criteria**:
- [ ] `feature_draft`가 장문 draft 생성 시 `write_phased`를 nested 호출할 수 있다.
- [ ] `implementation_plan`이 장문 plan 생성 시 `write_phased`를 nested 호출할 수 있다.
- [ ] `implementation_review`가 장문 review report 생성 시 `write_phased`를 nested 호출할 수 있다.
- [ ] `spec_review`가 장문 spec audit report 생성 시 `write_phased`를 nested 호출할 수 있다.
- [ ] nested 호출에 필요한 설정(`agents.max_depth`)이 pre-flight에서 검증된다.

**Technical Notes**:
- `feature_draft -> write_phased` direct integration은 더 이상 후속 논의 항목이 아니라 이번 범위의 포함 대상이다.
- `implementation`, `spec-update-*`는 1차 범위에서 제외하고 후속 최적화 후보로 남긴다.

**Dependencies**:
- `.codex/agents/write-phased.toml`
- `.codex/config.toml`

---

## Improvements

### Improvement: Platform Differences를 실행 모델 기준으로 재정렬
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Platform Differences`
**Current State**:
현재 스펙은 Codex를 "orchestration-compatible skill surface"로 설명하지만, 실제 실행 backbone(custom agents) 유무와 spawn 방식은 구체적으로 드러나지 않는다.
**Proposed**:
Claude는 `.claude/agents/*.md`, Codex는 `.codex/agents/*.toml`을 사용하는 식으로 플랫폼별 agent 레이어를 명시하고, 두 플랫폼 모두 wrapper + orchestrator + nested write-phased를 지원한다고 설명한다.
**Reason**:
지원 여부가 아니라 실행 모델 차이로 설명해야 사용자와 유지보수자 모두 구조를 정확히 이해할 수 있다.

### Improvement: AUTOPILOT_GUIDE와 예시 orchestrator를 spawn 모델로 갱신
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `사용 가이드 & 기대 결과 (§5)`
**Current State**:
현재 Codex autopilot 가이드는 orchestration contract와 artifact lifecycle은 설명하지만, generated orchestrator가 실제로 무엇을 spawn하는지는 약하다.
**Proposed**:
sample orchestrator, guide 예시, resume 설명을 custom agent spawn 기반으로 바꾼다.
**Reason**:
사용자-facing 가이드가 실제 실행 모델과 다르면 dry-run이나 디버깅이 어려워진다.

### Improvement: 검증 시나리오를 wrapper/agent/nested write-phased 기준으로 추가
**Priority**: Medium
**Target Section**: `_sdd/spec/main.md` > `Testing`
**Current State**:
현재 Codex 쪽 변경은 문서 정렬 중심으로 진행되어 wrapper -> agent, direct agent, nested write-phased, autopilot E2E 검증 계약이 비어 있다.
**Proposed**:
수동 검증 시나리오를 추가한다.
- wrapper -> agent 위임
- agent 직접 실행
- nested write-phased 호출
- autopilot small/medium dry-run
**Reason**:
이번 작업은 구조 변경이라서, 문서 정합성만으로는 충분하지 않다.

---

## Component Changes

### New Component: Codex custom agent layer
**Target Section**: `_sdd/spec/main.md` > `Architecture Overview`, `Component Details`
**Purpose**: wrapper skill 아래에서 spawn 가능한 Codex 실행 backbone 제공
**Input**: 사용자 요청, `_sdd/` artifacts, 대응 skill workflow
**Output**: 각 역할별 산출물과 로그
**Planned Methods**:
- `feature_draft`
- `implementation_plan`
- `implementation`
- `implementation_review`
- `spec_update_todo`
- `spec_update_done`
- `spec_review`
- `ralph_loop_init`
- `write_phased`

### Update Component: sdd-autopilot
**Target Section**: `_sdd/spec/main.md` > `Component Details > sdd-autopilot`
**Purpose**: generated orchestrator를 통해 Codex custom agents를 spawn하는 메타스킬로 정렬
**Input**: 사용자 요청, `_sdd/env.md`, `.codex/config.toml`, 기존 pipeline artifacts
**Output**: active orchestrator, pipeline log, archived orchestrator
**Planned Methods**:
- pre-flight check
- pipeline state detection
- scale assessment
- orchestrator generation
- approval checkpoint
- agent-spawn execution

### Update Component: write-phased
**Target Section**: `_sdd/spec/main.md` > `Component Details > write-phased`
**Purpose**: direct skill + nested custom agent 양쪽에서 사용하는 long-form writing engine
**Input**: target output format, context bundle, artifact paths
**Output**: skeleton -> filled final document/code
**Planned Methods**:
- skeleton generation
- section-wise fill
- marker cleanup

### Update Component: Codex wrapper skills
**Target Section**: `_sdd/spec/main.md` > `Component Details`
**Purpose**: 사용자 직접 호출 인터페이스 유지 + custom agent handoff
**Input**: 사용자 원문 요청, 지정된 artifact 경로
**Output**: 대응 agent 산출물과 next-step 안내
**Planned Methods**:
- agent handoff
- standalone/direct mode
- orchestrated mode

---

## Configuration Changes

### New Config: `.codex/config.toml`
**Target Section**: `_sdd/spec/main.md` > `Configuration`
**Type**: Config File
**Required**: Yes
**Default**:
```toml
[agents]
max_threads = 6
max_depth = 2
```
**Description**:
Codex custom agent spawn 정책을 프로젝트 단위로 정의한다. `max_depth = 2`는 `autopilot -> custom agent -> write_phased` 중첩을 허용하기 위한 최소 기준이다.

---

## Usage Scenarios

### Scenario: direct feature-draft wrapper execution on Codex
**Target Section**: `_sdd/spec/main.md` > `사용 가이드 & 기대 결과 (§5)`

**Setup**:
- `.codex/agents/feature-draft.toml`이 존재한다.
- `.codex/skills/feature-draft/SKILL.md`가 wrapper 역할을 수행한다.

**Action**:
사용자가 `$feature-draft`를 직접 호출한다.

**Expected Result**:
- wrapper skill이 `feature_draft` custom agent를 실행한다.
- agent가 draft 파일을 생성한다.
- 장문 draft가 필요하면 `write_phased`를 nested spawn한다.

### Scenario: Codex autopilot medium pipeline
**Target Section**: `_sdd/spec/main.md` > `사용 가이드 & 기대 결과 (§5)`

**Setup**:
- `.codex/config.toml`에 agent 설정이 존재한다.
- `.codex/agents/`에 medium pipeline에 필요한 agent가 존재한다.
- `_sdd/env.md`가 최신이다.

**Action**:
사용자가 `$sdd-autopilot "JWT 기반 인증 기능을 구현해줘"`를 호출한다.

**Expected Result**:
- Phase 1에서 pre-flight, artifact scan, scale assessment, approval이 수행된다.
- generated orchestrator가 `feature_draft -> implementation_plan -> implementation -> implementation_review -> spec_update_done` agent를 spawn한다.
- 장문 draft/plan/review는 필요 시 `write_phased` nested 호출로 생성된다.
- 실행 로그와 active/archived orchestrator가 규약대로 기록된다.

---

## Notes

### Context
- 기존 `feature_draft_codex_autopilot_orchestration.md`는 문서/계약/가이드 정렬에 초점을 둔 1차 draft였다.
- 이번 draft는 그 위에 실제 실행 backbone(custom agents)과 nested write-phased parity를 추가하는 2차 draft다.
- discussion 결과, 구현은 "한 번에 전부"보다 "agent backbone 우선"이 더 안전하다는 합의가 있었지만, 요구사항 명세에는 최종 목표 구조를 명시한다.

### Constraints
- 새 business/domain agent role은 추가하지 않는다.
- discussion은 full interactive skill로 유지한다.
- 이 저장소는 전통적 테스트 프레임워크가 없으므로 manual dry-run/validation 시나리오가 중요하다.
- project config를 repo에 포함할지 여부는 사용성에 직접 영향이 있으므로 명시적 설계가 필요하다.

<!-- spec-update-todo-input-end -->

---

# Part 2: Implementation Plan

## Overview
Codex autopilot이 실제로 동작할 수 있도록 `.codex/agents/` custom agent backbone을 도입하고, 핵심 pipeline skills를 wrapper로 재정렬하며, generated orchestrator가 custom agents를 spawn하도록 바꾼다. 동시에 장문 산출물이 핵심인 4개 agent에 `write_phased` nested usage를 포팅하고, pre-flight/config 검증 및 문서 정합성까지 함께 마무리한다.

## Scope

### In Scope
- `.codex/agents/` custom agent layer 추가
- 8개 핵심 pipeline unit + `write_phased` custom agent 정의
- Codex wrapper skill 전환
- `sdd-autopilot` 및 generated orchestrator의 custom agent spawn 모델 전환
- `feature_draft`, `implementation_plan`, `implementation_review`, `spec_review`의 nested `write_phased` 포팅
- `.codex/config.toml` 기반 agent config 도입
- pre-flight/resource-gap 검증
- spec/docs/guide 업데이트
- manual validation 시나리오 추가

### Out of Scope
- 새로운 business/domain agent 역할 추가
- `implementation`, `spec_update_done`, `spec_update_todo`의 1차 nested `write_phased` 연동
- 완전 자동화된 테스트 프레임워크 구축
- Claude 쪽 구조 대수선

## Components
1. **Codex Agent Layer**: `.codex/agents/*.toml` custom agents
2. **Codex Wrapper Skills**: 기존 `.codex/skills/*/SKILL.md`
3. **Codex Autopilot**: generated orchestrator + pipeline log + archive
4. **Long-form Writing Engine**: `write_phased`
5. **Platform Docs/Spec**: `_sdd/spec/main.md`, docs, decision log

## Implementation Phases

### Phase 1: Agent Backbone Foundation
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 1 | Add project agent config | P0 | - | Codex Agent Layer |
| 2 | Create planning custom agents | P0 | 1 | Codex Agent Layer |
| 3 | Create execution/review custom agents | P0 | 1 | Codex Agent Layer |
| 4 | Create spec sync/review custom agents | P0 | 1 | Codex Agent Layer |
| 5 | Create utility custom agents | P1 | 1 | Codex Agent Layer |

### Phase 2: Wrapper Parity
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 6 | Convert planning wrapper skills | P0 | 2 | Codex Wrapper Skills |
| 7 | Convert implementation wrapper skills | P0 | 3 | Codex Wrapper Skills |
| 8 | Convert spec wrapper skills | P0 | 4 | Codex Wrapper Skills |
| 9 | Convert utility wrapper skills | P1 | 5 | Codex Wrapper Skills |

### Phase 3: Autopilot Spawn Model
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 10 | Update sdd-autopilot to spawn custom agents | P0 | 2,3,4,5 | Codex Autopilot |
| 11 | Update generated orchestrator templates/examples | P0 | 10 | Codex Autopilot |
| 12 | Add pre-flight config and resource-gap checks | P0 | 1,10 | Codex Autopilot |

### Phase 4: write-phased Nested Parity
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 13 | Port nested write-phased to feature-draft | P1 | 2,5 | Long-form Writing Engine |
| 14 | Port nested write-phased to implementation-plan | P1 | 2,5 | Long-form Writing Engine |
| 15 | Port nested write-phased to implementation-review | P1 | 3,5 | Long-form Writing Engine |
| 16 | Port nested write-phased to spec-review | P1 | 4,5 | Long-form Writing Engine |

### Phase 5: Docs and Validation
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 17 | Update spec and guides for explicit custom agent model | P0 | 10,11,12 | Platform Docs/Spec |
| 18 | Add wrapper -> agent and nested write-phased validation guide | P1 | 6,7,8,9,13,14,15,16 | Platform Docs/Spec |
| 19 | Run Codex dry-run validation and capture results | P1 | 17,18 | Platform Docs/Spec |

## Task Details

### Task 1: Add project agent config
**Component**: Codex Agent Layer
**Priority**: P0-Critical
**Type**: Infrastructure

**Description**:
프로젝트 루트에 `.codex/config.toml`을 추가하여 Codex custom agent 실행에 필요한 기본 설정을 정의한다. 최소한 `agents.max_threads`, `agents.max_depth`를 포함한다.

**Acceptance Criteria**:
- [ ] `.codex/config.toml`이 생성된다.
- [ ] `[agents]` 섹션이 포함된다.
- [ ] `max_depth = 2` 이상으로 nested `write_phased` 호출을 허용한다.
- [ ] 설정값 선택 근거가 문서화된다.

**Target Files**:
- [C] `.codex/config.toml` -- Codex custom agent 실행 설정
- [M] `_sdd/spec/main.md` -- Configuration / Platform Differences 반영

**Technical Notes**:
- 이 저장소는 문서 중심 저장소이므로 과도한 thread 수보다 예측 가능한 depth 보장이 더 중요하다.
- `_sdd/env.md`와 함께 pre-flight 입력으로 사용된다.

**Dependencies**: -

### Task 2: Create planning custom agents
**Component**: Codex Agent Layer
**Priority**: P0-Critical
**Type**: Infrastructure

**Description**:
planning 계열 custom agents를 생성한다. `feature_draft`, `implementation_plan`이 대상이다.

**Acceptance Criteria**:
- [ ] `.codex/agents/feature-draft.toml`이 생성된다.
- [ ] `.codex/agents/implementation-plan.toml`이 생성된다.
- [ ] 두 agent 모두 대응 skill workflow를 source-of-truth로 참조한다.
- [ ] non-interactive/autonomous 동작 원칙이 명시된다.

**Target Files**:
- [C] `.codex/agents/feature-draft.toml` -- feature_draft custom agent 정의
- [C] `.codex/agents/implementation-plan.toml` -- implementation_plan custom agent 정의
- [C] `.codex/agents/README.md` -- agent naming / conventions / usage 안내

**Technical Notes**:
- developer_instructions는 대응 `.codex/skills/*/SKILL.md`와 references를 읽도록 유도할 수 있다.
- naming은 spawn 안정성을 위해 underscore 또는 hyphen 중 하나로 통일해야 한다.

**Dependencies**: 1

### Task 3: Create execution/review custom agents
**Component**: Codex Agent Layer
**Priority**: P0-Critical
**Type**: Infrastructure

**Description**:
`implementation`, `implementation_review` custom agents를 생성한다.

**Acceptance Criteria**:
- [ ] `.codex/agents/implementation.toml`이 생성된다.
- [ ] `.codex/agents/implementation-review.toml`이 생성된다.
- [ ] review-fix loop에서 재호출 가능한 실행 계약이 명시된다.

**Target Files**:
- [C] `.codex/agents/implementation.toml` -- implementation custom agent 정의
- [C] `.codex/agents/implementation-review.toml` -- implementation_review custom agent 정의

**Technical Notes**:
- implementation은 long-form writing보다 코드 수정/검증이 중심이다.
- implementation_review는 이후 nested `write_phased` 대상이다.

**Dependencies**: 1

### Task 4: Create spec sync/review custom agents
**Component**: Codex Agent Layer
**Priority**: P0-Critical
**Type**: Infrastructure

**Description**:
`spec_update_todo`, `spec_update_done`, `spec_review` custom agents를 생성한다.

**Acceptance Criteria**:
- [ ] 세 agent TOML 파일이 생성된다.
- [ ] spec 수정 가능 agent와 read-only review agent의 차이가 명시된다.
- [ ] `spec_review`는 nested `write_phased` 대상임이 명시된다.

**Target Files**:
- [C] `.codex/agents/spec-update-todo.toml` -- spec_update_todo custom agent 정의
- [C] `.codex/agents/spec-update-done.toml` -- spec_update_done custom agent 정의
- [C] `.codex/agents/spec-review.toml` -- spec_review custom agent 정의

**Technical Notes**:
- spec_review는 read-only, spec_update_*는 write-enabled 경로가 필요하다.

**Dependencies**: 1

### Task 5: Create utility custom agents
**Component**: Codex Agent Layer
**Priority**: P1-High
**Type**: Infrastructure

**Description**:
`ralph_loop_init`, `write_phased` custom agents를 생성한다.

**Acceptance Criteria**:
- [ ] `.codex/agents/ralph-loop-init.toml`이 생성된다.
- [ ] `.codex/agents/write-phased.toml`이 생성된다.
- [ ] `write_phased` agent가 nested 호출 전용/직접 호출 양쪽 설명을 가진다.

**Target Files**:
- [C] `.codex/agents/ralph-loop-init.toml` -- ralph_loop_init custom agent 정의
- [C] `.codex/agents/write-phased.toml` -- write_phased custom agent 정의

**Technical Notes**:
- write_phased는 Phase 4의 nested parity 작업 전제다.

**Dependencies**: 1

### Task 6: Convert planning wrapper skills
**Component**: Codex Wrapper Skills
**Priority**: P0-Critical
**Type**: Feature

**Description**:
`feature-draft`, `implementation-plan` skill을 wrapper 중심 구조로 정리한다. 사용자 직접 호출 시 대응 custom agent로 handoff하는 경로를 설명하고, orchestrated mode를 명시한다.

**Acceptance Criteria**:
- [ ] 두 skill의 Workflow Position/Overview/Orchestration Mode가 wrapper 관점으로 일관되게 갱신된다.
- [ ] direct use와 orchestrated use가 모두 설명된다.
- [ ] write-phased nested 계획과 standalone contract가 충돌하지 않는다.

**Target Files**:
- [M] `.codex/skills/feature-draft/SKILL.md` -- wrapper handoff 중심 서술로 조정
- [M] `.codex/skills/feature-draft/skill.json` -- description/metadata 동기화
- [M] `.codex/skills/implementation-plan/SKILL.md` -- wrapper handoff 중심 서술로 조정
- [M] `.codex/skills/implementation-plan/skill.json` -- description/metadata 동기화

**Technical Notes**:
- full workflow reference는 남기되, "누가 실행하는가"를 wrapper 기준으로 다시 써야 한다.

**Dependencies**: 2

### Task 7: Convert implementation wrapper skills
**Component**: Codex Wrapper Skills
**Priority**: P0-Critical
**Type**: Feature

**Description**:
`implementation`, `implementation-review` skill을 wrapper 중심 구조로 정리한다.

**Acceptance Criteria**:
- [ ] `implementation`이 custom agent handoff와 direct wrapper usage를 모두 설명한다.
- [ ] `implementation-review`가 review-fix loop 내 재호출 path를 명시한다.

**Target Files**:
- [M] `.codex/skills/implementation/SKILL.md` -- wrapper handoff 및 spawn model 반영
- [M] `.codex/skills/implementation/skill.json` -- metadata 동기화
- [M] `.codex/skills/implementation-review/SKILL.md` -- review loop wrapper 반영
- [M] `.codex/skills/implementation-review/skill.json` -- metadata 동기화

**Technical Notes**:
- implementation-review는 Phase 4에서 nested write_phased를 사용한다.

**Dependencies**: 3

### Task 8: Convert spec wrapper skills
**Component**: Codex Wrapper Skills
**Priority**: P0-Critical
**Type**: Feature

**Description**:
`spec-update-todo`, `spec-update-done`, `spec-review` wrapper를 정리한다.

**Acceptance Criteria**:
- [ ] 세 skill이 wrapper handoff 기준으로 설명된다.
- [ ] spec_review는 write_phased nested 대상임이 skill 설명과 일치한다.

**Target Files**:
- [M] `.codex/skills/spec-update-todo/SKILL.md` -- wrapper handoff 반영
- [M] `.codex/skills/spec-update-todo/skill.json` -- metadata 동기화
- [M] `.codex/skills/spec-update-done/SKILL.md` -- wrapper handoff 반영
- [M] `.codex/skills/spec-update-done/skill.json` -- metadata 동기화
- [M] `.codex/skills/spec-review/SKILL.md` -- wrapper handoff + nested write plan 반영
- [M] `.codex/skills/spec-review/skill.json` -- metadata 동기화

**Technical Notes**:
- spec-review는 read-only, spec-update-*는 write 경로를 분명히 나눠야 한다.

**Dependencies**: 4

### Task 9: Convert utility wrapper skills
**Component**: Codex Wrapper Skills
**Priority**: P1-High
**Type**: Feature

**Description**:
`ralph-loop-init`, `write-phased` skill 설명을 custom agent 존재를 전제로 재정렬한다.

**Acceptance Criteria**:
- [ ] `write-phased`가 direct skill + nested custom agent 양쪽 역할을 설명한다.
- [ ] `ralph-loop-init`이 standalone + autopilot conditional use를 설명한다.

**Target Files**:
- [M] `.codex/skills/ralph-loop-init/SKILL.md` -- wrapper/direct dual use 반영
- [M] `.codex/skills/ralph-loop-init/skill.json` -- metadata 동기화
- [M] `.codex/skills/write-phased/SKILL.md` -- nested custom agent parity 반영
- [M] `.codex/skills/write-phased/skill.json` -- metadata 동기화

**Technical Notes**:
- write-phased는 user-facing skill이기도 하므로 wrapper-only로 과도하게 축소하지 않는다.

**Dependencies**: 5

### Task 10: Update sdd-autopilot to spawn custom agents
**Component**: Codex Autopilot
**Priority**: P0-Critical
**Type**: Feature

**Description**:
`sdd-autopilot`을 "execution unit 재사용" 추상 표현에서 벗어나, generated orchestrator가 `.codex/agents/*.toml` custom agent를 spawn하는 실행 모델로 고친다.

**Acceptance Criteria**:
- [ ] `sdd-autopilot` skill 본문이 custom agent spawn 모델을 명시한다.
- [ ] Step 5/Step 7가 agent name 중심으로 다시 작성된다.
- [ ] review-fix 루프가 `implementation_review`/`implementation` 재호출 기준으로 정리된다.

**Target Files**:
- [M] `.codex/skills/sdd-autopilot/SKILL.md` -- agent spawn 중심 실행 모델 반영
- [M] `.codex/skills/sdd-autopilot/skill.json` -- description 동기화

**Technical Notes**:
- "skill을 subagent처럼 쓴다"는 표현은 제거해야 한다.

**Dependencies**: 2,3,4,5

### Task 11: Update generated orchestrator templates/examples
**Component**: Codex Autopilot
**Priority**: P0-Critical
**Type**: Feature

**Description**:
pipeline templates와 sample orchestrator를 custom agent spawn 기준으로 고친다.

**Acceptance Criteria**:
- [ ] sample orchestrator가 skill 이름이 아니라 custom agent 이름을 사용한다.
- [ ] small/medium/large template이 spawn 대상과 artifact handoff를 명시한다.
- [ ] write_phased nested 사용 지점이 템플릿에 반영된다.

**Target Files**:
- [M] `.codex/skills/sdd-autopilot/references/pipeline-templates.md` -- custom agent spawn 템플릿
- [M] `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md` -- explicit agent names 반영

**Technical Notes**:
- sample은 medium pipeline 기준이 가장 설명력이 높다.

**Dependencies**: 10

### Task 12: Add pre-flight config and resource-gap checks
**Component**: Codex Autopilot
**Priority**: P0-Critical
**Type**: Infrastructure

**Description**:
`_sdd/env.md`와 `.codex/config.toml`을 함께 읽는 pre-flight check를 추가한다.

**Acceptance Criteria**:
- [ ] 외부 서비스/환경 변수/테스트/빌드 요구 확인이 포함된다.
- [ ] `agents.max_depth`, `agents.max_threads` 확인이 포함된다.
- [ ] 부족한 설정이 있으면 approval 전에 사용자에게 리스크로 보고한다.

**Target Files**:
- [M] `.codex/skills/sdd-autopilot/SKILL.md` -- pre-flight logic 추가
- [M] `.codex/skills/sdd-autopilot/references/scale-assessment.md` -- resource-aware guidance 보강
- [M] `docs/AUTOPILOT_GUIDE.md` -- pre-flight 설명 보강

**Technical Notes**:
- 이 저장소에서는 외부 서비스보다 nested depth와 manual validation 준비가 핵심 resource다.

**Dependencies**: 1,10

### Task 13: Port nested write-phased to feature-draft
**Component**: Long-form Writing Engine
**Priority**: P1-High
**Type**: Feature

**Description**:
`feature_draft` agent가 최종 draft 문서 생성 시 `write_phased`를 nested spawn하도록 포팅한다.

**Acceptance Criteria**:
- [ ] feature_draft output generation 단계에서 write_phased 사용 규칙이 명시된다.
- [ ] Part 1 + Part 2 전체 format이 nested handoff에 포함된다.

**Target Files**:
- [M] `.codex/agents/feature-draft.toml` -- nested write_phased usage 규칙 추가
- [M] `.codex/skills/feature-draft/SKILL.md` -- direct integration 보류 문구 제거 및 nested parity 반영

**Technical Notes**:
- 이전 draft의 보류 결정과 충돌하므로 superseding note가 필요하다.

**Dependencies**: 2,5

### Task 14: Port nested write-phased to implementation-plan
**Component**: Long-form Writing Engine
**Priority**: P1-High
**Type**: Feature

**Description**:
`implementation_plan` agent가 장문 plan을 `write_phased`로 작성하도록 포팅한다.

**Acceptance Criteria**:
- [ ] 계획 문서 skeleton -> fill 전략이 agent 지침에 포함된다.
- [ ] wrapper skill과 충돌하지 않는다.

**Target Files**:
- [M] `.codex/agents/implementation-plan.toml` -- nested write_phased usage 규칙 추가
- [M] `.codex/skills/implementation-plan/SKILL.md` -- long-form nested parity 반영

**Technical Notes**:
- Phase/Task detail 구조를 한 번에 넘길 수 있도록 output schema 전달 방식이 필요하다.

**Dependencies**: 2,5

### Task 15: Port nested write-phased to implementation-review
**Component**: Long-form Writing Engine
**Priority**: P1-High
**Type**: Feature

**Description**:
`implementation_review` agent가 장문 review report 생성 시 `write_phased`를 nested spawn하도록 포팅한다.

**Acceptance Criteria**:
- [ ] review mode/tier 정보가 nested handoff에 포함된다.
- [ ] findings-first 보고 방식이 유지된다.

**Target Files**:
- [M] `.codex/agents/implementation-review.toml` -- nested write_phased usage 규칙 추가
- [M] `.codex/skills/implementation-review/SKILL.md` -- nested parity 반영

**Technical Notes**:
- review 품질을 위해 writer agent에는 findings structure를 그대로 전달해야 한다.

**Dependencies**: 3,5

### Task 16: Port nested write-phased to spec-review
**Component**: Long-form Writing Engine
**Priority**: P1-High
**Type**: Feature

**Description**:
`spec_review` agent가 spec audit report 생성 시 `write_phased`를 nested spawn하도록 포팅한다.

**Acceptance Criteria**:
- [ ] read-only review contract와 nested writing contract가 함께 유지된다.
- [ ] report output structure가 nested handoff에 반영된다.

**Target Files**:
- [M] `.codex/agents/spec-review.toml` -- nested write_phased usage 규칙 추가
- [M] `.codex/skills/spec-review/SKILL.md` -- nested parity 반영

**Technical Notes**:
- report generation은 long-form benefit이 크지만 read-only constraint를 깨면 안 된다.

**Dependencies**: 4,5

### Task 17: Update spec and guides for explicit custom agent model
**Component**: Platform Docs/Spec
**Priority**: P0-Critical
**Type**: Documentation

**Description**:
메인 스펙과 가이드를 explicit custom agent model 기준으로 업데이트한다.

**Acceptance Criteria**:
- [ ] `_sdd/spec/main.md`가 `.codex/agents/` 레이어를 명시한다.
- [ ] Platform Differences가 wrapper + custom agent + nested write_phased 기준으로 설명된다.
- [ ] AUTOPILOT_GUIDE, QUICK_START, WORKFLOW가 새 실행 모델과 일치한다.

**Target Files**:
- [M] `_sdd/spec/main.md` -- custom agent model 반영
- [M] `_sdd/spec/DECISION_LOG.md` -- 새 결정 기록
- [M] `docs/AUTOPILOT_GUIDE.md` -- explicit custom agent spawn 설명
- [M] `docs/SDD_QUICK_START.md` -- 실행 모델 요약 갱신
- [M] `docs/SDD_WORKFLOW.md` -- workflow 설명 갱신

**Technical Notes**:
- 기존 "orchestration-compatible skill surface" 문구는 새 실행 backbone 설명으로 대체해야 한다.

**Dependencies**: 10,11,12

### Task 18: Add wrapper -> agent and nested write-phased validation guide
**Component**: Platform Docs/Spec
**Priority**: P1-High
**Type**: Test

**Description**:
manual validation 시나리오를 문서화한다.

**Acceptance Criteria**:
- [ ] wrapper -> agent smoke test가 정의된다.
- [ ] direct agent execution 확인 절차가 정의된다.
- [ ] nested write_phased 확인 절차가 정의된다.
- [ ] autopilot small/medium dry-run 체크리스트가 정의된다.

**Target Files**:
- [C] `docs/AUTOPILOT_GUIDE.md` -- Codex agent validation 가이드
- [M] `docs/AUTOPILOT_GUIDE.md` -- validation link 추가

**Technical Notes**:
- 이 저장소는 전통적 테스트 대신 실행 체크리스트가 중요하다.

**Dependencies**: 6,7,8,9,13,14,15,16

### Task 19: Run Codex dry-run validation and capture results
**Component**: Platform Docs/Spec
**Priority**: P1-High
**Type**: Test

**Description**:
small/medium 시나리오로 Codex dry-run validation을 수행하고 결과를 기록한다.

**Acceptance Criteria**:
- [ ] wrapper -> agent 동작이 검증된다.
- [ ] nested write_phased가 최소 1회 검증된다.
- [ ] autopilot medium 시나리오가 end-to-end로 검증된다.
- [ ] 검증 결과와 남은 리스크가 기록된다.

**Target Files**:
- [C] `_sdd/pipeline/log_codex_agent_parity_validation_<timestamp>.md` -- 검증 로그
- [M] `_sdd/spec/DECISION_LOG.md` -- validation 결과 요약

**Technical Notes**:
- safe, doc-focused scenario를 택해 실제 코드 리스크를 최소화한다.

**Dependencies**: 17,18

## Parallel Execution Summary
| Phase | Total Tasks | Max Parallel | Sequential (conflicts) |
|-------|-------------|--------------|------------------------|
| 1 | 5 | 4 | 1 |
| 2 | 4 | 4 | 0 |
| 3 | 3 | 1 | 2 |
| 4 | 4 | 4 | 0 |
| 5 | 3 | 1 | 2 |

> `Max Parallel`은 file overlap과 dependency를 모두 고려한 값이다. Phase 3과 Phase 5는 autopilot/docs 중심이라 순차성이 높다.

## Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| `.codex/agents/` custom agent 지침이 너무 얇아 기존 skill 품질이 떨어짐 | wrapper parity만 생기고 실제 결과 품질 저하 | agent instructions가 대응 skill workflow를 source-of-truth로 읽도록 설계 |
| `max_depth` 부족으로 nested `write_phased` 실패 | 장문 산출물 생성 중단 | `.codex/config.toml` 도입 + pre-flight에서 depth 확인 |
| wrapper/agent 역할 경계가 불분명 | direct use와 orchestrated use가 뒤섞임 | wrapper는 user entry, agent는 execution backbone으로 문구 통일 |
| generated orchestrator가 skill 이름과 agent 이름을 혼동 | 실행 실패 또는 잘못된 문서 생성 | sample orchestrator와 template에서 agent naming을 명시적 규약으로 고정 |
| 이전 Codex draft와 요구사항 충돌 | 문서 드리프트 심화 | superseding decision을 DECISION_LOG와 spec patch에 함께 기록 |

## Open Questions
- [ ] `.codex/agents/*.toml`의 `name` 필드는 hyphen과 underscore 중 무엇으로 통일할 것인가?
- [ ] `.codex/config.toml`을 repo-tracked 기본값으로 둘지, 예시 파일로 둘지 확정이 필요한가?
- [ ] wrapper skill이 직접 spawn 지침만 둘지, 일부 full workflow 설명을 유지할지 기준을 얼마나 엄격하게 정할 것인가?

## Model Recommendation
이 작업은 다수의 SKILL/agent/config/spec/doc 파일을 동시에 건드리는 구조 변경이다. 구현은 `gpt-5.4` 또는 `gpt-5.3-codex`급 모델로 진행하는 것이 적절하다. wrapper/agent 반복 작업은 중간 reasoning, autopilot/orchestrator/spec sync는 높은 reasoning이 권장된다.
