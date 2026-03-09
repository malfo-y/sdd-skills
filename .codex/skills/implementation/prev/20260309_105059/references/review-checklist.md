# Implementation Review Checklists / 구현 리뷰 체크리스트

These checklists are used during **Phase Review** (Step 6) and **Final Review** (Step 7) of the parallel implementation process. They focus on cross-cutting quality concerns that TDD alone cannot catch — security, error handling, code patterns, performance, and test quality.

> **Note**: Task-level verification (acceptance criteria, file existence, test coverage per criterion) is already tracked during TDD implementation (Step 4). These checklists cover what remains after TDD.

## Code Quality Checklist / 코드 품질 체크리스트

When reviewing implementation code:

### Security / 보안
```markdown
- [ ] No SQL injection vulnerabilities (parameterized queries)
- [ ] No XSS vulnerabilities (output encoding)
- [ ] Authentication properly implemented
- [ ] Authorization checks in place
- [ ] Secrets not hardcoded
- [ ] Input validation on all endpoints
- [ ] CSRF protection where needed
```

### Error Handling / 에러 처리
```markdown
- [ ] Errors are caught and handled appropriately
- [ ] Error messages are helpful but not leaky
- [ ] Consistent error response format
- [ ] Logging for debugging
- [ ] Graceful degradation where appropriate
```

### Code Patterns / 코드 패턴
```markdown
- [ ] Follows existing project conventions
- [ ] Consistent naming
- [ ] No code duplication
- [ ] Appropriate abstraction level
- [ ] Dependencies properly managed
```

### Performance / 성능
```markdown
- [ ] No obvious N+1 queries
- [ ] Appropriate indexes in place
- [ ] No blocking operations in async code
- [ ] Resource cleanup (connections, files)
```

## Test Quality Checklist / 테스트 품질 체크리스트

When reviewing tests:

### Coverage / 커버리지
```markdown
- [ ] Happy path tested
- [ ] Error cases tested
- [ ] Edge cases tested
- [ ] Boundary conditions tested
```

### Test Quality / 테스트 품질
```markdown
- [ ] Tests are independent (no shared state)
- [ ] Tests are deterministic (no flaky tests)
- [ ] Tests are fast (or appropriately marked slow)
- [ ] Tests use appropriate assertions
- [ ] Test names describe the behavior
```

### TDD Verification / TDD 검증
```markdown
- [ ] Each acceptance criterion has a test
- [ ] Tests would have failed before implementation
- [ ] Tests aren't testing implementation details
```

## Parallel Execution Checklist / 병렬 실행 체크리스트

Additional checks specific to parallel sub-agent execution:

### Cross-Agent Consistency / 에이전트 간 일관성
```markdown
- [ ] Naming conventions consistent across sub-agent outputs
- [ ] Error handling patterns consistent across sub-agents
- [ ] No conflicting imports or dependency versions
- [ ] Shared utilities used consistently
```

### File Boundary Compliance / 파일 경계 준수
```markdown
- [ ] Each sub-agent only modified its Target Files
- [ ] No unauthorized file modifications
- [ ] Read-only files were not modified
```

### Integration / 통합
```markdown
- [ ] Sub-agent outputs work together without conflicts
- [ ] Shared interfaces are compatible
- [ ] No duplicate code across sub-agent outputs
```

## Issue Severity Classification / 이슈 심각도 분류

### Critical (Must Fix Before Next Phase) / 치명적 (다음 Phase 전 필수 수정)
```markdown
Criteria for Critical:
- [ ] Security vulnerability
- [ ] Data loss possible
- [ ] Core functionality broken
- [ ] Failing tests that block deployment
- [ ] Missing required feature (P0 task)
```

### Quality (Document, Proceed) / 품질 (기록 후 진행)
```markdown
Criteria for Quality:
- [ ] Missing tests for implemented code
- [ ] Inconsistent behavior
- [ ] Poor error handling
- [ ] Non-blocking bugs
- [ ] Technical debt that will grow
```

### Improvement (Note for Later) / 개선 (추후 참고)
```markdown
Criteria for Improvement:
- [ ] Performance optimization opportunity
- [ ] Code readability enhancement
- [ ] Documentation improvement
- [ ] Nice-to-have feature
```

## Common Issues to Look For / 주요 점검 항목

### Authentication/Authorization / 인증/인가
```markdown
- Missing auth checks on protected routes
- Insecure token storage
- Password requirements not enforced
- Session fixation vulnerabilities
- OAuth state parameter missing
```

### Data Handling / 데이터 처리
```markdown
- SQL injection (string interpolation in queries)
- Missing input validation
- Improper error messages exposing internals
- Sensitive data in logs
- Missing data sanitization
```

### API Design / API 설계
```markdown
- Inconsistent status codes
- Missing rate limiting
- No pagination on list endpoints
- Improper HTTP methods
- Missing CORS configuration
```

### Testing Gaps / 테스트 공백
```markdown
- No tests for error paths
- Missing edge case tests
- Integration tests missing
- No tests for async behavior
- Flaky tests ignored
```
