# Feature Draft: 전체 SDD 스킬 품질 복원 + 탐색/변경 강화

**날짜**: 2026-03-09
**근거**: `_sdd/discussion/discussion_spec_create_quality_regression.md`
**변경된 요구사항**: `docs/SDD_SPEC_REQUIREMENTS.md` (변경 없음, 현재 상태 유지)

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

### Improvement: 전체 스킬 24618c3 기반 복원
**Priority**: High
**Target Section**: `_sdd/spec/spec-lifecycle.md` > `Change Recipes`
**Current State**: 234c4f3 커밋에서 모든 스킬이 exploration-first로 전환되면서 이해 깊이(예시, 서술, 설계 결정 테이블)가 대폭 축소됨
**Proposed**: 234c4f3~HEAD 범위의 .claude/skills/ 변경을 revert하고, 유용한 3가지 변경(Overview MUST, Drift 추적, Quality Gate)만 선별 재적용
**Reason**: 스킬이 생성하는 스펙 문서가 너무 간략해져서 사람이 프로젝트를 이해할 수 없게 됨. 이해와 탐색 모두 중요

### Improvement: 4단계 워크플로우 제거
**Priority**: Medium
**Target Section**: `_sdd/spec/spec-lifecycle.md` > `Workflow`
**Current State**: 모든 스킬에 "spec-create → feature-draft → implementation → spec-update-done" 4단계 파이프라인이 삽입됨
**Proposed**: 4단계 워크플로우 참조 제거
**Reason**: 사용자 결정사항

## Notes

### Context
- `docs/SDD_SPEC_REQUIREMENTS.md`는 변경 없이 현재 상태 유지
- `.codex/skills/`는 이번 범위에서 제외 (별도 후속 작업)
- 이번 작업은 `.claude/skills/`에 한정

### Decision-Log Candidates
- **복원 방식**: git revert 후 선별 재적용을 선택. 이유: 이전 버전이 이해 가능한 스펙을 생성했으므로 그 기반으로 돌아가는 것이 가장 안전
- **재적용 범위**: Overview MUST, Drift 추적 + 앵커 섹션, Quality Gate만 유지. 이유: 이 3가지는 이전 버전에 없던 순수 개선이므로 가치가 있음
- **4단계 워크플로우 제거**: 사용자가 워크플로우 강제보다 자유로운 스킬 조합을 선호

<!-- spec-update-todo-input-end -->

---

# Part 2: Implementation Plan

## Overview

234c4f3~HEAD 범위에서 `.claude/skills/`를 수정한 4개 커밋(234c4f3, c77ca35, f7cce37, 0326a35)을 revert하고, 유용한 변경 3가지(Overview MUST 섹션, Drift 추적 + 앵커 섹션, Quality Gate)를 선별 재적용한다.

> **주의**: 120052f(sdd-upgrade)와 a8af2e6(spec-snapshot)은 새 스킬 추가이므로 revert 대상에서 제외한다.

## Scope

### In Scope
- `.claude/skills/` 아래 기존 스킬의 SKILL.md 및 references/examples 복원
- 복원 후 3가지 유용한 변경 재적용
- 4단계 워크플로우 참조 제거 확인

### Out of Scope
- `.codex/skills/` 동일 스킬 반영 (별도 후속 작업)
- `docs/SDD_SPEC_REQUIREMENTS.md` 변경 (현재 상태 유지)
- 새로 추가된 스킬(sdd-upgrade, spec-snapshot) — 이것들은 유지

## Components

1. **git revert**: 4개 커밋을 역순으로 revert (0326a35 → f7cce37 → c77ca35 → 234c4f3)
2. **Overview 재적용**: 컴포넌트 스펙에 Overview MUST 섹션 재추가
3. **Drift 추적 재적용**: MUST/CONSIDER/NO 분류, 앵커 섹션 추적 규칙 재추가
4. **Quality Gate 재적용**: spec-create의 Step 4.5 LLM-as-Judge 재추가
5. **4단계 워크플로우 제거 확인**: revert로 제거되었는지 검증

## Implementation Phases

### Phase 1: Git Revert (순차 실행 필수)
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 1 | 0326a35 revert (Overview MUST 커밋) | P0 | - | git revert |
| 2 | f7cce37 revert (subdirectory split 커밋) | P0 | 1 | git revert |
| 3 | c77ca35 revert (Quality Gate 커밋) | P0 | 2 | git revert |
| 4 | 234c4f3 revert (exploration-first 전환 커밋) | P0 | 3 | git revert |

### Phase 2: 유용한 변경 재적용 (병렬 가능)
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 5 | Overview MUST 섹션 재적용 (7개 스킬) | P0 | 4 | Overview 재적용 |
| 6 | Drift 추적 + 앵커 섹션 규칙 재적용 | P1 | 4 | Drift 추적 재적용 |
| 7 | Quality Gate (Step 4.5) 재적용 | P1 | 4 | Quality Gate 재적용 |

### Phase 3: 검증
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 8 | 4단계 워크플로우 제거 확인 + 전체 일관성 검증 | P1 | 5, 6, 7 | 검증 |

## Task Details

### Task 1: 0326a35 revert
**Component**: git revert
**Priority**: P0-Critical
**Type**: Infrastructure

**Description**:
`git revert 0326a35` — "Add Overview MUST section to component spec across 7 skills" 커밋을 revert한다. 이 커밋의 변경은 Task 5에서 더 나은 형태로 재적용되므로 먼저 제거한다.

**Acceptance Criteria**:
- [ ] revert 커밋이 성공적으로 생성됨
- [ ] 충돌이 있으면 해결

**Target Files**:
- [M] `.claude/skills/spec-create/references/template-full.md`
- [M] `.claude/skills/spec-create/SKILL.md`
- [M] `.claude/skills/spec-create/examples/simple-project-spec.md`
- [M] `.claude/skills/spec-create/examples/complex-project-spec.md`
- [M] `.claude/skills/spec-review/SKILL.md`
- [M] `.claude/skills/spec-review/references/review-checklist.md`
- [M] `.claude/skills/spec-rewrite/SKILL.md`
- [M] `.claude/skills/spec-rewrite/references/rewrite-checklist.md`
- [M] `.claude/skills/spec-summary/SKILL.md`
- [M] `.claude/skills/spec-summary/references/summary-template.md`
- [M] `.claude/skills/spec-update-done/SKILL.md`
- [M] `.claude/skills/spec-update-done/references/drift-patterns.md`
- [M] `.claude/skills/spec-update-todo/SKILL.md`
- [M] `.claude/skills/spec-update-todo/references/section-mapping.md`
- [M] `.claude/skills/feature-draft/SKILL.md`
- [M] `_sdd/spec/spec-lifecycle.md`

**Dependencies**: -

---

### Task 2: f7cce37 revert
**Component**: git revert
**Priority**: P0-Critical
**Type**: Infrastructure

**Description**:
`git revert f7cce37` — "Add subdirectory split guidelines" 커밋을 revert한다.

**Acceptance Criteria**:
- [ ] revert 커밋이 성공적으로 생성됨

**Target Files**:
- [M] `.claude/skills/spec-create/SKILL.md`
- [M] `.claude/skills/spec-rewrite/SKILL.md`

**Dependencies**: 1

---

### Task 3: c77ca35 revert
**Component**: git revert
**Priority**: P0-Critical
**Type**: Infrastructure

**Description**:
`git revert c77ca35` — "Add LLM-as-Judge Quality Gate" 커밋을 revert한다. Quality Gate는 Task 7에서 재적용된다.

**Acceptance Criteria**:
- [ ] revert 커밋이 성공적으로 생성됨

**Target Files**:
- [M] `.claude/skills/spec-create/SKILL.md`
- [M] 기타 Quality Gate가 추가된 스킬 파일들

**Dependencies**: 2

---

### Task 4: 234c4f3 revert
**Component**: git revert
**Priority**: P0-Critical
**Type**: Infrastructure

**Description**:
`git revert 234c4f3` — "Align all Claude Code skills with exploration-first SDD philosophy" 핵심 커밋을 revert한다. 이것이 가장 큰 변경이며, 이 revert 후 모든 스킬이 24618c3 상태로 복원된다.

**Acceptance Criteria**:
- [ ] revert 커밋이 성공적으로 생성됨
- [ ] 모든 스킬이 exploration-first 전환 이전 상태로 복원됨
- [ ] 충돌 해결 완료

**Target Files**:
- [M] `.claude/skills/spec-create/SKILL.md`
- [M] `.claude/skills/spec-create/references/template-full.md`
- [M] `.claude/skills/spec-create/references/examples.md`
- [M] `.claude/skills/spec-create/examples/simple-project-spec.md`
- [M] `.claude/skills/spec-create/examples/complex-project-spec.md`
- [M] `.claude/skills/spec-review/SKILL.md`
- [M] `.claude/skills/spec-review/references/review-checklist.md`
- [M] `.claude/skills/spec-rewrite/SKILL.md`
- [M] `.claude/skills/spec-rewrite/references/rewrite-checklist.md`
- [M] `.claude/skills/spec-summary/SKILL.md`
- [M] `.claude/skills/spec-summary/references/summary-template.md`
- [M] `.claude/skills/spec-update-done/SKILL.md`
- [M] `.claude/skills/spec-update-done/references/drift-patterns.md`
- [M] `.claude/skills/spec-update-todo/SKILL.md`
- [M] `.claude/skills/spec-update-todo/references/section-mapping.md`
- [M] `.claude/skills/feature-draft/SKILL.md`
- [M] `.claude/skills/implementation/SKILL.md`
- [M] `.claude/skills/implementation-plan/SKILL.md`
- [M] `.claude/skills/implementation-review/SKILL.md`
- [M] `.claude/skills/pr-review/SKILL.md`
- [M] `.claude/skills/pr-spec-patch/SKILL.md`
- [M] `.claude/skills/discussion/SKILL.md`

**Dependencies**: 3

---

### Task 5: Overview MUST 섹션 재적용
**Component**: Overview 재적용
**Priority**: P0-Critical
**Type**: Feature

**Description**:
revert로 제거된 Overview MUST 섹션을 24618c3 기반 스킬에 다시 추가한다. `docs/SDD_SPEC_REQUIREMENTS.md` §5, §6.5를 참고하여 다음 스킬에 반영:

1. **spec-create**: template-full.md 컴포넌트 템플릿에 Overview 섹션 (Responsibility 다음), Writing Guidance에 overview 언급, 예시 파일에 Overview 예시
2. **spec-review**: review-checklist에 Overview 검증 항목
3. **spec-rewrite**: rewrite-checklist에 Overview 보존 항목
4. **spec-update-done**: drift-patterns에 "Missing/stale Overview" 패턴
5. **spec-update-todo**: section-mapping에 Overview 매핑
6. **spec-summary**: summary-template에 Overview 요약 필드
7. **feature-draft**: Component Changes 포맷에 Overview 필드

기존 구현(0326a35)을 참고하되, 이전 버전의 풍부한 예시 스타일을 유지한다.

**Acceptance Criteria**:
- [ ] 7개 스킬 모두에 Overview 관련 변경이 반영됨
- [ ] template-full.md에 Overview MUST 섹션이 Responsibility 다음에 위치
- [ ] 예시 파일에 §6.5 스타일의 구체적 Overview 예시 포함
- [ ] spec-lifecycle.md의 Change Recipes에 Overview 경로 추가

**Target Files**:
- [M] `.claude/skills/spec-create/references/template-full.md`
- [M] `.claude/skills/spec-create/SKILL.md`
- [M] `.claude/skills/spec-create/examples/simple-project-spec.md`
- [M] `.claude/skills/spec-create/examples/complex-project-spec.md`
- [M] `.claude/skills/spec-review/SKILL.md`
- [M] `.claude/skills/spec-review/references/review-checklist.md`
- [M] `.claude/skills/spec-rewrite/SKILL.md`
- [M] `.claude/skills/spec-rewrite/references/rewrite-checklist.md`
- [M] `.claude/skills/spec-summary/SKILL.md`
- [M] `.claude/skills/spec-summary/references/summary-template.md`
- [M] `.claude/skills/spec-update-done/SKILL.md`
- [M] `.claude/skills/spec-update-done/references/drift-patterns.md`
- [M] `.claude/skills/spec-update-todo/SKILL.md`
- [M] `.claude/skills/spec-update-todo/references/section-mapping.md`
- [M] `.claude/skills/feature-draft/SKILL.md`
- [M] `_sdd/spec/spec-lifecycle.md`

**Technical Notes**:
- 0326a35 커밋의 변경 내용을 참고하되, 24618c3 기반 스킬 구조에 맞게 적용
- §6.5의 좋은/나쁜 예시를 참조하여 가이드 작성
- Overview는 서술형(prose)이 권장되는 유일한 MUST 섹션

**Dependencies**: 4

---

### Task 6: Drift 추적 + 앵커 섹션 규칙 재적용
**Component**: Drift 추적 재적용
**Priority**: P1-High
**Type**: Feature

**Description**:
234c4f3에서 도입된 유용한 drift 추적 규칙을 24618c3 기반 스킬에 선별 재적용한다:

1. **MUST/CONSIDER/NO update 분류**: implementation, spec-update-done, spec-update-todo 스킬에 스펙 갱신 기준(§8) 분류 규칙 추가
2. **앵커 섹션 추적**: 스펙 변경 시 영향받는 앵커 섹션을 명시하는 규칙 (Goal, Architecture Overview, Component Details, Environment & Dependencies, Identified Issues, Usage Examples, Open Questions)
3. **evidence 링크**: drift 보고 시 `file:line`, 테스트명, diff 근거 포함 규칙

적용 대상 스킬:
- implementation: Hard Rules에 drift 보고 규칙 추가
- implementation-plan: 갭 분류(MUST/CONSIDER/NO) 규칙 추가
- spec-update-done: 섹션별 갱신 분류 규칙 추가
- spec-update-todo: 앵커 섹션 매핑 규칙 추가
- feature-draft: 앵커 인식 드래프팅 규칙 추가

**Acceptance Criteria**:
- [ ] 5개 스킬에 drift/앵커 관련 규칙이 추가됨
- [ ] MUST/CONSIDER/NO 분류가 §8 기준과 일치
- [ ] 앵커 섹션 목록이 §5와 일치

**Target Files**:
- [M] `.claude/skills/implementation/SKILL.md`
- [M] `.claude/skills/implementation-plan/SKILL.md`
- [M] `.claude/skills/spec-update-done/SKILL.md`
- [M] `.claude/skills/spec-update-todo/SKILL.md`
- [M] `.claude/skills/feature-draft/SKILL.md`

**Technical Notes**:
- 234c4f3의 해당 변경 부분을 참고하되, 이전 스킬 구조에 자연스럽게 통합
- 4단계 워크플로우 참조는 포함하지 않음
- 기존 스킬의 설명 깊이와 예시 스타일을 유지

**Dependencies**: 4

---

### Task 7: Quality Gate (Step 4.5) 재적용
**Component**: Quality Gate 재적용
**Priority**: P1-High
**Type**: Feature

**Description**:
c77ca35에서 도입된 LLM-as-Judge Quality Gate를 spec-create 스킬에 재적용한다.

Step 4 (Output Validation) 이후에 Step 4.5를 추가:
- 4 Criteria: Understand, Locate, Change, Remember
- 각 기준에 PASS/WEAK/FAIL 판정표
- FAIL 시 Step 3으로 돌아가 보강
- 판정만 수행, 수정은 이전 단계에서

**Acceptance Criteria**:
- [ ] spec-create SKILL.md에 Step 4.5 Quality Gate가 추가됨
- [ ] 4개 Criteria 각각에 Probe + PASS/WEAK/FAIL 판정 기준 포함
- [ ] FAIL 시 Step 3 복귀 로직 명시

**Target Files**:
- [M] `.claude/skills/spec-create/SKILL.md`

**Technical Notes**:
- c77ca35의 Quality Gate 내용을 참고
- §11 품질 체크리스트와의 매핑도 고려하되, 기본적으로 4 Criteria 구조 유지
- 이전 스킬의 Step 번호 체계에 맞게 조정

**Dependencies**: 4

---

### Task 8: 전체 일관성 검증
**Component**: 검증
**Priority**: P1-High
**Type**: Test

**Description**:
모든 작업 완료 후 전체 스킬의 일관성을 검증한다:

1. **4단계 워크플로우 제거 확인**: 모든 스킬에서 "spec-create → feature-draft → implementation → spec-update-done" 참조가 없는지 검증
2. **이해 깊이 복원 확인**: 예시 파일이 구체적이고 풍부한지, placeholder가 아닌 실제 내용인지 확인
3. **Overview MUST 반영 확인**: 7개 스킬 모두에 Overview 관련 변경이 올바르게 적용되었는지
4. **Drift 규칙 반영 확인**: MUST/CONSIDER/NO 분류와 앵커 섹션 추적이 올바른지
5. **Quality Gate 반영 확인**: spec-create에 Step 4.5가 올바르게 추가되었는지
6. **새 스킬 보존 확인**: sdd-upgrade, spec-snapshot 스킬이 영향받지 않았는지

**Acceptance Criteria**:
- [ ] 모든 스킬에서 4단계 워크플로우 참조 없음
- [ ] spec-create 예시 파일이 이전 수준의 구체성 보유
- [ ] 재적용 3가지가 모두 올바르게 동작
- [ ] sdd-upgrade, spec-snapshot 스킬 무결

**Target Files**:
- (읽기 전용 검증 — 파일 수정 없음)

**Dependencies**: 5, 6, 7

---

## Parallel Execution Summary

| Phase | Total Tasks | Max Parallel | Sequential (conflicts) |
|-------|-------------|--------------|----------------------|
| 1     | 4           | 1            | 4 (git revert 순차 필수) |
| 2     | 3           | 2            | 1 (Task 5와 6은 feature-draft SKILL.md 공유) |
| 3     | 1           | 1            | 0 |

> **Phase 2 주의**: Task 5와 Task 6은 `feature-draft/SKILL.md`를 공유하므로 순차 실행 권장. Task 7은 `spec-create/SKILL.md`만 수정하므로 Task 5/6과 병렬 가능.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| git revert 시 충돌 발생 | 작업 지연 | 역순 revert로 충돌 최소화, 충돌 시 수동 해결 |
| revert로 새 스킬(sdd-upgrade, spec-snapshot)이 영향받음 | 기능 손실 | 이 두 커밋은 revert 대상에서 명시적 제외 |
| 재적용 시 이전 스킬 구조와 맞지 않는 부분 발생 | 비일관성 | 각 재적용을 이전 스킬 구조에 맞게 조정 |
| .codex/skills/와의 드리프트 확대 | 플랫폼 간 불일치 | 이번 작업 후 별도 codex 정렬 작업 계획 |

## Open Questions

- [ ] revert 시 충돌이 발생하면 squash revert(단일 커밋)로 전환할지, 개별 revert를 유지할지
- [ ] Phase 2에서 이전 커밋(0326a35)의 변경 내용을 그대로 재적용할지, 이전 스킬 구조에 맞게 재작성할지
- [ ] `.codex/skills/` 동기화 시점

## Model Recommendation

Phase 1(git revert)은 사람이 직접 실행하거나 충돌 해결이 필요하므로 **Opus 4.6** 권장.
Phase 2(재적용)은 이전 커밋 참고 + 구조 적응이 필요하므로 **Opus 4.6** 권장.
Phase 3(검증)은 **Sonnet 4.6**으로 충분.
