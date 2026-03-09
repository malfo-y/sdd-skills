# PR Review Checklist / PR 리뷰 체크리스트

Verification checklist used by the `pr-review` skill.

---

## Spec Compliance Verification / 스펙 준수 검증

```markdown
- [ ] Existing spec key requirements are not violated by the PR
- [ ] API contract changes maintain backward compatibility or explicitly note breaking changes
- [ ] New endpoints/components follow existing architecture patterns
- [ ] Security requirements (authentication, authorization, encryption) are met
- [ ] Data model changes are compatible with existing schemas
- [ ] Environment configuration changes match the spec's deployment requirements
```

---

## Patch Draft Verification / 패치 초안 검증

```markdown
- [ ] All Features in the patch draft are implemented in the PR
- [ ] All Improvements in the patch draft are reflected in the PR
- [ ] All Bug Fixes in the patch draft are addressed in the PR
- [ ] Corresponding code exists for each Acceptance Criterion
- [ ] Changes present in the PR but not listed in the patch draft are identified
```

---

## Test Verification / 테스트 검증

```markdown
- [ ] Before running local tests, check `_sdd/env.md` and apply environment (conda/env vars/services)
- [ ] Corresponding tests exist for each acceptance criterion
- [ ] All tests pass (CI or local)
- [ ] Test coverage for newly added code is verified
- [ ] Error path and boundary condition tests exist
```

---

## Code Quality / 코드 품질

```markdown
- [ ] Project's existing coding patterns and conventions are followed
- [ ] Error handling is properly implemented
- [ ] New environment variables/config values are documented (.env.example etc.)
- [ ] No hardcoded secrets
```

---

## Documentation / 문서화

```markdown
- [ ] New environment variables are listed in .env.example or config docs
- [ ] Breaking changes are noted in the PR description or CHANGELOG
- [ ] Request/response formats for new API endpoints are documented
- [ ] Configuration changes are reflected in the deployment guide
```

---

## Security / Performance / 보안 / 성능

```markdown
- [ ] No OWASP Top 10 vulnerabilities (SQL injection, XSS, etc.)
- [ ] Performance regression potential checked (N+1 queries, unnecessary I/O, etc.)
- [ ] Sensitive data is not exposed in logs
- [ ] Authentication/authorization logic is correctly applied
```

---

## Verdict Criteria Checklist / 판정 기준 체크리스트

### APPROVE Conditions / 승인 조건

```markdown
All items must be satisfied:
- [ ] 100% acceptance criteria met (✓)
- [ ] 0 spec violations
- [ ] All tests pass
- [ ] No security issues
- [ ] 0 blockers
```

### REQUEST CHANGES Conditions / 변경 요청 조건

```markdown
If any of the following apply:
- [ ] Acceptance criteria not met (✗) items exist
- [ ] Spec violation found
- [ ] Test failure
- [ ] Security vulnerability found
- [ ] Critical functionality bug
```

### NEEDS DISCUSSION Conditions / 논의 필요 조건

```markdown
If any of the following apply:
- [ ] Intentional spec change included (design decision needed)
- [ ] Implementation approach with trade-offs
- [ ] Requirements with ambiguous scope
- [ ] New architectural decision needed
- [ ] Significant changes not covered in the patch draft
```
