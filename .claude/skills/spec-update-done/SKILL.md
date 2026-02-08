---
name: spec-update-done
description: This skill should be used when the user asks to "review spec", "update spec from code", "sync spec with implementation", "spec drift check", "verify spec accuracy", "refresh spec document", "spec needs update", or mentions spec document maintenance, code-to-spec synchronization, or implementation log analysis.
version: 1.0.0
---

# Spec Review and Update

Review and update Software Design Description (SDD) spec documents based on code changes, implementation logs, and user feedback. Ensures spec documents remain accurate and synchronized with the actual codebase.

## Overview

This skill analyzes multiple sources of truth to identify spec drift and generate updates:
- Current spec documents in `_sdd/spec/`
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
| `TEST_SUMMARY.md` | Test results and coverage |
| `user_spec.md` | User requirements and feedback |
| `_sdd/implementation/prev/PREV_*.md` | Historical versions for context |

### 2. Code Changes

- `git diff` - Uncommitted changes
- `git log` - Recent commit history
- `git diff HEAD~N` - Changes over N commits

### 3. Current Spec Documents

- `_sdd/spec/main.md` or `<project-name>.md`
- Component-specific specs
- Any referenced sub-specs

### 4. User Conversation

- Direct feedback and corrections
- New requirements mentioned
- Clarifications on behavior

## Review Process

### Step 1: Gather Context

Collect information from all available sources:

```
1. Read current spec document(s)
2. Read implementation logs:
   - IMPLEMENTATION_PLAN.md (planned work)
   - IMPLEMENTATION_PROGRESS.md (what's done)
   - IMPLEMENTATION_REVIEW.md (issues found)
   - TEST_SUMMARY.md (test status)
3. Analyze code changes:
   - git status (current state)
   - git diff (uncommitted changes)
   - git log --oneline -20 (recent commits)
4. Note user conversation context
```

### Step 2: Identify Spec Drift

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

### Step 4: Apply Updates

Update spec document with identified changes:

**Update Strategy:**
1. Preserve accurate existing content
2. Add new sections/items as needed
3. Update changed information
4. Archive or remove obsolete content
5. Add changelog entry

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

Verify updated spec accuracy:

- Cross-reference with code
- Check all file paths exist
- Verify dependency versions
- Confirm API endpoints match
- Review with user if significant changes

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

### Updated Spec

After user approval, generate updated spec:

1. Create backup(s): for each spec file you will edit, save `prev/PREV_<spec-file>_<timestamp>.md` in `_sdd/spec/prev/` (create the directory first if needed)
2. Apply changes to spec document(s)
3. Update version and last-updated date
4. Add changelog entry (include references to `prev/PREV_...` backup(s), and note if the spec was split into multiple files)

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
- **Cross-reference**: Compare multiple sources

### Preservation

- **Keep history**: Always create `prev/PREV_...` backup under `_sdd/spec/prev/` before updates
- **Preserve context**: Don't remove valuable explanations
- **Maintain structure**: Follow existing spec organization
- **Version control**: Increment version appropriately

### Communication

- **Report before changing**: Show findings before applying updates
- **Highlight breaking changes**: Flag architecture/API changes
- **Ask when uncertain**: Use AskUserQuestion for ambiguities
- **Document decisions**: Note why changes were made

## Integration

### With Implementation Skills

```
create-spec → implementation-plan → implementation → implementation-review → spec-update-done
     ↑                                                                           │
     └───────────────────────────────────────────────────────────────────────────┘
```

### Trigger Points

- After `implementation-review` completes
- When user says "implementation done"
- Before creating new implementation plan
- Periodic maintenance (user-triggered)

## Additional Resources

### Reference Files
- **`references/drift-patterns.md`** - Common drift patterns and solutions
- **`references/update-strategies.md`** - Strategies for different update types

### Example Files
- **`examples/review-report.md`** - Sample review report format
- **`examples/changelog-entry.md`** - Changelog entry examples
