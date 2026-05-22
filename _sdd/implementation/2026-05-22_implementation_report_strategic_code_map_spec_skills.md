# Implementation Report: Strategic Code Map Spec Skills

## Summary

`Strategic Code Map`을 SDD spec lifecycle의 optional navigation surface로 표준화했다. global spec의 mandatory core는 유지하면서, 작은 repo에서는 compact appendix로, 큰 repo에서는 supporting surface로 분리하는 규칙을 docs, skill, agent mirror에 반영했다.

## Completed Tasks

- canonical docs에 `Strategic Code Map` 정의와 배치 규칙 추가
- Codex/Claude `spec-create`와 template/example 수정
- Codex/Claude `spec-review`, `spec-rewrite`, `spec-upgrade`, `spec-summary`, `spec-update-todo`, `spec-update-done`, `feature-draft` 수정
- Codex/Claude agent mirror(`feature-draft`, `spec-review`, `spec-update-todo`, `spec-update-done`) 수정
- feature draft와 implementation progress artifact 작성
- implementation-review 지적사항 반영:
  - Claude `feature-draft` skill에 누락된 `Strategic Code Map` 재검증 문장 3개 추가
  - Codex `feature-draft` skill-agent final checklist 순서 동기화
  - Claude `feature-draft` Hard Rule 번호를 Codex와 정렬
  - `feature-draft` supporting surface discovery 문장 구체화
  - `spec-create` Structure Decision 표의 `분할 축` 표현을 `탐색 축 / 배치`로 명확화

## Validation

| Check | Result | Notes |
|-------|--------|-------|
| `git diff --check` | PASS | whitespace 오류 없음 |
| TOML parse | PASS | `.codex/agents/*.toml` 모두 parse 성공 |
| targeted `rg` | PASS | docs / `.codex` / `.claude`에 핵심 문구 반영 확인 |
| skill mirror spot check | PASS | `spec-create`, `spec-review`, `spec-rewrite`, `spec-upgrade`, `spec-summary` Codex/Claude skill body 동일 |
| normalized skill-agent compare | PASS | `feature-draft`, `spec-review`, `spec-update-todo`, `spec-update-done` Codex/Claude 모두 frontmatter/wrapper 제외 본문 일치 |
| stale rule reference check | PASS | Claude `feature-draft`에 오래된 Hard Rule 9/10 참조 없음 |

## Unplanned Dependencies

- 없음.

## Deferred Items

- `_sdd/implementation/*`는 현재 `.gitignore` 대상이라 progress/report artifact는 로컬 파일로만 남는다.
- downstream project spec 리라이트는 이번 범위 밖이다.

## Follow-up

- downstream project spec 리라이트는 이번 범위 밖이다.
