# Feature Draft: spec-summary whitepaper surface

<!-- spec-update-todo-input-start -->
# Part 1: Temporary Spec Draft

## Change Summary

`spec-summary`는 `_sdd/spec/summary.md`에 이 저장소의 reader-facing whitepaper를 작성한다. 이 문서는 프로젝트가 해결하는 문제, 배경과 동기, 핵심 설계, 코드 근거, 사용 흐름과 기대 결과를 한 문서에서 설명하고, 더 깊은 세부 surface로 자연스럽게 이어져야 한다. 관련 `_sdd/drafts/` 또는 `_sdd/implementation/` artifact가 있으면 계획·진행 상태는 맨 뒤의 짧은 appendix로만 덧붙인다.

## Scope Delta

### In Scope

- `spec-summary` skill contract를 reader-facing whitepaper 목적에 맞게 정의
- `.claude` / `.codex` mirror `SKILL.md`와 `skill.json` metadata 동기화
- summary template/example을 whitepaper 구조로 재배치
- `_sdd/spec/` supporting docs와 `docs/` canonical docs에서 `spec-summary`를 whitepaper surface로 설명
- `sdd-autopilot` reasoning reference 같은 downstream reference 동기화
- `DECISION_LOG.md`와 `logs/changelog.md`에 이 surface의 의미를 기록

### Out of Scope

- `spec-summary` 이름 변경
- `spec-summary`를 여러 스킬로 분리
- `_sdd/spec/main.md`의 thin core 구조 자체 재설계
- `guide-create`, `spec-create`, `spec-upgrade`의 역할 재정의
- 실제 프로젝트별 `_sdd/spec/summary.md` 본문 생성 자동화 beyond current skill flow

### Guardrail Delta

- `summary.md`는 현재 기준의 계약과 구조를 설명하는 whitepaper여야 한다
- 문서는 문제, 동기, 설계, 코드 근거, 사용과 기대 결과를 모두 다루되, 모든 reference detail을 장문 복제하지 않는다
- 핵심 설계 설명에는 구체적인 code grounding 또는 source path가 포함되어야 한다
- 사용 흐름과 기대 결과는 독자가 "어떻게 쓰고 무엇을 기대해야 하는가"를 빠르게 이해할 수 있을 정도로 충분해야 한다
- 계획·진행 상태는 있을 수 있지만 appendix 또는 마지막 보조 섹션이어야 한다
- 산출물은 과거 방식이나 변경 이력을 설명하지 않고 현재 상태를 바로 서술한다
- `.claude` / `.codex` mirror와 repo-level docs는 같은 의미를 유지해야 한다

## Contract/Invariant Delta

| ID | Type | Change | Why |
|----|------|--------|-----|
| C1 | Modify | `spec-summary`는 `_sdd/spec/summary.md`를 현재 저장소의 reader-facing whitepaper로 생성하거나 갱신해야 한다 | 사람이 프로젝트의 존재 이유와 설계 의도를 한 문서에서 빠르게 파악할 수 있어야 한다 |
| C2 | Modify | summary 본문은 최소한 `Executive Summary`, `Background / Motivation`, `Core Design`, `Code Grounding`, `Usage / Expected Results`, `Further Reading / References`를 포함해야 한다 | 문제, 동기, 설계, 코드 근거, 사용과 기대 결과를 함께 담는 whitepaper 구조를 확보해야 한다 |
| C3 | Modify | `Code Grounding`은 실제 코드 경로, 관련 함수/모듈, 또는 source table로 핵심 설계 설명을 구체적인 구현 근거와 연결해야 한다 | 문서가 코드와 직접 대화할 수 있어야 drift를 줄이고 탐색성을 높일 수 있다 |
| C4 | Modify | 관련 draft/implementation artifact가 있으면 `Planned / Progress Snapshot`을 appendix 또는 마지막 보조 섹션으로 붙일 수 있다 | 실행 신호는 유지하되 whitepaper 본문을 가리지 않게 해야 한다 |
| I1 | Add | summary는 과거 상태나 개편 서사를 쓰지 않고 현재 기준의 계약과 구조를 직접 설명한다 | reader-facing surface가 migration memo처럼 읽히지 않게 해야 한다 |
| I2 | Add | summary는 설명 책임과 reference 책임을 구분하며, 데이터 모델/API/환경 상세가 길어질 때는 관련 surface로 연결한다 | whitepaper 품질을 유지하면서도 문서 비대화를 막아야 한다 |
| I3 | Add | `.claude` / `.codex` mirror skill, template/example, `_sdd/spec/`, `docs/`, downstream reference는 `spec-summary = whitepaper surface` 의미를 일관되게 유지한다 | 일부 surface만 다른 의미를 가지면 호출 기대와 운영 기준이 다시 흔들린다 |

## Touchpoints

- `.codex/skills/spec-summary/SKILL.md`
  - `spec-summary`의 목표, AC, process, output contract를 whitepaper 기준으로 고정한다.
- `.claude/skills/spec-summary/SKILL.md`
  - mirror contract parity를 유지한다.
- `.codex/skills/spec-summary/skill.json`
  - trigger description과 metadata를 whitepaper 의미에 맞춘다.
- `.claude/skills/spec-summary/skill.json`
  - mirror metadata parity를 유지한다.
- `.codex/skills/spec-summary/references/summary-template.md`
  - whitepaper section order와 appendix semantics를 template에 반영한다.
- `.claude/skills/spec-summary/references/summary-template.md`
  - template parity 유지 대상이다.
- `.codex/skills/spec-summary/examples/summary-output.md`
  - final output example이 whitepaper tone과 section flow를 보여주게 한다.
- `.claude/skills/spec-summary/examples/summary-output.md`
  - example parity 유지 대상이다.
- `_sdd/spec/components.md`
  - `spec-summary` component 설명을 whitepaper surface 기준으로 정리한다.
- `_sdd/spec/usage-guide.md`
  - `/spec-summary` expected result를 whitepaper 산출물 기준으로 기술한다.
- `docs/SDD_SPEC_DEFINITION.md`
  - `spec-summary`의 역할을 문제/동기/설계/코드 근거/기대 결과를 다루는 surface로 연결한다.
- `docs/SDD_WORKFLOW.md`
  - workflow 안에서 `spec-summary`가 reader-facing whitepaper로 쓰이는 시점을 분명히 한다.
- `docs/en/SDD_SPEC_DEFINITION.md`
  - 영문 mirror 동기화 대상이다.
- `docs/en/SDD_WORKFLOW.md`
  - 영문 mirror 동기화 대상이다.
- `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md`
  - downstream taxonomy에서 `spec-summary`를 whitepaper surface로 설명한다.
- `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md`
  - mirror reference 동기화 대상이다.
- `_sdd/spec/DECISION_LOG.md`
  - `spec-summary` surface 정의와 운영 원칙을 남긴다.
- `_sdd/spec/logs/changelog.md`
  - 관련 파일과 contract version을 짧게 기록한다.

## Implementation Plan

1. `spec-summary`의 core contract와 metadata를 whitepaper 기준으로 고정한다.
   - Goal, Acceptance Criteria, SDD Lens, Process, Output Contract에서 reader-facing whitepaper 목적을 명시한다.
   - `skill.json` description과 version을 mirror에서 함께 맞춘다.
2. template과 example을 whitepaper spine에 맞게 재작성한다.
   - 핵심 section order, code grounding, appendix-style planned/progress snapshot을 반영한다.
3. repo-level human docs를 동기화한다.
   - `_sdd/spec/` supporting docs와 `docs/` canonical docs에 같은 의미를 반영한다.
4. downstream reference와 history surface를 마무리 동기화한다.
   - `sdd-autopilot` reasoning reference, `DECISION_LOG.md`, `logs/changelog.md`를 정리한다.

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, C2 | manual diff review | `SKILL.md`, template, example에 whitepaper section order와 목적이 명시되어 있는지 확인 |
| V2 | C3, I2 | manual read, targeted grep | summary template/example에 `Code Grounding`, source path, code citation guidance가 반영되어 있는지 점검 |
| V3 | C4, I1 | manual read | planned/progress 정보가 appendix 또는 마지막 보조 섹션으로 배치되고, 본문에 과거/변경 이력 설명이 없는지 확인 |
| V4 | I3 | mirror diff review, targeted grep | `.claude` / `.codex`, `_sdd/spec/`, `docs/`, autopilot reference에서 `spec-summary = whitepaper surface` 의미가 일치하는지 점검 |
| V5 | C1, C2, C3 | example review or local dry-run | example 또는 샘플 생성 결과를 읽었을 때 문제, 동기, 설계, 코드 근거, 사용 기대 결과를 바로 말할 수 있는지 확인 |

## Risks / Open Questions

- whitepaper 범위를 과도하게 넓히면 `_sdd/spec/main.md`나 guide/reference surface와 중복될 수 있다. section별 책임 경계를 문구로 분명히 해야 한다.
- `Code Grounding`을 너무 느슨하게 쓰면 whitepaper가 다시 일반 설명문이 될 수 있다. 최소한 concrete path 또는 source table을 강제하는 편이 안전하다.
- `Usage / Expected Results`를 너무 압축하면 human-readable value가 약해지고, 너무 확장하면 whitepaper 본문이 장황해질 수 있다. example에서 균형을 먼저 고정해야 한다.
- 현재 기준으로 추가 open question은 없다.
<!-- spec-update-todo-input-end -->

# Part 2: Implementation Plan

## Overview

이 작업의 산출물은 `_sdd/spec/summary.md`를 만드는 `spec-summary`의 reader-facing whitepaper contract 세트다. 결과적으로 사용자는 `/spec-summary`를 호출했을 때 프로젝트의 문제, 배경과 동기, 핵심 설계, 코드 근거, 사용 흐름과 기대 결과를 한 번에 읽을 수 있어야 하며, 필요하면 관련 draft/implementation 상태를 appendix로 확인할 수 있어야 한다.

## Scope

### In Scope

- `spec-summary` mirror skill 계약과 metadata 정렬
- summary template/example의 whitepaper 구조화
- `_sdd/spec/` supporting docs와 `docs/` canonical docs의 의미 정렬
- autopilot reference와 history surface 동기화

### Out of Scope

- `spec-summary` rename
- `_sdd/spec/main.md` core structure 변경
- 새로운 skill 추가 또는 skill 분리
- 실제 프로젝트 요약 내용을 각 프로젝트별로 생성하는 별도 automation 추가

## Components

| Component | Responsibility |
|-----------|----------------|
| Skill Contract | `spec-summary`의 whitepaper 목적, section expectation, appendix rule, current-state narration rule 정의 |
| Mirror Metadata | `.claude` / `.codex` `skill.json` description/version parity 유지 |
| Output Assets | template/example에 whitepaper section flow와 code grounding expectation 반영 |
| Repo Spec Docs | `_sdd/spec/components.md`, `_sdd/spec/usage-guide.md`에서 `spec-summary`의 역할 설명 |
| Canonical Docs | `docs/SDD_SPEC_DEFINITION.md`, `docs/SDD_WORKFLOW.md`, 영문 mirror에 whitepaper surface semantics 반영 |
| Downstream References | `sdd-autopilot` reference와 decision/changelog에 최종 의미 기록 |

## Contract/Invariant Delta Coverage

| Task | Covers | Validated By |
|------|--------|--------------|
| T1 | C1, C4, I1, I3 | V1, V3, V4 |
| T2 | C2, C3, I2 | V1, V2, V5 |
| T3 | C1, C2, I3 | V4 |
| T4 | I1, I3 | V3, V4 |

## Implementation Phases

### Phase 1: Core Contract Fixation

- `spec-summary`의 목적과 section contract를 skill 문서와 metadata에서 먼저 고정한다.
- 이 단계에서 whitepaper body와 appendix rule을 source-of-truth로 만든다.

### Phase 2: Output Surface Construction

- template과 example을 phase 1 계약에 맞게 재구성한다.
- `Code Grounding`과 `Usage / Expected Results` 품질 기준을 예시로 보여준다.

### Phase 3: Repo Docs Sync

- `_sdd/spec/` supporting docs와 `docs/` canonical docs에서 동일한 의미를 반복한다.
- 사용 시나리오와 component 설명이 whitepaper surface에 맞게 읽히도록 정리한다.

### Phase 4: Downstream and History Sync

- autopilot reference, decision log, changelog를 마무리 동기화한다.
- contract version과 touched-file history를 추적 가능하게 남긴다.

## Task Details

### Task T1: `spec-summary` mirror contract와 metadata를 whitepaper 기준으로 고정
**Component**: Skill Contract
**Priority**: P0
**Type**: Refactor

**Description**:  
`.codex`와 `.claude`의 `spec-summary` skill 문서에서 Goal, Acceptance Criteria, SDD Lens, Process, Output Contract를 reader-facing whitepaper 기준으로 작성한다. summary는 현재 상태를 직접 설명하는 문서로 정의하고, planned/progress 정보는 appendix 또는 마지막 보조 섹션으로만 취급한다. `skill.json` description도 같은 의미를 반영하고 version은 `3.0.0`으로 동기화한다.

**Acceptance Criteria**:
- [ ] `spec-summary`의 산출물이 reader-facing whitepaper임이 Goal과 AC에 명시된다
- [ ] 문제, 배경/동기, 핵심 설계, 코드 근거, 사용/기대 결과가 summary 본문의 필수 책임으로 드러난다
- [ ] planned/progress 정보가 appendix 또는 마지막 보조 섹션으로만 정의된다
- [ ] 현재 기준 설명만 허용하고 change-history narration을 배제하는 rule이 포함된다
- [ ] `.claude` / `.codex` `skill.json` description과 version이 `3.0.0`으로 맞춰진다

**Target Files**:
- [M] `.codex/skills/spec-summary/SKILL.md` -- whitepaper contract 정의
- [M] `.claude/skills/spec-summary/SKILL.md` -- mirror contract 동기화
- [M] `.codex/skills/spec-summary/skill.json` -- description/version 동기화
- [M] `.claude/skills/spec-summary/skill.json` -- description/version 동기화

**Technical Notes**: Covers C1, C4, I1, I3. 다른 surface는 이 task의 wording을 source-of-truth로 따른다.
**Dependencies**: 없음

### Task T2: template과 example을 whitepaper spine으로 재구성
**Component**: Output Assets
**Priority**: P0
**Type**: Refactor

**Description**:  
summary template과 example을 whitepaper section flow에 맞게 구성한다. `Executive Summary`, `Background / Motivation`, `Core Design`, `Code Grounding`, `Usage / Expected Results`, `Further Reading / References`를 기본 본문으로 두고, `Planned / Progress Snapshot`은 optional appendix로 둔다. example은 concrete path/source table을 포함해 code grounding의 밀도를 보여줘야 한다.

**Acceptance Criteria**:
- [ ] template이 whitepaper body와 optional appendix를 분명히 구분한다
- [ ] example에 `Code Grounding` 또는 동등한 concrete source section이 포함된다
- [ ] example을 읽었을 때 문제, 동기, 설계, 코드 근거, 사용 기대 결과를 바로 말할 수 있다
- [ ] planned/progress 정보가 example에서도 뒤쪽 appendix로만 배치된다
- [ ] `.claude` / `.codex` template/example이 같은 section flow를 유지한다

**Target Files**:
- [M] `.codex/skills/spec-summary/references/summary-template.md` -- whitepaper template 정의
- [M] `.claude/skills/spec-summary/references/summary-template.md` -- mirror template sync
- [M] `.codex/skills/spec-summary/examples/summary-output.md` -- whitepaper example 작성
- [M] `.claude/skills/spec-summary/examples/summary-output.md` -- mirror example sync

**Technical Notes**: Covers C2, C3, I2. section title wording은 human readability를 우선하되 mirror에서 동일하게 유지한다.
**Dependencies**: T1

### Task T3: supporting docs와 canonical docs에 whitepaper 의미를 동기화
**Component**: Repo Spec Docs / Canonical Docs
**Priority**: P1
**Type**: Refactor

**Description**:  
`_sdd/spec/components.md`, `_sdd/spec/usage-guide.md`, `docs/SDD_SPEC_DEFINITION.md`, `docs/SDD_WORKFLOW.md`, 그리고 영문 mirror에서 `spec-summary`를 reader-facing whitepaper surface로 설명한다. usage guide는 `/spec-summary`의 expected result를 whitepaper output 기준으로 기술하고, canonical docs는 문제/동기/설계/코드 근거/사용 기대 결과를 함께 다루는 surface라는 점을 분명히 한다.

**Acceptance Criteria**:
- [ ] `components.md`의 `spec-summary` 설명이 whitepaper 목적과 이유를 반영한다
- [ ] `usage-guide.md`의 `/spec-summary` expected result가 whitepaper section flow를 보여준다
- [ ] `docs/SDD_SPEC_DEFINITION.md`에서 `spec-summary`가 whitepaper 성격과 code grounding을 다루는 surface로 읽힌다
- [ ] `docs/SDD_WORKFLOW.md`에서 `spec-summary`가 reader-facing whitepaper로 사용되는 시점이 분명하다
- [ ] 영문 mirror 문서도 같은 의미를 유지한다

**Target Files**:
- [M] `_sdd/spec/components.md` -- component 설명 수정
- [M] `_sdd/spec/usage-guide.md` -- expected result 수정
- [M] `docs/SDD_SPEC_DEFINITION.md` -- canonical definition sync
- [M] `docs/SDD_WORKFLOW.md` -- workflow sync
- [M] `docs/en/SDD_SPEC_DEFINITION.md` -- English mirror sync
- [M] `docs/en/SDD_WORKFLOW.md` -- English mirror sync

**Technical Notes**: Covers C1, C2, I3. main.md는 이번 범위에서 직접 수정하지 않는다.
**Dependencies**: T1, T2

### Task T4: downstream reference와 history surface 마무리 동기화
**Component**: Downstream References
**Priority**: P1
**Type**: Refactor

**Description**:  
autopilot reasoning reference, decision log, changelog에서 `spec-summary`를 whitepaper surface로 읽도록 문구를 정리한다. `DECISION_LOG.md`는 운영 판단과 이유를 담고, `logs/changelog.md`는 관련 파일과 contract version을 짧게 기록한다.

**Acceptance Criteria**:
- [ ] autopilot reference가 `spec-summary`를 whitepaper surface로 설명한다
- [ ] `DECISION_LOG.md`가 surface 목적과 운영 원칙을 남긴다
- [ ] `logs/changelog.md`가 관련 파일과 contract version을 기록한다
- [ ] 모든 history surface가 현재 기준 의미를 중심으로 읽히며 migration memo처럼 장황해지지 않는다

**Target Files**:
- [M] `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md` -- downstream taxonomy sync
- [M] `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md` -- mirror taxonomy sync
- [M] `_sdd/spec/DECISION_LOG.md` -- decision 기록
- [M] `_sdd/spec/logs/changelog.md` -- changelog 기록

**Technical Notes**: Covers I1, I3. `DECISION_LOG`와 `changelog`는 역할을 분리해 중복 서술을 피한다.
**Dependencies**: T1

## Parallel Execution Summary

- T1은 source-of-truth wording을 고정하므로 선행돼야 한다.
- T2는 T1 완료 후 바로 진행 가능하다.
- T3와 T4는 모두 T1 이후 병렬 가능하다.
- T3는 T2의 section wording을 참조하면 더 매끄럽기 때문에 실무상 `T2 -> T3` 순서가 안정적이다.

## Risks and Mitigations

- Whitepaper 본문이 너무 두꺼워질 위험: `Code Grounding`과 `Further Reading / References`를 분리해 본문과 reference의 경계를 유지한다.
- Example이 너무 추상적으로 작성될 위험: concrete path 또는 source table을 example AC에 넣어 방지한다.
- Mirror drift 위험: T1 완료 직후 `.claude` / `.codex` diff를 검토하는 검증 단계를 고정한다.

## Open Questions

- 없음
