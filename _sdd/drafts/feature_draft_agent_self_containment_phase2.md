# Feature Draft: Agent AC-First 재작성 Phase 2 (나머지 4개)

**날짜**: 2026-03-19
**선행 작업**: `feature_draft_agent_self_containment.md` -- 5개 agent 재작성 완료
**요청 배경**: 앞서 5개 agent(ralph-loop-init, spec-update-done, feature-draft, implementation, implementation-plan)를 AC-First 구조로 재작성. 나머지 4개도 동일한 원칙으로 정제한다.

---

<!-- spec-update-todo-input-start -->

# Part 1: Spec Patch Draft

> 이 패치는 해당 스펙 섹션에 직접 복사-붙여넣기하거나,
> `spec-update-todo` 스킬의 입력으로 사용할 수 있습니다.

## Spec Update Input

**Date**: 2026-03-19
**Author**: feature-draft
**Target Spec**: `_sdd/spec/main.md`
**Spec Update Classification**: SHOULD update

## Improvement Changes

### Improvement: 나머지 4개 Agent AC-First 재작성

**Priority**: Medium
**Current State**: 4개 agent (write-phased, implementation-review, spec-review, spec-update-todo) 합계 1,705줄. 외부 참조 의존도는 낮으나, AC-First 구조가 아니며 verbose한 섹션이 다수.
**Proposed**: SDD 철학에 맞게 AC-First 구조로 전면 재작성하여 간결하게 정제.

#### 현재 상태 vs 목표

| Agent | 현재 줄수 | 목표 줄수 | 감축률 | 주요 bloat |
|-------|----------|----------|--------|-----------|
| implementation-review | 812 | ~230 | 72% | Tier 1/2/3 각 5-step 반복 (삼중 구조), Output Template 80줄, Quick Review 50줄, Context Mgmt |
| spec-update-todo | 449 | ~160 | 64% | Update Templates 55줄, Input Sources 59줄, Best Practices, Context Mgmt |
| spec-review | 304 | ~130 | 57% | Output Template 66줄, Guardrails 장문, Context Mgmt, Error Handling 장문 |
| write-phased | 140 | ~80 | 43% | Examples 과다 (코드+문서 각 상세 예시), When to Apply 반복 설명 |
| **합계** | **1,705** | **~600** | **65%** | |

#### 재작성 원칙 (Phase 1과 동일)

1. **AC-First 구조**: Goal → Acceptance Criteria → Hard Rules → Process → Output Format
2. **공통 제거 대상**: Best Practices, Context Management, When to Use, Additional Resources
3. **Concise**: 장황한 prose → 테이블/체크리스트, 중복 제거
4. **외부 참조**: 있는 것은 optional로 표기 (필수 참조 금지)

#### Acceptance Criteria (전체)

- [ ] AC1: 4개 agent가 AC-First 구조 (Goal → AC → Hard Rules → Process → Output Format)를 따름
- [ ] AC2: 4개 agent 전체 합계 줄수가 현재 1,705줄에서 700줄 이하로 감축 (59%+)
- [ ] AC3: 각 agent의 핵심 기능이 보존됨
  - write-phased: Phase 1 (skeleton) → Phase 2 (fill by Edit) 전략 정상 동작
  - implementation-review: Tier 1/2/3 graceful degradation + 5-step review 정상 동작
  - spec-review: quality audit + drift audit + severity classification 정상 동작
  - spec-update-todo: 입력 소스 파싱 → 스펙 업데이트 → 요약 보고 정상 동작
- [ ] AC4: 기존 wrapper skill 및 다른 agent에서의 호출이 깨지지 않음 (frontmatter 보존)
- [ ] AC5: `references/` 참조가 있는 경우 "optional" 표기

<!-- spec-update-todo-input-end -->

---

# Part 2: Implementation Plan

## Overview

| Item | Detail |
|------|--------|
| 대상 | `.claude/agents/` 하위 4개 agent 파일 |
| 작업 유형 | AC-First 전면 재작성 |
| 총 태스크 | 4개 (전체 병렬 가능) |
| 예상 변경 규모 | 현재 1,705줄 → ~600줄 (65% 감축) |

## 재작성 공통 가이드

Phase 1과 동일한 AC-First Agent 구조를 적용한다:

```
---
frontmatter (name, description, tools, model -- 기존 유지)
---
# [Agent Name]
[1-2문장 Goal]

## Acceptance Criteria
- [ ] AC1: ...

## Hard Rules

## Process
### Step 1: ...

## Output Format
```

## 태스크 (전체 병렬 -- 파일 간 의존 없음)

### Task 1: implementation-review 재작성

**Target Files**:
- [M] `.claude/agents/implementation-review.md`

**현재**: 812줄 → **목표**: ~230줄

**Goal**: 구현 진행 상황을 Plan/Spec/Code 기반으로 리뷰하고, 이슈를 식별하여 리포트를 생성한다.

**Agent AC**:
- [ ] Tier 자동 판별 (Plan 유효 → Tier 1, Plan 없음/stale + Spec → Tier 2, 둘 다 없음 → Tier 3)
- [ ] 5-step review (Inventory → Verification → Assessment → Issues → Summary) 정상 동작
- [ ] `_sdd/implementation/IMPLEMENTATION_REVIEW.md`에 리포트 저장
- [ ] spec 파일 수정 금지

**재작성 방향**:
| 영역 | 현재 | 변경 |
|------|------|------|
| Tier 1/2/3 각 5-step 반복 | 3x~60줄 = 180줄 | Tier 1 기준 1회 작성 + Tier 2/3 델타만 ~20줄 |
| Output Template | 80줄 | ~25줄 간결 템플릿 |
| Quick Review Mode | 50줄 | 5줄 참고 노트 |
| Context Management | 14줄 | 삭제 |
| When to Use | 8줄 | 삭제 |
| Error Handling | 15행 | ~6행 |
| Autonomous Decision-Making | 11줄 | Hard Rules에 통합 |

### Task 2: spec-update-todo 재작성

**Target Files**:
- [M] `.claude/agents/spec-update-todo.md`

**현재**: 449줄 → **목표**: ~160줄

**Goal**: 사용자 입력/파일로부터 새로운 기능/요구사항을 파싱하여 스펙에 반영한다.

**Agent AC**:
- [ ] 3가지 입력 소스 (대화, user_spec.md, user_draft.md) 파싱
- [ ] 스펙 백업 → 섹션 매핑 → 업데이트 적용 → 버전 증가
- [ ] 처리 완료된 입력 파일에 `_processed_` 접두사 추가
- [ ] 업데이트 요약 보고 생성

**재작성 방향**:
| 영역 | 현재 | 변경 |
|------|------|------|
| Input Sources 설명 | 59줄 | ~15줄 테이블 |
| Update Templates 3개 | 55줄 | 1개 간결 템플릿 ~15줄 |
| Best Practices | 17줄 | 삭제 |
| Context Management | 14줄 | 삭제 |
| Language Handling | 6줄 | 2줄 |
| Error Handling | 21줄 | ~8줄 |
| references/ 참조 | 필수 참조 | optional 표기 |

### Task 3: spec-review 재작성

**Target Files**:
- [M] `.claude/agents/spec-review.md`

**현재**: 304줄 → **목표**: ~130줄

**Goal**: 스펙 품질과 코드-스펙 드리프트를 읽기 전용으로 감사하고, 리뷰 리포트를 생성한다.

**Agent AC**:
- [ ] 2차원 리뷰 (spec quality + code drift) 수행
- [ ] 발견 사항에 severity (High/Medium/Low) 분류
- [ ] decision 부여 (SPEC_OK / SYNC_REQUIRED / NEEDS_DISCUSSION)
- [ ] `_sdd/spec/SPEC_REVIEW_REPORT.md`에 저장
- [ ] spec 파일 수정 금지

**재작성 방향**:
| 영역 | 현재 | 변경 |
|------|------|------|
| Output Template | 66줄 | ~20줄 간결 템플릿 |
| Guardrails | 9줄 | 4줄 (Hard Rules에 통합) |
| Context Management | 14줄 | 삭제 |
| When to Use | 6줄 | 삭제 |
| Error Handling | 12행 | ~6행 |
| Additional Resources | 7줄 | optional 참조로 축소 |

### Task 4: write-phased 재작성

**Target Files**:
- [M] `.claude/agents/write-phased.md`

**현재**: 140줄 → **목표**: ~80줄

**Goal**: 구조적으로 복잡한 문서/코드를 Phase 1 (skeleton) → Phase 2 (fill by Edit) 2단계로 작성한다.

**Agent AC**:
- [ ] Phase 1: skeleton을 Write로 파일에 저장
- [ ] Phase 2: Edit으로 섹션별 채우기 (Write 덮어쓰기 금지)
- [ ] Phase 1 → 2 자동 진행 (사용자 확인 불필요)
- [ ] 완료 후 TODO 마커 전부 제거

**재작성 방향**:
| 영역 | 현재 | 변경 |
|------|------|------|
| When to Apply 테이블 | 8줄 | 3줄 |
| Examples 문서+코드 | 68줄 | 각 1개씩 ~30줄로 축소 |
| Phase 1+2 설명 중복 | 반복 설명 | 1회 설명 |

## Parallel Execution Summary

```
Phase 1: [Task 1] [Task 2] [Task 3] [Task 4]  <- 전체 병렬 (파일 간 의존 없음)
```

## Next Steps

1. 이 draft를 리뷰하고 승인
2. `/implementation` 으로 4개 태스크 병렬 실행
3. 완료 후 각 agent의 AC 검증
4. Phase 1 + Phase 2 전체 결과를 `/spec-update-done`으로 스펙 동기화
