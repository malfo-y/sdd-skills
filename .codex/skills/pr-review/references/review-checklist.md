# PR Review Checklist

Verification checklist used by the `pr-review` skill.

---

## Code-only Verification (항상 실행)

### Code Quality
```markdown
- [ ] Project's existing coding patterns and conventions are followed
- [ ] Error handling is properly implemented
- [ ] New environment variables/config values are documented (.env.example etc.)
- [ ] No hardcoded secrets
```

### Test Verification
```markdown
- [ ] Before running local tests, check `_sdd/env.md` and apply environment (conda/env vars/services)
- [ ] Corresponding tests exist for new/changed functionality
- [ ] All tests pass (CI or local)
- [ ] Test coverage for newly added code is verified
- [ ] Error path and boundary condition tests exist
```

### Security / Performance
```markdown
- [ ] No OWASP Top 10 vulnerabilities (SQL injection, XSS, etc.)
- [ ] Performance regression potential checked (N+1 queries, unnecessary I/O, etc.)
- [ ] Sensitive data is not exposed in logs
- [ ] Authentication/authorization logic is correctly applied
```

### Documentation
```markdown
- [ ] New environment variables are listed in .env.example or config docs
- [ ] Breaking changes are noted in the PR description or CHANGELOG
- [ ] Request/response formats for new API endpoints are documented
- [ ] Configuration changes are reflected in the deployment guide
```

---

## Spec-based Verification (from-branch에 spec 존재 시 추가)

### Spec AC Verification
```markdown
- [ ] All Features in the spec are implemented in the PR
- [ ] All Improvements in the spec are reflected in the PR
- [ ] All Bug Fixes in the spec are addressed in the PR
- [ ] Corresponding code exists for each Acceptance Criterion
```

### Spec Compliance
```markdown
- [ ] Existing spec key requirements are not violated by the PR
- [ ] API contract changes maintain backward compatibility or explicitly note breaking changes
- [ ] New endpoints/components follow existing architecture patterns
- [ ] Security requirements (authentication, authorization, encryption) are met
- [ ] Data model changes are compatible with existing schemas
```

---

## Verdict Criteria

Canonical verdict criteria live in `../SKILL.md` Step 4. Apply that table after collecting both reviewer returns; do not maintain a second verdict list here.
