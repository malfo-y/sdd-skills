---
name: plan-review
description: Use this skill to review an implementation plan before coding, identify overengineering and sloppy-code risks, and produce a findings-first plan review report. Triggered by "plan review", "review plan", "implementation plan review", "계획 리뷰", "플랜 리뷰", "구현 계획 리뷰", or when the user wants to check a plan against KISS/YAGNI/DRY/minimum-code principles before implementation.
version: 2.1.0
---

# Plan Review (Entrypoint Wrapper)

이 스킬은 entrypoint wrapper다. 사용자의 plan-review 요청을 `plan-review-agent`에 위임하고 결과를 사용자에게 전달한다. 전체 리뷰 프로세스·6-smell rubric·severity·리포트 형식은 agent가 단일 소스로 보유한다.

## Codex Runtime Adapter

런타임이 skill-internal agent dispatch를 허용하는 경우, 이 스킬의 직접 호출은 아래 내부 dispatch 범위에 대한 사용자 요청으로 처리한다. dispatch 전에 `spawn_agent`, `wait_agent`, `close_agent`가 active tools에 없으면 `tool_search` query `spawn_agent wait_agent close_agent multi-agent sub-agent`로 multi-agent tools를 먼저 로드한다. 현재 런타임 정책이 명시적 sub-agent 허가를 추가로 요구하면, dispatch 전에 사용자에게 위임 허가를 요청한다.

실제 Codex 호출은 `prompt`가 아니라 `message`를 사용한다:

```text
spawn_agent({agent_type: "plan-review-agent", message: "<요청 + 알려진 경로/컨텍스트>"})
wait_agent({targets: ["<agent_id>"], timeout_ms: 600000})
close_agent({target: "<agent_id>"})
```

## 실행

1. 사용자 요청 + 리뷰 대상 경로(있으면 plan/feature draft 경로)와 이미 아는 결정을 수집한다 (wrapper는 새 분석 read를 하지 않는다).
2. `spawn_agent({agent_type: "plan-review-agent", message: <요청 + 알려진 경로/컨텍스트>})`로 dispatch하고 `wait_agent`로 final status를 수거한다. final status가 반환된 뒤에만 결과를 기록하고 `close_agent({target: <agent_id>})`로 handle을 닫는다. `wait_agent`가 timeout이면 완료로 간주하지 말고 더 기다리거나, controlled stop/blocked 상태를 사용자에게 보고한 뒤에만 handle 정리를 결정한다. 대상 경로가 불명확하면 agent가 Input Sources 우선순위로 자체 탐색하도록 위임한다.
3. agent의 반환(리포트 경로 `_sdd/implementation/<YYYY-MM-DD>_plan_review_<slug>.md`, Blocker Status, Critical/High 요약)을 사용자에게 그대로 relay한다.

## 계약 (entrypoint·artifact 유지, 흉내 금지)

- trigger(plan-review 호출)와 리포트 경로 계약은 이 wrapper가 유지한다.
- 실제 감사·리포트 작성은 agent가 수행한다. agent가 지원하지 않는 동작을 wrapper가 흉내내지 않는다.
- agent가 노출하는 Blocker(Critical/High)·구현 전 차단 이슈를 wrapper가 relay해 보존한다.

> Source: 전체 계약·6-smell·severity·출력 형식은 `.codex/agents/plan-review-agent.toml`이 단일 소스로 보유한다 (wrapper↔agent; 더 이상 동일 본문 mirror 아님).
