# Feature Draft: Implementation Review Loop

**Date**: 2026-04-01
**Author**: hyunjoonlee
**Target Spec**: `_sdd/spec/main.md`
**Status**: Draft

---

<!-- spec-update-todo-input-start -->
# Part 1: Spec Patch Draft

> This patch can be copy-pasted into the corresponding spec section,
> or used as input for the `spec-update-todo` skill.

# Spec Update Input

**Date**: 2026-04-01
**Author**: hyunjoonlee
**Target Spec**: `_sdd/spec/main.md`

## Background & Motivation Updates

### Background Update: Implementation Iteration Review Loop 도입 배경

**Target Section**: `_sdd/spec/main.md` > `Background & Motivation`

**Proposed**:

implementation 스킬의 기존 Step 7(Final Review)은 단일 패스 리뷰로, 이슈를 발견해도 체계적인 수정-재검증 루프가 없었다. sdd-autopilot에서는 Hard Rule #9(Review-Fix 사이클 필수)로 이를 보완하지만, `/implementation` 직접 호출 시에는 리뷰 후 수정이 사용자 수동 개입에 의존했다.

v3.11에서 implementation 스킬 내부에 **Iteration Review Loop**를 도입하여, TDD 구현 완료 후 Skeptical Evaluator 자세로 AC를 엄격 검증하고, 미충족 항목을 자동으로 TDD 재실행하는 루프를 내장한다. 이를 통해:
- `/implementation` 직접 호출에서도 review-fix 사이클이 자동 적용
- sdd-autopilot 의존 없이 단독으로 품질 보장 가능
- 최대 5회 iteration으로 무한 루프 방지

## Design Changes

### Design Change: Iteration Review Loop 패턴 추가

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Core Design > Design Patterns`

**Description**:

**Iteration Review Loop 패턴**: implementation 스킬의 Step 7에서 사용한다. 전체 Phase 실행 완료 후, Skeptical Evaluator 자세로 모든 Acceptance Criteria를 검증(MET/NOT_MET/UNTESTED)하고, 미충족 AC 또는 Critical/High 이슈가 있으면 해당 Task만 TDD로 재실행한 뒤 다시 검증하는 루프를 반복한다.

```
Step 7: Iteration Review Loop
  iteration = 1, MAX_ITER = 5

  WHILE iteration ≤ MAX_ITER:
    7.1 Skeptical AC 검증
        - 모든 AC에 대해 MET/NOT_MET/UNTESTED 판정
        - Skeptical Evaluator: 증거(테스트 출력) 없으면 NOT_MET
        - Critical/High 이슈 식별

    7.2 종료 판단
        IF 모든 AC == MET AND Critical/High == 0:
          → PASS: Step 8(Report)로 진행
        IF iteration == MAX_ITER:
          → TIMEOUT: 미해결 목록 + 보고서 생성 → 사용자 위임

    7.3 수정 대상 선정
        - NOT_MET AC 관련 Task 목록
        - Critical/High 이슈 관련 Task 목록
        - 합집합 → 재실행 대상

    7.4 TDD 재실행
        - 대상 Task만 Step 4-5와 동일 방식으로 실행
        - iteration += 1
        → 7.1로 복귀
```

핵심 원리:
- **Skeptical Evaluator 자세**: "구현했으니 맞을 것이다"가 아니라, 테스트 실행 출력이나 코드 분석 증거가 없으면 NOT_MET으로 판정한다.
- **선택적 재실행**: 전체가 아닌 미충족 AC + Critical/High 관련 Task만 재실행하여 효율성을 유지한다.
- **유한 루프**: MAX_ITER = 5로 제한하여 무한 루프를 방지하고, 초과 시 사용자에게 위임한다.

### Design Change: implementation Step 7 변경

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Component Details > implementation`

**Description**:

implementation 스킬의 Step 7 "Final Review & Report"를 "Iteration Review Loop"로 전환한다. 기존 Step 7의 단일 패스 리뷰 + 리포트 생성을 Iteration Review Loop + 별도 Report Step(Step 8)으로 분리한다.

기존:
- Step 7: Final Review & Report (단일 패스 리뷰 + IMPLEMENTATION_REPORT.md 생성)

변경:
- Step 7: Iteration Review Loop (Skeptical AC 검증 → TDD 재실행 → 재검증, 최대 5회)
- Step 8: Report (IMPLEMENTATION_REPORT.md 생성, iteration 이력 포함)

## Improvements

### Improvement: implementation Step 7 → Iteration Review Loop 전환

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Component Details > implementation`

**Current State**: Step 7은 단일 패스 Final Review. 이슈 발견 시 Critical만 TDD 수정하고, 나머지는 문서화 후 종료. review-fix 반복 루프 없음.

**Proposed**: Step 7을 Iteration Review Loop로 대체. Skeptical Evaluator 자세로 모든 AC를 MET/NOT_MET/UNTESTED로 판정하고, NOT_MET AC + Critical/High 이슈가 있으면 해당 Task만 TDD 재실행. 모든 AC MET + Critical/High 0건이 될 때까지 최대 5회 반복. Step 8로 Report 생성을 분리.

**Reason**: sdd-autopilot 없이도 `/implementation` 단독으로 review-fix 사이클 보장. 기존 sdd-autopilot Hard Rule #9의 정신을 implementation 스킬 내부에 내장.

### Improvement: IMPLEMENTATION_REPORT.md에 Iteration History 섹션 추가

**Priority**: Medium
**Target Section**: `_sdd/spec/main.md` > `Component Details > implementation`

**Current State**: IMPLEMENTATION_REPORT.md에 iteration 이력 없음. 단일 패스 결과만 기록.

**Proposed**: IMPLEMENTATION_REPORT.md에 `### Iteration History` 섹션 추가. 각 iteration의 AC 상태, 발견 이슈, 재실행 Task, 결과를 테이블로 기록.

**Reason**: iteration 루프의 진행 과정과 최종 상태를 추적 가능하게 함.

## Failure Modes

| 시나리오 | 실패 시 | 사용자 가시성 | 처리 방안 |
|---------|---------|-------------|----------|
| 5회 iteration 후에도 AC 미충족 | 구현 품질 미달 상태로 종료 | 미해결 AC/이슈 목록이 보고서에 명시 | 보고서 생성 + 사용자에게 수동 개입 위임 |
| Skeptical 검증이 지나치게 엄격 | 정상 구현도 NOT_MET 판정 → 불필요한 재실행 | iteration 횟수 증가, 동일 Task 반복 재실행 관찰 | 2회 연속 동일 Task 재실행 시 경고 + 사용자 확인 |
| 재실행된 Task가 다른 Task에 영향 | 이전에 통과한 AC가 NOT_MET으로 전환 | regression 패턴 관찰 | Regression Iron Rule 적용 (기존 테스트 실패 시 자동 수정) |
| 리뷰 단계에서 컨텍스트 과부하 | AC 검증 품질 저하 | 누락된 이슈, 부정확한 판정 | AC 상태를 외부 파일에 추적하여 컨텍스트 lean 유지 |

## Notes

- implementation-review 스킬은 독립적으로 유지한다. 이 변경은 implementation 내부의 review 능력 강화이며, 별도 리뷰가 필요한 경우(PR 전 감사, 수동 검증) impl-review를 독립 호출할 수 있다.
- sdd-autopilot의 Hard Rule #9(Review-Fix 사이클 필수)와 호환된다. autopilot이 implementation을 호출하면 내부 iteration loop가 이미 review-fix를 수행하므로, autopilot 수준의 추가 review-fix가 중복될 수 있다. 향후 autopilot이 implementation의 iteration 결과를 확인하고 추가 사이클을 스킵하는 최적화를 고려할 수 있다.
- 기존 feature draft (implementation_inline_orchestration)와는 독립적인 변경이다. 두 변경을 동시 적용할 수 있으나, 순서는 사용자 판단에 따른다.

<!-- spec-update-todo-input-end -->

---

# Part 2: Implementation Plan

## Overview

implementation 스킬의 Step 7(Final Review & Report)을 Iteration Review Loop로 대체한다. Skeptical Evaluator 자세의 AC 검증 → 선택적 TDD 재실행 → 재검증 루프를 최대 5회 반복하여 구현 품질을 자체 보장한다.

## Scope

### In Scope
- implementation SKILL.md의 Step 7 재작성 (Iteration Review Loop)
- implementation SKILL.md에 Step 8 추가 (Report 생성, 기존 Step 7의 리포트 부분 분리)
- IMPLEMENTATION_REPORT.md 형식에 Iteration History 섹션 추가
- implementation agent.md에 동일 변경 반영 (Mirror 동기화)
- implementation SKILL.md AC 업데이트 (새 AC 반영)

### Out of Scope
- implementation-review 스킬/에이전트 변경 (독립 유지)
- sdd-autopilot 변경 (기존 동작 유지)
- feature_draft_implementation_inline_orchestration과의 통합 (별도 작업)
- Codex 측 변경 (`.codex/` 하위)

## Components

1. **Iteration Review Loop**: Step 7의 새로운 루프 로직 (Skeptical AC 검증 → 수정 대상 선정 → TDD 재실행)
2. **Report Step**: Step 8로 분리된 IMPLEMENTATION_REPORT.md 생성 로직 (Iteration History 포함)
3. **Mirror Sync**: implementation agent.md에 SKILL.md 변경 반영

## Implementation Phases

### Phase 1: implementation SKILL.md 재작성

| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| T1 | Step 7을 Iteration Review Loop로 재작성 | P0-Critical | - | Iteration Review Loop |
| T2 | Step 8 Report 생성 로직 추가 (기존 Step 7 리포트 부분 분리 + Iteration History) | P1-High | T1 | Report Step |
| T3 | AC 섹션 업데이트 (AC3 변경: iteration review loop 완료, AC5 추가: iteration history 포함) | P1-High | T1 | Iteration Review Loop |

### Phase 2: Mirror 동기화

| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| T4 | implementation agent.md에 SKILL.md 변경사항 동기화 | P1-High | T1, T2, T3 | Mirror Sync |

## Task Details

### Task T1: Step 7을 Iteration Review Loop로 재작성

**Component**: Iteration Review Loop
**Priority**: P0-Critical
**Type**: Refactor

**Description**: `.claude/skills/implementation/SKILL.md`의 Step 7 "Final Review & Report" 섹션을 Iteration Review Loop로 전면 재작성한다. 기존 Step 7의 cross-phase 통합 검증과 critical 이슈 TDD 수정 로직을 포함하되, Skeptical Evaluator 자세의 AC 검증 + 선택적 재실행 + 종료 조건 루프로 확장한다.

**Acceptance Criteria**:
- [ ] Step 7 제목이 "Iteration Review Loop"로 변경됨
- [ ] Step 7.1: Skeptical Evaluator 자세로 모든 AC에 대해 MET/NOT_MET/UNTESTED 판정 로직 포함
- [ ] Step 7.1: Critical/High 이슈 식별 로직 포함 (기존 Phase Review의 Quality Check 카테고리 재활용)
- [ ] Step 7.2: 종료 조건 — 모든 AC MET + Critical/High 0건 → Step 8 진행
- [ ] Step 7.2: 최대 iteration 5회 초과 시 미해결 목록 + 보고서 생성 → 사용자 위임
- [ ] Step 7.3: NOT_MET AC 관련 Task + Critical/High 이슈 관련 Task 합집합으로 재실행 대상 선정
- [ ] Step 7.4: 대상 Task만 Step 4-5와 동일 방식(TDD sub-agent dispatch)으로 재실행
- [ ] Skeptical Evaluator 정의: "테스트 실행 출력 또는 코드 분석 증거가 없으면 NOT_MET" 명시
- [ ] iteration 카운터와 MAX_ITER = 5 상수 명시
- [ ] 2회 연속 동일 Task 재실행 시 경고 로직 포함

**Target Files**:
- [M] `.claude/skills/implementation/SKILL.md` -- Step 7 섹션 재작성

**Technical Notes**:
- 기존 Step 7의 cross-phase 통합 검증(모듈 간 연동, 보안 경계, 전체 규모 성능)은 Step 7.1의 리뷰 범위에 포함한다.
- Skeptical Evaluator는 implementation-review의 Skeptical posture를 차용하되, 전체 Tier 시스템은 가져오지 않는다. Plan 기반(Tier 1) AC 검증만 수행.
- 재실행 시 Step 3의 병렬 그룹 재계산이 필요할 수 있다 (재실행 대상 Task들 간 충돌 분석).

**Dependencies**: -

---

### Task T2: Step 8 Report 생성 로직 추가

**Component**: Report Step
**Priority**: P1-High
**Type**: Refactor

**Description**: 기존 Step 7의 IMPLEMENTATION_REPORT.md 생성 로직을 Step 8로 분리하고, Iteration History 섹션을 추가한다.

**Acceptance Criteria**:
- [ ] Step 8 "Report" 섹션이 추가됨
- [ ] 기존 IMPLEMENTATION_REPORT.md 형식 유지 (Progress Summary, Parallel Execution Stats, Completed Tasks, Quality Assessment, Cross-Phase Review, Issues Found, Recommendations, Conclusion)
- [ ] `### Iteration History` 섹션 추가: iteration 번호, AC 상태 변화, 발견 이슈 수, 재실행 Task 목록, 결과 포함
- [ ] Conclusion에 iteration 횟수와 최종 종료 조건(PASS/TIMEOUT) 반영
- [ ] 기존 아카이브 로직 유지 (prev/PREV_IMPLEMENTATION_REPORT_<timestamp>.md)

**Target Files**:
- [M] `.claude/skills/implementation/SKILL.md` -- Step 8 섹션 추가 + IMPLEMENTATION_REPORT.md 형식 업데이트

**Technical Notes**:
- Step 8은 Step 7의 iteration 루프가 종료된 후(PASS 또는 TIMEOUT) 실행된다.
- Iteration History 테이블 형식:
  ```
  | Iteration | AC Status (MET/Total) | Critical | High | Re-executed Tasks | Result |
  |-----------|----------------------|----------|------|-------------------|--------|
  | 1         | 8/12                 | 1        | 2    | T3, T5, T7       | CONTINUE |
  | 2         | 11/12                | 0        | 1    | T7               | CONTINUE |
  | 3         | 12/12                | 0        | 0    | -                | PASS    |
  ```

**Dependencies**: T1

---

### Task T3: AC 섹션 업데이트

**Component**: Iteration Review Loop
**Priority**: P1-High
**Type**: Refactor

**Description**: implementation SKILL.md의 Acceptance Criteria 섹션을 업데이트하여 새로운 iteration review loop를 반영한다.

**Acceptance Criteria**:
- [ ] AC3 변경: "Phase별 실행 → 검증 → 리뷰 사이클 완료" → "Phase별 실행 → 검증 → Phase Review → Iteration Review Loop 완료"
- [ ] AC5 추가: "IMPLEMENTATION_REPORT.md에 Iteration History 포함"
- [ ] 기존 AC1, AC2, AC4 유지

**Target Files**:
- [M] `.claude/skills/implementation/SKILL.md` -- AC 섹션 수정

**Technical Notes**: AC3의 변경은 Step 7의 역할 변화를 반영한다.

**Dependencies**: T1

---

### Task T4: implementation agent.md Mirror 동기화

**Component**: Mirror Sync
**Priority**: P1-High
**Type**: Refactor

**Description**: `.claude/agents/implementation.md`에 SKILL.md의 변경사항(Step 7 → Iteration Review Loop, Step 8 추가, AC 업데이트)을 동기화한다.

**Acceptance Criteria**:
- [ ] agent.md의 Step 7이 SKILL.md와 동일한 Iteration Review Loop로 변경됨
- [ ] agent.md에 Step 8 Report가 추가됨
- [ ] agent.md의 AC 섹션이 SKILL.md와 동일하게 업데이트됨
- [ ] agent.md와 SKILL.md 간 내용 불일치 없음

**Target Files**:
- [M] `.claude/agents/implementation.md` -- SKILL.md Mirror 동기화

**Technical Notes**: Mirror 패턴에 따라 agent.md는 SKILL.md의 완전 복사본이어야 한다 (Mirror Notice 포함).

**Dependencies**: T1, T2, T3

## Parallel Execution Summary

| Phase | Total Tasks | Max Parallel | Sequential (conflicts) |
|-------|-------------|--------------|----------------------|
| Phase 1 | 3 (T1, T2, T3) | 1 | T2→T1 의존, T3→T1 의존. T2와 T3는 T1 완료 후 병렬 가능 (같은 파일이지만 다른 섹션) |
| Phase 2 | 1 (T4) | 1 | - |

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Skeptical Evaluator가 지나치게 엄격하여 불필요한 iteration 발생 | 실행 시간 증가, 사용자 경험 저하 | 2회 연속 동일 Task 재실행 시 경고 로직으로 조기 탈출 |
| 재실행된 Task가 다른 Task의 결과에 영향 (regression) | 이전 AC가 NOT_MET으로 전환 | 기존 Regression Iron Rule 적용, 전체 테스트 재실행으로 검증 |
| 5회 iteration 내 해결 불가능한 구조적 문제 | 사용자에게 위임되나 해결 방향 불명확 | 미해결 이슈 목록에 root cause 분석과 권고 사항 포함 |
| SKILL.md 파일 크기 증가로 인한 컨텍스트 부담 | 스킬 실행 품질 저하 | Step 7/8의 기술이 기존 Step 7 대비 크게 늘지 않도록 간결하게 작성 |
| sdd-autopilot과의 중복 review-fix | 불필요한 이중 리뷰 | Notes에 향후 최적화 방향 기록. 현재는 중복 허용 (안전 > 효율) |

## Open Questions

- [ ] sdd-autopilot이 implementation을 호출할 때, 내부 iteration loop의 결과를 활용하여 autopilot 수준의 review-fix 사이클을 스킵할 수 있는가? (향후 최적화 대상)
- [ ] Skeptical Evaluator의 "증거" 기준을 어디까지 엄격하게 적용할 것인가? (테스트 출력 필수 vs 코드 분석도 허용)

## Model Recommendation

- **Phase 1 (T1)**: Opus 필수. Step 7 전면 재작성은 기존 로직과의 정합성, Skeptical Evaluator 설계, 루프 종료 조건 등 복합적 판단 필요.
- **Phase 1 (T2, T3)**: Sonnet으로 충분. T1 완료 후 명확한 패턴에 따른 추가/수정.
- **Phase 2 (T4)**: Sonnet으로 충분. Mirror 복사.

---

## Next Steps

### Apply Spec Patch
- **Method A (automatic)**: Run `spec-update-todo` → Part 1을 입력으로 사용
- **Method B (manual)**: Part 1의 각 항목을 Target Section에 복사

### Execute Implementation
- **Parallel**: Run `implementation` skill → Part 2를 계획으로 사용
- **Sequential**: Phase 순서대로 태스크를 순차 실행
