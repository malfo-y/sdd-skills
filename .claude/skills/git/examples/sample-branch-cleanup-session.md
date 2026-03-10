# Sample Session: /git cleanup

그래프 정리 (rebase) 중심의 예제.

## Session Flow

### 1. ASSESS

```
User: /git cleanup

Claude:
📊 Git Status Dashboard
━━━━━━━━━━━━━━━━━━━━━━
🌿 Branch: feature/add-search → origin/feature/add-search
📡 Sync:   3 ahead, 5 behind  🔄
⚠️ Graph:  diverged (rebase recommended)

📁 Changes:
  Staged: none
  Unstaged: none
  Untracked: none
━━━━━━━━━━━━━━━━━━━━━━
```

### 2. CONFIRM

```
Claude:
🔄 Proposed Git Actions
━━━━━━━━━━━━━━━━━━━━━━

1️⃣ Graph cleanup:
   → git pull --rebase origin dev
   (5 commits behind, 3 local commits → rebase onto latest dev)

2️⃣ Push:
   → git push --force-with-lease origin feature/add-search
   (rebase 후 force push 필요)

Proceed? (y/n)
━━━━━━━━━━━━━━━━━━━━━━

User: y
```

### 3. EXECUTE & REPORT

```
Claude:
[1/2] git pull --rebase origin dev  ✅ (5 commits applied, no conflicts)
[2/2] git push --force-with-lease   ✅

✅ Git Actions Complete
━━━━━━━━━━━━━━━━━━━━━━
🌿 Branch: feature/add-search
🔄 Rebased: 3 local commits onto latest dev (5 new upstream commits)
📡 Pushed to: origin/feature/add-search (force-with-lease)
━━━━━━━━━━━━━━━━━━━━━━
```
