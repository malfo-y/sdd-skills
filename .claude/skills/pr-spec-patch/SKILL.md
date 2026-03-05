---
name: pr-spec-patch
description: This skill should be used when the user asks to "create spec patch from PR", "PR spec patch", "compare PR with spec", "PR to spec", "PR 스펙 패치", "PR 리뷰 준비", "스펙 패치 생성", "PR 변경사항 스펙 반영", or wants to generate a spec patch document by comparing a pull request against the current specification.
version: 1.0.0
---

# PR Spec Patch - PR-Based Spec Patch Draft Generation

Compares a PR (Pull Request) against the current spec, generates a structured spec patch draft, and refines it through conversation.

## Overview

This skill analyzes PR changes, compares them against the current spec documents, and generates a structured patch draft (`_sdd/pr/spec_patch_draft.md`) containing changes that should be reflected in the spec. The "Spec Patch Content" section of the output is compatible with the `spec-update-todo` skill's input format ("Spec Update Input"), so finalized patches can be directly applied via `spec-update-todo`.

## Hard Rule: This skill does NOT modify specs (IMPORTANT)

- Spec files under `_sdd/spec/` are **never** created/modified/deleted.
- The only output of this skill is `_sdd/pr/spec_patch_draft.md`.
- Spec updates **must** be done via `/spec-update-todo`.

## When to Use This Skill

- When generating a spec patch draft from a PR
- When organizing changes from a spec perspective before PR review
- When refining PR changes through conversation for spec integration
- When retroactively reflecting an already-merged PR into the spec

## Prerequisites

- `gh` CLI authenticated (`gh auth status` to verify)
- Spec documents exist in `_sdd/spec/` directory (recommended, not required)
- GitHub repository with an existing PR

## Input Sources

1. **Current spec (`_sdd/spec/`)**: Main spec document used as comparison baseline
2. **PR data (`gh` CLI)**: PR metadata, changed files, diff
3. **User conversation (current session)**: Patch draft refinement and finalization
4. **Existing draft (`_sdd/pr/spec_patch_draft.md`)**: If a prior draft exists, enter update mode

## Output

**File location**: `_sdd/pr/spec_patch_draft.md`

**Format**: PR summary + "Spec Update Input" compatible patch content + questions and suggestions

## Process

### Mode 1: Initial generation (no existing draft)

#### Step 1: Verify prerequisites

```
1. Run `gh auth status` to check authentication
2. Search for spec files in `_sdd/spec/` directory
3. Create `_sdd/pr/` directory if it doesn't exist
```

**When no spec file exists:**
- Warn user: "No spec document found. Recommend creating one first with `/spec-create`."
- If user wants to proceed, generate without a comparison baseline (note "no baseline")

#### Step 2: Read current spec

```
1. Load main spec file from `_sdd/spec/`
2. If multiple spec files exist, use AskUserQuestion to request selection
3. Understand the spec's component, feature, and section structure
```

#### Step 3: Collect PR data

If no PR number is specified, auto-detect from the current branch:

```bash
# Auto-detect PR number (based on current branch)
gh pr view --json number --jq '.number'

# Collect PR metadata
gh pr view [PR_NUMBER] --json title,body,author,state,url,additions,deletions,changedFiles,headRefName,baseRefName,commits,comments,reviews

# Collect PR diff
gh pr diff [PR_NUMBER]

# List changed files
gh pr diff [PR_NUMBER] --name-only
```

**Handling large PRs (changedFiles > 50):**
- Switch to directory/component-level summary
- Focus on components documented in the spec
- Inform user about the large PR and proceed with key changes only

**Decision Gate 3→4**:
```
spec_loaded = 스펙 문서 읽기 완료 (또는 baseline 없이 진행 확인)
pr_data_collected = PR 메타데이터 + diff 수집 완료

IF spec_loaded AND pr_data_collected → Step 4 진행
ELSE IF NOT pr_data_collected → PR 데이터 재수집 시도
ELSE → AskUserQuestion: 스펙 없이 진행 여부 확인
```

#### Step 4: Analyze changes

Map PR file changes to spec components:

| Category | Detection Criteria | Examples |
|----------|-------------------|----------|
| New Features | New files/modules added, new endpoints, new classes | New service class, new API endpoint |
| Improvements | Existing file modifications, performance improvements, refactoring | Function optimization, code cleanup |
| Bug Fixes | Bug fix commits, error handling additions | Exception handling added, condition fix |
| Component Changes | Component structure changes, interface changes | New method added, signature change |
| Configuration Changes | Config file changes, environment variable additions | .env change, config file modification |

**Decision Gate 4→5**:
```
changes_categorized = PR 변경사항 카테고리 분류 완료
spec_mapping_done = 스펙 컴포넌트 매핑 완료

IF changes_categorized AND spec_mapping_done → Step 5 진행
ELSE → 미분류 항목 추가 분석
```

#### Step 5: Generate patch draft

Save the collected/analyzed information in structured form to `_sdd/pr/spec_patch_draft.md`.

See the [Output Format](#output-format) section below for the output format.

#### Step 5.5: 패치 항목 PR Evidence 검증

```
패치 항목별 검증:
  a. 각 Feature/Improvement/Bug Fix에 PR Evidence (file:line) 존재 확인
  b. PR Evidence의 파일 경로가 PR diff 파일 목록에 포함되는지 확인
  c. Evidence 누락 항목 → "Evidence 미확인" 표시
  d. 스펙 섹션 매핑 누락 항목 → "Target Section TBD" 표시
```

#### Step 6: Present to user

1. Show summary of the generated patch draft
2. Highlight key items from the questions and suggestions section
3. Guide next steps:
   - Continue conversation if refinement is needed
   - Once finalized, can be applied via `/spec-update-todo`

### Mode 2: Conversation-based update (existing draft)

#### Step 1: Load existing draft

```
1. Read contents of `_sdd/pr/spec_patch_draft.md`
2. Compare the draft's PR number with the current request
3. If the draft is for a different PR: 기존 draft를 `_sdd/pr/prev/PREV_spec_patch_draft_<timestamp>.md`로 아카이브한 후 새로 생성
```

#### Step 2: Regenerate draft

기존 draft가 존재하는 경우 무조건 PR 데이터를 재수집하여 draft를 재생성한다:

1. PR 데이터 재수집 (gh pr view, gh pr diff)
2. 기존 draft의 사용자 수정 사항이 있으면 보존하여 반영
3. 새 draft 생성

#### Step 3: Apply changes

Update relevant sections based on user feedback:
- Modify/add/remove patch content
- Mark questions as resolved
- Update spec gaps

#### Step 4: Save

- Update draft file
- Increment conversation round in metadata
- Update timestamp

## Output Format

```markdown
# PR Spec Patch Draft

**Date**: YYYY-MM-DD
**PR**: #<number> - <title>
**PR Author**: <author>
**PR URL**: <url>
**Target Spec**: <spec filename>
**Status**: Draft / Reviewed / Finalized

---

## PR Summary

**Branch**: <head> → <base>
**Change Scale**: +<additions> -<deletions>, <changedFiles> files
**Key Changes**:
- <change 1>
- <change 2>
- <change 3>

---

## Spec Patch Content

<!-- Compatible with spec-update-todo's "Spec Update Input" format -->

### New Features

#### Feature: <feature name>
**Priority**: High/Medium/Low
**Category**: <category>
**Target Component**: <target component>
**Source**: PR #<number>

**Description**:
<feature description>

**Acceptance Criteria**:
- [ ] Criterion 1
- [ ] Criterion 2

**PR Evidence**:
- `<file>:<line>` - <change summary>

---

### Improvements

#### Improvement: <improvement name>
**Priority**: High/Medium/Low
**Current State**: <current state>
**Proposed**: <proposed change>
**Reason**: <reason for improvement>
**Source**: PR #<number>

**PR Evidence**:
- `<file>:<line>` - <change summary>

---

### Bug Reports

#### Bug Fix: <bug fix name>
**Severity**: High/Medium/Low
**Location**: <file:line>
**Source**: PR #<number>

**Description**:
<bug description>

**Fix Approach**:
<fix method>

**PR Evidence**:
- `<file>:<line>` - <change summary>

---

### Component Changes

#### New Component: <component name>
**Purpose**: <purpose>
**Input**: <input>
**Output**: <output>
**Source**: PR #<number>

**Planned Methods**:
- `method_name()` - description

#### Update Component: <component name>
**Change Type**: Enhancement/Refactor/Fix
**Source**: PR #<number>

**Changes**:
- Change 1
- Change 2

---

### Configuration Changes

#### New Config: <config name>
**Type**: Environment Variable / Config File
**Required**: Yes/No
**Default**: <default value>
**Description**: <description>
**Source**: PR #<number>

---

### Notes

#### Context
<PR background and context>

#### Constraints
<constraints>

---

## Questions and Suggestions

### Items Requiring Confirmation

1. **[Section: <spec section name>]** <question content>
   - Context: <why this question is needed>
   - Suggestion: <recommended approach>

2. **[Section: <spec section name>]** <question content>
   - Context: <why this question is needed>
   - Suggestion: <recommended approach>

### Spec Gaps

| # | Description | Spec Section | PR Evidence | Suggestion |
|---|------------|-------------|-------------|------------|
| 1 | <gap description> | <related spec section> | `<file>:<line>` | <suggestion> |

### Ambiguous Items

- <ambiguity 1>
- <ambiguity 2>

---

## Metadata

**Created**: YYYY-MM-DD HH:MM
**Spec version**: <version>
**PR commit**: <HEAD SHA>
**Conversation round**: <count>
```

## Edge Cases

| Situation | Response |
|-----------|----------|
| No spec file | Warn, recommend `/spec-create`, generate without baseline if user agrees |
| No PR / `gh` not authenticated | Detect error, guide `gh auth login` |
| Multiple spec files exist | Use AskUserQuestion to select comparison target |
| Existing draft for a different PR | 기존 draft를 아카이브한 후 새로 생성 |
| Already merged PR | Allow (retroactive spec maintenance), note merge status |
| Large PR (50+ files) | Directory/component-level summary, focus on spec-related components |
| No spec-related changes in PR | Notify user, generate minimal patch draft |

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

## Workflow Integration

```
implementation → PR → pr-spec-patch → (user refinement) → spec-update-todo
                          ↑                                    │
                     current spec                        main spec update
                  (_sdd/spec/)                         (_sdd/spec/)
```

1. **pr-spec-patch** (this skill): Compare PR against spec and generate patch draft
2. **User refinement**: Review/modify/finalize draft through conversation
3. **spec-update-todo**: Apply finalized patch to the main spec

## Best Practices

### Effective Patch Generation

- **Cite PR evidence**: Include specific file:line references from the PR diff for all patch items
- **Map to spec sections**: Clearly indicate which spec section each change corresponds to
- **Set priorities**: Assign priorities based on the PR's change scale and impact
- **Specific questions**: Include context and suggestions when asking for confirmation

### Conversation-Based Refinement

- **Iterative improvement**: Aim for iterative refinement rather than a perfect draft in one pass
- **Resolve questions first**: Resolve outstanding questions before finalizing
- **Track change history**: Manage revision history through conversation rounds

### File Management

- **Maintain single draft**: Keep one patch draft file per PR
- **Archive**: Archive drafts for other PRs before creating new ones
- **Post-finalization**: Apply finalized patches via `spec-update-todo` for management

## Language Handling

- **SKILL.md**: English (skill definition)
- **Patch draft output**: Korean
- **Follow spec language**: If the spec is in Korean, write the patch in Korean
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
- **`references/gh-commands.md`** - `gh` CLI command reference

### Example Files
- **`examples/spec_patch_draft.md`** - Patch draft output example
