# Feature Draft: Codex Implementation Review Loop

**Date**: 2026-04-01
**Author**: feature-draft
**Target Spec**: `_sdd/spec/main.md`
**Status**: Draft
**Discussion Reference**: `_sdd/discussion/discussion_implementation_review_loop.md`
**Implementation Review Reference**: `_sdd/implementation/IMPLEMENTATION_REVIEW.md`

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

### Background Update: Codex implementation review-fix loop 내장

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Background & Motivation`

**Current State**:
현재 Codex `implementation`은 Phase 실행과 검증까지는 수행하지만, 마지막 단계가 사실상 단일 패스 final report에 가깝다. `implementation-review`는 독립 스킬로 존재하나, `/implementation` 직접 호출 시 review-fix cycle이 자동으로 닫히지 않는다.

**Proposed**:
Codex `implementation`에 **Iteration Review Loop**를 도입한다. 모든 Phase 완료 후 Skeptical Evaluator 자세로 Plan의 각 Task별 Acceptance Criteria를 `MET / NOT_MET / UNTESTED`로 판정하고, `NOT_MET` AC 또는 `Critical / High` 이슈가 남아 있으면 관련 Task만 재실행한 뒤 다시 검증한다. 이 루프는 최대 5회 반복하며, 종료 후 별도 Report Step에서 최종 리포트를 저장한다.

**Reason**:
- `/implementation` 직접 호출에서도 review-fix cycle을 자체적으로 보장할 수 있다.
- sdd-autopilot의 review-fix 철학과 더 자연스럽게 정렬된다.
- 독립 `implementation-review` 스킬은 유지하면서, implementation 자체의 품질 closure를 강화할 수 있다.

## Design Changes

### Design Change: Iteration Review Loop 패턴의 Codex implementation 적용

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Core Design > Design Patterns`

**Description**:
Codex `implementation`에 **Iteration Review Loop**를 적용한다. Step 6(Phase Review)은 유지하고, 기존 Step 7의 단일 final report를 Step 7 iteration review loop + Step 8 report로 분리한다.

핵심 규칙:
- Skeptical Evaluator: 테스트 출력 또는 코드 분석 증거가 없으면 `NOT_MET`
- 종료 조건: 모든 AC가 `MET` 또는 `UNTESTED`이고 `Critical / High == 0`
- 재실행 범위: `NOT_MET AC 관련 Task ∪ Critical/High 이슈 관련 Task`
- 최대 반복: 5회

### Design Change: Codex implementation report에 Iteration History 추가

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Component Details > implementation`

**Description**:
Codex `implementation`의 최종 `IMPLEMENTATION_REPORT.md`에 `Iteration History` 섹션을 추가한다. 각 iteration별 AC 상태, `Critical / High` 개수, 재실행 대상 Task, 결과(`CONTINUE / PASS / TIMEOUT`)를 기록한다.

### Design Change: Codex implementation wording을 Claude review fixes 기준으로 보정

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Component Details > implementation`

**Description**:
Claude 첫 구현 리뷰에서 확인된 함정을 Codex 설계에 선반영한다.

- 종료 조건에 `UNTESTED` 처리 포함
- `"Plan AC"` 같은 모호한 표현 금지, `"Plan의 각 Task별 Acceptance Criteria"`로 명시
- Re-anchor 문구는 `"다시 읽는다"`가 아니라 `"재확인하고 준수한다"`로 서술
- Step 7.3에 `AC -> Task` 역추적 규칙을 명시
- 가능하면 재실행 worker prompt에 이전 실패 컨텍스트를 함께 전달

## Improvements

### Improvement: Codex implementation Step 7 전환

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Component Details > implementation`

**Current State**:
현재 Codex `implementation`은 Step 7이 `Final Report`에 머물러 있으며, review-fix loop가 내장되어 있지 않다.

**Proposed**:
Step 7을 `Iteration Review Loop`로 바꾸고, 기존 report 생성은 Step 8로 이동한다.

### Improvement: Codex implementation AC 강화

**Priority**: Medium
**Target Section**: `_sdd/spec/main.md` > `Component Details > implementation`

**Proposed**:
Codex `implementation`의 Acceptance Criteria에 아래를 추가 반영한다.

- iteration review loop 완료
- `IMPLEMENTATION_REPORT.md`에 iteration history 포함
- report 생성이 PASS/TIMEOUT 종료 상태를 드러냄

### Improvement: Mirror sync 유지

**Priority**: Medium
**Target Section**: `_sdd/spec/main.md` > `Core Design > Mirror 패턴`

**Proposed**:
이번 변경은 Codex `implementation` wrapper skill과 custom agent 모두에 동일하게 반영한다. Mirror drift를 허용하지 않는다.

## Failure Modes

| 시나리오 | 실패 시 | 사용자 가시성 | 처리 방안 |
|---------|---------|-------------|----------|
| `UNTESTED` 종료 조건 누락 | `_sdd/env.md` 없는 저장소에서 무조건 TIMEOUT | iteration이 끝나지 않거나 불필요한 실패 보고 | 종료 조건에 `MET 또는 UNTESTED`를 명시 |
| `"Plan AC"` 표현 모호 | implementation 자체 AC와 plan task AC 혼동 | 잘못된 검증 범위로 인해 오판정 | `"Plan의 각 Task별 Acceptance Criteria"`로 고정 |
| AC -> Task 역추적 규칙 누락 | 재실행 대상 선정이 추상적으로 남음 | 어떤 task를 다시 돌릴지 불명확 | Step 7.3에 역추적 문장을 명시 |
| 동일 Task 반복 재실행 | iteration 낭비, progress 정체 | 같은 task가 계속 재실행됨 | 2회 연속 동일 Task 재실행 시 반복 실패로 기록 |
| 재실행 worker에 실패 맥락이 없음 | 같은 실패를 반복 | 재실행 후에도 같은 결과가 반복됨 | worker prompt에 이전 실패 사유/근거를 추가 |

## Notes

- 이 변경은 Codex `implementation`에만 적용한다. `implementation-review` 스킬은 독립 스킬로 유지한다.
- Claude의 iteration review loop와 개념적으로 정렬하되, Codex의 현재 worker fan-out 구조를 그대로 재사용한다.
- sdd-autopilot의 review-fix 철학과 중복되는 부분이 있으나, 현재는 안전성 우선으로 중복을 허용한다.

## Open Questions

- [ ] 향후 sdd-autopilot이 Codex `implementation`의 iteration 결과를 읽고 추가 review-fix cycle을 생략할 수 있는가

<!-- spec-update-todo-input-end -->

---

# Part 2: Implementation Plan

## Overview

Codex `implementation`에 iteration review loop를 도입한다. 기존 Step 6(Phase Review)은 유지하고, 기존 Step 7(Final Report)을 Step 7(Iteration Review Loop) + Step 8(Report)로 분리한다. Claude 첫 구현 리뷰에서 확인된 함정(`UNTESTED`, 표현 모호성, AC->Task 역추적 누락)을 처음부터 반영하여 안정적으로 이식한다.

## Scope

### In Scope

- `.codex/skills/implementation/SKILL.md`에 iteration review loop 추가
- `.codex/agents/implementation.toml`에 동일 변경 동기화
- Codex implementation Acceptance Criteria 갱신
- Codex implementation report 형식에 `Iteration History` 추가
- 재실행 worker prompt contract에 실패 컨텍스트 전달 규칙 추가

### Out of Scope

- `.claude/` 하위 implementation 변경
- `implementation-review` 스킬/에이전트 변경
- `sdd-autopilot` 최적화
- `spec-update-done` 또는 `implementation-plan` 변경

## Components

1. **Iteration Review Loop**
   Step 7의 새로운 loop 본문. Skeptical Evaluator, 종료 판단, 재실행 대상 선정, TDD 재실행을 포함한다.
2. **Report Step**
   기존 final report를 Step 8로 분리하고 `Iteration History`를 추가한다.
3. **Mirror Sync**
   `.codex/skills/implementation/SKILL.md`와 `.codex/agents/implementation.toml` 본문을 동일하게 유지한다.
4. **Worker Retry Context**
   재실행 worker prompt에 이전 실패 사유/관련 AC/열린 이슈를 전달하는 규칙을 추가한다.

## Implementation Phases

### Phase 1: Iteration Loop 설계와 AC 반영

| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| T1 | Codex implementation AC를 iteration review loop 기준으로 갱신 | P1-High | - | Iteration Review Loop |
| T2 | Step 7을 Iteration Review Loop로 재작성 | P0-Critical | T1 | Iteration Review Loop |
| T3 | Step 8 Report 생성 로직 추가 및 Iteration History 형식 정의 | P1-High | T2 | Report Step |

### Phase 2: 실행 세부 규약과 Mirror 동기화

| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| T4 | 재실행 worker prompt contract에 실패 컨텍스트 전달 규칙 추가 | P2-Medium | T2 | Worker Retry Context |
| T5 | `.codex/agents/implementation.toml` Mirror 동기화 | P1-High | T1, T2, T3, T4 | Mirror Sync |

## Task Details

### Task T1: Codex implementation AC 갱신

**Component**: Iteration Review Loop  
**Priority**: P1-High  
**Type**: Refactor

**Description**:
현재 Codex `implementation`의 Acceptance Criteria는 병렬 실행과 리포트 생성까지만 설명한다. iteration review loop와 report history를 반영하도록 AC를 확장한다.

**Acceptance Criteria**:
- [ ] 기존 AC가 유지되면서 iteration review loop 완료 항목이 추가된다
- [ ] `IMPLEMENTATION_REPORT.md` 생성 항목이 명시된다
- [ ] `IMPLEMENTATION_REPORT.md`에 `Iteration History` 포함 항목이 추가된다

**Target Files**:
- [M] `.codex/skills/implementation/SKILL.md` -- Acceptance Criteria 섹션 수정

**Technical Notes**:
- Claude 최종 구현의 AC 방향을 참고하되, Codex 현재 용어에 맞게 자연스럽게 정리한다.
- `"Plan AC"` 같은 표현은 피하고, plan task AC와 skill AC를 구분한다.

**Dependencies**: -

---

### Task T2: Step 7 Iteration Review Loop 도입

**Component**: Iteration Review Loop  
**Priority**: P0-Critical  
**Type**: Refactor

**Description**:
현재 Step 7 `Final Report`를 제거하고, 그 자리에 Iteration Review Loop를 추가한다. 모든 Phase가 끝난 후 Skeptical Evaluator 자세로 Plan의 각 Task별 Acceptance Criteria를 판정하고, `NOT_MET` AC 또는 `Critical / High` 이슈가 남아 있으면 관련 Task만 재실행한다.

**Acceptance Criteria**:
- [ ] Step 7 제목이 `Iteration Review Loop`로 변경된다
- [ ] Re-anchor 블록이 포함되며 `"재확인하고 준수한다"` 표현을 사용한다
- [ ] Step 7.1에 `MET / NOT_MET / UNTESTED` 판정 기준이 명시된다
- [ ] Step 7.1에 `"Plan의 각 Task별 Acceptance Criteria"` 표현이 사용된다
- [ ] Step 7.2 종료 조건이 `모든 AC가 MET 또는 UNTESTED이고 Critical/High == 0`으로 정의된다
- [ ] Step 7.2에 `MAX_ITER = 5` TIMEOUT 경로가 정의된다
- [ ] Step 7.3에 `AC -> Task` 역추적 규칙이 명시된다
- [ ] Step 7.3에 반복 실패 감지 규칙이 포함된다
- [ ] Step 7.4가 기존 Step 4-5 실행 모델을 재사용하도록 명시된다

**Target Files**:
- [M] `.codex/skills/implementation/SKILL.md` -- Step 7 전면 재작성

**Technical Notes**:
- Claude 최종 구현의 Step 7 구조를 기준으로 삼되, Codex 현재 worker 용어를 유지한다.
- `UNTESTED`는 `_sdd/env.md` 부재나 실행 불가 상황에서만 허용한다.
- Phase Review의 품질 체크 카테고리를 Step 7.1의 cross-phase 검증에 재사용한다.

**Dependencies**: T1

---

### Task T3: Step 8 Report 추가와 Iteration History 정의

**Component**: Report Step  
**Priority**: P1-High  
**Type**: Refactor

**Description**:
기존 final report 저장 로직을 Step 8로 이동하고, 최종 `IMPLEMENTATION_REPORT.md` 형식에 `Iteration History` 섹션을 추가한다.

**Acceptance Criteria**:
- [ ] Step 8 `Report` 섹션이 추가된다
- [ ] 기존 report 저장 경로와 archive 규칙이 유지된다
- [ ] `Iteration History` 테이블 형식이 포함된다
- [ ] Conclusion에 `Iterations: N | Exit: PASS / TIMEOUT` 형식이 반영된다
- [ ] report 형식이 현재 Codex implementation 문서 톤과 호환된다

**Target Files**:
- [M] `.codex/skills/implementation/SKILL.md` -- Step 8 추가 및 report template 갱신

**Technical Notes**:
- 테이블 예시는 Claude 구현 형식을 참고하되, Codex 문맥에 맞게 `worker failures`, `parallel groups` 같은 필드를 유지한다.
- report는 iteration loop 종료 후 항상 생성된다. PASS와 TIMEOUT 모두 포함한다.

**Dependencies**: T2

---

### Task T4: 재실행 worker prompt에 실패 컨텍스트 전달 규칙 추가

**Component**: Worker Retry Context  
**Priority**: P2-Medium  
**Type**: Improvement

**Description**:
첫 구현 리뷰에서 낮은 우선순위로 남았던 “재실행 시 실패 컨텍스트 미전달”을 Codex 이식 때 선반영한다. Step 7.4에서 재실행 worker를 띄울 때 이전 iteration의 실패 사유, 관련 AC, 열린 Critical/High 이슈를 함께 넘기도록 prompt contract를 강화한다.

**Acceptance Criteria**:
- [ ] Worker Prompt Contract 또는 Step 7.4에 retry context 전달 규칙이 추가된다
- [ ] 최소 필드로 `failed_ac`, `failure_reason`, `open_issues`가 명시된다
- [ ] 동일 실패 반복 시 worker가 이전 시도를 인지하도록 문구가 포함된다

**Target Files**:
- [M] `.codex/skills/implementation/SKILL.md` -- Worker Prompt Contract 또는 Step 7.4 보강

**Technical Notes**:
- 필수 구현은 아니지만, Codex는 worker fan-out 재사용이 쉬워 체감 효과가 크다.
- 새 필드는 기존 worker result contract와 충돌하지 않도록 additive하게 설계한다.

**Dependencies**: T2

---

### Task T5: Codex implementation agent mirror 동기화

**Component**: Mirror Sync  
**Priority**: P1-High  
**Type**: Refactor

**Description**:
`.codex/skills/implementation/SKILL.md`에 반영된 Step 7/8, AC, worker prompt contract 변경을 `.codex/agents/implementation.toml`에 동일하게 반영한다.

**Acceptance Criteria**:
- [ ] `.codex/agents/implementation.toml`의 `developer_instructions`가 SKILL.md와 동일한 구조를 가진다
- [ ] Step 7 iteration review loop가 동일하게 반영된다
- [ ] Step 8 report 형식이 동일하게 반영된다
- [ ] AC와 Hard Rules 관련 wording drift가 없다

**Target Files**:
- [M] `.codex/agents/implementation.toml` -- mirror 동기화

**Technical Notes**:
- Mirror drift를 막기 위해 변경 후 두 파일을 diff 기준으로 함께 검토한다.
- TOML multiline string 안의 markdown 구조가 깨지지 않도록 formatting을 조심한다.

**Dependencies**: T1, T2, T3, T4

## Parallel Execution Summary

| Phase | Total Tasks | Max Parallel | Sequential (conflicts) |
|-------|-------------|--------------|------------------------|
| Phase 1 | 3 | 1 | T1, T2, T3 모두 `.codex/skills/implementation/SKILL.md`를 수정하므로 순차 실행 |
| Phase 2 | 2 | 1 | T4도 동일 파일을 수정하고, T5는 mirror sync 성격이라 순차 실행 |

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| `UNTESTED` 정책 누락 | `_sdd/env.md` 없는 저장소에서 loop가 무조건 TIMEOUT | Step 7.2 종료 조건에 `MET 또는 UNTESTED` 명시 |
| AC 범위 표현이 모호함 | 잘못된 검증 대상 판정 | Step 7.1에서 `"Plan의 각 Task별 Acceptance Criteria"`로 고정 |
| Step 7이 과도하게 길어짐 | 읽기 어려움, 유지보수성 저하 | Claude 최종 구조를 기준으로 compact하게 유지 |
| 반복 실패 감지가 약함 | 동일 Task 재실행 루프 | Step 7.3에 2회 연속 반복 실패 규칙 추가 |
| mirror sync 누락 | wrapper/agent drift | T5를 별도 task로 두고 diff 검증 |

## Open Questions

- [ ] 향후 Codex `implementation`의 iteration 결과를 `sdd-autopilot`이 읽어 추가 review-fix cycle을 줄일 수 있는가
- [ ] retry context를 worker prompt contract 본문에 넣을지, Step 7.4 전용 규칙으로 둘지 어느 쪽이 더 유지보수성이 좋은가

## Model Recommendation

- **T1-T3**: high reasoning 권장. Step 7/8 구조 변경과 wording 보정이 함께 필요하다.
- **T4-T5**: medium reasoning으로 충분. 기존 구조에 additive하게 붙이는 작업이다.

