---
name: implementation-plan
description: This skill should be used when the user asks to "create an implementation plan", "plan the implementation", "break down this spec", "create a development roadmap", "analyze requirements and create tasks", "create a parallel implementation plan", "plan parallel implementation", "병렬 구현 계획", "create parallel development roadmap", or wants a structured implementation plan with Target Files for parallel execution support.
version: 5.0.0
argument-hint: ["[--model <sonnet|opus|haiku|fable>]"]
---

# Implementation Plan (Orchestrator)

이 스킬은 **메인 루프 orchestrator**다. `feature-draft-agent`를 dispatch해 draft를 생성하고, `plan-review-agent`로 **review→fix→re-review loop**를 돌려 산출물 품질 gate를 자체 소유한다. agent는 draft producer 단일 소스이고 스킬이 loop를 소유한다 — producer/reviewer agent는 sub-agent를 spawn하지 못하므로 loop orchestration은 메인 루프(스킬)의 책임이다.

feature-draft는 **입력이 대화에서 태어나는** 스킬이다. agent는 파일은 read하나 이번 세션의 대화는 못 읽으므로, orchestrator가 대화 맥락 digest를 정리해 **생성·fix 라운드 모두에** 전달한다.

## Process

> **Model override**: `$ARGUMENTS`에 `--model <name>`이 있으면 이 스킬의 모든 `Agent(...)` 호출(생성·fix mode·review 포함)에 `model=<name>`을 추가한다. `<name>`은 `sonnet`·`opus`·`haiku`·`fable` 중 하나여야 하며, 그 외 값이면 dispatch하지 않고 사용자에게 허용값을 안내한다. 미지정 시 model을 생략한다(세션 기본값 상속).

### Step 1: 맥락 digest 수집

다음을 수집한다:
- 사용자 요청 원문 + 인자
- 이미 아는 경로·산출물(관련 `_sdd/spec/*`, 직전 draft/discussion 경로 등)
- **대화에만 있는 맥락 digest**: 이번 세션에서 합의된 요구사항·결정·제약·기각한 대안을 주제 기준으로 정리.

### Step 2: 생성 (producer dispatch)

`Agent(subagent_type="sdd-skills:feature-draft-agent", prompt=<요청 + 경로 + 대화 맥락 digest>)`로 **생성 mode** dispatch한다. agent가 draft를 `_sdd/drafts/<YYYY-MM-DD>_feature_draft_<slug>.md`에 저장하고 경로 + Step 9 surface 결정을 반환한다.

### Step 3: review-fix loop

산출 직후 review→fix→re-review loop를 닫는다. **공통 loop 정책**(autopilot `references/orchestrator-contract.md` §6 Review-Fix Contract 차용):

- **exit 조건**: `critical=high=medium=0`.
- **MAX**: 기본 3 iteration.
- **re-review scope**: loop 범위(draft) **전체 재리뷰** (변경분만 아님).
- **1 iteration 경계**: `review/re-review → finding>0이면 fix → 산출물 갱신`.
- **MAX 도달 분기**: critical/high 잔존 → 중단·사용자 보고. medium만 잔존 → 로그 후 진행(advisory degrade).

단계:

1. **review**: `Agent(subagent_type="sdd-skills:plan-review-agent")`로 draft Part 2(+Part 1 delta)를 review한다(`plan-review-agent`는 feature draft Part 2를 입력으로 수용 — Tier 2). reviewer가 Blocker Status + severity별 finding을 리포트(`_sdd/implementation/<YYYY-MM-DD>_plan_review_<slug>.md`)로 낸다.
2. **fix**: critical/high/medium finding이 있으면 `feature-draft-agent`를 **fix mode**로 재dispatch한다 — 입력: review 리포트 경로 + draft 경로 + 대상 findings + **대화 맥락 digest(유지)**. agent가 finding 부분만 surgical 수정한다.
3. **re-review**: fix 후 loop 범위 전체를 `plan-review-agent`로 재리뷰한다.
4. exit 충족 또는 MAX 도달까지 1~3을 반복한다. MAX 분기 적용.

> fix 라운드에도 digest를 producer에 함께 전달한다(입력이 대화에서 태어나는 특성 유지).

### Step 4: relay

최종 draft 경로 + Step 9 surface 결정(Confidence=LOW/User-confirmation=Yes) + loop 결과(iteration 수, 최종 Blocker Status, 잔존 advisory)를 사용자에게 relay한다.

## 경계

- 산출물(draft) 작성·수정은 `feature-draft-agent`만 한다(산출물 단일 작성자 — orchestrator는 직접 rewrite하지 않는다). 스킬은 loop만 소유한다.
- review·findings 분류는 `plan-review-agent`가 수행한다(중복 금지).

> **Role Pointer**: 이 스킬은 review-fix loop를 소유하는 **orchestrator**다. `feature-draft-agent`는 draft producer 단일 소스(생성·fix mode 수정), `plan-review-agent`는 reviewer다. 

> **DEPRECATED.** 이 스킬은 기존 사용자 트리거의 하위호환 보존을 위해서만 남아 있으며, 호출되면 `feature-draft`와 동일하게 동작한다. **신규 작업은 `feature-draft`를 직접 사용하라.**
