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
- `git push --force`

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

커밋 그룹에 포함되지 않는 변경사항은 stash로 보호한 뒤 작업 완료 후 복원한다.
