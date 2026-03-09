---
name: spec-update-done
description: This skill should be used when the user asks to "update spec from code", "sync spec with implementation", "apply implementation changes to spec", "reflect completed work in spec", "refresh spec after implementation", "implementation done sync", or mentions spec document maintenance tied to completed code changes.
version: 1.2.0
---

# Spec Sync and Update

Sync exploration-first spec documents with actual implementation.

This skill compares planned documentation against code, implementation logs, and user feedback, then updates the spec so it remains:
- accurate
- easy to understand
- easy to navigate for future changes
- explicit about risks, invariants, and unresolved items

## Simplified Workflow

This skill is **Step 4 of 4** in the SDD workflow:

```
spec -> feature-draft -> implementation -> spec-update-done (this)
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
6. **앵커 섹션 보존**: 가능하면 `Goal`, `Architecture Overview`, `Component Details`, `Environment & Dependencies`, `Identified Issues & Improvements`, `Usage Examples`, `Open Questions` 구조를 유지한다.
7. **실제 구현 우선**: 계획보다 코드와 검증 가능한 구현 상태를 우선한다.
8. **탐색성 유지**: 동기화 결과는 `Repository Map`, `Runtime Map`, `Component Index`, `Common Change Paths`를 더 정확하게 만들어야 한다.
9. **추정은 분리**: 구현만으로 확정할 수 없는 사항은 `Open Questions`에 남긴다.
10. **메타데이터 강제 금지**: version/date/changelog는 기존 문서가 이미 사용 중일 때만 갱신한다.
11. **스펙 갱신 기준 우선**: 편집 전에 이번 구현이 `MUST update`, `NO update`, `CONSIDER` 중 어디에 속하는지 먼저 판정한다.
12. **선택 섹션 최소화**: `Environment & Dependencies`, `Identified Issues & Improvements`, `Usage Examples` 등 선택 섹션은 실제 드리프트가 있을 때만 추가하거나 수정한다.
13. **빈 선택 섹션 금지**: 비어 있는 선택 섹션, 메타데이터 블록, placeholder 표는 남기지 않는다.
14. **Token-efficient sync**: 구현 반영은 반복 서술보다 경로, 표, 짧은 불릿 위주로 갱신한다.

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

**Tools**: `Read`, `Glob`, `Bash (git diff, git log, git status)`, `rg`

Collect:
1. current spec files
2. planned implementation artifacts
3. actual code changes
4. test/review signals
5. relevant decision-log entries
6. user-provided corrections or constraints

If local checks are needed, read `_sdd/env.md` first.

### Step 2: Identify Spec Drift

**Tools**: `rg`, `Glob`, `Read`, `Bash`

Look for drift in these areas:

#### Navigation Drift
- stale `Repository Map`
- stale `Runtime Map`
- missing or outdated `Component Index`
- `Common Change Paths` no longer pointing at the right files or symbols

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

- `MUST update`
  - actual user-visible behavior changed
  - runtime flow, ownership, contracts, paths, or change/debug entry points changed
  - environment/setup requirements changed
  - an `Open Questions` item was resolved or newly introduced by implementation
- `NO update`
  - tests-only, comments-only, formatting-only work
  - internal refactors with no behavior, navigation, contract, or maintenance-path impact
- `CONSIDER`
  - minor dependency bumps
  - low-visibility performance tuning
  - internal reorganizations whose navigation impact is limited

Then choose a strategy from `references/update-strategies.md`.

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

Apply changes by section:
- `Goal`: implemented user-visible capabilities and scope changes
- `Architecture Overview`: actual system boundary, runtime map, repository map, invariants
- `Component Details`: actual ownership, paths, symbols, contracts
- `Environment & Dependencies`: actual runtime/config/setup
- `Identified Issues & Improvements`: resolved issues removed/updated, new real issues added
- `Usage Examples`: run/test commands and common change/debug paths refreshed
- `Open Questions`: resolved items removed, unresolved items updated

Important rules:
1. replace planned-only wording with actual behavior when implemented
2. remove or downgrade stale `📋 계획됨` markers where reality is now known
3. update component/file maps when implementation created or moved files
4. update `Common Change Paths` when maintenance entry points changed
5. update `DECISION_LOG.md` only when rationale changed, not for every code diff
6. update version/date/changelog only if the spec already uses them
7. update optional sections only when the implementation changed them materially
8. remove empty optional sections or placeholder bullets instead of keeping stale shells

### Step 5: Validate Updates

**Tools**: `rg`, `Glob`, `Read`, `Bash`

Verify:
- documented paths exist
- `Repository Map` and `Component Index` reflect real code locations
- `Runtime Map` still matches actual behavior
- `Common Change Paths` point to real maintenance entry points
- resolved `Open Questions` are removed or updated
- preserved content was not accidentally regressed
- optional sections that remain are still relevant
- the synced spec stays compact enough for one focused read

### Step 5.5: Sync Quality Gate

구조 검증(Step 5) 통과 후, 이번 동기화 결과가 실제로 신뢰 가능한 change map이 되었는지 acceptance criteria로 다시 판정한다.
이 단계는 **판정만** 수행한다. FAIL이 나오면 Step 4로 돌아가 필요한 부분만 보강한 뒤 이 단계를 최대 1회 재실행한다.

Scope rules:
- 평가 대상은 **이번에 변경/추가한 섹션**이다. 기존 레거시 결함은 직접 평가 대상이 아니다.
- 이번 변경 범위와 직접 무관해 판단 근거가 부족한 criterion은 `WEAK`로 기록하고 `FAIL`로 간주하지 않는다.

#### Acceptance Criteria

| Criterion | Probe | PASS | WEAK | FAIL |
|-----------|-------|------|------|------|
| 저장소 이해 | "이번 동기화 후에도 이 저장소가 무엇을 하는지 빠르게 이해되는가?" | Goal/핵심 요약이 이번 구현 반영으로 더 명확해졌거나 유지된다 | Goal은 유지되지만 구현 반영이 다소 흐리다 | 구현 반영 후 목적/범위 설명이 모순되거나 불명확하다 |
| 기능 위치 탐색 | "이번에 동기화한 기능 X는 어디에 있는가?" | 동기화된 컴포넌트/기능이 실제 경로와 심볼에 연결된다 | 기능은 보이지만 경로/심볼 연결이 약하다 | 이번에 반영한 기능의 소유 위치를 알 수 없다 |
| 안전한 수정 판단 | "이제 변경 Y는 어디서 시작해야 하는가?" | `Common Change Paths`, `Usage Examples`, 컴포넌트 정보에서 시작점과 확인 포인트를 찾을 수 있다 | 시작점은 있으나 검증 포인트나 영향 범위가 약하다 | 동기화 후에도 변경 시작점이 보이지 않는다 |
| 결정/불변 조건 기억 | "이번 구현으로 확정된 결정/가정은 기록되었는가?" | 새 불변 조건, 해결/잔존 질문, rationale이 관련 섹션 또는 `DECISION_LOG.md`에 반영된다 | 일부만 반영되었다 | 새 결정/불변 조건이 문서에 남지 않았다 |

#### Self-Check Procedure

1. 이번에 변경/추가한 섹션과 직접 연결된 컴포넌트 스펙만 다시 읽는다.
2. 위 네 개 probe를 이번 동기화 범위에 대입해 본다.
3. 각 criterion을 `PASS` / `WEAK` / `FAIL`로 판정한다.
4. 결과에 따라 행동한다:
   - `ALL PASS`: 완료
   - `WEAK`만 존재: 개선 포인트를 완료 보고에 포함하고 진행
   - `FAIL` 존재: Step 4로 돌아가 해당 부분만 보강 후 재판정
   - 재판정 후에도 `FAIL`: 사용자에게 보고하고 판단을 맡긴다

#### Completion Output

완료 보고에 아래 표를 포함한다:

| Criterion | Probe | 판정 | 근거 |
|-----------|-------|------|------|
| 저장소 이해 | "이번 동기화 후 저장소 목적이 명확한가?" | PASS | (구체적 근거) |
| 기능 위치 탐색 | "동기화한 기능 X는 어디에?" | PASS | (구체적 근거) |
| 안전한 수정 판단 | "변경 시작점은 어디인가?" | PASS | (구체적 근거) |
| 결정/불변 조건 기억 | "새 결정/가정은 기록되었는가?" | PASS | (구체적 근거) |

**종합**: `PASS` / `PASS WITH NOTES` / `FAIL -> FIX`

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
- quality gate result
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

- verify against code, not just plan artifacts
- keep the main spec as the fastest entry point
- prefer path and symbol updates over vague narrative
- make future change points easier to find than before
- preserve meaningful rationale, but keep it compact

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
- `references/update-strategies.md` - sync strategy guide
- `references/drift-patterns.md` - common drift patterns for exploration-first specs

### Example Files
- `examples/review-report.md` - example sync report
- `examples/changelog-entry.md` - optional changelog examples

## Integration with Other Skills

- `feature-draft` creates the planned patch baseline
- `implementation` produces the implementation reality
- `spec-update-todo` records planned work before implementation
- `spec-review` is the review-only alternative
