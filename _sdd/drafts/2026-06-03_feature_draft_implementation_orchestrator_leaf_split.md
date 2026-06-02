# Feature Draft: implementation orchestrator/leaf 분리

> 근거 토론: `_sdd/discussion/2026-06-03_discussion_implementation_orchestrator_leaf_split.md` (leaf/orchestrator 분리, 그룹화=B 충돌→의존성, B1 mutex 흡수, 통합 규칙, Min scope)
> 선행 발견: `_sdd/implementation/2026-06-02_implementation_report_mirror_skills_to_agent_wrappers.md` (dispatch된 agent는 sub-agent spawn 불가 — nesting 1단계 제한)

# Part 1: Temporary Spec Draft

## Change Summary

`implementation`의 실행 모델을 **orchestrator(skill) + leaf(agent)** 로 분리한다. 동기: dispatch된 agent는 Agent 도구를 못 받아 sub-agent를 spawn할 수 없다(플랫폼 nesting 1단계 제한). 따라서 현재처럼 "skill과 agent가 동일 본문(병렬 TDD 전체)을 mirror"하면, agent가 dispatch되는 경로(autopilot 등)에서는 병렬 dispatch 지시가 실행 불가능한 죽은 코드가 된다.

재설계:
- **`implementation-agent`(leaf)**: 주어진 **단일 task**를 TDD(RED→GREEN→REFACTOR)로 구현하고 구조화된 결과를 반환한다. sub-agent를 spawn하지 않으며(Agent 도구 미보유), plan 파싱·그룹화·phase review·report 작성을 하지 않는다.
- **`implementation`(skill, orchestrator)**: 메인 루프에서 실행되어 fan-out이 가능하다. task-set을 확보(plan 파싱 또는 plan 없으면 요청을 경량 분해)하고, 병렬 그룹을 파생해 leaf agent를 task당 dispatch하며(병렬 가능 시), 통합·회귀·phase review·report를 소유한다. 병렬화는 최적화 토글일 뿐, 불가하면 순차 실행한다.
- **planner(`feature-draft`, `implementation-plan`)**: 의미적 충돌(모델 import, 동시 마이그레이션, 동일 config, API 생산-소비, 상수 충돌)을 **명시적 dependency로 인코딩**한다(이미 "같은 phase 또는 dependency"로 일부 수행 중 — 이를 dependency 우선으로 정식화). 무방향 상호배제도 임의 방향 dependency로 흡수한다.
- **`sdd-autopilot`**: 구현/fix 단계에서 단일 `implementation-agent` dispatch 대신 leaf를 그룹별 fan-out한다.

핵심 효과: nesting 문제 해소 + 직접 `/implementation` 호출에 병렬성 확보 + TDD 로직을 leaf 단일 소스로(DRY) + skill=entrypoint·agent=reusable unit이라는 기존 spec 결정(main.md L23/L90)과 정합.

## Scope Delta

**In-scope:**
- `implementation-agent` (claude `.md` + codex `.toml`): 단일 task TDD leaf로 축소, `Agent` 도구 제거.
- `implementation` SKILL (claude + codex): orchestrator로 재작성.
- `feature-draft`, `implementation-plan` (각 skill + agent, claude + codex = 8파일): 의미적 충돌 → dependency 인코딩 정식화(B/B1).
- `sdd-autopilot` (SKILL + orchestrator-contract, claude + codex): 구현/fix 단계 leaf fan-out.
- implementation skill↔agent의 Mirror Notice 제거(더 이상 동일 계약이 아님 — orchestrator vs leaf).

**Out-of-scope (의도적 보류, deferred):**
- `implementation-review`의 병렬 리뷰 레인(large-scope) 같은 패턴 전환 — 별도 트랙.
- non-fan-out 스킬 8종의 wrapper→agent 전환(원 작업) — 통합 규칙으로 방향만 확정, 별도 트랙.
- `_sdd/spec/*` 직접 수정(읽기만). Part 1 delta는 후속 `spec-update-todo`로 머지.

**Guardrail delta:**
- leaf는 sub-agent를 spawn하지 않는다(nesting 안전). orchestration은 전적으로 skill/autopilot(메인 루프).
- orchestrator의 병렬 판단: "같은 phase + dependency edge 없음 + Target Files disjoint"일 때만 병렬. **확신 없으면 순차**(기존 철학 유지). file-disjoint는 orchestrator의 싸구려 가드레일로 상시 유지(plan staleness/누락 방어).
- 사용자 entrypoint는 `implementation` skill. `implementation-agent`는 internal(직접 사용자 호출 대상 아님).

## Contract/Invariant Delta

| ID | Type | Change | Why |
|----|------|--------|-----|
| C1 | Modify | `implementation-agent` 계약을 "plan 전체 병렬 TDD"에서 "**주어진 단일 task TDD 실행**"으로 축소. plan 파싱·그룹화·phase review·report 작성 제거 | leaf는 dispatch돼도 동작 가능해야(nesting), TDD 로직 단일 소스화 |
| C2 | Modify | `implementation` skill = **orchestrator**: task-set 확보(plan 파싱 / no-plan 경량 분해) + 그룹 파생 + leaf fan-out + 통합/회귀 + phase review + report | 메인 루프에서 fan-out 수행, 직접 호출 병렬성 |
| C3 | Add | orchestrator 그룹 파생 규칙 = "같은 phase + dependency 없음 + Target Files disjoint → 병렬". 그 외 순차. file-disjoint 가드레일 상시 | 의미적 충돌을 planner가 dependency로 넘기므로 orchestrator는 trivial 규칙으로 파생(B) |
| C4 | Modify | planner(`feature-draft`, `implementation-plan`)는 의미적 충돌 5패턴을 **명시적 dependency로 인코딩**(무방향 mutex도 임의 방향 dep로 흡수) | 그룹화 두뇌를 planner에 두고 orchestrator는 dumb(B/B1) |
| C5 | Modify | `sdd-autopilot` 구현/fix 단계 = 단일 `implementation-agent` dispatch → **leaf 그룹별 fan-out** | autopilot 경로도 leaf 계약과 정합 + (가능 시) 병렬 |
| C6 | Add | implementation `progress`/`report` artifact 소유가 agent → **orchestrator(skill)/autopilot**로 이동 | leaf는 결과만 반환, 산출물은 호출자 소유 |
| I1 | Add | leaf agent는 sub-agent를 spawn하지 않는다(`Agent` 도구 미보유) | nesting 1단계 제한과 정합, 죽은 지시 제거 |
| I2 | Add | 사용자 entrypoint=`implementation` skill, `implementation-agent`=internal | main.md L23/L90 (skill=entrypoint, agent=reusable unit) 유지 |
| I3 | Add | 직접 `/implementation`은 plan 유무·병렬/순차와 무관하게 정확한 결과를 낸다(병렬은 최적화) | "병렬화만 빼고 순차" 동일 흐름 보장 |
| I4 | Add | claude/codex parity 유지 | dual-bundle 계약 |

## Touchpoints

> 모두 현재 코드 census(2026-06-03)로 확인.

- `.claude/agents/implementation-agent.md` (307줄) / `.codex/agents/implementation-agent.toml` (294줄) — 단일 task leaf로 축소. 현재 L157-189 "Sub-Agent Prompt" 블록이 leaf 계약의 기반. L8-10·L100-153·L195-283(그룹화·Step 4 병렬 dispatch·phase review·report)은 orchestrator로 이동/삭제. L4 `tools`에서 `"Agent"` 제거.
- `.claude/skills/implementation/SKILL.md` (306줄) / `.codex/skills/implementation/SKILL.md` (297줄) — orchestrator로. 기존 Step 1-7은 대부분 유지하되, Step 4의 "Sub-agent를 Agent tool로 dispatch"를 "`sdd-skills:implementation-agent` leaf를 task당 dispatch"로, Step 3 충돌감지를 "dependency 기반 그룹 파생 + file-disjoint 가드레일"로 정식화, no-plan 경량 분해 경로 명시.
- `.claude/skills/feature-draft/SKILL.md`(L181,218) + `.claude/agents/feature-draft-agent.md` + codex 2개 — "의미적 충돌→dependency 인코딩(B/B1)" 정식화.
- `.claude/skills/implementation-plan/SKILL.md`(L75-83,207-216) + agent + codex 2개 — 동일.
- `.claude/skills/sdd-autopilot/SKILL.md` + `references/orchestrator-contract.md`(L44,67,120-143) + codex 2개 — leaf fan-out, report 소유, model routing 정합.
- **변경 금지(negative)**: `_sdd/spec/*`, `implementation-review`·기타 스킬, standalone 스킬.

## Implementation Plan

1. **Phase 1 (독립 병렬)**: leaf agent 축소(T1) + planner dep-encoding(T3 feature-draft, T4 implementation-plan). 세 task는 파일 disjoint·의존 없음 → 병렬.
2. **Phase 2**: orchestrator skill 재작성(T2) — leaf 계약(T1)을 소비(hard dep). T3/T4(planner dep-encoding)는 병렬성 enhancer라 미완이어도 T2는 순차로 안전 동작(M3) → 순서 유연.
3. **Phase 3**: autopilot leaf dispatch 전환(T5) — leaf 계약(T1) + orchestrator 패턴(T2)을 따름. H1 해소(2026-06-03)로 contract 문구 수정 수준 저위험, 격리.
4. **Phase 4**: 검증 게이트(T6).

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, I1 | review (grep) | leaf 본문이 단일 task TDD + `tools`에 `Agent` 없음 + 그룹화/phase review/report 섹션 잔존 0 |
| V2 | C2, C3 | review (grep) | orchestrator가 task-set 확보(plan+no-plan 분해) + dependency 기반 그룹 파생 + `sdd-skills:implementation-agent` leaf dispatch + 통합/phase review/report 포함 |
| V3 | C4 | review (grep) | planner 4파일이 "의미적 충돌→명시적 dependency(B/B1)" 명시 |
| V4 | C5, C6 | review (grep) | autopilot가 초기구현 group 병렬 + fix finding 순차 leaf dispatch + report 소유, "단일 implementation-agent로 phase 통째 dispatch" 잔존 없음. progress/report 경로·필드가 spec-update-done(L68/L70)·spec-summary 입력과 호환 |
| V5 | I4 | review (diff) | claude/codex 대칭(식별자 컨벤션 차이 제외) |
| V6 | C2, C3, I3 | smoke (executable) | `/reload-skills`/새 세션 후: 2-task 독립 plan 직접 호출 → leaf 2개 병렬 dispatch 확인; no-plan 1-task 요청 → 순차 1 leaf. bounded(실제 파일 변경 최소 scratch). 불가 시 명시 기록 |

## Risks / Open Questions

### Q1. autopilot 결합 깊이 — T5가 단순 치환이 아님 → **RESOLVED (H1 미니 토론 2026-06-03)**
- **Decision taken**: autopilot은 **instruction 생성기**이고 `fix=implementation 재호출`(agent_mapping L116)이라, T5는 별도 fan-out 코드가 아니라 **orchestrator-contract 문구 수정** 수준으로 저위험화. 구체 결정: 초기구현=group 병렬 / fix=finding 순차 / 2-group(병렬 dispatch vs Checkpoint 리뷰) 중첩 분리 / report=실행 주체 소유·경로 보존. 상세 `_sdd/discussion/2026-06-03_discussion_autopilot_leaf_fix_loop.md`. T5 description/AC에 반영 완료.
- **Alternatives considered**: autopilot을 별도 후속 트랙으로 완전 분리 → leaf 계약(C1)과 autopilot 현 dispatch 불일치로 반쪽 상태. 기각(같은 브랜치에서 함께 닫음). / agent를 "순차 multi-task 엔진"으로 둬 autopilot 무변경 → Q3에서 기각(DRY 약화·이중 모드).
- **Confidence**: HIGH (H1 토론으로 MEDIUM→HIGH)
- **User confirmation needed**: No (RESOLVED)

### Q2. report/progress artifact 소유 이동 (agent → orchestrator/autopilot)
- **Decision taken**: leaf는 결과를 호출자에게 반환만 하고, `_sdd/implementation/*_implementation_progress_*`·`*_implementation_report_*` 작성은 orchestrator(skill)와 autopilot이 소유한다. autopilot 파이프라인이 이 artifact에 의존하는 지점은 T5에서 함께 갱신한다.
- **Alternatives considered**: leaf가 per-task 부분 리포트를 쓰고 orchestrator가 병합 → N개 leaf가 동시 같은 파일 충돌·복잡도 증가. 기각.
- **Confidence**: MEDIUM
- **User confirmation needed**: Yes → **CONFIRMED (2026-06-03, 권장안 확정)**

### Q3. leaf = strict single-task(권장) vs sequential multi-task 엔진
- **Decision taken**: **strict single-task leaf**. orchestrator/autopilot이 task당 dispatch하며, 순차가 필요하면 leaf를 하나씩 호출한다. 통합 규칙("fan-out은 orchestrator, leaf는 더 쪼갤 것 없는 단위")과 일관.
- **Alternatives considered**: leaf를 "1+ task 순차 엔진"으로 두면 autopilot이 phase를 통째 넘겨도 동작해 autopilot 변경이 줄지만, (a) leaf가 다시 task 분해·순차 관리를 품어 단일 task 경계가 흐려지고, (b) report/plan 파싱이 leaf에 남아 DRY가 약화되며, (c) skill fan-out 시 "단일 task 모드 vs 전체 모드" 이중 모드가 생긴다. 기각하되, autopilot 비용이 과하면 재고 여지.
- **Confidence**: MEDIUM
- **User confirmation needed**: Yes → **CONFIRMED (2026-06-03, strict single-task 권장안 확정)**. autopilot 변경(T5)이 필수가 됨을 수용.

### Q4. 전환기 — 구식 plan의 과병렬 위험
- **Decision taken**: orchestrator는 dependency를 신뢰하되 **file-disjoint 가드레일을 상시 적용**하고, dependency 정보가 빈약/부재하면 **순차로 기본 fallback**한다(기존 "불확실하면 순차" 유지). 즉 dependency 미인코딩 구식 plan은 안전하게 덜 병렬화될 뿐 오작동하지 않는다.
- **Alternatives considered**: orchestrator가 의미적 충돌 5패턴을 자체 재검출 → orchestrator가 다시 무거워져 planner와 중복(B 취지 상쇄). 기각.
- **Confidence**: MEDIUM
- **User confirmation needed**: No

### Q5. implementation skill↔agent Mirror Notice 처리
- **Decision taken**: 제거한다. 분리 후 둘은 동일 계약이 아니라 orchestrator↔leaf 관계이므로 "함께 수정" 동기화 의무가 성립하지 않는다. 대신 각자 1줄로 상대 역할을 참조(예: skill→"leaf는 implementation-agent", agent→"orchestrator는 implementation skill").
- **Alternatives considered**: Mirror Notice 유지 → 허위 동기화 의무. 기각.
- **Confidence**: HIGH
- **User confirmation needed**: No

---

# Part 2: Implementation Plan

## Overview

`implementation`의 mirror 구조(skill≈agent 전체 복제)를 **orchestrator(skill) + leaf(agent)** 로 분리하고, 그룹화 두뇌를 planner의 dependency 인코딩(B/B1)으로 옮긴다. leaf는 단일 task TDD만 수행(sub-agent spawn 없음)하므로 dispatch돼도 동작하며, fan-out은 메인 루프 orchestrator(implementation skill, autopilot)가 담당한다. autopilot은 결합이 깊어 마지막 Phase로 격리한다. 작업은 전용 브랜치 `refactor/implementation-orchestrator-leaf`에서 진행하고 검증 게이트 통과 후 커밋한다.

칼선: leaf = 단일 task TDD 엔진(C1/I1) / skill = task-set 확보 + 그룹 파생 + fan-out + 통합 + report(C2/C3/C6) / planner = 충돌을 dependency로(C4) / autopilot = leaf fan-out(C5).

## Scope

In/Out-of-scope는 Part 1 `Scope Delta`와 동일. 요약: implementation 2종(skill/agent) + planner 2종(skill+agent) + autopilot, 모두 ×claude/codex. implementation-review·wrapper 트랙·spec은 제외.

## Components

| Component | 역할 |
|-----------|------|
| leaf 계약 (implementation-agent) | 단일 task TDD 입력/규칙/출력 (기존 Sub-Agent Prompt 승격) |
| orchestrator (implementation skill) | task-set 확보 + 그룹 파생 + leaf fan-out + 통합/phase review/report |
| 그룹 파생 규칙 | "같은 phase + dep 없음 + Target Files disjoint → 병렬"(B), file-disjoint 가드레일 |
| planner dep-encoding | 의미적 충돌 5패턴 → 명시적 dependency(B), 무방향 mutex 임의 방향(B1) |
| autopilot fan-out | 구현/fix 단계 leaf 그룹별 dispatch + report 소유 |

### leaf 계약 (확정, 토론 산출)

```
# Implementation Task (leaf)

당신은 단일 task를 TDD로 구현하는 leaf agent다. sub-agent를 spawn하지 않는다.

## 입력 (orchestrator가 dispatch 시 전달)
- Task: id, title, component, priority, description, acceptance criteria, technical notes
- Target Files (쓰기 허용 경계)
- 환경/테스트: test command + env setup (orchestrator가 전달 — 재탐색 안 함)
- 선행 보장: 이 task의 dependency는 완료됨; 그 산출물은 read-only 참조 가능

## 규칙
1. TDD 필수: 각 AC마다 RED → GREEN → REFACTOR
2. 파일 경계: Target Files만 생성/수정/삭제, 그 외 read-only. 초과 필요 시 직접 건드리지 말고 `UNPLANNED_DEPENDENCY: {경로} - {설명}` 보고
3. Minimum-Code Mandate: AC 외 옵션·설정·추상화·에러처리 금지(REFACTOR 단계 단일 사용처 추상화도 금지)
4. Verification Gate: 테스트 실제 실행 + 출력 근거. 프레임워크 없으면 `UNTESTED` 표기
5. Spec 불가침: `_sdd/spec/` 미접촉

## 출력 (orchestrator로 반환)
- 결과: SUCCESS / PARTIAL / FAILED
- TDD 진행표 (Criterion·RED·GREEN·REFACTOR)
- 생성/수정 파일 [C/M] path (N lines)
- 테스트 결과 (새 테스트 수 + 통과 여부, 근거)
- UNPLANNED_DEPENDENCY (있으면)
- 발견 사항

## 안 하는 것 (orchestrator 소유)
plan 파싱 · 충돌분석/그룹화 · fan-out · post-group 전체 테스트·회귀 · phase review · progress/report 작성
```

## Contract/Invariant Delta Coverage

| Task | Covers |
|------|--------|
| T1 | C1, I1 (leaf 축소 + Agent 도구 제거) |
| T2 | C2, C3, C6, I2, I3 (orchestrator + 그룹 파생 + report 소유 + no-plan 분해) |
| T3 | C4 (feature-draft dep-encoding) |
| T4 | C4 (implementation-plan dep-encoding) |
| T5 | C5, C6 (autopilot fan-out + report 소유) |
| T6 | V1~V6 (검증) |

## Implementation Phases

| Phase | Tasks | 병렬성 | Checkpoint |
|-------|-------|--------|-----------|
| Phase 1 | T1, T3, T4 | 파일 disjoint·의존 없음 → 병렬 | false |
| Phase 2 | T2 | 단독 (T1 hard dep; T3/T4 enhancer) | **true** (핵심 계약 닫힘) |
| Phase 3 | T5 | 단독 (H1 해소로 저위험, 격리) | **true** |
| Phase 4 | T6 | 단독 | **true** |

> dependency 인코딩(우리 B 규칙의 자가적용): T2는 T1(leaf 계약, API 생산-소비)에 hard dep → Phase 2로 분리(T3/T4는 enhancer라 순서 유연, M3). T5는 T1·T2에 의존 → Phase 3.

## Task Details

### Task T1: implementation-agent를 단일 task TDD leaf로 축소
**Component**: leaf 계약
**Priority**: P0
**Type**: Refactor

**Description**: `implementation-agent`(claude `.md` + codex `.toml`)의 본문을 위 "leaf 계약"으로 교체한다. 현재 L157-189의 "Sub-Agent Prompt"를 정식 계약으로 승격하고, plan 로딩(Step 1)·task tracking(Step 2)·그룹화(Step 3)·병렬 dispatch(Step 4)·post-group 통합(Step 5)·phase review(Step 6)·final report(Step 7)를 **제거**한다(orchestrator로 이동). frontmatter `tools`에서 `"Agent"`를 제거한다(claude). description은 "단일 task를 TDD로 구현하는 internal leaf"로 갱신. Mirror Notice는 "orchestrator는 implementation skill" 1줄 포인터로 교체.

**Non-Goals**: orchestrator 로직을 leaf에 남기지 않는다. report/progress 작성 책임 없음. skill 파일은 T2에서.

**Acceptance Criteria**:
- [ ] leaf 본문 = 단일 task TDD 입력/규칙/출력 계약 (그룹화·phase review·report 섹션 없음)
- [ ] claude frontmatter `tools`에 `"Agent"` 없음
- [ ] description이 "단일 task leaf"로 갱신, codex `developer_instructions`도 동일 본문
- [ ] Mirror Notice → orchestrator 역할 포인터 1줄
- [ ] Verification Gate·Minimum-Code·파일 경계·Spec 불가침 규칙 보존

**Target Files**:
- [M] `.claude/agents/implementation-agent.md`
- [M] `.codex/agents/implementation-agent.toml`

**Technical Notes**: Covers C1, I1. leaf 계약은 Components 절 참조. codex는 본문이 `developer_instructions='''...'''`에 임베드됨.
**Dependencies**: 없음

---

### Task T2: implementation SKILL을 orchestrator로 재작성
**Component**: orchestrator
**Priority**: P0
**Type**: Refactor

**Description**: `implementation` SKILL(claude + codex)을 orchestrator로 재작성한다. (1) **task-set 확보**: plan 탐색(기존 Step 1 경로 유지) 또는 plan 없으면 요청을 task로 **경량 분해**(충돌분석 rigor 불필요 — 순차 실행이므로). (2) **그룹 파생**: "같은 phase + dependency edge 없음 + Target Files disjoint → 병렬 그룹"(C3). 의미적 충돌은 planner가 dependency로 인코딩하므로 orchestrator는 이 규칙만 적용하고, **file-disjoint 가드레일**(그룹 내 Target Files 실제 disjoint 검사 → 위반 시 그 그룹 순차)과 "확신 없으면 순차"를 유지(Q4). (3) **fan-out**: 그룹 내 task마다 `Agent(subagent_type="sdd-skills:implementation-agent")`(codex는 `spawn_agent(agent_type="implementation_agent")`+`wait_agent`)로 leaf dispatch, 프롬프트에 leaf 입력(task 필드 + Target Files + 환경/테스트 + 선행 보장)을 전달. 병렬 불가/no-plan이면 순차로 하나씩. (4) **통합/회귀/phase review/report**: 기존 Step 5-7을 orchestrator가 소유(C6). leaf 출력(UNPLANNED_DEPENDENCY 등)을 수집·처리.

**Non-Goals**: per-task TDD 절차를 skill에 복제하지 않는다(leaf 소유). autopilot은 T5.

**Acceptance Criteria**:
- [ ] task-set 확보가 plan 경로 + **no-plan 경량 분해** 두 경로를 명시
- [ ] 그룹 파생이 "phase + dependency + Target Files disjoint" 규칙 + file-disjoint 가드레일 + 순차 fallback 포함
- [ ] leaf dispatch가 `sdd-skills:implementation-agent`(claude)/`spawn_agent(...implementation_agent)`+`wait_agent`(codex)로, leaf 입력 4종 전달
- [ ] 통합·회귀(Regression Iron Rule)·phase review·report 소유가 skill에 명시
- [ ] **progress/report를 기존 canonical 경로·dated slug·소비 필드 그대로 생성**(소유자만 leaf→skill로 변경; spec-update-done/spec-summary 호환)(M2)
- [ ] "병렬화만 빼면 순차 동일 흐름"(I3)이 드러남
- [ ] Mirror Notice → "leaf는 implementation-agent" 포인터 1줄, frontmatter(name/description/version) 보존

**Target Files**:
- [M] `.claude/skills/implementation/SKILL.md`
- [M] `.codex/skills/implementation/SKILL.md`

**Technical Notes**: Covers C2, C3, C6, I2, I3. 기존 Step 3 충돌감지(5패턴)는 planner로 이동했으므로 orchestrator에는 dependency 기반 규칙만 남긴다.
**Dependencies**: T1 (leaf 계약)만 hard dep. **T3·T4는 병렬성 enhancer**(없어도 Q4 가드레일로 순차 안전) — hard dep 아니므로 분리 가능(M3).

---

### Task T3: feature-draft에 의미적 충돌→dependency 인코딩 정식화
**Component**: planner dep-encoding
**Priority**: P0
**Type**: Refactor

**Description**: `feature-draft`(skill + agent, claude + codex)에서 의미적 충돌 처리(현재 L181/L218: "같은 phase에 두거나 dependency를 명시")를 **"명시적 dependency 인코딩 우선"**으로 정식화한다(C4). 5패턴(모델 import, 동시 마이그레이션, 동일 config, API 생산-소비, 상수 충돌) 감지 시 task `Dependencies`에 edge로 기록하고, **무방향 상호배제(마이그레이션·config·상수)도 임의 방향 dependency로 흡수**(B1)함을 1줄 명시. orchestrator가 이 dependency로 그룹을 파생함을 짧게 언급(왜 dependency가 권위 있는지).

**Non-Goals**: 새 schema 필드 추가 금지(기존 `Dependencies` 사용). 그룹 자체를 plan에 emit하지 않음(orchestrator가 파생).

**Acceptance Criteria**:
- [ ] 5패턴 → `Dependencies` edge 인코딩이 명시(claude/codex skill+agent 4파일)
- [ ] 무방향 mutex의 임의 방향 dependency 흡수(B1) 1줄 포함
- [ ] 기존 `Dependencies` 필드만 사용(새 schema 없음)
- [ ] skill↔agent mirror 동기 유지(둘 다 동일 변경)

**Target Files**:
- [M] `.claude/skills/feature-draft/SKILL.md`
- [M] `.claude/agents/feature-draft-agent.md`
- [M] `.codex/skills/feature-draft/SKILL.md`
- [M] `.codex/agents/feature-draft-agent.toml`

**Technical Notes**: Covers C4. feature-draft는 skill↔agent가 여전히 mirror(둘 다 planner) → Mirror Notice 유지, 양쪽 동일 수정.
**Dependencies**: 없음

---

### Task T4: implementation-plan에 의미적 충돌→dependency 인코딩 정식화
**Component**: planner dep-encoding
**Priority**: P0
**Type**: Refactor

**Description**: `implementation-plan`(skill + agent, claude + codex)에서 의미적 충돌 처리(현재 L75-83, L207-216 "Map Dependencies and Parallelism")를 T3와 동일 규칙으로 정식화한다(C4/B1). "동일 파일 반복 → phase/dependency 조정"과 "의미적 충돌 → 같은 phase 또는 dependency"를 **dependency 인코딩 우선**으로 통일. phase `Checkpoint`(group 경계)와 task `Dependencies`(병렬 판단)의 역할 구분을 1줄 명확화.

**Non-Goals**: 새 schema 금지. autopilot의 Checkpoint 소비 규약은 변경하지 않음(T5에서 별도).

**Acceptance Criteria**:
- [ ] 5패턴 → `Dependencies` edge 인코딩 명시(claude/codex skill+agent 4파일)
- [ ] B1(무방향 mutex 흡수) 1줄 포함
- [ ] phase Checkpoint(리뷰 group 경계) vs dependency(병렬 판단) 역할 구분 명확
- [ ] skill↔agent mirror 동기 유지

**Target Files**:
- [M] `.claude/skills/implementation-plan/SKILL.md`
- [M] `.claude/agents/implementation-plan-agent.md`
- [M] `.codex/skills/implementation-plan/SKILL.md`
- [M] `.codex/agents/implementation-plan-agent.toml`

**Technical Notes**: Covers C4. T3와 동일 규칙을 공유하나 파일 disjoint라 T3와 병렬 가능.
**Dependencies**: 없음

---

### Task T5: sdd-autopilot 구현/fix 단계를 leaf fan-out으로 전환
**Component**: autopilot fan-out
**Priority**: P0
**Type**: Refactor

**Description**: `sdd-autopilot`(SKILL + `references/orchestrator-contract.md` + `examples/sample-orchestrator.md`, claude + codex)가 생성하는 오케스트레이션 instruction에서 구현/fix 단계의 dispatch 단위를 단일 task leaf로 전환한다(C5). **autopilot은 instruction 생성기**이므로 이 전환의 핵심은 orchestrator-contract 문구 수정이다 (H1 토론 `_sdd/discussion/2026-06-03_discussion_autopilot_leaf_fix_loop.md`). 구체:
- (a) **초기 구현 step** = task를 **group 단위 병렬** leaf dispatch (trivial dep 규칙, A').
- (b) **fix step** = `fix=implementation 재호출`(agent_mapping L116)이므로 review finding을 fix-task로 보고 **finding 하나씩 순차** leaf dispatch. 별도 fix 분해 기계장치 없음.
- (c) **2-group 중첩 분리** — "병렬 dispatch 그룹(phase 내부)" vs "Checkpoint 리뷰 그룹(phase 경계)"을 다른 용어로 구분(기존 모델이 이미 이 중첩 구조).
- (d) **progress/report 소유=autopilot**, leaf는 결과만 반환, **canonical 경로·소비 필드 보존**(C6, M2 — spec-update-done/spec-summary 호환).
Model Routing(`implementation-agent`→sonnet)·agent_mapping·Checkpoint gate 정합 유지.

**Non-Goals**: review-fix gate의 severity 정책·Checkpoint 의미 변경 금지(전환은 dispatch 단위에 한정). implementation-review-agent는 미변경. fix step에 병렬 도입 금지(순차).

**Acceptance Criteria**:
- [ ] 초기 구현 step이 task group 병렬 leaf dispatch로 서술(단일 phase-통째 dispatch 잔존 0)
- [ ] fix step이 review finding 단위 **순차** leaf dispatch로 서술(`fix=implementation` 재호출 정합)
- [ ] 병렬 dispatch 그룹 vs Checkpoint 리뷰 그룹이 용어로 구분됨
- [ ] progress/report 소유=autopilot + canonical 경로·포맷·소비 필드(spec-update-done/spec-summary 호환) 보존
- [ ] Model Routing/agent_mapping/Checkpoint gate 정합, sample-orchestrator 예시도 leaf dispatch로 갱신

**Target Files**:
- [M] `.claude/skills/sdd-autopilot/SKILL.md`
- [M] `.claude/skills/sdd-autopilot/references/orchestrator-contract.md`
- [M] `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md`
- [M] `.codex/skills/sdd-autopilot/SKILL.md`
- [M] `.codex/skills/sdd-autopilot/references/orchestrator-contract.md`
- [M] `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md`

**Technical Notes**: Covers C5, C6. H1 해소(2026-06-03 토론)로 contract 문구 수정 수준으로 저위험화 — autopilot은 instruction 생성기라 새 fan-out 코드가 아니라 dispatch granularity 변경(M1). autopilot은 메인 루프(스킬)라 병렬 fan-out 가능.
**Dependencies**: T1 (leaf 계약), T2 (orchestrator 패턴)

---

### Task T6: 검증 게이트
**Component**: Verification Gate
**Priority**: P0
**Type**: Test

**Description**: V1~V6를 실행한다. 정적(V1-V5) + 런타임 smoke(V6: reload 후 2-task 독립 plan 병렬 dispatch + no-plan 순차). 실패는 해당 task로 복귀. 커밋은 게이트 통과 후.

**Acceptance Criteria**:
- [ ] V1: leaf 단일 task + Agent 도구 없음 + 그룹화/report 섹션 0
- [ ] V2: orchestrator task-set(plan+no-plan)·그룹 파생·leaf dispatch·통합/report
- [ ] V3: planner 4파일 dependency 인코딩
- [ ] V4: autopilot leaf fan-out + report 소유, 단일 phase-dispatch 잔존 0
- [ ] V5: claude/codex 대칭
- [ ] V6: smoke(병렬 2 + 순차 1) 또는 reload 불가 시 명시 기록 + 사용자 보고

**Target Files**:
- [M] `_sdd/drafts/2026-06-03_feature_draft_implementation_orchestrator_leaf_split.md` -- 검증 결과 기록(검증만)

**Technical Notes**: Covers V1~V6. Checkpoint gate.
**Dependencies**: T2, T5

## Parallel Execution Summary

- **Phase 1 (T1·T3·T4)**: 파일 disjoint(agents/implementation-agent · skills+agents/feature-draft · skills+agents/implementation-plan), 의존 없음 → **병렬 dispatch 가능**.
- **Phase 2 (T2)**: 단독. **T1(leaf 계약, API 생산-소비)에만 hard dep**. T3/T4는 enhancer(없어도 순차 안전, M3)라 dependency edge가 약함 — 그래도 leaf 계약 소비를 위해 Phase 분리(B 규칙 자가적용).
- **Phase 3 (T5)**: 단독. H1 해소(2026-06-03)로 **contract 문구 수정 수준 저위험**. T1·T2 의존.
- **Phase 4 (T6)**: 단독 게이트.
- **충돌 메모**: implementation skill↔agent는 분리 후 mirror 아님(T1·T2 각자). feature-draft/implementation-plan은 여전히 mirror(T3/T4가 skill+agent 동시 수정).

## Risks and Mitigations

| Risk | Mitigation |
|------|-----------|
| autopilot 결합으로 T5가 review-fix 계약을 깨뜨림 | **H1 토론(2026-06-03)으로 해소**: fix=implementation 재호출이라 별도 기계장치 불필요, contract 문구 수정 수준. 2-group 중첩 분리 명시 |
| leaf 계약(C1)과 autopilot 현 dispatch 불일치로 반쪽 상태 | 같은 브랜치에서 T1~T5 함께 닫고 게이트 후 커밋 |
| 구식 plan 과병렬 | file-disjoint 가드레일 + "확신 없으면 순차" fallback(Q4) |
| report 소유 이동이 downstream(spec-update-done/spec-summary) 깨뜨림 | leaf는 미작성, 실행 주체가 **canonical 경로·소비 필드 보존**하여 작성. V4에 호환 확인(M2) |
| dispatch된 leaf가 또 spawn 시도 | leaf에서 Agent 도구 제거 + "spawn 안 함" 명시(I1) |
| V6 런타임 smoke 세션 캐시 함정 | `/reload-skills`/새 세션 후 실행, 불가 시 명시 기록 |
| codex `spawn_agent` 경로 미검증 | V6에서 claude 우선 확인, codex는 정적 + 가능 시 런타임 |

## Open Questions

- Q1(autopilot 결합)은 **H1 미니 토론(`_sdd/discussion/2026-06-03_discussion_autopilot_leaf_fix_loop.md`)으로 RESOLVED** — fix=implementation 재호출이라 contract 문구 수정 수준, T5 저위험화. Q2·Q3 확정(2026-06-03). Q4·Q5 결정됨. **in-scope 미결 0건.**
- plan-review(`_sdd/implementation/2026-06-03_plan_review_..._leaf_split.md`) 반영: H1 해소(T5 구체화) + M1(중복→dispatch granularity 변경 재서술) + M2(report 경로 보존 AC + V4 호환) + M3(T2 hard dep=T1만, T3/T4 enhancer) + M4(H1로 위험 해소되어 escape hatch 불요) + L1/L2(주석 수준).

---

## Part 2 Self-Containment Check (Hard Rule 11)

- **검토 섹션 수**: 6개 task(T1~T6) + Overview/Scope/Components/Phases/Parallel/Risks.
- **Pass 1 (외부 참조 inline purpose)**:
  - 근거 토론·선행 리포트: 상단 경로 + 합의/발견 재진술(leaf/orchestrator, B/B1, nesting 1단계). bare path 아님. ✓
  - C/I/V ID: Part 1 정의 후 Coverage·Technical Notes에서 `ID + purpose` 참조. ✓
  - 고유 용어(leaf, orchestrator, fan-out, B/B1, file-disjoint 가드레일, Checkpoint, nesting): 최초 사용 지점에 정의/근거. ✓
  - main.md L23/L90(skill=entrypoint, agent=reusable unit), L62(wrapper-backed): 재진술로 근거. ✓
- **Pass 2 (생초 독자 readthrough)**:
  - 발견 갭: "leaf가 단일 task인데 autopilot은 phase를 넘긴다"는 모순이 초기엔 안 보였음 → Q3 + T5 description에 "autopilot이 그룹 파생+task당 dispatch"로 해소 명시.
  - 발견 갭: no-plan 경로가 Part 1엔 있으나 task엔 흐릿 → T2 AC에 "no-plan 경량 분해 경로 명시" 추가.
  - 발견 갭: "phase Checkpoint(리뷰 경계) vs dependency(병렬 판단)" 혼동 가능 → T4 AC에 역할 구분 명시.
- **보완 완료**: Yes

---

## 검증 결과 (T6, 2026-06-03 실행)

구현 방식: orchestrator(메인 루프) 직접 순차 편집 + 정적 grep/diff 게이트. 사유 — 스킬/에이전트 파일 자체를 수정하는 self-referential 리팩터(현 implementation-agent를 dispatch하면 자기 정의 편집·claude↔codex parity drift 위험), env.md상 전통적 테스트 프레임워크 부재 → 검증=V1~V6 정적 게이트.

| ID | 대상 | 방법 | 결과 |
|----|------|------|------|
| V1 | C1, I1 | grep | **PASS** — leaf `tools`에 `Agent` 없음(claude), 그룹화 알고리즘·report 템플릿 잔존 0(claude/codex), 입력/출력/안하는것 3섹션 존재. orchestration 키워드는 전부 "leaf가 안 하는 것" 부정 서술뿐 |
| V2 | C2, C3 | grep | **PASS** — orchestrator가 task-set(plan 경로 A + no-plan 경로 B) + "dependency edge 없음 + Target Files disjoint" 그룹 파생 + file-disjoint 가드레일 + leaf dispatch(claude `Agent`/codex `spawn_agent`+`wait_agent`) + 통합/Phase Review/report 소유 포함 |
| V3 | C4 | grep | **PASS** — planner 8파일 전부 "명시적 dependency로 인코딩" + B1(임의 방향 mutex 흡수). implementation-plan 4파일은 Checkpoint(리뷰 group) vs dependency(병렬 판단) 역할 구분 1줄 보유 |
| V4 | C5, C6 | grep | **PASS** — autopilot 6파일에 초기구현=병렬 dispatch 그룹 + fix=finding 순차 + report=autopilot 소유(canonical 경로) + 2-group 중첩 분리(contract). "phase 통째 dispatch" 매치는 전부 "통째로 넘기지 않는다" 부정 서술(모순 0). spec-update-done/spec-summary 호환 표기 유지 |
| V5 | I4 | diff | **PASS** — 변경 18파일 = 계획된 타깃과 정확히 일치(T1:2/T2:2/T3:4/T4:4/T5:6). claude/codex 대칭(식별자 컨벤션 차이 제외). codex `.toml` triple-quote 짝 정상(2), frontmatter 유효. implementation skill↔agent Mirror Notice 제거→Role Pointer 4파일, planner는 mirror/sync footer 유지. 순증 -438줄(DRY) |
| V6 | C2,C3,I3 | smoke (executable) | **PASS (2026-06-03 실행)** — orchestrator(메인 루프)가 `sdd-skills:implementation-agent` leaf를 실제 dispatch. (a) **병렬 그룹**: disjoint scratch 2-task를 동시 dispatch → 2 leaf 병렬(~25s 동시) 성공, 각자 단일 task TDD(RED→GREEN→REFACTOR)·구조화 반환·**plan 파싱/sub-agent spawn/report 작성 안 함**·파일 경계 준수(leaf B가 A 파일 비접촉). (b) **순차 no-plan**: 1-task 직접 요청 → 단일 leaf 순차 성공. orchestrator Fresh Verification으로 3개 테스트 독립 재실행 전부 EXIT=0, 구현 최소(사변적 코드 0). H1(prefix 누락) 수정 후 prefix resolve 확인 |

**게이트 종합**: 정적(V1~V5) + 런타임(V6) **전부 PASS**. H1(implementation-review 발견, claude leaf dispatch prefix 누락) 수정 완료. 구현은 계약·런타임 모두 검증됨.
