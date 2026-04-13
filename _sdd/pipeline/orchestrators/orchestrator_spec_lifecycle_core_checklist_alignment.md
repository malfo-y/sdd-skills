# Orchestrator: spec lifecycle 공통 코어 체크리스트 정렬

**생성일**: 2026-04-13T20:08:53+0900
**규모**: 중규모
**생성자**: sdd-autopilot

## 기능 설명

기존 feature draft [2026-04-13_feature_draft_spec_lifecycle_core_checklist_alignment.md](../../drafts/2026-04-13_feature_draft_spec_lifecycle_core_checklist_alignment.md)를 기준으로 `spec-create`, `spec-review`, `spec-rewrite`, `spec-upgrade` 네 개 스킬과 관련 규범 문서를 정렬한다.

핵심 방향은 다음과 같다.

- 공통 코어 checklist 4축은 `docs/SDD_SPEC_DEFINITION.md`와 영문 mirror에 source-of-truth로 둔다.
- 각 스킬은 별도 shared block 없이 AC/Final Check에 공통 코어를 흡수한다.
- `spec-review`는 rubric separation + evidence strictness를 강화한다.
- `spec-create`는 structure rationale + `single-file default`를 고정한다.
- `spec-rewrite`는 rationale preservation과 body/log placement를 강화한다.
- `spec-upgrade`는 rewrite boundary judgment를 명시한다.
- `_sdd/spec/` supporting surface와 history surface 변경은 `spec_update_done`만 수행한다.

## Acceptance Criteria

- [ ] `docs/SDD_SPEC_DEFINITION.md`와 `docs/en/SDD_SPEC_DEFINITION.md`에 공통 코어 4축과 AC/Final Check 매핑 규칙이 반영된다.
- [ ] `spec-review` public skill, Claude agent, Codex agent, metadata가 같은 rubric separation + evidence strictness semantics를 가진다.
- [ ] `spec-create`, `spec-rewrite`, `spec-upgrade` mirror `SKILL.md`와 `skill.json`이 각자의 1차 추가 축을 반영한다.
- [ ] `spec-create` example, `spec-rewrite` checklist, `spec-upgrade` mapping reference가 새 semantics와 정렬된다.
- [ ] `_sdd/spec/components.md`, `_sdd/spec/usage-guide.md`, `_sdd/spec/DECISION_LOG.md`, `_sdd/spec/logs/changelog.md`가 구현 결과와 정렬된다.
- [ ] inline verification이 실제 실행되어 결과가 `_sdd/implementation/test_results/test_results_spec_lifecycle_core_checklist_alignment.md`에 저장된다.

## Reasoning Trace

- 기존 feature draft가 이미 있으므로 planning entry인 `feature-draft`는 재실행하지 않고 existing artifact를 canonical input으로 사용한다.
- 구현 범위는 문서/skill contract refactor 중심이고 single-pass dependency가 명확하므로 `implementation-plan`은 생략한다.
- `_sdd/spec/` 직접 수정은 autopilot hard rule에 따라 `spec_update_done`에만 위임하고, implementation 단계에서는 `.codex`, `.claude`, `docs/`와 reference/example 자산만 다룬다.
- 변경 범위가 여러 스킬에 걸치지만 phase gate가 필요한 수준의 코드 리스크는 아니므로 `Review-Fix Loop.scope = global`을 사용한다.
- 테스트는 전통적 프레임워크가 없는 저장소 특성상 `git diff --check`와 targeted `rg` 기반 inline verification을 선택하고, 결과는 별도 test results 문서에 저장한다.

## Pipeline Steps

### Step 1: implementation
**Codex agent_type**: `implementation`
**입력 파일**:
- `_sdd/drafts/2026-04-13_feature_draft_spec_lifecycle_core_checklist_alignment.md`
- `docs/SDD_SPEC_DEFINITION.md`
- `docs/en/SDD_SPEC_DEFINITION.md`
- `docs/SDD_WORKFLOW.md`
- `docs/en/SDD_WORKFLOW.md`
- `.codex/skills/spec-review/SKILL.md`
- `.claude/skills/spec-review/SKILL.md`
- `.claude/agents/spec-review.md`
- `.codex/agents/spec-review.toml`
- `.codex/skills/spec-create/SKILL.md`
- `.claude/skills/spec-create/SKILL.md`
- `.codex/skills/spec-rewrite/SKILL.md`
- `.claude/skills/spec-rewrite/SKILL.md`
- `.codex/skills/spec-upgrade/SKILL.md`
- `.claude/skills/spec-upgrade/SKILL.md`
- `.codex/skills/spec-create/examples/additional-specs.md`
- `.claude/skills/spec-create/examples/additional-specs.md`
- `.codex/skills/spec-rewrite/references/rewrite-checklist.md`
- `.claude/skills/spec-rewrite/references/rewrite-checklist.md`
- `.codex/skills/spec-upgrade/references/upgrade-mapping.md`
- `.claude/skills/spec-upgrade/references/upgrade-mapping.md`
- `.codex/skills/spec-create/skill.json`
- `.claude/skills/spec-create/skill.json`
- `.codex/skills/spec-review/skill.json`
- `.claude/skills/spec-review/skill.json`
- `.codex/skills/spec-rewrite/skill.json`
- `.claude/skills/spec-rewrite/skill.json`
- `.codex/skills/spec-upgrade/skill.json`
- `.claude/skills/spec-upgrade/skill.json`
**출력 파일**:
- `docs/SDD_SPEC_DEFINITION.md`
- `docs/en/SDD_SPEC_DEFINITION.md`
- `docs/SDD_WORKFLOW.md`
- `docs/en/SDD_WORKFLOW.md`
- `.codex/skills/spec-review/SKILL.md`
- `.claude/skills/spec-review/SKILL.md`
- `.claude/agents/spec-review.md`
- `.codex/agents/spec-review.toml`
- `.codex/skills/spec-create/SKILL.md`
- `.claude/skills/spec-create/SKILL.md`
- `.codex/skills/spec-rewrite/SKILL.md`
- `.claude/skills/spec-rewrite/SKILL.md`
- `.codex/skills/spec-upgrade/SKILL.md`
- `.claude/skills/spec-upgrade/SKILL.md`
- `.codex/skills/spec-create/examples/additional-specs.md`
- `.claude/skills/spec-create/examples/additional-specs.md`
- `.codex/skills/spec-rewrite/references/rewrite-checklist.md`
- `.claude/skills/spec-rewrite/references/rewrite-checklist.md`
- `.codex/skills/spec-upgrade/references/upgrade-mapping.md`
- `.claude/skills/spec-upgrade/references/upgrade-mapping.md`
- `.codex/skills/spec-create/skill.json`
- `.claude/skills/spec-create/skill.json`
- `.codex/skills/spec-review/skill.json`
- `.claude/skills/spec-review/skill.json`
- `.codex/skills/spec-rewrite/skill.json`
- `.claude/skills/spec-rewrite/skill.json`
- `.codex/skills/spec-upgrade/skill.json`
- `.claude/skills/spec-upgrade/skill.json`

**프롬프트**:
기존 feature draft `_sdd/drafts/2026-04-13_feature_draft_spec_lifecycle_core_checklist_alignment.md`를 authoritative input으로 사용해 구현을 진행하세요.

필수 요구사항:
- `docs/SDD_SPEC_DEFINITION.md`와 영문 mirror에 공통 코어 4축과 AC/Final Check 반영 매핑 규칙을 추가하세요.
- `docs/SDD_WORKFLOW.md`와 영문 mirror에 `spec-review`, `spec-create`, `spec-rewrite`, `spec-upgrade`의 역할 차이를 새 semantics로 정리하세요.
- `spec-review`는 rubric separation + evidence strictness를 반영하고, public skill / Claude agent / Codex agent / metadata parity를 맞추세요.
- `spec-create`는 structure rationale + `single-file default`를 반영하고 example을 보정하세요.
- `spec-rewrite`는 rationale preservation + body/log placement를 반영하고 rewrite checklist를 보정하세요.
- `spec-upgrade`는 rewrite boundary judgment를 반영하고 upgrade mapping reference를 보정하세요.
- `skill.json`은 mirror parity를 먼저 맞추고, semantic contract change를 반영하는 minor bump를 적용하세요.
- `_sdd/spec/` 아래 파일은 직접 수정하지 마세요. 그 범위는 `spec_update_done` 단계에 남기세요.

검증 관점:
- draft의 `C1~C5`, `I1~I4`, `V1~V7`에 맞춰 구현하세요.
- 리뷰에서 medium 이상 이슈가 남지 않도록 evidence와 wording consistency를 우선 보세요.

### Step 2: implementation_review
**Codex agent_type**: `implementation_review`
**입력 파일**:
- `_sdd/drafts/2026-04-13_feature_draft_spec_lifecycle_core_checklist_alignment.md`
- Step 1에서 수정된 파일 일체
**출력 파일**:
- `_sdd/implementation/2026-04-13_implementation_review_spec_lifecycle_core_checklist_alignment.md`

**프롬프트**:
Step 1 구현 결과를 기존 feature draft 기준으로 리뷰하세요.

리뷰 초점:
- 공통 코어 4축과 AC/Final Check 매핑 규칙이 정의 문서에 실제로 반영되었는가
- `spec-review`가 rubric separation + evidence strictness semantics를 가지는가
- `spec-create`, `spec-rewrite`, `spec-upgrade`의 1차 추가 축이 각 스킬/metadata/reference 자산에 일관되게 반영되었는가
- mirror drift, stale wording, version mismatch가 남아 있지 않은가

findings는 severity 순으로 작성하고, `critical/high/medium/low`를 명시하세요.

### Step 3: spec_update_done
**Codex agent_type**: `spec_update_done`
**입력 파일**:
- `_sdd/spec/main.md`
- `_sdd/drafts/2026-04-13_feature_draft_spec_lifecycle_core_checklist_alignment.md`
- `docs/SDD_SPEC_DEFINITION.md`
- `docs/SDD_WORKFLOW.md`
- `.codex/skills/spec-create/SKILL.md`
- `.codex/skills/spec-review/SKILL.md`
- `.codex/skills/spec-rewrite/SKILL.md`
- `.codex/skills/spec-upgrade/SKILL.md`
- `_sdd/implementation/2026-04-13_implementation_review_spec_lifecycle_core_checklist_alignment.md`
**출력 파일**:
- `_sdd/spec/components.md`
- `_sdd/spec/usage-guide.md`
- `_sdd/spec/DECISION_LOG.md`
- `_sdd/spec/logs/changelog.md`

**프롬프트**:
이번 구현 완료 기준으로 `_sdd/spec/` supporting surface와 history surface를 동기화하세요.

필수 요구사항:
- `_sdd/spec/components.md`에 `spec-create`, `spec-review`, `spec-rewrite`, `spec-upgrade`의 새 역할 차이를 반영하세요.
- `_sdd/spec/usage-guide.md`의 `/spec-create` expected result에서 old canonical wording(`CIV`, `usage`, `decision-bearing structure`)을 제거하고 thin global 기준으로 정정하세요.
- `_sdd/spec/DECISION_LOG.md`에는 공통 코어 checklist source-of-truth와 네 개 스킬 역할 정렬의 판단 근거를 남기세요.
- `_sdd/spec/logs/changelog.md`에는 변경 파일과 버전 변화를 짧게 기록하세요.
- temporary execution detail은 global spec 본문으로 올리지 말고, supporting/history surface 역할에 맞게만 반영하세요.

## Review-Fix Loop

- `scope`: `global`
- `max_rounds`: 3
- `exit_condition`: `critical = 0 AND high = 0 AND medium = 0`
- `fix_targets`: `critical/high/medium/low`
- `agent_mapping`: `review = implementation_review`, `fix = implementation`, `re-review = implementation_review`

## Test Strategy

- `mode`: `inline`
- `commands`:
  - `git diff --check`
  - `rg -n "Thinness|Decision-bearing truth|Anti-duplication|Navigation \\+ surface fit" docs/SDD_SPEC_DEFINITION.md docs/en/SDD_SPEC_DEFINITION.md`
  - `rg -n "rubric separation|evidence strictness|single-file default|rewrite boundary|decision_log|rewrite_report" .codex .claude docs -S`
  - `rg -n "CIV|decision-bearing structure" _sdd/spec/usage-guide.md`
- `selection_reason`: 저장소가 Markdown/skill contract 중심이고 전통적 테스트 프레임워크가 없으므로, formatting integrity + semantic grep + targeted stale wording 검증이 가장 직접적이다.
- `reporting`: 명령 실행 결과와 PASS/FAIL 판정을 `_sdd/implementation/test_results/test_results_spec_lifecycle_core_checklist_alignment.md` 및 최종 report에 기록한다.

## Error Handling

- `retry_policy`:
  - Step 1 구현 후 Step 2 리뷰에서 `critical/high/medium`이 나오면 최대 2회까지 implementation -> re-review를 반복한다.
- `critical_steps`:
  - Step 1 implementation
  - Step 2 implementation_review
  - Step 3 spec_update_done
  - inline verification
- `non_critical_steps`:
  - 없음
- `abort_conditions`:
  - review loop 종료 후 `critical` 또는 `high`가 남는 경우
  - inline verification에서 `git diff --check` 실패 또는 must-fix stale wording 잔존
- `degrade_conditions`:
  - 없음. 이번 범위에서는 `_sdd/spec/` supporting/history surface 동기화가 완료 조건에 포함되므로 `spec_update_done` 실패는 전체 실패로 취급한다.
