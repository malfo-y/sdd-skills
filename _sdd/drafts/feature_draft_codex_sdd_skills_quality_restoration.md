# Feature Draft: Codex SDD 스킬 품질 복원 + 선별 재적용

**Date**: 2026-03-09
**Author**: Codex
**Target Spec**: `_sdd/spec/main.md`, `_sdd/spec/spec-lifecycle.md`, `_sdd/spec/implementation-lifecycle.md`
**Status**: Draft

---

# Part 1: Spec Patch Draft

> 이 패치는 `spec-update-todo` 입력으로 사용할 수 있습니다.

# Spec Update Input

**Date**: 2026-03-09
**Author**: Codex
**Target Spec**: `_sdd/spec/main.md`, `_sdd/spec/spec-lifecycle.md`, `_sdd/spec/implementation-lifecycle.md`
**Spec Update Classification**: MUST update

## Improvements

### Improvement: Codex SDD 스킬을 역사적 baseline 기준으로 복원
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Identified Issues & Improvements`
**Affected Components**: `Spec Lifecycle Skills`, `Delivery Lifecycle Skills`, `PR Lifecycle Skills`, `Platform Distribution`

**Current State**:
Codex SDD 스킬은 `919c734`, `9be85e7`, `0950a85`, `f7cce37`, `0b64041`를 거치며 simplified workflow, exploration-first 압축, explanation-first 보강이 겹쳐진 상태다. 구조 정렬은 좋아졌지만, 예시 기반 학습, 절차적 설명, before/after 감각, 구체적 change recipe가 baseline보다 얕아졌다.

**Proposed**:
`.codex/skills/`의 핵심 SDD 스킬을 `9be85e7`에 보존된 per-skill `prev/` snapshot 기준으로 path-scoped restore 한 뒤, 유효한 개선만 선별 재적용한다.

**Reason**:
누적 패치 위에 다시 설명을 덧붙이는 방식보다, 이해 가능한 baseline으로 돌아간 뒤 필요한 규칙만 얹는 편이 품질 회귀를 더 안정적으로 줄인다.

**Related Paths**:
- `.codex/skills/spec-create/`
- `.codex/skills/spec-review/`
- `.codex/skills/spec-rewrite/`
- `.codex/skills/spec-summary/`
- `.codex/skills/spec-update-todo/`
- `.codex/skills/spec-update-done/`
- `.codex/skills/feature-draft/`
- `.codex/skills/implementation-plan/`
- `.codex/skills/implementation/`
- `.codex/skills/implementation-review/`
- `.codex/skills/pr-spec-patch/`
- `.codex/skills/pr-review/`

### Improvement: Codex skill 유지보수 레시피를 "restore + selective reapply"로 명시
**Priority**: High
**Target Section**: `_sdd/spec/spec-lifecycle.md` > `Change Recipes`
**Affected Components**: `Spec Lifecycle Skills`, `Platform Distribution`

**Current State**:
현재 문서는 상위 앵커 변경 시 양 플랫폼을 함께 점검하라고는 하지만, Codex 쪽처럼 나중에 추가된 스킬과 unrelated 변경이 섞인 히스토리에서 어떤 복원 전략이 안전한지 충분히 고정하지 않는다.

**Proposed**:
Codex 스킬 복원은 blanket git revert 대신, historical snapshot 또는 path-scoped restore를 우선하고 그 위에 `Overview MUST`, drift/anchor 규칙, quality gate만 선별 재적용하는 패턴을 change recipe로 명시한다.

**Reason**:
Codex에는 `spec-snapshot` 같은 후속 추가 스킬이 있어 전체 revert가 과복원으로 이어질 위험이 있다.

**Related Paths**:
- `_sdd/spec/spec-lifecycle.md`
- `_sdd/spec/main.md`
- `.codex/skills/`

### Improvement: Codex SDD 스킬에서 simplified 4-step workflow 참조 제거
**Priority**: Medium
**Target Section**: `_sdd/spec/implementation-lifecycle.md` > `Interfaces / Contracts`
**Affected Components**: `Delivery Lifecycle Skills`, `Spec Lifecycle Skills`, `PR Lifecycle Skills`

**Current State**:
여러 Codex 스킬에 `spec -> feature-draft -> implementation -> spec-update-done` 식의 4단계 파이프라인이 남아 있어, 사용자가 자유롭게 스킬을 조합하는 실제 유지보수 방식과 충돌한다.

**Proposed**:
복원 후 Codex 스킬들에서 4단계 workflow 설명을 제거하고, 필요하면 상호 의존 관계만 간결하게 남긴다.

**Reason**:
사용자 결정사항이며, workflow 강제가 개별 스킬의 설명 공간을 압축하는 원인 중 하나였다.

**Related Paths**:
- `.codex/skills/spec-create/SKILL.md`
- `.codex/skills/feature-draft/SKILL.md`
- `.codex/skills/implementation-plan/SKILL.md`
- `.codex/skills/implementation/SKILL.md`
- `.codex/skills/implementation-review/SKILL.md`
- `.codex/skills/spec-update-done/SKILL.md`

## Notes

### Context
- 근거 토론: `_sdd/discussion/discussion_spec_create_quality_regression.md`
- Codex 대규모 구조 전환의 핵심 커밋은 `9be85e7`이며, 이 커밋 안에 per-skill `prev/` snapshot이 남아 있다.
- 후속 커밋 `0950a85`, `f7cce37`, `0b64041`에는 유지할 가치가 있는 변화와 되돌릴 변화가 함께 섞여 있다.
- `docs/SDD_SPEC_REQUIREMENTS.md`는 이번 계획에서 수정 대상이 아니다.

### Constraints
- `spec-snapshot`은 유지한다. baseline 이전에 없었다는 이유만으로 제거하지 않는다.
- `ralph-loop-init`은 SDD 복원 범위 밖이다.
- Codex 전용 문구와 도구 제약은 Claude와 기계적으로 같게 만들지 않는다.
- 복원 source는 commit 전체보다 path 단위 snapshot을 우선한다.

### Decision-Log Candidates
- **복원 전략**: Codex는 repo-wide revert보다 path-scoped restore가 안전하다. 이유: 후속 추가 스킬과 unrelated commit을 살려야 한다.
- **재적용 범위**: `Overview MUST`, drift/anchor 규칙, quality gate만 유지한다. 이유: 품질 향상 효과가 크고, baseline의 설명 깊이와도 충돌이 적다.
- **workflow 제거**: simplified 4-step narrative는 제거한다. 이유: 설명 공간을 차지하고 실제 사용 패턴을 과도하게 고정한다.

## Open Questions
- Codex 복원 후 wording은 Claude와 얼마나 엄격하게 맞출지 결정이 필요하다.
- version policy를 blanket minor bump로 둘지, 복원 성격을 반영해 major bump로 둘지 아직 미정이다.
- `implementation`은 변화 폭이 상대적으로 작았는데, baseline restore를 전면 적용할지 현재 규칙 일부를 유지할지 검토가 필요하다.

---

# Part 2: Implementation Plan

## Overview

`.codex/skills/`의 핵심 SDD 스킬을 explanation-rich baseline으로 되돌린다. 복원 소스는 `9be85e7`에 남아 있는 per-skill `prev/` snapshot을 우선 사용하고, 그 위에 `Overview MUST`, drift/anchor 규칙, quality gate만 다시 얹는다. `spec-snapshot`은 유지하고, `ralph-loop-init`은 이번 작업에서 제외한다.

## Scope

### In Scope
- `.codex/skills/spec-create/`
- `.codex/skills/spec-review/`
- `.codex/skills/spec-rewrite/`
- `.codex/skills/spec-summary/`
- `.codex/skills/spec-update-todo/`
- `.codex/skills/spec-update-done/`
- `.codex/skills/feature-draft/`
- `.codex/skills/implementation-plan/`
- `.codex/skills/implementation/`
- `.codex/skills/implementation-review/`
- `.codex/skills/pr-spec-patch/`
- `.codex/skills/pr-review/`
- 해당 스킬들의 `references/`, `examples/`, `skill.json`

### Out of Scope
- `.codex/skills/spec-snapshot/`
- `.codex/skills/ralph-loop-init/`
- `.claude/skills/` mirror 작업
- `docs/SDD_SPEC_REQUIREMENTS.md` 수정
- `_sdd/spec/` 실제 반영

## Components
1. **Baseline Restore**: `9be85e7` 내 `prev/` snapshot 기준으로 SDD 스킬 복원
2. **Spec Lifecycle Recovery**: `spec-*` 계열 예시/레퍼런스/체크리스트 복원
3. **Delivery Lifecycle Recovery**: `feature-draft`, `implementation*` 설명/예시 복원
4. **PR Lifecycle Recovery**: `pr-spec-patch`, `pr-review` 추론/체크리스트 복원
5. **Selective Reapply**: Overview, drift/anchor, quality gate만 재적용
6. **Validation**: workflow 제거, examples 정렬, version 정책, 문구 일관성 확인

## Implementation Phases

### Phase 1: Baseline Restore
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 1 | Spec lifecycle 스킬 baseline 복원 | P0 | - | Spec Lifecycle Recovery |
| 2 | Delivery lifecycle 스킬 baseline 복원 | P0 | - | Delivery Lifecycle Recovery |
| 3 | PR lifecycle 스킬 baseline 복원 | P1 | - | PR Lifecycle Recovery |

### Phase 2: Selective Reapply
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 4 | Overview MUST + explanation-rich component guidance 재적용 | P0 | 1, 2, 3 | Selective Reapply |
| 5 | Drift/anchor + `MUST update / CONSIDER / NO update` 규칙 재적용 | P0 | 1, 2, 3 | Selective Reapply |
| 6 | spec-create quality gate와 token-efficiency checks 재적용 | P1 | 1 | Selective Reapply |

### Phase 3: Cleanup & Verification
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 7 | simplified workflow 참조 제거 및 examples/refs 재정렬 | P0 | 4, 5, 6 | Validation |
| 8 | version 정리와 최종 검증 | P1 | 7 | Validation |

## Task Details

### Task 1: Spec lifecycle 스킬 baseline 복원
**Component**: Spec Lifecycle Recovery
**Priority**: P0
**Type**: Refactor

**Description**:
`spec-create`, `spec-review`, `spec-rewrite`, `spec-summary`, `spec-update-todo`, `spec-update-done`를 각 스킬별 historical `prev/` snapshot 기준으로 되돌린다. 복원은 whole-commit revert가 아니라 파일 단위 restore로 진행한다.

**Acceptance Criteria**:
- [ ] 각 스킬의 `SKILL.md`, `references/`, `examples/`, `skill.json`이 current layered state가 아니라 baseline snapshot 기준으로 복원된다.
- [ ] placeholder 중심 예시가 설명-rich 예시로 복원된다.
- [ ] restore source와 적용 대상의 대응표가 구현 중 명확히 유지된다.

**Target Files**:
- [M] `.codex/skills/spec-create/SKILL.md` -- baseline prose, examples, references 복원
- [M] `.codex/skills/spec-create/references/template-full.md` -- richer spec template 복원
- [M] `.codex/skills/spec-create/references/examples.md` -- example-driven guidance 복원
- [M] `.codex/skills/spec-create/examples/simple-project-spec.md` -- concrete example 복원
- [M] `.codex/skills/spec-create/examples/complex-project-spec.md` -- concrete example 복원
- [M] `.codex/skills/spec-review/SKILL.md` -- review prose와 판단 기준 복원
- [M] `.codex/skills/spec-review/references/review-checklist.md` -- 상세 체크리스트 복원
- [M] `.codex/skills/spec-review/examples/spec-review-report.md` -- report example 복원
- [M] `.codex/skills/spec-rewrite/SKILL.md` -- before/after 성격의 rewrite guidance 복원
- [M] `.codex/skills/spec-rewrite/references/rewrite-checklist.md` -- rewrite checklist 복원
- [M] `.codex/skills/spec-rewrite/examples/rewrite-report.md` -- rewrite report example 복원
- [M] `.codex/skills/spec-summary/SKILL.md` -- summary 설명 밀도 복원
- [M] `.codex/skills/spec-summary/references/summary-template.md` -- summary template 복원
- [M] `.codex/skills/spec-summary/examples/summary-output.md` -- summary example 복원
- [M] `.codex/skills/spec-update-todo/SKILL.md` -- input expansion guidance 복원
- [M] `.codex/skills/spec-update-todo/references/input-format.md` -- structured input format 복원
- [M] `.codex/skills/spec-update-todo/references/section-mapping.md` -- mapping richness 복원
- [M] `.codex/skills/spec-update-todo/examples/user_spec.md` -- richer input example 복원
- [M] `.codex/skills/spec-update-done/SKILL.md` -- change report guidance 복원
- [M] `.codex/skills/spec-update-done/references/drift-patterns.md` -- drift pattern detail 복원
- [M] `.codex/skills/spec-update-done/references/update-strategies.md` -- update strategy detail 복원
- [M] `.codex/skills/spec-update-done/examples/review-report.md` -- review report example 복원
- [M] `.codex/skills/spec-update-done/examples/changelog-entry.md` -- changelog example 복원

**Technical Notes**:
- `9be85e7` 안의 각 `prev/<timestamp>/` 중 latest snapshot을 baseline으로 우선 채택한다.
- `spec-snapshot/`은 이 task에 포함하지 않는다.

**Dependencies**: -

### Task 2: Delivery lifecycle 스킬 baseline 복원
**Component**: Delivery Lifecycle Recovery
**Priority**: P0
**Type**: Refactor

**Description**:
`feature-draft`, `implementation-plan`, `implementation`, `implementation-review`를 baseline snapshot 기준으로 복원해, simplified workflow와 과도한 메타 지시 이전의 절차적 설명과 예시를 되살린다.

**Acceptance Criteria**:
- [ ] `feature-draft` example/output guidance가 richer procedural style로 복원된다.
- [ ] `implementation-plan`과 `implementation-review`가 현재보다 자세한 task/review guidance를 되찾는다.
- [ ] `implementation`은 spec sync 규칙을 잃지 않으면서 baseline readability를 회복한다.

**Target Files**:
- [M] `.codex/skills/feature-draft/SKILL.md` -- workflow/simple manifesto 이전의 설명 밀도 복원
- [M] `.codex/skills/feature-draft/references/output-format.md` -- richer patch/plan format 복원
- [M] `.codex/skills/feature-draft/references/adaptive-questions.md` -- deterministic completion baseline 정리
- [M] `.codex/skills/feature-draft/references/tool-and-gates.md` -- gate 구성 baseline 복원
- [M] `.codex/skills/feature-draft/examples/feature_draft_parallel.md` -- complex feature draft example 복원
- [M] `.codex/skills/implementation-plan/SKILL.md` -- planning guidance baseline 복원
- [M] `.codex/skills/implementation-plan/references/advanced-patterns.md` -- richer planning patterns 유지/정렬
- [M] `.codex/skills/implementation-plan/examples/sample-plan-parallel.md` -- sample plan baseline 복원
- [M] `.codex/skills/implementation/SKILL.md` -- execution guidance baseline 복원
- [M] `.codex/skills/implementation/references/parallel-execution.md` -- parallel execution guidance 정리
- [M] `.codex/skills/implementation/examples/sample-parallel-session.md` -- execution example 정리
- [M] `.codex/skills/implementation-review/SKILL.md` -- review prose baseline 복원
- [M] `.codex/skills/implementation-review/references/review-checklist.md` -- checklist baseline 복원
- [M] `.codex/skills/implementation-review/examples/sample-review.md` -- example baseline 복원

**Technical Notes**:
- `feature-draft`는 현재 1.3.0 explanation overlay를 제거한 뒤 selective reapply로 다시 얹는다.
- `implementation`은 변화 폭이 작으므로 baseline restore 후 selective merge가 필요할 수 있다.

**Dependencies**: -

### Task 3: PR lifecycle 스킬 baseline 복원
**Component**: PR Lifecycle Recovery
**Priority**: P1
**Type**: Refactor

**Description**:
`pr-spec-patch`, `pr-review`를 baseline snapshot 기준으로 복원해 상세 추론 예시와 풍부한 review language를 되살린다.

**Acceptance Criteria**:
- [ ] `pr-spec-patch` example이 단순 anchor mapping을 넘어서 richer reasoning example을 제공한다.
- [ ] `pr-review` checklist/report example이 blocker와 spec 영향 판정을 더 구체적으로 가르친다.

**Target Files**:
- [M] `.codex/skills/pr-spec-patch/SKILL.md` -- PR to spec reasoning baseline 복원
- [M] `.codex/skills/pr-spec-patch/references/gh-commands.md` -- command reference 유지/정렬
- [M] `.codex/skills/pr-spec-patch/examples/spec_patch_draft.md` -- richer draft example 복원
- [M] `.codex/skills/pr-review/SKILL.md` -- review guidance baseline 복원
- [M] `.codex/skills/pr-review/references/review-checklist.md` -- checklist baseline 복원
- [M] `.codex/skills/pr-review/examples/sample-review.md` -- review example baseline 복원

**Technical Notes**:
- PR skill pair는 Phase 1에서 병렬 작업 가능하지만, selective reapply 단계에서는 shared wording 때문에 함께 점검한다.

**Dependencies**: -

### Task 4: Overview MUST + explanation-rich component guidance 재적용
**Component**: Selective Reapply
**Priority**: P0
**Type**: Feature

**Description**:
baseline restore 후 `Overview`를 MUST section으로 다시 넣고, `Runtime Map`의 사용자 관점 설명, `Component Details > Overview` 매핑, component behavior/design intent 서술을 Codex 쪽에 재적용한다.

**Acceptance Criteria**:
- [ ] `spec-create` template/examples에 `Overview`와 user-facing `Runtime Map` 설명이 다시 존재한다.
- [ ] `feature-draft`, `spec-update-todo`, `spec-update-done`, `spec-review`, `spec-rewrite`, `spec-summary`가 `Component Details > Overview`를 인식한다.
- [ ] explanation이 token-efficient하게 유지되며 placeholder만 남지 않는다.

**Target Files**:
- [M] `.codex/skills/spec-create/SKILL.md`
- [M] `.codex/skills/spec-create/references/template-full.md`
- [M] `.codex/skills/spec-create/examples/simple-project-spec.md`
- [M] `.codex/skills/spec-create/examples/complex-project-spec.md`
- [M] `.codex/skills/feature-draft/SKILL.md`
- [M] `.codex/skills/feature-draft/references/output-format.md`
- [M] `.codex/skills/feature-draft/examples/feature_draft_parallel.md`
- [M] `.codex/skills/spec-update-todo/SKILL.md`
- [M] `.codex/skills/spec-update-todo/references/section-mapping.md`
- [M] `.codex/skills/spec-update-done/SKILL.md`
- [M] `.codex/skills/spec-update-done/references/drift-patterns.md`
- [M] `.codex/skills/spec-review/SKILL.md`
- [M] `.codex/skills/spec-review/references/review-checklist.md`
- [M] `.codex/skills/spec-rewrite/SKILL.md`
- [M] `.codex/skills/spec-rewrite/references/rewrite-checklist.md`
- [M] `.codex/skills/spec-summary/SKILL.md`
- [M] `.codex/skills/spec-summary/references/summary-template.md`

**Technical Notes**:
- 이 task는 baseline 복원본을 다시 exploration-first placeholder 상태로 만들지 말고, 설명-rich baseline 위에 selective patch만 얹는 것이 핵심이다.

**Dependencies**: 1, 2, 3

### Task 5: Drift/anchor + 분류 규칙 재적용
**Component**: Selective Reapply
**Priority**: P0
**Type**: Feature

**Description**:
`MUST update / CONSIDER / NO update` 분류, stable anchor target section, spec sync follow-up 규칙을 planning/review/PR 스킬 전반에 다시 얹는다.

**Acceptance Criteria**:
- [ ] `feature-draft`, `spec-update-*`, `implementation*`, `pr-*`가 동일한 분류 체계를 사용한다.
- [ ] anchor-aware drafting/review language가 baseline prose와 충돌하지 않는다.
- [ ] `Open Questions`와 low-confidence handling이 각 스킬 출력에 유지된다.

**Target Files**:
- [M] `.codex/skills/feature-draft/SKILL.md`
- [M] `.codex/skills/spec-update-todo/SKILL.md`
- [M] `.codex/skills/spec-update-todo/references/section-mapping.md`
- [M] `.codex/skills/spec-update-done/SKILL.md`
- [M] `.codex/skills/spec-update-done/references/drift-patterns.md`
- [M] `.codex/skills/spec-update-done/references/update-strategies.md`
- [M] `.codex/skills/implementation/SKILL.md`
- [M] `.codex/skills/implementation-review/SKILL.md`
- [M] `.codex/skills/implementation-review/references/review-checklist.md`
- [M] `.codex/skills/implementation-plan/SKILL.md`
- [M] `.codex/skills/pr-spec-patch/SKILL.md`
- [M] `.codex/skills/pr-review/SKILL.md`
- [M] `.codex/skills/pr-review/references/review-checklist.md`

**Technical Notes**:
- Codex-specific tool wording은 유지하되, classification vocabulary는 Claude 쪽과 drift 나지 않게 맞춘다.

**Dependencies**: 1, 2, 3

### Task 6: spec-create quality gate와 token-efficiency checks 재적용
**Component**: Selective Reapply
**Priority**: P1
**Type**: Feature

**Description**:
`spec-create` 중심으로 self-verification gate, token-efficiency 원칙, anti-pattern coverage를 baseline 복원본 위에 다시 넣는다. 이 변경은 downstream spec skills examples/checklists와도 맞물리도록 조정한다.

**Acceptance Criteria**:
- [ ] quality gate가 `docs/SDD_SPEC_REQUIREMENTS.md`의 품질 기준과 더 직접적으로 매핑된다.
- [ ] token-efficiency 원칙이 writing guidance에 남아 있다.
- [ ] anti-pattern/좋은 예시 참조가 baseline richness를 해치지 않고 살아 있다.

**Target Files**:
- [M] `.codex/skills/spec-create/SKILL.md`
- [M] `.codex/skills/spec-create/references/examples.md`
- [M] `.codex/skills/spec-create/references/template-full.md`
- [M] `.codex/skills/spec-create/examples/simple-project-spec.md`
- [M] `.codex/skills/spec-create/examples/complex-project-spec.md`
- [M] `.codex/skills/spec-review/SKILL.md`
- [M] `.codex/skills/spec-summary/SKILL.md`

**Technical Notes**:
- `0950a85`의 self-verification 아이디어는 유지하되, baseline explanation density와 충돌하는 terse wording은 피한다.

**Dependencies**: 1

### Task 7: simplified workflow 제거 및 examples/refs 재정렬
**Component**: Validation
**Priority**: P0
**Type**: Refactor

**Description**:
restored/reapplied 상태에서 simplified 4-step workflow와 과도한 공통 manifesto 문구를 제거하고, examples/references가 최종 `SKILL.md`와 같은 철학을 가르치도록 정렬한다.

**Acceptance Criteria**:
- [ ] 4-step workflow 표/문구가 Codex SDD 스킬에서 제거된다.
- [ ] examples와 references가 현재 `SKILL.md`의 출력 형식과 충돌하지 않는다.
- [ ] `spec-snapshot`, `ralph-loop-init`은 영향받지 않는다.

**Target Files**:
- [M] `.codex/skills/spec-create/SKILL.md`
- [M] `.codex/skills/feature-draft/SKILL.md`
- [M] `.codex/skills/implementation-plan/SKILL.md`
- [M] `.codex/skills/implementation/SKILL.md`
- [M] `.codex/skills/implementation-review/SKILL.md`
- [M] `.codex/skills/spec-update-done/SKILL.md`
- [M] `.codex/skills/spec-review/SKILL.md`
- [M] `.codex/skills/pr-review/SKILL.md`
- [M] `.codex/skills/pr-spec-patch/SKILL.md`

**Technical Notes**:
- workflow 제거는 단순 삭제가 아니라, 필요한 상호 의존 설명을 간결한 integration note로 대체해야 한다.

**Dependencies**: 4, 5, 6

### Task 8: version 정리와 최종 검증
**Component**: Validation
**Priority**: P1
**Type**: Test

**Description**:
복원 이후 version/front matter/skill.json 정합성을 맞추고, diff hygiene와 핵심 문구 검색으로 구조 드리프트를 검증한다.

**Acceptance Criteria**:
- [ ] 수정된 모든 Codex SDD 스킬의 front matter와 `skill.json` version이 일치한다.
- [ ] `git diff --check`가 통과한다.
- [ ] `rg` 기반 점검으로 `Overview`, classification vocabulary, workflow 제거 상태가 확인된다.

**Target Files**:
- [M] `.codex/skills/spec-create/skill.json`
- [M] `.codex/skills/spec-review/skill.json`
- [M] `.codex/skills/spec-rewrite/skill.json`
- [M] `.codex/skills/spec-summary/skill.json`
- [M] `.codex/skills/spec-update-todo/skill.json`
- [M] `.codex/skills/spec-update-done/skill.json`
- [M] `.codex/skills/feature-draft/skill.json`
- [M] `.codex/skills/implementation-plan/skill.json`
- [M] `.codex/skills/implementation/skill.json`
- [M] `.codex/skills/implementation-review/skill.json`
- [M] `.codex/skills/pr-spec-patch/skill.json`
- [M] `.codex/skills/pr-review/skill.json`

**Technical Notes**:
- version policy는 blanket minor bump를 기본안으로 두되, restore 성격을 major로 볼지 open question으로 남긴다.

**Dependencies**: 7

## Parallel Execution Summary

| Phase | Total Tasks | Max Parallel | File Conflicts |
|-------|-------------|--------------|----------------|
| 1 | 3 | 3 | None if family-scoped |
| 2 | 3 | 1 | `spec-create/*`, `feature-draft/*`, `spec-update-*`, `implementation*`, `pr-*` 중복 |
| 3 | 2 | 1 | `skill.json`, shared SKILL.md overlap |

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| baseline snapshot 선택이 잘못됨 | 잘못된 버전으로 복원 | 각 스킬의 latest `prev/<timestamp>`를 우선 사용하고, 현재 파일과 diff로 확인 |
| useful Codex-specific wording 손실 | 플랫폼 적합성 저하 | restore 후 selective reapply에서 Codex 전용 도구 제약만 다시 얹기 |
| `spec-snapshot`까지 잘못 건드림 | unrelated regression | scope에서 명시적으로 제외하고 `git diff -- .codex/skills` 점검 시 필터링 |
| examples는 풍부하지만 output contract가 깨짐 | downstream 스킬 호환성 저하 | `feature-draft` ↔ `spec-update-todo`, `implementation*`, `pr-*` 계약을 Phase 3에서 교차 점검 |

## Open Questions

- [ ] Codex 복원 후 `.claude/skills/`와 어느 수준까지 wording parity를 맞출지 확정 필요
- [ ] version 정책을 blanket minor bump로 둘지 restoration milestone로 볼지 확정 필요
- [ ] `implementation`은 full restore 후 selective merge로 갈지, 현재 상태를 baseline보다 더 신뢰할지 결정 필요

## Model Recommendation

`gpt-5.3-codex` (`reasoning effort: extra high`)

---

## Next Steps

### Apply Spec Patch
- `spec-update-todo`로 Part 1의 lifecycle/maintenance change를 `_sdd/spec/`에 반영

### Execute Implementation
- `implementation`으로 Part 2를 실행하되, Phase 1은 family 단위 병렬, Phase 2 이후는 순차 실행

### Sync After Completion
- Codex 복원 완료 후 `spec-update-done`으로 실제 유지보수 레시피와 상태를 다시 문서화
