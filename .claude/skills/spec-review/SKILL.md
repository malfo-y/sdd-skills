---
name: spec-review
description: "This skill should be used when the user asks to \"review spec\", \"spec drift check\", \"verify spec accuracy\", \"audit spec quality\", \"review spec against code\", \"refresh spec review\", \"스펙 리뷰\", \"스펙 검토\", \"스펙 드리프트 점검\", or wants a review-only analysis of spec quality and code-to-spec alignment without directly editing spec files."
version: 1.1.0
---

# Spec Review (Strict, Review-Only) (Wrapper)

이 스킬은 `spec-review` 서브에이전트에 작업을 위임합니다.

## Hard Rules

1. **직접 파일 작성 금지**: 모든 작업은 서브에이전트에 위임한다.
2. **원문 전달**: 사용자의 요청을 원문 그대로 서브에이전트에 전달한다.
3. **결과 보고**: 서브에이전트의 결과를 받아 사용자에게 보고한다.

## Output Contract

- 기본 산출물: `_sdd/spec/SPEC_REVIEW_REPORT.md`
- 세부 workflow, decision gate, hard rule, nested writing 규칙은 `spec-review` agent 정의가 담당한다.

## Execution

```
Agent(subagent_type="spec-review", prompt="[사용자의 원래 요청 전문]")
```
