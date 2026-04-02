# Feature Draft: PR Review Unification

**Date**: 2026-04-02
**Author**: malfo.y
**Target Spec**: `_sdd/spec/main.md`
**Status**: Draft
**Discussion**: `_sdd/discussion/discussion_pr_review_unification.md`

---

<!-- spec-update-todo-input-start -->
# Part 1: Spec Patch Draft

> This patch can be copy-pasted into the corresponding spec section,
> or used as input for the `spec-update-todo` skill.

# Spec Update Input

**Date**: 2026-04-02
**Author**: malfo.y
**Target Spec**: `_sdd/spec/main.md`

## Improvements

### Improvement: pr-spec-patch + pr-review 통합
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Component Details`
**Current State**: pr-spec-patch(패치 초안 생성)와 pr-review(리뷰 보고서 생성)가 별도 스킬로 분리. 항상 순차 실행 필요.
**Proposed**: 단일 pr-review 스킬로 통합. PR 주소/번호 입력 → spec 로딩(from-branch 우선) → diff 분석 → 코드 품질 검증(항상) + spec 기반 검증(spec 존재 시) → verdict → PR_REVIEW.md 생성.
**Reason**: 두 스킬이 항상 묶여서 실행되므로 분리 의미 없음. 중간 산출물(spec_patch_draft.md) 제거하여 워크플로우 단순화.

### Improvement: spec 선택 로직 변경
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Component Details > pr-review`
**Current State**: 로컬 _sdd/spec/ 디렉토리의 spec을 사용. PR의 base/head 브랜치 구분 없음.
**Proposed**: from-branch(head) spec을 검증 기준으로 사용. to-branch(base) spec은 변경 비교 참고용만. from-branch에 spec이 없으면 code-only 검증.
**Reason**: to-branch spec은 이전 계약. from-branch가 머지 후 상태를 나타내므로 이것이 검증 기준이어야 함.

### Improvement: 검증 모드 재구조화
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Component Details > pr-review`
**Current State**: spec 있으면 full review, 없으면 degraded mode(confidence 낮음 표기).
**Proposed**: code-only를 베이스 모드로, spec-based는 추가 레이어. code-only: PR 설명 기반 AC 추론, 코드 품질, 에러 처리, 테스트, 보안. spec-based: code-only + from-branch spec 기반 AC 검증, spec compliance, gap analysis.
**Reason**: spec 없어도 코드 품질 검증은 충분히 가능. "confidence 낮음"이 아니라 적극적으로 검증해야 함.

## Component Changes

### Remove Component: pr-spec-patch
**Target Section**: `_sdd/spec/main.md` > `Component Details`
**Purpose**: pr-review에 통합되어 독립 스킬로서의 역할 소멸. spec_patch_draft.md 산출물도 불필요.

### Update Component: pr-review
**Target Section**: `_sdd/spec/main.md` > `Component Details > pr-review`
**Purpose**: pr-spec-patch 기능 흡수 + spec 선택 로직 변경 + 검증 모드 재구조화

## Design Changes

### Design Change: 임시 스펙 유형에서 spec_patch_draft 제거
**Priority**: Medium
**Target Section**: `_sdd/spec/main.md` > `Core Design` (두 단계 스펙 구조)
**Description**: 임시 스펙 유형이 `feature_draft`, `spec_patch_draft`에서 `feature_draft`만으로 축소. PR 기반 스펙 패치 초안 개념 자체가 불필요해짐 (머지 후 /spec-update-todo로 대체).

### Design Change: PR 워크플로우 단순화
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Usage Guide & Expected Results`
**Description**: 기존 `PR → pr-spec-patch → pr-review → spec-update-todo` 흐름이 `PR → pr-review → (머지 후) spec-update-todo`로 단순화. `_sdd/pr/spec_patch_draft.md` 아티팩트 제거.

## Notes

- `_sdd/pr/` 디렉토리는 PR_REVIEW.md 용도로 유지
- docs/SDD_WORKFLOW.md, docs/en/SDD_WORKFLOW.md의 워크플로우 설명도 업데이트 필요
- sdd-autopilot reasoning reference의 임시 스펙 설명도 업데이트 필요
<!-- spec-update-todo-input-end -->

---

# Part 2: Implementation Plan

## Overview

pr-spec-patch와 pr-review를 단일 pr-review 스킬로 통합한다. 새 스킬은 PR 주소 입력만으로 spec 로딩 → diff 분석 → 코드/spec 검증 → verdict → PR_REVIEW.md 생성까지 원스톱으로 수행한다.

## Scope

### In Scope
- 통합 pr-review SKILL.md 작성 (Claude + Codex)
- pr-spec-patch 스킬 삭제 (Claude + Codex)
- marketplace.json 업데이트
- review-checklist.md 업데이트
- gh-commands.md 이전
- sdd-autopilot reasoning reference 업데이트
- docs 워크플로우 문서 업데이트

### Out of Scope
- `_sdd/spec/main.md` 직접 수정 (spec-update-todo로 별도 진행)
- 기존 _sdd/drafts/ 내 과거 feature draft 수정
- 기존 _sdd/ 분석 문서 수정

## Components

1. **pr-review skill (Claude)**: 통합 스킬 본체
2. **pr-review skill (Codex)**: Codex 미러
3. **marketplace.json**: 플러그인 등록
4. **docs**: 워크플로우 문서
5. **sdd-autopilot reference**: reasoning reference 내 임시 스펙/워크플로우 설명

## Implementation Phases

### Phase 1: Core Skill 작성
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| T1 | 통합 pr-review SKILL.md 작성 | P0-Critical | - | pr-review skill (Claude) |
| T2 | pr-review skill.json 업데이트 | P2-Medium | - | pr-review skill (Claude) |
| T3 | review-checklist.md 업데이트 | P1-High | - | pr-review skill (Claude) |
| T4 | gh-commands.md를 pr-review/references/로 이전 | P2-Medium | - | pr-review skill (Claude) |

### Phase 2: 삭제 및 등록
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| T5 | pr-spec-patch 디렉토리 삭제 (Claude) | P0-Critical | T4 | pr-review skill (Claude) |
| T6 | marketplace.json에서 pr-spec-patch 제거 | P0-Critical | T5 | marketplace.json |

### Phase 3: Codex 미러
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| T7 | Codex pr-review SKILL.md 작성 | P1-High | T1 | pr-review skill (Codex) |
| T8 | Codex pr-spec-patch 디렉토리 삭제 | P1-High | T7 | pr-review skill (Codex) |

### Phase 4: 문서 업데이트
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| T9 | sdd-reasoning-reference.md 업데이트 (Claude + Codex) | P1-High | T1 | sdd-autopilot reference |
| T10 | docs/SDD_WORKFLOW.md 업데이트 | P2-Medium | T1 | docs |
| T11 | docs/en/SDD_WORKFLOW.md 업데이트 | P2-Medium | T10 | docs |

## Task Details

### Task T1: 통합 pr-review SKILL.md 작성
**Component**: pr-review skill (Claude)
**Priority**: P0-Critical
**Type**: Refactor

**Description**: 기존 pr-spec-patch + pr-review의 기능을 합친 새 SKILL.md를 작성한다. 핵심 변경:
- spec 선택: from-branch spec 우선 (gh pr diff로 _sdd/spec/ 파일 확인, 없으면 로컬 _sdd/spec/ fallback 없이 code-only)
- 검증 모드: code-only 베이스 + spec-based 추가 레이어
- 산출물: PR_REVIEW.md 1개 (spec_patch_draft.md 제거)
- PR 워크플로우: `PR → pr-review → (머지 후) spec-update-todo`

**Acceptance Criteria**:
- [ ] from-branch spec 로딩 로직이 프로세스에 명시됨
- [ ] code-only 베이스 + spec-based 추가 검증 구조가 반영됨
- [ ] spec_patch_draft.md 관련 내용이 완전히 제거됨
- [ ] 기존 pr-review의 verdict 체계(APPROVE/REQUEST CHANGES/NEEDS DISCUSSION) 유지됨
- [ ] Output Format이 통합 구조로 재설계됨

**Target Files**:
- [M] `.claude/skills/pr-review/SKILL.md` -- 기존 내용 전체 교체

**Technical Notes**:
- from-branch spec 확인: `gh pr diff [PR_NUMBER] --name-only`에서 `_sdd/spec/` 경로 파일 존재 여부로 판단
- from-branch spec 내용 읽기: `gh pr view [PR_NUMBER] --json files` 또는 `git show origin/[headRefName]:_sdd/spec/main.md`
- conciseness 원칙 준수: 기존 두 스킬 합산 630줄 → 목표 300줄 이하

**Dependencies**: -

---

### Task T2: pr-review skill.json 업데이트
**Component**: pr-review skill (Claude)
**Priority**: P2-Medium
**Type**: Refactor

**Description**: 트리거 키워드에 기존 pr-spec-patch 키워드를 흡수한다.

**Acceptance Criteria**:
- [ ] pr-spec-patch 트리거 키워드("PR spec patch", "PR 스펙 패치", "PR 리뷰 준비", "스펙 패치 생성" 등)가 pr-review description에 추가됨

**Target Files**:
- [M] `.claude/skills/pr-review/skill.json` -- description 업데이트

**Dependencies**: -

---

### Task T3: review-checklist.md 업데이트
**Component**: pr-review skill (Claude)
**Priority**: P1-High
**Type**: Refactor

**Description**: "Patch Draft Verification" 섹션을 제거하고, code-only 베이스 검증 항목을 강화한다.

**Acceptance Criteria**:
- [ ] "Patch Draft Verification" 섹션 제거됨
- [ ] Code Quality / Security / Performance 섹션이 code-only 베이스 모드에 맞게 유지됨

**Target Files**:
- [M] `.claude/skills/pr-review/references/review-checklist.md` -- Patch Draft 섹션 제거

**Dependencies**: -

---

### Task T4: gh-commands.md를 pr-review/references/로 이전
**Component**: pr-review skill (Claude)
**Priority**: P2-Medium
**Type**: Refactor

**Description**: pr-spec-patch/references/gh-commands.md를 pr-review/references/로 복사한다. pr-spec-patch 삭제 전에 수행.

**Acceptance Criteria**:
- [ ] `.claude/skills/pr-review/references/gh-commands.md` 파일 존재

**Target Files**:
- [C] `.claude/skills/pr-review/references/gh-commands.md` -- pr-spec-patch에서 복사

**Dependencies**: -

---

### Task T5: pr-spec-patch 디렉토리 삭제 (Claude)
**Component**: pr-review skill (Claude)
**Priority**: P0-Critical
**Type**: Refactor

**Description**: `.claude/skills/pr-spec-patch/` 전체 삭제.

**Acceptance Criteria**:
- [ ] `.claude/skills/pr-spec-patch/` 디렉토리가 존재하지 않음

**Target Files**:
- [D] `.claude/skills/pr-spec-patch/SKILL.md` -- 삭제
- [D] `.claude/skills/pr-spec-patch/skill.json` -- 삭제
- [D] `.claude/skills/pr-spec-patch/references/gh-commands.md` -- 삭제 (T4에서 이전 완료)
- [D] `.claude/skills/pr-spec-patch/examples/spec_patch_draft.md` -- 삭제

**Dependencies**: T4

---

### Task T6: marketplace.json에서 pr-spec-patch 제거
**Component**: marketplace.json
**Priority**: P0-Critical
**Type**: Refactor

**Description**: `.claude-plugin/marketplace.json`의 skills 배열에서 pr-spec-patch 항목 제거.

**Acceptance Criteria**:
- [ ] marketplace.json에 pr-spec-patch 참조 없음

**Target Files**:
- [M] `.claude-plugin/marketplace.json` -- pr-spec-patch 항목 제거

**Dependencies**: T5

---

### Task T7: Codex pr-review SKILL.md 작성
**Component**: pr-review skill (Codex)
**Priority**: P1-High
**Type**: Refactor

**Description**: T1의 Claude 버전을 Codex 형식으로 미러링한다.

**Acceptance Criteria**:
- [ ] `.codex/skills/pr-review/SKILL.md`가 Claude 버전과 동일 내용

**Target Files**:
- [M] `.codex/skills/pr-review/SKILL.md` -- 통합 버전으로 교체
- [M] `.codex/skills/pr-review/skill.json` -- description 업데이트
- [M] `.codex/skills/pr-review/references/review-checklist.md` -- T3과 동일 변경

**Dependencies**: T1

---

### Task T8: Codex pr-spec-patch 디렉토리 삭제
**Component**: pr-review skill (Codex)
**Priority**: P1-High
**Type**: Refactor

**Description**: `.codex/skills/pr-spec-patch/` 전체 삭제.

**Acceptance Criteria**:
- [ ] `.codex/skills/pr-spec-patch/` 디렉토리가 존재하지 않음

**Target Files**:
- [D] `.codex/skills/pr-spec-patch/SKILL.md` -- 삭제
- [D] `.codex/skills/pr-spec-patch/skill.json` -- 삭제
- [D] `.codex/skills/pr-spec-patch/references/gh-commands.md` -- 삭제
- [D] `.codex/skills/pr-spec-patch/examples/spec_patch_draft.md` -- 삭제

**Dependencies**: T7

---

### Task T9: sdd-reasoning-reference.md 업데이트
**Component**: sdd-autopilot reference
**Priority**: P1-High
**Type**: Refactor

**Description**: 임시 스펙 유형에서 `spec_patch_draft` 제거, 스킬 목록에서 pr-spec-patch 제거.

**Acceptance Criteria**:
- [ ] `spec_patch_draft` 언급 제거
- [ ] pr-spec-patch 스킬 참조 제거
- [ ] pr-review 설명이 통합 기능을 반영

**Target Files**:
- [M] `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md` -- spec_patch_draft 및 pr-spec-patch 참조 업데이트
- [M] `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md` -- Claude 버전과 동일 변경

**Dependencies**: T1

---

### Task T10: docs/SDD_WORKFLOW.md 업데이트
**Component**: docs
**Priority**: P2-Medium
**Type**: Refactor

**Description**: 워크플로우 설명에서 pr-spec-patch 단계 제거, PR 리뷰 워크플로우 단순화, spec_patch_draft.md 아티팩트 참조 제거.

**Acceptance Criteria**:
- [ ] pr-spec-patch 언급 제거
- [ ] spec_patch_draft.md 참조 제거
- [ ] PR 워크플로우가 `PR → pr-review → (머지 후) spec-update-todo`로 업데이트

**Target Files**:
- [M] `docs/SDD_WORKFLOW.md` -- pr-spec-patch/spec_patch_draft 참조 전체 업데이트

**Dependencies**: T1

---

### Task T11: docs/en/SDD_WORKFLOW.md 업데이트
**Component**: docs
**Priority**: P2-Medium
**Type**: Refactor

**Description**: T10의 영문 미러 업데이트.

**Acceptance Criteria**:
- [ ] 영문 문서가 한글 문서와 동일한 변경 반영

**Target Files**:
- [M] `docs/en/SDD_WORKFLOW.md` -- T10과 동일 변경 (영문)

**Dependencies**: T10

---

## Parallel Execution Summary

| Phase | Total Tasks | Max Parallel | Sequential (conflicts) |
|-------|-------------|--------------|----------------------|
| Phase 1 | 4 | 4 | 없음 (T1, T2, T3, T4 모두 다른 파일) |
| Phase 2 | 2 | 1 | T5 → T6 (T5 삭제 후 T6 등록 제거) |
| Phase 3 | 2 | 1 | T7 → T8 (T7 작성 후 T8 삭제) |
| Phase 4 | 3 | 2 | T9 독립, T10 → T11 순차 |

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| 다른 스킬이 pr-spec-patch/spec_patch_draft를 참조 | 런타임 에러 | Grep으로 참조 전수 조사 완료 (40 파일 확인). 실제 수정 필요 파일은 Task에 포함됨 |
| Codex 미러 누락 | Codex 사용자 영향 | Phase 3에서 명시적으로 처리 |
| spec main.md 업데이트 누락 | spec drift | Out of Scope 명시. 구현 후 /spec-update-todo 실행 필요 |

## Open Questions

- 없음

## Model Recommendation

T1(통합 SKILL.md 작성)이 핵심 태스크. 기존 두 스킬의 구조를 이해하고 conciseness 원칙에 맞게 재설계해야 하므로 Opus급 모델 권장.

---

## Next Steps

### Apply Spec Patch
- **Method A (automatic)**: Run `spec-update-todo` → Part 1을 입력으로 사용

### Execute Implementation
- **Parallel**: Phase별 순차, Phase 내 병렬 실행
- Phase 1 → Phase 2 → Phase 3 → Phase 4
