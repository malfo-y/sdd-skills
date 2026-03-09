---
name: spec-update-done
description: This skill should be used when the user asks to "review spec", "update spec from code", "sync spec with implementation", "spec drift check", "verify spec accuracy", "refresh spec document", "spec needs update", or mentions spec document maintenance, code-to-spec synchronization, or implementation log analysis.
version: 1.0.0
---

# Spec Review and Update

Review and update Software Design Description (SDD) spec documents based on code changes, implementation logs, and user feedback. Ensures spec documents remain accurate and synchronized with the actual codebase.

## Workflow Position

| Workflow | Position | When |
|----------|----------|------|
| Large | Step 6 of 6 | 구현 완료 후 스펙 동기화 |
| Medium | Step 3 of 3 | 구현 완료 후 스펙 동기화 |
| Small | Optional | 스펙에 영향 있는 변경 시 |

## Hard Rules

1. **Report before changing**: 변경 사항을 적용하기 전에 반드시 Change Report를 사용자에게 먼저 제시한다.
2. **Always backup to prev/**: 스펙 파일 수정 전 `_sdd/spec/prev/PREV_<filename>_<timestamp>.md`로 백업한다.
3. **Copy-only archive**: 구현 산출물은 복사만 하며 원본을 이동/삭제하지 않는다.
4. **언어 규칙**: 기존 스펙/문서의 언어를 따른다. 새 프로젝트(기존 스펙 없음)는 한국어 기본. 사용자 명시 지정 시 해당 언어 사용.
5. **DECISION_LOG.md 최소화**: 결정 로그는 `DECISION_LOG.md`에만 기록하며, 추가 거버넌스 문서는 사용자 요청 시에만 생성한다.
6. **앵커 섹션 기준 드리프트 분류**: 드리프트 항목을 보고할 때 영향받는 앵커 섹션을 명시한다:
   - `Goal`, `Architecture Overview > Runtime Map`, `Component Details > Component Index`, `Usage Examples > Common Change Paths`, `Environment & Dependencies`, `Identified Issues & Improvements`, `Open Questions`
7. **드리프트 갱신 기준 적용**: 각 드리프트 항목을 아래 기준으로 분류한다:
   - `MUST update` — 스펙이 코드와 모순되거나 독자를 오도하는 경우
   - `CONSIDER` — 스펙에 없지만 유용한 정보, 또는 표현 개선이 필요한 경우
   - `NO update` — 코드 변경이 스펙 범위 밖이거나 스펙이 이미 정확한 경우
8. **근거 링크 첨부**: `MUST update` 항목에는 반드시 코드 근거(`path:line`, diff, commit)를 함께 제시한다.

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
   - else auto-generate a descriptive name (do not ask user)
```

**Decision Gate 1→2**:
```
spec_loaded = 스펙 문서 읽기 완료
sources_available = (구현 로그 OR git diff OR 사용자 피드백) 중 하나 이상 존재

IF spec_loaded AND sources_available → Step 2 진행
ELSE IF NOT spec_loaded → AskUserQuestion: 스펙 파일 위치 확인
ELSE IF NOT sources_available → AskUserQuestion: 비교 대상 소스 확인
```

### Step 2: Identify Spec Drift

**Tools**: `Grep`, `Glob`, `Read`, `Bash (git diff)`

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

IF report_presented → 바로 Step 4 진행 (사용자 확인을 기다리지 않는다)
ELSE IF NOT report_presented → Step 3 재실행
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

**Versioning:**
- Increment patch version for minor updates
- Increment minor version for feature changes
- Increment major version for architecture changes

### Step 5: Validate Updates

**Tools**: `Glob`, `Read`, `Grep`, `Bash (git diff)`

Verify updated spec accuracy:

- Cross-reference with code
- Check all file paths exist
- Verify dependency versions
- Confirm API endpoints match
- If local tests/commands are used for verification, apply `_sdd/env.md` setup first
- If `_sdd/env.md` is missing/incomplete, ask the user for environment details instead of guessing

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
6. If `feature_id` is still ambiguous, auto-generate a descriptive name from context (e.g., commit messages, changed file names) without asking the user.

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
| 50-200 파일 | 타겟 탐색 | `Grep`/`Glob`으로 후보 식별 → 타겟 `Read` |
| > 200 파일 | 타겟 탐색 | `Grep`/`Glob` 위주 → 최소한의 `Read` |

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

2. 바로 Step 4 진행 (상세 확인 묻지 않음)
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
- **Ask when uncertain**: Use AskUserQuestion for ambiguities
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
| feature_id 모호 | 컨텍스트에서 자동 생성 (커밋 메시지, 변경 파일명 등 활용) |
| 백업 디렉토리 미존재 | `mkdir -p _sdd/spec/prev/` 자동 생성 |
| 충돌하는 변경 사항 | 최선 판단 후 진행, `DECISION_LOG.md`에 결정 근거 기록. 판단 불가 시 스펙에 Open Questions로 기록 |

## Additional Resources

### Reference Files
- **`references/drift-patterns.md`** - Common drift patterns and solutions
- **`references/update-strategies.md`** - Strategies for different update types

### Example Files
- **`examples/review-report.md`** - Sample review report format
- **`examples/changelog-entry.md`** - Changelog entry examples
