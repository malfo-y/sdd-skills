---
name: implementation-review
description: "Use this skill to review implementation progress against the plan, verify acceptance criteria, identify issues, and determine next steps. Triggered by \"review implementation\", \"check progress\", \"verify implementation\", \"what's done\", \"implementation status\", or \"audit the code\". Works with or without an implementation plan (Graceful Degradation)."
version: 2.1.0
---

# Implementation Review (Wrapper)

이 스킬은 `implementation-review` 서브에이전트에 작업을 위임합니다.

## Hard Rules

1. **직접 파일 작성 금지**: 모든 작업은 서브에이전트에 위임한다.
2. **원문 전달**: 사용자의 요청을 원문 그대로 서브에이전트에 전달한다.
3. **결과 보고**: 서브에이전트의 결과를 받아 사용자에게 보고한다.

## Output Contract

- 기본 산출물: `_sdd/implementation/IMPLEMENTATION_REVIEW.md`
- 세부 workflow, decision gate, hard rule, nested writing 규칙은 `implementation-review` agent 정의가 담당한다.

## Execution

```
Agent(subagent_type="implementation-review", prompt="[사용자의 원래 요청 전문]")
```
