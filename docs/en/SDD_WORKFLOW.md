# SDD Workflow

This document explains the default SDD workflow and where each document layer is used.

## 1. Default flow

```text
discussion
  -> align global direction
  -> temporary spec or feature draft
  -> implementation plan
  -> implementation
  -> review-fix loop
  -> verification
  -> global spec sync
```

## 2. When the global spec is used

The global spec is the starting point for every stage, but it is not the storage layer for every detail.

What is read from it:

- repo-wide framing
- scope / non-goals / guardrails
- long-lived key decisions

What is not kept there by default:

- feature task breakdown
- execution-level validation detail
- feature-level usage / expected result

## 3. When temporary specs are used

For medium or larger changes, a temporary spec or feature draft becomes the center of execution.

It handles:

- change summary
- scope delta
- contract / invariant delta
- touchpoints
- implementation plan
- validation plan

Questions close to implementation are answered there.

## 4. When `spec-summary` is used

`spec-summary` is used when a human needs the repo to make sense as one document.

What it should cover:

- what the repo solves
- why this approach was chosen
- what the core design is
- where the concrete code grounding lives
- how to read or use it and what to expect

What should not dominate the body:

- migration memo narration
- changelog prose
- long plan or progress logs

Relevant draft or implementation signals may be attached only as a short appendix.

## 5. Role of review and update skills

- `spec-review`: for global specs, it checks concept + boundaries + decisions.
- `spec-summary`: it writes `summary.md` as a reader-facing whitepaper that explains the problem, motivation, choice rationale, core design, code grounding, and usage or expected results in one place, with an optional appendix for short plan or progress signals.
- `spec-rewrite`: it first checks whether the global body is polluted by feature-level detail.
- `spec-update-todo`, `spec-update-done`: they lift only persistent repo-wide information into the global spec.

## 6. Verification rule

In SDD, execution and verification are not separate concerns.

Rules:

- always go through Execute -> Verify
- choose the verification method that fits the task
- for document and skill refactors, diff, grep, and review evidence can be valid verification

## 7. Drift control

- do not copy temporary execution detail into the global spec
- move supporting information to README or separate docs
- let code/test/review carry code-obvious detail
- keep mirrored skills semantically aligned
