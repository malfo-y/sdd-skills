# PR Spec Patch Draft

**Date**: 2026-03-09
**PR**: #42 - 사용자 인증 시스템 구현 및 세션 관리 버그 수정
**PR Author**: developer-kim
**PR URL**: https://github.com/example/project/pull/42
**Baseline Spec**: `_sdd/spec/main.md`
**Status**: Draft

> 이 파일은 스펙 자체가 아니라 스펙 반영 초안이다. 실제 반영은 `/spec-update-todo` 또는 구현 완료 후 `/spec-update-done`로 진행한다.

## PR Summary

- 새 JWT 인증 플로우 추가
- 인증 미들웨어 도입
- 세션 갱신 버그 수정
- 관련 환경변수와 에러 응답 형식 일부 변경

## Exploration-First Spec Impact

| 영역 | 반영 필요 | 이유 |
|------|-----------|------|
| `Goal` | 예 | 인증 기능이 핵심 기능으로 승격됨 |
| `Architecture Overview > Runtime Map` | 예 | 로그인/토큰 갱신 플로우가 추가됨 |
| `Component Details > Component Index` | 예 | Auth 관련 컴포넌트와 경로가 늘어남 |
| `Component Details > Overview` | 예 | Auth 서비스와 middleware 분리 이유, 세션/토큰 책임 설명이 바뀜 |
| `Usage Examples > Common Change Paths` | 예 | 인증 정책 변경 시 시작 지점이 생김 |
| `Open Questions` | 예 | 토큰 만료 정책과 CORS 범위 확정 필요 |

## Spec Update Classification

- `MUST update`: 3
- `CONSIDER`: 1
- `NO update`: 1

## Spec Update Input

### Item 1
- **Change Type**: Feature
- **Spec Update Classification**: `MUST update`
- **Target Section**: `Goal > Key Features`
- **Target File**: `_sdd/spec/main.md`
- **Affected Components**: `Auth API`, `Auth Domain`
- **Related Paths / Symbols**:
  - `src/routes/auth.py`
  - `src/services/auth_service.py`
  - `AuthService`
- **Current State**: 메인 스펙에는 기본 세션 인증만 간단히 언급되어 있다.
- **Proposed Spec Update**: JWT 기반 로그인, 회원가입, 토큰 갱신, 로그아웃을 핵심 기능으로 명시한다.
- **Risks / Invariants**:
  - 리프레시 토큰 무효화 규칙을 함께 적어야 함
  - 비밀번호 해싱이 bcrypt라는 점을 불변 조건으로 남길지 검토 필요
- **Test / Observability Notes**:
  - `tests/test_auth_routes.py`
  - `tests/test_refresh_token.py`
- **PR Evidence**:
  - `src/routes/auth.py:1`
  - `src/services/auth_service.py:1`

### Item 2
- **Change Type**: Architecture Update
- **Spec Update Classification**: `MUST update`
- **Target Section**: `Architecture Overview > Runtime Map`
- **Target File**: `_sdd/spec/main.md`
- **Affected Components**: `Auth Middleware`
- **Related Paths / Symbols**:
  - `src/middleware/auth.py`
  - `require_auth`
- **Current State**: 요청 인증 흐름이 메인 스펙의 런타임 맵에 없다.
- **Proposed Spec Update**: 보호된 요청이 `Bearer token 추출 -> 토큰 검증 -> 사용자 컨텍스트 주입 -> 핸들러 실행` 순서로 흐른다는 점을 추가한다.
- **Risks / Invariants**:
  - 401/403 경계가 명확해야 함
- **Test / Observability Notes**:
  - 인증 실패 로그 위치 확인 필요
- **PR Evidence**:
  - `src/middleware/auth.py:12`

### Item 3
- **Change Type**: Component Update
- **Spec Update Classification**: `MUST update`
- **Target Section**: `Component Details > Component Index`
- **Target File**: `_sdd/spec/auth.md`
- **Affected Components**: `Auth API`, `Session Service`
- **Related Paths / Symbols**:
  - `src/services/session_service.py`
  - `src/utils/password.py`
- **Current State**: `auth.md`에 세션 서비스만 있고 JWT 관련 경로가 빠져 있다.
- **Proposed Spec Update**: 소유 경로, 핵심 심볼, 토큰 검증 책임을 추가한다.
- **Risks / Invariants**:
  - 세션 만료와 토큰 갱신의 관계를 명시해야 함
- **Test / Observability Notes**:
  - `test_refresh_expired_session`
- **PR Evidence**:
  - `src/services/session_service.py:89`
  - `src/utils/password.py:8`

### Item 4
- **Change Type**: Component Update
- **Spec Update Classification**: `MUST update`
- **Target Section**: `Component Details > Overview`
- **Target File**: `_sdd/spec/auth.md`
- **Affected Components**: `Auth API`, `Auth Middleware`, `Session Service`
- **Related Paths / Symbols**:
  - `src/routes/auth.py`
  - `src/middleware/auth.py`
  - `src/services/session_service.py`
- **Current State**: 컴포넌트 설명이 경로 중심이라, 세션 수명 관리와 middleware/service 분리 의도가 충분히 드러나지 않는다.
- **Proposed Spec Update**: 로그인/토큰 검증/세션 갱신 책임이 어떻게 분리되는지와 why-context를 `Overview`에 추가한다.
- **Risks / Invariants**:
  - middleware는 인증 컨텍스트 주입까지만 담당하고 비즈니스 정책은 service에 둔다는 경계를 문서화해야 함
- **Test / Observability Notes**:
  - `tests/test_auth_routes.py`
  - `tests/test_refresh_token.py`
- **PR Evidence**:
  - `src/middleware/auth.py:12`
  - `src/services/session_service.py:89`

### Item 5
- **Change Type**: Change Guide Update
- **Spec Update Classification**: `CONSIDER`
- **Target Section**: `Usage Examples > Common Change Paths`
- **Target File**: `_sdd/spec/main.md`
- **Affected Components**: `Auth`
- **Related Paths / Symbols**:
  - `src/routes/auth.py`
  - `src/middleware/auth.py`
- **Current State**: 인증 정책 변경 시 어디부터 봐야 하는지 안내가 없다.
- **Proposed Spec Update**: "권한/인증 정책 변경" 변경 경로를 추가한다.
- **Risks / Invariants**:
  - 환경변수와 토큰 만료 정책을 같이 확인해야 함
- **Test / Observability Notes**:
  - `tests/auth/`
- **PR Evidence**:
  - `src/routes/auth.py:25`
  - `src/middleware/auth.py:12`

### Item 6
- **Change Type**: Refactor
- **Spec Update Classification**: `NO update`
- **Target Section**: `Target Section TBD`
- **Target File**: -
- **Affected Components**: `Password Utility`
- **Related Paths / Symbols**:
  - `src/utils/password.py`
- **Current State**: 내부 helper 분리만 일어났다.
- **Proposed Spec Update**: 없음. 탐색성과 계약 변화가 없다.
- **Risks / Invariants**:
  - bcrypt 사용 invariant는 기존과 동일
- **Test / Observability Notes**:
  - `tests/test_password_utils.py`
- **PR Evidence**:
  - `src/utils/password.py:1`

## Open Questions

1. 토큰 만료 시간과 갱신 정책을 메인 스펙에 둘지 `auth.md`에만 둘지 결정 필요
2. CORS 설정 변경도 `Environment & Dependencies`에 반영해야 하는지 확인 필요
3. `Auth Middleware`의 책임 경계를 메인 스펙 요약에 둘지 `auth.md` `Overview`에만 둘지 결정 필요

## Decision-Log Candidates

1. JWT 기반 인증을 canonical auth flow로 승격
   - Why: 앞으로 인증 관련 변경 시작점이 middleware/service 중심으로 이동함
   - Evidence: `src/routes/auth.py:1`, `src/middleware/auth.py:12`

## Next Recommended Actions

1. `/pr-review`로 acceptance criteria와 문서 영향 검증
2. 머지 전 스펙 패치 초안 정리
3. 머지 후 `/spec-update-done`으로 실제 스펙 동기화
