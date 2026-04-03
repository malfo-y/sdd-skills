# Feature Draft: SDD Canonical Model Rollout

**Date**: 2026-04-03
**Author**: hyunjoonlee
**Target Spec**: `_sdd/spec/main.md` (supporting sync expected in `_sdd/spec/components.md` and `_sdd/spec/usage-guide.md`)
**Status**: Draft

---

<!-- spec-update-todo-input-start -->
# Part 1: Spec Patch Draft

> This patch can be copy-pasted into the corresponding spec section,
> or used as input for the `spec-update-todo` skill.

# Spec Update Input

**Date**: 2026-04-03
**Author**: hyunjoonlee
**Target Spec**: `_sdd/spec/main.md` (supporting sync expected in `_sdd/spec/components.md` and `_sdd/spec/usage-guide.md`)
**Spec Update Classification**: Improvement / Refactor / Documentation-System Migration

## Background & Motivation Updates

### Background Update: 새 SDD canonical model 채택 후 시스템 전반 동기화 필요

**Target Section**: `_sdd/spec/main.md` > `Background & Motivation`; supporting `_sdd/spec/components.md` > `spec-create`, `spec-upgrade`, `spec-review`, `feature-draft`, `implementation-plan`, `sdd-autopilot`

**Proposed**:

`docs/SDD_SPEC_DEFINITION.md`가 새 canonical definition으로 확정되면서, SDD 시스템은 더 이상 `whitepaper §1-§8 + architecture/component inventory 중심` 모델을 기준으로 동작하면 안 된다. 이제 canonical model은 다음을 전제로 한다.

- 글로벌 스펙은 `high-level concept + scope/non-goals/guardrails + key decisions + Contract / Invariants / Verifiability + usage/expected results + decision-bearing structure` 중심의 얇은 기준 문서다.
- 글로벌 스펙의 strategic code map은 appendix-level hint로 유지하고, 기본 운영 방식은 manual curated로 둔다.
- temporary spec은 `Change Summary`, `Scope Delta`, `Contract/Invariant Delta`, `Touchpoints`, `Implementation Plan`, `Validation Plan`, `Risks / Open Questions` 중심의 실행 청사진이다.
- skillchain은 이 정의를 실제 생성/업그레이드/요약/리뷰/계획/오케스트레이션에 반영해야 한다.

따라서 다음 순서의 전면 동기화가 필요하다.

1. 생성/변환 스킬(`spec-create`, `spec-upgrade`)과 canonical template를 먼저 갱신한다.
2. 소비/검증/계획 스킬(`spec-review`, `spec-summary`, `spec-rewrite`, `feature-draft`, `implementation-plan`, `spec-update-todo`, `spec-update-done`, `sdd-autopilot`)을 새 구조에 맞게 읽고 쓰도록 수정한다.
3. 그 다음 `docs/` 안내 문서를 실제 동작 기준으로 다시 설명한다.
4. 마지막으로 영문 미러, 예시, reference 문서를 동일한 canonical model로 정렬한다.

## Design Changes

### Design Change: 문서-스킬 동기화 순서를 `definition -> skills -> docs -> mirrors/examples`로 고정

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Core Design > Design Rationale`

**Description**:

이 프로젝트의 문서와 스킬은 동등한 authority를 가지지 않는다. `docs/SDD_SPEC_DEFINITION.md`는 헌법이고, skill/template는 실행 규칙이며, `docs/SDD_WORKFLOW.md` 같은 문서는 설명 계층이다. 따라서 canonical model 변경 시 다음 순서를 기본 운영 규칙으로 둔다.

1. definition 문서 갱신
2. generator / transformer skill 갱신
3. consumer / reviewer / planner / orchestrator skill 갱신
4. human-facing docs 갱신
5. english mirror / examples / reference sync

이 순서를 따르지 않으면 문서가 실제 skill behavior보다 앞서가거나, skill은 새 모델을 생성하지만 docs는 옛 모델을 설명하는 split-brain 상태가 생긴다.

### Design Change: global spec과 temporary spec의 비대칭 구조를 skillchain 전체의 canonical contract로 승격

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Core Design > Design Patterns`

**Description**:

skillchain 전체는 이제 `공통 코어 + 비대칭 밀도`를 전제로 동작해야 한다.

- global spec은 얇은 지속 문서다.
- temporary spec은 delta와 execution 중심 문서다.
- `Contract / Invariants / Verifiability`는 global spec의 독립 필수 축이다.
- temporary spec에서는 `Contract/Invariant Delta`와 `Validation Plan`으로 같은 의미를 표현한다.

이 변화는 단순 문체 변경이 아니라, spec generation, spec migration, review rubric, summary projection, planning output, orchestration reasoning까지 모두 바꾸는 상위 계약이다.

### Design Change: spec skillchain에 CIV 추적성과 ID 기반 검증 연결 도입

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Core Design > Design Patterns`

**Description**:

`Contract / Invariants / Verifiability`는 모든 SDD spec workflow의 canonical quality gate가 된다.

- global spec은 `Contract`, `Invariants`, `Verifiability` 3블록 구조를 사용한다.
- contract/invariant 항목은 `C1`, `I1`, `V1` 같은 고정 ID를 가진다.
- `Verification Method`는 `test`, `review`, `runtime-check`, `manual-check` enum을 사용한다.
- temporary spec의 `Contract/Invariant Delta`와 `Validation Plan`은 이 ID를 직접 참조한다.
- review / summary / orchestration skill은 이 ID 체계를 읽고 활용할 수 있어야 한다.

### Design Change: strategic code map은 manual curated를 기본 운영 모델로 사용

**Priority**: Medium
**Target Section**: `_sdd/spec/main.md` > `Appendix > Strategic Code Map`

**Description**:

strategic code map은 자동 생성 inventory가 아니라, 사람이 선별하고 유지하는 appendix-level hint를 기본 모델로 사용한다.

- 기본값은 manual curated다.
- 도구 보조 생성은 후속 옵션으로만 고려한다.
- 반자동 생성이 도입되더라도 canonical source는 curated 결과여야 한다.

이 원칙은 code map의 양보다 정확도와 drift 저항성을 우선한다는 새 canonical model과 일치한다.

## Improvements

### Improvement: `spec-create` / `spec-upgrade`를 새 canonical global/temporary 모델 기준으로 재작성

**Priority**: High
**Target Section**: `_sdd/spec/components.md` > `spec-create`, `spec-upgrade`

**Current State**:

- `spec-create`와 `spec-upgrade` reference/template가 `whitepaper §1-§8`를 canonical structure로 가정한다.
- `spec-upgrade` skill description과 acceptance criteria도 §1-§8 gap analysis를 핵심 기준으로 둔다.
- template/example은 CIV section, decision-bearing structure, temporary 7-section schema를 반영하지 않는다.

**Proposed**:

- `spec-create`가 global spec 생성 시 `Contract / Invariants / Verifiability`, `Decision-bearing structure`, appendix-level `Strategic Code Map`을 기본 구조로 사용하게 한다.
- `spec-upgrade`는 더 이상 `§1-§8 형식으로 변환`이 아니라, `새 canonical global spec 모델로 migration`하는 스킬로 재정의한다.
- `spec-create` / `spec-upgrade` template-compact, template-full, spec-format, upgrade-mapping, examples를 새 구조에 맞게 재작성한다.
- `.codex/`와 `.claude/` 쌍을 모두 동기화한다.

**Reason**:

generator / transformer 레이어가 바뀌지 않으면 이후 모든 skill과 docs 동기화가 공중전이 된다.

### Improvement: 소비/검증/정리 스킬을 새 canonical 구조의 reader로 업데이트

**Priority**: High
**Target Section**: `_sdd/spec/components.md` > `spec-review`, `spec-summary`, `spec-rewrite`

**Current State**:

- `spec-review`, `spec-summary`, `spec-rewrite`는 여전히 old whitepaper assumptions를 내포한다.
- review rubric과 summary projection은 `architecture/component detail이 본문 기본 구조`라는 옛 전제를 일부 유지한다.
- rewrite reference와 example은 새 global/temporary 비대칭 구조를 기준으로 평가하지 않는다.

**Proposed**:

- `spec-review`가 CIV 섹션, decision-bearing structure, appendix-level code map, temporary 7-section schema를 기준으로 quality/drift를 판단하도록 바꾼다.
- `spec-summary`는 global spec의 새 canonical outline을 반영하고, temporary spec은 delta/execution 문서로 요약하도록 조정한다.
- `spec-rewrite`는 `spec-as-whitepaper`를 더 두꺼운 서사 문서가 아니라 `얇은 글로벌 스펙 + appendix + explicit CIV` 기준으로 재정의한다.
- 관련 reference/example/template를 모두 업데이트한다.

**Reason**:

reader skill이 old model을 유지하면, 생성된 새 문서를 오히려 잘못된 기준으로 판단하게 된다.

### Improvement: planning / update / orchestration skillchain을 temporary spec 실행 청사진 모델에 맞게 정렬

**Priority**: High
**Target Section**: `_sdd/spec/components.md` > `feature-draft`, `implementation-plan`, `spec-update-todo`, `spec-update-done`, `sdd-autopilot`

**Current State**:

- `feature-draft` Part 1/Part 2 구조는 temporary spec 7섹션 schema를 직접 모델링하지 않는다.
- `implementation-plan`은 contract/invariant delta ID를 전제로 하지 않는다.
- `spec-update-todo` / `spec-update-done`은 global spec의 새 section model과 temporary delta model 차이를 명시적으로 다루지 않는다.
- `sdd-autopilot` reasoning reference는 old canonical structure를 기준으로 파이프라인을 조립한다.

**Proposed**:

- `feature-draft`가 `Scope Delta`, `Contract/Invariant Delta`, `Touchpoints`, `Validation Plan`, `Risks / Open Questions`를 임시 스펙적 관점에서 더 직접적으로 생성하도록 지시를 강화한다.
- `implementation-plan`이 `Contract/Invariant Delta` ID를 받아 plan/phase/validation 연결을 유지하도록 바꾼다.
- `spec-update-todo`와 `spec-update-done`은 global spec 본문과 appendix, temporary delta 문서 간 변환 규칙을 새 model에 맞게 재정의한다.
- `sdd-autopilot` reference는 생성/소비/검증 단계가 모두 새 canonical model을 전제로 reasoning하도록 수정한다.
- mirror/agent 파일이 있는 skill은 agent와 wrapper를 함께 동기화한다.
- temporary spec template과 example은 `Contract/Invariant Delta`와 `Validation Plan` 사이의 ID 매핑을 compact example로 직접 보여준다.

**Reason**:

temporary spec을 실행 청사진으로 재정의했으므로, planning 계층도 delta와 validation mapping을 직접 다룰 수 있어야 한다.

### Improvement: `docs/` 안내 문서를 새 canonical model의 설명 계층으로 재작성

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Usage Guide & Expected Results`; supporting `_sdd/spec/usage-guide.md`

**Current State**:

- `docs/SDD_WORKFLOW.md`, `docs/SDD_QUICK_START.md`, `docs/SDD_CONCEPT.md`, `docs/sdd.md`는 부분적으로 old whitepaper §1-§8 또는 architecture/component-heavy model을 설명한다.
- 일부 문서는 skill behavior보다 앞서거나 뒤처질 위험이 있다.

**Proposed**:

- `docs/SDD_WORKFLOW.md`는 새 canonical model, CIV 중심 검증, global/temporary 비대칭 구조, skills-first sync order를 설명한다.
- `docs/SDD_QUICK_START.md`는 새 global/temporary 구조와 skillchain 순서를 짧게 반영한다.
- `docs/SDD_CONCEPT.md`는 global spec을 inventory 문서가 아닌 기준 문서로 다시 설명한다.
- `docs/sdd.md`는 상위 철학 문서로서 contract/invariant/verifiability와 새 operational shape를 연결한다.

**Reason**:

human-facing docs는 skill behavior를 설명해야지, 이미 폐기한 canonical model을 계속 가르치면 안 된다.

### Improvement: 영문 미러와 예시/reference 자산을 새 model로 정렬

**Priority**: Medium
**Target Section**: `_sdd/spec/main.md` > `Architecture Overview > Documentation Artifacts`

**Current State**:

- `docs/en/*`는 old definition을 유지한다.
- 일부 example/reference 문서는 여전히 `whitepaper §1-§8` wording과 old section map을 기준으로 한다.

**Proposed**:

- `docs/en/SDD_SPEC_DEFINITION.md`, `docs/en/SDD_WORKFLOW.md`, `docs/en/SDD_QUICK_START.md`, `docs/en/SDD_CONCEPT.md`를 새 canonical model로 동기화한다.
- `docs/en/sdd.md`를 새로 생성하여 한국어 `docs/sdd.md`와 같은 철학 계층을 영어 surface에도 제공한다.
- skill examples/references 중 old canonical assumptions를 담은 자산을 함께 갱신한다.
- `.codex/`와 `.claude/` reference/example 쌍의 drift를 정리한다.

**Reason**:

영문 미러와 예시가 옛 모델을 유지하면, 이후 사용자/LLM이 다시 old pattern을 학습하게 된다.

## Failure Modes

| 시나리오 | 실패 시 | 사용자 가시성 | 처리 방안 |
|---------|---------|-------------|----------|
| 생성/변환 스킬보다 docs를 먼저 갱신 | 문서 설명과 실제 skill output이 어긋남 | 사용자가 새 구조를 기대하지만 old output 생성 | rollout order를 `definition -> skills -> docs -> mirrors/examples`로 강제 |
| `.codex/`와 `.claude/` mirror/agent 동기화 누락 | 플랫폼별 spec behavior 불일치 | 한 플랫폼에서는 새 구조, 다른 플랫폼에서는 옛 구조 | task별로 mirror write set을 명시하고 pair review 수행 |
| example/reference 자산 미갱신 | 새 스킬이 옛 예시를 참조하며 drift 재발 | generated output에 old section names 잔존 | generator/consumer task에 examples/reference를 함께 포함 |
| CIV schema는 도입됐지만 review/plan layer가 ID를 소비하지 못함 | contract/invariant 추적성 끊김 | validation plan이 contract delta와 연결되지 않음 | feature-draft, implementation-plan, spec-review, autopilot reference를 같은 phase에서 동기화 |
| global/temporary 비대칭 구조를 일부 skill만 이해 | update/review/orchestration 단계에서 schema 충돌 | spec-update-todo/done 또는 summary가 잘못된 섹션 기대 | temporary 7섹션과 global canonical outline을 reasoning reference에 명시 |

## Notes

- 이 rollout은 branch `feat/review-sdd-definition` 위에서 진행한다.
- `docs/SDD_SPEC_DEFINITION.md`는 이미 새 canonical definition으로 수정되었고, 이번 draft는 그 downstream sync를 계획한다.
- `spec-create` / `spec-upgrade`보다 `docs/`를 먼저 수정하지 않는다.
- `strategic code map`의 기본 운영 방식은 manual curated다.
- temporary spec 템플릿에는 `Contract/Invariant Delta`와 `Validation Plan`의 ID 매핑을 보여 주는 compact example을 포함한다.
- `docs/en/sdd.md`는 Phase 4에서 생성한다.

## Open Questions

- 현재 없음

<!-- spec-update-todo-input-end -->

---

# Part 2: Implementation Plan

## Overview

새 `SDD_SPEC_DEFINITION.md`를 실제 시스템의 canonical contract로 만들기 위해, 생성/변환 스킬, 소비/검증/계획 스킬, human-facing docs, 영문 미러/예시를 순차적으로 동기화한다. 핵심 원칙은 `definition -> generators/transformers -> consumers/planners -> docs -> mirrors/examples -> validation` 순서다.

## Scope

### In Scope

- `.codex/skills`와 `.claude/skills`의 spec 관련 skill instruction sync
- mirror notice가 있는 `.codex/agents/*.toml`, `.claude/agents/*.md` 동기화
- `spec-create`, `spec-upgrade` template/reference/example 재설계
- `spec-review`, `spec-summary`, `spec-rewrite`, `feature-draft`, `implementation-plan`, `spec-update-todo`, `spec-update-done`, `sdd-autopilot` 새 canonical model 대응
- `docs/` 한국어 안내 문서 sync
- `docs/en/` 영문 미러 문서 sync
- rollout 후 cross-surface drift review 리포트 작성

### Out of Scope

- 기존 사용자 프로젝트 스펙 일괄 migration
- spec 외 unrelated skill의 기능 변경
- strategic code map 자동 생성 도구 구현
- `_sdd/spec/main.md` 자체의 대규모 재작성

## Components

1. **Generator / Transformer Layer**: `spec-create`, `spec-upgrade`, template-compact/full, spec-format, upgrade-mapping, examples
2. **Consumer / Review Layer**: `spec-review`, `spec-summary`, `spec-rewrite`
3. **Planning / Update / Orchestration Layer**: `feature-draft`, `implementation-plan`, `spec-update-todo`, `spec-update-done`, `sdd-autopilot`
4. **Korean Docs Layer**: `docs/SDD_WORKFLOW.md`, `docs/SDD_QUICK_START.md`, `docs/SDD_CONCEPT.md`, `docs/sdd.md`
5. **English Mirror Layer**: `docs/en/*`, including new `docs/en/sdd.md`
6. **Validation Layer**: repo-wide drift search + final spec review report

## Implementation Phases

### Phase 1: Generator / Transformer Canonicalization

`spec-create`와 `spec-upgrade`가 새 global/temporary canonical structure를 실제로 생성하고 변환할 수 있게 만든다.

### Phase 2: Consumer / Planning Skillchain Realignment

review, summary, rewrite, draft, planning, update, orchestration skill이 새 canonical model을 읽고 쓰게 만든다.

### Phase 3: Human-Facing Docs Sync

한국어 docs를 skill behavior 기준으로 재작성한다.

### Phase 4: English Mirror and Validation

영문 미러를 동기화하고, old canonical references 잔존 여부를 최종 점검한다.

## Task Details

### Task FD-01: Codex generator/transformer layer를 새 canonical model로 전환
**Component**: Generator / Transformer Layer
**Priority**: P0
**Type**: Refactor

**Description**: Codex용 `spec-create`와 `spec-upgrade`를 새 global/temporary spec model 기준으로 재작성한다. §1-§8 canonical assumption을 제거하고, CIV, decision-bearing structure, appendix-level strategic code map, temporary 7-section schema를 반영한다.

**Acceptance Criteria**:
- [ ] `.codex/skills/spec-create/`가 새 global spec structure와 temporary spec concept를 기준으로 설명한다.
- [ ] `.codex/skills/spec-upgrade/`가 더 이상 `whitepaper §1-§8` conversion을 canonical goal로 말하지 않는다.
- [ ] codex reference templates가 `Contract / Invariants / Verifiability`와 appendix-level `Strategic Code Map`을 포함한다.
- [ ] codex templates/examples가 strategic code map을 manual curated appendix로 다룬다.
- [ ] codex examples가 old section map 대신 새 canonical structure를 보여준다.

**Target Files**:
- [M] `.codex/skills/spec-create/SKILL.md`
- [M] `.codex/skills/spec-create/references/template-compact.md`
- [M] `.codex/skills/spec-create/references/template-full.md`
- [M] `.codex/skills/spec-create/examples/simple-project-spec.md`
- [M] `.codex/skills/spec-create/examples/complex-project-spec.md`
- [M] `.codex/skills/spec-create/examples/additional-specs.md`
- [M] `.codex/skills/spec-upgrade/SKILL.md`
- [M] `.codex/skills/spec-upgrade/skill.json`
- [M] `.codex/skills/spec-upgrade/references/template-compact.md`
- [M] `.codex/skills/spec-upgrade/references/template-full.md`
- [M] `.codex/skills/spec-upgrade/references/spec-format.md`
- [M] `.codex/skills/spec-upgrade/references/upgrade-mapping.md`
- [M] `.codex/skills/spec-upgrade/examples/before-upgrade.md`
- [M] `.codex/skills/spec-upgrade/examples/after-upgrade.md`

**Technical Notes**: `spec-upgrade`는 migration semantics를 다시 써야 하므로, description/AC/process/reference/example을 한 번에 바꾸는 편이 낫다.
**Dependencies**: `docs/SDD_SPEC_DEFINITION.md`

### Task FD-02: Claude generator/transformer mirror를 Codex canonical semantics에 맞춰 동기화
**Component**: Generator / Transformer Layer
**Priority**: P0
**Type**: Refactor

**Description**: Claude용 `spec-create` / `spec-upgrade` 자산을 Codex와 동일한 canonical semantics로 맞춘다. 플랫폼별 표현 차이는 허용하되, spec shape와 migration semantics는 동일해야 한다.

**Acceptance Criteria**:
- [ ] `.claude/skills/spec-create/`와 `.claude/skills/spec-upgrade/`가 codex와 같은 canonical structure를 전제로 한다.
- [ ] template/reference/example drift가 codex 쌍과 비교했을 때 실질적으로 해소된다.
- [ ] `whitepaper §1-§8` canonical wording이 claude generator/upgrade layer에서 제거된다.

**Target Files**:
- [M] `.claude/skills/spec-create/SKILL.md`
- [M] `.claude/skills/spec-create/references/template-compact.md`
- [M] `.claude/skills/spec-create/references/template-full.md`
- [M] `.claude/skills/spec-create/examples/simple-project-spec.md`
- [M] `.claude/skills/spec-create/examples/complex-project-spec.md`
- [M] `.claude/skills/spec-create/examples/additional-specs.md`
- [M] `.claude/skills/spec-upgrade/SKILL.md`
- [M] `.claude/skills/spec-upgrade/skill.json`
- [M] `.claude/skills/spec-upgrade/references/template-compact.md`
- [M] `.claude/skills/spec-upgrade/references/template-full.md`
- [M] `.claude/skills/spec-upgrade/references/spec-format.md`
- [M] `.claude/skills/spec-upgrade/references/upgrade-mapping.md`
- [M] `.claude/skills/spec-upgrade/examples/before-upgrade.md`
- [M] `.claude/skills/spec-upgrade/examples/after-upgrade.md`

**Technical Notes**: Codex task 완료 후 semantic parity 체크리스트를 기준으로 이식하는 것이 안전하다.
**Dependencies**: Task FD-01

### Task FD-03: Consumer / review layer를 새 canonical quality rubric으로 재정렬
**Component**: Consumer / Review Layer
**Priority**: P0
**Type**: Refactor

**Description**: `spec-review`, `spec-summary`, `spec-rewrite`가 새 canonical global/temporary 구조, CIV 섹션, decision-bearing structure, appendix-level code map을 기준으로 읽고 평가하도록 수정한다.

**Acceptance Criteria**:
- [ ] `spec-review`가 CIV, global/temporary asymmetry, appendix code map, decision-bearing structure를 quality/drift dimension으로 본다.
- [ ] `spec-summary`가 global spec과 temporary spec을 다른 방식으로 요약한다.
- [ ] `spec-rewrite` rubric이 old whitepaper §1-§8보다 새 canonical model을 우선한다.
- [ ] mirror notice가 있는 파일은 agent와 wrapper가 함께 동기화된다.

**Target Files**:
- [M] `.codex/skills/spec-review/SKILL.md`
- [M] `.codex/agents/spec-review.toml`
- [M] `.claude/skills/spec-review/SKILL.md`
- [M] `.claude/agents/spec-review.md`
- [M] `.codex/skills/spec-summary/SKILL.md`
- [M] `.codex/skills/spec-summary/references/summary-template.md`
- [M] `.codex/skills/spec-summary/examples/summary-output.md`
- [M] `.claude/skills/spec-summary/SKILL.md`
- [M] `.claude/skills/spec-summary/references/summary-template.md`
- [M] `.claude/skills/spec-summary/examples/summary-output.md`
- [M] `.codex/skills/spec-rewrite/SKILL.md`
- [M] `.codex/skills/spec-rewrite/references/spec-format.md`
- [M] `.codex/skills/spec-rewrite/references/rewrite-checklist.md`
- [M] `.codex/skills/spec-rewrite/references/template-compact.md`
- [M] `.codex/skills/spec-rewrite/examples/rewrite-plan.md`
- [M] `.codex/skills/spec-rewrite/examples/rewrite-report.md`
- [M] `.claude/skills/spec-rewrite/SKILL.md`
- [M] `.claude/skills/spec-rewrite/references/spec-format.md`
- [M] `.claude/skills/spec-rewrite/references/rewrite-checklist.md`
- [M] `.claude/skills/spec-rewrite/references/template-compact.md`
- [M] `.claude/skills/spec-rewrite/examples/rewrite-plan.md`
- [M] `.claude/skills/spec-rewrite/examples/rewrite-report.md`

**Technical Notes**: `spec-review`는 새 canonical doc을 실제 품질 기준으로 읽어야 하므로, report output wording도 함께 바뀔 가능성이 크다.
**Dependencies**: Task FD-01, Task FD-02

### Task FD-04: Planning / update / orchestration layer를 temporary spec 실행 청사진 모델로 전환
**Component**: Planning / Update / Orchestration Layer
**Priority**: P0
**Type**: Refactor

**Description**: `feature-draft`, `implementation-plan`, `spec-update-todo`, `spec-update-done`, `sdd-autopilot`이 새 temporary spec model을 쓰고 읽도록 수정한다. 특히 `Contract/Invariant Delta`, `Touchpoints`, `Validation Plan`, CIV ID 연결을 명시적으로 다룬다.

**Acceptance Criteria**:
- [ ] `feature-draft`가 temporary spec 7섹션을 암묵적으로라도 직접 모델링한다.
- [ ] `implementation-plan`이 contract/invariant delta와 validation linkage를 읽을 수 있다.
- [ ] `spec-update-todo` / `spec-update-done`이 global spec과 temporary spec의 비대칭 구조를 설명하고 처리한다.
- [ ] `sdd-autopilot` reasoning reference가 새 canonical model을 기반으로 pipeline을 조립한다.
- [ ] temporary spec 관련 template/example이 `Contract/Invariant Delta`와 `Validation Plan`의 ID 매핑 compact example을 포함한다.
- [ ] mirror notice가 있는 codex skill은 agent file과 함께 업데이트된다.

**Target Files**:
- [M] `.codex/skills/feature-draft/SKILL.md`
- [M] `.codex/agents/feature-draft.toml`
- [M] `.claude/skills/feature-draft/SKILL.md`
- [M] `.claude/agents/feature-draft.md`
- [M] `.codex/skills/implementation-plan/SKILL.md`
- [M] `.codex/agents/implementation-plan.toml`
- [M] `.claude/skills/implementation-plan/SKILL.md`
- [M] `.claude/agents/implementation-plan.md`
- [M] `.codex/skills/spec-update-todo/SKILL.md`
- [M] `.codex/agents/spec-update-todo.toml`
- [M] `.claude/skills/spec-update-todo/SKILL.md`
- [M] `.claude/agents/spec-update-todo.md`
- [M] `.codex/skills/spec-update-done/SKILL.md`
- [M] `.codex/agents/spec-update-done.toml`
- [M] `.claude/skills/spec-update-done/SKILL.md`
- [M] `.claude/agents/spec-update-done.md`
- [M] `.codex/skills/sdd-autopilot/SKILL.md`
- [M] `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md`
- [M] `.codex/skills/sdd-autopilot/references/orchestrator-contract.md`
- [M] `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md`
- [M] `.claude/skills/sdd-autopilot/SKILL.md`
- [M] `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md`
- [M] `.claude/skills/sdd-autopilot/references/orchestrator-contract.md`
- [M] `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md`

**Technical Notes**: `feature-draft`는 temporary spec을 직접 생성하는 핵심 진입점이므로, wording drift를 허용하면 하위 skill 전체가 다시 old model로 끌려간다.
**Dependencies**: Task FD-01, Task FD-02, Task FD-03

### Task FD-05: Korean docs를 새 canonical model의 설명 계층으로 재작성
**Component**: Korean Docs Layer
**Priority**: P1
**Type**: Documentation

**Description**: 한국어 docs를 새 canonical model과 실제 skill behavior에 맞게 다시 쓴다. 특히 old whitepaper §1-§8 canonical framing, architecture/component-heavy default framing, docs-first 설명 순서를 제거한다.

**Acceptance Criteria**:
- [ ] `docs/SDD_WORKFLOW.md`가 새 global/temporary structure와 skills-first rollout order를 설명한다.
- [ ] `docs/SDD_QUICK_START.md`가 새 canonical definition을 짧게 전달한다.
- [ ] `docs/SDD_CONCEPT.md`가 global spec을 inventory 문서가 아닌 기준 문서로 설명한다.
- [ ] `docs/sdd.md`가 contract / invariant / verifiability와 새 operational model을 연결한다.
- [ ] 한국어 docs가 현재 skill behavior와 모순되지 않는다.

**Target Files**:
- [M] `docs/SDD_WORKFLOW.md`
- [M] `docs/SDD_QUICK_START.md`
- [M] `docs/SDD_CONCEPT.md`
- [M] `docs/sdd.md`

**Technical Notes**: `docs/SDD_SPEC_DEFINITION.md`는 이미 기준 문서로 수정되어 있으므로, 이 task는 그 하위 설명 문서를 동기화하는 역할에 집중한다.
**Dependencies**: Task FD-03, Task FD-04

### Task FD-06: English mirrors를 동기화하고 남은 old canonical references를 정리
**Component**: English Mirror Layer
**Priority**: P1
**Type**: Documentation

**Description**: 영문 미러 문서를 한국어 canonical docs와 같은 수준으로 맞춘다. 번역 수준이 아니라 semantic parity가 목표다.

**Acceptance Criteria**:
- [ ] `docs/en/SDD_SPEC_DEFINITION.md`가 새 canonical definition을 반영한다.
- [ ] `docs/en/SDD_WORKFLOW.md`, `docs/en/SDD_QUICK_START.md`, `docs/en/SDD_CONCEPT.md`가 한국어 원문과 동일한 model을 설명한다.
- [ ] `docs/en/sdd.md`가 생성되고, 한국어 `docs/sdd.md`와 철학 계층에서 semantic parity를 가진다.
- [ ] 영문 문서에서 old `whitepaper §1-§8` canonical wording이 제거되거나 재해석된다.

**Target Files**:
- [M] `docs/en/SDD_SPEC_DEFINITION.md`
- [M] `docs/en/SDD_WORKFLOW.md`
- [M] `docs/en/SDD_QUICK_START.md`
- [M] `docs/en/SDD_CONCEPT.md`
- [C] `docs/en/sdd.md`

**Technical Notes**: 영어 독자도 self-contained philosophy surface를 가져야 하므로 `docs/en/sdd.md`를 이번 rollout에서 함께 생성한다.
**Dependencies**: Task FD-05

### Task FD-07: Cross-surface drift audit와 rollout verification 수행
**Component**: Validation Layer
**Priority**: P1
**Type**: Test

**Description**: 전체 rollout 후 repo-wide search와 spec review를 수행해 old canonical references, mirror drift, docs-skill mismatch를 정리한다.

**Acceptance Criteria**:
- [ ] target surfaces에서 `whitepaper §1-§8` canonical wording이 제거되거나 의도적으로 재해석되었다.
- [ ] `.codex/`와 `.claude/` mirror pair가 필요한 범위에서 동기화되었다.
- [ ] docs와 skills가 `SDD_SPEC_DEFINITION.md`와 모순되지 않는다.
- [ ] 최종 review report가 생성된다.

**Target Files**:
- [C] `_sdd/spec/logs/spec_review_report_canonical_model_rollout.md`

**Technical Notes**: validation은 검색(`rg`) + spot review + final spec-review report 조합으로 수행한다.
**Dependencies**: Task FD-06

## Parallel Execution Summary

- Phase 1에서는 Task FD-01이 canonical semantics를 먼저 확정하고, Task FD-02는 그 결과를 Claude mirror로 이식하는 순서가 안전하다.
- Phase 2에서는 Task FD-03과 Task FD-04가 개념적으로 병렬화 가능하지만, 둘 다 Phase 1의 새 template semantics를 전제로 하므로 FD-01/02 후에 시작해야 한다.
- Phase 3의 Korean docs sync(Task FD-05)는 skill behavior가 정리된 뒤 수행해야 하므로 FD-03/04 이후가 적절하다.
- Phase 4의 English mirror sync(Task FD-06)는 Korean docs wording이 안정된 뒤 진행하는 것이 drift를 줄인다.
- 최종 audit(Task FD-07)는 모든 수정이 끝난 뒤 단일 verification pass로 수행한다.

## Risks and Mitigations

1. **Risk**: generator layer보다 docs를 먼저 바꿔 설명과 실제 output이 갈라질 수 있다.
   **Mitigation**: FD-01/02/03/04 완료 전에는 docs task를 시작하지 않는다.

2. **Risk**: `.codex/`와 `.claude/` 쌍이 부분적으로만 업데이트되어 platform drift가 생길 수 있다.
   **Mitigation**: mirror/agent pair를 task target files에 명시하고, FD-07에서 pairwise review를 수행한다.

3. **Risk**: old examples/reference가 남아 future generation을 다시 old model로 끌어갈 수 있다.
   **Mitigation**: generator/consumer/orchestrator tasks에 example/reference 파일을 함께 포함한다.

4. **Risk**: CIV schema는 도입됐지만 planning/update layer가 ID를 활용하지 못할 수 있다.
   **Mitigation**: FD-04에서 feature-draft, implementation-plan, spec-update-todo/done, autopilot reference를 함께 갱신한다.

5. **Risk**: temporary spec 7섹션 구조가 일부 skill에서 암묵적으로만 적용되어 명시성이 떨어질 수 있다.
   **Mitigation**: FD-04 acceptance criteria에 delta/touchpoints/validation linkage를 직접 넣고, FD-07에서 output contract drift를 재검토한다.

6. **Risk**: strategic code map을 반자동 생성 전제로 설계하면 appendix 품질이 inventory 나열로 다시 무너질 수 있다.
   **Mitigation**: 이번 rollout에서는 manual curated를 canonical default로 고정하고, 자동 생성은 후속 별도 기능으로 분리한다.

## Open Questions

- 없음
