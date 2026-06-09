---
name: spec-update-done
description: This skill should be used when the user asks to "update spec from code", "sync spec with implementation", "apply implementation changes to spec", "reflect completed work in spec", "refresh spec after implementation", "implementation done sync", or mentions spec document maintenance tied to completed code changes.
version: 3.0.0
---

# Spec Update (Done) (Entrypoint Wrapper)

이 스킬은 entrypoint wrapper다. 사용자의 spec-update-done 요청을 `spec-update-done-agent`에 위임하고 그 결과를 사용자에게 전달한다. 전체 sync 프로세스·drift 분류·Repo-wide Invariant Test·Change Report 형식은 agent가 단일 소스로 보유한다.

## Codex Runtime Adapter

이 스킬의 직접 호출은 아래 내부 agent dispatch에 대한 사용자 명시 허가로 간주한다. dispatch 전에 `spawn_agent`, `wait_agent`, `close_agent`가 active tools에 없으면 `tool_search` query `spawn_agent wait_agent close_agent multi-agent sub-agent`로 multi-agent tools를 먼저 로드한다.

실제 Codex 호출은 `prompt`가 아니라 `message`를 사용한다:

```text
spawn_agent({agent_type: "spec-update-done-agent", message: "<요청 + 알려진 경로/컨텍스트>"})
wait_agent({targets: ["<agent_id>"], timeout_ms: 600000})
close_agent({target: "<agent_id>"})
```

## 실행

1. 사용자 요청 + 대상 경로(있으면 feature draft / implementation artifact / spec 경로)와 이미 아는 결정을 수집한다 (wrapper는 새 분석 read를 하지 않는다).
2. `spawn_agent({agent_type: "spec-update-done-agent", message: <요청 + 알려진 경로/컨텍스트>})`로 dispatch하고 `wait_agent`로 결과를 수거한 뒤 `close_agent({target: <agent_id>})`로 handle을 닫는다. 대상 경로가 불명확하면 agent가 Input Sources 우선순위로 자체 탐색하도록 위임한다.
3. agent의 반환(갱신한 `_sdd/spec/*.md` 파일 목록, Spec Sync Report 변경 요약, Deferred/Open Questions)을 사용자에게 그대로 relay한다.

## 계약 (entrypoint·artifact 유지, 흉내 금지)

- trigger(spec-update-done 호출)와 `_sdd/spec/*.md` 동기화 계약은 이 wrapper가 유지한다.
- 실제 drift 분석·spec 수정·Change Report 작성은 agent가 수행한다. agent가 지원하지 않는 동작을 wrapper가 흉내내지 않는다.
- agent가 노출하는 Applied Updates·Deferred Items·Open Questions를 wrapper가 relay해 보존한다.

> Source: 전체 계약·drift 분류·Repo-wide Invariant Test·출력 형식은 `.codex/agents/spec-update-done-agent.toml`이 단일 소스로 보유한다 (wrapper↔agent; 더 이상 동일 본문 mirror 아님).
