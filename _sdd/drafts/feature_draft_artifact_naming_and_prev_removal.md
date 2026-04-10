# Feature Draft: Artifact Naming Convention Transition & prev/ Backup Removal

<!-- spec-update-todo-input-start -->
# Part 1: Temporary Spec Draft

## Change Summary

모든 스킬/에이전트에서 `prev/` 백업 로직을 완전 제거하고, 6개 쓰기 스킬의 산출물 파일명을 `<YYYY-MM-DD>_<filename>_<slug>.md` 패턴으로 전환한다. downstream 스킬의 입력 경로/glob 패턴을 새 패턴에 맞게 업데이트하고, spec-snapshot의 `prev/` 제외 규칙도 제거한다. 모든 변경은 `.claude/skills/`, `.claude/agents/`, `.codex/skills/`, `.codex/agents/` 4개 디렉토리에 동시 적용한다.

**근거**: git이 이미 버전 관리를 담당하며 실제 prev/ 참조 사례가 없다. slug 기반 파일명은 파일 시스템에서 히스토리를 유지하고 feature-draft에서 이미 검증된 패턴이다.

**참조 토론**: `_sdd/discussion/discussion_artifact_naming_and_prev_removal.md` (2026-04-10, 6 라운드)

## Scope Delta

### In-Scope

1. **prev/ 백업 로직 제거**: spec 스킬 6개(spec-create, spec-update-todo, spec-update-done, spec-rewrite, spec-upgrade, spec-summary) + 쓰기 스킬 4개(implementation-review, implementation, pr-review, guide-create)에서 prev/ 관련 규칙/로직 전체 제거
2. **spec-snapshot prev/ 제외 규칙 제거**: `prev/` 디렉토리가 더 이상 생성되지 않으므로 제외 규칙 자체가 불필요
3. **slug 기반 파일명 전환**: feature-draft, implementation-plan, implementation-review, implementation(report), pr-review, guide-create의 산출물 경로를 `<YYYY-MM-DD>_<filename>_<slug>.md`로 전환
4. **읽기 경로 업데이트**: implementation, implementation-review, spec-update-done, spec-summary, sdd-autopilot에서 slug 기반 파일을 읽기 위한 glob 패턴 업데이트
5. **global spec guardrails 업데이트**: `main.md` Guardrails의 prev/ 백업 언급 제거
6. **4개 디렉토리 동시 적용**: `.claude/skills/`, `.claude/agents/`, `.codex/skills/`, `.codex/agents/`

### Out-of-Scope

- 역사적 기록 파일 수정 (`_sdd/spec/DECISION_LOG.md`, `_sdd/spec/logs/changelog.md` 등)
- 기존 `_sdd/spec/prev/` 디렉토리의 물리적 삭제 (별도 정리 작업)
- spec 스킬의 파일명 패턴 변경 (spec은 덮어쓰기 방식 유지)
- discussion, investigate, ralph-loop-init, second-opinion, write-phased, git, spec-review 등 영향 없는 스킬

## Contract/Invariant Delta

### Contracts

| ID | Type | Description |
|----|------|-------------|
| C1 | REMOVE | 모든 스킬에서 `prev/prev_<filename>_<timestamp>.md` 백업 생성 계약 제거 |
| C2 | MODIFY | feature-draft 산출물 경로: `feature_draft_<name>.md` -> `<YYYY-MM-DD>_feature_draft_<slug>.md` |
| C3 | MODIFY | implementation-plan 산출물 경로: `implementation_plan.md` -> `<YYYY-MM-DD>_implementation_plan_<slug>.md` |
| C4 | MODIFY | implementation-review 산출물 경로: `implementation_review.md` -> `<YYYY-MM-DD>_implementation_review_<slug>.md` |
| C5 | MODIFY | implementation report 산출물 경로: `implementation_report.md` -> `<YYYY-MM-DD>_implementation_report_<slug>.md` |
| C6 | MODIFY | pr-review 산출물 경로: `pr_review.md` -> `<YYYY-MM-DD>_pr_review_<slug>.md` |
| C7 | MODIFY | guide-create 산출물 경로: `guide_<slug>.md` -> `<YYYY-MM-DD>_guide_<slug>.md` |
| C8 | MODIFY | downstream 스킬의 입력 탐색 순서에 slug glob 패턴 추가 |

### Invariants

| ID | Type | Description |
|----|------|-------------|
| I1 | REMOVE | "변경 전 원본을 `prev/` 백업한다" guardrail 제거 (global spec main.md) |
| I2 | ADD | slug 기반 파일명 패턴 `<YYYY-MM-DD>_<filename>_<slug>.md`가 모든 쓰기 스킬에서 일관 적용된다 |
| I3 | REMOVE | spec-snapshot에서 `prev/` 디렉토리 제외 규칙 제거 |
| I4 | PRESERVE | `.claude/`와 `.codex/`의 미러 관계 유지 -- 동일 변경이 양쪽에 적용된다 |

## Touchpoints

| Area | Files | Why |
|------|-------|-----|
| Global spec guardrails | `_sdd/spec/main.md` (line 63) | prev/ 백업 guardrail이 삭제 대상 |
| Spec 스킬 Hard Rules | `spec-create`, `spec-update-todo`, `spec-update-done`, `spec-rewrite`, `spec-upgrade`, `spec-summary` (SKILL.md + agent mirrors) | prev/ 백업 규칙이 Hard Rules에 있음 |
| 쓰기 스킬 산출물 경로 | `feature-draft`, `implementation-plan`, `implementation-review`, `implementation`, `pr-review`, `guide-create` (SKILL.md + agent mirrors) | 파일명 패턴과 prev/ 로직 동시 변경 |
| 읽기 스킬 입력 경로 | `implementation`, `implementation-review`, `spec-update-done`, `spec-summary` (SKILL.md + agent mirrors) | slug 기반 glob 패턴 필요 |
| Autopilot 예시 | `sdd-autopilot/examples/sample-orchestrator.md` (양 플랫폼) | 예시의 산출물 경로가 바뀜 |
| Snapshot 제외 규칙 | `spec-snapshot` (양 플랫폼) | prev/ 제외 규칙 제거 |
| Guide output-format | `guide-create/references/output-format.md` (양 플랫폼) | 파일명, 백업 규칙 변경 |
| PR review 예시 | `pr-review/examples/sample-review.md` | prev/ 아카이브 언급 |

## Implementation Plan

### Phase 1: Global Spec Guardrail 업데이트
- `_sdd/spec/main.md`의 guardrails에서 prev/ 백업 언급 제거

### Phase 2: prev/ 제거 (spec 스킬)
- 6개 spec 스킬의 Hard Rules, AC, Error Handling, Process에서 prev/ 관련 내용 제거

### Phase 3: prev/ 제거 + slug 파일명 전환 (쓰기 스킬)
- 6개 쓰기 스킬에서 prev/ 제거와 slug 기반 파일명으로 동시 전환

### Phase 4: 읽기 경로 업데이트
- 5개 downstream 스킬의 입력 탐색 순서에 slug glob 패턴 반영

### Phase 5: spec-snapshot prev/ 제외 규칙 제거
- 양 플랫폼의 spec-snapshot에서 `prev/` 제외 규칙 제거

## Validation Plan

| ID | Type | Description | Targets |
|----|------|-------------|---------|
| V1 | Manual Review | 모든 SKILL.md, agent.md, agent.toml에서 `prev/` 문자열이 더 이상 등장하지 않음 (역사적 기록 제외) | C1, I1, I3 |
| V2 | Manual Review | 6개 쓰기 스킬의 산출물 경로가 `<YYYY-MM-DD>_<filename>_<slug>.md` 패턴을 사용함 | C2, C3, C4, C5, C6, C7, I2 |
| V3 | Manual Review | downstream 스킬의 입력 탐색 순서에 slug glob 패턴이 포함됨 | C8 |
| V4 | Manual Review | `.claude/`와 `.codex/` 양쪽에 동일한 변경이 적용됨 | I4 |
| V5 | Grep Check | `grep -r "prev/" .claude/ .codex/` 결과에서 스킬/에이전트 파일에 prev/ 참조가 없음 | C1, I1, I3 |
| V6 | Manual Review | global spec main.md의 guardrails에서 prev/ 백업 규칙이 제거됨 | I1 |

## Risks / Open Questions

| # | Type | Description |
|---|------|-------------|
| R1 | Risk | 변경 파일 수가 50개 이상으로 매우 많다. 미러 관계 파일 간 불일치가 발생하지 않도록 phase별 grep 검증이 필요하다. |
| R2 | Risk | guide-create는 기존에 이미 `guide_<slug>.md` 형태로 slug를 사용하므로, 날짜 prefix만 추가하는 변경이다. output-format.md도 함께 수정해야 한다. |
| R3 | Risk | `_sdd/spec/main.md` guardrails의 prev/ 규칙 제거는 global spec mutation이다. 이 변경은 `spec-update-todo`가 아닌 직접 수정이 필요하다 (prev/ 제거를 위해 prev/ 백업을 하는 것은 모순). |
| R4 | Open Question | sdd-autopilot의 sample-orchestrator에서 출력 파일 경로가 slug 기반으로 바뀌면, 오케스트레이터 생성 로직 자체도 slug를 생성하는 방식이 필요한지 확인이 필요하다. 현재는 예시 파일만 수정한다. |
| R5 | Risk | spec-snapshot에서 `prev/` 제외 규칙을 제거하면, 기존에 남아있는 물리적 `_sdd/spec/prev/` 디렉토리가 snapshot에 포함될 수 있다. 기존 prev/ 디렉토리의 물리적 삭제 시점은 별도 결정이 필요하다. |
<!-- spec-update-todo-input-end -->

# Part 2: Implementation Plan

## Overview

prev/ 백업 로직을 전체 스킬에서 제거하고, 6개 쓰기 스킬의 산출물 파일명을 slug 기반 패턴으로 전환한다. 4개 디렉토리(`.claude/skills/`, `.claude/agents/`, `.codex/skills/`, `.codex/agents/`)에 동시 적용하며, downstream 스킬의 입력 경로도 함께 업데이트한다.

## Scope

- 변경 대상 스킬: 17개
- 변경 대상 파일: 약 55개
- 변경 유형: prev/ 제거, slug 파일명 전환, 읽기 경로 업데이트, 제외 규칙 제거

## Components

| Component | Role in This Change |
|-----------|-------------------|
| Global spec (main.md) | Guardrails에서 prev/ 규칙 제거 |
| Spec 스킬 (6개) | Hard Rules/AC/Process에서 prev/ 제거 |
| 쓰기 스킬 (6개) | prev/ 제거 + slug 파일명 전환 |
| 읽기 스킬 (5개) | 입력 탐색 glob 패턴 업데이트 |
| spec-snapshot (2개) | prev/ 제외 규칙 제거 |
| guide-create output-format (2개) | 파일명/백업 규칙 업데이트 |

## Contract/Invariant Delta Coverage

| Delta ID | Phase | Tasks |
|----------|-------|-------|
| C1, I1 | Phase 1 + Phase 2 + Phase 3 | T1, T2, T3, T4, T5, T6, T7, T8 |
| C2 | Phase 3 | T5 |
| C3 | Phase 3 | T6 |
| C4, C5 | Phase 3 | T7 |
| C6 | Phase 3 | T8 |
| C7 | Phase 3 | T9 |
| C8 | Phase 4 | T10, T11, T12, T13, T14 |
| I2 | Phase 3 | T5, T6, T7, T8, T9 |
| I3 | Phase 5 | T15 |
| I4 | All Phases | 모든 task에서 4개 디렉토리 동시 적용 |

## Implementation Phases

### Phase 1: Global Spec Guardrail Update

| Task | Description | Dependencies |
|------|-------------|-------------|
| T1 | main.md guardrails에서 prev/ 백업 규칙 제거 | None |

### Phase 2: prev/ Removal - Spec Skills

| Task | Description | Dependencies |
|------|-------------|-------------|
| T2 | spec-create prev/ 제거 | T1 |
| T3 | spec-update-todo + spec-update-done prev/ 제거 | T1 |
| T4 | spec-rewrite + spec-upgrade + spec-summary prev/ 제거 | T1 |

### Phase 3: prev/ Removal + Slug Naming - Writing Skills

| Task | Description | Dependencies |
|------|-------------|-------------|
| T5 | feature-draft slug 파일명 전환 | T1 |
| T6 | implementation-plan slug 파일명 전환 | T1 |
| T7 | implementation-review prev/ 제거 + slug 전환 | T1 |
| T8 | implementation report prev/ 제거 + slug 전환 | T1 |
| T9 | pr-review prev/ 제거 + slug 전환 | T1 |
| T10 | guide-create prev/ 제거 + slug 전환 | T1 |

### Phase 4: Reader Path Updates

| Task | Description | Dependencies |
|------|-------------|-------------|
| T11 | implementation 스킬 읽기 경로 업데이트 | T5, T6 |
| T12 | implementation-review 스킬 읽기 경로 업데이트 | T6 |
| T13 | spec-update-done 읽기 경로 업데이트 | T5, T6, T7, T8 |
| T14 | spec-summary 읽기 경로 업데이트 | T7 |
| T15 | sdd-autopilot 예시 경로 업데이트 | T5 |

### Phase 5: spec-snapshot Cleanup

| Task | Description | Dependencies |
|------|-------------|-------------|
| T16 | spec-snapshot prev/ 제외 규칙 제거 | T1 |

## Task Details

---

### T1: Global Spec Guardrail Update

**Description**: `_sdd/spec/main.md`의 Guardrails 섹션에서 prev/ 백업 규칙을 제거한다. `spec mutation은 target file을 식별한 뒤에만 수행하며, 변경 전 원본을 prev/prev_<filename>_<timestamp>.md로 백업한다` 문장에서 백업 부분을 제거한다.

**Acceptance Criteria**:
- [ ] main.md Guardrails에서 prev/ 백업 언급이 제거됨
- [ ] spec mutation 자체의 target file 식별 요건은 유지됨

**Technical Notes**: C1, I1 적용. 이 변경은 global spec mutation이므로 spec-update-todo 없이 직접 수정 (R3 참조).

**Target Files**:
- [M] `_sdd/spec/main.md`

---

### T2: spec-create prev/ Removal

**Description**: spec-create의 Hard Rules와 Error Handling에서 prev/ 백업 관련 내용을 제거한다.

**Acceptance Criteria**:
- [ ] Hard Rules에서 `prev/prev_<filename>_<timestamp>.md` 백업 규칙 제거
- [ ] Error Handling에서 `기존 스펙 존재 | 백업 후 갱신` 항목의 백업 부분 수정
- [ ] 양 플랫폼 동일 적용

**Technical Notes**: C1 적용.

**Target Files**:
- [M] `.claude/skills/spec-create/SKILL.md`
- [M] `.codex/skills/spec-create/SKILL.md`

---

### T3: spec-update-todo + spec-update-done prev/ Removal

**Description**: spec-update-todo와 spec-update-done의 Hard Rules, AC, Error Handling에서 prev/ 관련 내용을 제거한다.

**Acceptance Criteria**:
- [ ] spec-update-todo: Hard Rule 1 (`spec 수정 전 prev/ 백업을 만든다`) 제거
- [ ] spec-update-done: Hard Rule 2 (`스펙 파일 수정 전 prev/ 백업을 만든다`) 제거
- [ ] spec-update-done: Error Handling `백업 경로 없음 | prev/를 생성하고 진행한다` 항목 제거
- [ ] 양 플랫폼 동일 적용 (SKILL.md + agent mirrors)

**Technical Notes**: C1 적용. spec-update-done의 AC에서 `prev/` 아카이브 관련 항목이 있으면 함께 제거.

**Target Files**:
- [M] `.claude/skills/spec-update-todo/SKILL.md`
- [M] `.claude/agents/spec-update-todo.md`
- [M] `.codex/skills/spec-update-todo/SKILL.md`
- [M] `.codex/agents/spec-update-todo.toml`
- [M] `.claude/skills/spec-update-done/SKILL.md`
- [M] `.claude/agents/spec-update-done.md`
- [M] `.codex/skills/spec-update-done/SKILL.md`
- [M] `.codex/agents/spec-update-done.toml`

---

### T4: spec-rewrite + spec-upgrade + spec-summary prev/ Removal

**Description**: spec-rewrite, spec-upgrade, spec-summary의 Hard Rules, AC, Process에서 prev/ 관련 내용을 제거한다.

**Acceptance Criteria**:
- [ ] spec-rewrite: Hard Rule 1 (`prev/prev_<filename>_<timestamp>.md`로 백업), AC 중 백업 관련, Step 3 (Safety Backups) 수정
- [ ] spec-upgrade: Hard Rule 4 (`prev/prev_<filename>_<timestamp>.md`로 백업), AC 중 백업 관련, Step 4 (Backup and Migrate)에서 백업 부분 수정
- [ ] spec-summary: Hard Rule 3 (`prev/prev_summary_<timestamp>.md`로 백업) 제거
- [ ] 양 플랫폼 동일 적용

**Technical Notes**: C1 적용.

**Target Files**:
- [M] `.claude/skills/spec-rewrite/SKILL.md`
- [M] `.codex/skills/spec-rewrite/SKILL.md`
- [M] `.claude/skills/spec-upgrade/SKILL.md`
- [M] `.codex/skills/spec-upgrade/SKILL.md`
- [M] `.claude/skills/spec-summary/SKILL.md`
- [M] `.codex/skills/spec-summary/SKILL.md`

---

### T5: feature-draft Slug Naming Transition

**Description**: feature-draft의 산출물 경로를 `feature_draft_<feature_name>.md`에서 `<YYYY-MM-DD>_feature_draft_<slug>.md`로 전환한다.

**Acceptance Criteria**:
- [ ] 산출물 경로가 `_sdd/drafts/<YYYY-MM-DD>_feature_draft_<slug>.md`로 변경됨
- [ ] AC, Hard Rules, Required Output의 파일명 참조 모두 업데이트
- [ ] slug 규칙 설명 추가 (영문 소문자, 숫자, `_`만 사용)
- [ ] 양 플랫폼 동일 적용

**Technical Notes**: C2, I2 적용. 기존 `<feature_name>` 변수를 `<slug>`로 통일하고 날짜 prefix 추가.

**Target Files**:
- [M] `.claude/skills/feature-draft/SKILL.md`
- [M] `.codex/skills/feature-draft/SKILL.md`

---

### T6: implementation-plan Slug Naming Transition

**Description**: implementation-plan의 산출물 경로를 `implementation_plan.md`에서 `<YYYY-MM-DD>_implementation_plan_<slug>.md`로 전환한다.

**Acceptance Criteria**:
- [ ] 산출물 경로가 `_sdd/implementation/<YYYY-MM-DD>_implementation_plan_<slug>.md`로 변경됨
- [ ] AC, 본문 설명, Input Sources의 파일명 참조 모두 업데이트
- [ ] slug 규칙 설명 추가
- [ ] 양 플랫폼 동일 적용 (SKILL.md + agent mirrors)

**Technical Notes**: C3, I2 적용.

**Target Files**:
- [M] `.claude/skills/implementation-plan/SKILL.md`
- [M] `.claude/agents/implementation-plan.md`
- [M] `.codex/skills/implementation-plan/SKILL.md`
- [M] `.codex/agents/implementation-plan.toml`

---

### T7: implementation-review prev/ Removal + Slug Transition

**Description**: implementation-review에서 prev/ 백업 로직을 제거하고, 산출물 경로를 slug 기반으로 전환한다.

**Acceptance Criteria**:
- [ ] AC3에서 `(기존 파일은 prev/로 아카이브)` 제거
- [ ] Review Output 섹션에서 prev/ 아카이브 설명 제거
- [ ] Step 7에서 `기존 리뷰 파일이 있으면 prev/로 아카이브한다` 제거
- [ ] 산출물 경로가 `_sdd/implementation/<YYYY-MM-DD>_implementation_review_<slug>.md`로 변경
- [ ] 양 플랫폼 동일 적용 (SKILL.md + agent mirrors)

**Technical Notes**: C1, C4, I2 적용.

**Target Files**:
- [M] `.claude/skills/implementation-review/SKILL.md`
- [M] `.claude/agents/implementation-review.md`
- [M] `.codex/skills/implementation-review/SKILL.md`
- [M] `.codex/agents/implementation-review.toml`

---

### T8: implementation Report prev/ Removal + Slug Transition

**Description**: implementation 스킬의 report 생성 부분에서 prev/ 아카이브를 제거하고, 산출물 경로를 slug 기반으로 전환한다.

**Acceptance Criteria**:
- [ ] AC4에서 `implementation_report.md` 경로를 slug 기반으로 변경
- [ ] `implementation_report.md 생성` 섹션에서 prev/ 아카이브 설명 제거
- [ ] 산출물 경로가 `_sdd/implementation/<YYYY-MM-DD>_implementation_report_<slug>.md`로 변경
- [ ] 양 플랫폼 동일 적용 (SKILL.md + agent mirrors)

**Technical Notes**: C1, C5, I2 적용.

**Target Files**:
- [M] `.claude/skills/implementation/SKILL.md`
- [M] `.claude/agents/implementation.md`
- [M] `.codex/skills/implementation/SKILL.md`
- [M] `.codex/agents/implementation.toml`

---

### T9: pr-review prev/ Removal + Slug Transition

**Description**: pr-review에서 prev/ 백업 로직을 제거하고, 산출물 경로를 slug 기반으로 전환한다.

**Acceptance Criteria**:
- [ ] AC5에서 `기존 리뷰 파일이 있으면 _sdd/pr/prev/로 아카이브되었다` 제거
- [ ] Step 1에서 prev/ 아카이브 로직 제거
- [ ] Edge Cases에서 `Existing review file | _sdd/pr/prev/로 아카이브 후 생성` 수정
- [ ] 산출물 경로가 `_sdd/pr/<YYYY-MM-DD>_pr_review_<slug>.md`로 변경
- [ ] sample-review.md에서 prev/ 아카이브 언급 제거
- [ ] 양 플랫폼 동일 적용

**Technical Notes**: C1, C6, I2 적용.

**Target Files**:
- [M] `.claude/skills/pr-review/SKILL.md`
- [M] `.codex/skills/pr-review/SKILL.md`
- [M] `.claude/skills/pr-review/examples/sample-review.md`

---

### T10: guide-create prev/ Removal + Slug Transition

**Description**: guide-create에서 prev/ 백업 로직을 제거하고, 파일명에 날짜 prefix를 추가한다.

**Acceptance Criteria**:
- [ ] AC4에서 `기존 가이드 파일이 있었다면 _sdd/guides/prev/에 백업이 생성되었다` 제거
- [ ] Hard Rule 2 (`Allowed outputs`에서 prev/ 경로 제거)와 Hard Rule 6 (`Backup before overwrite`) 제거
- [ ] Step 6 (`Save with Backup Semantics`)에서 백업 로직 제거
- [ ] Error Handling에서 `기존 가이드 파일 존재 | _sdd/guides/prev/에 백업 후 덮어쓰기` 수정
- [ ] 산출물 경로가 `_sdd/guides/<YYYY-MM-DD>_guide_<slug>.md`로 변경
- [ ] output-format.md의 파일 규칙과 백업 규칙 섹션 업데이트
- [ ] 양 플랫폼 동일 적용

**Technical Notes**: C1, C7, I2 적용.

**Target Files**:
- [M] `.claude/skills/guide-create/SKILL.md`
- [M] `.claude/skills/guide-create/references/output-format.md`
- [M] `.codex/skills/guide-create/SKILL.md`
- [M] `.codex/skills/guide-create/references/output-format.md`

---

### T11: implementation Skill Reader Path Update

**Description**: implementation 스킬의 Plan 파일 탐색 순서와 feature_draft 입력 경로를 slug glob 패턴으로 업데이트한다.

**Acceptance Criteria**:
- [ ] Plan 파일 탐색에 `_sdd/implementation/*_implementation_plan_*.md` glob 추가
- [ ] feature_draft 입력에 `_sdd/drafts/*_feature_draft_*.md` glob 추가
- [ ] 기존 고정 경로는 legacy fallback으로 유지
- [ ] 양 플랫폼 동일 적용

**Technical Notes**: C8 적용.

**Target Files**:
- [M] `.claude/skills/implementation/SKILL.md`
- [M] `.claude/agents/implementation.md`
- [M] `.codex/skills/implementation/SKILL.md`
- [M] `.codex/agents/implementation.toml`

---

### T12: implementation-review Reader Path Update

**Description**: implementation-review의 Plan 파일 탐색 순서를 slug glob 패턴으로 업데이트한다.

**Acceptance Criteria**:
- [ ] Plan 파일 탐색에 `_sdd/implementation/*_implementation_plan_*.md` glob 추가
- [ ] 기존 고정 경로는 legacy fallback으로 유지
- [ ] 양 플랫폼 동일 적용

**Technical Notes**: C8 적용.

**Target Files**:
- [M] `.claude/skills/implementation-review/SKILL.md`
- [M] `.claude/agents/implementation-review.md`
- [M] `.codex/skills/implementation-review/SKILL.md`
- [M] `.codex/agents/implementation-review.toml`

---

### T13: spec-update-done Reader Path Update

**Description**: spec-update-done의 Input Sources에서 feature_draft, implementation_plan, implementation_review, implementation_report 경로를 slug glob 패턴으로 업데이트한다.

**Acceptance Criteria**:
- [ ] `_sdd/drafts/feature_draft_<name>.md` -> `_sdd/drafts/*_feature_draft_*.md` (또는 양쪽 모두 나열)
- [ ] `_sdd/implementation/implementation_plan.md` -> `_sdd/implementation/*_implementation_plan_*.md`
- [ ] `_sdd/implementation/implementation_review.md` -> `_sdd/implementation/*_implementation_review_*.md`
- [ ] `_sdd/implementation/implementation_report*.md` -> `_sdd/implementation/*_implementation_report_*.md`
- [ ] 양 플랫폼 동일 적용

**Technical Notes**: C8 적용.

**Target Files**:
- [M] `.claude/skills/spec-update-done/SKILL.md`
- [M] `.claude/agents/spec-update-done.md`
- [M] `.codex/skills/spec-update-done/SKILL.md`
- [M] `.codex/agents/spec-update-done.toml`

---

### T14: spec-summary Reader Path Update

**Description**: spec-summary의 Input Sources에서 implementation_review 경로를 slug glob 패턴으로 업데이트한다.

**Acceptance Criteria**:
- [ ] `_sdd/implementation/implementation_review.md` -> `_sdd/implementation/*_implementation_review_*.md`
- [ ] 양 플랫폼 동일 적용

**Technical Notes**: C8 적용.

**Target Files**:
- [M] `.claude/skills/spec-summary/SKILL.md`
- [M] `.codex/skills/spec-summary/SKILL.md`

---

### T15: sdd-autopilot Sample Orchestrator Path Update

**Description**: sdd-autopilot의 sample-orchestrator.md에서 산출물 경로 예시를 slug 기반으로 업데이트한다.

**Acceptance Criteria**:
- [ ] `feature_draft_jwt_auth.md` -> `<YYYY-MM-DD>_feature_draft_jwt_auth.md` (예시이므로 날짜는 고정값 사용)
- [ ] 양 플랫폼 동일 적용

**Technical Notes**: C2 적용 (예시 파일).

**Target Files**:
- [M] `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md`
- [M] `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md`

---

### T16: spec-snapshot prev/ Exclusion Rule Removal

**Description**: spec-snapshot에서 `prev/` 디렉토리 제외 규칙을 제거한다.

**Acceptance Criteria**:
- [ ] AC에서 `(prev/ 제외)` 언급 제거
- [ ] Hard Rules에서 `prev/` 백업 디렉토리 제외 규칙 제거
- [ ] Process Step 1에서 `prev/ 제외` 조건 제거
- [ ] 양 플랫폼 동일 적용

**Technical Notes**: I3 적용.

**Target Files**:
- [M] `.claude/skills/spec-snapshot/SKILL.md`
- [M] `.codex/skills/spec-snapshot/SKILL.md`

---

## Parallel Execution Summary

```
Phase 1: T1 (global spec)
  |
  v
Phase 2: T2 || T3 || T4 (spec 스킬 prev/ 제거 -- 병렬 가능)
  |
  v
Phase 3: T5 || T6 || T7 || T8 || T9 || T10 (쓰기 스킬 slug 전환 -- 병렬 가능)
  |
  v
Phase 4: T11 || T12 || T13 || T14 || T15 (읽기 경로 업데이트 -- 병렬 가능, Phase 3 완료 후)
  |
  v
Phase 5: T16 (spec-snapshot -- Phase 1 이후 언제든 가능, 독립적)
```

Phase 2와 Phase 3의 병렬 가능 task들은 파일 충돌이 없으므로 동시 실행 가능하다. Phase 4는 Phase 3의 산출물 경로가 확정된 후 실행해야 한다. Phase 5(T16)는 Phase 1 이후 독립적으로 실행 가능하다.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| 미러 불일치 | `.claude/`와 `.codex/`에서 내용이 달라질 수 있음 | 각 phase 완료 후 양쪽 디렉토리 diff 비교 검증 |
| 파일 수 과다 (55개+) | 작업 중 누락 가능성 | task별 Target Files를 strict하게 관리하고, 완료 후 grep 기반 잔여 검증 (V5) |
| 기존 prev/ 디렉토리 물리적 잔존 | spec-snapshot이 기존 prev/ 디렉토리를 포함하게 됨 | R5에 기록. 물리적 삭제는 별도 작업으로 분리 |
| 오케스트레이터 slug 생성 | autopilot이 동적으로 slug를 생성해야 할 수 있음 | R4에 기록. 현재는 예시 파일만 수정하고, 오케스트레이션 로직 변경은 후속 확인 |

## Open Questions

| # | Question | Impact |
|---|----------|--------|
| OQ1 | 기존 `_sdd/spec/prev/` 디렉토리의 물리적 삭제 시점은? (이 작업 범위 밖이지만 spec-snapshot에 영향) | Low - 별도 정리 작업으로 처리 가능 |
| OQ2 | sdd-autopilot 오케스트레이터 생성 로직에서 slug를 어떻게 결정하는지? 현재 예시만 수정하면 충분한지? | Medium - autopilot SKILL.md 본문 검토 필요 |
