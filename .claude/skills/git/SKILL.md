---
name: git
description: Smart Git workflow automation. Use this skill whenever the user says "/git", "커밋해줘", "푸시해줘", "git 정리", "브랜치 만들어", "git status", or any request related to committing, pushing, branching, rebasing, or managing git history. Also trigger when the user mentions messy git history, wants to clean up commits, or asks to push their current work. This skill analyzes staged/unstaged changes, semantically groups them into logical commits with Conventional Commits messages, auto-creates branches when changes are too large, and maintains a clean git graph via rebase.
version: 1.0.0
---

# /git — Smart Git Workflow Skill

One command to handle your entire git workflow: status check, semantic commit grouping, smart branching, push, and graph cleanup.

## Acceptance Criteria
> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.
- [ ] AC1: ASSESS 단계에서 branch, sync, working tree, graph 상태를 모두 파악했다
- [ ] AC2: 변경사항을 의미 단위로 semantic grouping 하고, 각 그룹에 Conventional Commits 형식 메시지를 작성했다
- [ ] AC3: CONFIRM 단계에서 커밋 그룹, diff 요약, 브랜치/push 계획을 사용자에게 보여주고 승인을 받았다
- [ ] AC4: 사용자 확인 없이 push/commit/rebase를 실행하지 않았다

## 5-Phase Workflow

```
1. ASSESS  → git status, branch info, remote sync state
2. PLAN    → analyze changes, decide strategy
3. CONFIRM → show the plan to user (diff preview + proposed commits)
4. EXECUTE → commit, branch if needed, rebase if needed, push
5. REPORT  → show result summary
```

> **Hard Rule**: Always show the plan and get confirmation before executing. Never auto-push without the user seeing what will happen.

---

## Phase 1: ASSESS

수집 명령:

```bash
git branch --show-current
git remote -v
git fetch --quiet 2>/dev/null
git rev-list --left-right --count HEAD...@{upstream} 2>/dev/null
git status --porcelain=v2 --branch
git log --oneline --graph --all -15
# 진행 중인 rebase/merge 확인
test -d .git/rebase-merge || test -d .git/rebase-apply && echo "REBASE_IN_PROGRESS"
test -f .git/MERGE_HEAD && echo "MERGE_IN_PROGRESS"
```

파악할 정보: branch(현재/upstream), sync(ahead/behind), working_tree(M/A/D/?), graph_health, in_progress 여부.

결과를 Status Dashboard로 요약 표시:

```
📊 Git Status Dashboard
━━━━━━━━━━━━━━━━━━━━━━
🌿 Branch: feature/user-auth → origin/feature/user-auth
📡 Sync:   2 ahead, 0 behind  ✅
📁 Changes:
  Staged (3):   M src/auth/login.ts, M src/auth/token.ts, A src/auth/types.ts
  Unstaged (2): M README.md, M package.json
  Untracked (1): ? src/utils/helper.ts
━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 2: PLAN

### 2a. Semantic Change Grouping

`git diff --stat`, `git diff --cached --stat`으로 전체 변경 파악 후 논리 단위로 그룹핑.

| 기준 | 설명 |
|------|------|
| Directory proximity | 같은 모듈/폴더의 파일 |
| Functional relationship | component + test + types = 하나 |
| Nature of change | refactor / feature / fix / config 분리 |

각 그룹에 Conventional Commits 메시지 부여: `<type>(<scope>): <description>`

> 상세 type 목록 및 grouping 전략: `references/conventional-commits.md`, `references/semantic-grouping.md` 참조

### 2b. Smart Branching Decision

| 조건 | 행동 |
|------|------|
| main/master/develop에서 feature 수준 변경 | 새 브랜치 생성 |
| diff 300줄+ / 10+ 파일 / 3+ 무관 모듈 | 새 브랜치 생성 |
| 이미 맞는 feature/fix 브랜치 | 현재 브랜치 유지 |
| 소규모 수정·docs/config만 | 현재 브랜치 유지 |

브랜치명: `<type>/<short-description>` (예: `feature/add-user-auth`, `fix/dropdown-overlap`)

### 2c. Graph Cleanup Decision

| 상황 | 전략 |
|------|------|
| Behind, no local commits | `git pull --ff-only` |
| Behind, with local commits | `git pull --rebase` |
| Messy graph, feature branch | `git rebase <base-branch>` |
| main/master/develop | **절대 force-rebase 금지** |

> 안전 규칙 상세: `references/safety-rules.md` 참조

---

## Phase 3: CONFIRM

실행 전 반드시 전체 계획을 보여주고 승인받는다. **절대 생략 불가.**

```
🔄 Proposed Git Actions
━━━━━━━━━━━━━━━━━━━━━━
1️⃣ Graph cleanup: git pull --rebase (2 commits behind)
2️⃣ Create branch: feature/add-user-auth
3️⃣ Commits (3):
   ┌─ feat(auth): add JWT login and refresh endpoints
   │  src/auth/login.ts, src/auth/token.ts, src/auth/types.ts
   ├─ docs(readme): add authentication setup guide
   │  README.md
   └─ chore(deps): add jsonwebtoken dependency
      package.json
4️⃣ Push: git push -u origin feature/add-user-auth

Proceed? (y/n/edit)
━━━━━━━━━━━━━━━━━━━━━━
```

각 커밋 그룹에 대해 condensed diff preview (`+lines, -lines`, 주요 함수명) 포함.

---

## Phase 4: EXECUTE

사용자 승인 후 순서대로 실행:

```
1. 관련 없는 변경 stash (필요시)
2. Graph cleanup (pull/rebase)
3. 새 브랜치 생성 (필요시)
4. 각 커밋 그룹별:
   a. git add <files>
   b. git commit -m "<message>"
5. git push [-u origin <branch>]
6. Stash pop (필요시)
```

부분 파일 스테이징: `git add -p <file>`. Hunk 경계 모호하면 전체 파일을 가장 관련 높은 그룹에 커밋.

### Conflict Resolution

1. `git diff --name-only --diff-filter=U`로 충돌 목록
2. 한쪽만 의미 있는 변경 → 해당 쪽 채택 / 다른 섹션 변경 → 양쪽 병합
3. 같은 줄 변경 → 사용자에게 제시: `⚠️ Conflict in <file> — Which version? (ours / theirs / both / manual)`

---

## Phase 5: REPORT

```
✅ Git Actions Complete
━━━━━━━━━━━━━━━━━━━━━━
🌿 Branch: feature/add-user-auth (new)
📝 Commits: 3
   • feat(auth): add JWT login and refresh endpoints  [a1b2c3d]
   • docs(readme): add authentication setup guide      [e4f5g6h]
   • chore(deps): add jsonwebtoken dependency           [i7j8k9l]
📡 Pushed to: origin/feature/add-user-auth
━━━━━━━━━━━━━━━━━━━━━━
```

---

## Edge Cases

| 상황 | 처리 |
|------|------|
| Protected branch (main/master/develop/release/*) | force-push 금지, 대안 제시 |
| Empty working tree | `✅ Working tree clean` 표시, 종료 |
| Untracked files | 분석 포함. build artifact면 `.gitignore` 제안 |
| Large binary (>1MB) | 경고, git-lfs 제안 |
| Detached HEAD | 경고, 브랜치 생성 권유 |
| Stash 대상 | 커밋 그룹에 안 맞는 변경은 stash 제안 |

---

## Shorthand Modes

| Command | Behavior |
|---------|----------|
| `/git`, `/git status` | Phase 1 only (dashboard) |
| `/git commit`, "커밋해줘" | Full workflow (Phase 1-5) |
| `/git push`, "푸시해줘" | Check sync + push |
| `/git cleanup`, "git 정리" | Graph cleanup (rebase, linearize) |
| `/git branch <name>` | Create branch, move uncommitted changes |
| `/git all` | Stage all → group → commit → push (confirms first) |

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

