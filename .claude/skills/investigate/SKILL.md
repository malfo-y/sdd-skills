---
name: investigate
description: "Use this skill when the user asks to \"investigate\", \"debug\", \"find root cause\", \"diagnose\", \"why is this failing\", \"track down bug\", \"근본원인 분석\", \"디버깅\", or wants systematic one-shot debugging of a specific issue. For long-running iterative debugging processes, use ralph-loop-init instead."
version: 2.0.0
---

# Investigate (Entrypoint Wrapper)

이 스킬은 entrypoint wrapper다. 사용자의 investigate(디버깅·근본원인 분석) 요청을 `sdd-skills:investigate-agent`에 위임하고 그 결과를 사용자에게 전달한다. 전체 디버깅 프로세스·3-Strike·Blast Radius·Fresh Verification·리포트 형식은 agent가 단일 소스로 보유한다.

## 실행 (Mode A: pass-through)

1. 사용자 요청 + 증상/재현 조건/기대 동작과 이미 아는 컨텍스트(에러 메시지, 관련 파일 경로)를 수집한다 (wrapper는 새 분석 read를 하지 않는다).
2. `Agent(subagent_type="sdd-skills:investigate-agent", prompt=<요청 + 알려진 증상/컨텍스트>)`로 dispatch한다. 범위가 불명확하면 agent가 Problem Definition 단계로 자체 확정하도록 위임한다.
3. agent의 반환(Investigation Report: 근본원인, 수정 파일:라인, Blast Radius, Verification 결과)을 사용자에게 그대로 relay한다.

## 계약 (entrypoint·artifact 유지, 흉내 금지)

- trigger(investigate 호출)와 Investigation Report 출력 계약은 이 wrapper가 유지한다.
- 실제 디버깅·수정·검증은 agent가 수행한다. agent가 지원하지 않는 동작을 wrapper가 흉내내지 않는다.
- agent가 노출하는 근본원인·Blast Radius·Verification(PASS/FAIL/UNTESTED) 결과를 wrapper가 relay해 보존한다.

> Source: 전체 계약·3-Strike·Blast Radius·Fresh Verification·출력 형식은 `.claude/agents/investigate-agent.md`가 단일 소스로 보유한다 (wrapper↔agent; 더 이상 동일 본문 mirror 아님).
