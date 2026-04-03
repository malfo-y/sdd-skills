# Implementation Progress: SDD Canonical Model Rollout

**Date**: 2026-04-04
**Source Draft**: `_sdd/drafts/feature_draft_sdd_canonical_model_rollout.md`
**Source Plan**: `_sdd/implementation/implementation_plan.md`
**Status**: DONE

| Task ID | Title | Phase | Dependencies | Status | Owner | Notes |
|---------|-------|-------|--------------|--------|-------|-------|
| FD-01 | Codex generator/transformer layer를 새 canonical model로 재작성 | Phase 1 | `docs/SDD_SPEC_DEFINITION.md` | DONE | implementation | `spec-create` / `spec-upgrade` SKILL, template, migration reference, examples를 current canonical model 기준으로 재작성 |
| FD-02 | Claude generator/transformer mirror 동기화 | Phase 1 | FD-01 | DONE | implementation | `.claude/skills/spec-create` / `.claude/skills/spec-upgrade` mirror를 Codex current canonical semantics와 semantic parity로 동기화했고, review follow-up으로 Claude-native interaction contract drift를 보정 |
| FD-03 | Consumer / review layer 재정렬 | Phase 2 | FD-01, FD-02 | DONE | implementation | `spec-review`, `spec-summary`, `spec-rewrite`의 global/temporary rubric과 rewrite template를 current canonical model 기준으로 정렬 |
| FD-04 | Planning / update / orchestration layer 전환 | Phase 2 | FD-01, FD-02, FD-03 | DONE | implementation | `feature-draft`, `implementation-plan`, `spec-update-*`, `sdd-autopilot`을 temporary spec delta/validation model로 전환했고, review follow-up으로 Claude wrapper의 Codex-only primitive/drift를 제거 |
| FD-05 | Korean docs sync | Phase 3 | FD-03, FD-04 | DONE | implementation | `docs/SDD_WORKFLOW.md`, `docs/SDD_QUICK_START.md`, `docs/SDD_CONCEPT.md`, `docs/sdd.md`를 새 canonical model과 current skill behavior 기준으로 재작성 |
| FD-06 | English mirror sync | Phase 4 | FD-05 | DONE | implementation | `docs/en/SDD_SPEC_DEFINITION.md`, `docs/en/SDD_WORKFLOW.md`, `docs/en/SDD_QUICK_START.md`, `docs/en/SDD_CONCEPT.md`를 semantic parity로 동기화하고 `docs/en/sdd.md`를 생성 |
| FD-07 | Cross-surface drift audit | Phase 5 | FD-06 | DONE | implementation | `guide-create` collateral template를 갱신하고 target-surface grep audit 및 `_sdd/spec/logs/spec_review_report_canonical_model_rollout.md`를 생성. repo-wide residual drift는 out-of-scope follow-up으로 기록 |
