---
name: spec-update-todo
description: This skill should be used when the user asks to "update spec with features", "add features to spec", "update spec from input", "add requirements to spec", "spec update", "expand spec", "add to-do to spec", "add to-implement to spec", or mentions adding new features, requirements, or planned improvements to an existing specification document.
version: 1.0.0
---

# Spec Update from User Input

Update existing spec documents with new features, requirements, and planned improvements based on user input. This skill focuses on adding "to-add" or "to-implement" items to the spec.

## Overview

This skill processes user requirements and feature requests to update spec documents. Input can come from:
1. **User conversation**: Direct discussion about new features
2. **Input file**: `_sdd/spec/user_spec.md` or `_sdd/spec/user_draft.md` containing structured requirements
3. **Decision log**: `_sdd/spec/DECISION_LOG.md` for existing rationale/constraints (if present)

After processing input files, rename them to mark as processed:
- `user_spec.md` → `_processed_user_spec.md`
- `user_draft.md` → `_processed_user_draft.md`

## When to Use This Skill

- Adding new feature requirements to an existing spec
- Expanding spec with planned improvements
- Incorporating user feedback into documentation
- Processing batched feature requests from input file
- Updating "to-implement" or roadmap sections

## Input Sources

### 1. User Conversation

Direct input from the current conversation:
- Feature descriptions
- Requirements discussions
- Enhancement requests
- Bug reports to document

### 2. Input File (`_sdd/spec/user_spec.md` or `user_draft.md`)

User input file for spec update. Two file types are supported:
- **`user_spec.md`**: User-written specification input
- **`user_draft.md`**: Draft created via `/spec-draft` conversation

If there are both `_sdd/spec/user_spec.md` or `_sdd/spec/user_draft.md` existing, ask user what to choose.

Recommended format is a structured file format for batched updates, but any free-form text are accepted.

Example structured file format:

```markdown
# Spec Update Input

## New Features

### Feature: [Feature Name]
**Priority**: [High/Medium/Low]
**Description**: [What it should do]
**Acceptance Criteria**:
- [ ] Criterion 1
- [ ] Criterion 2

### Feature: [Another Feature]
...

## Improvements

- [Improvement 1]
- [Improvement 2]

## Bug Reports

- [Bug description and expected fix]

## Notes

[Additional context or constraints]
```

### 3. Decision Log (`_sdd/spec/DECISION_LOG.md`, optional)

If present, use it as a constraint/rationale source:
- Prior decisions that limit solution space
- Rejected alternatives to avoid reintroducing
- Context needed to understand "why this requirement exists"

## Update Process

### Step 1: Identify Input Source

```
1. Check if user provided requirements in conversation
2. Check if input files exist (in order of priority):
   - `_sdd/spec/user_draft.md` (from /spec-draft)
   - `_sdd/spec/user_spec.md` (user-written)
3. If multiple sources exist, process all (conversation first, then files)
4. If no sources found, ask user for input
```

### Step 2: Load Current Spec

```
1. Locate the main spec document in `_sdd/spec/` (prefer `_sdd/spec/<project>.md` as the index/main spec; `_sdd/spec/main.md` may exist in older projects)
2. If multiple plausible main spec files exist, ask the user which file to update (and treat as the index/main spec)
3. If the spec is already split across multiple files, follow the index/links and update the appropriate file(s)
4. Check spec size/complexity. If the spec is getting too large to maintain comfortably in one file (e.g. >500 lines, or the component/API sections dominate navigation), ask the user whether they want to split the spec into multiple files.
   - If user agrees: keep `_sdd/spec/<project>.md` as an index/overview, extract long sections into separate files under `_sdd/spec/`, and link them from the index using a consistent naming scheme such as:
     - `_sdd/spec/<project>_API.md`
     - `_sdd/spec/<project>_DATA_MODEL.md`
     - `_sdd/spec/<project>_COMPONENTS.md`
     - Other suffixes are allowed if they better fit the project domain (e.g. `_ARCH.md`, `_FLOWS.md`, `_DB_SCHEMA.md`)—just keep the naming consistent and confirm the split/file map with the user before doing a large refactor.
     - Naming style: prefer `UPPER_SNAKE_CASE` suffixes (e.g. `_DATA_MODEL`, `_DB_SCHEMA`) for consistency.
     - Ask-first template:
       - "현재 스펙이 커져서 관리가 어려워 보여요. `_sdd/spec/<project>.md`를 인덱스로 두고 `_sdd/spec/<project>_API.md`, `_sdd/spec/<project>_DATA_MODEL.md`(등)으로 분할할까요? 원하시면 suffix/파일 구성을 먼저 합의한 뒤 진행할게요."
5. Read current spec content (index + any referenced sub-specs that will be affected)
6. If `_sdd/spec/DECISION_LOG.md` exists, read relevant entries before deciding how to insert/update requirements
7. Identify sections that will be updated:
   - "목표" / "Goal" → for new features
   - "발견된 이슈 및 개선 필요사항" / "Issues & Improvements" → for bugs/improvements
   - "컴포넌트 상세" / "Component Details" → for component changes
   - Create new sections if needed
```

### Step 3: Parse User Input

Extract structured information from input:

**From Conversation:**
- Feature names and descriptions
- Priority indicators
- Technical requirements
- Acceptance criteria

**From Input File:**
- Parse markdown structure
- Extract features, improvements, bugs
- Preserve priority and criteria

### Step 4: Categorize Updates

| Category | Target Section | Update Type |
|----------|---------------|-------------|
| New Feature | 목표 > 주요 기능 | Add to list |
| Enhancement | 개선 필요사항 > 개선 제안 | Add with priority |
| Bug Fix | 발견된 이슈 > 버그 | Add to issues |
| Component Change | 컴포넌트 상세 | Update/add section |
| Configuration | 설정 | Add options |
| API Change | API 레퍼런스 | Add endpoints |

### Step 5: Generate Update Plan

Before modifying, present update plan:

```markdown
## Spec Update Plan

**Spec File**: `_sdd/spec/apify_ig.md`
**Input Source**: [conversation / user_spec.md / both]

### Changes to Apply

#### Section: 목표 > 주요 기능
- ADD: [New feature 1]
- ADD: [New feature 2]

#### Section: 발견된 이슈 및 개선 필요사항
- ADD: [Improvement 1] (Priority: High)
- ADD: [Bug report 1]

#### New Section: [Section Name] (if needed)
- CREATE: [New section content]

### Questions (if any)
- [Clarification needed]
```

### Step 6: Apply Updates

Update spec document:

1. **Backup**: Before editing any spec file, save a versioned copy under `_sdd/spec/prev/`:
   - `prev/PREV_<spec-file>_<timestamp>.md`
   - If `_sdd/spec/prev/` does not exist, create it first
   - If multiple spec files will be edited (because the spec is split), create one `prev/PREV_...` backup for each file being modified
2. **Insert**: Add new items to appropriate sections
3. **Format**: Match existing style and language
4. **Version**: Increment patch version (X.Y.Z → X.Y.Z+1)
5. **Date**: Update "최종 수정일" / "Last Updated"
6. **Changelog**: Add an entry describing the update and referencing the `prev/PREV_...` backup(s)
7. **Decision Log** (optional but recommended): if this update introduces or changes a key decision, append a concise entry to `_sdd/spec/DECISION_LOG.md`

### Step 7: Process Input Files

Rename processed input files to mark as completed:

```bash
# If user_draft.md was used (from /spec-draft)
mv _sdd/spec/user_draft.md _sdd/spec/_processed_user_draft.md

# If user_spec.md was used (user-written)
mv _sdd/spec/user_spec.md _sdd/spec/_processed_user_spec.md
```

Add processing metadata to each processed file:
```markdown
<!-- Processed: 2026-02-04 -->
<!-- Applied to: apify_ig.md v1.0.1 -->
```

## Update Templates

### Adding New Feature

```markdown
## 목표

### 주요 기능

1. **기존 기능 1**: 설명
2. **기존 기능 2**: 설명
3. **[NEW] 새 기능**: 설명  <!-- 추가됨: 2026-02-04 -->
```

### Adding Improvement

```markdown
## 발견된 이슈 및 개선 필요사항

### 개선 제안

1. **기능 확장** (우선순위: 높음)  <!-- 추가됨: 2026-02-04 -->
   - 현재: [현재 상태]
   - 제안: [제안 내용]
   - 이유: [이유]
```

### Adding Component

```markdown
## 컴포넌트 상세

### 컴포넌트: [새 컴포넌트 이름]  <!-- 추가됨: 2026-02-04 -->

#### 개요

[컴포넌트 설명]

| 항목 | 설명 |
|------|------|
| **목적** | [목적] |
| **입력** | [입력] |
| **출력** | [출력] |
| **상태** | 📋 계획됨 (To-Implement) |
```

### Status Indicators

Use these status markers for planned items:

| Marker | Meaning |
|--------|---------|
| 📋 계획됨 | Planned, not started |
| 🚧 진행중 | In progress |
| ✅ 완료 | Completed |
| ⏸️ 보류 | On hold |

## Output Format

### Updated Spec

Apply changes directly to spec file with:
- Version increment
- Date update
- Changelog entry
- Inline comments for new items (optional)

### Update Summary

After updating, provide summary:

```markdown
## Spec Update Complete

**File**: `_sdd/spec/apify_ig.md`
**Version**: 1.0.0 → 1.0.1
**Date**: 2026-02-04

### Applied Changes

| Section | Change | Item |
|---------|--------|------|
| 주요 기능 | ADD | 새 기능 1 |
| 개선 제안 | ADD | 개선 사항 1 |
| 컴포넌트 | ADD | 새 컴포넌트 |

### Input File Status
- [x] `_sdd/spec/user_draft.md` → `_processed_user_draft.md` (if used)
- [x] `_sdd/spec/user_spec.md` → `_processed_user_spec.md` (if used)

### Decision Log
- [x] `_sdd/spec/DECISION_LOG.md` updated (if a new/changed decision was identified)
- [ ] No decision-log update needed

### Next Steps
- Run `/spec-update-done` after implementation to sync spec with code
```

## Best Practices

### Input Quality

- **Be Specific**: Include concrete requirements, not vague ideas
- **Include Criteria**: Define what "done" looks like
- **Set Priority**: Help prioritize implementation order
- **Provide Context**: Explain why the feature is needed

### Update Quality

- **Match Style**: Follow existing spec's language and format
- **Preserve Structure**: Don't reorganize existing content
- **Mark New Items**: Use comments or markers for traceability
- **Keep History**: Update changelog for significant additions
- **Preserve Why**: Reuse/update `_sdd/spec/DECISION_LOG.md` when requirements depend on non-obvious rationale
- **Keep Scope Tight**: Do not introduce additional side documents beyond `DECISION_LOG.md` unless requested

### File Management

- **Atomic Updates**: Complete all changes before saving
- **Backup Explicitly**: Always create `prev/PREV_<spec-file>_<timestamp>.md` in `_sdd/spec/prev/` before updating a spec file (even if git history exists)
- **Clean Up**: Rename processed input files
- **Track Processing**: Add metadata to processed files

## Language Handling

- **Follow Spec Language**: If spec is in Korean, add Korean content
- **Preserve Consistency**: Don't mix languages within sections
- **Translate if Needed**: Convert input to spec's language

## Error Handling

| Situation | Action |
|-----------|--------|
| Spec file not found | Suggest running `spec-create` first |
| Ambiguous input | Use AskUserQuestion for clarification |
| Conflicting requirements | Flag and ask user to resolve |
| Invalid input file format | Report parsing errors, suggest corrections |

## Integration with Other Skills

```
spec-create → spec-update-todo → implementation-plan → implementation → spec-update-done
                   ↑                                                    │
                   │                                                    │
              spec-draft                                                │
              (user_draft.md)                                           │
                   ↑                                                    │
                   └────────────────────────────────────────────────────┘
```

- **spec-draft**: Collect requirements via conversation, outputs `user_draft.md`
- **spec-create**: Create initial spec (run first if no spec exists)
- **implementation-plan**: Plan implementation of new features
- **implementation**: Implement the planned features
- **spec-update-done**: Sync spec with actual code after implementation

## Additional Resources

### Reference Files
- **`references/input-format.md`** - Detailed input file format guide
- **`references/section-mapping.md`** - How to map inputs to spec sections

### Example Files
- **`examples/user_spec.md`** - Sample input file
- **`examples/update-summary.md`** - Sample update summary
