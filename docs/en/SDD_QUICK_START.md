# SDD Quick Start Guide

This is the shortest path into the current SDD model.

Related documents:
- [SDD_SPEC_DEFINITION.md](SDD_SPEC_DEFINITION.md)
- [SDD_CONCEPT.md](SDD_CONCEPT.md)
- [SDD_WORKFLOW.md](SDD_WORKFLOW.md)

---

## 1. Remember These Four Things

1. The global spec is a thin durable reference.
2. A temporary spec is an execution blueprint for change.
3. `Contract / Invariants / Verifiability` is the shared quality gate.
4. Canonical changes follow `definition -> skills -> docs -> mirrors/examples`.

---

## 2. Pick a Starting Point

| Situation | Start with |
|-----------|------------|
| Most feature work | `/sdd-autopilot` |
| Direction or requirements are unclear | `/discussion` |
| No spec exists yet | `/spec-create` |
| A legacy spec must be migrated | `/spec-upgrade` |
| You need a fast overview of the current spec | `/spec-summary` |

---

## 3. Global Spec vs Temporary Spec

### Global Spec

The global spec keeps:

- Background and high-level concept
- Scope / Non-goals / Guardrails
- Core design and key decisions
- Contract / Invariants / Verifiability
- Usage guide & expected results
- Decision-bearing structure

Only add support sections when they are actually needed:

- data model / API / environment and configuration
- Strategic Code Map appendix

### Temporary Spec

The temporary spec uses:

- Change Summary
- Scope Delta
- Contract/Invariant Delta
- Touchpoints
- Implementation Plan
- Validation Plan
- Risks / Open Questions

---

## 4. Most Common Paths

### Default Path

```bash
/sdd-autopilot Implement this feature: [feature description]
```

### Manual Paths

Large:

```text
feature-draft -> spec-update-todo -> implementation-plan -> implementation -> implementation-review -> spec-update-done
```

Medium:

```text
feature-draft -> implementation -> spec-update-done
```

Small:

```text
direct implementation -> optional implementation-review / spec-update-done
```

---

## 5. Good Input

At minimum, include:

- What: what is changing
- Why: why it is needed
- Constraints: what boundaries apply

Example:

```text
/feature-draft
When a user uploads a CSV, auto-parse it and bulk-insert into the users table.
- Max 10MB
- Column mapping stays manual in the UI
- Skip invalid rows and emit a report
```

---

## 6. Where to Read More

- Spec definition: [SDD_SPEC_DEFINITION.md](SDD_SPEC_DEFINITION.md)
- Two-level model: [SDD_CONCEPT.md](SDD_CONCEPT.md)
- Full workflow: [SDD_WORKFLOW.md](SDD_WORKFLOW.md)
- Philosophy and operating model: [sdd.md](sdd.md)
