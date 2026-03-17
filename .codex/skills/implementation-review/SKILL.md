---
name: implementation-review
description: Use this skill to review implementation progress against the plan, verify acceptance criteria, identify issues, and determine next steps. Triggered by "review implementation", "check progress", "verify implementation", "what's done", "implementation status", or "audit the code".
version: 2.2.0
---

# Implementation Review (Wrapper)

이 스킬은 `implementation_review` custom agent에 작업을 위임합니다.

## Hard Rules

1. 이 wrapper는 직접 구현 로직이나 장문 workflow 본문을 들고 있지 않는다.
2. 사용자의 요청과 관련 artifact 경로를 가능한 한 그대로 `implementation_review`에 전달한다.
3. 결과는 custom agent의 산출물을 기준으로 사용자에게 보고한다.

## Output Contract

- 기본 산출물: _sdd/implementation/IMPLEMENTATION_REVIEW.md
- 세부 workflow, decision gate, hard rule, nested writing 규칙은 `implementation_review` agent 정의가 담당한다.

## Execution

생성된 orchestrator나 직접 호출 흐름 모두 `implementation_review` custom agent를 실행 단위로 사용한다.
