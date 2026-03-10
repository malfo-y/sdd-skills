---
name: git
description: Smart Git workflow automation. Use this skill whenever the user says "/git", "커밋해줘", "푸시해줘", "git 정리", "브랜치 만들어", "git status", or any request related to committing, pushing, branching, rebasing, or managing git history. Also trigger when the user mentions messy git history, wants to clean up commits, or asks to push their current work. This skill analyzes staged/unstaged changes, semantically groups them into logical commits with Conventional Commits messages, auto-creates branches when changes are too large, and maintains a clean git graph via rebase.
version: 1.0.0
---

# /git — Smart Git Workflow Skill

One command to handle your entire git workflow: status check, semantic commit grouping, smart branching, push, and graph cleanup.

## Quick Reference

When the user invokes `/git` (or any git-related request), follow this sequence:

```
1. ASSESS  → git status, branch info, remote sync state
2. PLAN    → analyze changes, decide strategy
3. CONFIRM → show the plan to user (diff preview + proposed commits)
4. EXECUTE → commit, branch if needed, rebase if needed, push
5. REPORT  → show result summary
```

Always show the plan and get confirmation before executing. Never auto-push without the user seeing what will happen.

---

## Phase 1: ASSESS — Understand the Current State

Run these commands and collect the results:

```bash
# Current branch and tracking info
git branch --show-current
git remote -v

# Sync state with remote
git fetch --quiet 2>/dev/null

# Divergence check: how far ahead/behind from remote
git rev-list --left-right --count HEAD...@{upstream} 2>/dev/null

# Status of working tree
git status --porcelain=v2 --branch

# Recent log for graph context (compact)
git log --oneline --graph --all -15

# Check for ongoing rebase/merge
test -d .git/rebase-merge || test -d .git/rebase-apply && echo "REBASE_IN_PROGRESS"
test -f .git/MERGE_HEAD && echo "MERGE_IN_PROGRESS"
```

Build a mental model from this:
- **branch**: current branch name and its upstream
- **sync**: commits ahead/behind remote
- **working_tree**: list of modified/added/deleted/untracked files with their paths
- **graph_health**: is the graph clean, or is there divergence/merge commits that need cleanup?
- **in_progress**: any ongoing rebase or merge?

### Status Dashboard

Present the assessment as a concise dashboard:

```
📊 Git Status Dashboard
━━━━━━━━━━━━━━━━━━━━━━
🌿 Branch: feature/user-auth → origin/feature/user-auth
📡 Sync:   2 ahead, 0 behind  ✅
⚠️ Graph:  clean

📁 Changes:
  Staged (3):
    M  src/auth/login.ts
    M  src/auth/token.ts
    A  src/auth/types.ts
  Unstaged (2):
    M  README.md
    M  package.json
  Untracked (1):
    ?  src/utils/helper.ts
━━━━━━━━━━━━━━━━━━━━━━
```

Indicators: 📡 Sync → ✅ in sync, ⚠️ behind, 🔄 diverged. Graph → ✅ clean, ⚠️ messy.

---

## Phase 2: PLAN — Analyze and Decide Strategy

### 2a. Semantic Change Grouping

Examine ALL changed files (staged + unstaged) and their diffs:

```bash
git diff --stat
git diff --cached --stat
git diff HEAD --   # individual file content when needed
```

Group changes into **logical commit units** by:
- **Directory proximity**: files in the same module/feature folder belong together
- **Functional relationship**: component + test + types = one commit
- **Nature of change**: separate refactors from features from fixes from config
- **File type patterns**: migrations together, config files may be separate

Each group gets a Conventional Commits message.

**Format**: `<type>(<scope>): <description>`

**Types**:
- `feat` — new feature or capability
- `fix` — bug fix
- `refactor` — code restructuring without behavior change
- `style` — formatting, whitespace, linting
- `docs` — documentation only
- `test` — adding or updating tests
- `chore` — build, deps, config, CI changes
- `perf` — performance improvement

**Scope**: derive from the primary directory or module (e.g., `auth`, `api`, `ui`, `db`)

**Description**: imperative mood, lowercase, no period, under 50 chars. Be specific.

**Examples:**
```
feat(auth): add JWT token refresh endpoint
fix(ui): resolve dropdown z-index overlap on mobile
refactor(api): extract validation logic into middleware
chore(deps): bump express from 4.18 to 4.21
test(auth): add integration tests for login flow
```

For breaking changes, add a body:
```
feat(api)!: migrate to v2 authentication scheme

BREAKING CHANGE: /auth/login now requires `client_id` parameter.
```

### 2b. Smart Branching Decision

**Create a new branch when ANY of these are true:**
- Current branch is `main`/`master`/`develop`/`release/*` AND changes are feature-level
- Total diff exceeds ~300 lines across 10+ files
- Changes span 3+ unrelated modules
- Work is clearly a new feature area unrelated to recent branch commits

**Branch naming**: `<type>/<short-description>`
- `feature/add-user-auth`
- `fix/dropdown-overlap`
- `refactor/extract-api-middleware`

**Stay on current branch when:**
- Already on a matching feature/fix branch
- Changes are small fixes or continuations
- Protected branch but changes are docs/config only

### 2c. Graph Cleanup Decision

**Rebase when:**
- Behind remote (new upstream commits after fetch)
- Unnecessary merge commits that could be linearized
- Tangled graph visible in `git log --graph`

**Strategy:**
- Behind, no local commits → `git pull --ff-only`
- Behind, with local commits → `git pull --rebase`
- Messy graph, on feature branch → `git rebase <base-branch>`
- Never force-rebase `main`/`master`/`develop`

---

## Phase 3: CONFIRM — Show the Plan

Present the full plan before executing. Never skip this.

```
🔄 Proposed Git Actions
━━━━━━━━━━━━━━━━━━━━━━

1️⃣ Graph cleanup:
   → git pull --rebase (2 commits behind origin/main)

2️⃣ Create branch:
   → git checkout -b feature/add-user-auth
   (reason: significant feature changes on main branch)

3️⃣ Commits (3):
   ┌─ feat(auth): add JWT login and refresh endpoints
   │  src/auth/login.ts, src/auth/token.ts, src/auth/types.ts
   ├─ docs(readme): add authentication setup guide
   │  README.md
   └─ chore(deps): add jsonwebtoken dependency
      package.json, package-lock.json

4️⃣ Push:
   → git push -u origin feature/add-user-auth

Proceed? (y/n/edit)
━━━━━━━━━━━━━━━━━━━━━━
```

### Diff Preview

Show a condensed diff preview per commit group:

```
📝 Diff Preview: feat(auth): add JWT login and refresh endpoints
━━━━━━━━━━━━━━━━━━━━━━
src/auth/login.ts  (+45, -3)  — new loginUser() and validateCredentials()
src/auth/token.ts  (+28, -0)  — new refreshToken() and generatePair()
src/auth/types.ts  (+15, -0)  — AuthPayload, TokenPair interfaces
━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 4: EXECUTE — Run the Plan

After user confirmation, execute step by step with error handling.

### Execution Order

```
1. Stash unrelated changes if needed
2. Graph cleanup (pull/rebase) if planned
3. Create new branch if planned
4. For each commit group:
   a. Stage the files: git add <files>
   b. Commit: git commit -m "<message>"
5. Push: git push [-u origin <branch>]
6. Pop stash if we stashed
```

### Staging Strategy for Multiple Commits

```bash
# Reset everything to unstaged first
git reset HEAD -- .

# Stage and commit each group separately
git add src/auth/login.ts src/auth/token.ts src/auth/types.ts
git commit -m "feat(auth): add JWT login and refresh endpoints"

git add README.md
git commit -m "docs(readme): add authentication setup guide"

git add package.json package-lock.json
git commit -m "chore(deps): add jsonwebtoken dependency"
```

For partial file staging, use `git add -p <file>`. If hunk boundaries are ambiguous, commit the whole file in the most relevant group.

### Conflict Resolution

If rebase/pull produces conflicts:

1. List conflicts: `git diff --name-only --diff-filter=U`
2. Examine each file's conflict markers
3. **Auto-resolve** if straightforward:
   - Only one side has meaningful changes → take that side
   - Both sides changed different sections → merge both
   - Same lines changed → present to user
4. After resolving: `git add <file>` then `git rebase --continue`
5. If ambiguous, show the conflict and ask:
```
⚠️ Conflict in src/auth/login.ts
Which version? (ours / theirs / both / manual)
```

---

## Phase 5: REPORT — Show Results

```
✅ Git Actions Complete
━━━━━━━━━━━━━━━━━━━━━━
🌿 Branch: feature/add-user-auth (new)
📝 Commits: 3
   • feat(auth): add JWT login and refresh endpoints  [a1b2c3d]
   • docs(readme): add authentication setup guide      [e4f5g6h]
   • chore(deps): add jsonwebtoken dependency           [i7j8k9l]
📡 Pushed to: origin/feature/add-user-auth
�� Rebased: 2 commits from origin/main applied cleanly
━━━━━━━━━━━━━━━━━━━━━━
```

---

## Edge Cases and Safety

### Protected Branches
Never force-push to `main`, `master`, `develop`, or `release/*`. Warn and suggest alternatives.

### Empty Working Tree
```
✅ Working tree clean — nothing to commit.
📡 Branch: main (in sync with origin/main)
```

### Untracked Files
Include in analysis. If they look like build artifacts (`dist/`, `*.pyc`, `node_modules/`), suggest `.gitignore` instead.

### Large Binary Files
Warn if binary file > 1MB. Suggest git-lfs if appropriate.

### Detached HEAD
Warn and suggest creating a branch before committing.

### Stash Handling
If uncommitted changes don't fit any commit group:
```
📦 Stash these unrelated files?
   M  scratch/notes.txt
   ?  tmp/debug.log
```

---

## Shorthand Modes

| Command | Behavior |
|---------|----------|
| `/git` or `/git status` | Phase 1 only — show dashboard |
| `/git commit` or "커밋해줘" | Full workflow (Phases 1–5) |
| `/git push` or "푸시해줘" | Check sync + push (skip commit if clean) |
| `/git cleanup` or "git 정리" | Graph cleanup focus (rebase, linearize) |
| `/git branch <name>` | Create branch, move uncommitted changes |
| `/git all` | Stage all → group → commit → push (still confirms) |
