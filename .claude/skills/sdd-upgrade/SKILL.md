---
name: sdd-upgrade
description: |
  Update SDD skills plugin from GitHub.
  Pulls latest changes and reports what was updated.
  Trigger: /sdd-skills:sdd-upgrade
user_invocable: true
---

# SDD Skills Upgrade

Pull latest SDD skills from GitHub and report changes.

## Instructions

1. Derive the **plugin root** from this skill's base directory (go up 2 levels — remove `/skills/sdd-upgrade`).
2. Run with Bash (single command):
   ```
   cd "<PLUGIN_ROOT>" && \
   BEFORE=$(git rev-parse --short HEAD) && \
   BRANCH=$(git rev-parse --abbrev-ref HEAD) && \
   REMOTE=$(git remote | head -1) && \
   git fetch "$REMOTE" "$BRANCH" 2>&1 && \
   LOCAL=$(git rev-parse HEAD) && \
   REMOTE_HEAD=$(git rev-parse "$REMOTE/$BRANCH") && \
   if [ "$LOCAL" = "$REMOTE_HEAD" ]; then \
     echo "ALREADY_UP_TO_DATE"; \
     echo "VERSION=$BEFORE"; \
   else \
     git pull "$REMOTE" "$BRANCH" 2>&1 && \
     AFTER=$(git rev-parse --short HEAD) && \
     echo "UPDATED" && \
     echo "BEFORE=$BEFORE" && \
     echo "AFTER=$AFTER" && \
     git log --oneline "$BEFORE".."$AFTER"; \
   fi
   ```
3. **IMPORTANT**: After the Bash tool completes, re-display the key results as markdown text directly in the conversation so the user sees them without expanding the tool output. Format as:

   **If updated:**
   ```
   ## sdd-skills upgrade
   - [x] Pulled latest from GitHub
   - [x] Updated: abc1234 → def5678
   - [x] Changes:
     - def5678 Commit message 1
     - ccc4444 Commit message 2

   **세션을 재시작**해야 새 버전이 적용됩니다.
   ```

   **If already up to date:**
   ```
   ## sdd-skills upgrade
   - [x] Already up to date (abc1234)
   ```

   Use `[x]` for success, `[ ]` for failure. Show actual commit hashes.
   Tell the user to **restart their Claude Code session** to pick up changes.
