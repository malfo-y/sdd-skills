# Feature Draft: Source 필드 코드 매핑

**날짜**: 2026-03-09
**근거 토론**: `_sdd/discussion/discussion_spec_code_mapping.md`

---

<!-- spec-update-todo-input-start -->

# Part 1: Spec Patch Draft

> 이 패치는 해당 스펙 섹션에 직접 복사-붙여넣기하거나,
> `spec-update-todo` 스킬의 입력으로 사용할 수 있습니다.

# Spec Update Input

**Date**: 2026-03-09
**Author**: feature-draft
**Target Spec**: `_sdd/spec/sdd_skills.md`

## Improvements

### Improvement: spec-create에 Source 필드 생성 로직 추가
**Priority**: High
**Target Section**: `_sdd/spec/sdd_skills.md` > `컴포넌트 상세 (Component Details)` > `각 스킬 상세` > `spec-create`
**Current State**: "Link to Code: Reference file paths and line numbers when helpful" best practice만 존재. 구조적 매핑 메커니즘 없음.
**Proposed**: spec-create가 코드 기반으로 스펙을 생성할 때, 각 컴포넌트 테이블에 `**Source**` 필드를 인라인으로 추가하는 로직 도입. 코드가 없는 프로젝트에서는 Source 필드를 생략.
**Reason**: 스펙 섹션 ↔ 소스코드 간 함수/클래스 레벨 traceability를 확보하여 스펙의 실용성을 높임.

---

### Improvement: spec-update-done에 Source 필드 갱신 로직 추가
**Priority**: High
**Target Section**: `_sdd/spec/sdd_skills.md` > `컴포넌트 상세 (Component Details)` > `각 스킬 상세` > `spec-update-done`
**Current State**: 드리프트 감지 및 스펙 업데이트는 수행하지만, 컴포넌트 테이블의 Source 필드를 체계적으로 갱신하는 로직 없음.
**Proposed**: 구현 산출물(implementation plan/report) 우선 참조 + 코드 탐색 보완 혼합 방식으로 Source 필드를 갱신하는 단계 추가. 새로 구현된 컴포넌트에 Source 필드가 없으면 추가.
**Reason**: 구현 후 스펙 동기화 시점이 Source 필드 갱신의 가장 자연스러운 타이밍.

---

### Improvement: spec-rewrite에 Source 필드 보존 규칙 추가
**Priority**: Medium
**Target Section**: `_sdd/spec/sdd_skills.md` > `컴포넌트 상세 (Component Details)` > `각 스킬 상세` > `spec-rewrite`
**Current State**: Hard Rules에 "Preserve decision context" 규칙은 있으나, Source 필드 보존에 대한 명시적 규칙 없음.
**Proposed**: Hard Rules 또는 Best Practices에 "기존 Source 필드가 있으면 반드시 보존할 것" 규칙 추가.
**Reason**: 스펙 재구성 시 축적된 코드 매핑 정보가 소실되는 것을 방지.

---

### Improvement: spec-review에 Source 필드 보존/검증 규칙 추가
**Priority**: Medium
**Target Section**: `_sdd/spec/sdd_skills.md` > `컴포넌트 상세 (Component Details)` > `각 스킬 상세` > `spec-review`
**Current State**: Code-Linked Drift Audit (Step 3)에서 코드 대비 스펙 검증을 수행하지만, Source 필드의 정확성을 검증하는 항목 없음.
**Proposed**: Drift Audit에 "Source 필드 정확성 검증" 항목 추가 — Source에 기재된 파일/클래스/함수가 실제로 존재하는지 확인.
**Reason**: Source 필드가 시간이 지나면 outdated될 수 있으므로 리뷰 시 검증이 필요.

---

## Notes

### Context
- 토론 7라운드를 통해 결정된 사항을 기반으로 함
- 현재 `spec-create`와 `spec-rewrite`의 Best Practices에 "Link to Code" 항목이 있으나, 이는 권장 수준이며 구조적 메커니즘은 아님
- `spec-update-done`의 changelog 예시에 파일 경로 참조(`src/module.py:45-89`)가 있으나, 스펙 본문 섹션별 매핑과는 다른 용도

### Constraints
- Source 필드 매핑은 **함수/클래스 레벨**까지 (파일 레벨만은 불충분)
- Source 필드 포맷: **파일별 줄바꿈 그룹핑 + 백틱**으로 파일 경로 표시
- 코드 없는 프로젝트에서는 Source 필드 **생략** (TBD 플레이스홀더 사용하지 않음)
- 핵심 로직은 **spec-create + spec-update-done**에만 추가
- spec-rewrite/spec-review에는 **보존 규칙만** 추가

### Source 필드 포맷 규격

```markdown
| **Source** | `src/auth/token.py`: verify_token(), decode_jwt() |
|            | `src/auth/handler.py`: AuthHandler |
```

규칙:
- 파일 경로는 백틱(`` ` ``)으로 감싸기
- 파일별로 줄바꿈하여 그룹핑
- 같은 파일의 클래스/함수는 콤마로 구분
- 프로젝트 루트 기준 상대 경로 사용

<!-- spec-update-todo-input-end -->

---

# Part 2: Implementation Plan

## Overview
SDD 스펙 스킬 4개(spec-create, spec-update-done, spec-rewrite, spec-review)에 Source 필드 코드 매핑 기능을 추가한다. spec-create와 spec-update-done에는 핵심 매핑 로직을, spec-rewrite와 spec-review에는 보존/검증 규칙을 추가한다.

## Scope

### In Scope
- spec-create SKILL.md: Source 필드 생성 지시사항 추가
- spec-create 템플릿/예시 파일: Source 필드 포함 예시 추가
- spec-update-done SKILL.md: Source 필드 갱신 로직 추가
- spec-update-done 예시 파일: Source 필드 갱신 예시 추가
- spec-rewrite SKILL.md: Source 필드 보존 규칙 추가
- spec-review SKILL.md: Source 필드 검증 항목 추가

### Out of Scope
- spec-update-todo, spec-summary, spec-snapshot 등 다른 스킬 수정
- 별도 CODE_MAP.md 파일 생성 메커니즘
- 자동화된 코드 파싱/AST 분석 도구

## Components
1. **spec-create Source 생성**: 코드 기반 스펙 생성 시 Source 필드를 컴포넌트 테이블에 추가
2. **spec-update-done Source 갱신**: 구현 후 스펙 동기화 시 Source 필드를 혼합 방식으로 갱신
3. **spec-rewrite Source 보존**: 스펙 재구성 시 기존 Source 필드 보존
4. **spec-review Source 검증**: 스펙 리뷰 시 Source 필드 정확성 검증

## Implementation Phases

### Phase 1: 핵심 로직 (spec-create + spec-update-done)
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 1  | spec-create SKILL.md에 Source 필드 생성 지시사항 추가 | P0 | - | spec-create Source 생성 |
| 2  | spec-create 템플릿/예시에 Source 필드 반영 | P1 | 1 | spec-create Source 생성 |
| 3  | spec-update-done SKILL.md에 Source 필드 갱신 로직 추가 | P0 | - | spec-update-done Source 갱신 |
| 4  | spec-update-done 예시에 Source 필드 갱신 사례 추가 | P1 | 3 | spec-update-done Source 갱신 |

### Phase 2: 보존/검증 규칙 (spec-rewrite + spec-review)
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 5  | spec-rewrite SKILL.md에 Source 필드 보존 규칙 추가 | P1 | - | spec-rewrite Source 보존 |
| 6  | spec-review SKILL.md에 Source 필드 검증 항목 추가 | P1 | - | spec-review Source 검증 |

## Task Details

### Task 1: spec-create SKILL.md에 Source 필드 생성 지시사항 추가
**Component**: spec-create Source 생성
**Priority**: P0-Critical
**Type**: Feature

**Description**:
spec-create의 SKILL.md에 다음 내용을 추가한다:

1. **Step 1 (Gather Information)** 또는 **Step 2 (Analyze)** 단계에서: 코드베이스가 존재하는지 판단하는 로직 명시 (이미 코드 탐색을 하므로 자연스럽게 확인 가능)
2. **Step 3 (Write the Spec)** 단계의 컴포넌트 테이블 템플릿에: `**Source**` 행을 조건부로 포함하는 지시사항 추가
3. **Best Practices > Writing Quality**에: 기존 "Link to Code" 항목을 Source 필드 규격으로 구체화

추가할 핵심 지시사항:
- 코드가 있을 때: 각 컴포넌트 테이블에 `**Source**` 필드를 추가하고, 해당 컴포넌트를 구현하는 주요 파일/클래스/함수를 기재
- 코드가 없을 때: Source 필드를 생략 (TBD 사용하지 않음)
- Source 필드 포맷 규격 (파일별 줄바꿈, 백틱, 상대경로)

**Acceptance Criteria**:
- [ ] Step 3 컴포넌트 테이블 템플릿에 조건부 Source 필드 포함
- [ ] 코드 유무 판단 기준이 명시됨
- [ ] Source 필드 포맷 규격이 문서화됨
- [ ] Best Practices의 "Link to Code" 항목이 Source 필드 규격으로 구체화됨

**Target Files**:
- [M] `.claude/skills/spec-create/SKILL.md` -- Step 3 템플릿 수정, Best Practices 수정

**Technical Notes**:
- 기존 "Link to Code" best practice 문구를 제거하지 않고 Source 필드 규격으로 확장
- 조건부 로직은 자연어 지시사항으로 표현 (코드가 아닌 프롬프트이므로)

**Dependencies**: 없음

---

### Task 2: spec-create 템플릿/예시에 Source 필드 반영
**Component**: spec-create Source 생성
**Priority**: P1-High
**Type**: Feature

**Description**:
spec-create의 참조 템플릿과 예시 파일에 Source 필드를 포함한 컴포넌트 테이블 예시를 추가한다.

1. `references/template-full.md`: 컴포넌트 상세 섹션의 테이블에 Source 행 추가 (주석으로 "코드 있을 때만" 안내)
2. `examples/complex-project-spec.md`: Source 필드가 포함된 컴포넌트 예시 추가
3. `examples/simple-project-spec.md`: 소규모 프로젝트이므로 Source 필드 포함 여부 확인 후 적절히 반영

**Acceptance Criteria**:
- [ ] template-full.md에 Source 필드가 포함된 컴포넌트 테이블 예시 존재
- [ ] complex-project-spec.md에 Source 필드 활용 예시 존재
- [ ] Source 필드 포맷이 Task 1의 규격과 일치

**Target Files**:
- [M] `.claude/skills/spec-create/references/template-full.md` -- 컴포넌트 테이블에 Source 행 추가
- [M] `.claude/skills/spec-create/examples/complex-project-spec.md` -- Source 필드 포함 예시
- [M] `.claude/skills/spec-create/examples/simple-project-spec.md` -- 필요시 Source 필드 예시

**Technical Notes**:
- template-full.md의 Source 행에는 `<!-- 코드 기반 생성 시에만 포함 -->` 주석 추가 권장
- simple-project-spec.md는 코드가 있는 예시인 경우에만 Source 추가

**Dependencies**: Task 1 (포맷 규격이 먼저 확정되어야 함)

---

### Task 3: spec-update-done SKILL.md에 Source 필드 갱신 로직 추가
**Component**: spec-update-done Source 갱신
**Priority**: P0-Critical
**Type**: Feature

**Description**:
spec-update-done의 SKILL.md에 다음 내용을 추가한다:

1. **Step 2 (Identify Spec Drift)** 에 "Source Drift" 카테고리 추가:
   - Source 필드가 없는 컴포넌트 식별 (새로 구현됨)
   - Source 필드가 outdated된 컴포넌트 식별 (파일/함수 변경됨)

2. **Step 4 (Apply Updates)** 에 Source 필드 갱신 절차 추가:
   - 혼합 방식: 구현 산출물(implementation plan/report)에서 파일 경로 우선 추출 → 코드 탐색(Grep/Glob)으로 누락분 보완
   - 새 컴포넌트: Source 필드 신규 추가
   - 기존 컴포넌트: Source 필드 갱신 (파일명 변경, 함수 추가/삭제 반영)

3. **Best Practices > Preservation** 에 Source 필드 보존 규칙 추가

**Acceptance Criteria**:
- [ ] Step 2에 Source Drift 감지 항목 추가됨
- [ ] Step 4에 Source 필드 갱신 절차가 명시됨
- [ ] 혼합 방식(구현 산출물 우선 + 코드 탐색 보완)이 명확히 기술됨
- [ ] Source 필드 포맷 규격 참조 포함
- [ ] 코드가 없는 컴포넌트는 Source 필드를 추가하지 않는다는 규칙 포함

**Target Files**:
- [M] `.claude/skills/spec-update-done/SKILL.md` -- Step 2, Step 4, Best Practices 수정

**Technical Notes**:
- 구현 산출물에서 Source 정보를 추출하는 구체적 방법: implementation plan의 Target Files 필드, implementation report의 변경 파일 목록, git diff 결과
- Explore agent 또는 Grep/Glob으로 코드 탐색 시 컴포넌트명 → 파일/클래스 매핑

**Dependencies**: 없음

---

### Task 4: spec-update-done 예시에 Source 필드 갱신 사례 추가
**Component**: spec-update-done Source 갱신
**Priority**: P1-High
**Type**: Feature

**Description**:
spec-update-done의 예시 파일에 Source 필드 갱신 전후를 보여주는 사례를 추가한다.

1. `examples/changelog-entry.md`: Source 필드 추가/갱신이 포함된 changelog 예시 추가
2. `examples/review-report.md`: Source Drift 발견 및 해결을 포함한 리뷰 리포트 예시 추가

**Acceptance Criteria**:
- [ ] changelog-entry.md에 Source 필드 갱신 관련 항목 예시 존재
- [ ] review-report.md에 Source Drift 항목 예시 존재

**Target Files**:
- [M] `.claude/skills/spec-update-done/examples/changelog-entry.md` -- Source 필드 갱신 changelog 예시 추가
- [M] `.claude/skills/spec-update-done/examples/review-report.md` -- Source Drift 리포트 예시 추가

**Technical Notes**:
- 기존 예시를 삭제하지 않고 추가 섹션으로 덧붙이기

**Dependencies**: Task 3 (갱신 로직이 먼저 확정되어야 함)

---

### Task 5: spec-rewrite SKILL.md에 Source 필드 보존 규칙 추가
**Component**: spec-rewrite Source 보존
**Priority**: P1-High
**Type**: Feature

**Description**:
spec-rewrite의 SKILL.md에 Source 필드 보존 규칙을 추가한다.

1. **Hard Rules** 에 규칙 추가: "기존 컴포넌트 테이블의 `Source` 필드가 있으면 반드시 보존한다."
2. **Step 7 (Validation)** 에 검증 항목 추가: "리라이트 후 기존 Source 필드가 모두 보존되었는지 확인"

**Acceptance Criteria**:
- [ ] Hard Rules에 Source 필드 보존 규칙 명시됨
- [ ] Step 7 Validation에 Source 필드 보존 검증 항목 포함됨

**Target Files**:
- [M] `.claude/skills/spec-rewrite/SKILL.md` -- Hard Rules, Step 7 수정

**Technical Notes**:
- 기존 Hard Rules 5개에 6번째 규칙으로 추가
- Step 7의 검증 스텝에 자연스럽게 통합

**Dependencies**: 없음

---

### Task 6: spec-review SKILL.md에 Source 필드 검증 항목 추가
**Component**: spec-review Source 검증
**Priority**: P1-High
**Type**: Feature

**Description**:
spec-review의 SKILL.md에 Source 필드 검증 항목을 추가한다.

1. **Step 3 (Code-Linked Drift Audit)** 에 검증 항목 추가:
   - Source 필드에 기재된 파일이 실제로 존재하는지 확인
   - Source 필드에 기재된 클래스/함수가 해당 파일에 존재하는지 확인
   - Source 필드가 없는 구현된 컴포넌트 식별
2. **Drift Type → Default Severity Mapping** 테이블에 `Source` 타입 추가 (Severity: Low)

**Acceptance Criteria**:
- [ ] Step 3에 Source 필드 검증 항목 3개 추가됨
- [ ] Drift Type 매핑에 Source 타입 추가됨
- [ ] Source 필드 검증 실패 시 리포트에 어떻게 기록하는지 명시됨

**Target Files**:
- [M] `.claude/skills/spec-review/SKILL.md` -- Step 3, Drift Type 매핑 수정

**Technical Notes**:
- Source drift는 기능적 영향이 낮으므로 Severity Low로 기본 설정
- 검증 시 Glob/Grep 사용하여 파일/클래스/함수 존재 여부 확인

**Dependencies**: 없음

---

## Parallel Execution Summary
| Phase | Total Tasks | Max Parallel | Sequential (conflicts) |
|-------|-------------|--------------|----------------------|
| 1     | 4           | 2            | 2 (Task 2→1, Task 4→3) |
| 2     | 2           | 2            | 0 |

> Phase 1에서 Task 1과 Task 3은 병렬 실행 가능. Task 2는 Task 1 완료 후, Task 4는 Task 3 완료 후 실행.
> Phase 2의 Task 5와 Task 6은 완전 병렬 실행 가능.

## Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| Source 필드 포맷이 마크다운 테이블에서 줄바꿈 렌더링 비일관 | 가독성 저하 | 포맷 예시를 여러 마크다운 렌더러에서 테스트 |
| spec-create가 코드 없는 프로젝트에서 실수로 Source 필드를 생성 | 불필요한 TBD/빈 필드 | "코드 유무 판단 기준"을 명확히 문서화 |
| spec-update-done에서 구현 산출물이 없을 때 Source 갱신 누락 | Source 필드 outdated | 코드 탐색 fallback 로직으로 보완 |

## Open Questions
- (없음 — 토론에서 모두 결정됨)

## Model Recommendation
스킬 SKILL.md 파일들의 프롬프트 수정이므로, 코드 구현보다는 자연어 프롬프트 엔지니어링에 해당. **Sonnet** 모델로 충분하며, 각 태스크가 단일 파일 수정이므로 병렬 실행 시 효율적.
