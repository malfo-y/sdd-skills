---
name: implementation-review
description: "Use this skill to review implementation progress against the plan, verify acceptance criteria, identify issues, and determine next steps. Triggered by \"review implementation\", \"check progress\", \"verify implementation\", \"what's done\", \"implementation status\", or \"audit the code\". Works with or without a draft/plan (graceful degradation)."
argument-hint: ["[--model <sonnet|opus|haiku|fable>]"]
---

# Implementation Review (2-렌즈 Orchestrator, Review-only)

이 스킬은 review-only orchestrator다. 사용자의 implementation-review 요청을 두 렌즈의 reviewer agent에 **병렬 dispatch**하고, 경량 반환들과 합산 severity 요약을 사용자에게 relay한다. correctness는 기준 draft의 task 수에 따라 shard 여러 개로, simplicity는 차원 묶음 2개로 나뉜다(아래 실행 1·2).

- `sdd-skills:implementation-review-agent` — **correctness** 렌즈 (AC 충족·버그·보안·spec drift — 기준 문서 적응)
- `sdd-skills:simplicity-review-agent` — **clarity** 렌즈 (동작-불변 형태 품질: 중복·죽은 코드·단일 사용처 추상화·도달 불가 에러 처리·과잉압축)

> **Review-only 경계**: 리뷰 프로세스·severity·반환 형식은 각 agent가 소유한다. 이 orchestrator는 맥락 수집·dispatch·결과 relay와 합산 요약만 수행한다. finding 반영·마감 판정은 호출자 소관이며 합집합 exit 판정은 하지 않는다.

## 병렬 안전성 근거

reviewer들은 sub-agent를 spawn하지 않고 **어떤 파일도 쓰지 않는** read-only leaf다 (`implementation-review-agent`: `["Read","Glob","Grep","Bash"]` — Bash는 테스트 실행용, `simplicity-review-agent`: `["Read","Glob","Grep"]`). 판정을 응답으로만 반환하므로 reviewer shard 수와 무관하게 한 메시지에서 동시 dispatch해도 안전하다.

## 실행

> **Model override**: `$ARGUMENTS`에 `--model <name>`이 있으면 모든 reviewer `Agent(...)` 호출에 `model=<name>`을 추가한다. `<name>`은 `sonnet`·`opus`·`haiku`·`fable` 중 하나여야 하며, 그 외 값이면 dispatch하지 않고 사용자에게 허용값을 안내한다. 미지정 시 model을 생략한다(세션 기본값 상속).

1. 다음을 수집한다 (공통 digest는 모든 reviewer에 전달):
   - 사용자 요청 원문 + 인자
   - 이미 아는 경로(plan/spec/코드, 직전 산출물)
   - **대화에만 있는 맥락 digest**
     - plan 있음: 경로와 필요한 맥락만 짧게 전달한다.
     - plan 없음: 이번 세션에서 무엇을·왜 구현했는지와 리뷰 범위를 전달한다.
     - 근거: reviewer는 이번 세션 대화를 직접 읽지 못한다.
   - **correctness 분할표**: 기준 draft의 Part 2 task가 2개 이상이면 correctness를 task별 shard로 나눈다 — shard k의 digest는 공통 digest에 **Task k의 AC·Target Files로 리뷰 범위를 한정**하는 지시를 더한 것이다(해당 task의 AC만 검증). task가 1개이거나 draft 없이 대화 digest 기반이면 분할하지 않는다(correctness 1회).
2. **한 메시지에서 모든 reviewer를 병렬 dispatch한다** (read-only leaf라 동시 실행 안전 — 위 근거):
   - correctness — shard마다 1회: `Agent(subagent_type="sdd-skills:implementation-review-agent", prompt=<요청 + 경로 + 공통 digest + shard 범위 한정>)`
   - simplicity — 차원 **묶음마다 1회**(참조 ∥ 국소), 각 dispatch는 **전체 변경 대상**: `Agent(subagent_type="sdd-skills:simplicity-review-agent", prompt=<요청 + 경로 + 공통 digest + 차원 묶음 한정>)`. 묶음 정의·범위 불변 근거는 agent의 `호출자 차원 한정` 절이 단일 소스다.
   - 대상 경로가 불명확하면 각 agent가 자체 Input 우선순위로 탐색하도록 위임한다.
3. 반환들을 모아 사용자에게 relay한다:
   - correctness: 리뷰 기준(draft/spec/코드만), AC verdict ledger, findings 요약, blocker. 분할 dispatch면 ledger는 shard 반환의 **연접**이다 — 모든 task의 AC가 정확히 한 shard에 속하므로 누락 없이 합쳐진다.
   - simplicity: 차원 판정과 findings 요약 — 차원 판정은 두 묶음 반환의 합집합이다(각 차원 정확히 한 묶음 소유라 중복 없음)
   - **합산 severity 요약**: 모든 반환의 Critical/High/Medium findings를 합쳐 한눈에 보이게 정리한다 (판정은 하지 않고 합산만). task들이 같은 파일을 만져 shard 간 중복 finding이 나와도 dedup하지 않고 전부 relay한다 — dedup은 fix 주체인 호출자 소관이다.

## 계약 (entrypoint·artifact 유지, 흉내 금지)

- trigger(implementation-review 호출) 계약은 이 orchestrator가 유지한다.
- 실제 검증은 각 reviewer agent가 수행한다. agent가 지원하지 않는 동작을 orchestrator가 흉내내지 않는다.
- reviewer들이 노출하는 Critical/High findings·blocker를 orchestrator가 relay해 보존한다 (합산 요약은 relay이지 gating이 아니다).

> Source: correctness 계약·severity·반환 형식은 `.claude/agents/implementation-review-agent.md`가, simplicity 계약·5개 차원·falsifiable severity는 `.claude/agents/simplicity-review-agent.md`가 각각 단일 소스로 보유한다 (orchestrator↔agent; 동일 본문 mirror 아님).
