# Implementation Review: Autopilot Planning Orchestration + Phase-Gated Review-Fix

**Review Date**: 2026-04-10
**Review Mode**: Tier 1
**Reference**: `_sdd/drafts/2026-04-10_feature_draft_autopilot_planning_phase_gates.md`
**Model**: GPT-5 Codex

## 1. Findings
### Critical
- 없음.

### High
- 없음.

### Medium
- `.claude/skills/implementation-plan/SKILL.md`와 `.claude/agents/implementation-plan.md`가 아직 실제 mirror pair가 아닙니다. 스킬 파일은 "복사본"이라고 명시하지만, clarification 질문 허용, lowercase canonical 출력 경로 규칙, `user_input.md` 후처리, 상세 process/template, mirror notice를 유지하는 반면, agent 파일은 이 규칙들을 생략하거나 "멈추지 않고 deterministic defaults로 진행"으로 바꾸고 있습니다. 그 결과 Claude에서 직접 `$implementation-plan`을 호출할 때의 계약과 autopilot이 내부적으로 소비하는 `implementation-plan` agent 계약이 달라집니다. 이번 변경의 T2/V4가 요구한 producer contract parity를 완전히 닫지 못했습니다. Evidence: `.claude/skills/implementation-plan/SKILL.md:31`, `:36`, `:51`, `:79`, `:278` vs `.claude/agents/implementation-plan.md:24`, `:25`, `:44`, `:62`, `:174`.

### Low
- 메인 가이드의 핵심 narrative는 교정되었지만, quick dry-run 예시와 related skills 표는 여전히 `/implementation-plan`을 standalone 시작점처럼 읽힐 수 있게 남겨 두고 있습니다. 앞선 섹션에서 "후속 확장 단계"라고 설명한 취지를 완전히 상쇄하지는 않지만, 사용자가 8.6B나 9절만 바로 읽을 경우 예전 peer-choice mental model을 다시 떠올릴 여지가 있습니다. Evidence: `docs/AUTOPILOT_GUIDE.md:539`, `:566`, `docs/en/AUTOPILOT_GUIDE.md:539`, `:566`.

## 2. Progress Overview
- Tier 1로 판단했습니다. 사용자가 지정한 `_sdd/drafts/2026-04-10_feature_draft_autopilot_planning_phase_gates.md` 안에 temporary spec과 implementation plan이 모두 포함되어 있고, 현재 worktree의 수정 파일 14개가 draft의 target file 집합과 직접 대응합니다.
- T1은 `MET`입니다. `.codex/skills/sdd-autopilot/SKILL.md`, `.claude/skills/sdd-autopilot/SKILL.md`, 양쪽 reasoning reference와 orchestrator contract에서 `feature-draft` 선행 원칙, multi-phase 시 `per-phase` gate, `final integration review` semantics가 확인됐습니다.
- T2는 `PARTIAL`입니다. phase metadata와 consumer contract 필드는 Codex/Claude surface에 모두 추가됐지만, Claude `implementation-plan` skill/agent pair는 서로 다른 문서를 유지하고 있어 producer contract parity가 완전히 닫히지 않았습니다.
- T3는 `MET`입니다. Claude/Codex sample orchestrator 모두 single-phase medium direct path와 multi-phase expanded path를 포함하며, multi-phase example에 `phase boundary source`, `carry-over policy`, `final integration review`가 드러납니다.
- T4는 `PARTIAL`입니다. ko/en guide의 규모별 파이프라인, phase gate, final integration review 설명은 정렬됐지만, quick dry-run/related skills 섹션의 standalone `implementation-plan` 예시는 보강이 필요합니다.
- `_sdd/spec/` 아래 파일은 이번 변경 집합에 포함되지 않아 out-of-scope guardrail은 지켜졌습니다.

## 3. Verification Summary
- Fresh verification은 현재 worktree 기준으로 다시 실행했습니다. 사용한 근거는 `git status --short`, `git diff --check -- .codex .claude docs`, target surface 대상 `rg`, 그리고 관련 파일 직접 열람/상호 diff입니다.
- `git diff --check -- .codex .claude docs`는 `PASS`였습니다. 이번 feature의 타깃 변경 파일들에는 whitespace/payload hygiene 이슈가 없습니다.
- repo 전체 `git diff --check`는 `FAIL`이었지만 원인은 이번 feature 범위 밖의 `_COMMENTS.md` trailing whitespace였습니다. 이번 리뷰에서는 범위 외 변경으로 분리했습니다.
- 구현 상태 마커:

| Area | Implementation | Criteria | Notes |
|------|----------------|----------|-------|
| T1 Autopilot core + reasoning | EXISTS | MET | planning precedence와 per-phase/final integration semantics 반영 |
| T2 Contract + implementation-plan producer | PARTIAL | NOT MET | Claude skill/agent mirror drift 잔존 |
| T3 Sample orchestrators | EXISTS | MET | medium direct path + multi-phase path 모두 존재 |
| T4 Guides | EXISTS | PARTIAL | 핵심 guide 본문은 정렬됐으나 command-reference caveat 보강 필요 |

- Runtime validation은 `UNTESTED`입니다. `_sdd/env.md:49`-`:50` 기준 이 저장소의 실질 검증은 슬래시 커맨드 실제 호출인데, 이번 리뷰에서는 `/implementation-plan` 또는 `/sdd-autopilot` dry-run을 실행하지 않았습니다. 따라서 wrapper/runtime 레벨의 실제 동작은 정적 문서 검증까지만 확인됐습니다.

## 4. Recommendations
- Must: `.claude/skills/implementation-plan/SKILL.md`와 `.claude/agents/implementation-plan.md`를 단일 contract source 수준으로 다시 동기화하고, mirror notice가 사실이 되도록 맞추세요. 수정 후에는 V3/V4 parity review를 다시 돌리는 편이 안전합니다.
- Should: `docs/AUTOPILOT_GUIDE.md`와 `docs/en/AUTOPILOT_GUIDE.md`의 8.6B, 9절에 `/implementation-plan`이 기본 planning entry가 아니라 `feature-draft` 이후 확장/예외 경로라는 caveat를 한 줄로라도 명시하세요.
- Could: `/implementation-plan` 단독 호출 1회, multi-phase `/sdd-autopilot` dry-run 1회를 실제로 수행해 `_sdd/pipeline/log_*.md` evidence를 남기면 UNTESTED 상태를 닫을 수 있습니다.

## 5. Conclusion
핵심 변경 의도인 `feature-draft` 중심 planning precedence, multi-phase의 `per-phase review-fix`, `final integration review` semantics는 전반적으로 구현됐습니다. 다만 Claude `implementation-plan` public skill과 internal agent가 아직 같은 producer contract로 수렴하지 않았고, runtime dry-run evidence도 없어서 현재 평가는 "대부분 구현됨, 그러나 clean pass는 아님"이 적절합니다.
