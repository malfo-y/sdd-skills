# Feature Draft: Strategic Code Map 기반 spec skill 정렬

<!-- spec-update-todo-input-start -->
# Part 1: Temporary Spec Draft

## Change Summary

spec lifecycle 계열 스킬은 `Strategic Code Map`을 agentic coding을 위한 공식 optional navigation surface로 다뤄야 한다. 목표는 thin global spec 모델을 유지하면서도, 사람과 LLM agent가 코드 탐색을 시작할 수 있는 압축된 좌표를 제공하는 것이다.

이번 변경은 canonical definition, spec 생성/리뷰/리라이트/업데이트 스킬, Claude/Codex skill mirror, 그리고 wrapper-backed agent mirror를 함께 정렬한다.

- global spec은 계속 `개념 + 경계 + 결정` 중심이다.
- `Strategic Code Map`은 exhaustive inventory가 아니라 compact navigation hint다.
- 작은 repo는 `main.md` 안에 짧은 appendix로 둘 수 있다.
- 길거나 설명이 필요한 map은 `components.md` 또는 `code-map.md` 같은 supporting surface로 분리한다.
- temporary spec과 implementation plan은 code map을 힌트로만 사용하고, 실제 `Touchpoints`와 `Target Files`는 현재 코드 탐색으로 재확인한다.

## Scope Delta

### In Scope

- SDD canonical docs에 `Strategic Code Map` 정의와 배치 규칙을 추가한다.
- `spec-create`가 primary navigation axis를 선택하고, 필요한 경우 compact map 또는 supporting surface를 생성하도록 수정한다.
- `spec-review`, `spec-rewrite`, `spec-upgrade`, `spec-update-todo`, `spec-update-done`, `spec-summary`, `feature-draft`가 navigation-critical hint와 exhaustive implementation inventory를 구분하도록 수정한다.
- 변경되는 `.codex/skills/*/SKILL.md`와 매칭되는 `.claude/skills/*/SKILL.md`를 함께 수정한다.
- agent copy가 존재하는 workflow는 `.codex/agents/*.toml`과 `.claude/agents/*.md`도 동일한 normative rule로 미러링한다.
- `spec-create` template/example도 함께 수정해 추상 규칙뿐 아니라 예시 기반 학습이 가능하게 한다.

### Out of Scope

- downstream project의 기존 `_sdd/spec/main.md`를 실제로 리라이트하지 않는다.
- 자동 code-map 생성 도구는 만들지 않는다.
- 모든 global spec에 새 mandatory section을 강제하지 않는다.
- feature/domain 축과 module/layer 축을 둘 다 병렬 문서 체계로 만들지 않는다. primary axis 하나가 기본이다.

### Guardrail Delta

- `Strategic Code Map`은 전체 파일 트리, 컴포넌트 카탈로그, API reference, 구현 narrative가 되면 안 된다.
- secondary axis는 cross-reference로만 둔다. 별도 동등 문서 체계로 만들지 않는다.
- code map은 시작 힌트일 뿐이다. feature planning은 현재 코드 탐색을 통해 `Touchpoints`와 `Target Files`를 다시 확정해야 한다.

## Contract/Invariant Delta

| ID | Type | Change | Why |
|----|------|--------|-----|
| C1 | Add | SDD definition 문서는 `Strategic Code Map`을 optional navigation surface로 정의한다. 허용 정보는 entrypoint, contract source, invariant hotspot, extension point, change hotspot, validation surface, supporting reference다. | 모든 spec lifecycle 스킬이 같은 용어와 기준을 공유하게 한다. |
| C2 | Modify | `spec-create`는 코드베이스가 있으면 primary navigation axis를 하나 선택한다. app/service는 feature/domain/change-path, library/framework는 module/layer, workflow/tooling repo는 entrypoint/workflow, 작은 repo는 `main.md` appendix를 기본 후보로 본다. | repo 성격에 맞는 agentic coding 지도 축을 선택하게 한다. |
| C3 | Modify | `spec-create`는 single-file default를 유지하되, 짧은 `Strategic Code Map`은 `main.md` appendix로 허용한다. 길거나 설명이 필요하면 supporting surface로 분리한다. | single-file default와 navigation 필요 사이의 긴장을 해소한다. |
| C4 | Modify | `spec-review`, `spec-rewrite`, `spec-upgrade`는 exhaustive inventory와 navigation-critical hint를 구분한다. | 정리/마이그레이션 과정에서 유용한 탐색 힌트를 잃지 않고, stale inventory는 제거하게 한다. |
| C5 | Modify | `spec-update-todo`, `spec-update-done`은 temporary `Touchpoints`를 global spec에 통째로 복사하지 않는다. 다만 장기적으로 남는 entrypoint, extension point, invariant hotspot, validation surface가 생기거나 바뀌면 code map entry를 보수적으로 갱신할 수 있다. | global spec thinness를 유지하면서 persistent navigation hint는 최신화한다. |
| C6 | Modify | `feature-draft`는 `Strategic Code Map`을 context gathering 출발점으로만 사용한다. 실제 `Touchpoints`와 `Target Files`는 현재 코드 탐색으로 검증한다. | stale map에 기반한 agentic coding 오류를 줄인다. |
| C7 | Add | 변경된 Codex skill은 매칭 Claude skill도 함께 수정한다. wrapper-backed workflow는 `.codex/agents`와 `.claude/agents`의 agent mirror도 함께 수정한다. | platform drift와 skill/agent instruction divergence를 막는다. |

| ID | Type | Invariant | Why |
|----|------|-----------|-----|
| I1 | Preserve | global spec mandatory core는 `background/concept`, `scope/non-goals/guardrails`, `core design/key decisions`로 유지한다. | code-map 도입이 inventory-heavy global spec 회귀로 이어지지 않게 한다. |
| I2 | Add | compact row 수를 넘거나 per-path narrative가 필요한 code map은 `main.md` 본문이 아니라 supporting surface에 둔다. | 작은 스펙은 읽기 쉽게, 큰 지도는 적절한 surface에 둔다. |
| I3 | Add | skill과 agent mirror는 host-specific format이 달라도 같은 normative rule을 담아야 한다. | 실행 런타임별 동작 차이를 줄인다. |

## Touchpoints

| Area | Paths | Reason |
|------|-------|--------|
| Canonical definition | `docs/SDD_SPEC_DEFINITION.md`, `docs/en/SDD_SPEC_DEFINITION.md` | 모든 spec lifecycle skill의 공통 기준이다. |
| Codex spec skills | `.codex/skills/spec-create/SKILL.md`, `.codex/skills/spec-review/SKILL.md`, `.codex/skills/spec-rewrite/SKILL.md`, `.codex/skills/spec-upgrade/SKILL.md`, `.codex/skills/spec-update-todo/SKILL.md`, `.codex/skills/spec-update-done/SKILL.md`, `.codex/skills/spec-summary/SKILL.md`, `.codex/skills/feature-draft/SKILL.md` | Codex 사용자/agent 진입점이다. |
| Claude spec skills | 위 Codex skill과 매칭되는 `.claude/skills/*/SKILL.md` | 사용자가 명시적으로 요청한 Claude skill parity 대상이다. |
| Codex agent mirrors | `.codex/agents/feature-draft.toml`, `.codex/agents/spec-review.toml`, `.codex/agents/spec-update-todo.toml`, `.codex/agents/spec-update-done.toml` | 변경 대상 wrapper-backed workflow의 Codex agent copy다. |
| Claude agent mirrors | `.claude/agents/feature-draft.md`, `.claude/agents/spec-review.md`, `.claude/agents/spec-update-todo.md`, `.claude/agents/spec-update-done.md` | 변경 대상 wrapper-backed workflow의 Claude agent copy다. |
| Spec-create teaching assets | `.codex/skills/spec-create/references/*.md`, `.codex/skills/spec-create/examples/*.md`, 매칭 `.claude/skills/spec-create/...` | 좋은 출력 형태를 예시로 학습시키는 surface다. |

## Implementation Plan

1. canonical docs에 `Strategic Code Map` 정의, 배치 규칙, primary-axis 선택 기준을 추가한다.
2. `spec-create`와 template/example을 수정해 작은 map은 `main.md`, 큰 map은 supporting surface로 가게 한다.
3. review/rewrite/upgrade/update/summary/feature-draft skill이 새 map을 올바르게 소비하고 보호하도록 수정한다.
4. 변경된 Codex skill을 모두 Claude skill에 미러링한다.
5. wrapper-backed workflow의 Codex/Claude agent mirror를 수정한다.
6. `git diff --check`, targeted `rg`, mirror parity review로 검증한다.

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, I1 | review | SDD definition이 global mandatory core를 유지하면서 `Strategic Code Map`을 optional surface로 정의하는지 확인한다. |
| V2 | C2, C3, I2 | review | `spec-create`에 primary-axis 선택, single-file appendix 허용, supporting-surface escalation 규칙이 있는지 확인한다. |
| V3 | C4 | review | review/rewrite/upgrade가 inventory와 navigation-critical hint를 구분하는지 확인한다. |
| V4 | C5 | review | update skill이 `Touchpoints` 통복사를 금지하고 persistent map entry만 허용하는지 확인한다. |
| V5 | C6 | review | feature-draft가 code map을 시작 힌트로만 쓰고 `Target Files`는 현재 코드로 검증하게 하는지 확인한다. |
| V6 | C7, I3 | manual-check | 변경된 Codex skill, Claude skill, Codex agent, Claude agent mirror가 같은 normative rule을 갖는지 확인한다. |
| V7 | 전체 | test | `git diff --check`와 `rg "Strategic Code Map|primary navigation axis|exhaustive inventory|Target Files"`를 실행한다. |

## Risks / Open Questions

### Q1. English docs를 같은 변경에서 수정할 것인가
- **Decision taken**: `docs/en/SDD_SPEC_DEFINITION.md`가 존재하고 현재 유지되는 mirror이므로 target에 포함한다.
- **Alternatives considered**: 한국어 docs만 수정; canonical rollout 시 영어 mirror drift가 생길 수 있어 기각한다.
- **Confidence**: MEDIUM
- **User confirmation needed**: No

### Q2. 공통 reference 파일을 새로 만들 것인가
- **Decision taken**: 이번 변경에서는 새 shared reference 파일을 만들지 않고, 관련 skill/agent surface에 compact normative text를 직접 넣는다.
- **Alternatives considered**: `references/strategic-code-map.md` 신설; 현재 스킬들이 self-contained instruction을 선호하므로 이번 범위에서는 보류한다.
- **Confidence**: MEDIUM
- **User confirmation needed**: No

### Q3. `implementation-plan`이나 `implementation-review` 같은 비-spec agent도 수정할 것인가
- **Decision taken**: 직접 dependency가 구현 중 발견되지 않는 한 제외한다. 이번 범위는 spec lifecycle과 feature-draft planning surface다.
- **Alternatives considered**: implementation 계열 전체 수정; blast radius가 커지고 사용자 요청 범위를 넘어서 기각한다.
- **Confidence**: HIGH
- **User confirmation needed**: No

<!-- spec-update-todo-input-end -->

# Part 2: Implementation Plan

## Overview

이 구현은 SDD spec lifecycle에서 `Strategic Code Map`을 agentic coding용 optional navigation hint로 표준화한다. 대상은 canonical docs, Codex skills, Claude skill mirrors, wrapper-backed Codex/Claude agent mirrors다.

`Strategic Code Map`은 사람이나 LLM이 코드 탐색을 시작할 때 먼저 확인해야 할 entrypoint, contract source, invariant hotspot, extension point, change hotspot, validation surface, supporting reference의 compact 목록이다. 전체 파일 목록이나 구현 상세 설명서가 아니다.

## Scope

### Included

- canonical definition과 optional placement rule.
- `spec-create` 생성 동작과 template/example.
- `spec-review`, `spec-rewrite`, `spec-upgrade`, `spec-update-*`, `spec-summary`, `feature-draft` 소비/보호 규칙.
- 모든 변경 Codex skill의 Claude skill mirror.
- agent copy가 있는 workflow의 `.codex/agents` / `.claude/agents` mirror.

### Excluded

- downstream project spec 리라이트.
- code map 자동 생성 도구.
- 직접 dependency가 없는 implementation execution agent 수정.
- feature axis와 module axis를 둘 다 authoritative 문서 체계로 만드는 작업.

## Components

| Component | Purpose | Primary Files |
|-----------|---------|---------------|
| Canonical docs | 공통 SDD semantics 정의 | `docs/SDD_SPEC_DEFINITION.md`, `docs/en/SDD_SPEC_DEFINITION.md` |
| Spec generation | thin global spec을 유지하면서 map 생성 | `.codex/skills/spec-create/*`, `.claude/skills/spec-create/*` |
| Spec quality controls | map을 리뷰/리라이트/업그레이드에서 올바르게 처리 | `spec-review`, `spec-rewrite`, `spec-upgrade` skill pairs |
| Spec sync controls | persistent navigation 변화만 승격 | `spec-update-todo`, `spec-update-done` skill/agent pairs |
| Planning controls | map을 힌트로 쓰고 Target Files는 코드로 검증 | `feature-draft` skill/agent pairs |
| Reader summary | map을 code grounding input으로 사용 | `spec-summary` skill pair |

## Contract/Invariant Delta Coverage

- C1은 canonical docs 변경으로 충족한다.
- C2/C3은 `spec-create` process, structure decision, output contract, template/example 변경으로 충족한다.
- C4는 review/rewrite/upgrade quality rule 변경으로 충족한다.
- C5는 planned/done spec sync mapping rule 변경으로 충족한다.
- C6은 feature-draft context gathering과 Target Files rule 변경으로 충족한다.
- C7/I3은 `.claude/skills`와 `.codex/agents` / `.claude/agents` mirror를 명시적 Target Files로 포함해 충족한다.
- I1/I2는 map을 optional, compact, supporting-surface-aware 규칙으로만 추가해 보존한다.

## Implementation Phases

| Phase | Checkpoint | Goal |
|-------|------------|------|
| Phase 1 | Yes | canonical docs와 `spec-create` 생성 자산 수정 |
| Phase 2 | Yes | 소비자/업데이트 skill과 Claude mirror 수정 |
| Phase 3 | Yes | wrapper-backed agent mirror 수정 |
| Phase 4 | No | validation과 wording tighten |

## Task Details

### Task 1: canonical docs에 `Strategic Code Map` 정의 추가

**Component**: Canonical docs
**Priority**: P0
**Type**: Documentation

**Description**: SDD definition에 `Strategic Code Map` 정의, 허용 필드, 배치 규칙, primary-axis 선택 기준을 추가한다. 이 task는 C1의 source를 만든다.

**Acceptance Criteria**:
- [ ] `docs/SDD_SPEC_DEFINITION.md`가 `Strategic Code Map`을 정의한다.
- [ ] 해당 정의가 optional surface임을 명시한다.
- [ ] `main.md` appendix, supporting surface, guide, temporary spec의 배치 기준을 구분한다.
- [ ] app/service, library/framework, workflow/tooling, small repo의 primary axis 기준을 포함한다.
- [ ] `docs/en/SDD_SPEC_DEFINITION.md`에 동등한 mirror 문구가 반영된다.

**Target Files**:
- [M] `docs/SDD_SPEC_DEFINITION.md` -- Korean canonical definition.
- [M] `docs/en/SDD_SPEC_DEFINITION.md` -- English mirror.

**Technical Notes**: Covers C1, I1, I2. `Strategic Code Map`은 mandatory global section이 아니라 optional/supporting information으로 둔다.

**Dependencies**: None.

### Task 2: Codex `spec-create` 동작 수정

**Component**: Spec generation
**Priority**: P0
**Type**: Documentation

**Description**: `spec-create`가 primary navigation axis를 고르고, 필요한 경우 compact `Strategic Code Map`을 생성하도록 수정한다. `_sdd/spec/main.md` single-file default는 유지하고, map이 길어지면 supporting surface로 보낸다.

**Acceptance Criteria**:
- [ ] `Structure Decision`에 primary navigation axis 선택 기준이 들어간다.
- [ ] `Process`가 entrypoint, contract source, invariant hotspot, extension point, change hotspot, validation surface, supporting reference 후보를 식별한다.
- [ ] `Write the Spec`가 short appendix와 supporting file 분기 기준을 설명한다.
- [ ] `Output Contract`가 `_sdd/spec/components.md` 또는 `_sdd/spec/code-map.md`를 조건부 산출물로 허용한다.
- [ ] Hard Rules 또는 Final Check가 exhaustive file inventory를 금지한다.

**Target Files**:
- [M] `.codex/skills/spec-create/SKILL.md` -- Codex generation behavior.

**Technical Notes**: Covers C2, C3, I2.

**Dependencies**: Task 1.

### Task 3: Claude `spec-create` mirror 수정

**Component**: Spec generation mirror
**Priority**: P0
**Type**: Documentation

**Description**: Codex `spec-create`와 같은 normative rule을 Claude skill mirror에 반영한다.

**Acceptance Criteria**:
- [ ] Claude `spec-create`가 primary-axis, short appendix, supporting surface, anti-inventory rule을 포함한다.
- [ ] host-specific 문구는 달라도 normative behavior는 Codex와 일치한다.

**Target Files**:
- [M] `.claude/skills/spec-create/SKILL.md` -- Claude mirror.

**Technical Notes**: Covers C7, I3.

**Dependencies**: Task 2.

### Task 4: `spec-create` template/example 수정

**Component**: Spec-create teaching assets
**Priority**: P1
**Type**: Documentation

**Description**: 추상적인 `appendix-level code map` 언급을 concrete `Strategic Code Map` 예시로 바꾼다. 작은 repo는 `main.md` appendix, 큰 repo는 supporting surface 분리 예시를 보여준다.

**Acceptance Criteria**:
- [ ] compact template에 optional `Strategic Code Map` table이 들어간다.
- [ ] full template에 supporting-surface 분기 기준이 들어간다.
- [ ] simple example은 `main.md` 안 짧은 appendix를 보여준다.
- [ ] complex/additional example은 `components.md` 또는 `code-map.md` 분리 기준을 보여준다.
- [ ] Claude assets가 Codex assets와 동등하다.

**Target Files**:
- [M] `.codex/skills/spec-create/references/template-compact.md` -- compact template.
- [M] `.codex/skills/spec-create/references/template-full.md` -- full template.
- [M] `.codex/skills/spec-create/examples/simple-project-spec.md` -- small repo example.
- [M] `.codex/skills/spec-create/examples/complex-project-spec.md` -- larger repo example.
- [M] `.codex/skills/spec-create/examples/additional-specs.md` -- split guidance.
- [M] `.claude/skills/spec-create/references/template-compact.md` -- Claude compact template.
- [M] `.claude/skills/spec-create/references/template-full.md` -- Claude full template.
- [M] `.claude/skills/spec-create/examples/simple-project-spec.md` -- Claude small repo example.
- [M] `.claude/skills/spec-create/examples/complex-project-spec.md` -- Claude larger repo example.
- [M] `.claude/skills/spec-create/examples/additional-specs.md` -- Claude split guidance.

**Technical Notes**: Covers C2, C3, C7, I2.

**Dependencies**: Task 2, Task 3.

### Task 5: spec quality/migration skill 수정

**Component**: Spec quality controls
**Priority**: P1
**Type**: Documentation

**Description**: review/rewrite/upgrade가 유용한 navigation hint는 보존하고, exhaustive inventory는 제거하거나 supporting surface로 이동하도록 수정한다.

**Acceptance Criteria**:
- [ ] `spec-review`는 code map 부재를 기본 defect로 보지 않는다.
- [ ] non-trivial repo에서 next surface가 전혀 없으면 `Improvements`로 제안한다.
- [ ] stale path나 misleading map은 `Quality`로 잡는다.
- [ ] 잘못된 authoritative contract를 선언하면 필요 시 `Critical`로 승격할 수 있다.
- [ ] `spec-rewrite`는 navigation hint를 삭제하지 않고 compact map 또는 supporting surface로 압축/이동한다.
- [ ] `spec-upgrade`는 legacy 내용을 decision-bearing truth, navigation-critical hint, stale/exhaustive detail로 나눈다.
- [ ] Claude skill mirror도 같은 규칙을 포함한다.

**Target Files**:
- [M] `.codex/skills/spec-review/SKILL.md` -- review rubric.
- [M] `.codex/skills/spec-rewrite/SKILL.md` -- rewrite rules.
- [M] `.codex/skills/spec-upgrade/SKILL.md` -- upgrade mapping.
- [M] `.claude/skills/spec-review/SKILL.md` -- Claude review mirror.
- [M] `.claude/skills/spec-rewrite/SKILL.md` -- Claude rewrite mirror.
- [M] `.claude/skills/spec-upgrade/SKILL.md` -- Claude upgrade mirror.

**Technical Notes**: Covers C4, C7.

**Dependencies**: Task 1.

### Task 6: spec sync/summary skill 수정

**Component**: Spec sync and reader summary
**Priority**: P1
**Type**: Documentation

**Description**: planned/done spec sync는 persistent map 변화만 반영하고, temporary touchpoint는 그대로 복사하지 않게 한다. summary는 map을 code grounding input으로 사용하되 map의 authoritative replacement가 되지 않게 한다.

**Acceptance Criteria**:
- [ ] `spec-update-todo`는 temporary `Touchpoints` 통복사를 금지한다.
- [ ] `spec-update-todo`는 planned persistent map entry를 명시적 planned status로 추가할 수 있다.
- [ ] `spec-update-done`은 구현/검증된 persistent map update만 반영한다.
- [ ] `spec-summary`는 code map을 `Code Grounding` 입력으로 사용하되 중복 replacement가 되지 않게 한다.
- [ ] Claude skill mirror도 같은 규칙을 포함한다.

**Target Files**:
- [M] `.codex/skills/spec-update-todo/SKILL.md` -- planned sync behavior.
- [M] `.codex/skills/spec-update-done/SKILL.md` -- completed sync behavior.
- [M] `.codex/skills/spec-summary/SKILL.md` -- summary behavior.
- [M] `.claude/skills/spec-update-todo/SKILL.md` -- Claude planned sync mirror.
- [M] `.claude/skills/spec-update-done/SKILL.md` -- Claude completed sync mirror.
- [M] `.claude/skills/spec-summary/SKILL.md` -- Claude summary mirror.

**Technical Notes**: Covers C5, C7.

**Dependencies**: Task 1.

### Task 7: feature-draft skill 수정

**Component**: Planning controls
**Priority**: P0
**Type**: Documentation

**Description**: `feature-draft`가 `Strategic Code Map` 또는 supporting surface를 context로 읽되, `Touchpoints`와 `Target Files`는 현재 코드 탐색으로 검증하게 한다.

**Acceptance Criteria**:
- [ ] Context gathering이 map/supporting surface를 읽도록 설명한다.
- [ ] Hard Rules가 map은 starting hint이지 `Target Files` source of truth가 아니라고 명시한다.
- [ ] `Touchpoints`는 현재 코드 기준으로 재검증해야 한다.
- [ ] `Target Files`는 실제 경로 확정 또는 `[TBD] <reason>`를 요구한다.
- [ ] Claude skill mirror도 같은 규칙을 포함한다.

**Target Files**:
- [M] `.codex/skills/feature-draft/SKILL.md` -- Codex feature draft skill.
- [M] `.claude/skills/feature-draft/SKILL.md` -- Claude feature draft mirror.

**Technical Notes**: Covers C6, C7.

**Dependencies**: Task 1.

### Task 8: wrapper-backed agent mirror 수정

**Component**: Agent mirror parity
**Priority**: P0
**Type**: Documentation

**Description**: agent copy가 존재하는 workflow에 같은 normative rule을 반영한다. Codex agent는 TOML `developer_instructions`, Claude agent는 Markdown frontmatter 형식이라 포맷은 달라도 동작 규칙은 같아야 한다.

**Acceptance Criteria**:
- [ ] `feature-draft` agents가 map-as-hint와 current-code-verification rule을 포함한다.
- [ ] `spec-review` agents가 map quality severity guidance를 포함한다.
- [ ] `spec-update-todo` agents가 persistent-map promotion과 no-wholesale-touchpoints-copy rule을 포함한다.
- [ ] `spec-update-done` agents가 verified persistent-map update rule을 포함한다.
- [ ] skill/agent mirror notice가 있는 경우 수정 후에도 참이다.

**Target Files**:
- [M] `.codex/agents/feature-draft.toml` -- Codex feature draft agent mirror.
- [M] `.codex/agents/spec-review.toml` -- Codex spec review agent mirror.
- [M] `.codex/agents/spec-update-todo.toml` -- Codex planned sync agent mirror.
- [M] `.codex/agents/spec-update-done.toml` -- Codex completed sync agent mirror.
- [M] `.claude/agents/feature-draft.md` -- Claude feature draft agent mirror.
- [M] `.claude/agents/spec-review.md` -- Claude spec review agent mirror.
- [M] `.claude/agents/spec-update-todo.md` -- Claude planned sync agent mirror.
- [M] `.claude/agents/spec-update-done.md` -- Claude completed sync agent mirror.

**Technical Notes**: Covers C7, I3.

**Dependencies**: Task 5, Task 6, Task 7.

### Task 9: wording과 mirror parity 검증

**Component**: Verification
**Priority**: P0
**Type**: Test

**Description**: lightweight text/diff check로 path, whitespace, mirror 누락을 잡는다.

**Acceptance Criteria**:
- [ ] `git diff --check`가 통과한다.
- [ ] `rg "Strategic Code Map|primary navigation axis|exhaustive inventory|Target Files" docs .codex .claude`에서 기대 surface가 확인된다.
- [ ] 변경된 `.codex/skills/<name>/SKILL.md`마다 매칭 `.claude/skills/<name>/SKILL.md`도 변경됐다.
- [ ] agent copy가 있는 변경 workflow마다 `.codex/agents/<name>.toml`과 `.claude/agents/<name>.md`가 함께 변경됐다.
- [ ] 어떤 문구도 code map을 global spec mandatory section으로 요구하지 않는다.

**Target Files**:
- [TBD] 파일 수정 없음 -- validation task.

**Technical Notes**: Covers V1-V7.

**Dependencies**: Tasks 1-8.

## Parallel Execution Summary

| Workstream | Can Run In Parallel | Notes |
|------------|---------------------|-------|
| Canonical docs | No | 먼저 수정해야 skill wording이 이를 참조할 수 있다. |
| Codex/Claude `spec-create` | Partly | Codex를 먼저 확정하고 Claude에 mirror하는 편이 안전하다. |
| Template/example | Yes after Task 2 | 한쪽을 확정한 뒤 다른 플랫폼에 동등 반영한다. |
| Review/rewrite/upgrade | Yes | 파일이 분리되어 있고 같은 개념 규칙을 적용한다. |
| Update/summary | Yes | persistent-map rule을 각 파일에 반영한다. |
| Agent mirrors | Yes after skill edits | agent는 최종 skill rule을 복사/압축해야 한다. |
| Validation | No | 모든 수정 후 실행한다. |

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| code map이 시간이 지나 exhaustive inventory로 커진다. | compactness와 supporting-surface escalation 규칙을 `spec-create`, `spec-review`, `spec-rewrite`에 넣는다. |
| Codex와 Claude skill이 한쪽만 수정돼 drift가 생긴다. | 모든 skill task에 Claude mirror Target Files를 포함하고 validation에서 확인한다. |
| agent mirror가 stale하게 남는다. | wrapper-backed workflow의 agent Target Files를 명시하고 parity validation을 둔다. |
| feature-draft가 stale code map을 과신한다. | map-as-hint rule과 current code exploration requirement를 추가한다. |
| summary가 code map을 중복 대체한다. | summary는 code grounding input으로만 사용하고 authoritative map replacement가 아니라고 명시한다. |

## Open Questions

사용자 확인이 필요한 항목은 없다. Part 1의 Q1-Q3은 구현 중 재검토 가능한 best-effort 결정이다.

## Self-Containment Check

- 검토 섹션 수: 10
- Pass 1 발견 갭 및 보완:
  - `Task 8`이 처음에는 "agent mirrors"라고만 되어 있어 구체 파일을 알기 어려웠다. `.codex/agents/*.toml`과 `.claude/agents/*.md` Target Files를 명시했다.
  - `Task 1`이 English docs 포함 여부를 모호하게 둘 수 있었다. `docs/en/SDD_SPEC_DEFINITION.md`를 target으로 명시하고 Q1에 판단 근거를 남겼다.
  - `Task 7`이 `Strategic Code Map` 용어를 정의 없이 사용했다. `Overview`에 1줄 정의를 추가했다.
- Pass 2 발견 갭 및 보완:
  - fresh reader가 `spec-create` examples를 왜 수정해야 하는지 모를 수 있었다. Task 4에 예시 기반 학습 목적을 추가했다.
  - 비-spec agent가 범위에 포함되는지 모호했다. Q3과 Scope Excluded에 implementation execution agent 제외 기준을 추가했다.
  - single-file default와 code map의 공존 방식이 불명확했다. C3, I2, Task 2 acceptance criteria로 보완했다.
- 보완 완료: Yes
