# GitHub CLI (`gh`) Commands Reference

`gh` CLI command reference used by the `pr-spec-patch` skill.

---

## Authentication Check

```bash
gh auth status
```

**Success output example:**
```
github.com
  ✓ Logged in to github.com account username (keyring)
  - Active account: true
  - Git operations protocol: https
  - Token: gho_****
  - Token scopes: 'gist', 'read:org', 'repo', 'workflow'
```

**On failure:**
```
You are not logged into any GitHub hosts. Run gh auth login to authenticate.
```

**Response:** Guide user to run `gh auth login`

---

## PR Auto-Detection

Query the PR number linked to the current branch:

```bash
gh pr view --json number --jq '.number'
```

**Success output:**
```
42
```

**When no PR exists:**
```
no pull requests found for branch "feature/my-branch"
```

**Response:** Request user to provide the PR number directly

---

## PR Metadata Collection

```bash
gh pr view [PR_NUMBER] --json title,body,author,state,url,additions,deletions,changedFiles,headRefName,baseRefName,commits,comments,reviews
```

**JSON field descriptions:**

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | PR title |
| `body` | string | PR description (markdown) |
| `author` | object | Author (`login` field) |
| `state` | string | PR state: `OPEN`, `CLOSED`, `MERGED` |
| `url` | string | PR URL |
| `additions` | number | Lines added |
| `deletions` | number | Lines deleted |
| `changedFiles` | number | Number of changed files |
| `headRefName` | string | Source branch name |
| `baseRefName` | string | Target branch name |
| `commits` | array | Commit list (each with `oid`, `messageHeadline`) |
| `comments` | array | PR comments |
| `reviews` | array | Review list |

**Output example:**
```json
{
  "title": "Implement user authentication system",
  "body": "## Summary\n\nImplement JWT-based authentication system...",
  "author": {
    "login": "developer-kim"
  },
  "state": "OPEN",
  "url": "https://github.com/example/project/pull/42",
  "additions": 847,
  "deletions": 123,
  "changedFiles": 12,
  "headRefName": "feature/auth-system",
  "baseRefName": "main",
  "commits": [
    {
      "oid": "abc1234def5678",
      "messageHeadline": "feat: implement JWT auth service"
    },
    {
      "oid": "def5678ghi9012",
      "messageHeadline": "fix: token refresh bug on session expiry"
    }
  ],
  "comments": [],
  "reviews": []
}
```

---

## PR Diff Collection

### Full Diff

```bash
gh pr diff [PR_NUMBER]
```

**Output:** Standard unified diff format

```diff
diff --git a/src/services/auth_service.py b/src/services/auth_service.py
new file mode 100644
--- /dev/null
+++ b/src/services/auth_service.py
@@ -0,0 +1,145 @@
+import jwt
+from datetime import datetime, timedelta
+...
```

### Changed Files List Only

```bash
gh pr diff [PR_NUMBER] --name-only
```

**Output:**
```
src/services/auth_service.py
src/routes/auth.py
src/middleware/auth.py
src/utils/password.py
src/utils/errors.py
src/models/user.py
src/routes/protected.py
src/services/session_service.py
tests/test_auth_service.py
tests/test_session_service.py
config/settings.py
.env.example
```

---

## Error Handling

### PR Not Found

```bash
gh pr view 999
```

**Output:**
```
GraphQL: Could not resolve to a PullRequest with the number of 999. (repository.pullRequest)
```

**Response:** Request correct PR number

### Not Authenticated

```bash
gh pr view 42
```

**Output:**
```
gh: not logged into any GitHub hosts
```

**Response:** Guide user to run `gh auth login`

### Running Outside a Repository

```bash
gh pr view 42
```

**Output:**
```
could not determine base repo: no git remotes found
```

**Response:** Guide user to run from a GitHub repository directory

---

## Useful Additional Commands

### Extract Specific Fields (jq filters)

```bash
# PR title only
gh pr view 42 --json title --jq '.title'

# Commit message list
gh pr view 42 --json commits --jq '.commits[].messageHeadline'

# HEAD commit SHA
gh pr view 42 --json commits --jq '.commits[-1].oid'
```

### PR Status Check

```bash
# PR status for current branch
gh pr status
```

### View Review Comments

```bash
gh api repos/{owner}/{repo}/pulls/42/comments
```

---

## Tips for Large PRs

When `changedFiles` is 50 or more:

1. Check the file list first with `--name-only`
2. Group by directory to understand change scope
3. Only check diffs for files related to components documented in the spec
4. Selectively check per-file diffs instead of the full diff:

```bash
# Check diff for specific directory only
gh pr diff 42 | grep -A 50 "^diff --git a/src/services/"
```
