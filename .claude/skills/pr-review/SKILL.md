---
name: pr-review
description: This skill should be used when the user asks to "review PR", "PR review", "review PR against spec", "PR 리뷰", "PR 검증", "스펙 기반 PR 리뷰", "PR 승인 검토", or wants to verify a pull request's implementation against the specification and spec patch draft.
version: 1.0.0
---

# PR Review - Spec-Based PR Verification and Verdict

Verifies PR implementation against the original spec and spec patch draft, then generates a structured review report (`_sdd/pr/PR_REVIEW.md`).

## Overview

This skill verifies PR implementation against the current spec documents (`_sdd/spec/`) and the spec patch draft (`_sdd/pr/spec_patch_draft.md`), producing a structured review report that includes acceptance criteria fulfillment, spec compliance status, gap analysis results, and a final verdict (Approve / Request Changes / Needs Discussion).

## Hard Rule: This skill does NOT modify specs (IMPORTANT)

- Spec files under `_sdd/spec/` are **never** created/modified/deleted.
- This skill only produces the review report (`_sdd/pr/PR_REVIEW.md`).
- If spec updates are needed, they are recorded in the report as "Items Requiring Spec Update" and the user is directed to use `/spec-update-todo` for actual changes.

## Workflow Position

```
implementation → PR → pr-spec-patch → pr-review → approve/revise → spec-update-todo
                          ↑              ↑↓
                     current spec   verification & verdict
                  (_sdd/spec/)     (_sdd/pr/PR_REVIEW.md)
```

## Language

- **Write in Korean**: All review report output must be written in Korean.
- Follow the spec's language: if the spec is in Korean, the review should also be in Korean.

## LLM Model to use

Use the default, most capable model (e.g. Opus 4.5) to review the PR otherwise mentioned by the user.
Report the model used at the beginning of the review.

## When to Use This Skill

- Post-PR, pre-merge verification
- Reviewing PR implementation from a spec perspective
- Verifying acceptance criteria claims in the patch draft
- Checking spec compliance and detecting violations
- Retroactive review of already-merged PRs

## Prerequisites

- `gh` CLI authenticated (`gh auth status` to verify)
- Spec documents exist in `_sdd/spec/` directory (recommended)
- `_sdd/pr/spec_patch_draft.md` exists (recommended, not required)
- GitHub repository with an existing PR
- If running code/tests locally, check `_sdd/env.md` first and apply the execution environment (e.g., conda, env vars, required services)

## Input Sources

1. **Current spec (`_sdd/spec/`)**: Existing spec requirements and architecture baseline
2. **Spec patch draft (`_sdd/pr/spec_patch_draft.md`)**: Claimed changes and acceptance criteria from the PR
3. **PR data (`gh` CLI)**: PR metadata, diff, commit information
4. **Test results**: CI status or local test execution results
5. **Environment docs (`_sdd/env.md`)**: Environment variables, conda environments, pre-execution procedures needed for local testing

## Output

**File location**: `_sdd/pr/PR_REVIEW.md`

**Format**: Verdict + metrics summary + acceptance criteria verification + spec compliance verification + gap analysis + recommendations

## Process

### Mode 1: Preferred (patch draft available)

#### Step 1: Verify prerequisites

```
1. Run `gh auth status` to check authentication
2. Search for spec files in `_sdd/spec/` directory
3. Verify `_sdd/pr/spec_patch_draft.md` exists
4. Determine PR number (auto-detect or user input)
5. Create `_sdd/pr/` directory if it doesn't exist
6. If planning to run tests locally, check `_sdd/env.md` and apply required environment settings
```

**When patch draft PR number doesn't match:**
- Warning: "The patch draft is for a different PR (#X)."
- Ignore the patch draft and run in degraded mode, or recommend re-running `/pr-spec-patch`

#### Step 2: Load context

```
1. Read current spec files (if multiple, use AskUserQuestion to select)
2. Read patch draft → extract Acceptance Criteria
3. Collect PR metadata (gh pr view)
4. Collect PR diff (gh pr diff)
```

See `pr-spec-patch/references/gh-commands.md` for PR data collection commands:

```bash
# Auto-detect PR number
gh pr view --json number --jq '.number'

# PR metadata
gh pr view [PR_NUMBER] --json title,body,author,state,url,additions,deletions,changedFiles,headRefName,baseRefName,commits,comments,reviews

# PR diff
gh pr diff [PR_NUMBER]

# Changed files list
gh pr diff [PR_NUMBER] --name-only
```

#### Step 3: Acceptance criteria verification

For each Feature/Improvement/Bug Fix in the patch draft:

```
For each Acceptance Criterion:
1. Find the corresponding implementation in the PR diff → file:line reference
2. Find related tests → test name
3. Verify test pass status (CI or local; apply `_sdd/env.md` instructions for local execution)
4. Determine status:
   - ✓ Met: Implementation exists + tests pass
   - ✗ Not met: No implementation or test failure
   - △ Partially met: Implementation exists but no tests, or partial implementation
```

#### Step 4: Spec compliance verification

```
1. Extract the list of key requirements from the existing spec
2. Check whether PR changes violate existing requirements
3. Identify breaking changes
4. Check for API contract changes
```

#### Step 4.5: Acceptance Criteria 검증 결과 요약 (Checkpoint)

**Tools**: `AskUserQuestion`

```
1. 검증 결과 요약 테이블을 사용자에게 제시:
   | 항목 | Met (✓) | Not Met (✗) | Partial (△) |
   |------|---------|-------------|-------------|
   | Features | N | N | N |
   | Improvements | N | N | N |
   | Bug Fixes | N | N | N |
   | Spec Violations | - | N | - |

2. AskUserQuestion: "Acceptance Criteria 검증 결과를 확인해 주세요."
   옵션:
   1. "확인, Gap 분석 진행" → Step 5
   2. "특정 항목 재검증" → 지정 항목 재검증 후 재제시
```

#### Step 5: Gap analysis

Three-perspective gap analysis:

**(a) Patch draft vs PR implementation:**
- Items claimed in the patch but not implemented in the PR
- Changes in the PR but not listed in the patch

**(b) Test gaps:**
- Acceptance criteria without tests
- Failing tests

**(c) Documentation gaps:**
- New settings/environment variables not documented
- API changes not documented

#### Step 6: Verdict decision

| Verdict | Conditions |
|---------|-----------|
| **APPROVE** | All acceptance criteria met + no spec violations + all tests pass |
| **REQUEST CHANGES** | Critical acceptance criteria not met / spec violation / test failure / security issue |
| **NEEDS DISCUSSION** | Intentional spec change / design trade-off / scope ambiguity / new architectural decision needed |

#### Step 7: Report generation

1. If existing `PR_REVIEW.md` exists, archive to `_sdd/pr/prev/PREV_PR_REVIEW_<timestamp>.md` (create `_sdd/pr/prev/` if needed)
2. Generate `_sdd/pr/PR_REVIEW.md` using the [Output Format](#output-format) below
3. **Progressive Disclosure**:
   ```
   1. 리뷰 요약 테이블 제시:
      | 항목 | 내용 |
      |------|------|
      | Verdict | APPROVE / REQUEST CHANGES / NEEDS DISCUSSION |
      | Acceptance Criteria | X/Y met (Z%) |
      | Spec Violations | N개 |
      | Test Pass Rate | N% |
      | Pre-merge Blockers | N개 |

   2. AskUserQuestion: "상세 리뷰 내용을 확인하시겠습니까?"
      옵션:
      1. "전체 리뷰" → 전체 리포트 출력
      2. "Blockers만" → Pre-merge Blockers만 상세 출력
      3. "파일로 저장" → PR_REVIEW.md 저장
   ```
4. Present summary to user and guide next steps

### Mode 2: Degraded (no patch draft)

When no patch draft is available:

#### Step 0: Large-diff gate

```
1. Check PR size:
   - `gh pr diff [PR_NUMBER] --name-only | wc -l` → changed file count
   - `gh pr view [PR_NUMBER] --json additions,deletions` → line change count
2. If large PR (10+ changed files OR 500+ total line changes):
   → AskUserQuestion: "이 PR은 변경 규모가 큽니다 (N개 파일, +X/-Y줄). Spec patch 없이 리뷰하면 정확도가 낮을 수 있습니다."
     옵션:
     1. "먼저 `/pr-spec-patch` 실행" → Stop and guide user to run `/pr-spec-patch` first
     2. "그대로 리뷰 진행" → Continue with degraded mode below
3. If small PR (< 10 files AND < 500 lines): Continue with degraded mode directly
```

#### Degraded mode execution

```
Warning message:
"Reviewing without a patch draft. Running `/pr-spec-patch` first and then re-reviewing will produce more accurate results."
```

**Differences:**
- Step 2: Skip patch draft loading
- Step 3: Infer acceptance criteria from PR diff (based on commit messages, PR description)
- Step 5: Cannot compare patch vs PR → compare PR vs spec only
- Report's "Patch Draft" field: "Not Found"
- Explicitly note lower confidence overall

Steps 4, 6, and 7 proceed identically.

## Context Management

| 스펙 크기 | 전략 | 구체적 방법 |
|-----------|------|-------------|
| < 200줄 | 전체 읽기 | `Read`로 전체 파일 읽기 |
| 200-500줄 | 전체 읽기 가능 | `Read`로 전체 읽기, 필요 시 섹션별 |
| 500-1000줄 | TOC 먼저, 관련 섹션만 | 상위 50줄(TOC) 읽기 → 관련 섹션만 `Read(offset, limit)` |
| > 1000줄 | 인덱스만, 타겟 최대 3개 | 인덱스/TOC만 읽기 → 타겟 섹션 최대 3개 선택적 읽기 |

| PR 크기 | 전략 | 구체적 방법 |
|---------|------|-------------|
| < 10 files | 전체 diff 분석 | `gh pr diff` 전체 읽기 |
| 10-50 files | 파일별 분석 | `gh pr diff --name-only` → 관련 파일만 diff 확인 |
| > 50 files | 디렉토리/컴포넌트 수준 | 디렉토리별 요약, 스펙 관련 컴포넌트만 상세 분석 |

## Output Format

```markdown
# PR Review Report

**PR**: #<number> - <title>
**PR Author**: <author>
**Review Date**: YYYY-MM-DD
**Reviewer**: Claude (<model>)
**Spec Version**: <version>
**Patch Draft**: Found / Not Found

---

## Verdict

**[APPROVE / REQUEST CHANGES / NEEDS DISCUSSION]**

**Rationale**: <1-2 sentence rationale>
**Key Findings**:
- <finding 1>
- <finding 2>

---

## Metrics Summary

| Item | Count |
|------|-------|
| Total acceptance criteria | N |
| Met (✓) | X (Y%) |
| Not met (✗) | A (B%) |
| Partially met (△) | C (D%) |
| Spec violations | E |
| Test pass rate | F% |

---

## Acceptance Criteria Verification

### Feature: <name>
**Source**: Patch Draft - <section>

| # | Acceptance Criterion | PR Implementation | Test | Status | Notes |
|---|---------------------|-------------------|------|--------|-------|
| 1 | <criterion> | `file:line` | test_name | ✓/✗/△ | note |

**Assessment**: X/Y met ✓/✗

(Repeat for each Feature/Improvement/Bug Fix)

---

## Spec Compliance Verification

### Existing Spec Requirements Verification

| Spec Section | Requirement | PR Impact | Status | Notes |
|-------------|------------|-----------|--------|-------|

### Spec Violations
(List or "None")

---

## Gap Analysis

### Patch Draft vs PR Implementation

#### Claimed in patch but not implemented
1. <item with file:line refs>

#### In PR but not listed in patch
1. <item with file:line refs>

### Test Gaps
1. <untested criteria or failing tests>

---

## Test Status

### Test Execution Results

| Test File | Test Count | Pass | Fail | Skip |
|-----------|-----------|------|------|------|

### Failed Test Details
(Per failed test: file, error, related acceptance criteria, severity, action)

---

## Recommendations

### Pre-merge Blockers
| Priority | Item | Severity | Location | Action |
|----------|------|----------|----------|--------|

### Pre-merge Recommended
| Priority | Item | Severity | Action |
|----------|------|----------|--------|

### Optional Improvements
| Priority | Item | Benefit |
|----------|------|---------|

---

## Reviewer Notes

### Design Decisions
### Items Requiring Spec Update
### Suggested Follow-up Work

---

## Next Steps

1. [ ] Take action based on Verdict
2. [ ] (if Request Changes) Fix and re-review: `/pr-review`
3. [ ] (if Approve) After merge, run `/spec-update-todo`

---

## Metadata

**Review version**: <count>
**PR commit SHA**: <sha>
**Spec file**: <path>
**Patch draft file**: <path or "None">
**Generated at**: YYYY-MM-DD HH:MM:SS
```

## Edge Cases

| Situation | Response |
|-----------|----------|
| No patch draft | Run in degraded mode, recommend running `/pr-spec-patch` |
| No spec file | Warn, recommend `/spec-create`, perform minimal review from PR diff only |
| No PR / `gh` not authenticated | Detect error, guide installation/authentication |
| Multiple spec files | Use AskUserQuestion to select |
| Existing review file | Archive to `_sdd/pr/prev/PREV_PR_REVIEW_<timestamp>.md` then create new |
| Patch draft for a different PR | Warn, ignore patch draft and run degraded mode or recommend re-running `/pr-spec-patch` |
| Already merged PR | Allow (retroactive review), note merge status |
| Large PR (50+ files) | Focus on spec-related components, summarize by directory |
| No tests / no CI | Mark test section as "Cannot verify", guide local execution |
| `_sdd/env.md` missing/incomplete | Do not guess execution environment, ask user to confirm environment before proceeding |

## Best Practices

### Effective Reviews

- **Evidence-based**: Include specific file:line references for all verdicts
- **Acceptance criteria-focused**: Systematically verify each acceptance criterion from the patch draft one by one
- **Verify against spec**: Check not only new features but also whether existing spec requirements are violated
- **Test linkage**: Verify existence and pass status of tests corresponding to each acceptance criterion

### Verdict Guidelines

- **Conservative verdicts**: When uncertain, verdict as NEEDS DISCUSSION
- **Clarify blockers**: When issuing REQUEST CHANGES, always provide a specific list of blockers
- **Separate design discussions**: Distinguish functional issues from design decisions in the report

### File Management

- **Archive first**: Always archive existing review files before creating new ones
- **Track review versions**: Increment version number on re-reviews
- **Link patch draft**: Record patch draft file path in metadata

## Language Handling

- **SKILL.md**: English (skill definition)
- **Review report output**: Korean
- **Follow spec language**: If the spec is in Korean, write the review in Korean
- **Preserve PR content**: Keep PR title/description as-is, provide translation alongside if needed

## Error Handling

| Situation | Response |
|-----------|----------|
| `gh` CLI not installed | Guide installation: `brew install gh` |
| `gh auth` failure | Guide running `gh auth login` |
| Wrong PR number | Display error message, request correct PR number |
| Network error | Guide retry |
| Spec file parsing failure | Show error location, request manual review |
| `_sdd/pr/` directory missing | Create automatically |

## Additional Resources

### Reference Files
- **`references/review-checklist.md`** - PR review checklist
- **`pr-spec-patch/references/gh-commands.md`** - `gh` CLI command reference

### Example Files
- **`examples/sample-review.md`** - PR review session example
