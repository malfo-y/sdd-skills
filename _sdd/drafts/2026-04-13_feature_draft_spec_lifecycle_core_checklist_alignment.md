# Feature Draft: spec lifecycle 공통 코어 체크리스트 정렬

<!-- spec-update-todo-input-start -->
# Part 1: Temporary Spec Draft

## Change Summary

`spec-summary`의 reader-facing whitepaper 정렬은 이미 끝났고, 이번 변경의 초점은 나머지 spec lifecycle 4개 스킬(`spec-create`, `spec-review`, `spec-rewrite`, `spec-upgrade`)을 같은 철학 위에서 다시 맞추는 것이다.

토론 결과의 핵심은 두 가지다.

1. 공통 코어 checklist 4축(`Thinness`, `Decision-bearing truth`, `Anti-duplication`, `Navigation + surface fit`)은 `docs/SDD_SPEC_DEFINITION.md`에 source-of-truth로 둔다.
2. 실제 운용은 각 스킬이 self-contained하게 가져가야 하므로, 별도 `Shared Core Checklist` 블록을 새로 추가하기보다 각 스킬의 Acceptance Criteria와 Final Check에 흡수한다.

그 위에 각 스킬은 자기 역할이 가장 잘 드러나는 1차 추가 축을 하나씩 가진다.

- `spec-review`: global/temporary rubric separation + 조건부 `Critical`
- `spec-create`: 구조 선택 근거 + single-file default
- `spec-rewrite`: 근거 보존 + 본문 vs 로그 배치 원칙
- `spec-upgrade`: rewrite 경계 판정

## Scope Delta

### In Scope

- `docs/SDD_SPEC_DEFINITION.md`와 영문 mirror에 공통 코어 4축과 AC 반영 매핑 규칙 추가
- `spec-review` 계약을 rubric separation 중심으로 강화하고, severity 판정에서 false positive를 줄이는 규칙 반영
- `spec-create` 계약에 구조 선택 근거와 `single-file` 기본값을 명시
- `spec-rewrite` 계약에 rationale preservation과 `decision_log` / `rewrite_report` 배치 원칙 반영
- `spec-upgrade` 계약에 "이 작업이 upgrade인가 rewrite인가"를 먼저 가르는 경계 판정 추가
- `.claude` / `.codex` mirror skill과 metadata parity 정리
- `spec-review`의 agent mirror(`.claude/agents/spec-review.md`, `.codex/agents/spec-review.toml`) 동기화
- 필요한 reference/example/supporting doc/history surface 동기화

### Out of Scope

- 이미 구현 완료된 `spec-summary`의 추가 재설계
- `spec-update-todo`, `spec-update-done`, `feature-draft`, `implementation-plan` 계약 변경
- 공통 코어 checklist를 별도 독립 파일이나 별도 reusable include 블록으로 분리
- 각 스킬의 secondary checklist 축까지 과도하게 확장하는 작업
- global spec 구조 자체 재작성

### Guardrail Delta

- 공통 코어 checklist는 정의 문서에 규범 기준선으로 두되, 실행 단계에서는 각 스킬이 스스로 필요한 질문을 품고 있어야 한다
- 네 개 스킬 모두 global spec을 다시 old canonical 또는 inventory-heavy 구조로 두껍게 복구하지 않는다
- `spec-review`는 더 많이 지적하는 도구가 아니라, 맞는 rubric으로 정확히 지적하는 도구여야 한다
- `spec-create`는 premature multi-file split을 기본 경로로 두지 않는다
- `spec-rewrite`는 pruning 중심 도구가 아니라, 중요한 판단 근거를 보존한 구조 개선 도구여야 한다
- `spec-upgrade`는 legacy -> current model migration 도구이지, 대규모 구조 재편까지 흡수하는 우산 도구가 아니다
- mirror skill, agent, metadata, supporting docs는 같은 의미를 유지해야 한다

## Contract/Invariant Delta

| ID | Type | Change | Why |
|----|------|--------|-----|
| C1 | Modify | `docs/SDD_SPEC_DEFINITION.md`는 spec lifecycle 공통 코어 4축과 각 스킬 AC/Final Check 반영 매핑 규칙의 source-of-truth가 되어야 한다 | 공통 철학을 스킬 본문에만 분산시키면 drift가 커진다 |
| C2 | Modify | `spec-review`는 global/temporary rubric separation을 1차 추가 축으로 삼고, global spec 오염은 기본적으로 `Quality`, 문서 타입 혼동이나 잘못된 repo-wide truth 서술을 일으킬 때만 `Critical`로 승격해야 한다 | 잘못된 rubric 적용이 review 품질을 가장 크게 해친다 |
| C3 | Modify | `spec-create`는 구조 선택 근거를 명시해야 하며, 기본값은 `main.md` 단일 파일이고 분할은 필요성이 증명될 때만 허용해야 한다 | 생성 단계의 premature split은 이후 rewrite 비용을 키운다 |
| C4 | Modify | `spec-rewrite`는 pruning 과정에서 중요한 `Why`, rationale, citation, code excerpt header를 보존해야 하고, 본문에 과한 설명은 `decision_log` 또는 `rewrite_report`로 내려보내야 한다 | 문서를 얇게 만들다가 판단 근거를 잃는 회귀를 막아야 한다 |
| C5 | Modify | `spec-upgrade`는 migration 시작 전에 rewrite boundary를 판정해야 하며, 대규모 분할/재배치/역할 재설계가 필요하면 `spec-rewrite`로 분기해야 한다 | upgrade와 rewrite의 책임이 섞이면 두 스킬 모두 흐려진다 |
| I1 | Add | 공통 코어 4축은 각 스킬의 AC/Final Check 문구에 흡수되어 self-contained하게 읽혀야 하며, 별도 `Shared Core Checklist` 블록을 강제하지 않는다 | 실행 시 다른 문서를 전제로 하지 않아야 한다 |
| I2 | Add | `spec-review`의 public skill, Claude agent mirror, Codex custom agent는 동일한 review contract를 유지해야 한다 | review 기준이 runtime마다 달라지면 audit 결과가 흔들린다 |
| I3 | Add | `.claude` / `.codex` mirror `SKILL.md`와 `skill.json`은 동일한 semantics와 versioning intent를 유지해야 한다 | 현재도 metadata drift가 존재하므로 이번 변경에서 함께 정리해야 한다 |
| I4 | Add | supporting docs와 workflow docs는 네 개 스킬의 역할 차이를 "thin global 유지" 관점에서 다시 설명해야 한다 | 사용자와 에이전트가 읽는 설명 surface가 예전 의미를 유지하면 기대가 어긋난다 |

## Touchpoints

- `docs/SDD_SPEC_DEFINITION.md`
  - 공통 코어 4축과 AC 반영 매핑 규칙의 source-of-truth를 추가해야 한다.
- `docs/en/SDD_SPEC_DEFINITION.md`
  - 영문 mirror도 같은 규범 기준선을 가져야 한다.
- `docs/SDD_WORKFLOW.md`
  - review/create/rewrite/upgrade의 역할 차이를 workflow 관점에서 짧게 다시 정리해야 한다.
- `docs/en/SDD_WORKFLOW.md`
  - workflow 영문 mirror 동기화 대상이다.
- `.codex/skills/spec-review/SKILL.md`
  - rubric separation, conditional `Critical`, self-contained AC 반영이 가장 직접적으로 필요하다.
- `.claude/skills/spec-review/SKILL.md`
  - mirror contract parity 대상이다.
- `.claude/agents/spec-review.md`
  - Claude wrapper-backed agent contract도 동일하게 갱신해야 한다.
- `.codex/agents/spec-review.toml`
  - Codex custom agent의 `developer_instructions`가 public skill과 같은 semantics를 가져야 한다.
- `.codex/skills/spec-review/skill.json`
  - 현재 `.claude`와 버전 drift가 있으므로 metadata sync 대상이다.
- `.claude/skills/spec-review/skill.json`
  - description/keyword parity를 맞춰야 한다.
- `.codex/skills/spec-create/SKILL.md`
  - structure rationale과 `single-file default`를 AC/Structure Decision/Final Check에 녹여야 한다.
- `.claude/skills/spec-create/SKILL.md`
  - mirror contract parity 대상이다.
- `.codex/skills/spec-create/skill.json`
  - Codex version이 뒤처져 있으므로 metadata sync 대상이다.
- `.claude/skills/spec-create/skill.json`
  - mirror versioning alignment 대상이다.
- `.codex/skills/spec-create/examples/additional-specs.md`
  - multi-file이 허용되는 조건과 supporting file 분리 기준을 예시에서 더 분명히 할 필요가 있다.
- `.claude/skills/spec-create/examples/additional-specs.md`
  - example parity 대상이다.
- `.codex/skills/spec-rewrite/SKILL.md`
  - rationale preservation과 body-vs-log placement를 AC/Hard Rules/Process에 더 분명히 반영해야 한다.
- `.claude/skills/spec-rewrite/SKILL.md`
  - mirror contract parity 대상이다.
- `.codex/skills/spec-rewrite/skill.json`
  - Codex version drift 정리 대상이다.
- `.claude/skills/spec-rewrite/skill.json`
  - versioning alignment 대상이다.
- `.codex/skills/spec-rewrite/references/rewrite-checklist.md`
  - 공통 코어 4축과 rationale preservation 관점이 checklist에서 보이도록 조정해야 한다.
- `.claude/skills/spec-rewrite/references/rewrite-checklist.md`
  - mirror checklist 동기화 대상이다.
- `.codex/skills/spec-upgrade/SKILL.md`
  - rewrite boundary judgment를 Goal/AC/Process/Validate에 더 명확히 넣어야 한다.
- `.claude/skills/spec-upgrade/SKILL.md`
  - mirror contract parity 대상이다.
- `.codex/skills/spec-upgrade/skill.json`
  - Codex version drift 정리 대상이다.
- `.claude/skills/spec-upgrade/skill.json`
  - versioning alignment 대상이다.
- `.codex/skills/spec-upgrade/references/upgrade-mapping.md`
  - migration으로 해결 가능한 것과 rewrite로 넘겨야 할 것을 구분하는 매핑 보강이 필요하다.
- `.claude/skills/spec-upgrade/references/upgrade-mapping.md`
  - mirror mapping 동기화 대상이다.
- `_sdd/spec/components.md`
  - 네 개 스킬의 목적 설명을 새 semantics에 맞게 짧게 조정해야 한다.
- `_sdd/spec/usage-guide.md`
  - `/spec-create` expected result와 spec lifecycle 설명에 old canonical 잔재가 있어 정정이 필요하다.
- `_sdd/spec/DECISION_LOG.md`
  - 공통 코어 checklist 반영과 네 개 스킬 역할 조정의 판단 근거를 남겨야 한다.
- `_sdd/spec/logs/changelog.md`
  - 버전/파일 단위 변경 이력을 기록해야 한다.

## Implementation Plan

1. 정의 문서에서 규범 기준선을 먼저 고정한다.
   - `docs/SDD_SPEC_DEFINITION.md`와 영문 mirror에 공통 코어 4축과 AC 반영 매핑 규칙을 추가한다.
   - `docs/SDD_WORKFLOW.md`와 영문 mirror에는 각 스킬의 역할 차이를 짧게 다시 써서 downstream drift를 줄인다.
2. `spec-review`를 가장 먼저 정렬한다.
   - global/temporary rubric separation을 1차 축으로 명시하고, severity 기준에서 false positive를 줄이는 조건부 `Critical` 규칙을 넣는다.
   - public skill, Claude agent, Codex agent, metadata를 한 번에 동기화한다.
3. 생성/재구성/업그레이드 스킬을 각자 자기 축으로 조정한다.
   - `spec-create`: structure rationale + `single-file default`
   - `spec-rewrite`: rationale preservation + body/log placement
   - `spec-upgrade`: rewrite boundary judgment
   - 각 스킬의 mirror와 metadata, 필요한 reference/example 자산을 함께 정리한다.
4. supporting docs와 history surface를 마무리 sync한다.
   - `_sdd/spec/components.md`, `_sdd/spec/usage-guide.md`의 설명을 정리한다.
   - `DECISION_LOG.md`와 `logs/changelog.md`를 각각 판단 근거와 변경 이력 역할로 나눠 기록한다.

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, I1, I4 | manual diff review | `docs/SDD_SPEC_DEFINITION.md`와 영문 mirror에 공통 코어 4축과 AC 반영 매핑 규칙이 들어갔는지 확인 |
| V2 | C2, I2, I3 | mirror diff review, grep | `spec-review` public skill, Claude agent, Codex agent, `skill.json`이 같은 rubric separation과 conditional `Critical` semantics를 가지는지 확인 |
| V3 | C3, I1, I3 | manual review, grep | `spec-create` AC/Structure Decision/Final Check와 example에서 `single-file default`와 split rationale 요구가 보이는지 점검 |
| V4 | C4, I1, I3 | manual review, checklist review | `spec-rewrite` 본문과 rewrite checklist에서 rationale preservation, body/log placement, contamination control이 함께 보이는지 확인 |
| V5 | C5, I1, I3 | manual review, mapping review | `spec-upgrade` 본문과 upgrade mapping에서 rewrite boundary decision이 명시되고, rewrite로 넘길 조건이 분명한지 확인 |
| V6 | I3, I4 | targeted grep + docs review | `.claude` / `.codex` version/description drift와 supporting docs의 old canonical wording이 정리되었는지 확인 |
| V7 | C1, C2, C3, C4, C5 | end-to-end contract readthrough | 네 개 스킬을 연속해서 읽었을 때 공통 철학은 일관되고, 각 스킬의 1차 추가 축은 명확히 구분되는지 검토 |

## Risks / Open Questions

- `spec-review`의 secondary 축은 이번 라운드에서 `evidence strictness`로 고정하는 편이 안전하다. primary 축이 rubric separation인 만큼, 그 다음 우선순위는 weak-evidence finding을 줄이는 것이다. `reporting/actionability`는 기존 AC의 `next action` 요구로도 당장은 충분히 커버된다.
- `spec-create`, `spec-rewrite`, `spec-upgrade`에 secondary checklist 축까지 동시에 넣으면 AC와 Final Check가 다시 비대해질 위험이 크다. 이번 범위에서는 1차 추가 축만 계약화하고, secondary 축은 구현 후 review에서 실제 공백이 확인될 때만 후속으로 여는 것이 안전하다.
- `skill.json` version bump는 exact number 자체보다 mirror parity와 semantic change 반영이 우선이다. 권장 규칙은 `mirror parity 우선 + Goal/AC/Process 수준 변경이면 minor bump`이며, 구현 시 네 개 스킬 모두 이 규칙으로 정렬한다.
- `_sdd/spec/usage-guide.md`의 `/spec-create` expected result stale wording과 `spec-review` agent mirror sync는 선택형 open question이 아니라 이번 범위의 must-fix다. 둘 중 하나라도 누락되면 사용자-facing 설명 또는 runtime contract drift가 즉시 재발한다.

### Resolved Decisions

- 공통 코어 checklist는 별도 reusable 블록으로 만들지 않고 각 스킬 AC/Final Check에 흡수한다.
- 공통 코어 checklist의 source-of-truth는 `docs/SDD_SPEC_DEFINITION.md`와 영문 mirror에 둔다.
- 네 개 스킬의 1차 추가 축만 이번 변경의 계약 범위에 포함한다.
- `spec-review`는 네 개 중 가장 먼저 정렬한다.
- `spec-review`의 secondary 축은 이번 라운드에서 `evidence strictness`를 우선 채택한다.
- `spec-create`, `spec-rewrite`, `spec-upgrade`의 secondary 축은 이번 라운드 범위에서 제외한다.
- `skill.json` 버전은 mirror parity를 먼저 맞추고, semantic contract change가 있으면 minor bump로 올린다.
- history surface는 `DECISION_LOG.md`와 `logs/changelog.md`를 둘 다 갱신하되 역할을 분리한다.
<!-- spec-update-todo-input-end -->

# Part 2: Implementation Plan

## Overview

이 변경은 spec lifecycle 스킬들의 역할을 "thin global 유지" 철학 아래 다시 정렬하는 문서/스킬 refactor다. 핵심 목표는 네 개 스킬이 같은 공통 코어를 공유하되, 실행 시에는 각자 self-contained하게 읽히고, 동시에 자기 역할을 가장 잘 드러내는 1차 추가 축을 명시하도록 만드는 것이다.

성공 기준은 다음 다섯 가지다.

1. `docs/SDD_SPEC_DEFINITION.md`가 공통 코어 4축과 AC 반영 매핑 규칙의 기준 문서가 된다.
2. `spec-review`가 rubric separation 중심 audit 도구로 선명해진다.
3. `spec-create`, `spec-rewrite`, `spec-upgrade`가 각각 구조 선택 근거, 근거 보존, rewrite 경계 판정을 명시한다.
4. public skill, agent mirror, metadata, reference/example 자산이 같은 semantics를 유지한다.
5. 사용자-facing supporting docs와 history surface도 예전 의미를 남기지 않는다.

## Scope

### In Scope

- 정의/워크플로우 문서의 규범 기준선 보강
- `spec-review` skill + agent mirror refactor
- `spec-create`, `spec-rewrite`, `spec-upgrade` skill contract refactor
- 필요한 reference/example 자산 보정
- `.claude` / `.codex` metadata parity 정리
- supporting docs와 history surface sync

### Out of Scope

- `spec-summary` 재작업
- spec update 계열 스킬 계약 변경
- 새로운 공통 reference 파일 추가
- 1차 추가 축을 넘는 secondary checklist 확장
- global spec 본문 구조 개편

## Components

| Component | Responsibility |
|-----------|----------------|
| Canonical Definition | 공통 코어 4축과 AC/Final Check 매핑 규칙을 선언한다 |
| Workflow Docs | review/create/rewrite/upgrade의 역할 차이를 workflow 문맥에서 설명한다 |
| Review Contract | `spec-review`의 rubric separation, severity rule, mirror parity를 고정한다 |
| Create Contract | `spec-create`의 구조 선택 근거와 `single-file default`를 고정한다 |
| Rewrite Contract | `spec-rewrite`의 rationale preservation과 body/log placement를 고정한다 |
| Upgrade Contract | `spec-upgrade`의 rewrite boundary judgment를 고정한다 |
| Reference Assets | rewrite checklist, upgrade mapping, create example 등 보조 자산을 새 semantics에 맞춘다 |
| Repo Surface Sync | `components.md`, `usage-guide.md`, `DECISION_LOG.md`, `logs/changelog.md`를 동기화한다 |

## Contract/Invariant Delta Coverage

| Task | Covers | Validated By |
|------|--------|--------------|
| T1 | C1, I1, I4 | V1, V7 |
| T2 | C2, I2, I3 | V2, V7 |
| T3 | C3, I1, I3 | V3, V7 |
| T4 | C4, I1, I3 | V4, V7 |
| T5 | C5, I1, I3 | V5, V7 |
| T6 | I3, I4 | V6 |

## Implementation Phases

### Phase 1: Canonical Rule Alignment

- 정의 문서와 workflow 문서에서 규범 기준선을 먼저 고정한다.
- 이후 모든 skill refactor는 이 기준을 source-of-truth로 참조한다.

### Phase 2: Review Contract First

- `spec-review`를 가장 먼저 수정해 audit 기준을 선명히 한다.
- review 기준이 먼저 맞아야 create/rewrite/upgrade의 성공선도 흔들리지 않는다.

### Phase 3: Skill-Specific Axis Rollout

- `spec-create`, `spec-rewrite`, `spec-upgrade`를 각자 자기 축으로 수정한다.
- 각 task는 mirror `SKILL.md`, `skill.json`, 필요한 reference/example 자산까지 한 번에 닫는다.

### Phase 4: Surface and History Sync

- supporting docs와 history surface를 새 semantics에 맞게 정리한다.
- old canonical wording이나 stale component notes를 제거한다.

## Task Details

### Task T1: 정의 문서에 공통 코어 4축과 AC 반영 매핑 규칙 추가
**Component**: Canonical Definition / Workflow Docs  
**Priority**: P0  
**Type**: Refactor

**Description**:  
`docs/SDD_SPEC_DEFINITION.md`와 영문 mirror에 공통 코어 4축(`Thinness`, `Decision-bearing truth`, `Anti-duplication`, `Navigation + surface fit`)과 "각 spec lifecycle 스킬은 이를 AC/Final Check에 흡수해 self-contained하게 가져간다"는 매핑 규칙을 추가한다. 이어서 `docs/SDD_WORKFLOW.md`와 영문 mirror에 review/create/rewrite/upgrade의 역할 차이를 짧게 다시 정리해, downstream 문서가 예전 의미를 반복하지 않게 만든다.

**Acceptance Criteria**:
- [ ] 공통 코어 4축이 정의 문서에 명시된다
- [ ] 별도 shared block이 아니라 AC/Final Check 흡수 방식임이 명시된다
- [ ] `spec-review`, `spec-create`, `spec-rewrite`, `spec-upgrade` 각각의 1차 추가 축이 정의 문서나 workflow 문맥에서 읽힌다
- [ ] 영문 mirror 문서도 같은 의미를 유지한다

**Target Files**:
- [M] `docs/SDD_SPEC_DEFINITION.md` -- 공통 코어 4축과 매핑 규칙 추가
- [M] `docs/en/SDD_SPEC_DEFINITION.md` -- 영문 mirror sync
- [M] `docs/SDD_WORKFLOW.md` -- 네 개 스킬 역할 차이 보강
- [M] `docs/en/SDD_WORKFLOW.md` -- 영문 workflow mirror sync

**Technical Notes**: Covers C1, I1, I4. 이후 skill 본문 wording은 이 task를 source-of-truth로 따른다.
**Dependencies**: 없음

### Task T2: `spec-review`를 rubric separation 중심으로 재정의
**Component**: Review Contract  
**Priority**: P0  
**Type**: Refactor

**Description**:  
`spec-review`의 Acceptance Criteria, Review Dimensions, Severity rule, Final Check를 global/temporary rubric separation 중심으로 조정한다. global spec 오염은 기본적으로 `Quality`로 두고, 문서 타입을 잘못 읽게 만들거나 repo-wide truth를 틀리게 고정하는 경우에만 `Critical`로 올린다. public skill, Claude agent, Codex custom agent, metadata를 함께 동기화해 runtime drift를 막는다.

**Acceptance Criteria**:
- [ ] global/temporary rubric separation이 AC와 Review Dimensions에 명시된다
- [ ] `Critical`과 `Quality`의 경계가 false positive를 줄이는 방식으로 정리된다
- [ ] public skill, Claude agent, Codex agent가 같은 review contract를 가진다
- [ ] `.claude` / `.codex` `skill.json` metadata가 의미상 정렬된다

**Target Files**:
- [M] `.codex/skills/spec-review/SKILL.md` -- review contract 보강
- [M] `.claude/skills/spec-review/SKILL.md` -- mirror skill sync
- [M] `.claude/agents/spec-review.md` -- Claude agent contract sync
- [M] `.codex/agents/spec-review.toml` -- Codex custom agent instructions sync
- [M] `.codex/skills/spec-review/skill.json` -- version/description parity 보정
- [M] `.claude/skills/spec-review/skill.json` -- metadata parity 보정

**Technical Notes**: Covers C2, I2, I3, validated by V2. severity wording은 "오염 자체"보다 "잘못된 문서 타입/판단 유발" 여부에 묶는 편이 안전하다.
**Dependencies**: T1

### Task T3: `spec-create`에 구조 선택 근거와 `single-file default`를 고정
**Component**: Create Contract  
**Priority**: P0  
**Type**: Refactor

**Description**:  
`spec-create`의 Acceptance Criteria, Structure Decision, Process, Final Check를 조정해 "왜 이 구조를 골랐는가"를 명시하도록 한다. 기본값은 `_sdd/spec/main.md` 단일 파일이며, multi-file은 repo 성격과 split 필요성이 실제로 증명될 때만 허용한다. supporting file을 여는 예시 문서도 이 기본값을 흔들지 않도록 정리한다.

**Acceptance Criteria**:
- [ ] 구조 선택 근거가 AC 또는 Final Check에 명시된다
- [ ] `single-file default`와 conditional multi-file 원칙이 분명해진다
- [ ] supporting file 분리는 정말 필요한 경우에만 열린다는 점이 예시에서도 읽힌다
- [ ] `.claude` / `.codex` mirror와 metadata가 같은 semantics를 유지한다

**Target Files**:
- [M] `.codex/skills/spec-create/SKILL.md` -- structure rationale + single-file default 반영
- [M] `.claude/skills/spec-create/SKILL.md` -- mirror skill sync
- [M] `.codex/skills/spec-create/skill.json` -- version/description parity 보정
- [M] `.claude/skills/spec-create/skill.json` -- metadata parity 보정
- [M] `.codex/skills/spec-create/examples/additional-specs.md` -- supporting file opening 조건 정리
- [M] `.claude/skills/spec-create/examples/additional-specs.md` -- mirror example sync

**Technical Notes**: Covers C3, I1, I3. simple project example은 이미 single-file 예시라 필수 수정 대상은 아니고, multi-file opening example만 정리해도 충분하다.
**Dependencies**: T1, T2

### Task T4: `spec-rewrite`에 근거 보존과 본문/로그 배치 원칙 반영
**Component**: Rewrite Contract / Reference Assets  
**Priority**: P0  
**Type**: Refactor

**Description**:  
`spec-rewrite` 본문에서 문서를 얇게 만드는 것보다 중요한 것이 무엇인지 더 분명히 한다. 중요한 `Why`, rationale, citation, code excerpt header는 보존해야 하고, 본문에 과한 설명은 `decision_log` 또는 `rewrite_report`로 이동시킨다는 배치 원칙을 AC/Hard Rules/Process에 명시한다. rewrite checklist도 같은 질문을 하도록 보강한다.

**Acceptance Criteria**:
- [ ] AC와 Hard Rules가 rationale preservation을 분명히 요구한다
- [ ] 본문에 남길 최소 rationale과 로그로 내릴 정리 메모의 경계가 설명된다
- [ ] rewrite checklist가 공통 코어와 rationale preservation을 함께 점검한다
- [ ] `.claude` / `.codex` mirror와 metadata가 같은 semantics를 유지한다

**Target Files**:
- [M] `.codex/skills/spec-rewrite/SKILL.md` -- rationale preservation과 placement rule 반영
- [M] `.claude/skills/spec-rewrite/SKILL.md` -- mirror skill sync
- [M] `.codex/skills/spec-rewrite/skill.json` -- version/description parity 보정
- [M] `.claude/skills/spec-rewrite/skill.json` -- metadata parity 보정
- [M] `.codex/skills/spec-rewrite/references/rewrite-checklist.md` -- checklist 보강
- [M] `.claude/skills/spec-rewrite/references/rewrite-checklist.md` -- mirror checklist sync

**Technical Notes**: Covers C4, I1, I3, validated by V4. "줄 수 줄이기"보다 "판단 근거를 잃지 않는 구조 개선"이 핵심임을 반복해야 한다.
**Dependencies**: T1, T2

### Task T5: `spec-upgrade`에 rewrite boundary judgment 추가
**Component**: Upgrade Contract / Reference Assets  
**Priority**: P0  
**Type**: Refactor

**Description**:  
`spec-upgrade`가 legacy -> current model migration에 집중하도록, 시작 단계에서 "이 작업이 upgrade로 닫히는가, rewrite로 넘겨야 하는가"를 먼저 판정하게 한다. 대규모 분할, index/support 역할 재설계, 광범위한 section 재배열 같은 구조 재편은 `spec-rewrite`로 분기한다는 규칙을 AC/Process/Validate와 upgrade mapping reference에 반영한다.

**Acceptance Criteria**:
- [ ] rewrite boundary judgment가 Goal/AC/Process에 명시된다
- [ ] 구조 재편이 필요한 조건과 rewrite로 넘겨야 하는 조건이 분명하다
- [ ] upgrade mapping reference가 migration vs rewrite 구분을 지원한다
- [ ] `.claude` / `.codex` mirror와 metadata가 같은 semantics를 유지한다

**Target Files**:
- [M] `.codex/skills/spec-upgrade/SKILL.md` -- rewrite boundary judgment 반영
- [M] `.claude/skills/spec-upgrade/SKILL.md` -- mirror skill sync
- [M] `.codex/skills/spec-upgrade/skill.json` -- version/description parity 보정
- [M] `.claude/skills/spec-upgrade/skill.json` -- metadata parity 보정
- [M] `.codex/skills/spec-upgrade/references/upgrade-mapping.md` -- migration vs rewrite mapping 보강
- [M] `.claude/skills/spec-upgrade/references/upgrade-mapping.md` -- mirror mapping sync

**Technical Notes**: Covers C5, I1, I3, validated by V5. upgrade가 rewrite를 잠식하지 않도록 "언제 멈추고 넘길 것인가"를 문서에 먼저 못 박는다.
**Dependencies**: T1, T2

### Task T6: supporting docs와 history surface를 새 semantics로 동기화
**Component**: Repo Surface Sync  
**Priority**: P1  
**Type**: Refactor

**Description**:  
`_sdd/spec/components.md`와 `_sdd/spec/usage-guide.md`에서 네 개 스킬 설명을 새 semantics에 맞게 갱신한다. 특히 `/spec-create` expected result에 남아 있는 old canonical wording을 thin global 기준으로 바로잡는다. 마지막으로 `DECISION_LOG.md`에는 판단 근거를, `logs/changelog.md`에는 touched files와 version change를 남겨 semantic shift를 추적 가능하게 만든다.

**Acceptance Criteria**:
- [ ] `components.md`의 네 개 스킬 설명이 새 역할 차이를 반영한다
- [ ] `usage-guide.md`의 `/spec-create` expected result가 thin global 기준으로 수정된다
- [ ] `DECISION_LOG.md`와 `logs/changelog.md`가 역할 분리된 방식으로 갱신된다
- [ ] supporting docs가 예전 semantics를 반복하지 않는다

**Target Files**:
- [M] `_sdd/spec/components.md` -- skill purpose/notes 보정
- [M] `_sdd/spec/usage-guide.md` -- `/spec-create` expected result와 lifecycle 설명 정정
- [M] `_sdd/spec/DECISION_LOG.md` -- 판단 근거 기록
- [M] `_sdd/spec/logs/changelog.md` -- 변경 이력 기록

**Technical Notes**: Covers I3, I4, validated by V6. `_sdd/spec/main.md`는 이번 범위에서 직접 수정하지 않는다.
**Dependencies**: T2, T3, T4, T5

## Parallel Execution Summary

- `T1`은 선행 작업이다. 공통 기준선이 여기서 고정된다.
- `T2`는 논리적으로 먼저 끝내는 편이 안전하다. review 기준이 anchor 역할을 하기 때문이다.
- `T3`, `T4`, `T5`는 `T1`과 `T2` 이후 병렬 실행이 가능하다.
  - `spec-create`, `spec-rewrite`, `spec-upgrade`는 서로 다른 디렉터리를 주로 수정한다.
  - 다만 versioning wording이나 공통 코어 표현은 `T1`의 문구를 그대로 따라야 한다.
- `T6`은 후행 통합 작업이다. 앞선 task들의 wording이 확정된 뒤 실행해야 supporting docs/history가 다시 drift하지 않는다.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| 공통 코어를 너무 길게 서술해 AC가 비대해짐 | self-contained는 되지만 읽기 비용이 커짐 | 각 스킬에는 질문형/판정형 문구로 압축하고, 정의 문서에만 전체 기준선을 둔다 |
| `spec-review` severity rule이 지나치게 느슨해짐 | 실제 중요한 오염을 놓칠 수 있음 | `문서 타입 혼동`과 `잘못된 repo-wide truth`는 명확히 `Critical`로 유지한다 |
| `spec-create`에서 multi-file 기준이 모호하게 남음 | 이후 rewrite 비용이 다시 커짐 | `single-file default`를 AC/Structure Decision/Final Check 모두에 반복 반영한다 |
| `spec-rewrite`가 여전히 pruning 중심으로 오해될 수 있음 | 판단 근거가 유실될 수 있음 | skill 본문과 rewrite checklist에 rationale preservation을 모두 넣는다 |
| `spec-upgrade`가 rewrite 경계를 넘어서 과도하게 일함 | 역할 중복과 산출물 불안정이 생김 | upgrade mapping reference에 rewrite trigger 예시를 넣어 early exit를 돕는다 |
| mirror/agent/metadata 중 일부만 갱신됨 | 플랫폼별 drift 재발 | task 단위에서 mirror와 metadata를 함께 닫도록 Target Files를 묶는다 |

## Open Questions

- `spec-review`의 secondary 축은 `evidence strictness`와 `reporting/actionability` 중 어느 쪽이 더 우선인지 아직 미결이다.
- `spec-create`, `spec-rewrite`, `spec-upgrade`도 secondary 축을 붙일 수 있지만, 이번 라운드에서 추가할지 여부는 구현 후 AC 길이와 명확성을 보고 다시 판단하는 편이 안전하다.
- 네 개 스킬의 exact version bump를 각각 어디까지 올릴지는 현재 `skill.json` drift 정리 방식과 함께 마지막에 결정하는 편이 낫다.
