# Implementation Progress: lowercase artifact canonical naming rollout

**Date**: 2026-04-02
**Source Draft**: `_sdd/drafts/feature_draft_lowercase_artifact_filenames.md`
**Status**: COMPLETE

| Task ID | Title | Phase | Dependencies | Status | Owner | Notes |
|---------|-------|-------|--------------|--------|-------|-------|
| T1 | Add lowercase canonical artifact naming policy and path map to repo spec | Phase 1 | None | DONE | implementation | `_sdd/spec/main.md`에 artifact naming policy, lowercase canonical artifact map, transition fallback 규칙 반영 |
| T2 | Update implementation-family skill and agent contracts to lowercase canonical paths | Phase 2 | T1 | DONE | implementation | `feature-draft`, `implementation-plan`, `implementation`, `implementation-review`, `sdd-autopilot`, mirror agents에 lowercase canonical path + legacy uppercase fallback 반영 |
| T3 | Update spec/reporting-family skill and agent contracts to lowercase canonical paths | Phase 2 | T1 | DONE | implementation | `spec-summary`, `spec-review`, `spec-rewrite`, `spec-snapshot`, `spec-create`, `spec-update-done`, `spec-update-todo`, `spec-upgrade` 관련 경로 및 mirror 정렬 |
| T4 | Normalize supporting skills and backup/archive rules | Phase 3 | T1 | DONE | implementation | `pr-review`, `guide-create`와 backup/archive prefix를 `prev_*` canonical로 정리 |
| T5 | Sync examples, templates, and orchestrator references | Phase 3 | T2, T3, T4 | DONE | implementation | `.codex` / `.claude` example/reference/template/orchestrator 문서를 canonical lowercase path 기준으로 동기화 |
| T6 | Verify repo-wide path consistency and document deferred historical rename scope | Phase 4 | T2, T3, T4, T5 | DONE | implementation | `git diff --check` PASS, 잔여 uppercase reference는 intentional fallback 또는 historical changelog로만 남김 |
