## Spec Sync Report

**Reviewed**: 2026-04-13
**Code State**: `docs/*`, `.codex/skills/spec-{create,review,rewrite,upgrade}/*`, `.claude/skills/spec-{create,review,rewrite,upgrade}/*`, `.claude/agents/spec-review.md`, `.codex/agents/spec-review.toml`이 공통 코어 4축과 스킬별 1차 추가 축 기준으로 정렬되어 있다. global supporting surface는 이 구현을 아직 충분히 반영하지 못한 상태였다.

### Change Summary
| Section | Delta IDs | Status | Action |
|--------|-----------|--------|--------|
| `_sdd/spec/main.md` | `I4` | IMPLEMENTED | `Spec Version` / `Last Updated` 메타데이터를 supporting/history revision과 맞게 `v4.1.8` / `2026-04-13`으로 동기화 |
| `_sdd/spec/components.md` | `C2`, `C3`, `C4`, `C5`, `I4` | IMPLEMENTED | 네 개 lifecycle 스킬의 역할 설명과 notes를 현재 contract에 맞게 보정 |
| `_sdd/spec/usage-guide.md` | `C3`, `I4` | IMPLEMENTED | `/spec-create` expected result에서 stale old canonical wording 제거, thin global + single-file default 기준으로 정리 |
| `_sdd/spec/DECISION_LOG.md` | `C1`, `I4` | IMPLEMENTED | 공통 코어 4축과 네 개 스킬 역할 정렬의 판단 근거를 기록 |
| `_sdd/spec/logs/changelog.md` | `C1`, `I4` | IMPLEMENTED | v4.1.8 변경 이력 추가 |

### Applied Updates
- canonical main header를 `v4.1.8` / `2026-04-13`으로 올려 supporting/history surface revision과 맞췄다.
- `spec-create`를 single-file default와 structure rationale 기준으로 설명하도록 supporting surface를 수정했다.
- `spec-review`를 rubric separation + evidence strictness 중심 audit surface로 설명했다.
- `spec-rewrite`를 rationale preservation과 body/log placement를 가진 구조 개선 도구로 설명했다.
- `spec-upgrade`를 rewrite boundary를 먼저 판정하는 migration 도구로 설명했다.
- `/spec-create` expected result에서 old canonical(`CIV`, `usage`, `decision-bearing structure`) wording을 제거했다.

### Deferred Items
- lowercase canonical `_sdd/spec/decision_log.md` 파일 자체는 아직 materialize되지 않았으므로, 현재 저장소의 active history surface는 계속 `DECISION_LOG.md`를 사용한다.
- `_sdd/pipeline/` 아래 autopilot artifact의 authoritative status 정리는 이번 sync 범위 밖이다.

### Open Questions
- 없다. 이번 sync 범위의 supporting/history surface drift는 구현 결과 기준으로 모두 반영했다.
