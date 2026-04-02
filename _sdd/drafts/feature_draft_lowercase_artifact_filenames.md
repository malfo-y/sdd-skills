# Feature Draft: artifact 결과 파일명 소문자 canonical 전환

<!-- spec-update-todo-input-start -->
# Part 1: Spec Patch Draft

# Spec Update Input

**Date**: 2026-04-02
**Author**: Codex
**Target Spec**: `_sdd/spec/main.md`
**Spec Update Classification**: Improvement

## Background & Motivation Updates

### Improvement: 산출물 파일명 규칙을 대문자 혼합에서 소문자 canonical 규칙으로 정리
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Architecture Overview` > `_sdd/ Artifact Map`
**Current State**: `_sdd/` 산출물 규칙이 혼합되어 있다. `discussion_<title>.md`, `guide_<slug>.md`처럼 소문자 slug 기반 이름도 있지만, `IMPLEMENTATION_PLAN.md`, `IMPLEMENTATION_REPORT.md`, `IMPLEMENTATION_REVIEW.md`, `SUMMARY.md`, `SPEC_REVIEW_REPORT.md`, `DECISION_LOG.md`, `PREV_*`처럼 대문자 또는 대문자 prefix 기반 이름도 넓게 사용된다.
**Proposed**: `_sdd/` 산출물의 canonical naming 규칙을 소문자 snake_case로 통일한다. 새로 생성되는 결과 파일은 소문자 canonical 이름을 사용하고, 기존 대문자 이름은 점진 전환 기간 동안 읽기/참조 호환 대상으로 유지한다.
**Reason**: slug 기반 파일명 규칙과 일관성을 맞추고, 대소문자 혼합으로 인한 탐색/검색/자동화 혼선을 줄이려면 canonical 규칙을 하나로 고정하는 편이 낫다. 다만 현재 경로가 스킬 본문, 예시, 스펙, 기존 기록에 넓게 퍼져 있으므로 즉시 rename보다 호환성 전환이 안전하다.

## Design Changes

### Improvement: Artifact Naming Policy를 "소문자 write, 이행 기간 dual-read" 계약으로 명시
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Core Design` 또는 `Architecture Overview` > `Artifact Naming / Compatibility`
**Current State**: 각 스킬이 자신의 출력 파일명을 독립적으로 설명하고 있어, 대문자/소문자 규칙과 호환성 경계가 전역 규칙으로 정리되어 있지 않다.
**Proposed**: 전역 artifact naming policy를 추가한다.
- canonical 결과 파일명은 소문자 snake_case를 사용한다
- 새 출력은 canonical 경로에 저장한다
- 기존 대문자 이름은 transition 기간 동안 입력/참조 fallback으로 허용한다
- historical artifact의 일괄 rename은 별도 단계로 다룬다
- backup prefix도 `PREV_*` 대신 `prev_*`를 canonical로 사용한다
**Reason**: 파일명 규칙을 component별 예외로 두면 이후 스킬을 추가할 때 다시 drift가 생긴다. 새 규칙과 호환성 규칙을 전역으로 먼저 선언해야 스킬별 구현이 같은 방향으로 수렴한다.

### Improvement: `_sdd/ Artifact Map`과 component output 경로를 lowercase canonical로 정규화
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `_sdd/ Artifact Map`
**Current State**: artifact map은 일부 root-level 대문자 경로(`_sdd/spec/SUMMARY.md`, `_sdd/spec/SPEC_REVIEW_REPORT.md`, `_sdd/implementation/IMPLEMENTATION_PLAN.md`)를 기준으로 기술되어 있고, 실제 일부 스킬 계약(`spec-review`의 `logs/`)과도 완전히 일치하지 않는다.
**Proposed**: artifact map을 아래 canonical 경로 중심으로 재정리한다.
- `_sdd/spec/summary.md`
- `_sdd/spec/logs/spec_review_report.md`
- `_sdd/spec/logs/rewrite_report.md`
- `_sdd/spec/decision_log.md`
- `_sdd/implementation/implementation_plan.md`
- `_sdd/implementation/implementation_report.md`
- `_sdd/implementation/implementation_report_phase_<n>.md`
- `_sdd/implementation/implementation_review.md`
- `_sdd/pr/pr_review.md`
- `_sdd/spec/prev/prev_<filename>_<timestamp>.md`
- `_sdd/implementation/prev/prev_<filename>_<timestamp>.md`
`discussion_<title>.md`, `guide_<slug>.md`, `spec-rewrite-plan.md`처럼 이미 소문자인 규칙은 그대로 유지한다.
**Reason**: artifact map이 canonical source of truth 역할을 해야 후속 스킬 계약과 예시를 안정적으로 정렬할 수 있다.

### Improvement: 주요 스킬들의 input/output contract에 lowercase canonical + uppercase fallback을 반영
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Component Details`
**Current State**: `implementation-plan`, `implementation`, `implementation-review`, `spec-summary`, `spec-review`, `spec-create`, `spec-update-done`, `spec-update-todo`, `spec-snapshot`, `pr-review`, `sdd-autopilot` 등은 대문자 artifact 경로를 직접 언급하거나 그 경로를 전제로 한 examples/references를 가진다.
**Proposed**: 각 component 설명에 다음 원칙을 반영한다.
- output은 lowercase canonical 경로를 기준으로 문서화
- input은 transition 기간 동안 lowercase canonical과 legacy uppercase를 모두 읽을 수 있다고 명시
- mirror 대상(`.codex`, `.claude`, agent definitions`)은 같은 경로 계약을 사용
**Reason**: 새 출력만 바꾸고 입력/예시/하위 스킬이 이전 경로를 그대로 요구하면 workflow가 즉시 깨진다. write-path와 read-path를 함께 정의해야 한다.

## Improvements

### Improvement: backup/archive 규칙도 lowercase로 통일
**Priority**: Medium
**Target Section**: `_sdd/spec/main.md` > `Core Design` 또는 `Artifact Naming / Compatibility`
**Current State**: 백업 파일은 `prev/` 디렉토리를 쓰면서도 파일명 prefix는 `PREV_*`로 대문자를 사용한다. 일부 스킬은 `PREV_SUMMARY_*`, `PREV_IMPLEMENTATION_REPORT_*`, `PREV_PR_REVIEW_*`처럼 개별 이름을 하드코딩하고 있다.
**Proposed**: 신규 backup/archive는 `prev_<filename>_<timestamp>.md`를 canonical로 사용한다. transition 기간 동안 기존 `PREV_*` 파일은 읽기/보존 대상으로 유지한다.
**Reason**: 디렉토리는 이미 `prev/` 소문자인데 prefix만 대문자인 상태는 규칙상 어색하다. 신규 생성 규칙부터 정리하는 편이 이행 비용 대비 효과가 크다.

### Improvement: historical rename과 `SYNC_*` 파일명 변경은 초기 rollout에서 분리
**Priority**: Medium
**Target Section**: `_sdd/spec/main.md` > `Issues / Appendix` 또는 `Open Questions`
**Current State**: `_sdd/implementation/features/*/SYNC_*` 계열과 과거 `_sdd/` 산출물은 이미 다수 존재하며, 문서 기록에도 남아 있다.
**Proposed**: 1차 rollout에서는 skill contract와 canonical path를 먼저 바꾸고, historical artifact rename 및 `SYNC_*` 소문자화는 별도 migration task로 분리한다.
**Reason**: 기존 기록까지 한 번에 rename하면 영향 범위가 과도하게 커진다. 먼저 "새 출력 규칙"과 "fallback read 규칙"을 정리한 뒤 historical cleanup을 따로 다루는 편이 안전하다.

## Failure Modes

| 시나리오 | 실패 시 | 사용자 가시성 | 처리 방안 |
|----------|---------|---------------|-----------|
| 새 출력만 소문자로 바꾸고 입력 fallback을 정의하지 않음 | 후속 스킬이 기존 대문자 경로를 찾지 못해 workflow 단절 | 특정 스킬이 "파일 없음" 또는 잘못된 경로를 참조 | output contract와 input source 양쪽에 lowercase/legacy fallback을 함께 명시 |
| `.codex`와 `.claude` 또는 agent mirror가 다른 경로를 사용 | 플랫폼마다 다른 artifact를 생성 | 동일 요청이 플랫폼별로 다른 파일명 출력 | mirror 파일을 같은 phase에서 동시 갱신 |
| examples/references/templates가 이전 이름을 그대로 유지 | 실제 contract와 학습 예시가 불일치 | 사용자가 예시를 따라가다 다른 이름 생성 | examples/references/summary template까지 함께 갱신 |
| backup prefix만 늦게 바뀜 | 결과물은 소문자인데 백업만 대문자라 규칙 혼합 지속 | `prev/` 안에서 `PREV_*`와 `prev_*` 공존 | 신규 backup 규칙을 같은 rollout에 포함하고 legacy는 보존만 한다 |
| historical rename을 성급히 진행 | 과거 기록 링크와 의사결정 로그가 깨짐 | DECISION_LOG/main.md의 과거 경로 참조가 부정확해짐 | historical rename은 별도 migration으로 분리하고 1차 rollout에서는 canonical 선언 + 새 출력 변경에 집중 |

## Notes

### Context
- 이번 변경은 cosmetic rename보다 "artifact contract 정규화"에 가깝다.
- 우선순위는 `새 출력 소문자화` → `입력 fallback 허용` → `examples/spec sync` → `historical cleanup 검토` 순으로 잡는다.
- `discussion_<title>.md`, `guide_<slug>.md`, `_sdd/spec/logs/spec-rewrite-plan.md`처럼 이미 소문자 규칙인 산출물은 유지한다.

### Open Questions
- `decision_log.md`까지 1차 rollout에 포함할지, 혹은 implementation/spec/reporting 계열만 먼저 바꿀지 결정이 필요하다.
- `spec_review_report.md` canonical path를 `_sdd/spec/logs/`로 완전히 고정할지, root-level legacy 경로도 문서에 병기할지 결정이 필요하다.
- `SYNC_*` 및 historical artifact의 실제 rename을 언제 할지 결정이 필요하다.

<!-- spec-update-todo-input-end -->

# Part 2: Implementation Plan

## Overview

대문자 기반 `_sdd/` artifact 이름을 소문자 canonical 규칙으로 점진 전환한다. 핵심은 "새 출력은 소문자", "기존 대문자 경로는 transition 기간 동안 입력/참조 fallback 허용", "스펙/스킬/examples/agent mirror를 같은 계약으로 정렬"이다.

이번 작업은 실제 historical artifact 전체 rename보다, 앞으로 생성되는 산출물의 canonical path를 재정의하고 workflow breakage를 막는 호환성 레이어를 문서 계약 수준에서 정리하는 데 초점을 둔다.

## Scope

### In Scope
- `_sdd/spec/main.md`에 lowercase artifact canonical policy와 artifact map 반영
- `.codex`/`.claude` skill contracts의 output path를 lowercase canonical로 전환
- mirror agent definitions(`.codex/agents/*.toml`, `.claude/agents/*.md`) 동기화
- examples / references / templates의 artifact path 예시 정렬
- 신규 backup/archive prefix를 `prev_*` canonical로 전환

### Out of Scope
- `_sdd/` 아래 historical artifact 실제 일괄 rename
- `SYNC_*` 계열 historical archive naming 일괄 변경
- 외부 문서/README의 광범위한 retrospective cleanup
- 파일명 변경을 강제하는 런타임 코드나 스크립트 추가

## Components

1. **Repo Spec Policy**: `_sdd/spec/main.md`의 artifact map, naming policy, component output 설명
2. **Implementation Artifact Family**: `feature-draft`, `implementation-plan`, `implementation`, `implementation-review`, `sdd-autopilot`
3. **Spec Artifact Family**: `spec-summary`, `spec-review`, `spec-rewrite`, `spec-snapshot`, `spec-create`, `spec-update-done`, `spec-update-todo`
4. **Supporting Skills / References**: `pr-review`, `guide-create`, examples, templates, reference docs
5. **Mirror Sync**: `.codex`와 `.claude`, agent mirror 간 동일 계약 유지

## Implementation Phases

### Phase 1: Canonical 정책 확정
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| T1 | `_sdd/spec/main.md`에 lowercase artifact naming policy와 canonical path map 반영 | P0 | - | Repo Spec Policy |

### Phase 2: 핵심 workflow artifact 전환
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| T2 | implementation 계열 skill/agent contract를 lowercase canonical + fallback 규칙으로 갱신 | P0 | T1 | Implementation Artifact Family |
| T3 | spec/reporting 계열 skill/agent contract를 lowercase canonical + fallback 규칙으로 갱신 | P0 | T1 | Spec Artifact Family |

### Phase 3: 지원 문서와 예시 정렬
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| T4 | supporting skills와 backup/archive 규칙을 lowercase canonical로 정리 | P1 | T1 | Supporting Skills / References |
| T5 | examples / templates / orchestrator references를 canonical path와 일치시킴 | P1 | T2, T3, T4 | Mirror Sync |

### Phase 4: 검증과 후속 migration 경계 확정
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| T6 | repo-wide path 검증과 historical rename defer 범위 문서화 | P1 | T2, T3, T4, T5 | Repo Spec Policy |

## Task Details

### Task T1: `_sdd/spec/main.md`에 lowercase artifact naming policy와 canonical path map 반영
**Component**: Repo Spec Policy
**Priority**: P0
**Type**: Refactor

**Description**:  
`_sdd/spec/main.md`를 canonical source of truth로 삼아 artifact naming policy를 재정의한다. `_sdd/ Artifact Map`과 각 component output 설명을 lowercase canonical 경로로 정리하고, transition 기간 동안 legacy uppercase 경로를 fallback input으로 허용한다는 규칙을 문서화한다.

**Acceptance Criteria**:
- [ ] `_sdd/spec/main.md`에 lowercase canonical artifact naming policy가 명시된다
- [ ] `_sdd/ Artifact Map`이 lowercase canonical 경로 기준으로 정리된다
- [ ] `implementation-*`, `spec-*`, `pr-review` 주요 output 경로가 canonical 이름으로 표현된다
- [ ] legacy uppercase 경로는 transition fallback으로 설명된다
- [ ] historical rename은 별도 migration 범위라는 점이 명시된다

**Target Files**:
- [M] `_sdd/spec/main.md` -- artifact naming policy, artifact map, component output 경로 갱신

**Technical Notes**:
- `spec-review`는 현재 skill contract가 `_sdd/spec/logs/`를 사용하므로 canonical path도 logs 기준으로 맞추는 편이 일관적이다
- 이미 소문자인 `discussion_<title>.md`, `guide_<slug>.md`, `spec-rewrite-plan.md`는 예외가 아니라 "기존 canonical 유지"로 설명하는 편이 낫다
- `PREV_*` 대문자 prefix는 `prev_*` canonical로 전환하되, legacy 보존 정책을 함께 적어야 한다

**Dependencies**: -

### Task T2: implementation 계열 skill/agent contract를 lowercase canonical + fallback 규칙으로 갱신
**Component**: Implementation Artifact Family
**Priority**: P0
**Type**: Refactor

**Description**:  
`feature-draft`, `implementation-plan`, `implementation`, `implementation-review`, `sdd-autopilot`의 output/input contract를 lowercase canonical artifact 이름으로 전환한다. 새로 쓰는 경로는 소문자 canonical을 사용하고, 입력으로 읽는 경로는 transition 기간 동안 uppercase legacy도 허용하도록 문구를 정리한다. mirror agent 파일도 함께 맞춘다.

**Acceptance Criteria**:
- [ ] `implementation_plan.md`, `implementation_report.md`, `implementation_review.md`가 canonical output으로 문서화된다
- [ ] phase report 및 관련 examples가 lowercase canonical 이름을 사용한다
- [ ] legacy uppercase input fallback이 필요한 곳에 명시된다
- [ ] `.codex` skill, `.codex` agent, `.claude` skill, `.claude` agent가 같은 계약을 사용한다
- [ ] `feature-draft`와 `sdd-autopilot` 예시/참조도 같은 artifact 이름을 사용한다

**Target Files**:
- [M] `.codex/skills/feature-draft/SKILL.md`
- [M] `.codex/skills/implementation-plan/SKILL.md`
- [M] `.codex/skills/implementation/SKILL.md`
- [M] `.codex/skills/implementation-review/SKILL.md`
- [M] `.codex/skills/sdd-autopilot/SKILL.md`
- [M] `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md`
- [M] `.codex/skills/sdd-autopilot/references/orchestrator-contract.md`
- [M] `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md`
- [M] `.codex/agents/feature-draft.toml`
- [M] `.codex/agents/implementation-plan.toml`
- [M] `.codex/agents/implementation.toml`
- [M] `.codex/agents/implementation-review.toml`
- [M] `.claude/skills/feature-draft/SKILL.md`
- [M] `.claude/skills/implementation-plan/SKILL.md`
- [M] `.claude/skills/implementation/SKILL.md`
- [M] `.claude/skills/implementation-review/SKILL.md`
- [M] `.claude/skills/sdd-autopilot/SKILL.md`
- [M] `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md`
- [M] `.claude/skills/sdd-autopilot/references/orchestrator-contract.md`
- [M] `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md`
- [M] `.claude/agents/feature-draft.md`
- [M] `.claude/agents/implementation-plan.md`
- [M] `.claude/agents/implementation.md`
- [M] `.claude/agents/implementation-review.md`

**Technical Notes**:
- `implementation`과 `implementation-review`는 backup path까지 같이 바꿔야 한다: `prev/prev_implementation_report_<timestamp>.md`, `prev/prev_implementation_review_<timestamp>.md`
- `feature-draft`는 output path 자체는 이미 소문자이지만 Part 2 내 canonical artifact 예시가 변경 대상이다
- `sdd-autopilot`은 orchestrator examples와 reasoning references에 implementation artifact 이름이 반복되므로 누락되기 쉽다

**Dependencies**: T1

### Task T3: spec/reporting 계열 skill/agent contract를 lowercase canonical + fallback 규칙으로 갱신
**Component**: Spec Artifact Family
**Priority**: P0
**Type**: Refactor

**Description**:  
`spec-summary`, `spec-review`, `spec-rewrite`, `spec-snapshot`, `spec-create`, `spec-update-done`, `spec-update-todo`의 output/input contract를 lowercase canonical artifact 기준으로 정리한다. `summary.md`, `spec_review_report.md`, `rewrite_report.md`, `decision_log.md`, `prev_*` naming을 문서 전반에서 일관되게 맞추고, agent mirror까지 동기화한다.

**Acceptance Criteria**:
- [ ] `summary.md`, `spec_review_report.md`, `rewrite_report.md`, `decision_log.md` canonical 경로가 반영된다
- [ ] `spec-rewrite-plan.md`처럼 이미 lowercase인 산출물은 유지된다고 설명된다
- [ ] `spec-create`, `spec-update-*` 입력 소스에 legacy uppercase fallback이 반영된다
- [ ] `spec-summary` examples/references가 canonical 경로와 일치한다
- [ ] `.codex`/`.claude` 및 agent mirror가 동일한 경로 계약을 사용한다

**Target Files**:
- [M] `.codex/skills/spec-summary/SKILL.md`
- [M] `.codex/skills/spec-summary/references/summary-template.md`
- [M] `.codex/skills/spec-summary/examples/summary-output.md`
- [M] `.codex/skills/spec-review/SKILL.md`
- [M] `.codex/skills/spec-rewrite/SKILL.md`
- [M] `.codex/skills/spec-rewrite/examples/rewrite-plan.md`
- [M] `.codex/skills/spec-rewrite/examples/rewrite-report.md`
- [M] `.codex/skills/spec-rewrite/references/rewrite-checklist.md`
- [M] `.codex/skills/spec-rewrite/references/spec-format.md`
- [M] `.codex/skills/spec-snapshot/SKILL.md`
- [M] `.codex/skills/spec-create/SKILL.md`
- [M] `.codex/skills/spec-create/references/template-full.md`
- [M] `.codex/skills/spec-update-done/SKILL.md`
- [M] `.codex/skills/spec-update-todo/SKILL.md`
- [M] `.codex/agents/spec-review.toml`
- [M] `.codex/agents/spec-update-done.toml`
- [M] `.codex/agents/spec-update-todo.toml`
- [M] `.claude/skills/spec-summary/SKILL.md`
- [M] `.claude/skills/spec-summary/references/summary-template.md`
- [M] `.claude/skills/spec-summary/examples/summary-output.md`
- [M] `.claude/skills/spec-review/SKILL.md`
- [M] `.claude/skills/spec-rewrite/SKILL.md`
- [M] `.claude/skills/spec-rewrite/examples/rewrite-plan.md`
- [M] `.claude/skills/spec-rewrite/examples/rewrite-report.md`
- [M] `.claude/skills/spec-rewrite/references/rewrite-checklist.md`
- [M] `.claude/skills/spec-rewrite/references/spec-format.md`
- [M] `.claude/skills/spec-snapshot/SKILL.md`
- [M] `.claude/skills/spec-create/SKILL.md`
- [M] `.claude/skills/spec-create/references/template-full.md`
- [M] `.claude/skills/spec-update-done/SKILL.md`
- [M] `.claude/skills/spec-update-todo/SKILL.md`
- [M] `.claude/agents/spec-review.md`
- [M] `.claude/agents/spec-update-done.md`
- [M] `.claude/agents/spec-update-todo.md`

**Technical Notes**:
- `spec-review`는 root-level `SPEC_REVIEW_REPORT.md`와 `logs/SPEC_REVIEW_REPORT.md`가 혼재하므로 이번에 canonical path를 하나로 고정해야 한다
- `spec-summary`는 backup/input exclusion/filter 예시가 많아서 reference와 example 동시 갱신이 필요하다
- `spec-rewrite`는 이미 `spec-rewrite-plan.md`가 lowercase이므로 report/decision-log만 같이 정렬하면 규칙 설명이 더 간결해진다

**Dependencies**: T1

### Task T4: supporting skills와 backup/archive 규칙을 lowercase canonical로 정리
**Component**: Supporting Skills / References
**Priority**: P1
**Type**: Refactor

**Description**:  
`pr-review`, `guide-create` 등 주변 스킬과 reference 문서에서 backup/archive 및 결과 파일 경로를 lowercase canonical 규칙으로 정리한다. 특히 `PREV_*`, `PR_REVIEW.md` 같은 남은 대문자 경로를 신규 canonical 규칙에 맞춘다.

**Acceptance Criteria**:
- [ ] `pr_review.md`와 `prev_pr_review_<timestamp>.md` canonical 규칙이 반영된다
- [ ] `guide-create` backup 규칙이 `prev_guide_<slug>_<timestamp>.md` canonical로 바뀐다
- [ ] supporting skill examples/reference도 같은 이름을 사용한다
- [ ] legacy uppercase naming은 fallback 또는 historical note로만 남는다

**Target Files**:
- [M] `.codex/skills/pr-review/SKILL.md`
- [M] `.codex/skills/guide-create/SKILL.md`
- [M] `.codex/skills/guide-create/references/output-format.md`
- [M] `.claude/skills/pr-review/SKILL.md`
- [M] `.claude/skills/pr-review/examples/sample-review.md`
- [M] `.claude/skills/guide-create/SKILL.md`
- [M] `.claude/skills/guide-create/references/output-format.md`

**Technical Notes**:
- `guide-create`는 이미 guide 본문은 소문자지만 backup prefix만 대문자라서 전환 난도가 낮다
- `pr-review`는 output filename과 backup filename을 둘 다 바꿔야 하므로 input/output contract를 함께 보아야 한다

**Dependencies**: T1

### Task T5: examples / templates / orchestrator references를 canonical path와 일치시킴
**Component**: Mirror Sync
**Priority**: P1
**Type**: Refactor

**Description**:  
Phase 2-3에서 바뀐 canonical path가 예시 문서, reference template, orchestrator contract 전반에 일관되게 반영되도록 마무리 정렬을 수행한다. 문서 본문은 바뀌었는데 example만 legacy 경로를 유지하는 상태를 방지한다.

**Acceptance Criteria**:
- [ ] example/reference/template 문서에서 canonical lowercase path가 일관되게 사용된다
- [ ] uppercase legacy path는 필요한 호환성 설명이 아닌 이상 제거된다
- [ ] `.codex`와 `.claude` 예시 문서가 같은 artifact naming 계약을 따른다
- [ ] repo-wide grep 기준으로 주요 canonical artifact에 대한 uppercase direct reference가 의미 있게 감소한다

**Target Files**:
- [M] `.codex/skills/spec-summary/references/summary-template.md`
- [M] `.codex/skills/spec-summary/examples/summary-output.md`
- [M] `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md`
- [M] `.codex/skills/sdd-autopilot/references/orchestrator-contract.md`
- [M] `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md`
- [M] `.claude/skills/spec-summary/references/summary-template.md`
- [M] `.claude/skills/spec-summary/examples/summary-output.md`
- [M] `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md`
- [M] `.claude/skills/sdd-autopilot/references/orchestrator-contract.md`
- [M] `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md`
- [M] `.claude/skills/pr-review/examples/sample-review.md`

**Technical Notes**:
- 실제 구현 시 T2/T3/T4에서 일부 파일이 이미 수정될 수 있다. 이 Task는 잔여 example/reference drift를 정리하는 마무리 역할로 보는 편이 적절하다
- 동일 파일 중복 수정이 생기지 않도록 실제 실행에서는 T2/T3/T4 write ownership을 먼저 고정해야 한다

**Dependencies**: T2, T3, T4

### Task T6: repo-wide path 검증과 historical rename defer 범위 문서화
**Component**: Repo Spec Policy
**Priority**: P1
**Type**: Test

**Description**:  
canonical path 전환 후 repo 전역에서 uppercase artifact direct reference가 어디까지 남는지 검증하고, 의도적으로 남기는 legacy fallback/historical paths의 범위를 문서화한다. 1차 rollout이 contract 정리인지, 실제 historical rename까지 포함하는지 경계를 명확히 한다.

**Acceptance Criteria**:
- [ ] repo-wide grep으로 주요 artifact 경로의 잔여 uppercase reference를 점검한다
- [ ] intentional legacy fallback과 accidental stale reference를 구분한다
- [ ] historical rename이 이번 범위 밖이면 그 사실이 문서에 남는다
- [ ] follow-up migration open question이 정리된다

**Target Files**:
- [M] `_sdd/spec/main.md` -- migration boundary / legacy fallback 범위 최종 정리
- [TBD] 필요 시 별도 migration note 문서 추가 -- 실제 검증 결과가 길 경우 보조 문서 분리 검토

**Technical Notes**:
- 이 Task는 새 canonical path 선언 이후 남는 legacy uppercase reference를 "오류"와 "의도된 호환성"으로 분리하는 마감 단계다
- 별도 migration note가 필요 없으면 `_sdd/spec/main.md`의 appendix/open questions로 처리해도 된다

**Dependencies**: T2, T3, T4, T5

## Parallel Execution Summary

- `T1`은 선행되어야 한다. canonical naming policy와 artifact map이 확정되어야 이후 skill 계약이 흔들리지 않는다.
- `T2`, `T3`, `T4`는 `T1` 이후 병렬화 가능하다.
  - `T2` write scope: implementation 계열 + autopilot 계열
  - `T3` write scope: spec/reporting 계열
  - `T4` write scope: pr-review / guide-create 계열
- `T5`는 examples/reference drift 정리 성격이므로 `T2-T4` 이후 수행하는 편이 안전하다.
- `T6`는 검증 및 migration boundary 정리이므로 마지막에 수행한다.
- mirror 파일은 같은 task 안에서 한 worker가 `.codex`와 `.claude`를 함께 소유하는 편이 parity drift를 줄인다.

## Risks and Mitigations

- **Risk**: lowercase output만 바꾸고 uppercase input fallback을 빼먹으면 workflow가 깨질 수 있다.  
  **Mitigation**: output contract와 input source 목록을 항상 쌍으로 갱신한다.
- **Risk**: `_sdd/spec/main.md`와 실제 skill contract가 다시 어긋날 수 있다.  
  **Mitigation**: T1을 먼저 수행하고, T6에서 repo-wide grep으로 잔여 drift를 검증한다.
- **Risk**: `.codex`/`.claude`/agent mirror 동기화 누락으로 플랫폼 parity가 깨질 수 있다.  
  **Mitigation**: mirror ownership을 task 단위로 묶고, 같은 task에서 동시 수정한다.
- **Risk**: `spec-review`처럼 기존 root/logs 경로가 이미 혼재한 경우 canonical path 결정이 지연될 수 있다.  
  **Mitigation**: T1에서 canonical path를 먼저 고정하고, legacy path는 fallback/historical note로만 남긴다.
- **Risk**: historical artifact rename 범위를 무리하게 포함하면 변경 규모가 급격히 커진다.  
  **Mitigation**: 이번 draft는 contract 정리와 신규 출력 규칙에 집중하고, historical cleanup은 open question으로 남긴다.

## Open Questions

- `decision_log.md`를 1차 rollout의 필수 항목으로 포함할지, 아니면 reporting/implementation 계열 이후 2차로 넘길지?
- `spec_review_report.md` canonical path를 `_sdd/spec/logs/`로 고정하는 데 동의하는지?
- `SYNC_*` historical artifact는 이번 기능 범위 밖으로 두는지?
- 실제 historical file rename을 나중에 할 경우, symlink/duplicate/one-shot rename 중 어떤 방식을 선호하는지?
