# Feature Draft: Orchestrator Storage Relocation

**Date**: 2026-04-03
**Author**: autopilot (discussion 기반)
**Target Spec**: `_sdd/spec/main.md`
**Status**: Draft

---

<!-- spec-update-todo-input-start -->
# Part 1: Spec Patch Draft

> This patch can be copy-pasted into the corresponding spec section,
> or used as input for the `spec-update-todo` skill.

# Spec Update Input

**Date**: 2026-04-03
**Author**: sdd-autopilot
**Target Spec**: `_sdd/spec/main.md`

## Improvements

### Improvement: 오케스트레이터 저장 경로 `_sdd/pipeline/orchestrators/`로 통합

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `핵심 설계 (§2)` > `2-Phase Orchestration 패턴`

**Current State**: 오케스트레이터가 `.claude/skills/orchestrator_<topic>/SKILL.md` (또는 `.codex/skills/orchestrator_<topic>/SKILL.md`)에 생성되어 스킬로 자동 등록됨. 완료 후 `_sdd/pipeline/orchestrators/<topic>_<timestamp>/`로 아카이브.

**Proposed**: 오케스트레이터를 `_sdd/pipeline/orchestrators/orchestrator_<topic>.md` 단일 플랫 파일로 저장. 스킬 등록 및 아카이브 이동 단계 제거. 활성/완료 구분은 `_sdd/pipeline/log_*.md`의 status 필드로 판단.

**Reason**: (1) 사용하지 않는 오케스트레이터가 스킬 목록에 남아 오염 (2) resume 기능이 실전에서 사용되지 않아 스킬 등록의 이점 없음 (3) 생성→스킬등록→실행→아카이브 라이프사이클이 불필요하게 복잡

### Improvement: 오케스트레이터 파일 형식 단순화

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `핵심 설계 (§2)` > `2-Phase Orchestration 패턴`

**Current State**: 오케스트레이터가 디렉토리 구조(skill.json + SKILL.md)로 저장됨

**Proposed**: 단일 .md 플랫 파일 (`orchestrator_<topic>.md`)로 변경. 내용 구조(메타데이터, 기능 설명, Pipeline Steps 등)는 기존 orchestrator-contract.md 계약 유지.

**Reason**: 스킬에서 빠져나오면 skill.json과 디렉토리 구조가 불필요. 플랫 파일이 관리 단순.

### Improvement: 아카이브 단계 제거 — 로그 기반 상태 판단

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `핵심 설계 (§2)` > `2-Phase Orchestration 패턴`

**Current State**: 완료된 오케스트레이터를 `_sdd/pipeline/orchestrators/<topic>_<timestamp>/`로 이동(아카이브). Hard Rule #8 (Claude) / #9 (Codex).

**Proposed**: 아카이브 이동 단계 제거. 오케스트레이터는 `_sdd/pipeline/orchestrators/`에 그대로 유지. 활성/완료 구분은 대응하는 로그 파일(`_sdd/pipeline/log_*.md`)의 Status 테이블로 판단. Resume(Step 0)도 로그 기반으로 동작하므로 오케스트레이터 위치에 무관.

**Reason**: 활성→아카이브 2단계 관리가 불필요. 로그가 이미 상태를 추적하고 있으므로 단일 위치로 충분.

## Design Changes

### Design Change: Artifact Map 경로 변경

**Priority**: Medium
**Target Section**: `_sdd/spec/main.md` > `Artifact Map`

**Description**: Artifact Map 테이블에서 오케스트레이터 관련 행 2개 수정:
- `.claude/skills/orchestrator_<topic>/SKILL.md` 또는 `.codex/skills/orchestrator_<topic>/SKILL.md` → `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`
- `_sdd/pipeline/orchestrators/<topic>_<ts>/` (아카이브) 행 제거

### Design Change: 디렉토리 구조도 경로 변경

**Priority**: Medium
**Target Section**: `_sdd/spec/main.md` > `§3 Architecture` > `디렉토리 구조`

**Description**: 디렉토리 구조 다이어그램에서:
- `.claude/skills/orchestrator_<topic>/` 또는 `.codex/skills/orchestrator_<topic>/` 제거
- `_sdd/pipeline/` 하위에 `orchestrators/` 설명을 "활성+완료 오케스트레이터 저장"으로 수정

### Design Change: 플랫폼별 차이 테이블 수정

**Priority**: Medium
**Target Section**: `_sdd/spec/main.md` > `§4 Components` > `플랫폼별 차이`

**Description**: Codex 제한 사항에서 "활성 오케스트레이터는 `.codex/skills/orchestrator_<topic>/`에 두고..." 문구를 `_sdd/pipeline/orchestrators/` 경로로 수정. 양쪽 플랫폼이 동일 경로를 사용하므로 플랫폼별 경로 차이 언급 제거.

### Design Change: 에이전트 호출 경로 테이블 수정

**Priority**: Low
**Target Section**: `_sdd/spec/main.md` > `§4 Components` > `에이전트 목록`

**Description**: 에이전트 Spawn 경로에서 "generated orchestrator"가 `.claude/skills/` 또는 `.codex/skills/`가 아닌 `_sdd/pipeline/orchestrators/`의 파일임을 반영.

## Failure Modes

| 시나리오 | 실패 시 | 사용자 가시성 | 처리 방안 |
|---------|---------|-------------|----------|
| resume 시 오케스트레이터 파일을 찾지 못함 | 파이프라인 재개 불가 | Step 0에서 "재개 불가" 메시지 | 로그 파일의 orchestrator 경로를 새 경로 형식으로 참조하도록 수정 |
| 기존 아카이브된 오케스트레이터와 경로 충돌 | 기존 `_sdd/pipeline/orchestrators/<topic>_<ts>/` 디렉토리와 새 플랫 파일이 공존 | 없음 (기존 아카이브는 디렉토리, 새 파일은 .md) | 기존 아카이브는 그대로 유지, 새로 생성되는 것만 플랫 파일 형식 적용 |

## Notes

- 논의 문서: `_sdd/discussion/discussion_orchestrator_storage_relocation.md`
- `sdd-reasoning-reference.md`는 오케스트레이터 경로를 직접 참조하지 않으므로 수정 불필요
- 기존 `_sdd/pipeline/orchestrators/` 디렉토리에 이미 아카이브된 디렉토리가 있을 수 있음. 하위 호환성 문제 없음 (디렉토리와 .md 파일 공존 가능)

<!-- spec-update-todo-input-end -->

---

# Part 2: Implementation Plan

## Overview

sdd-autopilot 오케스트레이터의 저장 경로를 `.claude/skills/` (`.codex/skills/`) 에서 `_sdd/pipeline/orchestrators/`로 이동하고, 파일 형식을 디렉토리(SKILL.md)에서 플랫 파일(.md)로 변경한다. 아카이브 이동 단계를 제거하고 로그 기반 상태 판단으로 전환한다.

## Scope

### In Scope
- `.claude/skills/sdd-autopilot/` 내 SKILL.md, orchestrator-contract.md, sample-orchestrator.md 경로/로직 수정
- `.codex/skills/sdd-autopilot/` 내 동일 파일 경로/로직 수정
- `_sdd/spec/main.md` 오케스트레이터 경로 참조 전체 수정

### Out of Scope
- `sdd-reasoning-reference.md` (오케스트레이터 경로 미참조)
- 기존 아카이브된 오케스트레이터 마이그레이션 (기존 것은 그대로 유지)
- 오케스트레이터 내용 구조(계약) 변경 (경로만 변경, 내용 형식은 유지)

## Components

1. **Claude autopilot 스킬**: `.claude/skills/sdd-autopilot/` 하위 3개 파일
2. **Codex autopilot 스킬**: `.codex/skills/sdd-autopilot/` 하위 3개 파일
3. **글로벌 스펙**: `_sdd/spec/main.md` 오케스트레이터 경로 참조

## Implementation Phases

### Phase 1: Claude autopilot 스킬 수정
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| T1 | SKILL.md AC + Hard Rules 수정 | P0-Critical | - | Claude autopilot |
| T2 | SKILL.md Step 4/7/8 경로·로직 수정 | P0-Critical | - | Claude autopilot |
| T3 | orchestrator-contract.md State Handoff 경로 수정 | P1-High | - | Claude autopilot |
| T4 | sample-orchestrator.md 로그 예시 경로 수정 | P2-Medium | - | Claude autopilot |

### Phase 2: Codex autopilot 스킬 수정
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| T5 | SKILL.md AC + Hard Rules 수정 | P0-Critical | - | Codex autopilot |
| T6 | SKILL.md Step 4/7/8 경로·로직 수정 | P0-Critical | - | Codex autopilot |
| T7 | orchestrator-contract.md State Handoff 경로 수정 | P1-High | - | Codex autopilot |
| T8 | sample-orchestrator.md 로그 예시 경로 수정 | P2-Medium | - | Codex autopilot |

### Phase 3: 스펙 수정
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| T9 | main.md 오케스트레이터 경로 참조 전체 수정 | P1-High | T1, T5 | 글로벌 스펙 |

## Task Details

### Task T1: Claude SKILL.md AC + Hard Rules 수정

**Component**: Claude autopilot
**Priority**: P0-Critical
**Type**: Refactor

**Description**: `.claude/skills/sdd-autopilot/SKILL.md`에서 오케스트레이터 경로 관련 AC와 Hard Rules를 수정한다.

**Acceptance Criteria**:
- [ ] AC2가 `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`를 참조한다
- [ ] AC10 (아카이브 필수)가 제거되었다
- [ ] Hard Rule #3이 새 경로를 참조한다
- [ ] Hard Rule #8 (Archive 필수)이 "로그 기반 상태 관리"로 변경되었다

**Target Files**:
- [M] `.claude/skills/sdd-autopilot/SKILL.md` -- AC2, AC10, Hard Rule #3, #8 수정

**Technical Notes**:
- AC2: `.claude/skills/orchestrator_<topic>/` → `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`에 생성되고
- AC10: 아카이브 행 전체 제거 (AC 번호 재정렬 불필요 — 빈 번호로 남기기보다 행 제거)
- Hard Rule #3: `.claude/skills/orchestrator_<topic>/SKILL.md` → `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`
- Hard Rule #8: "Archive 필수" → "로그 기반 상태 관리: 오케스트레이터는 `_sdd/pipeline/orchestrators/`에 유지. 활성/완료 구분은 로그 파일 status로 판단한다."

**Dependencies**: -

### Task T2: Claude SKILL.md Step 4/7/8 경로·로직 수정

**Component**: Claude autopilot
**Priority**: P0-Critical
**Type**: Refactor

**Description**: 오케스트레이터 생성(Step 4), 실행(Step 7), 최종 요약(Step 8) 단계의 경로 및 아카이브 로직을 수정한다.

**Acceptance Criteria**:
- [ ] Step 4.2 저장 경로가 `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`이다
- [ ] Step 7.1에서 오케스트레이터를 새 경로에서 Read한다
- [ ] Step 8에서 아카이브 이동 로직이 제거되었다
- [ ] Step 8.3 사용자 보고의 오케스트레이터 경로가 새 경로이다

**Target Files**:
- [M] `.claude/skills/sdd-autopilot/SKILL.md` -- Step 4.2 파일 경로, Step 7.1, Step 8 아카이브 로직

**Technical Notes**:
- Step 4.2: `파일 경로: .claude/skills/orchestrator_<topic>/SKILL.md` → `파일 경로: _sdd/pipeline/orchestrators/orchestrator_<topic>.md`
- Step 8: `active orchestrator를 _sdd/pipeline/orchestrators/<topic>_<timestamp>/에 아카이브` 문구 전체 제거
- Step 8.2 최종 보고서: `active orchestrator archive 경로` → 제거 또는 `orchestrator 경로`로 변경

**Dependencies**: -

### Task T3: Claude orchestrator-contract.md 경로 수정

**Component**: Claude autopilot
**Priority**: P1-High
**Type**: Refactor

**Description**: `orchestrator-contract.md`의 Section 10 (State Handoff)에서 오케스트레이터 경로를 수정한다.

**Acceptance Criteria**:
- [ ] Section 10의 `.claude/skills/orchestrator_<topic>/SKILL.md` → `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`로 변경되었다

**Target Files**:
- [M] `.claude/skills/sdd-autopilot/references/orchestrator-contract.md` -- Section 10 State Handoff 경로

**Technical Notes**:
- 변경 행: `- .claude/skills/orchestrator_<topic>/SKILL.md -> autopilot 실행 입력`
- 변경 후: `- _sdd/pipeline/orchestrators/orchestrator_<topic>.md -> autopilot 실행 입력`

**Dependencies**: -

### Task T4: Claude sample-orchestrator.md 경로 수정

**Component**: Claude autopilot
**Priority**: P2-Medium
**Type**: Refactor

**Description**: `sample-orchestrator.md`의 로그 파일 예시에서 오케스트레이터 참조 경로를 수정한다.

**Acceptance Criteria**:
- [ ] 로그 예시의 오케스트레이터 경로가 `_sdd/pipeline/orchestrators/orchestrator_<topic>.md` 형식이다

**Target Files**:
- [M] `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md` -- 로그 예시 내 오케스트레이터 경로

**Technical Notes**:
- `.claude/skills/orchestrator_image_cls_finetune/SKILL.md` → `_sdd/pipeline/orchestrators/orchestrator_image_cls_finetune.md`
- `_sdd/pipeline/orchestrator_jwt_auth_20260316_143000.md` (기존 아카이브 형식) → `_sdd/pipeline/orchestrators/orchestrator_jwt_auth.md`

**Dependencies**: -

### Task T5: Codex SKILL.md AC + Hard Rules 수정

**Component**: Codex autopilot
**Priority**: P0-Critical
**Type**: Refactor

**Description**: `.codex/skills/sdd-autopilot/SKILL.md`에서 오케스트레이터 경로 관련 AC와 Hard Rules를 수정한다.

**Acceptance Criteria**:
- [ ] AC2가 `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`를 참조한다
- [ ] AC10 (아카이브 필수)가 제거되었다
- [ ] Hard Rule #3이 새 경로를 참조한다
- [ ] Hard Rule #9 (Archive 필수)가 "로그 기반 상태 관리"로 변경되었다

**Target Files**:
- [M] `.codex/skills/sdd-autopilot/SKILL.md` -- AC2, AC10, Hard Rule #3, #9 수정

**Technical Notes**:
- Codex 버전은 `.codex/skills/orchestrator_<topic>/SKILL.md` 경로 사용. 동일하게 `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`로 변경.
- Hard Rule 번호가 Claude(#8)와 Codex(#9)에서 다를 수 있음 — Codex는 #8이 Agent lifecycle 수집, #9가 Archive.

**Dependencies**: -

### Task T6: Codex SKILL.md Step 4/7/8 경로·로직 수정

**Component**: Codex autopilot
**Priority**: P0-Critical
**Type**: Refactor

**Description**: Codex 버전의 오케스트레이터 생성/실행/완료 단계 경로를 수정한다.

**Acceptance Criteria**:
- [ ] Step 4 저장 경로가 `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`이다
- [ ] Step 7에서 새 경로를 참조한다
- [ ] Step 8에서 아카이브 이동 로직이 제거되었다

**Target Files**:
- [M] `.codex/skills/sdd-autopilot/SKILL.md` -- Step 4, 7, 8 경로·로직

**Technical Notes**:
- `.codex/skills/orchestrator_<topic>/SKILL.md` → `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`
- 아카이브 관련 문구 제거

**Dependencies**: -

### Task T7: Codex orchestrator-contract.md 경로 수정

**Component**: Codex autopilot
**Priority**: P1-High
**Type**: Refactor

**Description**: Codex `orchestrator-contract.md`의 Section 10에서 경로를 수정한다.

**Acceptance Criteria**:
- [ ] `.codex/skills/orchestrator_<topic>/SKILL.md` → `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`로 변경되었다

**Target Files**:
- [M] `.codex/skills/sdd-autopilot/references/orchestrator-contract.md` -- Section 10 State Handoff 경로

**Dependencies**: -

### Task T8: Codex sample-orchestrator.md 경로 수정

**Component**: Codex autopilot
**Priority**: P2-Medium
**Type**: Refactor

**Description**: Codex `sample-orchestrator.md`의 로그 예시에서 오케스트레이터 경로를 수정한다.

**Acceptance Criteria**:
- [ ] 로그 예시의 오케스트레이터 경로가 `_sdd/pipeline/orchestrators/orchestrator_<topic>.md` 형식이다

**Target Files**:
- [M] `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md` -- 로그 예시 내 오케스트레이터 경로

**Technical Notes**:
- `.codex/skills/orchestrator_jwt_auth/SKILL.md` → `_sdd/pipeline/orchestrators/orchestrator_jwt_auth.md`

**Dependencies**: -

### Task T9: 글로벌 스펙 오케스트레이터 경로 수정

**Component**: 글로벌 스펙
**Priority**: P1-High
**Type**: Refactor

**Description**: `_sdd/spec/main.md`에서 오케스트레이터 저장 경로를 참조하는 모든 위치를 수정한다. 최소 12개 참조 지점.

**Acceptance Criteria**:
- [ ] `.claude/skills/orchestrator_<topic>/` 및 `.codex/skills/orchestrator_<topic>/` 참조가 모두 `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`로 변경되었다
- [ ] `_sdd/pipeline/orchestrators/<topic>_<ts>/` 아카이브 참조가 제거되었다
- [ ] Artifact Map 테이블이 새 경로를 반영한다
- [ ] 디렉토리 구조 다이어그램이 새 경로를 반영한다
- [ ] 플랫폼별 차이 테이블에서 오케스트레이터 경로 차이 언급이 제거되었다

**Target Files**:
- [M] `_sdd/spec/main.md` -- 오케스트레이터 경로 참조 전체 (약 12개 지점)

**Technical Notes**:
주요 수정 지점 (줄 번호는 현재 버전 기준, 변경 시 밀릴 수 있음):
- L66: `generated orchestrator를 통해` — 문맥만 수정
- L78: `sdd-autopilot이나 generated orchestration skill이 실행 단위를 재사용` — 문맥 수정
- L95: `generated orchestration skill이 custom agent spawn` — 문맥 수정
- L337: `[.claude/skills/orchestrator_<topic>/ or .codex/skills/orchestrator_<topic>/]` → `[_sdd/pipeline/orchestrators/orchestrator_<topic>.md]`
- L429: Artifact Map 오케스트레이터 행 → 새 경로
- L432: Artifact Map 아카이브 행 → 제거
- L603: pipeline 디렉토리 설명 → 아카이브 언급 수정
- L622: Codex 제한 사항 → 경로 통일 반영
- 에이전트 Spawn 경로 테이블 (L482-504): "generated orchestrator" 참조는 유지하되, 경로가 `_sdd/` 하위임을 반영

**Dependencies**: T1, T5 (스킬 파일 수정이 선행되어야 스펙과 정합)

## Parallel Execution Summary

| Phase | Total Tasks | Max Parallel | Sequential (conflicts) |
|-------|-------------|--------------|----------------------|
| Phase 1 (Claude) | 4 | 4 | 없음 — 모두 다른 파일 |
| Phase 2 (Codex) | 4 | 4 | 없음 — 모두 다른 파일 |
| Phase 3 (스펙) | 1 | 1 | T9는 단일 파일 수정 |

Phase 1과 Phase 2는 **완전 병렬** 가능 (다른 디렉토리의 다른 파일).
Phase 3는 Phase 1, 2 완료 후 진행 권장 (스펙이 스킬 파일의 경로를 참조하므로).

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| 기존 아카이브 경로 형식(`<topic>_<ts>/`)의 오케스트레이터가 남아있음 | 혼란 가능 | 기존 것은 그대로 유지, 신규만 플랫 파일 적용. Step 0 resume 로직은 로그 파일 기반이라 영향 없음 |
| Codex SKILL.md의 Hard Rule 번호가 Claude와 다를 수 있음 | 잘못된 Rule 수정 | 각 파일의 실제 번호 확인 후 수정 (Claude #8 = Archive, Codex #9 = Archive) |

## Open Questions

- (없음 — 논의에서 모든 결정 사항 확정됨)

## Model Recommendation

전체 9개 태스크가 모두 텍스트 수정(경로 치환 + 문구 조정)이므로 sonnet 모델로 충분합니다. Phase 1과 Phase 2를 병렬로 실행하면 효율적입니다.

---

## Next Steps

### Apply Spec Patch
- **Method A (automatic)**: Run `spec-update-todo` → Part 1을 입력으로 사용
- **Method B (manual)**: Part 1의 각 항목을 Target Section에 복사

### Execute Implementation
- **Parallel**: Run `implementation` skill → Part 2를 계획으로 사용
- **Sequential**: Phase 1 + Phase 2 병렬 → Phase 3 순차
