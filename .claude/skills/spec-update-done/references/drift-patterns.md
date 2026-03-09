# Common Spec Drift Patterns

Common drift patterns for exploration-first specs and how to resolve them.

## 1. Navigation Drift

### Pattern: Stale Repository Map

**Symptoms**
- important directories moved but the map still points to old paths
- a newcomer opens the spec and follows dead or misleading paths
- `Architecture Overview > Repository Map`에 없는 새 디렉토리가 실제로 존재

**Resolution**
- update `Architecture Overview > Repository Map`
- remove dead paths
- add new important paths
- verify with `Glob` and `ls` that listed paths exist

### Pattern: Stale Runtime Map

**Symptoms**
- the documented request/event/batch flow no longer matches implementation
- new service hops or event steps are missing
- 런타임 흐름에 새 미들웨어, 이벤트 핸들러, 배치 단계가 추가되었으나 미반영

**Resolution**
- update `Architecture Overview > Runtime Map`
- add or adjust invariants if the flow change affects correctness
- verify actual flow by tracing entry points in code

### Pattern: Missing or Outdated Component Index

**Symptoms**
- a new component exists in code but is absent from the spec
- component names in the spec no longer match actual code ownership
- 컴포넌트 스펙 파일이 존재하지만 메인 스펙의 `Component Index`에 링크가 없음

**Resolution**
- update `Component Details > Component Index`
- link to component-specific docs when appropriate
- verify component ownership paths match actual directories

### Pattern: Stale Common Change Paths

**Symptoms**
- a maintainer cannot tell where to start for a common change
- the spec points to old files or old entry points
- `Usage Examples > Common Change Paths`의 파일/심볼이 리네임 또는 삭제됨

**Resolution**
- update `Usage Examples > Common Change Paths`
- include real paths and symbols
- verify each listed path exists in the current codebase

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
- update `Architecture Overview > Runtime Map` if the contract affects flow

### Pattern: Invariant Drift

**Symptoms**
- code now relies on a new assumption not documented
- an old invariant is no longer true

**Resolution**
- update `Cross-Cutting Invariants` only if the assumption is repository-wide
- otherwise update component-specific `Risks / Invariants`

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
