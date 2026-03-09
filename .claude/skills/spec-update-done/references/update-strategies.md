# Spec Update Strategies

Strategies for syncing exploration-first specs with actual implementation.

## Strategy Selection Matrix

| Scenario | Update Need | Strategy | Scope | Risk |
|----------|-------------|----------|-------|------|
| Internal refactor, no documented behavior change | `NO update` | Skip Update | none | low |
| Small config/path correction | `MUST update` | Targeted Sync | one section | low |
| Planned feature now implemented | `MUST update` | Planned-to-Actual Sync | multiple linked sections | medium |
| New component or ownership shift | `MUST update` | Component Map Refresh | component + maps | medium |
| Major architecture or navigation drift | `MUST update` | Full Navigation Refresh | main spec + split files | high |
| Ongoing phased delivery | `CONSIDER` or `MUST update` | Staged Sync | incremental | medium |

## 1. Skip Update

Use when:
- code changed internally but external behavior, ownership, and navigation remain the same
- tests or comments changed only

Action:
- no spec edit required
- optionally note in implementation artifacts only

## 2. Targeted Sync

Use when:
- one path changed
- one env var changed
- one command or setup note changed

Action:
- update the exact section only
- preserve the rest of the document

Examples:
- `Environment & Dependencies`
- `Usage Examples > Running the Project`
- one path inside `Repository Map`

## 3. Planned-to-Actual Sync

Use when:
- a `📋 계획됨` item was implemented
- a drafted feature is now real

Action:
- update `Goal` if the feature is user-visible
- update `Architecture Overview` if flows or boundaries changed
- update `Component Details` with actual paths/symbols/contracts
- refresh `Usage Examples > Common Change Paths`
- remove or replace stale planned markers

## 4. Component Map Refresh

Use when:
- a new component was added
- ownership moved
- a component spec should be created or updated

Action:
- update `Component Index`
- update or create the component spec file
- ensure paths and symbols are real

## 5. Full Navigation Refresh

Use when:
- `Repository Map`, `Runtime Map`, or `Component Index` are broadly stale
- the main spec no longer works as an entry point

Action:
- update the main spec first
- then update affected component files
- preserve rationale in `DECISION_LOG.md` if structure or intent changed
- consider `spec-rewrite` if the problem is mainly document structure rather than implementation drift

## 6. Staged Sync

Use when:
- implementation is landing in phases
- some planned items are done and some remain planned

Action:
- mark completed items as actual
- leave remaining planned items clear
- keep `Open Questions` current

## Strategy Selection Criteria

아래 질문으로 적절한 전략을 판별한다:

| 질문 | Yes -> Strategy |
|------|----------------|
| 외부 동작/계약/탐색 경로가 전혀 안 바뀌었나? | Skip Update |
| 변경이 단일 섹션 내에서 완결되나? | Targeted Sync |
| `📋 계획됨` 항목이 구현 완료되었나? | Planned-to-Actual Sync |
| 새 컴포넌트가 추가되었거나 소유권이 이동했나? | Component Map Refresh |
| Repository Map, Runtime Map, Component Index가 전반적으로 stale한가? | Full Navigation Refresh |
| 구현이 단계적으로 진행 중이고 일부만 완료되었나? | Staged Sync |

## Validation Checklist

- paths exist
- component names match real code
- runtime flow description matches implementation
- common change paths point to real edit/debug entry points
- planned vs actual state is consistent
- `Open Questions` is current
- optional sections that remain are still relevant
- duplicated prose was not reintroduced during sync
