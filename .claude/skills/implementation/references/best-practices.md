# TDD Implementation Best Practices

## The TDD Mindset

### Core Principle: Test First, Always

**Never write production code without a failing test.**

This isn't just a rule—it's a design tool. Writing tests first:
- Forces you to think about the API before implementation
- Ensures every feature has verification
- Keeps code minimal and focused
- Documents behavior through examples

### The Red-Green-Refactor Rhythm

```
RED    → Write a test that fails (proves test works)
GREEN  → Write minimal code to pass (nothing more)
REFACTOR → Clean up (tests protect you)
```

**Discipline**: Don't skip steps. Don't write extra code in GREEN. Don't refactor without tests passing.

## Writing Good Tests

### Test One Thing

Each test should verify one behavior:

```python
# Good - single behavior
def test_login_with_invalid_email_returns_400():
    response = client.post("/login", json={"email": "bad", "password": "pass"})
    assert response.status_code == 400

# Bad - multiple behaviors
def test_login_validation():
    # Tests invalid email
    # Tests missing password
    # Tests empty email
    # ... too much in one test
```

### Descriptive Names

Test names should explain the scenario and expected outcome:

```
test_<unit>_<scenario>_<expected_outcome>

Examples:
- test_user_registration_with_duplicate_email_returns_409
- test_password_hash_with_empty_input_raises_value_error
- test_jwt_token_after_expiry_returns_unauthorized
```

### Arrange-Act-Assert Structure

```python
def test_something():
    # ARRANGE - Set up preconditions
    user = create_user(email="test@example.com")

    # ACT - Perform the action
    result = login(email="test@example.com", password="wrong")

    # ASSERT - Verify outcome
    assert result.success is False
    assert result.error == "Invalid credentials"
```

### Test Edge Cases

For each feature, consider:
- Happy path (normal use)
- Empty/null inputs
- Boundary conditions
- Error conditions
- Concurrent access (if applicable)

## RED Phase: Writing Failing Tests

### Verify the Test Fails

Run the test before writing code. If it passes:
1. The feature already exists (verify this)
2. The test is wrong (check assertions)
3. The test isn't testing what you think (rewrite)

### Write the Simplest Failing Test

```python
# Start simple
def test_hash_password_returns_string():
    result = hash_password("test")
    assert isinstance(result, str)

# Add complexity incrementally
def test_hash_password_uses_bcrypt():
    result = hash_password("test")
    assert result.startswith("$2b$")
```

### Test the Interface, Not Implementation

```python
# Good - tests behavior
def test_user_can_login_with_correct_password():
    user = create_user(password="secret123")
    assert user.check_password("secret123") is True

# Bad - tests implementation details
def test_password_stored_as_bcrypt_hash():
    user = create_user(password="secret123")
    assert user._password_hash.startswith("$2b$")  # Exposes internals
```

## GREEN Phase: Making Tests Pass

### Write Minimal Code

Only write enough code to make the test pass:

```python
# Test
def test_add_returns_sum():
    assert add(2, 3) == 5

# Minimal GREEN (not ideal but valid)
def add(a, b):
    return 5  # Works for this test!

# After more tests force proper implementation
def add(a, b):
    return a + b
```

### Don't Anticipate Future Tests

If the test doesn't require error handling, don't add it yet:

```python
# Test only requires basic functionality
def test_divide_two_numbers():
    assert divide(10, 2) == 5

# GREEN - just enough to pass
def divide(a, b):
    return a / b  # No zero check yet!

# Later test will drive the zero handling
def test_divide_by_zero_raises_error():
    with pytest.raises(ValueError):
        divide(10, 0)

# Now add zero handling
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

### Fake It Till You Make It

It's okay to hardcode values initially:

```python
# Test 1
def test_fibonacci_of_0_is_0():
    assert fibonacci(0) == 0

# GREEN for test 1
def fibonacci(n):
    return 0

# Test 2
def test_fibonacci_of_1_is_1():
    assert fibonacci(1) == 1

# GREEN for tests 1 and 2
def fibonacci(n):
    return n  # Still minimal!

# Test 3 forces real implementation
def test_fibonacci_of_5_is_5():
    assert fibonacci(5) == 5
```

## REFACTOR Phase: Improving Code

### Keep Tests Green

**Never refactor with failing tests.** If a test fails during refactor:
1. Undo the change
2. Make smaller refactoring steps
3. Consider if the test is too implementation-specific

### Common Refactorings

- Extract method/function
- Rename for clarity
- Remove duplication (DRY)
- Simplify conditionals
- Extract constants

### Don't Change Behavior

Refactoring should not change what the code does—only how it's structured:

```python
# Before refactor
def calculate_price(quantity, unit_price):
    if quantity > 100:
        return quantity * unit_price * 0.9
    return quantity * unit_price

# After refactor - same behavior, cleaner code
BULK_DISCOUNT = 0.9
BULK_THRESHOLD = 100

def calculate_price(quantity, unit_price):
    base_price = quantity * unit_price
    if quantity > BULK_THRESHOLD:
        return base_price * BULK_DISCOUNT
    return base_price
```

## Handling Difficult Testing Scenarios

### External Dependencies

Mock external services:

```python
def test_send_welcome_email_on_registration(mocker):
    mock_email = mocker.patch('services.email.send')

    register_user(email="new@test.com")

    mock_email.assert_called_once_with(
        to="new@test.com",
        template="welcome"
    )
```

### Database Operations

Use test fixtures or in-memory databases:

```python
@pytest.fixture
def db():
    """Create fresh test database"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield Session(engine)
    # Cleanup happens automatically

def test_user_creation(db):
    user = User(email="test@test.com")
    db.add(user)
    db.commit()
    assert db.query(User).count() == 1
```

### Async Code

Use appropriate async test utilities:

```python
@pytest.mark.asyncio
async def test_async_fetch():
    result = await fetch_data("http://example.com")
    assert result.status == 200
```

### Time-Dependent Code

Freeze or mock time:

```python
def test_token_expiry(freezer):
    freezer.move_to("2024-01-01 12:00:00")
    token = create_token(expires_in=3600)

    freezer.move_to("2024-01-01 13:01:00")  # 61 minutes later
    assert token.is_expired() is True
```

## Anti-Patterns to Avoid

### Testing Implementation Details

```python
# Bad - tests private implementation
def test_uses_bcrypt_internally():
    assert user._hasher == bcrypt

# Good - tests observable behavior
def test_password_verification_works():
    user.set_password("secret")
    assert user.verify_password("secret") is True
```

### Too Many Assertions

```python
# Bad - tests multiple things
def test_user_registration():
    response = register(email="test@test.com", password="secret")
    assert response.status == 201
    assert response.user.email == "test@test.com"
    assert response.user.id is not None
    assert response.user.created_at is not None
    assert email_was_sent()

# Good - separate tests for each concern
def test_registration_returns_201():
    ...

def test_registration_returns_user_with_email():
    ...

def test_registration_sends_verification_email():
    ...
```

### Not Running Tests Frequently

Run tests after every change:
- After writing a test (should fail)
- After writing code (should pass)
- After refactoring (should still pass)

### Skipping the RED Phase

If you write code before the test, you don't know if:
- The test actually tests your code
- The test would have failed without your code
- You wrote more code than necessary

## Task Execution with TDD

### One Acceptance Criterion at a Time

```
For criterion in acceptance_criteria:
    RED: Write test for criterion
    GREEN: Make test pass
    REFACTOR: Clean up

    Run full test suite (catch regressions)
```

### Track Progress by Tests

```markdown
## Task: User Registration

### Criteria Progress
- [x] Accepts email/password (2 tests)
- [x] Validates email format (3 tests)
- [x] Returns 409 for duplicate (1 test)
- [ ] Hashes password (0 tests) ← current
- [ ] Returns JWT (0 tests)

Total tests: 6 passing, 0 failing
```

### When a Test is Hard to Write

This is **valuable feedback**. A hard-to-test design often indicates:
- Too many responsibilities
- Tight coupling
- Missing abstraction

Consider redesigning before forcing the test.

## Quality Checklist

Before marking a task complete:

```markdown
- [ ] Every acceptance criterion has at least one test
- [ ] All tests pass
- [ ] Full test suite runs without regressions
- [ ] Code follows existing patterns
- [ ] No untested code paths added
- [ ] Refactoring complete (no TODOs in code)
```

## Post-TDD Quality Review

TDD verifies **specified behavior** — every acceptance criterion gets a test, and the code is driven by those tests. But TDD cannot catch **unspecified risks**: security vulnerabilities, performance issues, cross-task integration gaps, and pattern violations that no acceptance criterion explicitly mentions.

The phase review (Step 5) and final review (Step 6) exist to cover this gap:

- **Security**: SQL injection, XSS, hardcoded secrets, missing auth — these are rarely acceptance criteria but always matter
- **Performance**: N+1 queries, missing indexes, blocking async calls — emerge from how code is used, not how it's specified
- **Patterns**: Naming inconsistencies, duplication across tasks, abstraction misuse — TDD drives correctness, not consistency
- **Integration**: Tasks pass individually but fail together — cross-task interactions aren't tested by single-criterion TDD

### Critical Issues → Fix with TDD

When a review uncovers a critical issue, fix it using the same TDD discipline:

1. Write a test that **exposes** the issue (RED)
2. Fix the code to make the test pass (GREEN)
3. Clean up (REFACTOR)

This ensures the fix is verified and regression-protected.

See `references/review-checklist.md` for detailed checklists used during phase and final reviews.
