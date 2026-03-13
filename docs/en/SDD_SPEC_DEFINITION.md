# What Is a Spec in SDD?

This document defines what a "spec" means in SDD, why it is more than simple documentation, and what kind of structure and qualities it should have.

Related documents:
- [SDD_CONCEPT.md](SDD_CONCEPT.md): the two-level structure of global specs and temporary specs
- [SDD_WORKFLOW.md](SDD_WORKFLOW.md): how specs are used in the actual development loop
- [sdd.md](../sdd.md): the broader philosophy and motivation behind SDD

---

## 1. Why Define the Spec Explicitly?

In SDD, a spec is not just a document. When humans and AI agents build software together, the spec is the anchor that fixes what should be built, why the design looks the way it does, and what must not be broken.

When the definition of a spec is weak, the same problems keep returning:

- the spec collapses into a component list or an API list
- design rationale disappears, so humans and AI keep re-deriving intent
- usage and expected outcomes are missing, so verification becomes vague
- the connection between code and documentation is too weak to manage drift well

That is why SDD needs an explicit definition of what belongs in a spec.

---

## 2. What a Spec Is Not

In SDD, a spec should not be reduced to any of the following:

- a simple feature checklist
- a collection of API, CLI, or configuration references
- a report written only after implementation is finished
- a manual that merely repeats facts already visible in the code

Those artifacts are still useful, but they do not explain why the structure exists, what the core idea is, or what outcomes the system is expected to produce.

---

## 3. What a Spec Is

In SDD, a spec has the following character:

> A spec is a whitepaper-like Single Source of Truth that captures the problem, background, motivation, core design, expected behavior, and code-grounded evidence of a project.

That means a spec must do all of the following at once:

- explain the problem: what this project is trying to solve
- explain the motivation: why this approach was chosen
- explain the core design: what ideas and structures make it work
- connect to implementation evidence: where this explanation maps to real code
- guide usage and verification: how it should be used and what results should be expected

From this perspective, a spec is closer to a technical whitepaper than a software manual.

---

## 4. Why a Whitepaper-Like Structure?

A whitepaper or technical paper does not just list outputs. It provides background, frames the problem, explains the core method, and connects implementation to results. SDD specs should follow the same flow.

The reason is practical:

- humans understand design decisions through background and motivation
- AI aligns to explicit intent and constraints instead of filling gaps by guesswork
- reviewers gain something verifiable by connecting expected outcomes to code evidence

So the whitepaper style is not an aesthetic preference. It is a structural device for preserving design intent.

---

## 5. Mapping Paper Elements to Code Specs

| Academic document element | SDD spec counterpart |
|---------------------------|----------------------|
| Abstract | Project overview and core value |
| Introduction / Motivation | Background, problem framing, and why this project exists |
| Related Work | Alternative approaches and why this one was chosen |
| Core Method / Algorithm | Core design, logic flow, and major algorithms |
| Implementation Details | Component details, data flow, and implementation specifics |
| Experiments | Usage scenarios, operating flows, and verification scenarios |
| Results | Expected outcomes, acceptance criteria, and observable behavior |
| References | Code citations, reference lists, and related document links |

The goal is not to imitate academic formatting literally, but to translate the explanatory structure of a paper into a code-centered specification.

---

## 6. What an SDD Spec Must Contain

Based on the discussions so far, an SDD spec should include at least the following axes.

### 1) Background and Motivation

- the problem being solved
- why this problem matters now
- why this approach was chosen over alternatives

### 2) Core Design

- the central system idea
- the logic flow or algorithmic shape
- the reasoning behind the chosen structure

### 3) Implementation Evidence and Code Mapping

- the explanation should connect to real code
- core design sections may include code citations or code excerpts
- a reader should be able to tell where to look in the codebase

### 4) Usage Guide and Expected Results

- the scenarios in which the system is used
- what results should appear when it is used correctly
- what is guaranteed in failure or edge cases

### 5) Supporting Reference Material

- data model
- API reference
- environment and configuration

Supporting reference material still matters, but it is not sufficient on its own to make a true spec.

---

## 7. Recommended Spec Shape

Based on the current direction, an SDD spec should naturally evolve toward a structure like this:

```markdown
# Project Spec

## 1. Background and Motivation
## 2. Core Design
## 3. Architecture Details
## 4. Component Details
## 5. Usage Guide & Expected Results
## 6. Data Model
## 7. API Reference
## 8. Environment and Configuration

## Appendix: Code Reference List
```

The important point is not to discard the existing reference-style sections, but to strengthen them with background, design narrative, and expected outcomes.

---

## 8. How a Spec Connects to Code

An SDD spec should not be a loosely related document. It should be able to speak directly to the codebase.

Recommended principles:

- connect core design sections to real code
- use inline citations in a form like `[filepath:functionName]`
- prefer real code excerpts over pseudocode for critical logic
- if an excerpt is 30 lines or fewer, include it in full; if it is longer, include the signature and the key logic
- place less critical implementation evidence in an appendix or source table

This gives humans a navigation path and gives AI precise grounding.

---

## 9. This Definition Applies to Both Global and Temporary Specs

SDD has both global specs and temporary specs. Their roles differ, but they share the same definition of what a spec is.

### Global Spec

- the stable Single Source of Truth for the project
- captures the current state and accepted design
- is realigned with code after implementation through `spec-update-done`

### Temporary Spec

- the blueprint for change
- fixes what will change and how it will be implemented
- leads into implementation after validation, then gets merged into the global spec

In other words, a temporary spec is not just a change proposal. It is also a whitepaper-like implementation blueprint.

---

## 10. How to Judge Whether a Spec Is Good

A good spec should be able to answer these questions:

- Why does this project or feature exist?
- What must it guarantee?
- How does the core design work?
- Where should someone look in the real code?
- What outcomes should a user expect?
- What must not be broken in the next change?

If a document cannot answer those questions, it may still be useful, but it is not yet a strong SDD spec.

---

## 11. One-Sentence Definition

In SDD, a spec is not just explanatory documentation. It is a whitepaper-like reference document that aligns humans and AI around implementation, review, and synchronization by capturing the problem, motivation, core design, expected results, and code-grounded evidence together.
