# Sample Implementation Review Session

This example shows how the implementation-review skill audits an authentication system implementation against its plan.

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

## Key Review Patterns Demonstrated

1. **Systematic Inventory**: Loading all tasks and criteria from the plan
2. **Evidence-Based Verification**: Finding actual code locations for each criterion
3. **Test Correlation**: Matching tests to acceptance criteria
4. **Issue Categorization**: Critical vs Quality vs Improvements
5. **Actionable Recommendations**: Prioritized next steps with specific locations
6. **Clear Summary**: Progress metrics and single most important action
