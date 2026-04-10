## Spec Sync Report

**Reviewed**: 2026-04-10
**Code State**: `main`의 2026-04-10 커밋(`ee4e1cd`, `d32686a`, `aa92c83`, `0725c25`) 기준으로 skill/agent/docs contract가 업데이트되어 있다. global spec은 planning precedence, phase-gated execution, skill-defined dated artifact naming, active orchestrator path를 일부 누락한 상태였다.

### Change Summary
| Section | Delta IDs | Status | Action |
|--------|-----------|--------|--------|
| `_sdd/spec/main.md` | `A1 planning precedence`, `A2 phase-gated execution`, `A3 artifact naming/history`, `A4 mirror sync constraint` | IMPLEMENTED | guardrails와 key decisions에 repo-wide invariant를 반영 |
| `_sdd/spec/components.md` | `A1`, `A2`, `A3` | IMPLEMENTED | `sdd-autopilot`, `implementation-plan`, `spec-update-done`, `discussion`, platform note를 현재 contract에 맞게 보정 |
| `_sdd/spec/usage-guide.md` | `A1`, `A2`, `A3`, `A5 orchestrator path` | IMPLEMENTED | manual/autopilot scenario의 실행 흐름과 artifact path를 현재 docs contract에 맞게 보정 |
| `_sdd/spec/DECISION_LOG.md` | `A1-A5` | IMPLEMENTED | rationale 변화와 spec revision 근거를 기록 |
| `_sdd/spec/logs/changelog.md` | `A1-A5` | IMPLEMENTED | v4.1.5 변경 이력을 추가 |

### Applied Updates
- non-trivial planning은 `feature-draft`를 기본 entry로 두고 `implementation-plan`은 follow-up expansion으로 설명되도록 global spec을 수정했다.
- multi-phase plan이 생성되면 `per-phase` review-fix와 `final integration review`를 집행하는 운영 규칙을 global spec에 반영했다.
- temporary artifact의 canonical naming/history 규칙을 lowercase canonical + skill-defined dated slug + git-history-first로 정리했다.
- autopilot usage 시 활성 오케스트레이터 기준 경로를 `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`로 반영했다.
- discussion 산출물 경로를 `_sdd/discussion/<YYYY-MM-DD>_discussion_<slug>.md`로 usage/components surface에 반영했다.

### Deferred Items
- lowercase canonical `_sdd/spec/decision_log.md` 파일 자체는 아직 저장소에 materialize되지 않았으므로, global spec의 실제 decision log surface는 계속 `DECISION_LOG.md`를 사용한다.
- slash-command dry-run evidence는 이번 sync 범위 밖이라 global spec에는 추가하지 않았다.

### Open Questions
- `_sdd/spec/decision_log.md` canonical file 생성과 `DECISION_LOG.md` legacy fallback 정리는 별도 spec migration으로 분리할지 검토가 필요하다.
