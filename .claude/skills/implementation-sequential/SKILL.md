---
name: implementation-sequential
description: Use this skill when the user asks for "implementation sequential", "sequential implementation", "legacy implementation", "순차 구현", or explicitly wants one-task-at-a-time sequential execution without parallel sub-agent grouping.
version: 1.2.0
---

# Implementation Execution (TDD Approach)

Execute implementation plans systematically using Test-Driven Development (TDD), working through tasks phase by phase while tracking progress and maintaining code quality.

## Simplified Workflow

This skill is **Step 3 of 4** in the simplified SDD workflow:

```
spec → feature-draft-sequential → implementation-sequential (this) → spec-update-done
```

| Step | Skill | Purpose |
|------|-------|---------|
| 1 | spec-create | Create the initial spec document |
| 2 | feature-draft-sequential | Draft feature spec patch + implementation plan |
| **3** | **implementation-sequential** | Execute the implementation plan (TDD) |
| 4 | spec-update-done | Sync spec with actual code |

> **Previous workflow** (7 steps): spec → spec-draft → spec-update-todo → implementation-plan-sequential → implementation-sequential → implementation-review → spec-update-done
> **New workflow** (4 steps): spec → feature-draft-sequential → implementation-sequential → spec-update-done
>
> This skill now includes in-phase and final reviews, so a separate `implementation-review` invocation is no longer required.

## Hard Rule: Never Modify Spec Files

- This skill **MUST NOT** create/edit/delete any spec documents under `<project_root>/_sdd/spec/`.
- If implementation reveals spec drift, ambiguity, or missing requirements:
  - Report it in the progress report / chat, and
  - Ask the user to update the spec via `spec-update-todo` (or run a spec audit via `spec-update-done`).

## Output reports

- Save per-phase report under `<project-root>/_sdd/implementation/IMPLEMENTATION_REPORT_PHASE_<phase-number>.md`.
- Save the final report under a user-specified file (default: `<project-root>/_sdd/implementation/IMPLEMENTATION_REPORT.md`).

## Core Principle: Test-Driven Development

All implementation follows the **Red-Green-Refactor** cycle:

```
┌─────────────────────────────────────────────────────────┐
│  1. RED: Write a failing test for the desired behavior  │
│              ↓                                          │
│  2. GREEN: Write minimal code to make the test pass     │
│              ↓                                          │
│  3. REFACTOR: Clean up while keeping tests green        │
│              ↓                                          │
│  (Repeat for each acceptance criterion)                 │
└─────────────────────────────────────────────────────────┘
```

## Prerequisites

Before starting implementation:

1. **Locate the Implementation Plan**: Check for plan at:
   - User-specified path
   - `<project_root>/_sdd/implementation/IMPLEMENTATION_PLAN.md` (preferred entry point; may link to phase files)
   - `<project_root>/_sdd/implementation/IMPLEMENTATION_PLAN_PHASE_<phase-number>.md` (when the plan is split by phase)
   - `<project_root>/_sdd/drafts/feature_draft_<feature_name>.md` (produced by `feature-draft-sequential` skill; use Part 2: 구현 계획 as the implementation plan)
   - Recent conversation context

If multiple plan files exist and the user did not specify a starting point:
- If only one source exists (IMPLEMENTATION_PLAN or a single feature draft), start from it.
- If both `IMPLEMENTATION_PLAN.md` and feature draft(s) exist, compare whether they describe the same feature. If they do, prefer `IMPLEMENTATION_PLAN.md`. If they describe different features, ask the user which to implement.
- If multiple feature drafts exist and no `IMPLEMENTATION_PLAN.md`, ask the user which feature draft to implement.
- For phase-split plans, ask the user which phase to start/resume (default: Phase 1).

2. **Verify Plan Exists**: If no plan is found, suggest using the `implementation-plan-sequential` or `feature-draft-sequential` skill first.

3. **Understand the Codebase**: Use codebase-retrieval or exploration to understand:
   - Existing code patterns
   - **Testing framework and conventions** (critical for TDD)
   - Test file locations and naming conventions

4. **Load the execution/test environment guide** before running any code or tests:
   - User-specified path
   - `<project_root>/_sdd/env.md` (source of environment variables, conda env, required setup commands)
   - Recent conversation context

If `_sdd/env.md` exists, apply its setup instructions first (for example: `conda activate ...`, required `export` variables, required local services).

## Process Overview

1. **Load the Plan** - Read and parse the implementation plan
2. **Initialize Task Tracking** - Create tasks in the task system
3. **Execute by Phase** - Work through phases in order
4. **Implement Tasks with TDD** - Red-Green-Refactor for each task
5. **Phase Review** - Quality checks after each phase (security, patterns, performance)
6. **Final Review & Report** - Comprehensive review and combined report after all phases

## Step 1: Load the Plan

Read the implementation plan file and extract:

- **Components**: The modules/features being built
- **Phases**: The ordered implementation stages
- **Tasks**: Individual work items with details
- **Dependencies**: Task relationships and blocking items

```markdown
Key sections to parse:
- ## Components
- ## Implementation Phases
- ## Task Details
- ## Open Questions (address before proceeding)
```

If the plan has **Open Questions**, use AskUserQuestion to resolve them before implementation.

## Step 2: Initialize Task Tracking

Create tasks in the tracking system for visibility:

```
For each task in the plan:
1. Use TaskCreate with:
   - subject: Task title from plan
   - description: Full task details including acceptance criteria
   - activeForm: Present continuous form (e.g., "Implementing user registration")

2. After creation, use TaskUpdate to set:
   - addBlockedBy: Tasks that must complete first (by ID mapping)
```

### Task ID Mapping

Maintain a mapping between plan task IDs and system task IDs:
```
Plan ID 1 → System Task "abc123"
Plan ID 2 → System Task "def456"
```

## Step 3: Execute by Phase

Work through phases in order:

```
For each phase:
1. Identify all tasks in this phase
2. Check which tasks are unblocked (no pending dependencies)
3. Work on unblocked P0 tasks first, then P1, P2, P3
4. Mark tasks complete as you finish them
5. Move to next phase when all tasks complete
```

### Phase Execution Pattern

```markdown
## Working on Phase 1: Foundation

### Available Tasks (unblocked):
- Task 1: Set up database schema [P0] ← Start here
- Task 2: Implement password hashing [P0]

### Blocked Tasks:
- Task 5: Implement registration [blocked by 1, 2]

Starting with Task 1...
```

## Step 4: Implement Individual Tasks with TDD

For each task, follow the TDD workflow:

### 4.1 Start Task
```
1. TaskUpdate: Set status to "in_progress"
2. Read task details: acceptance criteria, technical notes
3. Explore relevant code AND test files using codebase-retrieval
4. Identify the testing framework and patterns used
```

### 4.2 TDD Cycle: Red-Green-Refactor

For EACH acceptance criterion in the task:

#### RED: Write Failing Test First
```
1. Translate the acceptance criterion into a test case
2. Write the test that describes the expected behavior
3. Run the test - it MUST fail (confirms test is valid)
4. If test passes without implementation, the test is wrong or feature exists
```

Example:
```markdown
### Acceptance Criterion: "Returns 409 if email already exists"

Writing test first:
```python
def test_registration_returns_409_for_duplicate_email():
    # Arrange
    create_user(email="existing@test.com")

    # Act
    response = client.post("/api/auth/register", json={
        "email": "existing@test.com",
        "password": "SecurePass123"
    })

    # Assert
    assert response.status_code == 409
    assert "already exists" in response.json()["error"]
```

Running test... FAILED (as expected - endpoint doesn't handle this yet)
```

#### GREEN: Write Minimal Code to Pass
```
1. Write the simplest code that makes the test pass
2. Don't add extra functionality
3. Don't optimize prematurely
4. Run the test - it MUST pass now
```

Example:
```markdown
Implementing minimal code:
```python
@router.post("/register")
async def register(data: RegisterRequest):
    existing = await get_user_by_email(data.email)
    if existing:
        raise HTTPException(status_code=409, detail="Email already exists")
    # ... rest of registration
```

Running test... PASSED
```

#### REFACTOR: Clean Up (Keep Tests Green)
```
1. Improve code quality without changing behavior
2. Remove duplication
3. Improve naming
4. Run ALL tests after refactoring - must still pass
```

Example:
```markdown
Refactoring:
- Extracted email validation to shared utility
- Improved error message format

Running all tests... All PASSED
```

### 4.3 Repeat for Each Criterion

```
For each acceptance criterion in the task:
    RED → GREEN → REFACTOR

When all criteria have passing tests → Task is complete
```

### 4.4 Complete Task
```
1. Verify all acceptance criteria have corresponding tests
2. Run full test suite to check for regressions
3. TaskUpdate: Set status to "completed"
4. Note any follow-up items discovered
5. Check if this unblocks other tasks
```

## TDD Guidelines

### Testing environment

Before running any test or executable command, read `_sdd/env.md` and apply the listed setup.
If `_sdd/env.md` is missing, ask the user for the required runtime/test environment instead of guessing.

### What to Test

| Task Type | Test Focus |
|-----------|------------|
| API Endpoint | Request/response, status codes, validation |
| Service/Logic | Business rules, edge cases, error handling |
| Data Layer | CRUD operations, constraints, queries |
| Utility | Input/output transformations, edge cases |

### Test Naming Convention

Follow the project's existing convention, or use:
```
test_<unit>_<scenario>_<expected_result>

Examples:
- test_register_with_valid_data_creates_user
- test_register_with_duplicate_email_returns_409
- test_login_with_wrong_password_returns_401
```

### Test Structure (Arrange-Act-Assert)

```python
def test_something():
    # Arrange - Set up test data and conditions
    user = create_test_user()

    # Act - Perform the action being tested
    result = perform_action(user)

    # Assert - Verify the expected outcome
    assert result.status == "success"
```

### When TDD is Difficult

Some tasks don't fit pure TDD. Adapt the approach:

| Situation | Approach |
|-----------|----------|
| Database migrations | Write migration, then test the schema |
| Configuration/setup | Verify setup works, add smoke tests |
| UI components | Use component testing or integration tests |
| External integrations | Mock the external service in tests |

For these cases, still write tests, but the order may vary.

## Step 5: Phase Review

After completing all tasks in a phase (and before moving to the next phase), run a lightweight quality review. This catches cross-cutting issues that TDD alone cannot cover.

### 5.1 Collect Phase Context

Reuse data already tracked during TDD — **no re-discovery needed**:
- Files created/modified during this phase
- Tests written and their pass/fail status
- Acceptance criteria met
- Any notes or blockers encountered

### 5.2 Cross-Cutting Quality Checks

Run the following checks on all files touched in this phase. Reference `references/review-checklist.md` for detailed criteria.

| Category | What to Check |
|----------|---------------|
| **Security** | SQL injection, XSS, hardcoded secrets, missing auth, input validation |
| **Error Handling** | Consistent response format, logging, graceful degradation |
| **Code Patterns** | Naming conventions, abstraction level, duplication, project conventions |
| **Performance** | N+1 queries, missing indexes, async blocking, resource cleanup |
| **Test Quality** | Independent, deterministic, behavior-focused (not implementation-testing) |
| **Cross-Task Integration** | Tasks within this phase work together correctly |

### 5.3 Categorize Issues

Classify each finding by severity:

- **Critical**: Security vulnerability, data loss risk, core functionality broken → **must fix before next phase**
- **Quality**: Missing edge-case tests, inconsistent error handling, growing tech debt → document, proceed
- **Improvement**: Performance optimization, readability enhancement → note for later

### 5.4 Decision Gate

```
IF critical issues found:
    Fix using TDD (write test exposing the issue → fix → verify)
    Re-run phase review on fixed areas
ELSE IF quality issues only:
    Document findings, proceed to next phase
ELSE:
    Phase is clean — proceed
```

### 5.5 Phase Review Output

Append findings to the phase completion summary. Save per-phase report under `<project-root>/_sdd/implementation/IMPLEMENTATION_REPORT_PHASE_<phase-number>.md`.

## Step 6: Final Review & Report

After all phases complete, run a comprehensive quality review across the **entire implementation**, then produce a combined report.

### 6.1 Comprehensive Quality Review

Apply the same checklists from Step 5.2 but with **cross-phase scope**:
- Do modules from different phases integrate correctly?
- Are there inconsistent patterns between early and late phases?
- Do security boundaries hold across the full system?
- Are there performance issues that only appear at full scale?

### 6.2 Final Decision Gate

Same rules as Step 5.4. Critical issues must be fixed with TDD before declaring completion.

### 6.3 Generate Combined Report

Save the report under a user-specified file (default: `<project-root>/_sdd/implementation/IMPLEMENTATION_REPORT.md`).
- If the file already exists, archive it as `<project-root>/_sdd/implementation/prev/PREV_IMPLEMENTATION_REPORT_<timestamp>.md` (create `prev/` if needed) and create a new one.

The combined report should include:

### Progress Summary
```markdown
## Implementation Report

### Progress Summary
- Total Tasks: X
- Completed: X
- Tests Added: X
- All Passing: Yes/No

### Completed
- [x] Task 1: Set up database schema (3 tests)
- [x] Task 2: Implement password hashing (5 tests)

### Test Summary
- New tests added: 15
- All tests passing: Yes
- Coverage: 87%
```

### Quality Assessment
```markdown
### Quality Assessment

#### Phase Reviews
| Phase | Critical | Quality | Improvements | Status |
|-------|----------|---------|--------------|--------|
| 1: Foundation | 0 | 1 | 2 | Clean |
| 2: Core Auth | 1 (fixed) | 0 | 1 | Fixed |

#### Cross-Phase Review
- Integration: All modules communicate correctly
- Security: Auth boundaries verified across all endpoints
- Performance: No N+1 queries detected

#### Issues Found
| # | Severity | Description | Phase | Status |
|---|----------|-------------|-------|--------|
| 1 | Critical | Rate limiter not applied to OAuth routes | Cross-phase | Fixed |
| 2 | Quality | Password validation only checks length | Phase 1 | Documented |

#### Recommendations
1. Add password complexity validation before production
2. Consider adding integration test suite for cross-module flows

### Conclusion
[Overall assessment: READY / NEEDS WORK / BLOCKED]
```

## Output Format

### During TDD Implementation

Provide updates showing the TDD cycle:

```markdown
## Task 5: Implement user registration

**Status**: In Progress
**Component**: Auth Core

### TDD Progress

#### Criterion 1: Accepts email and password ✓
- [x] RED: Wrote test_register_accepts_valid_credentials
- [x] GREEN: Implemented basic endpoint
- [x] REFACTOR: Extracted validation

#### Criterion 2: Validates email format ✓
- [x] RED: Wrote test_register_rejects_invalid_email
- [x] GREEN: Added email validation
- [x] REFACTOR: Used shared email validator

#### Criterion 3: Returns 409 for duplicate email (current)
- [x] RED: Wrote test_register_returns_409_duplicate
- [ ] GREEN: Implementing...
- [ ] REFACTOR: Pending

#### Remaining Criteria
- [ ] Hashes password before storing
- [ ] Creates user record
- [ ] Returns JWT on success

### Files Modified
- src/routes/auth.ts
- tests/test_auth.py (new tests)

### Test Status
- Tests written: 6
- Tests passing: 5
- Tests failing: 1 (expected - in RED phase)
```

### Phase Completion (with Review)

```markdown
## Phase 1 Complete

### Summary
All foundation tasks completed with full test coverage.

### Completed Tasks
| ID | Task | Tests Added | Status |
|----|------|-------------|--------|
| 1 | Database schema | 4 | Done |
| 2 | Password hashing | 6 | Done |
| 3 | JWT utilities | 8 | Done |
| 4 | Rate limiting | 5 | Done |

### Test Summary
- Total new tests: 23
- All passing: Yes
- No regressions detected

### Phase Review Findings
| Category | Status | Notes |
|----------|--------|-------|
| Security | Clean | No hardcoded secrets, parameterized queries |
| Error Handling | Quality issue | Inconsistent error format in rate limiter |
| Code Patterns | Clean | Follows project conventions |
| Performance | Clean | Indexes in place |
| Test Quality | Clean | All tests independent and deterministic |

**Issues**: 1 Quality (inconsistent error format — documented, not blocking)
**Decision**: Proceed to Phase 2

### Ready for Phase 2
The following tasks are now unblocked:
- Task 5: User registration
- Task 6: Login endpoint

Proceeding to Phase 2...
```

### Final Report

```markdown
## Implementation Report

### Progress Summary
- Total Tasks: 20 | Completed: 20
- Tests Added: 113 | All Passing: Yes | Coverage: 91%

### Phase Reports
| Phase | Tasks | Tests | Critical | Quality | Status |
|-------|-------|-------|----------|---------|--------|
| 1: Foundation | 4 | 27 | 0 | 1 | Clean |
| 2: Core Auth | 5 | 34 | 1 (fixed) | 0 | Fixed |
| 3: OAuth | 3 | 18 | 0 | 0 | Clean |
| 4: User Mgmt | 4 | 22 | 0 | 2 | Clean |
| 5: Testing | 4 | 12 | 0 | 0 | Clean |

### Quality Assessment
#### Cross-Phase Review
- Integration: All modules communicate correctly
- Security: Auth boundaries verified across all endpoints
- Performance: No N+1 queries detected

#### Issues Found
| # | Severity | Description | Phase | Status |
|---|----------|-------------|-------|--------|
| 1 | Critical | Rate limiter not applied to OAuth routes | Cross-phase | Fixed |
| 2 | Quality | Password validation only checks length | 1 | Documented |
| 3 | Quality | Missing retry logic for email service | 4 | Documented |

### Recommendations
1. Add password complexity rules before production
2. Add retry/backoff to email service calls

### Conclusion
READY — All critical issues resolved, 3 quality items documented for follow-up.
```

## Handling Common Situations

### Test is Hard to Write
```
1. Simplify the acceptance criterion
2. Break into smaller, testable pieces
3. Consider if the design needs adjustment (TDD feedback)
4. Ask user if criterion can be clarified
```

### Test Passes Immediately (No Code Written)
```
1. Feature may already exist - verify
2. Test may be wrong - review the assertion
3. Test may be testing the wrong thing - rewrite
```

### Refactoring Breaks Tests
```
1. Undo the refactoring
2. Check if test was too implementation-specific
3. Refactor in smaller steps
4. Consider if the test needs updating (rarely)
```

### Task is Blocked by External Dependency
```
1. Write tests with mocks for the external dependency
2. Implement code against the mocks
3. Note that integration test needed when dependency available
4. Move to next task
```

### Acceptance Criteria Unclear
```
1. Check task details and technical notes
2. Review related code for context
3. Use AskUserQuestion if still unclear
4. Write test based on best interpretation, confirm with user
```

## Implementation Best Practices

### Code Quality
- **Test first, always**: No production code without a failing test
- **Minimal code**: Write only enough to pass the test
- **Follow existing patterns**: Match the codebase's style and conventions
- **Refactor fearlessly**: Tests give confidence to improve code

### Task Execution
- **One criterion at a time**: Complete Red-Green-Refactor before next
- **Check dependencies**: Never start a blocked task
- **Update status**: Keep task tracking current
- **Document blockers**: If stuck, note the issue and move to another task

### Communication
- **Report TDD progress**: Show which criteria have tests
- **Surface blockers**: Alert user to issues requiring decisions
- **Confirm scope changes**: Ask before deviating from the plan

## When to Pause and Ask

Use AskUserQuestion when:

- **Test unclear**: Can't determine what to assert
- **Ambiguous requirements**: Multiple valid interpretations
- **Scope decisions**: Discovered work that may or may not be in scope
- **Technical choices**: Multiple valid approaches with trade-offs
- **Blockers**: External dependencies or issues requiring user action

## Integration with Other Skills

- **implementation-plan-sequential**: Use first to create the plan this skill executes
- **feature-draft-sequential**: Also produces an implementation plan (Part 2: 구현 계획) inside its output file. This skill can consume feature drafts directly.
- **implementation-review**: Remains available as a standalone skill for independent audits. This implementation skill now includes in-place phase and final reviews, so a separate review invocation is no longer required for the standard workflow.

## Quick Start

When user says "implement the plan":

1. Acquire implementation plan by running `implementation-plan-sequential` or `feature-draft-sequential` skill if not exists
2. Look for implementation plan at `_sdd/implementation/IMPLEMENTATION_PLAN.md`, phase-split files, or `_sdd/drafts/feature_draft_<feature_name>.md`
3. If user input severely conflicts with the plan, abort and ask user to resolve the conflict
4. Parse the plan and create task tracking
5. **Identify testing framework** used in the project
6. Start with Phase 1, Task with lowest ID that is unblocked and highest priority
7. For each acceptance criterion: **RED → GREEN → REFACTOR**
8. After each phase: **Run phase review** (security, quality, patterns, performance)
9. Fix any **critical issues** found during review (using TDD)
10. After all phases: Run **final review**, generate `IMPLEMENTATION_REPORT.md`
