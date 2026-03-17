---
name: sdd-autopilot
description: This skill should be used when the user asks to "sdd-autopilot", "autopilot", "자동 구현", "end-to-end 구현", "전체 파이프라인", "처음부터 끝까지", or wants Codex to orchestrate the full SDD workflow from requirement clarification to spec sync.
version: 1.2.0
---

# SDD Autopilot - Codex Adaptive Orchestration Meta Skill

`sdd-autopilot`은 사용자 요청을 분석하고, 규모에 맞는 SDD 파이프라인을 설계한 뒤, Codex custom agents를 spawn하는 generated orchestration skill로 end-to-end 흐름을 오케스트레이션하는 메타스킬이다.

## Workflow Position

| Workflow | Position | When |
|----------|----------|------|
| SDD Full Pipeline | Orchestrator | 요구사항 분석부터 스펙 동기화까지 한 번에 실행할 때 |
| Standalone | Direct skill | `/sdd-autopilot`으로 직접 호출할 때 |

## Use When

- 기능 구현을 처음부터 끝까지 자동화하고 싶을 때
- "이 기능 구현해줘"처럼 discussion부터 spec sync까지 이어지는 넓은 요청일 때
- 여러 SDD 실행 단위를 순차 호출해야 하는 복합 작업일 때
- partial execution, resume, review-fix loop, spec sync까지 한 흐름으로 묶고 싶을 때

## Do Not Use When

- 단일 skill로 끝나는 작업일 때
- 이미 구현 계획이 있고 구현만 실행하면 되는 경우
- 토론만 필요한 경우
- 스펙 문서만 업데이트하면 되는 경우
- 단순 리뷰, 단순 가이드 작성, 단순 snapshot 작업인 경우

이 경우에는 해당 wrapper skill을 직접 사용한다.

## Execution Model

이 스킬은 새 business/domain agent 역할을 만들지 않는다. 아래의 기존 SDD custom agent만 재사용한다.

- `feature_draft`
- `implementation_plan`
- `implementation`
- `implementation_review`
- `spec_update_todo`
- `spec_update_done`
- `spec_review`
- `ralph_loop_init`
- `write_phased`

> custom agent definitions live under `.codex/agents/`. Wrapper skills remain user entry points, but generated orchestrators spawn custom agents directly.

## Hard Rules

1. **기존 custom agent만 재사용**: net-new business/domain agent role을 만들지 않는다.
2. **Discussion은 인라인**: 사용자와의 요구사항 정리는 `request_user_input` 또는 메인 스레드 대화로 진행한다.
3. **스펙 직접 수정 금지**: `_sdd/spec/` 변경은 `spec_update_todo` 또는 `spec_update_done` 실행 단위로만 수행한다.
4. **파일 기반 handoff**: 단계 간 상태 전달은 `_sdd/` 산출물 경로로만 수행한다.
5. **Review-Fix 사이클 필수**: review 단계가 포함되면 `review -> fix -> re-review`를 최대 3회까지 반드시 실행한다.
6. **오케스트레이터 라이프사이클 준수**: 미완료 orchestrator는 active `.codex/skills/orchestrator_<topic>/`에 유지하고, 완료 후 `_sdd/pipeline/orchestrators/<topic>_<timestamp>/`로 이동한다.
7. **언어 규칙**: 사용자의 활성 언어를 따른다. 지정이 없으면 기존 스펙/문서 언어를 따른다.
8. **요약 대신 원문 전달**: 하위 실행 단위로 넘길 때 사용자의 원래 요청과 산출물 경로를 유지한다.
9. **Pre-flight 필수**: 승인 전 `_sdd/env.md`와 `.codex/config.toml`을 함께 읽고 resource gap을 확인한다.
10. **Nested writing depth 보장**: `write_phased` nested spawn이 필요한 파이프라인에서는 `agents.max_depth >= 2`를 만족해야 한다.
11. **Generated orchestrator는 skill이 아니라 agent를 호출**: execution step은 `.codex/agents/*.toml`에 정의된 custom agent 이름만 사용한다.

## Inputs

- 사용자 기능 요청
- `_sdd/spec/*.md`
- `_sdd/drafts/feature_draft_*.md`
- `_sdd/implementation/IMPLEMENTATION_PLAN*.md`
- `_sdd/pipeline/log_*.md`
- `_sdd/env.md`
- `.codex/config.toml`

## Outputs

- active orchestrator: `.codex/skills/orchestrator_<topic>/SKILL.md`
- active orchestrator metadata: `.codex/skills/orchestrator_<topic>/skill.json`
- pipeline log: `_sdd/pipeline/log_<topic>_<timestamp>.md`
- final summary report: `_sdd/pipeline/report_<topic>_<timestamp>.md`
- archived orchestrator: `_sdd/pipeline/orchestrators/<topic>_<timestamp>/`

## References

- `references/pipeline-templates.md`
- `references/scale-assessment.md`
- `examples/sample-orchestrator.md`

## Process Overview

1. Detect existing pipeline state and related artifacts
2. Analyze the request and narrow requirements
3. Explore the codebase and assess scale
4. Decide test strategy and run pre-flight
5. Generate an orchestration skill and pipeline log
6. Ask the user for approval
7. Execute the approved pipeline autonomously
8. Write final report and archive orchestration artifacts

## Step 0: Pipeline State Detection

### 0.1 Log Scan

Check `_sdd/pipeline/log_*.md`.

- unfinished status 후보: `pending`, `in_progress`, `failed`
- completed run이라도 현재 요청과 topic이 명확히 연결되면 참고용으로 읽는다

### 0.2 Existing Artifact Scan

Check:

- `_sdd/drafts/feature_draft_*.md`
- `_sdd/implementation/IMPLEMENTATION_PLAN*.md`
- `_sdd/pipeline/report_*.md`

### 0.3 Resume Branch

If an unfinished pipeline exists:

- summarize the request, last completed step, reused artifacts, and current risks
- ask whether to resume or start fresh via `request_user_input`
- when the user asks for partial execution, detect start/end hints and narrow the pipeline range

If no unfinished pipeline exists, continue with a new run.

## Step 1: Request Analysis

Extract:

- feature description
- technical keywords
- explicit constraints
- review/test expectations
- start/end hints such as "구현부터", "리뷰까지만", "이어서"

Record a compact internal state:

```text
request_parsed = {
  original_request,
  clarified_scope,
  constraints,
  pipeline_range,
  reuse_candidates,
}
```

When existing artifacts appear related, prefer reusing them and record assumptions in the generated orchestration skill.

## Step 2: Interactive Clarification

Use `request_user_input` one question at a time only when clarification materially affects:

- scope
- architectural direction
- review/test expectations
- whether existing artifacts should be reused

### Clarification Strategy

| Initial Complexity | Typical Questions | Focus |
|--------------------|-------------------|-------|
| Small | 0-1 | 정확한 범위, 완료 기준 |
| Medium | 1-2 | 기능 범위, 제약 조건, review 기대치 |
| Large | 2-3 | 아키텍처 방향, 단계별 전략, 리스크, spec 영향 |

If the request is already clear enough, skip quickly to Step 3.

## Step 3: Codebase Exploration

Use read-only exploration (`rg`, `Glob`, `Read`, read-only shell) to identify:

- likely touched files/modules
- relevant tests and conventions
- existing SDD artifacts
- whether long-form output is likely

Summarize findings as:

```text
codebase_analysis = {
  project_structure,
  related_files,
  existing_patterns,
  test_structure,
  spec_status,
  estimated_file_count,
  new_components,
  spec_change_needed,
}
```

## Step 4: Scale Assessment

Determine `small`, `medium`, or `large` using `references/scale-assessment.md`.

Rules:

- if quantitative and qualitative signals disagree, choose the larger scale
- if uncertain, default to `medium`
- if review is requested, ensure the review-fix loop is present
- if partial execution is requested, apply scale to the requested slice, not blindly to the whole feature

### 4.2 Test Strategy Decision

Choose one:

- inline verification
- inline test/debug loop
- `ralph_loop_init`

Use the reference guide and `_sdd/env.md` to justify the choice.

## Step 4.5: Pre-flight Check

Read:

- `_sdd/env.md`
- `.codex/config.toml`

Verify:

- required external services and test/runtime assumptions
- whether `agents.max_threads` is sufficient for the chosen scale
- whether `agents.max_depth >= 2` when nested `write_phased` calls are expected
- whether wrapper/custom-agent contracts and repo state allow the chosen pipeline

If gaps exist:

- summarize them before approval
- treat them as execution risks, not silent assumptions
- include them in the generated orchestration skill and final report

## Step 5: Generate Orchestration Skill

Create:

- `.codex/skills/orchestrator_<topic>/SKILL.md`
- `.codex/skills/orchestrator_<topic>/skill.json`
- `_sdd/pipeline/log_<topic>_<timestamp>.md`

### 5.1 Required Orchestrator Sections

The generated orchestration skill must include:

- 기능 설명
- 구체화된 요구사항
- 제약 조건
- pipeline steps
- artifact handoff paths
- review-fix loop contract
- test strategy
- error handling
- pre-flight findings
- active/archive lifecycle

### 5.2 Execution Constraints

The generated orchestration skill must:

- name the chosen custom agents explicitly
- pass artifact paths forward
- keep logs updated after each milestone
- spawn only `.codex/agents/*.toml` custom agents
- use nested `write_phased` for long-form outputs in `feature_draft`, `implementation_plan`, `implementation_review`, and `spec_review`
- avoid inventing new execution agents

Use `examples/sample-orchestrator.md` as the minimum detail baseline.

## Step 6: Approval Checkpoint

Show the user:

- scale decision
- pipeline steps
- main outputs
- reused artifacts
- pre-flight findings
- expected test strategy

Then ask for:

- approve and execute
- revise pipeline
- stop

## Step 7: Autonomous Execution

After approval, execute without unnecessary user interruption.

### 7.1 Initialization

- initialize the pipeline log
- mark each step as `pending`
- record reused artifacts and pre-flight notes

### 7.2 Main Execution Loop

For each pipeline step:

1. write a start log entry
2. spawn the mapped custom agent
3. pass input artifact paths and original request
4. collect outputs and decisions
5. update the pipeline log

### 7.3 Review-Fix Loop

If review is included:

- run `implementation_review`
- if `critical > 0` or `high > 0`, send only those issues back to `implementation`
- re-run `implementation_review`
- stop after success or max 3 rounds

`medium` and `low` issues are logged but do not block completion.

### 7.4 Test Execution

When the selected strategy is inline:

- run tests or verification commands
- retry fix-and-rerun up to 5 times when the loop is short and local

When the selected strategy requires long-running or external orchestration:

- include `ralph_loop_init` in the pipeline or record why the test step is deferred

### 7.5 Error Handling

Default retry policy: 3 attempts per failing step.

Critical steps:

- `feature_draft`
- `implementation_plan`
- `implementation`
- `implementation_review` when review is included

Non-critical candidates:

- `spec_update_todo`
- `spec_update_done`
- `spec_review`
- `ralph_loop_init`

Critical step failure stops the pipeline. Non-critical failure is logged and reported with fallback guidance.

### 7.6 Milestone Reporting

After each step, log:

- start/end time
- output artifacts
- 핵심 결정사항
- issues or retries

### 7.7 Log and Report Management

Keep the pipeline log current throughout the run.

The final report must summarize:

- executed steps
- spawned agents
- created or modified artifacts
- review findings and fix rounds
- test results
- remaining risks or manual follow-up

## Step 8: Completion and Archival

When the run completes:

1. update the pipeline log with final status
2. write `_sdd/pipeline/report_<topic>_<timestamp>.md`
3. move `.codex/skills/orchestrator_<topic>/` to `_sdd/pipeline/orchestrators/<topic>_<timestamp>/`
4. leave the log, report, and other `_sdd/` artifacts in place for audit and resume history

If the run is incomplete or failed:

- keep the active orchestrator in `.codex/skills/orchestrator_<topic>/`
- still write the summary report with current progress and failure reason

## Additional Resources

### Reference Files

- `references/pipeline-templates.md` -- 규모별 generated orchestrator template과 review-fix, test, error-handling 계약
- `references/scale-assessment.md` -- 규모 판단 상세 기준, 경계 사례, 테스트 전략 힌트

### Example Files

- `examples/sample-orchestrator.md` -- 중규모 Codex orchestrator와 로그/보고서 예시
