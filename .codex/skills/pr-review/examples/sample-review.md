# Sample PR Review Session

이 예제는 통합된 `pr-review` 스킬이 두 가지 모드로 동작하는 모습을 보여준다.

- from-branch에 `_sdd/spec/`가 있으면 spec-based verification 포함
- from-branch에 spec이 없으면 code-only mode로 진행

> `pr-review`는 `_sdd/spec/`를 수정하지 않는다. 스펙 반영이 필요하면 리포트에 기록하고 후속으로 `/spec-update-todo`를 사용한다.

## Example A: from-branch spec 기반 리뷰

### 리뷰 시작

```text
User: PR #42 리뷰해 줘

Codex: PR 리뷰를 시작합니다.

## 사전 조건 확인

✓ gh auth status: 인증됨
✓ PR: #42 - 사용자 인증 시스템 구현 및 세션 관리 버그 수정
✓ 기존 리뷰 없음

## from-branch spec 탐색
- headRefName: feature/auth-system
- headRefOid: abcdef123456
- `git ls-tree -r --name-only feature/auth-system _sdd/spec` 확인
- from-branch spec 발견:
  - _sdd/spec/main.md
  - _sdd/spec/auth.md
  - _sdd/spec/security.md
- baseline: _sdd/spec/main.md
- linked sub-spec 로드: auth.md, security.md

## PR 데이터 수집
- 변경 규모: +847 -123, 12개 파일
- 상태: OPEN
- 커밋: 2개
```

### 검증 요약

```text
Codex:
## Code-only Verification

- 코드 품질: 전반적으로 프로젝트 패턴 준수
- 에러 처리: refresh 경로에서 만료 시간 재생성 누락
- 테스트: 신규 기능 대부분 커버, 미들웨어 컨텍스트 주입 테스트 누락
- 보안: JWT secret은 환경변수 사용
- 문서화: .env.example 갱신됨

## Spec-based Verification

### Spec AC Verification
| # | Acceptance Criterion | Implementation | Test | Status | Notes |
|---|----------------------|----------------|------|--------|-------|
| 1 | 회원가입 지원 | `src/routes/auth.py:25-42` | test_register_valid | ✓ | |
| 2 | JWT 토큰 발급 | `src/services/auth_service.py:45-67` | test_login_returns_tokens | ✓ | |
| 3 | refresh 시 새 만료 시간 생성 | `src/services/auth_service.py:89-102` | test_refresh_token | ✗ | exp 갱신 누락 |
| 4 | 인증 컨텍스트 주입 | `src/middleware/auth.py:47-55` | - | △ | 테스트 없음 |

### Spec Compliance
- 보안 요구사항: JWT secret 환경변수 사용으로 충족
- API 구조: `/auth/*` 엔드포인트는 기존 REST 규칙 준수
- 위반 사항: 없음

### Gap Analysis
- In spec but not in PR:
  - refresh 토큰 만료 시간 재생성 검증이 완전하지 않음
- In PR but not in spec:
  - CORS 설정에 Authorization 헤더 허용 추가
```

### 생성된 리포트 예시

```markdown
# PR Review Report

**PR**: #42 - 사용자 인증 시스템 구현 및 세션 관리 버그 수정
**PR Author**: developer-kim
**Review Date**: 2026-04-02
**Reviewer**: Codex (GPT-5)
**Spec**: Found (from-branch)

---

## Verdict

**REQUEST CHANGES**

**Rationale**: refresh 토큰 경로의 핵심 acceptance criterion이 미충족이고, 인증 컨텍스트 주입 테스트가 비어 있어 머지 전 보완이 필요하다.
**Key Findings**:
- refresh 시 새 만료 시간이 생성되지 않아 테스트가 실패함
- 인증 컨텍스트 주입 경로에 테스트가 없음
- CORS 설정 변경은 spec update 후보로 기록 필요

---

## Metrics Summary

| Item | Count |
|------|-------|
| Acceptance criteria | 4 (from spec) |
| Met (✓) | 2 (50%) |
| Not met (✗) | 1 (25%) |
| Partially met (△) | 1 (25%) |
| Spec violations | 0 |
| Test pass rate | 95% |

---

## Code-only Verification

### Inferred Acceptance Criteria
| # | Criterion (from PR description) | Implementation | Test | Status | Notes |
|---|--------------------------------|----------------|------|--------|-------|
| 1 | JWT 기반 인증 추가 | auth routes + services | 관련 테스트 존재 | ✓ | |
| 2 | 세션 갱신 버그 수정 | refresh flow | test_refresh_token | ✗ | exp 갱신 누락 |

### Code Quality
- 서비스/미들웨어 구조는 기존 프로젝트 패턴과 일치한다.
- `auth_service.py`의 refresh 분기에서 새 만료 시간 계산이 빠져 있다.

### Security & Performance
- hardcoded secret 없음
- 인증/인가 흐름은 기존 규칙과 일치

---

## Spec-based Verification

### Spec AC Verification
| # | Acceptance Criterion (from spec) | Implementation | Test | Status | Notes |
|---|----------------------------------|----------------|------|--------|-------|
| 1 | 회원가입 지원 | `src/routes/auth.py:25-42` | test_register_valid | ✓ | |
| 2 | JWT 토큰 발급 | `src/services/auth_service.py:45-67` | test_login_returns_tokens | ✓ | |
| 3 | refresh 시 새 만료 시간 생성 | `src/services/auth_service.py:89-102` | test_refresh_token | ✗ | exp 갱신 누락 |
| 4 | 인증 컨텍스트 주입 | `src/middleware/auth.py:47-55` | - | △ | 테스트 없음 |

### Spec Compliance
None

### Gap Analysis
#### In spec but not in PR
- refresh 만료 시간 갱신 보완 필요

#### In PR but not in spec
- CORS Authorization 헤더 허용

---

## Recommendations

### Pre-merge Blockers
| Priority | Item | Severity | Action |
|----------|------|----------|--------|
| 1 | refresh 만료 시간 갱신 누락 | High | refresh 시 새 exp 클레임 생성 |
| 2 | 인증 컨텍스트 주입 테스트 없음 | Medium | 테스트 추가 |

### Suggested Improvements
| Priority | Item | Benefit |
|----------|------|---------|
| 3 | CORS 변경을 후속 spec update 후보로 기록 | Drift 감소 |

---

## Next Steps

1. [ ] refresh 경로 수정
2. [ ] 미들웨어 테스트 추가
3. [ ] 수정 후 `/pr-review` 재실행
4. [ ] 머지 후 `/spec-update-todo`로 스펙 반영 검토

---

## Metadata

**Review version**: 1
**PR commit SHA**: abc1234
**Spec source**: from-branch
**Generated at**: 2026-04-02 17:40:00
```

## Example B: code-only mode

from-branch에 `_sdd/spec/`가 없는 저장소에서는 code-only mode로 진행한다.

```text
User: 이 PR 승인해도 되는지 봐 줘

Codex:
## from-branch spec 탐색
- headRefName: fix/password-reset-expiry
- `git ls-tree -r --name-only fix/password-reset-expiry _sdd/spec` 결과 없음
- head ref fetch 후 재확인 결과도 없음
- from-branch spec 부재 확인

→ code-only mode로 진행

## Inferred Acceptance Criteria
| # | Criterion | Evidence | Confidence |
|---|-----------|----------|------------|
| 1 | 만료된 비밀번호 재설정 토큰 거부 | PR title/body | High |
| 2 | 유효한 토큰은 정상 처리 | diff + tests | High |
| 3 | 실패 시 일관된 에러 응답 반환 | 구현 패턴 | Medium |
```

### code-only 리포트 예시

```markdown
# PR Review Report

**PR**: #51 - fix: 비밀번호 재설정 토큰 만료 검증 누락
**PR Author**: developer-lee
**Review Date**: 2026-04-02
**Reviewer**: Codex (GPT-5)
**Spec**: Not Found (code-only mode)

---

## Verdict

**APPROVE**

**Rationale**: PR 설명에서 추론한 acceptance criteria가 구현과 테스트로 모두 뒷받침되며, 보안상 명백한 회귀는 보이지 않는다.
**Key Findings**:
- 만료 토큰 차단 로직이 추가되었음
- 관련 테스트가 모두 통과함
- spec은 없어 code-only 기준으로 검토함

---

## Metrics Summary

| Item | Count |
|------|-------|
| Acceptance criteria | 3 (inferred) |
| Met (✓) | 3 (100%) |
| Not met (✗) | 0 (0%) |
| Partially met (△) | 0 (0%) |
| Spec violations | 0 |
| Test pass rate | 100% |

---

## Code-only Verification

### Inferred Acceptance Criteria
| # | Criterion (from PR description) | Implementation | Test | Status | Notes |
|---|--------------------------------|----------------|------|--------|-------|
| 1 | 만료 토큰 거부 | `src/services/password_service.py:34-42` | test_expired_token_rejected | ✓ | |
| 2 | 유효 토큰 정상 처리 | `src/services/password_service.py:28-33` | test_valid_token_reset | ✓ | |
| 3 | 에러 응답 반환 | `src/services/password_service.py:40` | test_expired_token_error_response | ✓ | |

### Code Quality
- 기존 서비스 패턴과 일치한다.

### Security & Performance
- 보안 버그 수정 목적과 구현이 일관된다.

---

## Recommendations

### Pre-merge Blockers
| Priority | Item | Severity | Action |
|----------|------|----------|--------|

### Suggested Improvements
| Priority | Item | Benefit |
|----------|------|---------|
| 1 | 추후 spec 도입 시 비밀번호 재설정 보안 규칙 문서화 | 운영 추적성 향상 |

---

## Next Steps

1. [ ] 머지 진행
2. [ ] 필요 시 `/spec-create` 또는 `/spec-update-todo` 검토

---

## Metadata

**Review version**: 1
**PR commit SHA**: def5678
**Spec source**: none
**Generated at**: 2026-04-02 18:00:00
```
