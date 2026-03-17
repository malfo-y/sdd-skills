---
name: spec-update-done
description: This skill should be used when the user asks to "update spec from code", "sync spec with implementation", "apply implementation changes to spec", "reflect completed work in spec", "refresh spec after implementation", "implementation done sync", or mentions spec document maintenance tied to completed code changes.
version: 1.2.0
---

# Spec Sync and Update (Wrapper)

이 스킬은 `spec_update_done` custom agent에 작업을 위임합니다.

## Hard Rules

1. 이 wrapper는 직접 구현 로직이나 장문 workflow 본문을 들고 있지 않는다.
2. 사용자의 요청과 관련 artifact 경로를 가능한 한 그대로 `spec_update_done`에 전달한다.
3. 결과는 custom agent의 산출물을 기준으로 사용자에게 보고한다.

## Output Contract

- 기본 산출물: _sdd/spec/*.md and `_sdd/spec/DECISION_LOG.md` when rationale changes
- 세부 workflow, decision gate, hard rule, nested writing 규칙은 `spec_update_done` agent 정의가 담당한다.

## Execution

생성된 orchestrator나 직접 호출 흐름 모두 `spec_update_done` custom agent를 실행 단위로 사용한다.
