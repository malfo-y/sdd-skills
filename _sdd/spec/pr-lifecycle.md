# PR Lifecycle Skills

## Responsibility

- 이 그룹은 PR 변화가 현재 spec에 어떤 영향을 주는지 정리하고, 그 구현이 spec과 맞는지 검증하는 역할을 담당한다.
- `pr-spec-patch`는 patch draft를 만들고, `pr-review`는 acceptance criteria / blocker / post-merge spec sync를 판정한다.
- 이 그룹은 patch draft와 review report를 만들지만, canonical spec 자체를 수정하지는 않는다.

## Owned Paths

- `.codex/skills/pr-spec-patch/`
- `.claude/skills/pr-spec-patch/`
- `.codex/skills/pr-review/`
- `.claude/skills/pr-review/`
- `_sdd/pr/`

## Key Symbols / Entry Points

- `.codex/skills/pr-spec-patch/SKILL.md`
- `.claude/skills/pr-spec-patch/SKILL.md`
- `.codex/skills/pr-spec-patch/references/gh-commands.md`
- `.claude/skills/pr-spec-patch/references/gh-commands.md`
- `.codex/skills/pr-spec-patch/examples/spec_patch_draft.md`
- `.claude/skills/pr-spec-patch/examples/spec_patch_draft.md`
- `.codex/skills/pr-review/SKILL.md`
- `.claude/skills/pr-review/SKILL.md`
- `.codex/skills/pr-review/references/review-checklist.md`
- `.claude/skills/pr-review/references/review-checklist.md`
- `.codex/skills/pr-review/examples/sample-review.md`
- `.claude/skills/pr-review/examples/sample-review.md`

## Interfaces / Contracts

### Expected Outputs

- patch draft: `_sdd/pr/spec_patch_draft.md`
- review report: `_sdd/pr/PR_REVIEW.md`

### Shared Review Contracts

- spec impact는 `Repository Map`, `Runtime Map`, `Component Index`, `Common Change Paths`, `Open Questions` 관점으로 본다.
- spec update 필요성은 `MUST update`, `CONSIDER`, `NO update`로 분류한다.
- PR 리뷰는 merge blocker와 post-merge spec sync를 분리해서 보여준다.

## Dependencies

### Upstream

- 현재 `_sdd/spec/` 문서
- `feature-draft` 또는 기존 patch draft
- GitHub PR 메타데이터와 diff

### Downstream

- `spec-update-todo`
- `spec-update-done`

## Change Recipes

### patch draft 포맷을 바꿀 때

1. `pr-spec-patch/examples/spec_patch_draft.md`를 먼저 수정한다.
2. `.codex/skills/`와 `.claude/skills/`의 `pr-spec-patch`가 같은 초안 구조를 읽고 쓰는지 확인한다.
3. `pr-review`가 그 초안을 어떻게 읽는지 확인한다.
4. 필요하면 `spec-update-todo` 입력 포맷과도 맞춘다.

### merge blocker 기준을 바꿀 때

1. `.codex/skills/pr-review/SKILL.md`, `.claude/skills/pr-review/SKILL.md`
2. `.codex/skills/pr-review/references/review-checklist.md`, `.claude/skills/pr-review/references/review-checklist.md`
3. `.codex/skills/pr-review/examples/sample-review.md`, `.claude/skills/pr-review/examples/sample-review.md`

이 세 파일은 두 플랫폼에서 함께 수정하는 것이 기본이다.

### spec update classification을 바꿀 때

1. `pr-spec-patch`
2. `pr-review`
3. `spec-update-*`

이 순서로 `.codex/skills/`와 `.claude/skills/`를 함께 정렬한다.

## Tests / Observability

- `gh auth status`가 가능한 환경인지 확인
- `rg "MUST update|NO update|CONSIDER|Merge Blockers|Post-Merge Spec Sync" .codex/skills/pr-* .claude/skills/pr-*`
- example report와 draft가 실제 SKILL 규칙을 따르는지 검토

## Risks / Invariants

- patch draft가 `spec-update-todo`와 완전히 다른 구조로 가면 후속 병합 작업이 불안정해진다.
- `pr-review`는 blocker와 spec sync를 섞으면 안 된다.
- `NO update` PR에도 억지로 문서 변경을 만들지 않아야 한다.
- `gh`가 없을 때는 degraded mode를 명시해야 한다.
- Codex와 Claude의 PR 스킬 문구가 어긋나면 같은 PR을 두 플랫폼에서 다르게 해석할 수 있다.
