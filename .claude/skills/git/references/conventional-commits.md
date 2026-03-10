# Conventional Commits Reference

시맨틱 커밋 메시지 작성 가이드.

## Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

## Types

| Type | 용도 | 예시 |
|------|------|------|
| `feat` | 새 기능 | `feat(auth): add JWT refresh endpoint` |
| `fix` | 버그 수정 | `fix(ui): resolve dropdown z-index overlap` |
| `refactor` | 리팩토링 (동작 변경 없음) | `refactor(api): extract validation middleware` |
| `style` | 포맷팅, 공백 | `style(lint): apply prettier formatting` |
| `docs` | 문서 | `docs(readme): add setup instructions` |
| `test` | 테스트 | `test(auth): add login integration tests` |
| `chore` | 빌드, 의존성, CI | `chore(deps): bump express to 4.21` |
| `perf` | 성능 개선 | `perf(query): add index for user lookup` |

## Scope

- 주요 디렉토리 또는 모듈에서 파생 (e.g., `auth`, `api`, `ui`, `db`)
- 단일 파일 변경 시 파일명 기반 스코프도 가능
- 여러 모듈에 걸친 변경 시 가장 핵심 모듈을 선택

## Description Rules

- 명령형 (imperative mood): "add", "fix", "remove" (not "added", "fixes")
- 소문자 시작
- 마침표 없음
- 50자 이내

## Breaking Changes

```
feat(api)!: migrate to v2 authentication scheme

BREAKING CHANGE: /auth/login now requires `client_id` parameter.
Old clients without `client_id` will receive 400 Bad Request.
```

## Multi-line Body (optional)

```
fix(auth): prevent token reuse after logout

Previously, refresh tokens remained valid after user logout.
Now tokens are added to a blocklist on logout and checked
during refresh attempts.

Closes #142
```
