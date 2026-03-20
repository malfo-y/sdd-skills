# Feature Draft: write-phased -> write-skeleton Refactoring

**날짜**: 2026-03-20
**요청 배경**: write-phased agent가 Phase 1(skeleton) + Phase 2(fill)를 모두 수행하면서 호출자에게 중간 과정이 보이지 않음. Agent를 skeleton 전용으로 축소하고, fill 책임을 호출자에게 돌려 가시성과 유연성을 확보한다.

---

<!-- spec-update-todo-input-start -->

# Part 1: Spec Patch Draft

> 이 패치는 해당 스펙 섹션에 직접 복사-붙여넣기하거나,
> `spec-update-todo` 스킬의 입력으로 사용할 수 있습니다.

## Spec Update Input

**Date**: 2026-03-20
**Author**: feature-draft
**Target Spec**: `_sdd/spec/main.md`
**Spec Update Classification**: MUST update

## Background & Motivation Updates

### Background Update: write-skeleton 패턴 도입

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > Core Design / Architecture

**Current State**:
`write-phased` agent가 Phase 1(skeleton 작성) + Phase 2(Edit으로 채우기)를 혼자 수행한다. 호출자(다른 agent, full skill)는 완성된 결과만 받으며, 중간 과정(어떤 섹션을 어떻게 채우는지)이 보이지 않는다. 13개 agent/skill이 write-phased를 호출한다.

**Proposed**:
write-phased agent를 `write-skeleton`으로 개명하고 역할을 축소한다:
- 짧은 문서: 전체 작성 후 `COMPLETE` 상태 반환
- 긴 문서: skeleton만 작성 후 `SKELETON_ONLY` 상태 + 미완성 섹션 목록 반환
- fill 책임은 호출자에게 이전 -- 호출자가 직접 Edit하거나 병렬 agent를 dispatch

**Reason**:
1. 호출자가 fill 전략을 결정할 수 있음 (병렬/순차/직접 Edit)
2. write-phased 스킬을 실제 오케스트레이션 스킬로 승격 -- 중간 과정이 사용자에게 보임
3. Agent 역할이 명확해짐 -- "skeleton 생성기" vs "fill 오케스트레이터"

## Design Changes

### Design Change: write-skeleton agent 반환 프로토콜

**Priority**: High

#### 반환 형식

```markdown
## Write Result
- **Status**: COMPLETE | SKELETON_ONLY
- **File**: <작성된 파일 경로>
- **Sections Written**: <완성된 섹션 목록>
- **Sections Remaining**: <미완성 섹션 목록 -- SKELETON_ONLY일 때만>
  - [섹션 제목]: [채워야 할 내용 요약]
  - [섹션 제목]: [채워야 할 내용 요약]
```

#### 판단 기준

| 조건 | 동작 | 반환 |
|------|------|------|
| 섹션 3개 미만 (문서) 또는 함수 5개 미만 (코드) | 전체 작성 | `COMPLETE` |
| 섹션 3개 이상 (문서) 또는 함수 5개 이상 (코드) | skeleton만 작성 | `SKELETON_ONLY` |

#### 호출자의 fill 처리 패턴

```
result = Agent(subagent_type="write-skeleton", prompt="...")

IF result.status == "COMPLETE":
  -> 완료
ELIF result.status == "SKELETON_ONLY":
  -> result.sections_remaining을 순회하며 Edit으로 채움
  -> 독립 섹션이 2개 이상이면 병렬 agent dispatch 가능
  -> 모든 TODO/Phase 마커 제거
```

### Design Change: write-phased 스킬 역할 변경

**Priority**: High

**Current**: 얇은 wrapper (agent에 위임만)
**Proposed**: 실제 오케스트레이션 스킬

```
# write-phased 스킬 (승격)
1. write-skeleton agent 호출 -> skeleton 생성
2. 반환값 확인
   - COMPLETE -> 사용자에게 보고
   - SKELETON_ONLY -> 미완성 섹션을 직접 Edit으로 채움
     - 독립 섹션 2개+ -> 병렬 agent dispatch
     - 의존 섹션 -> 순서대로 Edit
3. TODO/Phase 마커 정리
4. 완료 보고
```

이점: 스킬에서 직접 실행하므로 **모든 중간 과정이 사용자에게 보임**

## Component Changes

### Rename Component: write-phased agent -> write-skeleton agent

**Change Type**: Rename + Refactor
**Files**:
- `[M->D+C] .claude/agents/write-phased.md` -> `.claude/agents/write-skeleton.md`
- `[M] .claude/skills/write-phased/SKILL.md` (wrapper -> 오케스트레이션 스킬로 승격)

### Update Component: write-skeleton 호출자 수정 (13개)

**Change Type**: Enhancement

**Agents (4개)**:
- `[M] .claude/agents/feature-draft.md` -- write-skeleton 호출 + fill 처리
- `[M] .claude/agents/implementation-plan.md` -- write-skeleton 호출 + fill 처리
- `[M] .claude/agents/implementation-review.md` -- write-skeleton 호출 + fill 처리
- `[M] .claude/agents/spec-review.md` -- write-skeleton 호출 + fill 처리

**Full Skills (8개)**:
- `[M] .claude/skills/spec-create/SKILL.md`
- `[M] .claude/skills/spec-rewrite/SKILL.md`
- `[M] .claude/skills/spec-upgrade/SKILL.md`
- `[M] .claude/skills/spec-summary/SKILL.md`
- `[M] .claude/skills/pr-review/SKILL.md`
- `[M] .claude/skills/pr-spec-patch/SKILL.md`
- `[M] .claude/skills/guide-create/SKILL.md`
- `[M] .claude/skills/spec-snapshot/SKILL.md`

**참조 문서 (1개)**:
- `[M] .claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md`

## Acceptance Criteria

- [ ] AC1: `write-skeleton` agent가 짧은 문서에 COMPLETE, 긴 문서에 SKELETON_ONLY를 정확히 반환
- [ ] AC2: SKELETON_ONLY 반환 시 미완성 섹션 목록(섹션명 + 채울 내용 요약)이 포함됨
- [ ] AC3: skeleton 파일에 각 미완성 섹션마다 TODO 마커가 존재하여 호출자가 Edit 위치를 식별 가능
- [ ] AC4: write-phased 스킬이 오케스트레이션 스킬로 동작 -- skeleton 생성 -> fill -> 마커 정리
- [ ] AC5: 13개 호출자(agent 4 + skill 8 + 참조 1)가 write-skeleton 호출 + fill 패턴으로 수정됨
- [ ] AC6: 기존 write-phased agent/skill에 대한 참조가 코드베이스에 남아있지 않음 (rename 완료)
- [ ] AC7: 이전과 동일한 최종 산출물이 생성됨 (output format 하위 호환)

<!-- spec-update-todo-input-end -->

---

# Part 2: Implementation Plan

## Overview

| Item | Detail |
|------|--------|
| 대상 | write-phased -> write-skeleton 전환, 호출자 13개 수정, write-phased 스킬 승격 |
| 총 태스크 | 5개 (Phase 1: agent 변경 2 -> Phase 2: 호출자 수정 3) |
| 예상 변경 규모 | 14개 파일 수정/생성 |

## 태스크

### Phase 1: Agent 변경 (선행)

#### Task 1: write-phased agent -> write-skeleton agent 전환

**설명**: write-phased.md를 write-skeleton.md로 rename하고, 역할을 skeleton 전용으로 축소. 반환 프로토콜 추가.

**Target Files**:
- [D] `.claude/agents/write-phased.md`
- [C] `.claude/agents/write-skeleton.md`

**Acceptance Criteria**:
- [ ] 짧은 문서 (섹션 3개 미만 / 함수 5개 미만): 전체 작성 후 COMPLETE 반환
- [ ] 긴 문서: skeleton만 작성 후 SKELETON_ONLY + 미완성 섹션 목록 반환
- [ ] skeleton의 각 미완성 섹션에 TODO 마커 존재
- [ ] Phase 2 fill 로직 제거 (호출자 책임으로 이전)
- [ ] 반환 형식: Status, File, Sections Written, Sections Remaining

#### Task 2: write-phased 스킬을 오케스트레이션 스킬로 승격

**설명**: 얇은 wrapper에서 실제 오케스트레이션 스킬로 변경. write-skeleton agent 호출 -> 반환값 분기 -> fill 수행.

**Target Files**:
- [M] `.claude/skills/write-phased/SKILL.md`

**Acceptance Criteria**:
- [ ] write-skeleton agent 호출 -> COMPLETE/SKELETON_ONLY 분기 처리
- [ ] SKELETON_ONLY 시 직접 Edit으로 fill (독립 섹션 2개+ 이면 병렬 agent dispatch)
- [ ] 완료 후 TODO/Phase 마커 전부 제거
- [ ] 모든 중간 과정이 메인 대화에서 실행되어 사용자에게 보임

### Phase 2: 호출자 수정 (Phase 1 완료 후, 상호 독립 -> 병렬 가능)

#### Task 3: Agent 호출자 수정 (4개)

**설명**: write-phased -> write-skeleton 호출로 변경하고, SKELETON_ONLY 시 fill 처리 로직 추가.

**Target Files**:
- [M] `.claude/agents/feature-draft.md`
- [M] `.claude/agents/implementation-plan.md`
- [M] `.claude/agents/implementation-review.md`
- [M] `.claude/agents/spec-review.md`

**Acceptance Criteria**:
- [ ] 4개 agent에서 `write-phased` -> `write-skeleton` 호출로 변경
- [ ] COMPLETE -> 완료, SKELETON_ONLY -> Edit fill 로직 존재
- [ ] 멀티파일 작성 시 기존 병렬 패턴 유지 (인덱스 먼저 -> 컴포넌트 병렬)

#### Task 4: Full Skill 호출자 수정 (8개)

**설명**: full skill에서 write-phased -> write-skeleton 호출로 변경하고, SKELETON_ONLY 시 fill 처리.

**Target Files**:
- [M] `.claude/skills/spec-create/SKILL.md`
- [M] `.claude/skills/spec-rewrite/SKILL.md`
- [M] `.claude/skills/spec-upgrade/SKILL.md`
- [M] `.claude/skills/spec-summary/SKILL.md`
- [M] `.claude/skills/pr-review/SKILL.md`
- [M] `.claude/skills/pr-spec-patch/SKILL.md`
- [M] `.claude/skills/guide-create/SKILL.md`
- [M] `.claude/skills/spec-snapshot/SKILL.md`

**Acceptance Criteria**:
- [ ] 8개 skill에서 `write-phased` -> `write-skeleton` 호출로 변경
- [ ] COMPLETE -> 완료, SKELETON_ONLY -> skill이 직접 Edit으로 fill
- [ ] full skill에서 fill하므로 중간 과정이 사용자에게 보임

#### Task 5: 참조 문서 및 정리

**설명**: 나머지 참조 업데이트 및 잔여 write-phased 참조 제거.

**Target Files**:
- [M] `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md`
- [M] `.claude/skills/write-phased/skill.json` (description 업데이트)

**Acceptance Criteria**:
- [ ] sdd-reasoning-reference.md에서 write-phased -> write-skeleton 참조 변경
- [ ] skill.json description이 새 역할 반영
- [ ] 코드베이스에 `write-phased` agent 참조가 남아있지 않음 (write-phased 스킬명은 유지)

## Parallel Execution Summary

```
Phase 1: [Task 1] -> [Task 2]  <- 순차 (Task 2가 Task 1의 agent를 사용)
Phase 2: [Task 3] [Task 4] [Task 5]  <- 전체 병렬
```

## 주의사항

- write-phased **스킬명**은 유지 (사용자 호출 인터페이스 보존)
- write-phased **agent**만 write-skeleton으로 rename
- Codex 쪽도 동일한 변경이 필요하지만 이 draft에서는 Claude Code만 다룸

## Next Steps

1. 이 draft를 리뷰하고 승인
2. `/implementation`으로 Phase 1 -> Phase 2 순서로 실행
3. 완료 후 AC 검증
4. Codex 쪽 동일 변경 별도 진행
5. `/spec-update-done`으로 스펙 동기화
