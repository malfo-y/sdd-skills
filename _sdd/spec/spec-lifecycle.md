# Spec Lifecycle Skills

## Responsibility

- 이 그룹은 탐색형 스펙을 만들고, 재구성하고, 요약하고, 리뷰하고, 계획/구현 결과를 다시 스펙에 반영하는 스킬을 담당한다.
- 이 그룹의 핵심 목표는 “코드의 복사본”이 아니라 “이해와 안전한 변경을 위한 지도”를 유지하는 것이다.
- 이 그룹은 구현 코드를 직접 만드는 역할을 하지 않는다.

## Owned Paths

- `.codex/skills/spec-create/`
- `.claude/skills/spec-create/`
- `.codex/skills/spec-rewrite/`
- `.claude/skills/spec-rewrite/`
- `.codex/skills/spec-summary/`
- `.claude/skills/spec-summary/`
- `.codex/skills/spec-review/`
- `.claude/skills/spec-review/`
- `.codex/skills/spec-update-todo/`
- `.claude/skills/spec-update-todo/`
- `.codex/skills/spec-update-done/`
- `.claude/skills/spec-update-done/`
- `SDD_SPEC_REQUIREMENTS.md`
- `SDD_WORKFLOW.md`
- `SDD_CONCEPT.md`

## Key Symbols / Entry Points

- 각 플랫폼 스킬의 `SKILL.md`, `skill.json`
- `.codex/skills/spec-create/references/template-full.md`
- `.claude/skills/spec-create/references/template-full.md`
- `.codex/skills/spec-create/references/optional-sections.md`
- `.claude/skills/spec-create/references/optional-sections.md`
- `.codex/skills/spec-review/references/review-checklist.md`
- `.claude/skills/spec-review/references/review-checklist.md`
- `.codex/skills/spec-update-todo/references/input-format.md`
- `.claude/skills/spec-update-todo/references/input-format.md`
- `.codex/skills/spec-update-done/references/update-strategies.md`
- `.claude/skills/spec-update-done/references/update-strategies.md`

## Interfaces / Contracts

### Stable Spec Anchors

이 그룹은 아래 상위 앵커를 기준으로 서로 호환된다.

- `Goal`
- `Architecture Overview`
- `Component Details`
- `Environment & Dependencies`
- `Identified Issues & Improvements`
- `Usage Examples`
- `Open Questions`

### Spec Update Classification

계획/구현/PR 변화는 아래 분류를 공유한다.

- `MUST update`
- `CONSIDER`
- `NO update`

### Expected Outputs

- canonical spec: `_sdd/spec/main.md` 또는 컴포넌트 스펙
- review-only output: `_sdd/spec/SPEC_REVIEW_REPORT.md`
- summary output: `_sdd/spec/SUMMARY.md`
- planned patch input: `spec-update-todo`가 소비하는 입력 포맷

## Dependencies

### Upstream

- `SDD_SPEC_REQUIREMENTS.md`
- `SDD_WORKFLOW.md`
- `SDD_CONCEPT.md`
- 사용자 프로젝트의 `_sdd/spec/` 구조

### Downstream

- `feature-draft`
- `implementation-plan`
- `implementation`
- `implementation-review`
- `pr-spec-patch`
- `pr-review`

## Change Recipes

### 스펙 철학을 바꿀 때

1. `SDD_SPEC_REQUIREMENTS.md`에서 기준 문구를 먼저 바꾼다.
2. `.codex/skills/spec-create/`와 `.claude/skills/spec-create/` 템플릿/예시를 먼저 맞춘다.
3. `spec-rewrite`, `spec-summary`, `spec-review`, `spec-update-*`를 양 플랫폼에서 같은 기준으로 정렬한다.
4. 그 다음 `feature-draft`, `implementation*`, `pr*`가 이 앵커와 분류를 어떻게 읽는지 확인한다.

### 상위 앵커를 바꿀 때

1. `spec-create`와 템플릿을 먼저 수정한다.
2. `.codex/skills/`와 `.claude/skills/`의 `spec-summary`, `spec-review`, `spec-rewrite`가 새 앵커를 이해하는지 점검한다.
3. `feature-draft`, `implementation*`, `pr*`의 target section 매핑을 함께 바꾼다.

### `MUST update / CONSIDER / NO update` 정책을 바꿀 때

1. `spec-update-todo`, `spec-update-done`를 먼저 바꾼다.
2. `.codex/skills/`와 `.claude/skills/`의 `feature-draft`, `implementation`, `implementation-review`, `pr-spec-patch`, `pr-review`가 같은 분류를 쓰는지 확인한다.

## Tests / Observability

- `git diff --check`로 문서 위생 확인
- `rg "MUST update|NO update|CONSIDER" .codex/skills .claude/skills`로 분류 용어 사용 범위 확인
- `rg "Goal|Architecture Overview|Component Details|Open Questions" .codex/skills/spec-* .claude/skills/spec-*`로 앵커 정렬 확인
- 예시/참조 문서가 `SKILL.md`와 같은 철학을 가르치는지 직접 읽어 점검

## Risks / Invariants

- 상위 앵커는 하위/인접 스킬이 의존하므로 갑자기 깨면 안 된다.
- 메인 스펙은 항상 navigation-first, token-efficient 해야 한다.
- review-only 스킬은 실제 스펙 파일을 직접 수정하면 안 된다.
- `NO update` 케이스에서 불필요한 문서 편집을 강제하지 않아야 한다.
- 동일 이름의 Codex/Claude 스킬이 존재하면, 한쪽만 바꾸고 다른 쪽을 잊어버리는 드리프트가 자주 생긴다.
