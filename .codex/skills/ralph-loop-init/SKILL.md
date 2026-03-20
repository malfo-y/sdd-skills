---
name: ralph-loop-init
description: Use this skill when the user asks to "init ralph", "ralph loop", "set up ralph loop", "training loop", "training debug loop", "debug loop", "long-running test loop", "e2e loop", "create ralph", "set up training debug loop", "automated training loop", or wants to generate a ralph/ directory for LLM-driven automated long-running process debugging.
version: 2.0.0
---

# Ralph Loop Initialization

| Workflow | Position | When |
|----------|----------|------|
| Large | Optional utility | 장기 실행 루프/디버그 자동화 필요 |
| Medium | Optional utility | training/e2e/debug loop 필요 |
| Any | Standalone | `ralph/` workspace 초기화 |

이 agent는 장시간 실행되는 학습/테스트/디버그 프로세스를 LLM이 반복적으로 관찰하고 수정할 수 있도록 `ralph/` 워크스페이스를 생성한다.

## Acceptance Criteria

> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] `ralph/` 디렉터리가 생성된다.
- [ ] `CHECKS.md`, `state.md`, `run.sh`가 생성된다.
- [ ] 대상 프로세스의 성공 조건과 관찰 포인트가 문서화된다.
- [ ] 외부 example/reference 없이도 기본 워크스페이스를 만들 수 있다.

## Hard Rules

1. `_sdd/spec/`와 프로젝트 소스는 읽기 전용 컨텍스트로만 사용한다.
2. `ralph/` 초기화는 반복 실행 가능한 구조여야 한다.
3. 성공 조건은 추상적이지 않고 관찰 가능한 체크로 적는다.
4. 사용자가 특정 프로세스를 명시하지 않으면 현재 프로젝트의 long-running 검증 루프를 best-effort로 추론한다.

## Required Artifacts

최소 생성물:
- `ralph/CHECKS.md`
- `ralph/state.md`
- `ralph/run.sh`
- 필요 시 `ralph/results/`, `ralph/logs/` 안내

## Process

### Step 1: Read Project Context

다음을 확인한다.
- `_sdd/spec/*.md`
- `_sdd/env.md`
- README / 실행 스크립트 / 테스트 명령

목적:
- 어떤 long-running process를 감쌀지 결정
- 성공 조건과 실패 신호를 찾기

### Step 2: Discover Target Process

대상 프로세스를 정한다.
- training loop
- e2e/test loop
- debug reproduction loop
- batch validation loop

명시적 요청이 없으면 프로젝트 맥락상 가장 가치 높은 loop를 고른다.

### Step 3: Define Checks

`CHECKS.md`에 다음을 적는다.
- 성공 조건
- 실패 조건
- 관찰 포인트
- 사람이 봐야 할 증거

check는 binary하거나 명확한 상태 판정이 가능해야 한다.

### Step 4: Initialize State

`state.md`에 초기 상태를 적는다.
- current phase
- known blockers
- next action
- latest result summary

### Step 5: Create Runner

`run.sh`는 기본 실행/재실행 엔트리포인트다.

포함할 내용:
- 환경 준비 힌트
- 실제 실행 명령
- 로그/결과 저장 위치
- 실패 시 재시도 또는 상태 갱신에 필요한 최소 정보

## Error Handling

| 상황 | 대응 |
|------|------|
| 실행 명령이 불명확 | README / env / scripts를 보고 best-effort 기본 명령을 구성 |
| 성공 조건이 모호 | 관찰 가능한 최소 check부터 정의 |
| 환경 요구사항이 큼 | `_sdd/env.md`의 핵심 단계만 `run.sh` 주석에 남긴다 |
| 대상 프로세스 후보가 여러 개 | 가장 핵심적인 하나를 우선 선택하고 나머지는 notes로 남긴다 |

## Integration

- `implementation-review`: loop 결과를 구현 검증에 활용 가능
- `spec-update-done`: loop에서 확인된 실제 동작을 spec sync 근거로 활용 가능

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

> **Mirror Notice**: 이 스킬의 본문은 `.codex/agents/ralph-loop-init.toml`의 `developer_instructions` 복사본이다.
> 사용자가 직접 호출할 때 중간 과정의 가시성을 확보하기 위해 복붙되었다.
> 내용을 수정할 때는 agent 파일과 이 스킬 파일을 **반드시 함께** 수정해야 한다.
