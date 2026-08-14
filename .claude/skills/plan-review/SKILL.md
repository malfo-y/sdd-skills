---
name: plan-review
description: Use this skill to review a feature draft before coding, identify overengineering and sloppy-code risks, and return a findings-first verdict. Triggered by "plan review", "review plan", "draft review", "계획 리뷰", "플랜 리뷰", "구현 계획 리뷰", or when the user wants to check a draft for requirement fit, overengineering, hidden decisions, and weak verification before implementation.
argument-hint: ["[--model <sonnet|opus|haiku|fable>]"]
---

# Plan Review

이 스킬은 review-only orchestrator다. 사용자의 plan-review 요청에 대해 **병렬 gather → 단일 판정** 순서로 agent를 dispatch하고 반환을 정리해 사용자에게 전달한다. 리뷰(판정)는 단일 패스이며 리포트 파일을 만들지 않는다(gather digest는 로컬 전용 산출물이다).

## 실행

> **Model override**: `$ARGUMENTS`에 `--model <name>`이 있으면 모든 `Agent(...)` dispatch(gatherer 포함)에 `model=<name>`을 추가한다. `<name>`은 `sonnet`·`opus`·`haiku`·`fable` 중 하나여야 하며, 그 외 값이면 dispatch하지 않고 사용자에게 허용값을 안내한다. 미지정 시 model을 생략한다(세션 기본값 상속).

1. 사용자 요청 + 리뷰 대상 draft 경로와 이미 아는 결정을 수집한다. orchestrator의 read는 **다음 단계의 shard 구성을 위한 대상 draft 1회 read만** 허용한다 — 코드 분석 read는 하지 않는다(분석은 agent들의 몫이다).
2. **Gather phase** — draft 1회 read에서 Target Files 경로 전체(+draft가 명시 참조하는 spec anchor 파일)를 추출하고:
   - 디렉토리 근접 기준으로 3~5개 파일씩(총량이 그보다 적으면 한 그룹), 최대 ~6그룹으로 묶는다.
   - 그룹마다 `Agent(subagent_type="sdd-skills:plan-context-gatherer", prompt=<draft 경로 + 배정 파일 그룹 + digest 출력 경로>)`를 **한 메시지에서 병렬 dispatch**한다. digest 출력 경로는 `_sdd/pipeline/plan_review_gather/<draft-slug>/<그룹명>.md` — 재실행은 같은 경로를 덮어쓰며, 리뷰 후 삭제하지 않는다(사후 검시 자산).
   - **Degrade**: Target Files가 비었거나 gather dispatch가 전부 실패하면 gather를 생략하고 3의 단일 dispatch로 바로 진행한다. 일부만 실패하면 성공한 digest만으로 진행한다.
3. 판정 agent를 dispatch한다:
   - `Agent(subagent_type="sdd-skills:plan-review-agent", prompt=<요청 + 알려진 경로/컨텍스트 + digest 경로 목록>)`
   - digest는 **경로만** 전달한다 — 발췌 본문을 prompt에 전사하지 않는다.
   - 대상 경로가 불명확하면 리뷰 agent가 자체 Input 우선순위로 탐색하도록 위임한다.
4. 반환을 정리해 relay한다: Blocker Status는 **하나라도 BLOCKED면 BLOCKED**, findings/smell 판정은 정리해 전달한다. finding 반영은 호출자(draft 작성자) 소관이다.

## 계약 (entrypoint 유지, 흉내 금지)

- trigger(plan-review 호출) 계약은 이 orchestrator가 유지한다.
- 실제 감사·판정은 agent가 수행한다. agent가 지원하지 않는 동작을 orchestrator가 흉내내지 않는다.
- agent가 노출하는 Blocker(Critical/High)·구현 전 차단 이슈를 orchestrator가 relay해 보존한다 (병합은 relay이지 gating이 아니다).

> Source: 전체 계약·5-smell·severity·반환 형식은 `.claude/agents/plan-review-agent.md`가 단일 소스로 보유한다 (wrapper↔agent; 동일 본문 mirror 아님).
