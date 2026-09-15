# Git Safety Rules

안전한 Git 작업을 위한 규칙 모음.

## Protected Branches

다음 브랜치에는 절대 force-push 하지 않는다:
- `main`, `master`
- `develop`, `dev`
- `release/*`

## Force Push

- `--force-with-lease`만 사용 (절대 `--force` 사용 금지)
- Feature/fix 브랜치에서 rebase 후에만 사용
- 사용자 확인 필수

## Destructive Operations

다음 명령은 사용자 확인 없이 실행하지 않는다:
- `git reset --hard`
- `git checkout -- .`
- `git clean -f`
- `git branch -D`

Force-push는 위 Force Push 절을 따른다. 승인은 금지된 작업을 허용하지 않는다.

## Conflict Resolution

1. 충돌 목록 확인: `git diff --name-only --diff-filter=U`
2. 자동 해결 가능한 경우:
   - 한쪽만 의미 있는 변경 → 해당 쪽 선택
   - 양쪽 다른 섹션 변경 → 양쪽 병합
3. 동일 라인 변경 → 사용자에게 제시

## Detached HEAD

커밋 전 반드시 브랜치 생성을 제안한다.

## Large Files

- 1MB 초과 바이너리 파일 → git-lfs 제안
- `node_modules/`, `dist/`, `*.pyc` 등 빌드 산출물 → `.gitignore` 제안

## Stash Safety

작업을 막는 미커밋 변경만 안전하게 보존한다. rebase 전에는 관련 변경도 dirty 전제조건에 포함된다. stash를 쓰면 기존 stash와 구분할 식별자·대상·staged/unstaged 상태를 기록하고, 필요한 untracked 파일도 빠뜨리지 않는다. 이번 stash만 복원하고 파일·index 보존을 확인한 뒤 제거한다. 충돌·실패 시 stash를 남겨 복구할 수 있게 하고 후속 push를 중단한다. 기존 stash나 승인 범위 밖 변경을 임의로 삭제하지 않는다.
