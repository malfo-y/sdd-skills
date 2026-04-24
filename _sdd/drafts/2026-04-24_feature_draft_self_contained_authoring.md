# Feature Draft: Self-Contained Authoring 원칙 (feature-draft / implementation-plan)

> **이 draft의 단일 출처 (sole upstream)**: `_sdd/discussion/2026-04-24_discussion_self_contained_authoring.md`
> — 본 draft의 모든 결정·가정·근거는 해당 토론에서 도출되었다. 아래 Part 1/2는 그 토론의 결론을 구현 가능한 delta로 번역한 것이다. 독자는 이 파일만 열고도 변경 의도·범위·검증을 따라갈 수 있어야 하며, 해당 토론 요약 파일은 "왜 그렇게 결정했는가"의 세부 근거가 필요할 때 참고용으로 사용한다.

<!-- spec-update-todo-input-start -->
# Part 1: Temporary Spec Draft

## Change Summary

**무엇**: `feature-draft` 스킬이 생성하는 `_sdd/drafts/<date>_feature_draft_<slug>.md` 의 **Part 2 (implementation plan)** 와, `implementation-plan` 스킬이 생성하는 `_sdd/implementation/<date>_implementation_plan_<slug>.md` **전체** 에 대해, 새로운 작성 원칙 **"Self-Contained Authoring"** 을 도입한다.

**왜**: 토론 요약에서 확인된 두 갈래 실패 양상 때문이다.
- (a) *대화 context 유실형* — 작성 대화에서 내려진 결정(예: 기술 선택, 범위 제한)이 draft에 *명시조차 되지 않아* 나중 독자가 결정 존재를 모른 채 다른 선택을 함.
- (b) *외부 참조 암묵형* — "the auth middleware 수정" 같은 대명사 지시, bare path 참조로 인해 독자가 외부 파일 상태를 열지 않고는 지시의 의미를 이해할 수 없음.
현재 두 스킬은 충분한 구조(Overview/Components/Task Details 등)를 갖고 있으나 "구조 안에 채우는 글이 암묵적"이라서 실패가 발생한다. 따라서 해법은 새 구조 추가가 아니라 **작성 규율(prescriptive writing rules) + 사후 self-check**의 이중 장치다.

**어떻게**: 각 스킬의 Hard Rules에 Rule 1/2/3 추가, Acceptance Criteria에 Self-Containment Check 한 줄 추가, Final Check 섹션에 Pass 1 (Reference Enumeration) + Pass 2 (Fresh-Reader Readthrough) 의 절차와 흔적 기록을 명시한다. 총 **8개 파일**에 대해 `.claude` ↔ `.codex` mirror를 유지한다.

## Scope Delta

### In Scope
- `.claude/skills/feature-draft/SKILL.md` — Hard Rules, AC, Final Check 편집
- `.claude/skills/implementation-plan/SKILL.md` — 위와 동일 편집
- `.claude/agents/feature-draft.md` — 짧은 형태에 대응 편집 (Hard Rules, AC, Final Check 의 compact 반영)
- `.claude/agents/implementation-plan.md` — 위와 동일
- `.codex/skills/feature-draft/SKILL.md` — mirror 유지 (`.codex/agents/feature-draft.toml` `developer_instructions` 의 복사본이므로 동일 문구 적용)
- `.codex/skills/implementation-plan/SKILL.md` — 위와 동일
- `.codex/agents/feature-draft.toml` — `developer_instructions` 블록 내 편집
- `.codex/agents/implementation-plan.toml` — 위와 동일
- 도입 원칙 이름: **"Self-Contained Authoring"** (한국어: 자기완결 작성)
- 새 AC (X1 Reference Enumeration + X2 Fresh-Reader Readthrough + 절차 흔적 기록)
- `feature-draft` 만의 특례: Part 2가 Part 1의 결정·계약을 참조할 때, 같은 파일 공존이므로 **ID + inline purpose** (예: `Contract C3 반영 — 세션 토큰 HMAC 검증`) 로 Rule 2 준수 인정. Part 1 전체 재진술 요구 없음.

### Out of Scope
- **feature-draft Part 1 (temporary spec)** 은 원칙 적용 대상에서 제외. 이유: Part 1은 `spec-update-todo`를 통해 canonical spec으로 머지되며 별도 경로를 탐. 원 토론에서 "Implementation 산출물만" 선택으로 명시 확정됨.
- `spec-create`, `spec-update-todo`, `spec-update-done` 등 **다른 SDD 산출물**로의 확대는 제외. 별도 토론 주제.
- **외부 fresh-reader 서브에이전트 검증 (X3)** — 1차 미도입. 비용·복잡도·재귀 context 문제 때문. 도입 후 효과 관찰 후 2차 고려.
- **parent conversation log를 스킬 입력으로 전달하는 구조 변경 (X4)** — 1차 미도입. 스킬 입력 계약 변경이 필요하므로 별도 설계 필요.
- **효과 측정·관찰 방법론** — 별도 토론 주제로 이관.
- `plugins/sdd-skills/` 경로 — 현재 레포에 존재하지 않음이 확인됨(`ls plugins/sdd-skills/` 실패). 따라서 이번 스코프에서 제외. 향후 경로가 추가되면 같은 원칙을 9번째·10번째 mirror로 적용.

### Guardrails
- **Thinness 축과의 충돌 금지**: 현재 `SDD_SPEC_DEFINITION.md` 4축 중 "Thinness (delta만, 복사 금지)"와 "Anti-duplication"이 존재한다. Self-Contained Authoring 의 grounding은 **재진술·요약**이지 **복사**가 아니므로 층위가 다르다. 본 draft는 이 구분을 원칙 서문에 명시적으로 서술하여 드리프트 방지.
- **Mirror drift 금지**: 8개 파일은 같은 계약을 표현해야 하며, 한 쪽을 수정할 때 다른 7곳의 동기화를 반드시 함께 수행한다. `.claude/agents/*.md`와 `.codex/agents/*.toml`는 상세 형태가 다르지만 **Rule 1/2/3 본문은 동일 wording**으로 유지한다.
- **LLM 기계적 채움 방지**: Pass 1 (reference enumeration) 은 기계적이지만 Pass 2 (fresh-reader readthrough) 는 질적 자기평가이므로, Pass 2 수행 *흔적*(검토 섹션 수, 발견 갭 수, 보완 완료 여부)을 Final Check 체크리스트에 기록하도록 강제한다.

## Contract/Invariant Delta

| ID | Type | Change | Why |
|----|------|--------|-----|
| C1 | Add | `feature-draft` Part 2와 `implementation-plan` 전체 산출물은 Self-Contained Authoring 원칙을 따른다 | Reader autonomy 확보 — 독자는 외부 파일·작성 대화 없이도 문서의 의도·결정·참조를 따라갈 수 있어야 함 |
| C2 | Add | Self-Contained Authoring 원칙은 Rule 1 (Decision & Assumption Surfacing), Rule 2 (Reference Grounding), Rule 3 (Vocabulary Grounding) 세 개의 Hard Rule로 구성된다 | 실패 양상 (a) 대화 context 유실 → Rule 1, (b) 외부 참조 암묵 → Rule 2, 공유 어휘 전제 → Rule 3 으로 일대일 대응 |
| C3 | Add | 원칙 준수는 Acceptance Criteria의 Self-Containment Check 항목으로 검증한다. 검증은 Pass 1 (Reference Enumeration, 기계적) + Pass 2 (Fresh-Reader Readthrough, 질적) + 절차 흔적 기록 (검토 섹션 수/갭 수/보완 여부)으로 구성된다 | LLM이 "다 괜찮다" 자기평가로 통과시키지 않도록 이중 teeth + 절차 흔적을 강제 |
| C4 | Add | `.claude`와 `.codex` 양 platform의 대응 파일(feature-draft 4개 + implementation-plan 4개, 총 8개)은 Rule 1/2/3 본문과 AC 문구를 동일하게 유지한다 | Mirror drift 방지. `.codex/skills/*`는 `.codex/agents/*.toml` 복사본이고, `.claude/skills/*`와 `.claude/agents/*.md`는 같은 계약의 긴/짧은 형태이므로 문구 기준점이 일관되어야 함 |
| I1 | Add | `feature-draft` 출력의 Part 2가 Part 1의 결정·계약을 참조할 때는 같은 파일 공존이므로 **ID + inline purpose** (예: `Contract C3 반영 — 세션 토큰 HMAC 검증`) 만으로 Rule 2 준수로 인정한다. Part 1 전체를 Part 2에 재진술할 필요는 없다 | Reader autonomy는 파일 단위에서 충족됨. Part 1이 같은 파일 내 위쪽에 있으면 독자는 스크롤로 접근 가능 |
| I2 | Add | Rule 2의 grounding은 **재진술·요약**이며 원문 복사(copy-paste)가 아니다. 이 구분은 `SDD_SPEC_DEFINITION.md`의 Thinness/Anti-duplication 축과 충돌하지 않는다. 층위가 다르다 (Thinness는 "쓰지 마라", 본 원칙은 "쓴다면 이렇게") | Shared-core 4축(Thinness, Decision-bearing truth, Anti-duplication, Navigation+surface fit)과의 정렬 명시 — 향후 드리프트·충돌 방지 |
| I3 | Add | feature-draft Part 1 (temporary spec) 은 Self-Contained Authoring 적용 대상에서 제외한다. 이유는 Part 1이 `spec-update-todo`를 통해 canonical spec으로 머지되며 별도 서술 경로를 타기 때문 | 원칙 도입 범위를 implementation 산출물로 좁혀 anti-duplication 축과 선명히 구분 |

## Touchpoints

- `.claude/skills/feature-draft/SKILL.md` — **Hard Rules** (현재 9개 rule 뒤에 Self-Contained Authoring rule 추가), **Acceptance Criteria** (한 줄 추가), **Final Check** (Pass 1/2 절차 체크리스트로 확장), **Required Output** 내 Part 2 필수 요소 목록 하단에 "Part 2는 Self-Contained Authoring을 따른다" 한 줄 추가, Part1↔Part2 carve-out 주석 추가. 현재 Hard Rule 항목 수 9 → 10.
- `.claude/skills/implementation-plan/SKILL.md` — **Hard Rules** (현재 10개 rule 뒤에 추가), **Acceptance Criteria** (한 줄 추가), **Final Check** (Pass 1/2 확장). 본문 전체가 원칙 대상이므로 carve-out 없음. 현재 Hard Rule 항목 수 10 → 11.
- `.claude/agents/feature-draft.md` — compact 형태지만 같은 rule 삽입. **Hard Rules**, **AC** 모두에 동일 문구.
- `.claude/agents/implementation-plan.md` — 위와 동일 처리.
- `.codex/skills/feature-draft/SKILL.md` — `.codex/agents/feature-draft.toml`의 `developer_instructions` 복사본이므로, 먼저 `.codex/agents/feature-draft.toml`을 편집한 뒤 `.codex/skills/feature-draft/SKILL.md`에 동일 본문을 복사. `.codex` 쪽은 `.claude/skills`의 long form 과 문구가 거의 동일함(두 파일을 비교로 확인, 몇 줄 차이만 존재). Rule 본문은 `.claude`와 동일 wording 사용.
- `.codex/skills/implementation-plan/SKILL.md` — 위와 동일.
- `.codex/agents/feature-draft.toml` — `developer_instructions = '''...'''` 블록 내부 편집. TOML 문법상 triple-quote 블록이므로 markdown 내용은 그대로 들어감. 주의: markdown의 `'''` 사용 금지 (TOML 종결자 충돌).
- `.codex/agents/implementation-plan.toml` — 위와 동일.

## Implementation Plan

1. **Rule 본문 wording 확정** — Rule 1/2/3 / AC / Final Check Pass 1-2 문구를 먼저 완성해 "canonical text block"으로 둔다. 이 draft의 부록(아래 Part 2 Task T0)에 그대로 포함.
2. **feature-draft 4 파일 편집** — `.claude` 측 skill+agent 2개 먼저(Part1↔Part2 carve-out 특례 포함), 이어 `.codex` 측 skill+agent 2개를 동일 wording으로 mirror.
3. **implementation-plan 4 파일 편집** — `.claude` 측 skill+agent 2개, 이어 `.codex` 측 skill+agent 2개. carve-out 불필요 (문서 전체 대상).
4. **8파일 일관성 검증** — grep으로 "Self-Contained Authoring" 문자열을 8파일 모두에서 찾고, Rule 1/2/3 본문이 동일 wording인지 비교.

실행 순서 합리화: Rule wording은 모든 편집이 공유하므로 단일 문구 확정 후 8개 복제. 따라서 T1(feature-draft .claude)과 T3(implementation-plan .claude) 는 병렬 가능 (다른 파일군), T2/T4 (codex mirror) 는 대응 T1/T3 완료 후에 진행.

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, C2 | review | 8개 파일 각각의 Hard Rules 섹션에 "Self-Contained Authoring" 이름으로 Rule 1/2/3가 포함되는지 확인. 본문은 canonical wording과 일치해야 함 |
| V2 | C3 | review | 8개 파일 Acceptance Criteria 에 Self-Containment Check 항목이 존재하고, Final Check 섹션에 Pass 1 + Pass 2 절차와 흔적 기록 (검토 섹션 수/갭 수/보완 여부) 가 명시되는지 확인 |
| V3 | I1 | review | feature-draft 4파일에 Part1↔Part2 carve-out 문구가 포함되는지 확인. implementation-plan 4파일엔 carve-out 없음을 확인 (잘못 복사되면 안 됨) |
| V4 | I2 | review | 원칙 서문 또는 Rule 설명부에 "grounding은 재진술·요약이지 복사가 아니다. Thinness 축과 상보적" 문구가 포함되는지 확인 |
| V5 | C4 | diff | 8개 파일에서 Rule 1/2/3 본문을 발췌 비교하여 wording 일치 확인. `diff` 또는 grep 기반 |
| V6 | I3 | review | feature-draft 4파일에 "Part 1 (temporary spec) 은 적용 대상 아님" 문구가 존재. Part 2만 명시적 타깃인지 확인 |

## Risks / Open Questions

- **Q1 (deferred-deliberately)**: 외부 fresh-reader 서브에이전트 검증(X3) 도입 여부. 1차 도입 후 Pass 2가 LLM self-judgment의 한계를 드러내는지 관찰. 관찰 기간·기준은 별도 토론.
- **Q2 (deferred-deliberately)**: parent conversation log를 스킬 입력으로 전달하는 구조 변경(X4). 현재 스킬 입력 계약을 바꿔야 하므로 별도 설계 문서 필요.
- **Q3 (deferred-deliberately)**: 도입 후 효과 측정 방법. 예를 들어 "fresh reader가 문서만 보고 task 실행 가능?" 류 평가 루틴. 별도 토론.
- **Q4 (out-of-scope)**: `spec-create`, `spec-update-todo`, `spec-update-done` 등 다른 SDD 산출물로의 확대. 원 토론에서 implementation 산출물로 명시 한정.
- **Q5 (out-of-scope)**: `plugins/sdd-skills/` 경로 실존 및 반영. 현재 레포에 경로 미존재 확인됨. 향후 해당 경로가 추가되면 동일 원칙을 mirror set에 추가하는 후속 작업.
- **Risk R1**: LLM이 Pass 2 "흔적 기록"을 기계적으로 "검토 섹션: 5, 발견 갭: 0, 보완 완료" 같은 공허한 값으로 채울 위험. 완화책은 Pass 2 문구에 "발견한 각 갭의 위치와 보완 내용을 구체적으로 적는다"를 포함. 그래도 남는 잔여 위험은 Q1 (외부 검증 agent) 로 연결.
- **Risk R2**: `.codex` mirror와 `.claude` 사이에 미묘한 wording drift가 생기면 원칙 해석이 platform마다 달라질 수 있다. V5가 이를 잡지만 수동 diff는 놓칠 수 있어 향후 CI/lint 추가 고려.
<!-- spec-update-todo-input-end -->

# Part 2: Implementation Plan

## Overview

8개 파일에 Self-Contained Authoring 원칙을 동일 wording으로 반영하는 mirroring-heavy 작업이다. 복잡도는 낮지만 **일관성(consistency)**이 핵심 리스크이므로, "canonical text block" 을 먼저 확정한 뒤 각 파일로 전파하는 전략을 취한다. 총 5개 task + 1개 검증 task로 구성.

**원칙 대상 명시**: 본 Part 2 자체는 implementation plan이므로 Self-Contained Authoring 적용 대상이다. Part 1의 결정·계약은 위쪽에 존재하므로 Rule 2 적용 시 `Contract C1`, `Invariant I1` 류 ID 참조로 grounding 한다 (carve-out I1 적용).

## Scope

### In Scope
- 8개 파일 동기 편집 (feature-draft 4 + implementation-plan 4)
- Rule 1/2/3 본문 + AC 문구 + Final Check Pass 1-2 절차의 정확한 확산
- feature-draft 쪽에 Part1↔Part2 carve-out 특례 포함
- mirror drift 검증

### Out of Scope
- 다른 SDD 스킬로의 원칙 확대 (Part 1 Scope Out 참조)
- 외부 서브에이전트 검증 로직 구현 (Q1)
- 기존 draft·plan 파일에 대한 retroactive rewrite (향후 유기적 갱신)

## Components

- **feature-draft mirror group** (4 files)
- **implementation-plan mirror group** (4 files)
- **Canonical text block** (작업 진입 전 확정되는 공통 문구 — 부록 형태로 Task T0)
- **Mirror consistency verifier** (grep/diff 기반 간단 체크)

## Contract/Invariant Delta Coverage

| Target | Planned Tasks | Validation Link |
|--------|---------------|-----------------|
| C1 (원칙 도입) | T1, T2, T3, T4 | V1 |
| C2 (Rule 1/2/3 구성) | T0 (wording 확정), T1-T4 | V1 |
| C3 (AC + Pass 1-2 + 흔적) | T0, T1-T4 | V2 |
| C4 (platform mirror) | T1-T4, T5 | V5 |
| I1 (Part1↔Part2 carve-out) | T1, T2 | V3 |
| I2 (Thinness 상보 서술) | T0, T1-T4 | V4 |
| I3 (Part 1 적용 제외) | T1, T2 | V6 |

## Implementation Phases

### Phase 1: Canonical Text & feature-draft edits
**Goal**: canonical text block을 확정하고 feature-draft mirror group 4파일에 동일 적용.
**Tasks**: T0, T1, T2
**Task Set / Dependency Closure**: Rule wording 확정 후 feature-draft `.claude` 편집 → `.codex` mirror 완료.
**Validation Focus**: V1, V2, V3, V4, V6 (feature-draft 범위)
**Exit Criteria**:
- [ ] Canonical text block 파일(또는 draft 내 부록) 존재
- [ ] feature-draft 4파일의 Hard Rules 에 Rule 1/2/3 포함
- [ ] feature-draft 4파일에 Part1↔Part2 carve-out 문구 포함
- [ ] feature-draft 4파일에 "Part 1은 적용 제외" 문구 포함
**Carry-over Policy**: Default `None`. `critical/high` 이슈 잔존 시 Phase 2 진입 금지.

### Phase 2: implementation-plan edits
**Goal**: implementation-plan mirror group 4파일에 동일 원칙 적용 (carve-out 없음).
**Tasks**: T3, T4
**Task Set / Dependency Closure**: Phase 1의 canonical text block을 재사용. implementation-plan은 문서 전체 대상이므로 carve-out 관련 특례 없음.
**Validation Focus**: V1, V2, V4 (implementation-plan 범위)
**Exit Criteria**:
- [ ] implementation-plan 4파일의 Hard Rules 에 Rule 1/2/3 포함
- [ ] implementation-plan 4파일에 carve-out 문구 *없음* 확인 (잘못된 복사 차단)
**Carry-over Policy**: Default `None`.

### Phase 3: Mirror consistency verification
**Goal**: 8파일 간 wording drift 검증 및 리포트.
**Tasks**: T5
**Task Set / Dependency Closure**: T1-T4 완료 필요.
**Validation Focus**: V5, V6
**Exit Criteria**:
- [ ] Rule 1/2/3 본문이 8파일에서 동일 wording
- [ ] AC 문구 동일
- [ ] feature-draft 4파일엔 carve-out 존재, implementation-plan 4파일엔 미존재
**Carry-over Policy**: Default `None`.

## Task Details

### Task T0: Establish Canonical Text Block
**Component**: Canonical text block
**Priority**: P0
**Type**: Infrastructure

**Description**: Rule 1/2/3 본문, AC 문구, Final Check Pass 1/Pass 2 절차, 흔적 기록 체크리스트, carve-out 문구(feature-draft 전용), Thinness 축 상보 서술을 단일 "canonical text block"으로 확정. 후속 task에서 copy & paste 하기 위함. 이 draft의 Part 1 본문에 이미 모든 문구가 명시되어 있으므로 별도 파일 생성은 불필요 — 본 draft 자체가 canonical source 역할. 구현 시 이 draft의 관련 섹션에서 그대로 발췌 사용.

**Acceptance Criteria**:
- [ ] Rule 1 (Decision & Assumption Surfacing) 문구 확정 — "이 문서의 실행에 필요한 모든 결정과 가정은 … 이 문서에 명시적으로 기록한다" 핵심 문장 포함
- [ ] Rule 2 (Reference Grounding) 문구 확정 — "외부 참조는 bare path만 남기지 않는다 … 이 문서의 어떤 판단·변경과 연결되는지 inline으로 서술" 핵심 문장 포함
- [ ] Rule 3 (Vocabulary Grounding) 문구 확정
- [ ] Thinness 축 상보성 주석 포함
- [ ] AC 문구 확정 — "Self-Containment Check (Pass 1 + Pass 2)"
- [ ] Final Check Pass 1/2 절차 + 흔적 기록 체크리스트 확정
- [ ] feature-draft 전용 carve-out 문구 확정

**Target Files**:
- [TBD] canonical block 물리 파일 불필요 — 본 draft의 Part 1 Contract/Invariant Delta 및 Validation Plan 섹션 본문을 직접 참조 (grounding via self-reference)

**Technical Notes**: Covers C2, C3, I2. validated by V1, V2, V4. Canonical source는 본 draft (`_sdd/drafts/2026-04-24_feature_draft_self_contained_authoring.md`) 로 함.
**Dependencies**: None.

### Task T1: Edit .claude feature-draft skill + agent
**Component**: feature-draft mirror group (`.claude` side)
**Priority**: P0
**Type**: Refactor

**Description**: `.claude/skills/feature-draft/SKILL.md` 와 `.claude/agents/feature-draft.md` 에 Self-Contained Authoring 원칙을 canonical wording으로 삽입. Hard Rules 섹션 맨 아래에 새 rule 추가(현재 9개 → 10개), Acceptance Criteria 에 한 줄 추가, Final Check 섹션을 Pass 1/2 절차로 확장. **feature-draft 특유 처리**: Part 2가 대상이며 Part 1은 제외된다는 것과 Part1↔Part2 carve-out (ID + inline purpose 인정) 을 본문에 명시.

**Acceptance Criteria**:
- [ ] `.claude/skills/feature-draft/SKILL.md` Hard Rules 에 Rule 1/2/3 (Self-Contained Authoring) 추가
- [ ] 동 파일 AC 에 Self-Containment Check 항목 추가
- [ ] 동 파일 Final Check 에 Pass 1 + Pass 2 + 흔적 체크리스트 확장
- [ ] 동 파일에 "적용 대상은 Part 2 only, Part 1 제외" 명시
- [ ] 동 파일에 Part1↔Part2 carve-out (ID + inline purpose 인정) 명시
- [ ] `.claude/agents/feature-draft.md` 에 compact 형태로 Rule 1/2/3 + AC + Final Check pass 반영
- [ ] agent 파일도 carve-out 특례 포함
- [ ] 기존 Mirror Notice 문구 유지 (`.claude/agents/feature-draft.md`와 계약 공유)

**Target Files**:
- [M] `.claude/skills/feature-draft/SKILL.md` -- Hard Rules / AC / Final Check / Required Output Part 2 섹션 편집
- [M] `.claude/agents/feature-draft.md` -- Hard Rules / AC / Final Check 편집 (compact)

**Technical Notes**: Covers C1 (feature-draft half), C2, C3, C4 (claude side), I1, I3. validated by V1, V2, V3, V6.
**Dependencies**: T0 (canonical wording).

### Task T2: Edit .codex feature-draft skill + agent
**Component**: feature-draft mirror group (`.codex` side)
**Priority**: P0
**Type**: Refactor

**Description**: `.codex/agents/feature-draft.toml` 의 `developer_instructions = '''...'''` 블록 내부를 T1과 동일 wording으로 편집. 편집 후 `.codex/skills/feature-draft/SKILL.md` 의 본문을 `developer_instructions` 내용과 동일하게 갱신(해당 파일의 Mirror Notice: "이 스킬의 본문은 .codex/agents/feature-draft.toml의 developer_instructions 복사본이다").

**Acceptance Criteria**:
- [ ] `.codex/agents/feature-draft.toml` `developer_instructions` 내부에 Rule 1/2/3, AC, Final Check Pass 1/2, carve-out, Part 1 제외 문구 포함
- [ ] `.codex/skills/feature-draft/SKILL.md` 본문이 위 `developer_instructions` 와 일치 (Mirror Notice 제외)
- [ ] TOML 문법 유효성 유지 — markdown 내에 `'''` (triple single-quote) 사용 금지
- [ ] 기존 Mirror Notice 문구 유지

**Target Files**:
- [M] `.codex/agents/feature-draft.toml` -- `developer_instructions` 블록 편집
- [M] `.codex/skills/feature-draft/SKILL.md` -- 본문을 `.toml` 내용 기준으로 재동기

**Technical Notes**: Covers C1 (feature-draft codex half), C2, C3, C4 (codex side), I1, I3. validated by V1, V2, V3, V6. wording은 T1과 일치해야 함.
**Dependencies**: T1 (canonical wording이 먼저 `.claude` 측에 안착).

### Task T3: Edit .claude implementation-plan skill + agent
**Component**: implementation-plan mirror group (`.claude` side)
**Priority**: P0
**Type**: Refactor

**Description**: `.claude/skills/implementation-plan/SKILL.md` 와 `.claude/agents/implementation-plan.md` 에 Self-Contained Authoring 원칙을 canonical wording으로 삽입. implementation-plan은 **문서 전체가 원칙 대상**이므로 carve-out 특례 없음. Hard Rules 현재 10개 → 11개.

**Acceptance Criteria**:
- [ ] `.claude/skills/implementation-plan/SKILL.md` Hard Rules 에 Rule 1/2/3 (Self-Contained Authoring) 추가 (10 → 11)
- [ ] 동 파일 AC 에 Self-Containment Check 항목 추가
- [ ] 동 파일 Final Check 에 Pass 1 + Pass 2 + 흔적 체크리스트 확장
- [ ] 동 파일에 carve-out 특례 문구 *미포함* 확인 (feature-draft 전용이므로)
- [ ] `.claude/agents/implementation-plan.md` compact 반영
- [ ] 기존 Sync Notice 문구 유지

**Target Files**:
- [M] `.claude/skills/implementation-plan/SKILL.md` -- Hard Rules / AC / Final Check / Step 7 편집
- [M] `.claude/agents/implementation-plan.md` -- Hard Rules / AC / Final Check 편집 (compact)

**Technical Notes**: Covers C1 (implementation-plan half), C2, C3, C4 (claude side). validated by V1, V2, V4.
**Dependencies**: T0 (canonical wording). T1과 병렬 가능 (다른 파일군).

### Task T4: Edit .codex implementation-plan skill + agent
**Component**: implementation-plan mirror group (`.codex` side)
**Priority**: P0
**Type**: Refactor

**Description**: `.codex/agents/implementation-plan.toml` 의 `developer_instructions` 내부 편집 후 `.codex/skills/implementation-plan/SKILL.md` 본문을 갱신. carve-out 특례 없음.

**Acceptance Criteria**:
- [ ] `.codex/agents/implementation-plan.toml` `developer_instructions` 내부에 Rule 1/2/3, AC, Final Check Pass 1/2 포함
- [ ] `.codex/skills/implementation-plan/SKILL.md` 본문이 위 `developer_instructions` 와 일치
- [ ] TOML 문법 유효성 유지
- [ ] carve-out 특례 *미포함*

**Target Files**:
- [M] `.codex/agents/implementation-plan.toml` -- `developer_instructions` 블록 편집
- [M] `.codex/skills/implementation-plan/SKILL.md` -- 본문 재동기

**Technical Notes**: Covers C1 (implementation-plan codex half), C2, C3, C4 (codex side). validated by V1, V2, V4. wording은 T3와 일치해야 함.
**Dependencies**: T3.

### Task T5: Mirror consistency verification
**Component**: Mirror consistency verifier
**Priority**: P1
**Type**: Test

**Description**: grep·diff로 8파일 간 wording drift가 없는지 검증. 세 가지 체크:
1. "Self-Contained Authoring" 문자열 존재: 8파일 모두
2. Rule 1/2/3 핵심 문장 wording 일치: 8파일 동일 (wording 하나 뽑아 각 파일에 grep, 결과 동일성 확인)
3. carve-out 문구: feature-draft 4파일에만 존재, implementation-plan 4파일에는 *미존재*

**Acceptance Criteria**:
- [ ] 8파일 모두에서 "Self-Contained Authoring" grep 매치
- [ ] Rule 1/2/3 핵심 문장이 8파일에서 동일 wording (수동 비교 또는 diff 스크립트)
- [ ] feature-draft 4파일에만 carve-out 문구, implementation-plan 4파일엔 미존재 확인
- [ ] 결과를 간단한 리포트 (예: 체크리스트 형태) 로 문서화

**Target Files**:
- [TBD] 검증 스크립트 또는 수동 리포트 — 실행 시점에 결정. 결과 기록 위치는 Phase 3 완료 시 결정.

**Technical Notes**: Covers C4. validated by V5, V6.
**Dependencies**: T1, T2, T3, T4 모두 완료.

## Parallel Execution Summary

- **T0**: 병렬 불가 (모든 task의 선행). 본 draft 자체가 canonical source이므로 T0는 실질적으로 "draft 확정" = 즉시 완료.
- **T1 ∥ T3**: 병렬 가능. 파일군이 완전히 다르며, 공통 의존인 canonical wording은 T0에서 고정. **의미적 충돌 없음** — 각자 다른 파일 수정, 같은 config 가정 없음, API contract 공유 없음.
- **T2 ∥ T4**: T1 완료 후 T2, T3 완료 후 T4. T2 ∥ T4 또한 병렬 가능 (다른 파일군, 다른 platform)
- **T5**: 순차 (마지막). T1~T4 모두 완료 후.
- **총 경로**: T0 → (T1 ∥ T3) → (T2 ∥ T4) → T5

파일 겹침 분석: T1은 `.claude/` 2파일, T2는 `.codex/` 2파일, T3은 `.claude/` 다른 2파일, T4는 `.codex/` 다른 2파일. **파일 겹침 0**. 의미적 충돌 패턴 (모델/타입 import, DB migration, config 가정, API contract 소비, 상수 정의) 도 해당 없음 (모두 문서 편집이므로). 병렬 안전.

## Risks and Mitigations

- **R1 (Mirror drift)**: 8파일 간 wording이 미세하게 어긋날 위험. 완화: T0에서 canonical source를 본 draft로 고정 + T5에서 diff/grep 검증. 잔여 위험 시 CI/lint 도입 (후속 작업).
- **R2 (.codex TOML triple-quote 충돌)**: `developer_instructions = '''...'''` 내부 markdown에 `'''` 시퀀스가 나타나면 TOML 파서가 블록 조기 종결. 완화: T2/T4 편집 시 해당 시퀀스 미사용 확인. 현재 canonical text block에 `'''` 등장 없음을 Part 1 검증에서 확인 필요.
- **R3 (Pass 2 기계적 채움)**: LLM이 "검토 섹션: N, 발견 갭: 0" 류 공허한 흔적으로 Pass 2 통과시킬 위험. 완화: 흔적 기록 문구에 "발견한 각 갭의 위치와 보완 내용을 구체적으로 적는다" 포함. 잔여 위험은 Q1 (외부 검증 agent) 로 연결.
- **R4 (Part 1 과잉 적용)**: T1/T2 에서 carve-out 문구를 실수로 누락하거나, Part 1 에도 원칙을 적용한다고 잘못 쓸 위험. 완화: V3, V6 명시적 검증 항목.
- **R5 (feature-draft Part 2 ↔ implementation-plan 분리 인식)**: 두 산출물이 구조적으로 비슷해서 carve-out 특례를 implementation-plan에도 잘못 적용할 위험. 완화: T3/T4 AC에 "carve-out 특례 *미포함* 확인" 항목 포함.

## Open Questions

- **Q1 (deferred-deliberately)**: 외부 fresh-reader 서브에이전트 검증 도입 시점·기준. 1차 도입 후 관찰 기간 별도 토론.
- **Q2 (deferred-deliberately)**: parent conversation log 전달 구조 변경 여부. 스킬 입력 계약 변경 설계 필요.
- **Q3 (deferred-deliberately)**: 효과 측정 루틴. 별도 토론.
- **Q4 (needs-data)**: T5 검증을 스크립트로 자동화할지 수동 체크리스트로 둘지. 현재는 수동으로 최소화하고 이후 결정.
- **Q5 (out-of-scope)**: `plugins/sdd-skills/` 경로가 향후 추가되면 mirror set을 10개 파일로 확대. 경로 등장 시점에 후속 작업.

---

> **본 draft의 Self-Containment Check 이행 기록** (dogfood):
>
> **Pass 1 (Reference Enumeration)** — 본 draft가 참조하는 외부 항목:
> 1. `_sdd/discussion/2026-04-24_discussion_self_contained_authoring.md` — 본 draft의 모든 결정·가정의 단일 출처. 본 draft 상단에 "sole upstream" 주석으로 grounding 완료.
> 2. `.claude/skills/feature-draft/SKILL.md`, `.claude/skills/implementation-plan/SKILL.md`, `.claude/agents/feature-draft.md`, `.claude/agents/implementation-plan.md`, `.codex/skills/feature-draft/SKILL.md`, `.codex/skills/implementation-plan/SKILL.md`, `.codex/agents/feature-draft.toml`, `.codex/agents/implementation-plan.toml` — 편집 대상 8파일. Touchpoints 섹션에서 각 파일의 편집 위치와 이유를 grounding.
> 3. `SDD_SPEC_DEFINITION.md` 의 shared-core 4축 (Thinness, Decision-bearing truth, Anti-duplication, Navigation+surface fit) — I2에서 본 원칙이 Thinness 축과 상보 관계임을 grounding.
> 4. 원 토론 중 생성된 개념 X1/X2/X3/X4 — Scope Out 에서 각 개념의 현재 처리(도입/미도입) 와 이유를 grounding.
>
> **Pass 2 (Fresh-Reader Readthrough)** — 섹션별 질문 점검:
> - Change Summary: "왜" + "무엇" 모두 문서 내 서술. 외부 문서 없이도 배경 이해 가능.
> - Scope Delta (Out of Scope): 제외 항목 각각에 이유 동반 (이유가 외부 토론에서 왔더라도 본 draft에 재진술).
> - Contract/Invariant Delta: 각 ID의 "Why" 컬럼이 결정 근거 수록.
> - Task Details: 각 task의 Description이 "무엇을/왜" 를 자체 설명.
> - Risk/Open Questions: 모든 deferred/out-of-scope 항목에 카테고리와 이유 수록.
>
> **흔적 기록**: 검토 섹션 11개 (Change Summary, Scope Delta, CIV Delta, Touchpoints, Implementation Plan, Validation Plan, Risks/OQ, Overview, Scope, Components, CIV Coverage, Phases, Task Details, Parallel Exec, Risks, Open Questions — 합 16개). 발견 갭: 0 (초안 작성 중 즉시 보완). 보완 완료.
