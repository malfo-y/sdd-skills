# Feature Draft: spec-update shared-core self-containment 정렬

<!-- spec-update-todo-input-start -->
# Part 1: Temporary Spec Draft

## Change Summary

이번 변경은 `spec-update-todo`와 `spec-update-done`을 최근 정리된 shared-core 철학에 더 직접 맞추는 소규모 contract alignment다.

핵심 목표는 두 update 계열 스킬이 이미 가지고 있는 thin global / persistent truth 중심 동작을 유지하면서도, 그 기준이 Acceptance Criteria, Hard Rules, Apply/Validate 단계, Final Check에서 더 self-contained하게 읽히도록 만드는 것이다.

이번 범위는 새 secondary axis를 추가하는 작업이 아니다. 대신 아래 네 가지를 더 직접 드러내도록 정리한다.

1. wrong-surface inflation 방지
2. planned truth와 implemented truth의 명시적 분리
3. 검증된 decision-bearing truth만 global spec으로 승격
4. main / supporting / history surface fit를 먼저 판단하는 update discipline

## Scope Delta

### In Scope

- `spec-update-todo`의 AC / Hard Rules / Process / Final Check를 shared-core 4축이 self-contained하게 읽히도록 보강
- `spec-update-done`의 AC / Hard Rules / Process / Final Check를 shared-core 4축이 self-contained하게 읽히도록 보강
- planned truth / implemented truth / verified truth 구분 문구를 더 직접 명시
- global main / supporting / history surface fit 판단 문구 보강
- `.claude` / `.codex` mirror skill, agent, `skill.json` version parity 정렬

### Out of Scope

- `spec-update-todo`, `spec-update-done`의 workflow position 자체 변경
- output format 대개편
- 새로운 shared checklist 파일 또는 reusable include 블록 추가
- `spec-create/review/rewrite/upgrade` 재수정
- `_sdd/spec/` supporting docs/history surface 수정

### Guardrail Delta

- update 계열은 global spec을 다시 두껍게 복구하는 도구가 아니다.
- `spec-update-todo`는 아직 구현되지 않은 계획을 implemented truth와 같은 표면에 무표식으로 섞지 않는다.
- `spec-update-done`는 구현되었다고 해도 feature-level contract/validation detail을 global 본문으로 과복원하지 않는다.
- 두 스킬 모두 무엇을 올릴지뿐 아니라 무엇을 global spec에 올리지 않을지도 명확히 판단해야 한다.
- shared-core 4축은 별도 블록이 아니라 각 스킬의 AC/Final Check에 흡수되어 self-contained하게 읽혀야 한다.

## Contract/Invariant Delta

| ID | Type | Change | Why |
|----|------|--------|-----|
| C1 | Modify | `spec-update-todo`는 planned persistent information만 올리고, planned truth와 implemented truth를 문단/불릿/섹션 수준에서 명시적으로 분리해야 한다 | update 단계에서 가장 흔한 오염은 미구현 계획과 현재 truth의 혼합이다 |
| C2 | Modify | `spec-update-done`는 검증된 decision-bearing truth만 global spec으로 승격하고, feature-level contract/validation/touchpoint detail의 과복원을 금지해야 한다 | 구현 완료 후에도 wrong-surface restoration이 쉽게 발생할 수 있다 |
| C3 | Modify | 두 update 계열 스킬은 AC, Apply/Validate 단계, Final Check에서 `Thinness`, `Decision-bearing truth`, `Anti-duplication`, `Navigation + surface fit`를 self-contained하게 읽히도록 표현해야 한다 | 상위 정의만 읽어야 이해되는 계약은 실행 시 drift가 생기기 쉽다 |
| I1 | Add | `spec-update-todo`는 main / supporting / history surface 중 어디에 planned information을 둘지 먼저 판단하고, wrong-surface placement를 피해야 한다 | planned update도 surface fit 판단이 먼저여야 thin global이 유지된다 |
| I2 | Add | `spec-update-done`는 IMPLEMENTED / PARTIAL / NOT_IMPLEMENTED / UNVERIFIED 판정 뒤, global spec에 올리지 않을 항목을 명시적으로 보류 또는 제외해야 한다 | 구현 sync는 반영보다 비반영 판단이 더 중요할 수 있다 |
| I3 | Add | `.claude` / `.codex` skill, agent, metadata는 동일한 update semantics와 versioning intent를 유지해야 한다 | runtime마다 update 기준이 달라지면 spec sync 결과가 흔들린다 |

## Touchpoints

- `.claude/agents/spec-update-todo.md`
  - planned truth / implemented truth separation, surface-fit 판단, Final Check 보강 대상이다.
- `.claude/skills/spec-update-todo/SKILL.md`
  - public wrapper contract도 agent와 같은 shared-core self-contained 표현을 가져야 한다.
- `.claude/skills/spec-update-todo/skill.json`
  - semantic contract change에 맞는 version bump 대상이다.
- `.codex/agents/spec-update-todo.toml`
  - Codex custom agent `developer_instructions` parity 대상이다.
- `.codex/skills/spec-update-todo/SKILL.md`
  - public wrapper parity 대상이다.
- `.codex/skills/spec-update-todo/skill.json`
  - version parity 대상이다.
- `.claude/agents/spec-update-done.md`
  - verified truth only, non-restoration rule, Final Check 보강 대상이다.
- `.claude/skills/spec-update-done/SKILL.md`
  - public wrapper contract parity 대상이다.
- `.claude/skills/spec-update-done/skill.json`
  - version bump 대상이다.
- `.codex/agents/spec-update-done.toml`
  - Codex custom agent parity 대상이다.
- `.codex/skills/spec-update-done/SKILL.md`
  - public wrapper parity 대상이다.
- `.codex/skills/spec-update-done/skill.json`
  - 현재 version drift가 있으므로 parity 정리 대상이다.

## Implementation Plan

1. `spec-update-todo`를 먼저 정렬한다.
   - planned truth / implemented truth 분리와 wrong-surface inflation 방지를 AC, Hard Rules, Apply 단계, Final Check에 직접 드러낸다.
2. `spec-update-done`를 이어서 정렬한다.
   - verified decision-bearing truth만 승격하고, 과복원 금지를 Compare / Apply / Validate / Final Check에 직접 드러낸다.
3. mirror와 metadata를 닫는다.
   - `.claude` / `.codex` wrapper, agent, `skill.json` version parity를 함께 맞춘다.
4. self-review로 두 스킬이 shared-core 4축을 직접 읽히게 되었는지 확인한다.

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, C3, I1 | manual diff review | `spec-update-todo` AC / Hard Rules / Apply / Final Check에 planned-vs-implemented separation, surface fit, thinness가 직접 드러나는지 확인 |
| V2 | C2, C3, I2 | manual diff review | `spec-update-done` AC / Compare / Apply / Validate / Final Check에 verified-truth-only, non-restoration, anti-duplication이 직접 드러나는지 확인 |
| V3 | I3 | mirror diff review | `.claude` / `.codex` skill과 agent가 같은 semantics를 유지하는지 확인 |
| V4 | I3 | metadata parity check | `skill.json` version이 두 플랫폼에서 같은 intent로 정렬되는지 확인 |
| V5 | C1, C2, C3, I1, I2 | end-to-end contract readthrough | 상위 정의 문서를 다시 펼치지 않아도 update 계열 두 스킬의 core discipline이 self-contained하게 읽히는지 검토 |

## Risks / Open Questions

- update 계열도 shared-core 4축을 직접 드러내야 하지만, create/review/rewrite/upgrade처럼 별도 secondary axis를 또 만들면 불필요하게 비대해질 수 있다. 이번 범위에서는 secondary axis를 추가하지 않고 공통 코어의 self-contained 표현만 보강하는 쪽이 안전하다.
- `spec-update-done`는 이미 Repo-wide Invariant Test와 drift typing이 충분히 강한 편이라, 이번 변경에서 가장 중요한 건 새 규칙 추가보다 “무엇을 반영하지 않을지”를 더 직접 드러내는 것이다.
- `spec-update-todo`는 planned marker 규칙이 이미 있으므로, 이번 변경의 핵심은 marker 추가보다 implemented truth와의 혼합 금지와 surface-fit 판단을 더 명시하는 데 있다.
- `skill.json` 버전은 `mirror parity 우선 + semantic contract change면 minor bump` 규칙을 따르는 것이 적절하다. 권장안은 두 스킬 모두 `2.4.0`으로 정렬하는 것이다.

### Resolved Decisions

- 이번 범위는 `spec-update-todo`와 `spec-update-done`만 대상으로 한다.
- 새 shared checklist 파일은 만들지 않는다.
- secondary axis는 추가하지 않는다.
- docs/supporting/history surface 수정은 이번 범위에서 제외한다.
- 버전은 semantic contract change 기준으로 minor bump를 권장한다.
<!-- spec-update-todo-input-end -->

# Part 2: Implementation Plan

## Overview

이번 구현은 update 계열 두 스킬의 contract를 최근 shared-core 철학에 맞게 소규모 정합성 패치하는 작업입니다. 목적은 동작을 바꾸기보다, 이미 의도된 동작이 AC / Process / Final Check에서 더 직접 읽히도록 만드는 것입니다.

성공 기준은 아래 다섯 가지입니다.

1. `spec-update-todo`가 planned truth와 implemented truth 분리를 더 직접 명시한다.
2. `spec-update-done`가 verified decision-bearing truth only / non-restoration rule을 더 직접 명시한다.
3. 두 스킬 모두 wrong-surface placement 방지 문구가 더 선명해진다.
4. `.claude` / `.codex` wrapper와 agent가 같은 semantics를 유지한다.
5. `skill.json` version drift가 해소된다.

## Scope

### In Scope

- update 계열 두 스킬의 agent / wrapper / metadata 수정
- shared-core 4축의 self-contained 표현 보강
- version parity 정리

### Out of Scope

- workflow 문서 수정
- `_sdd/spec/` supporting surface 수정
- 새로운 reference/example 자산 추가
- output format 대개편

## Components

| Component | Responsibility |
|-----------|----------------|
| Todo Update Contract | planned truth / implemented truth separation, surface fit, planned marker discipline를 고정한다 |
| Done Sync Contract | verified truth only, non-restoration, selective sync discipline를 고정한다 |
| Claude Mirrors | `.claude/agents/` + `.claude/skills/` contract parity를 유지한다 |
| Codex Mirrors | `.codex/agents/` + `.codex/skills/` contract parity를 유지한다 |
| Metadata Layer | `skill.json` version parity와 semantic-change signal을 정리한다 |

## Contract/Invariant Delta Coverage

| Task | Covers | Validated By |
|------|--------|--------------|
| T1 | C1, C3, I1 | V1, V5 |
| T2 | C2, C3, I2 | V2, V5 |
| T3 | I3 | V3, V4 |

## Implementation Phases

### Phase 1: Todo Contract Alignment

- `spec-update-todo`의 AC / Hard Rules / Process / Final Check를 self-contained하게 보강한다.

### Phase 2: Done Contract Alignment

- `spec-update-done`의 Compare / Apply / Validate / Final Check를 self-contained하게 보강한다.

### Phase 3: Mirror and Metadata Closure

- `.claude` / `.codex` mirror와 `skill.json` version parity를 닫는다.

## Task Details

### Task T1: Align `spec-update-todo` with shared-core self-containment
**Component**: Todo Update Contract  
**Priority**: P1  
**Type**: Refactor

**Description**: `spec-update-todo`의 Acceptance Criteria, Hard Rules, Process, Final Check를 다듬어 planned persistent truth only, planned-vs-implemented separation, wrong-surface inflation 방지, main/supporting/history surface fit 판단이 직접 드러나도록 만든다.

**Acceptance Criteria**:
- [ ] `spec-update-todo` AC에 planned truth only와 wrong-surface 방지 의도가 더 직접 드러난다.
- [ ] Apply 단계에 planned information의 surface-fit 판단과 non-duplication 의도가 반영된다.
- [ ] Final Check만 읽어도 thinness / separation / surface fit 확인이 가능하다.
- [ ] Claude / Codex agent와 wrapper가 같은 semantics를 유지한다.

**Target Files**:
- [M] `.claude/agents/spec-update-todo.md`
- [M] `.claude/skills/spec-update-todo/SKILL.md`
- [M] `.codex/agents/spec-update-todo.toml`
- [M] `.codex/skills/spec-update-todo/SKILL.md`

**Technical Notes**: Covers C1, C3, I1, validated by V1 and V5  
**Dependencies**: 없음

### Task T2: Align `spec-update-done` with verified-truth-only sync discipline
**Component**: Done Sync Contract  
**Priority**: P1  
**Type**: Refactor

**Description**: `spec-update-done`의 Acceptance Criteria, Compare Delta to Reality, Apply Updates, Validate Updates, Final Check를 다듬어 verified decision-bearing truth only, feature-level detail non-restoration, selective exclusion discipline가 직접 드러나도록 만든다.

**Acceptance Criteria**:
- [ ] `spec-update-done` AC에 verified-truth-only와 over-restoration 금지 의도가 더 직접 드러난다.
- [ ] Compare / Apply / Validate 단계에서 “무엇을 반영하지 않을지” 판단이 명시된다.
- [ ] Final Check만 읽어도 non-duplication / thinness / surface fit 확인이 가능하다.
- [ ] Claude / Codex agent와 wrapper가 같은 semantics를 유지한다.

**Target Files**:
- [M] `.claude/agents/spec-update-done.md`
- [M] `.claude/skills/spec-update-done/SKILL.md`
- [M] `.codex/agents/spec-update-done.toml`
- [M] `.codex/skills/spec-update-done/SKILL.md`

**Technical Notes**: Covers C2, C3, I2, validated by V2 and V5  
**Dependencies**: T1과 독립 구현 가능. 다만 phrasing consistency를 위해 review는 함께 진행

### Task T3: Close mirror metadata parity for update skills
**Component**: Metadata Layer  
**Priority**: P2  
**Type**: Infrastructure

**Description**: `spec-update-todo` / `spec-update-done`의 `.claude` / `.codex` `skill.json` version parity를 semantic-change 기준으로 정렬한다. 현재 `spec-update-done`의 Codex version drift도 함께 해소한다.

**Acceptance Criteria**:
- [ ] `spec-update-todo`의 `.claude` / `.codex` `skill.json` version이 동일하다.
- [ ] `spec-update-done`의 `.claude` / `.codex` `skill.json` version drift가 제거된다.
- [ ] semantic contract change 기준 minor bump rationale이 설명 가능하다.

**Target Files**:
- [M] `.claude/skills/spec-update-todo/skill.json`
- [M] `.codex/skills/spec-update-todo/skill.json`
- [M] `.claude/skills/spec-update-done/skill.json`
- [M] `.codex/skills/spec-update-done/skill.json`

**Technical Notes**: Covers I3, validated by V3 and V4  
**Dependencies**: T1, T2

## Parallel Execution Summary

- T1과 T2는 write set이 분리되어 있어 병렬 실행 가능하다.
- T3는 두 작업의 최종 semantics를 보고 version을 확정하는 편이 안전하므로 후행 순차 작업으로 두는 것이 적절하다.
- 전체 규모가 작아서 실제 실행은 병렬 2-way 후 metadata close 1-way 구성이 가장 단순하다.

## Risks and Mitigations

- AC/Final Check에 shared-core 표현을 너무 직접 옮기면 문장이 장황해질 수 있다.
  - Mitigation: checklist 이름을 반복 나열하기보다, thinness / verified truth / surface fit / non-duplication 의미가 자연어로 드러나게 쓴다.
- `spec-update-done`는 이미 강한 규칙이 많아 과도한 중복이 생길 수 있다.
  - Mitigation: 새 규칙 추가보다 Compare / Apply / Validate / Final Check에 의미를 재배치하는 방식으로 처리한다.
- version bump 판단이 애매할 수 있다.
  - Mitigation: `mirror parity + semantic contract change면 minor bump` 원칙으로 통일하고 두 스킬 모두 `2.4.0` 권장안을 사용한다.

## Open Questions

- 없음. 이번 범위는 contract self-containment 보강으로 충분하며, docs/supporting surface 변경은 별도 작업으로 분리한다.
