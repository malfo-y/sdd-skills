---
name: spec-update-todo
description: "This skill should be used when the user asks to \"update spec with features\", \"add features to spec\", \"update spec from input\", \"add requirements to spec\", \"spec update\", \"expand spec\", \"add to-do to spec\", \"add to-implement to spec\", or mentions adding new features, requirements, or planned improvements to an existing specification document."
version: 1.1.0
---

# Spec Update Todo (Wrapper)

이 스킬은 `spec-update-todo` 서브에이전트에 작업을 위임합니다.

## Hard Rules

1. **직접 파일 작성 금지**: 모든 작업은 서브에이전트에 위임한다.
2. **원문 전달**: 사용자의 요청을 원문 그대로 서브에이전트에 전달한다.
3. **결과 보고**: 서브에이전트의 결과를 받아 사용자에게 보고한다.

## Output Contract

- 기본 산출물: `_sdd/spec/*.md`
- 세부 workflow, decision gate, hard rule, nested writing 규칙은 `spec-update-todo` agent 정의가 담당한다.

## Execution

```
Agent(subagent_type="spec-update-todo", prompt="[사용자의 원래 요청 전문]")
```
