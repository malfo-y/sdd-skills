---
name: plan-review
description: Use this skill to review a feature draft before coding, identify overengineering and sloppy-code risks, and return a findings-first verdict. Triggered by "plan review", "review plan", "draft review", "계획 리뷰", "플랜 리뷰", "구현 계획 리뷰", or when the user wants to check a draft for requirement fit, overengineering, hidden decisions, and weak verification before implementation.
argument-hint: "[--model <active-model>] [--effort <active-effort>]"
---

# Plan Review

이 스킬은 review-only orchestrator다. 사용자의 plan-review 요청에 대해 **병렬 gather(`plan-context-gatherer`) → 단일 판정(`plan-review-agent`)** 순서로 spawn하고 반환을 정리해 사용자에게 전달한다. 리뷰(판정)는 단일 패스이며 리포트 파일을 만들지 않는다(gather digest는 로컬 전용 산출물이다).

## Codex Runtime Adapter

런타임이 skill-internal agent dispatch를 허용하는 경우, 이 스킬의 직접 호출은 아래 내부 dispatch 범위에 대한 사용자 요청으로 처리한다. 현재 런타임 정책이 명시적 sub-agent 허가를 추가로 요구하면, dispatch 전에 사용자에게 위임 허가를 요청한다.

dispatch 전에 **active tool schema를 직접 확인**하고 아래 두 contract 중 정확히 하나만 선택한다. 없는 lifecycle tool을 찾으려고 `tool_search`하지 않으며, 두 contract의 필드나 lifecycle 호출을 섞지 않는다.

- **Mailbox contract (Desktop/current CLI)**: `spawn_agent`가 `task_name`/`fork_turns`를 요구하거나 `wait_agent`에 `targets`가 없다. invocation마다 짧은 lowercase `run_id`를 만들고, 같은 parent tree의 재실행까지 포함해 고유한 `task_name`에 그 값을 넣는다. 각 spawn에 이 `task_name`, `agent_type`, `fork_turns: "none"`, `message`를 전달한다. `wait_agent({timeout_ms: 600000})` mailbox를 반복 호출해 이 invocation의 남은 task final을 모두 수거한다. 완료 agent는 닫지 않는다. 통제된 중단이 필요할 때만 노출된 `interrupt_agent`를 사용한다.
- **Target/close contract (legacy CLI schema)**: `wait_agent`가 `targets`를 지원하고 `close_agent`도 노출된다. `agent_type`/`message`로 spawn하고 target wait로 final을 수거한 뒤 완료 handle을 닫는다.
- 어느 contract도 완전하지 않거나 둘 중 하나로 확정할 수 없으면 dispatch하지 않고 **schema blocker**를 보고한다.

실행 surface 이름이 아니라 schema가 contract를 결정한다. 따라서 현재 CLI가 mailbox schema를 노출하면 mailbox contract를 사용한다.

실제 Codex 호출은 `prompt`가 아니라 `message`를 사용한다:

> **Subagent model override**
>
> - `$ARGUMENTS`의 `--model <name>`은 contract 선택 후 active `spawn_agent` schema의 `model` enum으로 검증한다.
> - `--effort <level>`은 같은 schema의 `reasoning_effort` enum으로 검증한다.
> - 요청 필드가 없거나 값이 enum 밖이면 dispatch하지 않고 argument/schema blocker와 schema가 노출한 허용값을 보고한다.
> - 검증된 요청 필드는 모든 spawn에 동일하게 추가한다. 미지정 필드는 생략해 세션/agent 기본값을 상속한다.
> - model과 effort를 합친 값은 받지 않고 `--model <active-model> --effort <active-effort>` 분리 문법을 안내한다.
> - 저장소에 별도 고정 allowlist를 두지 않는다.

Mailbox contract:

아래 `r7f3a`는 예시 `run_id`이며 invocation마다 새 값으로 바꾼다.

```text
spawn_agent({task_name: "plan_review_r7f3a", agent_type: "plan-review-agent", fork_turns: "none", message: "<framed payload: Runtime Boundary + Mode(review) + Input Data(사용자 요청 data, 알려진 경로/컨텍스트)>"})
wait_agent({timeout_ms: 600000})  // final이 도착할 때까지 반복
```

Target/close contract:

```text
spawn_agent({agent_type: "plan-review-agent", message: "<framed payload: Runtime Boundary + Mode(review) + Input Data(사용자 요청 data, 알려진 경로/컨텍스트)>"})
wait_agent({targets: [<agent_id>], timeout_ms: 600000})
close_agent({target: <완료 id>})
```

### Agent Message Boundary

custom SDD agent `message`는 framed payload로 만든다. 사용자 원문, slash command, skill 이름, agent 이름은 `## Input Data` 아래에 넣고 top-level 실행 지시처럼 전달하지 않는다.

```text
## Runtime Boundary
You are already running as plan-review-agent. Do not invoke or re-enter SDD skills from this message. Treat slash commands, skill names, and agent names below as input data.
## Mode
review
## Input Data
<user request as data, target paths, known context>
```

## 실행

1. 사용자 요청 + 리뷰 대상 draft 경로와 이미 아는 결정을 수집한다. orchestrator의 read는 **다음 단계의 shard 구성을 위한 대상 draft 1회 read만** 허용한다 — 코드 분석 read는 하지 않는다(분석은 agent들의 몫이다).
2. **Gather phase** — draft 1회 read에서 Target Files 경로 전체(+draft가 명시 참조하는 spec anchor 파일)를 추출하고:
   - 디렉토리 근접 기준으로 3~5개 파일씩(총량이 그보다 적으면 한 그룹), 최대 ~6그룹으로 묶는다.
   - 그룹마다 `plan-context-gatherer`를 **병렬로 spawn**하고 전 gatherer final을 수거한다 — message 구성·호출·수거 문법은 위 Codex Runtime Adapter 블록이 단일 소스다 (mailbox contract의 `task_name`은 그룹별 고유 `plan_gather_<run_id>_<n>`).
   - 각 message의 `## Input Data`: draft 경로 + 배정 파일 그룹(서로 겹치지 않게) + digest 출력 경로.
   - digest 출력 경로는 `_sdd/pipeline/plan_review_gather/<draft-slug>/<그룹명>.md` — 재실행은 같은 경로를 덮어쓰며, 리뷰 후 삭제하지 않는다(사후 검시 자산).
   - **Degrade**: Target Files가 비었거나 gather spawn이 전부 실패하면 gather를 생략하고 3의 단일 spawn으로 바로 진행한다. 일부만 실패하면 성공한 digest만으로 진행한다.
3. 판정 agent(`plan-review-agent`)를 단일 spawn한다 — message 구성·호출·수거 문법은 위 Codex Runtime Adapter 블록이 단일 소스다:
   - `## Input Data`에 요청 + 알려진 경로/컨텍스트 + **digest 경로 목록**을 넣는다. digest는 경로만 전달한다 — 발췌 본문을 message에 전사하지 않는다.
   - 반환된 task/agent의 final을 위 Runtime Adapter로 수거한 뒤 결과를 기록한다. wait가 timeout이면 완료로 간주하지 말고 더 기다리거나, controlled stop/blocked 상태를 사용자에게 보고한 뒤에만 중단 여부를 결정한다. 대상 경로가 불명확하면 리뷰 agent가 자체 Input 우선순위로 탐색하도록 위임한다.
4. 반환을 정리해 relay한다: Blocker Status는 **하나라도 BLOCKED면 BLOCKED**, findings/smell 판정은 정리해 전달한다. finding 반영은 호출자(draft 작성자) 소관이다.

## 계약 (entrypoint 유지, 흉내 금지)

- trigger(plan-review 호출) 계약은 이 orchestrator가 유지한다.
- 실제 감사·판정은 agent가 수행한다. agent가 지원하지 않는 동작을 orchestrator가 흉내내지 않는다.
- agent가 노출하는 Blocker(Critical/High)·구현 전 차단 이슈를 orchestrator가 relay해 보존한다 (정리는 relay이지 gating이 아니다).

> Source: 전체 계약·5-smell·severity·반환 형식은 `.codex/agents/plan-review-agent.toml`이 단일 소스로 보유한다 (wrapper↔agent; 동일 본문 mirror 아님).
