---
name: pr-review
description: This skill should be used when the user asks to "review PR", "PR review", "review PR against spec", "PR 리뷰", "PR 검증", "스펙 기반 PR 리뷰", "PR 승인 검토", or wants to verify a pull request's implementation against the specification and spec patch draft.
version: 1.1.0
---

# PR Review - Spec-Based PR Verification and Verdict

Verifies PR implementation against the original spec and spec patch draft, then generates a structured review report (`_sdd/pr/PR_REVIEW.md`).

## Acceptance Criteria
> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.
- [ ] AC1: `_sdd/pr/PR_REVIEW.md` 리뷰 리포트가 Output Format에 맞게 생성되었다
- [ ] AC2: Verdict(APPROVE / REQUEST CHANGES / NEEDS DISCUSSION)가 근거와 함께 부여되었다
- [ ] AC3: Patch draft(또는 PR diff 기반 추론)의 모든 Acceptance Criteria가 개별 검증되었다
- [ ] AC4: 기존 spec 대비 compliance 위반 여부가 확인되었다
- [ ] AC5: 기존 리뷰 파일이 있으면 `_sdd/pr/prev/`로 아카이브되었다

## Hard Rules

- Spec files under `_sdd/spec/` are **never** created/modified/deleted. This skill only produces the review report.
- If spec updates are needed, record as "Items Requiring Spec Update" and direct user to `/spec-update-todo`.
- Review report output is written in **Korean**, following the spec's language.
- Preserve PR title/description as-is; provide translation alongside if needed.
- Use the default, most capable model (e.g. Opus 4.6) unless the user specifies otherwise. Report the model used at the beginning of the review.

## Workflow Position

```
implementation → PR → pr-spec-patch → pr-review → approve/revise → spec-update-todo
```

## Prerequisites

- `gh` CLI authenticated (`gh auth status`)
- Spec documents in `_sdd/spec/` (recommended)
- `_sdd/pr/spec_patch_draft.md` (recommended, not required)
- GitHub repository with an existing PR
- If running code/tests locally, check `_sdd/env.md` first

## Process

### Mode 1: Preferred (patch draft available)

#### Step 1: Verify prerequisites

1. `gh auth status` → check authentication
2. Search for spec files in `_sdd/spec/`
3. Verify `_sdd/pr/spec_patch_draft.md` exists
4. Determine PR number (auto-detect or user input)
5. Create `_sdd/pr/` directory if needed
6. If running tests locally, apply `_sdd/env.md` settings

**Patch draft PR number mismatch**: Warn user, then run degraded mode or recommend re-running `/pr-spec-patch`.

#### Step 2: Load context

1. Read current spec files (if multiple, use AskUserQuestion to select)
2. Read patch draft → extract Acceptance Criteria
3. Collect PR metadata (`gh pr view`)
4. Collect PR diff (`gh pr diff`)

```bash
gh pr view --json number --jq '.number'
gh pr view [PR_NUMBER] --json title,body,author,state,url,additions,deletions,changedFiles,headRefName,baseRefName,commits,comments,reviews
gh pr diff [PR_NUMBER]
gh pr diff [PR_NUMBER] --name-only
```

#### Step 3: Acceptance criteria verification

For each Feature/Improvement/Bug Fix in the patch draft:

| Step | Action |
|------|--------|
| 1 | Find corresponding implementation in PR diff → `file:line` reference |
| 2 | Find related tests → test name |
| 3 | Verify test pass status (CI or local; apply `_sdd/env.md` for local) |
| 4 | Mark status: **✓ Met** (impl + tests pass) / **✗ Not met** (no impl or test failure) / **△ Partially met** (impl but no tests, or partial) |

#### Step 4: Spec compliance verification

1. Extract key requirements from existing spec
2. Check whether PR changes violate existing requirements
3. Identify breaking changes
4. Check for API contract changes

#### Step 5: Gap analysis

| Perspective | What to check |
|-------------|--------------|
| Patch draft vs PR | Items claimed but not implemented; changes in PR but not in patch |
| Test gaps | AC without tests; failing tests |
| Documentation gaps | New settings/env vars not documented; API changes not documented |

#### Step 6: Verdict decision

| Verdict | Conditions |
|---------|-----------|
| **APPROVE** | All AC met + no spec violations + all tests pass |
| **REQUEST CHANGES** | Critical AC not met / spec violation / test failure / security issue |
| **NEEDS DISCUSSION** | Intentional spec change / design trade-off / scope ambiguity / new architectural decision needed |

#### Step 7: Report generation

1. If existing `PR_REVIEW.md` exists, archive to `_sdd/pr/prev/PREV_PR_REVIEW_<timestamp>.md`
2. Generate `_sdd/pr/PR_REVIEW.md` using the [Output Format](#output-format)
3. Present summary table then full report:
   ```
   | 항목 | 내용 |
   |------|------|
   | Verdict | APPROVE / REQUEST CHANGES / NEEDS DISCUSSION |
   | Acceptance Criteria | X/Y met (Z%) |
   | Spec Violations | N개 |
   | Test Pass Rate | N% |
   | Pre-merge Blockers | N개 |
   ```
4. Save report and guide next steps

### 파일 작성 위임

`write-skeleton` 서브에이전트에 위임한다. 반환값이 SKELETON_ONLY이면 Sections Remaining 목록을 보고 Edit으로 채운다.
- 독립 섹션 2개+ → 병렬 Agent dispatch 가능
- 의존 섹션 → 순서대로 Edit
- 완료 후 TODO/Phase 마커 제거

서브에이전트 호출 시 아래 Output Format 전체와 작성에 필요한 맥락(수집된 정보, 분석 결과 등)을 프롬프트에 포함한다.

### Mode 2: Degraded (no patch draft)

#### Step 0: Large-diff gate

1. Check PR size: `gh pr diff --name-only | wc -l` + `gh pr view --json additions,deletions`
2. If large (10+ files OR 500+ lines): AskUserQuestion with options to run `/pr-spec-patch` first or proceed
3. If small: continue directly

#### Degraded mode differences

| Step | Change |
|------|--------|
| Step 2 | Skip patch draft loading |
| Step 3 | Infer AC from PR diff (commit messages, PR description) |
| Step 5 | Compare PR vs spec only (no patch comparison) |
| Report | Patch Draft field = "Not Found"; note lower confidence |

Steps 4, 6, 7 proceed identically.

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
| No patch draft | Degraded mode; recommend `/pr-spec-patch` |
| No spec file | Warn; recommend `/spec-create`; minimal review from PR diff only |
| No PR / `gh` not authenticated | Guide installation/authentication |
| Multiple spec files | AskUserQuestion to select |
| Existing review file | Archive to `_sdd/pr/prev/` then create new |
| Already merged PR | Allow retroactive review; note merge status |
| No tests / no CI | Mark test section as "Cannot verify"; guide local execution |

## Error Handling

| Situation | Response |
|-----------|----------|
| `gh` CLI not installed | `brew install gh` |
| `gh auth` failure | `gh auth login` |
| Wrong PR number | Display error, request correct number |
| Network error | Guide retry |
| Spec file parsing failure | Show error location, request manual review |
| `_sdd/pr/` directory missing | Create automatically |
| `_sdd/env.md` missing | Do not guess; ask user to confirm environment |

## Additional Resources

- **`references/review-checklist.md`** - PR review checklist
- **`pr-spec-patch/references/gh-commands.md`** - `gh` CLI command reference
- **`examples/sample-review.md`** - PR review session example

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

