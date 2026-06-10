---
name: ralph-loop-init
description: Use this skill when the user asks to "init ralph", "ralph loop", "set up ralph loop", "training loop", "training debug loop", "debug loop", "long-running test loop", "e2e loop", "create ralph", "set up training debug loop", "automated training loop", or wants to generate a ralph/ directory for LLM-driven automated long-running process debugging.
version: 3.1.0
---

# Ralph Loop Init (Entrypoint Wrapper)

이 스킬은 entrypoint wrapper다. 사용자의 ralph-loop-init 요청을 `ralph-loop-init-agent`에 위임하고 결과를 사용자에게 전달한다. 전체 discovery 프로세스·상태 머신·파일 생성·CHECKS 검증·출력 형식은 agent가 단일 소스로 보유한다.

> **Security Notice**: 생성된 `run.sh`는 Codex CLI의 `--dangerously-bypass-approvals-and-sandbox`를 사용한다. **격리된 환경(컨테이너, VM, 샌드박스)에서만 실행할 것.**

## Codex Runtime Adapter

런타임이 skill-internal agent dispatch를 허용하는 경우, 이 스킬의 직접 호출은 아래 내부 dispatch 범위에 대한 사용자 요청으로 처리한다. dispatch 전에 `spawn_agent`, `wait_agent`, `close_agent`가 active tools에 없으면 `tool_search` query `spawn_agent wait_agent close_agent multi-agent sub-agent`로 multi-agent tools를 먼저 로드한다. 현재 런타임 정책이 명시적 sub-agent 허가를 추가로 요구하면, dispatch 전에 사용자에게 위임 허가를 요청한다.

실제 Codex 호출은 `prompt`가 아니라 `message`를 사용한다:

```text
spawn_agent({agent_type: "ralph-loop-init-agent", message: "<요청 + 알려진 진입점/환경 컨텍스트>"})
wait_agent({targets: ["<agent_id>"], timeout_ms: 600000})
close_agent({target: "<agent_id>"})
```

## 실행

1. 사용자 요청 + 대상 프로세스/진입점 컨텍스트와 이미 아는 결정을 수집한다 (wrapper는 새 분석 read를 하지 않는다).
2. `spawn_agent({agent_type: "ralph-loop-init-agent", message: <요청 + 알려진 진입점/환경 컨텍스트>})`로 dispatch하고 `wait_agent`로 final status를 수거한다. final status가 반환된 뒤에만 결과를 기록하고 `close_agent({target: <agent_id>})`로 handle을 닫는다. `wait_agent`가 timeout이면 완료로 간주하지 말고 더 기다리거나, controlled stop/blocked 상태를 사용자에게 보고한 뒤에만 handle 정리를 결정한다. 진입점이 불명확하면 agent가 Step 1 discovery로 자체 탐색하도록 위임한다.
3. agent의 반환(생성된 `ralph/` 산출물 — `config.sh`, `PROMPT.md`, `run.sh`, `state.md`, `CHECKS.md`, `results/` — 경로와 CHECKS 검증 요약, next steps)을 사용자에게 그대로 relay한다.

## 계약 (entrypoint·artifact 유지, 흉내 금지)

- trigger(ralph-loop-init 호출)와 `ralph/` 산출물 경로 계약은 이 wrapper가 유지한다.
- 실제 discovery·파일 생성·CHECKS 검증은 agent가 수행한다. agent가 지원하지 않는 동작을 wrapper가 흉내내지 않는다.
- agent가 노출하는 가정·미충족 CHECKS·에스컬레이션을 wrapper가 relay해 보존한다.

> Source: 전체 계약·상태 머신·run.sh 템플릿·출력 형식은 `.codex/agents/ralph-loop-init-agent.toml`이 단일 소스로 보유한다 (wrapper↔agent; 더 이상 동일 본문 mirror 아님).
