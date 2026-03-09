# PR Spec Patch Draft

**Date**: 2026-02-06
**PR**: #42 - 사용자 인증 시스템 구현 및 세션 관리 버그 수정
**PR Author**: developer-kim
**PR URL**: https://github.com/example/project/pull/42
**Target Spec**: project-api.md
**Status**: 초안
**Spec Update Classification**: MUST 4 / CONSIDER 2 / NO 1

> **중요**: `pr-spec-patch`는 `_sdd/spec/` 스펙을 직접 수정하지 않습니다. 이 파일(`_sdd/pr/spec_patch_draft.md`)은 **초안**만 생성하며, 스펙 반영은 `/spec-update-todo`로 진행합니다.

---

## PR 요약

**브랜치**: feature/auth-system → main
**변경 규모**: +847 -123, 12개 파일
**주요 변경사항**:
- JWT 기반 사용자 인증 시스템 신규 구현
- 로그인/회원가입 API 엔드포인트 추가
- 세션 만료 시 토큰 갱신 로직 버그 수정
- 인증 미들웨어 추가로 보호된 라우트 구현
- 비밀번호 해싱 유틸리티 추가

---

## 탐색형 스펙 영향 요약

| 질문 | 답변 | 영향 받는 섹션 |
|------|------|---------------|
| 새 디렉터리/파일/엔트리포인트? | Yes - `src/services/auth_service.py`, `src/middleware/auth.py`, `src/routes/auth.py` 신규 | `Repository Map`, `Component Details` |
| 기존 흐름에 새 단계 추가? | Yes - 모든 보호된 요청에 인증 미들웨어 단계 추가 | `Architecture Overview > Runtime Map` |
| 컴포넌트 책임 경계 변화? | Yes - SessionService에 토큰 검증 책임 추가, 새 AuthService 컴포넌트 | `Component Details > auth`, `Component Details > session` |
| 디버깅/운영 경로 변화? | Yes - 인증 실패 디버깅 경로 신규 (401 에러 추적 경로) | `Usage Examples > Common Change Paths` |
| Open Questions 해소/생성? | Yes - 소셜 로그인 지원 여부, 동시 세션 제한 정책 미정의 | `Open Questions` |

---

## 스펙 패치 내용

<!-- spec-update-todo의 "Spec Update Input" 형식과 호환 -->

### New Features

#### Feature: JWT 기반 사용자 인증
**Spec Update Classification**: MUST
**Priority**: High
**Target Section**: `Goal > Key Features`, `Component Details > auth`
**Source**: PR #42

**Description**:
JWT(JSON Web Token) 기반의 사용자 인증 시스템. 액세스 토큰과 리프레시 토큰을 사용한 이중 토큰 방식 구현. 토큰 만료 시 리프레시 토큰으로 자동 갱신 지원.

**Acceptance Criteria**:
- [ ] 이메일/비밀번호 기반 회원가입
- [ ] 로그인 시 JWT 액세스 토큰 + 리프레시 토큰 발급
- [ ] 액세스 토큰 만료 시 리프레시 토큰으로 갱신
- [ ] 로그아웃 시 리프레시 토큰 무효화
- [ ] 비밀번호 bcrypt 해싱

**PR Evidence**:
- `src/services/auth_service.py:1-145` - AuthService 클래스 신규 구현
- `src/routes/auth.py:1-89` - 인증 API 엔드포인트 (/login, /register, /refresh)
- `src/utils/password.py:1-32` - 비밀번호 해싱 유틸리티

---

#### Feature: 인증 미들웨어
**Spec Update Classification**: MUST
**Priority**: High
**Target Section**: `Architecture Overview > Runtime Map`, `Component Details > middleware`
**Source**: PR #42

**Description**:
보호된 API 라우트에 인증을 적용하는 미들웨어. 요청 헤더의 Bearer 토큰을 검증하고 사용자 정보를 요청 컨텍스트에 주입.

**Acceptance Criteria**:
- [ ] Authorization 헤더에서 Bearer 토큰 추출
- [ ] 토큰 유효성 검증 (서명, 만료)
- [ ] 인증 실패 시 401 응답
- [ ] 인증된 사용자 정보를 요청 컨텍스트에 주입

**PR Evidence**:
- `src/middleware/auth.py:1-67` - 인증 미들웨어 구현
- `src/routes/protected.py:12-15` - 미들웨어 적용 예시

---

### Improvements

#### Improvement: API 에러 응답 표준화
**Spec Update Classification**: CONSIDER
**Priority**: Medium
**Target Section**: `Component Details > error-handling`
**Current State**: 엔드포인트별 다른 에러 응답 형식
**Proposed**: 통일된 에러 응답 스키마 (code, message, details)
**Reason**: 인증 에러를 포함한 모든 API 에러의 일관된 처리
**Source**: PR #42

**PR Evidence**:
- `src/utils/errors.py:1-45` - 표준 에러 응답 클래스 추가
- `src/routes/auth.py:34,56,78` - 표준 에러 응답 사용

---

### Bug Reports

#### Bug Fix: 세션 만료 시 토큰 갱신 실패
**Spec Update Classification**: MUST
**Severity**: High
**Target Section**: `Component Details > session`
**Location**: src/services/session_service.py:89
**Source**: PR #42

**Description**:
세션이 만료된 후 리프레시 토큰으로 새 액세스 토큰을 요청할 때, 세션 상태 확인 로직이 만료된 세션을 유효하지 않은 것으로 처리하여 갱신이 실패하는 버그.

**Fix Approach**:
세션 만료 상태와 토큰 유효성을 분리하여 검증. 세션이 만료되었더라도 리프레시 토큰이 유효하면 새 세션 생성 허용.

**PR Evidence**:
- `src/services/session_service.py:89-102` - 세션 검증 로직 수정
- `tests/test_session_service.py:45-78` - 관련 테스트 추가

---

### Component Changes

#### New Component: AuthService
**Spec Update Classification**: MUST
**Target Section**: `Component Details > auth`
**Purpose**: 사용자 인증 및 토큰 관리
**Input**: 사용자 자격 증명 (이메일, 비밀번호), 토큰
**Output**: JWT 토큰 쌍, 사용자 정보, 인증 결과
**Source**: PR #42

**Planned Methods**:
- `register(email, password)` - 사용자 등록
- `login(email, password)` - 로그인 및 토큰 발급
- `refresh_token(refresh_token)` - 액세스 토큰 갱신
- `logout(refresh_token)` - 로그아웃 (토큰 무효화)
- `verify_token(token)` - 토큰 검증

#### Update Component: SessionService
**Spec Update Classification**: CONSIDER
**Target Section**: `Component Details > session`
**Change Type**: Fix
**Source**: PR #42

**Changes**:
- 세션 만료 상태와 토큰 유효성 분리 검증
- `validate_session()` 메서드에 `allow_expired` 파라미터 추가

---

### Environment & Dependency Changes

#### New Config: JWT_SECRET_KEY
**Spec Update Classification**: MUST
**Target Section**: `Environment & Dependencies`
**Type**: Environment Variable
**Required**: Yes
**Default**: None (필수 설정)
**Description**: JWT 토큰 서명에 사용되는 비밀 키
**Source**: PR #42

#### New Config: JWT_ACCESS_TOKEN_EXPIRE_MINUTES
**Spec Update Classification**: NO
**Target Section**: `Environment & Dependencies`
**Type**: Environment Variable
**Required**: No
**Default**: 30
**Description**: 액세스 토큰 만료 시간 (분)
**Source**: PR #42

#### New Config: JWT_REFRESH_TOKEN_EXPIRE_DAYS
**Spec Update Classification**: NO
**Target Section**: `Environment & Dependencies`
**Type**: Environment Variable
**Required**: No
**Default**: 7
**Description**: 리프레시 토큰 만료 시간 (일)
**Source**: PR #42

---

### Notes

#### Context
사용자 인증은 프로젝트 로드맵의 Phase 2 핵심 기능으로, 이후 역할 기반 접근 제어(RBAC) 구현의 기반이 됨.

#### Constraints
- JWT 비밀 키는 환경 변수로만 관리 (코드에 하드코딩 금지)
- 리프레시 토큰은 데이터베이스에 저장하여 무효화 가능하도록 설계

---

## Open Questions

### 확인 필요 사항

1. **[Target Section: `Component Details > auth`]** 리프레시 토큰 저장 방식이 스펙에 명시되어 있지 않습니다. 현재 구현은 데이터베이스 저장 방식인데, Redis 기반 저장도 고려해야 하나요?
   - 맥락: PR에서 PostgreSQL에 리프레시 토큰을 저장하지만, 대규모 사용자 환경에서 Redis가 더 적합할 수 있음
   - 제안: 현재 PostgreSQL 방식 유지, 추후 성능 이슈 발생 시 Redis 전환 검토

2. **[Target Section: `Component Details > auth`]** 토큰 갱신 엔드포인트(`/auth/refresh`)의 응답에 사용자 정보를 포함해야 하는지 스펙에 미정의됨
   - 맥락: 현재 구현은 새 토큰만 반환하지만, 프론트엔드에서 사용자 정보도 필요할 수 있음
   - 제안: 토큰만 반환하는 현재 방식 유지 (사용자 정보는 별도 `/me` 엔드포인트 사용)

3. **[Target Section: `Goal > Key Features`]** 비밀번호 재설정 기능이 이 PR에 포함되지 않았습니다. 별도 PR로 구현 예정인가요?
   - 맥락: 인증 시스템의 완성도를 위해 비밀번호 재설정은 필수 기능
   - 제안: 별도 PR로 구현하고, 스펙에 계획됨으로 추가

### 스펙 갭

| # | 설명 | 타겟 섹션 | PR Evidence | 제안 |
|---|------|----------|-------------|------|
| 1 | API 에러 응답 표준 스키마가 스펙에 미정의 | `Component Details > error-handling` | `src/utils/errors.py:1-45` | 에러 응답 스키마 섹션 추가 |
| 2 | 인증 미들웨어 적용 라우트 목록이 스펙에 미정의 | `Architecture Overview > Runtime Map` | `src/middleware/auth.py:1-67` | 보호된 엔드포인트 목록 섹션 추가 |

### 모호한 사항

- 소셜 로그인(OAuth) 지원 여부가 스펙에서 불명확. 현재 PR은 이메일/비밀번호만 지원.
- 동시 로그인 세션 수 제한 정책이 정의되지 않음. 현재 구현은 무제한 세션 허용.

---

## Next Recommended Actions

1. 확인 필요 사항 3건 검토 후 패치 항목 확정
2. `MUST` 항목 4건 우선 `/spec-update-todo`로 스펙 반영
3. `CONSIDER` 항목 2건은 팀 논의 후 반영 여부 결정
4. 소셜 로그인 / 동시 세션 제한 정책을 `Open Questions`에 기록

---

## 메타데이터

**생성일**: 2026-02-06 14:30
**스펙 버전**: 1.2.0
**PR 커밋**: abc1234
**대화 라운드**: 1
