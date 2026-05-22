# Implementation Progress: Strategic Code Map Spec Skills

| task_id | title | phase | dependencies | status | owner/sub-agent | notes |
|---------|-------|-------|--------------|--------|-----------------|-------|
| T1 | canonical docs에 Strategic Code Map 정의 추가 | Phase 1 | - | DONE | Codex | `docs/SDD_SPEC_DEFINITION.md`, `docs/en/SDD_SPEC_DEFINITION.md` 수정 |
| T2 | Codex spec-create 동작 수정 | Phase 1 | T1 | DONE | Codex | primary axis, compact map, supporting surface 규칙 추가 |
| T3 | Claude spec-create mirror 수정 | Phase 1 | T2 | DONE | Codex | Codex skill과 normative rule 동기화 |
| T4 | spec-create template/example 수정 | Phase 1 | T2,T3 | DONE | Codex | Codex/Claude template과 examples에 Strategic Code Map 예시 추가 |
| T5 | spec quality/migration skill 수정 | Phase 2 | T1 | DONE | Codex | review/rewrite/upgrade skill pair 수정 |
| T6 | spec sync/summary skill 수정 | Phase 2 | T1 | DONE | Codex | update-todo/update-done/summary skill pair 수정 |
| T7 | feature-draft skill 수정 | Phase 2 | T1 | DONE | Codex | map-as-hint 및 current-code verification rule 추가 |
| T8 | wrapper-backed agent mirror 수정 | Phase 3 | T5,T6,T7 | DONE | Codex | feature-draft/spec-review/spec-update-* Codex/Claude agent mirror 수정 |
| T9 | wording과 mirror parity 검증 | Phase 4 | T1-T8 | DONE | Codex | `git diff --check`, TOML parse, targeted `rg`, 주요 mirror 비교 완료 |
| T10 | implementation-review High finding 수정 | Review Fix | T9 | DONE | Codex | Claude `feature-draft` skill에 누락된 Strategic Code Map 재검증 문장 반영 |
| T11 | feature-draft mirror parity 보정 | Review Fix | T10 | DONE | Codex | Codex/Claude feature-draft skill-agent normalized body 일치 확인 |
| T12 | rule numbering/wording 보정 | Review Fix | T10 | DONE | Codex | Claude feature-draft Hard Rule 번호를 Codex와 정렬, supporting surface discovery 문구 구체화 |
| T13 | spec-create wording 보정 | Review Fix | T10 | DONE | Codex | `분할 축`을 `탐색 축 / 배치`로 변경해 small repo appendix case 명확화 |

## Plan Assumptions

- 사용자 확인이 필요한 Open Question 없음.
- `docs/en/SDD_SPEC_DEFINITION.md`는 존재하므로 영어 mirror도 수정 대상으로 포함했다.
- implementation execution agent 계열은 direct dependency가 발견되지 않는 한 수정하지 않는다.

## Phase Surprises

- 없음.

## Review Fix Verification

- `feature-draft` normalized skill-agent compare: PASS for Codex and Claude.
- `spec-review`, `spec-update-todo`, `spec-update-done` normalized skill-agent compare: PASS for Codex and Claude.
- Claude `feature-draft` stale Hard Rule 9/10 references: none.
- `.codex/agents/*.toml` parse: PASS.
- `git diff --check`: PASS.
