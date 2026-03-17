---
name: feature-draft
description: This skill should be used when the user asks to "feature draft", "draft feature", "feature plan", "plan feature", "draft and plan", "feature draft parallel", "parallel feature draft", "병렬 기능 초안", "parallel feature plan", or wants to combine requirements gathering, spec patch drafting, and implementation planning with Target Files for parallel execution support.
version: 1.2.0
---

# Feature Draft (Parallel) - Unified Spec Patch + Implementation Plan with Target Files (Wrapper)

이 스킬은 `feature_draft` custom agent에 작업을 위임합니다.

## Hard Rules

1. 이 wrapper는 직접 구현 로직이나 장문 workflow 본문을 들고 있지 않는다.
2. 사용자의 요청과 관련 artifact 경로를 가능한 한 그대로 `feature_draft`에 전달한다.
3. 결과는 custom agent의 산출물을 기준으로 사용자에게 보고한다.

## Output Contract

- 기본 산출물: _sdd/drafts/feature_draft_<feature_name>.md
- 세부 workflow, decision gate, hard rule, nested writing 규칙은 `feature_draft` agent 정의가 담당한다.

## Execution

생성된 orchestrator나 직접 호출 흐름 모두 `feature_draft` custom agent를 실행 단위로 사용한다.
