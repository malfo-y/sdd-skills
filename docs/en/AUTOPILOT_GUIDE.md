# SDD-Autopilot User Guide

**Version**: 2.2.0
**Date**: 2026-08-09

A guide for the sdd-autopilot meta-skill that runs the SDD chain end-to-end without approval steps.

---

## 1. Overview

**sdd-autopilot** takes a single feature request and runs planning → implementation → spec synchronization to completion via the **SDD chain**, with each skill running its own quality gate internally. There is no separate execution-plan artifact and no approval step: once requirements are settled, execution starts immediately. The user only answers the initial requirement questions (when needed) and any Open Questions surfaced by the draft.

## 2. The Chain

```
Request analysis
  → feature-draft           (feature spec: per-task AC + Target Files — internal gate+fix once by default, at most twice at the threshold)
  → implementation          (main loop writes RED→GREEN directly — internal gate+fix once by default, at most twice at the threshold)
  → spec-sync               (only when persistent spec changes exist)
  → final response summary  (no report files)
```

Core principles:

- **No approval steps**: a wrong direction surfaces cheaply at the draft stage, and `feature-draft` checks plan quality through its own quality gate.
- **Gates and fixes belong to the producer skill**: `feature-draft` and `implementation` always run gate 1 and fix 1. If the first invocation's pre-fix findings reach `Critical+High >= 3` or `Medium >= 5`, the producer invokes the same gate a second time, applies fix 2, and then stops. Each reviewer invocation is a single pass, and there is no third invocation. Autopilot neither recalls the gate nor applies fixes; the producer's final response distinguishes invocation 1/2 findings, fixes, verification, and unresolved findings.
- **Lightweight returns**: review results come back as responses, not report files. The only artifacts are the draft file, code + tests, the implementation ledger, the AC→evidence table in chat, and the updated spec.

## 3. Splitting (handling oversized changes)

When a change does not fit in a single context, it is **split into multiple features** instead of being escalated to a bigger pipeline:

1. The draft becomes a **rolling split draft** — the full feature list goes inside the Part 1 marker, and Part 2 holds only the first feature's tasks.
2. `spec-sync` pins the split list into the global spec as **one planned todo per feature**.
3. The chain runs for the first feature; each remaining feature later gets its own draft and runs the chain in turn.

The canonical split criteria (coverage not eyeball-checkable / exceeds a single context) and the split method live in the `feature-draft` SKILL. Census-style sweeps (renames/propagation) are handled not by splitting but by a mandatory read-only verification task at the end of the draft.

## 4. Usage

```
/sdd-autopilot <feature description>
```

Examples:

```
/sdd-autopilot Implement JWT-based authentication: login, logout, token refresh.
/sdd-autopilot Change the login button color from blue to green.
```

**Trigger keywords**: `sdd-autopilot`, `autopilot`, `자동 구현`, `end-to-end 구현`, `자동으로 구현해줘`

### The user's role

| Stage | What the user does |
|-------|--------------------|
| Request analysis | Answer clarifying questions (one branch at a time, at most 5) |
| Right after the draft | Answer Open Questions that need confirmation (often none) |
| After that | Nothing — autonomous execution until the final report |

## 5. Artifacts

| Artifact | Location |
|----------|----------|
| draft | `_sdd/drafts/<date>_feature_draft_<slug>.md` (renamed with a `_processed_` prefix after spec-sync) |
| code + tests | target files listed in the draft |
| AC→evidence table | final response (chat) |
| implementation ledger | `_sdd/implementation/<date>_implementation_ledger_<slug>.md` |
| spec updates | `_sdd/spec/` (via spec-sync only) |

## 6. FAQ

- **Does it work in a spec-less repo?** — Yes. It proceeds in spec-less mode and recommends `spec-create` after implementation.
- **What happened to the old orchestrator-based full pipeline?** — It was removed. If you ever need it back, the last full implementation is preserved at the git tag `full-lane-final`.

## 7. Related skills

- `feature-draft` — feature spec + canonical split rules
- `plan-review` — the draft quality gate `feature-draft` invokes once by default and at most twice at the threshold (each invocation is a single pass with a lightweight return)
- `implementation` — main-loop RED→GREEN implementation + canonical stop/split rules
- `implementation-review` — the implementation quality gate `implementation` invokes once at close by default and at most twice at the threshold (each invocation runs correctness shard N ∥ simplicity with a lightweight return)
- `spec-sync` — global spec synchronization (adapts to planned/implemented evidence)
