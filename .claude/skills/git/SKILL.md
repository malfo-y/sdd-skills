---
name: git
description: Smart Git workflow automation. Use this skill whenever the user says "/git", "커밋해줘", "푸시해줘", "git 정리", "브랜치 만들어", "git status", or any request related to committing, pushing, branching, rebasing, or managing git history. Also trigger when the user mentions messy git history, wants to clean up commits, or asks to push their current work. This skill analyzes staged/unstaged changes, semantically groups them into logical commits with Conventional Commits messages, auto-creates branches when changes are too large, and maintains a clean git graph via rebase.
---

# /git — Smart Git Workflow Skill

One command to handle your entire git workflow: status check, semantic commit grouping, smart branching, push, and graph cleanup.

## Acceptance Criteria
> 진입 시 Shorthand Modes로 요청 범위를 정하고, 종료 전 그 경로에 적용되는 기준만 검증한다.
- [ ] AC1: ASSESS 단계에서 branch, sync, working tree, graph 상태를 모두 파악했다
- [ ] AC2 (commit 생성 시): 변경을 의미 단위로 묶고 Conventional Commits 메시지를 작성했으며, 실제 commit 내용이 승인된 그룹과 일치한다
- [ ] AC3 (mutation 시): 실행 대상·diff 요약·순서를 표시하고, Phase 3에 따라 각 행동의 승인을 확인했다
- [ ] AC4 (mutation 시): 승인된 행동만 실행하고 결과와 기존 변경 보존을 확인했다

## 5-Phase Workflow

```
1. ASSESS  → git status, branch info, remote sync state
2. PLAN    → analyze changes, decide strategy
3. CONFIRM → show the plan to user (diff preview + proposed commits)
4. EXECUTE → commit, branch if needed, rebase if needed, push
5. REPORT  → show result summary
```

> **Hard Rule**: Mutation 전에 구체적인 계획을 표시한다. 행동별 기존 승인 인정과 추가 확인은 Phase 3, 위험 작업의 제한은 [safety-rules.md](references/safety-rules.md)가 소유한다.

---

## Phase 1: ASSESS

수집 명령:

```bash
git branch --show-current
git remote -v
git rev-list --left-right --count HEAD...@{upstream} 2>/dev/null
git status --porcelain=v2 --branch
git log --oneline --graph --all -15
# 진행 중인 rebase/merge 확인
if test -d "$(git rev-parse --git-path rebase-merge)" || test -d "$(git rev-parse --git-path rebase-apply)"; then
  echo "REBASE_IN_PROGRESS"
fi
test -f "$(git rev-parse --git-path MERGE_HEAD)" && echo "MERGE_IN_PROGRESS"
```

파악할 정보: branch(현재/upstream), sync(ahead/behind), working_tree(M/A/D/?), graph_health, in_progress 여부.

status 모드는 로컬 정보만 읽으며 sync는 마지막 fetch 기준임을 표시한다. mutation 계획에 최신 remote 상태가 필요하면 fetch 후 다시 판정하고, 실패·upstream 부재를 clean/synced로 해석하지 않는다. 진행 중인 rebase/merge가 있으면 새 cleanup을 시작하지 않는다. 상태 요청은 보고만 하고, 변경 요청은 기존 작업의 계속/중단 범위를 확인한다.

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

commit 생성 모드에서 `git diff`와 `git diff --cached`의 내용·stat을 확인해 논리 단위로 그룹핑한다. 시작 시 staged/unstaged 구분과 partial staging을 기록해 승인 범위 밖 변경을 보존한다.

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

rebase/pull은 작업트리와 index의 전제조건을 확인한다. dirty라면 승인된 변경을 먼저 commit하거나 필요한 미커밋 변경 전체를 보존·복원하는 순서를 계획에 넣는다. 설정된 autostash를 가정하지 않는다.

> mutation 전에 [safety-rules.md](references/safety-rules.md)를 읽는다. 위 전략은 후보이며 rebase 승인을 대신하지 않는다.

---

## Phase 3: CONFIRM

실행 대상과 순서를 먼저 보여주고 각 행동의 승인을 판정한다.

- 현재 대화에서 해당 대상·범위를 명시적으로 승인했다면 같은 비파괴적 행동을 재확인하지 않는다.
- 활성 goal의 `goal.md`를 Loop Protocol로 읽었다면 `자율 수행 위임`의 사전 승인 목록을 **행동별로** 적용한다. commit 승인만으로 push·rebase를 승인한 것으로 보지 않는다.
- protected branch 작업·force-push·history rewrite·파괴적 작업은 safety 규칙의 금지와 별도 명시적 승인을 적용한다. goal의 “항상 확인” 항목은 사전 위임으로 대체하지 않는다.
- 범위 밖 행동은 제외한다. 요청 완료에 꼭 필요하면 그 행동과 이유만 질문하고, 이미 승인된 독립 작업은 진행한다. 계획이 바뀌면 변경분의 승인도 다시 판정한다.

```
🔄 Proposed Git Actions
━━━━━━━━━━━━━━━━━━━━━━
1️⃣ Create branch: feature/add-user-auth
2️⃣ Commits (3):
   ┌─ feat(auth): add JWT login and refresh endpoints
   │  src/auth/login.ts, src/auth/token.ts, src/auth/types.ts
   ├─ docs(readme): add authentication setup guide
   │  README.md
   └─ chore(deps): add jsonwebtoken dependency
      package.json
3️⃣ Graph cleanup: git rebase origin/main (commit 후 clean 상태에서 실행)
4️⃣ Push: git push -u origin feature/add-user-auth

Proceed? (y/n/edit)
━━━━━━━━━━━━━━━━━━━━━━
```

각 커밋 그룹에 대해 condensed diff preview (`+lines, -lines`, 주요 함수명) 포함.

---

## Phase 4: EXECUTE

승인된 계획의 전제조건과 순서대로 실행한다. 아래 항목은 필요한 행동에만 적용한다.

1. 기존 변경·index를 보존하고 필요한 브랜치를 생성한다. 보존/복원은 safety reference의 Stash Safety를 따른다.
2. 각 commit 직전에 index가 **현재 승인 그룹의 파일·hunk만** 포함하는지 `git diff --cached`로 확인한다. 다른 그룹이 이미 staged되어 있으면 작업트리 내용을 버리지 않고 분리한다. partial staging은 `git add -p` 등을 사용하며, hunk 경계가 모호하면 그룹 계획을 조정한다. 전체 파일을 임의로 끼워 넣지 않는다.
3. `git commit` 후 실제 commit diff를 계획과 대조한다. 남은 그룹의 staging과 이번 commit에 포함되지 않은 사용자 staging을 보존·복원한다.
4. 계획한 pull/rebase는 clean 전제조건이 충족된 시점에만 실행한다. 실패·충돌 시 후속 push를 중단한다.
5. 이번 작업에서 보존한 변경을 복원하고 파일·index 상태를 확인한다. 승인된 push가 있으면 로컬 작업 성공 후 실행하고 remote sync 결과를 확인한다.

### Conflict Resolution

[safety-rules.md의 Conflict Resolution](references/safety-rules.md#conflict-resolution)을 따른다. 해결 후 해당 작업을 계속하고 결과를 검증한 뒤 남은 승인 작업으로 돌아간다. 미해결이면 완료로 보고하지 않는다.

---

## Phase 5: REPORT

```
✅ Git Actions Complete
━━━━━━━━━━━━━━━━━━━━━━
🌿 Branch: feature/add-user-auth (new)
📝 Commits: 3
   • feat(auth): add JWT login and refresh endpoints  [a1b2c3d]
   • docs(readme): add authentication setup guide      [e4f5a6b]
   • chore(deps): add jsonwebtoken dependency           [c7d8e9f]
📡 Pushed to: origin/feature/add-user-auth
━━━━━━━━━━━━━━━━━━━━━━
```

---

## Edge Cases

| 상황 | 처리 |
|------|------|
| Protected branch (main/master/develop/release/*) | force-push 금지, 대안 제시 |
| Empty working tree | clean 사실을 표시하되 ahead commit의 push·graph 정리·브랜치 작업이 남으면 계속한다. 요청 작업이 없을 때만 종료 |
| Untracked files | 분석 포함. build artifact면 `.gitignore` 제안 |
| Large binary (>1MB) | 경고, git-lfs 제안 |
| Detached HEAD | 경고, 브랜치 생성 권유 |
| Stash 대상 | 커밋 그룹에 안 맞는 변경은 stash 제안 |

---

## Shorthand Modes

| Command | Behavior |
|---------|----------|
| `/git`, `/git status` | Phase 1 only (dashboard) |
| `/git commit`, "커밋해줘" | Phase 1–5 중 commit 생성에 필요한 단계. push는 별도 요청/승인 시만 |
| `/git push`, "푸시해줘" | sync 확인 → push 계획·승인 판정 → 실행·보고. 새 commit은 만들지 않음 |
| `/git cleanup`, "git 정리" | graph cleanup 계획·별도 승인 → 실행·보고. push는 별도 요청/승인 시만 |
| `/git branch <name>` | Create branch, move uncommitted changes |
| `/git all` | 전체 변경 분석 → 그룹 계획·승인 판정 → 그룹별 stage/commit → push |

## Final Check

선택한 모드의 AC만 검증한다. 복구 가능한 누락은 보완한다. 외부 실패·승인 대기·미해결 충돌은 완료한 행동과 남은 작업을 구분해 보고하며, 원인이 바뀌지 않은 실패를 반복하지 않는다. 이미 발생한 승인·보존 위반을 소급 충족으로 표시하지 않는다.

