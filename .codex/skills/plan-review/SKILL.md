---
name: plan-review
description: Use this skill to review an implementation plan before coding, identify overengineering and sloppy-code risks, and produce a findings-first plan review report. Triggered by "plan review", "review plan", "implementation plan review", "계획 리뷰", "플랜 리뷰", "구현 계획 리뷰", or when the user wants to check a plan against KISS/YAGNI/DRY/minimum-code principles before implementation.
version: 2.0.0
---

# Plan Review (Entrypoint Wrapper)

이 스킬은 entrypoint wrapper다. 사용자의 plan-review 요청을 `plan_review_agent`에 위임하고 그 결과를 사용자에게 전달한다. 전체 리뷰 프로세스·6-smell rubric·severity·리포트 형식은 agent가 단일 소스로 보유한다.

## 실행

1. 사용자 요청 + 리뷰 대상 경로(있으면 plan/feature draft 경로)와 이미 아는 결정을 수집한다 (wrapper는 새 분석 read를 하지 않는다).
2. `spawn_agent(agent_type="plan_review_agent", prompt=<요청 + 알려진 경로/컨텍스트>)`로 dispatch하고 `wait_agent`로 결과를 수거한다. 대상 경로가 불명확하면 agent가 Input Sources 우선순위로 자체 탐색하도록 위임한다.
3. agent의 반환(리포트 경로 `_sdd/implementation/<YYYY-MM-DD>_plan_review_<slug>.md`, Blocker Status, Critical/High 요약)을 사용자에게 그대로 relay한다.

## 계약 (entrypoint·artifact 유지, 흉내 금지)

- trigger(plan-review 호출)와 리포트 경로 계약은 이 wrapper가 유지한다.
- 실제 감사·리포트 작성은 agent가 수행한다. agent가 지원하지 않는 동작을 wrapper가 흉내내지 않는다.
- agent가 노출하는 Blocker(Critical/High)·구현 전 차단 이슈를 wrapper가 relay해 보존한다.

> Source: 전체 계약·6-smell·severity·출력 형식은 `.codex/agents/plan-review-agent.toml`이 단일 소스로 보유한다 (wrapper↔agent; 더 이상 동일 본문 mirror 아님).
