# Sample Parallel TDD Implementation Session

This example shows how the `implementation` skill executes tasks using parallel sub-agent dispatch with TDD, from an authentication system plan that includes Target Files.

> **Important**: The `implementation` skill must **never** create/edit/delete spec documents under `_sdd/spec/`.

## Initial State

User has a parallel-ready implementation plan at `_sdd/drafts/feature_draft_auth_system.md` with Target Files on every task.

## Session Flow

### Step 1: Load the Plan

```
User: implement the plan in parallel

Claude: Found implementation plan at _sdd/drafts/feature_draft_auth_system.md

## Implementation Plan: User Authentication System

### Components Identified
1. Auth Core
2. OAuth Module
3. Security Layer

### Phases
- Phase 1: Foundation (4 tasks)
- Phase 2: Core Authentication (5 tasks)
- Phase 3: OAuth Integration (3 tasks)

### Target Files Detected ✓
All 12 tasks have Target Files — parallel execution enabled.

### Testing Framework Detected
- Framework: pytest
- Test location: tests/
- Naming convention: test_*.py

### Spec Context Loaded
- Goal: 인증 시스템과 OAuth 로그인 지원
- Runtime Map: 회원가입/로그인 요청이 auth routes → auth service → models/session 으로 흐름
- Component Index: Auth Core, OAuth Module, Security Layer
- Common Change Paths: 인증 규칙 변경은 `routes/auth.py`, `services/auth_service.py`, 관련 middleware 부터 확인
- Initial Spec Sync Risk: `CONSIDER` 1건, `MUST update` 후보 1건
```

### Step 2: Initialize Task Tracking

```
Claude:
## Task Tracking Initialized

| ID | Task | Phase | Priority | Status |
|----|------|-------|----------|--------|
| 1 | Database schema | 1 | P0 | PENDING |
| 2 | Password hashing | 1 | P0 | PENDING |
| 3 | JWT utilities | 1 | P0 | PENDING |
| 4 | Rate limiting | 1 | P1 | PENDING |
| 5 | Registration | 2 | P0 | PENDING |
| ... | ... | ... | ... | PENDING |

12 tasks tracked. Starting Phase 1...
```

### Step 3: Analyze Parallelization

```
Claude:
## Phase 1: Foundation — Parallel Analysis

### Unblocked Tasks:
| ID | Task | Priority | Target Files |
|----|------|----------|-------------|
| 1 | Database schema | P0 | migrations/001.py, models/user.py, models/session.py, tests/test_schema.py |
| 2 | Password hashing | P0 | utils/security.py, tests/test_security.py |
| 3 | JWT utilities | P0 | utils/jwt_handler.py, tests/test_jwt.py |
| 4 | Rate limiting | P1 | middleware/rate_limit.py, tests/test_rate_limit.py |

### Conflict Analysis:
- Task 1 ∩ Task 2 = ∅ ✓
- Task 1 ∩ Task 3 = ∅ ✓
- Task 1 ∩ Task 4 = ∅ ✓
- Task 2 ∩ Task 3 = ∅ ✓
- Task 2 ∩ Task 4 = ∅ ✓
- Task 3 ∩ Task 4 = ∅ ✓

### Parallel Groups:
- **Group 1**: [Task 1, Task 2, Task 3, Task 4] — ALL parallel! (No conflicts)

🚀 4 tasks dispatched simultaneously (4x speedup vs sequential)
```

### Step 4: Execute by Phase (Parallel)

#### Phase 1 — Dispatching Sub-Agents

```
Claude: Dispatching 4 sub-agents for Phase 1...

[Task tool call 1: Task 1 - Database schema]
[Task tool call 2: Task 2 - Password hashing]
[Task tool call 3: Task 3 - JWT utilities]
[Task tool call 4: Task 4 - Rate limiting]

(All 4 calls made simultaneously in a single message)

Waiting for all sub-agents to complete...
```

#### Phase 1 — Sub-Agent Results

```
Claude:
## Phase 1 Group 1 — Sub-Agent Results

### Task 1: Database schema ✅ SUCCESS
| Criterion | RED | GREEN | REFACTOR | Status |
|-----------|-----|-------|----------|--------|
| Users table | ✓ | ✓ | ✓ | 완료 |
| OAuth table | ✓ | ✓ | ✓ | 완료 |
| Sessions table | ✓ | ✓ | ✓ | 완료 |
| Indexes | ✓ | ✓ | ✓ | 완료 |
| Migration runs | ✓ | ✓ | - | 완료 |

Files: [C] migrations/001.py, [C] models/user.py, [C] models/session.py, [C] tests/test_schema.py
Tests: 6 new, all passing

### Task 2: Password hashing ✅ SUCCESS
| Criterion | RED | GREEN | REFACTOR | Status |
|-----------|-----|-------|----------|--------|
| bcrypt hash | ✓ | ✓ | ✓ | 완료 |
| Verify password | ✓ | ✓ | ✓ | 완료 |
| Reject empty | ✓ | ✓ | ✓ | 완료 |
| Timing-safe | ✓ | ✓ | - | 완료 |

Files: [C] utils/security.py, [C] tests/test_security.py
Tests: 7 new, all passing

### Task 3: JWT utilities ✅ SUCCESS
| Criterion | RED | GREEN | REFACTOR | Status |
|-----------|-----|-------|----------|--------|
| Access token | ✓ | ✓ | ✓ | 완료 |
| Refresh token | ✓ | ✓ | ✓ | 완료 |
| Token verify | ✓ | ✓ | ✓ | 완료 |
| Expired reject | ✓ | ✓ | - | 완료 |
| Bad signature | ✓ | ✓ | - | 완료 |

Files: [C] utils/jwt_handler.py, [C] tests/test_jwt.py
Tests: 9 new, all passing

### Task 4: Rate limiting ✅ SUCCESS
| Criterion | RED | GREEN | REFACTOR | Status |
|-----------|-----|-------|----------|--------|
| Per-IP limit | ✓ | ✓ | ✓ | 완료 |
| 429 response | ✓ | ✓ | ✓ | 완료 |
| Configurable | ✓ | ✓ | - | 완료 |

Files: [C] middleware/rate_limit.py, [C] tests/test_rate_limit.py
Tests: 5 new, all passing

### No Unplanned Dependencies reported.
```

#### Phase 2 — Analysis & Execution

```
Claude:
## Phase 2: Core Auth — Parallel Analysis

### Conflict Analysis:
- Task 5 ∩ Task 6 = {routes/auth.py, services/auth_service.py} ❌
- Task 5 ∩ Task 8 = ∅ ✓
- Task 5 ∩ Task 9 = ∅ ✓
- Task 6 ∩ Task 7 = {routes/auth.py, services/auth_service.py} ❌
- Task 8 ∩ Task 9 = ∅ ✓

### Parallel Groups:
- **Group 1**: [Task 5, Task 8, Task 9] — 3 tasks parallel
- **Group 2**: [Task 6] — sequential (shares auth.py with Task 5)
- **Group 3**: [Task 7] — sequential (shares auth.py with Task 6)

Speedup: 5 tasks → 3 groups (vs 5 sequential)

## Phase 2 Group 1 — Dispatching 3 sub-agents
[Task tool: Task 5 - Registration]
[Task tool: Task 8 - Input validation]
[Task tool: Task 9 - Auth middleware]
(3 calls made simultaneously)

### Group 1 Results: All 3 SUCCESS ✅
Running full test suite... 54 tests, ALL PASSING ✓

## Phase 2 Group 2 — Sequential: Task 6 (Login)
(Modifies auth.py created by Task 5)

### TDD Progress for Task 6:
#### Criterion 1: Email/password authentication ✓
- [x] RED: test_login_with_valid_credentials
- [x] GREEN: Implemented login endpoint
- [x] REFACTOR: Extracted common validation
... (all criteria complete) ...

Running full test suite... 68 tests, ALL PASSING ✓

## Phase 2 Group 3 — Sequential: Task 7 (Logout)
... (similar TDD flow) ...
Running full test suite... 74 tests, ALL PASSING ✓
```

### Step 5: Integrate & Verify

```
Claude:
## Post-Group Verification (Phase 1 example)

### Full Test Suite
Running all tests... 27 tests, ALL PASSING ✓

### File Integrity Check
- All sub-agents stayed within their Target Files ✓
- No unauthorized modifications ✓

### Integration Check
- No conflicting imports ✓
- No duplicate utility functions ✓

### Summary
| Metric | Value |
|--------|-------|
| Tasks completed | 4/4 |
| Tests added | 27 |
| All passing | Yes |
| Unplanned dependencies | 0 |
| Sub-agent failures | 0 |

### Spec Sync Check
- `MUST update`: refresh token 만료 정책이 Runtime Map/Change Paths 에 반영 필요
- `CONSIDER`: rate limiter 디버깅 포인트를 Usage Examples 에 추가할 가치 있음
- `NO update`: bcrypt 내부 리팩터링은 spec sync 불필요

All Phase 1 tasks complete. Running Phase Review...
```

### Step 6: Phase Review

```
Claude:
## Phase 1 Review

### Cross-Cutting Quality Checks

#### Security
- ✓ Parameterized queries in migrations
- ✓ No hardcoded secrets
- ✓ bcrypt with cost 12

#### Error Handling
- ✓ ValueError for empty passwords
- ⚠ Rate limiter returns raw string instead of JSON

#### Code Patterns
- ✓ Consistent naming across all 4 sub-agent outputs
- ✓ All follow project conventions

#### Performance
- ✓ Indexes on users.email and oauth_connections

#### Parallel Consistency
- ✓ All sub-agents used consistent import style
- ✓ No conflicting patterns detected

### Issues
| # | Severity | Description |
|---|----------|-------------|
| 1 | Quality | Rate limiter raw string error format |

**Decision**: No critical issues. Proceed to Phase 2.
```

```
## Phase 2 Review

### Cross-Cutting Quality Checks
- ✓ Security: Auth checks on all protected routes
- ✓ Error handling: Consistent JSON error responses
- ✓ Code patterns: Consistent across sequential and parallel tasks

### Parallel Consistency Check
- ✓ Task 8 (validation middleware) and Task 9 (auth middleware) have compatible patterns
- ✓ Both integrate cleanly with Task 5's auth routes

### Issue Found: None critical
**Decision**: Proceed to Phase 3
```

### Step 7: Final Review & Report

```
Claude:
## Implementation Report (Parallel Execution)

### Progress Summary
- Total Tasks: 12
- Completed: 12
- Tests Added: 98
- All Passing: Yes

### Parallel Execution Stats
- Total Groups Dispatched: 6
- Tasks Run in Parallel: 8 (of 12)
- Sequential Fallbacks: 4 (due to file conflicts)
- Sub-agent Failures: 0
- Speedup: ~2.5x vs fully sequential

### Phase Reports
| Phase | Tasks | Groups | Parallel | Sequential | Tests | Status |
|-------|-------|--------|----------|------------|-------|--------|
| 1: Foundation | 4 | 1 | 4 | 0 | 27 | Clean |
| 2: Core Auth | 5 | 3 | 3 | 2 | 47 | Clean |
| 3: OAuth | 3 | 2 | 2 | 1 | 24 | Clean |

### Quality Assessment

#### Cross-Phase Review
- Integration: All modules communicate correctly
- Security: Auth boundaries verified across all endpoints
- Performance: No N+1 queries detected
- Parallel Consistency: No conflicting patterns between sub-agents

#### Issues Found
| # | Severity | Description | Status |
|---|----------|-------------|--------|
| 1 | Quality | Rate limiter raw string format | Documented |

#### Spec Sync Candidates
| Item | Classification | Why | Recommended Action |
|------|----------------|-----|--------------------|
| Refresh token policy | MUST update | 운영/변경 경로에 영향 | spec-update-done |
| Rate limiter debugging notes | CONSIDER | 반복 디버깅 포인트 | spec-update-done |
| Internal bcrypt refactor | NO update | 탐색성/계약 변화 없음 | none |

### Conclusion
READY — All tasks complete with full test coverage. 1 quality item documented.
98 tests passing. Parallel execution achieved ~2.5x speedup.

Saved to: _sdd/implementation/IMPLEMENTATION_REPORT.md

### Recommended Spec Action
Run `spec-update-done` to sync Runtime Map and Common Change Paths.
```

## Key Parallel Patterns Demonstrated

1. **Full Parallelism**: Phase 1 — all 4 tasks had independent files → all ran simultaneously
2. **Partial Parallelism**: Phase 2 — 3 of 5 tasks parallelized, 2 ran sequentially due to shared `auth.py`
3. **Conflict Detection**: Target Files intersection identified `routes/auth.py` as a bottleneck
4. **Post-Group Verification**: Full test suite after each group ensures no regressions
5. **Sequential Fallback**: When files conflict, tasks gracefully fall back to sequential execution
6. **Parallel Consistency Review**: Phase review includes cross-agent pattern consistency check
7. **TDD Compliance**: Every sub-agent follows Red-Green-Refactor independently
8. **Speedup Tracking**: Report shows actual parallel vs sequential task counts
