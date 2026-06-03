---
name: spec-review
description: This skill should be used when the user asks to "review spec", "spec drift check", "verify spec accuracy", "audit spec quality", "review spec against code", "refresh spec review", "스펙 리뷰", "스펙 검토", "스펙 드리프트 점검", or wants a review-only analysis of spec quality and code-to-spec alignment without directly editing spec files.
version: 3.0.0
---

# Spec Review (Entrypoint Wrapper)

이 스킬은 entrypoint wrapper다. 사용자의 spec-review 요청을 `sdd-skills:spec-review-agent`에 위임하고 그 결과를 사용자에게 전달한다. 전체 리뷰 프로세스·global/temporary rubric·severity·리포트 형식은 agent가 단일 소스로 보유한다.

## 실행

1. 사용자 요청 + 리뷰 대상 경로(있으면 spec/draft/구현 경로)와 이미 아는 결정을 수집한다 (wrapper는 새 분석 read를 하지 않는다).
2. `Agent(subagent_type="sdd-skills:spec-review-agent", prompt=<요청 + 알려진 경로/컨텍스트>)`로 dispatch한다. 대상 경로가 불명확하면 agent가 Scope/Spec Type 우선순위로 자체 탐색하도록 위임한다.
3. agent의 반환(리포트 경로 `_sdd/spec/logs/spec_review_report.md`, Decision, Critical/Quality findings 요약)을 사용자에게 그대로 relay한다.

## 계약 (entrypoint·artifact 유지, 흉내 금지)

- trigger(spec-review 호출)와 리포트 경로 계약은 이 wrapper가 유지한다.
- 실제 감사·리포트 작성은 agent가 수행한다. agent가 지원하지 않는 동작을 wrapper가 흉내내지 않는다.
- agent가 노출하는 Blocker(Critical findings)·drift·후속 스킬 제안을 wrapper가 relay해 보존한다.

> Source: 전체 계약·global/temporary rubric·severity·출력 형식은 `.claude/agents/spec-review-agent.md`가 단일 소스로 보유한다 (wrapper↔agent; 더 이상 동일 본문 mirror 아님).
