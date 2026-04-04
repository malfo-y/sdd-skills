# Orchestrator: Global Definition and Skill Diet

**생성일**: 2026-04-04T03:16:15+0900
**규모**: 대규모
**생성자**: autopilot

## 기능 설명

`_sdd/discussion/discussion_codex_consumer_read_contracts.md`와 관련 discussion 결론을 기준으로 `docs/` 문서군과 이 저장소의 Codex/Claude skill surface를 다시 정렬한다.

### 사용자 요청 원문

`$sdd-autopilot _sdd/discussion/discussion_codex_consumer_read_contracts.md 랑 지금까지 논의된 거로 docs/ 아래 문서들이랑 여기 있는 코덱스랑 클로드코드 스킬들 한 번 더 엎자.`

### 구체화된 요구사항

- `docs/SDD_SPEC_DEFINITION.md`를 더 얇은 global spec definition으로 재작성한다.
- `docs/SDD_CONCEPT.md`, `docs/SDD_WORKFLOW.md`, `docs/SDD_QUICK_START.md`, `docs/sdd.md`와 `docs/en/` mirror를 새 definition에 맞게 정렬한다.
- Codex consumer 3종(`spec-review`, `spec-summary`, `spec-rewrite`)의 read contract를 discussion 결론대로 고정한다.
- Codex generator/transformer/planner/update/orchestrator skill이 더 이상 global mandatory core에 feature-level usage, reference, current-form CIV, strategic code map을 기본 요구사항처럼 전제하지 않게 만든다.
- Claude skill mirror와 관련 Claude agent surface를 Codex 변경과 의미상 동기화한다.
- `_sdd/spec/` 본문은 이번 파이프라인의 수정 대상에서 제외한다.

### 제약 조건

- 기준 문서는 `_sdd/discussion/discussion_global_definition_and_codex_skill_diet.md`, `_sdd/discussion/discussion_codex_consumer_read_contracts.md`다.
- global spec 최소 코어는 `배경/개념`, `scope/non-goals/guardrails`, `핵심 결정` 중심으로 유지한다.
- repo-wide invariant가 필요하면 독립 CIV 표가 아니라 guardrail 또는 key decision wording으로 흡수한다.
- temporary spec, feature guide, supporting reference는 global mandatory core와 분리한다.
- `docs/`와 skill 문서 수정이 중심이며 `_sdd/spec/` 직접 수정은 하지 않는다.

## Acceptance Criteria

- [ ] `docs/SDD_SPEC_DEFINITION.md`와 `docs/en/SDD_SPEC_DEFINITION.md`가 global mandatory core를 `개념 + 경계 + 결정` 중심으로 정의하고, `사용 가이드 & 기대 결과`, `참조 정보`, `Strategic Code Map`, current-form `Contract / Invariants / Verifiability`를 global core 기본 요구사항에서 제외한다.
- [ ] `docs/SDD_CONCEPT.md`, `docs/SDD_WORKFLOW.md`, `docs/SDD_QUICK_START.md`, `docs/sdd.md`와 `docs/en/` mirror가 thin global spec 모델과 skill update ordering을 일관되게 설명한다.
- [ ] `.codex/skills/spec-review/SKILL.md`, `.codex/skills/spec-summary/SKILL.md`, `.codex/skills/spec-rewrite/SKILL.md`가 discussion에서 고정한 consumer read contract를 반영한다.
- [ ] `.codex/skills/spec-create/`, `.codex/skills/spec-upgrade/`, `.codex/skills/feature-draft/`, `.codex/skills/implementation-plan/`, `.codex/skills/spec-update-todo/`, `.codex/skills/spec-update-done/`, `.codex/skills/sdd-autopilot/` 및 관련 reference/example file이 thin global spec model을 전제로 다시 서술된다.
- [ ] `.claude/skills/`와 `.claude/agents/`의 관련 surface가 Codex 쪽 변경과 의미상 동기화되고, Claude-specific 문맥만 남긴다.
- [ ] 검증 결과가 `_sdd/implementation/test_results/`에 남고, `git diff --check`와 targeted `rg` sweep에서 이번 변경의 핵심 계약 위반이 발견되지 않는다.

## Reasoning Trace

- 이번 요청은 구현 기능 추가가 아니라 definition + skillchain read/write contract 재정렬이므로 `_sdd/spec/` sync보다 `docs/`와 skill surface overhaul가 본 작업이다.
- 영향 범위가 docs, docs/en, Codex skills, Claude skills, Claude agents까지 넓어서 대규모로 판단했다.
- consumer contract를 먼저 잠근 discussion이 이미 있으므로 `feature_draft` 대신 `implementation_plan`으로 대상군과 edit order를 고정하는 편이 효율적이다.
- `_sdd/spec/` 직접 수정이 필요하지 않으므로 `spec_update_*`는 이번 파이프라인에서 제외한다.
- 전통적 테스트 프레임워크는 없어서 inline verification을 선택하되, grep/diff 기반 검증을 실제 실행하고 결과 파일을 남긴다.

## Pipeline Steps

### Step 1: implementation_plan
**Codex agent_type**: `implementation_plan`
**입력 파일**:
- `_sdd/discussion/discussion_global_definition_and_codex_skill_diet.md`
- `_sdd/discussion/discussion_codex_consumer_read_contracts.md`
- `docs/SDD_SPEC_DEFINITION.md`
- `docs/SDD_CONCEPT.md`
- `docs/SDD_WORKFLOW.md`
- `docs/SDD_QUICK_START.md`
- `docs/sdd.md`
**출력 파일**: `_sdd/implementation/implementation_plan_global_definition_skill_diet.md`

**프롬프트**:
discussion 결론을 기준으로 `docs/`, `docs/en/`, `.codex/skills/`, `.claude/skills/`, `.claude/agents/` overhaul 계획을 작성하세요.
consumer -> definition/docs -> generator/transformer -> planner/update/orchestrator -> Claude mirror 순으로 Target Files를 나누고,
각 task가 thin global spec model을 어떻게 반영하는지 명시하세요.
`_sdd/spec/`는 수정 대상에서 제외하고, verification용 grep/diff 체크 항목도 계획에 포함하세요.

### Step 2: implementation
**Codex agent_type**: `implementation`
**입력 파일**:
- `_sdd/implementation/implementation_plan_global_definition_skill_diet.md`
- `_sdd/discussion/discussion_global_definition_and_codex_skill_diet.md`
- `_sdd/discussion/discussion_codex_consumer_read_contracts.md`
**출력 파일**:
- `docs/SDD_SPEC_DEFINITION.md`
- `docs/SDD_CONCEPT.md`
- `docs/SDD_WORKFLOW.md`
- `docs/SDD_QUICK_START.md`
- `docs/sdd.md`
- `docs/en/SDD_SPEC_DEFINITION.md`
- `docs/en/SDD_CONCEPT.md`
- `docs/en/SDD_WORKFLOW.md`
- `docs/en/SDD_QUICK_START.md`
- `docs/en/sdd.md`
- `.codex/skills/spec-review/SKILL.md`
- `.codex/skills/spec-summary/SKILL.md`
- `.codex/skills/spec-rewrite/SKILL.md`
- `.codex/skills/spec-create/SKILL.md`
- `.codex/skills/spec-create/references/template-full.md`
- `.codex/skills/spec-create/references/template-compact.md`
- `.codex/skills/spec-upgrade/SKILL.md`
- `.codex/skills/spec-upgrade/references/spec-format.md`
- `.codex/skills/spec-upgrade/references/upgrade-mapping.md`
- `.codex/skills/spec-upgrade/references/template-full.md`
- `.codex/skills/spec-upgrade/references/template-compact.md`
- `.codex/skills/feature-draft/SKILL.md`
- `.codex/skills/implementation-plan/SKILL.md`
- `.codex/skills/spec-update-todo/SKILL.md`
- `.codex/skills/spec-update-done/SKILL.md`
- `.codex/skills/sdd-autopilot/SKILL.md`
- `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md`
- `.codex/skills/sdd-autopilot/references/orchestrator-contract.md`
- `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md`

**프롬프트**:
implementation plan을 기준으로 docs와 Codex skill surface를 thin global spec model에 맞게 수정하세요.
핵심은 global mandatory core를 `개념 + 경계 + 결정`으로 줄이고, feature-level usage/reference/current-form CIV/strategic code map을 global default expectation에서 제거하는 것입니다.
consumer 3종 read contract를 discussion대로 고정하고, downstream skills는 global/temporary/guide separation을 새 정의에 맞게 재서술하세요.
`_sdd/spec/`는 건드리지 마세요.

### Step 3: implementation
**Codex agent_type**: `implementation`
**입력 파일**:
- `_sdd/implementation/implementation_plan_global_definition_skill_diet.md`
- `_sdd/discussion/discussion_global_definition_and_codex_skill_diet.md`
- `_sdd/discussion/discussion_codex_consumer_read_contracts.md`
- `.codex/skills/spec-review/SKILL.md`
- `.codex/skills/spec-summary/SKILL.md`
- `.codex/skills/spec-rewrite/SKILL.md`
- `.codex/skills/spec-create/SKILL.md`
- `.codex/skills/spec-upgrade/SKILL.md`
- `.codex/skills/feature-draft/SKILL.md`
- `.codex/skills/implementation-plan/SKILL.md`
- `.codex/skills/spec-update-todo/SKILL.md`
- `.codex/skills/spec-update-done/SKILL.md`
- `.codex/skills/sdd-autopilot/SKILL.md`
**출력 파일**:
- `.claude/skills/spec-review/SKILL.md`
- `.claude/skills/spec-summary/SKILL.md`
- `.claude/skills/spec-rewrite/SKILL.md`
- `.claude/skills/spec-create/SKILL.md`
- `.claude/skills/spec-create/references/template-full.md`
- `.claude/skills/spec-create/references/template-compact.md`
- `.claude/skills/spec-upgrade/SKILL.md`
- `.claude/skills/spec-upgrade/references/spec-format.md`
- `.claude/skills/spec-upgrade/references/upgrade-mapping.md`
- `.claude/skills/spec-upgrade/references/template-full.md`
- `.claude/skills/spec-upgrade/references/template-compact.md`
- `.claude/skills/feature-draft/SKILL.md`
- `.claude/skills/implementation-plan/SKILL.md`
- `.claude/skills/spec-update-todo/SKILL.md`
- `.claude/skills/spec-update-done/SKILL.md`
- `.claude/skills/sdd-autopilot/SKILL.md`
- `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md`
- `.claude/skills/sdd-autopilot/references/orchestrator-contract.md`
- `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md`
- `.claude/agents/spec-review.md`
- `.claude/agents/spec-update-todo.md`
- `.claude/agents/spec-update-done.md`
- `.claude/agents/implementation-plan.md`
- `.claude/agents/feature-draft.md`

**프롬프트**:
Codex 쪽 변경과 의미가 맞도록 Claude skill/agent mirror를 동기화하세요.
Claude-specific 용어와 실행 방식은 유지하되, thin global spec model과 consumer read contract는 동일하게 반영해야 합니다.
다른 사람이 동시에 작업 중일 수 있으니 기존 변경을 되돌리지 말고 필요한 범위만 수정하세요.

### Step 4: implementation_review
**Codex agent_type**: `implementation_review`
**입력 파일**:
- `_sdd/implementation/implementation_plan_global_definition_skill_diet.md`
- `_sdd/discussion/discussion_global_definition_and_codex_skill_diet.md`
- `_sdd/discussion/discussion_codex_consumer_read_contracts.md`
- `docs/SDD_SPEC_DEFINITION.md`
- `docs/SDD_CONCEPT.md`
- `docs/SDD_WORKFLOW.md`
- `docs/SDD_QUICK_START.md`
- `docs/sdd.md`
- `.codex/skills/spec-review/SKILL.md`
- `.codex/skills/spec-summary/SKILL.md`
- `.codex/skills/spec-rewrite/SKILL.md`
- `.codex/skills/spec-create/SKILL.md`
- `.codex/skills/spec-upgrade/SKILL.md`
- `.codex/skills/feature-draft/SKILL.md`
- `.codex/skills/implementation-plan/SKILL.md`
- `.codex/skills/spec-update-todo/SKILL.md`
- `.codex/skills/spec-update-done/SKILL.md`
- `.codex/skills/sdd-autopilot/SKILL.md`
- `.claude/skills/spec-review/SKILL.md`
- `.claude/skills/spec-summary/SKILL.md`
- `.claude/skills/spec-rewrite/SKILL.md`
- `.claude/skills/spec-create/SKILL.md`
- `.claude/skills/spec-upgrade/SKILL.md`
- `.claude/skills/feature-draft/SKILL.md`
- `.claude/skills/implementation-plan/SKILL.md`
- `.claude/skills/spec-update-todo/SKILL.md`
- `.claude/skills/spec-update-done/SKILL.md`
- `.claude/skills/sdd-autopilot/SKILL.md`
**출력 파일**: `_sdd/implementation/implementation_review_global_definition_skill_diet.md`

**프롬프트**:
discussion 결론 대비 docs/Codex/Claude surface를 리뷰하세요.
결함은 severity별로 분류하고, 특히 아래를 중점 확인하세요.
- global core를 여전히 usage/reference/current-form CIV/strategic code map으로 두고 있지 않은가
- consumer 3종이 absence-as-non-defect contract를 반영했는가
- Claude mirror가 Codex와 semantic drift 없이 동기화됐는가
global spec에 usage/reference/CIV가 빠져 있다는 사실 자체는 defect로 분류하지 마세요.

### Step 5: implementation
**Codex agent_type**: `implementation`
**입력 파일**:
- `_sdd/implementation/implementation_plan_global_definition_skill_diet.md`
- `_sdd/implementation/implementation_review_global_definition_skill_diet.md`
**출력 파일**:
- `docs/SDD_SPEC_DEFINITION.md`
- `docs/SDD_CONCEPT.md`
- `docs/SDD_WORKFLOW.md`
- `docs/SDD_QUICK_START.md`
- `docs/sdd.md`
- `docs/en/SDD_SPEC_DEFINITION.md`
- `docs/en/SDD_CONCEPT.md`
- `docs/en/SDD_WORKFLOW.md`
- `docs/en/SDD_QUICK_START.md`
- `docs/en/sdd.md`
- `.codex/skills/spec-review/SKILL.md`
- `.codex/skills/spec-summary/SKILL.md`
- `.codex/skills/spec-rewrite/SKILL.md`
- `.codex/skills/spec-create/SKILL.md`
- `.codex/skills/spec-upgrade/SKILL.md`
- `.codex/skills/feature-draft/SKILL.md`
- `.codex/skills/implementation-plan/SKILL.md`
- `.codex/skills/spec-update-todo/SKILL.md`
- `.codex/skills/spec-update-done/SKILL.md`
- `.codex/skills/sdd-autopilot/SKILL.md`
- `.claude/skills/spec-review/SKILL.md`
- `.claude/skills/spec-summary/SKILL.md`
- `.claude/skills/spec-rewrite/SKILL.md`
- `.claude/skills/spec-create/SKILL.md`
- `.claude/skills/spec-upgrade/SKILL.md`
- `.claude/skills/feature-draft/SKILL.md`
- `.claude/skills/implementation-plan/SKILL.md`
- `.claude/skills/spec-update-todo/SKILL.md`
- `.claude/skills/spec-update-done/SKILL.md`
- `.claude/skills/sdd-autopilot/SKILL.md`

**프롬프트**:
review report의 critical/high/medium/low 이슈를 해결하세요.
thin global spec model을 다시 두껍게 만들지 말고, 필요한 수정만 최소 범위로 반영하세요.

### Step 6: implementation_review
**Codex agent_type**: `implementation_review`
**입력 파일**:
- `_sdd/implementation/implementation_plan_global_definition_skill_diet.md`
- `_sdd/implementation/implementation_review_global_definition_skill_diet.md`
- `docs/SDD_SPEC_DEFINITION.md`
- `docs/SDD_CONCEPT.md`
- `docs/SDD_WORKFLOW.md`
- `docs/SDD_QUICK_START.md`
- `docs/sdd.md`
- `docs/en/SDD_SPEC_DEFINITION.md`
- `docs/en/SDD_CONCEPT.md`
- `docs/en/SDD_WORKFLOW.md`
- `docs/en/SDD_QUICK_START.md`
- `docs/en/sdd.md`
- `.codex/skills/spec-review/SKILL.md`
- `.codex/skills/spec-summary/SKILL.md`
- `.codex/skills/spec-rewrite/SKILL.md`
- `.codex/skills/spec-create/SKILL.md`
- `.codex/skills/spec-upgrade/SKILL.md`
- `.codex/skills/feature-draft/SKILL.md`
- `.codex/skills/implementation-plan/SKILL.md`
- `.codex/skills/spec-update-todo/SKILL.md`
- `.codex/skills/spec-update-done/SKILL.md`
- `.codex/skills/sdd-autopilot/SKILL.md`
- `.claude/skills/spec-review/SKILL.md`
- `.claude/skills/spec-summary/SKILL.md`
- `.claude/skills/spec-rewrite/SKILL.md`
- `.claude/skills/spec-create/SKILL.md`
- `.claude/skills/spec-upgrade/SKILL.md`
- `.claude/skills/feature-draft/SKILL.md`
- `.claude/skills/implementation-plan/SKILL.md`
- `.claude/skills/spec-update-todo/SKILL.md`
- `.claude/skills/spec-update-done/SKILL.md`
- `.claude/skills/sdd-autopilot/SKILL.md`
**출력 파일**: `_sdd/implementation/implementation_review_global_definition_skill_diet_rerun.md`

**프롬프트**:
수정 후 재리뷰를 진행하세요.
종료 조건은 critical = 0 AND high = 0 AND medium = 0 입니다.
low만 남으면 로그에 남기고 종료하세요.

## Review-Fix Loop

- **최대 반복**: 2회
- **종료 조건**: critical = 0 AND high = 0 AND medium = 0
- **수정 대상**: critical/high/medium/low
- **MAX 도달 시 분기**: critical/high 잔존 시 중단, medium만 잔존 시 로그 기록 후 계속 진행

## Test Strategy

- **방식**: inline
- **실행 명령**:
  - `git diff --check -- docs docs/en .codex/skills .claude/skills .claude/agents _sdd/pipeline/orchestrators/orchestrator_global_definition_skill_diet.md`
  - `rg -n "사용 가이드|기대 결과|Strategic Code Map|Contract / Invariants / Verifiability" docs/SDD_SPEC_DEFINITION.md docs/en/SDD_SPEC_DEFINITION.md .codex/skills/spec-review/SKILL.md .codex/skills/spec-summary/SKILL.md .codex/skills/spec-rewrite/SKILL.md .codex/skills/spec-create/SKILL.md .codex/skills/spec-upgrade/SKILL.md .codex/skills/feature-draft/SKILL.md .codex/skills/implementation-plan/SKILL.md .codex/skills/spec-update-todo/SKILL.md .codex/skills/spec-update-done/SKILL.md .codex/skills/sdd-autopilot/SKILL.md .claude/skills/spec-review/SKILL.md .claude/skills/spec-summary/SKILL.md .claude/skills/spec-rewrite/SKILL.md .claude/skills/spec-create/SKILL.md .claude/skills/spec-upgrade/SKILL.md .claude/skills/feature-draft/SKILL.md .claude/skills/implementation-plan/SKILL.md .claude/skills/spec-update-todo/SKILL.md .claude/skills/spec-update-done/SKILL.md .claude/skills/sdd-autopilot/SKILL.md`
  - `rg -n "개념 \\+ 경계 \\+ 결정|concept \\+ boundaries \\+ decisions|absence-as-non-defect|thin global spec|guardrails" docs docs/en .codex/skills .claude/skills`
- **선택 근거**: `_sdd/env.md`상 전통적 테스트 프레임워크가 없고, 이번 변경은 문서/skill contract refactor이므로 diff/grep sweep이 가장 직접적인 검증 수단이다.
- **사용자 보고 형식**: 실행 명령, 통과/실패 여부, grep hit의 의미, 수동 spot-check 필요 파일을 `_sdd/implementation/test_results/test_results_global_definition_skill_diet.md`에 기록하고 최종 요약에서 집계한다.

## Error Handling

- **재시도 횟수**: 2회
- **핵심 단계**: `implementation_plan`, `implementation`, `implementation_review`
- **비핵심 단계**: 없음
- **실패 원칙**:
  - discussion 결론과 직접 충돌하는 수정안이 나오면 해당 단계는 실패로 간주하고 재시도한다.
  - Codex/Claude mirror semantic drift가 남으면 review-fix loop를 한 번 더 수행한다.
  - verification 명령 실패 시 원인과 수동 검증 방법을 테스트 결과 파일과 최종 보고서에 명시한다.
