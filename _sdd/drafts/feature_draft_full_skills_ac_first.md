# Feature Draft: Full Skills AC-First 정제

**날짜**: 2026-03-19
**선행 작업**: Agent Self-Containment Phase 1+2 완료 (9개 agent 재작성)
**요청 배경**: Agent가 아닌 full skill 11개도 AC-First 원칙으로 정제. 디렉토리 구조(references/, examples/)는 유지하되 SKILL.md 본문을 간결하게 다듬는다.

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

### Improvement: Full Skills AC-First 정제

**Priority**: Medium
**Current State**: 11개 full skill 합계 5,042줄. AC 섹션 없음, verbose 섹션 다수, Best Practices/Context Management 반복.
**Proposed**: SDD 철학에 맞게 AC-First 구조 적용. 디렉토리 구조(references/, examples/)는 유지.

#### 현재 상태 vs 목표

| Skill | 현재 줄수 | 목표 줄수 | 감축률 | 주요 bloat |
|-------|----------|----------|--------|-----------|
| sdd-autopilot | 923 | ~620 | 33% | Step 7 Autonomous Execution 과다, review-fix loop 반복, 에러 핸들링 장문 |
| spec-summary | 813 | ~550 | 32% | Process steps decision gate 과다, Version History |
| spec-create | 464 | ~320 | 31% | Directory Structure 장문, Context Mgmt 중복, Best Practices 중복 |
| pr-spec-patch | 429 | ~300 | 30% | Output Format 보일러플레이트, Context Mgmt 중복 |
| pr-review | 429 | ~310 | 28% | Context Mgmt 중복, Edge Cases 장문 |
| spec-upgrade | 413 | ~290 | 30% | Gap Analysis 반복, Code Analysis 스캐닝 전략 과다 |
| discussion | 382 | ~260 | 32% | Step 3 probing 전략 과다, Best Practices 중복, Context Mgmt |
| spec-rewrite | 376 | ~260 | 31% | Propose step 반복, Hard Rules 산재 |
| git | 329 | ~250 | 24% | Phase 2 semantic grouping 예시 과다, Edge Cases |
| guide-create | 327 | ~220 | 33% | Process steps context mgmt 과다, Hard Rules 과다 |
| spec-snapshot | 157 | ~125 | 20% | 이미 간결, Hard Rules 일부 병합 가능 |
| **합계** | **5,042** | **~3,505** | **30%** | |

#### 정제 원칙

1. **AC-First 구조 적용**: 각 SKILL.md 상단에 Acceptance Criteria + 자체 검증 지시 추가
   ```
   ## Acceptance Criteria
   > 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.
   - [ ] AC1: ...
   ```
2. **공통 제거 대상**:
   - `Best Practices` 섹션 → 삭제 (LLM 판단 영역)
   - `Context Management` 테이블 → 삭제 (11개 skill 중 8개에 중복)
   - `When to Use This Skill` → 삭제 (description에 이미 있음)
   - `Version History` → 삭제 (git으로 관리)
   - `Integration with Other Skills` → 삭제 또는 1줄로 축소
3. **디렉토리 구조 유지**: references/, examples/ 파일은 삭제하지 않음
4. **핵심 보존**: Hard Rules, Process Steps, Output Format, Error Handling

#### Acceptance Criteria (전체)

- [ ] AC1: 11개 skill이 AC-First 구조 (AC 섹션 + 자체 검증 지시)를 가짐
- [ ] AC2: 11개 skill 전체 합계 줄수가 현재 5,042줄에서 3,800줄 이하로 감축 (25%+)
- [ ] AC3: 각 skill의 핵심 기능이 보존됨 (Hard Rules, Process, Output Format)
- [ ] AC4: references/, examples/ 디렉토리 및 파일이 삭제되지 않음
- [ ] AC5: frontmatter (skill.json) 변경 없음

<!-- spec-update-todo-input-end -->

---

# Part 2: Implementation Plan

## Overview

| Item | Detail |
|------|--------|
| 대상 | `.claude/skills/` 하위 11개 full skill의 SKILL.md |
| 작업 유형 | AC-First 구조 적용 + verbose 섹션 정제 (references/examples는 유지) |
| 총 태스크 | 11개 (전체 병렬 가능 -- 각 skill 독립 파일) |
| 예상 변경 규모 | 현재 5,042줄 → ~3,505줄 (30% 감축) |

## 정제 공통 가이드

### AC-First 구조 (모든 skill 공통)

기존 SKILL.md 앞부분에 AC 섹션을 추가하고, verbose 섹션을 정제:

```
---
frontmatter (기존 유지 -- 수정하지 않음)
---
# [Skill Name]
[기존 설명 유지]

## Acceptance Criteria
> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.
- [ ] AC1: ...

## Hard Rules
(기존 유지)

## Process
(정제)

## Output Format
(정제)

## Error Handling
(정제)
```

### 공통 삭제 대상

| 섹션 | 해당 skill 수 | 이유 |
|------|-------------|------|
| Best Practices | 8/11 | LLM 판단 영역, 중복 |
| Context Management | 8/11 | 11개 skill에 반복, LLM 판단 영역 |
| When to Use This Skill | 9/11 | description에 이미 있음 |
| Version History | 1/11 (spec-summary) | git으로 관리 |
| Integration with Other Skills | 7/11 | 1줄로 축소 또는 삭제 |
| Language Handling (장문) | 4/11 | Hard Rules에 1줄로 통합 |

## 태스크 (전체 병렬 -- 파일 간 의존 없음)

### Task 1: sdd-autopilot 정제
**Target Files**: [M] `.claude/skills/sdd-autopilot/SKILL.md`
**현재**: 923줄 → **목표**: ~620줄 (33%)
**Agent AC**:
- [ ] 8-step pipeline process 보존
- [ ] review-fix loop 및 자율 실행 로직 보존
- [ ] AC 섹션 + 자체 검증 지시 추가
**정제**: Step 7 review-fix loop 반복 제거, Hard Rules 10→6개 통합, test 전략 A/B 구조 통합, Best Practices 삭제, 에러 핸들링 축소

### Task 2: spec-summary 정제
**Target Files**: [M] `.claude/skills/spec-summary/SKILL.md`
**현재**: 813줄 → **목표**: ~550줄 (32%)
**Agent AC**:
- [ ] 7-step summary generation process 보존
- [ ] Output Format (layered summary structure) 보존
- [ ] AC 섹션 + 자체 검증 지시 추가
**정제**: Process steps decision gate 축소, Version History 삭제, Best Practices 삭제, Success Criteria → AC 섹션으로 이동

### Task 3: spec-create 정제
**Target Files**: [M] `.claude/skills/spec-create/SKILL.md`
**현재**: 464줄 → **목표**: ~320줄 (31%)
**Agent AC**:
- [ ] Bootstrap + Write 프로세스 보존
- [ ] SS1-SS8 템플릿 참조 보존
- [ ] AC 섹션 + 자체 검증 지시 추가
**정제**: Directory Structure 장문 → 테이블 1개로 축소, Context Mgmt 삭제, Best Practices 삭제, Spec Management Operations 중복 제거

### Task 4: pr-spec-patch 정제
**Target Files**: [M] `.claude/skills/pr-spec-patch/SKILL.md`
**현재**: 429줄 → **목표**: ~300줄 (30%)
**Agent AC**:
- [ ] 2가지 모드 (Initial/Update) 보존
- [ ] spec-update-todo 호환 출력 형식 보존
- [ ] AC 섹션 + 자체 검증 지시 추가
**정제**: Context Mgmt 삭제, Best Practices 삭제, Output Format 보일러플레이트 축소, Language Handling → 1줄

### Task 5: pr-review 정제
**Target Files**: [M] `.claude/skills/pr-review/SKILL.md`
**현재**: 429줄 → **목표**: ~310줄 (28%)
**Agent AC**:
- [ ] 2가지 모드 (Preferred/Degraded) 보존
- [ ] Verdict 로직 (APPROVE/REQUEST CHANGES/NEEDS DISCUSSION) 보존
- [ ] AC 섹션 + 자체 검증 지시 추가
**정제**: Context Mgmt 삭제, Best Practices 삭제, Edge Cases 축소, Language Handling → 1줄

### Task 6: spec-upgrade 정제
**Target Files**: [M] `.claude/skills/spec-upgrade/SKILL.md`
**현재**: 413줄 → **목표**: ~290줄 (30%)
**Agent AC**:
- [ ] SS1-SS8 Gap Analysis + Whitepaper 변환 프로세스 보존
- [ ] references/ 참조 (template-compact, spec-format, upgrade-mapping) 보존
- [ ] AC 섹션 + 자체 검증 지시 추가
**정제**: Gap Analysis SS1-SS8 반복 테이블 축소, Code Analysis 스캐닝 전략 축소, Context Mgmt 삭제

### Task 7: discussion 정제
**Target Files**: [M] `.claude/skills/discussion/SKILL.md`
**현재**: 382줄 → **목표**: ~260줄 (32%)
**Agent AC**:
- [ ] 4-step iterative discussion process 보존
- [ ] 토론 결과 파일 저장 보존
- [ ] AC 섹션 + 자체 검증 지시 추가
**정제**: Step 3 probing 전략 축소, Context Mgmt 삭제, Best Practices 삭제, Progressive Disclosure 축소

### Task 8: spec-rewrite 정제
**Target Files**: [M] `.claude/skills/spec-rewrite/SKILL.md`
**현재**: 376줄 → **목표**: ~260줄 (31%)
**Agent AC**:
- [ ] 7-step rewrite process 보존
- [ ] references/ 참조 (rewrite-checklist, spec-format, template-compact) 보존
- [ ] AC 섹션 + 자체 검증 지시 추가
**정제**: Propose step 반복 제거, Hard Rules 통합, Context Mgmt 삭제, Best Practices 삭제, Quality Checklist → AC로 이동

### Task 9: git 정제
**Target Files**: [M] `.claude/skills/git/SKILL.md`
**현재**: 329줄 → **목표**: ~250줄 (24%)
**Agent AC**:
- [ ] 5-phase workflow (ASSESS→PLAN→CONFIRM→EXECUTE→REPORT) 보존
- [ ] Semantic grouping + Conventional Commits 보존
- [ ] AC 섹션 + 자체 검증 지시 추가
**정제**: Phase 2 semantic grouping 예시 축소, Edge Cases 축소, Shorthand Modes 축소

### Task 10: guide-create 정제
**Target Files**: [M] `.claude/skills/guide-create/SKILL.md`
**현재**: 327줄 → **목표**: ~220줄 (33%)
**Agent AC**:
- [ ] 6-step guide generation process 보존
- [ ] SS1-SS5 required sections structure 보존
- [ ] AC 섹션 + 자체 검증 지시 추가
**정제**: Process steps context mgmt 삭제, Hard Rules 축소, When to Use 삭제, Inline Citation Rules 중복 제거

### Task 11: spec-snapshot 정제
**Target Files**: [M] `.claude/skills/spec-snapshot/SKILL.md`
**현재**: 157줄 → **목표**: ~125줄 (20%)
**Agent AC**:
- [ ] 4-step snapshot process 보존
- [ ] 번역 규칙 보존
- [ ] AC 섹션 + 자체 검증 지시 추가
**정제**: Hard Rules 3+4 병합, Integration 축소

## Parallel Execution Summary

```
Phase 1: [Task 1-11]  <- 전체 병렬 (11개 skill 모두 독립 파일)
```

## Next Steps

1. 이 draft를 리뷰하고 승인
2. `/implementation`으로 11개 태스크 병렬 실행
3. 완료 후 각 skill의 AC 검증
4. Agent + Full Skill 전체 결과를 `/spec-update-done`으로 스펙 동기화
