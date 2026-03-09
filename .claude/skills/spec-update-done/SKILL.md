---
name: spec-update-done
description: This skill should be used when the user asks to "update spec from code", "sync spec with implementation", "apply implementation changes to spec", "reflect completed work in spec", "refresh spec after implementation", "implementation done sync", or mentions spec document maintenance tied to completed code changes.
version: 1.1.0
---

# Spec Sync and Update

Sync exploration-first spec documents with actual implementation.

A good spec is not a copy of the code. It is a searchable map that helps people and LLMs:
- understand what the repository does
- find where a feature or responsibility lives
- decide where to edit safely
- remember non-obvious decisions and invariants

This skill compares planned documentation against code, implementation logs, and user feedback, then updates the spec so it remains:
- accurate
- easy to understand
- easy to navigate for future changes
- explicit about risks, invariants, and unresolved items

## Simplified Workflow

This skill is **Step 4 of 4** in the SDD workflow:

```
spec-create -> feature-draft -> implementation -> spec-update-done (this)
```

| Step | Skill | Purpose |
|------|-------|---------|
| 1 | spec-create | Create the initial index-first spec |
| 2 | feature-draft | Draft planned spec changes |
| 3 | implementation | Execute the plan |
| **4** | **spec-update-done** | Sync actual implementation back to spec |

## Hard Rules

1. **Report before changing**: 변경 적용 전에 Change Report를 먼저 제시한다.
2. **Always backup**: 수정 전 `_sdd/spec/prev/PREV_<filename>_<timestamp>.md`로 백업한다.
3. **Copy-only archive**: 구현 산출물은 복사만 하고 원본을 이동/삭제하지 않는다.
4. **한국어 작성**: 추가/수정 내용은 메인 스펙 언어를 따르되 기본은 한국어다.
5. **DECISION_LOG.md 최소화**: 중요한 방향/가정 변경만 `DECISION_LOG.md`에 기록한다.
6. **앵커 섹션 보존**: `Goal`, `Architecture Overview`, `Component Details`, `Environment & Dependencies`, `Identified Issues & Improvements`, `Usage Examples`, `Open Questions` 섹션명을 유지한다.
7. **추정 명시**: 확인되지 않은 내용은 단정하지 않고 `Open Questions`에 기록한다.
8. **요약 우선**: 코드를 그대로 복사하지 말고 의도, 경계, 계약, 변경 지점, 불변 조건을 압축해서 정리한다.
9. **갱신 필요성 판단**: SDD §8 기준(`MUST update` / `NO update` / `CONSIDER`)에 따라 갱신 여부를 판단한다.
10. **실제 구현 우선**: 계획보다 코드와 검증 가능한 구현 상태를 우선한다.
11. **탐색성 유지**: 동기화 결과는 `Repository Map`, `Runtime Map`, `Component Index`, `Common Change Paths`를 더 정확하게 만들어야 한다.
12. **추정은 분리**: 구현만으로 확정할 수 없는 사항은 `Open Questions`에 남긴다.
13. **메타데이터 강제 금지**: version/date/changelog는 기존 문서가 이미 사용 중일 때만 갱신한다.
14. **선택 섹션 최소화**: `Environment & Dependencies`, `Identified Issues & Improvements`, `Usage Examples` 등 선택 섹션은 실제 드리프트가 있을 때만 추가하거나 수정한다.
15. **빈 선택 섹션 금지**: 비어 있는 선택 섹션, 메타데이터 블록, placeholder 표는 남기지 않는다.
16. **Token-efficient sync**: 구현 반영은 반복 서술보다 경로, 표, 짧은 불릿 위주로 갱신한다.

## Routing Guard

- If the user wants analysis only with no edits, route to `spec-review`.
- This skill performs actual spec synchronization.

## Overview

Sources of truth:
- current spec documents
- implementation logs in `_sdd/implementation/`
- feature draft artifacts in `_sdd/drafts/`
- code diffs and current repository state
- `_sdd/spec/DECISION_LOG.md`
- user conversation

## When to Use This Skill

- After implementation completes
- When code has drifted from the spec
- When planned items need to become implemented/actual descriptions
- Before starting a new feature and you need the base spec to be trustworthy again

## Input Sources

### 1. Implementation Logs
- `IMPLEMENTATION_PLAN.md`
- `IMPLEMENTATION_PROGRESS.md`
- `IMPLEMENTATION_REVIEW.md`
- `IMPLEMENTATION_REPORT*.md`
- `TEST_SUMMARY.md`
- `IMPLEMENTATION_INDEX.md`

### 2. Feature Drafts
- `_sdd/drafts/feature_draft_<name>.md`

### 3. Code Changes
- `git status`
- `git diff`
- recent commits

### 4. Current Spec Documents
- `_sdd/spec/main.md` or `_sdd/spec/<project>.md`
- component spec files
- `_sdd/spec/DECISION_LOG.md`

### 5. Environment Guide
- `_sdd/env.md` when local verification is needed

## Sync Process

### Step 1: Gather Context

**Tools**: `Read`, `Glob`, `Bash (git diff, git log, git status)`, `Grep`

Collect:
1. current spec files
2. planned implementation artifacts
3. actual code changes
4. test/review signals
5. relevant decision-log entries
6. user-provided corrections or constraints

If local checks are needed, read `_sdd/env.md` first.

### Step 2: Identify Spec Drift

**Tools**: `Grep`, `Glob`, `Read`, `Bash`

Look for drift in these areas:

#### Navigation Drift
- **Stale Repository Map**: 디렉토리/파일 경로가 실제와 불일치
- **Stale Runtime Map**: 런타임 흐름이 변경되었으나 미반영
- **Stale Component Index**: 컴포넌트 목록이 실제와 불일치
- **Stale Change Paths**: `Common Change Paths`가 현재 코드와 불일치

#### Behavior / Contract Drift
- planned features now implemented
- changed flow, boundary, or ownership
- changed component contracts
- new or resolved invariants

#### Environment Drift
- runtime or dependency changes
- changed setup/test commands
- changed env vars or config shape

#### Issue / Unknown Drift
- resolved issues still listed
- newly discovered issues not listed
- `Open Questions` now resolved or newly introduced

### Step 2.5: Select Sync Need and Strategy

**Tools**: deterministic defaults (non-interactive)

Classify the implementation impact before editing:

#### SDD §8 갱신 기준

- **`MUST update`**
  - actual user-visible behavior changed
  - runtime flow, ownership, contracts, paths, or change/debug entry points changed
  - environment/setup requirements changed
  - an `Open Questions` item was resolved or newly introduced by implementation
- **`NO update`**
  - tests-only, comments-only, formatting-only work
  - internal refactors with no behavior, navigation, contract, or maintenance-path impact
- **`CONSIDER`**
  - minor dependency bumps
  - low-visibility performance tuning
  - internal reorganizations whose navigation impact is limited

Then choose a strategy from `references/update-strategies.md`:

| Scenario | Update Need | Strategy |
|----------|-------------|----------|
| Internal refactor, no behavior change | `NO update` | Skip Update |
| Small config/path correction | `MUST update` | Targeted Sync |
| Planned feature now implemented | `MUST update` | Planned-to-Actual Sync |
| New component or ownership shift | `MUST update` | Component Map Refresh |
| Major architecture or navigation drift | `MUST update` | Full Navigation Refresh |
| Ongoing phased delivery | `CONSIDER` / `MUST update` | Staged Sync |

If classification is `NO update`, use `Skip Update`, provide the report, and stop before spec edits.

### Step 3: Generate Change Report

**Tools**: none

Present findings before edits.

~~~markdown
## Spec Sync Report

### Summary
- 변경 파일: N개
- 스펙 갱신 분류: MUST update
- 선택 전략: Planned-to-Actual Sync
- 주요 탐색 업데이트: N개
- 기능/계약 업데이트: N개
- 남는 Open Questions: N개

### Navigation Updates
- Repository Map 갱신 필요
- Component Index 갱신 필요

### Behavior / Contract Updates
- `실시간 알림` 기능 구현 완료
- NotificationService 계약 구체화 필요

### Risks / Invariants
- 알림 실패와 파이프라인 실패 상태 분리 유지

### Open Questions
- [item]
~~~

### Step 4: Apply Updates

**Tools**: `Edit`, `Write`, `Bash (mkdir -p)`

Update the spec to reflect actual implementation.

#### Update Strategy Selection Guide

Choose the appropriate strategy based on Step 2.5 classification:

1. **Skip Update** (변경 불필요)
   - 내부 리팩터링, 테스트만 추가, 포맷팅 변경
   - 스펙 편집 없이 리포트만 제공

2. **Targeted Sync** (단일 섹션)
   - 경로 하나, 환경변수 하나, 커맨드 하나 변경
   - 해당 섹션만 정확히 수정

3. **Planned-to-Actual Sync** (다중 섹션)
   - `📋 계획됨` 항목이 구현 완료
   - `Goal`, `Architecture Overview`, `Component Details`, `Usage Examples` 연쇄 갱신

4. **Component Map Refresh**
   - 새 컴포넌트 추가 또는 소유권 이동
   - `Component Index` 갱신 + 컴포넌트 스펙 생성/수정

5. **Full Navigation Refresh**
   - `Repository Map`, `Runtime Map`, `Component Index`가 전반적으로 stale
   - 메인 스펙 우선 갱신 후 컴포넌트 파일 순차 갱신

6. **Staged Sync**
   - 단계적 구현 진행 중
   - 완료된 항목만 actual로 전환, 나머지는 planned 유지

#### Apply changes by section:
- `Goal`: implemented user-visible capabilities and scope changes
- `Architecture Overview`: actual system boundary, runtime map, repository map, invariants
- `Component Details`: actual ownership, paths, symbols, contracts
- `Environment & Dependencies`: actual runtime/config/setup
- `Identified Issues & Improvements`: resolved issues removed/updated, new real issues added
- `Usage Examples`: run/test commands and common change/debug paths refreshed
- `Open Questions`: resolved items removed, unresolved items updated

#### Important rules:
1. replace planned-only wording with actual behavior when implemented
2. remove or downgrade stale `📋 계획됨` markers where reality is now known
3. update component/file maps when implementation created or moved files
4. update `Common Change Paths` when maintenance entry points changed
5. update `DECISION_LOG.md` only when rationale changed, not for every code diff
6. update version/date/changelog only if the spec already uses them
7. update optional sections only when the implementation changed them materially
8. remove empty optional sections or placeholder bullets instead of keeping stale shells

### Step 5: Validate Updates

**Tools**: `Grep`, `Glob`, `Read`, `Bash`

Verify:
- documented paths exist
- `Repository Map` and `Component Index` reflect real code locations
- `Runtime Map` still matches actual behavior
- `Common Change Paths` point to real maintenance entry points
- resolved `Open Questions` are removed or updated
- preserved content was not accidentally regressed
- optional sections that remain are still relevant
- the synced spec stays compact enough for one focused read

#### SDD Quality Checklist

| 항목 | 검증 내용 |
|------|----------|
| 앵커 섹션 완전성 | `Goal`, `Architecture Overview`, `Component Details` 등 필수 섹션 존재 |
| 경로 정확성 | `Repository Map`, `Component Index`의 경로가 실제 파일과 일치 |
| 런타임 흐름 일치 | `Runtime Map`이 실제 동작과 일치 |
| 계약 정확성 | 컴포넌트 인터페이스/계약이 실제 코드와 일치 |
| 변경 지점 유효성 | `Common Change Paths`가 현재 유효한 진입점을 가리킴 |
| Open Questions 현행성 | 해결된 항목 제거, 새 항목 추가 완료 |
| 불변 조건 현행성 | `Cross-Cutting Invariants`가 실제 코드 가정과 일치 |
| 빈 섹션 없음 | placeholder만 있는 선택 섹션이 남아있지 않음 |
| 중복 기술 없음 | 같은 정보가 여러 섹션에 반복되지 않음 |
| 토큰 효율성 | 산문보다 표/경로/불릿 위주로 압축되어 있음 |

### Step 6: Archive Implementation Artifacts by Feature

**Tools**: `Bash (cp, mkdir -p)`, `Write`, `Read`

After spec sync is complete:
1. create `_sdd/implementation/features/<feature_id>/` if needed
2. copy relevant implementation artifacts there
3. use timestamped destination filenames
4. update `_sdd/implementation/IMPLEMENTATION_INDEX.md`
5. keep root implementation files intact

## Output Format

### Change Report

Provide a concise report before edits.

### Sync Summary

After edits, summarize:
- spec update classification and selected strategy
- updated files
- navigation improvements
- behavior/contract changes reflected
- remaining `Open Questions`
- whether `DECISION_LOG.md` changed

### Optional Changelog

If the spec already uses a changelog, add a concise entry.
Do not introduce a changelog just because this skill ran.

## Context Management

| 스펙 크기 | 전략 |
|-----------|------|
| < 200줄 | 전체 읽기 |
| 200-500줄 | 전체 읽기 가능 |
| 500-1000줄 | TOC 먼저, 관련 섹션만 읽기 |
| > 1000줄 | 인덱스와 타겟 섹션 우선 |

## Best Practices

### Writing Quality

- **Fast first read**: 스펙의 처음 30줄이 "이 저장소가 뭔지"에 답해야 한다
- **Change-oriented detail**: 장황한 설명보다 "어디를 고쳐야 하는지"를 우선한다
- **Path-first references**: 구체적인 디렉토리, 파일, 커맨드, 심볼을 포함한다
- **Trace unknowns**: 불확실한 내용은 자신 있는 서술에 숨기지 말고 `Open Questions`에 분리한다

### LLM Token Efficiency

- 산문보다 테이블과 리스트를 선호한다
- 경로와 심볼은 `` ` ``로 감싸서 구분한다
- 같은 정보를 여러 섹션에 반복하지 않는다

### Anti-Pattern Reference

| 안티패턴 | 왜 문제인가 | 대안 |
|---------|------------|------|
| 코드를 그대로 복사한 문서 | 코드가 바뀌면 즉시 불일치 | 계약과 의도만 남기고 구현은 코드에 맡긴다 |
| 실제 경로/심볼이 없는 문서 | 검색 시작점이 없음 | Owned Paths, Key Symbols 명시 |
| 변경 포인트가 없는 문서 | "어디를 고치지?"에 답 불가 | Change Recipes 섹션 추가 |
| 불확실한 내용을 사실처럼 작성 | 잘못된 정보 신뢰 위험 | Open Questions로 분리 |

## Error Handling

| Situation | Action |
|-----------|--------|
| `_sdd/spec/` missing | `spec-create` 먼저 실행 권장 |
| implementation logs missing | git/code 중심으로 Quick Sync 진행 |
| `_sdd/env.md` incomplete | 로컬 실행 검증 생략, 문서 기반으로 진행 |
| `feature_id` ambiguous | 컨텍스트에서 자동 생성 |
| backup dir missing | `mkdir -p _sdd/spec/prev/` |
| conflicting signals | 더 보수적인 해석 적용 후 `Open Questions` 기록 |

## Additional Resources

### Reference Files
- `references/update-strategies.md` - sync strategy guide with 6-strategy selection matrix
- `references/drift-patterns.md` - common drift patterns for exploration-first specs

### Example Files
- `examples/review-report.md` - example sync report
- `examples/changelog-entry.md` - optional changelog examples

## Integration with Other Skills

- `feature-draft` creates the planned patch baseline
- `implementation` produces the implementation reality
- `spec-update-todo` records planned work before implementation
- `spec-review` is the review-only alternative
