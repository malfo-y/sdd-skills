---
name: plan-review
description: Use this skill to review a feature draft before coding, identify overengineering and sloppy-code risks, and return a findings-first verdict. Triggered by "plan review", "review plan", "draft review", "계획 리뷰", "플랜 리뷰", "구현 계획 리뷰", or when the user wants to check a draft against KISS/YAGNI/DRY/minimum-code principles before implementation.
argument-hint: ["[--model <sonnet|opus|haiku|fable>]"]
---

# Plan Review (2-렌즈 Orchestrator)

이 스킬은 review-only orchestrator다. 사용자의 plan-review 요청을 `sdd-skills:plan-review-agent` **2회 병렬 dispatch**(실측 렌즈 ∥ 판단 렌즈)로 위임하고 두 **경량 반환**을 병합해 사용자에게 전달한다. 전체 리뷰 프로세스·5-smell rubric·severity·반환 형식·렌즈 정의는 agent가 단일 소스로 보유한다. 리뷰는 단일 패스이며(렌즈 2개는 한 패스의 병렬 분해이지 loop가 아니다) 리포트 파일을 만들지 않는다. agent는 read-only leaf(파일을 쓰지 않음)라 동시 dispatch가 안전하다.

## 실행

> **Model override**: `$ARGUMENTS`에 `--model <name>`이 있으면 모든 `Agent(...)` dispatch에 `model=<name>`을 추가한다. `<name>`은 `sonnet`·`opus`·`haiku`·`fable` 중 하나여야 하며, 그 외 값이면 dispatch하지 않고 사용자에게 허용값을 안내한다. 미지정 시 model을 생략한다(세션 기본값 상속).

1. 사용자 요청 + 리뷰 대상 draft 경로와 이미 아는 결정을 수집한다 (orchestrator는 새 분석 read를 하지 않는다).
2. **한 메시지에서 두 렌즈를 병렬 dispatch한다** (렌즈 소유 정의는 agent의 `호출자 렌즈 한정` 절이 단일 소스):
   - `Agent(subagent_type="sdd-skills:plan-review-agent", prompt=<요청 + 알려진 경로/컨텍스트 + 실측 렌즈 한정>)`
   - `Agent(subagent_type="sdd-skills:plan-review-agent", prompt=<요청 + 알려진 경로/컨텍스트 + 판단 렌즈 한정>)`
   - 대상 경로가 불명확하면 각 dispatch가 자체 Input 우선순위로 탐색하도록 위임한다.
3. 두 반환을 병합해 relay한다: Blocker Status는 **하나라도 BLOCKED면 BLOCKED**, findings는 합산, smell 판정은 **합집합**(각 smell이 정확히 한 렌즈에 소유되므로 중복 없음), 규모 판정 검사 결과는 판단 렌즈 반환에서 온다. finding 반영은 호출자(draft 작성자) 소관이다.

## 계약 (entrypoint 유지, 흉내 금지)

- trigger(plan-review 호출) 계약은 이 orchestrator가 유지한다.
- 실제 감사·판정은 agent가 수행한다. agent가 지원하지 않는 동작을 orchestrator가 흉내내지 않는다.
- agent가 노출하는 Blocker(Critical/High)·구현 전 차단 이슈를 orchestrator가 relay해 보존한다 (병합은 relay이지 gating이 아니다).

> Source: 전체 계약·5-smell·severity·반환 형식은 `.claude/agents/plan-review-agent.md`가 단일 소스로 보유한다 (wrapper↔agent; 동일 본문 mirror 아님).
