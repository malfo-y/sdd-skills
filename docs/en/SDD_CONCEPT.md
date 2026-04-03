# SDD Core Concept: Global Specs and Temporary Specs

This document explains the two-level spec model in SDD. The point is not to create more documents. The point is to separate long-lived truth from change execution.

Related documents:
- [SDD_SPEC_DEFINITION.md](SDD_SPEC_DEFINITION.md)
- [SDD_WORKFLOW.md](SDD_WORKFLOW.md)
- [sdd.md](sdd.md)

---

## 1. What the Global Spec Is

The global spec is the project's Single Source of Truth. But it is no longer treated as a full implementation inventory.

What the global spec preserves:
- the problem and high-level concept
- scope, non-goals, and guardrails
- core design and key decisions
- `Contract / Invariants / Verifiability`
- decision-bearing structure
- expected usage and outcomes

In other words, the global spec is not "everything in the codebase written again." It is the durable reference that keeps humans and agents aligned.

### What to Keep vs What Not to Force

| Keep | Do not force as default body structure |
|------|----------------------------------------|
| high-level concept | full implementation inventory |
| scope / non-goals / guardrails | exhaustive component narration |
| key decisions | code copied into prose |
| CIV | local implementation detail |
| decision-bearing structure | low-signal file lists |

---

## 2. What a Temporary Spec Is

A temporary spec is not a summary of the global spec. It is an execution blueprint for a change.

Canonical seven sections:
- Change Summary
- Scope Delta
- Contract/Invariant Delta
- Touchpoints
- Implementation Plan
- Validation Plan
- Risks / Open Questions

Its job is to:
- fix the change boundary
- make contract and invariant deltas explicit
- expose the relevant code touchpoints
- connect validation directly to the delta

That is why a temporary spec is closer to an execution artifact than a permanent reference.

---

## 3. Why the Two Spec Types Are Asymmetric

Humans and LLMs do not need the same information density.

- Humans need concept, scope, and guardrails first.
- LLMs can inspect code quickly, so persistent prose does not need to explain every implementation detail.
- Both still benefit from explicit contracts, invariants, verification, and strategic code-entry hints.

So SDD intentionally adopts this asymmetry:

- global spec: thin durable reference
- temporary spec: delta- and execution-heavy blueprint

---

## 4. Lifecycle

### Medium-Scale Path

```text
feature-draft -> implementation -> spec-update-done
```

- `feature-draft` creates the temporary spec and implementation plan together.
- after implementation, `spec-update-done` syncs persistent truth back into the global spec

### Large-Scale Path

```text
feature-draft -> spec-update-todo -> implementation-plan -> implementation -> implementation-review -> spec-update-done
```

- `spec-update-todo` can register planned persistent information in advance
- `implementation-plan` expands delta and validation linkage into phases and tasks
- `implementation-review` verifies the plan against actual implementation

---

## 5. Artifact Types

### Persistent Documents

| Location | Role |
|----------|------|
| `_sdd/spec/` | global spec and supporting spec |
| `_sdd/env.md` | environment and verification hints |
| `_sdd/spec/decision_log.md` | durable decision records |

### Execution Artifacts

| Location | Role |
|----------|------|
| `_sdd/drafts/` | temporary spec drafts |
| `_sdd/implementation/` | plans, progress, reports, reviews |
| `_sdd/discussion/` | discussion handoffs |
| `_sdd/guides/` | feature guides |

Operating rule:
- the normal path treats global spec sync as a skillchain operation
- temporary specs and plans exist to drive execution, then get archived or absorbed into later steps

---

## 6. Summary

In one sentence:

> The global spec fixes long-lived truth, and the temporary spec fixes the execution blueprint for the current change.

This asymmetry is what lets SDD reduce drift without turning documentation into an implementation dump.
