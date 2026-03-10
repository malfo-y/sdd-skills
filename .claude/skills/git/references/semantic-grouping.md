# Semantic Change Grouping

변경사항을 논리적 커밋 단위로 그룹핑하는 전략.

## Grouping Criteria (우선순위 순)

### 1. Functional Relationship (기능적 연관)
같은 기능을 구성하는 파일들을 하나의 커밋으로 묶는다.

```
# 하나의 커밋으로 묶임
src/auth/login.ts          # 로그인 핸들러
src/auth/login.test.ts     # 로그인 테스트
src/types/auth.ts          # 인증 타입 정의
```

### 2. Directory Proximity (디렉토리 근접성)
같은 모듈/폴더의 파일들은 함께 묶일 가능성이 높다.

```
# 같은 모듈 → 하나의 커밋
src/api/users/controller.ts
src/api/users/service.ts
src/api/users/routes.ts
```

### 3. Nature of Change (변경 성격)
리팩토링, 기능 추가, 버그 수정은 별도 커밋으로 분리한다.

```
# 분리되는 예
feat: src/api/search.ts     → feat(api): add search endpoint
fix:  src/api/users.ts      → fix(api): handle null user gracefully
chore: package.json         → chore(deps): add elasticsearch client
```

### 4. File Type Patterns (파일 유형)
특정 파일 유형은 별도로 그룹핑한다.

| 패턴 | 커밋 타입 |
|------|-----------|
| `*.test.*`, `*.spec.*` | `test` |
| `*.md`, `docs/` | `docs` |
| `package.json`, `*.lock` | `chore(deps)` |
| `.eslintrc`, `tsconfig.json` | `chore(config)` |
| `Dockerfile`, `.github/` | `chore(ci)` |
| `migrations/` | `feat(db)` or `fix(db)` |

## Anti-patterns

- 하나의 커밋에 관련 없는 변경사항을 섞지 않는다
- "miscellaneous" 또는 "various fixes" 같은 모호한 커밋을 만들지 않는다
- 테스트만 별도 커밋으로 빼지 않는다 (기능과 함께 묶는다)
  - 단, 기존 코드에 대한 테스트 추가는 별도 `test` 커밋이 적절하다

## Edge Cases

### 단일 파일, 여러 성격의 변경
`git add -p`를 사용해 hunk 단위로 분리 가능하나, 경계가 모호하면 가장 관련 깊은 그룹에 포함한다.

### 설정 파일 + 코드 변경
설정 변경이 코드 변경의 직접적 결과라면 함께 묶는다. 독립적 설정 변경은 `chore` 커밋으로 분리한다.
