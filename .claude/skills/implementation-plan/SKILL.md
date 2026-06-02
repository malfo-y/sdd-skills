---
name: implementation-plan
description: This skill should be used when the user asks to "create an implementation plan", "plan the implementation", "break down this spec", "create a development roadmap", "analyze requirements and create tasks", "create a parallel implementation plan", "plan parallel implementation", "병렬 구현 계획", "create parallel development roadmap", or wants a structured implementation plan with Target Files for parallel execution support.
version: 3.0.0
---

# Implementation Plan (Entrypoint Wrapper)

이 스킬은 entrypoint wrapper다. 사용자의 implementation-plan 요청을 `sdd-skills:implementation-plan-agent`에 위임하고 그 결과를 사용자에게 전달한다. 전체 계획 프로세스·Target Files 규칙·phase metadata·plan 출력 형식은 agent가 단일 소스로 보유한다.

## 실행 (Mode A: pass-through)

1. 사용자 요청 + 계획 입력 경로(있으면 feature draft / temporary spec 경로)와 이미 아는 결정을 수집한다 (wrapper는 새 분석 read를 하지 않는다).
2. `Agent(subagent_type="sdd-skills:implementation-plan-agent", prompt=<요청 + 알려진 경로/컨텍스트>)`로 dispatch한다. 입력 경로가 불명확하면 agent가 Input Sources 우선순위로 자체 탐색하도록 위임한다.
3. agent의 반환(plan 경로 `_sdd/implementation/<YYYY-MM-DD>_implementation_plan_<slug>.md`, phase/task 요약, Open Questions 중 LOW/Yes 항목)을 사용자에게 그대로 relay한다.

## 계약 (entrypoint·artifact 유지, 흉내 금지)

- trigger(implementation-plan 호출)와 plan 경로 계약은 이 wrapper가 유지한다.
- 실제 task 분해·plan 작성은 agent가 수행한다. agent가 지원하지 않는 동작을 wrapper가 흉내내지 않는다.
- agent가 노출하는 Open Questions(Confidence=LOW / User confirmation needed=Yes)를 wrapper가 relay해 보존한다.

> Source: 전체 계약·프로세스·Target Files 규칙·출력 형식은 `.claude/agents/implementation-plan-agent.md`가 단일 소스로 보유한다 (wrapper↔agent; 더 이상 동일 본문 mirror 아님).
