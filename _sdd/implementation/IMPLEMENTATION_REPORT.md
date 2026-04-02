# Implementation Report: lowercase artifact canonical naming rollout

## Progress Summary

- Total Tasks: 6
- Completed: 6
- Deferred: 0
- Targeted Files Modified: 73
- Verification: `git diff --check` PASS, uppercase artifact grep reduced to intentional fallback + historical changelog references only

## Completed Tasks

- [x] `_sdd/spec/main.md`에 lowercase canonical artifact naming policy와 artifact map을 반영했다.
- [x] `.codex` / `.claude` implementation-family skill contracts를 lowercase canonical path 기준으로 정리했다.
- [x] mirror agent files(`.codex/agents/*.toml`, `.claude/agents/*.md`)도 같은 경로 계약으로 동기화했다.
- [x] `spec-summary`, `spec-review`, `spec-rewrite`, `spec-snapshot`, `spec-create`, `spec-update-*`, `spec-upgrade` 관련 path/reference를 lowercase canonical 기준으로 정리했다.
- [x] `pr-review`, `guide-create`, `sdd-autopilot` examples/references를 포함한 지원 문서를 lowercase canonical path와 `prev_*` backup 규칙으로 정리했다.
- [x] transition 기간용 legacy uppercase fallback 문구를 핵심 plan/review/reporting 스킬과 agent에 반영했다.

## Deferred / Partial Tasks

- 없음

## Files Changed

- Repo spec policy: `_sdd/spec/main.md`
- Codex mirrors: `.codex/skills/*`, `.codex/agents/*`
- Claude mirrors: `.claude/skills/*`, `.claude/agents/*`
- Runtime artifact: `_sdd/implementation/IMPLEMENTATION_PROGRESS.md`, `_sdd/implementation/IMPLEMENTATION_REPORT.md`

## Key Design Choices

- canonical naming은 소문자 `snake_case`로 통일하고, 새 출력은 모두 lowercase 경로를 기준으로 설명했다.
- 실제 historical artifact rename은 이번 범위에서 제외했다. changelog와 과거 백업 경로는 당시 실제 파일명을 유지할 수 있도록 남겼다.
- transition 기간에는 reader가 lowercase canonical을 먼저 보고, 없으면 legacy uppercase를 fallback으로 확인하도록 계약을 추가했다.
- `spec_review_report.md` canonical path는 `_sdd/spec/logs/`로 정리했다.
- `spec-rewrite-plan.md`, `discussion_<title>.md`, `guide_<slug>.md`처럼 이미 lowercase인 artifact는 기존 canonical을 유지했다.

## Verification

- `git diff --check`
  - PASS
- `rg -n "IMPLEMENTATION_PLAN|IMPLEMENTATION_REPORT|IMPLEMENTATION_REVIEW|IMPLEMENTATION_PROGRESS|SPEC_REVIEW_REPORT|REWRITE_REPORT|DECISION_LOG|PR_REVIEW|PREV_" .codex/skills .claude/skills .codex/agents .claude/agents _sdd/spec/main.md`
  - 잔여 uppercase reference는 1) intentional legacy fallback 2) `_sdd/spec/main.md` changelog의 historical actual path만 남음
- `_sdd/env.md` 확인
  - 이 저장소는 전통적 테스트 프레임워크가 없고, 문서 위생/정합성 검증 중심이므로 문서 검증 명령으로 확인

## Unplanned Dependency

- 없음

## Notes

- bulk path normalization 과정에서 `_COMMENTS.md`도 diff 대상에 포함되어 있었지만, 이 파일은 현재 작업 범위 밖의 기존 변경으로 간주하고 구현 결과/검증 대상에서 제외했다.
- 실제 파일 rename이나 duplicate lowercase artifact 생성은 이번 범위에 포함하지 않았다.
- 현재 repo에는 legacy uppercase artifact가 실제 파일로 남아 있으므로, 새 계약은 “lowercase write + uppercase fallback read”를 전제로 한다.

## Conclusion

**READY** -- `_sdd/` artifact naming contract가 lowercase canonical 기준으로 정리됐고, `.codex` / `.claude` / agent mirror / examples / references / repo spec이 같은 규칙을 공유하도록 동기화됐다. historical artifact rename은 의도적으로 보류했고, transition 기간 호환성 문구까지 포함해 바로 사용할 수 있는 상태다.
