# Sample PR Review Session

이 예제는 통합된 `pr-review` 스킬이 두 가지 모드로 동작하는 모습을 보여준다.

- from-branch에 `_sdd/spec/`가 있으면 spec-based verification 포함
- from-branch에 spec이 없으면 code-only mode로 진행

> `pr-review`는 `_sdd/spec/`를 수정하지 않는다. 스펙 반영이 필요하면 리포트에 기록하고 후속으로 `$spec-sync`를 사용한다.

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
**Signals**: correctness High 1·Med 1·Low 1 / simplicity Med 1 / AC MET 2 of 4 / test pass 95%

---

## 1. Pre-merge (고쳐야 할 것)

### 1. [High · correctness] refresh 시 새 만료 시간이 생성되지 않음
- **위치**: `src/services/auth_service.py:89-102`
- **문제**: refresh 분기가 기존 `exp` 클레임을 그대로 복사해 새 토큰이 원 토큰과 같은 시점에 만료된다. spec AC #3 위반이고 `test_refresh_token`이 실패한다.
- **수정**: refresh 시 현재 시각 기준으로 `exp`를 재계산해 토큰을 발급한다.

### 2. [Medium · simplicity] 토큰 검증 로직이 두 곳에 중복
- **위치**: `src/middleware/auth.py:30-45`, `src/services/auth_service.py:70-84`
- **문제**: 서명 검증 + 만료 확인 로직이 미들웨어와 서비스에 동일하게 복제돼 있다 (중복 코드 차원).
- **수정**: `verify_token()` 하나로 합치고 두 호출처에서 재사용한다 — 동작 동일.

---

## 2. 개선 제안 (non-blocking)

### 1. [Medium · correctness] 인증 컨텍스트 주입 경로에 테스트 없음
- **위치**: `src/middleware/auth.py:47-55`
- **문제**: spec AC #4의 구현은 있으나 테스트가 없어 회귀를 감지할 수 없다 (PARTIAL).
- **수정**: 미들웨어 통과 후 request context에 user가 실리는지 검증하는 테스트를 추가한다.

- `src/config/cors.py:12` — CORS Authorization 헤더 허용은 spec에 없는 변경이므로 머지 후 `$spec-sync`로 spec 반영을 검토한다.

---

## 3. 확인된 것

회원가입(AC #1)과 JWT 발급(AC #2)은 구현·테스트 모두 확인됐다 (증거는 correctness 리포트 §2 ledger). 테스트는 40개 중 38개 통과(95%)이고 실패 2건은 모두 위 refresh 결함에 기인한다. JWT secret은 환경변수로 관리되며 spec 보안 요구사항 위반은 없다.

---

## Metadata

**Review version**: 1
**PR commit SHA**: abc1234
**Spec source**: from-branch
**Correctness report**: `_sdd/pr/2026-04-02_pr_correctness_auth_system.md` — AC 검증 ledger·verification 상세
**Simplicity report**: `_sdd/implementation/2026-04-02_simplicity_review_auth_system.md` — 차원별 스캔 상세
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
**Signals**: correctness Low 1 / simplicity 없음 / AC MET 3 of 3 (inferred) / test pass 100%

---

## 1. Pre-merge (고쳐야 할 것)

없음.

---

## 2. 개선 제안 (non-blocking)

- `src/services/password_service.py:34` — 추후 spec 도입 시 비밀번호 재설정 보안 규칙(토큰 만료 정책)을 문서화하면 운영 추적성이 좋아진다 (`$spec-create` 검토).

---

## 3. 확인된 것

추론 AC 3건(만료 토큰 거부·유효 토큰 정상 처리·일관된 에러 응답) 모두 구현과 테스트로 확인됐다 (증거는 correctness 리포트 §2 ledger). 테스트 전체 통과(100%). simplicity 5개 차원 스캔에서 finding 없음.

---

## Metadata

**Review version**: 1
**PR commit SHA**: def5678
**Spec source**: none
**Correctness report**: `_sdd/pr/2026-04-02_pr_correctness_password_reset_expiry.md` — AC 검증 ledger·verification 상세
**Simplicity report**: `_sdd/implementation/2026-04-02_simplicity_review_password_reset_expiry.md` — 차원별 스캔 상세
**Generated at**: 2026-04-02 18:00:00
```
