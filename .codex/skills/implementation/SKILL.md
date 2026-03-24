---
name: implementation
description: Use this skill when the user wants to execute an implementation plan, start implementing tasks from a plan, work through a development roadmap, says "implement the plan", "start implementation", "execute the plan", "work on the tasks", or explicitly asks for "implement parallel", "parallel implementation", "병렬 구현", "병렬로 구현". Uses conflict-aware parallel execution when Target Files are available.
version: 2.0.0
---

# Implementation Execution

| Workflow | Position | When |
|----------|----------|------|
| Large | Step 3 of 6 | implementation plan 실행 |
| Medium | Step 3 of 3 | 구현 단계 |
| Small | Direct | 단일 변경 구현 |

이 agent는 implementation plan 또는 feature draft의 Part 2를 실행해 코드 변경과 `_sdd/implementation/` 진행 아티팩트를 만든다.

## Acceptance Criteria

> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] plan을 읽고 실행 가능한 task 단위로 파싱한다.
- [ ] `_sdd/implementation/IMPLEMENTATION_PROGRESS.md`를 갱신한다.
- [ ] Target Files 기반 병렬/순차 실행 판단이 가능하다.
- [ ] 테스트/검증/리포트까지 포함한 구현 사이클이 완료된다.

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
- 파일이 달라도 API contract, shared type, migration, config가 겹치면 의미적 충돌로 본다.
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

### Step 7: Final Report

최종 결과를 `_sdd/implementation/IMPLEMENTATION_REPORT.md`에 저장한다.

포함 내용:
- 완료 task
- 미완료/부분 완료 task
- 테스트 결과
- unplanned dependency
- critical/quality follow-up

기존 리포트가 있으면 `prev/PREV_IMPLEMENTATION_REPORT_<timestamp>.md`로 아카이브한다.

## Worker Prompt Contract

worker 또는 하위 실행 단위에 전달할 핵심 정보:
- task id / title
- description
- acceptance criteria
- target files
- technical notes
- env / test hints

worker 결과에는 최소한 다음이 있어야 한다.
- 결과 상태
- 생성/수정 파일
- 테스트 결과
- unplanned dependency

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
