# Orchestrator: spec-summary canonical overview alignment

**생성일**: 2026-04-13T17:36:28+09:00
**규모**: 중규모
**생성자**: sdd-autopilot

## 기능 설명

기존 feature draft `_sdd/drafts/2026-04-13_feature_draft_spec_summary_canonical_overview_alignment.md`를 구현한다.

핵심 작업은 `spec-summary`를 `global overview + optional planned/progress snapshot` 구조로 재정렬하고, 관련 template/example, supporting docs, canonical docs, downstream references, `_sdd/spec/` supporting surface를 동기화하는 것이다.

사용자 추가 제약:

- `spec-summary` 본문과 example/template에는 "예전에는 이랬고 지금은 이렇게 바뀌었다" 식의 transitional wording을 남기지 않는다.
- 수정된 최종 계약과 결과 shape만 바로 드러나게 쓴다.

## Acceptance Criteria

- [ ] `spec-summary` skill contract가 `_sdd/spec/summary.md`를 사람용 canonical overview로 정의하고, temporary spec 독립 summary mode를 제거한다.
- [ ] `spec-summary`는 관련 `_sdd/drafts/` / `_sdd/implementation/` artifact가 있을 때만 계획/진행 상태를 짧은 optional snapshot으로 보조 표기한다.
- [ ] `.claude` / `.codex` `spec-summary` mirror, `skill.json`, template, example이 같은 의미와 `Where Details Live` naming을 공유한다.
- [ ] `_sdd/spec/components.md`, `_sdd/spec/usage-guide.md`, `docs/SDD_SPEC_DEFINITION.md`, `docs/SDD_WORKFLOW.md`, 영문 mirror, autopilot references가 새 semantics와 일치한다.
- [ ] `_sdd/spec/DECISION_LOG.md`와 `_sdd/spec/logs/changelog.md`가 이번 semantic shift를 역할 분리된 방식으로 기록한다.
- [ ] 수정된 `spec-summary` 관련 문서들은 과거 대비 설명이 아니라 최종 계약/출력만 직접 서술한다.

## Reasoning Trace

- 해당 주제의 feature draft가 이미 존재하므로 planning precedence 규칙상 `feature-draft`를 재실행하지 않고 기존 artifact를 입력으로 활용한다.
- 변경 범위는 문서/스킬 semantics refactor지만 관련 surface가 다수이고 `_sdd/spec/` supporting docs sync가 포함되므로 single-phase medium path로 판단했다.
- `_sdd/spec/` 직접 수정은 autopilot hard rule에 따라 `spec_update_done` 단계에 위임하고, 구현 단계는 skill/docs/reference 파일과 non-`_sdd/spec/` 문서 변경에 집중한다.
- 저장소 특성상 전통적 테스트 프레임워크는 없으므로 inline verification에서 `git diff --check`, targeted `rg`, 구조 검토, artifact 결과 검토를 사용한다.
- 사용자 제약상 최종 산출물은 transitional wording 없이 final contract만 보여야 하므로, review-fix loop에서 해당 문체를 명시적으로 검사한다.

## Pipeline Steps

### Step 1: implementation
**Codex agent_type**: `implementation`
**입력 파일**:
- `_sdd/drafts/2026-04-13_feature_draft_spec_summary_canonical_overview_alignment.md`
- `.codex/skills/spec-summary/SKILL.md`
- `.claude/skills/spec-summary/SKILL.md`
- `.codex/skills/spec-summary/skill.json`
- `.claude/skills/spec-summary/skill.json`
- `.codex/skills/spec-summary/references/summary-template.md`
- `.claude/skills/spec-summary/references/summary-template.md`
- `.codex/skills/spec-summary/examples/summary-output.md`
- `.claude/skills/spec-summary/examples/summary-output.md`
- `docs/SDD_SPEC_DEFINITION.md`
- `docs/SDD_WORKFLOW.md`
- `docs/en/SDD_SPEC_DEFINITION.md`
- `docs/en/SDD_WORKFLOW.md`
- `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md`
- `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md`

**출력 파일**:
- `.codex/skills/spec-summary/SKILL.md`
- `.claude/skills/spec-summary/SKILL.md`
- `.codex/skills/spec-summary/skill.json`
- `.claude/skills/spec-summary/skill.json`
- `.codex/skills/spec-summary/references/summary-template.md`
- `.claude/skills/spec-summary/references/summary-template.md`
- `.codex/skills/spec-summary/examples/summary-output.md`
- `.claude/skills/spec-summary/examples/summary-output.md`
- `docs/SDD_SPEC_DEFINITION.md`
- `docs/SDD_WORKFLOW.md`
- `docs/en/SDD_SPEC_DEFINITION.md`
- `docs/en/SDD_WORKFLOW.md`
- `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md`
- `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md`

**프롬프트**:
feature draft를 기준으로 `spec-summary`를 구현하세요.

핵심 계약:
- `spec-summary`는 `_sdd/spec/summary.md`를 위한 canonical human overview를 만든다.
- temporary spec 독립 summary mode는 제거한다.
- 관련 `_sdd/drafts/` / `_sdd/implementation/` artifact가 있을 때만 계획/진행 상태를 짧은 optional snapshot으로 덧붙인다.
- navigation 섹션명은 `Where Details Live`를 사용한다.
- `.claude` / `.codex` mirror와 `skill.json`은 같은 커밋에서 함께 갱신하고 버전은 `2.0.0`으로 맞춘다.

문체 제약:
- `spec-summary` 본문, template, example에는 "예전에는 / 이제는 / 변경되었다" 같은 migration narration을 남기지 않는다.
- 최종 상태의 계약과 output shape만 직접적으로 서술한다.

### Step 2: spec_update_done
**Codex agent_type**: `spec_update_done`
**입력 파일**:
- `_sdd/drafts/2026-04-13_feature_draft_spec_summary_canonical_overview_alignment.md`
- `_sdd/spec/components.md`
- `_sdd/spec/usage-guide.md`
- `_sdd/spec/DECISION_LOG.md`
- `_sdd/spec/logs/changelog.md`
- `.codex/skills/spec-summary/SKILL.md`
- `.claude/skills/spec-summary/SKILL.md`
- `.codex/skills/spec-summary/skill.json`
- `.claude/skills/spec-summary/skill.json`
- `.codex/skills/spec-summary/references/summary-template.md`
- `.claude/skills/spec-summary/references/summary-template.md`
- `.codex/skills/spec-summary/examples/summary-output.md`
- `.claude/skills/spec-summary/examples/summary-output.md`
- `docs/SDD_SPEC_DEFINITION.md`
- `docs/SDD_WORKFLOW.md`
- `docs/en/SDD_SPEC_DEFINITION.md`
- `docs/en/SDD_WORKFLOW.md`
- `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md`
- `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md`

**출력 파일**:
- `_sdd/spec/components.md`
- `_sdd/spec/usage-guide.md`
- `_sdd/spec/DECISION_LOG.md`
- `_sdd/spec/logs/changelog.md`

**프롬프트**:
구현 결과를 기준으로 `_sdd/spec/` supporting surface를 동기화하세요.

반영 원칙:
- `components.md`와 `usage-guide.md`는 `spec-summary = canonical overview`, `guide = deep explanation`, `planned/progress snapshot = optional helper note` 의미를 final form으로 서술한다.
- `DECISION_LOG.md`는 왜 이 semantic shift를 선택했는지 판단 근거를 남긴다.
- `logs/changelog.md`는 어떤 파일과 버전이 바뀌었는지 짧게 남긴다.
- `_sdd/spec/main.md`는 수정하지 않는다.
- `_sdd/spec/` 문서에도 "예전에는 / 이제는" 식의 transitional wording은 넣지 않는다. 최종 상태 기준으로만 서술한다.

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
  - `rg -n "temporary spec|temporary summary|global/temporary spec 요약|현재 프로젝트 상태 요약|현재 스펙 상태|기능 대시보드" ...`
  - `rg -n "Where Details Live|2\\.0\\.0|canonical human overview|planned/progress" ...`
  - targeted manual read of changed files
- `선택 근거`:
  - 이 저장소는 전통적 테스트 프레임워크가 없고 문서/스킬 semantics 리팩터링이므로, diff/grep/review evidence가 가장 직접적인 검증 수단이다.
- `reporting`:
  - 검증 명령 결과와 수동 확인 항목을 `_sdd/implementation/test_results/test_results_spec_summary_canonical_overview_alignment.md`에 남기고, `_sdd/pipeline/report_spec_summary_canonical_overview_alignment_<timestamp>.md`에서 통과/실패를 요약한다.

## Error Handling

- `재시도 횟수`: review-fix 최대 3회, inline verification 명령 실패 시 원인 파악 후 1회 재실행
- `핵심 단계`: implementation, spec_update_done, review, re-review, inline verification
- `비핵심 단계`: changelog wording polish, reference 문구 미세 조정
