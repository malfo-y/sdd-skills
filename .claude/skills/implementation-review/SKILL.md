---
name: implementation-review
description: Use this skill to review implementation progress against the plan, verify acceptance criteria, identify issues, and determine next steps. Triggered by "review implementation", "check progress", "verify implementation", "what's done", "implementation status", or "audit the code".
version: 1.0.0
---

# Implementation Review

> **Simplified Workflow Note**: This skill is part of the **legacy workflow**.
> In the simplified 4-step workflow (`spec → feature-draft → implementation → spec-update-done`),
> the `implementation` skill now includes **in-phase and final reviews** built in.
> A separate `implementation-review` invocation is no longer required for the standard workflow.
> This skill remains available for **standalone audits** outside the normal flow.

Review implementation progress against the implementation plan, verify acceptance criteria are met, identify issues and improvements, and provide actionable next steps.

## 하드 룰: 스펙은 절대 수정하지 않기 (중요)

- 이 스킬은 **리뷰/검증 및 리포트 생성**만 수행합니다.
- `_sdd/spec/` 아래의 스펙 파일은 **생성/수정/삭제하지 않습니다.**
- 스펙 변경이 필요하면 리포트에 **"스펙 업데이트 필요"**로만 제안하고, 실제 반영은 `/spec-update-todo`(또는 `/spec-update-done`)로 진행하도록 안내합니다.

## Language

Use Korean (한국어) for all communications with the user.
모든 내용은 한국어로 작성합니다. 

## LLM Model to use

Use the default, most capable model (e.g. Opus 4.5) to review the implementation otherwise mentioned by the user.
Report the model used at the beginning of the reviewing.

## When to Use This Skill

- After completing implementation tasks
- During implementation to check progress
- Before marking a phase or project complete
- When user asks "what's the status?" or "what's left to do?"
- To audit code quality against requirements

## Prerequisites

1. **Locate the Implementation Plan and Progress**: Check for plan at:
   - User-specified paths
   - `<project_root>/_sdd/implementation/IMPLEMENTATION_{PLAN|PROGRESS}.md`
   - Recent conversation context

If there are multiple phase plan/progress files (e.g. `IMPLEMENTATION_PLAN_PHASE_1.md`, `IMPLEMENTATION_PROGRESS_PHASE_1.md`) and the user does not specify scope, ask whether to review the latest phase only (default) or all phases.

2. **No Plan Found**: If no plan exists, inform user and suggest:
   - Creating a plan with `implementation-plan` skill
   - Doing a general code review instead

3. **Load the execution/test environment guide** before running any local checks:
   - User-specified path
   - `<project_root>/_sdd/env.md` (source of environment variables, conda env, required setup commands)
   - Recent conversation context

If `_sdd/env.md` exists, apply its setup instructions first (for example: `conda activate ...`, required `export` variables, required local services).

## Review Process Overview

```
┌─────────────────────────────────────────────────────────┐
│  1. INVENTORY: What was supposed to be built?           │
│              ↓                                          │
│  2. VERIFICATION: What is actually implemented?         │
│              ↓                                          │
│  3. ASSESSMENT: Are acceptance criteria met?            │
│              ↓                                          │
│  4. ISSUES: What problems or gaps exist?                │
│              ↓                                          │
│  5. SUMMARY: What should be done next?                  │
└─────────────────────────────────────────────────────────┘
```

## Step 1: Inventory - What Was Planned

**Tools**: `Read`, `Glob`

Parse the implementation plan to extract:

### Tasks Inventory
```markdown
For each task in the plan, record:
- Task ID and title
- Component/module
- Priority (P0-P3)
- Acceptance criteria (list each one)
- Technical notes
- Dependencies
```

### Expected Artifacts
```markdown
Based on the plan, identify expected:
- Files to be created
- Functions/classes to implement
- Tests to write
- Configuration changes
- Database migrations
```

### Output Format
```markdown
## Plan Inventory

### Tasks (20 total)
| ID | Task | Component | Priority | Criteria |
|----|------|-----------|----------|----------|
| 1 | Database schema | Auth Core | P0 | 5 |
| 2 | Password hashing | Security | P0 | 4 |
...

### Expected Deliverables
- [ ] 12 source files
- [ ] 8 test files
- [ ] 3 migrations
- [ ] API documentation
```

**Decision Gate 1→2**:
```
plan_loaded = 구현 계획 읽기 완료
tasks_extracted = Task 목록 추출 완료
artifacts_listed = 예상 산출물 목록 작성 완료

IF plan_loaded AND tasks_extracted AND artifacts_listed → Step 2 진행
ELSE IF NOT plan_loaded → 사용자에게 Plan 위치 확인
ELSE → 누락 항목 추가 추출
```

## Step 2: Verification - What Is Implemented

**Tools**: `Glob`, `Grep`, `Read`, `Bash (test runner)`

Explore the codebase to verify what exists:

### Code Verification
```
For each expected artifact:
1. Use Glob/Grep to find the file/function
2. Read the implementation
3. Compare against task description
4. Note: EXISTS / PARTIAL / MISSING
```

### Test Verification
```
For each task with test requirements:
1. Read `_sdd/env.md` and apply required setup before local test execution
2. Find corresponding test files
3. Count test cases
4. Run tests if possible (or check CI status)
5. Note: PASSING / FAILING / MISSING
```

### Output Format
```markdown
## Implementation Status

### Task Verification
| ID | Task | Code | Tests | Status |
|----|------|------|-------|--------|
| 1 | Database schema | ✓ | ✓ 6/6 | COMPLETE |
| 2 | Password hashing | ✓ | ✓ 7/7 | COMPLETE |
| 3 | JWT utilities | ✓ | ✗ 3/8 | PARTIAL |
| 4 | Rate limiting | ✗ | ✗ 0/5 | MISSING |

### Files Found
- ✓ src/utils/security.py
- ✓ src/utils/jwt.py
- ✗ src/middleware/rate_limit.py (missing)
- ✓ tests/test_security.py
- △ tests/test_jwt.py (incomplete)
```

### Step 2.5: 검증 진행 상황 요약

검증 진행 상황 요약 테이블을 사용자에게 제시한 후 바로 Step 3으로 진행한다 (사용자 확인을 기다리지 않는다):

```
| 항목 | COMPLETE | PARTIAL | MISSING |
|------|----------|---------|---------|
| Tasks | N | N | N |
| Tests | N passing | N failing | N missing |
| Files | N found | N incomplete | N missing |
```

**Decision Gate 2→3**:
```
code_verified = 코드 존재 여부 확인 완료
test_verified = 테스트 존재/통과 여부 확인 완료

IF code_verified AND test_verified → Step 3 진행
ELSE → 미확인 항목 추가 검증
```

## Step 3: Assessment - Acceptance Criteria Check

**Tools**: `Read`, `Grep`, `Bash (test runner)`

For each task, verify every acceptance criterion:

### Criterion Verification Process
```
For each acceptance criterion:
1. Understand what it requires
2. Find the code that should satisfy it
3. Check if a test exists for this criterion
4. Verify the test passes (if exists)
5. Mark: MET / NOT MET / UNTESTED
```

### Evidence Collection
```markdown
For each criterion, document:
- Location: File and line number where implemented
- Test: Test name that verifies this
- Status: MET / NOT MET / UNTESTED
- Notes: Any concerns or observations
```

### Output Format
```markdown
## Acceptance Criteria Assessment

### Task 1: Database schema

| # | Criterion | Code | Test | Status |
|---|-----------|------|------|--------|
| 1 | Users table with required fields | migrations/001.py:12 | test_users_table | MET |
| 2 | OAuth connections table | migrations/001.py:28 | test_oauth_table | MET |
| 3 | Sessions table | migrations/001.py:45 | test_sessions_table | MET |
| 4 | Proper indexes | migrations/001.py:52 | test_indexes | MET |
| 5 | Migration runs successfully | - | test_migration_runs | MET |

**Task 1 Result**: 5/5 criteria met ✓

### Task 3: JWT utilities

| # | Criterion | Code | Test | Status |
|---|-----------|------|------|--------|
| 1 | Generate valid JWT tokens | jwt.py:15 | test_generate_token | MET |
| 2 | Validate token signature | jwt.py:32 | test_validate_sig | MET |
| 3 | Check token expiry | jwt.py:45 | - | UNTESTED |
| 4 | Refresh token flow | - | - | NOT MET |
| 5 | Revoke tokens | - | - | NOT MET |

**Task 3 Result**: 2/5 criteria met ✗
```

**Severity-based Decision Gate 3→4**:
```
IF critical_criteria_not_met > 0 → Step 4에서 Critical로 분류, 즉시 보고
ELSE IF untested_criteria > total * 0.3 → Step 4에서 Quality Issues로 분류
ELSE → 정상 진행
```

## Step 4: Issues and Improvements

**Tools**: `Read`, `Grep`

### Issue Categories

#### Critical Issues (Blockers)
```markdown
Issues that prevent the feature from working:
- Missing core functionality
- Failing tests
- Security vulnerabilities
- Breaking changes
```

#### Quality Issues
```markdown
Issues that affect maintainability/reliability:
- Missing tests for implemented code
- Code doesn't follow project patterns
- Error handling gaps
- Performance concerns
```

#### Improvements (Nice to Have)
```markdown
Suggestions that aren't blocking:
- Code could be cleaner
- Additional edge case handling
- Documentation improvements
- Optimization opportunities
```

### Output Format
```markdown
## Issues Identified

### Critical (3)

1. **Task 4: Rate limiting not implemented**
   - Impact: API vulnerable to abuse
   - Required for: Production deployment
   - Action: Implement rate_limit.py middleware

2. **Task 3: Token refresh not working**
   - Location: src/utils/jwt.py
   - Issue: refresh_token() returns None
   - Test: test_refresh_token FAILING
   - Action: Fix refresh logic

3. **Security: SQL injection in user search**
   - Location: src/services/user.py:45
   - Issue: Raw query with string interpolation
   - Action: Use parameterized query

### Quality Issues (5)

1. **Missing tests for JWT expiry**
   - Location: src/utils/jwt.py:45
   - Criterion: "Check token expiry" has no test
   - Action: Add test_token_expiry

2. **Inconsistent error handling**
   - Location: src/routes/auth.py
   - Issue: Some endpoints return 400, others 422 for validation
   - Action: Standardize to 422 for validation errors

...

### Improvements (3)

1. **Consider caching user lookups**
   - Location: src/services/user.py
   - Benefit: Reduce DB queries
   - Priority: Low

...
```

## Step 5: Summary and Next Steps

**Tools**: `Write`, `Bash (mkdir -p)`, `AskUserQuestion`

### Progress Summary
```markdown
## Implementation Review Summary

### Overall Progress
- **Tasks**: 15/20 complete (75%)
- **Criteria Met**: 58/72 (81%)
- **Test Coverage**: 85%

### By Phase
| Phase | Tasks | Complete | Partial | Missing |
|-------|-------|----------|---------|---------|
| 1: Foundation | 4 | 4 | 0 | 0 |
| 2: Core Auth | 5 | 3 | 2 | 0 |
| 3: OAuth | 3 | 1 | 1 | 1 |
| 4: User Mgmt | 4 | 4 | 0 | 0 |
| 5: Testing | 4 | 3 | 1 | 0 |

### Health Indicators
- ✓ All P0 tasks complete
- ✗ 3 critical issues found
- △ 5 quality issues need attention
- ✓ No security vulnerabilities (except noted SQL injection)
```

### Next Steps (Prioritized)
```markdown
## Recommended Next Steps

### Immediate (Before any deployment)
1. [ ] Fix SQL injection in user.py:45
2. [ ] Complete rate limiting (Task 4)
3. [ ] Fix token refresh bug (Task 3)

### Before Phase Complete
4. [ ] Add missing test for JWT expiry
5. [ ] Standardize error responses
6. [ ] Complete OAuth account linking (Task 12)

### Before Production
7. [ ] Review all quality issues
8. [ ] Run security audit
9. [ ] Load testing for rate limiter

### Optional Improvements
10. [ ] Add user lookup caching
11. [ ] Improve error messages
```

## Context Management

| 스펙 크기 | 전략 | 구체적 방법 |
|-----------|------|-------------|
| < 200줄 | 전체 읽기 | `Read`로 전체 파일 읽기 |
| 200-500줄 | 전체 읽기 가능 | `Read`로 전체 읽기, 필요 시 섹션별 |
| 500-1000줄 | TOC 먼저, 관련 섹션만 | 상위 50줄(TOC) 읽기 → 관련 섹션만 `Read(offset, limit)` |
| > 1000줄 | 인덱스만, 타겟 최대 3개 | 인덱스/TOC만 읽기 → 타겟 섹션 최대 3개 선택적 읽기 |

| 코드베이스 크기 | 전략 | 구체적 방법 |
|----------------|------|-------------|
| < 50 파일 | 자유 탐색 | `Glob` + `Read` 자유롭게 사용 |
| 50-200 파일 | 타겟 탐색 | `Grep`/`Glob`으로 후보 식별 → 타겟 `Read` |
| > 200 파일 | 타겟 탐색 | `Grep`/`Glob` 위주 → 최소한의 `Read` |

## Review Output Template

Use this template for the final review output:

```markdown
# Implementation Review: [Project Name]

**Review Date**: [Date]
**Plan Location**: [Path to plan]
**Reviewer**: Claude

---

## 1. Progress Overview

### Task Completion
[Table of tasks with status]

### Acceptance Criteria
- Total criteria: X
- Met: Y (Z%)
- Not met: A
- Untested: B

---

## 2. Detailed Assessment

### Completed Tasks
[List with evidence]

### Partial Tasks
[List with what's missing]

### Missing Tasks
[List with impact]

---

## 3. Issues Found

### Critical (X)
[Detailed list]

### Quality (Y)
[Detailed list]

### Improvements (Z)
[Suggestions]

---

## 4. Test Status

### Test Summary
- Total tests: X
- Passing: Y
- Failing: Z
- Coverage: X%

### Untested Areas
[List areas without tests]

---

## 5. Recommendations

### Must Do (Blockers)
[Prioritized list]

### Should Do (Quality)
[Prioritized list]

### Could Do (Improvements)
[Optional list]

---

## 6. Conclusion

[One paragraph summary: Is the implementation ready? What's the biggest risk? What's the single most important next action?]
```

## Quick Review Mode

For a quick status check, provide abbreviated output:

```markdown
## Quick Review: [Project Name]

**Progress**: 15/20 tasks (75%)
**Criteria**: 58/72 met (81%)
**Tests**: 45 passing, 2 failing

### Blockers (3)
1. Rate limiting not implemented
2. Token refresh bug
3. SQL injection vulnerability

### Next Action
Fix SQL injection in src/services/user.py:45

Need detailed review? Say "full review"
```

## Autonomous Decision-Making

다음 상황에서는 사용자에게 묻지 않고 최선의 판단으로 자율적으로 진행한다:

- **모호한 기준**: 가용 증거를 기반으로 최선의 판단 후 UNTESTED로 표시, 판단 근거를 리포트에 기록
- **누락된 맥락**: 가용 정보로 판단, 가정 사항을 리포트에 명시
- **트레이드오프 결정**: 리스크가 낮은 쪽을 선택하고 근거를 리포트에 기록
- **범위 질문**: 구현 계획에 명시된 범위 내에서만 평가, 범위 밖 개선사항은 "Optional Improvements"로 분류

## Error Handling

| 상황 | 대응 |
|------|------|
| 구현 계획 미발견 | `implementation-plan` 먼저 실행 권장, 또는 일반 코드 리뷰 제안 |
| 테스트 실행 실패 | `_sdd/env.md` 환경 설정 확인, 실패 시 사용자에게 환경 문의 |
| `_sdd/env.md` 미존재 | 로컬 테스트 건너뛰고 코드 분석만 수행 |
| 다수 Phase 존재 | 사용자에게 범위 확인 (최신 Phase만 vs 전체) |
| Acceptance Criteria 모호 | 최선 해석 후 UNTESTED로 표시, 사용자에게 확인 |
| 보안 취약점 발견 | Critical Issues로 즉시 보고 |
| 리뷰 파일 이미 존재 | `prev/PREV_IMPLEMENTATION_REVIEW_<timestamp>.md`로 아카이브 |
| 대규모 코드베이스 | `Grep`/`Glob` 위주 탐색, 핵심 컴포넌트만 검증 |

## Integration with Other Skills

- **implementation-plan**: Reference for what should exist
- **implementation**: Use review findings to guide remaining work

## Saving report

Save the report under a user-specified file (default: `<project-root>/_sdd/implementation/IMPLEMENTATION_REVIEW.md`).
    - If the file already exists, archive it as `<project-root>/_sdd/implementation/prev/PREV_IMPLEMENTATION_REVIEW_<timestamp>.md` (create `prev/` if needed) and create a new one.
Also update implementation plan (TODOs, status, acceptance criteria) document based on the review.
