# Spec Update Strategies

Strategies for syncing exploration-first specs with actual implementation.

## Strategy Selection Matrix

| Scenario | Strategy | Scope | Risk |
|----------|----------|-------|------|
| Internal refactor, no documented behavior change | Skip Update | none | low |
| Small config/path correction | Targeted Sync | one section | low |
| Planned feature now implemented | Planned-to-Actual Sync | multiple linked sections | medium |
| New component or ownership shift | Component Map Refresh | component + maps | medium |
| Major architecture or navigation drift | Full Navigation Refresh | main spec + split files | high |
| Ongoing phased delivery | Staged Sync | incremental | medium |

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

## Validation Checklist

- paths exist
- component names match real code
- runtime flow description matches implementation
- common change paths point to real edit/debug entry points
- planned vs actual state is consistent
- `Open Questions` is current
