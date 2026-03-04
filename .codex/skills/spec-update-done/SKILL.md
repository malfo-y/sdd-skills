---
name: spec-update-done
description: This skill should be used when the user asks to "review spec", "update spec from code", "sync spec with implementation", "spec drift check", "verify spec accuracy", "refresh spec document", "spec needs update", or mentions spec document maintenance, code-to-spec synchronization, or implementation log analysis.
version: 1.0.0
---

# Spec Review and Update

Review and update Software Design Description (SDD) spec documents based on code changes, implementation logs, and user feedback. Ensures spec documents remain accurate and synchronized with the actual codebase.

## Simplified Workflow

This skill is **Step 4 of 4** in the simplified SDD workflow:

```
spec → feature-draft → implementation → spec-update-done (this)
```

| Step | Skill | Purpose |
|------|-------|---------|
| 1 | spec-create | Create the initial spec document |
| 2 | feature-draft | Draft feature spec patch + implementation plan |
| 3 | implementation | Execute the implementation plan (TDD) |
| **4** | **spec-update-done** | Sync spec with actual code |

> **Workflow**: spec → feature-draft → implementation → spec-update-done

## Hard Rules

1. **Report before changing**: 변경 사항을 적용하기 전에 반드시 Change Report를 사용자에게 먼저 제시한다.
2. **Always backup to prev/**: 스펙 파일 수정 전 `_sdd/spec/prev/PREV_<filename>_<timestamp>.md`로 백업한다.
3. **Copy-only archive**: 구현 산출물은 복사만 하며 원본을 이동/삭제하지 않는다.
4. **한국어 작성**: 추가/수정 내용은 한국어로 작성한다 (기존 영어 부분 유지).
5. **DECISION_LOG.md 최소화**: 결정 로그는 `DECISION_LOG.md`에만 기록하며, 추가 거버넌스 문서는 사용자 요청 시에만 생성한다.

## Overview

This skill analyzes multiple sources of truth to identify spec drift and generate updates:
- Current spec documents in `_sdd/spec/`
- Decision rationale in `_sdd/spec/DECISION_LOG.md` (if present)
- Implementation logs in `_sdd/implementation/`
- Code diffs (git diff, recent commits)
- User conversation and feedback

## When to Use This Skill

- After significant code changes to sync documentation
- During implementation review cycles
- When spec accuracy is questioned
- Periodic spec maintenance and refresh
- Before creating new implementation plans

## Input Sources

### 1. Implementation Logs (`_sdd/implementation/`)

| File | Purpose |
|------|---------|
| `IMPLEMENTATION_PLAN.md` | Current implementation tasks and phases |
| `IMPLEMENTATION_PROGRESS.md` | Task completion status |
| `IMPLEMENTATION_REVIEW.md` | Review findings and issues |
| `IMPLEMENTATION_REPORT.md` | Final implementation report (progress, quality assessment, issues, recommendations) |
| `IMPLEMENTATION_REPORT_PHASE_<N>.md` | Per-phase implementation report |
| `TEST_SUMMARY.md` | Test results and coverage |
| `user_spec.md` | User requirements and feedback |
| `_sdd/implementation/prev/PREV_*.md` | Historical versions for context |
| `IMPLEMENTATION_INDEX.md` | Feature-level archive index (copy history by `feature_id`) |

### 2. Feature Drafts (`_sdd/drafts/`)

| File | Purpose |
|------|---------|
| `feature_draft_<name>.md` | Combined spec patch draft (Part 1) and implementation plan (Part 2) from `feature-draft` skill |

### 3. Code Changes

- `git diff` - Uncommitted changes
- `git log` - Recent commit history
- `git diff HEAD~N` - Changes over N commits

### 4. Current Spec Documents

- `_sdd/spec/main.md` or `<project-name>.md`
- Component-specific specs
- Any referenced sub-specs
- `_sdd/spec/DECISION_LOG.md` (if present)

### 5. User Conversation

- Direct feedback and corrections
- New requirements mentioned
- Clarifications on behavior

### 6. Execution/Test Environment Guide (when local verification is needed)

- `_sdd/env.md` (preferred)
- User-provided environment instructions

If local code/test execution is needed to verify claims, read `_sdd/env.md` first and apply required setup (e.g., conda env, environment variables, local services).

## Review Process

### Step 1: Gather Context

**Tools**: `Read`, `Glob`, `Bash (git diff, git log, git status)`

Collect information from all available sources:

```
1. Read current spec document(s)
2. Read implementation logs:
   - IMPLEMENTATION_PLAN.md (planned work)
   - IMPLEMENTATION_PROGRESS.md (what's done)
   - IMPLEMENTATION_REVIEW.md (issues found)
   - IMPLEMENTATION_REPORT.md (final report: progress, quality, issues, recommendations)
   - IMPLEMENTATION_REPORT_PHASE_<N>.md (per-phase reports, if present)
   - TEST_SUMMARY.md (test status)
3. Read feature drafts (if present):
   - _sdd/drafts/feature_draft_<name>.md (spec patch + implementation plan)
4. Analyze code changes:
   - git status (current state)
   - git diff (uncommitted changes)
   - git log --oneline -20 (recent commits)
5. Read relevant decision-log entries from `_sdd/spec/DECISION_LOG.md` (if file exists)
6. Note user conversation context
7. If local execution/tests are required for verification, load `_sdd/env.md` and apply setup before running commands
8. Resolve `feature_id` for archive step:
   - user-provided value if explicit
   - else derive from `feature_draft_<name>.md` when unambiguous
   - else derive from implementation plan/report title when unambiguous
   - else ask user before archive
```

**Decision Gate 1→2**:
```
spec_loaded = 스펙 문서 읽기 완료
sources_available = (구현 로그 OR git diff OR 사용자 피드백) 중 하나 이상 존재

IF spec_loaded AND sources_available → Step 2 진행
ELSE IF NOT spec_loaded → request_user_input (Plan mode) / direct question (Default mode): 스펙 파일 위치 확인
ELSE IF NOT sources_available → request_user_input (Plan mode) / direct question (Default mode): 비교 대상 소스 확인
```

### Step 2: Identify Spec Drift

**Tools**: `rg`, `Glob`, `Read`, `Bash`, `Read`, `Bash (git diff)`

Compare spec against reality to find discrepancies:

**Architecture Drift:**
- New components added but not documented
- Components removed or renamed
- Changed dependencies or integrations
- Modified data flow

**Feature Drift:**
- New features implemented
- Features removed or deprecated
- Changed behavior or API
- Modified configuration options

**Issue Drift:**
- Issues resolved but still listed
- New issues discovered
- Changed priorities or status
- Technical debt updates

**Environment Drift:**
- New dependencies added
- Version changes
- Configuration changes
- Directory structure changes

### Step 3: Generate Change Report

**Tools**: — (분석 결과 정리, 도구 불필요)

Create a structured diff report:

```markdown
## Spec Review Report

**Reviewed**: YYYY-MM-DD
**Spec Version**: X.Y.Z
**Code State**: <commit hash or description>

### Summary
- X sections need updates
- Y new items to add
- Z items to remove/archive

### Architecture Changes
| Section | Current Spec | Actual State | Action |
|---------|--------------|--------------|--------|
| Components | Lists A, B, C | Has A, B, C, D | Add D |

### Feature Changes
| Feature | Spec Status | Actual Status | Action |
|---------|-------------|---------------|--------|
| Auth | "Planned" | Implemented | Update |

### Issue Updates
| Issue | Spec Status | Actual Status | Action |
|-------|-------------|---------------|--------|
| BUG-001 | Open | Fixed in PR#42 | Mark resolved |

### Environment Changes
| Item | Spec Value | Actual Value | Action |
|------|------------|--------------|--------|
| Python | 3.10 | 3.11 | Update |
```

**Decision Gate 3→4**:
```
report_presented = Change Report를 사용자에게 제시 완료
user_approved = 사용자가 변경 사항 승인

IF report_presented AND user_approved → Step 4 진행
ELSE IF NOT report_presented → Step 3 재실행
ELSE IF NOT user_approved → 사용자 피드백 반영 후 Report 수정 → 재승인 요청 (최대 2라운드)
```

### Step 4: Apply Updates

**Tools**: `Edit`, `Write`, `Bash (mkdir -p)`

Update spec document with identified changes:

**Update Strategy:**
1. Preserve accurate existing content
2. Add new sections/items as needed
3. Update changed information
4. Archive or remove obsolete content
5. Add changelog entry
6. If behavior/architecture intent changed, append a concise entry to `_sdd/spec/DECISION_LOG.md`

**Spec Splitting (when spec is too large):**
- If the main spec has grown too large to maintain comfortably in a single file (e.g. >500 lines or difficult navigation), ask the user whether they want to split it into multiple files.
- If user agrees: keep `_sdd/spec/<project>.md` as an index/overview, move large sections into separate files under `_sdd/spec/`, and link them from the index using a consistent naming scheme such as:
  - `_sdd/spec/<project>_API.md`
  - `_sdd/spec/<project>_DATA_MODEL.md`
  - `_sdd/spec/<project>_COMPONENTS.md`
- Other suffixes are allowed if they better match the project domain (e.g. `_ARCH.md`, `_FLOWS.md`, `_DB_SCHEMA.md`). Keep the naming consistent and confirm the intended split with the user.
- Naming style: prefer `UPPER_SNAKE_CASE` suffixes (e.g. `_DATA_MODEL`, `_DB_SCHEMA`) for consistency.
- Ask-first template:
  - "현재 스펙이 커져서 관리가 어려워 보여요. `_sdd/spec/<project>.md`를 인덱스로 두고 `_sdd/spec/<project>_API.md`, `_sdd/spec/<project>_DATA_MODEL.md`(등)으로 분할할까요? 원하시면 suffix/파일 구성을 먼저 합의한 뒤 진행할게요."
- Create backups under `_sdd/spec/prev/` for every existing file you will modify during the split.

**Versioning:**
- Increment patch version for minor updates
- Increment minor version for feature changes
- Increment major version for architecture changes

### Step 5: Validate Updates

**Tools**: `rg`, `Glob`, `Read`, `Bash`, `Bash (git diff)`

Verify updated spec accuracy:

- Cross-reference with code
- Check all file paths exist
- Verify dependency versions
- Confirm API endpoints match
- If local tests/commands are used for verification, apply `_sdd/env.md` setup first
- If `_sdd/env.md` is missing/incomplete, ask the user for environment details instead of guessing
- Review with user if significant changes

**Decision Gate 5→6**:
```
all_paths_valid = 모든 파일 경로/링크 유효
versions_match = 의존성 버전 일치
no_regressions = 기존 정확한 내용 보존됨

IF all_paths_valid AND versions_match AND no_regressions → Step 6 진행
ELSE → 실패 항목 수정 후 재검증
```

### Step 6: Archive Implementation Artifacts by Feature (Copy-only)

**Tools**: `Bash (cp, mkdir -p)`, `Write`, `Read`

After spec updates are finalized, archive related implementation artifacts for the resolved `feature_id`.

Rules:
1. Keep `_sdd/implementation/IMPLEMENTATION_*.md` in place (no move/delete).
2. Create directory if missing: `_sdd/implementation/features/<feature_id>/`
3. Copy existing files (if present):
   - `IMPLEMENTATION_PLAN*.md`
   - `IMPLEMENTATION_PROGRESS*.md`
   - `IMPLEMENTATION_REVIEW.md`
   - `IMPLEMENTATION_REPORT*.md`
   - `TEST_SUMMARY.md`
4. Use timestamped destination filenames to avoid overwrite:
   - `_sdd/implementation/features/<feature_id>/SYNC_<YYYYMMDD_HHMMSS>_<original_filename>`
5. Create/update `_sdd/implementation/IMPLEMENTATION_INDEX.md`:
   - maintain one section per `feature_id`
   - append sync entries with `synced_at` (UTC), copied file mappings (`destination <- source`), and optional notes
6. If `feature_id` is still ambiguous, ask user and skip archive step until confirmed.

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

## Output Format

### Change Report

Present findings before making changes:

```markdown
## Spec Review Findings

### Changes Detected

**High Priority (Architecture/Breaking):**
1. [Change description]

**Medium Priority (Features/Behavior):**
1. [Change description]

**Low Priority (Documentation/Style):**
1. [Change description]

### Recommended Updates

[List of proposed changes]

### Questions for User

[Any ambiguities requiring clarification]
```

### Progressive Disclosure

```
1. Change Report 요약 테이블 제시:
   | 항목 | 내용 |
   |------|------|
   | 변경 섹션 수 | N개 |
   | 추가 항목 | N개 |
   | 제거/아카이브 항목 | N개 |
   | 버전 변경 | X.Y.Z → X.Y.Z+1 |

2. request_user_input (Plan mode) / direct question (Default mode): "상세 변경 내용을 확인하시겠습니까?"
   옵션:
   1. "전체 확인" → 모든 변경 사항 상세 출력
   2. "특정 카테고리만" → 선택한 카테고리만 출력
   3. "바로 적용" → Step 4 진행
```

### Updated Spec

After user approval, generate updated spec:

1. Create backup(s): for each spec file you will edit, save `prev/PREV_<spec-file>_<timestamp>.md` in `_sdd/spec/prev/` (create the directory first if needed)
2. Apply changes to spec document(s)
3. Update version and last-updated date
4. Add changelog entry (include references to `prev/PREV_...` backup(s), and note if the spec was split into multiple files)
5. Update `_sdd/spec/DECISION_LOG.md` if this sync introduces a new decision or changes previous rationale
6. Copy implementation artifacts to `_sdd/implementation/features/<feature_id>/` and update `_sdd/implementation/IMPLEMENTATION_INDEX.md` (copy-only; keep root implementation files intact)

## Automation Patterns

### Quick Sync

Fast update for minor changes:

```
1. git diff --stat (identify changed files)
2. Map changed files to spec sections
3. Update only affected sections
4. Preserve rest of document
```

### Full Review

Comprehensive review for major updates:

```
1. Read entire codebase structure
2. Compare against full spec
3. Generate complete change report
4. Rewrite affected sections
```

### Continuous Sync

Incremental updates during development:

```
1. Monitor IMPLEMENTATION_PROGRESS.md
2. Update spec as tasks complete
3. Flag issues for investigation
4. Maintain living documentation
```

## Best Practices

### Accuracy

- **Verify before updating**: Don't assume implementation matches plan
- **Check code directly**: Read actual files, not just logs
- **Test assertions**: Verify API endpoints, configs actually work
- **Use correct runtime setup**: Before local checks/tests, follow `_sdd/env.md`
- **Cross-reference**: Compare multiple sources

### Preservation

- **Keep history**: Always create `prev/PREV_...` backup under `_sdd/spec/prev/` before updates
- **Archive by feature safely**: Copy implementation artifacts to `features/<feature_id>/` and record them in `IMPLEMENTATION_INDEX.md` without moving root files
- **Preserve context**: Don't remove valuable explanations
- **Maintain structure**: Follow existing spec organization
- **Version control**: Increment version appropriately

### Communication

- **Report before changing**: Show findings before applying updates
- **Highlight breaking changes**: Flag architecture/API changes
- **Ask when uncertain**: Use request_user_input (Plan mode) / direct question (Default mode) for ambiguities
- **Document decisions**: Note why changes were made in `_sdd/spec/DECISION_LOG.md`
- **Avoid Artifact Sprawl**: Do not create extra context/governance docs unless the user explicitly asks

## Integration

### With Implementation Skills

```
spec-create → feature-draft → implementation → spec-update-done
                                    │                   │
                                    ↓                   │
                           IMPLEMENTATION_REPORT.md     │
     ↑                                                  │
     └──────────────────────────────────────────────────┘
```

### Trigger Points

- After `implementation` skill completes and generates `IMPLEMENTATION_REPORT.md`
- After `implementation-review` completes
- When user says "implementation done"
- Before creating new implementation plan
- Periodic maintenance (user-triggered)

## Error Handling

| 상황 | 대응 |
|------|------|
| `_sdd/spec/` 디렉토리 미존재 | `spec-create` 먼저 실행 권장 |
| 스펙 파일 미발견 | 사용자에게 스펙 파일 경로 확인 |
| 구현 로그 미존재 | git diff 기반 Quick Sync 모드로 전환 |
| git 이력 없음 | 코드 직접 분석으로 대체 |
| `_sdd/env.md` 미존재/불완전 | 로컬 실행 건너뛰고 사용자에게 환경 확인 |
| feature_id 모호 | 사용자에게 확인 후 아카이브 진행 |
| 대형 스펙 (500줄+) | 분할 제안 (ask-first) |
| 백업 디렉토리 미존재 | `mkdir -p _sdd/spec/prev/` 자동 생성 |
| 충돌하는 변경 사항 | 사용자에게 우선순위 확인 |

## Additional Resources

### Reference Files
- **`references/drift-patterns.md`** - Common drift patterns and solutions
- **`references/update-strategies.md`** - Strategies for different update types

### Example Files
- **`examples/review-report.md`** - Sample review report format
- **`examples/changelog-entry.md`** - Changelog entry examples
