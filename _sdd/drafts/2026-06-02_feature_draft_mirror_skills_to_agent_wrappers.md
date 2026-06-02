# Feature Draft: mirror 스킬을 agent thin wrapper로 전환

> 근거 토론: `_sdd/discussion/2026-06-02_discussion_mirror_skills_to_agent_wrappers.md` (10종×2 wrap, wrapper=A2 pass-through+맥락 forwarding, Mirror Notice→포인터, codex spawn_agent까지 합의)

# Part 1: Temporary Spec Draft

## Change Summary

agent와 본문이 거의 동일하게 중복된 **mirror 스킬 10종**(× claude/codex = 20개 SKILL.md)을, 호출 시 대응 agent를 dispatch하는 **thin wrapper**로 전환한다. 목적: **코드 중복 제거(DRY, ~5,400줄)** + **직접 호출 시 메인 컨텍스트 절약**(무거운 본문·프로세스를 agent 자체 context로 이동).

대상 10종: feature-draft, implementation, implementation-plan, implementation-review, investigate, plan-review, ralph-loop-init, spec-review, spec-update-done, spec-update-todo.

wrapper 방식은 **A2 (pass-through + 대화 맥락 forwarding)**: 사용자 원본 요청 + 이 대화에서 이미 아는 맥락(참조 경로·이전 산출물·결정)을 verbatim 전달하되, **새 파일 read·input 탐색은 하지 않는다**(agent의 Step 1이 담당). agent가 단일 canonical source가 된다.

## Scope Delta

**In-scope:**
- `.claude/skills/<slug>/SKILL.md` 10개: 본문(frontmatter 제외)을 thin wrapper로 교체.
- `.codex/skills/<slug>/SKILL.md` 10개: 동일, codex dispatch 메커니즘.
- 각 SKILL.md의 Mirror Notice → "이 스킬은 X-agent의 wrapper" 1줄 포인터로 교체.
- frontmatter(name/description/version) **그대로 유지** — auto-trigger 매칭 보존. version은 변경하지 않는다(저장소에 버저닝 정책이 없어 wrapper 전환만으로의 bump은 불필요 — YAGNI).

**Out-of-scope (의도적 보존):**
- **agent 파일(20개)** — 이미 canonical, 변경 없음.
- **autopilot**(SKILL.md / orchestrator-contract / examples / references) — orchestrator는 agent를 *직접* 호출하므로 스킬 wrapping 무영향.
- **standalone 스킬**(discussion, spec-create, spec-rewrite, spec-summary, spec-snapshot, spec-upgrade, guide-create, pr-review, write-phased, second-opinion, git, sdd-autopilot) — 대응 agent 없음 → wrap 대상 아님.
- sibling 스킬 참조(예: agent 본문의 `write-phased` 언급) — wrapper가 여전히 트리거되므로 무영향.

**Guardrail delta:**
- wrapper는 **process 로직을 1줄도 포함하지 않는다**(중복 0). input 탐색·검증·산출은 전적으로 agent.
- claude dispatch는 **`sdd-skills:<slug>-agent`** prefix 사용(로컬 dev + 플러그인 배포 양쪽에서 resolve — autopilot Hard Rule 14와 동일 근거). bare 이름 금지.

## Contract/Invariant Delta

| ID | Type | Change | Why |
|----|------|--------|-----|
| C1 | Modify | mirror 스킬 SKILL.md 본문 = thin wrapper (기존: agent 본문의 full 복제) | DRY, 컨텍스트 절약 |
| C2 | Add | claude wrapper는 `Agent(subagent_type="sdd-skills:<slug>-agent")`로, codex wrapper는 `spawn_agent(agent_type="<snake>_agent")` + `wait_agent`로 dispatch | 실행을 agent에 위임 |
| C3 | Add | wrapper는 A2 context(사용자 원본 요청 + 대화 맥락: 참조 경로·이전 산출물·결정)를 verbatim 전달하고, **agent가 사용자에게 노출한 확인 필요·저확신 항목을 요약 누락 없이 relay**한다 | sub-agent 대화 맥락 소실 방지 + 확인 필요 결정 유실 방지 |
| I1 | Add | wrapper는 process/계약 로직을 중복하지 않는다; agent가 단일 canonical | DRY 불변식 |
| I2 | Add | wrapper는 새 파일 read·input 탐색을 하지 않는다(agent 담당) | 컨텍스트 절약이 B로 상쇄되는 것 방지 |
| I3 | Add | frontmatter(name/description/version) **무변경** 보존, Mirror Notice→1줄 포인터 | auto-trigger 유지 + sync 의무 소멸 |
| I4 | Add | agent 파일과 autopilot은 변경되지 않는다 | 변경 surface를 스킬로 한정 |

## Touchpoints

> 모두 현재 코드 census(2026-06-02)로 확인. 20개 SKILL.md는 **각각 독립**(공유 파일 없음) → batch 내 높은 병렬성.

- `.claude/skills/<slug>/SKILL.md` ×10 — 본문 교체 + Mirror Notice 포인터화. Mirror Notice 위치(claude): feature-draft L269, implementation L305, implementation-plan L328(Sync Notice), implementation-review L239, investigate L85, plan-review L248, ralph-loop-init L601, spec-review L248, spec-update-done L196, spec-update-todo L198.
- `.codex/skills/<slug>/SKILL.md` ×10 — 동일, codex dispatch. Mirror Notice 위치(codex): feature-draft L320, implementation L295, implementation-plan L346, implementation-review L235, investigate L85, plan-review L248, ralph-loop-init L571, spec-review L248, spec-update-done L196, spec-update-todo L198.
- **변경 금지 확인(negative)**: `.claude/agents/*-agent.md`, `.codex/agents/*-agent.toml`, `.claude/skills/sdd-autopilot/**`, `.codex/skills/sdd-autopilot/**`, standalone 스킬 12종.

## Implementation Plan

1. **Pilot**: `implementation` 1종을 claude+codex 양쪽 wrapper로 교체(템플릿 2종 동시 확정) → `/reload-skills` 후 직접 호출이 agent를 dispatch하고, **agent가 다시 sub-agent를 spawn(nesting)** 하며 결과가 relay되는지 검증. implementation을 pilot으로 택한 이유: TDD sub-agent를 **항상 spawn**하므로 유일 미지수인 nesting 경로를 결정적으로 닫는다.
2. **Batch**: 나머지 9종(spec-review 포함) × 2를 검증된 템플릿으로 교체.
3. **Verification**: 20개 thin 확인, dispatch 식별자·frontmatter·포인터 확인, agent/autopilot 무변경 확인.

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, I1, I2 | test (grep/wc) | 20개 SKILL.md 본문이 thin(예: ≤ ~25줄 본문), agent의 process 섹션(Hard Rules/Process/Step 등)이 스킬에 잔존하지 않음 |
| V2 | C2, C3 | test (grep) | claude는 `sdd-skills:<slug>-agent` + A2 맥락 전달 문구, codex는 `spawn_agent(agent_type="<snake>_agent")` + `wait_agent` 포함 |
| V3 | C2 | smoke (executable) | pilot: **편집 후 `/reload-skills`(또는 새 세션)로 wrapper 로드** → wrapped `implementation` 직접 호출 → 해당 agent dispatch + **agent가 sub-agent를 spawn(nesting)** + relay 확인 (claude·codex 각 1). 부작용 방지: dispatch 프롬프트를 "wiring smoke — sub-agent 1개만 spawn해 OK 받고 파일 변경 없이 종료"로 bound. reload 불가 시 명시 기록 + 사용자 보고 |
| V4 | I3 | review (grep) | frontmatter(name/description/version) **무변경** 보존, Mirror Notice가 1줄 포인터로 교체 |
| V5 | I4 | review (git diff) | `.claude/agents/*`, `.codex/agents/*`, autopilot(`*/sdd-autopilot/**`), standalone 스킬 12종에 **변경 0건** (변경은 mirror 스킬 20개 + `_sdd/` 산출물에 한정) |

## Risks / Open Questions

### Q1. (a) codex 스킬 직접 호출 시 `spawn_agent`가 실제 dispatch되는가, (b) wrapper가 더하는 nesting(메인→wrapper가 agent dispatch→agent가 sub-agent spawn)이 동작하는가
- **Decision taken**: 둘 다 가능하다고 가정하되, **pilot을 `implementation`으로** 잡아 V3에서 결정적으로 확정한다. implementation-agent는 TDD sub-agent를 *항상* spawn하므로 (b) nesting을 우연이 아니라 보장으로 검증한다(claude·codex 양쪽). 보조 근거: autopilot이 이미 `메인 스킬→implementation-agent→TDD`로 동작한다. 실패 시 wrapper 방식 재검토(롤백: 스킬 본문 git restore).
- **Alternatives considered**: pilot=spec-review → sub-agent spawn이 조건부라 nesting을 보장 검증 못 함. 기각. / 가정 없이 batch 선실행 → 틀리면 20개 롤백. pilot 게이트가 차단하므로 불필요.
- **Confidence**: MEDIUM (pilot V3에서 HIGH로 승격)
- **User confirmation needed**: No

### Q2. claude dispatch에 `sdd-skills:` prefix를 쓸지 bare를 쓸지
- **Decision taken**: `sdd-skills:<slug>-agent` prefix 사용. 플러그인으로 설치돼 사용자 프로젝트에서 실행될 때 bare 이름은 resolve 안 됨(로컬 agent 부재). autopilot Hard Rule 14와 동일 근거.
- **Alternatives considered**: bare `<slug>-agent` → 로컬 dev에서만 동작, 플러그인 배포 시 dangling. 기각.
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q3. "대화 맥락 forwarding"(A2)의 구체 범위
- **Decision taken**: wrapper 템플릿에 전달 대상을 명시 — (1) 사용자 원본 요청 전체, (2) 이 세션에서 이미 established된 참조 파일 경로·이전 산출물(_sdd/... 등) 위치·내려진 결정. 그 외 새 탐색 금지.
- **Alternatives considered**: "관련 맥락 전달"만 추상적으로 → 해석 편차. 명시 리스트로 고정.
- **Confidence**: MEDIUM
- **User confirmation needed**: No

### Q4. version 필드 bump — RESOLVED (drop)
- **Decision taken**: **bump하지 않는다.** version은 무변경 보존. 저장소에 버저닝 정책이 없고 DRY·컨텍스트 절약 목표와 무관해 bump은 불필요(YAGNI). 변경 추적은 git commit/diff로 충분.
- **Alternatives considered**: bump → 목표 무관한 추가 변경. 기각.
- **Confidence**: HIGH
- **User confirmation needed**: No

---

# Part 2: Implementation Plan

## Overview

mirror 스킬 20개(10종×claude/codex)를 thin agent wrapper로 교체한다. 20개 SKILL.md는 서로 독립 파일이라(공유 파일 없음) batch 내 병렬성이 높지만, **template 검증을 위해 pilot-then-batch**를 따른다. claude/codex는 dispatch 메커니즘이 달라 wrapper 템플릿이 2종이다. agent·autopilot·standalone 스킬은 건드리지 않는다(I4). 작업은 전용 브랜치에서 진행하고 검증 게이트 통과 후 커밋한다.

핵심: wrapper는 process 로직을 0줄 포함하고(I1), 새 파일을 읽지 않으며(I2), 대화 맥락만 forwarding(C3)한다. 이 셋이 "DRY + 컨텍스트 절약"이라는 목표를 동시에 만족시키는 칼선이다.

## Scope

In/Out-of-scope는 Part 1 `Scope Delta`와 동일. 요약: `.claude/skills`·`.codex/skills`의 mirror 10종만, agent·autopilot·standalone은 보존.

## Components

| Component | 역할 |
|-----------|------|
| claude wrapper 템플릿 | `.claude/skills/<slug>/SKILL.md` 본문 표준 형태 |
| codex wrapper 템플릿 | `.codex/skills/<slug>/SKILL.md` 본문 표준 형태 |
| Identifier Map | slug → claude `sdd-skills:<slug>-agent` / codex `<snake>_agent` |
| Verification Gate | V1~V5 |

### claude wrapper 템플릿 (확정)

```markdown
---
name: <slug>
description: <기존 트리거 description 그대로>
version: <기존 값 그대로 — 변경 안 함>
---

# <Title> (agent wrapper)

이 스킬은 `<slug>-agent`의 thin wrapper다. 계약·프로세스의 canonical source는 agent이며, 이 스킬은 실행을 agent에 위임한다.

호출되면:
1. `Agent(subagent_type="sdd-skills:<slug>-agent")`로 dispatch한다. 프롬프트에 다음을 verbatim 포함한다:
   - 사용자의 원본 요청 전체
   - 이 대화에서 이미 확보된 관련 맥락: 참조된 파일 경로, 이전 산출물 위치(`_sdd/...` 등), 내려진 결정
2. 새로 파일을 읽거나 input을 탐색하지 않는다 — input 발견과 전체 프로세스는 agent가 수행한다.
3. agent 반환 후 사용자에게 전달한다: 결과 요약 + 생성된 artifact 경로. **agent가 노출한 "사용자 확인 필요/저확신 결정·미결 항목"이 있으면 요약으로 누락하지 말고 그대로 전달한다.**
```

### codex wrapper 템플릿 (확정)

```markdown
---
name: <slug>
description: <기존 트리거 description 그대로>
version: <기존 값 그대로 — 변경 안 함>
---

# <Title> (agent wrapper)

이 스킬은 `<snake>_agent`의 thin wrapper다. canonical source는 agent다.

호출되면:
1. `spawn_agent(agent_type="<snake>_agent")`로 dispatch하며, 프롬프트에 사용자 원본 요청 전체 + 대화에서 확보된 맥락(참조 경로·이전 산출물·결정)을 verbatim 포함한다.
2. 새 파일 read·input 탐색 금지 (agent 담당).
3. `wait_agent(...)`로 결과를 수집해 사용자에게 전달한다: 결과 요약 + artifact 경로. **agent가 노출한 사용자 확인 필요/저확신 항목은 요약 누락 없이 그대로 전달한다.**
```

### Identifier Map

| slug | claude dispatch | codex dispatch |
|------|-----------------|----------------|
| feature-draft | `sdd-skills:feature-draft-agent` | `feature_draft_agent` |
| implementation | `sdd-skills:implementation-agent` | `implementation_agent` |
| implementation-plan | `sdd-skills:implementation-plan-agent` | `implementation_plan_agent` |
| implementation-review | `sdd-skills:implementation-review-agent` | `implementation_review_agent` |
| investigate | `sdd-skills:investigate-agent` | `investigate_agent` |
| plan-review | `sdd-skills:plan-review-agent` | `plan_review_agent` |
| ralph-loop-init | `sdd-skills:ralph-loop-init-agent` | `ralph_loop_init_agent` |
| spec-review | `sdd-skills:spec-review-agent` | `spec_review_agent` |
| spec-update-done | `sdd-skills:spec-update-done-agent` | `spec_update_done_agent` |
| spec-update-todo | `sdd-skills:spec-update-todo-agent` | `spec_update_todo_agent` |

## Contract/Invariant Delta Coverage

| Task | Covers |
|------|--------|
| T1 | C1, C2, C3, I1, I2, I3 (pilot=implementation ×2, 템플릿 2종 확정 포함) |
| T2 | V1~V5 (pilot 게이트, V3 nesting+dispatch+relay) |
| T3 | C1, C2, C3, I1, I2, I3 (batch 9종×2) |
| T4 | V1, V2, V4, V5, I4 (최종 검증) |

## Implementation Phases

| Phase | Tasks | 병렬성 | Checkpoint |
|-------|-------|--------|-----------|
| Phase 1 (Pilot) | T1 → T2 | 순차 (T2는 T1 검증) | **true** (게이트) |
| Phase 2 (Batch) | T3 | 스킬별 독립 → 병렬 가능 | false |
| Phase 3 | T4 | 단독 | **true** |

> 20개 SKILL.md가 독립 파일이라 충돌이 없다. pilot(implementation)이 Q1의 (a)codex dispatch·(b)nesting을 확정하는 게 핵심 게이트.

## Task Details

### Task T1: Pilot — `implementation` 스킬 2개를 wrapper로 교체 (+ 템플릿 2종 확정)
**Component**: claude/codex wrapper, 템플릿
**Priority**: P0
**Type**: Refactor

**Description**: 먼저 claude/codex wrapper 템플릿 2종과 Identifier Map(Components 참조)을 구현 기준으로 확정한다. 그 다음 `implementation` 1종을 claude+codex 양쪽에서 wrapper로 교체한다. 본문(frontmatter 아래 전체)을 thin wrapper 템플릿으로 대체하고, Mirror Notice는 "이 스킬은 implementation-agent의 wrapper다" 1줄 포인터로 바꾼다. frontmatter(name/description/version)는 무변경 보존. **`implementation`을 pilot으로 택한 이유: implementation-agent는 TDD sub-agent를 *항상* spawn하므로, 유일 미지수인 nesting(메인→wrapper→agent→sub-agent)을 결정적으로 검증한다(claude·codex 양쪽).**

**Non-Goals**: 나머지 9종은 건드리지 않는다. agent·autopilot 변경 금지. description 트리거 문구·version 변경 금지.

**Acceptance Criteria**:
- [ ] claude/codex 템플릿 2종 확정 (dispatch 식별자 + A2 맥락 전달 + "새 read 금지" + relay(확인필요 항목 보존))
- [ ] `.claude/skills/implementation/SKILL.md` 본문이 claude 템플릿으로 교체, `Agent(subagent_type="sdd-skills:implementation-agent")` 포함
- [ ] `.codex/skills/implementation/SKILL.md` 본문이 codex 템플릿으로 교체, `spawn_agent(agent_type="implementation_agent")` + `wait_agent` 포함
- [ ] 양쪽 Mirror Notice → 1줄 wrapper 포인터
- [ ] frontmatter name/description/version 무변경 보존
- [ ] 스킬 본문에 기존 process 섹션(Hard Rules/Process/Step 등) 잔존 없음

**Target Files**:
- [M] `.claude/skills/implementation/SKILL.md`
- [M] `.codex/skills/implementation/SKILL.md`

**Technical Notes**: Covers C1, C2, C3, I1, I2, I3. (구 T0의 템플릿 확정을 흡수 — 별도 ceremony task 제거)
**Dependencies**: 없음

---

### Task T2: Pilot 검증 게이트
**Component**: Verification Gate
**Priority**: P0
**Type**: Test

**Description**: implementation에 한정해 V1~V5를 실행한다. 핵심은 V3 — **편집 후 `/reload-skills`(또는 새 세션)로 wrapper를 로드**한 뒤, wrapped `implementation`을 직접 호출했을 때 (claude) `sdd-skills:implementation-agent`가 dispatch되고 **그 agent가 다시 sub-agent를 spawn(nesting)** 하는지, (codex) `spawn_agent(agent_type="implementation_agent")` 경로가 동일하게 동작하고 결과가 relay되는지 확인. **부작용 방지**: smoke dispatch 프롬프트를 "wiring 확인용 — sub-agent 1개만 spawn해 OK 받고 파일 변경 없이 종료"로 bound한다. 실패/reload 불가 시 batch 중단 + 명시 기록 + 사용자 보고.

**Acceptance Criteria**:
- [ ] V1: 본문 thin(process 섹션 없음)
- [ ] V2: dispatch 식별자·A2 문구·relay(확인필요 보존)·wait_agent(codex) 존재
- [ ] V3: reload 후 implementation wrapper 호출 → implementation-agent dispatch + **sub-agent spawn(nesting) 확인** + relay 성공 (claude 1, codex 1, bounded no-op). 불가 시 명시 기록 + 사용자 보고
- [ ] V4: frontmatter(version 포함) 무변경 보존, 포인터 교체
- [ ] V5: agent·autopilot·standalone 무변경
- [ ] 게이트 통과 전 batch 미진행

**Target Files**:
- [M] `_sdd/drafts/2026-06-02_feature_draft_mirror_skills_to_agent_wrappers.md` -- 게이트 결과 기록 (검증만)

**Technical Notes**: Covers V1~V5. Checkpoint gate. Q1 (a)codex dispatch·(b)nesting 확정 지점.
**Dependencies**: T1

---

### Task T3: Batch — 나머지 9종 × 2 wrapper 교체
**Component**: claude/codex wrapper
**Priority**: P0
**Type**: Refactor

**Description**: T2 통과 후, feature-draft·implementation-plan·implementation-review·investigate·plan-review·ralph-loop-init·spec-review·spec-update-done·spec-update-todo 9종을 claude+codex 양쪽에서 검증된 템플릿으로 교체한다(implementation은 T1에서 처리됨). Identifier Map의 dispatch 이름을 정확히 사용하고, 각 스킬의 title은 기존 헤딩을 따른다. 스킬별 독립 파일이라 병렬 처리 가능.

**Non-Goals**: implementation 재변경 금지(T1 처리). agent·autopilot·standalone 변경 금지. version 변경 금지.

**Acceptance Criteria**:
- [ ] 9종 × claude: 본문 wrapper 교체, `sdd-skills:<slug>-agent` dispatch, relay(확인필요 보존), Mirror Notice 포인터화
- [ ] 9종 × codex: 본문 wrapper 교체, `spawn_agent(agent_type="<snake>_agent")` + `wait_agent` + relay, 포인터화
- [ ] 각 스킬 frontmatter name/description/version 무변경 보존
- [ ] dispatch 식별자가 Identifier Map과 1:1 일치 (오타·substring 오염 없음 — 특히 `implementation-plan`/`implementation-review`)

**Target Files**:
- [M] `.claude/skills/{feature-draft,implementation-plan,implementation-review,investigate,plan-review,ralph-loop-init,spec-review,spec-update-done,spec-update-todo}/SKILL.md`
- [M] `.codex/skills/{feature-draft,implementation-plan,implementation-review,investigate,plan-review,ralph-loop-init,spec-review,spec-update-done,spec-update-todo}/SKILL.md`

**Technical Notes**: Covers C1, C2, C3, I1, I2, I3. 스킬별 독립 → agent 단위 병렬 dispatch 가능.
**Dependencies**: T2

---

### Task T4: 최종 검증 게이트
**Component**: Verification Gate
**Priority**: P0
**Type**: Test

**Description**: 전체 20개에 대해 V1/V2/V4/V5를 실행한다. 모든 mirror 스킬이 thin wrapper이고, dispatch 식별자가 Identifier Map과 일치하며, frontmatter 보존·포인터 교체가 됐고, agent/autopilot/standalone이 무변경인지 확인. 실패는 T3로 복귀.

**Acceptance Criteria**:
- [ ] V1: 20개 본문 전부 thin, process 섹션 잔존 0
- [ ] V2: claude 10개 `sdd-skills:<slug>-agent`, codex 10개 `spawn_agent(...<snake>_agent...)` + wait_agent
- [ ] V4: 20개 frontmatter(version 포함) 무변경 보존 + Mirror Notice 포인터화
- [ ] V5: `git diff --name-only`에 `.claude/agents/*`·`.codex/agents/*`·autopilot(`*/sdd-autopilot/**`)·standalone 스킬 12종 **변경 0건** (변경은 mirror 스킬 20개 + `_sdd/` 산출물에 한정)
- [ ] 커밋은 본 게이트 통과 후

**Target Files**:
- [M] `_sdd/drafts/2026-06-02_feature_draft_mirror_skills_to_agent_wrappers.md` -- 최종 검증 결과 기록 (검증만)

**Technical Notes**: Covers V1, V2, V4, V5, I4. Checkpoint gate.
**Dependencies**: T3

## Parallel Execution Summary

- **Phase 1 (T1→T2)**: 순차. pilot=implementation이 Q1의 (a)codex dispatch·(b)nesting을 확정하는 게이트. 템플릿 확정도 T1이 흡수.
- **Phase 2 (T3)**: 18개 SKILL.md가 서로 독립 파일이라 충돌 0 → 스킬 단위 병렬 dispatch 가능.
- **Phase 3 (T4)**: 단독 최종 게이트.
- **충돌 메모**: rename 작업과 달리 **공유 파일이 없다**(autopilot은 무영향). 유일한 순차 의존은 pilot→batch 게이트.

## Risks and Mitigations

| Risk | Mitigation |
|------|-----------|
| codex `spawn_agent`-from-skill 미작동 / nesting 미작동 | pilot=implementation의 V3에서 dispatch+nesting 결정적 확정 후 batch |
| 편집한 wrapper가 같은 세션에서 안 먹음(스킬 캐시) | V3에 `/reload-skills`/새 세션 명시 |
| 직접 호출이 메인 컨텍스트 절약 못함(가정 오류) | wrapper 본문 미로드 + agent 자체 context 실행 → 구조적 절약; pilot에서 체감 확인 |
| bare 식별자로 플러그인 배포 시 dangling | claude는 `sdd-skills:` prefix 강제(Q2) |
| A2 맥락 전달 누락으로 agent가 맥락 소실 | 템플릿에 전달 대상 명시 리스트 박음(Q3) |
| relay가 agent의 "확인 필요" surfacing을 요약으로 누락 | 템플릿 relay 규칙에 "확인필요·저확신 항목 그대로 보존 전달" 명시(C3) |
| relay가 sub-agent 전체 출력을 쏟아 절약 상쇄 | relay는 결과 요약+확인필요 항목+artifact 경로; 프로세스 중간 산출은 sub-context에 머묾 |
| 추가 latency/토큰(agent spin-up) | 토론에서 컨텍스트 절약을 우선 목표로 수용한 trade-off |

## Open Questions

- Q1~Q4는 Part 1에 결정 기록됨. Q2 HIGH, Q4 RESOLVED(drop), Q1·Q3 MEDIUM(Q1은 pilot=implementation 게이트로 확정). User confirmation 전부 불요. **in-scope 미결 0건.**

---

## Part 2 Self-Containment Check (Hard Rule 11)

- **검토 섹션 수**: 4개 task(T1~T4) + Overview/Scope/Components/Phases/Parallel/Risks.
- **Pass 1 (외부 참조 inline purpose 확인)**:
  - 근거 토론 파일: 상단 경로 + 합의 항목(A2/Mirror Notice→포인터/codex spawn_agent) 재진술 → bare path 아님. ✓
  - C/I/V ID: Part 1 정의 후 Coverage 표·Technical Notes에서 `ID + purpose` 참조. ✓
  - 고유 용어(A2, pass-through, 맥락 forwarding, mirror, thin wrapper, Identifier Map, sdd-skills prefix): 최초 사용 지점에 정의/근거. ✓
  - autopilot Hard Rule 14 참조: "플러그인 배포 시 bare 미resolve" 근거를 재진술. ✓
- **Pass 2 (생초 독자 readthrough)**:
  - 발견 갭: 초기 draft에서 "왜 sdd-skills prefix인가"가 Q2에만 있고 템플릿 옆에 근거가 없었음 → claude 템플릿/Scope Guardrail에 1줄 근거 보강.
  - 발견 갭: "thin"의 기준이 모호 → V1에 "process 섹션 잔존 0 + 본문 ≤~25줄" 측정 기준 명시.
- **보완 완료**: Yes
- **Plan-review 반영(2026-06-02, `_sdd/implementation/2026-06-02_plan_review_mirror_skills_to_agent_wrappers.md`)**:
  - M1: pilot을 `spec-review`→**`implementation`**으로 교체(TDD sub-agent 항상 spawn → nesting 결정적 검증). T1/T2/T3/Q1/Phases 반영.
  - M2: wrapper 템플릿 relay에 "agent의 사용자 확인 필요/저확신 surfacing 보존 전달" 추가(C3 확장).
  - M3: V3에 `/reload-skills`(스킬 캐시) + bounded no-op nesting smoke 명시.
  - L1: version bump drop(Q4 RESOLVED, 템플릿/AC version 무변경).
  - L2: V5를 "agent·autopilot·standalone 무변경"으로 재서술(_sdd 산출물 제외).
  - L3: 무산출 ceremony였던 T0를 제거하고 템플릿 확정을 T1에 흡수.
