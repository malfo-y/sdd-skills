# Pipeline Report: Global Definition and Skill Diet

**Completed**: 2026-04-04T03:42:53+0900
**Orchestrator**: `_sdd/pipeline/orchestrators/orchestrator_global_definition_skill_diet.md`
**Log**: `_sdd/pipeline/log_global_definition_skill_diet_20260404_031927.md`

## 1. What Was Done

- `docs/`와 `docs/en/` definition 문서군을 thin global spec model 기준으로 재작성했다.
- Codex consumer/generator/update/orchestrator surface를 새 global minimum에 맞게 재정렬했다.
- Claude skills와 Claude agents를 같은 계약으로 동기화했다.
- review-fix loop와 inline verification 결과를 implementation artifact로 저장했다.

주요 산출물:

- `_sdd/implementation/implementation_plan_global_definition_skill_diet.md`
- `_sdd/implementation/implementation_review_global_definition_skill_diet.md`
- `_sdd/implementation/implementation_review_global_definition_skill_diet_rerun.md`
- `_sdd/implementation/test_results/test_results_global_definition_skill_diet.md`

## 2. Outcome

- global mandatory core는 `배경/개념`, `scope/non-goals/guardrails`, `핵심 결정` 중심으로 고정됐다.
- consumer 3종은 old global section 부재를 defect처럼 보지 않도록 바뀌었다.
- generator/update/orchestrator 계열은 feature-level execution detail을 global spec 기본 본문으로 복구하지 않게 정리됐다.
- Claude mirror는 대부분 동일하게 맞춰졌고, 일부 diff는 `.claude` 경로와 Claude-specific mirror wording 때문에 의도적으로 남겼다.
- 검증은 모두 통과했다: whitespace/patched diff 문제 없음, targeted negative grep 0건, thin-global positive grep 64건.

## 3. Remaining Work

- 치명적 후속 작업은 없다.
- `before-upgrade` examples는 legacy 상태를 보여주는 negative example이라 old section label을 의도적으로 유지했다.
- 이후 추가 개편이 생기면 Codex/Claude mirror parity를 다시 spot-check하는 것이 좋다.

## Taste Decisions

- global spec을 “얇은 decision memo”로 정의하고, feature-level usage/validation/reference는 companion surface로 내렸다.
- guide는 authoritative layer가 아니라 on-demand companion으로 유지했다.
- review에서 zero critical/high/medium이면 no-op fix를 허용했다.

## Status Check

- orchestrator 상태: completed
- review-fix loop: completed
- inline verification: completed
