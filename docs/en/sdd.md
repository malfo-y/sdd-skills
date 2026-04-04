# SDD

SDD is less about “writing specs” and more about keeping the right information in the right layer so judgment does not drift.

## 1. Core claims

- the global spec fixes repo-wide judgment
- the temporary spec provides the execution blueprint for a change
- code-obvious detail is usually better carried by code, tests, and review
- supporting information should be split into guides, README, and reference docs

## 2. Questions answered by the global spec

- what is this repo trying to solve
- where does scope end
- what is intentionally out of scope
- which guardrails and key decisions must survive

## 3. Questions answered by the temporary spec

- what changes now
- which delta exists
- what gets touched
- how the change will be verified

## 4. Separation rule

SDD does not put everything into one document.

- repo-wide judgment lives in the global spec
- feature-level execution detail lives in the temporary spec
- usage examples and supporting reference go to guides or README
- detail that is obvious from code stays with code, tests, and review

## 5. Practical rules

- keep the global spec focused on repo-wide judgment
- make temporary specs concrete
- if a repo-wide invariant really matters, keep it in guardrails or key decisions
- treat guides as on-demand companions, not authoritative spec layers

## 6. Summary

> SDD is not a way of creating more documents. It is a way of keeping the right information in the right layer.
