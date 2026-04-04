# Discussion Summary: Codex Consumer Read Contracts

**Date**: 2026-04-04
**Rounds**: 3
**Topic**: 더 얇아진 global spec definition을 기준으로 Codex consumer 3종(`spec-review`, `spec-summary`, `spec-rewrite`)의 read contract를 어떻게 고정할지
**Language**: Korean

## 핵심 논점

1. `spec-review`가 새 global minimum에서 무엇을 필수로 보고, 무엇이 빠져 있어도 정상으로 볼지
2. `spec-summary`가 새 global minimum을 어떤 shape로 요약해야 하는지
3. `spec-rewrite`가 global spec을 “too heavy”로 판정할 때 길이보다 무엇을 더 중요하게 봐야 하는지

## 결정 사항

1. **`spec-review`는 global spec에서 최소 코어만 요구한다.**
   - 필수로 보는 것:
     - 배경 및 high-level concept
     - scope / non-goals / guardrails
     - 핵심 설계와 주요 결정
   - 기본적으로 defect로 보지 않는 것:
     - `사용 가이드 & 기대 결과`
     - `참조 정보`
     - `Strategic Code Map`
     - 현재 형태의 `Contract / Invariants / Verifiability`

2. **`spec-summary`의 global summary shape는 `개념 + 경계 + 결정` 중심으로 간다.**
   - Executive Summary
   - Problem / High-Level Concept
   - Scope / Non-goals Snapshot
   - Key Decisions / Guardrails
   - delegated-out information에 대한 짧은 note
   - usage/CIV snapshot은 기본 shape에서 뺀다.

3. **`spec-rewrite`의 “too heavy” 판정은 길이보다 오염도를 우선한다.**
   - global 본문이 feature-level usage, expected result, contract, reference, inventory로 오염되어
   - 최소 코어(개념, 경계, 결정)가 흐려졌다면 rewrite 후보로 본다.
   - line 수나 token 수는 보조 signal일 뿐, 핵심 기준이 아니다.

## 결정의 의미

- 새 definition 아래에서 global spec은 더 이상 “많이 들어 있는 문서”가 아니라 “무엇을 의도적으로 안 담는지까지 포함한 얇은 기준 문서”가 된다.
- consumer skill도 이 전제를 공유해야만 generator/transformer나 planner/update 계열과 drift가 나지 않는다.
- 특히 `spec-review`가 old canonical 섹션 부재를 defect로 계속 잡으면 새 definition rollout이 불가능해진다.

## open questions

- 현재 범위에서는 없음.
- planner/update/orchestrator 계열이 feature-level usage/CIV를 temporary spec만으로 처리할지, 필요 시 guide 생성까지 계약에 넣을지는 다음 단계 action item으로 넘긴다.

## action items

1. `.codex/skills/spec-review/SKILL.md`의 global review dimension과 spec-type 판별 규칙을 새 global minimum에 맞게 수정한다.
2. `.codex/skills/spec-summary/SKILL.md`의 global summary shape와 AC를 새 기준에 맞게 수정한다.
3. `.codex/skills/spec-rewrite/SKILL.md`의 canonical-fit / metric 기준을 “오염도 중심”으로 재정의한다.
4. 이후 consumer 변경을 기준으로 `docs/SDD_SPEC_DEFINITION.md`와 generator/planner/update 계열 스킬의 wording을 맞춘다.

## 리서치 결과 요약

- [spec-review](/Users/hyunjoonlee/github/sdd_skills/.codex/skills/spec-review/SKILL.md)는 아직 global spec에 `Contract / Invariants / Verifiability`, `Decision-bearing structure`, `Strategic Code Map`을 기본 요구사항처럼 두고 있다.
- [spec-summary](/Users/hyunjoonlee/github/sdd_skills/.codex/skills/spec-summary/SKILL.md)는 global summary를 `concept / scope / CIV / decision-bearing structure / usage` 중심으로 가정하고 있다.
- [spec-rewrite](/Users/hyunjoonlee/github/sdd_skills/.codex/skills/spec-rewrite/SKILL.md)는 현재도 thin global spec 방향을 설명하지만, `Canonical Fit`에서 global spec의 `CIV`, `decision-bearing structure`, `usage`를 여전히 함께 요구한다.
- 이 세 skill의 read contract를 먼저 고정해야 새 definition을 기준으로 나머지 Codex skill을 재정렬할 수 있다.

## sources

- `.codex/skills/spec-review/SKILL.md`
- `.codex/skills/spec-summary/SKILL.md`
- `.codex/skills/spec-rewrite/SKILL.md`
- `_sdd/discussion/discussion_global_definition_and_codex_skill_diet.md`
- `.codex/skills/discussion/references/discussion-question-guide.md`

## 토론 흐름

### Round 1
- 질문: `spec-review`의 global-spec read contract를 어떻게 고정할지
- 응답: 최소 코어만 요구

### Round 2
- 질문: `spec-summary`의 global summary shape를 무엇으로 잡을지
- 응답: 개념+경계+결정 요약

### Round 3
- 질문: `spec-rewrite`의 “too heavy” 판정을 무엇을 기준으로 할지
- 응답: 오염도 중심

## 결론

> 새 global minimum 아래에서 Codex consumer 3종은 “global spec에 무엇이 있어야 하는가”보다 “global spec에 무엇이 없어도 정상인가”를 먼저 바꿔야 한다. `spec-review`는 최소 코어만 요구하고, `spec-summary`는 개념/경계/결정 중심으로 요약하며, `spec-rewrite`는 길이보다 feature-level 오염도를 기준으로 global을 얇게 만든다.
