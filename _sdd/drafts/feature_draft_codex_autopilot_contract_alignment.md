# Feature Draft: Codex Autopilot Contract Alignment

<!-- spec-update-todo-input-start -->
# Part 1: Spec Patch Draft
# Spec Update Input

**Date**: 2026-03-24
**Author**: Codex
**Target Spec**: `_sdd/spec/main.md`
**Spec Update Classification**: Improvement

## Background & Motivation Updates

### Update Item: Codex autopilot execution contract drift correction
**Type**: Improvement
**Target Section**: `sdd-autopilot`
**Current**: Codex autopilot skill, review agent, Ralph loop contract, sample orchestrator, and spec summary are partially out of sync. The runtime contract does not fully enforce Phase 1.5 approval/pre-flight, review severity buckets differ between autopilot and implementation review, and Ralph artifact expectations differ across runtime and reference files.
**Proposed**: Align the Codex execution contract so that Phase 1.5 requires explicit approval after pre-flight, review-fix operates on a shared severity schema, and Ralph output expectations converge on executable `run.sh` plus the currently required workspace artifacts.
**Reason**: The current drift can cause generated orchestrators and downstream verification to reason against incompatible contracts.

## Design Changes

### Update Item: Phase 1.5 checkpoint becomes mandatory before autonomous execution
**Type**: Improvement
**Target Section**: `sdd-autopilot` process / checkpoint / output contract
**Current**: Step 6 verifies the orchestrator and shares a short summary, but it does not explicitly require a pre-flight check against `_sdd/env.md` and `.codex/config.toml` or an approval gate before Step 7.
**Proposed**: Require Step 6 to run pre-flight, summarize resource/runtime risk, request explicit approval or modification, and only then enter Phase 2.
**Reason**: This matches the documented 2-phase orchestration model and prevents autonomous execution from starting on an unvalidated pipeline.

### Update Item: Review severity schema alignment
**Type**: Improvement
**Target Section**: `implementation-review` output contract, `sdd-autopilot` review-fix contract
**Current**: `implementation-review` emits `Critical / Quality / Improvements`, while the Codex autopilot contract, sample orchestrator, and docs expect `critical / high / medium / low`.
**Proposed**: Standardize the review output contract on `Critical / High / Medium / Low`. Autopilot continues to require fixes for `Critical / High / Medium`, while `Low` remains log-only unless explicitly requested.
**Reason**: The orchestrator needs deterministic severity buckets to decide fix scope and loop termination.

### Update Item: Ralph loop output and verification alignment
**Type**: Improvement
**Target Section**: `ralph-loop-init`
**Current**: The actual Codex Ralph agent/skill require `CHECKS.md`, `state.md`, and `run.sh`, but some Codex references and the spec still mention `PROMPT.md` and `config.sh`. The current Ralph contract also does not require `run.sh` to be executable.
**Proposed**: Standardize the required Ralph artifacts on `CHECKS.md`, `state.md`, and executable `run.sh`, and update the Codex reference/spec text to match.
**Reason**: Autopilot loads these references before generating orchestrators, so stale artifact names can create invalid verification steps.

### Update Item: Completion-time orchestrator archive
**Type**: Improvement
**Target Section**: `sdd-autopilot` finalize / artifact map
**Current**: The Codex autopilot skill writes log/report artifacts but does not explicitly archive the active orchestrator into `_sdd/pipeline/orchestrators/<topic>_<timestamp>/`.
**Proposed**: Require finalization to archive the active orchestrator after successful completion and include the archive path in the output contract.
**Reason**: This keeps active-vs-completed state unambiguous and preserves the documented resume/archive lifecycle.

## Improvements

### Update Item: Touched skill metadata stays coherent with the mirrored skill body
**Type**: Improvement
**Target Section**: Codex skill metadata
**Current**: Some touched Codex skills already have `skill.json` / `SKILL.md` version drift.
**Proposed**: For touched skills in this patch, align `skill.json` version metadata with the current mirrored skill body version.
**Reason**: Users and tooling should not see different versions for the same active contract.

## Failure Modes

| 시나리오 | 실패 시 | 사용자 가시성 | 처리 방안 |
|----------|---------|---------------|-----------|
| 승인 게이트 없이 Phase 2 진입 | 잘못된 파이프라인이 자율 실행됨 | autopilot 실행 중 리소스/계약 오류 발생 | Step 6에 pre-flight + explicit approval 추가 |
| severity schema 불일치 | review-fix 종료 조건 계산 실패 | implementation-review 결과를 autopilot이 해석하지 못함 | implementation-review와 sample/reference를 공통 4단계 severity로 통일 |
| Ralph artifact 명칭 드리프트 | 존재하지 않는 파일 검증 시도 | ralph verification false negative | runtime/reference/spec를 실제 산출물 기준으로 통일 |
| run.sh 비실행 파일 생성 | downstream verify 실패 | `ralph/run.sh` 존재하지만 실행되지 않음 | shebang + executable bit를 Ralph contract에 명시 |
| 완료 후 active orchestrator 미아카이브 | resume 상태 혼동 | 완료된 오케스트레이터가 active처럼 남음 | Step 8에 archive 절차 추가 |

## Notes

- 이번 패치는 Codex runtime-defining 파일과 직접 연결된 reference/spec 동기화에 집중한다.
- `docs/SDD_WORKFLOW.md`, `docs/en/SDD_WORKFLOW.md`의 Ralph 설명은 더 넓은 범위의 문서 정리로 보이며, 이번 패치에서는 후속 정리 후보로 남긴다.

## Open Questions

- `docs/SDD_WORKFLOW*.md`의 Ralph 구조를 현재 Codex minimal contract로 축소할지, 아니면 별도 full Ralph mode를 다시 복원할지는 후속 결정이 필요하다.
<!-- spec-update-todo-input-end -->

# Part 2: Implementation Plan

## Overview

Codex autopilot과 하위 agent들이 동일한 실행 계약을 사용하도록 Step 6/8, review severity schema, Ralph artifact contract, 그리고 직접 참조되는 sample/spec 파일을 함께 정렬한다.

## Scope

### In Scope

- `.codex/skills/sdd-autopilot/SKILL.md`의 checkpoint / pre-flight / archive contract 보강
- `.codex/agents/implementation-review.toml`와 mirror skill의 severity schema 정렬
- `.codex/agents/ralph-loop-init.toml`와 mirror skill의 executable runner contract 보강
- Codex autopilot reference/sample/spec에서 stale contract 문구 수정
- 이번 패치에서 touched skill의 `skill.json` metadata 정렬

### Out of Scope

- Ralph 전체 워크플로우 문서(`docs/SDD_WORKFLOW*.md`) 구조 재설계
- Claude-side agent/skill contract 변경
- 새 agent 추가 또는 autopilot pipeline shape 재설계

## Components

- Autopilot core contract
- Review severity contract
- Ralph runner/artifact contract
- Codex reference/spec synchronization
- Touched skill metadata

## Implementation Phases

### Phase 1: Patch planning artifacts and core autopilot contract

- feature draft 작성
- Step 6 checkpoint / pre-flight / approval 계약 보강
- Step 8 archive 계약 보강

### Phase 2: Align dependent agent contracts

- implementation-review severity schema를 4단계로 정렬
- ralph-loop-init runner contract에 executable requirement 추가

### Phase 3: Sync supporting references and spec summary

- sample orchestrator / reasoning reference 수정
- `_sdd/spec/main.md`의 직접 연결된 Codex contract 요약 수정
- touched skill metadata 정렬

## Task Details

### Task FD-1: Strengthen autopilot checkpoint and finalize contracts
**Component**: Autopilot core contract
**Priority**: P0
**Type**: Infrastructure

**Description**: `sdd-autopilot` skill에 Step 6 pre-flight + approval gate와 Step 8 orchestrator archive 절차를 명시하고 output contract를 갱신한다.

**Acceptance Criteria**:
- [ ] Step 6이 `_sdd/env.md`와 `.codex/config.toml` 기반 pre-flight를 요구한다.
- [ ] Step 6이 explicit approval / modify / cancel 분기를 요구한다.
- [ ] Step 8이 `_sdd/pipeline/orchestrators/<topic>_<timestamp>/` archive 절차를 명시한다.
- [ ] output contract에 archive artifact가 반영된다.

**Target Files**:
- [M] `.codex/skills/sdd-autopilot/SKILL.md`

**Technical Notes**: Phase 2 이후 `request_user_input` 금지 규칙과 충돌하지 않도록 승인 질문은 Step 6 안에서만 수행한다.
**Dependencies**: 없음

### Task FD-2: Align implementation review severity schema
**Component**: Review severity contract
**Priority**: P0
**Type**: Infrastructure

**Description**: implementation-review agent와 mirror skill의 findings format / classification rules를 `Critical / High / Medium / Low`로 통일하고 stale plan fallback 서술도 새 schema에 맞춘다.

**Acceptance Criteria**:
- [ ] report template이 4단계 severity 섹션을 가진다.
- [ ] classification 규칙이 autopilot review-fix contract와 호환된다.
- [ ] mirror skill과 agent 본문이 동일하게 유지된다.

**Target Files**:
- [M] `.codex/agents/implementation-review.toml`
- [M] `.codex/skills/implementation-review/SKILL.md`

**Technical Notes**: `Low`는 log-only 후속 항목으로 남기고, fix loop의 필수 수정 대상은 `Critical / High / Medium`으로 둔다.
**Dependencies**: 없음

### Task FD-3: Align Ralph runtime contract
**Component**: Ralph runner/artifact contract
**Priority**: P1
**Type**: Infrastructure

**Description**: Ralph agent와 mirror skill에 executable `run.sh` requirement를 추가하고, supporting Codex references/spec가 같은 artifact set을 바라보도록 수정한다.

**Acceptance Criteria**:
- [ ] Ralph AC/Hard Rules/Step 5가 shebang + executable `run.sh`를 요구한다.
- [ ] reasoning reference가 `CHECKS.md`, `state.md`, `run.sh` 기준으로 갱신된다.
- [ ] `_sdd/spec/main.md`의 Ralph output 설명이 실제 Codex contract와 맞는다.

**Target Files**:
- [M] `.codex/agents/ralph-loop-init.toml`
- [M] `.codex/skills/ralph-loop-init/SKILL.md`
- [M] `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md`
- [M] `_sdd/spec/main.md`

**Technical Notes**: broader Ralph docs drift는 이번 patch scope 밖으로 남기되, direct Codex runtime references는 모두 정렬한다.
**Dependencies**: 없음

### Task FD-4: Sync sample orchestrator and spec examples to the new contract
**Component**: Codex reference/spec synchronization
**Priority**: P1
**Type**: Documentation

**Description**: sample orchestrator와 spec summary/examples가 checkpoint, severity, archive expectations을 현재 contract와 모순 없이 보여주도록 갱신한다.

**Acceptance Criteria**:
- [ ] sample orchestrator review-fix loop가 `critical/high/medium` 기준과 호환된다.
- [ ] spec summary의 review-fix 종료 조건이 새 contract와 맞는다.
- [ ] archive / Phase 1.5 expectations이 문서 간 충돌 없이 유지된다.

**Target Files**:
- [M] `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md`
- [M] `_sdd/spec/main.md`
- [M] `docs/AUTOPILOT_GUIDE.md`

**Technical Notes**: `docs/AUTOPILOT_GUIDE.md`는 이미 approval/pre-flight와 4단계 severity를 설명하므로 필요한 최소 수정만 고려한다.
**Dependencies**: Task FD-1, Task FD-2, Task FD-3

### Task FD-5: Sync touched skill metadata
**Component**: Touched skill metadata
**Priority**: P2
**Type**: Configuration

**Description**: 이번에 수정한 mirror skill들의 `skill.json` version을 현재 `SKILL.md` frontmatter version과 맞춘다.

**Acceptance Criteria**:
- [ ] touched skill의 `skill.json` / `SKILL.md` version mismatch가 제거된다.

**Target Files**:
- [M] `.codex/skills/implementation-review/skill.json`
- [M] `.codex/skills/ralph-loop-init/skill.json`

**Technical Notes**: 이번 patch에서 content version bump는 하지 않고 existing mirrored version에 맞춘다.
**Dependencies**: Task FD-2, Task FD-3

## Parallel Execution Summary

- `FD-2`와 `FD-3`는 서로 다른 mirror pair를 다루므로 병렬 가능하다.
- `FD-1`은 autopilot core contract이므로 먼저 진행하는 편이 안전하다.
- `FD-4`는 `FD-1`~`FD-3`의 결과를 반영해야 하므로 마지막에 동기화한다.
- `FD-5`는 touched skill 본문이 확정된 뒤 순차로 마무리한다.

## Risks and Mitigations

- Risk: review severity를 4단계로 바꾸면서 기존 해석이 흔들릴 수 있다.
  Mitigation: autopilot fix scope는 그대로 `Critical / High / Medium`으로 고정하고 `Low`는 log-only로 명시한다.
- Risk: checkpoint gate 추가가 autopilot 흐름을 과도하게 복잡하게 만들 수 있다.
  Mitigation: Step 6에서 단일 승인 질문만 허용하고 수정 요청 시 Step 4/5로 되돌린다.
- Risk: Ralph broader docs와 direct runtime contract가 계속 어긋날 수 있다.
  Mitigation: 이번에는 direct Codex runtime references만 정렬하고, broader docs는 follow-up으로 분리 기록한다.

## Open Questions

- broader Ralph 문서군을 현재 minimal contract에 맞출지, 아니면 별도 full Ralph workspace 모드로 유지할지 추후 결정 필요.
