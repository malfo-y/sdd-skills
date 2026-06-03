# Feature Draft: sdd-autopilot contract hardening

<!-- spec-update-todo-input-start -->
# Part 1: Temporary Spec Draft

## Change Summary

`sdd-autopilot`이 생성하는 orchestrator 계약을 실제 Codex custom-agent 실행 모델에 맞게 단단하게 정리한다.

현재 review 결과상 핵심 문제는 다섯 가지다.

1. `implementation` pipeline step이 일반 custom-agent 단일 호출처럼 읽혀, 단일 task leaf인 `implementation_agent`에 feature/phase 전체가 넘어갈 수 있다.
2. generated orchestrator가 `feature_draft_agent` / `implementation_plan_agent`를 직접 호출하면서, wrapper skill이 소유하는 `plan_review_agent` review-fix gate를 우회할 수 있다.
3. review-fix loop에서 `Low` severity가 수정 대상인지 advisory인지 문서별로 다르게 쓰인다.
4. 기존 orchestrator 재개를 위한 legacy alias 지원은 필요 없으므로, 새 contract는 canonical `_agent` 이름만 허용해야 한다.
5. small/direct path와 `feature-draft` 기본 포함 정책이 reference와 본문 사이에서 다르게 읽힌다.

이번 변경은 코드 구현 자체가 아니라 **autopilot contract/reference/example 문서의 정합성 수정**이다. 목표는 생성된 orchestrator를 사람이 그대로 따라도, 또는 autopilot이 Step 7에서 그대로 집행해도 다음 흐름이 명확해지는 것이다.

```text
feature_draft_agent
  -> plan_review_agent
  -> feature_draft_agent fix mode if needed
  -> plan_review_agent re-review
  -> implementation dispatch controller
       -> task별 implementation_agent leaf spawn
       -> implementation_review_agent
       -> finding별 implementation_agent fix leaf spawn if needed
       -> implementation_review_agent re-review
  -> validation
  -> spec_update_done_agent
```

## Scope Delta

**In-scope**
- `.codex/skills/sdd-autopilot/SKILL.md`
  - Step 4 generation rules, Step 5 verification, Step 7 execution semantics 정리.
  - `implementation_agent` step의 특수 실행 의미를 일반 custom-agent 단일 호출보다 우선하도록 명시.
  - producer 산출물 review-fix gate와 canonical-only agent type rule 추가.
- `.codex/skills/sdd-autopilot/references/orchestrator-contract.md`
  - `Implementation Dispatch Controller` 계약 추가.
  - `Planning Producer Review Gate` 계약 추가.
  - Low severity advisory 정책 통일.
  - legacy alias 미지원 및 canonical `_agent` only rule 추가.
- `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md`
  - planning precedence를 본문과 일치시킴: trivial/small direct만 `feature-draft` 생략 가능, non-trivial은 `feature-draft` 기본 포함.
  - multi-phase는 `implementation_plan_agent` 필수 유지.
- `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md`
  - sample A/B를 최신 contract의 정답 예시로 갱신.
  - producer review gate, implementation dispatch controller, Low advisory, canonical agent type만 사용.
- `.claude/skills/sdd-autopilot/` mirror가 존재하면 동일 semantic 반영.

**Out-of-scope**
- legacy orchestrator 호환/재개 지원. 과거 `_sdd/pipeline/orchestrators/*.md`는 history artifact로 두며, 새 verifier가 normalize하지 않는다.
- `_sdd/spec/*` 직접 수정. 필요 시 후속 `spec_update_done_agent`가 동기화한다.
- `implementation_agent`, `implementation_review_agent`, `feature_draft_agent`, `implementation_plan_agent`, `plan_review_agent`의 본문 계약 변경. 이번 변경은 autopilot 생성/실행 계약의 정합성 보강이다.
- 기존 `_sdd/pipeline/orchestrators/*.md` 전체 migration. 대표 sample과 autopilot contract만 최신화한다.

**Guardrail Delta**
- 새 orchestrator는 canonical agent type만 사용한다. `implementation`, `implementation_review`, `spec_update_done` 같은 legacy names는 invalid다.
- `implementation_agent`는 단일 task leaf다. 어떤 path에서도 feature/phase 전체를 단일 leaf에게 넘기지 않는다.
- `Low` finding은 기본적으로 fix loop blocker가 아니다. `critical/high/medium`만 fix targets이며, Low는 advisory/logged follow-up으로 남긴다.

## Contract/Invariant Delta

| ID | Type | Change | Why |
|----|------|--------|-----|
| C1 | Modify | `implementation_agent`가 적힌 pipeline step은 일반 single custom-agent call이 아니라 **Implementation Dispatch Controller**로 해석된다. autopilot이 task set을 파싱하고 task별 `implementation_agent` leaf를 spawn한다. | 단일 task leaf에 feature/phase 전체가 넘어가는 실행 오류 방지 |
| C2 | Add | Initial implementation dispatch: 같은 phase + dependency edge 없음 + Target Files disjoint면 병렬 dispatch group, 아니면 순차 fallback. fix dispatch: review finding 하나씩 순차 leaf spawn. | leaf fan-out과 review-fix loop의 dispatch granularity를 명확히 분리 |
| C3 | Add | `feature_draft_agent` 산출 직후 `plan_review_agent` review-fix gate 필수. fix 필요 시 `feature_draft_agent` fix mode 재호출, re-review는 `plan_review_agent`. | generated orchestrator가 wrapper skill의 산출물 quality gate를 우회하지 않게 함 |
| C4 | Add | `implementation_plan_agent` 산출 직후 `plan_review_agent` review-fix gate 필수. fix 필요 시 `implementation_plan_agent` fix mode 재호출. | implementation plan의 Target Files/dependency 품질을 implementation 전에 닫음 |
| C5 | Modify | implementation review-fix loop의 `fix_targets`는 `critical/high/medium`으로 통일. `Low`는 advisory/logged follow-up. | review agent severity 정책과 sample/contract 불일치 해소 |
| C6 | Add | Canonical agent type only: 새 orchestrator는 `_agent` names만 허용한다. legacy alias는 normalize하지 않고 verification에서 reject/regenerate한다. | 호환 레이어 제거로 contract 단순화 |
| C7 | Modify | Planning precedence: trivial/small direct path만 `feature-draft` 생략 가능. non-trivial change는 `feature-draft` 기본 포함. multi-phase면 `implementation_plan_agent` 필수. | 본문/reference 정책 drift 제거 |
| C8 | Add | Step 5 verification은 producer review gate, implementation dispatch controller, Low advisory policy, canonical-only agent names를 구조 검증에 포함한다. | generator가 새 contract를 빠뜨리지 못하게 함 |
| I1 | Keep | `_sdd/spec/` 직접 수정은 `spec_update_todo_agent` / `spec_update_done_agent`만 수행한다. | 기존 spec ownership 유지 |
| I2 | Add | Review-fix gate 종료 조건은 `critical = 0 AND high = 0 AND medium = 0`. Low 잔존은 gate 종료를 막지 않는다. | loop 종료 조건과 fix target 일치 |
| I3 | Add | Planning producer review gate가 닫히기 전에는 downstream implementation으로 진행할 수 없다. | 품질 검증 없는 draft/plan handoff 금지 |
| I4 | Add | Implementation-scoped review-fix gate가 닫히기 전에는 validation/spec sync/downstream step으로 진행할 수 없다. | 기존 immediate gate 원칙 유지 및 강화 |

## Touchpoints

현재 review에서 확인한 주요 지점:

- `.codex/skills/sdd-autopilot/SKILL.md`
  - AC: 테스트/검증과 approval 기준은 유지.
  - Hard Rules: implementation dispatch special case, producer review gate, canonical-only rule 추가.
  - Step 4: orchestrator generation rules에 producer review gate와 dispatch controller 필드 추가.
  - Step 5: verification checklist에 새 invariants 추가.
  - Step 7.2: `custom-agent step이면 agent_type으로 호출한다` 일반 규칙보다 `implementation_agent` dispatch controller 규칙이 우선한다고 명시.
- `.codex/skills/sdd-autopilot/references/orchestrator-contract.md`
  - Step Contract: canonical allowed agent type에 `plan_review_agent` 추가. legacy names는 forbidden.
  - Implementation Dispatch Granularity: controller terminology로 재작성.
  - Review-Fix Contract: `fix_targets=critical/high/medium`, `Low=advisory`.
  - New section: Planning Producer Review Gate.
- `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md`
  - Planning precedence by scale: small direct 예외 조건 구체화.
  - Phase-gated execution rule의 `per-phase` 표현을 current contract의 `per-group`과 맞춤.
- `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md`
  - Example A: `feature_draft_agent` 직후 plan-review gate 추가. Step 2 implementation은 controller로 표기.
  - Example B: `implementation_plan_agent` 직후 plan-review gate 추가. Step 4는 phase-iterative dispatch controller로 표기.
  - 모든 `fix_targets: critical/high/medium/low` 제거.
- `.claude/skills/sdd-autopilot/...`
  - 존재 시 Codex와 semantic mirror 유지. 단, platform-specific invocation syntax만 다르게 둔다.

## Implementation Plan

1. **Contract skeleton 정리**
   - `orchestrator-contract.md`에 canonical-only, producer gate, implementation dispatch controller, Low advisory 정책을 먼저 반영한다.
   - 이 파일을 source contract로 삼아 `SKILL.md`와 sample을 맞춘다.
2. **Autopilot process 갱신**
   - Step 4 generation rules에 새 mandatory fields를 추가한다.
   - Step 5 verification에 reject conditions를 추가한다.
   - Step 7 execution semantics에 implementation dispatch controller 우선순위를 추가한다.
3. **Reasoning reference 정렬**
   - trivial/small direct 예외와 non-trivial feature-draft 기본 포함을 하나의 기준으로 정리한다.
   - `per-phase` vs `per-group` 용어 drift를 `per-group`/Checkpoint 기준으로 맞춘다.
4. **Sample orchestrator 갱신**
   - Example A/B 모두 producer gate와 controller semantics가 보이게 재작성한다.
   - Low advisory와 canonical-only names를 sample에 반영한다.
5. **Mirror 반영**
   - `.claude/skills/sdd-autopilot/` mirror가 있으면 같은 semantic 변경을 적용한다.
6. **정적 검증**
   - stale terms, Low fix target, legacy alias, missing producer gate, missing controller wording을 grep으로 확인한다.

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, C2 | grep + manual read | `implementation_agent` step이 `task당 spawn`, `dispatch controller`, `finding 하나씩 순차 fix`를 포함하고, phase/feature 전체 단일 leaf 호출 문구가 없음 |
| V2 | C3, C4, I3 | grep + manual read | `feature_draft_agent`와 `implementation_plan_agent` 직후 `plan_review_agent` gate가 contract/sample에 존재 |
| V3 | C5, I2 | grep | `fix_targets`/`수정 대상` context에서 `low`, `Low`, `critical/high/medium/low`가 fix 대상으로 남지 않고 Low advisory 문구가 존재 |
| V4 | C6 | grep + manual read | Codex/Claude contract/sample에서 invalid invocation context의 legacy alias가 없음: Codex `agent_type:`/`subagent_type:` bare legacy value, `agent_mapping` 또는 review-fix mapping의 `review = implementation_review`, `fix = implementation`, `re-review = implementation_review`, Claude subagent invocation의 suffix 없는 `sdd-skills:implementation-review`, `sdd-skills:implementation-plan`, `sdd-skills:feature-draft`를 reject/regenerate 대상으로 확인. 일반 planning prose의 `feature-draft`/`implementation-plan` 용어와 Claude canonical `sdd-skills:implementation-review-agent`, `sdd-skills:implementation-plan-agent`, `sdd-skills:feature-draft-agent` 호출은 금지하지 않음 |
| V5 | C7 | manual read | `SKILL.md`와 `sdd-reasoning-reference.md`의 planning precedence가 같은 조건을 말함 |
| V6 | C8 | manual read | Step 5 verification checklist가 producer gate/controller/Low/canonical-only를 모두 검사 |
| V7 | 전체 | `git diff --check` | Markdown whitespace/patch hygiene 통과 |

## Risks / Open Questions

### Q1. legacy orchestrator 재개 지원이 필요한가
- **Decision taken**: 필요 없다. 사용자가 명시적으로 legacy orchestrator를 쓸 일이 없다고 확인했다. 새 contract는 canonical-only로 단순화한다.
- **Alternatives considered**: alias normalization (`implementation` → `implementation_agent`)을 Step 0/5에 추가. 호환성은 생기지만 verifier가 비대해지고 오래된 contract를 계속 살려야 한다. 기각.
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q2. producer review gate를 generated orchestrator 안에 둘지, wrapper skill을 호출하게 할지
- **Decision taken**: generated orchestrator는 custom agents만 직접 spawn하는 구조를 유지하되, wrapper skill의 loop와 동등한 producer→plan_review→fix→re-review gate를 orchestrator contract에 포함한다.
- **Alternatives considered**: Phase 2에서 `feature-draft` skill 자체를 로컬 step으로 호출. 하지만 Phase 2 custom-agent step 중심 계약과 파일 기반 handoff가 흐려지고, wrapper/orchestrator 실행 경로가 중첩된다.
- **Confidence**: MEDIUM
- **User confirmation needed**: No

### Q3. Low finding을 자동으로 고칠지
- **Decision taken**: 기본적으로 고치지 않는다. `Low`는 advisory/logged follow-up이며 gate blocker가 아니다. 사용자가 별도 polish를 요구하거나 orchestrator가 명시적으로 Low cleanup step을 둘 때만 처리한다.
- **Alternatives considered**: `Low`까지 fix target에 포함. 실행 시간이 늘고 loop 종료 조건과 mismatch가 생긴다. 기각.
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q4. single-phase medium에서 implementation-plan을 생략해도 producer review gate는 충분한가
- **Decision taken**: 가능하다. 단, `feature_draft_agent` Part 2가 `Target Files`, dependencies, validation detail을 충분히 담고, 그 산출물이 `plan_review_agent` gate를 통과해야 한다.
- **Alternatives considered**: 모든 non-trivial에 `implementation_plan_agent` 강제. 작은 single-phase 변경에도 문서가 비대해진다. 기각.
- **Confidence**: MEDIUM
- **User confirmation needed**: No
<!-- spec-update-todo-input-end -->

# Part 2: Implementation Plan

## Overview

이 구현은 `sdd-autopilot`의 generated orchestrator contract를 실행 가능하고 모호성 적은 형태로 보강하는 문서 리팩터다. 핵심은 세 가지 실행 경계를 분리하는 것이다.

- **Planning producer gate**: `feature_draft_agent` / `implementation_plan_agent`는 산출물을 만들고, autopilot은 곧바로 `plan_review_agent` review-fix gate를 닫는다.
- **Implementation dispatch controller**: `implementation_agent`는 단일 task leaf다. autopilot이 task set을 파싱하고 leaf를 task별 spawn한다.
- **Implementation review-fix gate**: 구현 범위 review는 `implementation_review_agent`, fix는 finding별 `implementation_agent` leaf, re-review는 다시 `implementation_review_agent`다.

이 draft의 구현자는 legacy orchestrator compatibility를 추가하지 않는다. 과거 pipeline artifact는 history로 남기고, 새 생성물만 canonical contract를 따른다.

## Scope

### In Scope
- Codex `sdd-autopilot` skill, references, example 갱신.
- Claude mirror가 있으면 동일 semantic 갱신.
- 최신 sample orchestrator의 정답 예시화.
- 정적 검증 명령 실행.

### Out of Scope
- `_sdd/spec/*` 직접 수정.
- 기존 `_sdd/pipeline/orchestrators/*.md` 전면 migration.
- custom agent 본문 변경.
- legacy alias normalization.

## Components

| Component | Role | Change |
|-----------|------|--------|
| `SKILL.md` | autopilot runtime process | generation/verification/execution rules 보강 |
| `orchestrator-contract.md` | generated orchestrator source contract | controller/gate/canonical-only/Low advisory 계약 추가 |
| `sdd-reasoning-reference.md` | planning policy reference | small/direct vs feature-draft 기준 통일 |
| `sample-orchestrator.md` | expected output example | Example A/B 최신 계약 반영 |
| `.claude` mirror | platform mirror | Codex와 semantic parity 유지 |

## Contract/Invariant Delta Coverage

| Task | Covers |
|------|--------|
| T1 | C1, C2, C3, C4, C5, C6, I2, I3 |
| T2 | C1, C3, C4, C5, C6, C8, I3, I4 |
| T3 | C7 |
| T4 | C1, C2, C3, C4, C5, C6, C7 |
| T5 | Codex/Claude parity for C1-C8 |
| T6 | V1-V7 |

## Implementation Phases

### Phase 1: Core Contract
**Goal**: `orchestrator-contract.md`를 먼저 고쳐 이후 파일의 source contract로 삼는다.
**Tasks**: T1
**Validation Focus**: V1, V2, V3, V4, V5
**Exit Criteria**:
- [ ] canonical-only allowed agent list와 forbidden legacy rule이 있다.
- [ ] implementation dispatch controller 계약이 있다.
- [ ] planning producer review gate 계약이 있다.
- [ ] Low advisory 정책이 명시된다.
**Carry-over Policy**: None
**Checkpoint**: true
**Checkpoint Reason**: downstream 파일들이 이 contract를 기준으로 문구를 맞춘다.

### Phase 2: Autopilot Process
**Goal**: `SKILL.md` Step 4/5/7을 Phase 1 contract와 맞춘다.
**Tasks**: T2
**Validation Focus**: V1, V2, V6
**Exit Criteria**:
- [ ] generation rules가 producer gate와 controller를 생성하도록 한다.
- [ ] verification이 새 reject conditions를 검사한다.
- [ ] execution semantics에서 implementation dispatch controller가 일반 custom-agent dispatch보다 우선한다.
**Carry-over Policy**: None
**Checkpoint**: false

### Phase 3: Reasoning Policy
**Goal**: planning precedence drift를 제거한다.
**Tasks**: T3
**Validation Focus**: V5
**Exit Criteria**:
- [ ] trivial/small direct 예외와 non-trivial feature-draft 기본 포함 기준이 본문과 reference에서 일치한다.
- [ ] multi-phase는 `implementation_plan_agent` 필수로 남는다.
**Carry-over Policy**: None
**Checkpoint**: false

### Phase 4: Examples and Mirror
**Goal**: sample orchestrator와 mirror를 최신 contract와 맞춘다.
**Tasks**: T4, T5
**Validation Focus**: V1, V2, V3, V4, V5
**Exit Criteria**:
- [ ] sample A/B에 producer review gate와 dispatch controller가 보인다.
- [ ] sample에서 Low fix target과 legacy agent type이 없다.
- [ ] Claude mirror가 Codex와 semantic parity를 가진다.
**Carry-over Policy**: None
**Checkpoint**: true
**Checkpoint Reason**: sample/mirror는 사용자가 실제로 따라 할 surface라 최종 전 검증이 필요하다.

### Phase 5: Verification
**Goal**: 정적 검증 명령과 manual read로 contract drift를 닫는다.
**Tasks**: T6
**Validation Focus**: V1-V7
**Exit Criteria**:
- [ ] 검증 명령 통과.
- [ ] 잔여 Low/polish는 advisory로만 기록된다.
**Carry-over Policy**: Low advisory only
**Checkpoint**: true
**Checkpoint Reason**: 마지막 phase.

## Task Details

### T1: Update orchestrator contract
**Component**: `orchestrator-contract.md`
**Priority**: P0
**Type**: Contract refactor

**Description**: canonical allowed agent types를 정리하고, `plan_review_agent`를 명시적으로 포함한다. legacy names are invalid rule을 추가한다. `Implementation Dispatch Controller`와 `Planning Producer Review Gate` sections를 추가한다. Review-Fix Contract의 fix target을 `critical/high/medium`으로 통일하고 Low advisory policy를 둔다.

**Acceptance Criteria**:
- [ ] allowed agent list는 canonical `_agent` names만 포함한다.
- [ ] legacy alias는 unsupported/reject 대상이라고 명시한다.
- [ ] `implementation_agent` step은 controller로 해석된다는 규칙이 있다.
- [ ] producer 산출물 gate가 `feature_draft_agent`와 `implementation_plan_agent` 각각에 대해 있다.
- [ ] Low는 advisory/logged follow-up이며 fix target이 아니다.

**Target Files**:
- [M] `.codex/skills/sdd-autopilot/references/orchestrator-contract.md`

**Dependencies**: 없음

### T2: Update autopilot SKILL process
**Component**: `SKILL.md`
**Priority**: P0
**Type**: Process contract refactor

**Description**: Step 4 generation rules, Step 5 verification, Step 7 execution semantics를 T1 contract와 맞춘다. `implementation_agent` dispatch controller special case가 일반 custom-agent 호출 규칙보다 우선한다는 문구를 넣는다. Phase 2에서는 request_user_input 금지 유지.

**Acceptance Criteria**:
- [ ] Step 4가 producer review gate와 implementation dispatch controller를 생성하도록 요구한다.
- [ ] Step 5가 canonical-only, producer gate, controller, Low advisory를 검증한다.
- [ ] Step 7이 `implementation_agent` step을 task별 leaf spawn으로 실행한다고 명시한다.
- [ ] legacy alias 발견 시 normalize하지 않고 reject/regenerate한다.

**Target Files**:
- [M] `.codex/skills/sdd-autopilot/SKILL.md`

**Dependencies**: T1

### T3: Align reasoning reference planning precedence
**Component**: `sdd-reasoning-reference.md`
**Priority**: P1
**Type**: Policy alignment

**Description**: small direct path와 feature-draft 기본 포함 정책을 하나로 통일한다. trivial/small direct 예외 조건을 구체화하고, non-trivial은 `feature-draft`, multi-phase는 `implementation_plan_agent`를 기본으로 둔다. `per-phase` 표현이 남아 있으면 current contract의 `per-group`/Checkpoint terminology와 맞춘다.

**Acceptance Criteria**:
- [ ] `feature-draft` 생략 조건이 `SKILL.md`와 일치한다.
- [ ] multi-phase는 implementation plan 필수라고 명시한다.
- [ ] `per-phase`/`per-group` 용어가 충돌하지 않는다.

**Target Files**:
- [M] `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md`

**Dependencies**: T1

### T4: Update sample orchestrator
**Component**: `sample-orchestrator.md`
**Priority**: P0
**Type**: Example refactor

**Description**: Example A/B를 최신 contract의 기준 예시로 고친다. `feature_draft_agent`와 `implementation_plan_agent` 직후 plan-review gate를 넣고, implementation step은 dispatch controller로 표기한다. `fix_targets: critical/high/medium/low`를 제거하고 Low advisory policy를 반영한다. Sample reasoning text는 T3에서 확정한 planning precedence를 그대로 따른다: trivial/small direct만 `feature-draft` 생략 가능, non-trivial은 `feature-draft` 기본 포함, multi-phase면 `implementation_plan_agent` 필수.

**Acceptance Criteria**:
- [ ] Example A에 feature draft producer review gate가 있다.
- [ ] Example B에 feature draft 및 implementation plan producer review gate가 있다.
- [ ] Example A/B implementation step이 controller semantics를 명확히 가진다.
- [ ] canonical `_agent` names만 사용한다.
- [ ] Low는 advisory로만 등장한다.
- [ ] sample reasoning text가 C7 planning precedence와 일치한다.

**Target Files**:
- [M] `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md`

**Dependencies**: T1, T2, T3

### T5: Mirror Claude autopilot files
**Component**: `.claude/skills/sdd-autopilot/`
**Priority**: P1
**Type**: Mirror parity

**Description**: Claude mirror가 존재하면 T1-T4의 semantic 변경을 반영한다. platform-specific invocation syntax는 Claude 방식으로 유지한다.

**Acceptance Criteria**:
- [ ] Claude mirror가 Codex와 같은 contract/gate/policy를 말한다.
- [ ] platform syntax 차이 외 semantic drift가 없다.
- [ ] Claude suffix 없는 subagent invocation (`sdd-skills:implementation-review`, `sdd-skills:implementation-plan`, `sdd-skills:feature-draft`)은 canonical agent invocation으로 쓰이지 않고 reject/regenerate 대상으로만 남는다.
- [ ] Claude canonical invocation (`sdd-skills:implementation-review-agent`, `sdd-skills:implementation-plan-agent`, `sdd-skills:feature-draft-agent`)과 일반 planning prose의 `feature-draft`/`implementation-plan` 용어는 유지 가능하다.

**Target Files**:
- [M] `.claude/skills/sdd-autopilot/SKILL.md`
- [M] `.claude/skills/sdd-autopilot/references/orchestrator-contract.md`
- [M] `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md`
- [M] `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md`

**Dependencies**: T1, T2, T3, T4

### T6: Verify contract hardening
**Component**: verification
**Priority**: P0
**Type**: Validation

**Description**: grep/manual read/git diff checks로 stale policy와 invalid examples를 잡는다. 이 저장소는 `_sdd/env.md`상 전통적 테스트 프레임워크가 없으므로 문서 계약 검증을 테스트로 삼는다.

**Acceptance Criteria**:
- [ ] `git diff --check` 통과.
- [ ] Codex/Claude 양쪽에서 Low fix target/stale legacy alias 없음.
- [ ] `agent_type`, `subagent_type`, `agent_mapping`, review-fix mapping, Claude subagent invocation examples에서 legacy alias는 invalid invocation context로만 검사되고 reject/regenerate 대상으로 남는다.
- [ ] 일반 planning prose의 `feature-draft`/`implementation-plan` 용어와 Claude canonical `*-agent` invocation은 검증 grep이 실패로 잡지 않는다.
- [ ] producer gate/controller/canonical-only/advisory 문구가 존재.

**Target Files**:
- [C] `_sdd/implementation/test_results/test_results_sdd_autopilot_contract_hardening.md` -- 이 feature의 canonical validation evidence artifact를 새로 기록한다.

**Dependencies**: T1-T5

## Review-Fix Loop

이 draft를 구현하는 orchestrator는 다음 gate를 사용한다.

- `scope`: global
- `max_rounds`: 3
- `exit_condition`: `critical = 0 AND high = 0 AND medium = 0`
- `fix_targets`: `critical/high/medium`
- `advisory_targets`: `low`
- `agent_mapping`: `review = plan_review_agent`, `fix = implementation_agent`, `re-review = plan_review_agent`
- `low_policy`: Low findings are logged as advisory follow-up only. If a finding blocks C1-C8, classify it as Medium or higher.

Review focus:
- Does the plan remove ambiguity around `implementation_agent` dispatch?
- Does every producer output have a review-fix gate before implementation?
- Are Low findings consistently advisory?
- Are legacy aliases intentionally rejected rather than normalized?

## Test Strategy

- `mode`: inline
- `commands`:
  - `git diff --check`
  - `rg -n "(fix_targets|수정 대상)[^\\n]*(low|Low|critical/high/medium/low)" .codex/skills/sdd-autopilot .claude/skills/sdd-autopilot`
  - `rg -n -P "Codex agent_type\\*\\*: \`(implementation|implementation_review|spec_update_done)\`|(agent_type|subagent_type): *(implementation|implementation_review|implementation-review|implementation-plan|feature-draft|spec_update_done)(?![-_]agent)\\b" .codex/skills/sdd-autopilot`
  - `rg -n -P "(agent_mapping|review-fix mapping)[^\\n]*(review = implementation_review|fix = implementation\\b|re-review = implementation_review)" .codex/skills/sdd-autopilot .claude/skills/sdd-autopilot`
  - `rg -n -P "sdd-skills:(implementation-review|implementation-plan|feature-draft)(?!-agent)\\b" .claude/skills/sdd-autopilot`
  - `rg -n "plan_review_agent|dispatch controller|task당|advisory|canonical" .codex/skills/sdd-autopilot`
- `manual checks`:
  - Read sample A/B end to end and verify that each step has a closed gate before downstream execution.
  - Confirm `implementation_agent` never receives a whole phase as one task.
  - Confirm no legacy support is described as a feature.
  - Confirm Codex `agent_type`/`subagent_type`, review-fix mapping, and Claude subagent invocation examples reject legacy aliases instead of normalizing them.
  - Confirm normal planning prose may still use `feature-draft`/`implementation-plan`, and Claude canonical `sdd-skills:implementation-review-agent`, `sdd-skills:implementation-plan-agent`, `sdd-skills:feature-draft-agent` examples remain allowed.
- `reporting`: record command outputs and PASS/FAIL in `_sdd/implementation/test_results/test_results_sdd_autopilot_contract_hardening.md`.
