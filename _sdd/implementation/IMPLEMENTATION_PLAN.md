# Implementation Plan: gstack Patterns for SDD Skills

## Overview

gstack 패턴 토론에서 도출된 10개 결정 사항을 9개 파일(기존 7 + 신규 2)에 반영한다. Verification Gate, Regression Iron Rule, Failure Modes, Test Coverage Mapping, Scope Drift Detection, Fix-First, Code Analysis Metrics, Audit Trail, investigate 스킬을 추가한다.

핵심 원칙: **Conciseness** -- 각 수정은 AC 항목 또는 Hard Rule 1-2줄 수준으로 최소화. "이 문장이 없으면 AI가 못 하는가?" 기준 적용.

## Scope

### In Scope
- 5개 에이전트 파일 수정 (feature-draft, implementation-plan, implementation, implementation-review, spec-review)
- 2개 스킬 파일 수정 (pr-review, sdd-autopilot)
- 2개 신규 파일 생성 (investigate 에이전트 + 래퍼 스킬)

### Out of Scope
- Mirror Notice 스킬 파일 동기화 (별도 후속 태스크)
- Codex 에이전트/스킬 파일 (`.codex/`)
- `_sdd/spec/main.md` 직접 수정 (`spec-update-todo`/`spec-update-done`으로 위임)
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

**전략**: Dependency-Driven -- 신규 파일(investigate)만 내부 의존성이 있고, 나머지 7개 수정은 모두 독립적. Phase 1에서 기존 파일 수정을 병렬 처리하고, Phase 2에서 신규 파일을 순차 생성한다.

### Phase 1: 기존 파일 수정 (전체 병렬)
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 1 | implementation에 Verification Gate + Regression Iron Rule 추가 | P1-High | - | Verification & Regression |
| 2 | implementation-review에 Fresh Verification 규칙 추가 | P1-High | - | Verification & Regression |
| 3 | feature-draft에 Failure Modes 테이블 섹션 추가 | P2-Medium | - | Feature Draft Enhancement |
| 4 | implementation-plan에 Test Coverage Mapping 추가 | P2-Medium | - | Implementation Plan Enhancement |
| 5 | pr-review에 Scope Drift Detection + Fix-First 추가 | P1-High | - | PR Review Enhancement |
| 6 | spec-review에 코드 분석 지표 추가 | P3-Low | - | Spec Review Enhancement |
| 7 | sdd-autopilot에 Audit Trail + Taste Decision 추가 | P1-High | - | Autopilot Enhancement |

### Phase 2: 신규 파일 생성 (순차)
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 8 | investigate 에이전트 생성 | P3-Low | - | Investigate Skill |
| 9 | investigate 래퍼 스킬 생성 | P3-Low | 8 | Investigate Skill |

## Task Details

### Task 1: implementation에 Verification Gate + Regression Iron Rule 추가
**Component**: Verification & Regression
**Priority**: P1-High
**Type**: Improvement

**Description**: implementation 에이전트의 Hard Rules에 Verification Gate와 Regression Iron Rule을 추가한다.

**Acceptance Criteria**:
- [ ] Hard Rules에 Verification Gate가 추가되었다 ("should work" 금지, 코드 변경 후 테스트 재실행 필수, 이전 결과 재사용 금지)
- [ ] Hard Rules에 Regression Iron Rule이 추가되었다 (기존 테스트 실패 시 테스트 업데이트 + 회귀 방지 테스트 추가 필수, 사용자 확인 없이 자동)
- [ ] env.md 미존재 시 코드 분석 기반 fallback이 명시되었다

**Target Files**:
- [M] `.claude/agents/implementation.md` -- Hard Rules 섹션에 Verification Gate + Regression Iron Rule 추가

**Technical Notes**: Hard Rules 섹션 마지막에 2개 규칙을 간결하게 추가. 각 규칙 1-2줄. env.md 미존재 시 fallback: 코드 분석 기반 허용, 리포트에 "UNTESTED" 명시.
**Dependencies**: -

---

### Task 2: implementation-review에 Fresh Verification 규칙 추가
**Component**: Verification & Regression
**Priority**: P1-High
**Type**: Improvement

**Description**: implementation-review 에이전트의 Hard Rules에 Fresh Verification 규칙을 추가한다.

**Acceptance Criteria**:
- [ ] Hard Rules에 Fresh Verification 규칙이 추가되었다 (테스트 실행 출력을 근거로 판단, "should work" 금지)
- [ ] 이전 결과 재사용 금지가 명시되었다
- [ ] env.md 미존재 시 fallback이 명시되었다

**Target Files**:
- [M] `.claude/agents/implementation-review.md` -- Hard Rules 섹션에 Fresh Verification 추가

**Technical Notes**: 기존 Hard Rule #7(계획 문서 수정 금지) 뒤에 #8로 추가. 1-2줄로 간결하게.
**Dependencies**: -

---

### Task 3: feature-draft에 Failure Modes 테이블 섹션 추가
**Component**: Feature Draft Enhancement
**Priority**: P2-Medium
**Type**: Feature

**Description**: feature-draft 에이전트의 Part 1 스펙 패치 출력 템플릿에 Failure Modes 테이블을 항상 포함하도록 추가한다.

**Acceptance Criteria**:
- [ ] Part 1 출력 템플릿(Step 4)에 Failure Modes 섹션이 추가되었다
- [ ] 항상 포함, 간단하면 N/A 또는 1-2행 규칙이 명시되었다
- [ ] 4열 테이블 형식이 정의되었다 (시나리오/실패 시/사용자 가시성/처리 방안)

**Target Files**:
- [M] `.claude/agents/feature-draft.md` -- Step 4 Part 1 템플릿에 Failure Modes 섹션 추가

**Technical Notes**: `## Notes` 바로 위에 `## Failure Modes` 섹션 추가. 간단한 기능은 "N/A -- 단순 기능, 실패 경로 없음" 1행으로 처리 가능.
**Dependencies**: -

---

### Task 4: implementation-plan에 Test Coverage Mapping 추가
**Component**: Implementation Plan Enhancement
**Priority**: P2-Medium
**Type**: Feature

**Description**: implementation-plan 에이전트의 Step 3에 [M] 마커 대상 파일의 기존 테스트 커버리지를 매핑하는 하위 단계를 추가한다.

**Acceptance Criteria**:
- [ ] Step 3에 Test Coverage Mapping 하위 단계가 추가되었다
- [ ] [M] 마커 조건부 실행이 명시되었다 ([C] 전용이면 스킵)
- [ ] Grep 기반 테스트 파일/함수 검색 방법이 기술되었다

**Target Files**:
- [M] `.claude/agents/implementation-plan.md` -- Step 3 "Target Files 검증" 뒤에 Test Coverage Mapping 추가

**Technical Notes**: `Grep`으로 [M] 대상 파일명을 테스트 디렉토리에서 검색, 관련 테스트 파일/함수 목록을 Task의 Technical Notes에 기록. 테스트 디렉토리 미존재 시 스킵.
**Dependencies**: -

---

### Task 5: pr-review에 Scope Drift Detection + Fix-First 추가
**Component**: PR Review Enhancement
**Priority**: P1-High
**Type**: Feature

**Description**: pr-review 스킬에 (a) Step 2.5 Scope Drift Detection과 (b) Step 5.5 코드 품질 Fix-First를 추가한다.

**Acceptance Criteria**:
- [ ] Mode 1에 Step 2.5 Scope Drift Detection이 추가되었다 (PR diff 변경 파일 vs patch draft Target Files 비교)
- [ ] CLEAN/DRIFT/MISSING 판정이 Output Format에 반영되었다
- [ ] Step 5.5 코드 품질 Fix-First가 추가되었다
- [ ] AUTO-FIX 대상(미사용 import, 타입 불일치, 누락된 에러 처리)과 목록 기록 대상(동작 변경 가능성)의 분류 기준이 명시되었다
- [ ] 기존 스펙 레이어 verdict(APPROVE/REQUEST CHANGES/NEEDS DISCUSSION)는 변경되지 않았다

**Target Files**:
- [M] `.claude/skills/pr-review/SKILL.md` -- Step 2.5 + Step 5.5 추가, Output Format에 Scope Drift + Fix-First 섹션 추가

**Technical Notes**: Step 2.5는 `gh pr diff --name-only`와 patch draft의 Target Files를 비교. Step 5.5는 Step 5 Gap Analysis 직후 배치. AUTO-FIX는 기계적 수정으로 제한, 동작 변경 가능성은 목록 기록으로 분류.
**Dependencies**: -

---

### Task 6: spec-review에 코드 분석 지표 추가
**Component**: Spec Review Enhancement
**Priority**: P3-Low
**Type**: Feature

**Description**: spec-review 에이전트의 Step 3(Code Drift 감사)에 핫스팟, Focus Score, Test Coverage 지표를 추가한다.

**Acceptance Criteria**:
- [ ] Step 3에 코드 분석 지표 수집 단계가 추가되었다
- [ ] 핫스팟(자주 변경 파일), Focus Score(변경 집중도), Test Coverage(스펙 기능별 테스트 현황) 세 가지 지표가 정의되었다
- [ ] Output Format에 Code Analysis Metrics 테이블이 추가되었다

**Target Files**:
- [M] `.claude/agents/spec-review.md` -- Step 3에 코드 분석 지표 추가, Output Format에 지표 테이블 추가

**Technical Notes**: 핫스팟: `git log --format='' --name-only | sort | uniq -c | sort -rn | head -20`. Focus Score: 변경 파일 중 스펙 컴포넌트에 속하는 비율. Test Coverage: 스펙 기능별 관련 테스트 파일 존재 여부.
**Dependencies**: -

---

### Task 7: sdd-autopilot에 Audit Trail + Taste Decision 추가
**Component**: Autopilot Enhancement
**Priority**: P1-High
**Type**: Improvement

**Description**: sdd-autopilot 스킬의 Step 7.2 실행 루프에 자동 결정 로그 기록을 추가하고, Taste Decision을 Step 8 최종 보고서에 표면화한다.

**Acceptance Criteria**:
- [ ] Step 7.2에 자동 결정 로그 기록이 추가되었다 (형식: `[DECISION] <what> -- <why> -- <taste: yes/no>`)
- [ ] Taste Decision 분류 기준이 명시되었다 ("합리적으로 다르게 판단할 수 있는 것")
- [ ] Step 8 보고서에 Taste Decisions 섹션이 추가되었다

**Target Files**:
- [M] `.claude/skills/sdd-autopilot/SKILL.md` -- Step 7.2에 Audit Trail 추가, Step 8에 Taste Decision 표면화 추가

**Technical Notes**: Taste decision 예시: 테스트 전략 선택, 병렬 vs 순차 결정, 에러 복구 방식. Step 8.2 보고서 필수 항목에 "Taste Decisions" 추가.
**Dependencies**: -

---

### Task 8: investigate 에이전트 생성
**Component**: Investigate Skill
**Priority**: P3-Low
**Type**: Feature

**Description**: 범용 체계적 디버깅 에이전트를 AC-First + Self-Contained 구조로 신규 생성한다.

**Acceptance Criteria**:
- [ ] `.claude/agents/investigate.md`가 AC-First + Self-Contained 구조로 존재한다
- [ ] 근본원인 우선(Iron Law)이 Hard Rule로 명시되었다 ("증상 패치 금지, 근본원인을 찾아 수정")
- [ ] 3-strike 에스컬레이션이 Process에 포함되었다 (같은 접근 3회 실패 시 전략 변경)
- [ ] scope lock이 포함되었다 (초기 범위를 벗어나는 수정 금지)
- [ ] blast radius gate가 포함되었다 (수정 영향 범위 사전 평가)
- [ ] fresh verification이 포함되었다 (수정 후 테스트 재실행 필수)
- [ ] 독립 Agent 교차 검증이 포함되었다 (Agent A 가설 기반 + Agent B 코드 독립 탐지)

**Target Files**:
- [C] `.claude/agents/investigate.md` -- 범용 체계적 디버깅 에이전트 정의

**Technical Notes**: tools: Read, Write, Edit, Glob, Grep, Bash, Agent. ralph-loop-init과 차별화: investigate는 범용/단발, ralph-loop-init은 장시간 반복 프로세스 전용. 기존 에이전트 패턴(frontmatter + AC + Hard Rules + Process + Final Check) 준수.
**Dependencies**: -

---

### Task 9: investigate 래퍼 스킬 생성
**Component**: Investigate Skill
**Priority**: P3-Low
**Type**: Feature

**Description**: investigate 에이전트의 래퍼 스킬을 Agent Wrapper 패턴에 따라 생성한다.

**Acceptance Criteria**:
- [ ] `.claude/skills/investigate/SKILL.md`가 래퍼 구조로 존재한다
- [ ] investigate 에이전트에 올바르게 위임한다 (`Agent(subagent_type="investigate")`)
- [ ] description에 범용 단발 디버깅 용도가 명시되었다 (ralph-loop-init과 차별화)

**Target Files**:
- [C] `.claude/skills/investigate/SKILL.md` -- investigate 에이전트의 래퍼 스킬

**Technical Notes**: 기존 래퍼 스킬 패턴(예: `.claude/skills/implementation-review/SKILL.md`) 참고. frontmatter의 description에 트리거 키워드 포함.
**Dependencies**: 8

---

## Parallel Execution Summary

| Phase | Total Tasks | Max Parallel | File Conflicts |
|-------|-------------|--------------|----------------|
| 1 | 7 | 7 | None -- Task 1-7 모두 Target Files 비중복 |
| 2 | 2 | 1 | Task 9는 Task 8에 의존 (래퍼가 에이전트 구조 참조) |

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Verification Gate가 테스트 환경 없는 프로젝트에서 blocking | 구현 진행 불가 | env.md 미존재 시 코드 분석 기반 fallback 명시, "UNTESTED" 표기 |
| investigate가 ralph-loop-init과 역할 혼동 | 사용자가 잘못된 스킬 선택 | description에 범용 단발 vs 장시간 반복 차이를 명확히 기술 |
| 추가된 규칙이 기존 스킬의 conciseness를 해침 | 컨텍스트 효율 저하 | 모든 추가 내용에 "이 문장이 없으면 AI가 못 하는가?" 기준 적용 |
| AUTO-FIX가 의도치 않은 코드 변경 발생 | PR에 원치 않는 커밋 추가 | AUTO-FIX 대상을 기계적 수정으로 제한, 동작 변경 가능성은 목록 기록으로 분류 |
| Mirror Notice 스킬 파일 미동기화 | 에이전트와 스킬 파일 내용 불일치 | Out of Scope로 명시, 별도 후속 태스크로 처리 |

## Open Questions

- (없음 -- gstack 토론에서 모든 논점에 결정이 이루어짐)

## Model Recommendation

- **구현**: `sonnet` -- 마크다운 파일 수정은 패턴 매칭 위주로 Sonnet이 효율적
- **리뷰**: `opus` -- 구조적 정합성 + conciseness 검증에 더 높은 추론 능력 필요
