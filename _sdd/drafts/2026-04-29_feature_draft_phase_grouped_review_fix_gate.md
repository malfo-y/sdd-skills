# Feature Draft: Phase-Grouped Review-Fix Gate (multi-phase 실행에서 review-fix를 phase 단위가 아닌 group 단위로)

<!-- spec-update-todo-input-start -->
# Part 1: Temporary Spec Draft

## Change Summary

multi-phase implementation 실행에서 review-fix gate가 **모든 phase 직후에 발생**하는 현재 구조를 **plan이 표시한 group 경계에서만 발생**하는 구조로 바꾼다.

- 변경 동기: phase 단위가 너무 작아 (a) opus review가 trivial finding만 내고, (b) review-fix loop 누적으로 latency가 길고, (c) "phase = review 단위 아님" 부적합성이 누적된다 (`_sdd/discussion/2026-04-29_discussion_phase_grouping_review_fix_gate.md` Round 1).
- 핵심 변경: implementation-plan이 phase 메타에 `Checkpoint: true/false`를 명시한다. autopilot은 `Checkpoint=true` phase 직후에만 group-scoped review-fix gate를 실행한다. group 내부 phase는 light validation(test/typecheck/exit criteria)만 유지한다.
- 부수 변경: multi-phase 실행이 implementation-plan을 반드시 거치게 강화하고(`Execution Mode: phase-iterative ⇔ Phase Source = implementation-plan output` invariant), final integration review를 그룹 수에 따라 adaptive하게 처리한다.

## Scope Delta

### In Scope

- `implementation-plan` skill/agent의 phase metadata schema에 `Checkpoint` 필드 추가 (5필드 → 6필드)
- `sdd-autopilot` skill의 Review-Fix Loop 집행 규칙 변경 (per-phase → per-group)
- `sdd-autopilot` skill의 planning precedence 강화 (multi-phase면 implementation-plan 의무화)
- `sdd-autopilot` skill의 verification 가드 추가 (Phase Source 출처 검증)
- `references/orchestrator-contract.md`의 Review-Fix Gate 섹션 per-group 재기술
- `examples/sample-orchestrator.md` Example B (multi-phase) 갱신
- `_sdd/spec/main.md`의 multi-phase quality gate 표현 갱신 (per-phase → per-group + final adaptive)
- `.claude/`와 `.codex/` mirror pair 동기 적용

### Out of Scope

- per-group으로 넘어가면서 review prompt contract의 세부 wording 튜닝 (현 prompt를 group scope로 재인용하는 수준만 적용)
- foundation 판단 heuristic의 fine-grained symbol-level dependency 분석 (논의 결과 hint만, plan 자율 판단)
- 기존 plan artifact의 retroactive migration 자동 도구화 (deferred-deliberately, `_sdd/discussion/2026-04-29_discussion_phase_grouping_review_fix_gate.md` open question Q1)
- single-phase 경로의 동작 변경 (현 그대로 유지)

### Guardrail Delta

- `Checkpoint` 미명시 default = `false` (batch). 단독 gate가 필요한 phase만 explicit `true`.
- 마지막 phase는 explicit 값과 무관하게 implicit `Checkpoint=true` (gate 한 번은 반드시 닫히도록).
- foundation 판단 heuristic은 hard rule이 아닌 권장 hint (plan opus 자율 판단 + reasoning 한 줄 의무화).
- group의 최대 크기 제한 없음 (plan 신뢰 + review-fix loop max_rounds가 안전망).
- mid-group light validation에서 critical 이슈 발견 시 group boundary forced early로 review-fix gate 즉시 트리거.

## Contract/Invariant Delta

| ID | Type | Change | Why |
|----|------|--------|-----|
| C1 | Add | `implementation-plan` 산출 phase에 `Checkpoint: true/false` 필드를 추가한다. plan은 `Checkpoint=true` 결정에 reasoning 한 줄을 동반해야 한다. | group 경계의 단일 SoT를 plan-time annotation에 둔다. trace는 사용자 검증과 후속 디버깅에 필요. |
| C2 | Modify | `sdd-autopilot`은 multi-phase 실행에서 `Checkpoint=true` phase 직후에만 review-fix gate를 닫는다. group 내 phase는 light validation(test/typecheck/exit criteria)만 수행한다. | review의 의미 단위를 phase에서 group으로 키워 review depth와 latency를 동시에 개선. |
| C3 | Add | `sdd-autopilot`의 phase-iterative 실행은 `Phase Source = implementation-plan output`이어야 한다. feature-draft 산출물을 Phase Source로 사용하면 reject한다. | `Checkpoint` 필드를 만드는 곳이 implementation-plan뿐이므로, feature-draft 직행으로 multi-phase가 시작되면 그룹 체계가 깨진다. |
| C4 | Add | `sdd-autopilot`의 multi-phase 판단(Step 4 reasoning) 시 planning precedence가 자동으로 implementation-plan을 끼우도록 강제한다. 현재 "필요한 경우" 표현을 "multi-phase면 의무"로 강화한다. | C3 invariant를 plan generation 단계에서부터 보장. verification 단계에서 reject되기 전에 차단. |
| C5 | Modify | final integration review를 그룹 수 기준으로 adaptive하게 처리한다: 그룹 1개면 마지막 group gate가 final을 겸하고, 2개+면 별도 1회를 유지한다. | group 1개 케이스의 redundant round 제거 + 2개+ 케이스의 cross-group regression focus 유지. |
| C6 | Add | group 내 phase의 light validation이 critical 이슈를 잡으면 group boundary forced early로 즉시 review-fix gate를 트리거한다 (mid-group emergency escape). | plan을 신뢰하되 명백한 폭탄은 group 끝까지 누적하지 않는다. |

| ID | Type | Change | Why |
|----|------|--------|-----|
| I1 | Add | phase 메타에 `Checkpoint`가 명시되지 않으면 default `false` (group에 포함). | batch가 새 default. 단독 gate 필요 phase만 explicit `true`. |
| I2 | Add | phase 메타의 마지막 phase는 explicit `Checkpoint` 값과 무관하게 implicit `true`로 해석된다. | gate가 한 번도 안 닫히는 케이스 차단 (전체 phase가 모두 false인 plan에서도 마지막 phase 1회 gate 보장). |
| I3 | Modify | implementation-plan의 phase metadata 필드 수가 5개에서 6개로 확장된다 (`Goal`, `Task Set / Dependency Closure`, `Validation Focus`, `Exit Criteria`, `Carry-over Policy`, `Checkpoint`). | C1 schema의 명시적 표현. plan 산출 검증 항목도 5→6으로 갱신. |
| I4 | Modify | foundation 판단 heuristic은 hard rule이 아닌 권장 hint로만 명시된다 (primary 2개: 후속 phase 2+개가 의존하는 산출물, feature-draft에서 high/critical risk로 마크된 phase). | rigid heuristic은 fragile. opus 종합 판단이 더 신뢰. |

## Touchpoints

- `_sdd/spec/main.md:65,94` — multi-phase quality gate 표현 (현재 per-phase + mandatory final integration review). C2/C5 반영 필요.
- `.claude/skills/implementation-plan/SKILL.md`, `.codex/skills/implementation-plan/SKILL.md` — Phase 템플릿(L226-237 부근)에 Checkpoint 필드, AC L24, Hard Rule L40, Phase gate metadata 규칙 L176-186. C1/I3/I4 반영.
- `.claude/agents/implementation-plan.md`, `.codex/agents/implementation-plan.toml` — 동일 변경 mirror.
- `.claude/skills/sdd-autopilot/SKILL.md`, `.codex/skills/sdd-autopilot/SKILL.md` — Step 4 reasoning rules(L164-175), Step 5 verification(L187-198), Step 7.2 execution rules(L241-256), Step 7.3 Review-Fix Loop interpretation(L258-266). C2/C3/C4/C5/C6 반영.
- `.claude/skills/sdd-autopilot/references/orchestrator-contract.md`, `.codex/...` — Review-Fix Gate 섹션 per-group 재기술. multi-phase invariant 박기.
- `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md`, `.codex/...` — Example B Step 4의 per-phase gate 표기를 per-group(`Checkpoint=true` boundary)으로 갱신. mid-group emergency 명시. final adaptive 명시.

## Implementation Plan

순서:

1. **Phase 1 (foundation, single gate)**: implementation-plan에 `Checkpoint` schema 추가 (5→6 필드, 마지막 phase implicit true 규칙, foundation hint 명시, reasoning 의무화). Claude SKILL+agent / Codex SKILL+agent 4파일 동시 변경.
2. **Phase 2 (contract foundation, single gate)**: orchestrator-contract.md (Claude+Codex 2파일) Review-Fix Gate 섹션을 per-group으로 재기술하고, `phase-iterative ⇔ Phase Source = implementation-plan output` invariant + `multi-phase ⇒ implementation-plan 의무` invariant + mid-group emergency rule을 박는다.
3. **Phase 3 (autopilot execution rules, single gate)**: sdd-autopilot SKILL.md (Claude+Codex 2파일) Step 4 planning precedence 강화 + Step 5 verification 가드 + Step 7.2/7.3 group-aware execution 규칙을 갱신한다.
4. **Phase 4 (examples + spec text, single gate)**: sample-orchestrator.md (Claude+Codex 2파일) Example B 갱신 + `_sdd/spec/main.md` 라인 65/94 표현 동기화.

각 phase는 다음 phase의 contract foundation이므로 sequential. plan의 contract 변경(Phase 1)이 closing되지 않으면 Phase 2의 invariant 표현이 일관되지 않고, Phase 2의 contract 변경이 closing되지 않으면 Phase 3 SKILL.md가 contract와 어긋난다.

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, I3 | review + smoke test | implementation-plan SKILL+agent (Claude+Codex 4파일) 동기 변경 확인. 모의 plan 1건 생성해 phase block에 `Checkpoint` 필드와 reasoning 줄이 등장하는지 검증. |
| V2 | C2, I1, I2, C6 | review + sample-orchestrator dry-run | orchestrator-contract.md / sdd-autopilot SKILL.md / sample-orchestrator.md (Claude+Codex 6파일) 동기 변경. multi-phase 시나리오에서 (a) Checkpoint=true phase 직후에만 review-fix gate, (b) 마지막 phase implicit gate, (c) mid-group critical → forced early gate가 해석되는지 확인. |
| V3 | C3, C4 | review | sdd-autopilot SKILL.md Step 4/5에 invariant + verification 가드 명시 확인. phase-iterative + Phase Source가 feature-draft인 케이스를 reject 또는 implementation-plan 자동 삽입 처리한다는 표현 존재. |
| V4 | C5 | review | sample-orchestrator Example B에 final integration review의 그룹 수 기반 adaptive 처리 명시 확인 (1 group=겸함, 2+groups=분리). orchestrator-contract도 동일. |
| V5 | I4 | review | implementation-plan SKILL/agent에 foundation hint(dependency closure, risk level)가 권장으로만 명시되고 plan 자율 판단 + reasoning 의무화 표현 존재. |
| V6 | (cross-cut) | mirror diff | Claude ↔ Codex mirror pair 4쌍(SKILL.md, agent file, orchestrator-contract.md, sample-orchestrator.md)가 의미적으로 동일한 변경을 담는지 diff 확인. |

## Risks / Open Questions

- **R1 (mitigated)**: 기존 plan artifact는 `Checkpoint` 필드가 없어 default=false로 해석되고, 결과적으로 모든 phase가 한 group으로 묶인다. 이 케이스는 마지막 phase implicit `true`(I2)로 gate 1회는 보장되지만 review depth 측면에서 새로운 best practice를 받지 못한다. mitigation: 변경 적용 후 기존 plan은 그대로 동작 + 새 plan부터 explicit annotation 사용을 SKILL.md guidance로 명시. retroactive migration 도구는 별도 작업으로 분리 (deferred-deliberately).
- **R2 (accepted)**: implementation-plan(opus)이 foundation 판단을 잘못해 group이 너무 커지면 review-fix loop가 큰 finding 폭탄을 받는다. mitigation: review-fix max_rounds(현 3) + reasoning 강제 trace + Step 6 user checkpoint에서 사용자 review. hard limit/safety net은 도입하지 않는다 (논의 Round 6 합의).
- **R3 (deferred)**: dependency 측정 단위(file/module vs symbol-level)는 plan 자율로 위임. 운영 데이터 누적 후 hint를 fine-tuning할 수 있음. (`_sdd/discussion/2026-04-29_discussion_phase_grouping_review_fix_gate.md` open question Q2)
- **OQ1**: mid-group emergency escape의 trigger 임계값 — `critical` severity만 트리거할지, 기존 review-fix loop의 `critical/high/medium` block 정책과 동일하게 갈지. 본 draft에서는 `critical` 단독 트리거로 가정하고 implementation 단계에서 확정한다.
- **OQ2**: implementation agent가 group boundary를 인지해야 하는가 — 현재 가설은 "autopilot이 group boundary를 관리하고 implementation은 phase 단위로만 동작". 운영해보고 필요 시 별도 hint를 추가한다. (`_sdd/discussion/2026-04-29_discussion_phase_grouping_review_fix_gate.md` open question Q3)
- **OQ3**: Codex 쪽 model/effort 라우팅(`gpt-5.5` + `reasoning_effort`)도 같은 변경에서 함께 갱신할지, 별도 작업으로 둘지. 본 draft는 Claude/Codex mirroring을 의미적 동등성 수준으로 맞추고, Codex의 reasoning_effort 정책은 기존 그대로 유지하는 것을 가정한다.

<!-- spec-update-todo-input-end -->

# Part 2: Implementation Plan

## Overview

`_sdd/discussion/2026-04-29_discussion_phase_grouping_review_fix_gate.md`에서 합의된 phase-grouped review-fix gate 디자인을 sdd-skills 코드베이스(Claude + Codex 양쪽)에 적용한다. 변경 핵심은 (a) implementation-plan의 phase 메타에 `Checkpoint` 필드 도입, (b) sdd-autopilot의 review-fix gate 집행을 per-phase에서 per-group으로 전환, (c) multi-phase 실행이 implementation-plan을 반드시 거치도록 invariant 강화. 모든 변경은 `.claude/`와 `.codex/`를 mirror로 동기 적용한다.

## Scope

### In Scope

- `implementation-plan` SKILL.md(Claude+Codex), agent 정의 파일(Claude .md + Codex .toml) 4파일 — Checkpoint schema 추가
- `sdd-autopilot` SKILL.md(Claude+Codex), `references/orchestrator-contract.md`(Claude+Codex), `examples/sample-orchestrator.md`(Claude+Codex) 6파일 — group-aware execution 규칙 + invariant + adaptive final
- `_sdd/spec/main.md` 1파일 — multi-phase quality gate 표현 갱신

### Out of Scope

- review prompt contract의 세부 wording 튜닝 (group scope로 재인용 수준)
- 기존 plan artifact retroactive migration
- Codex의 `reasoning_effort` 정책 변경
- single-phase path 동작 변경

## Components

| Component | 파일군 | 변경 성격 |
|-----------|--------|----------|
| **implementation-plan schema** | `.claude/skills/implementation-plan/SKILL.md`, `.codex/skills/implementation-plan/SKILL.md`, `.claude/agents/implementation-plan.md`, `.codex/agents/implementation-plan.toml` | phase metadata 5→6필드, Checkpoint 규칙, foundation hint, reasoning 의무 |
| **autopilot orchestrator contract** | `.claude/skills/sdd-autopilot/references/orchestrator-contract.md`, `.codex/skills/sdd-autopilot/references/orchestrator-contract.md` | Review-Fix Gate 섹션 per-group 재기술, invariant(C3/C4) 박기, mid-group emergency(C6) |
| **autopilot SKILL execution rules** | `.claude/skills/sdd-autopilot/SKILL.md`, `.codex/skills/sdd-autopilot/SKILL.md` | Step 4 planning precedence(C4) + Step 5 verification 가드(C3) + Step 7.2/7.3 group-aware execution(C2/C5/C6) |
| **autopilot sample example** | `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md`, `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md` | Example B per-group gate, mid-group emergency, final adaptive 표기 |
| **global spec 표현** | `_sdd/spec/main.md` | 라인 65/94 multi-phase quality gate 문장 갱신 |

## Contract/Invariant Delta Coverage

| Delta | 다루는 Component / Task |
|-------|------------------------|
| C1, I3, I4 | implementation-plan schema (T1) |
| C3, C4 | autopilot orchestrator contract + SKILL execution rules (T2, T3) |
| C2, I1, I2 | autopilot orchestrator contract + SKILL execution rules + sample example (T2, T3, T4) |
| C5 | autopilot orchestrator contract + sample example (T2, T4) |
| C6 | autopilot orchestrator contract + SKILL execution rules + sample example (T2, T3, T4) |

V1 ↔ T1 / V2 ↔ T2+T3+T4 / V3 ↔ T3 / V4 ↔ T2+T4 / V5 ↔ T1 / V6 ↔ 전 task의 mirror diff

## Implementation Phases

### Phase 1 — implementation-plan schema 확장

**Goal**: implementation-plan이 만드는 phase 메타에 `Checkpoint` 필드(C1)와 마지막 phase implicit true 규칙(I2)을 추가. foundation hint(I4) 명시. reasoning 의무화. plan AC도 5→6필드로 갱신(I3).

**Checkpoint**: `true` (Phase 2~4의 contract foundation. 후속 phase들이 모두 이 schema에 의존)
**Reason for Checkpoint**: 후속 3개 phase(2, 3, 4)가 `Checkpoint` 필드 schema에 의존. plan이 이 필드를 만들지 않으면 autopilot의 group-aware execution 규칙(Phase 3)과 sample example(Phase 4)이 무의미해짐. 단독 gate로 격리해 schema correctness를 우선 검증.

**Tasks**: T1
**Validation Focus**: V1, V5
**Exit Criteria**:
- [ ] Claude/Codex 양쪽의 implementation-plan SKILL.md AC 항목이 phase 메타 6필드를 요구
- [ ] Claude/Codex 양쪽의 implementation-plan agent 파일이 동일 schema 명시
- [ ] Phase 템플릿이 `Checkpoint` 필드 + reasoning 라인을 포함
- [ ] foundation hint 2개(dependency closure / risk level)가 권장 hint로만 명시 (hard rule 아님)
- [ ] mirror diff: Claude ↔ Codex 의미적 동등성 확인

### Phase 2 — orchestrator-contract group-aware rules

**Goal**: orchestrator-contract.md (Claude+Codex)에 Review-Fix Gate 섹션을 per-group으로 재기술(C2, I1, I2). multi-phase invariant(C3, C4) 박기. mid-group emergency 규칙(C6) 정의. final adaptive 처리(C5) 명시.

**Checkpoint**: `true` (sdd-autopilot SKILL.md와 sample example이 contract에 의존하므로 contract가 closing 안 되면 후속 표현이 어긋남)
**Reason for Checkpoint**: contract foundation. SKILL.md(Phase 3)와 sample(Phase 4)이 이 contract의 구체 표현을 인용한다. contract가 잘못되면 모든 후속 인용이 drift.

**Tasks**: T2
**Validation Focus**: V2, V4
**Exit Criteria**:
- [ ] orchestrator-contract.md(Claude+Codex)에 "Review-Fix Gate Group Boundary" 서브섹션 존재
- [ ] `Checkpoint=true` phase 직후 gate / 마지막 phase implicit / mid-group critical → forced early 규칙 명시
- [ ] `Execution Mode: phase-iterative ⇔ Phase Source = implementation-plan output` invariant 명시
- [ ] `multi-phase ⇒ implementation-plan 의무` invariant 명시
- [ ] final integration review의 group 수 기반 adaptive 규칙 명시
- [ ] mirror diff 통과

### Phase 3 — autopilot SKILL execution rules

**Goal**: SKILL.md (Claude+Codex)의 Step 4 planning precedence를 강화하여 multi-phase 판단 시 implementation-plan을 자동 의무화(C4). Step 5 verification에 Phase Source 출처 가드(C3) 추가. Step 7.2/7.3을 group-aware execution(C2, C5, C6)으로 갱신.

**Checkpoint**: `false` (Phase 4 sample example만 의존. sample이 SKILL.md 표현을 인용하긴 하지만 sample 자체가 example이라 risk가 작아 group 끝에서 한 번에 review)
**Reason for Checkpoint**: sample example이 SKILL.md의 표현을 인용하지만, sample은 illustrative 성격이라 SKILL.md의 정합성이 contract(Phase 2)에 맞기만 하면 충분. Phase 3-4를 한 group으로 묶어 review-fix를 한 번에 닫는다.

**Tasks**: T3
**Validation Focus**: V2, V3
**Exit Criteria**:
- [ ] Step 4 reasoning rule에 "multi-phase 판단 → implementation-plan 자동 포함" 표현 존재
- [ ] Step 5 verification 항목에 phase-iterative path의 Phase Source 출처 검증 추가
- [ ] Step 7.2 execution rule에서 phase 단위 gate 표현이 group 단위 gate 표현으로 교체
- [ ] Step 7.3 Review-Fix Loop interpretation이 per-group + final adaptive로 재기술
- [ ] mid-group emergency escape 명시
- [ ] mirror diff 통과

### Phase 4 — examples + spec 표현 동기화

**Goal**: sample-orchestrator.md(Claude+Codex) Example B를 group-aware로 갱신. `_sdd/spec/main.md` 라인 65/94의 multi-phase quality gate 표현을 새 디자인에 맞게 갱신.

**Checkpoint**: `true` (마지막 phase, implicit true. 전체 변경의 group-end gate)
**Reason for Checkpoint**: 마지막 phase. Phase 3과 한 group을 닫는 review-fix gate가 여기서 트리거되며, group 1개 케이스(Phase 1, 2, 3, 4가 모두 단독 gate면 group이 phase 수만큼)가 아니므로 group 끝 gate + 별도 final integration review 적용.

**Tasks**: T4
**Validation Focus**: V2, V4
**Exit Criteria**:
- [ ] Example B Step 4가 per-phase gate 표기 대신 `Checkpoint=true` boundary에 review-fix gate를 두는 표기로 갱신
- [ ] Example B에 mid-group emergency, final adaptive 표기 등장
- [ ] `_sdd/spec/main.md` 라인 65/94의 표현이 "per-phase review-fix + mandatory final integration review"에서 새 표현(group-scoped + adaptive final)으로 변경
- [ ] mirror diff 통과

## Task Details

### Task T1: implementation-plan schema에 Checkpoint 필드 추가
**Component**: implementation-plan schema
**Priority**: P0
**Type**: Feature

**Description**:
implementation-plan SKILL.md(Claude+Codex)와 agent 파일(Claude .md + Codex .toml) 4파일에 phase metadata `Checkpoint: true/false` 필드를 추가한다. 마지막 phase는 explicit 값과 무관하게 implicit `true`로 해석된다는 규칙을 명시한다. 미명시 default는 `false` (group에 포함). foundation 판단은 hard rule이 아닌 권장 hint로 명시 — primary 2개: (a) 후속 phase 2개 이상이 이 phase의 산출물(파일/schema/module)에 의존, (b) feature-draft에서 high/critical risk로 마크된 phase. plan은 `Checkpoint=true` 결정에 reasoning 한 줄을 동반해야 한다. AC와 Hard Rule, Phase 템플릿, Phase gate metadata 규칙 섹션을 모두 갱신한다.

**Acceptance Criteria**:
- [ ] Claude/Codex implementation-plan SKILL.md의 AC 항목이 6필드를 요구하도록 변경
- [ ] Claude/Codex implementation-plan agent 파일이 동일 schema 명시
- [ ] Phase 템플릿에 `**Checkpoint**: true | false (default: false; last phase implicit true)` + `**Checkpoint Reason**: <한 줄>` 추가
- [ ] foundation hint 2개가 "권장 hint" 표현으로 등장 (hard rule 표현 금지)
- [ ] mirror diff (Claude ↔ Codex) 의미적 동등

**Target Files**:
- [M] `.claude/skills/implementation-plan/SKILL.md` -- AC + Hard Rule + Phase 템플릿 + Phase gate metadata 규칙
- [M] `.codex/skills/implementation-plan/SKILL.md` -- 동일 변경 mirror
- [M] `.claude/agents/implementation-plan.md` -- 동일 schema 표현
- [M] `.codex/agents/implementation-plan.toml` -- developer_instructions 내부 동일 schema 표현

**Technical Notes**: Covers C1, I3, I4, validated by V1, V5
**Dependencies**: 없음 (Phase 1)

### Task T2: orchestrator-contract.md group-aware rules
**Component**: autopilot orchestrator contract
**Priority**: P0
**Type**: Feature

**Description**:
`.claude/skills/sdd-autopilot/references/orchestrator-contract.md`와 `.codex/...` 양쪽에 다음 변경을 동기 적용한다. (1) Review-Fix Gate 섹션을 per-phase에서 per-group으로 재기술 — `Checkpoint=true` phase 직후에만 gate 발생, 마지막 phase implicit `true`, group 내 phase는 light validation만. (2) `Execution Mode: phase-iterative ⇔ Phase Source = implementation-plan output` invariant를 명시 (feature-draft 산출물을 Phase Source로 못 쓰게). (3) multi-phase 판단 시 implementation-plan 의무 invariant 추가. (4) mid-group light validation에서 critical 발견 시 group boundary forced early로 즉시 gate 트리거 규칙. (5) final integration review의 그룹 수 기반 adaptive 처리 (1 group=group gate 겸함, 2+groups=별도 1회).

**Acceptance Criteria**:
- [ ] Review-Fix Gate 섹션이 group-scope으로 재기술되고 per-phase 표현이 제거
- [ ] phase-iterative ⇔ implementation-plan output invariant 명시
- [ ] multi-phase ⇒ implementation-plan 의무 invariant 명시
- [ ] mid-group emergency rule 명시
- [ ] final adaptive rule 명시
- [ ] mirror diff 통과

**Target Files**:
- [M] `.claude/skills/sdd-autopilot/references/orchestrator-contract.md`
- [M] `.codex/skills/sdd-autopilot/references/orchestrator-contract.md`

**Technical Notes**: Covers C2, C3, C4, C5, C6, I1, I2, validated by V2, V4
**Dependencies**: T1 (Checkpoint schema가 contract에서 인용됨)

### Task T3: sdd-autopilot SKILL.md execution rules
**Component**: autopilot SKILL execution rules
**Priority**: P0
**Type**: Feature

**Description**:
`.claude/skills/sdd-autopilot/SKILL.md`와 `.codex/...` 양쪽에 다음 변경을 동기 적용한다. (1) Step 4 reasoning rule에 "multi-phase로 판단되면 planning precedence가 implementation-plan을 의무로 포함한다" 명시 강화. (2) Step 5 verification 항목에 "phase-iterative path의 Phase Source가 implementation-plan output인가" 검증 추가. 위반 시 reject 또는 implementation-plan step 자동 삽입(self-correction). (3) Step 7.2 execution rule에서 phase 단위 gate 표현을 group 단위(`Checkpoint=true` boundary)로 교체. (4) Step 7.3 Review-Fix Loop interpretation을 per-group + final adaptive로 재기술. (5) mid-group emergency escape 표현 추가.

**Acceptance Criteria**:
- [ ] Step 4 reasoning rule에 multi-phase ⇒ implementation-plan 의무 표현 존재
- [ ] Step 5 verification에 Phase Source 출처 가드 추가
- [ ] Step 7.2/7.3에서 per-phase gate 표현 모두 per-group으로 전환
- [ ] mid-group emergency escape 명시
- [ ] mirror diff 통과

**Target Files**:
- [M] `.claude/skills/sdd-autopilot/SKILL.md`
- [M] `.codex/skills/sdd-autopilot/SKILL.md`

**Technical Notes**: Covers C2, C3, C4, C5, C6, I1, I2, validated by V2, V3
**Dependencies**: T2 (contract foundation closing 후 SKILL.md 표현 정합)

### Task T4: sample-orchestrator.md Example B + spec 표현 동기화
**Component**: autopilot sample example + global spec
**Priority**: P0
**Type**: Feature

**Description**:
`.claude/skills/sdd-autopilot/examples/sample-orchestrator.md`와 `.codex/...` 양쪽 Example B(multi-phase) Step 4를 새 디자인으로 갱신한다. per-phase gate 표기를 `Checkpoint=true` boundary에 review-fix gate를 두는 group 표기로 변경. mid-group emergency rule 표기. final integration review의 그룹 수 기반 adaptive 처리 표기. 그리고 `_sdd/spec/main.md` 라인 65/94의 "per-phase review-fix + mandatory final integration review" 표현을 group-scoped + adaptive final 표현으로 갱신한다.

**Acceptance Criteria**:
- [ ] Example B Step 4의 per-phase review-fix gate 블록이 per-group으로 갱신
- [ ] Example B에 phase별 `Checkpoint` 필드 표기 등장 (foundation phase=true, 나머지=false 또는 미명시)
- [ ] Example B에 mid-group emergency rule, final adaptive rule 표기 등장
- [ ] `_sdd/spec/main.md` 라인 65 "phase별 implementation -> review -> fix -> validation을 닫아야 하며 마지막에 final integration review를 1회 더 수행" 표현이 새 디자인에 맞게 갱신
- [ ] `_sdd/spec/main.md` 라인 94 "multi-phase quality gate" 행이 새 디자인에 맞게 갱신
- [ ] mirror diff 통과 (sample은 Claude/Codex)

**Target Files**:
- [M] `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md`
- [M] `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md`
- [M] `_sdd/spec/main.md` -- 라인 65, 94 표현 갱신 (Part 1을 spec-update-todo가 머지하도록 위임. 직접 수정은 spec-update-done 또는 spec-update-todo 단계에서)

**Technical Notes**: Covers C2, C5, C6, I1, I2, validated by V2, V4
**Dependencies**: T3 (SKILL.md execution rule이 닫힌 뒤 sample이 그것을 인용)

## Parallel Execution Summary

각 Task(T1~T4)는 sequential dependency (T1 → T2 → T3 → T4). 같은 phase 안에서는 Claude/Codex mirror pair를 동일 task로 묶었으므로 task 내부 병렬은 자동 (한 사람이 두 파일 동시에 수정해도 의미 충돌 없음 — file path가 다르고 의미 동등성만 유지).

phase 간 fan-out 없음 — 전형적 sequential plan.

## Risks and Mitigations

| Risk | 영향 | Mitigation |
|------|------|-----------|
| 기존 plan에 Checkpoint 필드 없음 → default=false로 해석되어 거대 single group으로 동작 | review depth 측면에서 새 best practice 미적용. 단 마지막 phase implicit true로 gate 1회는 보장. | 변경 적용 후 사용자 release note에 명시. retroactive migration 도구는 별도 작업으로 분리. |
| implementation-plan(opus)이 foundation 판단을 잘못해 group이 너무 커짐 | review-fix loop가 큰 finding 폭탄을 받음 | review-fix max_rounds + reasoning trace + Step 6 user checkpoint. hard limit/safety net은 도입하지 않음 (논의 합의). |
| Claude/Codex mirror drift | 두 플랫폼 동작이 어긋남 | 모든 task에 mirror diff exit criteria 포함. T6 V6 cross-cut validation으로 마지막에 한 번 더 점검. |
| Phase 3의 SKILL.md 표현이 Phase 2 contract와 어긋남 | autopilot 행동이 contract와 다르게 해석됨 | Phase 2를 단독 gate(Checkpoint=true)로 두어 contract closing 후 Phase 3 진행. |
| Codex의 reasoning_effort 정책과 mirror 의미 동등성 충돌 | Codex 쪽 표현이 Claude와 정확히 일치하지 않을 수 있음 | OQ3에 정리. mirror는 의미적 동등성 수준에서만 맞추고 reasoning_effort 표현은 Codex 그대로 유지. |

## Open Questions

- **OQ1**: mid-group emergency escape의 trigger severity. 본 draft 가정은 `critical`만. implementation 단계에서 review-fix loop의 기존 정책(`critical/high/medium` block)과 일관성을 살펴 확정.
- **OQ2**: implementation agent가 group boundary를 인지해야 하는가. 본 draft 가정은 "autopilot이 boundary 관리, implementation은 phase 단위만 인지". 운영 후 필요 시 hint 추가.
- **OQ3**: Codex의 `reasoning_effort` 라우팅도 group-aware 변경에서 같이 갱신할지. 본 draft 가정은 "기존 정책 그대로 유지, 의미적 mirror만 맞춤".
- **OQ4**: `Checkpoint Reason` 필드의 명칭/형식 — 별도 필드(`Checkpoint Reason: ...`)로 둘지, `Checkpoint: true (reason: ...)` inline으로 둘지. T1 구현 시 확정.

## Self-Containment Check

이 Part 2는 Hard Rule 10 (Self-Contained Authoring) Pass 1/2를 다음과 같이 통과시켰다.

**Pass 1 (Reference Enumeration)**:
- 외부 참조 1: `_sdd/discussion/2026-04-29_discussion_phase_grouping_review_fix_gate.md` — 본 plan의 모든 디자인 결정의 출처 토론 문서. 본 문서 Overview/Risks/Open Questions에서 inline 인용으로 grounding됨.
- 외부 참조 2: `_sdd/spec/main.md:65,94` — Part 1 Touchpoints + Part 2 Phase 4 Target Files에서 라인 번호와 변경 의도(per-phase 표현 → group-scoped + adaptive final)를 inline 명시.
- 외부 참조 3: `.claude/skills/implementation-plan/SKILL.md:24,40,176-186,226-237` 부근 — Touchpoints에서 라인 번호와 변경 항목(AC/Hard Rule/Phase 템플릿/metadata 규칙)을 inline 명시.
- 외부 참조 4: `.claude/skills/sdd-autopilot/SKILL.md:164-175,187-198,241-256,258-266` — Touchpoints에서 라인 번호와 Step 항목(Step 4/5/7.2/7.3)을 inline 명시.
- bare path만 남긴 항목 없음. 모든 참조에 "이 문서의 어떤 판단·변경과 연결되는가"가 동반됨.

**Pass 2 (Fresh-Reader Readthrough)**:
- "왜 group 단위 review-fix가 필요한가" → Overview에서 토론 문서 round 1 motivation 재진술 (review depth 부족, latency 누적, phase 부적합) — surfaced.
- "Checkpoint 필드의 의미와 default" → Part 1 Guardrail Delta + Part 2 Phase 1 description에서 default=false, 마지막 phase implicit true 둘 다 surfaced.
- "왜 multi-phase에서 implementation-plan을 의무화하는가" → Part 1 Change Summary에서 "Checkpoint 필드 owner는 implementation-plan뿐"이라는 근거 surfaced. 토론 round 9 결정 출처도 inline 인용.
- "왜 hard limit / safety net을 도입하지 않는가" → Part 1 Guardrail Delta + Part 2 Risks에서 "plan(opus) 신뢰 + max_rounds + Step 6 user checkpoint" 근거 surfaced (논의 round 6 합의 출처).
- "foundation 판단 hint 2개가 어디서 왔는가" → Part 1 Guardrail Delta + Phase 1 description에서 hint 2개를 명시하고 plan 자율 판단 + reasoning 의무라는 근거 surfaced.
- "Phase 3에서 Checkpoint=false인 이유" → Phase 3 Reason for Checkpoint에서 "sample은 illustrative라 SKILL.md correctness가 contract(Phase 2)와 일치하면 충분, 그래서 Phase 3-4를 한 group으로 묶음" 근거 surfaced.

**흔적 기록**:
- 검토 섹션 수: Part 2의 9개 섹션 (Overview, Scope, Components, Coverage, Phases, Tasks, Parallel, Risks, Open Questions)
- Pass 1 발견 갭 및 보완:
  - 초안 작성 시 일부 라인 번호가 path만 남기로 되어 있었음 → Touchpoints에서 라인 번호와 변경 항목 둘 다 명시하도록 보완.
  - Components 표의 "변경 성격" 컬럼이 too generic이었음 → C/I delta ID를 inline 인용해 grounding 보강.
- Pass 2 발견 갭 및 보완:
  - Phase 1~4의 Checkpoint=true/false 결정 근거가 처음에 없었음 → 각 phase block에 "Reason for Checkpoint" 줄을 추가해 plan 자율 판단의 trace 의무를 본 plan 자체에 적용 (meta).
  - Risks 표가 처음에 mitigation을 짧게만 적었음 → "왜 그 mitigation으로 충분한가"의 근거(논의 round 결정 출처)를 inline으로 보강.
  - OQ3 Codex 처리 방향이 처음에 implicit이었음 → "기존 정책 그대로 유지, 의미적 mirror만 맞춤"으로 explicit 가정 surfacing.
- 보완 완료: Yes
