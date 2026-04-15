# Feature Draft: Autopilot Orchestrator Output Boundary + Phase-Iterative Execution Loop

**Date**: 2026-04-15
**Status**: Draft
**Change Type**: Improvement / Refactor
**Source Context**:
- current discussion about `sdd-autopilot` Step 4 output boundary and multi-phase execution semantics
- `_sdd/drafts/2026-04-10_feature_draft_autopilot_planning_phase_gates.md`
- `.codex/skills/sdd-autopilot/SKILL.md`
- `.codex/skills/sdd-autopilot/references/orchestrator-contract.md`

<!-- spec-update-todo-input-start -->
# Part 1: Temporary Spec Draft

## Change Summary

`sdd-autopilot`의 오케스트레이터 생성/실행 경계를 더 엄격하게 정리한다. 이번 변경의 핵심은 세 가지다. 첫째, Step 4 `Reasoning -> Orchestrator Generation`은 오직 `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`만 생성해야 하며, downstream step이 나중에 만들 `_sdd/drafts/*`, `_sdd/implementation/*` artifact를 미리 생성하거나 materialize하면 안 된다. 둘째, 오케스트레이터 내부에 `implementation-plan` step이 포함되는 expanded path에서는 Step 4 시점에 phase 개수와 경계가 아직 확정되지 않으므로, generated orchestrator는 `implementation` step을 flat single-shot step으로 쓰지 않고 `phase-iterative` execution unit으로 선언해야 한다. 셋째, 규모와 무관하게 review가 포함된 모든 path에서는 `implementation`과 `implementation-review`가 항상 sub-agent 실행 단위여야 하며, 부모 autopilot이 로컬 직구현이나 로컬 리뷰로 대체하면 안 된다.

이번 draft의 목적은 현재 `sdd-autopilot`의 전체 pipeline shape나 step skeleton을 재설계하는 것이 아니라, 이미 의도된 실행 구조가 잘못 해석되거나 약하게 집행될 수 있는 지점을 contract hardening과 verification strengthening으로 보강하는 데 있다.

이 선언은 적어도 다음 의미를 가져야 한다. `implementation-plan` output이 phase metadata를 생성하면, 그 이후 `implementation` step은 각 phase마다 `implementation -> implementation-review -> fix(필요 시 implementation 재호출) -> implementation-review -> phase validation`을 반복한다. 마지막 phase 뒤에는 `final integration review`를 반드시 한 번 더 수행한다. small/medium direct path나 single-phase medium path에서도 review가 있으면 같은 sub-agent mapping으로 global review-fix loop를 닫아야 한다. 즉, multi-phase 구조는 문서 장식이 아니라 runtime control flow contract이며, review-fix loop의 실행 주체도 항상 sub-agent다.

## Scope Delta

### In Scope

- `.codex/` / `.claude/` `sdd-autopilot` skill에서 Step 4의 artifact boundary를 명시한다.
- `.codex/` / `.claude/` `sdd-autopilot` skill에서 review가 포함된 모든 규모의 path에 대해 `implementation`과 `implementation-review`가 sub-agent 실행 단위라는 invariant를 명시한다.
- Step 5 verification에서 "Step 4가 orchestrator 외 artifact를 만들지 않았는가"를 검증 대상으로 추가한다.
- Step 7 execution semantics에서 `implementation-plan` 이후 `implementation` step이 `phase-iterative` loop일 수 있음을 명시한다.
- small/medium direct path와 single-phase medium path에서도 review가 있으면 `implementation -> implementation-review -> fix -> implementation-review` loop를 sub-agent로 수행한다는 규칙을 보강한다.
- `references/orchestrator-contract.md`에 `phase-iterative implementation step` 계약을 추가한다.
- sample orchestrator와 ko/en guide에서 expanded path를 `implementation-plan -> phase-iterative implementation loop`로 설명한다.
- sample orchestrator와 ko/en guide에서 small/medium/large 모두 review path는 sub-agent mapping을 고정으로 사용한다고 설명한다.
- Claude/Codex parity를 유지한다.

### Out of Scope

- `sdd-autopilot`의 8-step 구조나 phase 구분 자체를 새 workflow로 재설계하는 일
- `feature-draft -> implementation-plan -> implementation -> spec sync`라는 기본 expanded path 골격을 다른 형태로 바꾸는 일
- `implementation-plan` skill이 이미 제공하는 phase metadata 구조 자체를 새로 설계하는 일
- `implementation`, `implementation-review` skill의 내부 작업 방식 재설계
- `_sdd/spec/` 직접 수정
- Step 4에서 downstream artifact를 preview 생성하는 fallback 허용

### Guardrails

- Step 4는 orchestrator file 외 어떤 실행 artifact도 생성하지 않는다.
- Step 4는 future step의 출력 경로를 오케스트레이터 안에 선언할 수는 있지만, 해당 파일을 미리 만들 수는 없다.
- review가 포함된 path에서는 규모와 무관하게 `implementation`과 `implementation-review`를 항상 sub-agent step으로 실행한다. 부모 autopilot의 로컬 구현/로컬 리뷰로 대체하지 않는다.
- `implementation-plan`이 오케스트레이터 내부 step으로 존재하면 phase 수/경계는 Step 4가 추측으로 고정하지 않고 Step 7 runtime에서 plan output을 읽어 해석한다.
- expanded path의 `implementation` step은 독립 필드 `Execution Mode: phase-iterative`와 `Phase Source`를 함께 명시해야 하며, 각 phase의 review-fix/validation gate가 닫히기 전에는 다음 phase나 downstream step으로 진행할 수 없다.
- 마지막 phase 뒤 `final integration review`는 별도 필수 gate로 유지한다.

## Contract/Invariant Delta

| ID | Type | Change | Why |
|----|------|--------|-----|
| C1 | Modify | Step 4 `Reasoning -> Orchestrator Generation`의 허용 출력물은 `_sdd/pipeline/orchestrators/orchestrator_<topic>.md` 한 개다. `_sdd/drafts/*`, `_sdd/implementation/*`, `_sdd/pipeline/report_*`, 기타 downstream step artifact를 이 단계에서 생성하면 안 된다. | planning 단계와 execution 단계의 artifact boundary를 분리해야 phase source와 실행 상태가 혼동되지 않는다. |
| C2 | Add | 오케스트레이터에 `implementation-plan` step이 포함되고 downstream `implementation`이 그 output을 소비하는 경우, generated orchestrator는 해당 `implementation` step에 독립 필드 `Execution Mode: phase-iterative`를 선언해야 한다. | Step 4 시점에는 phase 개수가 아직 미정이므로, flat step으로 쓰면 runtime loop semantics가 문서에 드러나지 않는다. |
| C3 | Add | `Execution Mode: phase-iterative`로 선언된 implementation step은 독립 필드 `Phase Source`를 통해 `implementation-plan` output을 가리켜야 하며, 그 phase metadata를 읽고 각 phase마다 `implementation -> implementation-review -> fix(implementation 재호출, 필요 시) -> implementation-review -> phase validation`을 반복한다. | per-phase review-fix가 실제 제어 흐름임을 오케스트레이터가 명시해야 한다. |
| C4 | Add | Step 5 verification은 expanded path에서 `Execution Mode: phase-iterative` 선언, `Phase Source` linkage, per-phase gate semantics, final integration review 존재 여부를 검증해야 한다. | 문서에 loop semantics가 빠진 orchestrator를 승인 단계 전에 걸러야 한다. |
| C5 | Add | review가 포함된 small/medium/large 모든 path에서 `implementation`과 `implementation-review`는 각각 대응 sub-agent 호출로만 수행되며, review-fix loop는 `implementation -> implementation-review -> fix(implementation 재호출) -> implementation-review` mapping을 유지해야 한다. | patch 과정에서 large-path semantics만 강조되다가 cross-scale sub-agent invariant가 약해지는 것을 막아야 한다. |
| I1 | Add | future step artifact는 "planned output"으로만 존재할 수 있으며, 실제 생성 시점은 해당 step execution 이후다. | Step 4가 implementation-plan을 미리 생성해 버리는 drift를 막는다. |
| I2 | Add | `implementation-plan`이 오케스트레이터 내부에 있는 한, phase count와 boundary는 runtime-resolved metadata이며 Step 4가 precomputed phase list를 산출물처럼 만들어서는 안 된다. | "phase 수를 모르는 상태"와 "phase loop를 명시해야 하는 상태"를 동시에 만족시키는 계약이 필요하다. |
| I3 | Add | `phase-iterative` path에서는 각 phase의 `medium` 이슈도 기본적으로 exit blocker이며, 마지막 `final integration review` 전에는 `spec-update-done` 같은 downstream step으로 진행할 수 없다. | multi-phase 경계에서 결함을 닫지 못한 채 후속 단계로 넘어가는 것을 막는다. |
| I4 | Add | global review-fix loop든 per-phase review-fix loop든 실행 주체는 항상 sub-agent mapping이다. `implementation`/`implementation-review`를 부모가 inline local work로 대체하는 fallback은 허용되지 않는다. | "문서에는 review loop가 있지만 실제로는 부모가 다 해버리는" drift를 계약 차원에서 막아야 한다. |

## Touchpoints

| Area | Why It Changes |
|------|----------------|
| `.codex/skills/sdd-autopilot/SKILL.md` | Step 4, Step 5, Step 7에 artifact boundary와 독립 필드 `Execution Mode: phase-iterative` semantics, 그리고 cross-scale sub-agent invariant를 명시해야 한다. |
| `.claude/skills/sdd-autopilot/SKILL.md` | Claude mirror도 같은 generation/runtime contract를 가져야 한다. |
| `.codex/skills/sdd-autopilot/references/orchestrator-contract.md` | `Execution Mode: phase-iterative` implementation step, `Phase Source`, Step 4 output boundary 검증 규칙을 계약으로 고정해야 한다. |
| `.claude/skills/sdd-autopilot/references/orchestrator-contract.md` | Claude orchestrator contract parity를 유지해야 한다. |
| `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md` | expanded path reasoning에서 "implementation-plan inside orchestrator"와 runtime-resolved phase loop semantics를 설명해야 한다. |
| `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md` | Claude reasoning reference parity를 유지해야 한다. |
| `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md` | flat implementation step 대신 `phase-iterative` example을 보여주고, small/medium/large review path가 모두 sub-agent mapping을 쓰는 점을 드러내야 한다. |
| `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md` | Claude example도 같은 semantics를 보여줘야 한다. |
| `docs/AUTOPILOT_GUIDE.md` | Step 4는 orchestrator-only output이라는 점과 expanded path loop semantics를 사용자-facing 설명에 반영해야 한다. |
| `docs/en/AUTOPILOT_GUIDE.md` | 영문 guide에도 같은 semantics를 반영해야 한다. |

## Implementation Plan

1. autopilot core skill에서 Step 4 output boundary와 Step 5 verifier rule을 먼저 고정한다.
2. autopilot core skill과 orchestrator contract에 "review path는 항상 sub-agent mapping" invariant를 함께 고정한다.
3. orchestrator contract에 독립 필드 `Execution Mode: phase-iterative`와 `Phase Source` vocabulary를 추가하고, Step 7 executor binding과 연결한다.
4. reasoning reference, sample orchestrator, ko/en guide를 같은 용어로 동기화한다.
5. `_sdd/spec/` 반영은 이번 patch 구현 후 `spec-update-todo` 또는 `spec-update-done` follow-up으로 남긴다.

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, I1 | review, grep | Step 4/5 wording과 guide text를 읽어 "orchestrator만 생성" 규칙, `_sdd/drafts/*`/`_sdd/implementation/*` non-materialization 규칙, downstream artifact 생성 시점 분리가 명시되는지 확인한다. |
| V2 | C2, C3, I2, I3 | review walkthrough | sample orchestrator, Step 7 executor wording, orchestrator contract를 함께 읽어 `Execution Mode: phase-iterative` declaration, `Phase Source`, per-phase loop 순서가 연결되는지 확인한다. |
| V3 | C4, I3 | review | Step 5 verification 항목과 Step 7 gate semantics가 expanded path의 `final integration review`까지 일관되게 요구하는지 확인한다. |
| V4 | C5, I4 | review walkthrough | small direct path, single-phase medium path, multi-phase expanded path example과 core skill wording을 함께 읽어 review path의 실행 주체가 항상 sub-agent mapping으로 고정되는지 확인한다. |
| V5 | C1, C2, C3, C4, C5, I1, I2, I3, I4 | parity review | Claude/Codex, ko/en surface 간에 같은 contract vocabulary가 유지되고 stale flat-step wording이나 local-inline fallback wording이 남지 않았는지 교차 점검한다. |

## Risks / Open Questions

- 기존 sample/guide에는 이미 `Phase Gate 1/3` 같은 결과 로그가 있지만, "왜 Step 4에서 이걸 미리 평탄화하지 않았는가"를 설명하는 문장은 부족하다. 이번 patch에서 reasoning/guide wording을 함께 보강해야 한다.
- `_sdd/spec/main.md`, `_sdd/spec/components.md`, `_sdd/spec/usage-guide.md`도 장기적으로 sync가 필요할 수 있으나, 이번 draft의 implementation 범위에서는 직접 수정하지 않는다.
- small/medium example wording에서 "간단하니까 부모가 그냥 처리한다"처럼 읽히는 표현이 남아 있으면 이번 patch의 핵심 invariant를 약화시킬 수 있으므로, guide/example parity review를 더 엄격하게 봐야 한다.

<!-- spec-update-todo-input-end -->

# Part 2: Implementation Plan

## Overview

이번 구현은 `sdd-autopilot`의 expanded path를 더 정확한 오케스트레이션 계약으로 정리하는 문서/contract patch다. 핵심은 Step 4가 pure orchestrator generation 단계라는 점을 고정하고, `implementation-plan`이 오케스트레이터 내부 step으로 포함될 때 downstream `implementation` step이 실제로는 phase-iterative loop라는 의미를 오케스트레이터 문서 자체에 명시하게 만드는 것이다.

## Scope

### In Scope

- `.codex/skills/sdd-autopilot/SKILL.md`의 Step 4, Step 5, Step 7 갱신
- `.claude/skills/sdd-autopilot/SKILL.md` mirror parity 갱신
- `.codex/` / `.claude/` orchestrator contract 갱신
- `.codex/` / `.claude/` reasoning reference 및 sample orchestrator 갱신
- `docs/AUTOPILOT_GUIDE.md`, `docs/en/AUTOPILOT_GUIDE.md` 갱신

### Out of Scope

- `implementation-plan` skill output shape 자체의 대규모 재설계
- `implementation`, `implementation-review` skill/agent 내부 프로세스 변경
- `_sdd/spec/*` 직접 수정
- runtime code 추가나 별도 executor 스크립트 도입

## Components

1. **Autopilot Core Contract**: Step 4 output boundary, Step 5 verifier, Step 7 executor binding, cross-scale sub-agent invariant
2. **Orchestrator Contract**: `Execution Mode: phase-iterative` + `Phase Source` semantics
3. **Reasoning and Examples**: expanded path 설명과 sample orchestrator
4. **User Guides**: ko/en AUTOPILOT guide wording

## Contract/Invariant Delta Coverage

| Target | Planned Tasks | Validation Link |
|--------|---------------|-----------------|
| C1 | T1, T4 | V1, V5 |
| C2 | T1, T2, T3, T4 | V2, V5 |
| C3 | T1, T2, T3 | V2, V5 |
| C4 | T1, T2 | V3, V5 |
| C5 | T1, T2, T3, T4 | V4, V5 |
| I1 | T1, T4 | V1, V5 |
| I2 | T1, T2, T3 | V2, V5 |
| I3 | T1, T2, T3, T4 | V2, V3, V5 |
| I4 | T1, T2, T3, T4 | V4, V5 |

## Implementation Phases

### Phase 1: Freeze Step 4/5/7 Contract

**Goal**: autopilot core skill에서 Step 4 output boundary, Step 5 verifier, Step 7 phase-loop executor binding을 먼저 고정한다.
**Task Set / Dependency Closure**:
- T1 core skill patch
- Step 4는 orchestrator-only output
- review path는 항상 sub-agent mapping
- Step 5는 output boundary + `Execution Mode`/`Phase Source` declaration 검증
- Step 7은 runtime-resolved phase loop 해석
**Validation Focus**:
- `.codex/skills/sdd-autopilot/SKILL.md`
- `.claude/skills/sdd-autopilot/SKILL.md`
- V1
- V2
- V3
- V4
**Exit Criteria**:
- [ ] Step 4가 orchestrator 외 artifact를 만들지 않는다고 명시된다.
- [ ] small/medium/large review path 모두 `implementation`과 `implementation-review`를 sub-agent step으로 실행한다고 명시된다.
- [ ] Step 5가 expanded path에서 `Execution Mode: phase-iterative` declaration과 `Phase Source` linkage를 검증 대상으로 삼는다.
- [ ] Step 7이 `implementation-plan` output을 읽고 per-phase loop를 닫는다고 명시된다.
**Carry-over Policy**: None. `critical/high/medium` wording drift는 모두 exit blocker다.

### Phase 2: Align Contract, Reasoning, and Example Surfaces

**Goal**: orchestrator contract, reasoning reference, sample orchestrator가 같은 `Execution Mode: phase-iterative`와 `Phase Source` vocabulary를 사용하도록 정렬한다.
**Task Set / Dependency Closure**:
- T2 orchestrator contract patch
- T3 reasoning reference + sample patch
- core skill wording과 동일한 field/term 사용
**Validation Focus**:
- `.codex/skills/sdd-autopilot/references/orchestrator-contract.md`
- `.claude/skills/sdd-autopilot/references/orchestrator-contract.md`
- `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md`
- `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md`
- sample orchestrator pair
- V2
- V3
- V4
- V5
**Exit Criteria**:
- [ ] contract/reference/example이 `Execution Mode: phase-iterative`, `Phase Source`, per-phase loop 순서를 같은 의미로 설명한다.
- [ ] expanded path example이 phase count를 Step 4 산출물이 아니라 runtime-resolved plan output으로 다룬다.
- [ ] direct path와 single-phase medium path 예시도 review가 있으면 sub-agent mapping을 유지한다.
- [ ] final integration review requirement가 contract와 example 모두에서 유지된다.
**Carry-over Policy**: None.

### Phase 3: Sync User-Facing Guide Wording

**Goal**: ko/en guide가 Step 4 output boundary와 expanded path loop semantics를 사용자 관점에서 같은 의미로 설명하도록 닫는다.
**Task Set / Dependency Closure**:
- T4 guide patch
- stale flat-step wording 제거
- orchestrator-only generation wording 추가
**Validation Focus**:
- `docs/AUTOPILOT_GUIDE.md`
- `docs/en/AUTOPILOT_GUIDE.md`
- V1
- V2
- V4
- V5
**Exit Criteria**:
- [ ] guide가 Step 4 output을 orchestrator file로만 설명한다.
- [ ] expanded path 설명이 `implementation-plan -> phase-iterative implementation loop` semantics를 반영한다.
- [ ] small/medium review path도 `implementation`과 `implementation-review`가 sub-agent loop로 실행된다고 설명한다.
- [ ] ko/en guide 간 wording drift가 남지 않는다.
**Carry-over Policy**: None.

## Task Details

### Task T1: Patch Step 4 output boundary and Step 7 phase-loop executor binding
**Component**: Autopilot Core Contract
**Priority**: P0
**Type**: Refactor

**Description**: `sdd-autopilot` skill 본문에서 Step 4를 pure orchestrator generation 단계로 고정하고, Step 5 verifier 및 Step 7 executor wording을 이에 맞게 갱신한다. expanded path에서는 `implementation-plan` step 이후 downstream `implementation`에 독립 필드 `Execution Mode: phase-iterative`와 `Phase Source`가 선언된다는 점을 문서에 명시하고, small/medium/large의 모든 review path에서 `implementation`과 `implementation-review`가 항상 sub-agent 실행 단위라는 invariant도 함께 고정한다.

**Acceptance Criteria**:
- [ ] Step 4는 `_sdd/pipeline/orchestrators/orchestrator_<topic>.md` 외 artifact를 생성하지 않는다고 명시한다.
- [ ] review가 포함된 모든 path에서 `implementation`과 `implementation-review`를 부모가 로컬 inline으로 대체할 수 없다고 명시한다.
- [ ] Step 5는 expanded path에서 `Execution Mode: phase-iterative` declaration, `Phase Source` linkage, final integration review requirement를 검증 대상으로 포함한다.
- [ ] Step 7은 `implementation-plan` output을 읽어 각 phase마다 `implementation -> implementation-review -> fix -> implementation-review -> validation`을 반복한다고 설명한다.
- [ ] Claude/Codex skill 본문이 같은 semantics를 유지한다.

**Target Files**:
- [M] `.codex/skills/sdd-autopilot/SKILL.md`
- [M] `.claude/skills/sdd-autopilot/SKILL.md`

**Technical Notes**: Covers C1, C2, C3, C4, C5, I1, I2, I3, I4. Validated by V1, V2, V3, V4, V5.
**Dependencies**: None

### Task T2: Extend orchestrator contract for `Execution Mode: phase-iterative` + `Phase Source`
**Component**: Orchestrator Contract
**Priority**: P0
**Type**: Feature

**Description**: orchestrator contract에 expanded path의 `implementation` step이 flat step이 아니라 독립 필드 `Execution Mode: phase-iterative`와 `Phase Source`를 가진 execution unit일 수 있음을 명시하고, 이 경우 필요한 declaration과 verification rule을 추가한다. 동시에 review가 포함된 모든 규모의 path에서 `implementation`/`implementation-review`의 실행 주체가 항상 sub-agent mapping임을 contract 수준으로 고정한다.

**Acceptance Criteria**:
- [ ] contract에 Step 4 output boundary와 future artifact non-materialization rule이 반영된다.
- [ ] contract에 `Execution Mode: phase-iterative`와 `Phase Source` declaration requirement가 추가된다.
- [ ] contract가 phase source, per-phase loop 순서, final integration review precondition을 설명한다.
- [ ] contract가 global review-fix path와 per-phase review-fix path 모두에서 `implementation`/`implementation-review` sub-agent mapping을 강제한다.
- [ ] Claude/Codex orchestrator contract가 같은 vocabulary를 사용한다.

**Target Files**:
- [M] `.codex/skills/sdd-autopilot/references/orchestrator-contract.md`
- [M] `.claude/skills/sdd-autopilot/references/orchestrator-contract.md`

**Technical Notes**: Covers C2, C3, C4, C5, I1, I2, I3, I4. Validated by V2, V3, V4, V5.
**Dependencies**: T1

### Task T3: Sync reasoning reference and sample orchestrators with runtime-resolved phase loops
**Component**: Reasoning and Examples
**Priority**: P1
**Type**: Refactor

**Description**: reasoning reference와 sample orchestrator를 갱신해 expanded path에서 `implementation-plan`이 오케스트레이터 내부 producer step이고, 그 output을 다음 `Execution Mode: phase-iterative` + `Phase Source` implementation step이 소비한다는 semantics를 예시로 드러낸다. 동시에 small direct path와 single-phase medium path 예시에서도 review가 있으면 sub-agent review-fix mapping을 동일하게 유지한다는 점을 드러낸다.

**Acceptance Criteria**:
- [ ] reasoning reference가 Step 4에서 phase count를 미리 materialize하지 않는 이유를 설명한다.
- [ ] sample orchestrator의 expanded path가 `implementation-plan -> Execution Mode: phase-iterative implementation loop`와 `Phase Source`를 명시한다.
- [ ] sample orchestrator가 per-phase `implementation / implementation-review / fix / validation` 흐름과 final integration review를 표현한다.
- [ ] single-phase/direct path example도 review가 있으면 `implementation / implementation-review` sub-agent mapping을 유지한다.
- [ ] Claude/Codex example pair가 같은 semantics를 유지한다.

**Target Files**:
- [M] `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md`
- [M] `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md`
- [M] `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md`
- [M] `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md`

**Technical Notes**: Covers C2, C3, C5, I2, I3, I4. Validated by V2, V4, V5.
**Dependencies**: T1, T2

### Task T4: Refresh ko/en AUTOPILOT guides for orchestrator-only generation and phase loops
**Component**: User Guides
**Priority**: P1
**Type**: Documentation

**Description**: ko/en guide에 Step 4 output boundary와 expanded path loop semantics를 반영해, 사용자가 "왜 implementation-plan이 Step 4에서 생기지 않는가"와 "왜 오케스트레이터가 phase loop를 선언해야 하는가"를 이해할 수 있게 한다. 또한 small/medium/large를 막론하고 review가 있는 path에서는 `implementation`과 `implementation-review`가 항상 sub-agent loop를 돈다는 점을 분명히 드러낸다.

**Acceptance Criteria**:
- [ ] guide가 Step 4 output을 orchestrator file only로 설명한다.
- [ ] expanded path example/log wording이 `Execution Mode: phase-iterative implementation loop` semantics와 충돌하지 않는다.
- [ ] future artifact는 실행 시점에 생성된다는 설명이 포함된다.
- [ ] guide가 small/medium/large review path 모두에서 sub-agent review-fix loop를 고정 invariant로 설명한다.
- [ ] ko/en guide parity가 유지된다.

**Target Files**:
- [M] `docs/AUTOPILOT_GUIDE.md`
- [M] `docs/en/AUTOPILOT_GUIDE.md`

**Technical Notes**: Covers C1, C2, C5, I1, I3, I4. Validated by V1, V2, V4, V5.
**Dependencies**: T1, T2, T3

## Parallel Execution Summary

- T1은 core wording과 cross-scale invariant를 고정하므로 가장 먼저 수행하는 편이 안전하다.
- T2는 T1의 vocabulary를 그대로 소비해야 하므로 순차 의존이 있다.
- T3는 T1/T2 이후에는 reference/example 범위만 다루므로 독립 실행 가능하다.
- T4는 guide wording이 reference/example semantics를 따라야 하므로 마지막에 수행하는 편이 안전하다.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| `Execution Mode: phase-iterative` 또는 `Phase Source` declaration이 일부 surface에서 누락됨 | implementation 단계에서 다시 flat step처럼 해석되거나 phase source를 잘못 읽을 수 있음 | contract와 sample에서 동일한 독립 field name을 사용하도록 강제한다 |
| small/medium path wording에서 review sub-agent invariant가 약하게 서술됨 | patch가 large path 전용처럼 읽혀 local-inline fallback이 다시 허용될 수 있음 | core skill, sample, guide에 cross-scale invariant를 반복적으로 명시한다 |
| Step 4 output boundary가 guide에는 반영되지만 core skill에는 약하게 남음 | 다시 implementation-plan precreation drift가 발생할 수 있음 | T1에서 Step 4/5/7을 먼저 고정하고 T4는 그 결과만 설명한다 |
| Claude/Codex parity 누락 | 플랫폼별 의미 드리프트 발생 | 같은 concern의 `.claude/` + `.codex/` 파일을 한 task에서 함께 수정한다 |

## Open Questions

- `_sdd/spec/main.md`와 `_sdd/spec/components.md`까지 같은 턴에 sync할지는 후속 `spec-update-todo` 판단으로 남긴다.
