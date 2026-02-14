# Implementation Review Checklist (Phase + Final)

Use this checklist for built-in review steps inside the `implementation` skill.

## Security

- [ ] No obvious injection risk in DB/query paths
- [ ] Authentication/authorization boundaries are enforced
- [ ] No hardcoded secrets in code/tests/config
- [ ] Input validation exists for external-facing entry points

## Error Handling

- [ ] Error responses are consistent
- [ ] Failure paths are handled explicitly
- [ ] Logs are actionable and not overly leaky

## Code Patterns

- [ ] Naming follows repository conventions
- [ ] No avoidable duplication across tasks/phases
- [ ] Abstractions match project style

## Performance

- [ ] No obvious N+1 query patterns
- [ ] Required indexes exist for new heavy queries
- [ ] Async paths avoid blocking calls

## Test Quality

- [ ] Happy path and failure path covered
- [ ] Edge/boundary cases covered for core behavior
- [ ] Tests are deterministic and independent
- [ ] Critical paths have regression protection

## Cross-Task / Cross-Phase Integration

- [ ] Components implemented in different tasks integrate correctly
- [ ] Data/contracts are consistent across module boundaries
- [ ] Final behavior matches plan intent end-to-end

## Severity Gate

- **Critical**: must fix before proceeding/finalizing
- **Quality**: document and proceed
- **Improvement**: optional backlog item

