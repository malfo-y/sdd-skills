---
name: implementation-plan
description: "This skill should be used when the user asks to \"create an implementation plan\", \"plan the implementation\", \"break down this spec\", \"create a development roadmap\", \"analyze requirements and create tasks\", \"create a parallel implementation plan\", \"plan parallel implementation\", \"병렬 구현 계획\", \"create parallel development roadmap\", or wants a structured implementation plan with Target Files for parallel execution support."
version: 1.1.0
---

# Implementation Plan (Wrapper)

이 스킬은 `implementation-plan` 서브에이전트에 작업을 위임합니다.

## Hard Rules

1. **직접 파일 작성 금지**: 모든 작업은 서브에이전트에 위임한다.
2. **원문 전달**: 사용자의 요청을 원문 그대로 서브에이전트에 전달한다.
3. **결과 보고**: 서브에이전트의 결과를 받아 사용자에게 보고한다.

## Output Contract

- 기본 산출물: `_sdd/implementation/IMPLEMENTATION_PLAN.md`
- 세부 workflow, decision gate, hard rule, nested writing 규칙은 `implementation-plan` agent 정의가 담당한다.

## Execution

```
Agent(subagent_type="implementation-plan", prompt="[사용자의 원래 요청 전문]")
```
