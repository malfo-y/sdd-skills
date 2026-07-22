# Sample PR Review Session

이 예제는 `pr-review` 스킬이 두 가지 모드로 동작하는 모습을 보여준다.

- from-branch에 `_sdd/spec/`가 있으면 spec-based verification 포함
- from-branch에 spec이 없으면 code-only mode로 진행

> `pr-review`는 `_sdd/spec/`를 수정하지 않는다. 스펙 반영이 필요하면 리포트에 기록하고 후속으로 `/spec-sync`를 사용한다.

## Example A: from-branch spec 기반 리뷰

### 리뷰 시작

```text
User: PR #42 리뷰해 줘

Claude: PR 리뷰를 시작합니다.

## 사전 조건 확인

✓ gh auth status: 인증됨
✓ PR: #42 - 사용자 인증 시스템 구현 및 세션 관리 버그 수정
✓ 현재 브랜치 = headRefName (feature/auth-system)

## from-branch spec 로드
- gh pr diff #42 --name-only에서 _sdd/spec/ 경로 확인
- git show origin/feature/auth-system:_sdd/spec/main.md 로드
- linked sub-spec 로드: auth.md, security.md

## PR 데이터 수집
- 변경 규모: +847 -123, 12개 파일
- 상태: OPEN
- 커밋: 2개
- 통합 리포트 slug: auth_system
```

### 병렬 dispatch와 verdict 합성

```text
Claude:
## Parallel Dispatch

Agent(subagent_type="sdd-skills:pr-review-agent")         → correctness 렌즈
Agent(subagent_type="sdd-skills:simplicity-review-agent") → clarity 렌즈

두 agent 반환 요약:
- correctness: AC MET 2 / NOT MET 1 / PARTIAL 1, test pass 95%, High 1·Med 1·Low 1 (finding당 위치·문제·수정 포함)
- simplicity: Medium 1 (위치·현재 형태·제안 형태 포함)

→ Verdict: REQUEST CHANGES (correctness High 1 + simplicity Medium 1이 rationale에 기여)
```

### 생성된 리포트 예시

```markdown
# PR Review Report

**PR**: #42 - 사용자 인증 시스템 구현 및 세션 관리 버그 수정
**PR Author**: developer-kim
**Review Date**: 2026-04-02
**Reviewer**: Claude (Opus 4.6)
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

- `src/config/cors.py:12` — CORS Authorization 헤더 허용은 spec에 없는 변경이므로 머지 후 `/spec-sync`로 spec 반영을 검토한다.

---

## 3. 확인된 것

회원가입(AC #1)과 JWT 발급(AC #2)은 구현·테스트 모두 확인됐다 (tests/test_auth.py 통과 출력). 테스트는 40개 중 38개 통과(95%)이고 실패 2건은 모두 위 refresh 결함에 기인한다. JWT secret은 환경변수로 관리되며 spec 보안 요구사항 위반은 없다.

---

## Metadata

**PR commit SHA**: abc1234
**Spec source**: from-branch
**Generated at**: 2026-04-02 17:40:00
```

## Example B: code-only mode

from-branch에 `_sdd/spec/`가 없는 저장소에서는 code-only mode로 진행한다.

```text
User: 이 PR 승인해도 되는지 봐 줘

Claude:
## from-branch spec 탐색
- headRefName: fix/password-reset-expiry
- gh pr diff --name-only 및 from-branch 트리에 _sdd/spec/ 없음

→ code-only mode로 dispatch (spec 컨텍스트 없이)
- correctness reviewer가 PR title/body/코멘트에서 AC를 추론해 검증
```

### code-only 리포트 예시

```markdown
# PR Review Report

**PR**: #51 - fix: 비밀번호 재설정 토큰 만료 검증 누락
**PR Author**: developer-lee
**Review Date**: 2026-04-02
**Reviewer**: Claude (Opus 4.6)
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

- `src/services/password_service.py:34` — 추후 spec 도입 시 비밀번호 재설정 보안 규칙(토큰 만료 정책)을 문서화하면 운영 추적성이 좋아진다 (`/spec-create` 검토).

---

## 3. 확인된 것

추론 AC 3건(만료 토큰 거부·유효 토큰 정상 처리·일관된 에러 응답) 모두 구현과 테스트로 확인됐다 (tests/test_token_expiry.py 통과 출력). 테스트 전체 통과(100%). simplicity 5개 차원 스캔에서 finding 없음.

---

## Metadata

**PR commit SHA**: def5678
**Spec source**: none
**Generated at**: 2026-04-02 18:00:00
```
