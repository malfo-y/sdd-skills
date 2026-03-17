# Feature Draft: Codex Autopilot 오케스트레이션 + Wrapper 전환

**Date**: 2026-03-17
**Author**: Codex
**Target Spec**: main.md
**Status**: Draft
**Features**: Codex autopilot 메타스킬, 기존 SDD agent 재사용형 wrapper 전환, write-phased Codex 편입

---

<!-- spec-update-todo-input-start -->
# Part 1: Spec Patch Draft

> 이 패치는 해당 스펙 섹션에 copy-paste하거나,
> `spec-update-todo` 스킬의 입력으로 사용할 수 있습니다.

# Spec Update Input

**Date**: 2026-03-17
**Author**: Codex
**Target Spec**: main.md
**Spec Update Classification**: MUST update

## Background & Motivation Updates

### Background Update: Codex autopilot 지원 공백 해소
**Target Section**: `_sdd/spec/main.md` > `배경 및 동기 (§1)`
**Change Type**: Problem Statement / Motivation / Alternative Comparison

**Current**:
메인 스펙은 듀얼 플랫폼(Claude Code + Codex)을 강조하지만, 실제 아키텍처 설명과 Platform Differences에는 Codex가 `sdd-autopilot`과 agent-wrapper 패턴을 지원하지 않는 것으로 남아 있다. 이로 인해 사용자는 "듀얼 플랫폼"이라는 목표와 "Codex 미지원"이라는 운영 설명 사이에서 혼선을 겪는다.

**Proposed**:
Codex도 기존 SDD agent 집합을 재사용하는 오케스트레이션 경로를 갖는다는 점을 스펙 목표에 명시한다. 다만 범위는 "신규 agent 역할 추가"가 아니라, 기존 SDD agent를 조합하는 `sdd-autopilot` 메타스킬과 generated orchestration skill 지원으로 한정한다.

**Reason**:
현재 논의의 핵심은 Claude 전용 구조를 그대로 복제하는 것이 아니라, Codex에서도 동일한 end-to-end SDD 흐름을 사용할 수 있게 하는 것이다. 스펙의 플랫폼 목표와 실제 지원 범위를 다시 일치시켜야 한다.

---

## Design Changes

### Design Change: Codex autopilot은 기존 SDD agent를 조합하는 메타스킬로 정의
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `핵심 설계 (§2)`
**Change Type**: Logic Flow / Design Rationale

**Description**:
Codex의 `sdd-autopilot`은 사용자 요청을 분석하고, discussion 및 코드베이스 탐색 결과를 바탕으로 요청별 orchestration skill을 생성한 뒤, 기존 SDD agent들을 순서대로 호출하는 메타스킬로 정의한다. 핵심 원칙은 "새 agent 역할을 발명하지 않고, 이미 정해진 SDD agent roster를 재사용"하는 것이다.

**Impact**:
- Codex의 `feature-draft`, `implementation-plan`, `implementation`, `implementation-review`, `spec-update-done`, `spec-update-todo`, `spec-review`, `ralph-loop-init`, `write-phased`가 오케스트레이션 가능한 실행 단위로 정렬된다.
- `sdd-autopilot`은 사용자 대화와 파이프라인 설계에 집중하고, 실제 단계 실행은 orchestration skill에 위임한다.

### Design Change: Codex의 generated orchestration skill + pipeline log 계약 추가
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `핵심 설계 (§2)`
**Change Type**: Logic Flow / Design Rationale

**Description**:
Codex에서도 요청별 orchestration skill을 생성하고, `_sdd/pipeline/log_<topic>_<timestamp>.md`에 실행 상태를 기록하는 계약을 추가한다. generated orchestration skill은 active 실행 중에는 `.codex/skills/orchestrator_<topic>/SKILL.md`와 대응 `skill.json` 형식을 사용하고, 파이프라인 완료 후에는 `_sdd/pipeline/orchestrators/<topic>_<timestamp>/` 아래로 이동해 실행 아카이브로 보관한다. 로그는 Meta + Status + Execution Log 구조를 따른다.

**Impact**:
- resume/partial execution 설계를 Codex까지 확장할 수 있다.
- 오케스트레이터 정의와 실행 상태를 분리하는 현재 autopilot 설계 원칙이 플랫폼 간 일관성을 갖는다.

### Design Change: write-phased를 Codex long-form writing utility로 승격
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `핵심 설계 (§2)`
**Change Type**: Algorithm / Design Rationale

**Description**:
Codex의 `write-phased`를 "긴 문서/코드 파일은 skeleton -> fill 2단계로 작성"하는 공용 utility로 명시한다. `spec-create`, `guide-create`, `pr-spec-patch`, `pr-review`, `spec-summary`, `spec-upgrade`와 향후 generated orchestration skill은 장문 산출물 생성 시 `write-phased`를 우선 사용한다.

**Impact**:
- Codex에서도 Claude와 동일한 2-phase generation 패턴을 일관되게 적용한다.
- 장문 스펙/문서/코드 작성 시 후반 품질 저하와 큰 diff 재작성 문제를 줄인다.

---

## New Features

### Feature: Codex sdd-autopilot 메타스킬
**Priority**: High
**Category**: Core Feature
**Target Component**: `sdd-autopilot`
**Target Section**: `_sdd/spec/main.md` > `Goal > Key Features`

**Description**:
Codex에서 `sdd-autopilot`을 호출하면, 요구사항 정리 -> 코드베이스 탐색 -> 규모 판단 -> orchestration skill 생성 -> 승인 -> 자율 실행까지 수행한다. 이 기능은 기존 SDD agent를 재사용하며, generated orchestration skill과 `_sdd/pipeline` 로그를 통해 재개/부분 실행과 연결된다.

**Acceptance Criteria**:
- [ ] Codex에서 `sdd-autopilot`을 독립 skill로 사용할 수 있다.
- [ ] autopilot이 요청별 orchestration skill 생성을 명시적으로 지시한다.
- [ ] orchestration skill이 기존 SDD agent roster만 사용하도록 제한된다.
- [ ] `_sdd/pipeline/log_*.md` 기반 resume/partial execution 계약이 Codex에도 문서화된다.

**Technical Notes**:
- generated orchestration skill은 runtime artifact이며, 미완료 파이프라인 동안만 active `.codex/skills/orchestrator_<topic>/`에 유지한다.
- 완료된 orchestrator는 `_sdd/pipeline/orchestrators/<topic>_<timestamp>/`로 이동해 resume 이력과 감사 추적용으로 보관한다.
- Phase 1 인터랙션과 Phase 2 자율 실행의 2-phase orchestration 원칙을 유지한다.

**Dependencies**:
- `_sdd/discussion/discussion_autopilot_meta_skill.md`
- `_sdd/discussion/discussion_autopilot_resume_and_partial_execution.md`

### Feature: Codex wrapper-based pipeline skill execution
**Priority**: High
**Category**: Enhancement
**Target Component**: `feature-draft`, `implementation-plan`, `implementation`, `implementation-review`, `spec-update-done`, `spec-update-todo`, `spec-review`, `ralph-loop-init`
**Target Section**: `_sdd/spec/main.md` > `Goal > Key Features`

**Description**:
Codex의 주요 파이프라인 스킬을 기존 풀 SKILL.md 유지 상태에서 벗어나, "사용자 진입점은 유지하되 agent 실행 단위를 호출 가능한 wrapper surface"로 재정렬한다. discussion은 여전히 full skill로 유지하고, 나머지 파이프라인 단계는 autopilot/orchestrator가 조합 가능한 구조로 맞춘다.

**Acceptance Criteria**:
- [ ] 파이프라인 필수 스킬의 Codex 문서가 wrapper-orchestration 관점을 명시한다.
- [ ] discussion은 interactive boundary로 남고, 나머지 단계는 non-interactive 실행 원칙을 따른다.
- [ ] skill 설명과 spec의 Platform Differences가 "Codex 미지원"이 아니라 "Codex 오케스트레이션 지원" 기준으로 정렬된다.

**Technical Notes**:
- 이번 범위는 "net-new agent role 추가"가 아니라 "기존 SDD agent roster 재사용"이다.
- standalone 사용성과 orchestrator 하위 실행 가능성을 모두 유지해야 한다.
- wrapper와 실제 agent binding은 repo 내 강결합 manifest가 아니라 Codex 런타임/환경 레이어 책임으로 둔다.

**Dependencies**:
- `.codex/skills/feature-draft/`
- `.codex/skills/implementation-plan/`
- `.codex/skills/implementation/`
- `.codex/skills/implementation-review/`
- `.codex/skills/spec-update-done/`
- `.codex/skills/spec-update-todo/`
- `.codex/skills/spec-review/`
- `.codex/skills/ralph-loop-init/`

### Feature: Codex write-phased orchestration integration
**Priority**: Medium
**Category**: Enhancement
**Target Component**: `write-phased`
**Target Section**: `_sdd/spec/main.md` > `Goal > Key Features`

**Description**:
Codex의 `write-phased`를 단독 utility를 넘어, 장문 산출물을 만드는 producer skill들과 `sdd-autopilot`이 공통으로 사용할 수 있는 writing strategy로 연결한다. 1차 범위에서는 `spec-create`, `guide-create`, `pr-spec-patch`, `pr-review`, `spec-summary`, `spec-upgrade`를 연결 대상으로 삼고, `feature-draft`의 직접 연동은 후속 최적화로 분리한다.

**Acceptance Criteria**:
- [ ] Codex의 `write-phased` 설명이 long-form utility 역할로 명확히 정리된다.
- [ ] 장문 producer skill 최소 6개가 `write-phased` 사용 규칙을 문서화한다.
- [ ] `write-phased`의 skeleton 저장, patch-based fill, marker cleanup 규칙이 플랫폼 전반에 일관되게 반영된다.

**Technical Notes**:
- 긴 문서/코드 작성 시 무조건 중첩 호출하지 않고, 필요 시 orchestration skill이 직접 `write-phased` 경로를 타도록 평탄화할 수 있다.
- `feature-draft -> write-phased` 직접 연동은 이번 범위에서 제외하고, autopilot/wrapper 안정화 이후 후속 작업으로 다룬다.

**Dependencies**:
- `_sdd/discussion/discussion_write_phased_skill_design.md`
- `.codex/skills/write-phased/SKILL.md`

---

## Improvements

### Improvement: Platform Differences와 아키텍처 다이어그램의 Codex 설명 갱신
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Architecture Overview`
**Current State**:
현재 메인 스펙은 `.codex/skills/`를 "17개 풀 SKILL.md 유지"로 설명하고, `sdd-autopilot`을 Codex 미지원으로 표기한다.
**Proposed**:
Codex 아키텍처를 "existing agent roster를 활용하는 orchestration-capable skill layer"로 갱신하고, `sdd-autopilot` 및 `write-phased`의 Codex 위치를 다이어그램과 플랫폼 비교 표에 반영한다.
**Reason**:
사용자 기대치와 실제 설계 방향을 맞추고, Claude/Codex 차이를 "지원 여부"가 아니라 "운영 방식 차이"로 설명해야 한다.

### Improvement: AUTOPILOT_GUIDE의 저장 위치/플랫폼 설명 드리프트 수정
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `사용 가이드 & 기대 결과 (§5)`
**Current State**:
`docs/AUTOPILOT_GUIDE.md`는 오케스트레이터 저장 위치, 플랫폼 범위, generated artifact 설명이 discussion의 최신 결정과 어긋난 부분이 있다.
**Proposed**:
오케스트레이터 정의와 실행 로그의 분리, Codex 지원 범위, generated orchestration skill 규약을 최신 결정에 맞춰 갱신한다.
**Reason**:
가이드는 사용자-facing entry point이므로 가장 먼저 최신 설계와 맞아야 한다.

### Improvement: Codex write-phased의 long-form producer 연결 명시
**Priority**: Medium
**Target Section**: `_sdd/spec/main.md` > `Component Details`
**Current State**:
Codex에는 `write-phased` skill이 존재하지만, 다른 `.codex/skills`가 이를 공통 utility로 활용한다는 계약이 문서화되어 있지 않다.
**Proposed**:
producer skill들에 `write-phased` 연결 규칙을 명시하고, component/source 목록에서도 Codex 측 사용처를 추가한다.
**Reason**:
현재 상태는 "스킬이 있긴 하지만 오케스트레이션에 연결되지 않은 상태"에 가깝다. 공용 전략으로 승격해야 재사용 가치가 생긴다.

---

## Component Changes

### Update Component: sdd-autopilot
**Target Section**: `_sdd/spec/main.md` > `Component Details > sdd-autopilot`
**Change Type**: Enhancement

**Changes**:
- Codex용 `sdd-autopilot` skill source와 artifact 규약을 추가
- generated orchestration skill 생성 책임을 명시
- `_sdd/pipeline/log_*.md`와 resume/partial execution 흐름을 Codex까지 확장
- "기존 SDD agent 재사용, net-new agent role 추가 금지" 원칙을 명시

### Update Component: Codex Pipeline Skills
**Target Section**: `_sdd/spec/main.md` > `Component Details`
**Change Type**: Enhancement

**Changes**:
- `feature-draft`, `implementation-plan`, `implementation`, `implementation-review`, `spec-update-done`, `spec-update-todo`, `spec-review`, `ralph-loop-init`의 Codex 측 실행 형태를 wrapper/orchestrator-compatible 구조로 기술
- discussion은 full skill로 유지하고, pipeline skill은 non-interactive 실행 원칙으로 분리
- Platform Differences의 "Codex full SKILL.md only" 서술을 최신 구조에 맞게 교체

### Update Component: write-phased
**Target Section**: `_sdd/spec/main.md` > `Component Details > write-phased`
**Change Type**: Enhancement

**Changes**:
- Codex 측 source 경로와 사용처를 명시
- producer skill들이 장문 산출물에서 `write-phased`를 활용하는 계약을 추가
- skeleton 저장 -> patch fill -> marker cleanup 규칙을 Codex 설명에 연결

---

## Usage Scenarios

### Scenario: Codex에서 end-to-end autopilot 실행
**Target Section**: `_sdd/spec/main.md` > `사용 가이드 & 기대 결과 (§5)`

**Setup**:
- `_sdd/spec/main.md`가 존재한다.
- Codex skill set에 `sdd-autopilot`이 포함된다.

**Action**:
사용자가 Codex에서 autopilot을 호출해 기능 구현을 요청한다.

**Expected Result**:
- autopilot이 요구사항을 정리하고 규모를 판단한다.
- 요청별 orchestration skill과 pipeline log가 생성된다.
- 기존 SDD agent가 순차/조건부로 실행된다.
- 구현 완료 후 review-fix loop와 spec sync가 이어진다.

### Scenario: Codex long-form output을 write-phased로 생성
**Target Section**: `_sdd/spec/main.md` > `사용 가이드 & 기대 결과 (§5)`

**Setup**:
- 장문 스펙/가이드/패치 초안을 생성해야 하는 Codex skill이 실행된다.

**Action**:
producer skill 또는 orchestration skill이 `write-phased` 규칙을 사용해 skeleton을 먼저 만들고, 이어서 section-by-section fill을 수행한다.

**Expected Result**:
- 초기 골조가 실제 파일에 저장된다.
- 후속 작성은 patch 기반으로 진행된다.
- 최종 결과물에 placeholder/phase marker가 남지 않는다.

---

## Notes

### Context
- `_sdd/discussion/discussion_autopilot_meta_skill.md`와 `_sdd/discussion/discussion_autopilot_resume_and_partial_execution.md`는 Claude 중심으로 정리된 autopilot 설계를 보여주지만, 현재 논의는 이를 Codex에도 확장하는 방향이다.
- `.codex/skills/write-phased/SKILL.md`는 이미 2-phase writing strategy를 담고 있으나, producer skill과 autopilot 오케스트레이션까지 연결되지는 않았다.
- `_sdd/spec/main.md`는 듀얼 플랫폼을 표방하면서도 Codex를 `sdd-autopilot` 미지원으로 남겨 두고 있어 spec drift가 존재한다.

### Constraints
- 이번 범위는 `.codex/skills/`, `docs/`, `_sdd/spec/` 업데이트를 중심으로 한다.
- 새 business/domain agent 역할을 추가하지 않는다. 기존 SDD agent roster만 사용한다.
- generated orchestration skill은 runtime artifact이며, 미완료 동안만 active `.codex/skills/orchestrator_<topic>/`에 두고 완료 후 `_sdd/pipeline/orchestrators/`로 이동한다.
- wrapper와 실제 agent binding은 런타임/환경 레이어 책임으로 두고, repo 범위에서는 wrapper/orchestration contract만 문서화한다.
- discussion은 interactive skill로 유지하고, pipeline execution 단계는 non-interactive 원칙을 따른다.

### Decision-Log Candidates
- Codex `sdd-autopilot`은 기존 SDD agent를 조합하는 메타스킬로 정의한다.
- Codex도 generated orchestration skill + pipeline log 계약을 사용하되, 미완료 orchestrator는 active로 유지하고 완료 후 `_sdd/pipeline/orchestrators/`로 아카이브한다.
- Codex wrapper skill의 실제 agent binding은 repo 내 manifest가 아니라 런타임/환경 레이어 책임으로 둔다.
- `write-phased`는 Codex long-form producer skill의 공용 utility로 승격한다.
- `feature-draft -> write-phased` 직접 연동은 이번 범위에서 제외하고 후속 최적화로 분리한다.

### References
- `_sdd/discussion/discussion_autopilot_meta_skill.md`
- `_sdd/discussion/discussion_autopilot_resume_and_partial_execution.md`
- `_sdd/discussion/discussion_write_phased_skill_design.md`
- `docs/AUTOPILOT_GUIDE.md`

### Resolved Scope Decisions
- 미완료 generated orchestrator는 active `.codex/skills/orchestrator_<topic>/`에 유지하고, 완료 후에는 `_sdd/pipeline/orchestrators/<topic>_<timestamp>/`로 이동한다.
- Codex wrapper skill의 실제 agent binding은 런타임/환경 레이어 책임으로 두며, repo에는 wrapper/orchestration contract만 유지한다.
- `feature-draft`의 직접 `write-phased` 연동은 이번 범위에서 제외하고 후속 최적화 작업으로 분리한다.

<!-- spec-update-todo-input-end -->

---

# Part 2: Implementation Plan

## Overview

Codex 측 SDD 워크플로우를 "풀 SKILL.md 집합"에서 "기존 SDD agent 재사용형 wrapper + autopilot orchestration + write-phased integration" 구조로 재정렬한다. 핵심 목표는 Claude에서 이미 성숙한 autopilot / agent-wrapper / write-phased 설계 원칙을 Codex에도 맞추되, 새 agent 역할을 추가하지 않고 기존 실행 단위를 조합하는 것이다.

## Scope

### In Scope
- `.codex/skills/sdd-autopilot/` 신규 추가
- 기존 Codex pipeline skill들의 wrapper/orchestration-compatible 정렬
- `.codex/skills/write-phased/` 개선 및 long-form producer skill 연결
- `docs/AUTOPILOT_GUIDE.md`, `docs/SDD_WORKFLOW.md`, `docs/SDD_QUICK_START.md` 업데이트
- `_sdd/spec/main.md`, `_sdd/spec/DECISION_LOG.md` 동기화

### Out of Scope
- `.claude/agents/` 구조 재설계
- net-new SDD agent role 추가
- runtime에서 생성되는 실제 orchestration skill을 저장소에 고정 산출물로 커밋
- Codex 외 플랫폼의 자동화/배포 방식 변경

## Components

1. **Codex Autopilot Metaskill**: 요청 분석, 규모 판단, orchestration skill 생성, resume/logging 책임
2. **Codex Pipeline Wrappers**: 기존 SDD agent roster를 오케스트레이션 가능한 실행 surface로 정렬
3. **Codex Long-form Writing Layer**: `write-phased`와 producer skill 연결
4. **Docs & Spec Sync**: 사용자 가이드, 워크플로우 문서, 스펙/결정 로그 업데이트

## Implementation Phases

### Phase 1: Autopilot Scaffold

| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 1 | Codex sdd-autopilot core skill 생성 | P0 | - | Codex Autopilot Metaskill |
| 2 | Codex sdd-autopilot references/examples 작성 | P1 | 1 | Codex Autopilot Metaskill |

### Phase 2: Wrapper & Utility Alignment

| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 3 | planning 계열 Codex wrapper 정렬 (`feature-draft`, `implementation-plan`) | P0 | 1 | Codex Pipeline Wrappers |
| 4 | execution/review 계열 Codex wrapper 정렬 (`implementation`, `implementation-review`) | P0 | 1 | Codex Pipeline Wrappers |
| 5 | spec-maintenance 계열 Codex wrapper 정렬 (`spec-update-todo`, `spec-update-done`, `spec-review`, `ralph-loop-init`) | P1 | 1 | Codex Pipeline Wrappers |
| 6 | Codex `write-phased` core skill 강화 | P0 | 1 | Codex Long-form Writing Layer |
| 7 | long-form producer skill에 `write-phased` 연결 | P1 | 6 | Codex Long-form Writing Layer |

### Phase 3: Docs & Spec Sync

| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 8 | AUTOPILOT_GUIDE 및 사용자 워크플로우 문서 갱신 | P1 | 1, 3, 4, 5, 6, 7 | Docs & Spec Sync |
| 9 | 메인 스펙과 Decision Log 동기화 | P1 | 1, 3, 4, 5, 6, 7 | Docs & Spec Sync |

## Task Details

### Task 1: Codex sdd-autopilot core skill 생성
**Component**: Codex Autopilot Metaskill
**Priority**: P0-Critical
**Type**: Feature

**Description**:
Codex용 `sdd-autopilot` skill의 핵심 파일을 생성한다. 이 skill은 사용자 요청을 받아 Phase 1 인터랙션, 규모 판단, orchestration skill 생성, 승인, resume/logging, Phase 2 자율 실행 규칙을 Codex 환경에 맞게 정의한다.

**Acceptance Criteria**:
- [ ] `.codex/skills/sdd-autopilot/SKILL.md`가 생성된다.
- [ ] `.codex/skills/sdd-autopilot/skill.json`이 생성되고 version/description이 SKILL.md와 일치한다.
- [ ] "기존 SDD agent roster 재사용, net-new agent role 추가 금지" 원칙이 hard rule로 명시된다.
- [ ] generated orchestration skill과 `_sdd/pipeline/log_*.md` 계약이 포함된다.
- [ ] 미완료 orchestrator active 유지와 완료 후 `_sdd/pipeline/orchestrators/` 아카이브 규칙이 포함된다.

**Target Files**:
- [C] `.codex/skills/sdd-autopilot/SKILL.md` -- Codex autopilot 메타스킬 본문
- [C] `.codex/skills/sdd-autopilot/skill.json` -- 스킬 메타데이터

**Technical Notes**:
- Claude용 `.claude/skills/sdd-autopilot/`를 그대로 복사하지 말고, Codex interaction/tooling 문법에 맞게 재서술해야 한다.
- generated orchestration skill 경로는 active 상태에서 `.codex/skills/orchestrator_<topic>/`, 완료 후 `_sdd/pipeline/orchestrators/<topic>_<timestamp>/`를 기본 가정으로 문서화한다.

**Dependencies**: -

---

### Task 2: Codex sdd-autopilot references/examples 작성
**Component**: Codex Autopilot Metaskill
**Priority**: P1-High
**Type**: Documentation

**Description**:
Codex autopilot이 일관된 파이프라인을 생성하도록 reference와 example를 작성한다. 규모 판단, pipeline template, sample orchestrator를 Codex 기준으로 정리한다.

**Acceptance Criteria**:
- [ ] scale assessment 기준이 Codex용으로 문서화된다.
- [ ] small/medium/large 파이프라인 템플릿이 reference에 포함된다.
- [ ] sample orchestrator가 generated skill의 실제 구조와 artifact handoff 방식을 보여준다.

**Target Files**:
- [C] `.codex/skills/sdd-autopilot/references/pipeline-templates.md` -- 규모별 파이프라인 템플릿
- [C] `.codex/skills/sdd-autopilot/references/scale-assessment.md` -- 규모 판단 기준
- [C] `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md` -- 생성 예시

**Technical Notes**:
- sample orchestrator는 `feature-draft -> implementation-plan -> implementation -> implementation-review -> spec-update-done` 흐름과 `write-phased` 연결 지점을 보여주는 것이 좋다.
- resume/partial execution 관련 상태 필드는 sample에도 반영한다.
- sample에는 active orchestrator와 archived orchestrator의 라이프사이클을 함께 예시로 넣는다.

**Dependencies**: 1

---

### Task 3: planning 계열 Codex wrapper 정렬 (`feature-draft`, `implementation-plan`)
**Component**: Codex Pipeline Wrappers
**Priority**: P0-Critical
**Type**: Refactor

**Description**:
`feature-draft`와 `implementation-plan`을 Codex autopilot/orchestrator에서 직접 조합 가능한 wrapper surface로 정렬한다. standalone 사용성은 유지하되, non-interactive orchestration 실행을 전제로 한 설명과 hard rules를 강화한다.

**Acceptance Criteria**:
- [ ] `feature-draft`가 multi-feature grouping, Target Files, Part 1/Part 2 출력 규약을 유지한 채 orchestration-friendly하게 정리된다.
- [ ] `implementation-plan`이 `feature-draft` 산출물 및 generated orchestration 흐름과의 연결을 명시한다.
- [ ] 두 skill의 `skill.json` version이 본문 변경과 함께 갱신된다.

**Target Files**:
- [M] `.codex/skills/feature-draft/SKILL.md` -- wrapper/orchestration 친화 규칙 반영
- [M] `.codex/skills/feature-draft/skill.json` -- 버전/설명 갱신
- [M] `.codex/skills/implementation-plan/SKILL.md` -- orchestration input/output 계약 정렬
- [M] `.codex/skills/implementation-plan/skill.json` -- 버전/설명 갱신

**Technical Notes**:
- `feature-draft`는 장문 산출물 생성이지만, 직접 `write-phased` 연동은 후속 최적화로 미루고 이번 작업에서는 wrapper/orchestration 계약 정렬을 우선한다.
- 두 skill 모두 `_sdd/` 파일 handoff 규약을 분명히 해야 한다.
- wrapper와 실제 binding 방식은 repo 밖 런타임 레이어 책임이라는 전제를 명시한다.

**Dependencies**: 1

---

### Task 4: execution/review 계열 Codex wrapper 정렬 (`implementation`, `implementation-review`)
**Component**: Codex Pipeline Wrappers
**Priority**: P0-Critical
**Type**: Refactor

**Description**:
`implementation`과 `implementation-review`를 Codex orchestration에서 review-fix loop를 안정적으로 수행할 수 있는 형태로 정렬한다. Task/Target Files 기반 실행, review 결과 기반 재시도, non-interactive 동작 원칙을 명시한다.

**Acceptance Criteria**:
- [ ] `implementation`이 Target Files 기반 실행 규약과 orchestration 사용 시의 기대 입력을 분명히 한다.
- [ ] `implementation-review`가 severity 분류와 review-fix loop 재진입 판단 기준을 명시한다.
- [ ] 두 skill의 설명과 버전이 최신 구조에 맞게 갱신된다.

**Target Files**:
- [M] `.codex/skills/implementation/SKILL.md` -- orchestration-compatible 실행 규칙
- [M] `.codex/skills/implementation/skill.json` -- 버전/설명 갱신
- [M] `.codex/skills/implementation-review/SKILL.md` -- review-fix loop 판단 규칙 정렬
- [M] `.codex/skills/implementation-review/skill.json` -- 버전/설명 갱신

**Technical Notes**:
- review 결과는 orchestration skill이 읽을 수 있는 요약 포맷을 유지해야 한다.
- 같은 Phase 내 다중 task 병렬 실행과 review 결과 loop는 문서상 분리해 설명하는 것이 좋다.

**Dependencies**: 1

---

### Task 5: spec-maintenance 계열 Codex wrapper 정렬 (`spec-update-todo`, `spec-update-done`, `spec-review`, `ralph-loop-init`)
**Component**: Codex Pipeline Wrappers
**Priority**: P1-High
**Type**: Refactor

**Description**:
스펙 반영/검증/장시간 디버깅 계열 skill을 Codex autopilot의 후반부 단계와 맞물리도록 정렬한다. 특히 `spec-update-todo` / `spec-update-done`는 autopilot과 generated orchestration skill의 마지막 단계에서 호출될 수 있어야 한다.

**Acceptance Criteria**:
- [ ] `spec-update-todo`와 `spec-update-done`이 autopilot/generated orchestration 산출물과의 연결 방식을 명시한다.
- [ ] `spec-review`가 Codex 후속 검증 단계로 사용 가능한 위치를 분명히 한다.
- [ ] `ralph-loop-init`가 긴 테스트/디버깅 시점에만 조건부로 들어가는 역할을 명확히 한다.

**Target Files**:
- [M] `.codex/skills/spec-update-todo/SKILL.md` -- autopilot planned patch 연결 규칙
- [M] `.codex/skills/spec-update-todo/skill.json` -- 버전/설명 갱신
- [M] `.codex/skills/spec-update-done/SKILL.md` -- post-implementation sync 규칙 정렬
- [M] `.codex/skills/spec-update-done/skill.json` -- 버전/설명 갱신
- [M] `.codex/skills/spec-review/SKILL.md` -- orchestration 후속 검증 위치 명시
- [M] `.codex/skills/spec-review/skill.json` -- 버전/설명 갱신
- [M] `.codex/skills/ralph-loop-init/SKILL.md` -- 장시간 iteration 조건 명시
- [M] `.codex/skills/ralph-loop-init/skill.json` -- 버전/설명 갱신

**Technical Notes**:
- `spec-update-done`와 `spec-review`는 docs/spec drift 정리와도 연결되므로 결과 문구를 일관되게 맞추는 편이 좋다.

**Dependencies**: 1

---

### Task 6: Codex `write-phased` core skill 강화
**Component**: Codex Long-form Writing Layer
**Priority**: P0-Critical
**Type**: Enhancement

**Description**:
기존 `.codex/skills/write-phased/`를 long-form writing utility로 명확히 승격한다. skeleton 저장, patch 기반 fill, marker cleanup, multi-file ordering, orchestration integration 관점을 강화한다.

**Acceptance Criteria**:
- [ ] hard rules가 Claude 쪽 설계 의도와 실질적으로 동등한 수준으로 정렬된다.
- [ ] long-form utility 역할과 적용/비적용 기준이 더 분명해진다.
- [ ] `skill.json` version과 설명이 본문과 일치한다.

**Target Files**:
- [M] `.codex/skills/write-phased/SKILL.md` -- long-form utility 역할 강화
- [M] `.codex/skills/write-phased/skill.json` -- 버전/설명 갱신

**Technical Notes**:
- apply_patch 기반 in-place fill 원칙은 Codex 편집 제약과도 잘 맞는다.
- 중첩 깊이를 줄이기 위해 long-form writing은 필요한 경우 orchestration skill이 직접 `write-phased`를 쓰는 경로를 우선한다.

**Dependencies**: 1

---

### Task 7: long-form producer skill에 `write-phased` 연결
**Component**: Codex Long-form Writing Layer
**Priority**: P1-High
**Type**: Refactor

**Description**:
장문 문서/패치/요약을 생성하는 Codex skill들이 `write-phased`를 공용 writing strategy로 사용하도록 연결 규칙을 추가한다.

**Acceptance Criteria**:
- [ ] producer skill 최소 6개가 `write-phased` 사용 지침을 포함한다.
- [ ] 장문 산출물 생성 시 skeleton -> fill 전략을 사용할 조건이 명시된다.
- [ ] 관련 `skill.json` version이 함께 갱신된다.
- [ ] 이번 단계의 producer 연결 범위에서 `feature-draft`는 의도적으로 제외됨이 문서에 명시된다.

**Target Files**:
- [M] `.codex/skills/spec-create/SKILL.md` -- 장문 스펙 생성 시 write-phased 활용 규칙
- [M] `.codex/skills/spec-create/skill.json` -- 버전/설명 갱신
- [M] `.codex/skills/guide-create/SKILL.md` -- 가이드 초안 작성 시 write-phased 활용 규칙
- [M] `.codex/skills/guide-create/skill.json` -- 버전/설명 갱신
- [M] `.codex/skills/pr-spec-patch/SKILL.md` -- patch draft 장문 작성 연결
- [M] `.codex/skills/pr-spec-patch/skill.json` -- 버전/설명 갱신
- [M] `.codex/skills/pr-review/SKILL.md` -- 리뷰 리포트 장문 작성 연결
- [M] `.codex/skills/pr-review/skill.json` -- 버전/설명 갱신
- [M] `.codex/skills/spec-summary/SKILL.md` -- 장문 요약 작성 연결
- [M] `.codex/skills/spec-summary/skill.json` -- 버전/설명 갱신
- [M] `.codex/skills/spec-upgrade/SKILL.md` -- 대형 스펙 변환 시 write-phased 활용 규칙
- [M] `.codex/skills/spec-upgrade/skill.json` -- 버전/설명 갱신

**Technical Notes**:
- 각 skill에서 무조건 `write-phased`를 호출하도록 강제하기보다, 구조적 복잡도 기준으로 사용하게 하는 편이 유연하다.
- 중첩 깊이 리스크가 크면 orchestration skill에서 직접 long-form task를 맡는 경로를 추가 검토한다.
- `feature-draft`는 별도 후속 작업에서 직접 연동 여부를 검토한다.

**Dependencies**: 6

---

### Task 8: AUTOPILOT_GUIDE 및 사용자 워크플로우 문서 갱신
**Component**: Docs & Spec Sync
**Priority**: P1-High
**Type**: Documentation

**Description**:
사용자-facing 문서를 최신 Codex 지원 범위에 맞게 갱신한다. 특히 `AUTOPILOT_GUIDE`의 저장 위치/플랫폼 설명 드리프트를 바로잡고, 워크플로우/퀵스타트 문서에 Codex autopilot 지원과 write-phased 활용 경로를 반영한다.

**Acceptance Criteria**:
- [ ] `docs/AUTOPILOT_GUIDE.md`가 Codex 지원 구조와 generated orchestration skill/log 계약을 반영한다.
- [ ] `docs/SDD_WORKFLOW.md`와 `docs/SDD_QUICK_START.md`가 Codex autopilot 사용 가능성을 최신 상태로 설명한다.
- [ ] guide의 오케스트레이터 저장 위치와 로그 설명이 spec/decision과 일치한다.

**Target Files**:
- [M] `docs/AUTOPILOT_GUIDE.md` -- Codex 지원, artifact, 저장 위치 설명 갱신
- [M] `docs/SDD_WORKFLOW.md` -- Codex autopilot/workflow 설명 갱신
- [M] `docs/SDD_QUICK_START.md` -- 빠른 시작 가이드 갱신

**Technical Notes**:
- 사용자 문서는 내부 구현 세부를 과도하게 드러내기보다, 사용법/기대 동작/제약을 우선해야 한다.
- `write-phased`는 사용자-facing 문서에서는 "긴 문서/코드 작성 utility" 정도로 간결히 설명하는 편이 좋다.

**Dependencies**: 1, 3, 4, 5, 6, 7

---

### Task 9: 메인 스펙과 Decision Log 동기화
**Component**: Docs & Spec Sync
**Priority**: P1-High
**Type**: Documentation

**Description**:
`_sdd/spec/main.md`와 `_sdd/spec/DECISION_LOG.md`를 Codex autopilot / wrapper / write-phased 지원 구조에 맞게 갱신한다.

**Acceptance Criteria**:
- [ ] `main.md`의 Key Features, Core Design, Architecture Overview, Component Details, Platform Differences가 최신 구조를 반영한다.
- [ ] `DECISION_LOG.md`에 Codex autopilot + write-phased 통합 결정이 기록된다.
- [ ] "Codex 미지원" 또는 "Codex full SKILL.md only" 같은 구식 서술이 제거되거나 최신화된다.

**Target Files**:
- [M] `_sdd/spec/main.md` -- Codex 지원 구조 반영
- [M] `_sdd/spec/DECISION_LOG.md` -- 결정사항 기록

**Technical Notes**:
- spec는 "지원 여부"보다 "운영 방식 차이"를 강조하는 방향이 더 적합하다.
- 기존 Claude 중심 설명은 유지하되, Codex를 후순위/후속으로만 다루는 문구는 정리할 필요가 있다.

**Dependencies**: 1, 3, 4, 5, 6, 7

## Parallel Execution Summary

| Phase | Total Tasks | Max Parallel | Sequential (conflicts) |
|-------|-------------|--------------|------------------------|
| 1 | 2 | 1 | 1 |
| 2 | 5 | 4 | 1 |
| 3 | 2 | 2 | 0 |

> Phase 1은 Task 2가 Task 1 산출물에 의존합니다. Phase 2는 Task 7이 Task 6에 의존하고, 나머지 wrapper 정렬 작업은 파일이 겹치지 않아 병렬화 가능합니다.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Codex에서 wrapper skill과 agent binding 방식이 repo 밖 설정에 의존 | 구현 경로 불명확 | repo 범위에서는 wrapper/orchestration contract를 우선 고정하고, binding은 런타임/환경 레이어 책임으로 명시 |
| completed orchestrator가 active `.codex/skills/`에 누적됨 | skill 공간 오염, 탐색성 저하 | 미완료만 active 유지하고 완료 시 `_sdd/pipeline/orchestrators/`로 이동 |
| autopilot -> orchestration -> producer -> write-phased 중첩이 깊어짐 | 실행 지연 또는 운영 복잡도 증가 | long-form writing은 필요 시 orchestration skill이 직접 담당하도록 평탄화 |
| Claude와 Codex 설명이 다시 drift | 문서/사용자 혼선 | docs + spec + skill.json version을 같은 변경 세트로 갱신 |
| AUTOPILOT_GUIDE와 spec의 저장 위치/플랫폼 설명 불일치 재발 | 운영 혼선 | docs 변경 시 `_sdd/spec/main.md`, `DECISION_LOG.md` 동시 점검 체크리스트 도입 |

## Resolved Scope Decisions

- 미완료 generated orchestrator는 active `.codex/skills/orchestrator_<topic>/`에 유지하고, 완료 후 `_sdd/pipeline/orchestrators/<topic>_<timestamp>/`로 이동한다.
- Codex wrapper skill의 실제 agent binding은 런타임/환경 레이어 책임으로 두며, repo 내 추가 manifest는 이번 범위에 포함하지 않는다.
- `feature-draft`의 직접 `write-phased` 연동은 이번 범위에서 제외하고 후속 최적화 작업으로 분리한다.

## Model Recommendation

설계/문서/프롬프트 구조가 함께 바뀌는 작업이므로, 구현 본체는 고 reasoning 코딩 모델이 적합하다. 추천은 `gpt-5.4` 또는 동급 reasoning-high 모델로 cross-file prompt refactor를 수행하고, 이후 dry-run 리뷰나 wording 정리는 `gpt-5.3-codex` 급 모델로 보조 검증하는 방식이다.

## Next Steps

1. 이 draft를 기준으로 Codex 범위를 확정한다.
2. `sdd-autopilot`과 `write-phased`를 먼저 구현하고, 그 다음 wrapper 정렬로 넘어간다.
3. 마지막에 docs/spec 동기화를 한 번에 처리해 drift를 줄인다.
