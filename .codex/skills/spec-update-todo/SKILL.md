---
name: spec-update-todo
description: This skill should be used when the user asks to "update spec with features", "add features to spec", "update spec from input", "add requirements to spec", "spec update", "expand spec", "add to-do to spec", "add to-implement to spec", or mentions adding new features, requirements, or planned improvements to an existing specification document.
version: 1.0.0
---

# Spec Update from User Input

| Workflow | Position | When |
|----------|----------|------|
| Large | Step 2 of 6 | feature-draft 후 스펙에 사전 반영 (드리프트 방지) |
| Medium | — | feature-draft가 통합 처리 |
| Small | — | 직접 구현 |

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
3. **언어 규칙**: 기존 스펙/문서의 언어를 따른다. 새 프로젝트(기존 스펙 없음)는 한국어 기본. 사용자 명시 지정 시 해당 언어 사용.
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

If both `_sdd/spec/user_spec.md` and `_sdd/spec/user_draft.md` exist, prefer `user_draft.md` first and merge complementary details from `user_spec.md`. Record the assumption in the update plan when both materially contribute.

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
4. If no sources found, stop with a short report explaining that there is no update input to apply
```

**Decision Gate 1→2**:
```
input_found = (사용자 대화 OR user_draft.md OR user_spec.md) 중 하나 이상 존재

IF input_found → Step 2 진행
ELSE → 짧은 보고 후 종료: 업데이트할 요구사항 입력이 없음
```

### Step 2: Load Current Spec

**Tools**: `Read`, `Glob`

```
1. Locate the main spec document in `_sdd/spec/` with this priority:
   - (1) `_sdd/spec/<project>.md` (프로젝트명 기반)
   - (2) `_sdd/spec/main.md` (이전 프로젝트)
   - (3) 단일 .md 파일만 존재하면 자동 선택
   - (4) 2개 이상 후보 시에는 인덱스 역할이 가장 명확한 파일을 선택하고, 선택 근거를 Update Plan에 기록
2. If multiple plausible main spec files exist, choose the most likely index/main spec deterministically and record the assumption in the Update Plan
3. If the spec is already split across multiple files, follow the index/links and update the appropriate file(s)
4. Read current spec content (index + any referenced sub-specs that will be affected)
5. If `_sdd/spec/DECISION_LOG.md` exists, read relevant entries before deciding how to insert/update requirements
   - DECISION_LOG 충돌 처리: (1) Update Plan에 충돌 사항 명시 (2) DECISION_LOG에 새 항목으로 추가 (3) Summary에 포함
6. Identify sections that will be updated:
   - "배경 및 동기" / "Background & Motivation" (§1) → for motivation/problem statement changes
   - "핵심 설계" / "Core Design" (§2) → for design/algorithm changes
   - "목표" / "Goal" → for new features
   - "발견된 이슈 및 개선 필요사항" / "Issues & Improvements" → for bugs/improvements
   - "컴포넌트 상세" / "Component Details" (§4) → for component changes
   - "사용 가이드 & 기대 결과" / "Usage Guide & Expected Results" (§5) → for usage scenarios
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
| Background/Motivation | 배경 및 동기 (§1) | Update narrative |
| Design Change | 핵심 설계 (§2) | Update design/algorithm |
| New Feature | 목표 > 주요 기능 | Add to list |
| Enhancement | 개선 필요사항 > 개선 제안 | Add with priority |
| Bug Fix | 발견된 이슈 > 버그 | Add to issues |
| Component Change | 컴포넌트 상세 (§4) | Update/add section |
| Usage Scenario | 사용 가이드 & 기대 결과 (§5) | Add scenario |
| Configuration | 설정 (§8) | Add options |
| API Change | API 레퍼런스 (§7) | Add endpoints |
| Code Reference | 부록: 코드 레퍼런스 목록 | Add reference |

> 상세 섹션 매핑 규칙은 `references/section-mapping.md`를 참조한다.

### Step 5: Generate Update Plan

**Tools**: — (보고 단계, 도구 불필요)

Before modifying, present an update plan as a report:

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

### Open Questions (if any)
- [Clarification needed]
```

**Decision Gate 5→6**:
```
plan_presented = Update Plan을 작업 로그로 제시 완료

IF plan_presented → Step 6 진행 (보고 후 자동 진행)
ELSE → Step 5 재실행
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
| 50-200 파일 | 타겟 탐색 | `rg`/`Glob`으로 후보 식별 → 타겟 `Read` |
| > 200 파일 | 타겟 탐색 | `rg`/`Glob` 위주 → 최소한의 `Read` |

## Language Handling

- **Follow Spec Language**: 기존 스펙/문서의 언어를 따른다
- **Preserve Consistency**: 섹션 내 언어를 혼합하지 않는다
- **Translate if Needed**: 입력을 스펙 언어로 변환한다
- **New Project Default**: 새 프로젝트(기존 스펙 없음)는 한국어 기본

## Error Handling

| Situation | Action |
|-----------|--------|
| Spec file not found | Suggest running `spec-create` first |
| Ambiguous input | 최선의 해석으로 진행, 판단 불가 시 스펙에 Open Questions로 기록 |
| Conflicting requirements | 충돌 내용을 Update Plan과 `Open Questions`에 기록하고, 비파괴적 방향으로만 적용 |
| Invalid input file format | Report parsing errors, suggest corrections |
| 백업 디렉토리 미존재 | `mkdir -p _sdd/spec/prev/` 자동 생성 |
| 다수 입력 파일 존재 | `user_draft.md` 우선 + 보조 입력 병합 규칙 적용, 가정은 Update Plan에 기록 |
| 입력 파일과 스펙 섹션 매핑 불가 | 보수적인 섹션에만 반영하고 불확실한 항목은 `Open Questions`에 기록 |

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
Large:    feature-draft → spec-update-todo → implementation-plan → implementation → implementation-review → spec-update-done
Medium:   feature-draft → implementation → spec-update-done
Small:    직접 구현 (→ implementation-review) (→ spec-update-done)
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
