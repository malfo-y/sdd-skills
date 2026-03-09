# SDD Core Concept: Two-Level Spec Structure

A guide to the core concepts of Spec-Driven Development (SDD) for first-time users

---

## 1. What is SDD? — A Global Spec That Replaces CLAUDE.md

In a typical Claude Code project, you write project context in `CLAUDE.md`. But as a project grows, `CLAUDE.md` alone becomes insufficient for covering architecture, component details, requirements, issue tracking, and more.

In SDD, `CLAUDE.md` is used only as a **pointer**, while the substantive project documentation lives in the **global spec** (`_sdd/spec/main.md`).

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
- All SDD skills use this document as their reference point
- A living document that evolves alongside the code (synced after implementation)

---

## 2. Two-Level Spec Structure — Think of It Like Git Branches

In SDD, the global spec is **never modified directly**. Instead, you first create a **draft spec** (a blueprint for implementation), validate it, implement the feature according to that spec, and then merge it into the global spec upon completion.

A draft spec is not simply a "document change proposal." It is a **blueprint for implementing a feature**. A draft spec contains both what to build (spec patch) and how to build it (implementation plan).

This structure follows the same principle as Git branches:

```
Git Workflow                       SDD Workflow
────────────                       ────────────

main branch          ←→           Global Spec (main.md)
  │                                   │
  ├─ feature branch  ←→           Draft Spec (feature_draft, spec_patch_draft)
  │    │                               │
  │    ├─ develop     ←→           Implementation (/implementation)
  │    │                               │
  │    └─ PR review   ←→           User Verification
  │         │                          │
  └─ merge  ←────────→           Merge into Global Spec (spec-update-done)
       │                               │
  branch delete      ←→           Archive (_processed_*, prev/)
```

**Why not modify directly?**
- **Implementation baseline**: The draft spec serves as a blueprint for implementation, providing clear criteria before coding begins
- **Change tracking**: Records of what changed and why are preserved
- **User verification**: Changes can be reviewed before implementation
- **Original preservation**: If problems arise, you can restore from the previous version (`prev/`)

---

## 3. Lifecycle of a Draft Spec

A draft spec is created, goes through validation, **the feature is implemented according to that spec**, and then it is merged into the global spec and archived.

```
Create              Validate          Implement          Merge              Archive
─────              ─────             ─────              ─────              ─────

/feature-draft → User review  → /implementation → /spec-update-done → Move to prev/
  feature_draft    (refine via       Code                main.md update
                    conversation)    implementation
```

There are two paths depending on the scale:

### Medium-scale: Merge After Implementation

This is the most basic flow. Create a draft spec, implement it, and then reflect the results in the global spec.

```
/feature-draft → User verification → /implementation → /spec-update-done
  (Create blueprint)  (Review content)   (Write code)     (Reflect results in global spec)
```

1. `/feature-draft` → Creates `_sdd/drafts/feature_draft_<name>.md` (spec patch + implementation plan)
2. User reviews and refines the content
3. `/implementation` → Implements code based on the draft spec
4. `/spec-update-done` → Reflects implementation results in the global spec

### Large-scale: Pre-register Then Implement

For large-scale features, the draft spec is **pre-registered in the global spec as a planned status** before implementation. This path prevents drift from the global spec during long-running implementations.

```
/feature-draft → /spec-update-todo → /implementation-plan → /implementation → /spec-update-done
  (Create blueprint)  (Pre-register in       (Phase-by-phase     (Write code)     (Update status
                       global spec as          plan)                                to ✅ done)
                       📋 planned)
```

1. `/feature-draft` → Create draft spec
2. `/spec-update-todo` → Pre-register in the global spec as planned status (📋)
3. `/implementation-plan` → Develop detailed implementation plan by phase
4. `/implementation` → Implement by phase (iterative)
5. `/spec-update-done` → Update completed items' status to ✅ done

> **Key difference**: Medium-scale reflects results in the global spec after implementation is complete, while large-scale registers the plan in the global spec before implementation begins.

### PR-based Spec Reflection

This path reflects changes that originated from a PR into the spec.

1. `/pr-spec-patch` → Creates `_sdd/pr/spec_patch_draft.md`
2. User reviews and refines the content
3. Patch content is moved to `_sdd/spec/user_draft.md`
4. `/spec-update-todo` → Merges into the global spec

---

## 4. Spec File Classification — Permanent vs. Temporary

Files under `_sdd/` are classified into **permanent documents** and **temporary inputs**.

### Permanent Documents (Always Retained)

| File | Role |
|------|------|
| `_sdd/spec/main.md` | Global Spec (Single Source of Truth) |
| `_sdd/spec/DECISION_LOG.md` | Records of decisions and their rationale |
| `_sdd/spec/SUMMARY.md` | Spec summary (generated by spec-summary) |
| `_sdd/spec/prev/PREV_*.md` | Previous version backups |
| `_sdd/env.md` | Environment setup guide |

### Temporary Inputs (Create → Process → Archive)

| File | Role | After Processing |
|------|------|------------------|
| `_sdd/spec/user_draft.md` | User input (recommended format) | `_processed_user_draft.md` |
| `_sdd/spec/user_spec.md` | User input (free-form) | `_processed_user_spec.md` |
| `_sdd/drafts/feature_draft_*.md` | Feature draft (patch + plan) | Moved to `_sdd/drafts/prev/` |
| `_sdd/pr/spec_patch_draft.md` | PR-based patch draft | Moved to `_sdd/pr/prev/` |

### Key Rules

- **Permanent documents** can only be modified by designated skills (`spec-update-todo`, `spec-update-done`)
- **Temporary inputs** must be archived after processing (to prevent reprocessing)
- **Previous versions** must not be deleted until the project is stabilized

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
Draft Spec (blueprint) ────→ Implementation ────→ Reflect in Global Spec
(feature_draft)              (write code)          (spec-update-done)
```

For detailed workflows and skill usage: [SDD_WORKFLOW.md](SDD_WORKFLOW.md)
