# SDD Core Concept: Two-Level Spec Structure

A guide to the core concepts for users new to Spec-Driven Development (SDD).

---

## 1. What is SDD? — A Global Spec That Replaces CLAUDE.md

In a typical Claude Code project, you write project context in `CLAUDE.md`. But as a project grows, `CLAUDE.md` alone cannot adequately cover architecture, component details, requirements, issue tracking, and more.

In SDD, `CLAUDE.md` is used only as a **pointer**, while the actual project documentation lives in the **global spec** (`_sdd/spec/main.md`).

```
CLAUDE.md                          _sdd/spec/main.md (Global Spec)
┌─────────────────────┐            ┌─────────────────────────────┐
│ "Refer to _sdd/spec/│            │ Goal, Architecture,         │
│  for project spec   │──points──▶│ Component Details,          │
│  documents"         │            │ Issues, Usage Examples ...  │
└─────────────────────┘            └─────────────────────────────┘
    Pointer (brief)                    Single Source of Truth (detailed)
```

**What the global spec does:**
- Documents the project's goals, architecture, and component details
- All SDD skills use this document as their reference
- A living document that evolves alongside the code (synced after implementation)

---

## 2. Two-Level Spec Structure — Think of It Like Git Branches

In SDD, the global spec is **never modified directly**. Instead, you first create a **temporary spec** (a blueprint for implementation), validate it, implement features according to that spec, then merge it into the global spec after completion.

A temporary spec is not merely a "document change proposal." It is a **blueprint for implementing features**. A temporary spec contains both what to build (spec patch) and how to build it (implementation plan).

This structure follows the same principle as Git branches:

```
Git Workflow                       SDD Workflow
────────────                       ────────────

main branch          ←→           Global Spec (main.md)
  │                                   │
  ├─ feature branch  ←→           Temporary Spec (feature_draft, spec_patch_draft)
  │    │                               │
  │    ├─ development ←→           Implementation (/implementation)
  │    │                               │
  │    └─ PR review   ←→           User Verification
  │         │                          │
  └─ merge  ←────────→           Merge into Global Spec (spec-update-done)
       │                               │
  branch delete      ←→           Archive (_processed_*, prev/)
```

**Why not modify directly?**
- **Implementation foundation**: The temporary spec serves as a blueprint, providing clear criteria before implementation
- **Change tracking**: Records of what changed and why are preserved
- **User verification**: Changes can be reviewed before implementation
- **Original preservation**: Previous versions (`prev/`) allow rollback if issues arise

---

## 3. Lifecycle of a Temporary Spec

A temporary spec is created, validated, **features are implemented according to it**, then it is merged into the global spec and archived.

```
Create              Validate          Implement          Merge              Archive
─────              ─────             ─────             ─────              ─────

/feature-draft → User review  → /implementation → /spec-update-done → Move to prev/
  feature_draft    (refine via       Code impl          Update main.md
                    conversation)
```

There are two paths depending on scale:

### Medium-Scale: Implement Then Merge

The most basic flow. Create a temporary spec, implement it, then reflect the results in the global spec.

```
/feature-draft → User review → /implementation → /spec-update-done
  (create blueprint)  (review)   (write code)     (reflect results in global spec)
```

1. `/feature-draft` → Creates `_sdd/drafts/feature_draft_<name>.md` (spec patch + implementation plan)
2. User reviews and refines the content
3. `/implementation` → Implements code based on the temporary spec
4. `/spec-update-done` → Reflects implementation results in the global spec

### Large-Scale: Pre-Register Then Implement

For large features, the temporary spec is first **pre-registered as planned status** in the global spec before implementation. This path prevents drift from the global spec during long implementation periods.

```
/feature-draft → /spec-update-todo → /implementation-plan → /implementation → /spec-update-done
  (create blueprint)  (pre-register as     (phase-by-phase      (write code)     (update status
                       📋Planned in          planning)                              to ✅Done)
                       global spec)
```

1. `/feature-draft` → Create temporary spec
2. `/spec-update-todo` → Pre-register as planned status (📋) in global spec
3. `/implementation-plan` → Develop detailed phase-by-phase implementation plan
4. `/implementation` → Implement by phase (iterate)
5. `/spec-update-done` → Update completed items' status to ✅Done

> **Key difference**: Medium-scale reflects changes in the global spec after implementation is complete, while large-scale registers the plan in the global spec before implementation begins.

### PR-Based Spec Reflection

A path for reflecting changes from PRs into the spec.

1. `/pr-spec-patch` → Creates `_sdd/pr/spec_patch_draft.md`
2. User reviews and refines the content
3. Move patch content to `_sdd/spec/user_draft.md`
4. `/spec-update-todo` → Merge into global spec

---

## 4. Spec File Categories — Permanent vs Temporary

Files under `_sdd/` are categorized as **permanent documents** and **temporary inputs**.

### Permanent Documents (Always Maintained)

| File | Role |
|------|------|
| `_sdd/spec/main.md` | Global Spec (Single Source of Truth) |
| `_sdd/spec/DECISION_LOG.md` | Decision records with rationale |
| `_sdd/spec/SUMMARY.md` | Spec summary (generated by spec-summary) |
| `_sdd/spec/prev/PREV_*.md` | Previous version backups |
| `_sdd/env.md` | Environment configuration guide |

### Temporary Inputs (Create → Process → Archive)

| File | Role | After Processing |
|------|------|-----------------|
| `_sdd/spec/user_draft.md` | User input (recommended format) | `_processed_user_draft.md` |
| `_sdd/spec/user_spec.md` | User input (free format) | `_processed_user_spec.md` |
| `_sdd/drafts/feature_draft_*.md` | Feature draft (patch + plan) | Moved to `_sdd/drafts/prev/` |
| `_sdd/pr/spec_patch_draft.md` | PR-based patch draft | Moved to `_sdd/pr/prev/` |

### Key Rules

- **Permanent documents** can only be modified by designated skills (`spec-update-todo`, `spec-update-done`)
- **Temporary inputs** must be archived after processing (to prevent reprocessing)
- **Previous versions** must not be deleted until project stabilization

---

## Summary

```
CLAUDE.md (pointer)
    │
    ▼
Global Spec (main.md) ◀──── Single Source of Truth
    ▲                          │
    │ Merge                    │ Reference
    │                          ▼
Temporary Spec (blueprint) ────→ Implementation ────→ Reflect in Global Spec
(feature_draft)                  (write code)          (spec-update-done)
```

For detailed workflows and skill usage: [SDD_WORKFLOW.md](SDD_WORKFLOW.md)
