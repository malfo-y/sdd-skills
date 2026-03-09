# Spec Review Report (Strict)

**Date**: 2026-02-07
**Reviewer**: Claude
**Scope**: Spec+Code
**Spec Files**:
- `_sdd/spec/apify_ig.md`
- `_sdd/spec/apify_ig/02-architecture.md`
- `_sdd/spec/apify_ig/04-interfaces.md`
**Code State**: Workspace + recent commits (`abc1234..def5678`)
**Decision**: SYNC_REQUIRED

## Executive Summary

The spec remains mostly aligned with project intent, but multiple high-confidence drifts were found in API limits and component boundaries. Navigation surfaces (Repository Map, Component Index) are stale relative to recent implementation changes. The document also has medium-severity quality gaps in acceptance criteria definition. Spec updates are required before the next implementation planning cycle.

## Findings by Severity

### High
1. API rate-limit mismatch between spec and code
   - Evidence: `src/config/rate_limit.py:12`, `src/api/middleware.py:47`, integration test `tests/test_rate_limit.py::test_rpm_limit`
   - Impact: operational misconfiguration and incorrect capacity assumptions
   - Recommendation: update spec API/config sections to reflect canonical rate-limit values and override rules

2. Undocumented component introduced in implementation
   - Evidence: `src/services/video_processor.py:1`, import usage in `src/pipeline/main.py:28`
   - Impact: architecture diagram and dependency descriptions are stale; Component Index is missing this entry
   - Recommendation: add component responsibility and interfaces to architecture/component sections

3. Stale Repository Map — new `src/services/` subdirectory not reflected
   - Evidence: `src/services/video_processor.py`, `src/services/thumbnail_cache.py` exist but Repository Map lists only `src/pipeline/`, `src/api/`, `src/config/`
   - Impact: LLM or developer navigating via spec will miss the services layer entirely
   - Recommendation: update Repository Map to include `src/services/` with role description

### Medium
1. Acceptance criteria for retry policy are non-measurable
   - Evidence: `_sdd/spec/apify_ig.md:210` ("retry sufficiently")
   - Impact: completion verification ambiguity during review/testing
   - Recommendation: replace with numeric retry bounds and failure thresholds

2. Missing documentation for new optional config
   - Evidence: `src/settings.py:64` (`ENABLE_PROXY_ROTATION`)
   - Impact: inconsistent runtime behavior across environments
   - Recommendation: add config field with default/value range and operational notes

3. Component Index stale — `VideoProcessor` ownership path missing
   - Evidence: Component Index lists 4 components; implementation has 5 (`VideoProcessor` added in commit `e7f8901`)
   - Impact: responsibility boundaries unclear for new component
   - Recommendation: add `VideoProcessor` entry with 책임/비책임/경로

4. Common Change Paths not updated for video processing scenario
   - Evidence: adding a new media type now requires touching `src/services/video_processor.py` + `src/pipeline/main.py` + `tests/test_video.py`, but Change Paths only documents image-related scenarios
   - Impact: developer editing video flow has no guided entry point
   - Recommendation: add "Add/modify video processing" change path

### Low
1. Cross-link inconsistency in sub-spec index
   - Evidence: `_sdd/spec/apify_ig.md:88` (stale relative path)
   - Impact: lower navigability
   - Recommendation: normalize relative links

## Entry Point / Navigation Notes

- **Goal clarity**: Goal section clearly states the project purpose in one paragraph. Adequate.
- **System Boundary**: External API dependencies (Instagram API, proxy service) are listed but proxy failover behavior is not bounded.
- **Repository Map**: Stale — missing `src/services/` directory added in recent commits. (High finding #3)
- **Runtime Map**: Request flow diagram covers the image pipeline but does not show the video processing branch added later.
- **Component Index**: Missing `VideoProcessor` component. 4 of 5 implementation components are documented. (Medium finding #3)

## Changeability Notes

- **Common Change Paths**: Covers image-related scenarios well. Video processing scenario is missing. (Medium finding #4)
- **Test/debug discoverability**: Test file naming convention (`tests/test_<module>.py`) is documented; debug logging entry points are not mentioned.
- **Responsibility boundaries**: Clear for original 4 components. `VideoProcessor` lacks 책임/비책임 distinction, making it unclear whether thumbnail generation belongs here or in the pipeline.

## Spec-to-Code Drift Notes

- **Architecture**: one new implementation component (`VideoProcessor`) is not documented
- **Features**: implemented video handling not fully represented in feature list
- **API**: rate-limit values diverge from current middleware behavior
- **Configuration**: one new env option (`ENABLE_PROXY_ROTATION`) undocumented
- **Issues/Technical debt**: spec issue status lags behind test outcomes
- **Navigation drift**: Repository Map missing `src/services/`, Component Index missing `VideoProcessor`, Common Change Paths missing video scenario

## LLM Efficiency Notes

- **Token cost of entry**: Goal + System Boundary are concise (~40 lines). Good entry point efficiency.
- **Navigation precision**: Repository Map is stale, causing an LLM to potentially explore wrong directories before finding `src/services/`. Fixing the map would save 1-2 unnecessary glob/grep cycles.
- **선택 섹션 과잉 여부**: No unnecessary OPT sections present. The spec is lean. No action needed.

## Open Questions

1. Should `VideoProcessor` be first-class in architecture, or remain internal under existing pipeline component?
2. Is proxy rotation optional by environment, or should production require it by default?
3. Should Runtime Map be split into separate image/video flow diagrams, or kept as a single unified diagram?

## Suggested Next Actions

1. Run `/spec-update-done` to apply high-priority corrections (API limits, Repository Map, Component Index).
2. Add `VideoProcessor` to Component Index with 책임/비책임/경로.
3. Add video processing scenario to Common Change Paths.
4. Convert ambiguous acceptance criteria into measurable thresholds.
5. Regenerate `/spec-summary` after approved updates are applied.

## Decision Log Follow-ups (Proposal Only)

- Proposed entry: "Rate-limit canonical policy update"
  - Context: Spec and middleware values diverged after recent scaling changes.
  - Decision: Use middleware-config values as the canonical policy source.
  - Rationale: Runtime behavior already depends on middleware settings.
  - Alternatives considered: Keep legacy static spec values (rejected: drift recurrence risk).
  - Impact / follow-up: Update rate-limit section and tests/docs cross-reference.

- Proposed entry: "VideoProcessor component boundary"
  - Context: Video processing was added incrementally without spec update.
  - Decision: (pending — requires team input)
  - Rationale: —
  - Alternatives considered: (a) first-class component, (b) sub-module of pipeline
  - Impact / follow-up: Affects Component Index, Runtime Map, and Change Paths structure.

## Handoff for Spec Updates (if SYNC_REQUIRED)

- Recommended command: `/spec-update-done`
- Update priorities:
  - P1: API throughput/rate-limit alignment, Repository Map update
  - P2: Component Index + VideoProcessor documentation
  - P3: Common Change Paths + link hygiene
