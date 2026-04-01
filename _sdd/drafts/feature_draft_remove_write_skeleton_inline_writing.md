# Feature Draft: Remove write_skeleton and Shift to Inline 2-Phase Writing

**Date**: 2026-04-01
**Author**: feature-draft
**Target Spec**: `_sdd/spec/main.md`
**Status**: Draft
**Discussion Reference**: `_sdd/discussion/discussion_write_skeleton_removal_and_inline_writing.md`

---

<!-- spec-update-todo-input-start -->
# Part 1: Spec Patch Draft

> This patch can be copy-pasted into the corresponding spec section,
> or used as input for the `spec-update-todo` skill.

# Spec Update Input

**Date**: 2026-04-01
**Author**: feature-draft
**Target Spec**: `_sdd/spec/main.md`
**Spec Update Classification**: MUST update

## Background & Motivation Updates

### Background Update: write_skeleton helper 제거 배경

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Core Design > Key Idea`

**Current State**:
현재 Claude Code와 Codex 양쪽 모두 장문 문서/코드 작성에 대해 `write_skeleton` helper agent 또는 그에 준하는 skeleton-first helper를 전제하는 문서가 남아 있다. 이 구조는 이론적으로는 skeleton 작성과 fill을 분리해 품질을 높이려 했지만, 실제로는 다음 비용을 초래한다.

- skeleton 생성이 부모 콘텍스트에 강하게 의존한다
- caller가 충분한 맥락을 다시 말아 전달해야 한다
- `fork_context`, handoff contract, 반환 해석 규칙이 추가로 필요하다
- "그럴 바엔 호출자가 현재 콘텍스트에서 직접 skeleton을 만들고 채우는 게 더 낫다"는 사용성 문제가 발생한다

**Proposed**:
기본 writing 경로에서 `write_skeleton` helper agent를 제거하고, producer/caller가 현재 콘텍스트에서 직접 다음 순서로 작성한다.

1. 대상 파일에 skeleton/섹션 제목/placeholder를 먼저 기록
2. 같은 호출 흐름에서 섹션별 내용을 채움
3. TODO/Phase marker를 정리하고 finalize

**Reason**:
- 부모가 이미 가진 콘텍스트를 재설명할 필요가 없다
- helper 분리보다 inline execution이 가시성과 품질에 유리하다
- 플랫폼별 subagent 문법 차이와 handoff complexity를 줄일 수 있다

## Design Changes

### Design Change: Producer-Owned Inline 2-Phase Writing

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Core Design > Design Patterns`

**Description**:
`write_skeleton` 기반 helper 분리를 기본 경로에서 제거하고, producer skill/agent가 자신의 산출물을 현재 콘텍스트에서 직접 작성하는 **Producer-Owned Inline 2-Phase Writing** 패턴을 도입한다.

```text
# Before
caller
  -> helper agent(write_skeleton)
  -> helper가 skeleton 작성
  -> caller가 반환값 해석
  -> fill

# After
caller
  -> 현재 콘텍스트에서 skeleton 직접 작성
  -> 같은 흐름에서 fill
  -> finalize
```

핵심 규칙:
- skeleton 생성과 fill은 같은 호출 흐름에서 수행한다
- helper handoff를 기본값으로 두지 않는다
- 필요 시 병렬화는 skeleton helper가 아니라 producer의 own task/file decomposition으로 수행한다

### Design Change: write_skeleton 완전 제거

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Component Details`

**Description**:
Claude Code의 `.claude/agents/write-skeleton.md`와 Codex의 `.codex/agents/write-skeleton.toml`을 제거한다. 이 컴포넌트는 deprecated 유지가 아니라 **완전 제거** 대상으로 본다.

Acceptance intent:
- helper agent를 기본 writing backbone으로 설명하지 않는다
- 기존 caller는 helper 호출 대신 inline skeleton 작성 규칙으로 이관한다

### Design Change: write-phased 역할 재정의

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Component Details > write-phased`

**Description**:
`write-phased`는 더 이상 `write_skeleton` helper를 호출하는 orchestrator가 아니다. 대신 subagent 없이 producer/caller가 직접 수행하는 **inline 2-phase writing utility contract**로 재정의한다.

새 contract:
- Phase 1: caller가 파일에 skeleton/outline/TODO marker를 직접 기록
- Phase 2: caller가 같은 콘텍스트에서 내용을 채움
- Finalize: marker 정리, cross-reference 검증, 보고

### Design Change: Platform Runtime Guidance 단순화

**Priority**: Medium
**Target Section**: `_sdd/spec/main.md` > `Core Design > SKILL.md / Agent 정의 공통 구조`

**Description**:
Claude Code와 Codex 양쪽의 writing 관련 runtime guidance에서 nested `write_skeleton` helper 전제를 제거한다. 문서 작성 규칙은 다음처럼 단순화한다.

- Claude: caller가 `Write`/`Edit` 중심으로 inline 2-phase 수행
- Codex: caller가 현재 컨텍스트에서 inline 2-phase 수행하며, 별도 helper spawn을 기본으로 요구하지 않음
- `write-phased`는 helper spawn 예시 대신 inline skeleton + fill 규칙을 제공

## Improvements

### Improvement: Claude Code writing caller 정리

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Usage Guide & Expected Results`

**Current State**:
다수 Claude skill/agent 문서가 `sdd-skills:write-skeleton` helper 호출을 설명한다.

**Proposed**:
현재 runtime 파일 기준으로 다음 Claude 파일을 inline 2-phase writing 규칙으로 갱신한다.

- `.claude/agents/write-skeleton.md` -- 삭제
- `.claude/skills/write-phased/SKILL.md`
- `.claude/skills/write-phased/skill.json`
- `.claude/agents/feature-draft.md`
- `.claude/agents/implementation-plan.md`
- `.claude/agents/implementation-review.md`
- `.claude/agents/spec-review.md`
- `.claude/skills/feature-draft/SKILL.md`
- `.claude/skills/guide-create/SKILL.md`
- `.claude/skills/implementation-plan/SKILL.md`
- `.claude/skills/implementation-review/SKILL.md`
- `.claude/skills/pr-review/SKILL.md`
- `.claude/skills/pr-spec-patch/SKILL.md`
- `.claude/skills/spec-create/SKILL.md`
- `.claude/skills/spec-review/SKILL.md`
- `.claude/skills/spec-rewrite/SKILL.md`
- `.claude/skills/spec-snapshot/SKILL.md`
- `.claude/skills/spec-summary/SKILL.md`
- `.claude/skills/spec-upgrade/SKILL.md`
- `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md`

### Improvement: Codex writing caller 정리

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Usage Guide & Expected Results`

**Current State**:
다수 Codex skill/agent 문서가 `write_skeleton` helper 호출 또는 nested helper 전제를 가진다.

**Proposed**:
현재 runtime 파일 기준으로 다음 Codex 파일을 inline 2-phase writing 규칙으로 갱신한다.

- `.codex/agents/write-skeleton.toml` -- 삭제
- `.codex/agents/README.md`
- `.codex/skills/write-phased/SKILL.md`
- `.codex/skills/write-phased/skill.json`
- `.codex/agents/feature-draft.toml`
- `.codex/agents/implementation-plan.toml`
- `.codex/agents/implementation-review.toml`
- `.codex/skills/feature-draft/SKILL.md`
- `.codex/skills/guide-create/SKILL.md`
- `.codex/skills/implementation-plan/SKILL.md`
- `.codex/skills/implementation-review/SKILL.md`
- `.codex/skills/pr-review/SKILL.md`
- `.codex/skills/pr-spec-patch/SKILL.md`
- `.codex/skills/spec-create/SKILL.md`
- `.codex/skills/spec-rewrite/SKILL.md`
- `.codex/skills/spec-snapshot/SKILL.md`
- `.codex/skills/spec-summary/SKILL.md`
- `.codex/skills/spec-upgrade/SKILL.md`
- `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md`

### Improvement: Current Spec / Decision 문서 동기화

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Identified Issues & Improvements`

**Proposed**:
현재 스펙과 결정 로그에서 `write_skeleton` 또는 nested writing helper를 기본 경로처럼 설명하는 부분을 inline 2-phase writing 기준으로 재서술한다.

Current spec/docs targets:
- `_sdd/spec/main.md`
- `_sdd/spec/DECISION_LOG.md`
- `_sdd/discussion/discussion_write_skeleton_removal_and_inline_writing.md`

## Failure Modes

| 시나리오 | 실패 시 | 사용자 가시성 | 처리 방안 |
|---------|---------|-------------|----------|
| helper 제거 후 caller가 skeleton 작성 규칙을 잊음 | 문서가 한 번에 길게 써져 후반 품질 저하 | 결과 문서 품질 저하로 직접 관찰 | `write-phased`와 producer 문서에 inline 2-phase 절차를 명시 |
| 기존 `write_skeleton` 참조가 일부 잔존 | 플랫폼별 문서/실행 계약 불일치 | 특정 스킬만 옛 helper 전제를 보임 | affected files checklist로 전수 점검 |
| `write-phased` 역할 재정의가 불완전 | utility 설명과 실제 caller 행동이 어긋남 | 문서 간 상충 표현 노출 | `write-phased` + caller + spec를 한 묶음으로 동시 수정 |
| historical draft/prev 문서가 과거 설명을 유지 | 탐색 시 혼란 가능 | 오래된 문서를 읽을 때만 발생 | current runtime/spec 우선 수정, 과거 문서는 후속 cleanup으로 분리 |
| inline 2-phase가 producer 문서마다 제각각이 됨 | writing 규칙이 분산 | 산출물 품질 편차 | `write-phased`를 공용 inline-writing contract로 유지 |

## Notes

- 이번 범위의 핵심은 **현재 runtime + 현재 spec/docs** 정리다. `_sdd/spec/prev/`와 과거 구현 산출물은 직접 수정 범위에서 제외한다.
- Claude와 Codex 모두 영향을 받지만, 플랫폼별 문법 차이는 "helper 제거" 이후 오히려 축소된다.
<!-- spec-update-todo-input-end -->

---

# Part 2: Implementation Plan

## Overview

`write_skeleton` helper agent를 Claude Code와 Codex 양쪽에서 제거하고, writing 관련 caller들을 inline 2-phase writing으로 전환한다. `write-phased`는 helper orchestrator가 아니라 공용 inline writing contract로 재정의하며, 현재 스펙/결정 문서도 이에 맞춰 동기화한다.

## Scope

### In Scope

- Claude Code runtime에서 `write-skeleton` 제거 및 caller 정리
- Codex runtime에서 `write_skeleton` 제거 및 caller 정리
- `write-phased` 재정의
- current spec/decision/discussion 문서 동기화
- current runtime affected files 전수 리스트업 및 수정 계획 수립

### Out of Scope

- `_sdd/spec/prev/` 아래 historical snapshot 대량 정리
- `_sdd/drafts/`의 과거 초안 전수 리라이트
- 구현 완료 후의 후속 docs hygiene 일괄 정리
- inline 2-phase writing 이후의 추가 fan-out 최적화

## Components

1. **Claude Inline Writing Runtime**: Claude caller와 utility에서 helper 제거
2. **Codex Inline Writing Runtime**: Codex caller와 utility에서 helper 제거
3. **Shared Writing Contract**: `write-phased`를 inline 2-phase utility로 재정의
4. **Spec & Decision Sync**: 현재 스펙/결정/토론 문서를 최신 설계와 동기화

## Affected Files

### Claude Code -- Current Runtime Files

- `.claude/agents/write-skeleton.md`
- `.claude/skills/write-phased/SKILL.md`
- `.claude/skills/write-phased/skill.json`
- `.claude/agents/feature-draft.md`
- `.claude/agents/implementation-plan.md`
- `.claude/agents/implementation-review.md`
- `.claude/agents/spec-review.md`
- `.claude/skills/feature-draft/SKILL.md`
- `.claude/skills/guide-create/SKILL.md`
- `.claude/skills/implementation-plan/SKILL.md`
- `.claude/skills/implementation-review/SKILL.md`
- `.claude/skills/pr-review/SKILL.md`
- `.claude/skills/pr-spec-patch/SKILL.md`
- `.claude/skills/spec-create/SKILL.md`
- `.claude/skills/spec-review/SKILL.md`
- `.claude/skills/spec-rewrite/SKILL.md`
- `.claude/skills/spec-snapshot/SKILL.md`
- `.claude/skills/spec-summary/SKILL.md`
- `.claude/skills/spec-upgrade/SKILL.md`
- `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md`

### Codex -- Current Runtime Files

- `.codex/agents/write-skeleton.toml`
- `.codex/agents/README.md`
- `.codex/skills/write-phased/SKILL.md`
- `.codex/skills/write-phased/skill.json`
- `.codex/agents/feature-draft.toml`
- `.codex/agents/implementation-plan.toml`
- `.codex/agents/implementation-review.toml`
- `.codex/skills/feature-draft/SKILL.md`
- `.codex/skills/guide-create/SKILL.md`
- `.codex/skills/implementation-plan/SKILL.md`
- `.codex/skills/implementation-review/SKILL.md`
- `.codex/skills/pr-review/SKILL.md`
- `.codex/skills/pr-spec-patch/SKILL.md`
- `.codex/skills/spec-create/SKILL.md`
- `.codex/skills/spec-rewrite/SKILL.md`
- `.codex/skills/spec-snapshot/SKILL.md`
- `.codex/skills/spec-summary/SKILL.md`
- `.codex/skills/spec-upgrade/SKILL.md`
- `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md`

### Current Spec / Decision / Discussion Files

- `_sdd/spec/main.md`
- `_sdd/spec/DECISION_LOG.md`
- `_sdd/discussion/discussion_write_skeleton_removal_and_inline_writing.md`

## Implementation Phases

### Phase 1: Shared Contract Re-definition

| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 1 | `write-phased`를 inline 2-phase utility로 재정의 | P0-Critical | - | Shared Writing Contract |
| 2 | `write_skeleton` 제거 기준과 caller 책임 경계를 명문화 | P0-Critical | 1 | Shared Writing Contract |

### Phase 2: Claude Runtime Migration

| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 3 | Claude `write-skeleton` agent 삭제 및 utility 정리 | P1-High | 1, 2 | Claude Inline Writing Runtime |
| 4 | Claude caller/producer 문서 전환 | P1-High | 3 | Claude Inline Writing Runtime |

### Phase 3: Codex Runtime Migration

| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 5 | Codex `write_skeleton` custom agent 삭제 및 README 정리 | P1-High | 1, 2 | Codex Inline Writing Runtime |
| 6 | Codex caller/producer 문서 전환 | P1-High | 5 | Codex Inline Writing Runtime |

### Phase 4: Spec / Decision Sync

| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 7 | current spec/decision/discussion 문서 동기화 | P1-High | 3, 4, 5, 6 | Spec & Decision Sync |

## Task Details

### Task 1: `write-phased`를 inline 2-phase utility로 재정의
**Component**: Shared Writing Contract
**Priority**: P0-Critical
**Type**: Refactor

**Description**: `write-phased`를 helper agent orchestration에서 producer-owned inline writing utility로 재정의한다. skeleton 생성, fill, marker cleanup을 모두 caller가 같은 실행 흐름에서 수행하는 규칙으로 바꾼다.

**Acceptance Criteria**:
- [ ] Claude/Codex `write-phased` 설명에서 `write_skeleton` helper 호출 전제가 제거된다
- [ ] 새 contract가 "skeleton 작성 -> fill -> finalize" 흐름으로 정리된다
- [ ] helper 반환 형식(`SKELETON_ONLY`, `Sections Remaining`) 의존 설명이 제거되거나 비핵심으로 내려간다

**Target Files**:
- [M] `.claude/skills/write-phased/SKILL.md` -- inline writing utility로 재정의
- [M] `.claude/skills/write-phased/skill.json` -- 설명 동기화
- [M] `.codex/skills/write-phased/SKILL.md` -- inline writing utility로 재정의
- [M] `.codex/skills/write-phased/skill.json` -- 설명 동기화

**Technical Notes**: helper 호출 예시 대신 현재 콘텍스트에서 skeleton을 직접 기록하는 절차를 넣는다.
**Dependencies**: -

### Task 2: `write_skeleton` 제거 기준과 caller 책임 경계 명문화
**Component**: Shared Writing Contract
**Priority**: P0-Critical
**Type**: Refactor

**Description**: helper 제거 이후 caller가 무엇을 직접 책임지는지 명확히 한다. producer는 자신의 산출물 구조와 초안 skeleton을 직접 작성하고, `write-phased`는 공용 writing 규칙만 제공한다.

**Acceptance Criteria**:
- [ ] "helper가 skeleton 생성" 설명이 "caller가 skeleton 작성" 설명으로 치환된다
- [ ] inline 2-phase 규칙이 producer 문서에 재사용 가능한 수준으로 정리된다
- [ ] helper handoff contract를 기본 경로로 설명하지 않는다

**Target Files**:
- [M] `.claude/skills/write-phased/SKILL.md`
- [M] `.codex/skills/write-phased/SKILL.md`
- [M] `_sdd/spec/main.md`

**Technical Notes**: "producer-owned inline writing"라는 용어를 일관되게 사용할지 검토한다.
**Dependencies**: 1

### Task 3: Claude `write-skeleton` agent 삭제 및 utility 정리
**Component**: Claude Inline Writing Runtime
**Priority**: P1-High
**Type**: Refactor

**Description**: Claude helper agent를 삭제하고, utility 및 reference 문서에서 helper 전제를 제거한다.

**Acceptance Criteria**:
- [ ] `.claude/agents/write-skeleton.md`가 삭제된다
- [ ] Claude `write-phased`와 reasoning reference가 helper 없는 구조로 설명된다
- [ ] runtime guidance가 inline writing 기준으로 일관된다

**Target Files**:
- [D] `.claude/agents/write-skeleton.md`
- [M] `.claude/skills/write-phased/SKILL.md`
- [M] `.claude/skills/write-phased/skill.json`
- [M] `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md`

**Technical Notes**: Claude는 `Agent(subagent_type="write-skeleton")` 문법 자체를 제거하거나 legacy note로만 남긴다.
**Dependencies**: 1, 2

### Task 4: Claude caller/producer 문서 전환
**Component**: Claude Inline Writing Runtime
**Priority**: P1-High
**Type**: Refactor

**Description**: 현재 Claude caller/producer가 helper 호출을 전제하는 문구를 inline 2-phase writing 지시로 바꾼다.

**Acceptance Criteria**:
- [ ] 아래 affected files에서 `write-skeleton` helper 의존이 제거된다
- [ ] skeleton/fill/finalize를 caller가 직접 수행하도록 지시가 바뀐다
- [ ] mirror 관계가 있는 파일은 일관되게 갱신된다

**Target Files**:
- [M] `.claude/agents/feature-draft.md`
- [M] `.claude/agents/implementation-plan.md`
- [M] `.claude/agents/implementation-review.md`
- [M] `.claude/agents/spec-review.md`
- [M] `.claude/skills/feature-draft/SKILL.md`
- [M] `.claude/skills/guide-create/SKILL.md`
- [M] `.claude/skills/implementation-plan/SKILL.md`
- [M] `.claude/skills/implementation-review/SKILL.md`
- [M] `.claude/skills/pr-review/SKILL.md`
- [M] `.claude/skills/pr-spec-patch/SKILL.md`
- [M] `.claude/skills/spec-create/SKILL.md`
- [M] `.claude/skills/spec-review/SKILL.md`
- [M] `.claude/skills/spec-rewrite/SKILL.md`
- [M] `.claude/skills/spec-snapshot/SKILL.md`
- [M] `.claude/skills/spec-summary/SKILL.md`
- [M] `.claude/skills/spec-upgrade/SKILL.md`

**Technical Notes**: 필요한 경우 "먼저 파일에 outline 작성" 같은 direct Edit/Write 지시를 플랫폼 문법에 맞게 넣는다.
**Dependencies**: 3

### Task 5: Codex `write_skeleton` custom agent 삭제 및 README 정리
**Component**: Codex Inline Writing Runtime
**Priority**: P1-High
**Type**: Refactor

**Description**: Codex helper custom agent를 삭제하고, `.codex/agents/README.md`에서 nested writing helper를 기본 경로처럼 설명하는 부분을 정리한다.

**Acceptance Criteria**:
- [ ] `.codex/agents/write-skeleton.toml`이 삭제된다
- [ ] `.codex/agents/README.md`에서 `write_skeleton` helper를 기본 예시로 설명하지 않는다
- [ ] Codex runtime guidance가 inline writing 전환과 모순되지 않는다

**Target Files**:
- [D] `.codex/agents/write-skeleton.toml`
- [M] `.codex/agents/README.md`
- [M] `.codex/skills/write-phased/SKILL.md`
- [M] `.codex/skills/write-phased/skill.json`
- [M] `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md`

**Technical Notes**: README의 invocation contract는 유지하되, helper 예시는 inline writing 원칙과 충돌하지 않도록 조정한다.
**Dependencies**: 1, 2

### Task 6: Codex caller/producer 문서 전환
**Component**: Codex Inline Writing Runtime
**Priority**: P1-High
**Type**: Refactor

**Description**: Codex caller/producer가 `write_skeleton` helper를 spawn하도록 설명하는 부분을 inline 2-phase writing 지시로 바꾼다.

**Acceptance Criteria**:
- [ ] 아래 affected files에서 `write_skeleton` helper 호출 전제가 제거된다
- [ ] Codex-native 문법은 유지하되, writing은 caller가 직접 수행하는 방향으로 정리된다
- [ ] nested helper 전제가 남지 않는다

**Target Files**:
- [M] `.codex/agents/feature-draft.toml`
- [M] `.codex/agents/implementation-plan.toml`
- [M] `.codex/agents/implementation-review.toml`
- [M] `.codex/skills/feature-draft/SKILL.md`
- [M] `.codex/skills/guide-create/SKILL.md`
- [M] `.codex/skills/implementation-plan/SKILL.md`
- [M] `.codex/skills/implementation-review/SKILL.md`
- [M] `.codex/skills/pr-review/SKILL.md`
- [M] `.codex/skills/pr-spec-patch/SKILL.md`
- [M] `.codex/skills/spec-create/SKILL.md`
- [M] `.codex/skills/spec-rewrite/SKILL.md`
- [M] `.codex/skills/spec-snapshot/SKILL.md`
- [M] `.codex/skills/spec-summary/SKILL.md`
- [M] `.codex/skills/spec-upgrade/SKILL.md`

**Technical Notes**: 필요 시 "spawn_agent(write_skeleton)" 예시를 "직접 skeleton 작성" 절차나 bounded worker fan-out 예시로 대체한다.
**Dependencies**: 5

### Task 7: current spec/decision/discussion 문서 동기화
**Component**: Spec & Decision Sync
**Priority**: P1-High
**Type**: Documentation

**Description**: 현재 스펙, 결정 로그, 토론 요약을 helper 제거와 inline writing 전환에 맞게 동기화한다.

**Acceptance Criteria**:
- [ ] `_sdd/spec/main.md`의 component/design pattern 설명이 최신 구조와 맞다
- [ ] `_sdd/spec/DECISION_LOG.md`에 helper 제거 및 write-phased 재정의 결정이 기록된다
- [ ] discussion 문서와 spec 서술이 서로 충돌하지 않는다

**Target Files**:
- [M] `_sdd/spec/main.md`
- [M] `_sdd/spec/DECISION_LOG.md`
- [M] `_sdd/discussion/discussion_write_skeleton_removal_and_inline_writing.md`

**Technical Notes**: historical `prev/`는 reference로만 두고 current doc만 authoritative하게 갱신한다.
**Dependencies**: 3, 4, 5, 6

## Parallel Execution Summary

- Task 1, 2는 shared contract이므로 순차
- Task 3과 Task 5는 플랫폼별 helper 제거 작업으로 병렬 가능
- Task 4와 Task 6은 플랫폼별 caller migration이므로 병렬 가능
- Task 7은 앞선 runtime 변경 방향이 확정된 뒤 수행

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| helper 제거 후 일부 문서에 옛 설명 잔존 | 플랫폼별 동작 계약 불일치 | affected files 전수 체크리스트 기반으로 수정 |
| `write-phased` 재정의가 모호함 | utility가 다시 애매한 helper처럼 남음 | skeleton/fill/finalize를 caller 책임으로 명시 |
| Claude와 Codex 문법 차이로 표현이 어긋남 | 플랫폼별 drift | 공통 개념은 같게, 호출 문법만 플랫폼별로 분리 |
| current spec만 고치고 draft/history가 남아 혼동 | 탐색 중 혼란 | 이번 범위는 current authoritative docs 우선, history cleanup은 별도 후속 작업 |

## Open Questions

- 없음. 현재 요구 수준에서는 helper 제거와 inline writing 전환이 핵심 결정으로 충분하다.
