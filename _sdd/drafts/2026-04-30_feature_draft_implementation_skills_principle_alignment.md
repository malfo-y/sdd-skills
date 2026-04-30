# Feature Draft: implementation 3개 스킬 agentic coding principle 정합화

# Part 1: Temporary Spec Draft

## Change Summary

implementation-plan / implementation / implementation-review 3개 스킬과 그 agent 미러 6개 파일에 다음을 도입한다:

- **Minimum-Code Mandate** (P0-1, P0-2): plan task와 sub-agent 산출물이 AC 외 사변적 코드(옵션·설정·추상화·도달 불가 에러 처리)를 포함하지 못하도록 plan→implement→review 체인 전체에 강제.
- **Open Questions schema + Surface mechanism** (P1-1, P2): implementation-plan은 best-effort 결정 + 4-필드 스키마 + Step 8 Surface, implementation은 시작 전 Plan Assumptions Surface + Phase 후 예외 기반 Surprises Surface.
- **Speculative Code review 차원** (P1-2): implementation-review가 사변적 코드를 점검하고, 자기 권고도 Min-Code 원칙으로 구속.

근거: `docs/agentic_coding_principle.md` 4원칙 중 Simplicity First가 3개 스킬 전체에서 미적용이라는 시스템적 갭을 메우고, Think Before Coding의 alternatives surfacing 패턴을 feature-draft (이미 적용됨, 2.3.0)와 일관시킨다. 결정 출처: `_sdd/discussion/2026-04-30_discussion_implementation_skills_principle_alignment.md`.

## Scope Delta

**In scope**:
- `.claude/skills/implementation-plan/SKILL.md` ↔ `.claude/agents/implementation-plan.md`
- `.claude/skills/implementation/SKILL.md` ↔ `.claude/agents/implementation.md`
- `.claude/skills/implementation-review/SKILL.md` ↔ `.claude/agents/implementation-review.md`

**Out of scope** (의도적 제외):
- `feature-draft`: 이미 2.3.0에서 동일 패턴 적용 완료 (Hard Rule 10, 4, 9, Step 8).
- `spec-update-todo` / `spec-update-done` / `spec-review`: 별도 분석 필요. 본 draft 범위에 미포함.
- 실제 dogfooding 검증 (변경 후 실제 feature를 한 번 돌려 enforcement loop 작동 확인): 별도 후속 task로 분리 (Q1).

**Guardrail delta**:
- 9쌍 SKILL ↔ agent 본문 미러 정합성을 깨지 않는다 (이미 commit `e8c17bf`로 정합 상태). 변경되는 3쌍은 SKILL+agent 동시 수정.
- 기존 contract (Hard Rule 번호 체계, AC 의미, Process step 순서)는 바꾸지 않고 *추가*만.

## Contract/Invariant Delta

| ID | Type | Change | Why |
|----|------|--------|-----|
| C1 | Add | implementation-plan task description/AC가 Min-Code Mandate 따른다 (요청되지 않은 옵션·설정·추상화·에러 처리 금지) | feature-draft Rule 10 패턴을 plan 단계에 일관 적용 — 부풀린 task가 하류로 전파되는 것을 차단 |
| C2 | Add | implementation sub-agent prompt가 Min-Code 규칙을 명시 (REFACTOR 단계도 단일 사용처 추상화 금지 포함) | sub-agent가 plan을 그대로 구현할 때 발생할 수 있는 spec creep을 실행 시점에 차단 |
| C3 | Add | implementation-plan Open Questions가 Decision / Alternatives / Confidence / User confirmation needed 4-필드 스키마 따른다 | feature-draft Rule 4와 동일 — silent decision 차단, alternatives 가시화 |
| C4 | Add | implementation-review가 Speculative Code를 Step 5 Assessment 차원과 Step 6 Findings 분류로 점검 | enforcement loop 완성: plan/implement에 들어간 Min-Code를 review가 verify |
| C5 | Add | implementation-review Recommendations 자체도 Min-Code: 사변적 'future-proof' 권고 금지 | reviewer가 자기 권고로 spec creep을 재도입하는 self-defeating 차단 |
| C6 | Add | implementation이 Plan 로드 직후 Plan Assumptions, 매 Phase 종료 시 Phase Surprises를 사용자에게 알림 (질문 아님) | long-running 실행 중 critical decision이 Final Report에만 묻혀 redirect 기회를 잃는 갭 해소 |
| I1 | Modify | 3쌍 SKILL.md ↔ agent.md 본문 미러 정합 유지 (Mirror Notice 자기 지칭만 차이) | 호출 진입점(/skill vs Agent tool)에 무관한 동일 contract — drift 재발 방지 |
| I2 | Add | feature-draft (2.3.0)의 Min-Code + Open Q schema + Surface 패턴이 implementation 체인 전체에 일관 적용 | 한 스킬의 enforcement 만으로는 chain 전체가 막히지 않음 — upstream-to-downstream 일관성 |

## Touchpoints

| 파일 | 변경 영역 | 이유 |
|------|----------|------|
| `.claude/skills/implementation-plan/SKILL.md` | Hard Rules (10 보강 / 12 신규 / 2 교체), AC, Required Output (Open Q schema), Step 4 (self-check), Step 7 (review item), Step 8 신규, Error Handling | P0-1 + P1-1 적용 표면 |
| `.claude/agents/implementation-plan.md` | 위와 동일 (mirror) | I1 유지 |
| `.claude/skills/implementation/SKILL.md` | Hard Rules (Min-Code 신규), AC, Step 1 끝 (Plan Assumptions Surface), Sub-agent prompt 규칙 4, Step 6 Phase Review 품질 체크표 + Decision Gate, Step 6 끝 (Phase Surprises Surface) | P0-2 + P2 적용 표면 |
| `.claude/agents/implementation.md` | 위와 동일 (mirror) | I1 유지 |
| `.claude/skills/implementation-review/SKILL.md` | Hard Rules (Recommendations Min-Code 신규), AC, Step 5 (Speculative Code 축), Step 6 Findings (명시 분류), Output Format (Recommendations 가이드) | P1-2 적용 표면 |
| `.claude/agents/implementation-review.md` | 위와 동일 (mirror) | I1 유지 |

## Implementation Plan

3쌍 6파일을 동시 변경. 각 쌍은 file-disjoint이므로 병렬 가능. 단 SKILL.md와 같은 페어의 agent.md는 하나의 task에서 함께 처리해 mirror drift를 원천 차단.

순서: P0-1+P1-1 (implementation-plan) ∥ P0-2+P2 (implementation) ∥ P1-2 (implementation-review) → mirror parity 검증.

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1 | review | implementation-plan SKILL.md에 Hard Rule 12 (Min-Code Mandate) + AC 항목 + Step 4 self-check + Step 7 review item이 feature-draft Rule 10 패턴과 동일 구조로 존재 |
| V2 | C2 | review | implementation SKILL.md Hard Rules에 Minimum-Code Mandate (REFACTOR 절 포함) + Sub-agent prompt 규칙 4 + Phase Review "Speculative Code" 행이 존재 |
| V3 | C3 | review | implementation-plan SKILL.md Hard Rule 2가 best-effort + 4-필드 스키마로 교체 + Required Output에 Open Q 스키마 + Step 8 (Surface) 존재 |
| V4 | C4, C5 | review | implementation-review SKILL.md Step 5에 Speculative Code 축 + Step 6에 명시 분류 + Hard Rule (Recommendations Min-Code) + Output Format 가이드 존재 |
| V5 | C6 | review | implementation SKILL.md Step 1 끝 "Surface Plan Assumptions" + Step 6 끝 "Surface Phase Surprises" sub-step 존재, "알림만" 형식 |
| V6 | I1, I2 | test | `diff` 명령으로 9쌍 SKILL ↔ agent 본문 (frontmatter 제외) 차이가 Mirror Notice block 라인 수 이하임을 확인 (feature-draft pair: 4줄, spec-review pair: 2줄, 나머지: 4줄) |

## Risks / Open Questions

### Q1. 변경 후 dogfooding 검증을 본 draft에 포함할지

- **Decision taken**: 본 draft 범위에서 제외. 구현 후 별도 후속 task로 분리.
- **Alternatives considered**:
  - (a) 본 draft에 dogfooding task 추가. 기각: scope 부풀림 — feature-draft Rule 10 (Min-Code) 정신에 반함.
  - (b) 별도 verification spec 즉시 작성. 보류: 변경 결과를 보고 어떤 feature로 dogfood 할지 결정하는 게 합리적.
- **Confidence**: MEDIUM
- **User confirmation needed**: Yes

### Q2. Hard Rule 11 (Self-Contained Authoring)와 신규 Hard Rule 12 (Min-Code) 공존 — 별도 룰 vs 통합

- **Decision taken**: implementation-plan에 Hard Rule 12로 *별도 추가*. feature-draft가 이미 Rule 9 (Self-Contained) + Rule 10 (Min-Code)를 별도 룰로 운영 중.
- **Alternatives considered**:
  - (a) 통합한 큰 룰 하나. 기각: 두 룰의 적용 영역(문서 자기충족 vs 코드 최소성)과 검증 절차(Pass 1/2 vs self-check 3 questions)가 다름.
  - (b) Self-Contained 안의 sub-rule. 기각: 카테고리가 다름 (문서 vs 코드).
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q3. implementation의 Surface sub-step을 별도 Step number로 분리할지

- **Decision taken**: 별도 step number 만들지 않고 Step 1 끝 (Plan Assumptions) / Step 6 끝 (Phase Surprises) 안의 sub-step으로 통합.
- **Alternatives considered**:
  - (a) Step 1.5 / 6.5 신규 추가. 기각: Step counting 깨짐, 기존 step 번호 흐름이 깨짐.
  - (b) 새 Step 8 / Step 9. 기각: implementation은 이미 Step 1~7 구조 — 늘리면 Phase 사이클이 끊김.
- **Confidence**: MEDIUM (구체 위치 명칭은 구현 시 미세조정 가능)
- **User confirmation needed**: No

### Q4. implementation의 Hard Rule 추가 시 numbering — 현재 bullet 형식 (numbered list 아님). 새 규칙도 bullet?

- **Decision taken**: 기존 형식 유지 (bullet, `**룰 이름**: 본문`).
- **Alternatives considered**:
  - (a) 번호 매기기로 전환. 기각: 변경 범위가 본 draft scope를 초과 (모든 기존 Hard Rule을 번호 매겨야 함).
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q5. spec-update-todo / spec-update-done / spec-review에도 동일 패턴 적용 필요한가

- **Decision taken**: 본 draft 범위 외. 별도 분석 후 결정.
- **Alternatives considered**:
  - (a) 본 draft에 포함. 기각: 9쌍 미러 commit (`e8c17bf`)과 별개로 각 스킬의 역할(read-only review vs spec write)에 따라 Min-Code 적용 방식이 다를 수 있음 — 분석 필요.
- **Confidence**: MEDIUM
- **User confirmation needed**: Yes

# Part 2: Implementation Plan

## Overview

직전 commit `e8c17bf` (9쌍 미러 정합) + `3180933` (feature-draft 2.3.0 Min-Code/Open Q schema/Step 8 도입) 위에서 시작. 본 plan은 동일 패턴을 implementation 체인 3개 스킬로 확산한다.

P-label 체계 (출처: `_sdd/discussion/2026-04-30_discussion_implementation_skills_principle_alignment.md`):

- **P0-1**: implementation-plan에 Minimum-Code Mandate (task 대상)
- **P0-2**: implementation에 Minimum-Code Mandate (sub-agent 대상, 4-layer enforcement)
- **P1-1**: implementation-plan Open Questions schema + Surface (feature-draft Rule 4 패턴 미러)
- **P1-2**: implementation-review Speculative Code 차원 + Recommendations Min-Code 구속
- **P2**: implementation에 Plan Assumptions Surface (시작 전) + Phase Surprises Surface (Phase 후 예외 기반)

P0-1 + P1-1은 같은 파일 페어 (implementation-plan), P0-2 + P2는 같은 파일 페어 (implementation), P1-2는 단독 (implementation-review). 따라서 task 단위는 페어 + P-label 묶음으로 나눈다.

## Scope

### In Scope

- 3개 스킬 SKILL.md 6개 영역 변경: Hard Rules / AC / Required Output / Process / Error Handling / Output Format
- 3개 agent.md 미러 동시 변경
- 9쌍 미러 정합성 사후 검증

### Out of Scope

- feature-draft, spec-update-*, spec-review (Part 1 Scope Delta 참조)
- dogfooding 검증 (Q1 deferred)
- Hard Rule 형식 일괄 normalization (Q4 — bullet vs numbered, scope 초과)

## Components

| Component | Files |
|-----------|-------|
| implementation-plan skill pair | `.claude/skills/implementation-plan/SKILL.md`, `.claude/agents/implementation-plan.md` |
| implementation skill pair | `.claude/skills/implementation/SKILL.md`, `.claude/agents/implementation.md` |
| implementation-review skill pair | `.claude/skills/implementation-review/SKILL.md`, `.claude/agents/implementation-review.md` |

## Contract/Invariant Delta Coverage

| Target | Planned Tasks | Validation Link |
|--------|---------------|-----------------|
| C1 (plan task Min-Code) | T1 | V1 |
| C2 (sub-agent Min-Code) | T2 | V2 |
| C3 (plan Open Q schema) | T1 | V3 |
| C4 (review Speculative Code) | T3 | V4 |
| C5 (review Recommendations Min-Code) | T3 | V4 |
| C6 (implementation Surface) | T2 | V5 |
| I1 (mirror parity) | T1, T2, T3 (각 task가 페어 동시 처리) | V6 |
| I2 (chain consistency) | T1, T2, T3 | V1, V2, V3, V4, V5 |

## Implementation Phases

### Phase 1: 3쌍 동시 변경

**Goal**: implementation-plan, implementation, implementation-review 3쌍에 각 P-label을 적용. SKILL+agent는 각 task 안에서 동시 처리.

**Task Set / Dependency Closure**: T1 (impl-plan: P0-1+P1-1), T2 (impl: P0-2+P2), T3 (impl-review: P1-2). 세 task는 file-disjoint — 완전 병렬.

**Validation Focus**: V1, V2, V3, V4, V5 (각 task의 변경이 feature-draft 패턴과 동일 구조를 갖는지 review).

**Exit Criteria**:
- [ ] T1, T2, T3 모두 SUCCESS (각 task의 AC 전부 만족, Hard Rule 12 위반 없음 = Covers C1)
- [ ] V6 통과: 9쌍 SKILL ↔ agent 본문 diff가 Mirror Notice block 라인 수 이하 (Covers I1)
- [ ] feature-draft Rule 10 (Min-Code Mandate) 미러 구조와 신규 Hard Rule들이 의미상 동일 — phase exit 조건으로서 review-fix gate 통과 (Covers I2)

**Carry-over Policy**: Default `None`. critical/high/medium 이슈 발견 시 phase exit 막힘. carry-over 예외 없음.

**Checkpoint**: implicit `true` (마지막 phase).

**Checkpoint Reason**: 본 plan은 single-phase. Phase 1 종료 시 모든 변경이 commit-ready 상태여야 함 — review-fix gate를 반드시 한 번은 닫아야 mirror parity가 보장됨.

## Task Details

### Task T1: implementation-plan에 Min-Code Mandate + Open Questions 스키마 + Surface 단계 적용

**Component**: implementation-plan skill pair
**Priority**: P0
**Type**: Improvement

**Description**: implementation-plan SKILL.md와 agent.md에 P0-1 (Hard Rule 12 Minimum-Code Mandate + Hard Rule 10 보강) 및 P1-1 (Hard Rule 2 교체 + Open Q schema + Step 8 Surface)을 동시 적용한다. feature-draft 2.3.0의 Hard Rule 10 (Minimum-Code Mandate, Part 2 task 대상)과 Hard Rule 4 (best-effort + 4-필드 스키마)를 패턴 템플릿으로 그대로 옮긴다 — implementation-plan의 task가 plan 산출물의 task에 해당.

**Acceptance Criteria**:

- [ ] Hard Rule 12 (Minimum-Code Mandate) 신규 추가. 본문은 feature-draft Hard Rule 10과 동일 4-bullet (요청되지 않은 기능·옵션·설정 금지 / 단일 사용처 추상화 금지 / 도달 불가 에러 처리 금지 / 사변적 형용사는 Technical Notes 근거 시만). 적용 대상은 "각 task의 description, AC, Technical Notes".
- [ ] Hard Rule 10 (multi-phase metadata) 끝에 한 줄 보강: "phase는 실제 dependency closure가 필요할 때만 분리한다."
- [ ] Hard Rule 2 교체: 기존 "구조, task boundary, target files, verification 전략을 실질적으로 바꾸는 핵심 ambiguity면 질문 1회를 추가한다" → "결과 방향을 바꿀 수 있는 ambiguity는 best-effort로 결정하되 Open Questions에 (Decision taken / Alternatives considered / Confidence / User confirmation needed)를 기록한다. 사용자에게 inline 질문을 던지지 않으며, Confidence=LOW 또는 User confirmation needed=Yes 항목은 Step 8에서 채팅으로 노출한다."
- [ ] Required Output template의 Open Questions 섹션에 4-필드 스키마 명시 (Q1./Q2. 단위 블록).
- [ ] AC 섹션에 두 항목 추가:
  - "Plan task 어느 것도 요청되지 않은 추상화·옵션·설정·에러 처리를 포함하지 않는다 (Hard Rule 12)."
  - "Open Questions 각 항목이 Decision/Alternatives/Confidence/User confirmation needed 스키마를 따른다 (Hard Rule 2)."
- [ ] Step 4 (Define Tasks) 끝에 Min-Code self-check 3개 질문 추가 (feature-draft Step 6과 동일 — AC 도출 / 사변적 형용사 / description 압축).
- [ ] Step 7 (Write the Plan) 점검 항목에 "Hard Rule 12 위반 표현 없는가" 추가.
- [ ] Step 8 (Surface Key Decisions to User) 신규 추가, Step 7 이후 Final Check 이전. feature-draft Step 8 형식 그대로 (LOW/Yes 항목 1줄씩, 알림만, 질문 아님).
- [ ] Error Handling "user input 모호" 행이 best-effort + 스키마 기록 형식으로 갱신.
- [ ] `.claude/skills/implementation-plan/SKILL.md`와 `.claude/agents/implementation-plan.md` 본문이 Mirror Notice 자기 지칭 외 byte-identical.

**Target Files**:
- [M] `.claude/skills/implementation-plan/SKILL.md` -- Hard Rules / AC / Required Output / Step 4 / Step 7 / Step 8 / Error Handling 변경
- [M] `.claude/agents/implementation-plan.md` -- 위 SKILL.md와 동일 변경 (mirror)

**Technical Notes**: Covers C1 (plan task Min-Code), C3 (Open Q schema), I2 (chain consistency); validated by V1, V3. 패턴 출처: feature-draft 2.3.0 Hard Rule 10 / 4 / Step 8 — 본 task는 그 mirror를 plan 도메인 (task)으로 적용한 것.

**Dependencies**: 없음. T2, T3와 file-disjoint.

---

### Task T2: implementation에 Min-Code 4-layer + Plan/Phase Surface 적용

**Component**: implementation skill pair
**Priority**: P0
**Type**: Improvement

**Description**: implementation SKILL.md와 agent.md에 P0-2 (Hard Rule + AC + sub-agent prompt 규칙 4 + Phase Review Speculative Code 카테고리 = 4-layer enforcement) 및 P2 (Step 1 끝 Plan Assumptions Surface + Step 6 끝 Phase Surprises Surface)를 동시 적용한다. P0-2의 4-layer는 Hard Rule (declaration), AC (verification target), sub-agent prompt (execution-level), Phase Review (integration check) 순.

**Non-Goals**: sub-agent 완료 보고에 Min-Code self-check 필드를 추가하지 않는다 (Phase Review가 catch하므로 잡음 방지).

**Acceptance Criteria**:

- [ ] Hard Rules 섹션에 신규 항목 "Minimum-Code Mandate" 추가. 본문: "Sub-agent와 후속 검증은 AC가 요구하는 동작만 구현·검증한다. 요청되지 않은 옵션·설정·추상화·에러 처리 추가 금지. 사변적 형용사 (future-proof / extensible / configurable)는 task의 Technical Notes에 근거가 명시될 때만 허용. **TDD의 REFACTOR 단계도 단일 사용처 추상화 도입은 금지한다 — 중복 제거·명확성 향상에 한정한다.**"
- [ ] Sub-agent prompt 규칙 4번 추가: "Minimum-Code: AC가 요구하지 않는 옵션·설정·추상화·에러 처리 금지. 사변적 형용사는 Technical Notes 근거 시만. REFACTOR 단계도 단일 사용처 추상화 금지."
- [ ] Step 6 Phase Review 품질 체크표에 "Speculative Code" 행 추가 — 체크 항목: "AC 외 옵션·설정·추상화, 미사용 추상화, 도달 불가 에러 처리".
- [ ] Step 6 Decision Gate에 명시: Speculative Code는 기본 Quality, 실제 버그·보안 영향 시 Critical로 escalate.
- [ ] Step 1 (Load the Plan) 끝에 sub-step "Surface Plan Assumptions" 추가. Plan Open Questions 중 Confidence=LOW 또는 User confirmation needed=Yes 항목 노출 + Autonomous Decision-Making 카테고리 중 이번 실행에 적용될 항목 예고. 알림만, 질문 아님. P1-1 미적용 plan은 Open Q를 보수적으로 모두 노출 (defensive default).
- [ ] Step 6 (Phase Review) 끝에 sub-step "Surface Phase Surprises" 추가. 그 phase에서 발생한 (a) UNPLANNED_DEPENDENCY 자동 해결, (b) Regression Iron Rule 발동 (기존 테스트 자동 업데이트), (c) Sub-agent failure → 순차 fallback. 1-3줄 요약. 발생 항목 없으면 sub-step 자체 생략.
- [ ] AC 섹션에 두 항목 추가:
  - "Sub-agent 출력이 AC 외 추가 코드 (옵션·설정·추상화·에러 처리)를 포함하지 않으며, 발견 시 Phase Review에서 Quality 또는 Critical로 분류"
  - "시작 전 Plan Assumptions와 Phase별 Surprises가 사용자에게 노출됐다 (해당 항목 없으면 생략 가능)"
- [ ] `.claude/skills/implementation/SKILL.md`와 `.claude/agents/implementation.md` 본문이 Mirror Notice 자기 지칭 외 byte-identical.

**Target Files**:
- [M] `.claude/skills/implementation/SKILL.md` -- Hard Rules / AC / Step 1 끝 / Sub-agent prompt 규칙 / Step 6 Phase Review + 끝
- [M] `.claude/agents/implementation.md` -- 위 SKILL.md와 동일 변경 (mirror)

**Technical Notes**: Covers C2 (sub-agent Min-Code), C6 (Surface), I2 (chain consistency); validated by V2, V5. REFACTOR 절은 TDD vs Min-Code 충돌 가능성을 명시 차단 — 토론 비판적 review에서 식별된 risk.

**Dependencies**: 없음. T1, T3와 file-disjoint.

---

### Task T3: implementation-review에 Speculative Code 차원 + Recommendations Min-Code 적용

**Component**: implementation-review skill pair
**Priority**: P1
**Type**: Improvement

**Description**: implementation-review SKILL.md와 agent.md에 P1-2 (Step 5 Assessment Speculative Code 축 + Step 6 Findings 명시 분류 + Hard Rule Recommendations Min-Code + Output Format 가이드)를 동시 적용한다. enforcement loop를 닫는 마지막 단계 — plan/implement에 들어간 Min-Code를 review가 verify하고, reviewer 자신의 권고도 Min-Code로 구속해 self-defeating을 차단한다.

**Acceptance Criteria**:

- [ ] Step 5 Assessment Tier 3 검사 항목에 "Speculative Code (사변적 추가)" 축 추가. Tier 1과 Tier 2도 plan/spec이 요구하지 않는 추가 코드 점검을 명시.
- [ ] Step 6 Findings Classification에 명시 분류 추가: 기본 Medium (사변적 옵션·설정·추상화·도달 불가 에러 처리), 실제 버그·보안 영향 시 Critical로 escalate.
- [ ] Hard Rules에 신규 룰 추가: "Recommendations 자체도 Min-Code 원칙을 따른다. 'future-proof / extensible / configurable' 같은 사변적 권고 금지. 권고는 발견된 실제 결함 또는 측정된 위험에 직접 대응해야 한다."
- [ ] Output Format `## 4. Recommendations` 섹션에 가이드 한 줄 추가: "Must / Should / Could는 모두 발견된 결함 또는 측정 위험에 직접 연결돼야 한다. 사변적 권고 금지."
- [ ] AC 섹션에 항목 추가: "Speculative Code 차원이 Step 5 Assessment에서 점검되고, Step 6 Findings에 분류 기준이 적용됐다."
- [ ] `.claude/skills/implementation-review/SKILL.md`와 `.claude/agents/implementation-review.md` 본문이 Mirror Notice 자기 지칭 외 byte-identical.

**Target Files**:
- [M] `.claude/skills/implementation-review/SKILL.md` -- Hard Rules / AC / Step 5 / Step 6 / Output Format
- [M] `.claude/agents/implementation-review.md` -- 위 SKILL.md와 동일 변경 (mirror)

**Technical Notes**: Covers C4 (Speculative Code review 차원), C5 (Recommendations Min-Code), I2 (chain consistency); validated by V4. enforcement loop 완성 단계 — plan에서 Min-Code 강제 (T1) → implement에서 Min-Code 강제 (T2) → review에서 Min-Code verify + 권고도 구속 (T3).

**Dependencies**: 없음. T1, T2와 file-disjoint.

## Parallel Execution Summary

T1, T2, T3는 완전 병렬 (file-disjoint). 의미적 충돌 없음:

- (1) 각 task가 만드는 모델/타입 import 관계 없음
- (2) DB 마이그레이션 없음
- (3) config/env 가정 공유 없음
- (4) API contract 생산-소비 없음 — 다만 *I2 (chain consistency)* 차원에서 세 task가 같은 패턴(Min-Code, Open Q schema, Surface)을 적용하지만, 이는 *contract* 일치이지 file-level 의존이 아님. Phase exit에서 review-fix로 일관성 검증
- (5) 같은 상수/타입 다른 값 가정 없음

→ 3 task 병렬 그룹 1개로 dispatch 가능.

## Risks and Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| feature-draft 패턴 미러 시 미세한 wording drift 발생 — 시간이 지나며 누적되어 의미 어긋남 | Medium | 각 task AC에 "feature-draft Rule X와 동일 N-bullet 구조" 명시. T1/T2/T3 후 V1~V5 review에서 wording 대조. |
| TDD REFACTOR vs Min-Code 충돌 — REFACTOR가 합법적 추출도 막을 위험 | Medium | T2 Hard Rule에 "REFACTOR는 *중복 제거·명확성 향상*에 한정, *단일 사용처* 추상화만 금지"로 경계 명시. |
| P1-1 미적용 plan을 implementation이 받았을 때 Step 1 끝 Surface가 schema 가정으로 깨짐 | Low | T2 AC 명시: "P1-1 미적용 plan은 Open Q를 보수적으로 모두 노출 (defensive default)". |
| AC 항목 증가로 verification 표면적 비대화 (impl-plan 7→9, impl 4→6, impl-review 5→6) | Low | 각 신규 AC가 새 contract와 1:1 — 부풀림 아님. Phase exit에서 종합 review로 충분. |
| Hard Rule 번호 충돌 — implementation-plan은 numbered list (현 11개), implementation은 bullet — 두 형식이 mix | Low | Q4 결정에 따라 기존 형식 유지. T1은 Hard Rule 12 추가 (numbered), T2는 bullet 추가. 형식 normalization은 별도 작업. |

## Open Questions

> Part 1 `Risks / Open Questions`와 동일한 4-필드 스키마. Part 2-Part 1 carve-out (feature-draft Rule 9): 같은 파일 내라 "ID + inline purpose"로 충족 — 본 섹션은 Part 1 Q1~Q5에 대한 *재진술이 아닌 참조*임. 자세한 4-필드는 Part 1 참조.

- **Q1** (출처: Part 1 Q1) — dogfooding 검증을 본 draft에 포함할지. **Decision**: 제외, 별도 후속. **User confirmation needed**: Yes.
- **Q5** (출처: Part 1 Q5) — spec-update-todo / spec-update-done / spec-review에도 동일 패턴 적용할지. **Decision**: 본 draft 범위 외. **User confirmation needed**: Yes.

Q2, Q3, Q4는 Confidence=HIGH/MEDIUM이고 User confirmation needed=No이므로 본 섹션에서 재참조 생략 (Part 1에서만 추적).

---

## Self-Containment Check (Hard Rule 9)

**Pass 1 — Reference Enumeration**: Part 2의 외부 참조 목록과 inline purpose 동반 여부.

| 외부 참조 | 위치 | Inline purpose 동반? |
|----------|------|---------------------|
| `_sdd/discussion/2026-04-30_discussion_implementation_skills_principle_alignment.md` | Part 1 Change Summary, Part 2 Overview | ✓ "결정 출처 / P-label 체계 출처" 명시 |
| `docs/agentic_coding_principle.md` | Part 1 Change Summary | ✓ "원칙 출처 — Simplicity First 갭의 정의" |
| feature-draft Hard Rule 10 / 4 / 9 / Step 8 | Part 1 Change Summary, Part 2 T1/T2 Description, Technical Notes | ✓ "패턴 템플릿 — 본 변경의 미러 원본" 명시 |
| commit `e8c17bf` (9쌍 미러) | Part 1 Scope Delta Guardrail, Part 2 Overview | ✓ "정합 기준선" 명시 |
| commit `3180933` (feature-draft 2.3.0) | Part 2 Overview | ✓ "패턴 도입 commit — 본 plan의 출발점" 명시 |
| Part 1 ↔ Part 2 ID 참조 (C1~C6, I1, I2, V1~V6, T1~T3, Q1~Q5) | 전반 | Part 1↔Part 2 carve-out에 따라 "ID + inline purpose"로 충족 |

**Pass 2 — Fresh-Reader Readthrough**: 작성 대화·외부 파일 접근 없는 독자가 따라갈 수 있는가.

| 섹션 | 갭 검사 | 보완 |
|------|--------|------|
| Overview "P-label 체계" | "P0-1 / P0-2 / P1-1 / P1-2 / P2가 어디서 왔는가?" | Overview 안에 출처(discussion 파일)와 5개 라벨의 의미를 inline 정의 — 보완 완료 |
| T1 "feature-draft Rule 10 패턴 템플릿" | "feature-draft Rule 10이 무엇인가?" | T1 AC가 4-bullet 내용을 그대로 명시 (요청되지 않은 기능·옵션·설정 금지 / 단일 사용처 추상화 금지 / 도달 불가 에러 처리 금지 / 사변적 형용사 근거 명시 시만) — 보완 완료 |
| T2 "Autonomous Decision-Making 카테고리" | "그 카테고리가 무엇인가?" | implementation SKILL.md 자체에 정의된 6 카테고리(Target Files 불명확 / 테스트 불명확 / 모호한 요구사항 / 범위 / 기술 선택 / 블로커) — 본 plan은 implementation 파일 자체를 변경하므로 reader는 변경 대상 파일을 함께 본다는 전제가 합리적. 추가 inline 정의는 noise — 보완 불필요 |
| Risks "Phase exit gate" | "review-fix gate가 무엇인가?" | implementation Step 5/6의 기존 메커니즘 — 변경 대상 파일에 정의됨. 같은 이유로 inline 재정의 불필요 |
| Self-Containment Check 자체 | reader가 이 표를 어떻게 해석? | 헤더 주석 + Part 1↔Part 2 carve-out 명시로 충족 — 보완 완료 |

**흔적 기록**:
- 검토 섹션 수: 8 (Overview / Scope / Components / CIV Coverage / Phases / Task Details / Parallel Summary / Risks / Open Questions)
- Pass 1 발견 갭 및 보완: 0건 — 모든 외부 참조가 inline purpose 동반
- Pass 2 발견 갭 및 보완: 1건 (Overview의 P-label 체계 출처 — Overview 안 inline 정의로 보완)
- 보완 완료: Yes
