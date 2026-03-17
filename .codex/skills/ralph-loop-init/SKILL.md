---
name: ralph-loop-init
description: Use this skill when the user asks to "init ralph", "ralph loop", "set up ralph loop", "training loop", "training debug loop", "create ralph", "set up training debug loop", "automated training loop", or wants to generate a ralph/ directory for LLM-driven automated ML training debugging.
version: 1.2.0
---

# Ralph Loop Initialization (Wrapper)

이 스킬은 `ralph_loop_init` custom agent에 작업을 위임합니다.

## Hard Rules

1. 이 wrapper는 직접 구현 로직이나 장문 workflow 본문을 들고 있지 않는다.
2. 사용자의 요청과 관련 artifact 경로를 가능한 한 그대로 `ralph_loop_init`에 전달한다.
3. 결과는 custom agent의 산출물을 기준으로 사용자에게 보고한다.

## Output Contract

- 기본 산출물: the generated `ralph/` workspace
- 세부 workflow, decision gate, hard rule, nested writing 규칙은 `ralph_loop_init` agent 정의가 담당한다.

## Execution

생성된 orchestrator나 직접 호출 흐름 모두 `ralph_loop_init` custom agent를 실행 단위로 사용한다.
