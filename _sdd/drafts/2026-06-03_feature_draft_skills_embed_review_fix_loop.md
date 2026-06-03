# Feature Draft: 세 스킬에 producer→review→fix loop 내장 + feature-draft/implementation-plan orchestrator 승격

# Part 1: Temporary Spec Draft

## Change Summary

세 스킬(`implementation`, `feature-draft`, `implementation-plan`)이 자기 산출물의 품질 gate를 **자체 소유**하도록, autopilot의 review→fix→re-review loop 패턴을 각 스킬 안에 내장한다.

- **무엇이 바뀌나**:
  1. `implementation`: 현재 Step 6 Phase Review의 *인라인* 경량 self-review(Critical만 leaf 재dispatch)를 **외부 `implementation-review-agent` loop**(review→fix→re-review)로 교체한다.
  2. `feature-draft` / `implementation-plan`: 현재 thin **entrypoint wrapper**(요청을 producer-agent에 위임하고 결과를 relay)를 **orchestrator**로 승격해, 산출 직후 producer→`plan-review-agent`→fix loop를 메인 루프(스킬)가 직접 돌린다.
  3. 두 producer-agent(`feature-draft-agent`, `implementation-plan-agent`)에 **fix mode** 입력 계약을 추가한다 — review 리포트 경로 + 기존 산출물 경로를 받아 자기 산출물을 finding 반영 수정한다.
- **왜 바뀌나**: 각 스킬을 직접(autopilot 없이) 호출하는 경로에서도 산출물이 review gate를 통과하도록 보장하기 위해서다. 현재는 `implementation`만 인라인 self-review가 있고(외부 reviewer 미사용), `feature-draft`/`implementation-plan`은 review gate가 전혀 없다.
- **왜 지금 이 구조인가**: 세 producer/reviewer agent 모두 Agent 도구를 보유하지 않아 sub-agent를 spawn하지 못한다. 따라서 loop orchestration은 반드시 메인 루프(스킬)가 소유해야 하며, 이는 `feature-draft`/`implementation-plan` wrapper를 orchestrator로 승격해야 함을 강제한다. 이번 변경의 핵심 메커니즘(스킬이 loop만 소유 + fix=producer-agent 재dispatch + 산출물 단일 작성자 유지)의 검증된 선례는 `implementation` 스킬이다 — orchestrator가 review-fix loop를 소유하고 fix를 `implementation-agent` leaf에 재dispatch하는 구조가 이미 동작한다. (참고로 `investigate`도 wrapper를 제거하고 인라인 소유로 전환한 선례지만, read-only Explore fan-out이며 fix를 orchestrator가 인라인 write하므로 본 변경의 review-fix·재dispatch 메커니즘과는 별개다.)
- **범위 경계**: autopilot은 건드리지 않는다. autopilot이 만드는 오케스트레이터는 스킬이 아니라 `*-agent` leaf를 직접 dispatch하므로 스킬 내장 loop와 실행 경로가 겹치지 않는다(개념적 유사 ≠ 이중 실행).

## Scope Delta

**In-scope**:
- `implementation` 스킬의 Step 6 인라인 Phase Review → 외부 `implementation-review-agent` review→fix→re-review loop 교체 (claude + codex).
- `feature-draft` 스킬 wrapper → orchestrator 승격: Mode B 맥락 forwarding 유지 + producer 산출 직후 `plan-review-agent` loop 소유 (claude + codex).
- `implementation-plan` 스킬 wrapper → orchestrator 승격: producer 산출 직후 `plan-review-agent` loop 소유 (claude + codex).
- `feature-draft-agent` / `implementation-plan-agent`에 fix mode 입력 계약 추가 (claude + codex).
- 세 loop 공통 정책: exit `critical=high=medium=0`, MAX 기본 3회, re-review scope = loop 범위 전체.

**Out-of-scope**:
- autopilot SKILL 및 `orchestrator-contract.md` 수정 (실행 경로 비중첩 — 결정 1).
- `implementation-agent`의 본문 계약 변경 (이미 fix dispatch 대상인 TDD leaf — fix mode 추가 불필요, I3 참조).
- `plan-review-agent` / `implementation-review-agent`의 review 본문 계약 변경 (입력으로 plan/draft Part 2/구현 상태를 이미 수용하므로 재사용만).
- `_sdd/spec/*` 파일의 실제 수정 (Hard Rule: spec 불가침). global spec delta는 본 Part 1로만 기술하고, 실제 머지는 후속 `spec-update-todo`/`spec-update-done` 대상.

**Guardrail delta**:
- 산출물 단일 작성자 불변식 유지: producer-agent만 자기 산출물을 write/수정한다. orchestrator(스킬)는 loop만 소유하고 산출물을 직접 rewrite하지 않는다(I1).
- nesting 1단계 제한 유지: 승격된 스킬은 메인 루프이므로 leaf agent를 dispatch할 수 있다. producer/reviewer agent는 여전히 leaf로 sub-agent를 spawn하지 않는다.

## Contract/Invariant Delta

| ID | Type | Change | Why |
|----|------|--------|-----|
| C1 | Modify | `implementation` 스킬 Step 6: 인라인 self-review → 외부 `implementation-review-agent` review→fix→re-review loop. fix=`implementation-agent` leaf 재dispatch(finding 순차), exit `critical=high=medium=0` | 직접 호출 경로도 외부 reviewer gate를 통과하게 함 (결정 6) |
| C2 | Modify | `feature-draft` 스킬: entrypoint wrapper → orchestrator. Mode B 맥락 forwarding 유지 + producer 산출 직후 `plan-review-agent` review→fix→re-review loop 소유 | wrapper는 leaf를 spawn 못 하므로 loop를 메인 루프가 소유 (결정 2, 7) |
| C3 | Modify | `implementation-plan` 스킬: entrypoint wrapper → orchestrator. producer 산출 직후 `plan-review-agent` review→fix→re-review loop 소유 | C2와 동형 (결정 2) |
| C4 | Add | `feature-draft-agent` / `implementation-plan-agent`에 fix mode 입력 계약: (review 리포트 경로 + 기존 산출물 경로 + 대상 findings) → finding 반영 수정. 생성 mode와 fix mode를 입력 신호로 분기 | fix=producer-agent 재dispatch이므로 producer가 자기 산출물 수정 (결정 3, 10) |
| C5 | Add | 세 loop 공통 정책 계약: exit `critical=high=medium=0`, MAX 기본 3회, re-review scope=loop 범위 전체, MAX 도달 분기(critical/high 잔존→중단·보고, medium만→로그 후 진행) | autopilot loop 계약과 통일 (결정 4, 5, 9) |
| C6 | Modify | 승격된 ②③ 스킬의 Role/Source Pointer 재정의: agent는 여전히 산출물 **producer 단일 소스**지만 스킬이 **loop를 소유**하는 orchestrator임을 명시(Role Pointer) | wrapper→orchestrator 승격으로 "Source Pointer = agent가 단일 소스" 문구가 부정확해짐 |
| I1 | Add | 산출물 단일 작성자 불변식: 각 산출물(draft/plan/code)은 producer-agent(또는 implementation leaf)만 write한다. orchestrator 스킬은 loop만 소유하고 산출물을 직접 rewrite하지 않는다 | fix=producer 재dispatch 결정의 핵심 보장 (결정 3) |
| I2 | Add | loop 종료 불변식: 세 스킬의 review gate는 exit 조건 충족 또는 MAX 도달 전에는 다음 단계로 진행하지 않는다(`implementation`은 다음 phase/완료, ②③은 사용자 relay) | autopilot gate 불변식과 동형 |
| I3 | Keep | `implementation-agent` leaf는 fix mode 별도 계약 없이 finding을 fix-task(task 필드 + Target Files)로 받아 기존 TDD 계약으로 처리한다 | leaf는 이미 단일 task TDD 수행자 — 새 분기 불필요 (확정할 세부) |

## Touchpoints

현재 코드 기준 재확인 결과 (Strategic Code Map은 본 repo에서 별도 heading으로 존재하지 않아 직접 파일 탐색):

- `.claude/skills/implementation/SKILL.md` **Step 6 Phase Review** (현재 145–215행 영역): "orchestrator가 경량 품질 리뷰를 수행" + 품질 체크 표 + Decision Gate 표. → 외부 `implementation-review-agent` 호출 + fix(`implementation-agent` 재dispatch) + re-review로 교체. Step 4 fan-out 루프의 "전체 그룹 완료 → Phase Review (Step 6)" 줄도 loop 진입점으로 연결.
  - 동일 구조 mirror: `.codex/skills/implementation/SKILL.md` (Step 6, 178–192행 영역; spawn_agent/wait_agent 표기).
- `.claude/skills/feature-draft/SKILL.md` 전체 (31행): 현재 Mode B wrapper 3-step(수집→dispatch→relay). → orchestrator로 재작성: digest 수집 → producer dispatch → `plan-review-agent` loop → relay. "Source" pointer(30행) → Role Pointer로 변경.
  - mirror: `.codex/skills/feature-draft/SKILL.md` (spawn_agent/wait_agent).
- `.claude/skills/implementation-plan/SKILL.md` 전체 (24행): Mode A pass-through wrapper. → orchestrator로 재작성: 입력 수집 → producer dispatch → `plan-review-agent` loop → relay.
  - mirror: `.codex/skills/implementation-plan/SKILL.md`.
- `.claude/agents/feature-draft-agent.md` (Process / Source Pointer): fix mode 입력 계약 섹션 추가, mode 분기 서술.
  - mirror: `.codex/agents/feature-draft-agent.toml` (developer_instructions).
- `.claude/agents/implementation-plan-agent.md` (Process / Source Pointer): fix mode 입력 계약 섹션 추가.
  - mirror: `.codex/agents/implementation-plan-agent.toml`.
- 참조만 (수정 없음, read-only): `.claude/agents/plan-review-agent.md`(reviewer 계약·리포트 경로 `_sdd/implementation/<date>_plan_review_<slug>.md`·Blocker Status), `.claude/agents/implementation-review-agent.md`(reviewer), `.claude/agents/implementation-agent.md`(fix leaf), `.claude/skills/sdd-autopilot/references/orchestrator-contract.md`(loop 계약 참조 템플릿).

## Implementation Plan

1. **공통 loop 정책 확정** (Part 2 Phase 0): exit/MAX/re-review scope/리포트 소유/iteration 단계 경계를 한 곳에서 결정해 세 스킬에 동일 적용.
2. **① `implementation` Step 6 교체** (Phase 1): 인라인 Phase Review → 외부 review→fix→re-review loop. claude/codex 동시. multi-phase loop scope는 실행분(phase) 단위 1 gate로 단순화(YAGNI).
3. **producer-agent fix mode 추가** (Phase 2): `feature-draft-agent`/`implementation-plan-agent`에 fix mode 입력 계약·분기 서술 추가. claude/codex 동시. (②③ 승격이 이 계약에 의존하므로 선행.)
4. **②③ 스킬 wrapper→orchestrator 승격** (Phase 3): `feature-draft`/`implementation-plan` 스킬을 loop-owning orchestrator로 재작성, Role Pointer 재정의. claude/codex 동시. Phase 2 fix mode에 의존.
5. **정적 게이트 + smoke 검증** (Phase 4): grep/diff로 계약 일관성·parity 확인, reload 후 런타임 smoke.

순서 근거: fix mode 계약(C4)이 ②③ 승격(C2/C3)의 전제이므로 Phase 2가 Phase 3보다 앞선다. ①(C1)은 producer fix mode와 의미적으로 독립(leaf 재dispatch라 I3)이나 orchestrator 병렬은 same-phase에서만 표현 가능하므로 별도 phase로 순차 진행하며, 공통 정책(C5) 확정 후 시작한다.

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, I2 | review, static grep | `implementation` SKILL(claude+codex) Step 6에 외부 `implementation-review-agent` 호출·fix(`implementation-agent` 재dispatch)·re-review·exit 조건이 명시되고, 인라인 self-review 문구가 제거됐는지 grep 확인 |
| V2 | C2, C3, I2 | review, static grep | ②③ SKILL(claude+codex)이 orchestrator로 재작성되어 producer dispatch 후 `plan-review-agent` loop·exit·MAX를 소유하는지 확인. wrapper-only 문구("위임하고 relay") 잔존 없음 |
| V3 | C4, I1 | review, static grep | 두 producer-agent(claude .md + codex .toml)에 fix mode 입력 계약(리포트 경로+산출물 경로+findings)과 mode 분기가 추가됐는지 확인. 산출물 단일 작성자 유지. fix mode 적용 후에도 codex `feature-draft-agent`의 `<!-- spec-update-todo-input-start -->` / `<!-- spec-update-todo-input-end -->` 마커가 grep으로 존재 확인됨(surgical 수정이 마커 유실하지 않음) |
| V4 | C5 | review | 세 loop의 exit(`critical=high=medium=0`)·MAX(3)·re-review scope(전체)·MAX 분기가 동일 정책으로 기술됐는지 cross-check |
| V5 | C6 | review, static grep | ②③ SKILL의 Role/Source Pointer가 "agent=producer 단일 소스 + skill=loop orchestrator"로 재정의됐는지 확인 |
| V6 | C1–C6, I1–I3 | reload smoke | 플러그인 reload 후 `/implementation`·`/feature-draft`·`/implementation-plan` trigger가 정상 resolve되고, dispatch 표기(claude `sdd-skills:` prefix / codex `*_agent`)가 유효한지 smoke |
| V7 | I3 | review | `implementation-agent`(claude .md + codex .toml) 본문이 변경 없이도 finding을 fix-task로 처리 가능함을 근거로 명시 확인. 불필요 시 미변경 근거 기록 |

## Risks / Open Questions

### Q1. 승격된 ②③ orchestrator에서 `plan_review` 리포트와 산출물의 소유/생성 주체 분리
- **Decision taken**: `plan-review-agent`가 자기 리포트(`_sdd/implementation/<date>_plan_review_<slug>.md`)를 소유·생성한다(현 계약 유지). producer-agent는 draft/plan 산출물을 소유한다. orchestrator(스킬)는 loop를 돌리고 두 경로를 fix dispatch에 전달만 한다. ①의 경우 `implementation-review-agent`가 review 리포트를, orchestrator가 `implementation_report`를 소유(현 계약 유지).
- **Alternatives considered**: (a) orchestrator가 plan_review 리포트를 직접 작성 — `plan-review-agent`가 이미 리포트 write 계약을 보유하므로 중복·단일 작성자 위반. (b) producer-agent가 review 리포트도 작성 — reviewer/producer 역할 혼선.
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q2. multi-phase `implementation`의 loop scope (global vs per-group)를 자체적으로 가질지
- **Decision taken**: `implementation` 스킬은 autopilot의 global/per-group scope 개념을 자체 도입하지 않고, **실행분(phase) 단위 1 gate**로 단순화한다. 각 phase 완료 직후 review→fix→re-review를 1회 닫고 다음 phase로 진행한다(YAGNI — 직접 호출 경로는 autopilot의 Checkpoint 그룹핑 메타데이터를 소비하지 않음).
- **Alternatives considered**: autopilot의 per-group scope·Checkpoint 메타 차용 — 직접 호출 경로엔 Checkpoint 신호를 줄 상위 오케스트레이터가 없어 사변적 복잡도. global 1회만 — multi-phase에서 후반 phase 결함이 누적돼 fix 비용 증가.
- **Confidence**: MEDIUM
- **User confirmation needed**: No

### Q3. `implementation-agent`에 fix mode 별도 계약이 필요한가
- **Decision taken**: 불필요. `implementation-agent`는 이미 단일 task를 TDD로 수행하는 leaf이고, orchestrator가 review finding을 fix-task(task 필드 + Target Files = finding 영향 파일)로 변환해 기존 dispatch 계약으로 넘기면 충분하다(I3). autopilot의 `fix = implementation 재호출` 계약과 동형. `implementation-agent` 본문은 변경하지 않는다.
- **Alternatives considered**: leaf에 명시적 fix mode 추가 — leaf 계약 비대화, autopilot fix 계약과 불일치. producer-agent fix mode(C4)와 비대칭이나, ②③ producer는 "문서 전체를 재작성하는 단일 작성자"라 mode 분기가 필요한 반면 implementation leaf는 "task 단위 실행자"라 finding 자체가 task로 매핑되는 구조적 차이가 있음.
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q4. producer-agent fix mode 입력 신호로 "생성 vs fix"를 어떻게 분기하나
- **Decision taken**: dispatch 프롬프트에 **review 리포트 경로 + 기존 산출물 경로 + 대상 findings**가 포함되면 fix mode, 없으면 생성 mode로 분기한다. fix mode에서 agent는 기존 산출물을 read하고 findings에 해당하는 부분만 수정하며 전체 재작성하지 않는다(I1 단일 작성자 유지, surgical change).
- **Alternatives considered**: 명시적 `mode: fix` 플래그 토큰 — 입력 존재 신호로 충분해 추가 토큰은 과잉. 매 라운드 전체 재생성 — 수렴 불안정·기존 결정 유실 위험.
- **Confidence**: MEDIUM
- **User confirmation needed**: No

### Q5. 승격 시 기존 wrapper의 Source Pointer / Mirror Notice 처리
- **Decision taken**: ②③ SKILL의 "Source: agent가 단일 소스" 문구를 **Role Pointer**로 교체한다 — "agent는 산출물 producer 단일 소스, 스킬은 loop를 소유하는 orchestrator". 이 형태는 `implementation` 스킬이 이미 갖춘 "orchestrator가 loop 소유 + leaf는 producer/fix 수행자" Role Pointer와 동형이다(②③ 승격의 검증된 선례). `implementation` 스킬의 기존 Role Pointer(orchestrator↔leaf)는 유지하되 Step 6 외부 loop 반영. agent 본문의 Source Pointer는 "producer 단일 소스"로 유지(loop 소유 주체가 스킬임을 한 줄 보강).
- **Alternatives considered**: Source Pointer 문구 그대로 유지 — wrapper→orchestrator 승격 후 "thin wrapper" 서술이 사실과 불일치(검증 V5 실패). 동형 선례로 `investigate`를 인용 — investigate는 review-fix loop가 아니라 read-only Explore fan-out이고 fix를 orchestrator가 인라인 write하므로 본 변경의 재dispatch 메커니즘 선례로 부정확(기각).
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q6. loop 한 iteration의 정확한 단계 경계 (re-review 시점/횟수)
- **Decision taken**: 1 iteration = `review(또는 re-review) → (finding>0이면) fix → 산출물 갱신`. re-review는 fix 직후 새 iteration의 review로 수행하며, 매 iteration마다 loop 범위 **전체**를 재리뷰한다(변경분만 아님, 결정 9). exit 조건(critical=high=medium=0) 충족 시 즉시 종료, 미충족이면 MAX(3)까지 반복. MAX 도달 시 critical/high 잔존→중단·사용자 보고, medium만 잔존→로그 후 진행.
- **Alternatives considered**: 변경분만 re-review — 누락된 cross-finding 회귀 위험, autopilot 계약과 불일치. fix 없이 review만 반복 — 무의미.
- **Confidence**: HIGH
- **User confirmation needed**: No

---

# Part 2: Implementation Plan

## Overview

이 계획은 SDD workflow bundle의 세 entrypoint 스킬(`implementation`, `feature-draft`, `implementation-plan`)에 producer→review→fix→re-review loop를 내장하고, 그중 `feature-draft`/`implementation-plan`을 thin wrapper에서 loop-owning orchestrator로 승격하는 self-referential 리팩터다.

용어 정의 (이 문서 고유 사용):
- **orchestrator skill**: 메인 루프에서 실행되어 leaf agent를 dispatch할 수 있는 스킬(`_sdd/spec/main.md` 59행 "orchestrator(skill) + leaf(agent)" 모델). 이번 변경으로 `feature-draft`/`implementation-plan`이 이 형태가 된다.
- **entrypoint wrapper**: 요청을 producer-agent에 위임하고 결과를 relay만 하는 thin 스킬(현재 `feature-draft`/`implementation-plan`의 상태). 이번 변경으로 제거된다.
- **producer-agent**: 산출물(draft 또는 plan)을 write하는 단일 작성자 agent — `feature-draft-agent`, `implementation-plan-agent`.
- **fix mode**: producer-agent가 review 리포트 + 기존 산출물 경로를 입력받아 finding을 반영해 자기 산출물을 surgical 수정하는 dispatch 모드(Part 1 Contract C4 — fix=producer 재dispatch).
- **review-fix loop**: review→fix→re-review 반복 gate. autopilot의 `references/orchestrator-contract.md` §6 Review-Fix Contract를 직접 호출 경로용으로 차용. exit `critical=high=medium=0`, MAX 기본 3회.

대상 플랫폼: claude(`.claude/`)와 codex(`.codex/`) 양쪽. claude는 `Agent(subagent_type="sdd-skills:<name>-agent")`, codex는 `spawn_agent(agent_type="<name>_agent")` + `wait_agent`로 dispatch한다.

이 계획은 코드 산출물이 아니라 skill/agent 마크다운 계약 파일을 수정하는 문서 리팩터이므로, "테스트"는 정적 게이트(grep/diff로 계약 일관성·pl`atform parity 확인)와 reload 후 런타임 smoke(trigger resolve)로 대체한다(`_sdd/env.md`상 테스트 프레임워크 없음).

## Scope

### In Scope
- `implementation` 스킬(claude+codex)의 Step 6 인라인 Phase Review를 외부 `implementation-review-agent` review→fix→re-review loop로 교체 (Part 1 Contract C1 — 직접 호출 경로도 외부 reviewer gate 통과).
- `feature-draft`/`implementation-plan` 스킬(claude+codex) wrapper→orchestrator 승격, loop 소유 (Part 1 Contract C2/C3).
- `feature-draft-agent`/`implementation-plan-agent`(claude .md + codex .toml)에 fix mode 입력 계약 추가 (Part 1 Contract C4).
- 세 loop 공통 정책 통일 (Part 1 Contract C5).
- ②③ 스킬 Role/Source Pointer 재정의 (Part 1 Contract C6).

### Out of Scope
- autopilot SKILL 및 `_sdd/spec/*` 파일 수정 (Part 1 Scope Delta — spec 불가침, autopilot 실행 경로 비중첩).
- `implementation-agent`/`plan-review-agent`/`implementation-review-agent` 본문 review/TDD 계약 변경 (재사용만, Part 1 Invariant I3).

## Components

| Component | 역할 | 변경 |
|-----------|------|------|
| `implementation` skill (claude/codex) | TDD 구현 orchestrator | Step 6 외부 review-fix loop로 교체 |
| `feature-draft` skill (claude/codex) | draft 생성 entrypoint | wrapper→orchestrator 승격 + loop |
| `implementation-plan` skill (claude/codex) | plan 생성 entrypoint | wrapper→orchestrator 승격 + loop |
| `feature-draft-agent` (claude/codex) | draft producer | fix mode 입력 계약 추가 |
| `implementation-plan-agent` (claude/codex) | plan producer | fix mode 입력 계약 추가 |
| `implementation-review-agent` | 구현 reviewer | 참조만 (①의 reviewer) |
| `plan-review-agent` | plan/draft reviewer | 참조만 (②③의 reviewer) |
| `implementation-agent` | TDD fix leaf | 참조만 (①의 fix dispatch 대상, I3) |

## Contract/Invariant Delta Coverage

| Target | Planned Tasks | Validation Link |
|--------|---------------|-----------------|
| C1 (implementation Step 6 외부 loop) | T2 | V1 |
| C2 (feature-draft 승격) | T4 | V2 |
| C3 (implementation-plan 승격) | T5 | V2 |
| C4 (producer fix mode) | T3 | V3 |
| C5 (공통 loop 정책) | T1 | V4 |
| C6 (②③ Role Pointer 재정의) | T4, T5 | V5 |
| I1 (산출물 단일 작성자) | T3, T4, T5 | V3 |
| I2 (loop 종료 불변식) | T2, T4, T5 | V1, V2 |
| I3 (implementation-agent fix mode 불필요) | T2 | V7 |
| 전체 (reload smoke) | T6 | V6 |

## Implementation Phases

전략: **Dependency-Driven**. 근거 — fix mode 계약(C4, T3)이 ②③ 승격(C2/C3, T4/T5)의 전제이고, 공통 loop 정책(C5, T1)이 세 loop 모두의 선행 정의다. 의존성 체인 깊이가 명확해 dependency 순으로 phase를 닫는다.

### Phase 0: 공통 loop 정책 정의
**Goal**: 세 스킬이 동일하게 참조할 review-fix loop 정책(exit/MAX/re-review scope/iteration 경계/MAX 분기)을 단일 정의로 확정.
**Tasks**: T1
**Task Set / Dependency Closure**: 외부 의존 없음. T2/T4/T5가 이 정책 문구를 인용하므로 선행.
**Validation Focus**: V4
**Exit Criteria**:
- [ ] exit(`critical=high=medium=0`)·MAX(3)·re-review scope(전체)·MAX 분기·iteration 경계가 한 정의로 확정됨 (Part 1 C5).
**Carry-over Policy**: Default `None` (critical/high/medium block).
**Checkpoint**: false

### Phase 1: implementation Step 6 외부 loop 교체
**Goal**: `implementation` 스킬(claude+codex)의 인라인 Phase Review를 외부 `implementation-review-agent` review→fix→re-review loop로 교체.
**Tasks**: T2
**Task Set / Dependency Closure**: T1(공통 정책)에 의존. producer fix mode(T3, Phase 2)와는 의미적으로 독립(① loop는 leaf 재dispatch, I3)이나, orchestrator 병렬 규칙은 "같은 phase + dependency 없음 + Target Files disjoint"라 phase 경계를 넘는 병렬은 표현 불가 — Phase 1→Phase 2 순차로 진행한다(문서 리팩터라 병렬 이득 작음).
**Validation Focus**: V1, V7
**Exit Criteria**:
- [ ] claude+codex `implementation` SKILL Step 6에 외부 reviewer 호출·fix 재dispatch·re-review·exit 조건이 명시되고 인라인 self-review 문구 제거됨 (Part 1 C1, I2).
**Carry-over Policy**: Default `None`.
**Checkpoint**: false

### Phase 2: producer-agent fix mode 추가
**Goal**: `feature-draft-agent`/`implementation-plan-agent`(claude+codex)에 fix mode 입력 계약과 mode 분기를 추가.
**Tasks**: T3
**Task Set / Dependency Closure**: T1에 의존. T4/T5(승격)가 이 fix 계약을 호출하므로 선행 필수. Phase 1(T2)과는 phase 순차(병렬 주장 없음 — orchestrator 병렬은 same-phase에서만 표현 가능).
**Validation Focus**: V3
**Exit Criteria**:
- [ ] 두 producer-agent(claude .md + codex .toml)에 fix mode 입력 계약(리포트 경로+산출물 경로+findings)·mode 분기·단일 작성자 보존이 명시됨 (Part 1 C4, I1).
**Carry-over Policy**: Default `None`.
**Checkpoint**: true
**Checkpoint Reason**: 후속 Phase 3의 ②③ 승격이 이 fix mode 계약을 직접 호출하므로, 진행 전 review-fix gate로 계약 정합을 확정한다.

### Phase 3: feature-draft/implementation-plan 승격
**Goal**: 두 스킬(claude+codex)을 wrapper→orchestrator로 재작성, loop 소유 + Role Pointer 재정의.
**Tasks**: T4, T5
**Task Set / Dependency Closure**: T1(정책)·T3(fix mode)에 의존. T4/T5는 서로 다른 파일을 수정하고 dependency edge 없음 → 병렬 가능.
**Validation Focus**: V2, V5
**Exit Criteria**:
- [ ] 두 스킬(claude+codex)이 producer dispatch→`plan-review-agent` loop→relay 구조로 재작성되고 Role Pointer가 재정의됨 (Part 1 C2/C3/C6, I2).
**Carry-over Policy**: Default `None`.
**Checkpoint**: false

### Phase 4: 정적 게이트 + smoke 검증
**Goal**: 계약 일관성·platform parity를 grep/diff로 확인하고 reload 후 trigger resolve smoke.
**Tasks**: T6
**Task Set / Dependency Closure**: T2/T4/T5 산출에 의존.
**Validation Focus**: V6, V4
**Exit Criteria**:
- [ ] 세 loop 정책 일관성·claude↔codex parity가 grep/diff로 확인되고, reload 후 세 trigger가 resolve됨 (Part 1 모든 C/I).
**Carry-over Policy**: Default `None`.
**Checkpoint**: true (마지막 phase, implicit true)
**Checkpoint Reason**: 최종 통합 검증 — 세 loop·양 플랫폼의 정합을 닫는 마지막 gate.

## Task Details

### Task T1: 공통 review-fix loop 정책을 단일 정의로 확정
**Component**: 세 스킬 공통
**Priority**: P0
**Type**: Infrastructure

**Description**: 세 스킬에 내장될 review-fix loop의 공통 정책을 한 정의로 확정한다. 이 정의는 autopilot의 `.claude/skills/sdd-autopilot/references/orchestrator-contract.md` §6 Review-Fix Contract(exit `critical = 0 AND high = 0 AND medium = 0`, MAX 도달 분기, fix=finding 순차 dispatch)를 직접 호출 경로용으로 차용·재진술한 것이다. 확정 항목: (a) exit = `critical=high=medium=0`, (b) MAX = 기본 3회, (c) re-review scope = loop 범위 전체 재리뷰(변경분만 아님), (d) 1 iteration 경계 = `review/re-review → finding>0이면 fix → 산출물 갱신`, (e) MAX 도달 분기 = critical/high 잔존이면 중단·사용자 보고, medium만 잔존이면 로그 후 진행(medium은 fix 시도하되 MAX에서 막히면 advisory degrade). 이 task는 별도 파일을 만들지 않고, 확정된 정책 문구를 T2/T4/T5가 각 SKILL 본문에 인용해 인라인 기술할 수 있도록 정리한다(단일 사용처 추상화 파일 도입 금지 — Part 1 Hard Rule, 세 스킬이 각자 인라인 보유).

**Acceptance Criteria**:
- [ ] exit/MAX/re-review scope/iteration 경계/MAX 분기 5개 항목이 명시적 문구로 확정된다.
- [ ] 각 항목이 autopilot orchestrator-contract §6의 어느 규칙에서 차용됐는지 출처가 기록된다.
- [ ] 별도 shared 정책 파일을 생성하지 않고 각 SKILL이 인라인 보유하는 방침이 명시된다.

**Target Files**:
- [M] `_sdd/drafts/2026-06-03_feature_draft_skills_embed_review_fix_loop.md` -- 본 draft Part 2 내 정책 확정 기록 (별도 산출 파일 없음; T2/T4/T5가 본 정의를 인용)

**Technical Notes**: Covers C5, validated by V4. 정책 단일 정의지만 물리적 공유 파일은 만들지 않는다 — 세 스킬이 직접 호출 경로에서 각자 인라인 기술(YAGNI, 단일 사용처 추상화 회피). 출처: orchestrator-contract.md §6.
**Dependencies**: 없음

### Task T2: implementation 스킬 Step 6를 외부 review-fix loop로 교체 (claude+codex)
**Component**: `implementation` skill
**Priority**: P0
**Type**: Refactor

**Description**: `implementation` 스킬의 Step 6 Phase Review를 현재의 *인라인 경량 self-review*(orchestrator가 직접 품질 체크 후 Critical만 leaf 재dispatch, Quality는 문서화)에서 **외부 `implementation-review-agent` review→fix→re-review loop**로 교체한다. 각 phase의 모든 task 완료 후 orchestrator는: (1) `implementation-review-agent`를 호출해 그 phase 범위 변경 파일 전체 + 테스트 결과를 review 입력으로 전달, (2) reviewer가 반환한 finding을 severity별로 받아 critical/high/medium finding이 있으면 `implementation-agent` leaf를 **finding 하나씩 순차** fix-task로 재dispatch(finding 영향 파일 = 그 leaf의 Target Files), (3) fix 후 loop 범위 전체를 re-review, (4) exit(`critical=high=medium=0`) 또는 MAX(3) 도달까지 반복. MAX 도달 시 T1 분기 정책 적용. loop scope는 **실행분(phase) 단위 1 gate**로 단순화한다 — autopilot의 global/per-group·Checkpoint 메타 개념을 도입하지 않는다(Part 1 Risk Q2: 직접 호출 경로엔 Checkpoint 신호를 줄 상위 오케스트레이터가 없음). dispatch 표기는 claude `Agent(subagent_type="sdd-skills:implementation-review-agent")` / `sdd-skills:implementation-agent`, codex `spawn_agent(agent_type="implementation_review_agent"/"implementation_agent")`+`wait_agent`. Model Routing: review/re-review=opus, fix=sonnet(autopilot Review-Fix Gate Model Assignment 동형).

**Non-Goals**: `implementation-agent` 본문 수정(I3 — leaf는 finding을 task로 받아 기존 TDD 계약으로 처리, fix mode 불필요). Step 7 Final Review의 cross-phase 종합 리뷰 구조 변경(현 계약 유지). autopilot per-group scope 도입.

**Acceptance Criteria**:
- [ ] claude+codex `implementation` SKILL Step 6에서 인라인 self-review 품질 체크표·Decision Gate가 외부 `implementation-review-agent` 호출로 교체된다.
- [ ] review→fix(`implementation-agent` finding 순차 재dispatch)→re-review→exit(`critical=high=medium=0`)/MAX(3) loop가 명시된다.
- [ ] loop scope가 phase 단위 1 gate임이 명시되고, autopilot global/per-group 개념을 도입하지 않음이 드러난다. multi-phase plan에서 각 phase 완료 직후 gate가 정확히 1회씩 닫히고 다음 phase로 진행함이 기술된다(Part 1 Risk Q2 검증 환류 — single-phase만으로 AC가 만족되지 않도록).
- [ ] Model Routing(review/re-review=opus, fix=sonnet)과 양 플랫폼 dispatch 표기가 명시된다.
- [ ] `implementation-agent`가 fix mode 별도 계약 없이 fix-task를 처리함이 근거와 함께 기술된다 (I3).

**Target Files**:
- [M] `.claude/skills/implementation/SKILL.md` -- Step 6 교체, Step 4 loop 진입점 연결
- [M] `.codex/skills/implementation/SKILL.md` -- 동일 (spawn_agent/wait_agent 표기)

**Technical Notes**: Covers C1, I2, I3; validated by V1, V7. 참조: orchestrator-contract.md §6 Review-Fix Contract + Review-Fix Gate Model Assignment. T1 공통 정책 인용.
**Dependencies**: T1

### Task T3: producer-agent에 fix mode 입력 계약 추가 (claude+codex)
**Component**: `feature-draft-agent`, `implementation-plan-agent`
**Priority**: P0
**Type**: Feature

**Description**: 두 producer-agent에 **fix mode** 입력 계약을 추가한다. dispatch 프롬프트에 (a) review 리포트 경로(`plan-review-agent`가 생성한 `_sdd/implementation/<date>_plan_review_<slug>.md`), (b) 기존 산출물 경로(feature-draft는 `_sdd/drafts/<date>_feature_draft_<slug>.md`, implementation-plan은 `_sdd/implementation/<date>_implementation_plan_<slug>.md`), (c) 대상 findings가 포함되면 **fix mode**로, 없으면 기존 **생성 mode**로 분기한다(Part 1 Risk Q4: 입력 존재 신호로 분기, 별도 플래그 토큰 불필요). 분기 경계는 결정적이다 — 세 입력(review 리포트 경로 + 기존 산출물 경로 + 대상 findings)이 **모두** 있어야 fix mode이고, 하나라도 없으면 생성 mode로 처리한다(부분 입력·재개 케이스도 생성 mode로 귀결). fix mode에서 agent는 기존 산출물을 Read하고 findings에 해당하는 부분만 surgical 수정하며 문서 전체를 재생성하지 않는다(Part 1 Invariant I1 단일 작성자 — producer-agent만 자기 산출물 write). 각 agent의 Process 말미 또는 별도 "Fix Mode" 섹션에 이 계약을 기술하고, Source Pointer에 loop 소유 주체가 스킬임을 한 줄 보강한다.

**Non-Goals**: review 수행(reviewer agent 책임). 생성 mode의 기존 Process 단계 변경. loop orchestration(스킬 책임 — agent는 sub-agent spawn 불가).

**Acceptance Criteria**:
- [ ] `feature-draft-agent`(claude .md + codex .toml)에 fix mode 입력 계약(리포트 경로+산출물 경로+findings)과 생성/fix mode 분기 신호가 명시된다.
- [ ] `implementation-plan-agent`(claude .md + codex .toml)에 동일 fix mode 계약이 명시된다.
- [ ] fix mode가 기존 산출물을 Read해 finding 부분만 surgical 수정하고 전체 재생성하지 않음(단일 작성자 보존)이 기술된다 (I1).
- [ ] fix mode가 codex `feature-draft-agent`의 `<!-- spec-update-todo-input-start -->` / `<!-- spec-update-todo-input-end -->` 마커를 보존한다(Part 1 영역 surgical 수정이 마커를 유실하지 않음 — downstream `spec-update-todo` 입력 파싱 보호). (claude/codex 마커 비대칭 자체의 정합화는 본 plan 범위 밖 — finding으로만 노출.)
- [ ] mode 분기 신호가 "입력 존재 여부"임이 명시된다 (별도 플래그 토큰 미도입).

**Target Files**:
- [M] `.claude/agents/feature-draft-agent.md` -- fix mode 섹션 추가, Source Pointer 보강
- [M] `.codex/agents/feature-draft-agent.toml` -- 동일 (developer_instructions)
- [M] `.claude/agents/implementation-plan-agent.md` -- fix mode 섹션 추가
- [M] `.codex/agents/implementation-plan-agent.toml` -- 동일

**Technical Notes**: Covers C4, I1; validated by V3. fix=producer 재dispatch(Part 1 결정 3). 입력 포맷은 reviewer 리포트 경로 계약(`plan-review-agent`의 `_sdd/implementation/<date>_plan_review_<slug>.md`)과 정합.
**Dependencies**: T1

### Task T4: feature-draft 스킬 wrapper→orchestrator 승격 + loop 소유 (claude+codex)
**Component**: `feature-draft` skill
**Priority**: P0
**Type**: Refactor

**Description**: `feature-draft` 스킬을 entrypoint wrapper(현재: digest 수집→producer dispatch→relay 3-step)에서 **loop-owning orchestrator**로 재작성한다. 새 흐름: (1) Mode B 맥락 digest 수집(기존 유지 — 입력이 대화에서 태어나므로 orchestrator가 대화 맥락을 정리해 전달, Part 1 결정 7), (2) `feature-draft-agent`를 생성 mode로 dispatch해 draft 산출, (3) `plan-review-agent`를 호출해 draft Part 2를 review(`plan-review-agent`는 feature draft Part 2를 입력으로 수용 — Tier 2), (4) critical/high/medium finding이 있으면 `feature-draft-agent`를 **fix mode**(T3 계약: review 리포트 경로 + draft 경로 + findings)로 재dispatch, (5) loop 범위 전체 re-review, (6) exit(`critical=high=medium=0`)/MAX(3)까지 반복(T1 정책), (7) 최종 draft 경로 + Step 8 surface 결정을 사용자에게 relay. MAX 도달 분기는 T1 정책 적용(critical/high 잔존→중단·보고). fix 라운드에서도 digest를 producer에 함께 전달한다(Part 1 결정 7 — fix 라운드도 맥락 큐레이션 유지). Role Pointer를 재정의한다: "agent는 draft producer 단일 소스, 스킬은 review-fix loop를 소유하는 orchestrator"(Part 1 C6, Risk Q5). dispatch 표기는 claude `sdd-skills:` prefix / codex `*_agent`+`wait_agent`. Model Routing: producer/fix=`feature-draft-agent`(opus), review/re-review=`plan-review-agent`(opus).

**Non-Goals**: draft 본문 작성(producer-agent 책임 — 중복 금지). `plan-review-agent`/`feature-draft-agent` 본문 변경(T3에서 producer fix mode만 추가). Mode B digest 수집 로직 제거(유지 필수 — 승격의 핵심 제약).

**Acceptance Criteria**:
- [ ] claude+codex `feature-draft` SKILL이 producer dispatch→`plan-review-agent` review→fix→re-review→relay orchestrator 구조로 재작성된다.
- [ ] Mode B 맥락 digest 수집이 생성·fix 라운드 모두에서 producer에 전달됨이 명시된다 (결정 7).
- [ ] exit(`critical=high=medium=0`)/MAX(3)/MAX 분기가 T1 정책으로 명시된다.
- [ ] Role Pointer가 "agent=producer 단일 소스 + skill=loop orchestrator"로 재정의되고 wrapper-only 문구가 제거된다 (C6).
- [ ] 양 플랫폼 dispatch 표기와 Model Routing(producer/fix·review/re-review)이 명시된다.

**Target Files**:
- [M] `.claude/skills/feature-draft/SKILL.md` -- orchestrator 재작성, Role Pointer
- [M] `.codex/skills/feature-draft/SKILL.md` -- 동일 (spawn_agent/wait_agent)

**Technical Notes**: Covers C2, C6, I2; validated by V2, V5. `plan-review-agent`는 feature draft Part 2 수용(Tier 2). fix dispatch는 T3 fix mode 계약 호출. T1 공통 정책 인용.
**Dependencies**: T1, T3

### Task T5: implementation-plan 스킬 wrapper→orchestrator 승격 + loop 소유 (claude+codex)
**Component**: `implementation-plan` skill
**Priority**: P0
**Type**: Refactor

**Description**: `implementation-plan` 스킬을 entrypoint wrapper(현재 Mode A pass-through: 입력 수집→producer dispatch→relay)에서 **loop-owning orchestrator**로 재작성한다. 새 흐름: (1) 사용자 요청 + 계획 입력 경로 수집(기존 유지), (2) `implementation-plan-agent`를 생성 mode로 dispatch해 plan 산출, (3) `plan-review-agent`로 plan을 review(Tier 1), (4) critical/high/medium finding이 있으면 `implementation-plan-agent`를 fix mode(T3 계약: review 리포트 경로 + plan 경로 + findings)로 재dispatch, (5) loop 범위 전체 re-review, (6) exit/MAX(3)까지 반복(T1 정책), (7) 최종 plan 경로 + Open Questions(LOW/Yes)를 relay. MAX 분기는 T1 정책. Role Pointer 재정의: "agent는 plan producer 단일 소스, 스킬은 review-fix loop orchestrator"(C6, Risk Q5). dispatch 표기 claude `sdd-skills:` / codex `*_agent`. Model Routing: producer/fix=`implementation-plan-agent`(opus), review/re-review=`plan-review-agent`(opus). Mode A는 대화 digest forwarding이 없으므로(feature-draft의 Mode B와 달리 입력이 파일/경로에서 태어남) digest 수집 단계는 두지 않는다.

**Non-Goals**: plan 본문 task 분해(producer-agent 책임). Mode B digest 수집 도입(implementation-plan은 Mode A — 입력이 파일에서 태어나 불필요). reviewer/producer 본문 변경(T3에서 producer fix mode만).

**Acceptance Criteria**:
- [ ] claude+codex `implementation-plan` SKILL이 producer dispatch→`plan-review-agent` review→fix→re-review→relay orchestrator 구조로 재작성된다.
- [ ] exit(`critical=high=medium=0`)/MAX(3)/MAX 분기가 T1 정책으로 명시된다.
- [ ] Role Pointer가 "agent=producer 단일 소스 + skill=loop orchestrator"로 재정의되고 wrapper-only 문구가 제거된다 (C6).
- [ ] Mode A(파일 입력)이므로 digest forwarding을 두지 않음이 드러난다(feature-draft Mode B와 구분).
- [ ] 양 플랫폼 dispatch 표기와 Model Routing이 명시된다.

**Target Files**:
- [M] `.claude/skills/implementation-plan/SKILL.md` -- orchestrator 재작성, Role Pointer
- [M] `.codex/skills/implementation-plan/SKILL.md` -- 동일

**Technical Notes**: Covers C3, C6, I2; validated by V2, V5. `plan-review-agent` Tier 1 입력. fix dispatch는 T3 fix mode 계약 호출. T1 공통 정책 인용.
**Dependencies**: T1, T3

### Task T6: 정적 게이트 + reload smoke 검증
**Component**: 전체
**Priority**: P1
**Type**: Test

**Description**: 변경된 계약의 일관성과 claude↔codex parity를 정적으로 검증하고, 플러그인 reload 후 trigger resolve를 smoke한다. 정적 게이트: (a) grep으로 세 스킬에 exit `critical=high=medium=0`·MAX 3·re-review 전체 scope 문구가 일관되게 존재하는지, (b) ②③ SKILL에서 wrapper-only 문구("위임하고 relay"만)와 "Source: agent가 단일 소스" 잔존이 없는지, (c) claude `sdd-skills:` prefix / codex `*_agent`+`wait_agent` dispatch 표기가 양 플랫폼에 대응되는지 diff. reload smoke: 플러그인 reload 후 `/implementation`·`/feature-draft`·`/implementation-plan` trigger가 resolve되고 dispatch 대상 agent(`*-agent` / `*_agent`)가 유효한지 확인. `_sdd/env.md`상 테스트 프레임워크가 없으므로 코드 분석 기반 검증을 허용하되 결과에 근거(grep/diff 출력)를 제시한다.

**Acceptance Criteria**:
- [ ] 세 스킬 loop 정책 문구 일관성이 grep으로 확인된다 — 핵심 토큰 `critical=high=medium=0`, `MAX 3`(또는 동등 표기), `전체 재리뷰`가 6개 파일(세 SKILL × claude/codex 2 플랫폼) **모두**에 존재하는지 grep으로 대조한다.
- [ ] multi-phase plan 입력 시 각 phase 직후 review-fix gate가 1회씩 닫힘이 smoke로 확인된다(Part 1 Risk Q2 phase 단위 1 gate가 single-phase뿐 아니라 multi-phase에서도 정확히 동작).
- [ ] ②③에 wrapper-only/Source Pointer 잔존 문구가 없음이 확인된다.
- [ ] claude↔codex parity가 diff로 확인된다(dispatch 표기·계약 구조).
- [ ] reload 후 세 trigger가 resolve되고 dispatch 대상 agent가 유효함이 smoke된다.

**Target Files**:
- [M] 후속 implementation report (`_sdd/implementation/<date>_implementation_report_skills_embed_review_fix_loop.md`) -- grep/diff 검증 근거와 reload smoke 결과를 이 report에 첨부 (코드 산출 없음 — 테스트 프레임워크 부재로 정적 게이트 산출물만, V6 evidence 추적 위치 확정)

**Technical Notes**: Covers 전체 C/I; validated by V6, V4. `_sdd/env.md` 테스트 프레임워크 부재 → 정적 게이트(grep/diff) + reload smoke.
**Dependencies**: T2, T4, T5

## Parallel Execution Summary

- **T1** (Phase 0): 단독 선행. 모든 후속 task가 의존.
- **T2** (Phase 1)와 **T3** (Phase 2): 의미적으로는 독립(① loop는 leaf 재dispatch, ②③ producer fix mode — I3로 분리, Target Files도 `implementation` SKILL vs producer-agent로 disjoint)이지만 서로 다른 phase에 있다. orchestrator 병렬 규칙은 "같은 phase + dependency 없음 + Target Files disjoint"라 phase 경계를 넘는 병렬은 표현 불가 → **phase 순차**(Phase 1→Phase 2)로 진행한다(문서 리팩터라 병렬 이득 작음). Phase 2는 Checkpoint=true이므로 T3 완료 후 gate를 닫고 Phase 3로 진행.
- **T4, T5** (Phase 3): 서로 다른 SKILL 파일 수정, dependency edge 없음, Target Files disjoint → **병렬 가능**. 둘 다 T1+T3에 의존(fix mode 계약 호출).
- **T6** (Phase 4): T2/T4/T5 산출에 의존 → 최후 순차.
- 의미적 충돌 점검: T2와 T3/T4/T5는 모두 "공통 loop 정책(T1)"을 인용하는 생산-소비 관계지만, T1이 먼저 정책을 확정(dependency edge)하므로 충돌 인코딩 완료. claude/codex 파일은 같은 task 내에서 함께 수정(같은 계약의 양 플랫폼 mirror)하여 parity 일관성을 task 경계 안에서 보장.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| 승격된 ②③ loop가 producer fix mode 계약(T3)과 미정합 | fix dispatch 실패 | T3를 Phase 2 Checkpoint=true gate로 닫고 Phase 3 진행 전 계약 정합 확정 |
| medium까지 fix 시도 시 수렴 실패(무한 fix) | 시간 낭비·산출 불안정 | MAX(3) 도달 시 medium만 잔존이면 advisory degrade·로그 후 진행(T1 정책) |
| claude↔codex parity 누락 | 한 플랫폼만 동작 | 각 task가 양 플랫폼 파일을 Target Files에 함께 포함, T6 diff 게이트 |
| `plan-review-agent`가 feature draft Part 2(Tier 2)와 plan(Tier 1)을 다르게 처리 | review 깊이 차이 | reviewer는 이미 두 입력을 Tier로 graceful 수용(현 계약) — 재사용만, 본문 무변경 |

## Open Questions

> Part 1 `Risks / Open Questions`(Q1–Q6)에서 모든 결정이 best-effort로 확정됐고, Confidence=LOW 또는 User confirmation needed=Yes 항목은 없다. Part 2 고유의 추가 미결은 없다. Q2(loop scope 단순화)·Q4(fix mode 분기 신호)는 Confidence=MEDIUM이나 User confirmation needed=No로 진행한다.

---

## Self-Containment Check (Hard Rule 11 검증)

- **검토 섹션 수**: 8 (Overview, Scope, Components, C/I Delta Coverage, Implementation Phases, Task Details(T1–T6), Parallel Execution Summary, Risks/Open Questions).
- **Pass 1 (Reference Enumeration) 발견 갭 및 보완**:
  - 외부 참조 `orchestrator-contract.md §6`이 T1/T2에서 bare로 등장 → "Review-Fix Contract(exit 조건·MAX 분기·fix 순차)" inline purpose를 동반하도록 T1 Description·Technical Notes에 재진술 보완 완료.
  - `plan-review-agent` 리포트 경로 참조 → T3에서 `_sdd/implementation/<date>_plan_review_<slug>.md` 전체 경로 + "fix mode 입력으로 사용" inline purpose 명시 보완 완료.
  - Part 1 Contract/Invariant ID(C1–C6, I1–I3) 참조 → 각 task Technical Notes에 `ID + inline purpose`(예: "Covers C4, I1 — fix mode 단일 작성자") 형식으로 동반(Hard Rule 11 Part 1↔Part 2 carve-out 충족).
- **Pass 2 (Fresh-Reader Readthrough) 발견 갭 및 보완**:
  - "Mode B / Mode A" 용어가 생초 독자에게 불명 → T4(Mode B = 대화에서 입력이 태어남, digest forwarding)·T5(Mode A = 파일/경로에서 입력)에서 1줄 정의 보완 완료.
  - "leaf / orchestrator / producer-agent / fix mode" 핵심 용어 → Overview 용어 정의 블록에 1줄씩 추가 보완 완료.
  - "왜 implementation-agent는 fix mode가 없고 producer-agent는 있나"라는 비대칭 의문 → Part 1 Risk Q3 + T2 Non-Goals(I3 근거: leaf는 finding을 task로 매핑, producer는 문서 단일 작성자라 mode 분기 필요)로 답 보완 완료.
- **보완 완료**: Yes
- **Plan-review fix loop 반영(2026-06-03)**: H1(T3 AC·V3에 codex `spec-update-todo-input` 마커 보존 항목 추가)·H2(승격 동형 선례 investigate→`implementation`으로 정정, Change Summary·Q5)·M1(T2/T3 cross-phase 병렬 주장 삭제, phase 순차로 단순화)·M2(T6 grep 비교 기준 핵심 토큰 6파일 명시)·M3(T2 AC·T6 smoke에 multi-phase phase별 gate 1회 종료 확인 추가)·L1(T6 Target Files를 후속 implementation report로 확정)·L2(T3 Description에 fix mode 분기 경계 1줄 명확화) findings를 surgical 반영. 마커 보존·multi-phase gate 검증이 V3·V6/T6에 환류되어 H1·M3 verification linkage 갭이 닫힘.

## Minimum-Code Mandate Self-Check (Hard Rule 12)

- T1은 "단일 정책 정의"를 별도 공유 파일로 만들지 않고 세 스킬 인라인 기술로 두어 단일 사용처 추상화 파일을 회피했다.
- 어느 task도 요청되지 않은 옵션·설정 가능성·추상화를 도입하지 않는다. "configurable/extensible/future-proof" 형용사 미사용.
- T3 fix mode는 별도 플래그 토큰을 도입하지 않고 입력 존재 신호로 분기(과잉 메커니즘 회피, Risk Q4).
- ① implementation은 `implementation-agent`에 fix mode 계약을 추가하지 않는다(I3 — 발생하지 않는 비대칭 처리 회피).
- 세 loop는 autopilot global/per-group scope 개념을 차용하지 않고 phase 단위 1 gate로 단순화(Risk Q2 — 사변적 복잡도 회피).
