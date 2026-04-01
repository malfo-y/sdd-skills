---
name: implementation
description: Use this skill when the user wants to execute an implementation plan, start implementing tasks from a plan, work through a development roadmap, says "implement the plan", "start implementation", "execute the plan", "work on the tasks", or explicitly asks for "implement parallel", "parallel implementation", "병렬 구현", "병렬로 구현". Uses conflict-aware parallel execution when Target Files are available.
version: 2.1.1
---

# Implementation Execution (Parallel TDD)

| Workflow | Position | When |
|----------|----------|------|
| Large | Step 3 of 6 | implementation plan 실행 |
| Medium | Step 3 of 3 | 구현 단계 |
| Small | Direct | 단일 변경 구현 |

이 agent는 implementation plan 또는 feature draft의 Part 2를 실행해 코드 변경과 `_sdd/implementation/` 진행 아티팩트를 만든다. Phase별 실행과 검증 뒤에는 iteration review loop를 수행해 review-fix cycle을 자체적으로 닫는다.

## Acceptance Criteria

> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] plan을 읽고 실행 가능한 task 단위로 파싱한다.
- [ ] `_sdd/implementation/IMPLEMENTATION_PROGRESS.md`를 갱신한다.
- [ ] Target Files 기반 병렬/순차 실행 판단이 가능하다.
- [ ] Phase별 실행 → 검증 → Phase Review → Iteration Review Loop가 완료된다.
- [ ] `_sdd/implementation/IMPLEMENTATION_REPORT.md`를 생성한다.
- [ ] `IMPLEMENTATION_REPORT.md`에 Iteration History와 필요한 `UNTESTED` 근거가 포함된다.

## Hard Rules

1. `_sdd/spec/` 아래 파일은 생성/수정/삭제하지 않는다.
2. TDD를 기본 원칙으로 사용한다. 최소한 RED → GREEN → REFACTOR 의도를 유지한다.
3. task는 `Target Files` 경계 밖을 수정하지 않는다. 추가 수정이 필요하면 `UNPLANNED_DEPENDENCY`로 보고한다.
4. 각 phase/group 이후에는 검증을 수행한다.
5. Critical 이슈가 남아 있으면 그대로 종료하지 않는다.
6. **Verification Gate**: "should work" 금지. 코드 변경 후 반드시 테스트를 재실행하고 출력을 근거로 제시한다. 이전 실행 결과 재사용 금지. `_sdd/env.md` 미존재 시 코드 분석 기반 검증을 허용하되, 리포트에 `UNTESTED` 표기.
7. **Regression Iron Rule**: 기존 테스트 실패 시 (1) 테스트 업데이트 + (2) 회귀 방지 테스트 추가를 사용자 확인 없이 자동 수행한다.

## Target Files and Conflicts

```markdown
**Target Files**:
- [C] `...`
- [M] `...`
- [D] `...`
```

충돌 규칙:
- 동일 파일을 만지는 task는 기본적으로 충돌이다.
- 파일이 달라도 다음 5가지 패턴이면 의미적 충돌:
  1. Task A가 생성하는 모델/타입을 Task B가 import
  2. 두 태스크 모두 DB 마이그레이션 생성
  3. 두 태스크가 동일 config/env 값을 가정
  4. Task A가 정의하는 API contract를 Task B가 소비
  5. 두 태스크가 같은 상수/타입을 다른 값으로 가정
- 확신이 낮으면 병렬보다 순차 실행이 우선이다.

## Input Sources

우선순위:
1. 사용자 지정 경로
2. `_sdd/implementation/IMPLEMENTATION_PLAN.md`
3. `_sdd/implementation/IMPLEMENTATION_PLAN_PHASE_<N>.md`
4. `_sdd/drafts/feature_draft_<name>.md`의 Part 2

## Process

### Step 1: Load the Plan

plan에서 다음을 추출한다.
- phases
- tasks
- target files
- dependencies
- acceptance criteria
- technical notes

plan이 없으면 `implementation-plan` 또는 `feature-draft` 후속 사용을 안내한다.

### Step 2: Initialize Task Tracking

`_sdd/implementation/IMPLEMENTATION_PROGRESS.md`에 tracking row를 만든다.

기본 필드:
- task_id
- title
- phase
- dependencies
- status
- owner/sub-agent
- notes

초기 상태:
- dependency가 있으면 `BLOCKED`
- 없으면 `READY`

### Step 3: Analyze Parallelization

Target Files와 dependency를 기준으로 병렬 그룹을 만든다.

- 모든 task에 target files가 있으면 전체 병렬 분석
- 일부만 있으면 있는 task만 병렬 분석
- target files가 없거나 불명확하면 순차 fallback

병렬 그룹을 만들 때:
- 파일 겹침 없는 task 우선
- shared contract 충돌 없는 task만 같은 group
- 큰 phase는 group 크기를 작게 유지

### Step 4: Execute Tasks

각 phase마다 다음 순서로 진행한다.

1. unblocked task를 찾는다
2. 병렬 그룹 또는 순차 순서를 만든다
3. task를 실행한다
4. 결과를 progress artifact에 반영한다

병렬 실행 시 worker 규칙:
- 한 worker는 하나의 task를 담당한다
- worker는 할당된 Target Files만 수정한다
- sibling worker의 변경을 되돌리지 않는다
- 실패한 task만 재시도한다

### Step 5: Verify After Each Group

각 group 또는 순차 task 이후 아래를 수행한다.
- 관련 테스트 실행
- 새 코드와 기존 코드의 통합 확인
- `UNPLANNED_DEPENDENCY` 처리 여부 판단
- 실패/부분 완료 상태 기록

검증 상태 예시:
- SUCCESS
- PARTIAL
- FAILED

### Step 6: Phase Review

phase 종료 후 경량 리뷰를 수행한다.
- security
- error handling
- code patterns
- performance
- test quality
- integration consistency

Critical 이슈가 있으면 수정 후 다시 검증한다.

phase 리포트는 필요 시 `_sdd/implementation/IMPLEMENTATION_REPORT_PHASE_<N>.md`로 저장한다.

### Step 7: Iteration Review Loop

모든 phase 완료 후, Skeptical Evaluator 자세로 Plan의 각 Task별 Acceptance Criteria를 검증하고 미충족 항목을 재실행하는 루프를 수행한다.

최대 5회 iteration을 반복한다. 매 iteration 시작 시 Re-anchor 블록을 재확인하고 7.1(AC 검증) → 7.2(종료 판단)를 수행한다. 종료 조건을 충족하면 Step 8로 진행하고, 미충족이면 7.3(수정 대상 선정) → 7.4(TDD 재실행) 후 다음 iteration으로 돌아간다.

#### Re-anchor (매 iteration 시작 시 재확인)

> **매 iteration 시작 전에 아래 원칙을 재확인하고 준수한다.**
>
> 1. **Skeptical Evaluator**: 테스트 출력이나 `UNTESTED` 판정을 뒷받침할 코드 분석 근거가 없으면 `NOT_MET`이다. "이전에 봤으니 MET"라고 판단하지 않는다.
> 2. **종료 조건**: 모든 AC가 `MET`이거나, `UNTESTED`인 경우에도 코드 분석 근거와 사유가 명시되어 있고 `Critical/High == 0`일 때만 PASS다.
> 3. **MAX_ITER**: iteration은 최대 5회까지만 반복한다. 초과 시 TIMEOUT으로 종료한다.
> 4. **반복 감지**: 2회 연속 동일 task가 재실행 대상이면 `반복 실패`로 기록하고 스킵한다.
> 5. **Spec 불가침**: `_sdd/spec/` 아래 파일은 수정하지 않는다.

#### 7.1 Skeptical AC 검증

Plan의 각 Task별 Acceptance Criteria에 대해 아래 기준으로 판정한다.

| 판정 | 기준 |
|------|------|
| MET | 테스트 통과 출력으로 충족 확인 |
| NOT_MET | 증거 부족, 테스트 실패, 구현 누락, 또는 `UNTESTED` 판정을 뒷받침할 코드 분석 근거 부족 |
| UNTESTED | `_sdd/env.md` 미존재 또는 환경 제약으로 테스트 실행이 불가하지만, 코드 분석으로 구현 충족을 설명할 수 있고 그 사유를 리포트에 기록함 |

동시에 cross-phase 통합 검증을 수행한다.
- 모듈 간 연동
- 보안 경계
- 전체 규모 성능
- Step 6 품질 체크 카테고리(Security, Error Handling, Code Patterns, Performance, Test Quality, Integration) 재적용

이슈 분류:
- **Critical**: 핵심 기능 누락, 실패 테스트, 보안 취약점, 데이터 손실 위험
- **High**: AC 일부 불충족, 주요 에러 처리 갭, 중요 통합 깨짐

#### 7.2 종료 판단

| 조건 | 결과 |
|------|------|
| 모든 AC가 `MET`이거나, `UNTESTED`인 항목마다 코드 분석 근거와 사유가 기록되어 있고 `Critical/High == 0` | **PASS** → Step 8 진행 |
| `iteration == MAX_ITER` 이고 `NOT_MET` 존재 또는 `Critical/High > 0` | **TIMEOUT** → 미해결 AC/이슈 목록을 리포트에 기록하고 Step 8 진행 |

#### 7.3 수정 대상 선정

Plan에서 `NOT_MET` AC를 포함하는 task를 역추적한다. AC가 여러 task에 걸치면 모두 포함한다. 재실행 대상은 `NOT_MET AC 관련 Task ∪ Critical/High 이슈 관련 Task`의 합집합이다.

> **반복 감지**: 2회 연속 동일 task가 재실행 대상이면 해당 task를 리포트에 `반복 실패`로 기록하고 나머지 task만 재실행한다. 모든 대상이 반복 실패면 TIMEOUT과 동일하게 처리한다.

#### 7.4 TDD 재실행

재실행 대상 task를 Step 4-5와 동일한 worker fan-out 또는 순차 실행 방식으로 다시 수행한다. 재실행 worker prompt에는 현재 iteration에서 확인된 `failed_ac`, `failure_reason`, `open_critical_high_issues`를 반드시 포함한다. 재실행 대상 간에도 Step 3의 충돌 분석 규칙을 적용해 병렬/순차를 다시 결정한다.

`iteration += 1` 후 7.1로 복귀한다.

### Step 8: Report

Iteration Review Loop 종료 후(PASS 또는 TIMEOUT) 최종 결과를 `_sdd/implementation/IMPLEMENTATION_REPORT.md`에 저장한다.

포함 내용:
- 완료 task
- 미완료/부분 완료 task
- 테스트 결과
- unplanned dependency
- critical/quality follow-up
- iteration history
- untested ac rationale (해당하는 경우)

기존 리포트가 있으면 `prev/PREV_IMPLEMENTATION_REPORT_<timestamp>.md`로 아카이브한다.

리포트 형식 예시:

```markdown
# Implementation Report: [Topic]

## Progress Summary
- Total Tasks: X | Completed: Y | Partial: Z

## Parallel Execution Stats
- Groups Dispatched: X | Parallel Tasks: Y | Sequential Fallbacks: Z
- Worker Failures: X (retried: Y, resolved: Z)

## Iteration History
| Iteration | AC Status (MET/Total) | Critical | High | Re-executed Tasks | Result |
|-----------|----------------------|----------|------|-------------------|--------|

## Completed Tasks
- [x] Task ...

## Quality Assessment
| Phase | Critical | Quality | Improvements | Groups | Status |
|-------|----------|---------|--------------|--------|--------|

## Cross-Phase Review
- Integration / Security / Performance / Consistency

## Issues Found
| # | Severity | Description | Phase | Status |

## Recommendations
1. ...

## Conclusion
[READY / NEEDS WORK / BLOCKED]
Iterations: N | Exit: PASS / TIMEOUT
```

## Worker Prompt Contract

worker 또는 하위 실행 단위에 전달할 핵심 정보:
- task id / title
- description
- acceptance criteria
- target files
- technical notes
- env / test hints
- retry context (재실행일 때만): failed_ac, failure_reason, open_critical_high_issues

worker 결과에는 최소한 다음이 있어야 한다.
- 결과 상태
- 생성/수정 파일
- 테스트 결과
- unplanned dependency
- retry context를 받았을 때는 이전 실패 사유를 어떻게 해소했는지

## Error Handling

| 상황 | 대응 |
|------|------|
| plan 없음 | `implementation-plan` 또는 `feature-draft` 사용 안내 |
| target files 불명확 | 순차 실행 + low confidence 기록 |
| 테스트 실행 실패 | `_sdd/env.md` 확인 후 실패 사실 기록 |
| worker 실패 | 실패 task만 재시도하고 나머지 결과는 보존 |
| file boundary 위반 | 미승인 변경을 분리/교정하고 순차 재실행 |

## Integration

- `implementation-plan`: primary input
- `feature-draft`: plan 부재 시 대체 입력
- `implementation-review`: 구현 후 검증
- `spec-update-done`: 구현 완료 후 스펙 동기화

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

> **Mirror Notice**: 이 스킬의 본문은 `.codex/agents/implementation.toml`의 `developer_instructions` 복사본이다.
> 사용자가 직접 호출할 때 중간 과정의 가시성을 확보하기 위해 복붙되었다.
> 내용을 수정할 때는 agent 파일과 이 스킬 파일을 **반드시 함께** 수정해야 한다.
