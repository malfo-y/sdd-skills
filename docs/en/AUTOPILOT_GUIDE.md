# SDD-Autopilot User Guide

**Version**: 3.0.0
**Date**: 2026-08-10

## 1. Overview

`sdd-autopilot` is no longer an independent runner that starts implementation immediately. It is an **SDD-specific goal harness setup entrypoint**. It forwards the feature outcome to `goal-init(preset=sdd)`, creates a self-contained completion condition and four files under `_sdd/goal/<date>_<slug>/`, and hands them back for the user to review and activate.

Planning, implementation, and spec synchronization repeat only inside the native goal after the user activates it, never during setup.

## 2. Setup and execution flow

```text
/sdd-autopilot <feature outcome>
  → goal-init(preset=sdd)
  → Goal Intake → Divergence → Condition Crafting → Harness Setup → Handoff
  → condition string + four-file harness (still inactive)

User reviews and activates the native /goal
  → the SDD Loop Protocol repeats feature-sized SDD paths as needed
  → stop only after every DONE WHEN item and the final integration proof pass
```

The existing five `goal-init` stages, evaluator self-check (tool-free judgment, surfaced evidence, and at most 4,000 characters), and four-file format stay the same as the generic path. The SDD preset changes only the Loop Protocol payload in `goal.md`.

## 3. SDD Loop Protocol

The active native goal follows this order on every turn:

1. Pick the smallest next feature from either an unmet `DONE WHEN` item or a gap exposed by a failed final integration proof.
2. If no reviewed draft exists, run `feature-draft`. If it splits, choose the smallest next unit inside the current goal.
3. Execute the selected draft with `implementation`, including its producer-owned quality gate.
4. Run `spec-sync` when persistent changes exist.
5. Surface verification output and record the evidence, completed feature, remaining gap, and next action in the journal/report.
6. Finish only when every `DONE WHEN` item and the final integration proof pass; otherwise return to step 1.

If `feature-draft` splits again during execution, it does not create a nested `goal-init`. The current native goal keeps selecting the next smallest feature through the same Loop Protocol.

## 4. Boundaries

- **Setup only**: initial `feature-draft`, `implementation`, and `spec-sync` do not run during `/sdd-autopilot` setup.
- **User activation**: the skill never activates the native goal itself.
- **Existing goal remains untouched**: setup does not read current goal status, mutate, clear, pause, replace, or merge an existing goal, and it does not block because a goal is active.
- **Handoff invariant**: the result always states that the goal was not activated and the existing goal state was not changed.
- **Producer ownership**: after activation, `feature-draft` and `implementation` continue to own their plan and implementation quality gates and fixes.
- **Existing harness reused**: the roles and formats of `goal.md`, `experiments.md`, `journal.md`, and `report.md` remain unchanged; no separate queue or state-machine schema is introduced.

## 5. Usage

```text
/sdd-autopilot <verifiable multi-turn feature outcome>
```

Examples:

```text
/sdd-autopilot Implement JWT authentication with login, logout, token refresh, and integration proof.
/sdd-autopilot Migrate the legacy payment module to the new API, including regression tests and documentation sync.
```

A native goal is appropriate for a multi-turn task with a verifiable end state. For a one-line change, the `goal-init` suitability gate recommends redefining the outcome or using a one-shot task; autopilot does not start implementation automatically.

### The user's role

| Stage | What the user does |
|-------|--------------------|
| Goal Intake / Condition Crafting | Answer questions that define the outcome and DONE WHEN items |
| Handoff | Review the condition string and four-file harness |
| Activation | Decide whether and when to activate the native `/goal` |
| During execution | Use `/goal status`, `pause`, `resume`, or `clear` when needed |

## 6. Artifacts

| Artifact | Location / meaning |
|----------|--------------------|
| `goal.md` | Completion condition, SDD Loop Protocol, and runtime instructions |
| `experiments.md` | Pending/done backlog of approach hypotheses |
| `journal.md` | Append-only evidence, completed feature, remaining gap, and next action |
| `report.md` | Current conclusion and integration-proof status |

The four files are created under `_sdd/goal/<YYYY-MM-DD>_<slug>/`. Setup does not create a draft, code changes, an implementation ledger, or spec changes. Those artifacts appear feature by feature only after the user activates the native goal.

## 7. FAQ

- **Does this work without an existing spec?** — Goal harness setup does. After activation, the producer contracts and repository state determine whether a loop iteration has a persistent spec change to synchronize.

## 8. Related skills

- `goal-init` — canonical owner of the five-stage condition/harness setup, including the SDD preset payload
- `feature-draft` — specifies the next feature and owns split rules inside the active goal
- `implementation` — implements the draft RED→GREEN and runs its internal quality gate
- `spec-sync` — synchronizes persistent changes into the global spec
