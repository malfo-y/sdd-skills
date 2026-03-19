---
name: ralph-loop-init
description: "Use this skill when the user asks to \"init ralph\", \"ralph loop\", \"set up ralph loop\", \"training loop\", \"training debug loop\", \"debug loop\", \"long-running test loop\", \"e2e loop\", \"create ralph\", \"set up training debug loop\", \"automated training loop\", or wants to generate a ralph/ directory for LLM-driven automated long-running process debugging."
version: 1.1.0
---

# Ralph Loop Init (Wrapper)

이 스킬은 `ralph-loop-init` 서브에이전트에 작업을 위임합니다.

## Hard Rules

1. **직접 파일 작성 금지**: 모든 작업은 서브에이전트에 위임한다.
2. **원문 전달**: 사용자의 요청을 원문 그대로 서브에이전트에 전달한다.
3. **결과 보고**: 서브에이전트의 결과를 받아 사용자에게 보고한다.

## Output Contract

- 기본 산출물: the generated `ralph/` workspace for long-running process debugging
- 세부 workflow, decision gate, hard rule, nested writing 규칙은 `ralph-loop-init` agent 정의가 담당한다.

## Execution

```
Agent(subagent_type="ralph-loop-init", prompt="[사용자의 원래 요청 전문]")
```
