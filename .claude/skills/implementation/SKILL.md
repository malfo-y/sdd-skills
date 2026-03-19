---
name: implementation
description: "Use this skill when the user wants to execute an implementation plan, start implementing tasks from a plan, work through a development roadmap, says \"implement the plan\", \"start implementation\", \"execute the plan\", \"work on the tasks\", or explicitly asks for \"implement parallel\", \"parallel implementation\", \"병렬 구현\", \"병렬로 구현\". Uses conflict-aware parallel execution when Target Files are available."
version: 1.1.0
---

# Implementation Execution (Wrapper)

이 스킬은 `implementation` 서브에이전트에 작업을 위임합니다.

## Hard Rules

1. **직접 파일 작성 금지**: 모든 작업은 서브에이전트에 위임한다.
2. **원문 전달**: 사용자의 요청을 원문 그대로 서브에이전트에 전달한다.
3. **결과 보고**: 서브에이전트의 결과를 받아 사용자에게 보고한다.

## Output Contract

- 기본 산출물: code changes plus `_sdd/implementation/` progress artifacts when produced
- 세부 workflow, decision gate, hard rule, nested writing 규칙은 `implementation` agent 정의가 담당한다.

## Execution

```
Agent(subagent_type="implementation", prompt="[사용자의 원래 요청 전문]")
```
