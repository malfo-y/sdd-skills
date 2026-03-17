# Pipeline Templates - Codex SDD Autopilot

`sdd-autopilot`이 generated orchestration skill을 만들 때 사용하는 규모별 템플릿이다.

## Small

### Use When

- touched code files: 1-3
- spec update unnecessary
- 신규 컴포넌트 0-1개
- 단일 함수, 단일 문서, 단일 wrapper 수준의 국소 변경

### Pipeline

```text
implementation
-> inline verification
-> optional implementation_review when explicitly requested
```

### Generated Orchestrator Minimum

```markdown
# Orchestrator: <topic>

**generated**: <timestamp>
**scale**: small
**owner**: sdd-autopilot
**status**: active

## Goal

<사용자 요청 원문 + 구체화된 요구사항>

## Pipeline Steps

### Step 1: implementation

**agent**: `implementation`
**input**: (none or existing implementation plan when resuming)
**output**: <modified files>

## Review-Fix Loop

- small 기본: review 미포함
- 단, review가 들어가면 `implementation_review -> implementation -> implementation_review`

## Test Strategy

- strategy: inline verification
- command: <repo-specific command>

## Error Handling

- retry: 3
- critical: implementation, implementation_review when included
```

## Medium

### Use When

- touched code files: 4-10
- 기존 스펙 섹션 패치 필요
- 신규 컴포넌트 1-3개
- 여러 모듈 연동 또는 skill/reference/example 동시 수정

### Pipeline

```text
feature_draft -> implementation_plan -> implementation
-> implementation_review -> fix -> re-review
-> inline test / verification
-> spec_update_done
```

### Generated Orchestrator Minimum

```markdown
# Orchestrator: <topic>

**generated**: <timestamp>
**scale**: medium
**owner**: sdd-autopilot
**status**: active

## Goal

<사용자 요청 원문>

### Clarified Requirements
- <요구사항 1>
- <요구사항 2>

### Constraints
- <제약 조건>

## Pipeline Steps

### Step 1: feature_draft
**agent**: `feature_draft`
**output**: `_sdd/drafts/feature_draft_<topic>.md`

### Step 2: implementation_plan
**agent**: `implementation_plan`
**input**: `_sdd/drafts/feature_draft_<topic>.md`
**output**: `_sdd/implementation/IMPLEMENTATION_PLAN.md`

### Step 3: implementation
**agent**: `implementation`
**input**: `_sdd/implementation/IMPLEMENTATION_PLAN.md`
**output**: <changed files>

### Step 4: implementation_review
**agent**: `implementation_review`
**input**: implementation outputs + implementation plan

### Step 5: spec_update_done
**agent**: `spec_update_done`
**input**: updated implementation + related spec

## Artifact Handoff

- feature draft -> implementation plan
- implementation plan -> implementation review
- implementation outputs -> spec update

## Review-Fix Loop

- max rounds: 3
- stop when critical = 0 and high = 0
- fix only critical/high

## Test Strategy

- strategy: inline verification
- command: <repo-specific command>
- retry loop: up to 5 when local and short-running

## Error Handling

- retry: 3
- critical: feature_draft, implementation_plan, implementation, implementation_review
- non-critical: spec_update_done
```

### Notes

- long-form draft, plan, review output은 nested `write_phased` 또는 동일한 skeleton -> fill 전략을 적용한다
- medium pipeline이라도 spec patch가 선행돼야 하면 `spec_update_todo`를 앞에 삽입할 수 있다

## Large

### Use When

- touched code files: 10+
- 신규 스펙 섹션 추가 필요
- 신규 컴포넌트 3개+
- 아키텍처 레벨 변경

### Pipeline

```text
feature_draft -> spec_update_todo -> implementation_plan -> implementation
-> implementation_review -> fix -> re-review
-> test / debug (inline or ralph_loop_init)
-> spec_update_done -> optional spec_review
```

### Generated Orchestrator Minimum

```markdown
# Orchestrator: <topic>

**generated**: <timestamp>
**scale**: large
**owner**: sdd-autopilot
**status**: active

## Goal

<사용자 요청 원문>

### Clarified Requirements
- <요구사항 목록>

### Constraints
- <제약 목록>

## Pipeline Steps

### Step 1: feature_draft
**agent**: `feature_draft`

### Step 2: spec_update_todo
**agent**: `spec_update_todo`

### Step 3: implementation_plan
**agent**: `implementation_plan`

### Step 4: implementation
**agent**: `implementation`

### Step 5: implementation_review
**agent**: `implementation_review`

### Step 6: test / debug
**agent**: inline verification or `ralph_loop_init`

### Step 7: spec_update_done
**agent**: `spec_update_done`

### Step 8: spec_review
**agent**: `spec_review` when quality gate is needed

## Review-Fix Loop

- max rounds: 3
- stop when critical = 0 and high = 0
- log medium/low as residual issues

## Test Strategy

- strategy: inline or `ralph_loop_init`
- justify the choice with `_sdd/env.md` and scale assessment

## Error Handling

- retry: 3
- critical: feature_draft, implementation_plan, implementation, implementation_review
- non-critical: spec_update_todo, spec_update_done, spec_review, `ralph_loop_init`
```

### Notes

- 테스트/디버깅이 길면 `ralph_loop_init`을 조건부로 포함한다
- long-form output이 많은 단계는 `write_phased`를 우선한다
- generated orchestrator는 custom agent 이름을 사용하고 wrapper skill 이름을 직접 실행 단위로 쓰지 않는다

## Generated Orchestrator Lifecycle

- active run: `.codex/skills/orchestrator_<topic>/`
- completed archive: `_sdd/pipeline/orchestrators/<topic>_<timestamp>/`
- execution log: `_sdd/pipeline/log_<topic>_<timestamp>.md`
- final report: `_sdd/pipeline/report_<topic>_<timestamp>.md`
