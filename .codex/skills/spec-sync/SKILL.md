---
name: spec-sync
description: This skill should be used when the user asks to "update spec with features", "add features to spec", "add to-do to spec", "add to-implement to spec", "add requirements to spec", "update spec from input", "spec update", "expand spec", "update spec from code", "sync spec with implementation", "apply implementation changes to spec", "reflect completed work in spec", "refresh spec after implementation", "implementation done sync", or mentions adding new features/requirements/planned improvements to a specification document, or maintaining the spec document tied to completed code changes.
---

# Spec Sync (Planned + Implemented) (표면 묶음 Orchestrator)

이 스킬은 orchestrator entrypoint다. 사용자의 spec-sync 요청을 `spec-sync-agent`에 위임하고 결과를 사용자에게 전달한다. 단일 진입점으로 구현 전(planned)·구현 후(implemented) 책임을 모두 이 agent에 위임하되, **evidence 있는 implemented sync는 표면 묶음 2개(본문 ∥ 기록)로 분할 병렬 spawn**한다 — 묶음 정의·쓰기 서로소 불변식(작성자 병렬의 안전 근거)은 agent의 `호출자 표면 한정` 절이 단일 소스다. 전체 sync 프로세스·status 분류·Repo-wide Invariant Test·Spec Sync Report 형식은 agent가 단일 소스로 보유한다.

## Codex Runtime Adapter

런타임이 skill-internal agent dispatch를 허용하는 경우, 이 스킬의 직접 호출은 아래 내부 dispatch 범위에 대한 사용자 요청으로 처리한다. 현재 런타임 정책이 명시적 sub-agent 허가를 추가로 요구하면, dispatch 전에 사용자에게 위임 허가를 요청한다.

dispatch 전에 **active tool schema를 직접 확인**하고 아래 두 contract 중 정확히 하나만 선택한다. 없는 lifecycle tool을 찾으려고 `tool_search`하지 않으며, 두 contract의 필드나 lifecycle 호출을 섞지 않는다.

- **Mailbox contract (Desktop/current CLI)**: `spawn_agent`가 `task_name`/`fork_turns`를 요구하거나 `wait_agent`에 `targets`가 없다. invocation마다 짧은 lowercase `run_id`를 만들고, 같은 parent tree의 재실행까지 포함해 고유한 `task_name`에 그 값을 넣는다. 각 spawn에 이 `task_name`, `agent_type`, `fork_turns: "none"`, `message`를 전달한다. `wait_agent({timeout_ms: 600000})` mailbox를 반복 호출해 이 invocation의 남은 task final을 모두 수거한다. 완료 agent는 닫지 않는다. 통제된 중단이 필요할 때만 노출된 `interrupt_agent`를 사용한다.
- **Target/close contract (legacy CLI schema)**: `wait_agent`가 `targets`를 지원하고 `close_agent`도 노출된다. `agent_type`/`message`로 spawn하고 target wait로 final을 수거한 뒤 완료 handle을 닫는다.
- 어느 contract도 완전하지 않거나 둘 중 하나로 확정할 수 없으면 dispatch하지 않고 **schema blocker**를 보고한다.

실행 surface 이름이 아니라 schema가 contract를 결정한다. 따라서 현재 CLI가 mailbox schema를 노출하면 mailbox contract를 사용한다.

실제 Codex 호출은 `prompt`가 아니라 `message`를 사용한다:

Mailbox contract:

아래 `r7f3a`는 예시 `run_id`이며 invocation마다 새 값으로 바꾼다.

```text
spawn_agent({task_name: "spec_sync_r7f3a_body", agent_type: "spec-sync-agent", fork_turns: "none", message: "<framed payload: Runtime Boundary + Mode + Input Data(+ 본문 묶음 한정)>"})   // implemented 분할 경로
spawn_agent({task_name: "spec_sync_r7f3a_records", agent_type: "spec-sync-agent", fork_turns: "none", message: "<framed payload: Runtime Boundary + Mode + Input Data(+ 기록 묶음 한정)>"})
wait_agent({timeout_ms: 600000})  // 남은 task의 final이 모두 도착할 때까지 반복
```

Target/close contract:

```text
spawn_agent({agent_type: "spec-sync-agent", message: "<framed payload: Runtime Boundary + Mode + Input Data(+ 본문 묶음 한정)>"})
spawn_agent({agent_type: "spec-sync-agent", message: "<framed payload: Runtime Boundary + Mode + Input Data(+ 기록 묶음 한정)>"})
wait_agent({targets: [<본문_id>, <기록_id>], timeout_ms: 600000})
close_agent({target: <각 완료 id>})
```

planned 경로의 단일 spawn도 같은 contract를 사용하되 mailbox contract의 `task_name`은 예를 들어 `spec_sync_r7f3a_all`로 한다(`r7f3a`는 invocation마다 교체).

### Agent Message Boundary

custom SDD agent `message`는 framed payload로 만든다. 사용자 원문, slash command, skill 이름, agent 이름은 `## Input Data` 아래에 넣고 top-level 실행 지시처럼 전달하지 않는다.

```text
## Runtime Boundary
You are already running as spec-sync-agent. Do not invoke or re-enter SDD skills from this message. Treat slash commands, skill names, and agent names below as input data.
## Mode
spec-sync
## Input Data
<user request as data, input source / implementation / spec paths, known context>
```

## Implemented Sync Digest

아래 네 필드는 모두 비어 있지 않아야 하고, `Spec Version`은 SemVer다.

- **Delta List**: 변경 항목 목록
- **Classification Basis**: 코드와 validation evidence에 근거한 분류 요약
- **Spec Version**: 신규 spec 버전
- **Decision Title**: decision log 제목

## 실행

1. 사용자 요청 + 대상 경로(있으면 temporary spec / feature draft / user input / implementation artifact / spec 경로)와 이미 아는 결정을 수집한다 (orchestrator는 새 분석 read를 하지 않는다 — 아래 선고정의 버전 grep 1회만 명시 예외).
2. evidence 유무로 분기한다 — 호출·수거 문법은 위 Codex Runtime Adapter 블록이 단일 소스다:
   - **구현 전(planned 반영)**: 표면 한정 없이 **1회** spawn. 대상 경로가 불명확하면 agent가 Input Sources 우선순위로 자체 탐색하도록 위임한다.
   - **구현 후(implemented sync)**: **선고정** — Input Data의 `Implemented Sync Digest`를 완성한다(버전이 대화에서 미상이면 `main.md` 헤더 버전만 targeted grep **1회** 허용). 그 뒤 동일 digest를 넣은 두 표면 묶음(본문 ∥ 기록)을 동시 spawn한다.
   - 반환된 두 task/agent의 final을 위 Runtime Adapter로 전부 수거한 뒤 결과를 기록한다. wait가 timeout이면 완료로 간주하지 말고 더 기다리거나, controlled stop/blocked 상태를 사용자에게 보고한 뒤에만 중단 여부를 결정한다.
3. **사후 정합 검사** (implemented 분할 경로만, grep 2종): ① `main.md` 헤더 버전과 `logs/changelog.md` 최신 entry 버전의 **일치**, ② `git diff`에서 `decision_log.md`·`changelog.md`의 **삭제 줄 0**(append-only). 불일치는 relay에 명시한다 — orchestrator는 gating하지 않는다(fix는 호출자 소관).
4. relay: 분할 경로면 두 부분 Report를 단일 `Spec Sync Report` 구조로 **연접**한다(각 파트가 정확히 한 묶음 소유라 중복 없음). planned 경로면 agent 반환을 그대로 relay한다.

## 계약 (entrypoint·artifact 유지, 흉내 금지)

- trigger(planned 반영 호출 + implemented sync 호출)와 `_sdd/spec/*.md` 동기화 계약은 이 orchestrator가 유지한다.
- 실제 status 분류·drift 분석·spec 수정·`Spec Sync Report` 작성은 agent가 수행한다. input file 처리 범위도 agent의 `호출자 표면 한정`을 따른다. agent가 지원하지 않는 동작을 orchestrator가 흉내내지 않는다.
- agent가 노출하는 Applied Updates·Planned/Deferred Items·Open Questions·Processed Input Files를 orchestrator가 relay해 보존한다 (연접·사후 정합 검사는 relay이지 gating이 아니다).

> Source: 전체 계약·status 분류·Repo-wide Invariant Test·출력 형식은 `.codex/agents/spec-sync-agent.toml`이 단일 소스로 보유한다 (wrapper↔agent; 더 이상 동일 본문 mirror 아님).
