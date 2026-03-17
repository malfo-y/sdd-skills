---
name: implementation-plan
description: This skill should be used when the user asks to "create an implementation plan", "plan the implementation", "break down this spec", "create a development roadmap", "analyze requirements and create tasks", "create a parallel implementation plan", "plan parallel implementation", "병렬 구현 계획", "create parallel development roadmap", or wants a structured implementation plan with Target Files for parallel execution support.
version: 1.2.0
---

# Implementation Plan Creation (Parallel-Ready) (Wrapper)

이 스킬은 `implementation_plan` custom agent에 작업을 위임합니다.

## Hard Rules

1. 이 wrapper는 직접 구현 로직이나 장문 workflow 본문을 들고 있지 않는다.
2. 사용자의 요청과 관련 artifact 경로를 가능한 한 그대로 `implementation_plan`에 전달한다.
3. 결과는 custom agent의 산출물을 기준으로 사용자에게 보고한다.

## Output Contract

- 기본 산출물: _sdd/implementation/IMPLEMENTATION_PLAN.md
- 세부 workflow, decision gate, hard rule, nested writing 규칙은 `implementation_plan` agent 정의가 담당한다.

## Execution

생성된 orchestrator나 직접 호출 흐름 모두 `implementation_plan` custom agent를 실행 단위로 사용한다.
