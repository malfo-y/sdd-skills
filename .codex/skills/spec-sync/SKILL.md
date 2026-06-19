---
name: spec-sync
description: This skill should be used when the user asks to "update spec with features", "add features to spec", "add to-do to spec", "add to-implement to spec", "add requirements to spec", "update spec from input", "spec update", "expand spec", "update spec from code", "sync spec with implementation", "apply implementation changes to spec", "reflect completed work in spec", "refresh spec after implementation", "implementation done sync", or mentions adding new features/requirements/planned improvements to a specification document, or maintaining the spec document tied to completed code changes.
version: 3.0.0
---

# Spec Sync (Planned + Implemented) (Entrypoint Wrapper)

이 스킬은 entrypoint wrapper다. 사용자의 spec-sync 요청을 `spec-sync-agent`에 위임하고 결과를 사용자에게 전달한다. 단일 진입점으로 구현 전(planned)·구현 후(implemented) 책임을 모두 이 agent에 위임한다. 전체 sync 프로세스·status 분류·Repo-wide Invariant Test·Spec Sync Report 형식은 agent가 단일 소스로 보유한다.

## Codex Runtime Adapter

런타임이 skill-internal agent dispatch를 허용하는 경우, 이 스킬의 직접 호출은 아래 내부 dispatch 범위에 대한 사용자 요청으로 처리한다. dispatch 전에 `spawn_agent`, `wait_agent`, `close_agent`가 active tools에 없으면 `tool_search` query `spawn_agent wait_agent close_agent multi-agent sub-agent`로 multi-agent tools를 먼저 로드한다. 현재 런타임 정책이 명시적 sub-agent 허가를 추가로 요구하면, dispatch 전에 사용자에게 위임 허가를 요청한다.

실제 Codex 호출은 `prompt`가 아니라 `message`를 사용한다:

```text
spawn_agent({agent_type: "spec-sync-agent", message: "<framed payload: Runtime Boundary + Mode + Input Data>"})
wait_agent({targets: ["<agent_id>"], timeout_ms: 600000})
close_agent({target: "<agent_id>"})
```

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

## 실행

1. 사용자 요청 + 대상 경로(있으면 temporary spec / feature draft / user input / implementation artifact / spec 경로)와 이미 아는 결정을 수집한다 (wrapper는 새 분석 read를 하지 않는다).
2. `spawn_agent({agent_type: "spec-sync-agent", message: <framed payload: Runtime Boundary + spec-sync mode + Input Data(사용자 요청 data, 알려진 경로/컨텍스트)>})`로 dispatch하고 `wait_agent`로 final status를 수거한다. final status가 반환된 뒤에만 결과를 기록하고 `close_agent({target: <agent_id>})`로 handle을 닫는다. `wait_agent`가 timeout이면 완료로 간주하지 말고 더 기다리거나, controlled stop/blocked 상태를 사용자에게 보고한 뒤에만 handle 정리를 결정한다. 대상 경로가 불명확하면 agent가 Input Sources 우선순위로 자체 탐색하고, evidence 유무로 구현 전/후 동작을 자동 결정하도록 위임한다.
3. agent의 반환(갱신한 `_sdd/spec/*.md` 파일 목록, `Spec Sync Report` 변경 요약, `_processed_*` 마킹, Deferred / Open Questions)을 사용자에게 그대로 relay한다.

## 계약 (entrypoint·artifact 유지, 흉내 금지)

- trigger(planned 반영 호출 + implemented sync 호출)와 `_sdd/spec/*.md` 동기화 계약은 이 wrapper가 유지한다.
- 실제 status 분류·drift 분석·spec 수정·`Spec Sync Report` 작성·`_processed_*` 마킹은 agent가 수행한다. agent가 지원하지 않는 동작을 wrapper가 흉내내지 않는다.
- agent가 노출하는 Applied Updates·Planned/Deferred Items·Open Questions·Processed Input Files를 wrapper가 relay해 보존한다.

> Source: 전체 계약·status 분류·Repo-wide Invariant Test·출력 형식은 `.codex/agents/spec-sync-agent.toml`이 단일 소스로 보유한다 (wrapper↔agent; 더 이상 동일 본문 mirror 아님).
