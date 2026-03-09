---
name: spec-update-todo
description: This skill should be used when the user asks to "update spec with features", "add features to spec", "update spec from input", "add requirements to spec", "spec update", "expand spec", "add to-do to spec", "add to-implement to spec", or mentions adding new features, requirements, or planned improvements to an existing specification document.
version: 1.4.0
---

# Spec Update from Planned Input

Apply planned requirements into an existing exploration-first spec.

This skill updates `_sdd/spec/` with planned or to-implement items.
It does not implement code. It turns draft requirements into spec entries that help future readers understand:
- what is planned
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
11. **갱신 필요도 분류**: 입력 항목마다 `MUST update / CONSIDER / NO update` 관점으로 문서 영향도를 판단한다.

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
- `Architecture Overview > System Boundary / Repository Map / Runtime Map / Cross-Cutting Invariants`
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
- target section hints
- affected components / paths
- acceptance criteria
- risks / invariants
- dependencies and constraints

### Step 4: Categorize and Map Updates

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

### Step 5: Generate Update Plan

**Tools**: deterministic defaults (non-interactive)

Before editing, present a concise update plan:

~~~markdown
## Spec Update Plan

**Target Files**:
- `_sdd/spec/main.md`
- `_sdd/spec/notification.md`

### Planned Changes
- Goal > Key Features: ADD `실시간 알림`
- Architecture Overview > Runtime Map: UPDATE 알림 이벤트 흐름
- Component Details: ADD `NotificationService`
- Usage Examples > Common Change Paths: ADD 알림 관련 변경 시작점
- Open Questions: ADD 이메일 알림 범위 미정
~~~

### Step 6: Apply Updates

**Tools**: `Edit`, `Write`, `Bash (mkdir -p)`

Apply planned changes directly to the relevant spec files.

Rules:
1. create a `prev/PREV_...` backup for every modified file
2. preserve existing accurate content
3. add planned markers such as `📋 계획됨` only where they improve clarity
4. update multiple sections when one feature affects multiple views of the system
5. add or refresh `Component Index`, `Runtime Map`, or `Common Change Paths` when needed for planned changes
6. update `Component Details > Overview` when the plan changes how a component works or why the structure exists
7. make the updated `Runtime Map` explain user-facing or operator-facing flow, not only arrows
8. add/merge `Open Questions` for unresolved assumptions
9. update `DECISION_LOG.md` only if the planned direction introduces a meaningful decision
10. update version/date/changelog only if the current spec already uses them

If the updated content grows too large:
- prefer splitting by responsibility (`auth.md`, `jobs.md`, `billing.md`)
- keep the main spec as the entry point
- record the file map in `Open Questions` if the split is non-obvious

### Step 7: Process Input Files

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
- updated files
- changed sections
- planned items added
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
