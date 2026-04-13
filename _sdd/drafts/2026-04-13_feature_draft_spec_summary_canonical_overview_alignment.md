# Feature Draft: spec-summary canonical overview 정렬

<!-- spec-update-todo-input-start -->
# Part 1: Temporary Spec Draft

## Change Summary

`spec-summary`를 "현재 상태 요약" 성격이 섞인 보조 스킬에서, `_sdd/spec/summary.md`를 생성하는 사람용 canonical overview 스킬로 재정렬한다.

이번 변경은 스킬 분리나 신규 surface 추가가 아니라, 기존 `spec-summary`의 계약을 더 날카롭게 다시 쓰는 작업이다. 토론 결과에 따라 global summary의 주역은 `목적 / 경계 / 핵심 결정 / 다음에 읽을 surface`가 되어야 하고, `status / issues / next steps`는 보조 섹션으로 내려가야 한다. 동시에 `summary.md`는 canonical human overview, `guide`는 기능별 deep explanation이라는 역할 분리를 repo 문서 전반에 반영해야 한다.

## Scope Delta

### In Scope

- `spec-summary`의 Goal, Acceptance Criteria, SDD Lens, Process를 canonical human overview 기준으로 재정의
- `.claude` / `.codex` mirror skill과 `skill.json` 메타데이터 정렬
- global summary template/example을 navigation-first 구조로 재배치
- optional planned/progress snapshot은 허용하되 보조 정보로만 다루도록 계약을 정리
- `_sdd/spec/` supporting surface와 `docs/` canonical 문서에 `summary.md` / `guide` 책임 경계 반영
- downstream reference(`sdd-autopilot` reasoning reference 등)의 설명 문구 동기화

### Out of Scope

- `spec-summary`를 둘 이상의 별도 스킬로 분리
- `guide-create` 자체의 목적이나 output contract 재설계
- 공통 코어 checklist를 다른 스킬들(`spec-create`, `spec-rewrite`, `spec-upgrade`, `spec-review`)에 실제로 삽입하는 작업
- `summary.md`의 실제 프로젝트별 내용 생성 자동화 이상으로, 새로운 runtime/tooling 추가

### Guardrail Delta

- global summary는 authoritative spec을 대체하지 않고, 사람이 `_sdd/spec/`를 어떤 관점으로 읽어야 하는지 안내하는 overview surface여야 한다
- global summary는 `개념 + 경계 + 결정 + 다음 읽을 surface`를 우선시하고, implementation/status 신호는 보조로만 다룬다
- planned/draft/implementation artifact가 있으면 `Planned / In Progress / Blocked / Next` 수준의 짧은 snapshot을 붙일 수 있지만, temporary spec 자체를 독립 요약 모드로 다루지 않는다
- `summary.md`와 `guide`는 모두 supporting surface이며, global decision-bearing truth를 장문 복제하지 않는다
- mirror skill과 repo-level human docs는 의미적으로 같은 계약을 유지해야 한다

## Contract/Invariant Delta

| ID | Type | Change | Why |
|----|------|--------|-----|
| C1 | Modify | `spec-summary`의 global mode는 `_sdd/spec/summary.md`를 `_sdd/spec/`용 canonical human overview로 생성해야 하며, generic current-state dashboard처럼 정의하지 않는다 | 토론에서 합의한 `summary.md`의 존재의의를 스킬 계약에 반영해야 한다 |
| C2 | Modify | global summary의 기본 shape는 `목적/개념`, `경계`, `핵심 결정`, `어디에 세부가 있는가`를 전면에 두고, `status / issues / next steps`는 보조 섹션으로 배치한다 | 사람이 global spec을 읽기 전에 올바른 판단과 다음 경로를 잡게 해야 한다 |
| C3 | Modify | `spec-summary`는 temporary spec을 독립 summary mode로 다루지 않고, 관련 `_sdd/drafts/` 또는 `_sdd/implementation/` artifact가 있을 때만 계획/진행 상태를 짧은 snapshot으로 보조 표기한다 | canonical overview의 대상과 기대 결과를 단순화하고 global/temporary 역할 충돌을 줄여야 한다 |
| I1 | Add | global summary는 main/global spec의 repo-wide truth를 복제 확장하지 않고 overview와 navigation 역할에 머물러야 한다 | `summary.md`가 다시 mini-spec으로 비대해지는 회귀를 막아야 한다 |
| I2 | Add | `.claude` / `.codex` mirror skill, template/example, `_sdd/spec/` supporting docs, `docs/` canonical 문서는 `summary.md = canonical overview`, `guide = deep explanation` 의미를 일관되게 유지해야 한다 | surface 책임 경계가 일부 문서에만 반영되면 drift가 재발한다 |
| I3 | Add | global summary 관련 설명 문구는 `상태를 빠르게 파악`보다 `목적/경계/결정/다음 surface를 빠르게 파악`에 무게를 둬야 한다 | human overview 역할이 status-heavy wording에 다시 가려지지 않게 해야 한다 |

## Touchpoints

- `.codex/skills/spec-summary/SKILL.md`
  - Codex 쪽 canonical skill contract. Goal/AC/Process wording을 가장 직접적으로 수정해야 한다.
- `.claude/skills/spec-summary/SKILL.md`
  - Claude mirror contract. Codex와 의미 parity를 유지해야 한다.
- `.codex/skills/spec-summary/skill.json`
  - 현재 `SKILL.md`와 버전/description drift가 있으므로 메타데이터를 동기화하고 `2.0.0`으로 함께 올려야 한다.
- `.claude/skills/spec-summary/skill.json`
  - mirror metadata parity와 trigger wording 정합성을 맞추고 `2.0.0`으로 함께 올려야 한다.
- `.codex/skills/spec-summary/references/summary-template.md`
  - global summary shape를 navigation-first canonical overview 구조로 재배치하고, optional planned/progress snapshot은 보조 섹션으로만 남겨야 한다.
- `.claude/skills/spec-summary/references/summary-template.md`
  - template parity 유지 대상이다.
- `.codex/skills/spec-summary/examples/summary-output.md`
  - 결과 예시가 status-heavy가 아니라 overview-first가 되도록 갱신하고, 계획/진행 상태는 짧은 snapshot 수준으로 제한해야 한다.
- `.claude/skills/spec-summary/examples/summary-output.md`
  - example parity 유지 대상이다.
- `_sdd/spec/components.md`
  - `spec-summary` 설명이 현재 "현재 스펙 상태" 중심이라 canonical overview 의미로 보정이 필요하다.
- `_sdd/spec/usage-guide.md`
  - Scenario 3b에서 `/spec-summary` expected result를 overview-first wording으로 갱신해야 한다.
- `docs/SDD_SPEC_DEFINITION.md`
  - `spec-summary`에 대한 선언을 "개념 + 경계 + 결정"에서 한 단계 더 나아가 overview/navigation 역할로 명시할 수 있다.
- `docs/SDD_WORKFLOW.md`
  - workflow 관점에서 global summary의 위치를 status sheet가 아니라 reading aid로 보정해야 한다.
- `docs/en/SDD_SPEC_DEFINITION.md`
  - 영문 mirror 동기화가 필요하다.
- `docs/en/SDD_WORKFLOW.md`
  - 영문 mirror 동기화가 필요하다.
- `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md`
  - downstream skill taxonomy/description에 `spec-summary`의 새 의미를 반영해야 한다.
- `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md`
  - mirror reference 동기화가 필요하다.
- `_sdd/spec/DECISION_LOG.md`
  - `spec-summary` semantics 재정의의 판단 근거를 남겨야 한다.
- `_sdd/spec/logs/changelog.md`
  - 문서/skill semantics 변경 파일 목록과 버전 변화를 짧게 남겨야 한다.

## Implementation Plan

1. `spec-summary`의 core contract를 먼저 재정의한다.
   - Goal, AC, SDD Lens, Process, Output Contract에서 global summary를 canonical human overview로 못 박는다.
   - temporary spec 독립 요약 모드는 제거하고, optional planned/progress snapshot만 보조적으로 허용한다.
   - 이 단계에서 mirror metadata drift(`skill.json` version/description)도 함께 정리하고 `.claude` / `.codex`를 `2.0.0`으로 맞춘다.
2. output surface 자산을 contract에 맞게 재배치한다.
   - template과 example에서 overview-first structure, delegated detail note, 보조 status/planned 섹션을 반영한다.
   - navigation 섹션명은 `Where Details Live`로 고정한다.
3. repo-level human docs를 동기화한다.
   - `_sdd/spec/` supporting surface와 `docs/` canonical 문서에 `summary.md` / `guide` 역할 분리를 명시한다.
   - `main.md`에는 supporting surface를 추가로 올리지 않는다.
4. downstream reference를 마무리 동기화한다.
   - `sdd-autopilot` reasoning reference처럼 간접 소비 지점의 설명 문구를 맞춘다.
   - `DECISION_LOG.md`와 `logs/changelog.md`를 모두 갱신해 semantic shift를 추적 가능하게 만든다.

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, C2, I1 | diff review | `SKILL.md`와 template/example에서 global summary가 overview-first structure인지 확인 |
| V2 | C3, I2 | mirror diff review, grep | `.claude` / `.codex` mirror, `docs/`, `_sdd/spec/`, downstream reference에서 `canonical overview + optional planned/progress snapshot` 의미와 surface 책임 표현이 일치하는지 확인 |
| V3 | I3 | targeted grep + manual read | `현재 프로젝트 상태 요약`, `현재 스펙 상태`, `기능 대시보드`, `global/temporary spec 요약` 같은 status-heavy wording이 overview-first wording으로 치환되었는지 점검 |
| V4 | C1, C2, C3, I1 | example review or local dry-run | example 또는 실제 `summary.md` 생성 결과를 사람이 읽었을 때 `목적 / 경계 / 핵심 결정 / 다음 surface`를 빠르게 말할 수 있는지 확인 |

## Risks / Open Questions

- `.codex/skills/spec-summary/skill.json`의 버전/description drift가 이미 존재하므로, mirror update 중 메타데이터 불일치가 다시 생길 위험이 있다.
- 기존 `temporary summary` 기대를 갖고 있던 사용자는 호출 결과 차이를 느낄 수 있으므로, usage/docs wording을 함께 바꿔 기대를 재설정해야 한다.
- `DECISION_LOG.md`와 `logs/changelog.md`를 둘 다 갱신하므로, 중복 서술이 아니라 판단 근거와 변경 이력을 역할 분리해서 써야 한다.

### Resolved Decisions

- `summary.md`를 `_sdd/spec/main.md`의 Supporting Surfaces 목록에 새로 올리지는 않는다.
- `.claude` / `.codex` `skill.json`은 `SKILL.md`와 같은 변경에서 함께 갱신하고 버전은 `2.0.0`으로 올린다.
- `DECISION_LOG.md`와 `_sdd/spec/logs/changelog.md`는 둘 다 갱신한다.
- navigation 섹션 명칭은 `Where Details Live`로 고정한다.
<!-- spec-update-todo-input-end -->

# Part 2: Implementation Plan

## Overview

이 변경은 `spec-summary`를 유지한 채 역할을 재정렬하는 문서/스킬 refactor다. 핵심 목적은 `_sdd/spec/summary.md`를 "현재 상태 요약"이 아니라 "사람이 global spec과 supporting surface를 어떤 관점으로 읽어야 하는지 가장 먼저 잡아주는 canonical overview"로 재정의하는 것이다.

구현의 성공 기준은 세 가지다.

1. `spec-summary` contract가 `global overview + optional planned/progress snapshot` 구조로 더 분명해질 것
2. output template/example이 overview-first shape를 보여줄 것
3. repo-level docs와 downstream references가 같은 의미를 반복하게 될 것
4. `skill.json 2.0.0`, `DECISION_LOG.md`, `logs/changelog.md`, `Where Details Live` 명칭이 명시 규칙대로 동기화될 것

## Scope

### In Scope

- `spec-summary` mirror skill 계약 개편
- template/example 개편
- `_sdd/spec/` supporting docs 및 `docs/` canonical 정의 보정
- downstream reference sync
- 필요 시 decision/changelog 기록

### Out of Scope

- 신규 skill 추가
- `guide-create` 재설계
- 다른 spec lifecycle 스킬의 checklist 삽입
- runtime automation 추가

## Components

| Component | Responsibility |
|-----------|----------------|
| Skill Contract | `spec-summary`의 Goal/AC/Process/Output semantics를 canonical overview 기준으로 재정의 |
| Mirror Metadata | `.claude` / `.codex` `skill.json` version/description drift 해소 및 `2.0.0` 동시 갱신 |
| Output Assets | template/example을 overview-first shape로 재배치하고 optional planned/progress snapshot을 보조 섹션으로 제한하며 `Where Details Live`를 사용 |
| Repo Spec Docs | `components.md`, `usage-guide.md` 등 supporting surface 정책 정리 |
| Canonical Docs | `docs/SDD_SPEC_DEFINITION.md`, `docs/SDD_WORKFLOW.md`, 영문 mirror의 의미 동기화 |
| Downstream References | autopilot reasoning reference 등 간접 소비 지점의 설명 갱신과 history docs 기록 |

## Contract/Invariant Delta Coverage

| Task | Covers | Validated By |
|------|--------|--------------|
| T1 | C1, C3, I2 | V1, V2 |
| T2 | C2, I1, I3 | V1, V4 |
| T3 | C1, C2, I2, I3 | V2, V3 |
| T4 | I2, I3 | V2, V3 |

## Implementation Phases

### Phase 1: Core Contract Alignment

- `spec-summary`의 core semantics를 mirror skill 문서와 metadata에서 먼저 고정한다.
- 이 단계에서 temporary spec 독립 summary 모드를 제거하고, optional planned/progress snapshot semantics만 남긴다.
- 이 phase가 끝나기 전에는 template/example이나 repo docs의 wording을 확정하지 않는다.

### Phase 2: Output Surface Reshape

- template/example을 phase 1 계약에 맞게 재배치한다.
- global overview 본체와 optional planned/progress snapshot의 주종 관계를 문서 구조에 반영한다.

### Phase 3: Repo Docs and Downstream Sync

- `_sdd/spec/` supporting docs, `docs/` canonical docs, downstream references를 새 semantics에 맞춰 동기화한다.
- 필요 시 decision/changelog까지 마무리해 semantic shift를 추적 가능하게 만든다.

## Task Details

### Task T1: `spec-summary` mirror contract와 metadata 재정의
**Component**: Skill Contract
**Priority**: P0
**Type**: Refactor

**Description**:  
`.codex`와 `.claude`의 `spec-summary` skill 문서에서 Goal, Acceptance Criteria, SDD Lens, Process, Output Contract를 canonical human overview 기준으로 다시 쓴다. temporary spec 독립 summary mode는 제거하고, 관련 draft/implementation artifact가 있을 때만 짧은 계획/진행 상태 snapshot을 보조적으로 붙일 수 있게 정의한다. 동시에 `skill.json` version/description drift를 정리해 메타데이터 parity를 맞추고 버전은 `2.0.0`으로 함께 올린다.

**Acceptance Criteria**:
- [ ] global summary가 `_sdd/spec/summary.md`용 canonical human overview임이 Goal과 AC에 명시된다
- [ ] temporary spec 독립 summary mode가 계약에서 빠지고, optional planned/progress snapshot만 보조 정보로 남는다
- [ ] `status / issues / next steps`가 보조 정보임이 skill contract에 반영된다
- [ ] `.claude` / `.codex` mirror 문서와 `skill.json` metadata가 의미적으로 정렬되고 버전이 `2.0.0`으로 맞춰진다

**Target Files**:
- [M] `.codex/skills/spec-summary/SKILL.md` -- Codex skill contract 재정의
- [M] `.claude/skills/spec-summary/SKILL.md` -- Claude mirror contract 동기화
- [M] `.codex/skills/spec-summary/skill.json` -- version/description drift 보정
- [M] `.claude/skills/spec-summary/skill.json` -- metadata parity 유지

**Technical Notes**: Covers C1, C3, I2, I3. `Goal/AC`를 먼저 바꾸고, 그 wording을 template/docs의 source로 삼는다.
**Dependencies**: 없음

### Task T2: template과 example을 overview-first output shape로 재배치
**Component**: Output Assets
**Priority**: P0
**Type**: Refactor

**Description**:  
summary template과 example을 새 계약에 맞춰 다시 구성한다. global summary에서는 `문제/개념`, `경계`, `핵심 결정`, `어디에 세부가 있는가`를 앞쪽에 두고, `status / issues / next steps` 또는 `planned/progress snapshot`은 마지막 보조 섹션으로 내린다. temporary spec 자체를 별도 summary shape로 제공하지 않도록 template 범위를 정리하고, navigation 섹션명은 `Where Details Live`로 통일한다.

**Acceptance Criteria**:
- [ ] template의 global summary 구조가 overview-first 순서를 따른다
- [ ] example이 사람이 읽고 `목적 / 경계 / 핵심 결정 / 다음 surface`를 빠르게 말할 수 있는 shape를 보여 준다
- [ ] status 정보는 global summary에서 보조 섹션으로 내려간다
- [ ] optional planned/progress snapshot이 있더라도 summary 본체보다 뒤에 위치한다
- [ ] navigation 섹션명이 `Where Details Live`로 통일된다
- [ ] `.claude` / `.codex` example/template이 같은 shape를 유지한다

**Target Files**:
- [M] `.codex/skills/spec-summary/references/summary-template.md` -- global overview + optional snapshot shape로 재배치
- [M] `.claude/skills/spec-summary/references/summary-template.md` -- mirror template sync
- [M] `.codex/skills/spec-summary/examples/summary-output.md` -- overview-first example로 갱신
- [M] `.claude/skills/spec-summary/examples/summary-output.md` -- mirror example sync

**Technical Notes**: Covers C2, I1, I2, I3, validated by V1 and V4. navigation section 명칭은 T1 wording에 맞춰 선택한다.
**Dependencies**: T1

### Task T3: repo-level spec docs와 usage surface를 canonical overview semantics로 동기화
**Component**: Repo Spec Docs
**Priority**: P1
**Type**: Refactor

**Description**:  
`_sdd/spec/`와 `docs/`에서 `spec-summary` 설명이 status-heavy wording에 머무르는 지점을 새 semantics로 교체한다. `components.md`와 `usage-guide.md`에서 `summary.md = canonical overview`, `guide = deep explanation`, `planned/progress snapshot = optional helper note` 분리를 명시한다. `summary.md`는 `_sdd/spec/main.md` Supporting Surfaces 목록에 새로 올리지 않는다.

**Acceptance Criteria**:
- [ ] `_sdd/spec/components.md`의 `spec-summary` 설명이 human overview 중심으로 바뀐다
- [ ] `_sdd/spec/usage-guide.md`의 `/spec-summary` expected result가 overview-first wording으로 바뀌고 계획/진행 상태는 optional snapshot으로 설명된다
- [ ] `docs/SDD_SPEC_DEFINITION.md`와 `docs/SDD_WORKFLOW.md`가 새 semantics를 지지한다
- [ ] 영문 mirror 문서가 의미상 같은 변경을 반영한다
- [ ] `_sdd/spec/main.md`를 수정하지 않아도 supporting surface semantics가 충분히 전달된다

**Target Files**:
- [M] `_sdd/spec/components.md` -- `spec-summary` 설명 보정
- [M] `_sdd/spec/usage-guide.md` -- scenario wording과 expected result 갱신
- [M] `docs/SDD_SPEC_DEFINITION.md` -- canonical definition wording 보정
- [M] `docs/SDD_WORKFLOW.md` -- workflow semantics wording 보정
- [M] `docs/en/SDD_SPEC_DEFINITION.md` -- 영문 mirror sync
- [M] `docs/en/SDD_WORKFLOW.md` -- 영문 mirror sync

**Technical Notes**: Covers C1, C2, I2, I3, validated by V2 and V3. `summary.md`는 supporting docs에서 충분히 설명하고, thin global main에는 새 surface를 추가로 올리지 않는다.
**Dependencies**: T1

### Task T4: downstream references와 change history를 마무리 동기화
**Component**: Downstream References
**Priority**: P2
**Type**: Refactor

**Description**:  
autopilot reasoning reference처럼 `spec-summary`를 간접 참조하는 문서를 갱신하고, `DECISION_LOG.md`와 `logs/changelog.md`에 semantic shift를 남긴다. 이 단계는 동작을 바꾸기보다는 downstream drift를 줄이는 마무리 sync 성격이다.

**Acceptance Criteria**:
- [ ] `sdd-autopilot` reference가 `spec-summary`를 status-heavy helper가 아니라 overview-oriented helper로 설명한다
- [ ] `.claude` / `.codex` reference wording이 맞춰진다
- [ ] `DECISION_LOG.md`에 판단 근거가 남는다
- [ ] `_sdd/spec/logs/changelog.md`에 변경 파일/버전 이력이 남는다

**Target Files**:
- [M] `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md` -- downstream description sync
- [M] `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md` -- mirror reference sync
- [M] `_sdd/spec/DECISION_LOG.md` -- semantics 변경 기록 필요 시 반영
- [M] `_sdd/spec/logs/changelog.md` -- release/doc log 필요 시 반영

**Technical Notes**: Covers I2 and I3, validated by V2 and V3. `DECISION_LOG.md`는 왜 바꿨는지, `changelog.md`는 무엇이 바뀌었는지로 역할을 분리한다.
**Dependencies**: T1, T3

## Parallel Execution Summary

- T1은 선행되어야 한다. `spec-summary`의 계약 문구가 확정되기 전에는 template/docs wording이 흔들릴 가능성이 높다.
- T2와 T3는 T1 이후 병렬 가능하다.
  - T2 write set: `spec-summary` template/example 자산
  - T3 write set: `_sdd/spec/`와 `docs/` surface
  - 의미적 의존성은 T1에만 걸려 있고, 서로의 write set은 겹치지 않는다.
- T4는 T3 이후가 안전하다.
  - downstream reference와 change history는 최종 wording을 받아 적는 성격이 강해, docs sync가 끝난 뒤에 처리하는 편이 drift를 줄인다.
- 병렬 실행 시에도 `.claude` / `.codex` mirror pair는 같은 task 안에서 함께 수정해야 한다. mirror를 분리 병렬화하면 parity drift 위험이 커진다.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| 기존 `temporary summary` 기대와 새 계약이 충돌함 | 사용자 기대와 문서 설명 mismatch 발생 | T1/T3에서 `global overview + optional planned/progress snapshot`으로 명확히 재정의하고 usage wording도 함께 수정한다 |
| mirror drift 재발 | `.claude` / `.codex` 계약 불일치 | mirror pair를 같은 task/phase에서 함께 수정하고 V2에서 diff review 수행 |
| `summary.md`가 mini-spec으로 비대화 | anti-duplication 원칙 훼손 | T2/T3에서 `status`를 보조로 내리고 delegated detail 위치를 명확히 적는다 |
| repo docs 일부만 바뀌어 downstream wording mismatch 발생 | human docs와 skill 계약 drift | T3/T4에서 `_sdd/spec/`, `docs/`, downstream reference를 함께 sync한다 |
| `skill.json` version/description drift가 놓침 | 배포/탐색 metadata 혼란 | T1 acceptance criteria에 metadata parity를 포함한다 |

## Open Questions

- 현재 없음
