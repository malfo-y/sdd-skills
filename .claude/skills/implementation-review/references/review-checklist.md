# Implementation Review Checklists

## Pre-Review Checklist

Before starting the review:

```markdown
- [ ] Implementation plan is located and readable
- [ ] Codebase is accessible
- [ ] Test suite can be run (or CI results available)
- [ ] Clear on review scope (full review vs specific phase)
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
