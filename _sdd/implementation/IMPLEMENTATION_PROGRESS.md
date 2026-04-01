# Implementation Progress: Remove write_skeleton and Shift to Inline 2-Phase Writing

**Date**: 2026-04-01
**Source Draft**: `_sdd/drafts/feature_draft_remove_write_skeleton_inline_writing.md`
**Status**: COMPLETE

| Task ID | Title | Phase | Dependencies | Status | Owner | Notes |
|---------|-------|-------|--------------|--------|-------|-------|
| T1 | Delete Claude/Codex `write_skeleton` agent files | Runtime | None | DONE | implementation | `.claude/agents/write-skeleton.md`, `.codex/agents/write-skeleton.toml` 삭제 |
| T2 | Redefine `write-phased` as inline 2-phase writing contract | Runtime | T1 | DONE | implementation | Claude/Codex `SKILL.md`, `skill.json`, Codex agent README 갱신 |
| T3 | Replace current caller guidance from helper delegation to caller-owned skeleton writing | Runtime | T2 | DONE | implementation | Claude/Codex writing producer 문구 일괄 치환 |
| T4 | Sync current spec and decision docs | Docs | T1, T2, T3 | DONE | implementation | `_sdd/spec/main.md`, `_sdd/spec/DECISION_LOG.md` 갱신 |
| T5 | Verify current runtime/spec cleanliness | Verify | T1, T2, T3, T4 | DONE | implementation | `rg -uuu ...`, `git diff --check` 통과 |
