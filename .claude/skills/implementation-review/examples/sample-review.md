# Sample Implementation Review Sessions

This document shows examples for each review tier.

> **Important**: The `implementation-review` skill must **never** create/edit/delete spec documents under `_sdd/spec/`. If spec changes are needed, record them as “spec update needed” and direct the user to `spec-update-todo` (or `spec-update-done`).

---

# Tier 1: Plan-Based Review

This example shows how the skill audits an authentication system implementation against its plan.

## Session Flow

### 1. Starting the Review

```
User: review implementation

Claude: Found implementation plan at _sdd/implementation/IMPLEMENTATION_PLAN.md

Starting implementation review for: User Authentication System

## Step 1: Loading Plan Inventory

### Tasks in Plan (20 total)
| Phase | Tasks | Criteria |
|-------|-------|----------|
| 1: Foundation | 4 | 17 |
| 2: Core Auth | 5 | 24 |
| 3: OAuth | 3 | 12 |
| 4: User Mgmt | 4 | 15 |
| 5: Testing | 4 | 8 |

### Expected Artifacts
- Source files: 14
- Test files: 12
- Migrations: 3
- Config files: 2

Proceeding to verification...
```

### 2. Verifying Implementation

```
Claude:
## Step 2: Verifying Implementation

### Searching for expected files...

#### Source Files
- ✓ src/utils/security.py (found)
- ✓ src/utils/jwt.py (found)
- ✓ src/middleware/auth.py (found)
- ✗ src/middleware/rate_limit.py (MISSING)
- ✓ src/routes/auth.py (found)
- ✓ src/services/user.py (found)
- ✓ src/services/email.py (found)
- △ src/services/oauth.py (partial - only Google implemented)
...

#### Test Files
- ✓ tests/test_security.py (7 tests)
- △ tests/test_jwt.py (5 tests - expected 8)
- ✓ tests/test_auth_routes.py (12 tests)
- ✗ tests/test_rate_limit.py (MISSING)
- ✓ tests/test_user_service.py (8 tests)
...

#### Migrations
- ✓ migrations/001_create_users.py
- ✓ migrations/002_add_oauth.py
- ✓ migrations/003_add_sessions.py

### Running Tests...

Test Results:
- Total: 45
- Passing: 43
- Failing: 2
- Skipped: 0

Failed Tests:
1. test_jwt.py::test_refresh_token_generates_new_token
2. test_oauth.py::test_github_oauth_callback
```

### 3. Assessing Acceptance Criteria

```
Claude:
## Step 3: Acceptance Criteria Assessment

### Phase 1: Foundation

#### Task 1: Database schema (5/5 criteria) ✓

| # | Criterion | Evidence | Test | Status |
|---|-----------|----------|------|--------|
| 1 | Users table with required fields | migrations/001.py:12-25 | test_users_table_columns | MET |
| 2 | OAuth connections table | migrations/002.py:8-18 | test_oauth_table_columns | MET |
| 3 | Sessions table | migrations/003.py:5-15 | test_sessions_table | MET |
| 4 | Proper indexes on email, provider | migrations/001.py:27, 002.py:20 | test_indexes_exist | MET |
| 5 | Migration runs successfully | All migrations applied | test_migration_sequence | MET |

#### Task 2: Password hashing (4/4 criteria) ✓

| # | Criterion | Evidence | Test | Status |
|---|-----------|----------|------|--------|
| 1 | Hash with bcrypt cost 12 | security.py:15 `gensalt(rounds=12)` | test_hash_uses_bcrypt_12 | MET |
| 2 | Verify passwords | security.py:22 `checkpw()` | test_verify_correct/incorrect | MET |
| 3 | Reject empty passwords | security.py:12 `if not password` | test_hash_empty_raises | MET |
| 4 | Timing-attack safe | Uses bcrypt.checkpw | test_constant_time | MET |

#### Task 3: JWT utilities (3/5 criteria) △

| # | Criterion | Evidence | Test | Status |
|---|-----------|----------|------|--------|
| 1 | Generate valid tokens | jwt.py:18 | test_generate_valid_token | MET |
| 2 | Validate signature | jwt.py:35 | test_validate_signature | MET |
| 3 | Check token expiry | jwt.py:42 | - | UNTESTED |
| 4 | Refresh token flow | jwt.py:55 (buggy) | test_refresh_token FAILING | NOT MET |
| 5 | Revoke tokens | jwt.py:68 | test_revoke_token | MET |

**Issue Found**: refresh_token() at line 55 doesn't generate new expiry

#### Task 4: Rate limiting (0/3 criteria) ✗

| # | Criterion | Evidence | Test | Status |
|---|-----------|----------|------|--------|
| 1 | Limit requests per IP | - | - | NOT MET |
| 2 | Configurable limits | - | - | NOT MET |
| 3 | Return 429 when exceeded | - | - | NOT MET |

**Issue Found**: rate_limit.py not implemented

---

### Phase 2: Core Auth

#### Task 5: User registration (6/7 criteria) △

| # | Criterion | Evidence | Test | Status |
|---|-----------|----------|------|--------|
| 1 | Accepts email/password | routes/auth.py:25 | test_register_valid | MET |
| 2 | Validates email format | routes/auth.py:28 | test_register_invalid_email | MET |
| 3 | Returns 409 duplicate | routes/auth.py:32 | test_register_duplicate | MET |
| 4 | Hashes password | routes/auth.py:35 calls security.hash | test_password_hashed | MET |
| 5 | Creates user record | routes/auth.py:38 | test_user_created | MET |
| 6 | Returns JWT | routes/auth.py:42 | test_register_returns_jwt | MET |
| 7 | Triggers email verification | routes/auth.py:45 | - | UNTESTED |

**Issue Found**: Email verification trigger not tested

...

### Phase 3: OAuth

#### Task 10: Google OAuth (4/4 criteria) ✓
[All criteria met]

#### Task 11: GitHub OAuth (2/4 criteria) ✗

| # | Criterion | Evidence | Test | Status |
|---|-----------|----------|------|--------|
| 1 | Redirect to GitHub | oauth.py:45 | test_github_redirect | MET |
| 2 | Handle callback | oauth.py:52 (buggy) | test_github_callback FAILING | NOT MET |
| 3 | Create/link user | - | - | NOT MET |
| 4 | Return JWT | - | - | NOT MET |

**Issue Found**: GitHub callback fails - token exchange error

...
```

### 4. Issues and Improvements

```
Claude:
## Step 4: Issues Identified

### Critical Issues (4)

#### 1. Rate limiting not implemented
- **Task**: 4
- **Impact**: API vulnerable to brute force attacks
- **Location**: src/middleware/rate_limit.py (missing)
- **Blocked by**: Nothing
- **Action**: Create rate_limit.py with IP-based limiting

#### 2. JWT refresh token bug
- **Task**: 3
- **Impact**: Users can't refresh expired tokens
- **Location**: src/utils/jwt.py:55-62
- **Evidence**:
  ```python
  def refresh_token(token):
      payload = decode_token(token)
      # BUG: Missing new expiry timestamp
      return encode_token(payload)  # Returns same expiry!
  ```
- **Test**: test_refresh_token_generates_new_token FAILING
- **Action**: Add new exp claim in refresh_token()

#### 3. GitHub OAuth callback broken
- **Task**: 11
- **Impact**: GitHub login doesn't work
- **Location**: src/services/oauth.py:52-65
- **Evidence**: Token exchange uses wrong client_secret env var
- **Test**: test_github_oauth_callback FAILING
- **Action**: Fix GITHUB_CLIENT_SECRET reference

#### 4. SQL injection vulnerability
- **Task**: N/A (discovered during review)
- **Impact**: Security vulnerability
- **Location**: src/services/user.py:45
- **Evidence**:
  ```python
  # VULNERABLE
  query = f"SELECT * FROM users WHERE email LIKE '%{search}%'"
  ```
- **Action**: Use parameterized query

### Quality Issues (6)

#### 1. Token expiry check untested
- **Task**: 3, Criterion 3
- **Location**: src/utils/jwt.py:42
- **Risk**: Expiry logic might have bugs
- **Action**: Add test_token_expiry_check

#### 2. Email verification untested
- **Task**: 5, Criterion 7
- **Location**: src/routes/auth.py:45
- **Risk**: Verification might not trigger
- **Action**: Add test with mock email service

#### 3. Inconsistent HTTP status codes
- **Location**: src/routes/auth.py
- **Issue**: Login returns 400, Register returns 422 for invalid input
- **Action**: Standardize on 422 for validation errors

#### 4. Missing error messages in OAuth failures
- **Location**: src/services/oauth.py
- **Issue**: OAuth errors return generic "Auth failed"
- **Action**: Add specific error messages

#### 5. No logging in auth routes
- **Location**: src/routes/auth.py
- **Issue**: Auth attempts not logged
- **Action**: Add logging for security audit trail

#### 6. Password validation only checks length
- **Location**: src/utils/security.py:8
- **Issue**: No uppercase/number requirement per spec
- **Action**: Add password strength validation

### Potential Improvements (3)

#### 1. Add request ID to responses
- **Benefit**: Easier debugging
- **Priority**: Low

#### 2. Cache user lookups
- **Location**: src/services/user.py:get_user_by_email
- **Benefit**: Reduce DB load
- **Priority**: Low

#### 3. Add metrics/monitoring
- **Benefit**: Production observability
- **Priority**: Medium (before production)
```

### 5. Summary and Next Steps

```
Claude:
## Step 5: Implementation Review Summary

# Implementation Review: User Authentication System

**Review Date**: 2024-01-15
**Plan**: _sdd/implementation/IMPLEMENTATION_PLAN.md
**Reviewer**: Claude

---

## Progress Overview

### Task Completion
| Status | Count | Percentage |
|--------|-------|------------|
| Complete | 14 | 70% |
| Partial | 4 | 20% |
| Missing | 2 | 10% |
| **Total** | **20** | |

### Acceptance Criteria
- **Total**: 76 criteria
- **Met**: 58 (76%)
- **Not Met**: 12 (16%)
- **Untested**: 6 (8%)

### Test Status
- **Total Tests**: 45
- **Passing**: 43 (96%)
- **Failing**: 2 (4%)
- **Coverage**: 82%

### By Phase
| Phase | Complete | Partial | Missing |
|-------|----------|---------|---------|
| 1: Foundation | 3 | 1 | 0 |
| 2: Core Auth | 4 | 1 | 0 |
| 3: OAuth | 1 | 1 | 1 |
| 4: User Mgmt | 4 | 0 | 0 |
| 5: Testing | 2 | 1 | 1 |

---

## Issues Summary

| Severity | Count | Blocking Release? |
|----------|-------|-------------------|
| Critical | 4 | Yes |
| Quality | 6 | Recommended to fix |
| Improvements | 3 | No |

---

## Recommended Next Steps

### Immediate (Blockers - Must fix before any deployment)

| Priority | Task | Issue | Location |
|----------|------|-------|----------|
| 1 | Fix SQL injection | Security vulnerability | user.py:45 |
| 2 | Implement rate limiting | Task 4 not started | rate_limit.py |
| 3 | Fix JWT refresh bug | Criterion not met | jwt.py:55 |
| 4 | Fix GitHub OAuth | Callback broken | oauth.py:52 |

### Before Phase Sign-off (Quality)

| Priority | Task | Issue |
|----------|------|-------|
| 5 | Add token expiry test | Untested criterion |
| 6 | Add email verification test | Untested criterion |
| 7 | Standardize HTTP status codes | Inconsistent API |
| 8 | Add password strength validation | Spec requirement |

### Before Production (Recommended)

| Priority | Task | Benefit |
|----------|------|---------|
| 9 | Add auth logging | Security audit |
| 10 | Improve OAuth error messages | User experience |
| 11 | Add monitoring/metrics | Observability |

---

## Conclusion

The implementation is **76% complete** with 4 critical issues blocking release.
The most urgent issue is the **SQL injection vulnerability** in user.py:45 which
should be fixed immediately. After addressing the 4 critical issues, the core
authentication functionality will be working.

**Recommended action**: Fix the SQL injection first, then tackle rate limiting
as it's the largest missing feature.

---

Would you like me to:
1. Start fixing the critical issues?
2. Create detailed tasks for the remaining work?
3. Do a deeper review of any specific area?
```

## Key Tier 1 Patterns

1. **Systematic Inventory**: Loading all tasks and criteria from the plan
2. **Evidence-Based Verification**: Finding actual code locations for each criterion
3. **Test Correlation**: Matching tests to acceptance criteria
4. **Issue Categorization**: Critical vs Quality vs Improvements
5. **Actionable Recommendations**: Prioritized next steps with specific locations
6. **Clear Summary**: Progress metrics and single most important action

---

# Tier 2: Spec-Based Review

This example shows how the skill reviews a REST API implementation when only a spec exists (no implementation plan).

## Session Flow

### 1. Tier Detection

```
User: review implementation

Claude: 구현 계획을 탐색합니다...

❌ _sdd/implementation/IMPLEMENTATION_PLAN*.md — 미발견
✓ _sdd/spec/ — 3개 파일 발견
  - spec/overview.md
  - spec/api_endpoints.md
  - spec/data_model.md

**Review Mode**: Tier 2 — Spec-based review (Plan not found)

Spec 구조를 분석합니다...
```

### 2. Spec Analysis

```
Claude:
## Tier 2 Step 1: Spec Analysis

**Spec 구조**: 구조화 (명확한 endpoint/모델 정의 존재)
**추출된 요구사항 수**: 12

| # | 요구사항 | 출처 | 유형 |
|---|---------|------|------|
| 1 | GET /api/users — 사용자 목록 반환 | spec/api_endpoints.md:## Users | 기능 |
| 2 | POST /api/users — 사용자 생성 | spec/api_endpoints.md:## Users | 기능 |
| 3 | User 모델: id, email, name, created_at | spec/data_model.md:## User | 데이터 |
| 4 | 인증: JWT Bearer token | spec/overview.md:## Authentication | 아키텍처 |
| 5 | 페이지네이션: offset/limit 방식 | spec/api_endpoints.md:## Pagination | 기능 |
| ... | ... | ... | ... |

Spec에서 12개 요구사항을 추출했습니다. 구현 상태를 검증합니다...
```

### 3. Verification & Alignment

```
Claude:
## Tier 2 Step 2-3: Verification & Alignment

### Spec Alignment
| # | 요구사항 | 구현 상태 | 테스트 | Status |
|---|---------|----------|-------|--------|
| 1 | GET /api/users | routes/users.py:15 | test_list_users | ALIGNED |
| 2 | POST /api/users | routes/users.py:42 | test_create_user | ALIGNED |
| 3 | User 모델 필드 | models/user.py:8 | - | DRIFT (name 필드 누락) |
| 4 | JWT 인증 | middleware/auth.py:12 | test_jwt_auth | ALIGNED |
| 5 | 페이지네이션 | - | - | MISSING |
| ... | ... | ... | ... | ... |

**요약**: 12개 요구사항 중 8 aligned, 2 drift, 2 missing
```

### 4. Summary

```
Claude:
# Implementation Review: REST API

**Review Date**: 2026-03-11
**Review Mode**: Tier 2 — Spec-based review (Plan not found)
**Reference**: _sdd/spec/ (3 files)
**Reviewer**: Claude

## Progress Overview
- **Spec Requirements**: 12 total
- **Aligned**: 8 (67%)
- **Drift**: 2 (17%)
- **Missing**: 2 (17%)

## Issues Summary
### Critical (1)
1. **User 모델에 name 필드 누락** — Spec에서 필수 필드로 정의, 구현 누락

### Quality (2)
1. 페이지네이션 미구현 — Spec 요구사항
2. 일부 endpoint에 인증 미적용

## Recommended Next Steps
1. [ ] User 모델에 name 필드 추가 + 마이그레이션
2. [ ] 페이지네이션 구현
3. [ ] 모든 endpoint에 인증 미들웨어 적용

## Conclusion
Spec 대비 67% 정합성. name 필드 누락이 가장 시급한 이슈.
구현 계획이 필요하면 `implementation-plan` 스킬 사용을 권장합니다.
```

## Key Tier 2 Patterns

1. **Spec Structure Detection**: 구조화/비구조화 자동 판별
2. **Requirement Extraction**: Spec에서 검증 가능한 요구사항 추출
3. **Alignment Assessment**: ALIGNED / DRIFT / MISSING 3단계 판정
4. **Graceful Fallback**: Plan 없이도 유의미한 리뷰 제공

---

# Tier 3: Code Quality Review

This example shows how the skill reviews code quality when no plan or spec exists.

## Session Flow

### 1. Tier Detection

```
User: review implementation

Claude: 구현 계획을 탐색합니다...

❌ _sdd/implementation/IMPLEMENTATION_PLAN*.md — 미발견
❌ _sdd/spec/ — 디렉토리 미존재 또는 비어있음

**Review Mode**: Tier 3 — Code quality review (no Plan or Spec)

최근 변경 사항을 분석합니다...
```

### 2. Scope Identification

```
Claude:
## Tier 3 Step 1: Review Scope

**모드**: 최근 변경 중심 코드 품질 리뷰
**기간**: 2026-02-25 ~ 2026-03-11 (최근 2주)
**변경 파일 수**: 8
**핵심 변경 영역**: src/services/, src/routes/

| # | 파일 | 변경 유형 | 변경량 |
|---|------|----------|-------|
| 1 | src/services/payment.py | Modified | +120/-15 |
| 2 | src/routes/checkout.py | Created | +85 |
| 3 | src/models/order.py | Modified | +30/-5 |
| 4 | tests/test_payment.py | Created | +60 |
| 5 | src/utils/currency.py | Created | +25 |
| ... | ... | ... | ... |
```

### 3. Code & Test Review

```
Claude:
## Tier 3 Step 2: Code Review

### 보안
- ⚠️ src/services/payment.py:45 — API 키가 하드코딩됨
- ✓ 입력 검증 적절히 수행
- ✓ SQL injection 위험 없음

### 에러 처리
- ✓ payment.py — try/except로 결제 실패 처리
- ⚠️ checkout.py:32 — 외부 API 타임아웃 처리 누락

### 코드 패턴
- ✓ 프로젝트 컨벤션 준수
- ⚠️ currency.py — 유사 함수 3개가 중복 로직 포함

## Tier 3 Step 3: Test Review

- test_payment.py: 8 tests, all passing
- test_checkout.py: 미존재 ⚠️
- test_currency.py: 미존재 ⚠️
- 변경된 코드의 테스트 커버리지: 약 40% (payment만 커버)
```

### 4. Summary

```
Claude:
# Implementation Review: Recent Changes

**Review Date**: 2026-03-11
**Review Mode**: Tier 3 — Code quality review (no Plan or Spec)
**Reference**: Codebase — git log (2026-02-25 ~ 2026-03-11, 8 files)
**Reviewer**: Claude

## Assumptions
- Plan/Spec 미존재로 인해 최근 변경 중심 코드 품질 리뷰 수행
- 리뷰 범위: 최근 2주간 변경된 8개 파일
- 기능 요구사항 대비 검증은 수행하지 않음 (Plan/Spec 필요)

## Issues Summary

### Critical (1)
1. **API 키 하드코딩** — src/services/payment.py:45
   - 환경변수로 이동 필요

### Quality (3)
1. checkout.py에 외부 API 타임아웃 처리 누락
2. checkout.py, currency.py 테스트 미존재
3. currency.py 내 중복 로직

### Improvements (1)
1. currency.py 중복 함수를 공통 헬퍼로 리팩토링

## Recommended Next Steps
1. [ ] payment.py의 하드코딩된 API 키를 환경변수로 이동
2. [ ] checkout.py에 타임아웃 + 재시도 로직 추가
3. [ ] test_checkout.py, test_currency.py 작성

## Conclusion
최근 변경의 핵심 이슈는 API 키 하드코딩 (보안). 테스트 커버리지가 40%로 낮음.
Spec이나 구현 계획이 필요하면 `spec-create` 또는 `implementation-plan` 스킬을 권장합니다.
```

## Key Tier 3 Patterns

1. **Git-Based Scoping**: git log/diff로 리뷰 범위 자동 결정
2. **Non-Interactive**: 기본값(최근 변경)으로 자동 진행, 가정사항 명시
3. **Quality-Focused**: 보안, 에러 처리, 패턴, 테스트 커버리지 중심
4. **Upgrade Path**: Spec/Plan 생성을 위한 후속 스킬 안내
