# Common Spec Drift Patterns

Common drift patterns for exploration-first specs and how to resolve them.

## 1. Navigation Drift

### Pattern: Stale Repository Map

**Symptoms**
- important directories moved but the map still points to old paths
- a newcomer opens the spec and follows dead or misleading paths

**Resolution**
- update `Architecture Overview > Repository Map`
- remove dead paths
- add new important paths

### Pattern: Stale Runtime Map

**Symptoms**
- the documented request/event/batch flow no longer matches implementation
- new service hops or event steps are missing
- the arrows remain, but the user/operator-facing scenario no longer matches reality

**Resolution**
- update `Architecture Overview > Runtime Map`
- add or adjust invariants if the flow change affects correctness

### Pattern: Missing or Outdated Component Overview

**Symptoms**
- a component path and symbol are documented, but how it works is still opaque
- implementation changed the component flow or design intent, but the spec still describes the old rationale

**Resolution**
- update `Component Details > Overview`
- keep behavior summary and design intent aligned with actual ownership boundaries

### Pattern: Missing or Outdated Component Index

**Symptoms**
- a new component exists in code but is absent from the spec
- component names in the spec no longer match actual code ownership

**Resolution**
- update `Component Details > Component Index`
- link to component-specific docs when appropriate

### Pattern: Stale Common Change Paths

**Symptoms**
- a maintainer cannot tell where to start for a common change
- the spec points to old files or old entry points

**Resolution**
- update `Usage Examples > Common Change Paths`
- include real paths and symbols

## 2. Planned vs Actual Drift

### Pattern: Planned but Implemented

**Symptoms**
- spec still says `📋 계획됨`
- code and tests show the behavior exists

**Resolution**
- replace planned wording with actual behavior
- update related component and flow sections

### Pattern: Planned but Changed in Delivery

**Symptoms**
- implementation differs from original draft
- same feature exists but with different boundaries or contracts

**Resolution**
- sync the actual behavior
- update `DECISION_LOG.md` if rationale changed materially
- keep unresolved mismatch in `Open Questions` if needed

## 3. Contract Drift

### Pattern: Component Contract Changed

**Symptoms**
- inputs/outputs/events changed
- downstream callers or tests reflect new assumptions

**Resolution**
- update `Component Details`
- update `Component Details > Overview` if the contract change alters how the component works
- update `Architecture Overview > Runtime Map` if the contract affects flow

### Pattern: Invariant Drift

**Symptoms**
- code now relies on a new assumption not documented
- an old invariant is no longer true

**Resolution**
- update `Cross-Cutting Invariants` or component-specific `Risks / Invariants`

## 4. Environment Drift

### Pattern: Setup / Test Command Drift

**Symptoms**
- documented commands no longer run
- new services or env vars are required

**Resolution**
- update `Environment & Dependencies`
- update `Usage Examples` if the run/debug flow changed

### Pattern: Dependency or Config Drift

**Symptoms**
- new runtime dependency or env var exists
- docs still show old setup

**Resolution**
- update runtime/config sections
- mention operational implications if relevant

## 5. Issue and Unknown Drift

### Pattern: Resolved Issue Still Listed

**Symptoms**
- issue is fixed in code but still shown as open

**Resolution**
- remove or mark resolved in `Identified Issues & Improvements`

### Pattern: New Real Issue Not Documented

**Symptoms**
- implementation review or tests expose a limitation not in the spec

**Resolution**
- add it to `Identified Issues & Improvements`
- include affected component/path if known

### Pattern: Open Question Now Resolved

**Symptoms**
- a previous uncertainty is now settled by code or decision

**Resolution**
- remove it from `Open Questions`
- move the answer into the proper section if it is enduring knowledge
