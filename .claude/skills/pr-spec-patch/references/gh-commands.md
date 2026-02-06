# GitHub CLI (`gh`) Commands Reference

`pr-spec-patch` 스킬에서 사용하는 `gh` CLI 명령어 레퍼런스.

---

## 인증 확인

```bash
gh auth status
```

**성공 출력 예시:**
```
github.com
  ✓ Logged in to github.com account username (keyring)
  - Active account: true
  - Git operations protocol: https
  - Token: gho_****
  - Token scopes: 'gist', 'read:org', 'repo', 'workflow'
```

**실패 시:**
```
You are not logged into any GitHub hosts. Run gh auth login to authenticate.
```

**대응:** `gh auth login` 실행 안내

---

## PR 자동 감지

현재 브랜치에 연결된 PR 번호 조회:

```bash
gh pr view --json number --jq '.number'
```

**성공 출력:**
```
42
```

**PR 없을 때:**
```
no pull requests found for branch "feature/my-branch"
```

**대응:** PR 번호를 직접 입력하도록 요청

---

## PR 메타데이터 수집

```bash
gh pr view [PR_NUMBER] --json title,body,author,state,url,additions,deletions,changedFiles,headRefName,baseRefName,commits,comments,reviews
```

**JSON 필드 설명:**

| 필드 | 타입 | 설명 |
|------|------|------|
| `title` | string | PR 제목 |
| `body` | string | PR 설명 (마크다운) |
| `author` | object | 작성자 (`login` 필드) |
| `state` | string | PR 상태: `OPEN`, `CLOSED`, `MERGED` |
| `url` | string | PR URL |
| `additions` | number | 추가된 라인 수 |
| `deletions` | number | 삭제된 라인 수 |
| `changedFiles` | number | 변경된 파일 수 |
| `headRefName` | string | 소스 브랜치명 |
| `baseRefName` | string | 타깃 브랜치명 |
| `commits` | array | 커밋 목록 (각 항목에 `oid`, `messageHeadline`) |
| `comments` | array | PR 코멘트 |
| `reviews` | array | 리뷰 목록 |

**출력 예시:**
```json
{
  "title": "사용자 인증 시스템 구현",
  "body": "## Summary\n\nJWT 기반 인증 시스템 구현...",
  "author": {
    "login": "developer-kim"
  },
  "state": "OPEN",
  "url": "https://github.com/example/project/pull/42",
  "additions": 847,
  "deletions": 123,
  "changedFiles": 12,
  "headRefName": "feature/auth-system",
  "baseRefName": "main",
  "commits": [
    {
      "oid": "abc1234def5678",
      "messageHeadline": "feat: JWT 인증 서비스 구현"
    },
    {
      "oid": "def5678ghi9012",
      "messageHeadline": "fix: 세션 만료 시 토큰 갱신 버그 수정"
    }
  ],
  "comments": [],
  "reviews": []
}
```

---

## PR Diff 수집

### 전체 Diff

```bash
gh pr diff [PR_NUMBER]
```

**출력:** 표준 unified diff 형식

```diff
diff --git a/src/services/auth_service.py b/src/services/auth_service.py
new file mode 100644
--- /dev/null
+++ b/src/services/auth_service.py
@@ -0,0 +1,145 @@
+import jwt
+from datetime import datetime, timedelta
+...
```

### 변경된 파일 목록만

```bash
gh pr diff [PR_NUMBER] --name-only
```

**출력:**
```
src/services/auth_service.py
src/routes/auth.py
src/middleware/auth.py
src/utils/password.py
src/utils/errors.py
src/models/user.py
src/routes/protected.py
src/services/session_service.py
tests/test_auth_service.py
tests/test_session_service.py
config/settings.py
.env.example
```

---

## 에러 핸들링

### PR을 찾을 수 없는 경우

```bash
gh pr view 999
```

**출력:**
```
GraphQL: Could not resolve to a PullRequest with the number of 999. (repository.pullRequest)
```

**대응:** 올바른 PR 번호 확인 요청

### 인증되지 않은 경우

```bash
gh pr view 42
```

**출력:**
```
gh: not logged into any GitHub hosts
```

**대응:** `gh auth login` 실행 안내

### 리포지토리 외부에서 실행

```bash
gh pr view 42
```

**출력:**
```
could not determine base repo: no git remotes found
```

**대응:** GitHub 저장소 디렉토리에서 실행하도록 안내

---

## 유용한 추가 명령어

### 특정 필드만 추출 (jq 필터)

```bash
# PR 제목만
gh pr view 42 --json title --jq '.title'

# 커밋 메시지 목록
gh pr view 42 --json commits --jq '.commits[].messageHeadline'

# HEAD 커밋 SHA
gh pr view 42 --json commits --jq '.commits[-1].oid'
```

### PR 상태 확인

```bash
# 현재 브랜치의 PR 상태
gh pr status
```

### 리뷰 코멘트 조회

```bash
gh api repos/{owner}/{repo}/pulls/42/comments
```

---

## 대규모 PR 처리 팁

`changedFiles`가 50 이상인 경우:

1. `--name-only`로 파일 목록 먼저 확인
2. 디렉토리별 그룹핑으로 변경 규모 파악
3. 스펙에 문서화된 컴포넌트 관련 파일만 diff 확인
4. 전체 diff 대신 파일별 diff 선택적 확인:

```bash
# 특정 파일의 diff만 확인
gh pr diff 42 | grep -A 50 "^diff --git a/src/services/"
```
