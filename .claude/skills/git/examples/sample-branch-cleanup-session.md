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
📡 Sync:   0 ahead, 0 behind (origin/feature/add-search)
⚠️ Base:   origin/dev에 새 commit 5개; feature commit 3개 재배치 후보

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
   → git rebase origin/dev
   (fetch로 확인한 origin/dev 위로 이미 push된 feature commit 3개 재배치)

2️⃣ Push:
   → git push --force-with-lease origin feature/add-search
   (추가 제안: 게시된 history 변경을 remote에 반영)

위 history rewrite와 force-with-lease push를 각각 승인하시겠습니까? (y/n)
━━━━━━━━━━━━━━━━━━━━━━

User: 둘 다 승인
```

### 3. EXECUTE & REPORT

```
Claude:
[1/2] git rebase origin/dev  ✅ (feature commit 3개 재배치, 충돌 없음)
[2/2] git push --force-with-lease   ✅

✅ Git Actions Complete
━━━━━━━━━━━━━━━━━━━━━━
🌿 Branch: feature/add-search
🔄 Rebased: 3 feature commits onto latest dev (5 new upstream commits)
📡 Pushed to: origin/feature/add-search (force-with-lease)
━━━━━━━━━━━━━━━━━━━━━━
```
