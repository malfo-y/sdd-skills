---
name: git
description: Smart Git workflow automation. Use this skill whenever the user says "/git", "커밋해줘", "푸시해줘", "git 정리", "브랜치 만들어", "git status", or any request related to committing, pushing, branching, rebasing, or managing git history. Also trigger when the user mentions messy git history, wants to clean up commits, or asks to push their current work. This skill analyzes staged/unstaged changes, semantically groups them into logical commits with Conventional Commits messages, auto-creates branches when changes are too large, and maintains a clean git graph via rebase.
---

# /git

요청받은 git 작업(상태 확인, 커밋, 브랜치, push, 그래프 정리)을 한다. 변경은 의미 단위로 묶어 Conventional Commits 메시지로 커밋하고, 승인된 행동만 실행한다.

## Acceptance Criteria

> `호출 범위`로 요청 범위를 정하고, 그 범위에 해당하는 기준만 점검한다.

- [ ] AC1: 브랜치, 원격과의 차이, 작업 폴더, 진행 중인 rebase·merge 상태를 파악했다.
- [ ] AC2 (커밋할 때): 변경을 의미 단위로 묶어 Conventional Commits 메시지를 썼고, 실제 커밋 내용이 승인된 묶음과 같다.
- [ ] AC3 (저장소를 바꿀 때): 실행 대상과 순서를 먼저 보여 줬고, `승인`대로 행동마다 승인을 확인했다.
- [ ] AC4 (저장소를 바꿀 때): 승인된 행동만 실행했고, 결과와 기존 변경의 보존을 확인했다.

## 호출 범위

| 호출 | 하는 일 |
|---|---|
| `/git`, `/git status` | 상태만 보고한다. |
| `/git commit`, "커밋해줘" | 커밋까지 한다. push는 따로 요청하거나 승인했을 때만 한다. |
| `/git push`, "푸시해줘" | 원격과의 차이를 확인하고 push한다. 새 커밋은 만들지 않는다. |
| `/git cleanup`, "git 정리" | 그래프 정리를 계획하고 따로 승인받아 실행한다. push는 따로 요청하거나 승인했을 때만 한다. |
| `/git branch <name>` | 브랜치를 만들고 미커밋 변경을 그대로 옮긴다. |
| `/git all` | 전체 변경을 묶어 커밋하고 push한다. |

## 상태 파악

- 브랜치와 upstream, ahead/behind, staged·unstaged·untracked, 진행 중인 rebase·merge를 본다.
- 원격과의 차이는 마지막 fetch 기준이다. 상태만 보고할 때는 그 사실을 함께 적는다. 저장소를 바꾸는 계획에 원격의 최신 상태가 필요하면 fetch한 뒤 다시 판정한다. fetch 실패나 upstream 없음을 "동기화됨"으로 읽지 않는다.
- rebase·merge가 진행 중이면 새 정리를 시작하지 않는다. 상태 요청이면 보고만 하고, 변경 요청이면 기존 작업을 이어 갈지 중단할지 확인한다.
- 작업 폴더가 깨끗해도 push할 커밋이나 요청받은 브랜치·정리 작업이 남아 있으면 계속한다.

## 계획

- **커밋 묶기**: 한 기능을 이루는 파일(구현, 테스트, 타입)은 한 커밋으로 묶는다. 성격이 다른 변경(기능, 수정, 리팩터링, 문서, 설정)은 나눈다. 한 파일에 성격이 다른 변경이 섞여 있으면 hunk 단위로 나눈다. 시작할 때 staged와 unstaged의 구분을 적어 두고, 승인 범위 밖 변경은 보존한다.
- **메시지**: `<type>(<scope>): <description>`. description은 명령형, 소문자 시작, 마침표 없음, 50자 이내다. 호환을 깨는 변경은 type 뒤에 `!`를 붙이고 `BREAKING CHANGE:` footer를 쓴다.
- **브랜치**: 브랜치 이름은 `<type>/<short-description>`이다.

  | 조건 | 행동 |
  |---|---|
  | main/master/develop에서 기능 수준 변경 | 새 브랜치 |
  | diff 300줄 이상, 파일 10개 이상, 무관한 모듈 3개 이상 | 새 브랜치 |
  | 이미 맞는 feature/fix 브랜치 | 현재 브랜치 유지 |
  | 작은 수정, 문서·설정만 | 현재 브랜치 유지 |

- **동기화와 정리**: 뒤처졌고 로컬 커밋이 없으면 `git pull --ff-only`, 로컬 커밋이 있으면 `git pull --rebase`, feature 브랜치의 그래프 정리는 `git rebase <base-branch>`다. pull·rebase 전에 작업 폴더와 index가 깨끗한지 본다. 깨끗하지 않으면 승인된 변경을 먼저 커밋하거나, 미커밋 변경을 보존하고 복원하는 순서를 계획에 넣는다. autostash 설정을 가정하지 않는다.

## 승인

저장소를 바꾸기 전에 실행 대상, 순서, 커밋별 파일과 diff 요약을 보여 주고, 행동마다 승인을 판정한다.

- 이 대화에서 그 대상과 범위를 명시적으로 승인받았으면 같은 비파괴 행동을 다시 묻지 않는다.
- 활성 goal의 `goal.md`를 Loop Protocol로 읽었으면 `자율 수행 위임`의 사전 승인 목록을 **행동별로** 적용한다. 커밋 승인을 push나 rebase의 승인으로 보지 않는다.
- 보호 브랜치 작업, force-push, 이력 재작성, 파괴적 작업은 `안전 규칙`의 금지와 별도의 명시적 승인을 적용한다. goal의 "항상 확인" 항목은 사전 위임으로 대신하지 않는다.
- 범위 밖 행동은 뺀다. 요청을 끝내는 데 꼭 필요하면 그 행동과 이유만 묻고, 이미 승인된 독립 작업은 진행한다. 계획이 바뀌면 바뀐 부분의 승인을 다시 판정한다.

## 실행

1. 기존 변경과 index를 보존하고 필요한 브랜치를 만든다.
2. 커밋 직전에 `git diff --cached`로 index가 **지금 승인된 묶음의 파일과 hunk만** 담는지 확인한다. 다른 묶음이 이미 staged면 작업 폴더 내용을 버리지 않고 분리한다. 부분 staging은 `git add -p` 같은 방법을 쓰고, hunk 경계가 모호하면 묶음 계획을 고쳐 다시 승인받는다.
3. 커밋한 뒤 실제 커밋 diff를 계획과 대조한다. 남은 묶음의 staging과, 이번 커밋에 넣지 않은 사용자의 staging을 보존한다.
4. pull·rebase는 깨끗한 상태에서만 실행한다. 실패하거나 충돌하면 뒤따르는 push를 멈춘다.
5. 보존해 둔 변경을 복원하고 파일과 index 상태를 확인한다. 승인된 push는 로컬 작업이 성공한 뒤에 실행하고 원격 반영을 확인한다.

끝나면 만든 브랜치, 커밋(해시와 메시지), push 결과, 남은 작업을 보고한다.

## 안전 규칙

- **보호 브랜치**(`main`, `master`, `develop`, `dev`, `release/*`)에는 force-push와 force-rebase를 하지 않는다. 승인이 있어도 하지 않고 대안을 제시한다.
- **force-push**는 `--force-with-lease`만 쓴다(`--force` 금지). feature/fix 브랜치에서 rebase한 뒤에만, 사용자 확인을 받고 쓴다.
- **파괴적 명령**(`git reset --hard`, `git checkout -- .`, `git clean -f`, `git branch -D`)은 사용자 확인 없이 실행하지 않는다.
- **충돌**: `git diff --name-only --diff-filter=U`로 목록을 본다. 한쪽에만 의미 있는 변경이 있으면 그쪽을 고르고, 양쪽이 다른 부분을 바꿨으면 둘 다 살린다. 같은 줄을 바꿨으면 사용자에게 보여 주고 묻는다. 해결한 뒤 그 작업을 이어 가고 결과를 확인한다. 해결하지 못했으면 완료로 보고하지 않는다.
- **stash**: 작업을 막는 미커밋 변경만 보존한다. stash를 쓰면 기존 stash와 구분할 식별자, 대상, staged·unstaged 상태를 적어 두고, 필요한 untracked 파일도 포함한다. 이번에 만든 stash만 복원하고, 파일과 index가 보존됐는지 확인한 뒤 지운다. 충돌하거나 실패하면 stash를 남겨 두고 뒤따르는 push를 멈춘다. 기존 stash와 승인 범위 밖 변경은 지우지 않는다.
- **detached HEAD**에서는 커밋 전에 브랜치 생성을 제안한다.
- **큰 파일**: 1MB를 넘는 바이너리는 git-lfs를 제안한다. `node_modules/`, `dist/`, `*.pyc` 같은 빌드 산출물은 `.gitignore`를 제안한다.

## Final Check

요청 범위에 해당하는 Acceptance Criteria만 점검한다. 보완할 수 있는 누락은 고친다. 외부 실패, 승인 대기, 풀지 못한 충돌은 끝낸 행동과 남은 작업을 나눠 보고하고, 원인이 그대로인 실패를 반복하지 않는다. 이미 일어난 승인·보존 위반을 나중에 충족된 것으로 적지 않는다.
