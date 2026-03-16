---
name: feature-draft
description: "This skill should be used when the user asks to \"feature draft\", \"draft feature\", \"feature plan\", \"plan feature\", \"draft and plan\", \"feature draft parallel\", \"parallel feature draft\", \"병렬 기능 초안\", \"parallel feature plan\", or wants to combine requirements gathering, spec patch drafting, and implementation planning with Target Files for parallel execution support."
version: 1.1.0
---

# Feature Draft (Wrapper)

이 스킬은 `feature-draft` 서브에이전트에 작업을 위임합니다.

## Hard Rules

1. **직접 파일 작성 금지**: 이 스킬에서 직접 파일을 생성/수정하지 않는다. 모든 작업은 서브에이전트에 위임한다.
2. **원문 전달**: 사용자의 요청을 요약하지 않고 원문 그대로 서브에이전트에 전달한다.
3. **결과 보고**: 서브에이전트의 결과를 받아 사용자에게 보고한다.

## Execution

사용자의 요청을 `feature-draft` 에이전트에 위임한다:

```
Agent(subagent_type="feature-draft", prompt="[사용자의 원래 요청 전문]")
```
