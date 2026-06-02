---
name: investigate
description: "Use this skill when the user asks to \"investigate\", \"debug\", \"find root cause\", \"diagnose\", \"why is this failing\", \"track down bug\", \"근본원인 분석\", \"디버깅\", or wants systematic one-shot debugging of a specific issue. For long-running iterative debugging processes, use ralph-loop-init instead."
version: 3.0.0
---

# Investigate (Entrypoint Wrapper — Mode B)

이 스킬은 entrypoint wrapper다. 사용자의 investigate(디버깅·근본원인 분석) 요청을 `sdd-skills:investigate-agent`에 위임하고 그 결과를 사용자에게 전달한다. 전체 디버깅 프로세스·3-Strike·Blast Radius·Fresh Verification·리포트 형식은 agent가 단일 소스로 보유한다.

## 실행 (Mode B: context-forwarding)

investigate의 **문제 정의(증상·재현 조건·기대 동작)는 대화에서 태어난다**(agent Step 1). agent는 파일은 read하지만 **이번 세션의 대화는 못 읽으므로**, wrapper가 그 맥락을 정리해 전달한다.

1. 다음을 수집한다:
   - 사용자 요청 원문 + 인자
   - 이미 아는 경로·증거(에러 메시지, 관련 파일 경로, 재현 명령)
   - **대화에만 있는 맥락 digest**: 이번 세션에서 드러난 증상·재현 조건·기대 동작, 그리고 **이미 시도한 가설/접근과 그 결과**(3-Strike 중복 방지).
2. `Agent(subagent_type="sdd-skills:investigate-agent", prompt=<요청 + 증거 경로 + 대화 맥락 digest>)`로 dispatch한다.
3. agent의 반환(Investigation Report: 근본원인, 수정 파일:라인, Blast Radius, Verification 결과)을 사용자에게 그대로 relay한다.

> **경계**: wrapper는 *대화 맥락을 모아 전달*까지만 한다. 가설 수립·근본원인 분석·수정·검증은 agent의 Process(Step 1~6)가 수행한다(중복 금지).

## 계약 (entrypoint·artifact 유지, 흉내 금지)

- trigger(investigate 호출)와 Investigation Report 출력 계약은 이 wrapper가 유지한다.
- 실제 디버깅·수정·검증은 agent가 수행한다. agent가 지원하지 않는 동작을 wrapper가 흉내내지 않는다.
- agent가 노출하는 근본원인·Blast Radius·Verification(PASS/FAIL/UNTESTED) 결과를 wrapper가 relay해 보존한다.

> Source: 전체 계약·3-Strike·Blast Radius·Fresh Verification·출력 형식은 `.claude/agents/investigate-agent.md`가 단일 소스로 보유한다 (wrapper↔agent; 더 이상 동일 본문 mirror 아님).
