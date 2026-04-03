# Implementation Plan: SDD Canonical Model Rollout

## Overview

`docs/SDD_SPEC_DEFINITION.md`에서 확정한 새 canonical model을 실제 시스템 전반에 반영한다. 구현 대상은 생성/변환 스킬, 소비/검증/계획 스킬, 한국어 docs, 영문 미러, 최종 drift audit까지다.

이번 작업은 문서만 바꾸는 마이그레이션이 아니라, 스킬이 생성하고 읽고 검증하는 contract 자체를 바꾸는 rollout이다. 따라서 실행 순서는 `definition -> generators/transformers -> consumers/planners -> docs -> english mirrors -> audit`로 고정한다.

작업 브랜치는 `feat/review-sdd-definition`이다. `docs/SDD_SPEC_DEFINITION.md`는 이미 수정되었고, 이번 plan에서는 이를 입력 계약으로 취급한다.

테스트 관점에서는 전통적인 `tests/` 디렉토리가 확인되지 않았다. 따라서 phase별 검증은 다음 조합으로 수행한다.

- target file diff spot review
- `.codex/` / `.claude/` mirror parity review
- `rg` 기반 old canonical wording 탐색
- 최종 spec review report 작성

## Scope

### In Scope

- `.codex/skills` generator/transformer 레이어를 새 canonical global/temporary model에 맞게 재작성
- `.claude/skills` generator/transformer mirror를 Codex와 semantic parity로 동기화
- `spec-review`, `spec-summary`, `spec-rewrite`를 새 CIV + global/temporary asymmetry rubric으로 재정렬
- `feature-draft`, `implementation-plan`, `spec-update-todo`, `spec-update-done`, `sdd-autopilot`을 temporary spec 실행 청사진 모델로 전환
- `docs/SDD_WORKFLOW.md`, `docs/SDD_QUICK_START.md`, `docs/SDD_CONCEPT.md`, `docs/sdd.md` 동기화
- `docs/en/SDD_*` 동기화 및 `docs/en/sdd.md` 생성
- repo-wide drift audit 및 최종 review report 작성

### Out of Scope

- 기존 사용자 프로젝트 스펙 일괄 migration
- spec 관련이 아닌 unrelated skill behavior 변경
- strategic code map 자동 생성 도구 구현
- `_sdd/spec/main.md` 자체의 대규모 재작성
- legacy uppercase implementation artifact 정리 작업

## Components

1. **Generator / Transformer Layer**: `spec-create`, `spec-upgrade`, template/reference/example
2. **Consumer / Review Layer**: `spec-review`, `spec-summary`, `spec-rewrite`
3. **Planning / Update / Orchestration Layer**: `feature-draft`, `implementation-plan`, `spec-update-todo`, `spec-update-done`, `sdd-autopilot`
4. **Korean Docs Layer**: `docs/SDD_WORKFLOW.md`, `docs/SDD_QUICK_START.md`, `docs/SDD_CONCEPT.md`, `docs/sdd.md`
5. **English Mirror Layer**: `docs/en/SDD_*`, `docs/en/sdd.md`
6. **Validation Layer**: repo-wide grep audit, mirror parity review, final report

## Implementation Phases

**Strategy**: Dependency-Driven

선택 이유:

- 새 canonical semantics를 먼저 generator/transformer에 반영하지 않으면 이후 consumer와 docs가 거짓말이 된다.
- consumer/planning layer는 generator layer의 새 구조를 전제로 읽어야 한다.
- docs는 실제 skill behavior가 안정된 뒤에만 정확하게 다시 쓸 수 있다.
- english mirror와 final audit은 한국어 원문 및 실제 skill behavior가 고정된 뒤 수행하는 편이 drift를 줄인다.

### Phase 1: Generator / Transformer Canonicalization

목표: `spec-create`와 `spec-upgrade`가 새 global/temporary canonical shape를 실제로 생성하고 변환하게 만든다.

포함 task:

- FD-01
- FD-02

Phase Exit Criteria:

- `spec-create`와 `spec-upgrade` 양쪽 플랫폼이 더 이상 `whitepaper §1-§8`를 canonical goal로 설명하지 않는다.
- template/example이 `Contract / Invariants / Verifiability`, decision-bearing structure, appendix-level strategic code map, temporary 7-section schema를 반영한다.
- strategic code map은 manual curated appendix로 취급된다.

### Phase 2: Consumer / Planning Skillchain Realignment

목표: reader, reviewer, planner, updater, orchestrator가 새 canonical model을 읽고 쓰게 만든다.

포함 task:

- FD-03
- FD-04

Phase Exit Criteria:

- `spec-review`, `spec-summary`, `spec-rewrite`가 새 quality rubric을 사용한다.
- `feature-draft`, `implementation-plan`, `spec-update-todo`, `spec-update-done`, `sdd-autopilot`이 temporary spec의 delta/validation linkage를 다룬다.
- CIV ID와 temporary delta linkage가 문서와 예시에서 모두 확인된다.

### Phase 3: Korean Docs Sync

목표: 한국어 안내 문서가 새 skill behavior와 canonical definition을 설명하게 만든다.

포함 task:

- FD-05

Phase Exit Criteria:

- `docs/SDD_WORKFLOW.md`와 `docs/SDD_QUICK_START.md`가 더 이상 `spec-upgrade = §1-§8 migration`을 설명하지 않는다.
- `docs/SDD_CONCEPT.md`와 `docs/sdd.md`가 global/temporary asymmetry와 CIV 중심 모델을 설명한다.

### Phase 4: English Mirror Sync

목표: 영문 surface가 한국어 문서와 같은 model을 설명하도록 맞추고, 영어 self-contained philosophy doc를 추가한다.

포함 task:

- FD-06

Phase Exit Criteria:

- `docs/en/SDD_SPEC_DEFINITION.md`, `docs/en/SDD_WORKFLOW.md`, `docs/en/SDD_QUICK_START.md`, `docs/en/SDD_CONCEPT.md`가 새 canonical model을 설명한다.
- `docs/en/sdd.md`가 생성된다.

### Phase 5: Drift Audit and Closeout

목표: rollout 후 잔존 old wording, mirror drift, low-impact collateral references를 정리하고 최종 review report를 남긴다.

포함 task:

- FD-07

Phase Exit Criteria:

- 주요 target surfaces에서 old `whitepaper §1-§8` canonical wording이 제거되거나 의도적으로 재해석된다.
- `.codex/`와 `.claude/` mirror pair가 필요한 범위에서 동기화되었다.
- 최종 review report가 생성된다.

## Task Details

### Task FD-01: Codex generator/transformer layer를 새 canonical model로 재작성
**Component**: Generator / Transformer Layer
**Priority**: P0
**Type**: Refactor

**Description**: Codex용 `spec-create`와 `spec-upgrade`를 새 canonical global/temporary model 기준으로 다시 쓴다. old `§1-§8` canonical assumption을 제거하고, CIV, decision-bearing structure, appendix-level strategic code map, temporary 7-section schema를 생성 규칙에 반영한다.

**Acceptance Criteria**:
- [ ] `.codex/skills/spec-create/SKILL.md`가 새 global spec structure와 temporary spec concept를 기준으로 설명한다.
- [ ] `.codex/skills/spec-upgrade/`가 더 이상 `whitepaper §1-§8 형식으로 변환`을 canonical goal로 말하지 않는다.
- [ ] codex template/reference/example이 `Contract / Invariants / Verifiability`, decision-bearing structure, appendix-level `Strategic Code Map`을 반영한다.
- [ ] strategic code map은 manual curated appendix로 설명된다.
- [ ] temporary spec 예시 또는 설명에 `Change Summary`, `Scope Delta`, `Contract/Invariant Delta`, `Touchpoints`, `Implementation Plan`, `Validation Plan`, `Risks / Open Questions`가 드러난다.

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

**Technical Notes**: `spec-upgrade`는 migration semantics 자체가 바뀌므로 description, AC, process, reference, examples를 한 번에 수정하는 편이 안전하다. 테스트 디렉토리는 없으므로 verification은 template/example spot review와 `rg` 탐색 중심으로 수행한다.
**Dependencies**: `docs/SDD_SPEC_DEFINITION.md`

### Task FD-02: Claude generator/transformer mirror를 Codex canonical semantics에 맞춰 동기화
**Component**: Generator / Transformer Layer
**Priority**: P0
**Type**: Refactor

**Description**: Claude용 `spec-create` / `spec-upgrade` 자산을 Codex와 같은 canonical semantics로 맞춘다. 플랫폼별 표현 차이는 허용하되, spec shape와 migration semantics는 동일해야 한다.

**Acceptance Criteria**:
- [ ] `.claude/skills/spec-create/`와 `.claude/skills/spec-upgrade/`가 codex와 같은 canonical structure를 전제로 한다.
- [ ] template/reference/example drift가 codex 쌍과 비교했을 때 해소된다.
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

**Technical Notes**: Codex patch를 먼저 만든 뒤 semantic parity 체크리스트로 Claude에 이식하는 편이 drift를 줄인다. mirror review는 file-by-file diff rather than line-by-line copy를 권장한다.
**Dependencies**: FD-01

### Task FD-03: Consumer / review layer를 새 canonical quality rubric으로 재정렬
**Component**: Consumer / Review Layer
**Priority**: P0
**Type**: Refactor

**Description**: `spec-review`, `spec-summary`, `spec-rewrite`가 새 canonical global/temporary 구조, CIV 섹션, decision-bearing structure, appendix-level code map을 기준으로 읽고 평가하도록 수정한다.

**Acceptance Criteria**:
- [ ] `spec-review`가 CIV, global/temporary asymmetry, appendix code map, decision-bearing structure를 quality/drift dimension으로 본다.
- [ ] `spec-summary`가 global spec과 temporary spec을 다른 방식으로 요약한다.
- [ ] `spec-rewrite`가 old `whitepaper §1-§8` 중심 판단보다 새 canonical model을 우선한다.
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

**Technical Notes**: 이 레이어는 새 문서를 잘못된 기준으로 평가하면 안 되므로 wording뿐 아니라 report/summary output contract까지 같이 점검해야 한다.
**Dependencies**: FD-01, FD-02

### Task FD-04: Planning / update / orchestration layer를 temporary spec 실행 청사진 모델로 전환
**Component**: Planning / Update / Orchestration Layer
**Priority**: P0
**Type**: Refactor

**Description**: `feature-draft`, `implementation-plan`, `spec-update-todo`, `spec-update-done`, `sdd-autopilot`이 새 temporary spec model을 쓰고 읽도록 수정한다. 특히 `Contract/Invariant Delta`, `Touchpoints`, `Validation Plan`, CIV ID 연결을 명시적으로 다룬다.

**Acceptance Criteria**:
- [ ] `feature-draft`가 temporary spec 7섹션을 직접적으로 모델링한다.
- [ ] `implementation-plan`이 contract/invariant delta와 validation linkage를 읽고 phase/task에 연결할 수 있다.
- [ ] `spec-update-todo` / `spec-update-done`이 global spec과 temporary spec의 비대칭 구조를 설명하고 처리한다.
- [ ] `sdd-autopilot` reasoning reference가 새 canonical model을 기반으로 pipeline을 조립한다.
- [ ] temporary spec template/example이 `Contract/Invariant Delta`와 `Validation Plan`의 ID 매핑 compact example을 포함한다.
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

**Technical Notes**: `feature-draft`와 `implementation-plan`은 temporary spec shape를 가장 직접적으로 표면화하는 진입점이다. 여기서 wording drift를 허용하면 하위 skill 전체가 다시 old model로 끌려간다.
**Dependencies**: FD-01, FD-02, FD-03

### Task FD-05: Korean docs를 새 canonical model의 설명 계층으로 재작성
**Component**: Korean Docs Layer
**Priority**: P1
**Type**: Documentation

**Description**: 한국어 docs를 새 canonical model과 실제 skill behavior에 맞게 다시 쓴다. old `whitepaper §1-§8` canonical framing, architecture/component-heavy default framing, docs-first 설명 순서를 제거한다.

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

**Technical Notes**: `docs/SDD_SPEC_DEFINITION.md`는 이미 기준 문서로 수정되어 있으므로, 이 task는 하위 설명 계층을 동기화하는 역할에 집중한다.
**Dependencies**: FD-03, FD-04

### Task FD-06: English mirrors를 동기화하고 `docs/en/sdd.md`를 생성
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
**Dependencies**: FD-05

### Task FD-07: Cross-surface drift audit를 수행하고 잔여 저충격 참조를 정리
**Component**: Validation Layer
**Priority**: P1
**Type**: Test

**Description**: 전체 rollout 후 repo-wide search와 spec review를 수행해 old canonical references, mirror drift, docs-skill mismatch를 정리한다. audit 중 발견되는 low-impact collateral references는 같은 phase에서 정리한다.

**Acceptance Criteria**:
- [ ] 주요 target surfaces에서 old `whitepaper §1-§8` canonical wording이 제거되거나 의도적으로 재해석되었다.
- [ ] `.codex/`와 `.claude/` mirror pair가 필요한 범위에서 동기화되었다.
- [ ] `guide-create` 같은 collateral reference가 새 canonical model을 명백히 거스르지 않는다.
- [ ] docs와 skills가 `docs/SDD_SPEC_DEFINITION.md`와 모순되지 않는다.
- [ ] 최종 review report가 생성된다.

**Target Files**:
- [M] `.codex/skills/guide-create/references/template-compact.md`
- [M] `.claude/skills/guide-create/references/template-compact.md`
- [C] `_sdd/spec/logs/spec_review_report_canonical_model_rollout.md`

**Technical Notes**: validation은 `rg` + spot review + 최종 report 조합으로 수행한다. low-impact collateral cleanup은 audit 결과가 명확한 경우에만 수행하고, 범위가 커지면 follow-up task로 분리한다.
**Dependencies**: FD-06

## Parallel Execution Summary

| Phase | Tasks | Max Parallel | File Conflict Notes |
|------|-------|--------------|---------------------|
| 1 | FD-01, FD-02 | 1 | FD-02는 FD-01 결과를 mirror해야 하므로 순차가 안전 |
| 2 | FD-03, FD-04 | 2 | write set이 분리되어 있어 병렬 가능. 둘 다 Phase 1 완료 후 시작 |
| 3 | FD-05 | 1 | skill behavior 확정 후 수행 |
| 4 | FD-06 | 1 | 한국어 docs wording 안정화 후 수행 |
| 5 | FD-07 | 1 | 모든 수정 후 단일 verification pass |

실행 권장 순서:

1. Phase 1 완료
2. Phase 1 grep gate 통과 확인
3. Phase 2 병렬 또는 순차 수행
4. docs sync
5. english sync
6. final audit

## Risks and Mitigations

1. **Risk**: generator layer보다 docs를 먼저 바꾸면 설명과 실제 output이 갈라질 수 있다.  
   **Mitigation**: FD-01/02/03/04 완료 전에는 docs task를 시작하지 않는다.

2. **Risk**: `.codex/`와 `.claude/` 쌍이 부분적으로만 업데이트되어 platform drift가 생길 수 있다.  
   **Mitigation**: mirror/agent pair를 task target files에 명시하고, Phase 5에서 pairwise review를 수행한다.

3. **Risk**: old examples/reference가 남아 future generation을 다시 old model로 끌어갈 수 있다.  
   **Mitigation**: generator, consumer, orchestrator task에 example/reference 파일을 함께 포함한다.

4. **Risk**: CIV schema는 도입됐지만 planning/update layer가 ID를 활용하지 못할 수 있다.  
   **Mitigation**: FD-04에서 feature-draft, implementation-plan, spec-update-todo/done, autopilot reference를 함께 갱신한다.

5. **Risk**: temporary spec 7섹션 구조가 일부 skill에서 암묵적으로만 적용되어 명시성이 떨어질 수 있다.  
   **Mitigation**: FD-04 acceptance criteria에 delta/touchpoints/validation linkage를 직접 넣고, Phase 5에서 output contract drift를 재검토한다.

6. **Risk**: strategic code map을 반자동 생성 전제로 설계하면 appendix 품질이 inventory 나열로 다시 무너질 수 있다.  
   **Mitigation**: 이번 rollout에서는 manual curated를 canonical default로 고정하고, 자동 생성은 후속 별도 기능으로 분리한다.

7. **Risk**: secondary references like `guide-create` template가 old spec numbering을 계속 가르칠 수 있다.  
   **Mitigation**: Phase 5 audit에서 low-impact collateral references를 sweep하고, 범위가 커지면 follow-up task로 격리한다.

## Open Questions

- 없음
