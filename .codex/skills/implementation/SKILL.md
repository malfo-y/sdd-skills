---
name: implementation
description: Use this skill when the user wants to execute an implementation plan, start implementing tasks from a plan, work through a development roadmap, says "implement the plan", "start implementation", "execute the plan", "work on the tasks", or explicitly asks for "implement parallel", "parallel implementation", "병렬 구현", "병렬로 구현". Uses conflict-aware parallel execution when Target Files are available.
version: 1.2.0
---

# Implementation Execution (Parallel TDD Approach) (Wrapper)

이 스킬은 `implementation` custom agent에 작업을 위임합니다.

## Hard Rules

1. 이 wrapper는 직접 구현 로직이나 장문 workflow 본문을 들고 있지 않는다.
2. 사용자의 요청과 관련 artifact 경로를 가능한 한 그대로 `implementation`에 전달한다.
3. 결과는 custom agent의 산출물을 기준으로 사용자에게 보고한다.

## Output Contract

- 기본 산출물: code changes plus `_sdd/implementation/` progress artifacts when produced
- 세부 workflow, decision gate, hard rule, nested writing 규칙은 `implementation` agent 정의가 담당한다.

## Execution

생성된 orchestrator나 직접 호출 흐름 모두 `implementation` custom agent를 실행 단위로 사용한다.
