# Feature Draft: gstack Patterns for SDD Skills

**Date**: 2026-03-24
**Author**: Claude (feature-draft agent)
**Target Spec**: `_sdd/spec/main.md`
**Status**: Part 1 Processed (spec-update-todo applied to main.md v3.6.1, 2026-03-24)

---

<!-- spec-update-todo-input-start -->
# Part 1: Spec Patch Draft

> This patch can be copy-pasted into the corresponding spec section,
> or used as input for the `spec-update-todo` skill.

# Spec Update Input

**Date**: 2026-03-24
**Author**: Claude
**Target Spec**: `_sdd/spec/main.md`

## New Features

### Feature: Failure Modes Table in Feature Draft
**Priority**: Medium
**Target Section**: `_sdd/spec/main.md` > `Component Details > feature-draft`
**Description**: feature-draft Part 1 스펙 패치에 경량 Failure Modes 테이블 섹션을 항상 포함. 간단하면 N/A 또는 1-2행, 복잡하면 3-5행 (시나리오/실패 시/사용자 가시성/처리 방안).
**Acceptance Criteria**:
- [ ] Part 1 출력에 Failure Modes 섹션이 항상 존재한다
- [ ] 간단한 기능에서는 N/A 또는 1-2행으로 유지된다

### Feature: Investigate Skill (Systematic Debugging)
**Priority**: Low
**Target Section**: `_sdd/spec/main.md` > `Component Details`
**Description**: 범용 체계적 디버깅 에이전트/스킬 신규 생성. 근본원인 우선(Iron Law), 3-strike 에스컬레이션, scope lock, blast radius gate, fresh verification, 독립 Agent 교차 검증 포함.
**Acceptance Criteria**:
- [ ] `.claude/agents/investigate.md` 에이전트가 AC-First + Self-Contained 구조로 존재한다
- [ ] `.claude/skills/investigate/SKILL.md` 래퍼 스킬이 존재한다
- [ ] 근본원인 우선, 3-strike, scope lock, blast radius gate, fresh verification, 독립 Agent 교차 검증이 포함되어 있다

### Feature: Test Coverage Mapping in Implementation Plan
**Priority**: Medium
**Target Section**: `_sdd/spec/main.md` > `Component Details > implementation-plan`
**Description**: Target Files에 [M] 마커가 있을 때 해당 파일의 기존 테스트 커버리지를 매핑. [C] 전용이면 스킵.
**Acceptance Criteria**:
- [ ] [M] 마커 대상 파일에 대해 기존 테스트 커버리지가 매핑된다
- [ ] [C] 전용 계획에서는 매핑 단계가 스킵된다

### Feature: Scope Drift Detection in PR Review
**Priority**: Medium
**Target Section**: `_sdd/spec/main.md` > `Component Details > pr-review`
**Description**: PR diff 변경 파일 vs 스펙 패치 초안 범위를 비교하는 pre-step 추가. CLEAN/DRIFT/MISSING 판정을 리포트 상단에 표시.
**Acceptance Criteria**:
- [ ] Step 2.5로 Scope Drift Detection이 실행된다
- [ ] 판정 결과(CLEAN/DRIFT/MISSING)가 리포트 상단에 표시된다

### Feature: Code Quality Fix-First in PR Review
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Component Details > pr-review`
**Description**: 누락된 에러 처리, 타입 불일치, 미사용 import 등을 AUTO-FIX(즉시 수정) / 목록 기록(수정 불가) 분류. AskUserQuestion 없이 처리. 스펙 레이어(APPROVE/REQUEST CHANGES/NEEDS DISCUSSION)는 유지.
**Acceptance Criteria**:
- [ ] Step 5.5로 코드 품질 Fix-First가 실행된다
- [ ] AUTO-FIX 대상과 목록 기록 대상이 분류된다
- [ ] 스펙 레이어 verdict는 변경되지 않는다

### Feature: Code Analysis Metrics in Spec Review
**Priority**: Low
**Target Section**: `_sdd/spec/main.md` > `Component Details > spec-review`
**Description**: 핫스팟(자주 변경 파일), Focus Score(변경 집중도), Test Coverage(스펙 기능별 테스트 현황) 지표를 추가하여 "어디를 더 깊이 봐야 하는지" 데이터 기반 판단.
**Acceptance Criteria**:
- [ ] 핫스팟, Focus Score, Test Coverage 지표가 리뷰에 포함된다
- [ ] 지표 결과가 리뷰 우선순위 결정에 활용된다

## Improvements

### Improvement: Verification Gate Iron Rule
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Component Details > implementation, implementation-review`
**Current State**: 코드 변경 후 검증이 명시적으로 강제되지 않음
**Proposed**: "should work" 금지, 코드 변경 후 테스트 재실행 필수, 이전 결과 재사용 금지를 Hard Rule로 추가
**Reason**: "should work"는 증거가 아님. 테스트 실행 출력을 근거로 제시해야 함

### Improvement: Regression Iron Rule
**Priority**: Medium
**Target Section**: `_sdd/spec/main.md` > `Component Details > implementation`
**Current State**: 기존 테스트 실패 시 처리 방안이 명시되지 않음
**Proposed**: 기존 테스트 실패 시 테스트 업데이트 + 회귀 방지 테스트 추가를 필수 단계로 강제. 사용자 확인 없이 자동
**Reason**: 회귀 방지를 자동화하여 기존 기능 안정성 보장

### Improvement: Audit Trail + Taste Decision in SDD Autopilot
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Component Details > sdd-autopilot`
**Current State**: Phase 2 자동 결정이 로그에 구조화되어 기록되지 않음
**Proposed**: Step 7.2 실행 루프에서 모든 자동 결정을 로그에 기록 (판단 근거 포함). Taste decision은 Step 8 최종 보고서에 표면화
**Reason**: 동적 생성 철학을 유지하면서도 투명성을 확보

## Failure Modes

| 시나리오 | 실패 시 | 사용자 가시성 | 처리 방안 |
|---------|---------|-------------|----------|
| Verification Gate가 테스트 환경 없는 프로젝트에 적용됨 | 테스트 재실행이 불가능해 gate 통과 불가 | 구현이 멈춤 | env.md 미존재 시 코드 분석 기반 fallback 허용, 리포트에 "UNTESTED" 명시 |
| Failure Modes 테이블이 모든 기능에 과도하게 상세 작성됨 | feature-draft 문서가 불필요하게 비대해짐 | 문서 가독성 저하 | "간단하면 N/A 또는 1-2행" 규칙으로 경량 유지 강제 |
| investigate의 독립 Agent 교차 검증이 동일 결론에 수렴 | 교차 검증의 가치가 없어짐 | 시간만 소모 | 3-strike 후 자동 에스컬레이션으로 다른 접근 시도 |
| PR review의 AUTO-FIX가 의도치 않은 코드 변경 발생 | 기능 동작이 변경됨 | PR에 원치 않는 커밋 추가 | AUTO-FIX 대상을 기계적 수정(import 정리, 타입 수정)으로 제한. 동작 변경 가능성은 목록 기록으로 분류 |

## Notes
- 모든 수정은 Conciseness 원칙 적용: "이 문장이 없으면 AI가 못 하는가?" 기준
- Self-contained 원칙: 외부 참조 최소화, 필요한 규칙을 파일 내에 명시
- AC-First 원칙: 새 기능은 AC 항목으로 추가
- 기존 AC/Hard Rules/Process 구조를 유지하면서 최소한의 추가
- Mirror Notice가 있는 스킬 파일(implementation, implementation-review, implementation-plan, feature-draft, spec-review)은 에이전트 파일과 함께 수정 필요
<!-- spec-update-todo-input-end -->

---

# Part 2: Implementation Plan

## Overview

gstack 패턴 토론에서 도출된 10개 결정 사항을 SDD Skills의 7개 기존 파일 + 2개 신규 파일에 반영한다. Verification Gate, Regression Iron Rule, Failure Modes, Test Coverage Mapping, Scope Drift Detection, Fix-First, Code Analysis Metrics, Audit Trail, investigate 스킬을 추가한다.

## Scope

### In Scope
- 7개 기존 에이전트/스킬 파일 수정 (+ 5개 Mirror Notice 스킬 파일 동기화)
- 2개 신규 파일 생성 (investigate 에이전트 + 래퍼 스킬)
- 10개 결정 사항 전체 반영

### Out of Scope
- Codex 에이전트/스킬 파일 (`.codex/`) -- 별도 태스크로 후속 처리
- `_sdd/spec/main.md` 직접 수정 -- `spec-update-todo`/`spec-update-done`으로 위임
- gstack 패턴 중 미채택 항목 (retro 스킬 등)

## Components

1. **Verification & Regression**: implementation, implementation-review에 Verification Gate + Regression Iron Rule 추가
2. **Feature Draft Enhancement**: feature-draft에 Failure Modes 테이블 추가
3. **Implementation Plan Enhancement**: implementation-plan에 Test Coverage Mapping 추가
4. **PR Review Enhancement**: pr-review에 Scope Drift Detection + Fix-First 추가
5. **Spec Review Enhancement**: spec-review에 코드 분석 지표 추가
6. **Autopilot Enhancement**: sdd-autopilot에 Audit Trail + Taste Decision 추가
7. **Investigate Skill**: 신규 에이전트 + 래퍼 스킬 생성

## Implementation Phases

### Phase 1: Core Safety Rules (Verification & Regression)
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 1 | implementation에 Verification Gate + Regression Iron Rule 추가 | P1-High | - | Verification & Regression |
| 2 | implementation-review에 Fresh Verification 규칙 추가 | P1-High | - | Verification & Regression |

### Phase 2: Existing Skill Enhancement (병렬 가능)
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 3 | feature-draft에 Failure Modes 테이블 섹션 추가 | P2-Medium | - | Feature Draft Enhancement |
| 4 | implementation-plan에 Test Coverage Mapping 추가 | P2-Medium | - | Implementation Plan Enhancement |
| 5 | pr-review에 Scope Drift Detection + Fix-First 추가 | P1-High | - | PR Review Enhancement |
| 6 | spec-review에 코드 분석 지표 추가 | P3-Low | - | Spec Review Enhancement |
| 7 | sdd-autopilot에 Audit Trail + Taste Decision 추가 | P1-High | - | Autopilot Enhancement |

### Phase 3: New Skill Creation
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 8 | investigate 에이전트 생성 | P3-Low | - | Investigate Skill |
| 9 | investigate 래퍼 스킬 생성 | P3-Low | 8 | Investigate Skill |

## Task Details

### Task 1: implementation에 Verification Gate + Regression Iron Rule 추가
**Component**: Verification & Regression
**Priority**: P1-High
**Type**: Improvement

**Description**: implementation 에이전트의 Hard Rules에 Verification Gate("should work" 금지, 코드 변경 후 테스트 재실행 필수, 이전 결과 재사용 금지)와 Regression Iron Rule(기존 테스트 실패 시 테스트 업데이트 + 회귀 방지 테스트 추가 필수, 사용자 확인 없이 자동)을 추가한다.

**Acceptance Criteria**:
- [ ] Hard Rules에 Verification Gate 규칙이 추가되었다
- [ ] Hard Rules에 Regression Iron Rule이 추가되었다
- [ ] Mirror Notice 스킬 파일도 동일하게 수정되었다

**Target Files**:
- [M] `.claude/agents/implementation.md` -- Hard Rules 섹션에 Verification Gate + Regression Iron Rule 추가
- [M] `.claude/skills/implementation/SKILL.md` -- Mirror Notice 동기화

**Technical Notes**: Hard Rules 섹션 마지막에 2개 규칙을 간결하게 추가. AC 섹션에는 기존 AC4 다음에 AC5 추가 불필요 -- Hard Rules로 충분.
**Dependencies**: -

### Task 2: implementation-review에 Fresh Verification 규칙 추가
**Component**: Verification & Regression
**Priority**: P1-High
**Type**: Improvement

**Description**: implementation-review 에이전트의 Hard Rules에 Fresh Verification 규칙을 추가한다. 코드를 읽고 "맞다"가 아니라 테스트 실행 출력을 근거로 판단해야 하며, "should work" 금지.

**Acceptance Criteria**:
- [ ] Hard Rules에 Fresh Verification 규칙이 추가되었다
- [ ] "should work" 금지가 명시되었다
- [ ] Mirror Notice 스킬 파일도 동일하게 수정되었다

**Target Files**:
- [M] `.claude/agents/implementation-review.md` -- Hard Rules 섹션에 Fresh Verification 추가
- [M] `.claude/skills/implementation-review/SKILL.md` -- Mirror Notice 동기화

**Technical Notes**: 기존 Hard Rule #6(env.md 우선) 뒤에 추가. 테스트 실행이 불가능한 경우(env.md 미존재)의 fallback도 명시.
**Dependencies**: -

### Task 3: feature-draft에 Failure Modes 테이블 섹션 추가
**Component**: Feature Draft Enhancement
**Priority**: P2-Medium
**Type**: Feature

**Description**: feature-draft 에이전트의 Part 1 스펙 패치 출력에 Failure Modes 테이블을 항상 포함하도록 추가한다. Step 4 템플릿과 Output Format에 섹션을 추가한다.

**Acceptance Criteria**:
- [ ] Step 4 Part 1 템플릿에 Failure Modes 섹션이 추가되었다
- [ ] 항상 포함, 간단하면 N/A 또는 1-2행 규칙이 명시되었다
- [ ] Mirror Notice 스킬 파일도 동일하게 수정되었다

**Target Files**:
- [M] `.claude/agents/feature-draft.md` -- Step 4 템플릿에 Failure Modes 섹션 추가
- [M] `.claude/skills/feature-draft/SKILL.md` -- Mirror Notice 동기화

**Technical Notes**: `## Notes` 바로 위에 `## Failure Modes` 섹션 추가. 4열 테이블 형식 (시나리오/실패 시/사용자 가시성/처리 방안). 간단한 기능은 "N/A -- 단순 기능, 실패 경로 없음" 1행으로 처리 가능.
**Dependencies**: -

### Task 4: implementation-plan에 Test Coverage Mapping 추가
**Component**: Implementation Plan Enhancement
**Priority**: P2-Medium
**Type**: Feature

**Description**: implementation-plan 에이전트의 Step 3 (Task Definition) 부분에 [M] 마커 대상 파일의 기존 테스트 커버리지를 매핑하는 단계를 추가한다. [C] 전용이면 스킵.

**Acceptance Criteria**:
- [ ] Step 3에 Test Coverage Mapping 하위 단계가 추가되었다
- [ ] [M] 마커 조건부 실행이 명시되었다
- [ ] Mirror Notice 스킬 파일도 동일하게 수정되었다

**Target Files**:
- [M] `.claude/agents/implementation-plan.md` -- Step 3에 Test Coverage Mapping 추가
- [M] `.claude/skills/implementation-plan/SKILL.md` -- Mirror Notice 동기화

**Technical Notes**: Step 3 "Target Files 검증" 바로 뒤에 "Test Coverage Mapping" 하위 섹션 추가. `Grep`으로 [M] 대상 파일명을 테스트 디렉토리에서 검색, 관련 테스트 파일/함수 목록을 Task의 Technical Notes에 기록.
**Dependencies**: -

### Task 5: pr-review에 Scope Drift Detection + Fix-First 추가
**Component**: PR Review Enhancement
**Priority**: P1-High
**Type**: Feature

**Description**: pr-review 스킬에 (a) Step 2.5 Scope Drift Detection pre-step과 (b) Step 5.5 코드 품질 Fix-First step을 추가한다.

**Acceptance Criteria**:
- [ ] Step 2.5 Scope Drift Detection이 Mode 1에 추가되었다
- [ ] CLEAN/DRIFT/MISSING 판정이 Output Format에 반영되었다
- [ ] Step 5.5 코드 품질 Fix-First가 추가되었다
- [ ] AUTO-FIX와 목록 기록의 분류 기준이 명시되었다

**Target Files**:
- [M] `.claude/skills/pr-review/SKILL.md` -- Step 2.5 + Step 5.5 추가, Output Format에 Scope Drift + Fix-First 섹션 추가

**Technical Notes**: Step 2.5는 `gh pr diff --name-only`와 patch draft의 Target Files를 비교. Step 5.5는 Step 5 Gap Analysis 직후에 배치. AUTO-FIX 대상: 미사용 import, 타입 불일치, 누락된 에러 처리 등 기계적 수정. 동작 변경 가능성이 있는 항목은 목록 기록으로 분류.
**Dependencies**: -

### Task 6: spec-review에 코드 분석 지표 추가
**Component**: Spec Review Enhancement
**Priority**: P3-Low
**Type**: Feature

**Description**: spec-review 에이전트의 Step 3(Code Drift 감사)에 핫스팟, Focus Score, Test Coverage 지표를 추가한다.

**Acceptance Criteria**:
- [ ] Step 3에 코드 분석 지표 수집 단계가 추가되었다
- [ ] 핫스팟, Focus Score, Test Coverage 세 가지 지표가 정의되었다
- [ ] Output Format에 지표 테이블이 추가되었다
- [ ] Mirror Notice 스킬 파일도 동일하게 수정되었다

**Target Files**:
- [M] `.claude/agents/spec-review.md` -- Step 3에 코드 분석 지표 추가, Output Format에 지표 테이블 추가
- [M] `.claude/skills/spec-review/SKILL.md` -- Mirror Notice 동기화

**Technical Notes**: 핫스팟은 `git log --format='' --name-only | sort | uniq -c | sort -rn | head -20`으로 측정. Focus Score는 변경 파일 중 스펙 컴포넌트에 속하는 비율. Test Coverage는 스펙 기능별 관련 테스트 파일/함수 존재 여부.
**Dependencies**: -

### Task 7: sdd-autopilot에 Audit Trail + Taste Decision 추가
**Component**: Autopilot Enhancement
**Priority**: P1-High
**Type**: Improvement

**Description**: sdd-autopilot 스킬의 Step 7.2 실행 루프에서 모든 자동 결정을 로그에 기록하고, Taste Decision은 Step 8 최종 보고서에 표면화한다.

**Acceptance Criteria**:
- [ ] Step 7.2에 자동 결정 로그 기록이 추가되었다
- [ ] Taste Decision 분류 기준이 명시되었다
- [ ] Step 8 보고서에 Taste Decisions 섹션이 추가되었다

**Target Files**:
- [M] `.claude/skills/sdd-autopilot/SKILL.md` -- Step 7.2에 Audit Trail 추가, Step 8에 Taste Decision 표면화 추가

**Technical Notes**: 자동 결정 로그 형식: `[DECISION] <what> -- <why> -- <taste: yes/no>`. Taste decision 정의: "합리적으로 다르게 판단할 수 있는 것" (예: 테스트 전략 선택, 병렬 vs 순차 결정, 에러 복구 방식). Step 8.2 보고서 필수 항목에 "Taste Decisions" 추가.
**Dependencies**: -

### Task 8: investigate 에이전트 생성
**Component**: Investigate Skill
**Priority**: P3-Low
**Type**: Feature

**Description**: 범용 체계적 디버깅 에이전트를 AC-First + Self-Contained 구조로 신규 생성한다. 근본원인 우선(Iron Law), 3-strike 에스컬레이션, scope lock, blast radius gate, fresh verification, 독립 Agent 교차 검증을 포함한다.

**Acceptance Criteria**:
- [ ] `.claude/agents/investigate.md`가 AC-First + Self-Contained 구조로 존재한다
- [ ] 근본원인 우선(Iron Law)이 Hard Rule로 명시되었다
- [ ] 3-strike 에스컬레이션이 Process에 포함되었다
- [ ] scope lock + blast radius gate가 포함되었다
- [ ] fresh verification이 포함되었다
- [ ] 독립 Agent 교차 검증이 포함되었다

**Target Files**:
- [C] `.claude/agents/investigate.md` -- 범용 체계적 디버깅 에이전트 정의

**Technical Notes**: tools에 Read, Write, Edit, Glob, Grep, Bash, Agent 포함. 독립 Agent 교차 검증은 Agent A(가설 기반 탐색)와 Agent B(코드만 독립 탐지)를 병렬 dispatch. ralph-loop-init과 차별화: investigate는 범용/단발, ralph-loop-init은 장시간 반복 프로세스 전용.
**Dependencies**: -

### Task 9: investigate 래퍼 스킬 생성
**Component**: Investigate Skill
**Priority**: P3-Low
**Type**: Feature

**Description**: investigate 에이전트의 래퍼 스킬을 Agent Wrapper 패턴에 따라 생성한다.

**Acceptance Criteria**:
- [ ] `.claude/skills/investigate/SKILL.md`가 래퍼 구조로 존재한다
- [ ] investigate 에이전트에 올바르게 위임한다

**Target Files**:
- [C] `.claude/skills/investigate/SKILL.md` -- investigate 에이전트의 래퍼 스킬

**Technical Notes**: 기존 래퍼 스킬 패턴(예: `.claude/skills/implementation-review/SKILL.md`)을 참고. skill.json 생성 불필요 -- frontmatter의 description으로 충분.
**Dependencies**: 8

## Parallel Execution Summary

| Phase | Total Tasks | Max Parallel | Sequential (conflicts) |
|-------|-------------|--------------|----------------------|
| 1 | 2 | 2 | None -- Task 1, 2는 Target Files 비중복 |
| 2 | 5 | 5 | None -- Task 3-7 모두 Target Files 비중복 |
| 3 | 2 | 1 | Task 9는 Task 8에 의존 |

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Mirror Notice 동기화 누락 | 에이전트와 스킬 파일 내용 불일치 | 각 Task AC에 Mirror Notice 동기화를 포함 |
| Verification Gate가 테스트 환경 없는 프로젝트에서 blocking | 구현 진행 불가 | fallback 규칙 명시 (env.md 미존재 시 코드 분석 기반) |
| investigate 스킬이 ralph-loop-init과 역할 혼동 | 사용자가 잘못된 스킬 선택 | description에 범용 단발 vs 장시간 반복 차이를 명확히 기술 |
| 추가된 규칙이 기존 스킬 구조의 conciseness를 해침 | 컨텍스트 효율 저하 | 모든 추가 내용에 "이 문장이 없으면 AI가 못 하는가?" 기준 적용 |

## Open Questions
- (없음 -- 토론에서 모든 논점에 결정이 이루어짐)

## Model Recommendation
- **구현**: Sonnet -- 마크다운 파일 수정은 패턴 매칭 위주로 Sonnet이 효율적
- **리뷰**: Opus -- 구조적 정합성 + conciseness 검증에 더 높은 추론 능력 필요

---

## Next Steps

### Apply Spec Patch
- **Method A (automatic)**: Run `spec-update-todo` -- Part 1을 입력으로 사용
- **Method B (manual)**: Part 1의 각 항목을 Target Section에 복사

### Execute Implementation
- **Parallel**: Run `implementation` skill -- Part 2를 계획으로 사용
- **Sequential**: Phase 1 (Task 1-2) -> Phase 2 (Task 3-7 병렬) -> Phase 3 (Task 8 -> 9 순차)
