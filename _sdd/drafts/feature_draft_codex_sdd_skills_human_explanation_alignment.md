# Feature Draft: Codex SDD 스킬 설명-탐색 균형 정렬

**Date**: 2026-03-09
**Author**: Codex
**Target Spec**: main.md
**Status**: Draft

---

# Part 1: Spec Patch Draft

> 이 패치는 `spec-update-todo` 입력으로 사용할 수 있습니다.

# Spec Update Input

**Date**: 2026-03-09
**Author**: Codex
**Target Spec**: main.md
**Spec Update Classification**: MUST update

## New Features

### Feature: 설명-탐색 균형형 Codex SDD 스킬 출력
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Goal > Key Features`
**Affected Components**: `Spec Lifecycle Skills`, `Implementation Lifecycle Skills`, `PR Lifecycle Skills`
**Related Paths**: `.codex/skills/spec-create/`, `.codex/skills/spec-review/`, `.codex/skills/spec-rewrite/`, `.codex/skills/spec-summary/`, `.codex/skills/spec-update-todo/`, `.codex/skills/spec-update-done/`, `.codex/skills/feature-draft/`, `.codex/skills/implementation-plan/`, `.codex/skills/implementation-review/`, `.codex/skills/pr-spec-patch/`, `.codex/skills/pr-review/`

**Description**:
Codex용 SDD 스킬이 경로/계약/변경 지점만 요약하는 수준을 넘어, 사람이 빠르게 이해할 수 있는 동작 개요와 설계 의도를 함께 생성·검증·동기화하도록 정렬한다.

**Acceptance Criteria**:
- [ ] `spec-create` 템플릿과 예시가 메인 스펙의 서술형 `Runtime Map`과 컴포넌트 스펙의 `Overview`를 기본 구조로 보여준다.
- [ ] `feature-draft`, `spec-update-todo`, `spec-update-done`, `pr-spec-patch`가 `Component Details > Overview`와 서술형 `Runtime Map` 갱신을 명시적으로 다룬다.
- [ ] `spec-review`, `spec-rewrite`, `spec-summary`가 탐색성뿐 아니라 설명 품질과 설계 의도 보존 여부를 평가한다.
- [ ] 후속 소비 스킬(`implementation-plan`, `implementation-review`, `pr-review`)이 `Overview`를 읽거나, 누락 시 spec gap/follow-up으로 기록한다.

**Spec Impact**:
- Goal: 이 저장소의 Codex SDD 스킬은 "어디를 바꾸는가"와 함께 "무엇이 어떻게 동작하는가"를 함께 드러내는 출력으로 이동한다.
- Architecture/Flow: `docs/SDD_SPEC_REQUIREMENTS.md` -> `spec-create` 템플릿/예시 -> update/review/rewrite/summary -> planning/review/PR 소비 스킬 순으로 변경 전파 경로가 생긴다.
- Usage/Change Paths: 앞으로 SDD 요구사항 변경 시 canonical authoring assets와 downstream 소비 스킬을 분리해서 점검해야 한다.
- Tests/Observability: reference/template/example/checklist가 새 설명 기준의 문서형 회귀 장치 역할을 한다.

**Risks / Invariants**:
- 설명 강화가 코드 구현 복사나 장황한 산문으로 돌아가면 안 된다.
- 메인 스펙은 계속 entry point 크기를 유지해야 한다.
- `feature-draft` Part 1 출력은 `spec-update-todo` 호환성을 유지해야 한다.

**Dependencies**:
- `docs/SDD_SPEC_REQUIREMENTS.md`
- `_sdd/discussion/discussion_spec_human_explanation.md`

## Improvements

### Improvement: canonical spec authoring surface 재정렬
**Priority**: High
**Target Section**: `_sdd/spec/spec-lifecycle.md` > `Change Recipes`
**Affected Components**: `spec-create`, `spec-review`, `spec-rewrite`, `spec-summary`

**Current State**:
Codex 스킬은 stable anchors를 사용하지만, 실제 `spec-create` 템플릿과 예시는 `Component Overview`와 서술형 `Runtime Map`을 강제하지 않아 설명 보강이 생성 결과까지 전달되지 않는다.

**Proposed**:
`spec-create` 템플릿/예시를 canonical authoring surface로 보고, `spec-review`, `spec-rewrite`, `spec-summary`가 이 구조를 평가·보존·요약하도록 일관되게 맞춘다.

**Reason**:
템플릿과 예시가 바뀌지 않으면 상위 요구사항 문서만 수정되어도 실제 산출물의 품질은 그대로 남는다.

**Related Paths**:
- `.codex/skills/spec-create/SKILL.md`
- `.codex/skills/spec-create/references/template-full.md`
- `.codex/skills/spec-create/examples/simple-project-spec.md`
- `.codex/skills/spec-create/examples/complex-project-spec.md`
- `.codex/skills/spec-review/references/review-checklist.md`
- `.codex/skills/spec-rewrite/references/rewrite-checklist.md`
- `.codex/skills/spec-summary/references/summary-template.md`

### Improvement: planned/synced patch 흐름의 설명 섹션 지원
**Priority**: High
**Target Section**: `_sdd/spec/implementation-lifecycle.md` > `Interfaces / Contracts`
**Affected Components**: `feature-draft`, `spec-update-todo`, `spec-update-done`, `implementation-plan`, `implementation-review`

**Current State**:
계획/동기화/리뷰 흐름은 `Runtime Map`, `Component Index`, `Common Change Paths` 중심으로 정렬되어 있고, `Overview`와 설계 의도 보존은 간접적이거나 누락돼 있다.

**Proposed**:
planned patch와 sync/report 흐름에 `Component Details > Overview`와 사용자 관점의 `Runtime Map` 설명을 1급 타겟으로 추가한다.

**Reason**:
기능 초안이나 구현 리뷰가 경로 중심으로만 정리되면, 왜 이런 구조를 택했는지와 실제 동작 경계가 후속 단계에서 손실된다.

**Related Paths**:
- `.codex/skills/feature-draft/SKILL.md`
- `.codex/skills/feature-draft/references/output-format.md`
- `.codex/skills/spec-update-todo/references/section-mapping.md`
- `.codex/skills/spec-update-done/references/drift-patterns.md`
- `.codex/skills/implementation-plan/SKILL.md`
- `.codex/skills/implementation-review/references/review-checklist.md`

### Improvement: PR/리뷰 계열의 설명 drift 감지 강화
**Priority**: Medium
**Target Section**: `_sdd/spec/pr-lifecycle.md` > `Interfaces / Contracts`
**Affected Components**: `pr-spec-patch`, `pr-review`

**Current State**:
PR 스킬은 경로, 흐름, 컴포넌트 인덱스 drift는 잘 잡지만, 설명용 `Runtime Map` 서술과 `Overview`의 누락/노후화는 명시적으로 검토하지 않는다.

**Proposed**:
PR 패치 초안과 리뷰 체크리스트에서 `Overview`와 설명 drift를 별도 검토 대상으로 추가한다.

**Reason**:
구현은 맞아도 스펙의 사람 친화 설명이 낡으면 이후 변경 안전성이 다시 떨어진다.

**Related Paths**:
- `.codex/skills/pr-spec-patch/SKILL.md`
- `.codex/skills/pr-spec-patch/examples/spec_patch_draft.md`
- `.codex/skills/pr-review/SKILL.md`
- `.codex/skills/pr-review/references/review-checklist.md`

## Component Changes

### Update Component: Spec Lifecycle Skills
**Target Section**: `_sdd/spec/spec-lifecycle.md` > `Interfaces / Contracts`
**Change Type**: Enhancement

**Changes**:
- `spec-create`가 메인 `Runtime Map`의 서술형 동작 시나리오와 컴포넌트 `Overview`(동작 개요 + 설계 의도)를 기본 산출물로 생성하도록 강화
- `spec-review`가 설명 품질과 탐색 품질을 분리 평가하도록 확장
- `spec-rewrite`가 `Overview`와 서술형 `Runtime Map`을 보존/재구성 대상으로 다루도록 보강
- `spec-summary`가 "설명보다 탐색" 톤을 제거하고, 짧은 설명 + 탐색 시작점의 균형을 유지하도록 수정
- `spec-update-todo`/`spec-update-done`가 `Overview`와 설명 drift를 update 대상에 포함

**Risks / Invariants**:
- 상위 anchor(`Goal`, `Architecture Overview`, `Component Details`, `Open Questions`)는 유지해야 한다.
- `Overview`는 컴포넌트 스펙의 MUST 섹션으로 다루되, 새 top-level anchor를 추가해 호환성을 깨면 안 된다.

### Update Component: Implementation Lifecycle Skills
**Target Section**: `_sdd/spec/implementation-lifecycle.md` > `Interfaces / Contracts`
**Change Type**: Enhancement

**Changes**:
- `feature-draft`가 `Component Details > Overview`와 서술형 `Runtime Map`을 spec patch draft에서 직접 타겟팅
- `implementation-plan`이 `Overview`를 plan input 또는 spec gap 판정 근거로 읽도록 정렬
- `implementation-review`가 spec sync follow-up에서 `Overview` 갱신 필요 여부를 분류

**Risks / Invariants**:
- `Target Files` 규약과 `MUST update / CONSIDER / NO update` 분류 체계는 유지해야 한다.
- 구현 본체를 과도하게 문서 의존적으로 만들지 않고, 설명 부족만 follow-up으로 남겨야 한다.

### Update Component: PR Lifecycle Skills
**Target Section**: `_sdd/spec/pr-lifecycle.md` > `Interfaces / Contracts`
**Change Type**: Enhancement

**Changes**:
- `pr-spec-patch`가 PR diff를 `Overview`와 설명형 `Runtime Map` 관점에서도 patch item으로 분류
- `pr-review`가 explanation drift를 blocker와 post-merge sync와 구분해 보고
- examples/checklists가 `Overview` 누락, 설계 의도 drift, 서술형 flow 누락 사례를 보여주도록 보강

**Risks / Invariants**:
- evidence-linked review 원칙은 그대로 유지해야 한다.
- `NO update` PR에 불필요한 문서 변경을 강제하면 안 된다.

## Notes

### Context
- `_sdd/discussion/discussion_spec_human_explanation.md`는 현재 SDD 스펙/스킬이 참조와 변경 시작점에 비해 사람 친화 설명이 구조적으로 부족하다고 정리했다.
- `docs/SDD_SPEC_REQUIREMENTS.md`는 이미 `Overview` MUST 섹션, 서술형 `Runtime Map`, "어떻게 동작하는가"와 "어디를 바꾸면 되는가"의 균형을 기준으로 삼는다.
- `.codex/skills/spec-create/references/template-full.md`, 예시 파일들, summary/review/rewrite/update references는 아직 이 기준을 완전히 반영하지 못한다.

### Constraints
- 이번 계획의 구현 범위는 `.codex/skills/` 아래 SDD 스킬과 그 참조/예시/버전 파일로 한정한다.
- `.claude/skills/` 동기화는 의도적으로 후속 작업으로 남긴다.
- 한국어 출력, token-efficient 구조, `spec-update-todo` 호환성은 유지해야 한다.
- 빈 선택 섹션을 만들지 않는 원칙은 그대로 유지한다.

### Decision-Log Candidates
- 컴포넌트 스펙의 `Overview`를 Codex 스킬 전반에서 MUST 지원 대상으로 본다.
- 요약/리뷰/동기화 스킬은 "설명 대 탐색"의 우선순위 문제가 아니라 균형 문제로 취급한다.
- Codex만 선행 수정할 경우 일시적 플랫폼 drift를 허용하되, 후속 mirror 계획을 명시한다.

### References
- `docs/SDD_SPEC_REQUIREMENTS.md`
- `_sdd/discussion/discussion_spec_human_explanation.md`
- `_sdd/spec/spec-lifecycle.md`
- `_sdd/spec/implementation-lifecycle.md`
- `_sdd/spec/pr-lifecycle.md`

## Open Questions
- `.claude/skills/` mirror를 같은 변경 세트에 묶을지, Codex 검증 후 별도 단계로 둘지 결정이 필요하다.
- `.codex/skills/implementation/SKILL.md`까지 `Overview` 소비를 명시적으로 확장할지, 현재는 `implementation-plan`/`implementation-review` 정렬만으로 충분한지 추가 판단이 필요하다.
- `spec-summary`에서 설명 보강을 어느 정도까지 허용할지 기준선(예: 1-2문장 narrative 한도)을 별도 가이드로 고정할지 미정이다.

---

# Part 2: Implementation Plan

## Overview

`.codex/skills`의 SDD 스킬을 `docs/SDD_SPEC_REQUIREMENTS.md`의 최신 기준에 맞춰 재정렬한다. 핵심은 `spec-create`를 비롯한 canonical authoring assets에서 서술형 `Runtime Map`과 컴포넌트 `Overview`를 기본 구조로 만들고, 이후 plan/review/sync/PR 스킬이 그 구조를 읽고 유지하도록 연결하는 것이다.

## Scope

### In Scope
- `.codex/skills/spec-*` 계열 SDD 스킬의 prompt/reference/example 정렬
- `.codex/skills/feature-draft/`의 spec patch draft 포맷 보강
- `.codex/skills/implementation-plan/`, `.codex/skills/implementation-review/`의 spec 소비 정렬
- `.codex/skills/pr-spec-patch/`, `.codex/skills/pr-review/`의 explanation drift 감지 보강
- 변경된 스킬의 `skill.json` 버전 갱신

### Out of Scope
- `.claude/skills/` mirror 수정
- `docs/SDD_SPEC_REQUIREMENTS.md` 자체 수정
- `_sdd/spec/` 실제 반영
- `implementation` 본체의 병렬 실행 로직 변경

## Components
1. **Canonical Authoring Assets**: `spec-create`, `feature-draft`
2. **Spec Maintenance & Quality Gates**: `spec-update-todo`, `spec-update-done`, `spec-review`, `spec-rewrite`, `spec-summary`
3. **Downstream Consumers**: `implementation-plan`, `implementation-review`, `pr-spec-patch`, `pr-review`

## Implementation Phases

### Phase 1: Canonical Output Alignment
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 1 | `spec-create` 템플릿/예시를 설명 강화 기준으로 정렬 | P0 | - | Canonical Authoring Assets |
| 2 | `feature-draft` 출력 포맷에 `Overview`/서술형 flow patch 지원 추가 | P0 | 1 | Canonical Authoring Assets |
| 3 | `spec-update-todo` 입력 매핑을 `Overview` 대응으로 확장 | P0 | 1, 2 | Spec Maintenance & Quality Gates |

### Phase 2: Sync and Quality Gate Alignment
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 4 | `spec-update-done` drift/sync 전략에 설명 drift 규칙 추가 | P1 | 1, 3 | Spec Maintenance & Quality Gates |
| 5 | `spec-review`가 설명 품질과 설계 의도 보존을 평가하도록 확장 | P1 | 1 | Spec Maintenance & Quality Gates |
| 6 | `spec-rewrite`가 `Overview`와 narrative `Runtime Map`을 재구성하도록 보강 | P1 | 1 | Spec Maintenance & Quality Gates |
| 7 | `spec-summary`의 톤/템플릿을 설명-탐색 균형으로 재정렬 | P1 | 1 | Spec Maintenance & Quality Gates |

### Phase 3: Downstream Consumer Alignment
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 8 | `implementation-plan`/`implementation-review`가 `Overview`를 읽고 follow-up으로 남기도록 정렬 | P2 | 2, 3, 4, 5 | Downstream Consumers |
| 9 | `pr-spec-patch`/`pr-review`가 explanation drift를 patch/review 대상으로 다루도록 정렬 | P2 | 2, 3, 4, 5 | Downstream Consumers |

## Task Details

### Task 1: `spec-create` 템플릿/예시를 설명 강화 기준으로 정렬
**Component**: Canonical Authoring Assets
**Priority**: P0
**Type**: Feature

**Description**:
`spec-create`가 실제 생성물에서 서술형 `Runtime Map`과 컴포넌트 `Overview`를 기본으로 만들도록 prompt, reference template, examples를 함께 수정한다.

**Acceptance Criteria**:
- [ ] `SKILL.md`가 explanation/navigation 균형을 명시한다.
- [ ] `template-full.md`에 컴포넌트 `Overview`가 MUST 구조로 들어간다.
- [ ] `simple-project-spec.md`, `complex-project-spec.md` 예시에 `Overview`와 사용자 관점 서술형 flow가 반영된다.
- [ ] `skill.json` 버전이 변경 의도를 반영해 갱신된다.

**Target Files**:
- [M] `.codex/skills/spec-create/SKILL.md` -- 생성 스킬의 설명/탐색 균형 규칙 추가
- [M] `.codex/skills/spec-create/skill.json` -- 버전 갱신
- [M] `.codex/skills/spec-create/references/template-full.md` -- `Overview` 및 narrative `Runtime Map` 템플릿 반영
- [M] `.codex/skills/spec-create/examples/simple-project-spec.md` -- 소형 예시에 `Overview`와 설명형 flow 추가
- [M] `.codex/skills/spec-create/examples/complex-project-spec.md` -- 대형 예시에 설계 의도/사용자 관점 flow 추가

**Technical Notes**:
- `Overview`는 `Responsibility` 다음, `Owned Paths` 앞에 두는 구조를 기본으로 한다.
- `Runtime Map`은 다이어그램 + 짧은 서술형 시나리오 조합을 기본 예시로 맞춘다.

**Dependencies**: -

### Task 2: `feature-draft` 출력 포맷에 `Overview`/서술형 flow patch 지원 추가
**Component**: Canonical Authoring Assets
**Priority**: P0
**Type**: Feature

**Description**:
`feature-draft`가 planned patch 단계에서 `Component Details > Overview`와 설명형 `Runtime Map`을 직접 타겟팅할 수 있도록 prompt, output format, example을 확장한다.

**Acceptance Criteria**:
- [ ] `SKILL.md`가 `Overview`와 narrative flow를 stable drafting target으로 다룬다.
- [ ] `references/output-format.md`에 관련 `Target Section` 규칙과 예시가 추가된다.
- [ ] `examples/feature_draft_parallel.md`가 `Overview` 항목을 포함한다.
- [ ] `spec-update-todo` 호환성에 필요한 기본 구조는 그대로 유지된다.

**Target Files**:
- [M] `.codex/skills/feature-draft/SKILL.md` -- drafting target과 설명 기준 보강
- [M] `.codex/skills/feature-draft/skill.json` -- 버전 갱신
- [M] `.codex/skills/feature-draft/references/output-format.md` -- `Overview`/narrative flow patch 예시 추가
- [M] `.codex/skills/feature-draft/examples/feature_draft_parallel.md` -- component `Overview` 반영 예시 추가

**Technical Notes**:
- `Spec Update Input`의 top-level section 구조는 유지하고, item-level `Target Section`만 확장한다.
- `Decision-Log Candidates`와 `Open Questions`에 explanation risk를 분리한다.

**Dependencies**: 1

### Task 3: `spec-update-todo` 입력 매핑을 `Overview` 대응으로 확장
**Component**: Spec Maintenance & Quality Gates
**Priority**: P0
**Type**: Feature

**Description**:
planned update 반영 스킬이 `Overview`와 설명형 `Runtime Map`을 정상적인 update 대상으로 취급하도록 prompt와 mapping references를 수정한다.

**Acceptance Criteria**:
- [ ] `SKILL.md`에 `Overview` 갱신 조건과 판단 기준이 추가된다.
- [ ] `section-mapping.md`가 behavior/design intent 변화 시 `Component Details > Overview`를 타겟으로 안내한다.
- [ ] `input-format.md`가 관련 예시를 포함한다.
- [ ] example 입력 파일이 새 타겟 섹션을 보여준다.

**Target Files**:
- [M] `.codex/skills/spec-update-todo/SKILL.md` -- update rules에 `Overview` 반영
- [M] `.codex/skills/spec-update-todo/skill.json` -- 버전 갱신
- [M] `.codex/skills/spec-update-todo/references/section-mapping.md` -- `Overview` 매핑 규칙 추가
- [M] `.codex/skills/spec-update-todo/references/input-format.md` -- `Overview` 대상 예시 추가
- [M] `.codex/skills/spec-update-todo/examples/user_spec.md` -- planned input 예시 정렬

**Technical Notes**:
- `Goal`/`Architecture Overview`/`Component Details` 상위 anchor는 그대로 두고, component 내부 subsection으로 `Overview`를 다룬다.
- `NO update` 기준은 그대로 유지한다.

**Dependencies**: 1, 2

### Task 4: `spec-update-done` drift/sync 전략에 설명 drift 규칙 추가
**Component**: Spec Maintenance & Quality Gates
**Priority**: P1
**Type**: Feature

**Description**:
구현 후 sync 스킬이 stale narrative `Runtime Map`, missing `Overview`, outdated design intent를 drift pattern으로 인식하고 수정 전략에 반영하도록 보강한다.

**Acceptance Criteria**:
- [ ] `SKILL.md`가 `Overview` sync 필요 여부를 명시적으로 다룬다.
- [ ] `drift-patterns.md`에 설명 drift 패턴이 추가된다.
- [ ] `update-strategies.md`가 design intent sync 전략을 포함한다.
- [ ] review/report 예시가 새 drift 유형을 보여준다.

**Target Files**:
- [M] `.codex/skills/spec-update-done/SKILL.md` -- sync 대상에 `Overview`와 explanation drift 추가
- [M] `.codex/skills/spec-update-done/skill.json` -- 버전 갱신
- [M] `.codex/skills/spec-update-done/references/drift-patterns.md` -- stale narrative flow / missing overview 패턴 추가
- [M] `.codex/skills/spec-update-done/references/update-strategies.md` -- design intent sync 전략 추가
- [M] `.codex/skills/spec-update-done/examples/review-report.md` -- 새 drift 유형 예시 보강

**Technical Notes**:
- planned/actual 상태 동기화 규칙은 유지하고, explanation drift는 `MUST update` 또는 `CONSIDER`로 분기한다.
- `DECISION_LOG.md` 후보와 component-level `Overview` 갱신 기준을 분리해 적는다.

**Dependencies**: 1, 3

### Task 5: `spec-review`가 설명 품질과 설계 의도 보존을 평가하도록 확장
**Component**: Spec Maintenance & Quality Gates
**Priority**: P1
**Type**: Feature

**Description**:
review-only 스킬이 경로/흐름/인덱스 존재 여부만 보는 수준을 넘어, 설명이 충분한지와 설계 의도가 남아 있는지도 판단하도록 축을 확장한다.

**Acceptance Criteria**:
- [ ] `SKILL.md` review dimensions에 explanation quality 또는 equivalent axis가 추가된다.
- [ ] checklist가 `Overview` 존재/품질과 narrative `Runtime Map` 품질을 점검한다.
- [ ] example report가 explanation gap finding을 보여준다.
- [ ] finding severity 기준이 설명 부족과 navigation drift를 구분할 수 있다.

**Target Files**:
- [M] `.codex/skills/spec-review/SKILL.md` -- review dimension/보고 형식 보강
- [M] `.codex/skills/spec-review/skill.json` -- 버전 갱신
- [M] `.codex/skills/spec-review/references/review-checklist.md` -- `Overview`/설명 품질 체크 추가
- [M] `.codex/skills/spec-review/examples/spec-review-report.md` -- explanation gap 예시 추가

**Technical Notes**:
- optional section 미존재를 과잉 패널티하지 않는 원칙은 유지한다.
- evidence-linked finding 방식은 바꾸지 않는다.

**Dependencies**: 1

### Task 6: `spec-rewrite`가 `Overview`와 narrative `Runtime Map`을 재구성하도록 보강
**Component**: Spec Maintenance & Quality Gates
**Priority**: P1
**Type**: Refactor

**Description**:
리라이트 스킬이 문서를 짧게 만드는 데 치우치지 않고, 사람이 이해하기 위한 설명 축을 재구성 대상으로 명시하도록 수정한다.

**Acceptance Criteria**:
- [ ] `SKILL.md`가 `Overview` 재구성과 설명 보존을 목표로 포함한다.
- [ ] `rewrite-checklist.md`에 `Overview`/narrative flow 관련 항목이 추가된다.
- [ ] rewrite 예시가 `Overview`를 남기는 방향으로 갱신된다.
- [ ] top-level anchor 구조는 유지된다.

**Target Files**:
- [M] `.codex/skills/spec-rewrite/SKILL.md` -- rewrite target shape와 규칙 보강
- [M] `.codex/skills/spec-rewrite/skill.json` -- 버전 갱신
- [M] `.codex/skills/spec-rewrite/references/rewrite-checklist.md` -- `Overview`/설명 품질 점검 추가
- [M] `.codex/skills/spec-rewrite/examples/rewrite-report.md` -- 설명 보강 예시 정렬

**Technical Notes**:
- `Overview`는 component spec 기준으로 추가하고, main spec은 Runtime narrative로 설명을 압축한다.
- "짧게"보다 "빠르게 이해 가능"을 우선 문구로 재정렬한다.

**Dependencies**: 1

### Task 7: `spec-summary`의 톤/템플릿을 설명-탐색 균형으로 재정렬
**Component**: Spec Maintenance & Quality Gates
**Priority**: P1
**Type**: Feature

**Description**:
`spec-summary`가 현재의 "설명보다 탐색" 톤을 제거하고, 짧은 동작 설명과 탐색 시작점을 함께 담는 요약 템플릿으로 바뀌도록 수정한다.

**Acceptance Criteria**:
- [ ] `SKILL.md`가 explanation/navigation balance를 명시한다.
- [ ] `summary-template.md`가 간단한 동작 개요 또는 설계 의도 요약 슬롯을 제공한다.
- [ ] example summary가 여전히 짧지만 설명이 결핍되지 않는다.
- [ ] `skill.json` 버전이 갱신된다.

**Target Files**:
- [M] `.codex/skills/spec-summary/SKILL.md` -- 요약 원칙 문구 재정렬
- [M] `.codex/skills/spec-summary/skill.json` -- 버전 갱신
- [M] `.codex/skills/spec-summary/references/summary-template.md` -- explanation-friendly 요약 슬롯 추가
- [M] `.codex/skills/spec-summary/examples/summary-output.md` -- 균형형 summary 예시 반영

**Technical Notes**:
- summary는 여전히 2-4 화면 이내를 목표로 한다.
- 긴 narrative 섹션을 만들지 않고, 1-2문장 summary를 각 핵심 영역에 배치한다.

**Dependencies**: 1

### Task 8: `implementation-plan`/`implementation-review`가 `Overview`를 읽고 follow-up으로 남기도록 정렬
**Component**: Downstream Consumers
**Priority**: P2
**Type**: Refactor

**Description**:
구현 계획과 구현 리뷰 스킬이 `Component Details > Overview`를 spec input으로 읽고, 누락 또는 drift 시 spec gap / spec sync follow-up으로 남기도록 수정한다.

**Acceptance Criteria**:
- [ ] `implementation-plan`이 `Overview`를 input extraction 목록 또는 spec gap 판단 기준에 포함한다.
- [ ] `implementation-review` checklist가 `Overview` sync 필요 여부를 확인한다.
- [ ] 관련 examples가 새 판단 기준을 보여준다.
- [ ] 두 스킬의 `skill.json` 버전이 갱신된다.

**Target Files**:
- [M] `.codex/skills/implementation-plan/SKILL.md` -- spec input 목록에 `Overview`와 narrative flow 반영
- [M] `.codex/skills/implementation-plan/skill.json` -- 버전 갱신
- [M] `.codex/skills/implementation-plan/examples/sample-plan-parallel.md` -- plan 예시 정렬
- [M] `.codex/skills/implementation-review/SKILL.md` -- spec sync follow-up에 `Overview` 추가
- [M] `.codex/skills/implementation-review/skill.json` -- 버전 갱신
- [M] `.codex/skills/implementation-review/references/review-checklist.md` -- `Overview` follow-up 체크 추가
- [M] `.codex/skills/implementation-review/examples/sample-review.md` -- review 예시 정렬

**Technical Notes**:
- `implementation` 본체는 이번 범위에서 직접 수정하지 않는다.
- `Overview`가 없을 때는 즉시 blocker로 만들기보다 `Spec Gaps` 또는 follow-up으로 분류한다.

**Dependencies**: 2, 3, 4, 5

### Task 9: `pr-spec-patch`/`pr-review`가 explanation drift를 patch/review 대상으로 다루도록 정렬
**Component**: Downstream Consumers
**Priority**: P2
**Type**: Refactor

**Description**:
PR 관련 스킬이 `Runtime Map`과 `Component Index`뿐 아니라 `Overview`와 설계 의도 drift를 spec impact의 일부로 분류하도록 수정한다.

**Acceptance Criteria**:
- [ ] `pr-spec-patch`가 `Overview` 대상 patch item을 생성할 수 있다.
- [ ] `pr-review` checklist/report가 explanation drift를 명시적으로 본다.
- [ ] example draft/review가 새 분류를 보여준다.
- [ ] 두 스킬의 `skill.json` 버전이 갱신된다.

**Target Files**:
- [M] `.codex/skills/pr-spec-patch/SKILL.md` -- spec impact mapping에 `Overview` 반영
- [M] `.codex/skills/pr-spec-patch/skill.json` -- 버전 갱신
- [M] `.codex/skills/pr-spec-patch/examples/spec_patch_draft.md` -- `Overview` patch 예시 추가
- [M] `.codex/skills/pr-review/SKILL.md` -- review axes/report 섹션에 explanation drift 반영
- [M] `.codex/skills/pr-review/skill.json` -- 버전 갱신
- [M] `.codex/skills/pr-review/references/review-checklist.md` -- `Overview` 검토 체크 추가
- [M] `.codex/skills/pr-review/examples/sample-review.md` -- explanation drift finding 예시 추가

**Technical Notes**:
- blocker와 post-merge sync를 섞지 않는 기존 규칙은 유지한다.
- `NO update` PR에는 no-op 판단이 가능해야 한다.

**Dependencies**: 2, 3, 4, 5

## Parallel Execution Summary

| Phase | Total Tasks | Max Parallel | File Conflicts |
|-------|-------------|--------------|----------------|
| 1 | 3 | 1 | canonical spec shape를 먼저 확정해야 하므로 순차 권장 |
| 2 | 4 | 4 | 없음 (`spec-update-done`, `spec-review`, `spec-rewrite`, `spec-summary`는 파일 분리) |
| 3 | 2 | 2 | 없음 (`implementation-*`와 `pr-*` 파일 분리) |

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| 설명 강화가 장황한 코드 덤프로 흐름 | 스킬 출력 품질 저하 | template/example에 "동작 개요 + 설계 의도"만 허용하고 구현 복사 금지 예시 포함 |
| `feature-draft`와 `spec-update-todo` 포맷 불일치 | 후속 스펙 반영 실패 | Task 2 -> Task 3 순으로 진행하고 item-level `Target Section`만 확장 |
| Codex만 먼저 수정해 플랫폼 drift 발생 | 사용자 혼선 | 이번 계획의 범위를 명시하고, 후속 `.claude/skills` mirror 작업을 Open Questions로 남김 |
| 요약 스킬이 다시 너무 길어짐 | LLM 소비성 저하 | `spec-summary`는 1-2문장 narrative 슬롯만 추가하고 길이 제한 유지 |

## Open Questions

- [ ] `implementation/SKILL.md` 수정은 이번 계획 범위에서 제외하고, Codex SDD 스킬 정렬 완료 후 별도 후속 작업으로 검토

## Fixed Decisions

- `skill.json` 버전 정책은 이번 변경 범위에서 일괄 minor bump로 통일
- `.claude/skills` mirror는 이번 계획 범위에 포함하지 않음

## Next Steps

### Apply Spec Patch
- `spec-update-todo`를 실행해 Part 1의 planned update를 `_sdd/spec/`에 반영

### Execute Implementation
- 위 Phase 순서대로 `.codex/skills/` 수정
- 각 Phase 종료 시 `git diff --check`와 `rg "Overview|동작 개요|설계 의도|Runtime Map" .codex/skills`로 정합성 확인

### Sync After Completion
- Codex 쪽 변경 검증 후 필요하면 `.claude/skills/` mirror용 별도 feature draft 작성
