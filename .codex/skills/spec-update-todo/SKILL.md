---
name: spec-update-todo
description: This skill should be used when the user asks to "update spec with features", "add features to spec", "update spec from input", "add requirements to spec", "spec update", "expand spec", "add to-do to spec", "add to-implement to spec", or mentions adding new features, requirements, or planned improvements to an existing specification document.
version: 3.0.0
---

# Spec Update (To-do) (Entrypoint Wrapper)

이 스킬은 entrypoint wrapper다. 사용자의 spec-update-todo 요청을 `spec_update_todo_agent`에 위임하고 그 결과를 사용자에게 전달한다. 전체 프로세스·Hard Rules·Repo-wide Invariant Test·매핑 규칙·출력 형식은 agent가 단일 소스로 보유한다.

## 실행

1. 사용자 요청 + 입력 소스 경로(있으면 temporary spec / feature draft / user input 경로)와 이미 아는 결정을 수집한다 (wrapper는 새 분석 read를 하지 않는다).
2. `spawn_agent(agent_type="spec_update_todo_agent", prompt=<요청 + 알려진 경로/컨텍스트>)`로 dispatch하고 `wait_agent`로 결과를 수거한 뒤 `close_agent(target=<agent_id>)`로 handle을 닫는다. 입력 소스가 불명확하면 agent가 Input Sources 우선순위로 자체 탐색하도록 위임한다.
3. agent의 반환(갱신한 `_sdd/spec/*.md` 파일·반영/제외 요약·남은 open questions·`_processed_*` 마킹)을 사용자에게 그대로 relay한다.

## 계약 (entrypoint·artifact 유지, 흉내 금지)

- trigger(spec-update-todo 호출)와 `_sdd/spec/*.md` 갱신 계약은 이 wrapper가 유지한다.
- 실제 spec 갱신은 agent가 수행한다. agent가 지원하지 않는 동작을 wrapper가 흉내내지 않는다.
- agent가 노출하는 planned/implemented 분리, open questions, spec drift 경고를 wrapper가 relay해 보존한다.

> Source: 전체 계약·Hard Rules·Repo-wide Invariant Test·매핑 규칙·출력 형식은 `.codex/agents/spec-update-todo-agent.toml`이 단일 소스로 보유한다 (wrapper↔agent; 더 이상 동일 본문 mirror 아님).
