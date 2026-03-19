---
name: pr-spec-patch
description: This skill should be used when the user asks to "create spec patch from PR", "PR spec patch", "compare PR with spec", "PR to spec", "PR 스펙 패치", "PR 리뷰 준비", "스펙 패치 생성", "PR 변경사항 스펙 반영", or wants to generate a spec patch document by comparing a pull request against the current specification.
version: 1.0.0
---

# PR Spec Patch - PR-Based Spec Patch Draft Generation

| Workflow | Position | When |
|----------|----------|------|
| PR workflow | Step 1 of 2 | PR 기반 스펙 패치 초안 생성 |

Compares a PR against the current spec, generates a structured spec patch draft, and refines it through conversation.

## Acceptance Criteria

> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] AC1: `_sdd/pr/spec_patch_draft.md` 파일이 Output Format에 맞게 생성됨
- [ ] AC2: 모든 패치 항목에 PR Evidence (`file:line`) 포함
- [ ] AC3: "Spec Patch Content" 섹션이 `spec-update-todo`의 "Spec Update Input" 형식과 호환
- [ ] AC4: 스펙 파일(`_sdd/spec/`)은 일절 수정하지 않음

## Hard Rules

- Spec files under `_sdd/spec/` are **never** created/modified/deleted. The only output is `_sdd/pr/spec_patch_draft.md`.
- Spec updates **must** be done via `/spec-update-todo`.
- Patch draft output language follows the spec language (Korean spec → Korean patch). PR title/description은 원문 유지, 필요 시 번역 병기.

## Prerequisites

- `gh` CLI authenticated (`gh auth status`)
- Spec documents in `_sdd/spec/` (recommended, not required)
- GitHub repository with an existing PR

## Process

### Mode 1: Initial Generation (no existing draft)

#### Step 1: Verify prerequisites

1. Run `gh auth status`
2. Search for spec files in `_sdd/spec/`
3. Create `_sdd/pr/` directory if needed

No spec file → warn user, recommend `/spec-create`, proceed without baseline if user agrees.

#### Step 2: Read current spec

1. Load main spec from `_sdd/spec/`
2. Multiple spec files → AskUserQuestion to select
3. Understand component/feature/section structure

#### Step 3: Collect PR data

No PR number specified → auto-detect from current branch:

```bash
gh pr view --json number --jq '.number'
gh pr view [PR_NUMBER] --json title,body,author,state,url,additions,deletions,changedFiles,headRefName,baseRefName,commits,comments,reviews
gh pr diff [PR_NUMBER]
gh pr diff [PR_NUMBER] --name-only
```

Large PR (50+ files) → directory/component-level summary, focus on spec-related components.

**Exit → Step 4**: spec loaded (or baseline-skip confirmed) AND PR data collected.

#### Step 4: Analyze changes

Map PR file changes to spec components:

| Category | Detection Criteria |
|----------|-------------------|
| New Features | New files/modules, new endpoints/classes |
| Improvements | Existing file modifications, refactoring |
| Bug Fixes | Bug fix commits, error handling additions |
| Component Changes | Structure/interface changes |
| Configuration Changes | Config/env file changes |

**Exit → Step 5**: changes categorized AND spec mapping done.

#### Step 5: Generate patch draft

Save analyzed information to `_sdd/pr/spec_patch_draft.md` per Output Format.

출력 문서 작성 시 `write-phased` 서브에이전트에 위임한다. Output Format 전체와 맥락(수집 정보, 분석 결과)을 프롬프트에 포함.

#### Step 5.5: PR Evidence 검증

| Check | Fail action |
|-------|-------------|
| 각 패치 항목에 PR Evidence (`file:line`) 존재 | "Evidence 미확인" 표시 |
| Evidence 파일 경로가 PR diff 파일 목록에 포함 | 경로 재확인 |
| 스펙 섹션 매핑 존재 | "Target Section TBD" 표시 |

#### Step 6: Present to user

1. Show patch draft summary
2. Highlight key questions/suggestions
3. Guide: refine via conversation → finalize → apply via `/spec-update-todo`

### Mode 2: Update (existing draft)

#### Step 1: Load existing draft

1. Read `_sdd/pr/spec_patch_draft.md`
2. Different PR → archive to `_sdd/pr/prev/PREV_spec_patch_draft_<timestamp>.md`, then create new

#### Step 2: Regenerate draft

1. Re-collect PR data (`gh pr view`, `gh pr diff`)
2. Preserve user modifications from existing draft
3. Generate new draft

#### Step 3: Apply user feedback

Modify/add/remove patch content, resolve questions, update spec gaps.

#### Step 4: Save

Update draft file, increment conversation round, update timestamp.

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

---

## Spec Patch Content

<!-- Compatible with spec-update-todo's "Spec Update Input" format -->

### New Features

#### Feature: <feature name>
**Priority**: High/Medium/Low | **Category**: <category>
**Target Component**: <component> | **Source**: PR #<number>

**Description**: <feature description>

**Acceptance Criteria**:
- [ ] Criterion 1

**PR Evidence**:
- `<file>:<line>` - <change summary>

### Improvements

#### Improvement: <improvement name>
**Priority**: High/Medium/Low
**Current State**: <current> | **Proposed**: <proposed> | **Reason**: <reason>
**Source**: PR #<number>

**PR Evidence**:
- `<file>:<line>` - <change summary>

### Bug Reports

#### Bug Fix: <bug fix name>
**Severity**: High/Medium/Low | **Location**: <file:line> | **Source**: PR #<number>

**Description**: <bug description>
**Fix Approach**: <fix method>

**PR Evidence**:
- `<file>:<line>` - <change summary>

### Component Changes

#### New/Update Component: <component name>
**Change Type**: New/Enhancement/Refactor/Fix | **Source**: PR #<number>
- Change details / Planned methods

### Configuration Changes

#### Config: <config name>
**Type**: Env Var / Config File | **Required**: Yes/No | **Default**: <value>
**Description**: <description> | **Source**: PR #<number>

### Notes

- **Context**: <PR background>
- **Constraints**: <constraints>

---

## Questions and Suggestions

### Items Requiring Confirmation

1. **[Section: <spec section>]** <question>
   - Context: <why> / Suggestion: <recommendation>

### Spec Gaps

| # | Description | Spec Section | PR Evidence | Suggestion |
|---|------------|-------------|-------------|------------|
| 1 | <gap> | <section> | `<file>:<line>` | <suggestion> |

### Ambiguous Items

- <ambiguity 1>

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
| Multiple spec files | AskUserQuestion to select comparison target |
| Existing draft for different PR | Archive existing, create new |
| Already merged PR | Allow (retroactive spec maintenance), note merge status |
| Large PR (50+ files) | Directory/component-level summary |
| No spec-related changes | Notify user, generate minimal draft |

## Error Handling

| Situation | Response |
|-----------|----------|
| `gh` CLI not installed | Guide: `brew install gh` |
| `gh auth` failure | Guide: `gh auth login` |
| Wrong PR number | Error message, request correct number |
| Network error | Guide retry |
| Spec file parsing failure | Show error location, request manual review |
| `_sdd/pr/` directory missing | Create automatically |

## Workflow Integration

`implementation → PR → pr-spec-patch → (user refinement) → spec-update-todo`

## Additional Resources

- **`references/gh-commands.md`** - `gh` CLI command reference
- **`examples/spec_patch_draft.md`** - Patch draft output example
