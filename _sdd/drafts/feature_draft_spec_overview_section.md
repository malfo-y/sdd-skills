# Feature Draft: 스펙 Overview 섹션 및 서술형 설명 보강

**날짜**: 2026-03-09
**근거**: `_sdd/discussion/discussion_spec_human_explanation.md`
**변경된 요구사항**: `docs/SDD_SPEC_REQUIREMENTS.md` (이미 반영 완료)

---

<!-- spec-update-todo-input-start -->

# Part 1: Spec Patch Draft

> This patch can be copy-pasted into the corresponding spec section,
> or used as input for the `spec-update-todo` skill.

# Spec Update Input

**Date**: 2026-03-09
**Author**: SDD Skills maintainer
**Target Spec**: `_sdd/spec/spec-lifecycle.md`, `_sdd/spec/main.md`
**Spec Update Classification**: MUST update

## Improvements

### Improvement: 컴포넌트 스펙 Overview MUST 섹션 도입
**Priority**: High
**Target Section**: `_sdd/spec/spec-lifecycle.md` > `Component Details`
**Current State**: 컴포넌트 스펙에 Responsibility(1-2문장) 외에 동작 설명이나 설계 의도를 담는 전용 섹션이 없음
**Proposed**: Responsibility 다음에 `Overview` MUST 섹션을 추가하여 동작 개요(어떻게 동작하는가)와 설계 의도(왜 이렇게 만들었는가)를 서술형으로 기록
**Reason**: SDD_SPEC_REQUIREMENTS.md §2, §5, §9.2 변경에 따라 "설명 = 탐색" 균형 달성. 사람이 컴포넌트의 동작과 설계 근거를 이해할 수 있어야 안전한 변경이 가능함

### Improvement: 메인 스펙 Runtime Map 서술형 보강
**Priority**: Medium
**Target Section**: `_sdd/spec/main.md` > `Architecture Overview > Runtime Map`
**Current State**: Runtime Map이 단계별 리스트 수준이며 "왜 이 흐름인가", "사용자 관점에서 어떤 시나리오인가"에 대한 서술이 없음
**Proposed**: 기존 흐름 리스트에 사용자 관점의 서술형 동작 시나리오를 보강
**Reason**: SDD_SPEC_REQUIREMENTS.md §5 메인 스펙 Runtime Map 설명에 "서술형 동작 시나리오" 포함이 명시됨

### Improvement: spec-create 스킬의 "이해와 변경의 균형" 반영
**Priority**: High
**Target Section**: `_sdd/spec/spec-lifecycle.md` > `Change Recipes`
**Current State**: spec-create의 Writing Guidance가 "Favor tables with actual paths over long narrative"로 서술형 설명을 억제
**Proposed**: 경로/테이블 우선은 유지하되, Overview 섹션에서는 서술형 동작 설명과 설계 의도 기술을 권장하도록 가이드라인 보강
**Reason**: §9.2가 "이해와 변경의 균형(understand-then-change)"으로 변경됨

## Notes

### Context
- `docs/SDD_SPEC_REQUIREMENTS.md`는 이미 5곳 수정 완료 (L38, §4, §5, §6.5, §9.2)
- 이제 이 변경된 요구사항을 실제 스킬 코드에 반영해야 함
- `.codex/skills/`에도 동일 스킬이 존재하나, 이번 범위는 `.claude/skills/`에 한정

### Decision-Log Candidates
- **Overview 섹션 위치**: Responsibility 바로 다음에 배치. Responsibility는 "하는 일/안 하는 일" 경계 정의에 집중하고, Overview는 "어떻게/왜"를 담당하는 역할 분리
- **서술형 vs 구조화 균형**: Overview는 의도적으로 서술형(prose)을 허용하는 유일한 MUST 섹션. 나머지는 테이블/리스트 우선 유지

<!-- spec-update-todo-input-end -->

---

# Part 2: Implementation Plan

## Overview

SDD_SPEC_REQUIREMENTS.md의 5가지 변경사항을 `.claude/skills/` 아래의 7개 스펙 관련 스킬에 반영한다. 핵심 변경은:

1. **컴포넌트 스펙 템플릿에 `Overview` MUST 섹션 추가** (spec-create)
2. **스킬별 컴포넌트 섹션 리스트/체크리스트에 Overview 포함** (spec-review, spec-rewrite, spec-update-done/todo, spec-summary)
3. **"변경 우선(change-first)" → "이해와 변경의 균형(understand-then-change)" 철학 반영** (spec-create, spec-summary)
4. **Runtime Map 서술형 가이드 보강** (spec-create)
5. **feature-draft의 컴포넌트 패치에 Overview 포함** (feature-draft)

## Scope

### In Scope
- `.claude/skills/` 아래 7개 스킬의 SKILL.md 및 references/examples 수정
- `_sdd/spec/spec-lifecycle.md` Change Recipes 갱신

### Out of Scope
- `.codex/skills/` 동일 스킬 반영 (별도 후속 작업)
- 이미 완료된 `docs/SDD_SPEC_REQUIREMENTS.md` 수정
- 기존 사용자 프로젝트 스펙의 마이그레이션

## Components

1. **spec-create**: 템플릿과 가이드라인의 원본. 가장 큰 변경
2. **spec-review**: 품질 검증 체크리스트에 Overview 반영
3. **spec-rewrite**: 재작성 시 Overview 포함 보장
4. **spec-update-done**: 드리프트 패턴에 Overview 누락 감지 추가
5. **spec-update-todo**: 섹션 매핑에 Overview 추가
6. **spec-summary**: 요약 시 Overview 정보 포함
7. **feature-draft**: 새 컴포넌트 패치에 Overview 필드 추가

## Implementation Phases

### Phase 1: 핵심 템플릿 및 원본 스킬 (spec-create)
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 1 | spec-create 컴포넌트 템플릿에 Overview 섹션 추가 | P0 | - | spec-create |
| 2 | spec-create Runtime Map 템플릿 서술형 보강 | P0 | - | spec-create |
| 3 | spec-create Writing Guidance 철학 변경 반영 | P0 | - | spec-create |
| 4 | spec-create 예시 파일에 Overview 반영 | P1 | 1 | spec-create |

### Phase 2: 검증/동기화 스킬 (spec-review, spec-rewrite, spec-update-*)
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 5 | spec-review 체크리스트에 Overview 검증 추가 | P1 | 1 | spec-review |
| 6 | spec-rewrite 체크리스트에 Overview 포함 보장 | P1 | 1 | spec-rewrite |
| 7 | spec-update-done 드리프트 패턴에 Overview 누락 추가 | P1 | 1 | spec-update-done |
| 8 | spec-update-todo 섹션 매핑에 Overview 추가 | P1 | 1 | spec-update-todo |

### Phase 3: 보조 스킬 + 스펙 갱신
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 9  | spec-summary 요약 템플릿에 Overview 반영 | P2 | 1 | spec-summary |
| 10 | feature-draft 컴포넌트 패치에 Overview 추가 | P2 | 1 | feature-draft |
| 11 | spec-lifecycle.md Change Recipes 갱신 | P2 | 1-10 | spec |

## Task Details

### Task 1: spec-create 컴포넌트 템플릿에 Overview 섹션 추가
**Component**: spec-create
**Priority**: P0-Critical
**Type**: Feature

**Description**:
`references/template-full.md`의 컴포넌트 스펙 템플릿에 `## Overview` 섹션을 `## Responsibility` 다음에 추가한다. 하위 구조: `### 동작 개요` + `### 설계 의도`.

**Acceptance Criteria**:
- [ ] `references/template-full.md` 컴포넌트 템플릿에 `## Overview` MUST 섹션이 Responsibility 바로 다음에 존재
- [ ] Overview 하위에 `### 동작 개요`와 `### 설계 의도` 서브섹션 포함
- [ ] 각 서브섹션에 가이드 코멘트(무엇을 써야 하는지) 포함

**Target Files**:
- [M] `.claude/skills/spec-create/references/template-full.md` -- 컴포넌트 스펙 템플릿에 Overview 섹션 추가

**Technical Notes**:
- 현재 템플릿 구조: Responsibility → Owned Paths → Key Symbols → ...
- 변경 후: Responsibility → **Overview** → Owned Paths → Key Symbols → ...
- SDD_SPEC_REQUIREMENTS.md §6.5의 좋은/나쁜 예시를 참고하여 가이드 작성

**Dependencies**: -

---

### Task 2: spec-create Runtime Map 템플릿 서술형 보강
**Component**: spec-create
**Priority**: P0-Critical
**Type**: Feature

**Description**:
`references/template-full.md`의 메인 스펙 Runtime Map 템플릿에 서술형 동작 시나리오 가이드를 추가한다. 기존 다이어그램/흐름 리스트는 유지하면서, 사용자 관점의 시나리오 서술을 권장하는 구조를 추가한다.

**Acceptance Criteria**:
- [ ] Runtime Map 템플릿에 "서술형 동작 시나리오" 서브섹션 또는 가이드 포함
- [ ] 기존 다이어그램/흐름 구조는 유지
- [ ] 서술형 시나리오가 "사용자 관점"임을 명시

**Target Files**:
- [M] `.claude/skills/spec-create/references/template-full.md` -- Runtime Map 섹션 보강

**Dependencies**: -

---

### Task 3: spec-create Writing Guidance 철학 변경 반영
**Component**: spec-create
**Priority**: P0-Critical
**Type**: Improvement

**Description**:
SKILL.md의 Writing Guidance에서 "변경 우선(change-first)" 톤을 "이해와 변경의 균형(understand-then-change)"으로 조정한다. "Favor tables with actual paths over long narrative" 가이드라인에 Overview 섹션에서는 서술형이 권장된다는 예외를 추가한다.

**Acceptance Criteria**:
- [ ] Writing Guidance에서 "change-first" 또는 "변경 우선" 표현이 "understand-then-change" / "이해와 변경의 균형"으로 변경
- [ ] Overview 섹션에서는 서술형 설명이 권장된다는 가이드 추가
- [ ] 기존 경로/테이블 우선 원칙은 Overview 외 섹션에서 유지

**Target Files**:
- [M] `.claude/skills/spec-create/SKILL.md` -- Writing Guidance 섹션 수정

**Technical Notes**:
- 현재 L322: "Start with the repository map and runtime map before writing detailed component prose"
- 현재 L323: "Favor tables with actual paths over long narrative"
- 이 원칙들은 유지하되, Overview 섹션 관련 예외와 철학 전환을 반영

**Dependencies**: -

---

### Task 4: spec-create 예시 파일에 Overview 반영
**Component**: spec-create
**Priority**: P1-High
**Type**: Feature

**Description**:
`examples/simple-project-spec.md`와 `examples/complex-project-spec.md`의 컴포넌트 스펙 부분에 Overview 섹션 예시를 추가한다.

**Acceptance Criteria**:
- [ ] `simple-project-spec.md` 내 컴포넌트 스펙에 Overview 섹션 포함
- [ ] `complex-project-spec.md` 내 컴포넌트 스펙에 Overview 섹션 포함
- [ ] 예시가 SDD_SPEC_REQUIREMENTS.md §6.5의 "좋은 예시" 스타일을 따름

**Target Files**:
- [M] `.claude/skills/spec-create/examples/simple-project-spec.md` -- Overview 예시 추가
- [M] `.claude/skills/spec-create/examples/complex-project-spec.md` -- Overview 예시 추가

**Dependencies**: 1

---

### Task 5: spec-review 체크리스트에 Overview 검증 추가
**Component**: spec-review
**Priority**: P1-High
**Type**: Feature

**Description**:
`references/review-checklist.md`와 SKILL.md의 품질 평가 기준에 Overview 섹션 존재 여부 및 품질 검증 항목을 추가한다.

**Acceptance Criteria**:
- [ ] 체크리스트에 "컴포넌트 스펙에 Overview 섹션이 있는가?" 항목 추가
- [ ] "Overview가 코드 구현 복사가 아닌 사용자 관점 동작 설명인가?" 품질 항목 추가
- [ ] Overview 누락 시 severity 수준 정의 (MUST 섹션이므로 High)

**Target Files**:
- [M] `.claude/skills/spec-review/SKILL.md` -- 리뷰 차원/기준에 Overview 반영
- [M] `.claude/skills/spec-review/references/review-checklist.md` -- 체크리스트 항목 추가

**Dependencies**: 1

---

### Task 6: spec-rewrite 체크리스트에 Overview 포함 보장
**Component**: spec-rewrite
**Priority**: P1-High
**Type**: Feature

**Description**:
`references/rewrite-checklist.md`와 SKILL.md의 재작성 품질 기준에 Overview 섹션 생성/보존을 추가한다.

**Acceptance Criteria**:
- [ ] 재작성 체크리스트에 "Overview 섹션이 포함되었는가?" 항목 추가
- [ ] 앵커 섹션 보존 규칙에 Overview 언급
- [ ] 재작성 시 기존 Overview 내용 보존 원칙 명시

**Target Files**:
- [M] `.claude/skills/spec-rewrite/SKILL.md` -- 앵커 섹션 및 품질 기준에 Overview 추가
- [M] `.claude/skills/spec-rewrite/references/rewrite-checklist.md` -- 체크리스트 항목 추가

**Dependencies**: 1

---

### Task 7: spec-update-done 드리프트 패턴에 Overview 누락 추가
**Component**: spec-update-done
**Priority**: P1-High
**Type**: Feature

**Description**:
`references/drift-patterns.md`에 "Overview 섹션 누락 또는 구현과 불일치" 드리프트 패턴을 추가하고, SKILL.md의 섹션별 업데이트 로직에 Overview 처리를 포함한다.

**Acceptance Criteria**:
- [ ] drift-patterns.md에 "Missing or stale Overview" 패턴 추가
- [ ] SKILL.md의 section-by-section update 로직에 Overview 포함
- [ ] Overview가 MUST 섹션으로 분류되어, 컴포넌트 스펙에 없으면 추가 대상이 됨

**Target Files**:
- [M] `.claude/skills/spec-update-done/SKILL.md` -- 섹션별 업데이트에 Overview 추가
- [M] `.claude/skills/spec-update-done/references/drift-patterns.md` -- Overview 드리프트 패턴 추가

**Dependencies**: 1

---

### Task 8: spec-update-todo 섹션 매핑에 Overview 추가
**Component**: spec-update-todo
**Priority**: P1-High
**Type**: Feature

**Description**:
`references/section-mapping.md`에 Overview 관련 입력 유형 → 타겟 섹션 매핑을 추가하고, SKILL.md의 앵커 섹션 리스트에 Overview를 포함한다.

**Acceptance Criteria**:
- [ ] section-mapping.md에 "동작 변경 / 설계 의도 변경 → Component Spec > Overview" 매핑 추가
- [ ] SKILL.md의 앵커 섹션 리스트 또는 컴포넌트 스펙 섹션 참조에 Overview 포함

**Target Files**:
- [M] `.claude/skills/spec-update-todo/SKILL.md` -- 컴포넌트 섹션 참조에 Overview 추가
- [M] `.claude/skills/spec-update-todo/references/section-mapping.md` -- 매핑 테이블에 Overview 추가

**Dependencies**: 1

---

### Task 9: spec-summary 요약 템플릿에 Overview 반영
**Component**: spec-summary
**Priority**: P2-Medium
**Type**: Feature

**Description**:
`references/summary-template.md`와 SKILL.md에서 컴포넌트 요약 시 Overview 정보(동작 개요)를 포함하도록 한다. 또한 "change-first" 참조를 "understand-then-change"로 갱신한다.

**Acceptance Criteria**:
- [ ] 요약 템플릿의 컴포넌트 섹션에 Overview/동작 개요 정보 포함 구조 추가
- [ ] SKILL.md의 "change-first" 참조를 "understand-then-change"로 변경
- [ ] 기존 토큰 효율 원칙은 유지 (Overview 요약은 간결하게)

**Target Files**:
- [M] `.claude/skills/spec-summary/SKILL.md` -- 철학 참조 변경 + 컴포넌트 요약에 Overview 포함
- [M] `.claude/skills/spec-summary/references/summary-template.md` -- 요약 템플릿에 Overview 필드 추가

**Dependencies**: 1

---

### Task 10: feature-draft 컴포넌트 패치에 Overview 추가
**Component**: feature-draft
**Priority**: P2-Medium
**Type**: Feature

**Description**:
SKILL.md의 Part 1 "Component Changes" 포맷에 `Overview` 필드를 추가한다. 새 컴포넌트 제안 시 동작 개요와 설계 의도를 함께 기술하도록 한다.

**Acceptance Criteria**:
- [ ] Part 1의 "New Component" 템플릿에 `Overview` 필드 추가 (동작 개요 + 설계 의도)
- [ ] Overview 필드가 Responsibility 바로 다음에 위치

**Target Files**:
- [M] `.claude/skills/feature-draft/SKILL.md` -- Component Changes 포맷에 Overview 추가

**Dependencies**: 1

---

### Task 11: spec-lifecycle.md Change Recipes 갱신
**Component**: spec
**Priority**: P2-Medium
**Type**: Improvement

**Description**:
`_sdd/spec/spec-lifecycle.md`의 Change Recipes에 "Overview 섹션을 스킬에 추가/수정할 때"의 경로를 추가한다.

**Acceptance Criteria**:
- [ ] Change Recipes에 Overview 관련 변경 시 확인해야 할 파일 목록 추가
- [ ] 검증 포인트 포함

**Target Files**:
- [M] `_sdd/spec/spec-lifecycle.md` -- Change Recipes에 Overview 관련 경로 추가

**Dependencies**: 1-10

---

## Parallel Execution Summary

| Phase | Total Tasks | Max Parallel | Sequential (conflicts) |
|-------|-------------|--------------|----------------------|
| 1     | 4           | 3            | 1 (Task 4 depends on 1; Tasks 1,2 share template-full.md) |
| 2     | 4           | 4            | 0 |
| 3     | 3           | 2            | 1 (Task 11 depends on all) |

> **Phase 1 주의**: Task 1과 Task 2는 같은 파일(`template-full.md`)을 수정하므로 순차 실행 권장. Task 3은 다른 파일이므로 병렬 가능.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Overview 섹션이 코드 복사 덤프가 될 수 있음 | 스펙 품질 저하 | §6.5 나쁜/좋은 예시를 모든 관련 스킬에 참조시킴 |
| `.codex/skills/`와의 드리프트 확대 | 플랫폼 간 불일치 | 이번 작업 후 별도 codex 정렬 작업 계획 |
| 토큰 사용량 증가 (서술형 추가) | LLM 컨텍스트 압박 | Overview는 2-3문단 권장 상한을 가이드에 명시 |
| 기존 스펙에 Overview 누락 경고 폭주 | spec-review 노이즈 | 기존 스펙은 "추가 권장" 수준으로, 신규 생성 시만 MUST 적용 |

## Open Questions

- [ ] `.codex/skills/` 동일 스킬에 대한 반영 시점과 방법 (수동 동기화 vs 별도 작업)
- [ ] Overview의 권장 분량 상한을 명시할지 (예: 2-3문단, 200단어 이내)
- [ ] 기존 프로젝트 스펙에 Overview가 없는 경우 spec-review가 어떤 severity로 보고할지 (High vs Medium)

## Model Recommendation

각 태스크가 단일 SKILL.md 또는 reference 파일의 특정 섹션만 수정하는 비교적 단순한 문서 편집이므로, **Sonnet 4.6** (`claude-sonnet-4-6`)으로 충분합니다. 다만 Phase 1의 Task 1-3은 전체 맥락 이해가 필요하므로 **Opus 4.6**이 권장됩니다.
