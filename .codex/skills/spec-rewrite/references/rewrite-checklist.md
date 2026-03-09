# Spec Rewrite Checklist

Checklist to reduce omissions when turning an existing spec into an exploration-first spec.

## 1) Pre-Check

- [ ] Identify the main target spec file (`_sdd/spec/main.md` or `_sdd/spec/<project>.md`)
- [ ] Collect linked sub-spec files
- [ ] Confirm backup policy (`_sdd/spec/prev/PREV_<filename>_<timestamp>.md`)
- [ ] Load `_sdd/spec/DECISION_LOG.md` if present
- [ ] Check whether the main spec already uses stable anchors (`Goal`, `Architecture Overview`, `Component Details`, `Open Questions`)
- [ ] Check whether the current spec is hard to navigate, not merely long

## 2) Navigation Diagnosis

- [ ] Can a newcomer understand the project purpose within 5 minutes?
- [ ] Is system boundary visible?
- [ ] Is there a repository map?
- [ ] Is there a runtime map?
- [ ] Does the runtime map explain the user/operator-facing flow, not only arrows?
- [ ] Is there a component index?
- [ ] Do major components have `Overview` for behavior and design intent?
- [ ] Are major components tied to real paths or symbols?
- [ ] Are change/debug entry points visible?
- [ ] Are invariants and risks visible?
- [ ] Are unknowns separated into `Open Questions`?

## 3) Rewrite Target Shape

Keep these in the main spec:
- Goal -> Project Snapshot / Key Features / Non-Goals
- Architecture Overview -> System Boundary / Repository Map / Runtime Map
- Component Details -> Component Index + brief component summaries + Overview
- Usage Examples -> Running / Common Operations / Common Change Paths
- Open Questions

Split out by responsibility when needed:
- auth
- billing
- jobs
- ingestion
- api

Move out of the main flow only when necessary:
- long execution logs
- repeated tables
- reference-only detail
- low-value historical narrative

## 4) Split Rules

- [ ] Prefer `main.md + <component>.md` over numbered topic files
- [ ] Each split file has one responsibility
- [ ] Every split file is reachable from the main spec
- [ ] Links are valid
- [ ] Naming is consistent
- [ ] Appendix files exist only when truly useful

## 5) Rationale and Unknowns

- [ ] Important removed rationale is preserved in `_sdd/spec/DECISION_LOG.md`
- [ ] Unverified claims are moved to `Open Questions`
- [ ] No uncertain statement is left as confident prose

## 6) Exit Criteria

- [ ] The main spec works as a 5-minute entry point
- [ ] Repository Map exists
- [ ] Runtime Map exists
- [ ] Component Index exists
- [ ] Major components include `Overview`
- [ ] Common Change Paths exists (or equivalent change guide)
- [ ] Important areas include real paths or symbols
- [ ] Tests/logs/debug entry points are discoverable
- [ ] Duplication is reduced
- [ ] Main risks and invariants are visible
- [ ] The rewritten spec is easier to understand and easier to modify against
