---
name: spec-update-done
description: "This skill should be used when the user asks to \"update spec from code\", \"sync spec with implementation\", \"apply implementation changes to spec\", \"reflect completed work in spec\", \"refresh spec after implementation\", \"implementation done sync\", or mentions spec document maintenance tied to completed code changes."
version: 1.1.0
---

# Spec Sync and Update (Wrapper)

이 스킬은 `spec-update-done` 서브에이전트에 작업을 위임합니다.

## Hard Rules

1. **직접 파일 작성 금지**: 모든 작업은 서브에이전트에 위임한다.
2. **원문 전달**: 사용자의 요청을 원문 그대로 서브에이전트에 전달한다.
3. **결과 보고**: 서브에이전트의 결과를 받아 사용자에게 보고한다.

## Output Contract

- 기본 산출물: `_sdd/spec/*.md` and `_sdd/spec/DECISION_LOG.md` when rationale changes
- 세부 workflow, decision gate, hard rule, nested writing 규칙은 `spec-update-done` agent 정의가 담당한다.

## Execution

```
Agent(subagent_type="spec-update-done", prompt="[사용자의 원래 요청 전문]")
```
