---
name: plan-review
description: Use this skill to review a lite feature draft before coding, identify overengineering and sloppy-code risks, and return a findings-first verdict. Triggered by "plan review", "review plan", "draft review", "계획 리뷰", "플랜 리뷰", "구현 계획 리뷰", or when the user wants to check a draft against KISS/YAGNI/DRY/minimum-code principles before implementation.
version: 3.0.0
argument-hint: ["[--model <sonnet|opus|haiku|fable>]"]
---

# Plan Review (Entrypoint Wrapper)

이 스킬은 entrypoint wrapper다. 사용자의 plan-review 요청을 `sdd-skills:plan-review-agent`에 위임하고 그 **경량 반환**을 사용자에게 전달한다. 전체 리뷰 프로세스·6-smell rubric·severity·반환 형식은 agent가 단일 소스로 보유한다. 리뷰는 단일 패스이며 리포트 파일을 만들지 않는다.

## 실행

> **Model override**: `$ARGUMENTS`에 `--model <name>`이 있으면 `Agent(...)` dispatch에 `model=<name>`을 추가한다. `<name>`은 `sonnet`·`opus`·`haiku`·`fable` 중 하나여야 하며, 그 외 값이면 dispatch하지 않고 사용자에게 허용값을 안내한다. 미지정 시 model을 생략한다(세션 기본값 상속).

1. 사용자 요청 + 리뷰 대상 lite draft 경로와 이미 아는 결정을 수집한다 (wrapper는 새 분석 read를 하지 않는다).
2. `Agent(subagent_type="sdd-skills:plan-review-agent", prompt=<요청 + 알려진 경로/컨텍스트>)`로 dispatch한다. 대상 경로가 불명확하면 agent가 자체 Input 우선순위로 탐색하도록 위임한다.
3. agent의 경량 반환(Blocker Status, severity별 finding, Lite 적격 검사 결과, smell 6행 판정)을 사용자에게 그대로 relay한다. finding 반영은 호출자(draft 작성자) 소관이다.

## 계약 (entrypoint 유지, 흉내 금지)

- trigger(plan-review 호출) 계약은 이 wrapper가 유지한다.
- 실제 감사·판정은 agent가 수행한다. agent가 지원하지 않는 동작을 wrapper가 흉내내지 않는다.
- agent가 노출하는 Blocker(Critical/High)·구현 전 차단 이슈를 wrapper가 relay해 보존한다.

> Source: 전체 계약·6-smell·severity·반환 형식은 `.claude/agents/plan-review-agent.md`가 단일 소스로 보유한다 (wrapper↔agent; 동일 본문 mirror 아님).
