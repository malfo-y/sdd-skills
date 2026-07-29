# SDD Concept

This document explains how SDD places information across layers.

## 1. Core layers

| Layer | Role | Holds |
|------|------|-------|
| Harness (AGENTS.md + hook assets) | repo work conventions (how) / work entry | work principles, reading order, verification standard, workflow stage order, judgment-criteria pointers, and the executable assets that enforce or restore those conventions |
| Global spec | repo-wide judgment layer | concept, boundaries, key decisions |
| Temporary spec | execution blueprint for a change | delta, scope, per-task contracts/AC, target files |
| Code/Test | actual behavior and detailed truth | implementation, runtime flow, detailed contract |
| Guide/README/Refs | supporting explanation | usage examples, environment detail, reference information |

The harness is its own layer and it does not grow the global spec body. Understanding (what/why) belongs to the global spec; work conventions (how) belong to the harness. The harness is **not documentation alone** — conventions that a model can silently skip are carried by executable assets. Those assets work in two directions: they **enforce** a convention (the work-log commit gate), or they **re-inject** one that has been lost (the harness re-injection after compact/clear). Conventions written only as prose do not get followed, and a convention that has fallen out of context may as well not exist; that observation is why this layer carries executable assets. The harness holds no skill catalog or routing table (it points at the installed SDD skills), and no repo-specific behavior triggers either (the global spec Guardrails are the single source for those).

## 2. Role of the global spec

The global spec fixes how the repo should be understood, where scope ends, and which guardrails and key decisions must survive later changes.

It is responsible for:

- background and high-level concept
- scope / non-goals / guardrails
- core design and key decisions

It is not the default home for:

- feature-level usage guides
- feature-level contract / validation detail
- exhaustive inventory
- explanations that can be recovered directly from code

## 3. Role of the temporary spec

A temporary spec is the document for executing one change.

It is responsible for:

- what changes now
- which boundaries move
- which contract / invariant delta exists
- what gets touched
- how the change will be verified

So if the global spec is the repo-wide judgment layer, the temporary spec is the task-level blueprint.

## 4. Role of guides

A guide is not a permanent extra spec layer. It is a companion surface created when needed.

Good cases:

- a feature flow needs fast explanation
- a reviewer needs bounded context
- a guide is faster than reconstructing everything from code alone

A guide does not replace the global spec, and it does not turn the temporary spec into a permanent storage layer.

## 5. Information placement rule

When deciding where something belongs, use this order.

1. Is it repo-wide judgment?
2. Is it feature-level execution context?
3. Is it supporting reference?
4. Is it obvious from code?

Rule of thumb:

- if it is close to 1, it belongs in the global spec
- if it is close to 2, it belongs in a temporary spec or guide
- if it is close to 3, it belongs in README or separate docs
- if it is close to 4, code/test/review is the better home
