# SDD Concept

This document explains how SDD places information across layers.

## 1. Core layers

| Layer | Role | Holds |
|------|------|-------|
| Global spec | repo-wide judgment layer | concept, boundaries, key decisions |
| Temporary spec | execution blueprint for a change | delta, touchpoints, validation, plan |
| Code/Test | actual behavior and detailed truth | implementation, runtime flow, detailed contract |
| Guide/README/Refs | supporting explanation | usage examples, environment detail, reference information |

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
