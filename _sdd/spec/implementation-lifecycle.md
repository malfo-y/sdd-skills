# Implementation Lifecycle Skills

## Responsibility

- 이 그룹은 요구사항을 구현 가능한 작업 단위로 바꾸고, 실제 구현을 진행하고, 진행 상태를 검증하는 스킬을 담당한다.
- 핵심 연결 고리는 `feature-draft -> implementation-plan -> implementation -> implementation-review`다.
- 이 그룹은 canonical spec을 직접 수정하지 않는다. 구현 과정에서 생긴 문서 영향은 follow-up으로 넘긴다.

## Owned Paths

- `.codex/skills/feature-draft/`
- `.claude/skills/feature-draft/`
- `.codex/skills/implementation-plan/`
- `.claude/skills/implementation-plan/`
- `.codex/skills/implementation/`
- `.claude/skills/implementation/`
- `.codex/skills/implementation-review/`
- `.claude/skills/implementation-review/`
- `_sdd/implementation/`

## Key Symbols / Entry Points

- `.codex/skills/feature-draft/SKILL.md`
- `.claude/skills/feature-draft/SKILL.md`
- `.codex/skills/feature-draft/references/output-format.md`
- `.claude/skills/feature-draft/references/output-format.md`
- `.codex/skills/feature-draft/references/target-files-spec.md`
- `.claude/skills/feature-draft/references/target-files-spec.md`
- `.codex/skills/implementation-plan/references/target-files-spec.md`
- `.claude/skills/implementation-plan/references/target-files-spec.md`
- `.codex/skills/implementation/references/parallel-execution.md`
- `.claude/skills/implementation/references/parallel-execution.md`
- `.codex/skills/implementation-review/references/review-checklist.md`
- `.claude/skills/implementation-review/references/review-checklist.md`

## Interfaces / Contracts

### Draft and Plan Outputs

- `feature-draft`는 `_sdd/drafts/feature_draft_<name>.md` 형태의 통합 초안을 만든다.
- `implementation-plan`은 `_sdd/implementation/IMPLEMENTATION_PLAN*.md` 계열 문서를 만든다.
- `implementation`은 plan과 현재 spec을 읽되 `_sdd/spec/`은 수정하지 않는다.
- `implementation-review`는 진행 상태와 spec sync follow-up을 분류해서 보고한다.

### Shared Contracts

- spec 입력은 `Goal`, `Architecture Overview`, `Component Details`, `Open Questions` 중심으로 읽는다.
- target files가 확실하지 않으면 deterministic default + sequential fallback을 사용한다.
- spec 영향은 `MUST update`, `CONSIDER`, `NO update`로 분류한다.

## Dependencies

### Upstream

- spec lifecycle 그룹이 만든 탐색형 spec
- 사용자 요구사항 또는 `_sdd/spec/user_*`, `_sdd/drafts/*`

### Downstream

- `spec-update-todo`
- `spec-update-done`
- `pr-spec-patch`, `pr-review`

## Change Recipes

### feature draft 포맷을 바꿀 때

1. `feature-draft/references/output-format.md`를 먼저 수정한다.
2. `.codex/skills/`와 `.claude/skills/`의 `feature-draft`가 같은 포맷을 쓰는지 확인한다.
3. `implementation-plan`이 그 출력을 어떻게 소비하는지 확인한다.
4. `spec-update-todo`와의 입력 호환성도 같이 점검한다.

### Target Files / 병렬화 규칙을 바꿀 때

1. `.codex/skills/feature-draft/references/target-files-spec.md`
2. `.codex/skills/implementation-plan/references/target-files-spec.md`
3. `.codex/skills/implementation/references/parallel-execution.md`
4. 같은 이름의 `.claude/skills/` 대응 파일

위 세 파일을 세트로 보고 바꿔야 한다.

### 구현 중 spec sync follow-up 규칙을 바꿀 때

1. `.codex/skills/implementation/SKILL.md`, `.claude/skills/implementation/SKILL.md`
2. `.codex/skills/implementation-review/SKILL.md`, `.claude/skills/implementation-review/SKILL.md`
3. `.codex/skills/spec-update-done/SKILL.md`, `.claude/skills/spec-update-done/SKILL.md`

이 세 스킬은 플랫폼별 대응 파일까지 포함해 분류 체계가 어긋나지 않아야 한다.

## Tests / Observability

- `rg "Target Files|parallel|Spec Sync" .codex/skills/feature-draft .codex/skills/implementation* .claude/skills/feature-draft .claude/skills/implementation*`
- `_sdd/implementation/IMPLEMENTATION_PLAN.md`, `IMPLEMENTATION_REVIEW.md`와 현재 스킬 문구가 같은 개념을 쓰는지 확인
- example 파일에서 plan/draft/report 형식이 실제 `SKILL.md`와 일치하는지 점검

## Risks / Invariants

- `implementation`은 spec을 직접 수정하지 않는다.
- low-confidence target files는 병렬화보다 순차 실행이 우선이다.
- `feature-draft`의 spec patch 형식이 깨지면 `spec-update-todo`와의 연결이 약해진다.
- `implementation-review`는 단순 진척 요약이 아니라 spec sync follow-up까지 분명히 남겨야 한다.
- 같은 이름의 Codex/Claude 실행 스킬이 동시에 존재하므로, 한쪽만 바꾸면 사용자 기대와 설치 문서가 어긋날 수 있다.
