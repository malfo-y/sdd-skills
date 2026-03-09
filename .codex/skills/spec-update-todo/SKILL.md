---
name: spec-update-todo
description: This skill should be used when the user asks to "update spec with features", "add features to spec", "update spec from input", "add requirements to spec", "spec update", "expand spec", "add to-do to spec", "add to-implement to spec", or mentions adding new features, requirements, or planned improvements to an existing specification document.
version: 1.3.0
---

# Spec Update from Planned Input

Apply planned requirements into an existing exploration-first spec.

This skill updates `_sdd/spec/` with planned or to-implement items.
It does not implement code. It turns draft requirements into spec entries that help future readers understand:
- what is planned
- how important components are expected to behave and why
- where the change affects the system
- which components or paths are involved
- what risks or unknowns remain

## Overview

Input can come from:
1. user conversation
2. `_sdd/spec/user_spec.md` or `_sdd/spec/user_draft.md`
3. Part 1 of a `feature-draft` output
4. `_sdd/spec/DECISION_LOG.md` as supporting rationale

After processing input files, rename them with `_processed_`.

## When to Use This Skill

- Adding planned features to an existing spec
- Reflecting feature-draft output into `_sdd/spec/`
- Expanding roadmap or to-implement sections in a structured spec
- Updating component, flow, environment, or change-path documentation before implementation

## Hard Rules

1. **Always backup**: 수정 전 반드시 `_sdd/spec/prev/PREV_<filename>_<timestamp>.md`로 백업한다.
2. **Rename processed input files**: 처리한 입력 파일은 `_processed_` 접두사로 이름 변경한다.
3. **한국어 작성**: 추가 내용은 메인 스펙 언어를 따르되 기본은 한국어다.
4. **DECISION_LOG.md 최소화**: 결정 로그는 `DECISION_LOG.md`에만 기록한다.
5. **앵커 섹션 보존**: 가능하면 `Goal`, `Architecture Overview`, `Component Details`, `Environment & Dependencies`, `Identified Issues & Improvements`, `Usage Examples`, `Open Questions` 구조를 유지한다.
6. **탐색성 유지**: planned update는 단순 목록 추가가 아니라 탐색성과 변경 시작점을 강화해야 한다.
7. **실제 경로 우선**: 컴포넌트와 관련 경로가 확인되면 문서에 포함한다.
8. **추정은 분리**: 신뢰도 낮은 내용은 `Open Questions`로 보낸다.
9. **책임 기반 분할 우선**: 분할이 필요하면 `main.md + <component>.md` 형태를 기본으로 한다.
10. **메타데이터 강제 금지**: version/date/changelog는 기존 문서가 이미 그 메타데이터를 사용할 때만 갱신한다.
11. **스펙 갱신 기준 우선**: 편집 전에 각 입력 항목을 `MUST update`, `NO update`, `CONSIDER`로 분류한다.
12. **선택 섹션 최소화**: `Environment & Dependencies`, `Identified Issues & Improvements`, `Usage Examples` 등 선택 섹션은 실제 영향이 있을 때만 추가하거나 수정한다.
13. **빈 선택 섹션 금지**: 비어 있는 선택 섹션, 메타데이터 블록, placeholder 표는 만들지 않는다.
14. **Token-efficient update**: 반복 설명보다 기존 표, 경로 인덱스, 짧은 불릿 갱신을 우선한다.

## Input Sources

### 1. User Conversation
- feature descriptions
- requirement discussions
- improvement requests
- bug reports to record as planned work

### 2. Input Files
- `_sdd/spec/user_spec.md`
- `_sdd/spec/user_draft.md`

### 3. Decision Log
- `_sdd/spec/DECISION_LOG.md` when previous decisions constrain the planned change

## Update Process

### Step 1: Identify Input Source

**Tools**: `Glob`, `Read`

Load all applicable sources in this order:
1. conversation
2. `user_draft.md`
3. `user_spec.md`

If multiple sources exist, merge them and preserve conflicts or ambiguity in `Open Questions`.

### Step 2: Load Current Spec

**Tools**: `Read`, `Glob`, `rg`

Treat the spec as a navigation surface.

Read:
- the main spec (`_sdd/spec/<project>.md` or `_sdd/spec/main.md`)
- linked component spec files that will be affected
- `_sdd/spec/DECISION_LOG.md` if present

Prioritize these target areas:
- `Goal > Project Snapshot / Key Features / Non-Goals`
- `Architecture Overview > System Boundary / Repository Map / Runtime Map`
- `Component Details > Component Index / Overview`
- `Environment & Dependencies`
- `Identified Issues & Improvements`
- `Usage Examples > Common Operations / Common Change Paths`
- `Open Questions`

If the spec lacks these anchors and the change is still local, add missing subsections minimally.
If the spec shape is fundamentally poor, continue with minimal safe updates and note a `spec-rewrite` follow-up in `Open Questions`.

### Step 3: Parse Input

**Tools**: `Read`

Accepted input structure is defined in `references/input-format.md`.

Supported sections:
- `New Features`
- `Improvements`
- `Bug Reports`
- `Component Changes`
- `Environment & Dependency Changes`
- `Notes`
- `Open Questions`

Extract:
- feature name and priority
- spec update classification if provided
- target section hints
- affected components / paths
- acceptance criteria
- risks / invariants
- dependencies and constraints

### Step 4: Classify Whether Spec Edits Are Needed

**Tools**: none

Classification rules:
- `MUST update`
  - user-visible feature or scope change
  - new or changed runtime flow, ownership, contract, or repository path that affects navigation
  - new environment/setup requirement that affects running or testing
  - new enduring risk, invariant, or unresolved question worth preserving
- `NO update`
  - tests-only, comments-only, formatting-only changes
  - internal refactors that do not change behavior, navigation, contracts, or maintenance entry points
- `CONSIDER`
  - minor dependency bumps
  - internal reorganizations with unclear navigation impact
  - performance tuning with limited user-visible impact

If the input already includes `Spec Update Classification`, verify it against the above rules.
If the correct classification is `NO update`, prepare a no-op summary and skip spec edits.

### Step 5: Categorize and Map Updates

**Tools**: none

Apply the mapping rules from `references/section-mapping.md`.

Default mapping:

| Input Type | Preferred Target Section |
|------------|--------------------------|
| New Feature | `Goal > Key Features` |
| Boundary or flow change | `Architecture Overview` |
| Component behavior/design intent change | `Component Details > Overview` |
| Component change | `Component Details` |
| Environment/dependency/config change | `Environment & Dependencies` |
| Planned operational/debug path | `Usage Examples` |
| Risk or debt | `Identified Issues & Improvements` |
| Uncertainty | `Open Questions` |

Important rule:
one input item may require updates in multiple spec areas.

Example:
- a new feature may require `Goal > Key Features`
- plus `Architecture Overview > Runtime Map`
- plus `Component Details`
- plus `Usage Examples > Common Change Paths`

### Step 6: Generate Update Plan

**Tools**: deterministic defaults (non-interactive)

Before editing, present a concise update plan:

~~~markdown
## Spec Update Plan

**Target Files**:
- `_sdd/spec/main.md`
- `_sdd/spec/notification.md`

**Spec Update Classification**: MUST update

### Planned Changes
- Goal > Key Features: ADD `실시간 알림`
- Architecture Overview > Runtime Map: UPDATE 알림 이벤트 흐름
- Component Details: ADD `NotificationService`
- Usage Examples > Common Change Paths: ADD 알림 관련 변경 시작점
- Open Questions: ADD 이메일 알림 범위 미정
~~~

If classification is `NO update`, present a compact no-op plan instead.

### Step 7: Apply Updates

**Tools**: `Edit`, `Write`, `Bash (mkdir -p)`

Apply planned changes directly to the relevant spec files.

Rules:
1. create a `prev/PREV_...` backup for every modified file
2. preserve existing accurate content
3. if classification is `NO update`, skip spec edits and report why
4. add planned markers such as `📋 계획됨` only where they improve clarity
5. update multiple sections when one feature affects multiple views of the system
6. add or refresh `Component Index`, component `Overview`, `Runtime Map`, or `Common Change Paths` when needed for planned changes
7. add or update optional sections only when they materially help future navigation
8. add/merge `Open Questions` for unresolved assumptions
9. update `DECISION_LOG.md` only if the planned direction introduces a meaningful decision
10. update version/date/changelog only if the current spec already uses them

If the updated content grows too large:
- prefer splitting by responsibility (`auth.md`, `jobs.md`, `billing.md`)
- keep the main spec as the entry point
- record the file map in `Open Questions` if the split is non-obvious

### Step 7.5: Planned Update Quality Gate

업데이트 적용 후, 이번 planned update가 실제로 탐색성과 변경 시작점을 강화했는지 acceptance criteria로 다시 판정한다.
이 단계는 **판정만** 수행한다. FAIL이 나오면 Step 7로 돌아가 필요한 부분만 보강한 뒤 이 단계를 최대 1회 재실행한다.

Scope rules:
- 평가 대상은 **이번에 추가/수정한 planned items**다. 기존 스펙의 레거시 결함은 직접 평가 대상이 아니다.
- 이번 변경 범위와 직접 무관해 판단 근거가 부족한 criterion은 `WEAK`로 기록하고 `FAIL`로 간주하지 않는다.
- 판단의 중심은 "새 planned item이 어디에 붙고, 나중에 어디서 수정/검증을 시작해야 하는지"다.

#### Acceptance Criteria

| Criterion | Probe | PASS | WEAK | FAIL |
|-----------|-------|------|------|------|
| 저장소 이해 | "이번 planned update가 저장소 목적/범위를 흐리지 않는가?" | Goal이나 관련 설명이 이번 planned item과 충돌하지 않는다 | 기존 Goal과의 연결이 다소 약하다 | 이번 planned item이 저장소 목적/범위를 혼란스럽게 만든다 |
| 기능 위치 탐색 | "이번에 추가한 planned item X는 어디에 붙는가?" | 새 planned item이 `Component Details`/`Component Index`/`Overview`/관련 경로에 명확히 연결된다 | 컴포넌트 수준 설명은 있으나 경로/심볼 연결이 약하다 | planned item의 소유 컴포넌트나 경로를 알 수 없다 |
| 안전한 수정 판단 | "이 planned item을 구현하려면 어디서 시작해야 하는가?" | `Change Recipes` 또는 `Common Change Paths` 수준의 변경 시작점과 확인 포인트가 있다 | 시작점은 있으나 검증 포인트나 영향 범위가 약하다 | 구현 시작점과 변경 가이드가 없다 |
| 결정/불변 조건 기억 | "이번 planned item으로 새로 생긴 결정/가정은 무엇인가?" | 새 결정, 제약, 미해결 사항이 `Open Questions` 또는 `DECISION_LOG.md` 등에 기록된다 | 기록은 있으나 불명확하다 | 새 결정/가정이 전혀 남지 않는다 |

#### Self-Check Procedure

1. 이번에 추가/수정한 planned items와 직접 영향받은 섹션만 다시 읽는다.
2. 위 네 개 probe를 planned item 하나 이상에 대입해 본다.
3. 각 criterion을 `PASS` / `WEAK` / `FAIL`로 판정한다.
4. 결과에 따라 행동한다:
   - `ALL PASS`: 완료
   - `WEAK`만 존재: 개선 포인트를 완료 보고에 포함하고 진행
   - `FAIL` 존재: Step 7로 돌아가 해당 부분만 보강 후 재판정
   - 재판정 후에도 `FAIL`: 사용자에게 보고하고 판단을 맡긴다

#### Completion Output

완료 보고에 아래 표를 포함한다:

| Criterion | Probe | 판정 | 근거 |
|-----------|-------|------|------|
| 저장소 이해 | "이번 planned update가 목적을 흐리지 않는가?" | PASS | (구체적 근거) |
| 기능 위치 탐색 | "planned item X는 어디에?" | PASS | (구체적 근거) |
| 안전한 수정 판단 | "구현 시작점은 어디인가?" | PASS | (구체적 근거) |
| 결정/불변 조건 기억 | "새 결정/가정은 무엇인가?" | PASS | (구체적 근거) |

**종합**: `PASS` / `PASS WITH NOTES` / `FAIL -> FIX`

### Step 8: Process Input Files

**Tools**: `Bash (mv)`

Rename processed files:
- `_sdd/spec/user_draft.md` -> `_sdd/spec/_processed_user_draft.md`
- `_sdd/spec/user_spec.md` -> `_sdd/spec/_processed_user_spec.md`

Add processing metadata:

~~~markdown
<!-- Processed: YYYY-MM-DD -->
<!-- Applied by: spec-update-todo -->
<!-- Target Spec: main.md -->
~~~

## Output Summary

After updating, summarize:
- spec update classification
- updated files
- changed sections
- planned items added
- quality gate result
- whether `DECISION_LOG.md` changed
- processed input file status
- remaining `Open Questions`

## Context Management

| 스펙 크기 | 전략 |
|-----------|------|
| < 200줄 | 전체 읽기 |
| 200-500줄 | 전체 읽기 가능 |
| 500-1000줄 | TOC 먼저, 관련 섹션만 읽기 |
| > 1000줄 | 인덱스와 타겟 섹션 우선 |

## Error Handling

| Situation | Action |
|-----------|--------|
| Spec file not found | `spec-create` 먼저 실행 권장 |
| Ambiguous input | deterministic defaults + `Open Questions` 기록 |
| Conflicting requirements | 더 보수적인 해석 적용 후 `Open Questions` 기록 |
| Backup dir missing | `mkdir -p _sdd/spec/prev/` |
| Spec structure poor | 최소 안전 업데이트 후 `spec-rewrite` follow-up 기록 |
| Split needed | 책임 기반 분할로 전환 |

## Additional Resources

### Reference Files
- `references/input-format.md` - accepted input shape
- `references/section-mapping.md` - how planned items map into the spec

### Example Files
- `examples/user_spec.md` - example input file
- `examples/update-summary.md` - example completion summary

## Integration with Other Skills

- `feature-draft` produces Part 1 that this skill can consume
- `implementation` executes planned work after this step
- `spec-update-done` syncs actual implementation back after completion
