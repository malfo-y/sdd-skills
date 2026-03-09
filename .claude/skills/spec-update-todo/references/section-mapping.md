# Section Mapping Guide

How to map planned requirements into the exploration-first spec structure.

## Quick Reference

Map each planned item to the appropriate SDD anchor section:

| Planned Change | Preferred Target Section |
|----------------|--------------------------|
| New user-visible feature | `Goal > Key Features` |
| Scope or ownership boundary change | `Architecture Overview > System Boundary` |
| Runtime/data/event flow change | `Architecture Overview > Runtime Map` |
| New or changed component | `Component Details` |
| Behavior change / design intent change | `Component Spec > Overview` |
| New config/dependency/runtime change | `Environment & Dependencies` |
| Operational or debugging workflow | `Usage Examples > Common Operations` or `Common Change Paths` |
| Planned risk or technical debt | `Identified Issues & Improvements` |
| Uncertainty / missing detail | `Open Questions` |

## Update Need Triage (SDD §8)

- `MUST update`
  - user-visible capability changes
  - boundary, flow, ownership, or contract changes
  - new environment/setup requirements
  - new common change/debug entry points
- `NO update`
  - tests-only or comment-only changes
  - internal refactors with no behavior or navigation impact
- `CONSIDER`
  - minor dependency/runtime adjustments
  - performance tuning with low documentation impact
  - internal reorganizations whose maintenance impact is still unclear

## Detailed Rules

### 1. New Features

When the input describes a new user-visible capability:
- add or update `Goal > Key Features`
- if the feature adds a new flow, also update `Architecture Overview > Runtime Map`
- if it introduces a new ownership boundary, also update `Component Details`
- if it creates a new editing/debugging path, also update `Usage Examples > Common Change Paths`

### 2. Architecture / Flow Changes

When the input changes how the system is connected or how work moves:
- update `Architecture Overview > System Boundary` if scope changes
- update `Architecture Overview > Runtime Map` if request/event/batch flow changes
- add `Cross-Cutting Invariants` only if the new plan introduces repository-wide guarantees that are worth preserving globally

### 3. Component Changes

When the input adds or changes a component:
- update `Component Details`
- add or refresh `Component Index`
- use the SDD component spec structure:
  - Responsibility (하는 일 / 하지 않는 일)
  - Owned Paths (실제 파일/디렉토리 경로)
  - Key Symbols / Entry Points
  - Interfaces / Contracts (입력/출력, 불변 조건)
  - Dependencies (upstream / downstream)
  - Change Recipes (변경 유형별 시작점과 검증 포인트)

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

## Multi-Section Impact Awareness

One planned change may map to multiple sections.
Do not force every item into only one place when the spec would become misleading.

Example — a new `NotificationService` feature may require updates in:

| Target Section | What to Add |
|---------------|-------------|
| `Goal > Key Features` | 실시간 알림 기능 항목 |
| `Architecture Overview > Runtime Map` | 알림 이벤트 흐름 |
| `Component Details` | NotificationService 컴포넌트 엔트리 (Responsibility, Owned Paths, Interfaces, Change Recipes 포함) |
| `Environment & Dependencies` | `NOTIFICATION_WEBHOOK` 환경변수 |
| `Usage Examples > Common Change Paths` | 알림 관련 변경 시작점 |
| `Open Questions` | 이메일 알림 범위 미정 |

Always check whether a single input item has cross-section impact before finalizing the update plan.
