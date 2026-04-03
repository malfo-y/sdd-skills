# Spec-Driven Development (SDD)

In the AI agent era, faster code generation is not enough. What matters is whether humans and agents keep making decisions from the same source of truth. SDD fixes that source in a spec.

Related documents:
- [SDD_SPEC_DEFINITION.md](SDD_SPEC_DEFINITION.md)
- [SDD_CONCEPT.md](SDD_CONCEPT.md)
- [SDD_WORKFLOW.md](SDD_WORKFLOW.md)

---

## 1. Why SDD Exists

Agent-assisted development keeps running into the same three failures:

### Interpretation Drift

The same requirement leads to different implementation choices depending on who or what is doing the work.

### Context Compression Failure

As the codebase grows, agents miss existing patterns, boundaries, and decisions. They duplicate logic or break conventions.

### Hallucinated Contracts

Non-existent APIs, vague I/O, and incorrect guarantees get turned into plausible-looking code.

SDD does not solve this by asking for better prompts alone. It externalizes intent, boundaries, and verification into the spec.

---

## 2. What the Spec Controls

An SDD spec acts as a control plane. It fixes:

- the high-level concept
- scope / non-goals / guardrails
- core design and key decisions
- Contract / Invariants / Verifiability
- expected outcomes
- decision-bearing structure

The point is not to document every implementation detail. The point is to preserve the information that future changes still need.

---

## 3. Why CIV Matters

`Contract / Invariants / Verifiability` is the central quality gate in SDD.

### Contract

What goes in, what comes out, what must be true before execution, what must be true after execution, and what must still be guaranteed in failure.

### Invariants

The system or domain rules that must survive future changes.

### Verifiability

The link from each contract or invariant to a real verification path.

This shifts review from "does this look plausible?" to "does this satisfy the contract?"

---

## 4. Why Humans and LLMs Need Different Density

Humans need:

- concept
- scope
- non-goals
- guardrails
- decisions

LLMs can inspect code quickly, so long-lived prose does not need to preserve every implementation explanation. But they still benefit from:

- contracts
- invariants
- verification linkage
- strategic code-entry hints

That is why SDD keeps the global spec thin and uses strategic code maps only as appendix-level navigation hints.

---

## 5. Global Specs and Temporary Specs

### Global Spec

The global spec is the durable reference.

- Background and high-level concept
- Scope / Non-goals / Guardrails
- Core design and key decisions
- Contract / Invariants / Verifiability
- Usage guide & expected results
- Decision-bearing structure

### Temporary Spec

The temporary spec is the execution blueprint.

- Change Summary
- Scope Delta
- Contract/Invariant Delta
- Touchpoints
- Implementation Plan
- Validation Plan
- Risks / Open Questions

They share a conceptual core, but their density and role are intentionally different.

---

## 6. The Operating Loop

The basic SDD loop is:

```text
requirements -> temporary spec / plan -> implementation -> verification -> global spec sync
```

For large work:

```text
feature-draft -> spec-update-todo -> implementation-plan -> implementation -> implementation-review -> spec-update-done
```

For medium work:

```text
feature-draft -> implementation -> spec-update-done
```

In practice, `/sdd-autopilot` usually orchestrates this loop automatically.

---

## 7. Adoption Principles

Adopting SDD does not mean "write more docs."

- keep the global spec thin
- make CIV explicit
- treat temporary specs as execution blueprints
- do not let docs drift away from actual skill behavior
- when the canonical model changes, follow `definition -> skills -> docs -> mirrors/examples`

In short, SDD is not a documentation-heavy process. It is an operating model that keeps humans and agents working under the same contracts.
