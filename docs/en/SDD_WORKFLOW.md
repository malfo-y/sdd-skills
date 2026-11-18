# SDD Workflow

This document explains the default SDD workflow and where each document layer is used.

## 1. Default flow

```text
discussion
  -> align global direction
  -> plan (write the plan file + plan review)
  -> implementation (failing check first + implementation review)
  -> verification
  -> global spec sync
```

`sdd-orchestrator` runs the stages after discussion directly in the main session. The same session does the plan review and the implementation review once each and fixes what it finds in place. When an independent review is needed, use `pr-review` at PR time.

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
- places to change / end conditions and how each is judged / progress record

Questions close to implementation are answered there.

## 5. When the four shared core axes are used

`Thinness`, `Decision-bearing truth`, `Anti-duplication`, and `Navigation + surface fit` are the shared baseline across spec lifecycle skills.

In practice:

- create: keep the global spec thin and retain only truth that changes judgment
- upgrade (audit): judge violations of the four axes and drift from the code, with evidence
- upgrade (fix): reduce a legacy spec toward the four axes and rearrange structure so the four axes become clearer

## 6. Role differences across the two lifecycle skills

- `spec-create`: creates the first thin global spec. The default shape is a single `main.md`, and splitting is allowed only when a structure rationale justifies it.
- `spec-upgrade`: audits an existing spec and brings it up to the current model. When only an audit is requested, it does not edit the spec or the harness and reports findings with evidence. Feature-level contamination in a global spec is `Quality` by default, and becomes `Critical` only when it misleads judgment, as wrong repo-wide truth does. When fixing, it migrates an old format into the current model and reorganizes structure while preserving rationale, citations, and code excerpt headers, and moves migration history or execution-log style explanation out of the body and into `decision_log`. After fixing, it refreshes the harness (`AGENTS.md` and hooks).

## 7. Role of review and update skills

- the audit of `spec-upgrade`: audits quality and drift. It does not edit.
- the spec-sync stage of `sdd-orchestrator`: it lifts only persistent repo-wide information into the global spec (handling pre-implementation planned alignment and post-implementation evidence sync, adapting to evidence).
- the sync stage does not copy temporary execution detail into the global body.

## 8. Verification rule

In SDD, execution and verification are not separate concerns.

Rules:

- always go through Execute -> Verify
- choose the verification method that fits the task
- for document and skill refactors, diff, grep, and review evidence can be valid verification

## 9. Drift control

- do not copy temporary execution detail into the global spec
- move supporting information to README or separate docs
- let code/test/review carry code-obvious detail
- keep mirrored skills semantically aligned
