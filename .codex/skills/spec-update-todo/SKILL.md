---
name: spec-update-todo
description: This skill should be used when the user asks to "update spec with features", "add features to spec", "update spec from input", "add requirements to spec", "spec update", "expand spec", "add to-do to spec", "add to-implement to spec", or mentions adding new features, requirements, or planned improvements to an existing specification document.
version: 1.0.0
---

# Spec Update from User Input

> **Workflow Role Note**: In the large-scale SDD path, run this skill after `feature-draft` to pre-reflect planned requirements into spec documents before implementation.
> `feature-draft` generates draft artifacts only; actual spec document updates are applied by this skill.

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

## Hard Rules

1. **Always backup**: 스펙 파일 수정 전 반드시 `_sdd/spec/prev/PREV_<filename>_<timestamp>.md`로 백업한다.
2. **Rename processed input files**: 처리된 입력 파일은 반드시 `_processed_` 접두사로 이름 변경한다.
3. **한국어 작성**: 추가 내용은 스펙 문서 언어를 따르되, 기본은 한국어로 작성한다.
4. **DECISION_LOG.md 최소화**: 결정 로그는 `DECISION_LOG.md`에만 기록하며, 추가 문서는 사용자 요청 시에만 생성한다.
5. **스펙 구조 보존**: 기존 스펙의 구조와 스타일을 유지하며, 필요한 항목만 추가한다.

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
- **`user_draft.md`**: 사용자 작성 초안 (draft)

If there are both `_sdd/spec/user_spec.md` or `_sdd/spec/user_draft.md` existing, apply deterministic defaults what to choose.

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

**Tools**: `Glob`, `Read`

```
1. Check if user provided requirements in conversation
2. Check if input files exist (in order of priority):
   - `_sdd/spec/user_draft.md` (사용자 초안)
   - `_sdd/spec/user_spec.md` (user-written)
3. If multiple sources exist, process all (conversation first, then files)
4. If no sources found, apply deterministic defaults for input
```

**Decision Gate 1→2**:
```
input_found = (사용자 대화 OR user_draft.md OR user_spec.md) 중 하나 이상 존재

IF input_found → Step 2 진행
ELSE → deterministic defaults (non-interactive): 업데이트할 요구사항 요청
```

### Step 2: Load Current Spec

**Tools**: `Read`, `Glob`, `deterministic defaults (non-interactive)`

```
1. Locate the main spec document in `_sdd/spec/` (prefer `_sdd/spec/<project>.md` as the index/main spec; `_sdd/spec/main.md` may exist in older projects)
2. If multiple plausible main spec files exist, apply deterministic defaults which file to update (and treat as the index/main spec)
3. If the spec is already split across multiple files, follow the index/links and update the appropriate file(s)
4. Check spec size/complexity. If the spec is getting too large to maintain comfortably in one file (e.g. >500 lines, or the component/API sections dominate navigation), split automatically using deterministic defaults.
   - keep `_sdd/spec/<project>.md` as an index/overview, extract long sections into separate files under `_sdd/spec/`, and link them from the index using a consistent naming scheme such as:
     - `_sdd/spec/<project>_API.md`
     - `_sdd/spec/<project>_DATA_MODEL.md`
     - `_sdd/spec/<project>_COMPONENTS.md`
     - Other suffixes are allowed if they better fit the project domain (e.g. `_ARCH.md`, `_FLOWS.md`, `_DB_SCHEMA.md`)—keep the naming consistent and log the split/file map in `Open Questions`.
     - Naming style: prefer `UPPER_SNAKE_CASE` suffixes (e.g. `_DATA_MODEL`, `_DB_SCHEMA`) for consistency.
     - Split rationale template:
       - "대형 스펙 자동 분할 적용: 인덱스+하위 문서 구조로 전환하고 파일맵을 기록."
5. Read current spec content (index + any referenced sub-specs that will be affected)
6. If `_sdd/spec/DECISION_LOG.md` exists, read relevant entries before deciding how to insert/update requirements
7. Identify sections that will be updated:
   - "목표" / "Goal" → for new features
   - "발견된 이슈 및 개선 필요사항" / "Issues & Improvements" → for bugs/improvements
   - "컴포넌트 상세" / "Component Details" → for component changes
   - Create new sections if needed
```

### Step 3: Parse User Input

**Tools**: `Read`

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

**Tools**: — (분류/매핑, 도구 불필요)

| Category | Target Section | Update Type |
|----------|---------------|-------------|
| New Feature | 목표 > 주요 기능 | Add to list |
| Enhancement | 개선 필요사항 > 개선 제안 | Add with priority |
| Bug Fix | 발견된 이슈 > 버그 | Add to issues |
| Component Change | 컴포넌트 상세 | Update/add section |
| Configuration | 설정 | Add options |
| API Change | API 레퍼런스 | Add endpoints |

### Step 5: Generate Update Plan

**Tools**: `deterministic defaults (non-interactive)`

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

**Decision Gate 5→6**:
```
plan_presented = Update Plan을 작업 로그로 제시 완료
plan_validated = 자동 일관성 검증 통과

IF plan_presented AND plan_validated → Step 6 진행
ELSE IF NOT plan_presented → Step 5 재실행
ELSE → 자동 보정 후 계획 수정 (최대 2라운드)
```

### Step 6: Apply Updates

**Tools**: `Edit`, `Write`, `Bash (mkdir -p)`

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

**Tools**: `Bash (mv)`

Rename processed input files to mark as completed:

```bash
# If user_draft.md was used
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

## Context Management

| 스펙 크기 | 전략 | 구체적 방법 |
|-----------|------|-------------|
| < 200줄 | 전체 읽기 | `Read`로 전체 파일 읽기 |
| 200-500줄 | 전체 읽기 가능 | `Read`로 전체 읽기, 필요 시 섹션별 |
| 500-1000줄 | TOC 먼저, 관련 섹션만 | 상위 50줄(TOC) 읽기 → 관련 섹션만 `Read(offset, limit)` |
| > 1000줄 | 인덱스만, 타겟 최대 3개 | 인덱스/TOC만 읽기 → 타겟 섹션 최대 3개 선택적 읽기 |

| 코드베이스 크기 | 전략 | 구체적 방법 |
|----------------|------|-------------|
| < 50 파일 | 자유 탐색 | `Glob` + `Read` 자유롭게 사용 |
| 50-200 파일 | 타겟 탐색 | `rg`/`Glob`/`Read`/`Bash`으로 후보 식별 → 타겟 `Read` |
| > 200 파일 | 타겟 탐색 | `rg`/`Glob`/`Read`/`Bash` 위주 → 최소한의 `Read` |

## Language Handling

- **Follow Spec Language**: If spec is in Korean, add Korean content
- **Preserve Consistency**: Don't mix languages within sections
- **Translate if Needed**: Convert input to spec's language

## Error Handling

| Situation | Action |
|-----------|--------|
| Spec file not found | Suggest running `spec-create` first |
| Ambiguous input | Use deterministic defaults (non-interactive) for clarification |
| Conflicting requirements | Flag and apply deterministic defaults to resolve |
| Invalid input file format | Report parsing errors, suggest corrections |
| 백업 디렉토리 미존재 | `mkdir -p _sdd/spec/prev/` 자동 생성 |
| 대형 스펙 (500줄+) | 인덱스+하위 문서 구조로 자동 분할 |
| 다수 입력 파일 존재 | 입력 우선순위 규칙으로 자동 병합 |
| 입력 파일과 스펙 섹션 매핑 불가 | 휴리스틱 매핑 후 `Open Questions` 기록 |

### Post-Update Glob 검증

```
1. Glob("_sdd/spec/<project>.md") → 수정된 스펙 파일 존재 확인
2. 변경 로그(Changelog) 항목 존재 확인
3. 버전 번호 증가 확인
4. prev/PREV_* 백업 파일 존재 확인
5. 처리된 입력 파일 이름 변경 확인 (_processed_ 접두사)
```

## Integration with Other Skills

```
spec-create → spec-update-todo → implementation-plan → implementation → spec-update-done
                                                                        │
                                                                        │
                                                                        │
                   └────────────────────────────────────────────────────┘
```

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
