# Feature Draft: mirror 스킬을 agent thin wrapper로 전환

> 근거 토론: `_sdd/discussion/2026-06-03_discussion_implementation_orchestrator_leaf_split.md` — 통합 규칙 "fan-out→orchestrator+leaf / non-fan-out→wrapper→agent" 확정. 이 작업은 후자(wrapper) 트랙.
> 선행: implementation은 orchestrator/leaf 분리로 별도 해결되어 main 머지됨(`70f0fc2`). 본 작업 범위에서 제외.
> census(2026-06-03): 후보 9개 중 core fan-out 0 · interactive(AskUserQuestion) 0. 예외는 implementation-plan의 선택적 worker 병렬 fill뿐(순차 degrade 수용, 사용자 확정).

# Part 1: Temporary Spec Draft

## Change Summary

mirror 스킬 9종(`feature-draft`, `implementation-plan`, `plan-review`, `implementation-review`, `ralph-loop-init`, `spec-review`, `spec-update-done`, `spec-update-todo`, `investigate`)의 **SKILL을 thin wrapper로 전환**한다. 현재 각 스킬은 SKILL과 agent가 동일 full 본문을 mirror해 스킬당 full 본문이 4벌(claude skill+agent, codex skill+agent) 존재하고, "함께 수정" 동기화 부담이 크다.

전환 후: **SKILL = entrypoint wrapper**(사용자 요청을 해당 agent에 dispatch하고 결과를 relay), **agent = 단일 full-body source**. full 본문은 4벌 → 2벌(agent ×claude/codex) + thin wrapper 2벌로 줄어 중복이 절반이 된다.

동기: 원래 wrapper 전환 pilot(2026-06-02)이 `implementation`을 wrapping하려다 nesting 1단계 제한(dispatch된 agent는 sub-agent를 spawn 못 함)에 막혀 보류됐다. 그 blocker는 **core fan-out 스킬에만** 적용되는데, implementation은 이미 orchestrator/leaf로 빠졌고 나머지 9종은 core fan-out이 없어(census 확인) wrapping이 안전하다. 스펙 main.md L62가 이미 "wrapper-backed skill"을 모델로 명시하므로, 이 전환은 스펙 의도를 코드에 반영하는 작업이다.

## Scope Delta

**In-scope:**
- 9종 mirror 스킬의 SKILL(claude + codex)을 thin wrapper로 전환.
- agent 본문은 단일 소스로 유지하되, ① dead `Agent` 도구 선언 제거(미사용 4종: feature-draft, plan-review, spec-review, investigate), ② Mirror Notice → wrapper↔agent pointer로 교체.
- `implementation-plan` agent의 선택적 worker 병렬 fill 서술을 "dispatch 시 순차"로 정직하게 정리(L62 — 조용한 흉내 금지).
- 안전한 1종(`plan-review`)을 먼저 pilot으로 전환·검증한 뒤 나머지 8종 batch.

**Out-of-scope (의도적 보류):**
- `implementation`(이미 orchestrator/leaf, main 머지) — 범위 밖.
- agent가 없는 skill-only 스킬(`discussion`, `git`, `guide-create`, `pr-review`, `spec-create`, `spec-rewrite`, `spec-snapshot`, `spec-summary`, `spec-upgrade`, `write-phased`, `sdd-autopilot`, `second-opinion`) — wrapper 대상 아님(위임할 agent 없음).
- agent 본문 프로세스 자체의 리팩터/개선 — 이번엔 wrapper 전환과 최소 정리만.
- `_sdd/spec/*` 직접 수정(읽기만). Part 1 delta는 후속 `spec-update-todo`로 머지.

**Guardrail delta:**
- wrapper는 entrypoint(trigger description)와 artifact 경로 계약을 유지하며, 지원하지 않는 동작을 조용히 흉내내지 않는다(spec L62). 실제 작업·계약은 agent가 수행.
- wrapped 스킬은 agent를 1단계 dispatch만 하며(메인 루프 → agent), agent는 sub-agent를 또 spawn하지 않는다(nesting 안전). core fan-out이 필요한 스킬은 이 트랙이 아니라 orchestrator/leaf 트랙으로 간다.
- 사용자 노출(결정/blocker/리포트 경로)은 agent 반환을 wrapper가 relay해 보존한다.

## Contract/Invariant Delta

| ID | Type | Change | Why |
|----|------|--------|-----|
| C1 | Modify | 9종 SKILL(claude+codex)을 thin wrapper로 전환: 사용자 요청+컨텍스트를 해당 agent에 dispatch하고 결과를 relay. full 프로세스 본문 제거 | DRY(본문 4벌→2벌), 스펙 wrapper-backed 모델(L62) 준수 |
| C2 | Add | wrapper의 dispatch 참조 = claude `Agent(subagent_type="sdd-skills:<name>-agent")`, codex `spawn_agent(agent_type="<name>_agent")`+`wait_agent` | 플러그인 resolve(prefix 필수) + codex 관용구 정합 |
| C3 | Modify | 미사용 `Agent` 도구 선언 제거(feature-draft, plan-review, spec-review, investigate agent) | dead 선언 정리, 흉내 금지(L62) |
| C4 | Modify | 9종 skill↔agent Mirror Notice → wrapper↔agent pointer(더 이상 동일 본문 mirror 아님; agent가 단일 소스) | 허위 "동일 본문 동기화" 의무 제거 |
| C5 | Modify | `implementation-plan` agent의 worker 병렬 fill 서술을 "dispatch 시 순차 degrade"로 정직화 + `Agent` 도구 제거 | 선택적 fan-out이 dispatch 경로에선 불가 — 조용한 흉내 금지(L62), 사용자 순차 수용 확정. 도구도 제거해 4종과 일관(M2) |
| C6 | Add | wrapper는 2-모드: **A(pass-through, 기본)** = 요청 원문 + 이미 아는 경로·산출물·결정만 relay(새 read·분석 없음); **B(context-forwarding, feature-draft 전용)** = A에 더해 대화에만 있는 맥락(요구사항·결정·제약·기각안)을 주제 기준 digest로 정리해 전달 | 원리: agent는 파일은 read하나 **대화는 못 읽는다**. 입력이 대화에서 태어나는 feature-draft는 맥락 forwarding 없이는 자기 입력을 굶음(Q1). curation은 "맥락 모아 전달"까지지 요구사항 분석은 agent 몫 |
| I1 | Add | wrapped 스킬은 agent를 1단계 dispatch만; agent는 sub-agent를 spawn하지 않는다 | nesting 1단계 제한과 정합 |
| I2 | Add | 사용자 entrypoint(trigger description)·artifact 경로 계약은 wrapper가 유지 | 직접 호출 UX·산출물 호환 보존(L59/L62) |
| I3 | Add | agent가 사용자에게 노출할 결정/blocker/리포트 경로를 반환하면 wrapper가 relay | 비대화형 스킬의 최종 노출 보존 |
| I4 | Add | claude/codex parity 유지(식별자 컨벤션 차이 제외) | dual-bundle 계약 |

## Touchpoints

> 모두 현재 코드 census(2026-06-03)로 확인.

- 9종 × 4파일 = **36파일**. 각 `.claude/skills/<name>/SKILL.md`(full→wrapper), `.claude/agents/<name>-agent.md`(소스 유지 + tool/Notice 정리), `.codex/skills/<name>/SKILL.md`(full→wrapper), `.codex/agents/<name>-agent.toml`(소스 유지 + Notice 정리).
- 본문 규모 참고: `ralph-loop-init` 602/603줄(최대 DRY 효과), `implementation-plan` 331/332(+worker 서술 L325 정직화), `feature-draft` 270/271(최고 컨텍스트 민감 — 전달 검증 중요), `investigate` 86/87(최소).
- dead `Agent` 도구: `.claude/agents/{feature-draft,plan-review,spec-review,investigate}-agent.md` frontmatter `tools`.
- wrapper 템플릿 근거: 스펙 `_sdd/spec/main.md` L59/L62/L90(skill=entrypoint·agent=reusable·wrapper-backed). codex dispatch 관용구: `.codex/skills/implementation/SKILL.md`(이미 `spawn_agent`+`wait_agent` 사용, main 머지).
- **변경 금지(negative)**: `_sdd/spec/*`, implementation(orchestrator/leaf), skill-only 스킬, plugin manifest(이미 agent 등록됨).

## Implementation Plan

1. **Phase 1 (Pilot)**: `plan-review`를 wrapper로 전환(4파일) + wrapper 템플릿 확정. end-to-end 검증(claude dispatch + codex spawn_agent 경로 + 리포트 산출 + 결정 relay). **동등성 게이트(H1)**: 직접-호출 대비 산출물 구조·노출 결정·핵심 판단 보존 확인 → 통과 시 템플릿 확정.
2. **Phase 2 (Batch)**: 나머지 8종을 동일 템플릿으로 전환. 각 스킬 4파일은 파일 disjoint → 병렬 가능(우리 orchestrator의 그룹 파생 규칙 자가 적용). `feature-draft`는 컨텍스트 전달 위험이 가장 커 **우선 전환 + 동등성 게이트 개별 적용**, `implementation-plan`은 worker 서술 정직화 + 도구 제거 동반. **동등성 미통과 스킬은 wrapping하지 않고 mirror로 유지**(H1 fallback).
3. **Phase 3 (Verify)**: 정적 게이트 V1~V5 + 런타임 smoke V6(reload 후 pilot + 1개 batch 스킬 실제 호출). 최종 wrap 대상은 "동등성 통과분"으로 확정.

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1 | review (grep) | 9종 SKILL이 thin wrapper. **측정 기준(전부 충족)**: ① wrapper SKILL에 `### Step ` 다단계 프로세스 헤딩 = 0 (grep -c) AND ② full `## Hard Rules` 다항목 목록 부재 AND ③ dispatch 호출(claude `sdd-skills:<name>-agent` / codex `spawn_agent(<name>_agent)`) 존재 AND ④ wrapper 본문 ≤ 40줄(frontmatter 제외) |
| V2 | C2 | review (grep) | wrapper dispatch 참조 = claude `sdd-skills:<name>-agent`, codex `spawn_agent(<name>_agent)`+`wait_agent` |
| V3 | C3, C5 | review (grep) | **5종** agent(feature-draft/plan-review/spec-review/investigate + implementation-plan) frontmatter `tools`에 `Agent` 없음 |
| V4 | C4, C5 | review (grep) | 9종 skill+agent Mirror Notice→pointer; implementation-plan worker 서술이 "dispatch 시 순차"로 정직화 |
| V5 | I4 | review (diff) | claude/codex wrapper 대칭(식별자 컨벤션 차이 제외) |
| V6 | C1, C6, I1, I2, I3 | smoke (executable) | reload/새 세션 후: pilot(`plan-review`, Mode A) wrapper 호출 → agent dispatch·리포트 생성·경로 relay 확인; **feature-draft(Mode B)** 호출 → 대화 맥락 digest 전달로 직접-호출 동등성 확인. agent가 sub-agent를 spawn하지 않음 확인. 불가 시 명시 기록 |

## Risks / Open Questions

### Q1. wrapper가 agent에 충분한 컨텍스트를 전달하는가 (대화 맥락 손실)
- **Decision taken**: wrapper는 사용자 요청 원문 + 인자 + 관련 산출물 경로(예: 직전 plan/draft 경로)를 dispatch 프롬프트에 명시 전달하고, agent는 자체 Read/Glob/Grep으로 파일을 읽는다. 컨텍스트 민감도가 높은 `feature-draft`는 Phase 2에서 우선 검증한다.
- **모드화(C6) + Exit 기준 / fallback (H1 반영)**: wrapper는 2-모드(A pass-through / B context-forwarding). 기본 **Mode A**로 시도 → **동등성 게이트**(dispatch 산출물이 직접-호출 대비 (a) 산출물 구조·경로, (b) 노출 결정/blocker, (c) 핵심 판단 보존) 미통과면 **Mode B로 승격** → 그래도 미통과면 **그 스킬은 wrapping 안 하고 mirror 유지**(사유 기록). feature-draft는 입력이 대화 태생이라 **처음부터 Mode B** 지정. 즉 "9종 전부 wrap"이 아니라 **"동등성 통과분만 wrap(필요 시 Mode B)"**으로 commit 조정.
- **Alternatives considered**: 대화 전체를 그대로 전달 → 토큰 낭비·노이즈. 기각. / 컨텍스트 없이 args만 → context-heavy 스킬 품질 저하. 기각. / 검증 결과와 무관히 전부 wrap → 품질 저하 스킬 강제 전환 위험. 기각(H1).
- **Confidence**: MEDIUM
- **User confirmation needed**: No (pilot/Phase 2 동등성 게이트로 실측, 미통과분은 mirror 유지)

### Q2. implementation-plan 선택적 worker 병렬 fill 상실
- **Decision taken**: wrapping하면 dispatch된 agent가 worker를 spawn 못 하므로 장문 plan을 순차 fill한다. 정확성 유지, 병렬성만 상실. agent 서술도 이에 맞춰 정직화(C5). **사용자 확정**(순차 degrade 수용).
- **Alternatives considered**: implementation-plan만 mirror 유지 → census상 예외 1건 위해 일관성 깨짐. 기각(사용자 결정).
- **Confidence**: HIGH (사용자 확정)
- **User confirmation needed**: No

### Q3. pilot 스킬 선택
- **Decision taken**: `plan-review`. read-only(리포트 산출), core fan-out·interactive 0, 입력 우선순위가 명확해 컨텍스트 전달 위험이 낮음 → 메커니즘(템플릿·codex 경로·relay) 검증에 적합.
- **Alternatives considered**: `investigate`(최소이나 코드 수정 active라 부작용 위험) / `feature-draft`(가장 context-heavy — pilot로는 과함, Phase 2 우선 검증으로 분리). 기각.
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q4. ralph-loop-init(602줄) 등 대형 본문 전환 특이사항
- **Decision taken**: 동일 wrapper 템플릿 적용. 본문은 agent에 그대로 남으므로 전환 자체는 SKILL을 wrapper로 치환하는 동형 작업 — 본문 크기와 무관하게 위험 낮음. DRY 효과만 큼.
- **Alternatives considered**: 대형 본문은 보류 → DRY 동기 약화. 기각.
- **Confidence**: MEDIUM
- **User confirmation needed**: No

### Q5. codex skill→agent dispatch의 이중 실행 우려
- **Decision taken**: codex도 skill=thin dispatch(`spawn_agent`+`wait_agent`), agent=full. 이미 `.codex/skills/implementation/SKILL.md`에서 검증된 관용구라 이중 실행이 아니라 정상 위임이다.
- **Alternatives considered**: codex는 wrapping 제외(claude만) → parity 깨짐·codex 본문 중복 잔존. 기각.
- **Confidence**: MEDIUM
- **User confirmation needed**: No

---

# Part 2: Implementation Plan

## Overview

9종 mirror 스킬의 SKILL을 thin wrapper로 바꾸고(사용자 요청→agent dispatch→결과 relay), agent를 단일 full-body 소스로 둔다. wrapper는 entrypoint·artifact 계약을 유지하되 지원 못 하는 동작을 흉내내지 않는다(스펙 L62). 안전한 `plan-review` 1종을 pilot으로 템플릿을 확정한 뒤 나머지 8종을 batch(파일 disjoint → 병렬)한다. 전용 브랜치 `refactor/skills-as-agent-wrappers`에서 진행, 게이트 통과 후 커밋.

칼선: SKILL = entrypoint wrapper(dispatch+relay) / agent = full-body 소스 / Mirror Notice → pointer / dead Agent 도구·implementation-plan worker 서술 정리.

## Scope

In/Out-of-scope는 Part 1 `Scope Delta`와 동일. 요약: 9종 × (claude skill+agent, codex skill+agent). implementation·skill-only·spec 직접수정 제외.

## Components

| Component | 역할 |
|-----------|------|
| wrapper 템플릿 | SKILL을 "요청 수집 → agent dispatch → 결과 relay"로 표준화(claude/codex 각 dispatch 관용구) |
| agent 소스 정리 | dead `Agent` 도구 제거(4종) + Mirror Notice→pointer + implementation-plan worker 정직화 |
| pilot 검증 | plan-review 1종 end-to-end(템플릿·codex 경로·relay) |
| batch 전환 | 나머지 8종 동형 전환(파일 disjoint 병렬) |

### wrapper 2-모드 (C6)

원리: **agent는 파일은 read하지만 대화는 못 읽는다.** 따라서 wrapper가 무엇을 전달할지는 "그 입력이 어디 사는가"로 갈린다.

- **Mode A — pass-through (기본)**: 요청 원문 + 이미 아는 경로·산출물·결정만 relay. wrapper는 **새 read·분석을 하지 않는다**. 입력이 파일+직접 요청인 스킬(plan-review, spec-review, spec-update-done, spec-update-todo, ralph-loop-init, implementation-plan)에 적용.
- **Mode B — context-forwarding**: Mode A에 더해, **대화에만 있는 맥락**을 주제 기준 digest로 정리해 dispatch 프롬프트에 포함한다. 경계: wrapper는 *맥락을 모아 전달*까지만 하고, 분석·설계는 agent가 수행(중복 금지). **적용 스킬(동등성 게이트로 확정, 2026-06-03)**: feature-draft(요구사항·결정·기각안), **investigate**(증상·재현·기대 동작·시도한 가설 — 입력이 대화 태생), **implementation-review**(무엇을·왜 구현했는지·범위, plan 부재 시 특히).
- **모드 선택 = 동등성 게이트(H1)와 연동**: 기본 Mode A로 시도 → 게이트(직접-호출 동등성; "agent는 파일은 read하나 대화는 못 읽는다") 미통과면 Mode B로 승격 → 그래도 미통과면 mirror 유지. 게이트 결과: feature-draft·investigate·implementation-review = Mode B, 나머지 6종 = Mode A.

### wrapper 템플릿 (확정안)

**claude SKILL (`.claude/skills/<name>/SKILL.md`):** (아래는 Mode A 골격. Mode B는 "실행 1." 단계에 대화 맥락 digest 수집을 추가)
```markdown
---
name: <name>
description: "<기존 trigger description 그대로 유지>"
version: <bump>
---

# <Title> (Entrypoint Wrapper)

이 스킬은 entrypoint wrapper다. 사용자 요청을 `sdd-skills:<name>-agent`에 위임하고
그 결과를 사용자에게 전달한다. 전체 프로세스·계약·산출물 형식은 agent가 단일 소스로 보유한다.

## 실행
1. 사용자 요청 원문 + 인자 + 관련 산출물 경로(있으면)를 수집한다.
2. `Agent(subagent_type="sdd-skills:<name>-agent", prompt=<요청 + 컨텍스트>)`로 dispatch한다.
3. agent의 반환(리포트 경로·노출 결정·blocker)을 사용자에게 그대로 relay한다.

## 계약 (entrypoint·artifact 유지, 흉내 금지)
- 사용자 entrypoint(trigger)와 산출물 경로 계약은 이 wrapper가 유지한다.
- 실제 작업은 agent가 수행한다. agent가 못 하는 동작을 wrapper가 흉내내지 않는다.
- agent가 노출하는 결정/blocker/경로는 wrapper가 relay해 보존한다.

> Source: 전체 계약·프로세스는 `.claude/agents/<name>-agent.md`가 보유한다 (wrapper↔agent).
```

**codex SKILL (`.codex/skills/<name>/SKILL.md`):** 동일 구조, dispatch만 `spawn_agent(agent_type="<name>_agent", prompt=...)` 후 `wait_agent`로 결과 수거. Source pointer는 `.codex/agents/<name>-agent.toml`.

> agent 파일은 본문 유지 + (해당 시) `Agent` 도구 제거 + Mirror Notice→pointer. codex agent는 tools 배열이 없어 Notice만 정리.

**thin wrapper 판정 기준 (M1, V1과 동일)**: wrapper SKILL은 ① `### Step ` 프로세스 헤딩 0건, ② full `## Hard Rules` 다항목 목록 없음, ③ dispatch 호출 존재, ④ 본문 ≤ 40줄(frontmatter 제외)을 모두 만족해야 한다. 각 task의 "thin wrapper, full 본문 중복 0" AC는 이 기준으로 판정한다.

## Contract/Invariant Delta Coverage

| Task | Covers |
|------|--------|
| T1 (pilot plan-review) | C1, C2, C3, C4, C6(Mode A 골격), I1, I2, I3 (템플릿 확정 포함) |
| T2 feature-draft | C1, C2, C3, C4, C6(Mode B 적용) |
| T3 implementation-plan | C1, C2, C4, C5 (worker 정직화) |
| T4 implementation-review | C1, C2, C4 |
| T5 ralph-loop-init | C1, C2, C4 |
| T6 spec-review | C1, C2, C3, C4 (dead tool 제거) |
| T7 spec-update-done | C1, C2, C4 |
| T8 spec-update-todo | C1, C2, C4 |
| T9 investigate | C1, C2, C3, C4 (dead tool 제거) |
| T10 검증 | V1~V6 |

## Implementation Phases

| Phase | Tasks | 병렬성 | Checkpoint |
|-------|-------|--------|-----------|
| Phase 1 (Pilot) | T1 | 단독 — 템플릿 확정 | **true** |
| Phase 2 (Batch) | T2~T9 | 스킬별 4파일 disjoint·의존 없음 → 병렬 | **true** |
| Phase 3 (Verify) | T10 | 단독 게이트 | **true** |

> dependency: T2~T9는 T1(wrapper 템플릿, API 생산-소비)에 의존 → Phase 분리. T10은 T2~T9에 의존. Phase 2 내부는 파일 disjoint라 병렬(orchestrator 자가 적용).

## Task Details

### Task T1: plan-review를 wrapper로 전환 + 템플릿 확정 (Pilot)
**Component**: pilot 검증 / wrapper 템플릿
**Priority**: P0
**Type**: Refactor

**Description**: `plan-review`의 SKILL(claude+codex)을 위 "wrapper 템플릿"으로 치환한다. claude는 `Agent(subagent_type="sdd-skills:plan-review-agent")`, codex는 `spawn_agent(agent_type="plan_review_agent")`+`wait_agent`로 dispatch하고 결과(리포트 경로 `_sdd/implementation/<date>_plan_review_<slug>.md`·blocker 요약)를 relay한다. plan-review agent의 dead `Agent` 도구 선언을 제거하고, skill+agent Mirror Notice를 wrapper↔agent pointer로 교체한다. 이 task로 템플릿(컨텍스트 전달 형식·relay 형식·codex 경로)을 확정한다.

**Non-Goals**: agent 본문 프로세스(리뷰 로직) 변경 금지. 다른 스킬은 T2~T9.

**Acceptance Criteria**:
- [ ] claude/codex SKILL이 thin wrapper(요청 수집→dispatch→relay), full 리뷰 프로세스 본문 중복 0
- [ ] dispatch 참조: claude `sdd-skills:plan-review-agent` / codex `spawn_agent(plan_review_agent)`+`wait_agent`
- [ ] plan-review agent frontmatter `tools`에 `Agent` 없음
- [ ] skill+agent Mirror Notice → wrapper↔agent pointer
- [ ] entrypoint(trigger description)·리포트 경로 계약 보존, blocker relay 명시
- [ ] **동등성 게이트 확정(H1)**: dispatch 산출물이 직접-호출 대비 구조·노출 결정·핵심 판단 보존 — 이후 batch에 적용할 판정 기준으로 고정

**Target Files**:
- [M] `.claude/skills/plan-review/SKILL.md`
- [M] `.claude/agents/plan-review-agent.md`
- [M] `.codex/skills/plan-review/SKILL.md`
- [M] `.codex/agents/plan-review-agent.toml`

**Technical Notes**: Covers C1,C2,C3,C4,I1,I2,I3. 템플릿은 Components 절 참조. plan-review는 read-only 리포트 산출이라 컨텍스트 전달 위험 낮음 — 메커니즘 검증에 적합(Q3).
**Dependencies**: 없음

---

### Task T2: feature-draft를 wrapper로 전환
**Component**: batch 전환
**Priority**: P0
**Type**: Refactor

**Description**: `feature-draft` SKILL(claude+codex)을 **Mode B(context-forwarding) wrapper**로 치환(dispatch=`sdd-skills:feature-draft-agent` / `spawn_agent(feature_draft_agent)`). feature-draft agent의 dead `Agent` 도구 제거, Mirror Notice→pointer. **입력이 대화 태생인 유일 스킬**(Q1·C6)이므로, wrapper는 ① 요청 원문 + 관련 spec/draft 경로(Mode A) 위에 ② **대화에만 있는 맥락**(이번 세션의 요구사항·결정·제약·기각한 대안)을 주제 기준 digest로 정리해 dispatch 프롬프트에 포함한다. 경계: wrapper는 맥락 모아 전달까지만 하고 요구사항 분석·delta 설계는 agent가 수행(중복 금지). agent의 결정 surfacing(Step 8) 출력이 반환→relay로 보존됨을 확인한다.

**Non-Goals**: feature-draft agent 본문 프로세스 변경 금지.

**Acceptance Criteria**:
- [ ] claude/codex SKILL이 thin wrapper, full 본문 중복 0
- [ ] dispatch 참조 정확(claude prefix / codex spawn_agent)
- [ ] feature-draft agent `tools`에 `Agent` 없음
- [ ] Mirror Notice → pointer
- [ ] **Mode B(C6)**: wrapper가 대화 태생 맥락(요구사항·결정·제약·기각안) digest를 정리해 전달, 요구사항 분석은 agent에 위임(중복 없음)
- [ ] agent의 결정 노출(Step 8)이 반환→relay로 보존(I3), 동등성 게이트 통과

**Target Files**:
- [M] `.claude/skills/feature-draft/SKILL.md`
- [M] `.claude/agents/feature-draft-agent.md`
- [M] `.codex/skills/feature-draft/SKILL.md`
- [M] `.codex/agents/feature-draft-agent.toml`

**Technical Notes**: Covers C1,C2,C3,C4. context-heavy(Q1) — Phase 2에서 우선 검증.
**Dependencies**: T1

---

### Task T3: implementation-plan을 wrapper로 전환 (+ worker 정직화)
**Component**: batch 전환
**Priority**: P0
**Type**: Refactor

**Description**: `implementation-plan` SKILL(claude+codex)을 wrapper로 치환(dispatch=`sdd-skills:implementation-plan-agent` / `spawn_agent(implementation_plan_agent)`). Mirror Notice→pointer. agent 본문의 "독립 섹션은 `worker` agent로 bounded 병렬 fill할 수 있다" 서술을 **"dispatch 경로에서는 worker spawn 불가 → 순차 fill"**로 정직화한다(C5, spec L62; 순차 degrade 사용자 확정). implementation-plan agent의 `Agent` 도구는 dispatch 경로에서 worker spawn이 불가하므로 **제거로 확정**한다(다른 4종과 일관, 미사용·오용 방지 — M2 반영).

**Non-Goals**: 그룹화/dependency 인코딩 로직(직전 작업) 변경 금지.

**Acceptance Criteria**:
- [ ] claude/codex SKILL이 thin wrapper, full 본문 중복 0
- [ ] dispatch 참조 정확
- [ ] agent worker 병렬 fill 서술이 "dispatch 시 순차 degrade"로 정직화(조용한 흉내 제거)
- [ ] implementation-plan agent `tools`에 `Agent` 없음 (제거 확정, M2)
- [ ] Mirror Notice → pointer

**Target Files**:
- [M] `.claude/skills/implementation-plan/SKILL.md`
- [M] `.claude/agents/implementation-plan-agent.md`
- [M] `.codex/skills/implementation-plan/SKILL.md`
- [M] `.codex/agents/implementation-plan-agent.toml`

**Technical Notes**: Covers C1,C2,C4,C5. 유일한 선택적 fan-out(Q2).
**Dependencies**: T1

---

### Task T4: implementation-review를 wrapper로 전환
**Component**: batch 전환
**Priority**: P0
**Type**: Refactor

**Description**: `implementation-review` SKILL(claude+codex)을 wrapper로 치환(dispatch=`sdd-skills:implementation-review-agent` / `spawn_agent(implementation_review_agent)`). Mirror Notice→pointer. agent는 직전 작업에서 이미 `Agent` 도구가 제거됨(추가 제거 불필요). 리뷰 lane 순차 서술은 유지.

**Non-Goals**: 리뷰 lane 로직 변경 금지(직전 작업 결과 보존).

**Acceptance Criteria**:
- [ ] claude/codex SKILL이 thin wrapper, full 본문 중복 0
- [ ] dispatch 참조 정확
- [ ] Mirror Notice → pointer
- [ ] agent `tools`에 `Agent` 없음(직전 상태 유지 확인)

**Target Files**:
- [M] `.claude/skills/implementation-review/SKILL.md`
- [M] `.claude/agents/implementation-review-agent.md`
- [M] `.codex/skills/implementation-review/SKILL.md`
- [M] `.codex/agents/implementation-review-agent.toml`

**Technical Notes**: Covers C1,C2,C4.
**Dependencies**: T1

---

### Task T5: ralph-loop-init을 wrapper로 전환
**Component**: batch 전환
**Priority**: P0
**Type**: Refactor

**Description**: `ralph-loop-init` SKILL(claude+codex, 602/603줄 — 최대 DRY 효과)을 wrapper로 치환(dispatch=`sdd-skills:ralph-loop-init-agent` / `spawn_agent(ralph_loop_init_agent)`). Mirror Notice→pointer. 본문은 agent에 그대로 유지(동형 전환, Q4).

**Non-Goals**: agent 본문(루프 init 로직) 변경 금지.

**Acceptance Criteria**:
- [ ] claude/codex SKILL이 thin wrapper, full 본문 중복 0
- [ ] dispatch 참조 정확
- [ ] Mirror Notice → pointer
- [ ] entrypoint·artifact 계약 보존

**Target Files**:
- [M] `.claude/skills/ralph-loop-init/SKILL.md`
- [M] `.claude/agents/ralph-loop-init-agent.md`
- [M] `.codex/skills/ralph-loop-init/SKILL.md`
- [M] `.codex/agents/ralph-loop-init-agent.toml`

**Technical Notes**: Covers C1,C2,C4. ralph-loop-init agent는 Agent 도구 미보유(census).
**Dependencies**: T1

---

### Task T6: spec-review를 wrapper로 전환
**Component**: batch 전환
**Priority**: P0
**Type**: Refactor

**Description**: `spec-review` SKILL(claude+codex)을 wrapper로 치환(dispatch=`sdd-skills:spec-review-agent` / `spawn_agent(spec_review_agent)`). spec-review agent의 dead `Agent` 도구 제거, Mirror Notice→pointer.

**Non-Goals**: 리뷰 로직 변경 금지.

**Acceptance Criteria**:
- [ ] claude/codex SKILL이 thin wrapper, full 본문 중복 0
- [ ] dispatch 참조 정확
- [ ] spec-review agent `tools`에 `Agent` 없음
- [ ] Mirror Notice → pointer

**Target Files**:
- [M] `.claude/skills/spec-review/SKILL.md`
- [M] `.claude/agents/spec-review-agent.md`
- [M] `.codex/skills/spec-review/SKILL.md`
- [M] `.codex/agents/spec-review-agent.toml`

**Technical Notes**: Covers C1,C2,C3,C4.
**Dependencies**: T1

---

### Task T7: spec-update-done을 wrapper로 전환
**Component**: batch 전환
**Priority**: P0
**Type**: Refactor

**Description**: `spec-update-done` SKILL(claude+codex)을 wrapper로 치환(dispatch=`sdd-skills:spec-update-done-agent` / `spawn_agent(spec_update_done_agent)`). Mirror Notice→pointer. 본문의 "worker retry/backoff 정책" 언급은 ralph 루프 워커 정책 서술이지 자기 fan-out이 아님을 확인(자기 spawn 아니면 그대로 유지).

**Non-Goals**: spec 머지 로직 변경 금지.

**Acceptance Criteria**:
- [ ] claude/codex SKILL이 thin wrapper, full 본문 중복 0
- [ ] dispatch 참조 정확
- [ ] Mirror Notice → pointer
- [ ] artifact(progress/report 소비) 경로 계약 보존

**Target Files**:
- [M] `.claude/skills/spec-update-done/SKILL.md`
- [M] `.claude/agents/spec-update-done-agent.md`
- [M] `.codex/skills/spec-update-done/SKILL.md`
- [M] `.codex/agents/spec-update-done-agent.toml`

**Technical Notes**: Covers C1,C2,C4. agent는 Agent 도구 미보유(census).
**Dependencies**: T1

---

### Task T8: spec-update-todo를 wrapper로 전환
**Component**: batch 전환
**Priority**: P0
**Type**: Refactor

**Description**: `spec-update-todo` SKILL(claude+codex)을 wrapper로 치환(dispatch=`sdd-skills:spec-update-todo-agent` / `spawn_agent(spec_update_todo_agent)`). Mirror Notice→pointer.

**Non-Goals**: spec todo 머지 로직 변경 금지.

**Acceptance Criteria**:
- [ ] claude/codex SKILL이 thin wrapper, full 본문 중복 0
- [ ] dispatch 참조 정확
- [ ] Mirror Notice → pointer

**Target Files**:
- [M] `.claude/skills/spec-update-todo/SKILL.md`
- [M] `.claude/agents/spec-update-todo-agent.md`
- [M] `.codex/skills/spec-update-todo/SKILL.md`
- [M] `.codex/agents/spec-update-todo-agent.toml`

**Technical Notes**: Covers C1,C2,C4. agent는 Agent 도구 미보유(census).
**Dependencies**: T1

---

### Task T9: investigate를 wrapper로 전환
**Component**: batch 전환
**Priority**: P0
**Type**: Refactor

**Description**: `investigate` SKILL(claude+codex)을 wrapper로 치환(dispatch=`sdd-skills:investigate-agent` / `spawn_agent(investigate_agent)`). investigate agent의 dead `Agent` 도구 제거, Mirror Notice→pointer.

**Non-Goals**: 디버깅 로직 변경 금지.

**Acceptance Criteria**:
- [ ] claude/codex SKILL이 thin wrapper, full 본문 중복 0
- [ ] dispatch 참조 정확
- [ ] investigate agent `tools`에 `Agent` 없음
- [ ] Mirror Notice → pointer

**Target Files**:
- [M] `.claude/skills/investigate/SKILL.md`
- [M] `.claude/agents/investigate-agent.md`
- [M] `.codex/skills/investigate/SKILL.md`
- [M] `.codex/agents/investigate-agent.toml`

**Technical Notes**: Covers C1,C2,C3,C4.
**Dependencies**: T1

---

### Task T10: 검증 게이트
**Component**: Verification Gate
**Priority**: P0
**Type**: Test

**Description**: V1~V6 실행. 정적(V1-V5: grep/diff) + 런타임 smoke(V6: reload 후 pilot+batch 1종 호출 → agent dispatch·리포트 산출·relay·sub-agent 미spawn 확인). 실패는 해당 task 복귀. 커밋은 게이트 통과 후.

**Acceptance Criteria**:
- [ ] V1: 9종(또는 동등성 통과분) SKILL이 thin wrapper — 측정 기준(`### Step ` 0건 + full Hard Rules 부재 + dispatch 호출 존재 + 본문 ≤40줄) 충족 (M1)
- [ ] V2: dispatch 참조(claude prefix / codex spawn_agent) 정확
- [ ] V3: 5종 agent(feature-draft/plan-review/spec-review/investigate/implementation-plan) `Agent` 도구 없음 (M2)
- [ ] V4: Mirror Notice→pointer, implementation-plan worker 정직화
- [ ] V5: claude/codex 대칭
- [ ] **동등성 게이트(H1)**: wrap된 각 스킬이 직접-호출 대비 산출물 구조·노출 결정·핵심 판단 보존(미통과분은 mirror 유지로 기록, wrap 대상에서 제외)
- [ ] V6: 런타임 smoke(pilot+1) 또는 reload 불가 시 명시 기록 + 사용자 보고

**Target Files**:
- [M] `_sdd/drafts/2026-06-03_feature_draft_skills_as_agent_wrappers.md` -- 검증 결과 기록(검증만)

**Technical Notes**: Covers V1~V6.
**Dependencies**: T2, T3, T4, T5, T6, T7, T8, T9

## Parallel Execution Summary

- **Phase 1 (T1)**: 단독 pilot — wrapper 템플릿(API 생산) 확정. Checkpoint.
- **Phase 2 (T2~T9)**: 각 스킬의 4파일이 완전 disjoint, 의존 없음(공유 schema 없음) → **8개 병렬 dispatch 가능**(orchestrator 그룹 파생 규칙 자가 적용). T1(템플릿)에만 의존.
- **Phase 3 (T10)**: 단독 게이트.
- **충돌 메모**: 스킬 간 파일 겹침 0. 공통 의존은 "T1이 정한 템플릿"이라는 API 생산-소비뿐 → dependency edge로 T1→T2~T9.

## Risks and Mitigations

| Risk | Mitigation |
|------|-----------|
| wrapper 컨텍스트 전달 부족으로 품질 저하(특히 feature-draft) | wrapper가 요청 원문+관련 경로 명시 전달, agent 자체 read. pilot(plan-review)·feature-draft에 **동등성 게이트(H1)** 적용 — 직접-호출 대비 동등성 깨지면 **그 스킬은 mirror 유지**(wrap 제외). "통과분만 wrap"으로 commit 조정 |
| dispatch된 agent가 또 spawn 시도(nesting) | census상 core fan-out 0. implementation-plan worker만 정직화(C5). 그 외 spawn 없음(I1) |
| 사용자 노출(결정/blocker) 손실 | agent 반환을 wrapper가 relay(I3), pilot에서 확인 |
| codex spawn_agent 경로 미검증 | 이미 implementation SKILL에서 사용 중. pilot에서 codex 정적 + 가능 시 런타임 |
| 본문 동기화 의무 혼선 | Mirror Notice→pointer로 "agent 단일 소스" 명시(C4) |
| V6 reload 세션 캐시 | reload/새 세션 후 실행, 불가 시 명시 기록 |

## Open Questions

- in-scope 미결: Q1(컨텍스트 전달)은 **동등성 게이트 + mirror fallback(H1)**로 닫는다 — 통과분만 wrap. Q2(순차 degrade)·Q3(pilot)·Q5는 결정됨. Q4(대형 본문)는 동형 전환으로 저위험.
- plan-review(`_sdd/implementation/2026-06-03_plan_review_skills_as_agent_wrappers.md`) 반영: **H1**(Q1 exit 기준·mirror fallback 추가 → "통과분만 wrap") + **M1**(V1 측정 기준: `### Step ` 0 + Hard Rules 부재 + dispatch 호출 + ≤40줄) + **M2**(implementation-plan `Agent` 도구 제거 확정, 대상 5종) + L1/L2(wrapper 최소 골격·인접 cleanup 추적성, 주석 수준).
- 후속: 머지 후 Part 1 delta(C1~C5, I1~I4)를 `spec-update-todo`로 canonical spec에 반영.

---

## Part 2 Self-Containment Check (Hard Rule 11)

- **검토 섹션 수**: 10개 task(T1~T10) + Overview/Scope/Components/Phases/Parallel/Risks.
- **Pass 1 (외부 참조 inline purpose)**:
  - 근거 토론·선행 머지: 상단에 경로+합의 재진술(통합 규칙, implementation 별도 해결). bare path 아님. ✓
  - census(2026-06-03): 후보 9종·core fan-out 0·interactive 0를 재진술. ✓
  - 스펙 L59/L62/L90: "skill=entrypoint·agent=reusable·wrapper-backed·흉내 금지"를 재진술로 근거. ✓
  - 고유 용어(wrapper, dispatch, relay, core fan-out, dead Agent 도구, worker 병렬 fill, nesting): 최초 사용 지점에 정의/근거. ✓
  - C/I/V ID: Part 1 정의 후 Coverage·Technical Notes에서 ID+purpose 참조. ✓
- **Pass 2 (생초 독자 readthrough)**:
  - 발견 갭: "agent는 안 바뀌나?"가 모호 → 각 task에 "agent 본문 유지 + tool/Notice 정리"로 명시, T3는 worker 정직화 예외 명시.
  - 발견 갭: implementation-review는 이미 Agent 도구 제거됨(직전 작업) → T4에 "추가 제거 불필요, 상태 유지 확인"으로 구분.
  - 발견 갭: "왜 plan-review가 pilot인가" → Q3 + T1 Technical Notes에 근거(read-only·컨텍스트 위험 낮음).
- **보완 완료**: Yes
