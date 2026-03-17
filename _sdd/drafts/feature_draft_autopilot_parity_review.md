# Feature Draft: Autopilot Parity Review and Restoration

**Date**: 2026-03-17
**Author**: Codex
**Target Spec**: main.md
**Status**: Draft
**Features**: Codex/Claude autopilot parity audit, gap classification, restoration plan

---

<!-- spec-update-todo-input-start -->
# Part 1: Spec Patch Draft

> 이 패치는 해당 스펙 섹션에 copy-paste하거나,
> `spec-update-todo` 스킬의 입력으로 사용할 수 있습니다.

# Spec Update Input

**Date**: 2026-03-17
**Author**: Codex
**Target Spec**: `_sdd/spec/main.md`
**Spec Update Classification**: SHOULD update

## Background & Motivation Updates

### Background Update: Codex autopilot parity 검증 절차 명시 필요
**Target Section**: `_sdd/spec/main.md` > `배경 및 동기 (§1)`
**Change Type**: Problem Statement / Motivation / Governance

**Current**:
Codex용 `sdd-autopilot`은 이미 추가되었지만, Claude Code의 `sdd-autopilot`과 어떤 항목을 기준으로 동등성을 비교하고, 어떤 차이를 의도적 divergence로 인정하며, 어떤 차이를 결함으로 분류할지에 대한 공식 검토 절차는 문서화되어 있지 않다.

**Proposed**:
Codex/Claude autopilot parity review를 정기 또는 변경 후 검증 단계로 정의한다. 비교 대상은 최소한 다음을 포함한다.
- `.codex/skills/sdd-autopilot/SKILL.md`
- `.codex/skills/sdd-autopilot/references/pipeline-templates.md`
- `.codex/skills/sdd-autopilot/references/scale-assessment.md`
- `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md`
- `.claude/skills/sdd-autopilot/`의 대응 파일들

또한 비교 결과는 `동등`, `의도적 차이`, `빠짐`, `잘못된 번역/치환`, `문서 드리프트` 중 하나로 분류한다.

**Reason**:
현재 Codex쪽은 구조 이식이 빠르게 진행되었기 때문에, 본문/참조/예시/agent 연결이 Claude 원본 의도와 동일한지 체계적으로 검토할 필요가 있다. parity review 기준이 없으면 수정이 누적될수록 드리프트를 놓치기 쉽다.

---

## Design Changes

### Design Change: autopilot parity audit을 공식 검토 단계로 추가
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `핵심 설계 (§2)`
**Change Type**: Governance / Design Rationale

**Description**:
`sdd-autopilot` 변경 후에는 Codex와 Claude의 대응 autopilot skill 세트를 비교 검토하는 절차를 수행한다. 이 절차는 단순 diff가 아니라, “의미 보존 여부”를 평가하는 구조적 검토다.

기본 비교 축:
- workflow position / trigger / when-to-use
- step 0~8 process
- inline discussion / clarification 방식
- scale assessment 기준
- generated orchestrator format
- review-fix loop, test/debug, error handling
- resume / partial execution / archive lifecycle
- file-based handoff / artifact contract
- generated orchestrator가 실제 Codex custom agents와 연결되는지

**Impact**:
- Codex autopilot 품질을 Claude 기준과 지속적으로 비교 가능
- 기능 추가와 문서 드리프트를 분리해서 판단 가능
- 향후 regression review 체크리스트로 재사용 가능

### Design Change: parity review 결과 분류 체계 도입
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `핵심 설계 (§2)` > `Design Patterns`
**Change Type**: Governance / Logic Flow

**Description**:
비교 결과를 다음 다섯 유형으로 분류한다.

- `Equivalent`: 의미와 계약이 사실상 동일
- `Intentional Divergence`: Codex 실행 모델 차이로 인해 일부러 다르게 둔 항목
- `Missing`: Claude에는 있으나 Codex에 없는 항목
- `Incorrect Translation`: 항목은 옮겼지만 의미가 잘못 바뀐 경우
- `Doc Drift`: 본문/참조/예시/validation 문서가 서로 불일치하는 경우

**Impact**:
- “차이가 있다”와 “문제가 있다”를 구분할 수 있다.
- 불필요한 parity chase를 줄이고, 실제 수정 우선순위를 높일 수 있다.

### Design Change: autopilot 비교 범위에 skill + reference + example + execution link 포함
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `핵심 설계 (§2)`
**Change Type**: Logic Flow / Design Rationale

**Description**:
autopilot parity review의 기본 범위를 단일 `SKILL.md` 비교로 제한하지 않는다. 아래 4층을 함께 본다.

1. Main skill body
2. Reference documents (`pipeline-templates`, `scale-assessment`)
3. Example orchestrator
4. Codex execution link (`.codex/agents/*.toml`과의 연결)

**Impact**:
- “본문만 맞고 예시가 틀린” 드리프트를 잡을 수 있다.
- Codex의 문서 설계가 실제 실행 backbone과 연결되는지도 확인 가능하다.

### Design Change: parity review output contract 추가
**Priority**: Medium
**Target Section**: `_sdd/spec/main.md` > `사용 가이드 & 기대 결과 (§5)`
**Change Type**: Output Contract

**Description**:
parity review의 산출물은 최소 다음을 포함하는 review note 또는 draft여야 한다.

- 비교 범위
- 항목별 분류표
- 빠진 항목 목록
- 의도적 divergence 목록
- 즉시 수정 필요 항목
- 후속 작업 후보

필요 시 `_sdd/drafts/feature_draft_autopilot_parity_review.md` 같은 draft 파일로 남긴다.

**Impact**:
- 이후 implementation/review 스텝으로 자연스럽게 handoff 가능
- 단발성 대화가 아니라 추적 가능한 산출물이 남음

---

## New Features

### Feature: Autopilot parity review checklist
**Priority**: High
**Category**: Governance
**Target Component**: `sdd-autopilot`
**Target Section**: `_sdd/spec/main.md` > `Goal > Key Features`

**Description**:
Codex autopilot과 Claude autopilot의 의미적 동등성을 점검하기 위한 체크리스트를 정의한다. 이 체크리스트는 본문, 참조, 예시, 실행 연결까지 포괄한다.

**Acceptance Criteria**:
- [ ] parity review에서 비교할 파일 목록이 명시된다.
- [ ] 본문/참조/예시/agent 연결 4층 비교 구조가 정의된다.
- [ ] 결과 분류 체계가 정의된다.
- [ ] 즉시 수정 항목과 의도적 divergence를 구분하는 규칙이 포함된다.

**Technical Notes**:
- Codex에서는 `.codex/skills/sdd-autopilot/` 과 `.codex/agents/`의 연결을 본다.
- Claude에서는 `.claude/skills/sdd-autopilot/`을 기준 원본으로 본다.
- 단순 line diff보다 “step/contract/intent” 비교를 우선한다.

**Dependencies**:
- `.codex/skills/sdd-autopilot/SKILL.md`
- `.codex/skills/sdd-autopilot/references/pipeline-templates.md`
- `.codex/skills/sdd-autopilot/references/scale-assessment.md`
- `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md`
- `.claude/skills/sdd-autopilot/SKILL.md`
- `.claude/skills/sdd-autopilot/references/pipeline-templates.md`
- `.claude/skills/sdd-autopilot/references/scale-assessment.md`
- `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md`

### Feature: Codex autopilot gap audit plan
**Priority**: High
**Category**: Enhancement
**Target Component**: Codex `sdd-autopilot`
**Target Section**: `_sdd/spec/main.md` > `Goal > Key Features`

**Description**:
Codex autopilot의 현재 상태를 Claude 원본과 대조하여 빠진 항목, 잘못 치환된 항목, 문서 드리프트를 찾는 구체적인 검토 계획을 정의한다.

**Acceptance Criteria**:
- [ ] main skill body parity review 계획이 있다.
- [ ] reference docs parity review 계획이 있다.
- [ ] sample orchestrator parity review 계획이 있다.
- [ ] agent linkage sanity check 계획이 있다.

**Technical Notes**:
- 현재 우선 의심 포인트는 `when to use / when not to use`, `error handling`, `test strategy`, `sample orchestrator detail density`다.
- Codex 특화 항목(`.codex/config.toml`, custom agents, nested `write_phased`)은 의도적 divergence 후보로 따로 평가한다.

**Dependencies**:
- `.codex/config.toml`
- `.codex/agents/*.toml`
- `.codex/agents/README.md`
- `docs/AUTOPILOT_GUIDE.md`

---

## Improvements

### Improvement: sample orchestrator parity 명시
**Priority**: Medium
**Target Section**: `_sdd/spec/main.md` > `Component Details > sdd-autopilot`
**Current State**:
Codex sample orchestrator는 Claude 예시에 비해 프롬프트 구조, 세부 step 명세, error-handling 정보가 더 얇을 가능성이 있다.
**Proposed**:
sample orchestrator 비교 시 “실제 생성물의 최소 밀도”를 기준으로 별도 점검 항목을 둔다.
**Reason**:
예시는 구현 품질 기대치를 정의하는 역할도 한다.

### Improvement: Codex-specific divergence register 추가
**Priority**: Medium
**Target Section**: `_sdd/spec/main.md` > `Platform Differences`
**Current State**:
Codex는 `request_user_input`, custom agents, `.codex/config.toml`, nested `write_phased` 같은 차이를 가지지만, 어떤 차이가 정상이며 어떤 차이가 결함인지 한눈에 보이는 register가 없다.
**Proposed**:
parity review 결과에서 Codex-specific divergence를 별도 레지스터로 관리한다.
**Reason**:
Claude와 “다르다”는 이유만으로 잘못된 수정이 발생하는 것을 막기 위함이다.

---

## Open Questions

1. parity review 산출물을 최종적으로 `_sdd/discussion/`에 둘지, draft 문서로만 유지할지 정할 필요가 있다.
2. Codex sample orchestrator의 밀도는 Claude 수준까지 올릴지, 현재처럼 축약 예시를 허용할지 결정이 필요하다.
3. `error handling`과 `retry policy`를 Codex main skill에 더 명시적으로 넣을지 판단이 필요하다.

<!-- spec-update-todo-input-end -->

---

# Part 2: Implementation Plan

## Goal

Codex `sdd-autopilot`이 Claude `sdd-autopilot`과 비교했을 때 빠지거나 잘못 번역된 부분이 없는지 체계적으로 검토하고, 수정 우선순위를 정할 수 있는 parity review 계획을 만든다.

## Scope

- In scope:
  - `.codex/skills/sdd-autopilot/`
  - `.claude/skills/sdd-autopilot/`
  - `.codex/agents/*.toml` 중 autopilot과 직접 연결되는 실행 단위
  - validation / guide 문서 중 autopilot 동작을 설명하는 문서
- Out of scope:
  - 전체 skill ecosystem parity 전수조사
  - autopilot 외 개별 skill의 본문 품질 전면 재검토

## Components

- Codex autopilot main skill
- Claude autopilot main skill
- shared reference files
- sample orchestrator examples
- Codex execution linkage

## Implementation Phases

### Phase 1: Main Skill Body Parity Review

**Objective**: 두 `SKILL.md`의 핵심 step/contract 의미를 맞대어 본다.

### Phase 2: Reference / Example Parity Review

**Objective**: `pipeline-templates`, `scale-assessment`, `sample-orchestrator`의 드리프트를 확인한다.

### Phase 3: Codex Execution Link Sanity Check

**Objective**: Codex 문서가 실제 `.codex/agents/`와 연결되는지 확인한다.

### Phase 4: Gap Classification and Action Proposal

**Objective**: 발견된 차이를 분류하고 즉시 수정 vs 후속 검토로 나눈다.

## Task Details

### Task: Compare main autopilot skill bodies
**Component**: Codex autopilot main skill
**Priority**: P0-Critical
**Type**: Research

**Description**:
`.codex/skills/sdd-autopilot/SKILL.md` 와 `.claude/skills/sdd-autopilot/SKILL.md` 를 step-by-step으로 비교한다.

**Acceptance Criteria**:
- [ ] workflow position 비교
- [ ] hard rules 비교
- [ ] step 0~8 절차 비교
- [ ] input/output contract 비교
- [ ] resume / partial execution / archive 비교

**Target Files**:
- [M] `.codex/skills/sdd-autopilot/SKILL.md` -- parity gaps가 있으면 수정 후보
- [M] `.claude/skills/sdd-autopilot/SKILL.md` -- 기준 원본 확인용, 직접 수정은 기본 범위 아님
- [C] `_sdd/drafts/feature_draft_autopilot_parity_review.md` -- parity review plan and findings seed

**Technical Notes**:
- 결과는 `Equivalent / Intentional Divergence / Missing / Incorrect Translation / Doc Drift`로 태깅한다.
- Codex-specific primitives는 차이 자체보다 의미 보존 여부를 본다.

**Dependencies**: none

### Task: Compare pipeline template parity
**Component**: Reference docs
**Priority**: P1-High
**Type**: Research

**Description**:
small / medium / large pipeline 템플릿이 Claude와 Codex에서 같은 파이프라인 의미를 유지하는지 비교한다.

**Acceptance Criteria**:
- [ ] small pipeline parity 확인
- [ ] medium pipeline parity 확인
- [ ] large pipeline parity 확인
- [ ] review-fix / test-debug / spec sync 유무 비교

**Target Files**:
- [M] `.codex/skills/sdd-autopilot/references/pipeline-templates.md` -- parity gap correction candidate
- [M] `.claude/skills/sdd-autopilot/references/pipeline-templates.md` -- baseline reference

**Technical Notes**:
- Codex에서는 agent 이름이 underscore 형식이라는 차이를 허용한다.
- 내용 밀도 차이가 의미 손실로 이어지는지 본다.

**Dependencies**:
- `.codex/skills/sdd-autopilot/SKILL.md`
- `.claude/skills/sdd-autopilot/SKILL.md`

### Task: Compare scale-assessment parity
**Component**: Reference docs
**Priority**: P1-High
**Type**: Research

**Description**:
규모 판단 기준이 Claude 원본의 정량/정성/경계 사례 규칙을 충분히 보존하는지 점검한다.

**Acceptance Criteria**:
- [ ] quantitative signal parity 확인
- [ ] qualitative signal parity 확인
- [ ] boundary rule parity 확인
- [ ] test strategy hint parity 확인

**Target Files**:
- [M] `.codex/skills/sdd-autopilot/references/scale-assessment.md` -- parity gap correction candidate
- [M] `.claude/skills/sdd-autopilot/references/scale-assessment.md` -- baseline reference

**Technical Notes**:
- Codex 쪽 축약이 단순 압축인지, 실제 판단 규칙 상실인지 구분한다.

**Dependencies**: none

### Task: Compare sample orchestrator detail density and contract
**Component**: Example docs
**Priority**: P1-High
**Type**: Research

**Description**:
Codex sample orchestrator가 Claude example에 비해 필요한 step detail, prompt contract, handoff 구조를 과도하게 잃지 않았는지 비교한다.

**Acceptance Criteria**:
- [ ] generated orchestrator 기본 메타데이터 parity 확인
- [ ] pipeline steps/agent declarations parity 확인
- [ ] artifact handoff parity 확인
- [ ] review-fix / test strategy / archive 표현 parity 확인

**Target Files**:
- [M] `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md` -- parity gap correction candidate
- [M] `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md` -- baseline reference

**Technical Notes**:
- Codex example는 agent spawn 모델을 보여줘야 한다.
- Claude example 수준의 구체 프롬프트를 모두 유지할지는 별도 판단 항목이다.

**Dependencies**:
- `.codex/skills/sdd-autopilot/references/pipeline-templates.md`
- `.claude/skills/sdd-autopilot/references/pipeline-templates.md`

### Task: Sanity-check Codex execution linkage
**Component**: Execution linkage
**Priority**: P1-High
**Type**: Research

**Description**:
Codex autopilot 문서가 실제 `.codex/agents/*.toml`, `.codex/config.toml`, validation 문서와 맞물리는지 확인한다.

**Acceptance Criteria**:
- [ ] skill 본문의 agent roster와 실제 agent names가 일치한다
- [ ] nested `write_phased` 전제가 config와 맞는다
- [ ] validation 문서가 현재 구조를 올바르게 설명한다

**Target Files**:
- [M] `.codex/skills/sdd-autopilot/SKILL.md` -- linkage mismatch correction candidate
- [M] `.codex/agents/README.md` -- execution model clarification candidate
- [M] `docs/AUTOPILOT_GUIDE.md` -- validation contract correction candidate
- [M] `.codex/config.toml` -- config sanity check
- [M] `.codex/agents/*.toml` -- actual execution backbone

**Technical Notes**:
- 이 단계는 parity review의 보조 검증이다.
- 비교 기준은 Claude가 아니라 “Codex 문서가 자기 실행 모델과 일치하느냐”다.

**Dependencies**:
- `.codex/skills/sdd-autopilot/`

### Task: Produce gap classification table and restoration proposal
**Component**: Reporting
**Priority**: P0-Critical
**Type**: Documentation

**Description**:
발견된 차이를 표로 정리하고, 즉시 수정 / 후속 논의 / 의도적 divergence로 나눠 제안한다.

**Acceptance Criteria**:
- [ ] 차이 목록이 유형별로 분류된다
- [ ] 즉시 수정 항목이 우선순위와 함께 제시된다
- [ ] 의도적 divergence가 명시된다
- [ ] 후속 open questions가 정리된다

**Target Files**:
- [M] `_sdd/drafts/feature_draft_autopilot_parity_review.md` -- final parity review planning artifact
- [TBD] `_sdd/discussion/` 관련 정리 문서 -- 필요 시 후속 discussion candidate

**Technical Notes**:
- findings-first 구조를 사용한다.
- parity correction implementation으로 이어질 수 있게 target file 기준으로 묶는다.

**Dependencies**:
- Previous research tasks

## Risks

- Codex-specific divergence와 실제 결함을 혼동할 수 있다.
- Claude sample orchestrator의 장문 프롬프트를 어디까지 Codex에 유지할지 기준이 모호할 수 있다.
- 현재 Codex 문서가 최근 구조 변경 중이라 문서 드리프트가 여러 층에 걸쳐 있을 수 있다.

## Open Questions

1. Codex sample orchestrator는 Claude 수준의 상세 프롬프트를 유지해야 하는가, 아니면 요약 예시로 충분한가?
2. parity review 결과를 draft 문서로만 남길지, 별도 validation guide에 흡수할지 정할 필요가 있다.
3. Codex main skill에 `When not to use`, `Error handling`, `Retry policy`를 Claude 수준으로 더 노출할지 결정이 필요하다.
