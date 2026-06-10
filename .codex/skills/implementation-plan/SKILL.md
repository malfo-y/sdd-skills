---
name: implementation-plan
description: This skill should be used when the user asks to "create an implementation plan", "plan the implementation", "break down this spec", "create a development roadmap", "analyze requirements and create tasks", "create a parallel implementation plan", "plan parallel implementation", "병렬 구현 계획", "create parallel development roadmap", or wants a structured implementation plan with Target Files for parallel execution support.
version: 4.0.0
---

# Implementation Plan (Orchestrator)

이 스킬은 **메인 루프 orchestrator**다. `implementation-plan-agent`를 spawn해 plan을 생성하고, `plan-review-agent`로 **review→fix→re-review loop**를 돌려 산출물 품질 gate를 자체 소유한다. agent는 plan producer 단일 소스이고 스킬이 loop를 소유한다 — producer/reviewer agent는 sub-agent를 spawn하지 못하므로 loop orchestration은 메인 루프(스킬)의 책임이다.

implementation-plan은 입력이 파일/경로에서 태어난다. 대화 맥락 digest forwarding을 두지 않는다 — agent가 입력 경로를 자체 read한다.

## Codex Runtime Adapter

런타임이 skill-internal agent dispatch를 허용하는 경우, 이 스킬의 직접 호출은 이 스킬 내부의 `implementation-plan-agent` / `plan-review-agent` dispatch 범위에 대한 사용자 요청으로 처리한다. dispatch 전에 `spawn_agent`, `wait_agent`, `close_agent`가 active tools에 없으면 `tool_search` query `spawn_agent wait_agent close_agent multi-agent sub-agent`로 multi-agent tools를 먼저 로드한다. 현재 런타임 정책이 명시적 sub-agent 허가를 추가로 요구하면, dispatch 전에 사용자에게 위임 허가를 요청한다.

실제 Codex 호출은 `prompt`가 아니라 `message`를 사용한다. 아래는 호출 형태 예시이며, 실제 실행 순서는 Process를 따른다:

```text
spawn_agent({agent_type: "implementation-plan-agent", message: "<요청 + 알려진 경로/컨텍스트>"})
spawn_agent({agent_type: "plan-review-agent", message: "<plan 경로 + review 요청>"})
wait_agent({targets: ["<agent_id>"], timeout_ms: 600000})
close_agent({target: "<agent_id>"})
```

## Process

### Step 1: 입력 수집

사용자 요청 + 계획 입력 경로(있으면 feature draft / temporary spec 경로)와 이미 아는 결정을 수집한다. 입력 경로가 불명확하면 agent가 Input Sources 우선순위로 자체 탐색하도록 위임한다(스킬은 새 분석 read를 하지 않는다).

### Step 2: 생성 (producer spawn)

`spawn_agent({agent_type: "implementation-plan-agent", message: <요청 + 알려진 경로/컨텍스트>})`로 **생성 mode** spawn하고 `wait_agent`로 final status를 수거한다. final status가 반환된 뒤에만 결과를 기록하고 `close_agent({target: <agent_id>})`로 producer handle을 닫는다. `wait_agent`가 timeout이면 완료로 간주하지 말고 더 기다리거나, controlled stop/blocked 상태를 사용자에게 보고한 뒤에만 handle 정리를 결정한다. agent가 plan을 `_sdd/implementation/<YYYY-MM-DD>_implementation_plan_<slug>.md`에 저장하고 경로 + phase/task 요약 + Open Questions(LOW/Yes)를 반환한다.

### Step 3: review-fix loop

산출 직후 review→fix→re-review loop를 닫는다. **공통 loop 정책**(autopilot `references/orchestrator-contract.md` §6 Review-Fix Contract 차용):

- **exit 조건**: `critical=high=medium=0`.
- **MAX**: 기본 3 iteration.
- **re-review scope**: loop 범위(plan) **전체 재리뷰** (변경분만 아님).
- **1 iteration 경계**: `review/re-review → finding>0이면 fix → 산출물 갱신`.
- **MAX 도달 분기**: critical/high 잔존 → 중단·사용자 보고. medium만 잔존 → 로그 후 진행(advisory degrade).

단계:

1. **review**: `spawn_agent({agent_type: "plan-review-agent", message: <plan 경로 + review 요청>})`로 plan을 review하고 `wait_agent`로 final status를 수거한다. final status가 반환된 뒤에만 결과를 기록하고 `close_agent({target: <agent_id>})`로 reviewer handle을 닫는다(Tier 1 — implementation plan 입력). reviewer가 Blocker Status + severity별 finding을 리포트(`_sdd/implementation/<YYYY-MM-DD>_plan_review_<slug>.md`)로 낸다.
2. **fix**: critical/high/medium finding이 있으면 `spawn_agent({agent_type: "implementation-plan-agent", message: <review 리포트 경로 + plan 경로 + 대상 findings>})`로 **fix mode** 재spawn한다. `wait_agent`로 final status를 수거하고, final status가 반환된 뒤에만 결과를 기록한 후 `close_agent({target: <agent_id>})`로 producer handle을 닫는다. agent가 finding 부분만 surgical 수정한다.
3. **re-review**: fix 후 loop 범위 전체를 `plan-review-agent`로 재리뷰한다.
4. exit 충족 또는 MAX 도달까지 1~3을 반복한다. MAX 분기 적용.

### Step 4: relay

최종 plan 경로 + phase/task 요약 + Open Questions(LOW/Yes) + loop 결과(iteration 수, 최종 Blocker Status, 잔존 advisory)를 사용자에게 relay한다.

## 경계

- 산출물(plan) 작성·수정은 `implementation-plan-agent`만 한다(산출물 단일 작성자 — orchestrator는 직접 rewrite하지 않는다). 스킬은 loop만 소유한다.
- review·findings 분류는 `plan-review-agent`가 수행한다(중복 금지).

> **Role Pointer**: 이 스킬은 review-fix loop를 소유하는 **orchestrator**다. `implementation-plan-agent`는 plan producer 단일 소스(생성·fix mode 수정), `plan-review-agent`는 reviewer다. (구 entrypoint 형태에서 orchestrator로 승격됨 — 더 이상 단순 위임이 아니다.)
