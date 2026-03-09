# Implementation Plan: User Authentication System (Parallel-Ready)

## 개요

이메일/비밀번호 로그인, OAuth 연동 (Google, GitHub), 세션 관리, 역할 기반 접근 제어를 갖춘 사용자 인증 시스템을 구축합니다.

## 범위

### In Scope
- 이메일/비밀번호 회원가입 및 로그인
- OAuth 통합 (Google, GitHub)
- JWT 기반 세션 관리
- 역할 기반 접근 제어 (RBAC)
- 비밀번호 재설정 플로우
- 이메일 인증
- 인증 엔드포인트 레이트 제한

### Out of Scope
- 다중 인증 (MFA) — 향후 Phase
- SSO/SAML 통합
- 생체 인증
- Google/GitHub 이외 소셜 로그인

## 컴포넌트

1. **Auth Core**: 회원가입, 로그인, 로그아웃, 세션 관리
2. **OAuth Module**: 서드파티 프로바이더 통합
3. **User Management**: 프로필, 역할, 권한
4. **Email Service**: 인증, 비밀번호 재설정 이메일
5. **Security Layer**: 레이트 제한, CSRF 보호, 입력 검증

## Spec Inputs Used

- **Goal**: 이메일/비밀번호 로그인, OAuth, RBAC가 핵심 기능으로 정의되어 있다.
- **Runtime Map**: 로그인 -> 토큰 발급 -> 보호된 요청 -> 권한 검사 흐름이 구현 대상이다.
- **Component Index**: `Auth Core`, `OAuth`, `Security` 관련 경로가 이미 나뉘어 있다.
- **Common Change Paths**: 인증 정책 변경 시 `routes/auth`, `middleware`, `Policy`를 함께 보게 되어 있다.

## 구현 단계

### Phase 1: 기반 설정

| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 1 | 데이터베이스 스키마 설정 | P0 | - | Auth Core |
| 2 | 비밀번호 해싱 유틸리티 구현 | P0 | - | Security |
| 3 | JWT 토큰 생성/검증 구현 | P0 | - | Auth Core |
| 4 | 레이트 제한 미들웨어 설정 | P1 | - | Security |

### Phase 2: 핵심 인증

| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 5 | 사용자 회원가입 엔드포인트 | P0 | 1, 2 | Auth Core |
| 6 | 로그인 엔드포인트 | P0 | 1, 2, 3 | Auth Core |
| 7 | 로그아웃 엔드포인트 | P0 | 3 | Auth Core |
| 8 | 입력 검증 미들웨어 | P1 | - | Security |
| 9 | 인증 미들웨어 | P0 | 3 | Auth Core |

### Phase 3: OAuth 통합

| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 10 | Google OAuth 플로우 구현 | P1 | 5, 6 | OAuth |
| 11 | GitHub OAuth 플로우 구현 | P1 | 5, 6 | OAuth |
| 12 | OAuth 계정 연결 처리 | P2 | 10, 11 | OAuth |

## 태스크 상세

### Task 1: 데이터베이스 스키마 설정
**Component**: Auth Core
**Priority**: P0
**Type**: Infrastructure

**설명**:
사용자와 세션 테이블의 데이터베이스 마이그레이션을 생성합니다.

**Acceptance Criteria**:
- [ ] Users 테이블: id, email, password_hash, email_verified, created_at, updated_at
- [ ] OAuth connections 테이블: user_id, provider, provider_id, access_token
- [ ] Sessions 테이블: id, user_id, token_hash, expires_at, revoked
- [ ] email, provider 조회에 적절한 인덱스
- [ ] 마이그레이션 성공 실행

**Target Files**:
- [C] `migrations/001_create_users.py` -- Users, OAuth connections, Sessions 테이블 마이그레이션
- [C] `src/models/user.py` -- User 모델 정의
- [C] `src/models/session.py` -- Session 모델 정의
- [C] `tests/test_schema.py` -- 스키마 테스트

**Technical Notes**:
- UUID를 Primary Key로 사용
- Email은 unique, 대소문자 구분 없음

**Dependencies**: -

---

### Task 2: 비밀번호 해싱 유틸리티 구현
**Component**: Security
**Priority**: P0
**Type**: Feature

**설명**:
bcrypt를 사용한 비밀번호 해싱 및 검증 유틸리티를 구현합니다.

**Acceptance Criteria**:
- [ ] bcrypt cost factor 12로 비밀번호 해싱
- [ ] 저장된 해시와 비밀번호 검증
- [ ] 빈 문자열/None 비밀번호 거부
- [ ] 타이밍 공격 안전

**Target Files**:
- [C] `src/utils/security.py` -- hash_password, verify_password 함수
- [C] `tests/test_security.py` -- 비밀번호 해싱 테스트

**Technical Notes**:
- bcrypt 라이브러리 사용
- constant-time comparison 보장

**Dependencies**: -

---

### Task 3: JWT 토큰 생성/검증 구현
**Component**: Auth Core
**Priority**: P0
**Type**: Feature

**설명**:
JWT 기반 액세스/리프레시 토큰 생성 및 검증 기능을 구현합니다.

**Acceptance Criteria**:
- [ ] 액세스 토큰 생성 (15분 만료)
- [ ] 리프레시 토큰 생성 (7일 만료)
- [ ] 토큰 검증 및 디코딩
- [ ] 만료 토큰 거부
- [ ] 잘못된 서명 토큰 거부

**Target Files**:
- [C] `src/utils/jwt_handler.py` -- JWT 유틸리티 함수
- [C] `tests/test_jwt.py` -- JWT 테스트

**Technical Notes**:
- PyJWT 라이브러리 사용
- HS256 알고리즘
- 시크릿 키는 환경 변수에서 로드

**Dependencies**: -

---

### Task 4: 레이트 제한 미들웨어 설정
**Component**: Security
**Priority**: P1
**Type**: Feature

**설명**:
인증 엔드포인트에 적용할 레이트 제한 미들웨어를 구현합니다.

**Acceptance Criteria**:
- [ ] IP당 분당 요청 수 제한
- [ ] 제한 초과 시 429 응답
- [ ] 제한 설정 가능 (환경 변수)

**Target Files**:
- [C] `src/middleware/rate_limit.py` -- 레이트 제한 미들웨어
- [C] `tests/test_rate_limit.py` -- 레이트 제한 테스트

**Technical Notes**:
- 인메모리 카운터 (단일 인스턴스) 또는 Redis (다중 인스턴스)
- 슬라이딩 윈도우 알고리즘

**Dependencies**: -

---

### Task 5: 사용자 회원가입 엔드포인트
**Component**: Auth Core
**Priority**: P0
**Type**: Feature

**설명**:
POST /api/auth/register 엔드포인트를 생성합니다.

**Acceptance Criteria**:
- [ ] 이메일과 비밀번호 요청 본문 수용
- [ ] 이메일 형식 및 비밀번호 강도 검증
- [ ] 이메일 중복 시 409 반환
- [ ] 비밀번호 해싱 후 저장
- [ ] 사용자 레코드 생성
- [ ] 성공 시 JWT 토큰 반환

**Target Files**:
- [C] `src/routes/auth.py` -- 회원가입 엔드포인트
- [C] `src/services/auth_service.py` -- 인증 비즈니스 로직
- [C] `tests/test_registration.py` -- 회원가입 테스트

**Technical Notes**:
- 비밀번호 요구사항: 최소 8자, 대문자 1개, 숫자 1개
- 레이트 제한: IP당 분당 5회

**Dependencies**: 1, 2

---

### Task 6: 로그인 엔드포인트
**Component**: Auth Core
**Priority**: P0
**Type**: Feature

**설명**:
POST /api/auth/login 엔드포인트를 생성합니다.

**Acceptance Criteria**:
- [ ] 이메일과 비밀번호로 인증
- [ ] 잘못된 자격 증명 시 401 반환
- [ ] 성공 시 JWT 액세스/리프레시 토큰 반환
- [ ] 세션 레코드 생성

**Target Files**:
- [M] `src/routes/auth.py` -- 로그인 엔드포인트 추가
- [M] `src/services/auth_service.py` -- 로그인 로직 추가
- [C] `tests/test_login.py` -- 로그인 테스트

**Technical Notes**:
- 로그인 실패 시 동일한 에러 메시지 (email enumeration 방지)

**Dependencies**: 1, 2, 3

---

### Task 7: 로그아웃 엔드포인트
**Component**: Auth Core
**Priority**: P0
**Type**: Feature

**설명**:
POST /api/auth/logout 엔드포인트를 생성합니다.

**Acceptance Criteria**:
- [ ] 현재 세션 무효화
- [ ] 리프레시 토큰 블랙리스트
- [ ] 인증되지 않은 요청 시 401 반환

**Target Files**:
- [M] `src/routes/auth.py` -- 로그아웃 엔드포인트 추가
- [M] `src/services/auth_service.py` -- 로그아웃 로직 추가
- [C] `tests/test_logout.py` -- 로그아웃 테스트

**Technical Notes**:
- 세션 테이블의 revoked 필드 활용

**Dependencies**: 3

---

### Task 8: 입력 검증 미들웨어
**Component**: Security
**Priority**: P1
**Type**: Feature

**설명**:
모든 API 엔드포인트에 적용할 입력 검증 미들웨어를 구현합니다.

**Acceptance Criteria**:
- [ ] 이메일 형식 검증
- [ ] 비밀번호 복잡도 검증
- [ ] XSS 방지를 위한 입력 살균
- [ ] 검증 실패 시 400 + 상세 에러 메시지

**Target Files**:
- [C] `src/middleware/validation.py` -- 입력 검증 미들웨어
- [C] `src/validators/auth_validators.py` -- 인증 관련 검증 스키마
- [C] `tests/test_validation.py` -- 검증 테스트

**Technical Notes**:
- Pydantic 모델 기반 검증

**Dependencies**: -

---

### Task 9: 인증 미들웨어
**Component**: Auth Core
**Priority**: P0
**Type**: Feature

**설명**:
보호된 라우트에 적용할 JWT 인증 미들웨어를 구현합니다.

**Acceptance Criteria**:
- [ ] Authorization 헤더에서 Bearer 토큰 추출
- [ ] 토큰 검증 및 사용자 정보 주입
- [ ] 유효하지 않은 토큰 시 401 반환
- [ ] 만료된 토큰 시 401 반환 (적절한 에러 메시지)

**Target Files**:
- [C] `src/middleware/auth.py` -- 인증 미들웨어
- [C] `tests/test_auth_middleware.py` -- 인증 미들웨어 테스트

**Technical Notes**:
- JWT 유틸리티 재사용
- 데코레이터 또는 미들웨어 패턴

**Dependencies**: 3

---

### Task 10: Google OAuth 플로우 구현
**Component**: OAuth
**Priority**: P1
**Type**: Feature

**설명**:
Google OAuth 2.0 인증 플로우를 구현합니다.

**Acceptance Criteria**:
- [ ] Google OAuth 인증 URL 생성
- [ ] 콜백 처리 및 토큰 교환
- [ ] Google 프로필 정보로 사용자 생성/연결
- [ ] 기존 이메일 사용자와 자동 연결

**Target Files**:
- [C] `src/routes/oauth.py` -- OAuth 라우트
- [C] `src/services/google_oauth.py` -- Google OAuth 서비스
- [C] `tests/test_google_oauth.py` -- Google OAuth 테스트

**Technical Notes**:
- Google Cloud Console에서 OAuth 클라이언트 설정 필요
- state 파라미터로 CSRF 방지

**Dependencies**: 5, 6

---

### Task 11: GitHub OAuth 플로우 구현
**Component**: OAuth
**Priority**: P1
**Type**: Feature

**설명**:
GitHub OAuth 인증 플로우를 구현합니다.

**Acceptance Criteria**:
- [ ] GitHub OAuth 인증 URL 생성
- [ ] 콜백 처리 및 토큰 교환
- [ ] GitHub 프로필 정보로 사용자 생성/연결

**Target Files**:
- [M] `src/routes/oauth.py` -- GitHub OAuth 라우트 추가
- [C] `src/services/github_oauth.py` -- GitHub OAuth 서비스
- [C] `tests/test_github_oauth.py` -- GitHub OAuth 테스트

**Technical Notes**:
- GitHub Developer Settings에서 OAuth App 설정 필요

**Dependencies**: 5, 6

---

### Task 12: OAuth 계정 연결 처리
**Component**: OAuth
**Priority**: P2
**Type**: Feature

**설명**:
하나의 사용자 계정에 여러 OAuth 프로바이더를 연결하는 기능을 구현합니다.

**Acceptance Criteria**:
- [ ] 로그인된 사용자가 추가 OAuth 계정 연결 가능
- [ ] 이미 다른 사용자에 연결된 OAuth 계정 처리
- [ ] 연결된 OAuth 계정 목록 조회

**Target Files**:
- [M] `src/routes/oauth.py` -- 계정 연결 라우트 추가
- [C] `src/services/account_linking.py` -- 계정 연결 서비스
- [C] `tests/test_account_linking.py` -- 계정 연결 테스트

**Technical Notes**:
- oauth_connections 테이블 활용

**Dependencies**: 10, 11

---

## 병렬 실행 요약

| Phase | Total Tasks | Max Parallel | File Conflicts |
|-------|-------------|--------------|----------------|
| 1 | 4 | **4** (전부 독립) | 없음 |
| 2 | 5 | **2** (Task 8 + Task 9) | `auth.py` (Task 5, 6, 7), `auth_service.py` (Task 5, 6, 7) |
| 3 | 3 | **2** (Task 10 + 11) | `oauth.py` (Task 10, 11, 12) |

### Phase 1 병렬 그룹:
- **Group 1**: Task 1 + Task 2 + Task 3 + Task 4 (모든 Target Files 독립 → 전부 동시 실행!)

### Phase 2 병렬 그룹:
- **Group 1**: Task 8 + Task 9 (독립 파일들, 동시 실행 가능)
- **Group 2**: Task 5 (Task 1, 2 의존 해소 후, auth.py 생성)
- **Group 3**: Task 6 (auth.py, auth_service.py 공유로 Task 5 후)
- **Group 4**: Task 7 (auth.py, auth_service.py 공유로 Task 6 후)

### Phase 3 병렬 그룹:
- **Group 1**: Task 10 + Task 11 동시 가능 여부 → oauth.py 충돌
  - 대안: Task 10에서 oauth.py를 생성, Task 11에서 수정 → 순차 실행
- **Group 2**: Task 12 (Task 10, 11 의존)

## 위험 요소 및 대응

| 위험 | 영향 | 확률 | 대응 |
|------|------|------|------|
| OAuth 프로바이더 API 변경 | Medium | Low | 프로바이더 상호작용 추상화, changelog 모니터링 |
| 토큰 보안 취약점 | High | Medium | 보안 리뷰, 검증된 라이브러리 사용, 짧은 토큰 수명 |
| 이메일 전송 실패 | Medium | Medium | 검증된 이메일 서비스 사용, 재시도 로직 |
| auth.py 병렬 충돌 | Medium | High | Task 5, 6, 7 순차 실행 또는 라우트별 파일 분리 |

## Spec Gaps

- [ ] refresh token 만료/회전 정책의 canonical 위치가 메인 스펙인지 `auth.md`인지 불명확하다.

## Expected Spec Sync Follow-ups

- `MUST update`: `Architecture Overview > Runtime Map` - OAuth callback과 refresh flow가 구체화될 가능성이 크다.
- `CONSIDER`: `Environment & Dependencies` - OAuth provider 설정과 mail provider 설정이 실제 구현에 따라 달라질 수 있다.

## 미해결 질문

- [ ] JWT 토큰 수명은? (제안: 액세스 15분, 리프레시 7일)
- [ ] "Remember me" 기능 지원?
- [ ] 이메일 서비스 프로바이더?
- [ ] 비밀번호 요구사항 설정 가능하게 할 것인지?

## 모델 추천

이 구현은 **중-대규모 복잡도** (12개 태스크, 3 Phase, OAuth 통합 포함)입니다.
- **추천 모델**: `sonnet` (표준 구현)
- OAuth 통합 및 보안 아키텍처 결정 시 `opus` 고려
