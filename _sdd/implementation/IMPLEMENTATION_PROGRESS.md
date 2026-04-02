# Implementation Progress: spec-rewrite Quality Rubric and Whitepaper Alignment

**Date**: 2026-04-02
**Source Draft**: `_sdd/drafts/feature_draft_spec_rewrite_quality_rubric.md`
**Status**: COMPLETE_WITH_DEFERRED_SPEC_SYNC

| Task ID | Title | Phase | Dependencies | Status | Owner | Notes |
|---------|-------|-------|--------------|--------|-------|-------|
| T1 | Define 8-metric rubric and scoring contract in spec-rewrite SKILLs | Phase 1 | None | DONE | implementation | `.codex` / `.claude` SKILL.md 모두 `0-3` scoring + metric vocabulary 반영 |
| T2 | Connect plan/validation/output contract to rubric | Phase 1 | T1 | DONE | implementation | metric-driven rationale, whitepaper warnings, report contract 강화 |
| T3 | Add metric scorecard + whitepaper fit assessment to rewrite report examples | Phase 1 | T1, T2 | DONE | implementation | 양쪽 example 리포트에 scorecard / unresolved warnings 추가 |
| T4 | Rebuild rewrite-checklist as question-style rubric | Phase 2 | T1 | DONE | implementation | 8개 metric 각각에 질문형 rubric 추가 |
| T5 | Align spec-format reference with `docs/SDD_SPEC_DEFINITION.md` | Phase 2 | T1 | DONE | implementation | section presence + explanation quality + rewrite boundary 반영 |
| T6 | Sync `.codex` and `.claude` spec-rewrite document sets and bump versions | Phase 2 | T1, T2, T3, T4, T5 | DONE | implementation | `skill.json` 양쪽 `1.6.0`으로 갱신 |
| T7 | Update `_sdd/spec/main.md` spec-rewrite description | Phase 3 | T1, T2, T3, T4, T5, T6 | DEFERRED | implementation | `implementation` Hard Rule 1에 따라 `_sdd/spec/` 수정 불가. 후속 `spec-update-done` 또는 별도 작업으로 이관 |
| T8 | Run consistency and hygiene verification | Phase 3 | T6 | DONE | implementation | `git diff --check` PASS, metric vocabulary grep PASS |
