# Feature Draft: task ordering late-binding (feature-draft에서 분리 → 구현 직전)

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

planning 파이프라인에서 **task ordering**(task 간 dependency edge 계산 + 실행 순서 + phase 분할 + multi/single-phase 판정 + Checkpoint 배치)을 `feature-draft` 산출에서 떼어내, 구현 직전에 도는 신규 `task-ordering-agent`로 **late-binding**한다. `feature-draft` Part 2는 **task 정의**(AC·Target Files·Contract/Invariant Delta·Validation Plan)를 그대로 소유하되 dependency edge·phase 그룹핑·multi/single 선언만 빼서 **dependency 없는 flat task-set**을 낸다. `implementation`(상위 orchestrator가 없는 사용자 직접 실행 전용 진입점)은 Step 1 task-set 확보 후 **항상** `task-ordering-agent`를 self-dispatch해 ordering을 파생한다. `sdd-autopilot`은 orchestrator가 task-ordering step을 소유해 그 산출(phase+Checkpoint)을 자신의 implementation-dispatch-controller step에 `Phase Source`로 넘긴다(`implementation` SKILL 미개입). `plan-review`는 dependency/parallelism/phase 리뷰 항목을 내려놓고 task 정의 리뷰만 유지한다. `implementation-plan` **skill 2파일**은 하위호환용 **deprecated `feature-draft` mirror**로 은퇴하고, `implementation-plan-agent` 2파일은 새 설계에서 caller가 없어 **삭제**한다.

근거: ordering을 미루는 이득의 근원은 코드베이스 실측이 아니라 **전체 조망**(모든 task가 정의된 뒤에야 의존 그래프 전모가 보인다)이므로, ordering은 확정된 task 정의에서 파생되는 결정론적 경량 계산이다. 이 판단은 구조화 토론 합의(`_sdd/discussion/2026-07-09_discussion_task_ordering_late_binding.md`)의 결정 D1~D8을 반영한다.

## Scope Delta

**In scope**
- `feature-draft` Part 2 산출 계약을 flat task-set으로 축소(ordering 제거, task 정의 유지).
- 신규 `task-ordering-agent`: flat task-set만 입력받아 ordering 산출. review-fix loop 없이 self-check만, single/multi 무관하게 항상 경유. 코드베이스 실측 없음.
- `implementation`은 상위 orchestrator가 없는 **사용자 직접 실행 전용** 진입점이므로, Step 1 task-set 확보 후 **항상** `task-ordering-agent`를 self-dispatch해 ordering을 받고 wave를 파생한다(구 "경로 B 경량 분해"의 정식 승격). Phase Source 소비 분기는 두지 않는다.
- `sdd-autopilot` 재배선(`feature-draft → task-ordering → implementation-dispatch-controller`) — autopilot이 task-ordering step을 소유해 그 산출(phase+Checkpoint)을 자신의 implementation-dispatch-controller step에 `Phase Source`로 넘긴다(`implementation` SKILL 미개입) + "multi-phase ⇒ implementation-plan 필수/single 직행" precedence 폐기 + orchestrator-contract의 implementation-plan 전용 Checkpoint 계약을 task-ordering으로 이동 + 허용 subagent_type에 `task-ordering-agent` 추가.
- `plan-review-agent`에서 dependency/parallelism/phase 추출·리뷰 항목 제거.
- `implementation-plan` **skill 2파일**을 deprecated `feature-draft` mirror로 전환(기존 트리거 보존)하고, **`implementation-plan-agent` 2파일(.md/.toml)은 삭제**(새 설계에서 caller 없음 — skill은 feature-draft-agent를, autopilot은 task-ordering-agent를 부름).
- 등록 표면 갱신: marketplace.json agents 배열·codex agents README에 `task-ordering-agent` 추가 + `implementation-plan-agent` 제거.
- claude ↔ codex 미러 짝 동시 반영.

**Out of scope**
- deprecated `implementation-plan` mirror의 완전 제거(제거 시점은 새 경로 안정화 후 별도 결정 — Q3).
- 이 변경의 실제 착수 방식(도그푸딩 vs 직접 브랜치 — Q2).
- `task-ordering-agent`의 "전체 조망" 가정을 실측으로 검증하는 후속 작업(Q1/R1).

**Guardrail delta**
- `feature-draft` Part 2의 task 정의 계약(AC·Target Files·Contract/Invariant Delta·Validation Plan), `plan-review`의 task-정의 검증, `implementation`의 런타임 가드(file-disjoint 가드레일·RED 게이트·phase review-fix gate)는 불가침으로 유지한다.
- 기존 `implementation-plan` 사용자 트리거 문구를 보존한다(하위호환).

## Persistent Spec Implications

`_sdd/spec/main.md` §2 Guardrails / §3 주요 결정에 남아야 하는 계약·불변식·검증 의도:

- **planning precedence 재정의**: non-trivial planning의 단일 entry는 `feature-draft`이며 flat task-set을 낸다. "multi-phase ⇒ `implementation-plan` 필수" precedence는 폐기한다. task ordering은 `feature-draft` 산출이 아니라 구현 직전 `task-ordering-agent`가 담당한다(late-binding). 근거: 전체 조망.
- **task ordering 소유권 불변식**: dependency edge·phase 분할·multi/single 판정·Checkpoint 배치는 `task-ordering-agent`가 단일 소유한다. `feature-draft`는 task 정의만, `plan-review`는 task 정의 리뷰만 담당한다. dispatch 배선: `implementation`(사용자 직접 실행)은 `task-ordering-agent`를 **항상 self-dispatch**한다. `sdd-autopilot`은 orchestrator가 task-ordering step을 소유해 그 산출(phase+Checkpoint)을 자신의 implementation-dispatch-controller step에 `Phase Source`로 넘긴다(`implementation` SKILL 미개입 — 상위 orchestrator가 없는 직접 실행 경로가 아니므로 소비 분기 불필요).
- **ordering 단계 계약**: `task-ordering-agent`는 flat task-set(파일)만 입력받고 코드베이스를 실측하지 않으며, review-fix loop 없이 self-check만 수행하고, single/multi 무관하게 항상 경유한다(결정론적 파생이므로 loop 불필요). "전체 조망"으로 dependency를 신뢰성 있게 복원하지 못한다고 판단되면 BLOCKED 보고한다.
- **하위호환 결정**: `implementation-plan` **skill 2파일**만 deprecated `feature-draft` mirror로 은퇴하며 기존 사용자 트리거 문구를 보존한다(사용자 트리거 표면이므로 껍데기 유지). `implementation-plan-agent`는 사용자 트리거 대상이 아닌 내부 dispatch 전용이고 새 설계에서 caller가 하나도 없어(skill은 feature-draft-agent를, autopilot은 task-ordering-agent를 부름) **삭제**한다. 새 역할에는 `task-ordering-agent` 새 이름을 쓴다(옵션 B 이름 분리; D5의 "agent도 mirror 유지"는 caller 부재 census로 "agent 삭제"로 정정).
- **런타임 가드 불변식**: ordering을 신뢰하되 `implementation`의 file-disjoint 가드레일·RED 게이트·phase review-fix gate는 late-binding 후에도 그대로 안전망으로 작동한다.
- **미러 parity**: 위 계약은 claude·codex 양 플랫폼 표면(skill/agent/contract/reference)에 동일 의미로 유지한다.

decision_log에 D1~D8 및 기각 대안(Part 2 통째 이동·현상 유지·옵션 A)을 기록한다.
<!-- spec-update-todo-input-end -->

# Part 2: Implementation and Validation Plan

## Overview

이 변경은 이 repo의 "코드"(= SDD skill/agent markdown·toml·plugin 매니페스트)를 수정해 planning 파이프라인 계약을 바꾼다. 핵심 용어(문서 전체 1회 정의):

- **flat task-set**: task 정의(AC·Target Files·Contract/Invariant Delta·Validation Plan)만 담고 task 간 dependency edge·phase 그룹핑·multi/single 선언이 없는 task 목록. 변경 후 `feature-draft` Part 2의 산출 형태다.
- **task ordering**: flat task-set을 입력으로 계산되는 dependency edge + 실행 순서 + phase 분할 + multi/single 판정 + Checkpoint 배치.
- **late-binding**: task ordering을 planning 시점이 아니라 구현 직전으로 미뤄, 모든 task가 정의된 뒤의 **전체 조망**(의존 그래프 전모)에서 파생하는 것.
- **전체 조망**: task를 다 정의해야 비로소 보이는 task 간 의존 관계의 전모. late-binding 이득의 근원이며(코드베이스 실측이 아님), ordering이 순수 파생 계산일 수 있는 전제다.

변경은 mirror 짝(claude `.md`/`.codex .toml`, claude/codex SKILL·reference) 단위 task로 나뉜다. 각 task는 한 컴포넌트를 새 계약으로 정렬한다.

Part 1의 `implementation-plan` skill deprecated mirror 전환 + `implementation-plan-agent` 삭제는 Contract C6에서, 등록 표면 정렬은 C7에서, ordering 소유권 이동은 C1~C5에서 실행 전개한다(Part 1 재진술 없이 ID로 연결).

> 작성 주의(잔여 갭 1줄): 이 draft 자체는 아직 시행되지 않은 현행 `feature-draft` 계약 하에서 생성되어 `Dependencies`/`Parallel Execution Summary`를 포함한다(변경 후엔 flat task-set이 됨 — Q2 도그푸딩 관련).

## Scope

**In scope**: Part 1 Scope Delta의 in-scope 항목 전부(ID C1~C7로 전개).
**Out of scope**: Part 1 Scope Delta의 out-of-scope 전부(Q1·Q2·Q3).

## Contract/Invariant Delta and Coverage

| ID | Type | Change | Covered By | Validated By |
|----|------|--------|------------|--------------|
| C1 | Modify | `feature-draft` Part 2가 flat task-set을 낸다 — dependency edge·phase 그룹핑·multi/single 선언 제거, task 정의 계약은 유지 | T1 | V1 |
| C2 | Add | 신규 `task-ordering-agent` — flat task-set(파일)만 입력, 코드베이스 실측 없음, dependency+순서+phase 분할+Checkpoint 산출, review-fix loop 없이 self-check만, 항상 경유 | T2 | V2 |
| C3 | Modify | `implementation`은 상위 orchestrator가 없는 사용자 직접 실행 전용 진입점이므로, Step 1 task-set 확보 후 **항상** `task-ordering-agent`를 dispatch해 ordering을 받고 wave를 파생한다(구 "경로 B 경량 분해"의 정식 승격); Phase Source 소비 분기 없음; 런타임 가드 유지 | T4 | V4 |
| C4 | Modify | `sdd-autopilot`(상위 orchestrator)은 task-ordering step을 자신이 소유해 `feature-draft → task-ordering → implementation-dispatch-controller`로 재배선하고, task-ordering 산출(ordered task-set + phase + Checkpoint)을 downstream implementation-dispatch-controller step의 `Phase Source`로 hand-off한다(`implementation` SKILL 미개입); precedence 폐기, orchestrator-contract에서 `Phase Source`·Checkpoint·planning-producer/gate 계약을 implementation-plan output → task-ordering output으로 재지정(§2·§4·§5·§6·§8), 허용 subagent_type에 `task-ordering-agent` 추가, 보조 파일(sample-orchestrator·validate_orchestrator)의 implementation-plan-agent 참조 처리 | T5 | V5 |
| C5 | Modify | `plan-review-agent`에서 dependency/parallelism/phase 추출·리뷰 항목 제거; task-정의 리뷰 유지 | T3 | V3 |
| C6 | Modify | `implementation-plan` **skill 2파일**을 deprecated `feature-draft` mirror로 전환(트리거 보존, feature-draft-agent로 위임); **agent 2파일(.md/.toml)은 삭제**(새 설계에서 caller 없음 — skill은 feature-draft-agent를, autopilot은 task-ordering-agent를 부름) | T6 | V6 |
| C7 | Modify | 등록 표면에서 `implementation-plan-agent`를 제거하고 `task-ordering-agent`를 추가 — marketplace.json agents 배열·codex README `## Agent Set`/`## Inline Writing` | T7 | V7 |
| I1 | Preserve | `feature-draft` Part 2 task 정의 계약(AC·Target Files·Contract/Invariant Delta·Validation Plan) 불변 — ordering만 제거 | T1 | V1 |
| I2 | Preserve | `implementation` 런타임 가드(file-disjoint 가드레일·RED 게이트·phase review-fix gate)와 `plan-review` task-정의 검증 불변 | T3, T4 | V3, V4 |
| I3 | Preserve | 기존 `implementation-plan` 사용자 트리거 문구 보존(하위호환) | T6 | V6 |
| I4 | Preserve | claude ↔ codex 미러 parity — 변경 컴포넌트마다 양 플랫폼 짝 동시 반영 | T1–T7 | V8 |
| I5 | Add | `task-ordering-agent`가 task 정의만으로 dependency를 신뢰성 있게 복원 못 하면 BLOCKED 보고(중단 조건 — 전체 조망 가정) | T2 | V2 |

## Touchpoints

현재 코드 재확인 기준(읽어서 확정):

- `.claude/agents/feature-draft-agent.md` / `.codex/agents/feature-draft-agent.toml` — Part 2 `Required Output` 템플릿에 `## Parallel Execution Summary`, Task 템플릿 `**Dependencies**`, `Target Files Rules`의 의미적 충돌→dependency 인코딩 규칙, Step 6의 "병렬 가능성" 지시가 있다. 이들이 ordering 산출물이므로 제거/재서술 대상. task 정의(AC·Target Files·Contract/Invariant Delta·Validation Plan) 관련 지시는 유지.
- `.claude/agents/plan-review-agent.md` / `.codex/agents/plan-review-agent.toml` — Step 2 Inventory의 `dependencies, parallelism`, 6-smell의 `Task Boundary Drift`/`DRY Risk` 중 dependency·parallel 겨냥 문구는 제거 대상, `Verification Weakness`는 유지. Input Sources·Tier는 유지. 추가로 Orchestrator Review Mode rubric(claude line 90)의 "planning precedence 준수 — feature-draft 스킵에 유효한 근거가 있는가, **multi-phase면 implementation-plan이 포함되는가**"는 C4의 precedence 폐기와 어긋나므로 새 배선(항상 task-ordering 경유)과 정합하게 문구 교체 대상 — 갱신하지 않으면 유효한 신규 orchestrator를 "implementation-plan 누락"으로 오탐해 reject/regenerate로 막는 기능적 파손이 생긴다.
- `.claude/skills/implementation/SKILL.md` / `.codex/skills/implementation/SKILL.md` — Step 1 "경로 B — no-plan 경량 분해"와 Step 3 그룹 파생이 현재 dependency 소스를 feature-draft Part 2로 가정. `implementation`은 상위 orchestrator가 없는 사용자 직접 실행 전용 진입점이므로 이 지점에 "task-set 확보 후 `task-ordering-agent`를 **항상** dispatch → 그 ordering으로 wave 파생"을 승격(Phase Source 소비 분기 없음). 런타임 가드 서술(Step 3 file-disjoint, Step 4 RED 게이트, Step 6 phase review)은 불변.
- `.claude/skills/sdd-autopilot/SKILL.md` / `.codex/skills/sdd-autopilot/SKILL.md` — planning precedence 메모(claude line 159~164), Implementation Dispatch Controller 서술.
- `.claude/skills/sdd-autopilot/references/orchestrator-contract.md` / codex 짝 — `implementation-plan output`을 `Phase Source`·Checkpoint 소스로 참조하는 계약이 단일 §이 아니라 여러 절에 분산돼 있어 census로 확정함: §2 허용 subagent_type 목록(line 55)·§2 Invariant(line 72-73 Phase Source 출처 = implementation-plan output / multi-phase ⇒ implementation-plan 의무), §4 Execution Mode(line 39,41-43 phase-iterative + Phase Source 경로), §5 planning producer/gate(line 100,107 producer = feature-draft+implementation-plan, gate 필수), §6 Checkpoint group gate(line 155,168,171,175 multi-phase per-group / Checkpoint phase / group boundary), §8 implementation-plan 전용 계약(line 202,211,217-218). 이 전 절에서 `implementation-plan output` → `task-ordering output`으로 재지정 대상. §5 producer/gate 서술은 task-ordering을 "review-fix gate 면제 파생 step"(self-check만)으로 구분해야 함.
- `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md` / codex 짝 — `feature-draft` precedence, plan-review gate placement, multi-phase execution unit selection.
- `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md` / codex 짝 — Step 4 "implementation-plan" step·Step 5 "implementation-plan producer review gate"·subagent_type·planning producer 서술이 `implementation-plan-agent`를 참조(census: claude 9 hit, codex 9 hit). task-ordering step으로 재배선 + `implementation-plan-agent` 참조 처리 대상.
- `.claude/skills/sdd-autopilot/scripts/validate_orchestrator.py` / codex 짝 — 허용 agent 목록(line 22 `"implementation-plan-agent"`)과 Phase Source 검증 메시지(line 93 "must be an implementation-plan output")가 `implementation-plan-agent`를 하드코딩. 허용 목록에 `task-ordering-agent` 추가 + `implementation-plan-agent` 처리(Phase Source 출처 검증을 task-ordering output으로 재지정) 대상.
- `.claude/skills/implementation-plan/SKILL.md` / `.codex/skills/implementation-plan/SKILL.md` — deprecated `feature-draft` mirror로 전환(skill 2파일만). frontmatter `description`의 트리거 문구는 보존.
- `.claude/agents/implementation-plan-agent.md` / `.codex/agents/implementation-plan-agent.toml` — 새 설계에서 caller가 없어 **삭제** 대상.
- `.claude-plugin/marketplace.json` — `agents` 배열(implementation-plan-agent 제거 + task-ordering-agent 추가). `.codex/agents/README.md` — `## Agent Set`(line 22)·`## Inline Writing`(line 38) 목록(implementation-plan-agent 제거 + task-ordering-agent 처리).
- (읽기 전용 참조, Target Files 아님) `_sdd/spec/main.md`·`components.md`·`decision_log.md`는 Part 1 → `spec-sync`가 갱신한다.

## Implementation Phases

- **Phase 1 — 정의 계약 축소**: T1(feature-draft flat task-set). dependency 없음.
- **Phase 2 — 신규 ordering + 하위호환**: T2(task-ordering-agent 생성, dep T1), T6(implementation-plan deprecate, dep T1). disjoint → 병렬.
- **Phase 3 — 소비자 재배선 + 등록**: T4(implementation, dep T2), T5(autopilot/contract, dep T2), T7(플러그인 등록, dep T2). disjoint → 병렬.
- **Phase 4 — precedence 정합**: T3(plan-review trim + Orchestrator Review Mode precedence 정합, dep T5). plan-review-agent 짝은 다른 task와 파일 disjoint이나, precedence 문구가 T5가 확정한 새 배선을 참조하므로(pattern ⑤ 동일 precedence 값 가정) T5 이후에 배치.

## Task Details

### Task T1: feature-draft-agent Part 2를 flat task-set으로 축소
**Priority**: P0
**Type**: Refactor

**Description**: `.claude/agents/feature-draft-agent.md`와 `.codex/agents/feature-draft-agent.toml`에서 Part 2 산출이 dependency edge·phase 그룹핑·multi/single 선언을 담지 않도록 지시를 제거한다. 구체적으로 (a) Required Output 템플릿의 `## Implementation Phases`(line 74)와 `## Parallel Execution Summary`(line 77) 산출 섹션, (b) Task 템플릿의 `**Dependencies**` 필드, (c) `Target Files Rules`의 "의미적 충돌 → dependency 인코딩" 규칙, (d) Step 6의 "병렬 가능성" 서술, (e) Delta Design의 `Implementation Phases / Task Details: 실행 순서와 task 상세`(line 138)에서 실행 순서·phase 작성 지시를 제거하고, Part 2가 flat task-set(task 정의만)을 낸다는 것을 명시한다. Integration의 relay 문구(line 320 "phase 전략이 불명확할 때만 별도 plan으로 확장")는 새 배선(ordering은 항상 `task-ordering-agent` 경유)과 정합하게 갱신한다 — feature-draft가 더 이상 phase를 산출하지 않으므로 "phase 불명확 → implementation-plan 확장" 판단 기준을 제거/재서술한다. task 정의 계약(AC 작성 위계·Target Files·Contract/Invariant Delta and Coverage·Validation Plan)은 손대지 않는다.

**Non-Goals**: task 정의 관련 어떤 지시도 바꾸지 않는다(AC falsifiability·Target Files 규격·Validation Plan linkage 유지). ordering을 어디서 하는지는 T2가 정의한다.

**Acceptance Criteria**:
- [ ] 두 파일의 Part 2 `Required Output` 템플릿에 `Implementation Phases`·`Parallel Execution Summary` 산출 섹션과 Task 템플릿의 `Dependencies` 필드가 없다.
- [ ] Delta Design의 phase/실행-순서 작성 지시(line 138)와 Step 6 "병렬 가능성" 서술이 제거되고, `Target Files Rules`의 "의미적 충돌 → dependency 인코딩(5패턴)" 지시가 제거되며, Part 2가 flat task-set을 낸다는 서술이 있다.
- [ ] Integration relay 문구(line 320)가 "feature-draft가 phase를 산출한다"는 가정을 제거하고 새 배선과 정합하게 갱신된다("phase 불명확 → implementation-plan 확장" 판단 기준 잔존 0).
- [ ] Part 2 task 정의 계약(AC·Target Files·Contract/Invariant Delta and Coverage·Validation Plan) 관련 지시가 이전과 동일하게 남아 있다.
- [ ] claude `.md`와 codex `.toml`이 같은 의미를 담는다.

**Target Files**:
- [M] `.claude/agents/feature-draft-agent.md` -- Part 2에서 ordering 산출 지시 제거
- [M] `.codex/agents/feature-draft-agent.toml` -- 동일 (codex 미러)

**Technical Notes**: Covers C1, I1(task 정의 계약 유지), I4(미러). validated by V1. Part 2가 downstream `task-ordering-agent`(T2)의 입력이 되므로 flat task-set 형식이 T2 입력 계약과 정합해야 한다.
**Dependencies**: 없음

### Task T2: task-ordering-agent 신규 생성
**Priority**: P0
**Type**: Feature

**Description**: flat task-set만 입력받아 task ordering을 산출하는 신규 agent를 만든다. 입력=`feature-draft` Part 2가 남긴 flat task-set 파일(코드베이스 실측 없음, 파일만 read). 출력=dependency edge + 실행 순서 + phase 분할 + multi/single 판정 + Checkpoint 배치. 동작 계약: review-fix loop 없이 self-check만 수행하고, single/multi 무관하게 항상 경유하며(결정론적 파생이라 loop 불필요), 전체 조망으로 dependency를 신뢰성 있게 복원하지 못한다고 판단되면 BLOCKED를 보고한다(중단 조건). dependency 인코딩 규칙(의미적 충돌 5패턴 → 무방향 mutex도 임의 방향 dependency로 흡수)과 Checkpoint 규칙은 기존 `implementation-plan-agent`가 보유하던 서술을 이 agent로 옮겨 근거를 둔다. claude `.md`와 codex `.toml` 짝을 만든다.

**Non-Goals**: task 정의(AC·Target Files 등)를 재작성하지 않는다(입력을 그대로 정렬만). 코드베이스를 실측하지 않는다. 자체 sub-agent를 spawn하지 않는다(nesting 1단계).

**Acceptance Criteria**:
- [ ] `.claude/agents/task-ordering-agent.md`와 `.codex/agents/task-ordering-agent.toml`이 생성된다.
- [ ] agent 계약에 입력=flat task-set 파일(코드베이스 실측 없음), 출력=dependency+순서+phase 분할+multi/single 판정+Checkpoint가 명시된다.
- [ ] "review-fix loop 없이 self-check만", "single/multi 무관 항상 경유", "복원 불가 시 BLOCKED 보고(중단 조건)"가 각각 문장으로 존재한다.
- [ ] agent가 Grep/Glob로 코드베이스를 실측하라는 지시가 없다(입력 파일 read만).
- [ ] claude `.md`와 codex `.toml`이 같은 의미를 담는다(codex는 `spawn_agent`/Codex Agent Boundary 규약 반영).

**Target Files**:
- [C] `.claude/agents/task-ordering-agent.md` -- 신규 ordering agent (D1/D4가 분리한 새 역할, 기존 어느 agent에도 속하지 않음)
- [C] `.codex/agents/task-ordering-agent.toml` -- codex 미러

**Technical Notes**: Covers C2, I5(BLOCKED 중단 조건), I4(미러). validated by V2. `[C]` 근거: task ordering은 task 정의(feature-draft)와 분리된 별도 execution unit이라 기존 파일에 얹으면 D1의 역할 분리를 깬다 — agent layer 관례(파일당 1 execution unit)에 맞춰 신규 파일이 맞다. dependency 인코딩·Checkpoint 규칙의 현행 근거는 feature-draft-agent(T1이 제거)와 `implementation-plan-agent`(T6가 삭제)에 있으므로 이 규칙을 task-ordering-agent로 옮겨 새 단일 홈을 둔다(refactor 이동 — 내용은 authoring 시점에 반영하며, 파일 삭제 타이밍과 무관).
**Dependencies**: T1 (task-ordering 입력 = feature-draft flat task-set 산출 계약; producer-consumer)

### Task T3: plan-review-agent에서 dependency/parallelism/phase 리뷰 제거
**Priority**: P1
**Type**: Refactor

**Description**: `.claude/agents/plan-review-agent.md`와 codex 짝에서 ordering 소관이 된 리뷰 항목을 제거한다. Step 2 Inventory의 `dependencies, parallelism` 추출, 6-smell의 dependency·parallel·phase 충돌 겨냥 문구를 내린다. task-정의 리뷰(Scope Creep·New File Justification·Single-use Abstraction·Verification Weakness의 AC↔V·Target Files·falsifiability)는 그대로 유지한다.

**Non-Goals**: task 정의 리뷰 rubric을 약화하지 않는다. Tier·Input Sources는 손대지 않는다.

**Acceptance Criteria**:
- [ ] Step 2 Inventory에서 `dependencies`·`parallelism` 추출 지시가 제거된다.
- [ ] 6-smell 중 dependency/phase 충돌을 직접 겨냥하던 문구가 ordering은 리뷰 대상 아님을 반영해 제거/재서술된다.
- [ ] task-정의 리뷰 항목(Verification Weakness의 AC↔`V*` 1:1·Target Files·New File Justification)이 그대로 남는다.
- [ ] Orchestrator Review Mode rubric(claude line 90)의 "multi-phase면 implementation-plan이 포함되는가" 문구가 새 배선(항상 task-ordering 경유 — Contract C4 precedence 폐기 반영)과 정합하게 교체되고, 두 플랫폼 짝(.md + .toml)에 동일 반영된다. 교체 후 rubric에 "multi-phase ⇒ implementation-plan 포함"을 요구하는 문구가 남지 않는다.
- [ ] claude `.md`와 codex `.toml`이 같은 의미를 담는다.

**Target Files**:
- [M] `.claude/agents/plan-review-agent.md` -- dependency/parallelism/phase 리뷰 항목 제거 + Orchestrator Review Mode precedence 문구 교체
- [M] `.codex/agents/plan-review-agent.toml` -- codex 미러

**Technical Notes**: Covers C5, I2(task-정의 검증 유지), I4(미러). validated by V3. Orchestrator Review Mode의 "planning precedence" rubric 문구를 T5의 precedence 폐기(C4)와 정합하게 교체하는 것이 이 task 범위에 포함된다 — T5(orchestrator-contract·autopilot)와 plan-review는 파일 겹침이 없으나 precedence 개념의 생산-소비 관계이므로 dependency로 인코딩.
**Dependencies**: T5 (precedence 폐기 계약의 정합 대상 — plan-review rubric 문구가 T5가 확정한 새 배선을 참조)

### Task T4: implementation Step 1에 task-ordering 항상 경유 배선
**Priority**: P0
**Type**: Refactor

**Description**: `.claude/skills/implementation/SKILL.md`와 codex 짝에서, `implementation`이 상위 orchestrator가 없는 **사용자 직접 실행 전용** 진입점임을 반영해 task-set 확보(Step 1) 후 **항상** `task-ordering-agent`를 self-dispatch하고, 받은 ordering(dependency edge·phase·Checkpoint)으로 Step 3 wave를 파생하도록 서술한다. 현재 "경로 B — no-plan 경량 분해"가 이 정식 ordering 단계로 승격된다(구 '경로 B 경량 분해'의 정식 승격). dependency 소스가 feature-draft Part 2 직접 파싱이 아니라 `task-ordering-agent` 출력임을 명시한다. Phase Source 소비 분기는 두지 않는다. 런타임 가드(Step 3 file-disjoint 가드레일, Step 4 RED 게이트, Step 6 phase review-fix gate)는 그대로 둔다.

**Non-Goals**: wave 파생 규칙·file-disjoint 가드레일·RED/GREEN 게이트·phase review loop를 바꾸지 않는다. `task-ordering-agent` 내부 계약은 T2 소관. 상위 orchestrator(autopilot)의 task-ordering step 소유·hand-off 배선은 T5 소관이며, autopilot은 `implementation` SKILL을 경유하지 않으므로 이 SKILL에 Phase Source 소비 분기를 넣지 않는다.

**Acceptance Criteria**:
- [ ] task-set 확보(Step 1) 후 `task-ordering-agent`를 **항상** self-dispatch해 ordering을 수령함이 명시된다(Phase Source 유무 분기 없음).
- [ ] Step 3 wave 파생이 `task-ordering-agent` 출력(dependency/phase)을 소스로 삼는다는 서술이 있다(feature-draft Part 2 직접 파싱 가정 제거/갱신).
- [ ] Phase Source 소비 분기·"자체 dispatch 생략" 서술이 이 SKILL에 존재하지 않는다.
- [ ] file-disjoint 가드레일·RED 게이트·phase review-fix gate 서술이 이전과 동일하게 남아 있다.
- [ ] claude와 codex SKILL이 같은 의미를 담는다.

**Target Files**:
- [M] `.claude/skills/implementation/SKILL.md` -- Step 1 후 task-ordering 항상 self-dispatch + wave 소스 갱신
- [M] `.codex/skills/implementation/SKILL.md` -- codex 미러

**Technical Notes**: Covers C3, I2(런타임 가드 유지), I4(미러). validated by V4. `task-ordering-agent`의 출력 형식(T2)을 wave 파생이 소비하므로 producer-consumer. `implementation`은 상위 orchestrator가 없는 사용자 직접 실행 전용 진입점이라 항상 self-dispatch가 유일 경로다(구 '경로 B 경량 분해'의 정식 승격) — autopilot은 이 SKILL을 호출하지 않고 자체 implementation-dispatch-controller로 wave를 돌리므로(T5), "이중 실행" 시나리오는 애초에 성립하지 않는다.
**Dependencies**: T2 (ordering 출력 계약 소비)

### Task T5: sdd-autopilot 재배선 + precedence 폐기 + 계약 이동
**Priority**: P0
**Type**: Refactor

**Description**: autopilot(상위 orchestrator)을 `feature-draft → task-ordering → implementation-dispatch-controller`로 재배선하고, **autopilot이 task-ordering step을 자신이 소유**해 그 산출(ordered task-set + phase + Checkpoint)을 downstream implementation-dispatch-controller step(autopilot이 직접 wave를 파생·dispatch하는 step, `implementation` SKILL 미개입)의 `Phase Source`로 hand-off하도록 계약을 세운다. `orchestrator-contract.md`에서 `implementation-plan output`을 `Phase Source`·Checkpoint 소스로 참조하는 계약이 여러 절에 분산돼 있으므로(Touchpoints census 참조: §2·§4·§5·§6·§8), 부분 편집이 아니라 census된 전 절을 재지정한다. (1) planning precedence 메모(autopilot SKILL·reference)에서 "multi-phase ⇒ `implementation-plan` 필수 / single-phase 직행"을 폐기하고 task-ordering 항상 경유로 대체. (2) §2 허용 subagent_type 목록에 `sdd-skills:task-ordering-agent` 추가. (3) §2 Invariant(line 72 `Phase Source` 출처 = implementation-plan output / line 73 multi-phase ⇒ implementation-plan 의무)·§4 Execution Mode(line 39,41-43 phase-iterative + Phase Source 경로)·§6 Checkpoint group gate(line 155,168,171,175 multi-phase per-group / Checkpoint phase / group boundary)·§8 implementation-plan 전용 Checkpoint 계약(line 202,211,217-218)에서 소스를 `implementation-plan output` → `task-ordering output`으로 재지정한다. (4) §5 planning producer/gate(line 100,107)에서 task-ordering을 producer로 오분류하거나 plan-review gate를 강요하지 않도록, task-ordering이 **review-fix gate 면제(self-check만) 파생 step**임을 명시적으로 구분한다. (5) `sdd-reasoning-reference.md`의 feature-draft precedence·plan-review gate placement·multi-phase execution unit selection 서술을 새 배선으로 갱신. (6) 보조 파일 census: `sample-orchestrator.md` 짝의 Step 4 "implementation-plan" step·Step 5 "implementation-plan producer review gate"·subagent_type·producer 서술을 task-ordering step으로 재배선하고, `validate_orchestrator.py` 짝의 허용 agent 목록(line 22)에 `task-ordering-agent`를 추가하고 Phase Source 출처 검증 메시지(line 93 "must be an implementation-plan output")를 task-ordering output으로 재지정하며, 두 보조 파일에서 `implementation-plan-agent` 참조를 새 배선과 정합하게 처리한다. claude·codex 10개 파일(SKILL 2 + contract 2 + reference 2 + example 2 + script 2)에 동일 반영.

**Non-Goals**: implementation-dispatch-controller의 wave 3단계(test-author → RED 게이트 → impl)·review-fix gate 계약은 바꾸지 않는다. `implementation-plan` skill의 deprecated mirror 본문·`implementation-plan-agent` 삭제는 T6 소관. `implementation` SKILL(사용자 직접 실행 경로)의 self-dispatch 배선은 T4 소관(autopilot은 이 SKILL을 경유하지 않음).

**Acceptance Criteria**:
- [ ] autopilot SKILL·reference에서 "multi-phase ⇒ implementation-plan 필수/single 직행" precedence가 제거되고 `feature-draft → task-ordering → implementation-dispatch-controller` 배선이 명시된다.
- [ ] autopilot이 task-ordering step을 소유하고 그 산출(ordered task-set + phase + Checkpoint)을 downstream implementation-dispatch-controller step의 `Phase Source`로 hand-off함이 명시된다(`implementation` SKILL 미개입).
- [ ] `orchestrator-contract.md` 허용 subagent_type 목록에 `sdd-skills:task-ordering-agent`가 있다.
- [ ] `implementation-plan output`을 `Phase Source`·Checkpoint 소스로 참조하던 §2·§4·§6·§8 계약이 모두 `task-ordering output`으로 재지정되어, `Phase Source = implementation-plan output` 잔존 참조가 0이다(deprecated mirror 밖에서).
- [ ] §5 planning producer/gate 서술에서 task-ordering이 review-fix gate 면제(self-check만) 파생 step으로 구분되고, producer(feature-draft)의 plan-review gate 필수 규정과 혼동되지 않는다.
- [ ] autopilot per-group review-fix gate가 이 `Phase Source`(phase+Checkpoint)를 group boundary 소스로 읽음이 반영된다.
- [ ] `sample-orchestrator.md` 짝에서 Step 4/5·subagent_type·producer 서술이 task-ordering step으로 재배선되고 `implementation-plan-agent` 잔존 참조가 처리된다(구 배선 잔존 0).
- [ ] `validate_orchestrator.py` 짝의 허용 agent 목록에 `task-ordering-agent`가 있고, Phase Source 출처 검증이 task-ordering output을 허용하며, `implementation-plan-agent` 하드코딩이 새 배선과 정합하게 처리된다.
- [ ] claude·codex 짝(SKILL·contract·reference·example·script 각 2)이 같은 의미를 담는다.

**Target Files**:
- [M] `.claude/skills/sdd-autopilot/SKILL.md` -- precedence 폐기 + 재배선
- [M] `.codex/skills/sdd-autopilot/SKILL.md` -- codex 미러
- [M] `.claude/skills/sdd-autopilot/references/orchestrator-contract.md` -- subagent_type 추가 + §2·§4·§5·§6·§8 계약 재지정
- [M] `.codex/skills/sdd-autopilot/references/orchestrator-contract.md` -- codex 미러
- [M] `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md` -- precedence/gate placement 갱신
- [M] `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md` -- codex 미러
- [M] `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md` -- Step 4/5·subagent_type·producer 서술 task-ordering 재배선 + implementation-plan-agent 참조 처리
- [M] `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md` -- codex 미러
- [M] `.claude/skills/sdd-autopilot/scripts/validate_orchestrator.py` -- 허용 agent 목록에 task-ordering-agent 추가 + Phase Source 출처 검증 재지정 + implementation-plan-agent 처리
- [M] `.codex/skills/sdd-autopilot/scripts/validate_orchestrator.py` -- codex 미러

**Technical Notes**: Covers C4, I4(미러). validated by V5, V8. 10-파일 단일 목적(autopilot 재배선 + Phase Source hand-off 계약 단일화)이나 표면이 넓다 — orchestrator-contract에서 ordering 계약이 §2·§4·§5·§6·§8에 분산돼 있고 보조 파일(sample-orchestrator·validate_orchestrator)에도 implementation-plan-agent 참조가 흩어져 있어 census 근거로 함께 묶는다(§섹션 propagation·신규 agent 등록 갭 실패 클래스 주의). autopilot이 `implementation` SKILL을 호출하지 않으므로 downstream은 autopilot 자신의 implementation-dispatch-controller step이다. task-ordering-agent 이름은 T2 산출과 정합해야 하고, T2가 계약 소스이므로 dependency. T3(plan-review precedence 정합)이 이 task가 확정한 precedence 폐기를 참조하므로 T3가 이 task에 의존한다.
**Dependencies**: T2 (task-ordering agent 존재·이름·계약 참조)

### Task T6: implementation-plan skill을 deprecated feature-draft mirror로 은퇴 + agent 삭제
**Priority**: P1
**Type**: Refactor

**Description**: `implementation-plan` **skill 2파일**(claude·codex SKILL.md)을 하위호환용 deprecated `feature-draft` mirror로 전환하고, 실동작을 `feature-draft-agent`(flat task-set 산출)로 위임한다. skill frontmatter `description`의 기존 사용자 트리거 문구("create an implementation plan", "병렬 구현 계획" 등)는 보존하되(I3, 사용자 트리거 표면이므로 껍데기 유지) deprecated임을 본문에 명시한다. `implementation-plan-agent` **2파일(.md/.toml)은 삭제**한다 — 새 설계에서 이 agent를 부르는 caller가 하나도 없기 때문이다(skill은 feature-draft-agent를 위임 호출하고, autopilot은 task-ordering-agent를 부른다). agent는 사용자 트리거 대상이 아닌 내부 dispatch 전용이므로 deprecated mirror로 남길 이유가 없다. 실제 ordering 역할은 `task-ordering-agent`(T2)로 이동했음을 skill 본문에 서술한다.

**Non-Goals**: `implementation-plan` skill 트리거 문구를 삭제/변경하지 않는다(I3). skill 완전 제거는 하지 않는다(Q3). ordering 계약을 skill에 남기지 않는다(T2로 이동됨).

**Acceptance Criteria**:
- [ ] `implementation-plan` skill 2파일이 deprecated `feature-draft` mirror로 위임함(feature-draft-agent 호출)을 본문에 명시한다.
- [ ] skill frontmatter `description`의 기존 트리거 문구가 그대로 보존된다(I3는 skill frontmatter 대상).
- [ ] `.claude/agents/implementation-plan-agent.md`와 `.codex/agents/implementation-plan-agent.toml`이 삭제된다(리포지토리에서 부재).
- [ ] rewrite된 `implementation-plan` skill 2파일 **본문**에 삭제된 `implementation-plan-agent` 토큰(agent 참조)이 0이다(dangling 참조 없음 — 보존되는 것은 skill 이름/트리거 `implementation-plan`뿐).
- [ ] skill이 ordering(dependency/phase/Checkpoint) 산출을 더 이상 자기 계약으로 주장하지 않는다(task-ordering으로 이동 참조).
- [ ] claude·codex 짝(skill 2)이 같은 의미를 담는다.

**Target Files**:
- [M] `.claude/skills/implementation-plan/SKILL.md` -- deprecated feature-draft mirror(feature-draft-agent 위임, 트리거 보존)
- [M] `.codex/skills/implementation-plan/SKILL.md` -- codex 미러
- [D] `.claude/agents/implementation-plan-agent.md` -- caller 없음, 삭제
- [D] `.codex/agents/implementation-plan-agent.toml` -- codex 짝, 삭제

**Technical Notes**: Covers C6, I3(트리거 보존 — skill frontmatter 대상), I4(미러). validated by V6. 위임 대상인 `feature-draft` flat task-set 계약(T1)이 확정돼야 skill mirror가 올바른 대상(변경된 feature-draft-agent)을 가리킴 → dependency T1. agent 삭제는 caller 부재 census(skill→feature-draft-agent, autopilot→task-ordering-agent)로 근거를 둔다.
**Dependencies**: T1 (skill mirror 위임 대상 = 변경된 feature-draft 계약)

### Task T7: 등록 표면에서 implementation-plan-agent 제거 + task-ordering-agent 추가
**Priority**: P0
**Type**: Infrastructure

**Description**: 등록 표면을 새 agent 집합에 정렬한다. `.claude-plugin/marketplace.json`의 `agents` 배열에서 `implementation-plan-agent.md`를 제거하고 `./.claude/agents/task-ordering-agent.md`를 추가한다. `.codex/agents/README.md`에는 `## Agent Set`(line 19-31)과 `## Inline Writing`(line 33-43, 장문 산출을 별도 helper에 넘기지 않고 caller가 skeleton→fill→finalize를 수행하는 producer agent 목록) 두 목록에 `implementation-plan-agent`(line 22·38)가 있으므로, 두 목록 모두에서 `implementation-plan-agent`를 제거한다. `## Agent Set`에는 `task-ordering-agent`를 추가한다. `## Inline Writing` 소속 여부는 판단해 반영한다 — task-ordering-agent가 ordering(dependency/phase/Checkpoint) 산출물을 inline으로 쓰는 producer이면 추가하고, 비대상으로 판단하면 그 근거(예: ordering은 장문 inline writing이 아닌 구조화 파생물)를 남긴다.

**Non-Goals**: implementation-plan-agent 외 다른 agent 등록을 건드리지 않는다. skill 등록(skills 배열)은 대상 아님(신규 skill 없음; implementation-plan skill은 트리거 보존이라 등록 유지 — T6).

**Acceptance Criteria**:
- [ ] `marketplace.json` `agents` 배열에 `./.claude/agents/task-ordering-agent.md`가 있고, `implementation-plan-agent.md` 항목이 없다.
- [ ] `.codex/agents/README.md` `## Agent Set`에 `task-ordering-agent`가 있고, `## Agent Set`·`## Inline Writing` 두 목록 모두에서 `implementation-plan-agent`가 제거된다.
- [ ] `## Inline Writing` 목록에 대한 task-ordering-agent 소속 판단이 내려져, 소속이면 추가되고 비대상이면 근거가 명시된다(어느 쪽이든 판단 흔적이 관찰 가능).
- [ ] 등록 표면 전체(marketplace.json + codex README 두 목록)에서 `implementation-plan-agent` 잔존 참조가 0이다.
- [ ] JSON이 유효하다(파싱 가능).

**Target Files**:
- [M] `.claude-plugin/marketplace.json` -- agents 배열에서 implementation-plan-agent.md 제거 + task-ordering-agent.md 추가
- [M] `.codex/agents/README.md` -- Agent Set/Inline Writing에서 implementation-plan-agent 제거 + Agent Set에 task-ordering-agent 추가

**Technical Notes**: Covers C7, I4(미러 등록). validated by V7. 등록 추가 대상 agent 파일이 존재해야 하고(T2), 제거 대상 agent 파일은 T6에서 삭제되므로 등록 잔존 참조도 함께 제거해야 dangling 방지 — 신규 agent 등록 갭·삭제 census 잔존은 이 repo의 알려진 실패 클래스(SDD 파이프라인이 못 잡음)라 명시 task로 분리.
**Dependencies**: T2 (등록 추가 대상 파일 존재)

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, I1 | 1등급 grep + 2등급 rubric | grep으로 feature-draft-agent 2파일에 `Parallel Execution Summary`·task `Dependencies` 산출 요구 부재 확인(0 hit) + `Contract/Invariant Delta and Coverage`·`Validation Plan`·`Target Files` 지시 잔존 확인(hit). 2등급: 리뷰어가 task 정의 계약 약화 사례를 지목 못 하면 I1 충족. 증거=grep 출력 + 리뷰 판정 |
| V2 | C2, I5 | 1등급 grep + 2등급 rubric | grep으로 신규 2파일 존재 + "self-check만/항상 경유/BLOCKED 중단조건" 문장 존재 + 코드베이스 실측(Grep/Glob 지시) 부재 확인. 2등급: 리뷰어가 task 정의(AC·Target Files·Contract/Invariant Delta)만으로 dependency 5패턴을 복원하는 지시가 완결적인지 판정 — 복원 불가 사례를 지목 못 하면 I5 설계 충족(실측 검증은 Q1/R1로 후속). 증거=파일 존재·grep·리뷰 판정 |
| V3 | C5, I2 | 1등급 grep + 2등급 rubric | grep으로 plan-review-agent 2파일에서 Step 2 `dependencies`·`parallelism` 추출 지시 부재 + `Verification Weakness`/AC↔`V*`/Target Files/New File Justification 잔존 확인. Orchestrator Review Mode precedence census: "multi-phase면 implementation-plan이 포함되는가" 문구가 2파일에서 0 hit이고, 새 배선(항상 task-ordering 경유) 정합 문구가 hit. 2등급: 리뷰어가 task-정의 리뷰 약화 사례 또는 구 precedence 잔존을 지목 못 하면 C5/I2 충족. 증거=grep(구 문구 0 hit·신 문구 hit) + 리뷰 판정 |
| V4 | C3, I2 | 1등급 grep + 2등급 rubric | grep으로 implementation SKILL 2파일에 "task-set 확보 후 `task-ordering-agent` 항상 dispatch" 서술 존재 + "Phase Source 소비/자체 dispatch 생략" 분기 부재(0 hit), wave 소스=ordering 서술 존재, `file-disjoint`·`RED 게이트`·`phase review` 서술 잔존(hit) 확인. 2등급: 리뷰어가 항상 self-dispatch 단일 경로임을 확인 — Phase Source 소비 분기 잔존을 지목 못 하면 C3 충족. 증거=grep + 리뷰 판정 |
| V5 | C4 | 1등급 census grep + 2등급 rubric | grep으로 autopilot 10파일에서 (a) "multi-phase ⇒ implementation-plan 필수" 문구 0 hit, (b) 허용 subagent_type/agent 목록(orchestrator-contract §2 + `validate_orchestrator.py` line 22)에 `task-ordering-agent` hit, (c) `feature-draft → task-ordering → implementation-dispatch-controller` 배선 hit, (d) autopilot이 task-ordering step 소유 + `Phase Source` hand-off(implementation SKILL 미개입) 서술 hit. §5/§6 census: `Phase Source = implementation-plan output`(contract line 72·`validate_orchestrator.py` line 93 포함) 및 "multi-phase implementation-plan per-group"·"implementation-plan output의 각 phase Checkpoint" 잔존 참조가 deprecated mirror 밖에서 0 hit(→ task-ordering output으로 재지정 확인). §5 producer/gate에서 task-ordering "gate 면제/self-check" 구분 문구 hit. 보조 파일 census: `sample-orchestrator.md` 짝·`validate_orchestrator.py` 짝에서 `implementation-plan-agent` 잔존 참조가 새 배선과 정합하게 처리됨(구 배선 잔존 0). 2등급: 리뷰어가 §2·§4·§5·§6·§8 및 보조 파일 재지정 후 모순(implementation-plan 필수/Phase Source=implementation-plan output 잔존, task-ordering을 gate 필수 producer로 오분류, 보조 파일의 구 배선 잔존)을 지목 못 하면 충족. 증거=census grep(잔존 0 hit) + 리뷰 판정 |
| V6 | C6, I3 | 1등급 grep + 2등급 rubric | grep으로 implementation-plan **skill 2파일** frontmatter `description` 트리거 문구가 변경 전과 동일(diff 부재) + "deprecated"/"feature-draft mirror"/feature-draft-agent 위임 서술 존재 확인; `.claude/agents/implementation-plan-agent.md`·`.codex/agents/implementation-plan-agent.toml`이 리포지토리에 부재(파일 존재 확인 = not found); rewrite된 skill 2파일 **본문**에서 `implementation-plan-agent` 토큰 0 hit 확인(삭제된 agent로의 dangling 참조 census — skill 이름/트리거 `implementation-plan`은 보존 대상이라 hit 허용). 2등급: 리뷰어가 skill 위임이 실동작을 feature-draft-agent로 넘기는지, agent 삭제가 dangling caller/본문 토큰을 남기지 않는지 판정. 증거=frontmatter diff + grep(skill 본문 agent-token 0 hit) + 파일 부재 확인 + 리뷰 판정 |
| V7 | C7 | 1등급 grep + 2등급 rubric | grep `task-ordering-agent` in `.claude-plugin/marketplace.json`(agents 배열 hit) + `.codex/agents/README.md` `## Agent Set`(hit); `implementation-plan-agent`가 marketplace.json agents 배열·codex README `## Agent Set`·`## Inline Writing`에서 0 hit(등록 잔존 0); `## Inline Writing` 목록 census — 소속이면 `task-ordering-agent` hit, 비대상이면 근거 문장 hit(둘 중 하나가 관찰됨); `python3 -c json.load`로 marketplace.json 파싱 성공. 2등급: 리뷰어가 codex README 다중 목록(Agent Set + Inline Writing) 중 누락된 필수 등록 또는 implementation-plan-agent 등록 잔존을 지목 못 하면 충족. 증거=grep(신규 hit·구 0 hit) + JSON 파싱 exit 0 + 리뷰 판정 |
| V8 | I4 | 1등급 census grep + 2등급 parity | 변형형 census: `task.ordering`, `implementation.plan`, `implementation-plan-agent`, `task ordering`, 글롭/slash 변형을 claude·codex 양 트리에서 grep해 (a) 신규 agent가 양 플랫폼에 짝으로 존재. census 스코프는 토큰별로 분리한다: (b) **agent-token 전역 0** — 삭제된 `implementation-plan-agent`(agent 참조) 토큰은 deprecated skill mirror 안을 **포함해 전역 0 hit**여야 한다(삭제된 agent로의 dangling 참조 금지); 구 precedence 문구("multi-phase ⇒ implementation-plan 필수", feature-draft Part 2 dependency 산출)도 mirror 안 포함 전역 0. (c) **skill-trigger 보존** — deprecated mirror 안에서 정당하게 보존되는 토큰은 skill 이름/트리거 `implementation-plan`(frontmatter description의 사용자 트리거 문구, I3)뿐이다. 2등급: 리뷰어가 claude/codex 미러 의미 불일치 또는 삭제된 agent 토큰의 mirror 안 잔존을 지목 못 하면 parity 충족. 증거=census grep 출력(agent-token 전역 0 hit) + 리뷰 판정 |

## Parallel Execution Summary

- **Phase 1**: T1 — feature-draft-agent 짝, dependency 없음.
- **Phase 2 (병렬)**: T2 ∥ T6 — disjoint(신규 task-ordering-agent 짝 vs implementation-plan 4파일), 둘 다 dep T1.
- **Phase 3 (병렬)**: T4 ∥ T5 ∥ T7 — disjoint(implementation SKILL 짝 vs autopilot 10파일[SKILL·contract·reference·example·script 각 2] vs 등록 2파일), 셋 다 dep T2.
- **Phase 4**: T3 — plan-review-agent 짝, dep T5.
- **직렬 의존**: T1 → {T2, T6}; T2 → {T4, T5, T7}; T5 → T3. 근거는 파일 겹침이 아니라 의미적 관계(T1 flat task-set 계약 → T2 입력·T6 위임대상; T2 ordering 계약·agent 존재 → T4 소비·T5 참조·T7 등록; T5 precedence 폐기 → T3 plan-review rubric 정합, pattern ⑤ 동일 precedence 값 mutex). 각 task의 `**Dependencies**`로 인코딩되어 orchestrator가 wave를 파생한다.

# Risks/Mitigations and Open Questions

## Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| R1: `task-ordering-agent`가 task 정의만으로 dependency를 신뢰성 있게 복원 못 함(전체 조망 가정 붕괴) | 잘못된 wave 그룹핑 → 병렬 파일/의미 충돌 | `implementation` file-disjoint 가드레일(I2)이 런타임 최종 안전망; 복원 불가 판단 시 BLOCKED 보고(I5). 실측 검증은 Q1 후속 |
| R2: claude/codex 미러 의미 drift | 한 플랫폼만 새 계약 반영 → 플랫폼별 동작 불일치 | V8 census + 각 task AC의 미러 동일성 항목 |
| R3: 신규 agent 플러그인 등록 누락(알려진 실패 클래스) | `task-ordering-agent` dispatch 불가 → 파이프라인 파손 | T7 명시 task + V7 등록 grep + JSON 파싱 |
| R4: deprecated mirror 전환이 기존 트리거를 깨뜨림 | `implementation-plan` 사용자 진입 하위호환 파손 | I3 + V6 frontmatter 트리거 diff 부재 확인 |
| R5: precedence 폐기 후 §섹션/문서 표면에 구 계약 잔존 참조 | 상충하는 지시 공존(implementation-plan 필수 vs task-ordering 항상) | V8 변형형 census(claude·codex, kebab/underscore/공백/글롭/slash) |

## Open Questions

### Q1. `task-ordering-agent`의 "전체 조망"만으로 dependency 복원이 충분한가
- **Decision taken**: 전체 조망을 전제로 진행 — ordering을 task 정의 파생의 결정론적 경량 계산으로 두고 코드베이스 실측을 넣지 않는다. 구현 후 실측으로 검증하고, 신뢰성 없으면 BLOCKED 보고(I5/R1).
- **Alternatives considered**: (a) ordering 단계에 코드베이스 재실측을 넣는다 → 기각(토론 D5에서 late-binding 이득의 근원은 실측이 아니라 전체 조망으로 확정 — 실측은 중복 비용). (b) feature-draft가 richer context를 task에 실어 넘긴다 → 기각(task 정의 계약 확대 = D2의 flat task-set 취지 훼손).
- **Confidence**: MEDIUM
- **User confirmation needed**: No (설계 확정 사안이며 검증은 구현 후 실측/중단조건으로 닫힌다)

### Q2. 이 변경의 착수 방식 — 도그푸딩 vs 직접 브랜치
- **Decision taken**: 이 draft는 설계·계획만 확정한다. 착수 방식은 사용자 결정에 남기며, AI 추천은 (가) 이 변경을 `feature-draft`에 태워 도그푸딩. (이 draft가 현행 계약 하에 dependencies/Parallel Execution Summary를 포함하는 것도 이 미결과 연결된다.)
- **Alternatives considered**: (나) 직접 브랜치 구현 → 도그푸딩이 새 flat task-set/late-binding 경로를 실제 검증하는 이점이 커 (가) 추천하되 사용자 판단에 위임.
- **Confidence**: MEDIUM
- **User confirmation needed**: Yes

### Q3. deprecated `implementation-plan` mirror의 완전 제거 시점
- **Decision taken**: 이번엔 제거하지 않고 하위호환 mirror로 유지. 제거는 새 경로 안정화 확인 후 별도 작업으로 미룬다.
- **Alternatives considered**: 지금 제거 → 기각(하위호환 트리거 파손 위험 + 안정화 미확인). 토론 D5/Q3와 정합.
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q4. 관련 변경을 단일 draft로 묶을지
- **Decision taken**: 단일 draft로 묶는다 — 7개 task가 하나의 응집된 delta(ordering late-binding)의 부분들이고 강한 producer-consumer 의존으로 얽혀 있다.
- **Alternatives considered**: agent별 분리 draft → 기각(delta traceability·미러 census가 파편화되고 T1→T2→T4/T5 의존이 문서 경계를 넘음).
- **Confidence**: HIGH
- **User confirmation needed**: No
