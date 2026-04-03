# Spec Rewrite Checklist

Checklist to reduce omissions during spec rewrite work under the current canonical model.

## 1) Pre-Check

- [ ] Identify the main target spec file (`_sdd/spec/main.md` or `_sdd/spec/<project>.md`)
- [ ] Collect the list of linked sub-spec files
- [ ] Write `_sdd/spec/logs/spec-rewrite-plan.md` before backup or rewrite work starts
- [ ] Confirm backup policy (`_sdd/spec/prev/prev_<filename>_<timestamp>.md`)
- [ ] Load `_sdd/spec/decision_log.md` if present
- [ ] Read `docs/SDD_SPEC_DEFINITION.md`
- [ ] Confirm with the user before large-scale file splitting

## 2) Core Quality Scorecard

Record a short score/evidence note for:

- `Component Separation`
- `Findability`
- `Repo Purpose Clarity`
- `Architecture Clarity`
- `Usage Completeness`
- `Environment Reproducibility`
- `Ambiguity Control`
- `Why/Decision Preservation`
- `Canonical Fit`

## 3) Canonical Fit Checks

### Global Spec Checks

- [ ] Background & High-Level Concept is visible
- [ ] Scope / Non-goals / Guardrails is visible
- [ ] Contract / Invariants / Verifiability is visible
- [ ] Decision-Bearing Structure is visible
- [ ] Usage Guide & Expected Results is visible
- [ ] Reference information does not replace the main body

### Temporary Spec Checks

- [ ] Change Summary is visible
- [ ] Scope Delta is visible
- [ ] Contract/Invariant Delta is visible
- [ ] Touchpoints are visible
- [ ] Validation linkage is visible
- [ ] Risks / Open Questions are visible

## 4) Prune / Appendix Decision Rules

Move to appendix or reference:

- long logs or historical records
- exhaustive file inventories
- low-value repeated tables
- setup detail that does not carry decisions

Keep in main:

- problem, scope, guardrails
- core design and key decisions
- CIV
- decision-bearing structure
- usage and expected results

## 5) Preservation Rules

- [ ] Important design reasons remain inline or are explicitly preserved elsewhere
- [ ] `Source` mappings and inline citations remain valid
- [ ] Strategic code map stays selective
- [ ] Missing canonical content is flagged, not invented

## 6) Exit Criteria

- [ ] Main document better matches the current canonical model
- [ ] Orphan files and broken links are removed
- [ ] Key rationale remains understandable from the main path
- [ ] Rewrite report documents unresolved warnings and deviations
