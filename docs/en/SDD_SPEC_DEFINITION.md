# What Is a Spec in SDD?

This document defines what a spec means in SDD, why it is more than simple documentation, and what structure and qualities it should have.

Related documents:
- [SDD_CONCEPT.md](SDD_CONCEPT.md)
- [SDD_WORKFLOW.md](SDD_WORKFLOW.md)
- [sdd.md](sdd.md)

---

## 1. Why Define the Spec Explicitly?

In SDD, a spec is not just another document. When humans and AI agents build software together, the spec is the anchor that fixes what should be built, why it should be built that way, and what must not be broken.

Without an explicit definition, the same problems keep returning:

- the spec collapses into a feature list or API list
- design intent disappears, so people and agents keep re-deriving it
- expected results become vague, so review and verification drift
- code and documentation lose their connection

That is why SDD needs a clear definition of what belongs in a spec.

---

## 2. What a Spec Is Not

An SDD spec should not be reduced to:

- a simple checklist
- an API, CLI, or config reference dump
- a report written only after implementation
- a manual that merely repeats facts already visible in the code

Those artifacts can still be useful, but they are not enough to preserve intent, boundaries, or verification.

---

## 3. What a Spec Is

In SDD, a spec has the following character:

> A spec is a whitepaper-style Single Source of Truth that aligns humans and AI by capturing the problem, high-level concept, scope, non-goals, guardrails, key decisions, Contract / Invariants / Verifiability, expected results, and, when needed, strategic hints for entering the code.

That means a spec must do all of the following:

- explain the problem and concept
- fix scope and boundaries
- declare guardrails and protected decisions
- describe the core design
- make contracts and invariants explicit
- provide implementation entry hints when useful
- guide usage and verification

The important point is that an SDD spec is not a full implementation inventory. It is a high-signal reference that reduces guesswork.

---

## 4. Why Whitepaper Style?

Whitepaper style matters because humans and agents do not need the same information density.

- Humans need background, concept, scope, and guardrails before they can reason well.
- LLMs can inspect code quickly, so they do not need every implementation detail preserved in persistent prose.
- Reviewers need explicit contracts, expected results, and code-entry hints to verify changes.

So the whitepaper shape is not an aesthetic choice. It is a structural choice that preserves intent without turning the global spec into an implementation encyclopedia.

---

## 5. Mapping Paper Elements to SDD Specs

| Paper element | SDD counterpart |
|---------------|-----------------|
| Abstract | Project overview, high-level concept, core value |
| Introduction / Motivation | Background, problem framing, reason for existence |
| Related Work | Alternative approaches and why this one was chosen |
| Core Method / Algorithm | Core design, preserved structure, key decisions |
| Implementation Details | Decision-bearing structure, temporary-spec touchpoints and implementation plan, or appendix-level strategic code map |
| Experiments | Usage scenarios, validation plan, verification scenarios |
| Results | Expected outcomes, observable behavior, failure guarantees |
| References | Code citations, related docs, appendix references |

The goal is not to imitate academic formatting literally. The goal is to translate explanatory structure into a code-centered operating model.

---

## 6. What an SDD Spec Must Contain

All specs share a common core, but global specs and temporary specs have different density.

### 1) Shared core

#### a. Background and high-level concept

- the problem being solved
- why it matters now
- how this project should be understood
- why this approach was chosen

#### b. Scope / Non-goals / Guardrails

- what the system provides
- what responsibilities it owns
- what it intentionally does not do
- what constraints and prohibitions must hold

Scope is not just a feature list. It is a boundary declaration.

#### c. Core design and key decisions

- the central system idea
- the main logic shape
- why the structure looks this way
- which decisions should survive future changes

#### d. Contract / Invariants / Verifiability

This axis becomes more important as the persistent spec gets thinner.

For global specs, the canonical shape is:

**Contract**

| ID | Subject | Inputs/Outputs | Preconditions | Postconditions | Failure Guarantees |
|----|---------|----------------|---------------|----------------|--------------------|
| C1 | ... | ... | ... | ... | ... |

**Invariants**

| ID | Scope | Invariant | Why It Matters |
|----|-------|-----------|----------------|
| I1 | ... | ... | ... |

**Verifiability**

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, I1 | test | ... |

Rules:
- keep the cells short and normative
- use verification enum values: `test`, `review`, `runtime-check`, `manual-check`
- keep ID linkage explicit even if multi-value surface formatting stays flexible

In temporary specs, the same meaning appears as `Contract/Invariant Delta` and `Validation Plan`.

#### e. Usage guide and expected results

- where the system is used
- what results should appear
- what is guaranteed in failure or edge cases

### 2) Additional requirements for global specs

#### a. Decision-bearing structure

Global specs should preserve structural judgments such as:

- system boundaries
- ownership
- cross-component contracts
- extension points
- invariant hotspots

This is different from keeping a full component inventory.

#### b. Supporting reference information

- data model
- API reference
- environment and configuration

#### c. Appendix-level strategic code map

The spec should connect to code, but it should not duplicate the codebase. A strategic code map should stay in an appendix or later support section and focus on:

- entrypoints
- invariant hotspots
- extension points
- change hotspots

### 3) Additional requirements for temporary specs

A temporary spec is an execution blueprint, not a compressed copy of the global spec.

Its canonical sections are:

- Change Summary
- Scope Delta
- Contract/Invariant Delta
- Touchpoints
- Implementation Plan
- Validation Plan
- Risks / Open Questions

Important rules:

- `Touchpoints` is mandatory
- `Validation Plan` should link directly to delta IDs
- invariant changes should be explicit, not hidden inside generic contract prose

---

## 7. Recommended Shapes

Global spec:

```markdown
# Project Global Spec

## 1. Background and high-level concept
## 2. Scope / Non-goals / Guardrails
## 3. Core design and key decisions
## 4. Contract / Invariants / Verifiability
## 5. Usage guide & expected results
## 6. Decision-bearing structure
## 7. Reference information
### Data model
### API reference
### Environment and configuration

## Appendix A. Strategic Code Map
## Appendix B. Related docs and code references
```

Temporary spec:

```markdown
# Feature Temporary Spec

## 1. Change Summary
## 2. Scope Delta
## 3. Contract/Invariant Delta
## 4. Touchpoints
## 5. Implementation Plan
## 6. Validation Plan
## 7. Risks / Open Questions
```

Architecture details or component details are not banned. They are simply no longer forced as the default top-level body shape.

---

## 8. How Specs Connect to Code

An SDD spec should talk to the codebase directly.

Recommended principles:

- cite real code when it materially supports the explanation
- prefer navigation hints over large implementation dumps
- use appendices for supporting code references
- keep the global body focused on decisions and contracts

Humans need orientation. LLMs need grounding. A good spec serves both without becoming a duplicate code tour.

---

## 9. Global and Temporary Specs Share a Core but Not the Same Density

Global and temporary specs are not two names for the same document.

- the global spec is the long-lived reference
- the temporary spec is the change blueprint
- both share the same conceptual core
- they differ in density, time horizon, and operational role

This asymmetry is part of the canonical SDD model.

---

## 10. How to Judge Whether a Spec Is Good

A good spec should answer:

- Why does this project or feature exist?
- What is in scope and out of scope?
- What must it guarantee?
- What invariants must survive changes?
- How will those guarantees be verified?
- Where should a reader or agent look in the code when deeper grounding is needed?

If a document cannot answer those questions, it may still be useful, but it is not yet a strong SDD spec.

---

## 11. One-Sentence Definition

In SDD, a spec is a whitepaper-style reference that aligns humans and AI by preserving concept, boundaries, contracts, verification, and strategic code-entry hints in one durable Source of Truth.
