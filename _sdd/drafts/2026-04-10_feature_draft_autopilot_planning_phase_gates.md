# Feature Draft: Autopilot Planning Orchestration + Phase-Gated Review-Fix

**Date**: 2026-04-10
**Status**: Draft
**Source Discussions**:
- `_sdd/discussion/discussion_autopilot_phase_review_fix_loop.md`
- `_sdd/discussion/discussion_autopilot_planning_skill_orchestration.md`
**Change Type**: Improvement / Refactor

<!-- spec-update-todo-input-start -->
# Part 1: Temporary Spec Draft

## Change Summary

`sdd-autopilot`의 planning 계열 스킬 관계와 multi-phase 구현의 review-fix 실행 규칙을 함께 정리한다. 핵심 변경은 두 가지다. 첫째, non-trivial change에서 planning 진입점은 기본적으로 `feature-draft`이며, `implementation-plan`은 이를 대체하는 선택지가 아니라 `feature-draft` 이후의 상세 확장 단계로 표현한다. 둘째, medium 이상에서 `implementation-plan`이 multi-phase 구조를 만들면 autopilot은 그 phase를 실제 execution gate로 소비하여 `implementation -> review -> fix -> phase validation`을 반복하고, 마지막에 `final integration review`를 반드시 한 번 더 수행한다.

이 변경은 runtime 코드를 새로 추가하는 작업이 아니라, `.claude/` / `.codex/` skill 문서, reference contract, sample orchestrator, user guide가 같은 오케스트레이션 의미를 공유하도록 정리하는 문서 계약 변경이다.

## Scope Delta

### In Scope

- `sdd-autopilot` skill 본문에서 planning depth를 정리하고, 오케스트레이터 contract 보강에 맞춰 Step 7 executor binding을 정렬한다.
- `references/sdd-reasoning-reference.md`에서 `feature-draft`, `spec-update-todo`, `implementation-plan`의 선후관계와 standalone 예외 조건을 명시한다.
- `references/orchestrator-contract.md`에 per-phase review-fix 실행용 필드와 규칙을 추가한다.
- `implementation-plan` skill/agent 계약에 phase goal, validation focus, exit criteria, carry-over policy 등 phase gate 소비용 메타데이터를 추가한다.
- sample orchestrator와 `docs/AUTOPILOT_GUIDE.md` / `docs/en/AUTOPILOT_GUIDE.md`를 새 의미에 맞게 갱신한다.
- Claude/Codex mirror surface 간 의미적 parity를 유지한다.

### Out of Scope

- 새로운 agent type 추가
- `implementation`, `implementation-review` 자체의 상세 실행 로직 재설계
- `_sdd/spec/*.md` 직접 수정
- `docs/SDD_WORKFLOW.md`와 `_sdd/spec/usage-guide.md`의 즉시 동기화

### Guardrails

- small/medium 경로는 과도하게 무겁게 만들지 않는다.
- `implementation-plan`은 기본적으로 `feature-draft` 이후의 확장 단계로만 설명한다.
- `spec-update-todo`는 complex planned global alignment가 필요한 경우에만 붙인다.
- per-phase review-fix는 multi-phase plan이 생성된 large/complex 경로의 기본값이며, medium 규모라도 multi-phase plan이면 기본값으로 승격한다. 마지막 `final integration review`는 항상 남긴다.
- medium 이슈는 기본적으로 phase exit를 막고, 명시적 carry-over policy가 있을 때만 예외를 허용한다.
- Claude/Codex와 ko/en guide는 같은 contract vocabulary를 사용한다.

## Contract/Invariant Delta

| ID | Type | Change | Why |
|----|------|--------|-----|
| C1 | Modify | `sdd-autopilot`의 non-trivial planning entry는 기본적으로 `feature-draft`이며, `implementation-plan`은 `feature-draft` Part 2가 부족하거나 large/complex 분해가 필요한 경우의 후속 확장 단계로 설명한다. `spec-update-todo`는 conditional planned-global alignment step으로 유지한다. | planning 스킬을 peer alternative처럼 읽는 오해를 줄인다. |
| C2 | Add | `implementation-plan`이 multi-phase면 large/complex 경로에서는 물론, medium 규모라도 `Review-Fix Loop.scope = per-phase`를 기본값으로 적용하고, 현재 phase exit criteria를 충족하기 전에는 다음 phase로 넘어갈 수 없게 한다. 마지막에는 `final integration review`를 반드시 1회 수행한다. | phase 구조를 실제 execution control로 연결하고 결함 전파를 줄인다. |
| C3 | Add | `implementation-plan`은 autopilot이 소비할 수 있도록 phase별 `goal`, `task set / dependency closure`, `validation focus`, `exit criteria`, `carry-over policy`를 stable한 문서 구조로 제공해야 한다. | per-phase review gate를 실행하려면 producer-side phase metadata가 필요하다. |
| I1 | Add | small path와 single-phase medium path, 또는 `feature-draft` Part 2만으로 충분한 direct path는 기존 global review-fix loop를 유지할 수 있다. 반대로 medium 이상에서 multi-phase plan이 나오면 per-phase gating을 기본값으로 본다. | 단순 경로의 비용 증가를 막으면서 multi-phase 계획의 실행 제어를 강화한다. |
| I2 | Add | `medium` 이슈는 기본적으로 phase exit를 막는다. carry-over는 phase 문서와 로그에 명시된 정책과 근거가 있을 때만 허용한다. | 안전성을 기본값으로 두고 예외를 통제한다. |
| I3 | Add | `.claude/`, `.codex/`, `docs/AUTOPILOT_GUIDE.md`, `docs/en/AUTOPILOT_GUIDE.md`는 planning precedence와 phase-gate semantics를 같은 용어로 설명해야 한다. | contract drift를 막고 플랫폼별 오해를 줄인다. |

## Touchpoints

| Area | Why It Changes |
|------|----------------|
| `.codex/skills/sdd-autopilot/SKILL.md` | Step 4의 planning depth 표현과, 보강된 오케스트레이터 contract를 Step 7이 어떻게 집행하는지 정렬해야 한다. |
| `.claude/skills/sdd-autopilot/SKILL.md` | Claude runtime도 같은 planning precedence와 phase gate semantics를 가져야 한다. |
| `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md` | planning 계열 스킬의 선후관계와 standalone 예외를 reasoning reference에 고정해야 한다. |
| `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md` | Claude 측 reference parity를 유지해야 한다. |
| `.codex/skills/sdd-autopilot/references/orchestrator-contract.md` | `Review-Fix Contract`와 `implementation-plan` precondition/phase metadata contract를 추가해야 한다. |
| `.claude/skills/sdd-autopilot/references/orchestrator-contract.md` | Claude 측 orchestrator contract도 같은 필드를 가져야 한다. |
| `.codex/skills/implementation-plan/SKILL.md`, `.codex/agents/implementation-plan.toml` | producer contract에 phase goal, validation focus, exit criteria, carry-over policy를 반영해야 한다. |
| `.claude/skills/implementation-plan/SKILL.md`, `.claude/agents/implementation-plan.md` | Claude implementation-plan surface도 autopilot consumer contract와 맞춰야 한다. |
| `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md`, `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md` | single-phase medium direct path와 multi-phase medium/large path를 예시로 보여줘야 한다. |
| `docs/AUTOPILOT_GUIDE.md`, `docs/en/AUTOPILOT_GUIDE.md` | 사용자-facing 설명이 기존 peer-choice wording과 single review loop 설명에 머물지 않도록 갱신해야 한다. |

## Implementation Plan

1. autopilot core surface에서 planning precedence와 phase-gated review-fix vocabulary를 먼저 확정한다.
2. orchestrator contract와 implementation-plan producer contract를 같은 필드 이름으로 정렬한다.
3. sample orchestrator와 user guide를 새 contract에 맞게 갱신한다.
4. Claude/Codex, ko/en surface에 stale wording이 남지 않았는지 parity review로 닫는다.

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, I1 | review, grep | `sdd-autopilot` Step 4와 reasoning reference, guide scale table에서 `feature-draft`가 기본 planning entry로 표현되고 `implementation-plan`이 확장 단계로 설명되는지 확인한다. |
| V2 | C2, I2 | review walkthrough | orchestrator contract, autopilot Step 7, sample multi-phase example을 함께 읽어 `scope`, phase boundary, exit criteria, carry-over policy, `final integration review`가 연결되는지 확인한다. |
| V3 | C3, I2 | review | `implementation-plan` skill/agent 템플릿에 phase goal, validation focus, exit criteria, carry-over policy, dependency closure가 드러나는지 확인한다. |
| V4 | C1, C2, C3, I1, I2, I3 | parity review | Claude/Codex, ko/en surface에서 같은 semantics를 유지하고 stale wording이 남지 않았는지 교차 점검한다. |

## Risks / Open Questions

- `_sdd/spec/usage-guide.md`와 `_sdd/spec/components.md`는 이번 구현 범위 밖으로 두는 것이 안전하다. 다만 구현 완료 후 `spec-update-todo` 또는 `spec-update-done`으로 supporting spec sync가 필요할 수 있다.
- medium 규모라도 multi-phase plan이 생성되면 `per-phase` scope를 기본값으로 승격한다는 판단을 이번 draft의 기준으로 채택한다. 구현 시 guide/example wording도 이 기준에 맞춰 통일해야 한다.
- `docs/SDD_WORKFLOW.md`와 `docs/en/SDD_WORKFLOW.md`까지 같은 턴에 갱신할지 여부는 선택 사항이다. 이번 범위에서는 AUTOPILOT guide 우선으로 가정한다.

<!-- spec-update-todo-input-end -->

# Part 2: Implementation Plan

## Overview

이번 구현은 autopilot이 planning 스킬을 잘못 대체 선택지로 읽는 문제와, multi-phase 구현에서 phase 구조가 review gate로 소비되지 않는 문제를 한 번에 정리하는 문서/contract refactor다. 핵심은 `feature-draft -> (optional) spec-update-todo -> (optional) implementation-plan` 관계를 명시하고, medium 이상에서 multi-phase plan이 나오면 실제 `per-phase review-fix + final integration review` 실행 규칙으로 이어지게 만드는 것이다.

## Scope

### In Scope

- `.claude/` / `.codex/` `sdd-autopilot` skill 본문 갱신
- `.claude/` / `.codex/` reasoning reference, orchestrator contract 갱신
- `.claude/` / `.codex/` implementation-plan skill/agent 계약 갱신
- sample orchestrator 갱신
- `docs/AUTOPILOT_GUIDE.md`와 `docs/en/AUTOPILOT_GUIDE.md` 갱신

### Out of Scope

- 새 skill/agent 생성
- `_sdd/spec/*.md` 직접 수정
- implementation runtime의 별도 테스트 harness 추가
- `implementation`, `implementation-review`의 상세 알고리즘 변경

## Components

1. **Autopilot Core Binding**: planning depth 정리와 Step 7 executor binding 정렬
2. **Orchestrator Contract**: `Review-Fix Loop.scope`, phase boundary source, exit criteria, carry-over policy, final integration review
3. **Implementation Plan Producer Contract**: phase goal, validation focus, exit criteria, carry-over policy, dependency closure
4. **Examples and Guides**: sample orchestrator, AUTOPILOT guide ko/en

## Contract/Invariant Delta Coverage

| Target | Planned Tasks | Validation Link |
|--------|---------------|-----------------|
| C1 | T1, T3, T4 | V1, V4 |
| C2 | T1, T2, T3, T4 | V2, V4 |
| C3 | T2 | V3, V4 |
| I1 | T1, T3, T4 | V1, V4 |
| I2 | T1, T2, T3, T4 | V2, V3, V4 |
| I3 | T1, T2, T3, T4 | V4 |

## Implementation Phases

### Phase 1: Planning Semantics Freeze

**Goal**: `feature-draft` 중심 planning precedence를 고정하고, medium 이상 multi-phase plan에 대한 오케스트레이터 contract와 Step 7 executor binding을 먼저 정렬한다.  
**Tasks**: T1  
**Validation Focus**: V1, V2  
**Exit Criteria**:
- autopilot Step 4가 `implementation-plan`을 non-trivial 기본 진입점처럼 설명하지 않는다.
- autopilot Step 7이 오케스트레이터의 per-phase 선언을 어떻게 집행하는지와 final integration review semantics를 설명한다.
- Claude/Codex core surface에서 용어가 일치한다.

### Phase 2: Producer/Consumer Contract Alignment

**Goal**: orchestrator contract와 implementation-plan producer contract가 같은 phase-gate field vocabulary를 사용하도록 정렬한다.  
**Tasks**: T2  
**Validation Focus**: V2, V3  
**Exit Criteria**:
- orchestrator contract에 `scope`, `phase boundary source`, `phase exit criteria`, `carry-over policy`, `final integration review` 규칙이 명시된다.
- implementation-plan docs가 phase goal, validation focus, exit criteria, carry-over policy를 출력 구조에 반영한다.

### Phase 3: Example and Guide Synchronization

**Goal**: example 및 guide surface가 새 contract를 실제 사용 흐름으로 보여주게 만든다.  
**Tasks**: T3, T4  
**Validation Focus**: V1, V2, V4  
**Exit Criteria**:
- sample orchestrator가 single-phase medium direct path와 multi-phase medium/large path를 모두 보여준다.
- ko/en guide에 stale peer-choice 설명과 single global review-only 설명이 남아 있지 않다.

## Task Details

### Task T1: Align autopilot planning precedence and Step 7 executor binding
**Component**: Autopilot Core Binding  
**Priority**: P0  
**Type**: Feature

**Description**: `sdd-autopilot` skill 본문과 reasoning reference를 갱신해 `feature-draft`를 non-trivial planning의 기본 entry로 고정하고, `implementation-plan`을 후속 확장 단계로 재정의한다. 동시에 Step 7 설명은 새 per-phase contract를 오케스트레이터가 선언하고 autopilot이 집행한다는 executor binding을 명확히 드러내도록 정렬한다.

**Acceptance Criteria**:
- [ ] `.claude/skills/sdd-autopilot/SKILL.md`와 `.codex/skills/sdd-autopilot/SKILL.md`의 Step 4가 planning 계열 스킬을 peer alternative처럼 서술하지 않는다.
- [ ] 두 runtime의 Step 7 설명이 `per-phase` scope 선언을 오케스트레이터 기준으로 집행한다는 binding과 final integration review semantics를 반영한다.
- [ ] reasoning reference가 small direct path, single-phase medium path, multi-phase medium/large expanded path를 구분해 설명한다.
- [ ] standalone `implementation-plan` 사용은 예외 조건이 있는 경우로만 설명된다.

**Target Files**:
- [M] `.codex/skills/sdd-autopilot/SKILL.md` -- Step 4 planning 및 Step 7 executor binding 정렬
- [M] `.claude/skills/sdd-autopilot/SKILL.md` -- Claude runtime parity 반영
- [M] `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md` -- planning skill 선후관계와 예외 조건 명시
- [M] `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md` -- Claude reference parity 반영

**Technical Notes**: Covers C1, C2, I1, I2, I3. Validated by V1, V2, V4.
**Dependencies**: None

### Task T2: Extend phase-gate contract and implementation-plan producer metadata
**Component**: Orchestrator Contract + Implementation Plan Producer Contract  
**Priority**: P0  
**Type**: Feature

**Description**: `Review-Fix Contract`에 phase gate 실행 필드를 추가하고, `implementation-plan` skill/agent가 autopilot이 읽을 수 있는 phase metadata를 내보내도록 계약을 보강한다. 이때 `feature-draft` 선행 원칙과 carry-over policy 기본값도 함께 정리한다.

**Acceptance Criteria**:
- [ ] `.claude/` / `.codex/` orchestrator contract에 `scope`, `phase boundary source`, `phase exit criteria`, `carry-over policy`, `final integration review` 관련 규칙이 추가된다.
- [ ] `.claude/` / `.codex/` implementation-plan skill/agent에 phase goal, validation focus, exit criteria, carry-over policy, dependency closure를 반영한 구조가 추가된다.
- [ ] Claude implementation-plan surface도 Codex와 동일하게 `feature-draft` 선행 원칙과 standalone 예외를 설명한다.
- [ ] phase metadata와 `C*` / `I*` / `V*` linkage가 plan output 구조에서 유지된다.

**Target Files**:
- [M] `.codex/skills/sdd-autopilot/references/orchestrator-contract.md` -- per-phase review-fix contract 필드 추가
- [M] `.claude/skills/sdd-autopilot/references/orchestrator-contract.md` -- Claude contract parity 반영
- [M] `.codex/skills/implementation-plan/SKILL.md` -- phase gate metadata와 integration guidance 추가
- [M] `.codex/agents/implementation-plan.toml` -- custom agent mirror 동기화
- [M] `.claude/skills/implementation-plan/SKILL.md` -- Claude skill wording 및 phase metadata 보강
- [M] `.claude/agents/implementation-plan.md` -- Claude agent contract 동기화

**Technical Notes**: Covers C2, C3, I2, I3. Validated by V2, V3, V4.
**Dependencies**: T1

### Task T3: Refresh sample orchestrators for medium and large phase-gated paths
**Component**: Examples  
**Priority**: P1  
**Type**: Refactor

**Description**: sample orchestrator를 갱신해 single-phase medium direct path와 multi-phase medium/large expanded path를 구분해서 보여준다. multi-phase example에는 per-phase review-fix, phase boundary source, exit criteria, carry-over handling, final integration review를 드러낸다.

**Acceptance Criteria**:
- [ ] sample orchestrator에 single-phase medium path와 multi-phase path가 모두 보인다.
- [ ] multi-phase example이 `feature-draft -> (optional) spec-update-todo -> implementation-plan` 이후 phase별 review/fix 흐름을 보여준다.
- [ ] final integration review가 multi-phase example에서 별도 단계 또는 명시 규칙으로 드러난다.
- [ ] Claude/Codex sample wording이 같은 의미를 유지한다.

**Target Files**:
- [M] `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md` -- Codex 예시 오케스트레이터 갱신
- [M] `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md` -- Claude 예시 오케스트레이터 parity 반영

**Technical Notes**: Covers C1, C2, I1, I2, I3. Validated by V1, V2, V4.
**Dependencies**: T1, T2

### Task T4: Sync user-facing autopilot guides with the new orchestration model
**Component**: Guides  
**Priority**: P1  
**Type**: Refactor

**Description**: `docs/AUTOPILOT_GUIDE.md`와 영어 가이드를 갱신해 scale table, pipeline example, review-fix 설명, artifact wording이 새 계약과 일치하도록 맞춘다. 구현자와 사용자가 `implementation-plan`을 기본 peer choice로 오해하지 않도록 guide narrative를 보정하고, medium 규모라도 multi-phase plan이면 per-phase gate가 기본이라는 점을 반영한다.

**Acceptance Criteria**:
- [ ] ko/en guide의 규모별 파이프라인 설명이 `feature-draft` 중심 planning 관계를 반영한다.
- [ ] multi-phase path 설명에 per-phase review-fix와 final integration review가 반영된다.
- [ ] `implementation-plan`과 `spec-update-todo`의 사용 조건이 조건부 확장 단계로 설명된다.
- [ ] 기존 예시 로그/산출물 설명이 새 semantics와 충돌하지 않는다.

**Target Files**:
- [M] `docs/AUTOPILOT_GUIDE.md` -- 한국어 사용자 가이드 갱신
- [M] `docs/en/AUTOPILOT_GUIDE.md` -- 영어 사용자 가이드 parity 반영

**Technical Notes**: Covers C1, C2, I1, I2, I3. Validated by V1, V2, V4.
**Dependencies**: T1, T2

## Parallel Execution Summary

- T1과 T2는 shared vocabulary를 먼저 고정해야 하므로 순차 실행이 안전하다.
- T3와 T4는 T1/T2 이후에는 write set이 겹치지 않으므로 병렬 실행 가능하다.
- Claude/Codex parity가 핵심이므로, 하나의 worker가 같은 concern의 `.claude/` + `.codex/` 쌍을 함께 소유하는 편이 안전하다.

## Risks and Mitigations

- **Risk**: contract field 이름이 T2 중간에 바뀌면 sample/guide surface가 다시 drift할 수 있다.  
  **Mitigation**: T2에서 field vocabulary를 먼저 고정하고 T3/T4를 시작한다.
- **Risk**: Claude implementation-plan surface가 Codex보다 오래된 계약을 유지해 parity가 깨질 수 있다.  
  **Mitigation**: T2에서 skill + agent mirror를 한 번에 묶어 수정한다.
- **Risk**: user guide 수정 범위가 과도하게 커져 요청 범위를 넘어갈 수 있다.  
  **Mitigation**: scale table, pipeline sequence, review-fix semantics, examples 관련 섹션만 최소 수정한다.
- **Risk**: `_sdd/spec` supporting surface는 그대로 남아 문서 간 시차가 생길 수 있다.  
  **Mitigation**: 구현 완료 후 `spec-update-todo` 또는 `spec-update-done` 후속 작업을 명시적으로 남긴다.

## Open Questions

- `docs/SDD_WORKFLOW.md`, `docs/en/SDD_WORKFLOW.md`, `_sdd/spec/usage-guide.md`까지 같은 턴에 맞출지 여부는 별도 sync 작업으로 분리할 수 있다.
