# Spec Review Report

**Review Date**: 2026-04-03
**Reviewed Spec**: `docs/SDD_SPEC_DEFINITION.md`
**Decision**: NEEDS_DISCUSSION

## 1. Findings

### Critical

1. **The revised definition is not yet a stable canonical definition because it conflicts with the rest of the SDD system.**
   - The reviewed document redefines the spec around `high-level concept + scope/non-goals/guardrails + key decisions + selective code map` and makes `전략적 Code Map` optional in the recommended structure. See [SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md#L44), [SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md#L107), [SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md#L153), [SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md#L200).
   - But the surrounding documentation and tooling still define the canonical spec as a fuller `whitepaper §1-§8` document with architecture/component detail as core structure. See [SDD_WORKFLOW.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_WORKFLOW.md#L61), [SDD_WORKFLOW.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_WORKFLOW.md#L32), [SDD_QUICK_START.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_QUICK_START.md#L9), [SDD_QUICK_START.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_QUICK_START.md#L30), [SDD_CONCEPT.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_CONCEPT.md#L9), [SDD_CONCEPT.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_CONCEPT.md#L24), [spec-upgrade/SKILL.md](/Users/hyunjoonlee/github/sdd_skills/.codex/skills/spec-upgrade/SKILL.md#L3), [spec-upgrade/SKILL.md](/Users/hyunjoonlee/github/sdd_skills/.codex/skills/spec-upgrade/SKILL.md#L11), [spec-upgrade/SKILL.md](/Users/hyunjoonlee/github/sdd_skills/.codex/skills/spec-upgrade/SKILL.md#L122).
   - The English mirror is also still on the old definition. See [en/SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/en/SDD_SPEC_DEFINITION.md#L44), [en/SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/en/SDD_SPEC_DEFINITION.md#L127).
   - As a result, the doc may be philosophically improved, but it is not yet operationally true inside this repo.

### Quality

2. **The document de-emphasizes implementation detail without promoting executable contracts to first-class required content.**
   - The revised definition strongly emphasizes concept, scope, guardrails, and navigation hints, but it never explicitly makes `I/O`, `preconditions`, `postconditions`, and `invariants` mandatory sections or mandatory subcontent. See [SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md#L44), [SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md#L98), [SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md#L217).
   - That is a real gap because SDD’s broader philosophy explicitly frames the spec as a contract and defines verifiability through I/O, preconditions, postconditions, and invariants. See [sdd.md](/Users/hyunjoonlee/github/sdd_skills/docs/sdd.md#L60), [sdd.md](/Users/hyunjoonlee/github/sdd_skills/docs/sdd.md#L68), [sdd.md](/Users/hyunjoonlee/github/sdd_skills/docs/sdd.md#L78), [sdd.md](/Users/hyunjoonlee/github/sdd_skills/docs/sdd.md#L97), [sdd.md](/Users/hyunjoonlee/github/sdd_skills/docs/sdd.md#L107), [sdd.md](/Users/hyunjoonlee/github/sdd_skills/docs/sdd.md#L185).
   - Without this, the new definition risks becoming a thinner orientation document rather than an executable spec.

3. **The document hardens unresolved design choices as if they were settled.**
   - The discussion record explicitly left open where the strategic code map should live and how much architecture/component detail should remain in the persistent spec. See [discussion_whitepaper_for_humans_vs_llms.md](/Users/hyunjoonlee/github/sdd_skills/_sdd/discussion/discussion_whitepaper_for_humans_vs_llms.md#L29), [discussion_whitepaper_for_humans_vs_llms.md](/Users/hyunjoonlee/github/sdd_skills/_sdd/discussion/discussion_whitepaper_for_humans_vs_llms.md#L31).
   - But the reviewed document already fixes `전략적 Code Map` as `§4` in the recommended structure and relegates architecture/component detail to optional reference material or separate docs. See [SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md#L153), [SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md#L166).
   - That is premature specification. It turns open questions into normative structure without an explicit decision log or migration rule.

4. **“Implementation Details” is mapped too aggressively to “strategic code map / navigation hint,” which is conceptually inaccurate.**
   - In the paper-to-spec mapping table, `Implementation Details` now maps to “필요한 경우에만 남기는 전략적 code map / navigation hint.” See [SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md#L87).
   - A navigation hint is not the same thing as implementation detail. This overcorrection removes a clear conceptual home for architecturally significant design detail that is too important to leave entirely to ad hoc code search.
   - The rest of the document partly compensates for this by keeping “핵심 설계와 주요 결정,” but the mapping table still teaches the wrong abstraction.

5. **The global-vs-temporary distinction remains too soft for the main thesis of this revision.**
   - The core motivation of the revision is that the persistent human-facing spec should be thinner, while LLMs can recover detail on demand.
   - Yet the section that claims the definition applies to both global and temporary specs only says that temporary specs “can contain more implementation-oriented information.” See [SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md#L193), [SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md#L208).
   - This is not operational enough. The reader still does not know which parts are mandatory for global specs, which become optional for global specs, and which become strongly expected in temporary specs.

### Improvements

6. **Term control is weak for a definition document.**
   - The document mixes Korean and English labels (`high-level concept`, `scope`, `guardrails`, `navigation hint`, `code map`) without a small glossary or canonical Korean equivalents. See [SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md#L44), [SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md#L100), [SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md#L123).
   - That is not fatal, but in a canonical definition doc, terminology drift tends to propagate into templates and skills quickly.

## 2. Spec Quality Summary

The revised document is directionally strong. It captures the core insight from the discussion: humans and LLMs do not need the same information density, and a persistent SDD spec should emphasize orientation, scope boundaries, and guardrails rather than duplicate the codebase. The `scope` clarification is especially good and materially improves the definition.

However, as a canonical definition, the document is not yet mature. It currently has three structural weaknesses:

- it is inconsistent with the rest of the repository’s documentation and tooling
- it does not restore a first-class place for executable contracts after demoting implementation detail
- it hardens several still-open structural choices into normative guidance

So the document is philosophically promising but systemically premature.

## 3. Drift Summary

- **ALIGNED with the latest discussion** on thinner persistent specs, scope as boundary, and selective code maps. See [discussion_whitepaper_for_humans_vs_llms.md](/Users/hyunjoonlee/github/sdd_skills/_sdd/discussion/discussion_whitepaper_for_humans_vs_llms.md#L20), [discussion_whitepaper_for_humans_vs_llms.md](/Users/hyunjoonlee/github/sdd_skills/_sdd/discussion/discussion_whitepaper_for_humans_vs_llms.md#L22), [discussion_whitepaper_for_humans_vs_llms.md](/Users/hyunjoonlee/github/sdd_skills/_sdd/discussion/discussion_whitepaper_for_humans_vs_llms.md#L23), [discussion_whitepaper_for_humans_vs_llms.md](/Users/hyunjoonlee/github/sdd_skills/_sdd/discussion/discussion_whitepaper_for_humans_vs_llms.md#L25).
- **DRIFT from surrounding docs and skills** that still assume the older “whitepaper §1-§8 with architecture/component detail” model. See [SDD_WORKFLOW.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_WORKFLOW.md#L61), [SDD_QUICK_START.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_QUICK_START.md#L30), [spec-upgrade/SKILL.md](/Users/hyunjoonlee/github/sdd_skills/.codex/skills/spec-upgrade/SKILL.md#L18).
- **DRIFT from the broader SDD philosophy** because contracts/verifiability are central in [sdd.md](/Users/hyunjoonlee/github/sdd_skills/docs/sdd.md#L97) but not first-class in the reviewed definition.

## 4. Code Analysis Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| Top Hotspots | `spec-create` (41), `spec-rewrite` (33), `spec-review` (27), `_sdd/spec/main.md` (24), `SDD_WORKFLOW.md` (22) | Recent churn is concentrated in spec-generation and workflow assets, so definition drift will propagate quickly if left unresolved. |
| Focus Score | N/A | This review targeted a definition document, not a feature slice with changed implementation files. |
| Test Coverage | N/A | No executable test surface applies to this documentation-only review. |

## 5. Recommended Next Actions

1. Decide whether this document is now the new canonical model or still an exploratory thesis. If canonical, sync [SDD_WORKFLOW.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_WORKFLOW.md), [SDD_QUICK_START.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_QUICK_START.md), [SDD_CONCEPT.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_CONCEPT.md), the English mirror, and `spec-upgrade`/`spec-create` templates in the same change set.
2. Add an explicit `Contract / Invariants / Verifiability` requirement to the definition so the new thinner model does not collapse into a non-executable overview.
3. Resolve the open structural questions before standardizing the recommended layout:
   - whether `전략적 Code Map` belongs in the main body, appendix, or separate artifact
   - whether `Architecture Details` / `Component Details` are optional sections, appendix material, or temporary-spec-only material
4. Reword the paper-mapping table so `Implementation Details` does not collapse into `navigation hint`.
5. Strengthen the `global spec` vs `temporary spec` section with explicit expectations about information density and mandatory sections for each.
