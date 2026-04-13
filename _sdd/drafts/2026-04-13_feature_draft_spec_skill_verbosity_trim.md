# Feature Draft: spec skill verbosity trim

<!-- spec-update-todo-input-start -->
# Part 1: Temporary Spec Draft

## Change Summary

이번 변경은 `spec-create`, `spec-review`, `spec-rewrite`, `spec-upgrade`, `spec-summary` 5개 스킬의 계약 의미를 바꾸지 않고, 내부 중복을 줄여 읽기 밀도를 낮추는 정리 패치다.

핵심 목표는 각 스킬에서 같은 기준이 `Acceptance Criteria`, `SDD Lens`, `Hard Rules`, `Process`, `Final Check`, companion asset에 반복 복제되는 패턴을 줄이고, 섹션별 역할을 다시 분리하는 것이다.

이번 라운드의 원칙은 다음과 같다.

1. `Acceptance Criteria`는 결과 기준 선언에 집중한다.
2. `SDD Lens`는 AC 반복이 아니라 철학/관점만 남긴다.
3. `Hard Rules`는 비가역 제약이나 금지 규칙만 남기고, AC와 완전히 같은 문장은 축약한다.
4. `Process`는 실행 시 필요한 구체 판단만 남긴다.
5. `Final Check`는 AC 전체 재서술이 아니라 `AC 충족 확인 + 추가 검증`으로 제한한다.
6. reference/example/checklist asset은 SKILL 본문을 다시 말하는 대신 보완 가치가 있어야 한다.

## Scope Delta

### In Scope

- `spec-create`의 `single-file default`, `repo-wide invariant`, `feature-level out-of-body` 반복을 줄이고 companion example과 역할을 분리
- `spec-review`의 AC/Hard Rules 중 동일 문장을 축약하고 review-only contract는 유지
- `spec-rewrite`의 body/log placement, rationale preservation 반복을 줄이고 `rewrite-checklist`, `rewrite-plan` stale 내용을 정리
- `spec-upgrade`의 upgrade-vs-rewrite boundary 판단을 Step 1 중심으로 재배치하고 `upgrade-mapping`은 보완 자산으로 축소
- `spec-summary`의 whitepaper shape, `Code Grounding`, history-narration 금지 반복을 줄여 섹션 역할을 다시 분리
- `.claude` / `.codex` mirror `SKILL.md`, 관련 agent, companion asset, `skill.json` version parity 정렬

### Out of Scope

- spec lifecycle의 공통 철학 자체 변경
- 새 secondary axis 추가
- `_sdd/spec/` 문서나 workflow docs 수정
- output format 자체 변경
- `spec-update-todo`, `spec-update-done`, `feature-draft` 계약 수정

### Guardrail Delta

- 이번 변경은 semantics-preserving verbosity trim이다. 핵심 동작이나 권한 경계는 바꾸지 않는다.
- AC에서 제거한 내용은 실제로 Hard Rule이나 Process에서만 필요할 때만 남긴다.
- companion asset은 SKILL 본문을 복제하지 않고, checklist/example/mapping으로서 독립 가치를 가져야 한다.
- `spec-review`는 다른 네 개보다 이미 상대적으로 압축되어 있으므로, 최소 수정 원칙을 적용한다.
- stale example은 단순 중복보다 우선순위가 높으므로 함께 정리한다.

## Contract/Invariant Delta

| ID | Type | Change | Why |
|----|------|--------|-----|
| C1 | Modify | 다섯 스킬은 AC/SDD Lens/Hard Rules/Process/Final Check의 역할을 더 분리해, 같은 의미를 2~5회 반복하지 않아야 한다 | self-contained를 유지하더라도 과도한 반복은 읽기 비용과 drift를 키운다 |
| C2 | Modify | `spec-create`는 `single-file default`와 `feature-level은 global core가 아니다`라는 판단을 source section에 집중시키고, `additional-specs`는 판단 질문의 재서술이 아니라 보완 예시로 남겨야 한다 | 현재는 본문과 example이 거의 같은 판단 질문을 반복한다 |
| C3 | Modify | `spec-review`는 evidence strictness와 read-only contract를 유지하되, AC와 Hard Rules가 같은 문장을 거의 그대로 반복하지 않아야 한다 | review contract는 유지해야 하지만, 동일 문장 중복은 줄일 수 있다 |
| C4 | Modify | `spec-rewrite`는 body/log placement와 rationale preservation의 source section을 선명히 하고, checklist는 검증 질문으로서만 보완 가치를 가져야 한다 | 현재는 본문 규칙을 checklist가 거의 그대로 되풀이한다 |
| C5 | Modify | `spec-upgrade`는 upgrade-vs-rewrite boundary judgment를 Step 1의 source-of-truth로 두고, 다른 섹션은 이를 참조하는 수준으로 축약해야 한다 | 경계 판정 규칙이 AC, Lens, Hard Rules, Process, mapping에 과분산되어 있다 |
| C6 | Modify | `spec-summary`는 whitepaper shape와 `Code Grounding` requirement를 유지하되, 같은 section list와 금지 규칙을 Goal/AC/Lens/Process/Final Check에 반복하지 않아야 한다 | 다섯 스킬 중 현재 verbosity 체감이 가장 크다 |
| I1 | Add | `.claude` / `.codex` mirror는 같은 trim strategy와 section responsibility를 유지해야 한다 | runtime별 phrasing drift를 막아야 한다 |
| I2 | Add | companion asset 수정은 duplication trim 또는 stale cleanup이 실제로 필요한 파일에만 제한한다 | 보조 자산까지 과잉 수정하면 범위가 불필요하게 커진다 |
| I3 | Add | wording compression만 일어나는 경우 versioning은 `mirror parity + patch bump`를 기본으로 본다 | semantic contract change와 단순 trim을 구분해야 한다 |

## Touchpoints

- `.claude/skills/spec-create/SKILL.md`
  - `single-file default`, repo-wide invariant, feature-level exclusion 반복 축소 대상
- `.codex/skills/spec-create/SKILL.md`
  - mirror parity 대상
- `.claude/skills/spec-create/examples/additional-specs.md`
  - `Default Shape First`가 본문 판단 질문을 반복하지 않도록 재작성 대상
- `.codex/skills/spec-create/examples/additional-specs.md`
  - mirror parity 대상
- `.claude/skills/spec-create/skill.json`
  - patch bump parity 대상
- `.codex/skills/spec-create/skill.json`
  - patch bump parity 대상
- `.claude/skills/spec-review/SKILL.md`
  - AC/Hard Rules의 동일 문장 축소 대상
- `.codex/skills/spec-review/SKILL.md`
  - mirror parity 대상
- `.claude/agents/spec-review.md`
  - public skill과 같은 review contract trim 반영 대상
- `.codex/agents/spec-review.toml`
  - mirror parity 대상
- `.claude/skills/spec-review/skill.json`
  - patch bump parity 대상
- `.codex/skills/spec-review/skill.json`
  - patch bump parity 대상
- `.claude/skills/spec-rewrite/SKILL.md`
  - body/log placement, rationale preservation 중복 축소 대상
- `.codex/skills/spec-rewrite/SKILL.md`
  - mirror parity 대상
- `.claude/skills/spec-rewrite/references/rewrite-checklist.md`
  - 질문형 검증 자산으로 남기되 본문 재진술을 줄이는 대상
- `.codex/skills/spec-rewrite/references/rewrite-checklist.md`
  - mirror parity 대상
- `.claude/skills/spec-rewrite/examples/rewrite-plan.md`
  - stale diagnosis axis 정리 대상
- `.codex/skills/spec-rewrite/examples/rewrite-plan.md`
  - mirror parity 대상
- `.claude/skills/spec-rewrite/skill.json`
  - patch bump parity 대상
- `.codex/skills/spec-rewrite/skill.json`
  - patch bump parity 대상
- `.claude/skills/spec-upgrade/SKILL.md`
  - boundary judgment의 source section 재배치 대상
- `.codex/skills/spec-upgrade/SKILL.md`
  - mirror parity 대상
- `.claude/skills/spec-upgrade/references/upgrade-mapping.md`
  - Step 1 보조 자산으로 축약 대상
- `.codex/skills/spec-upgrade/references/upgrade-mapping.md`
  - mirror parity 대상
- `.claude/skills/spec-upgrade/skill.json`
  - patch bump parity 대상
- `.codex/skills/spec-upgrade/skill.json`
  - patch bump parity 대상
- `.claude/skills/spec-summary/SKILL.md`
  - whitepaper shape, `Code Grounding`, history-narration 금지 반복 축소 대상
- `.codex/skills/spec-summary/SKILL.md`
  - mirror parity 대상
- `.claude/skills/spec-summary/skill.json`
  - patch bump parity 대상
- `.codex/skills/spec-summary/skill.json`
  - patch bump parity 대상

## Implementation Plan

1. 공통 trim policy를 먼저 적용한다.
   - 각 스킬에서 AC/SDD Lens/Hard Rules/Process/Final Check의 역할을 구분해 어떤 문장을 어디에 남길지 정한다.
2. 중복이 큰 스킬부터 순서대로 정리한다.
   - `spec-summary` -> `spec-create` -> `spec-upgrade` -> `spec-rewrite` -> `spec-review`
3. companion asset을 최소 범위로 정리한다.
   - `additional-specs`, `rewrite-checklist`, `rewrite-plan`, `upgrade-mapping`만 수정한다.
4. mirror와 metadata를 닫는다.
   - `.claude` / `.codex` skill, agent, `skill.json`을 같은 trim semantics와 patch bump로 맞춘다.

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, I1 | manual readthrough | 각 스킬에서 AC/Lens/Rules/Process/Final Check 역할이 분리되었는지 확인 |
| V2 | C2, I2 | diff review | `spec-create` 본문과 `additional-specs`가 더 이상 같은 판단 질문을 반복하지 않는지 확인 |
| V3 | C3, I1 | diff review | `spec-review` AC/Hard Rules가 동일 문장 반복 없이 review-only contract를 유지하는지 확인 |
| V4 | C4, I2 | diff review | `spec-rewrite` 본문과 `rewrite-checklist`의 중복이 줄고 `rewrite-plan` stale axis가 정리되었는지 확인 |
| V5 | C5, I2 | diff review | `spec-upgrade`에서 boundary judgment가 Step 1 중심으로 재배치되고 mapping은 보완 자산으로 남는지 확인 |
| V6 | C6, I1 | diff review | `spec-summary`의 whitepaper shape, `Code Grounding`, history-narration 금지가 유지되면서도 반복이 줄었는지 확인 |
| V7 | I1, I3 | mirror/version check | `.claude` / `.codex` `SKILL.md`, agent, `skill.json`이 같은 semantics와 patch bump intent를 가지는지 확인 |

## Risks / Open Questions

- self-contained contract를 너무 공격적으로 압축하면 실행 중 필요한 guardrail이 사라질 수 있다. 이번 범위에서는 `중복 제거`가 아니라 `source section 집중`만 한다.
- `spec-summary`는 whitepaper shape 자체가 section list를 포함하므로, 완전한 중복 제거는 불가능하다. 이번 라운드에서는 같은 리스트의 반복 횟수만 줄이는 것이 현실적이다.
- companion asset은 독립 가치가 있는 경우 중복처럼 보여도 일부 반복을 남길 수 있다. `rewrite-checklist`는 완전 삭제가 아니라 질문형 검증 자산으로서의 최소 반복만 허용한다.
- version 정책은 `mirror parity + wording compression only면 patch bump`가 적절하다. 권장 예시는 `spec-create 1.9.1`, `spec-review 2.3.1`, `spec-rewrite 1.10.1`, `spec-upgrade 1.10.1`, `spec-summary 3.0.1`이다.

### Resolved Decisions

- 이번 범위는 5개 스킬의 verbosity trim만 다룬다.
- 공통 철학이나 workflow position은 바꾸지 않는다.
- `_sdd/spec/` 문서와 workflow docs는 이번 구현 범위에서 제외한다.
- companion asset은 duplication trim이나 stale cleanup이 명확한 파일만 수정한다.
- `spec-review`는 최소 수정 원칙을 적용한다.
- `spec-review`의 허용 중복은 최대 2개 섹션까지만 인정한다.
- `spec-review`에서 `rubric separation`은 `AC + Process`, `evidence strictness`는 `AC + Hard Rules` 조합만 허용한다.
- `spec-review`의 read-only contract는 `Hard Rules` 단일 source-of-truth로 두고, AC에서는 제거한다.
- `spec-review`의 `Final Check`는 AC 재서술이 아니라 `AC 충족 확인 + rubric misclassification / weak-evidence leakage` 추가 검증만 남긴다.
- `spec-summary`와 `spec-create`는 우선 정리 대상으로 본다.
- versioning은 semantic change가 아니라면 patch bump를 기본으로 한다.
<!-- spec-update-todo-input-end -->

# Part 2: Implementation Plan

## Overview

이번 구현은 5개 spec 스킬의 contract를 더 짧고 읽기 쉽게 다듬는 문서 refactor입니다. 목표는 기능을 바꾸는 것이 아니라, 같은 의미가 여러 섹션에 복제된 부분을 줄이고 각 섹션이 자기 역할만 하도록 되돌리는 것입니다.

핵심 성공 기준은 세 가지입니다.

1. 같은 기준이 2~5회 반복되는 패턴이 줄어든다.
2. companion asset이 본문 재서술이 아니라 보완 자산으로 읽힌다.
3. mirror와 version metadata가 일관되게 정리된다.

## Scope

### In Scope

- 5개 스킬의 `SKILL.md` trim
- 필요한 companion asset trim/stale cleanup
- `spec-review` agent mirror trim
- `skill.json` patch bump 및 parity 정리

### Out of Scope

- 새로운 철학 추가
- 공통 docs 수정
- output format 변경
- spec update 계열 재수정

## Components

| Component | Responsibility |
|-----------|----------------|
| Section Responsibility Trim | AC/Lens/Rules/Process/Final Check의 역할을 다시 분리한다 |
| Create Asset Cleanup | `additional-specs`가 본문 반복이 아니라 예시가 되도록 조정한다 |
| Review Contract Trim | review-only contract는 유지하고 동일 문장 반복만 줄인다 |
| Rewrite Asset Cleanup | checklist/question value와 stale example를 정리한다 |
| Upgrade Boundary Trim | boundary judgment의 source section을 Step 1로 집중시킨다 |
| Summary Shape Trim | whitepaper shape와 grounding requirement를 유지하면서 반복만 줄인다 |
| Mirror Metadata | `.claude` / `.codex` parity와 patch bump를 맞춘다 |

## Contract/Invariant Delta Coverage

| Task | Covers | Validated By |
|------|--------|--------------|
| T1 | C6, I1, I3 | V1, V6, V7 |
| T2 | C2, I1, I2, I3 | V1, V2, V7 |
| T3 | C5, I1, I2, I3 | V1, V5, V7 |
| T4 | C4, I1, I2, I3 | V1, V4, V7 |
| T5 | C3, I1, I3 | V1, V3, V7 |

## Implementation Phases

### Phase 1: Highest-Impact Trim

- `spec-summary`와 `spec-create`를 먼저 줄인다.
- 가장 체감되는 반복을 먼저 줄여 전체 방향을 고정한다.

### Phase 2: Boundary and Asset Cleanup

- `spec-upgrade`와 `spec-rewrite`를 정리한다.
- source section과 companion asset의 역할 분리를 맞춘다.

### Phase 3: Conservative Review Cleanup

- `spec-review`를 최소 수정 원칙으로 정리한다.
- agent mirror와 metadata까지 함께 닫는다.

## Task Details

### Task T1: Trim repeated whitepaper-shape wording in `spec-summary`
**Component**: Summary Shape Trim  
**Priority**: P1  
**Type**: Refactor

**Description**: `spec-summary`에서 whitepaper section list, `Code Grounding`, history-narration 금지 문구가 Goal/AC/Lens/Process/Final Check에 반복되는 패턴을 줄인다.

**Acceptance Criteria**:
- [ ] whitepaper shape requirement는 유지된다.
- [ ] 같은 section list의 반복 횟수가 줄어든다.
- [ ] `Code Grounding` requirement는 남지만 동일 문장 반복은 줄어든다.
- [ ] Claude / Codex mirror가 같은 trim semantics를 유지한다.

**Target Files**:
- [M] `.claude/skills/spec-summary/SKILL.md`
- [M] `.codex/skills/spec-summary/SKILL.md`
- [M] `.claude/skills/spec-summary/skill.json`
- [M] `.codex/skills/spec-summary/skill.json`

**Technical Notes**: Covers C6, I1, I3, validated by V6 and V7  
**Dependencies**: 없음

### Task T2: Trim `spec-create` duplication and separate `additional-specs`
**Component**: Create Asset Cleanup  
**Priority**: P1  
**Type**: Refactor

**Description**: `spec-create`에서 `single-file default`, `repo-wide invariant`, `feature-level out-of-body` 반복을 줄이고, `additional-specs`는 본문 재서술이 아니라 split/supporting 예시로 재정렬한다.

**Acceptance Criteria**:
- [ ] `single-file default`의 source section이 더 선명해진다.
- [ ] `additional-specs`가 SKILL 본문 판단 질문을 그대로 반복하지 않는다.
- [ ] global core vs feature-level/supporting surface 경계는 유지된다.
- [ ] Claude / Codex mirror와 metadata가 정렬된다.

**Target Files**:
- [M] `.claude/skills/spec-create/SKILL.md`
- [M] `.codex/skills/spec-create/SKILL.md`
- [M] `.claude/skills/spec-create/examples/additional-specs.md`
- [M] `.codex/skills/spec-create/examples/additional-specs.md`
- [M] `.claude/skills/spec-create/skill.json`
- [M] `.codex/skills/spec-create/skill.json`

**Technical Notes**: Covers C2, I1, I2, I3, validated by V2 and V7  
**Dependencies**: 없음

### Task T3: Concentrate boundary judgment in `spec-upgrade`
**Component**: Upgrade Boundary Trim  
**Priority**: P1  
**Type**: Refactor

**Description**: `spec-upgrade`에서 upgrade-vs-rewrite boundary judgment를 Step 1의 source-of-truth로 집중시키고, Lens/Hard Rules/Validate/mapping은 참조형 표현으로 줄인다.

**Acceptance Criteria**:
- [ ] boundary judgment의 기준 문구가 Step 1에 집중된다.
- [ ] 다른 섹션은 Step 1 기준을 보완하거나 참조하는 수준으로 줄어든다.
- [ ] `upgrade-mapping`은 보완 자산으로 읽히고 본문 재진술이 줄어든다.
- [ ] Claude / Codex mirror와 metadata가 정렬된다.

**Target Files**:
- [M] `.claude/skills/spec-upgrade/SKILL.md`
- [M] `.codex/skills/spec-upgrade/SKILL.md`
- [M] `.claude/skills/spec-upgrade/references/upgrade-mapping.md`
- [M] `.codex/skills/spec-upgrade/references/upgrade-mapping.md`
- [M] `.claude/skills/spec-upgrade/skill.json`
- [M] `.codex/skills/spec-upgrade/skill.json`

**Technical Notes**: Covers C5, I1, I2, I3, validated by V5 and V7  
**Dependencies**: 없음

### Task T4: Trim `spec-rewrite` repetition and clean stale assets
**Component**: Rewrite Asset Cleanup  
**Priority**: P1  
**Type**: Refactor

**Description**: `spec-rewrite`의 body/log placement와 rationale preservation 반복을 줄이고, `rewrite-checklist`는 질문형 보조 자산으로 다듬으며, `rewrite-plan` example의 stale diagnosis axis를 현재 기준으로 정리한다.

**Acceptance Criteria**:
- [ ] body/log placement의 source section이 더 선명해진다.
- [ ] rationale preservation requirement는 유지되지만 반복은 줄어든다.
- [ ] `rewrite-checklist`가 본문 복제보다 검증 질문으로 읽힌다.
- [ ] `rewrite-plan` example의 stale axis가 제거된다.
- [ ] Claude / Codex mirror와 metadata가 정렬된다.

**Target Files**:
- [M] `.claude/skills/spec-rewrite/SKILL.md`
- [M] `.codex/skills/spec-rewrite/SKILL.md`
- [M] `.claude/skills/spec-rewrite/references/rewrite-checklist.md`
- [M] `.codex/skills/spec-rewrite/references/rewrite-checklist.md`
- [M] `.claude/skills/spec-rewrite/examples/rewrite-plan.md`
- [M] `.codex/skills/spec-rewrite/examples/rewrite-plan.md`
- [M] `.claude/skills/spec-rewrite/skill.json`
- [M] `.codex/skills/spec-rewrite/skill.json`

**Technical Notes**: Covers C4, I1, I2, I3, validated by V4 and V7  
**Dependencies**: 없음

### Task T5: Conservatively trim `spec-review` duplicate contract lines
**Component**: Review Contract Trim  
**Priority**: P2  
**Type**: Refactor

**Description**: `spec-review`에서 evidence strictness와 read-only contract를 유지하면서, AC/Hard Rules의 거의 동일한 문장만 최소 범위로 압축한다.

**Acceptance Criteria**:
- [ ] review-only contract와 severity discipline은 유지된다.
- [ ] AC와 Hard Rules의 완전 동일에 가까운 문장 반복이 줄어든다.
- [ ] Claude skill, Codex skill, Claude agent, Codex agent가 같은 semantics를 유지한다.
- [ ] metadata parity가 맞는다.

**Target Files**:
- [M] `.claude/skills/spec-review/SKILL.md`
- [M] `.codex/skills/spec-review/SKILL.md`
- [M] `.claude/agents/spec-review.md`
- [M] `.codex/agents/spec-review.toml`
- [M] `.claude/skills/spec-review/skill.json`
- [M] `.codex/skills/spec-review/skill.json`

**Technical Notes**: Covers C3, I1, I3, validated by V3 and V7  
**Dependencies**: 없음

## Parallel Execution Summary

- T1, T2, T3, T4는 write set이 분리되어 있어 병렬 실행 가능하다.
- T5는 `spec-review` agent mirror까지 포함하지만 write set이 독립적이므로 병렬 실행 가능하다.
- 다만 wording strategy consistency를 위해 먼저 T1 또는 T2에서 trim 스타일을 고정하고, 이후 나머지를 병렬로 퍼뜨리는 방식이 가장 안전하다.

## Risks and Mitigations

- 반복을 줄이다가 섹션별 self-contained성이 약해질 수 있다.
  - Mitigation: 완전 삭제가 아니라 source section 집중과 cross-reference 축약만 허용한다.
- companion asset을 과도하게 손보면 범위가 커질 수 있다.
  - Mitigation: duplication trim 또는 stale cleanup 근거가 명확한 파일만 수정한다.
- patch bump가 과소평가로 보일 수 있다.
  - Mitigation: 이번 범위가 semantics-preserving trim임을 implementation report에서 명확히 기록한다.

## Open Questions

- `spec-summary`는 summary-template까지 함께 줄일 필요가 있는지 추가 확인이 필요하다. 현재 사용자 리뷰는 SKILL 내부 중복 중심이므로 1차 범위에서는 template 수정 없이 갈 수 있다.
- `spec-review`는 실제 구현 전에 다시 한 번 “이 정도 반복은 허용” 기준을 정하고 들어가는 편이 안전하다.
