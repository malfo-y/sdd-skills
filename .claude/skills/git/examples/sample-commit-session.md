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
   ?  src/utils/helper.ts — 커밋에 포함하시겠습니까?

3️⃣ Push:
   → git push origin feature/user-auth

Proceed? (y/n/edit)
━━━━━━━━━━━━━━━━━━━━━━

User: y
```

### 3. EXECUTE — 실행

```
Claude:
[1/3] git add src/auth/login.ts src/auth/token.ts src/auth/types.ts
      git commit -m "feat(auth): add JWT login and refresh endpoints"  ✅ [a1b2c3d]
[2/3] git add README.md
      git commit -m "docs(readme): add authentication setup guide"     ✅ [e4f5g6h]
[3/3] git add package.json
      git commit -m "chore(deps): add jsonwebtoken dependency"          ✅ [i7j8k9l]
```

### 4. REPORT — 결과 요약

```
✅ Git Actions Complete
━━━━━━━━━━━━━━━━━━━━━━
🌿 Branch: feature/user-auth
📝 Commits: 3
   • feat(auth): add JWT login and refresh endpoints  [a1b2c3d]
   • docs(readme): add authentication setup guide      [e4f5g6h]
   • chore(deps): add jsonwebtoken dependency           [i7j8k9l]
📡 Pushed to: origin/feature/user-auth
━━━━━━━━━━━━━━━━━━━━━━
```
