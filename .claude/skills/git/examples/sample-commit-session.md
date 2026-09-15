# Sample Session: /git commit

여러 파일 변경사항을 시맨틱 커밋으로 자동 그룹핑하는 예제.

## Session Flow

### 1. ASSESS — 상태 확인

```
User: /git commit

Claude:
📊 Git Status Dashboard
━━━━━━━━━━━━━━━━━━━━━━
🌿 Branch: feature/user-auth → origin/feature/user-auth
📡 Sync:   2 ahead, 0 behind  ✅
📈 Graph:  clean

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

### 2. PLAN & CONFIRM — 시맨틱 그룹핑 + 계획 제시

```
Claude:
🔄 Proposed Git Actions
━━━━━━━━━━━━━━━━━━━━━━

1️⃣ Commits (3):
   ┌─ feat(auth): add JWT login and refresh endpoints
   │  src/auth/login.ts (+45, -3), src/auth/token.ts (+28, -0), src/auth/types.ts (+15, -0)
   ├─ docs(readme): add authentication setup guide
   │  README.md (+12, -0)
   └─ chore(deps): add jsonwebtoken dependency
      package.json (+2, -1)

2️⃣ Untracked (skip):
   ?  src/utils/helper.ts — 이번 commit 대상에서 제외하고 보존

Proceed? (y/n/edit)
━━━━━━━━━━━━━━━━━━━━━━

User: y
```

### 3. EXECUTE — 실행

```
Claude:
[1/3] 기존 staging을 기록하고, index가 auth 그룹만 포함하는지 diff 확인
      git add src/auth/login.ts src/auth/token.ts src/auth/types.ts
      git commit -m "feat(auth): add JWT login and refresh endpoints"  ✅ [a1b2c3d]
[2/3] git add README.md → index가 README 그룹만 포함하는지 diff 확인
      git commit -m "docs(readme): add authentication setup guide"     ✅ [e4f5a6b]
[3/3] git add package.json → index가 deps 그룹만 포함하는지 diff 확인
      git commit -m "chore(deps): add jsonwebtoken dependency"          ✅ [c7d8e9f]
```

### 4. REPORT — 결과 요약

```
✅ Git Actions Complete
━━━━━━━━━━━━━━━━━━━━━━
🌿 Branch: feature/user-auth
📝 Commits: 3
   • feat(auth): add JWT login and refresh endpoints  [a1b2c3d]
   • docs(readme): add authentication setup guide      [e4f5a6b]
   • chore(deps): add jsonwebtoken dependency           [c7d8e9f]
📡 Push: 요청 없음 — 실행하지 않음
📁 Preserved: src/utils/helper.ts (untracked)
━━━━━━━━━━━━━━━━━━━━━━
```
