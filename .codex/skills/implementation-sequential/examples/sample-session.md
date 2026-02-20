# Sample TDD Implementation Session

This example shows how the implementation skill executes tasks using Test-Driven Development from an authentication system plan.

> **Important**: The `implementation-sequential` skill must **never** create/edit/delete spec documents under `_sdd/spec/`. If spec changes are needed, report drift and ask the user to run `spec-update-todo` (or `spec-update-done`).

## Initial State

User has an implementation plan at `_sdd/implementation/IMPLEMENTATION_PLAN.md` for a User Authentication System.

## Session Flow

### 1. Loading the Plan

```
User: implement the plan

Codex: Found implementation plan at _sdd/implementation/IMPLEMENTATION_PLAN.md

## Implementation Plan: User Authentication System

### Components Identified
1. Auth Core
2. OAuth Module
3. User Management
4. Email Service
5. Security Layer

### Phases
- Phase 1: Foundation (4 tasks)
- Phase 2: Core Authentication (5 tasks)
- Phase 3: OAuth Integration (3 tasks)
- Phase 4: User Management & Email (4 tasks)
- Phase 5: Testing & Documentation (4 tasks)

### Testing Framework Detected
- Framework: pytest
- Test location: tests/
- Naming convention: test_*.py

### Open Questions
- JWT token lifetime? (Need to resolve before starting)

Let me ask about this before we begin...
```

### 2. Starting Phase 1 with TDD

```
Codex:
## Phase 1: Foundation - Starting

### Available Tasks (no blockers):
| ID | Task | Priority | Acceptance Criteria |
|----|------|----------|---------------------|
| 1 | Set up database schema | P0 | 5 criteria |
| 2 | Implement password hashing | P0 | 4 criteria |
| 3 | Create JWT utilities | P0 | 5 criteria |
| 4 | Set up rate limiting | P1 | 3 criteria |

Starting with Task 1...
```

### 3. TDD Implementation of Task 1

```
Codex:
## Task 1: Set up database schema

**Status**: In Progress
**Component**: Auth Core
**Priority**: P0

### Acceptance Criteria
1. Users table with: id, email, password_hash, email_verified, created_at, updated_at
2. OAuth connections table with: user_id, provider, provider_id, access_token
3. Sessions table with: id, user_id, token_hash, expires_at, revoked
4. Proper indexes on email, provider lookups
5. Migration runs successfully

### TDD Progress

#### Criterion 1: Users table schema ✓

**RED** - Writing failing test:
```python
# tests/test_schema.py
def test_users_table_has_required_columns():
    """Users table should have all required columns"""
    columns = get_table_columns('users')
    required = ['id', 'email', 'password_hash', 'email_verified', 'created_at', 'updated_at']
    for col in required:
        assert col in columns, f"Missing column: {col}"
```
Running test... FAILED ✗ (Table doesn't exist yet)

**GREEN** - Creating migration:
```python
# migrations/001_create_users.py
def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('email_verified', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), onupdate=sa.func.now()),
    )
```
Running migration... Done
Running test... PASSED ✓

**REFACTOR** - No refactoring needed for schema

---

#### Criterion 2: OAuth connections table ✓

**RED** - Writing failing test:
```python
def test_oauth_connections_table_has_required_columns():
    columns = get_table_columns('oauth_connections')
    required = ['user_id', 'provider', 'provider_id', 'access_token']
    for col in required:
        assert col in columns
```
Running test... FAILED ✗

**GREEN** - Adding to migration:
```python
op.create_table(
    'oauth_connections',
    sa.Column('id', sa.UUID(), primary_key=True),
    sa.Column('user_id', sa.UUID(), sa.ForeignKey('users.id')),
    sa.Column('provider', sa.String(50), nullable=False),
    sa.Column('provider_id', sa.String(255), nullable=False),
    sa.Column('access_token', sa.Text()),
)
```
Running test... PASSED ✓

**REFACTOR** - No changes needed

---

#### Criterion 3: Sessions table ✓

**RED** - Writing failing test:
```python
def test_sessions_table_has_required_columns():
    columns = get_table_columns('sessions')
    required = ['id', 'user_id', 'token_hash', 'expires_at', 'revoked']
    for col in required:
        assert col in columns
```
Running test... FAILED ✗

**GREEN** - Adding sessions table
Running test... PASSED ✓

---

#### Criterion 4: Proper indexes ✓

**RED** - Writing test for indexes:
```python
def test_users_email_has_index():
    indexes = get_table_indexes('users')
    assert any('email' in idx['columns'] for idx in indexes)

def test_oauth_provider_lookup_has_index():
    indexes = get_table_indexes('oauth_connections')
    assert any('provider' in idx['columns'] and 'provider_id' in idx['columns']
               for idx in indexes)
```
Running tests... FAILED ✗

**GREEN** - Adding indexes:
```python
op.create_index('ix_users_email', 'users', ['email'])
op.create_index('ix_oauth_provider_lookup', 'oauth_connections', ['provider', 'provider_id'])
```
Running tests... PASSED ✓

---

#### Criterion 5: Migration runs successfully ✓

**RED** - Integration test:
```python
def test_migration_runs_in_clean_database():
    """Full migration should run without errors"""
    reset_database()
    result = run_migrations()
    assert result.success
    assert get_current_revision() == 'head'
```
Running test... PASSED ✓ (Already working from previous steps)

---

### Task 1 Complete

**Summary**:
- All 5 acceptance criteria have passing tests
- Tests added: 6
- Files created:
  - migrations/001_create_users.py
  - tests/test_schema.py

Running full test suite... All tests pass ✓

Moving to Task 2...
```

### 4. TDD Implementation of Task 2

```
Codex:
## Task 2: Implement password hashing utility

**Status**: In Progress
**Component**: Security
**Priority**: P0

### Acceptance Criteria
1. Hash passwords using bcrypt with cost factor 12
2. Verify passwords against stored hashes
3. Reject empty or None passwords
4. Function is timing-attack safe

### TDD Progress

#### Criterion 1: Hash with bcrypt cost 12 ✓

**RED**:
```python
# tests/test_security.py
def test_hash_password_uses_bcrypt():
    """Password should be hashed with bcrypt"""
    hashed = hash_password("testpassword")
    assert hashed.startswith("$2b$")  # bcrypt identifier

def test_hash_password_uses_cost_12():
    """Bcrypt should use cost factor 12"""
    hashed = hash_password("testpassword")
    # bcrypt format: $2b$12$...
    assert "$12$" in hashed
```
Running tests... FAILED ✗ (hash_password doesn't exist)

**GREEN**:
```python
# src/utils/security.py
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode(), salt).decode()
```
Running tests... PASSED ✓

**REFACTOR**: Added type hints, docstring

---

#### Criterion 2: Verify passwords ✓

**RED**:
```python
def test_verify_password_returns_true_for_correct():
    hashed = hash_password("mypassword")
    assert verify_password("mypassword", hashed) is True

def test_verify_password_returns_false_for_incorrect():
    hashed = hash_password("mypassword")
    assert verify_password("wrongpassword", hashed) is False
```
Running tests... FAILED ✗

**GREEN**:
```python
def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())
```
Running tests... PASSED ✓

---

#### Criterion 3: Reject empty passwords ✓

**RED**:
```python
def test_hash_password_raises_for_empty():
    with pytest.raises(ValueError):
        hash_password("")

def test_hash_password_raises_for_none():
    with pytest.raises(ValueError):
        hash_password(None)
```
Running tests... FAILED ✗

**GREEN**:
```python
def hash_password(password: str) -> str:
    if not password:
        raise ValueError("Password cannot be empty")
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode(), salt).decode()
```
Running tests... PASSED ✓

---

#### Criterion 4: Timing-attack safe ✓

**RED**:
```python
def test_verify_uses_constant_time_comparison():
    """Verification should use constant-time comparison"""
    # bcrypt.checkpw is inherently constant-time
    # We verify by checking the function used
    import inspect
    source = inspect.getsource(verify_password)
    assert 'bcrypt.checkpw' in source
```
Running test... PASSED ✓ (already using bcrypt.checkpw)

---

### Task 2 Complete

**Summary**:
- All 4 acceptance criteria have passing tests
- Tests added: 7
- Files created:
  - src/utils/security.py
  - tests/test_security.py

Running full test suite... 13 tests, all pass ✓

Moving to Task 3...
```

### 5. Phase 1 Completion Summary

```
Codex:
## Phase 1 Complete

### Summary
All foundation tasks completed using TDD approach.

### Completed Tasks
| ID | Task | Tests | Status |
|----|------|-------|--------|
| 1 | Database schema | 6 | Done |
| 2 | Password hashing | 7 | Done |
| 3 | JWT utilities | 9 | Done |
| 4 | Rate limiting | 5 | Done |

### Test Summary
- Total tests added: 27
- All passing: Yes
- Test coverage: 94%
- No regressions

### Files Created
- migrations/001_create_users.py
- src/utils/security.py
- src/utils/jwt.py
- src/middleware/rate_limit.py
- tests/test_schema.py
- tests/test_security.py
- tests/test_jwt.py
- tests/test_rate_limit.py

### Unblocked for Phase 2
- Task 5: User registration (was blocked by 1, 2)
- Task 6: Login endpoint (was blocked by 1, 2, 3)
- Task 7: Logout endpoint (was blocked by 3)
- Task 8: Input validation (no blockers)
- Task 9: Auth middleware (was blocked by 3)

Proceeding to Phase 2...
```

### 6. Handling a Difficult Test Case

```
Codex:
## Task 5: User registration

### TDD Progress

#### Criterion: Triggers email verification (can be async)

**Challenge**: Testing async email sending is complex

**Approach**: Use mocking for external service

**RED**:
```python
def test_registration_triggers_verification_email(mocker):
    """Registration should queue verification email"""
    mock_send = mocker.patch('src.services.email.send_verification_email')

    response = client.post("/api/auth/register", json={
        "email": "new@test.com",
        "password": "SecurePass123"
    })

    assert response.status_code == 201
    mock_send.assert_called_once_with("new@test.com", mocker.ANY)
```
Running test... FAILED ✗

**GREEN**:
```python
@router.post("/register")
async def register(data: RegisterRequest, background_tasks: BackgroundTasks):
    # ... validation and user creation ...
    background_tasks.add_task(send_verification_email, user.email, token)
    return {"id": user.id, "email": user.email}
```
Running test... PASSED ✓

**REFACTOR**: Extracted email task to service layer
Running all tests... PASSED ✓
```

### 7. Final Implementation Summary

```
Codex:
## Implementation Complete

### Overall Progress
- Total Tasks: 20
- Completed: 20
- Blocked: 0

### Test Coverage
| Phase | Tasks | Tests Added |
|-------|-------|-------------|
| 1: Foundation | 4 | 27 |
| 2: Core Auth | 5 | 34 |
| 3: OAuth | 3 | 18 |
| 4: User Mgmt | 4 | 22 |
| 5: Testing & Docs | 4 | 12 |

### Summary
- **Total tests**: 113
- **All passing**: Yes
- **Coverage**: 91%
- **TDD compliance**: All features test-first

### Files Created/Modified
- 14 source files
- 12 test files
- 3 migration files

### Next Steps
1. Run full E2E test suite
2. Deploy to staging
3. Security review

All acceptance criteria verified through tests.
```

## Key TDD Patterns Demonstrated

1. **Red-Green-Refactor**: Every feature started with a failing test
2. **One Criterion at a Time**: Focused TDD cycles
3. **Test Naming**: Descriptive names explaining expected behavior
4. **Mocking**: External dependencies isolated in tests
5. **Progress Tracking**: Test counts reported throughout
6. **Regression Prevention**: Full suite run after each task
