---
name: spec-update-done
description: This skill should be used when the user asks to "update spec from code", "sync spec with implementation", "apply implementation changes to spec", "reflect completed work in spec", "refresh spec after implementation", "implementation done sync", or mentions spec document maintenance tied to completed code changes.
version: 3.0.0
---

# Spec Update (Done) (Entrypoint Wrapper)

이 스킬은 entrypoint wrapper다. 사용자의 spec-update-done 요청을 `sdd-skills:spec-update-done-agent`에 위임하고 그 결과를 사용자에게 전달한다. 전체 sync 프로세스·drift 분류·Repo-wide Invariant Test·Change Report 형식은 agent가 단일 소스로 보유한다.

## 실행 (Mode A: pass-through)

1. 사용자 요청 + 대상 경로(있으면 feature draft / implementation artifact / spec 경로)와 이미 아는 결정을 수집한다 (wrapper는 새 분석 read를 하지 않는다).
2. `Agent(subagent_type="sdd-skills:spec-update-done-agent", prompt=<요청 + 알려진 경로/컨텍스트>)`로 dispatch한다. 대상 경로가 불명확하면 agent가 Input Sources 우선순위로 자체 탐색하도록 위임한다.
3. agent의 반환(갱신한 `_sdd/spec/*.md` 파일 목록, Spec Sync Report 변경 요약, Deferred/Open Questions)을 사용자에게 그대로 relay한다.

## 계약 (entrypoint·artifact 유지, 흉내 금지)

- trigger(spec-update-done 호출)와 `_sdd/spec/*.md` 동기화 계약은 이 wrapper가 유지한다.
- 실제 drift 분석·spec 수정·Change Report 작성은 agent가 수행한다. agent가 지원하지 않는 동작을 wrapper가 흉내내지 않는다.
- agent가 노출하는 Applied Updates·Deferred Items·Open Questions를 wrapper가 relay해 보존한다.

> Source: 전체 계약·drift 분류·Repo-wide Invariant Test·출력 형식은 `.claude/agents/spec-update-done-agent.md`가 단일 소스로 보유한다 (wrapper↔agent; 더 이상 동일 본문 mirror 아님).
