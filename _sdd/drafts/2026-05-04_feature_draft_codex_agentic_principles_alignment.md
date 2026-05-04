# Feature Draft: Codex skills agentic principles alignment

<!-- spec-update-todo-input-start -->
# Part 1: Temporary Spec Draft

## Change Summary

`.claude/skills`에 최근 반영된 `docs/agentic_coding_principle.md` 기반 수정사항을 `.codex/skills`와 `.codex/agents`에도 적용한다.

핵심 변경은 다음 4가지다.

- `feature-draft`: `.claude/skills/feature-draft` 2.3.0의 Open Questions schema, Surface Key Decisions, Minimum-Code Mandate를 Codex 진입점에도 반영한다.
- `implementation-plan`: plan task가 요청되지 않은 옵션, 설정, 추상화, 도달 불가 에러 처리를 명세하지 않도록 Min-Code self-check를 추가한다.
- `implementation`: sub-agent prompt와 phase review가 AC 외 사변적 코드 생성을 막고 드러내도록 강화한다.
- `implementation-review`: Speculative Code를 명시 리뷰 축으로 추가하고, recommendations 자체도 Min-Code 원칙을 따르게 한다.

근거: `docs/agentic_coding_principle.md`의 Simplicity First, Think Before Coding, Goal-Driven Execution 원칙을 Codex skill chain에도 동일하게 적용해야 direct skill 호출과 internal agent 호출이 같은 계약으로 동작한다.

## Scope Delta

**In Scope**

- `.codex/skills/feature-draft/SKILL.md`와 `.codex/agents/feature-draft.toml`
- `.codex/skills/implementation-plan/SKILL.md`와 `.codex/agents/implementation-plan.toml`
- `.codex/skills/implementation/SKILL.md`와 `.codex/agents/implementation.toml`
- `.codex/skills/implementation-review/SKILL.md`와 `.codex/agents/implementation-review.toml`

**Out of Scope**

- `.claude/*` 파일 재수정. 이미 source reference로 사용하며 이번 변경 대상은 아니다.
- `spec-update-todo`, `spec-update-done`, `spec-review` 등 spec mutation/review 계열의 별도 Min-Code 적용. 역할별 분석이 필요해 후속 범위로 둔다.
- `skill.json` metadata 변경. 이번 변경은 실행 계약 본문 중심이며 skill discovery metadata는 변경하지 않는다.
- 실제 dogfooding 실행. 수정 후 별도 implementation-review 또는 smoke invocation으로 검증한다.

**Guardrail Delta**

- Codex 쪽의 기존 추가 규칙은 보존한다: `spec-update-todo-input-start/end` marker, thin global spec 상태에서도 code exploration을 생략하지 않는 규칙, lowercase decision log + legacy uppercase fallback.
- 각 skill의 public `SKILL.md`와 internal `.codex/agents/*.toml` `developer_instructions`는 같은 본문 계약을 유지한다. 차이는 TOML wrapper와 Mirror Notice 표현에만 허용한다.

## Contract/Invariant Delta

| ID | Type | Change | Why |
|----|------|--------|-----|
| C1 | Add | `feature-draft`가 Risks / Open Questions 4필드 스키마를 사용한다: Decision taken, Alternatives considered, Confidence, User confirmation needed | Think Before Coding 원칙을 문서화하고 silent assumption을 막는다 |
| C2 | Add | `feature-draft` Part 2 task에 Minimum-Code Mandate를 추가한다 | 계획 단계에서 요청되지 않은 옵션, 설정, 추상화, 에러 처리가 downstream으로 전파되는 것을 막는다 |
| C3 | Add | `implementation-plan` task description, AC, Technical Notes에 Minimum-Code Mandate와 self-check를 추가한다 | feature draft 이후 plan 확장 단계에서도 Simplicity First를 유지한다 |
| C4 | Add | `implementation` hard rules, sub-agent prompt, phase review에 Minimum-Code / Speculative Code 검사를 추가한다 | 실행 단계에서 AC 밖 코드 생성을 막고 phase 단위로 드러낸다 |
| C5 | Add | `implementation-review` assessment/finding 기준에 Speculative Code와 Recommendations Min-Code를 추가한다 | review 단계가 사변적 복잡도를 결함으로 분류하고 권고로 재도입하지 않게 한다 |
| C6 | Add | `feature-draft`, `implementation-plan`, `implementation`이 LOW confidence 또는 사용자 확인 필요 결정을 채팅에 surface한다 | 장문 artifact 안에 중요한 결정이 묻히는 것을 방지한다 |
| I1 | Modify | `.codex/skills/*/SKILL.md`와 `.codex/agents/*.toml`의 mirror contract를 동시 갱신한다 | direct invocation과 internal agent invocation의 drift를 막는다 |
| I2 | Preserve | Codex-specific marker/code-exploration 규칙은 유지한다 | `.claude` 변경을 무비판 복사하지 않고 Codex consumer contract를 보존한다 |

## Touchpoints

| 파일 | 변경 영역 | 이유 |
|------|----------|------|
| `.codex/skills/feature-draft/SKILL.md` | version, AC, Hard Rules 4/5/10/11, Required Output, Part 1/2 templates, Step 3/4/5/6/7, Step 8 신규, Error Handling | `feature-draft` 자체에 agentic coding principles 적용 |
| `.codex/agents/feature-draft.toml` | `developer_instructions` 내 동일 본문 | internal agent mirror 유지 |
| `.codex/skills/implementation-plan/SKILL.md` | AC, Hard Rules 2/10/12, Step 4 self-check, Open Questions schema, Step 8, Error Handling | plan 단계 Min-Code + decision surfacing |
| `.codex/agents/implementation-plan.toml` | `developer_instructions` 내 동일 본문 | internal agent mirror 유지 |
| `.codex/skills/implementation/SKILL.md` | AC, Hard Rules, Step 1 Surface Plan Assumptions, Sub-agent prompt, Phase Review, Surface Phase Surprises | execution 단계 Min-Code enforcement |
| `.codex/agents/implementation.toml` | `developer_instructions` 내 동일 본문 | internal agent mirror 유지 |
| `.codex/skills/implementation-review/SKILL.md` | AC, Hard Rules, Step 5 Assessment, Step 6 Findings, Output Format Recommendations | review 단계 Speculative Code 검사 |
| `.codex/agents/implementation-review.toml` | `developer_instructions` 내 동일 본문 | internal agent mirror 유지 |

## Implementation Plan

1. `feature-draft` pair를 먼저 갱신한다. 이 pair는 downstream skill들이 참조할 패턴 source가 된다.
2. `implementation-plan`, `implementation`, `implementation-review` 3개 pair를 같은 원칙으로 갱신한다.
3. 전체 pair mirror 검증을 수행한다.

Codex-specific 보존 결정 때문에 `.claude` 본문을 단순 복사하지 않는다. 대신 `.claude`의 원칙 적용 문구를 기준으로 Codex 기존 계약에 surgical merge한다.

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, C2, C6 | review | `feature-draft`에 4필드 Open Q schema, Minimum-Code Mandate, Step 8 Surface가 있고 marker/code exploration 규칙이 유지됨 |
| V2 | C3, C6 | review | `implementation-plan`에 Hard Rule 12, task self-check, Open Q schema, Step 8 Surface가 있음 |
| V3 | C4, C6 | review | `implementation`에 Minimum-Code hard rule, sub-agent prompt rule, Speculative Code phase review, Surface Plan/Surprises가 있음 |
| V4 | C5 | review | `implementation-review`에 Speculative Code assessment/finding, escalation, Recommendations Min-Code가 있음 |
| V5 | I1 | test | skill/agent pair별 본문 동기화 확인. TOML wrapper와 Mirror Notice 외 의미 차이가 없어야 함 |
| V6 | I2 | review | `feature-draft` output marker, thin spec code exploration, lowercase decision log fallback 규칙이 삭제되지 않음 |

## Risks / Open Questions

### Q1. `.claude/skills/feature-draft` 2.3.0을 Codex에 그대로 복사할지, Codex-specific 규칙을 보존할지

- **Decision taken**: Codex-specific 규칙을 보존하고 `.claude` 변경을 surgical merge한다.
- **Alternatives considered**: `.claude` 본문을 그대로 복사하면 빠르지만 `spec-update-todo` marker와 thin-spec code exploration 규칙이 사라질 수 있어 기각한다.
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q2. `feature-draft` 외 implementation chain까지 이번 명세에 포함할지

- **Decision taken**: 포함한다. `.claude` 최근 변경은 feature draft 하나가 아니라 plan -> implement -> review enforcement loop를 닫는 변경이기 때문이다.
- **Alternatives considered**: `feature-draft`만 먼저 적용하는 방안은 작지만, downstream에서 Min-Code가 빠져 동일 문제가 재발할 수 있어 기각한다.
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q3. `skill.json` version도 함께 올릴지

- **Decision taken**: 이번 draft에서는 제외한다. 현재 변경 대상은 실행 계약 본문이고, 기존 `.claude` implementation-chain 변경도 frontmatter version을 일괄 갱신하지 않았다.
- **Alternatives considered**: 모든 `skill.json` version bump를 포함할 수 있지만 discovery metadata 정책 확인 없이 바꾸면 scope가 커져 보류한다.
- **Confidence**: MEDIUM
- **User confirmation needed**: Yes

<!-- spec-update-todo-input-end -->

# Part 2: Implementation Plan

## Overview

이 plan은 `.codex` skill chain에 `docs/agentic_coding_principle.md` 기반 enforcement를 이식한다. 변경은 문서 계약 수정이며 런타임 코드는 없다. 따라서 검증은 구조적 review와 mirror parity 확인 중심이다.

핵심 적용 패턴:

- Open Questions는 best-effort decision + alternatives + confidence + user confirmation schema로 작성한다.
- Minimum-Code Mandate는 task description/AC/Technical Notes 또는 sub-agent output에 적용한다.
- Speculative Code는 review 단계에서 중간 이상 severity로 분류한다.
- 중요한 낮은 확신 결정은 artifact 안에만 두지 않고 채팅에 surface한다.

## Scope

### In Scope

- 4개 public skill entrypoint 갱신
- 4개 internal Codex agent mirror 갱신
- Codex-specific feature-draft behavior 보존
- pair mirror 검증

### Out of Scope

- `.claude` 파일 변경
- spec mutation skill군 확장 적용
- dogfooding 실행
- `skill.json` metadata 갱신

## Components

| Component | Files |
|-----------|-------|
| feature-draft pair | `.codex/skills/feature-draft/SKILL.md`, `.codex/agents/feature-draft.toml` |
| implementation-plan pair | `.codex/skills/implementation-plan/SKILL.md`, `.codex/agents/implementation-plan.toml` |
| implementation pair | `.codex/skills/implementation/SKILL.md`, `.codex/agents/implementation.toml` |
| implementation-review pair | `.codex/skills/implementation-review/SKILL.md`, `.codex/agents/implementation-review.toml` |

## Contract/Invariant Delta Coverage

| Target | Planned Tasks | Validation Link |
|--------|---------------|-----------------|
| C1, C2, C6, I2 | T1 | V1, V6 |
| C3, C6 | T2 | V2 |
| C4, C6 | T3 | V3 |
| C5 | T4 | V4 |
| I1 | T1, T2, T3, T4 | V5 |

## Implementation Phases

### Phase 1: Codex feature-draft pattern source 갱신

**Goal**: Codex `feature-draft`에 `.claude` 2.3.0 원칙을 적용하되 Codex-specific marker/code exploration contract를 보존한다.

**Tasks**: T1

**Task Set / Dependency Closure**: T1이 downstream task의 문구 패턴 source를 확정한다.

**Validation Focus**: V1, V6

**Exit Criteria**:
- [ ] T1 완료
- [ ] `feature-draft` pair에서 marker, code exploration, Minimum-Code, Open Q schema, Step 8이 모두 공존

**Carry-over Policy**:
- Default: `None` (`critical/high/medium` block)
- Allowed Exception: 없음

**Checkpoint**: true

**Checkpoint Reason**: 후속 3개 pair가 feature-draft 문구 패턴을 참조한다.

### Phase 2: Codex implementation chain 갱신

**Goal**: implementation-plan -> implementation -> implementation-review 3개 pair에 plan/execute/review enforcement loop를 적용한다.

**Tasks**: T2, T3, T4

**Task Set / Dependency Closure**: T2/T3/T4는 파일이 분리되어 병렬 가능하지만, 최종 mirror parity 검증은 세 task 이후 수행한다.

**Validation Focus**: V2, V3, V4, V5

**Exit Criteria**:
- [ ] T2, T3, T4 완료
- [ ] 4개 Codex skill/agent pair mirror 검증 통과
- [ ] `rg`로 Minimum-Code, Speculative Code, Decision taken, User confirmation needed 문구가 target files에 기대 위치로 확인됨

**Carry-over Policy**:
- Default: `None` (`critical/high/medium` block)
- Allowed Exception: 없음

**Checkpoint**: true

**Checkpoint Reason**: 마지막 phase이며 mirror parity와 chain consistency를 닫아야 한다.

## Task Details

### Task T1: Codex feature-draft에 2.3.0 원칙을 surgical merge

**Component**: feature-draft pair
**Priority**: P0
**Type**: Improvement

**Description**: `.claude/skills/feature-draft` 2.3.0에서 도입된 Open Questions schema, Surface Key Decisions, Minimum-Code Mandate를 `.codex` feature-draft pair에 반영한다. Codex 기존 계약인 `spec-update-todo-input-start/end` marker, thin global spec 상태의 code exploration, lowercase `decision_log.md` + legacy uppercase fallback은 유지한다.

**Non-Goals**: `.claude` feature-draft와 byte-identical하게 만들지 않는다. Codex-specific consumer contract 보존이 우선이다.

**Acceptance Criteria**:
- [ ] `version`을 `2.3.0`으로 갱신한다.
- [ ] AC에 Open Questions 4필드 schema와 Part 2 Minimum-Code 항목을 추가한다.
- [ ] Hard Rule 4를 best-effort decision + 4필드 schema + Step 8 surface 방식으로 교체한다.
- [ ] 여러 기능 통합/분리 판단은 Alternatives에 기록하도록 Hard Rule을 보강한다.
- [ ] Self-Contained Authoring은 압축형 Rule로 정리하되 Pass 1/2 흔적 기록 요구를 유지한다.
- [ ] Minimum-Code Mandate를 별도 Hard Rule로 추가한다.
- [ ] Required Output은 기존 `spec-update-todo-input-start/end` marker를 유지한다.
- [ ] Part 1 `Risks / Open Questions` schema 예시를 추가한다.
- [ ] Part 2 task template에 필요한 경우만 쓰는 `Non-Goals` 필드를 추가한다.
- [ ] Step 6에 Minimum-Code self-check 3문항을 추가한다.
- [ ] Step 8 `Surface Key Decisions to User`를 추가한다.
- [ ] Error Handling의 모호한 요청/여러 기능 대응이 4필드 schema 기록 방식으로 바뀐다.
- [ ] `.codex/skills/feature-draft/SKILL.md`와 `.codex/agents/feature-draft.toml`의 `developer_instructions`가 의미상 동일하다.

**Target Files**:
- [M] `.codex/skills/feature-draft/SKILL.md`
- [M] `.codex/agents/feature-draft.toml`

**Technical Notes**: Covers C1, C2, C6, I1, I2; validated by V1, V5, V6. `docs/agentic_coding_principle.md` Simplicity First와 Think Before Coding을 `feature-draft` 산출 계약에 반영한다.

**Dependencies**: 없음.

### Task T2: Codex implementation-plan에 Min-Code와 Open Q schema 적용

**Component**: implementation-plan pair
**Priority**: P0
**Type**: Improvement

**Description**: implementation-plan task가 요청된 동작에 필요한 최소 코드만 명세하도록 Hard Rule과 self-check를 추가하고, 모호함은 4필드 Open Questions schema로 surface한다.

**Acceptance Criteria**:
- [ ] AC에 Plan task Min-Code 항목과 Open Questions schema 항목을 추가한다.
- [ ] Hard Rule 2를 best-effort decision + 4필드 schema + Step 8 surface 방식으로 교체한다.
- [ ] Hard Rule 10에 사변적 phase 분리 금지 문장을 추가한다.
- [ ] Hard Rule 12 `Minimum-Code Mandate`를 추가한다.
- [ ] Step 4에 Min-Code self-check 3문항을 추가한다.
- [ ] Step 7에 Open Questions schema template과 저장 전 Min-Code/schema 점검을 추가한다.
- [ ] Step 8 `Surface Key Decisions to User`를 추가한다.
- [ ] Error Handling의 user input 모호 대응을 schema 기록 방식으로 갱신한다.
- [ ] skill/agent mirror가 유지된다.

**Target Files**:
- [M] `.codex/skills/implementation-plan/SKILL.md`
- [M] `.codex/agents/implementation-plan.toml`

**Technical Notes**: Covers C3, C6, I1; validated by V2, V5. Task AC는 `feature-draft` T1의 Min-Code 패턴에서 직접 도출된다.

**Dependencies**: T1 이후 권장.

### Task T3: Codex implementation에 execution-time Min-Code enforcement 추가

**Component**: implementation pair
**Priority**: P0
**Type**: Improvement

**Description**: implementation 실행 과정에서 sub-agent가 AC 외 옵션, 설정, 추상화, 에러 처리를 추가하지 못하도록 hard rule과 prompt를 보강하고, phase review에서 Speculative Code를 검사한다.

**Acceptance Criteria**:
- [ ] AC에 sub-agent output Min-Code 검증과 Plan/Phase surface 항목을 추가한다.
- [ ] Hard Rules에 Minimum-Code Mandate를 추가한다. REFACTOR 단계의 단일 사용처 추상화 금지도 포함한다.
- [ ] Step 1에 `Surface Plan Assumptions` sub-step을 추가한다.
- [ ] Sub-Agent Prompt 규칙에 Minimum-Code clause를 추가한다.
- [ ] Phase Review 품질 체크표에 `Speculative Code` 행을 추가한다.
- [ ] Decision Gate에서 Speculative Code 기본 분류와 Critical escalation을 명시한다.
- [ ] Step 6 끝에 `Surface Phase Surprises` sub-step을 추가한다.
- [ ] skill/agent mirror가 유지된다.

**Target Files**:
- [M] `.codex/skills/implementation/SKILL.md`
- [M] `.codex/agents/implementation.toml`

**Technical Notes**: Covers C4, C6, I1; validated by V3, V5. Goal-Driven Execution 원칙에 따라 phase review가 "should work"가 아니라 AC 외 코드 여부까지 검증한다.

**Dependencies**: T1 이후 권장. T2와 병렬 가능.

### Task T4: Codex implementation-review에 Speculative Code review 축 추가

**Component**: implementation-review pair
**Priority**: P1
**Type**: Improvement

**Description**: implementation-review가 plan/spec/codebase 기준으로 사변적 코드를 명시 탐지하고, recommendations 자체도 발견된 결함 또는 측정 위험에만 연결되도록 제한한다.

**Acceptance Criteria**:
- [ ] AC에 Speculative Code assessment/finding 적용 항목과 Recommendations Min-Code 항목을 추가한다.
- [ ] Hard Rule에 Recommendations Min-Code를 추가한다.
- [ ] Step 5 Tier 1/2/3 Assessment에 Speculative Code 점검 축을 추가한다.
- [ ] Step 6 Findings Classification에서 Speculative Code 기본 severity를 Medium으로 분류한다.
- [ ] Speculative Code가 실제 버그, 보안 영향, 데이터 손실 위험을 만들면 Critical로 escalate한다고 명시한다.
- [ ] Output Format Recommendations 설명에 사변적 `future-proof` 권고 금지를 추가한다.
- [ ] skill/agent mirror가 유지된다.

**Target Files**:
- [M] `.codex/skills/implementation-review/SKILL.md`
- [M] `.codex/agents/implementation-review.toml`

**Technical Notes**: Covers C5, I1; validated by V4, V5. Review recommendations가 다시 spec creep을 만드는 일을 막는다.

**Dependencies**: T1 이후 권장. T2/T3와 병렬 가능.

## Parallel Execution Summary

| Group | Tasks | Parallel? | Reason |
|-------|-------|-----------|--------|
| G1 | T1 | No | downstream 문구 패턴 source 확정 |
| G2 | T2, T3, T4 | Yes | 서로 다른 skill/agent pair를 수정한다 |
| G3 | Mirror parity validation | No | 모든 변경 후 한 번에 검증 |

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| `.claude` 본문 복사 중 Codex-specific marker 삭제 | `spec-update-todo` handoff contract 손상 | T1 AC와 V6에서 marker 보존을 명시한다 |
| TOML heredoc quoting 손상 | agent 로딩 실패 | `.codex/agents/*.toml` 수정 후 TOML parse 또는 최소 syntax check를 수행한다 |
| skill/agent mirror drift | direct invocation과 internal agent 동작 차이 | V5에서 pair별 의미 동등성을 확인한다 |
| Min-Code 문구가 너무 일반적이라 실행력이 약함 | 사변적 코드 방지 효과 저하 | task/sub-agent/review 단계별 구체 금지 항목을 반복 명시한다 |

## Open Questions

### Q1. `skill.json` version bump를 같이 할지

- **Decision taken**: 이번 구현에서는 제외한다.
- **Alternatives considered**: 함께 bump하면 release traceability가 좋아지지만 metadata 정책 확인이 필요해 이번 surgical change 범위를 넘는다.
- **Confidence**: MEDIUM
- **User confirmation needed**: Yes

### Q2. dogfooding 검증을 이번 구현에 포함할지

- **Decision taken**: 이번 구현 범위에서는 문서 구조 검증까지만 수행하고, 실제 skill invocation은 후속 검증으로 둔다.
- **Alternatives considered**: 즉시 dogfooding하면 신뢰도는 높지만 명세 적용 작업 자체보다 시간이 커질 수 있다.
- **Confidence**: MEDIUM
- **User confirmation needed**: No

## Self-Containment Check

- 검토 섹션 수: 10
- Pass 1 발견 갭 및 보완:
  - `Codex-specific 규칙`의 의미가 불명확할 수 있어 Scope Delta와 T1 Description에 marker, thin spec code exploration, decision log fallback을 구체적으로 재진술했다.
  - `Speculative Code`가 무엇인지 Task T3/T4 AC에 옵션, 설정, 추상화, 도달 불가 에러 처리로 풀어 썼다.
- Pass 2 발견 갭 및 보완:
  - reader가 왜 feature-draft만이 아니라 implementation chain도 포함하는지 모를 수 있어 Q2와 Overview에 plan -> implement -> review enforcement loop 근거를 추가했다.
  - reader가 어떤 파일을 실제로 수정해야 하는지 한눈에 보기 어렵기 때문에 Components와 각 task Target Files에 skill/agent pair를 모두 명시했다.
- 보완 완료: Yes
