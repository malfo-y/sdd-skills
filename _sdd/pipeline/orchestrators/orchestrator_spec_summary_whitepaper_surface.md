# Orchestrator: spec-summary whitepaper surface

**생성일**: 2026-04-13
**규모**: 중규모
**생성자**: sdd-autopilot

## 기능 설명

`spec-summary`를 `_sdd/spec/summary.md`용 reader-facing whitepaper surface로 구현한다. 산출물은 문제와 배경/동기, 핵심 설계, 코드 근거, 사용 흐름과 기대 결과를 한 문서에서 설명해야 하며, 관련 계획/진행 상태는 optional appendix로만 다룬다. `.claude` / `.codex` mirror, template/example, repo docs, canonical docs, downstream reference, `_sdd/spec/` supporting docs가 같은 의미를 유지해야 한다.

## Acceptance Criteria

- [ ] `spec-summary` mirror `SKILL.md`와 `skill.json`이 whitepaper contract를 반영하고 version `3.0.0`으로 정렬된다.
- [ ] summary template/example이 `Executive Summary`, `Background / Motivation`, `Core Design`, `Code Grounding`, `Usage / Expected Results`, `Further Reading / References` 본문과 optional appendix 구조를 보여준다.
- [ ] `docs/SDD_SPEC_DEFINITION.md`, `docs/SDD_WORKFLOW.md`, `docs/en/*`, autopilot reference가 `spec-summary = reader-facing whitepaper surface` 의미로 정렬된다.
- [ ] `_sdd/spec/components.md`, `_sdd/spec/usage-guide.md`, `_sdd/spec/DECISION_LOG.md`, `_sdd/spec/logs/changelog.md`가 같은 계약을 반영한다.
- [ ] `spec-summary` surface 본문/템플릿/예시는 과거 비교나 migration narration 없이 현재 기준 내용만 직접 설명한다.
- [ ] inline verification이 실행되고 결과가 `_sdd/implementation/test_results/`와 최종 보고서에 기록된다.

## Reasoning Trace

- 관련 feature draft가 이미 있으므로 planning entry는 재생성하지 않고 해당 draft를 authoritative temporary spec으로 사용한다.
- 변경 범위는 문서/스킬 asset refactor이지만 target files와 validation linkage가 충분히 명시돼 있어 single-phase medium path로 처리 가능하다.
- `_sdd/spec/` 직접 수정은 autopilot hard rule에 따라 `spec_update_done`으로만 위임하고, 그 외 파일은 `implementation`이 담당한다.
- 테스트 프레임워크가 없는 문서 저장소이므로 `_sdd/env.md` 기준에 맞춰 inline verification(`git diff --check`, targeted grep, manual read`)을 사용한다.

## Pipeline Steps

### Step 1: implementation
**Codex agent_type**: `implementation`
**입력 파일**:
- `_sdd/drafts/2026-04-13_feature_draft_spec_summary_whitepaper_surface.md`
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
- `_sdd/implementation/2026-04-13_implementation_progress_spec_summary_whitepaper_surface.md`
- `_sdd/implementation/2026-04-13_implementation_report_spec_summary_whitepaper_surface.md`

**프롬프트**:
`2026-04-13_feature_draft_spec_summary_whitepaper_surface.md`의 Part 2를 실행하세요.
수정 범위는 Step 1 출력 파일로 제한합니다.
`spec-summary`를 `_sdd/spec/summary.md`용 reader-facing whitepaper surface로 구현하세요.
핵심 요구사항:
- `skill.json` version은 `.claude` / `.codex` 모두 `3.0.0`
- summary 본문/템플릿/예시는 `Executive Summary`, `Background / Motivation`, `Core Design`, `Code Grounding`, `Usage / Expected Results`, `Further Reading / References` + optional appendix 구조
- `Code Grounding`에는 concrete path 또는 source table expectation을 반영
- `planned/progress`는 appendix 또는 마지막 보조 섹션으로만 유지
- `spec-summary` surface 자체에는 과거 상태 비교나 “예전엔 이랬다”류 narration을 넣지 말고 현재 기준 내용만 직접 서술
- `_sdd/spec/` 아래 파일은 수정하지 말고, 필요 변경은 보고서에 남긴 뒤 Step 2가 처리하도록 둡니다
검증은 최소 `git diff --check`, targeted grep, 핵심 파일 manual read를 수행하고 결과를 implementation artifact에 남기세요.

### Step 2: spec_update_done
**Codex agent_type**: `spec_update_done`
**입력 파일**:
- `_sdd/drafts/2026-04-13_feature_draft_spec_summary_whitepaper_surface.md`
- `_sdd/implementation/2026-04-13_implementation_progress_spec_summary_whitepaper_surface.md`
- `_sdd/implementation/2026-04-13_implementation_report_spec_summary_whitepaper_surface.md`
- `_sdd/implementation/2026-04-13_implementation_review_spec_summary_whitepaper_surface.md`
- `_sdd/spec/components.md`
- `_sdd/spec/usage-guide.md`
- `_sdd/spec/DECISION_LOG.md`
- `_sdd/spec/logs/changelog.md`
**출력 파일**:
- `_sdd/spec/components.md`
- `_sdd/spec/usage-guide.md`
- `_sdd/spec/DECISION_LOG.md`
- `_sdd/spec/logs/changelog.md`

**프롬프트**:
feature draft와 구현/리뷰 evidence를 바탕으로 `_sdd/spec/` supporting docs를 동기화하세요.
대상 파일은 `components.md`, `usage-guide.md`, `DECISION_LOG.md`, `logs/changelog.md`로 제한합니다.
적용 원칙:
- `spec-summary`를 reader-facing whitepaper surface로 설명
- `/spec-summary` expected result는 whitepaper output 기준으로 기술
- `DECISION_LOG.md`는 운영 판단과 이유를 담되, summary surface 자체와 history surface의 역할 차이를 분명히 유지
- `logs/changelog.md`는 관련 파일과 contract version을 간단히 기록
- 구현되지 않았거나 검증되지 않은 내용은 완료된 사실처럼 쓰지 말고, final-state contract만 반영

## Review-Fix Loop

- `scope`: `global`
- `max_rounds`: 3
- `exit_condition`: `critical = 0 AND high = 0 AND medium = 0`
- `fix_targets`: `critical/high/medium/low`
- `agent_mapping`:
  - `review = implementation_review`
  - `fix = implementation`
  - `re-review = implementation_review`

## Test Strategy

- `mode`: `inline`
- `commands`:
  - `git diff --check`
  - `rg -n "canonical human overview|Global Spec Overview|Where Details Live" .codex/skills/spec-summary .claude/skills/spec-summary docs docs/en _sdd/spec/components.md _sdd/spec/usage-guide.md`
  - `rg -n "reader-facing whitepaper|Background / Motivation|Code Grounding|Usage / Expected Results|Further Reading / References" .codex/skills/spec-summary .claude/skills/spec-summary docs docs/en _sdd/spec/components.md _sdd/spec/usage-guide.md`
  - 핵심 파일 manual read (`.codex/.claude spec-summary`, template/example, `docs/SDD_*`, `_sdd/spec/components.md`, `_sdd/spec/usage-guide.md`, `_sdd/spec/DECISION_LOG.md`, `_sdd/spec/logs/changelog.md`)
- `선택 근거`: `_sdd/env.md` 기준으로 이 저장소는 문서/스킬 자산 저장소이며 전통적 테스트 프레임워크가 없다. 따라서 diff hygiene + targeted grep + manual read가 이 변경의 적절한 실행 검증이다.
- `reporting`: 검증 결과를 `_sdd/implementation/test_results/test_results_spec_summary_whitepaper_surface.md`와 `_sdd/pipeline/report_spec_summary_whitepaper_surface_<timestamp>.md`에 기록한다.

## Error Handling

- Step 1 실패: implementation artifact와 오류를 보존하고 같은 step을 최대 1회 재실행한다.
- Review에서 `critical/high/medium` 발견: 같은 feature draft를 입력으로 `implementation`을 재호출해 수정 후 `implementation_review`를 다시 수행한다.
- Step 2 실패: `_sdd/spec/` 대상 파일만 좁혀 재시도한다.
- Inline verification 실패: 실패 명령과 원인을 테스트 결과 문서와 파이프라인 로그에 기록하고, block severity에 따라 재수정 또는 중단한다.
