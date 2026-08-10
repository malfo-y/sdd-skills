# SDD Workflow

This document explains the default SDD workflow and where each document layer is used.

## 1. Default flow

```text
discussion
  -> align global direction
  -> feature draft (plan-review + fix: one pass by default, at most two at the threshold)
  -> implementation (implementation-review + fix: one pass by default, at most two at the threshold)
  -> verification
  -> global spec sync
```

Each reviewer invocation is a single pass. When the first invocation's pre-fix findings reach `Critical+High >= 3` or `Medium >= 5`, the producer (`feature-draft` or `implementation`) invokes the same gate a second time, applies the fixes itself, and stops. There is no third invocation, and neither the user nor autopilot invokes or fixes the gate separately.

## 2. When the harness is used

The harness (`AGENTS.md`) is the work-entry and work-convention layer, and it sits above the global spec. At the start of a task you read the harness first, then branch from it into the global spec, `_sdd/env.md`, or an in-progress temporary spec.

The harness carries work conventions (how) only; repo-specific triggers are owned solely by the global spec Guardrails.

## 3. When the global spec is used

The global spec is the starting point for every stage, but it is not the storage layer for every detail.

What is read from it:

- repo-wide framing
- scope / non-goals / guardrails
- long-lived key decisions

What is not kept there by default:

- feature task breakdown
- execution-level validation detail
- feature-level usage / expected result

## 4. When temporary specs are used

For medium or larger changes, the temporary spec (= the feature draft) becomes the center of execution.

It handles:

- change summary
- scope (In/Out)
- per-task contracts / AC / target files

Questions close to implementation are answered there.

## 5. When the four shared core axes are used

`Thinness`, `Decision-bearing truth`, `Anti-duplication`, and `Navigation + surface fit` are the shared baseline across spec lifecycle skills.

In practice:

- create: keep the global spec thin and retain only truth that changes judgment
- review: judge violations of the four axes with the rubric that matches the spec type
- rewrite: rearrange structure so the four axes become clearer
- upgrade: reduce a legacy spec toward the four axes, but hand off to rewrite when the scope exceeds migration

## 6. When `spec-summary` is used

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

## 7. Role differences across the four lifecycle skills

- `spec-create`: creates the first thin global spec. The default shape is a single `main.md`, and splitting is allowed only when a structure rationale justifies it.
- `spec-review`: audits with separate global and temporary rubrics. Feature-level contamination in a global spec is `Quality` by default, and becomes `Critical` only when it creates document-type confusion or wrong repo-wide truth. Every finding must carry evidence.
- `spec-rewrite`: reorganizes an existing spec into a better structure. It preserves rationale, citations, and code excerpt headers while moving migration history or execution-log style explanation out of the body and into `decision_log` or the rewrite report.
- `spec-upgrade`: migrates an old format into the current model. If the real issue is large-scale structural redesign, it should branch to `spec-rewrite` instead of stretching upgrade.

## 8. Role of review and update skills

- `spec-review`: audits quality and drift. It does not edit.
- `spec-sync`: it lifts only persistent repo-wide information into the global spec (handling pre-implementation planned alignment and post-implementation evidence sync, adapting to evidence).
- the sync skill does not copy temporary execution detail into the global body.

## 9. Verification rule

In SDD, execution and verification are not separate concerns.

Rules:

- always go through Execute -> Verify
- choose the verification method that fits the task
- for document and skill refactors, diff, grep, and review evidence can be valid verification

## 10. Drift control

- do not copy temporary execution detail into the global spec
- move supporting information to README or separate docs
- let code/test/review carry code-obvious detail
- keep mirrored skills semantically aligned
