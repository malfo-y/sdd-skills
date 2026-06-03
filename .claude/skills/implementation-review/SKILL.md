---
name: implementation-review
description: "Use this skill to review implementation progress against the plan, verify acceptance criteria, identify issues, and determine next steps. Triggered by \"review implementation\", \"check progress\", \"verify implementation\", \"what's done\", \"implementation status\", or \"audit the code\". Works with or without an implementation plan (Graceful Degradation)."
version: 5.0.0
---

# Implementation Review (Entrypoint Wrapper)

이 스킬은 entrypoint wrapper다. 사용자의 implementation-review 요청을 `sdd-skills:implementation-review-agent`에 위임하고 그 결과를 사용자에게 전달한다. 전체 리뷰 프로세스·Tier graceful degradation·findings-first severity·리포트 형식은 agent가 단일 소스로 보유한다.

## 실행

plan 파일이 있으면 agent가 그것으로 범위를 잡지만(Tier 1), **plan 없이 "방금 구현한 거 리뷰"처럼 호출되면 무엇을·왜 구현했는지·리뷰 범위가 대화에 산다**. agent는 파일은 read하지만 **이번 세션의 대화는 못 읽으므로**, wrapper가 그 맥락을 정리해 전달한다.

1. 다음을 수집한다:
   - 사용자 요청 원문 + 인자
   - 이미 아는 경로(plan/spec/코드, 직전 산출물)
   - **대화에만 있는 맥락 digest**: 이번 세션에서 무엇을 구현/변경했는지, 그 의도, 리뷰 대상 범위(plan 파일이 없을 때 특히). plan 파일이 분명하면 이 digest는 짧아진다.
2. `Agent(subagent_type="sdd-skills:implementation-review-agent", prompt=<요청 + 경로 + 대화 맥락 digest>)`로 dispatch한다. 대상 경로가 불명확하면 agent가 Tier Selection·Input 우선순위로 자체 탐색하도록 위임한다.
3. agent의 반환(리포트 경로 `_sdd/implementation/<YYYY-MM-DD>_implementation_review_<slug>.md`, Tier, findings 요약, blocker)을 사용자에게 그대로 relay한다.

> **경계**: wrapper는 *대화 맥락을 모아 전달*까지만 한다. Tier 판별·검증·findings 분류·리포트 작성은 agent의 Process가 수행한다(중복 금지).

## 계약 (entrypoint·artifact 유지, 흉내 금지)

- trigger(implementation-review 호출)와 리포트 경로 계약은 이 wrapper가 유지한다.
- 실제 검증·리포트 작성은 agent가 수행한다. agent가 지원하지 않는 동작을 wrapper가 흉내내지 않는다.
- agent가 노출하는 Tier·Critical/High findings·blocker를 wrapper가 relay해 보존한다.

> Source: 전체 계약·Tier·severity·출력 형식은 `.claude/agents/implementation-review-agent.md`가 단일 소스로 보유한다 (wrapper↔agent; 더 이상 동일 본문 mirror 아님).
