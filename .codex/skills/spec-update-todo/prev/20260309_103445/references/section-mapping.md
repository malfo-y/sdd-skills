# Section Mapping Guide

How to map planned requirements into the exploration-first spec structure.

## Quick Reference

| Planned Change | Preferred Target Section |
|----------------|--------------------------|
| New user-visible feature | `Goal > Key Features` |
| Scope or ownership boundary change | `Architecture Overview > System Boundary` |
| Runtime/data/event flow change | `Architecture Overview > Runtime Map` |
| New or changed component | `Component Details` |
| New config/dependency/runtime change | `Environment & Dependencies` |
| Operational or debugging workflow | `Usage Examples > Common Operations` or `Common Change Paths` |
| Planned risk or technical debt | `Identified Issues & Improvements` |
| Uncertainty / missing detail | `Open Questions` |

## Detailed Rules

### 1. New Features

When the input describes a new user-visible capability:
- add or update `Goal > Key Features`
- if the feature adds a new flow, also update `Architecture Overview > Runtime Map`
- if it introduces a new ownership boundary, also update `Component Details`

### 2. Architecture / Flow Changes

When the input changes how the system is connected or how work moves:
- update `Architecture Overview > System Boundary` if scope changes
- update `Architecture Overview > Runtime Map` if request/event/batch flow changes
- add `Cross-Cutting Invariants` if the new plan introduces important guarantees

### 3. Component Changes

When the input adds or changes a component:
- update `Component Details`
- add or refresh `Component Index`
- include owned paths, key symbols, responsibility, and contracts when known

### 4. Environment & Dependencies

For dependencies, env vars, runtime versions, setup commands:
- update `Environment & Dependencies`
- if the change affects how to run or verify behavior, also update `Usage Examples`

### 5. Operational / Change Guidance

If a planned change creates a new editing/debugging path:
- update `Usage Examples > Common Change Paths`
- optionally update `Common Operations`

### 6. Risks / Debt / Bugs

Use `Identified Issues & Improvements` for:
- planned improvements
- known limitations
- reported bugs to track
- technical debt that should remain visible

### 7. Unknowns

Use `Open Questions` for:
- ambiguous scope
- unclear ownership
- missing contract detail
- unresolved dependency or rollout decision

## Important Rule

One planned change may map to multiple sections.
Do not force every item into only one place when the spec would become misleading.
