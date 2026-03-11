# Spec Review Report (Strict)

**Date**: 2026-02-07  
**Reviewer**: Codex  
**Scope**: Spec+Code  
**Spec Files**:
- `_sdd/spec/apify_ig.md`
- `_sdd/spec/apify_ig/02-architecture.md`
- `_sdd/spec/apify_ig/04-interfaces.md`
**Code State**: Workspace + recent commits (`abc1234..def5678`)  
**Decision**: SYNC_REQUIRED

## Executive Summary

The spec remains mostly aligned with project intent, but multiple high-confidence drifts were found in API limits and component boundaries. The document also has medium-severity quality gaps in acceptance criteria definition. Spec updates are required before the next implementation planning cycle.

## Findings by Severity

### High
1. API rate-limit mismatch between spec and code
   - Evidence: `src/config/rate_limit.py:12`, `src/api/middleware.py:47`, integration test `tests/test_rate_limit.py::test_rpm_limit`
   - Impact: operational misconfiguration and incorrect capacity assumptions
   - Recommendation: update spec API/config sections to reflect canonical rate-limit values and override rules

2. Undocumented component introduced in implementation
   - Evidence: `src/services/video_processor.py:1`, import usage in `src/pipeline/main.py:28`
   - Impact: architecture diagram and dependency descriptions are stale
   - Recommendation: add component responsibility and interfaces to architecture/component sections

### Medium
1. Acceptance criteria for retry policy are non-measurable
   - Evidence: `_sdd/spec/apify_ig.md:210` ("retry sufficiently")
   - Impact: completion verification ambiguity during review/testing
   - Recommendation: replace with numeric retry bounds and failure thresholds

2. Missing documentation for new optional config
   - Evidence: `src/settings.py:64` (`ENABLE_PROXY_ROTATION`)
   - Impact: inconsistent runtime behavior across environments
   - Recommendation: add config field with default/value range and operational notes

### Low
1. Cross-link inconsistency in sub-spec index
   - Evidence: `_sdd/spec/apify_ig.md:88` (stale relative path)
   - Impact: lower navigability
   - Recommendation: normalize relative links

## Spec-Only Quality Notes

- Clarity: mostly clear, but retry and fallback language is ambiguous
- Completeness: core architecture present; config/options coverage incomplete
- Explainability: most components have Purpose only; 2 of 5 components lack Why/rationale explaining design motivation and existence reason
- Consistency: two conflicting statements found for API throughput
- Testability: several requirements are testable; retry/failure handling is not fully measurable
- Structure: index split is good; minor link hygiene issues remain

## Spec-to-Code Drift Notes

- Architecture: one new implementation component is not documented
- Features: implemented video handling not fully represented in feature list
- API: rate-limit values diverge from current middleware behavior
- Configuration: one new env option undocumented
- Issues/Technical debt: spec issue status lags behind test outcomes

## Open Questions

1. Should `VideoProcessor` be first-class in architecture, or remain internal under existing pipeline component?
2. Is proxy rotation optional by environment, or should production require it by default?

## Suggested Next Actions

1. Run `/spec-update-done` to apply high-priority corrections (API limits, architecture component mapping).
2. Convert ambiguous acceptance criteria into measurable thresholds.
3. Regenerate `/spec-summary` after approved updates are applied.

## Decision Log Follow-ups (Proposal Only)

- Proposed entry: "Rate-limit canonical policy update"
  - Context: Spec and middleware values diverged after recent scaling changes.
  - Decision: Use middleware-config values as the canonical policy source.
  - Rationale: Runtime behavior already depends on middleware settings.
  - Alternatives considered: Keep legacy static spec values (rejected: drift recurrence risk).
  - Impact / follow-up: Update rate-limit section and tests/docs cross-reference.

## Handoff for Spec Updates (if SYNC_REQUIRED)

- Recommended command: `/spec-update-done`
- Update priorities:
  - P1: API throughput/rate-limit alignment
  - P2: architecture and component documentation
  - P3: link hygiene and wording improvements
