# Implementation Review Checklists

## Tier Detection Checklist

Before starting the review, determine which tier to use:

```markdown
### Step 1: Plan Detection
- [ ] Check _sdd/implementation/IMPLEMENTATION_PLAN*.md
- [ ] Check user-specified paths
- [ ] Check recent conversation context

### Step 2: Plan Validation (if found)
- [ ] Plan의 Task 목록이 참조하는 파일이 코드베이스에 존재하는가?
- [ ] Plan이 참조하는 Spec과 현재 _sdd/spec/ 내용이 일치하는가?
- [ ] Plan 이후 대규모 코드 변경이 없었는가? (git log 확인)
- Result: 정합성 OK → Tier 1 / 불일치 → Tier 2 fallback

### Step 3: Spec Detection (if no valid plan)
- [ ] Check _sdd/spec/ directory exists and has files
- Result: Spec 있음 → Tier 2 / Spec 없음 → Tier 3

### Determined Tier: [ 1 / 2 / 3 ]
```

## Pre-Review Checklist

### Tier 1 (Plan-based)
```markdown
- [ ] Implementation plan is located and readable
- [ ] Plan과 코드베이스 정합성 확인됨
- [ ] Codebase is accessible
- [ ] `_sdd/env.md` is checked and required runtime/test setup is applied
- [ ] Test suite can be run (or CI results available)
- [ ] Clear on review scope (full review vs specific phase)
```

### Tier 2 (Spec-based)
```markdown
- [ ] Spec files located in _sdd/spec/
- [ ] Spec 구조 판별됨 (구조화 / 비구조화)
- [ ] Codebase is accessible
- [ ] `_sdd/env.md` is checked (if exists)
- [ ] Test suite can be run (or CI results available)
```

### Tier 3 (Code quality)
```markdown
- [ ] Codebase is accessible
- [ ] git log/diff로 최근 변경 범위 확인됨
- [ ] `_sdd/env.md` is checked (if exists)
- [ ] Test suite can be run (or CI results available)
- [ ] 리뷰 범위 결정됨 (기본: 최근 2주 변경)
```

## Task Verification Checklist

For each task in the plan:

```markdown
### Task [N]: [Title]

#### Code Verification
- [ ] Expected files exist
- [ ] Functions/classes mentioned in task are implemented
- [ ] Code follows project patterns
- [ ] No obvious bugs or issues

#### Test Verification
- [ ] Test file exists
- [ ] Tests cover each acceptance criterion
- [ ] Tests are passing
- [ ] Test names are descriptive

#### Acceptance Criteria
For each criterion:
- [ ] Criterion [1]: [Description]
  - Evidence: [file:line]
  - Test: [test name]
  - Status: MET / NOT MET / UNTESTED
```

## Code Quality Checklist

When reviewing implementation code:

### Security
```markdown
- [ ] No SQL injection vulnerabilities (parameterized queries)
- [ ] No XSS vulnerabilities (output encoding)
- [ ] Authentication properly implemented
- [ ] Authorization checks in place
- [ ] Secrets not hardcoded
- [ ] Input validation on all endpoints
- [ ] CSRF protection where needed
```

### Error Handling
```markdown
- [ ] Errors are caught and handled appropriately
- [ ] Error messages are helpful but not leaky
- [ ] Consistent error response format
- [ ] Logging for debugging
- [ ] Graceful degradation where appropriate
```

### Code Patterns
```markdown
- [ ] Follows existing project conventions
- [ ] Consistent naming
- [ ] No code duplication
- [ ] Appropriate abstraction level
- [ ] Dependencies properly managed
```

### Performance
```markdown
- [ ] No obvious N+1 queries
- [ ] Appropriate indexes in place
- [ ] No blocking operations in async code
- [ ] Resource cleanup (connections, files)
```

## Test Quality Checklist

When reviewing tests:

### Coverage
```markdown
- [ ] Happy path tested
- [ ] Error cases tested
- [ ] Edge cases tested
- [ ] Boundary conditions tested
```

### Test Quality
```markdown
- [ ] Tests are independent (no shared state)
- [ ] Tests are deterministic (no flaky tests)
- [ ] Tests are fast (or appropriately marked slow)
- [ ] Tests use appropriate assertions
- [ ] Test names describe the behavior
```

### TDD Verification
```markdown
- [ ] Each acceptance criterion has a test
- [ ] Tests would have failed before implementation
- [ ] Tests aren't testing implementation details
```

## Issue Severity Classification

### Critical (Must Fix)
```markdown
Criteria for Critical:
- [ ] Security vulnerability
- [ ] Data loss possible
- [ ] Core functionality broken
- [ ] Failing tests that block deployment
- [ ] Missing required feature (P0 task)
```

### Quality (Should Fix)
```markdown
Criteria for Quality:
- [ ] Missing tests for implemented code
- [ ] Inconsistent behavior
- [ ] Poor error handling
- [ ] Non-blocking bugs
- [ ] Technical debt that will grow
```

### Improvement (Could Fix)
```markdown
Criteria for Improvement:
- [ ] Performance optimization opportunity
- [ ] Code readability enhancement
- [ ] Documentation improvement
- [ ] Nice-to-have feature
```

## Review Output Checklist

Before presenting findings:

```markdown
- [ ] All tasks have been verified
- [ ] All acceptance criteria checked
- [ ] Issues are categorized by severity
- [ ] Each issue has:
  - [ ] Clear description
  - [ ] Location (file:line)
  - [ ] Evidence/example
  - [ ] Recommended action
- [ ] Next steps are prioritized
- [ ] Summary includes:
  - [ ] Progress metrics
  - [ ] Biggest risk
  - [ ] Single most important action
```

## Quick Review Checklist

For fast status checks:

```markdown
1. [ ] Count completed vs total tasks
2. [ ] Run test suite - note failures
3. [ ] Check for any P0 tasks incomplete
4. [ ] Identify top 3 blockers
5. [ ] State single next action
```

## Phase Sign-off Checklist

Before marking a phase complete:

```markdown
### Phase [N]: [Name]

#### Completion
- [ ] All tasks in phase marked complete
- [ ] All acceptance criteria met
- [ ] All tests passing

#### Quality
- [ ] No critical issues open
- [ ] Quality issues documented (if deferring)
- [ ] Code review completed

#### Documentation
- [ ] API documentation updated
- [ ] README updated if needed
- [ ] Deployment notes if needed

#### Sign-off
- [ ] Ready for next phase: YES / NO
- [ ] Blockers: [list or "none"]
```

## Common Issues to Look For

### Authentication/Authorization
```markdown
- Missing auth checks on protected routes
- Insecure token storage
- Password requirements not enforced
- Session fixation vulnerabilities
- OAuth state parameter missing
```

### Data Handling
```markdown
- SQL injection (string interpolation in queries)
- Missing input validation
- Improper error messages exposing internals
- Sensitive data in logs
- Missing data sanitization
```

### API Design
```markdown
- Inconsistent status codes
- Missing rate limiting
- No pagination on list endpoints
- Improper HTTP methods
- Missing CORS configuration
```

### Testing Gaps
```markdown
- No tests for error paths
- Missing edge case tests
- Integration tests missing
- No tests for async behavior
- Flaky tests ignored
```

## Tier 2: Spec Alignment Checklist

When reviewing against spec (no plan):

### Spec Analysis
```markdown
- [ ] Spec 구조 판별 완료 (구조화 / 비구조화)
- [ ] 요구사항 추출 완료 (구조화) 또는 핵심 의도 파악 (비구조화)
- [ ] 추출된 요구사항을 검증 체크리스트로 정리
```

### Alignment Assessment
```markdown
For each extracted requirement:
- [ ] 관련 코드 탐색 완료
- [ ] 구현 상태 판정: ALIGNED / DRIFT / MISSING
- [ ] DRIFT인 경우: 구체적 불일치 내용 기록
- [ ] MISSING인 경우: 영향도 평가
```

### Stale Plan Detection (Tier 1 → Tier 2 fallback 시)
```markdown
- [ ] 리포트에 ⚠️ Stale Plan detected 메시지 포함
- [ ] Stale 판단 근거 기록 (어떤 불일치가 발견되었는지)
- [ ] Spec 기반 리뷰로 전환된 사실 명시
```

## Tier 3: Code Quality Review Checklist

When reviewing without plan or spec:

### Scope Definition
```markdown
- [ ] git log로 최근 변경 범위 확인
- [ ] 변경된 파일 목록 추출
- [ ] 리뷰 범위 결정 (소규모/중규모/대규모)
- [ ] Assumptions 섹션에 범위 결정 근거 기록
```

### Code Quality Focus Areas
```markdown
- [ ] 보안: 하드코딩된 시크릿, injection, 인증/인가
- [ ] 에러 처리: 일관성, 로깅, 예외 처리
- [ ] 코드 패턴: 컨벤션 준수, 중복, 복잡도
- [ ] 성능: N+1 쿼리, 블로킹, 리소스 정리
- [ ] 테스트: 변경 코드 대비 테스트 존재 여부
```

### Tier 3 Output Requirements
```markdown
- [ ] Assumptions 섹션 포함 (Plan/Spec 미존재, 리뷰 범위, 한계)
- [ ] 후속 스킬 안내 포함 (spec-create, implementation-plan)
```

## Review Report Template

```markdown
# Implementation Review Report

## Executive Summary
- **Project**: [Name]
- **Review Date**: [Date]
- **Progress**: [X]% complete
- **Status**: READY / NEEDS WORK / BLOCKED

## Key Findings

### What's Working Well
1. [Positive finding]
2. [Positive finding]

### Critical Issues
1. [Issue with action]
2. [Issue with action]

### Recommendations
1. [Priority 1 action]
2. [Priority 2 action]

## Detailed Findings
[Full assessment]

## Metrics
| Metric | Value |
|--------|-------|
| Tasks Complete | X/Y |
| Criteria Met | X/Y |
| Tests Passing | X/Y |
| Coverage | X% |

## Next Steps
1. [ ] [Action item]
2. [ ] [Action item]
```
