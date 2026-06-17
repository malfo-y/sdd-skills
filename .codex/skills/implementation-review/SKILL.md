---
name: implementation-review
description: Use this skill to review implementation progress against the plan, verify acceptance criteria, identify issues, and determine next steps. Triggered by "review implementation", "check progress", "verify implementation", "what's done", "implementation status", or "audit the code". Works with or without an implementation plan (Graceful Degradation).
version: 6.0.0
---

# Implementation Review (2-Reviewer Orchestrator, Review-only)

이 스킬은 review-only orchestrator다. 사용자의 implementation-review 요청을 두 개의 형제 reviewer agent에 **병렬 dispatch**하고, 두 리포트 경로와 합산 severity 요약을 사용자에게 relay한다.

- `implementation-review-agent` — **correctness** 렌즈 (AC 충족·버그·보안·spec drift·Tier graceful degradation)
- `simplicity-review-agent` — **clarity** 렌즈 (동작-불변 형태 품질: 중복·죽은 코드·단일 사용처 추상화·도달 불가 에러 처리·과잉압축)

전체 리뷰 프로세스·Tier·findings-first severity·리포트 형식은 각 agent가 단일 소스로 보유한다. 이 orchestrator는 맥락을 모아 전달하고 두 리포트를 relay할 뿐이다.

> **Review-only 경계**: 이 스킬은 두 report를 relay만 한다. fix → re-review loop와 exit 조건 합집합 판정 같은 gating 의사결정은 이 스킬이 소유하지 않으며, 그것은 `implementation` 스킬의 review gate 소관이다.

## Codex Runtime Adapter

런타임이 skill-internal agent dispatch를 허용하는 경우, 이 스킬의 직접 호출은 아래 내부 dispatch 범위에 대한 사용자 요청으로 처리한다. dispatch 전에 `spawn_agent`, `wait_agent`, `close_agent`가 active tools에 없으면 `tool_search` query `spawn_agent wait_agent close_agent multi-agent sub-agent`로 multi-agent tools를 먼저 로드한다. 현재 런타임 정책이 명시적 sub-agent 허가를 추가로 요구하면, dispatch 전에 사용자에게 위임 허가를 요청한다.

실제 Codex 호출은 `prompt`가 아니라 `message`를 사용한다. 두 reviewer를 한 번에 spawn한 뒤 `wait_agent`로 둘 다 수거한다:

```text
spawn_agent({agent_type: "implementation-review-agent", message: "<요청 + 경로 + 대화 맥락 digest>"})
spawn_agent({agent_type: "simplicity-review-agent", message: "<요청 + 경로 + 대화 맥락 digest>"})
wait_agent({targets: ["<correctness_id>", "<simplicity_id>"], timeout_ms: 600000})
close_agent({target: "<correctness_id>"})
close_agent({target: "<simplicity_id>"})
```

## 병렬 안전성 근거

두 reviewer는 모두 **read-only leaf**다 (`tools = ["Read", "Glob", "Grep"]`, sub-agent를 spawn하지 않음). 코드·plan·spec를 수정하지 않고 각자 자기 리포트만 쓴다. 그리고 두 리포트가 **서로 다른 경로**(`*_implementation_review_*` vs `*_simplicity_review_*`)에 저장돼 write 충돌이 없다. 따라서 한 번에 동시 spawn해도 안전하다.

## 실행

plan 파일이 있으면 agent가 그것으로 범위를 잡지만(Tier 1), **plan 없이 "방금 구현한 거 리뷰"처럼 호출되면 무엇을·왜 구현했는지·리뷰 범위가 대화에 산다**. agent는 파일은 read하지만 **이번 세션의 대화는 못 읽으므로**, orchestrator가 그 맥락을 정리해 전달한다.

1. 다음을 수집한다 (digest는 두 reviewer에 공통으로 전달):
   - 사용자 요청 원문 + 인자
   - 이미 아는 경로(plan/spec/코드, 직전 산출물)
   - **대화에만 있는 맥락 digest**: 이번 세션에서 무엇을 구현/변경했는지, 그 의도, 리뷰 대상 범위(plan 파일이 없을 때 특히). plan 파일이 분명하면 이 digest는 짧아진다.
2. **두 reviewer를 동시 spawn한다** (read-only leaf라 동시 실행 안전 — 위 근거):
   - `spawn_agent({agent_type: "implementation-review-agent", message: <요청 + 경로 + 대화 맥락 digest>})`
   - `spawn_agent({agent_type: "simplicity-review-agent", message: <요청 + 경로 + 대화 맥락 digest>})`
   - 반환된 두 agent ids를 `wait_agent({targets: [<correctness_id>, <simplicity_id>], timeout_ms: 600000})`로 수거한다. 두 handle 모두 final status가 반환된 뒤에만 결과를 기록하고 `close_agent`로 닫는다. `wait_agent`가 timeout이면 완료로 간주하지 말고 더 기다리거나, controlled stop/blocked 상태를 사용자에게 보고한 뒤에만 handle 정리를 결정한다. 대상 경로가 불명확하면 각 agent가 자체 Input 우선순위로 탐색하도록 위임한다.
3. 두 agent의 반환을 모아 사용자에게 relay한다:
   - correctness 리포트 경로 `_sdd/implementation/<YYYY-MM-DD>_implementation_review_<slug>.md` (+ Tier, findings 요약, blocker)
   - simplicity 리포트 경로 `_sdd/implementation/<YYYY-MM-DD>_simplicity_review_<slug>.md` (+ findings 요약)
   - **합산 severity 요약**: 두 리포트의 Critical/High/Medium findings를 합쳐 한눈에 보이게 정리한다 (판정은 하지 않고 합산만).

> **경계**: orchestrator는 *대화 맥락을 모아 전달*하고 *두 리포트를 relay*까지만 한다. Tier 판별·검증·findings 분류·리포트 작성은 각 agent의 Process가 수행한다(중복 금지). 합집합 exit 판정·fix loop는 하지 않는다.

## 계약 (entrypoint·artifact 유지, 흉내 금지)

- trigger(implementation-review 호출)와 두 리포트 경로 계약은 이 orchestrator가 유지한다.
- 실제 검증·리포트 작성은 두 agent가 각각 수행한다. agent가 지원하지 않는 동작을 orchestrator가 흉내내지 않는다.
- 두 agent가 노출하는 Tier·Critical/High findings·blocker를 orchestrator가 relay해 보존한다 (합산 요약은 relay이지 gating이 아니다).

> Source: correctness 계약·Tier·severity·출력 형식은 `.codex/agents/implementation-review-agent.toml`이, simplicity 계약·5개 차원·falsifiable severity는 `.codex/agents/simplicity-review-agent.toml`이 각각 단일 소스로 보유한다 (orchestrator↔agent; 더 이상 동일 본문 mirror 아님).
