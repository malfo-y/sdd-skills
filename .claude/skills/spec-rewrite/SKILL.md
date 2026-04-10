---
name: spec-rewrite
description: This skill should be used when the user asks to "rewrite spec", "refactor spec", "simplify spec", "split spec into files", "clean up spec", "review spec quality", or equivalent phrases indicating they want to reorganize an overly long/complex spec by pruning noise, splitting into hierarchical files, and explicitly listing ambiguities/problems.
version: 1.9.0
---

# spec-rewrite

## Goal

비대하거나 혼란스러운 스펙을 current canonical model에 더 잘 맞는 구조로 재작성한다. 현재 모델에서 global spec의 목표는 `개념 + 경계 + 결정`을 더 선명하게 만드는 것이고, feature-level usage/contract/reference/inventory는 global 본문에서 내려보내는 것이다.

핵심 내용은 보존하고, 저가치 내용은 appendix 또는 별도 supporting surface로 이동하거나 제거하며, ambiguity와 unresolved issue는 명시적으로 남긴다. `spec-rewrite`는 missing content authoring 도구가 아니라 구조 개선 도구다.

## Acceptance Criteria

- [ ] 리라이트 대상과 범위를 핵심 metric으로 진단하고 근거를 남겼다.
- [ ] `_sdd/spec/logs/spec-rewrite-plan.md`가 canonical-fit rationale, split map, ambiguity/risk를 포함한 상태로 먼저 저장되었다.
- [ ] rewritten spec가 현재 canonical model에 더 잘 맞는 구조를 가진다.
- [ ] 중요한 rationale, `Why`, inline citation, code excerpt header는 보존되었다.
- [ ] `rewrite_report.md`가 metric scorecard, canonical-fit 평가, unresolved warning, plan 대비 주요 deviation을 포함한다.
- [ ] 누락된 내용을 임의로 창작하지 않고, 필요한 경우 warning으로 남겼다.

## SDD Lens

- spec-rewrite는 feature 추가가 아니라 문서 구조 개선 작업이다.
- current canonical model에서 global spec은 얇은 기준 문서이고, temporary spec은 실행 청사진이다.
- rewrite의 목표는 global 본문에서 feature-level usage, contract, reference, inventory를 걷어내고 핵심 결정이 잘 보이게 만드는 것이다.
- repo-wide invariant가 정말 필요하면 guardrails 또는 key decisions에 흡수한다.

## Companion Assets

- `references/template-compact.md`
- `references/spec-format.md`
- `references/rewrite-checklist.md`
- `examples/rewrite-plan.md`
- `examples/rewrite-report.md`
- SDD 정의 문서: https://github.com/malfo-y/sdd-skills/tree/main/docs

## Hard Rules

1. 삭제하는 내용에 중요한 rationale이 있으면 `decision_log.md` 또는 rewrite report에 보존한다.
2. `Source`, component-level `Why`, inline citation, code excerpt header가 있으면 재구성 후에도 유지한다.
3. `_sdd/spec/logs/spec-rewrite-plan.md`를 rewrite 시작 전에 반드시 저장하고, 이후 실행은 이 파일을 기준으로 진행한다.
4. 대규모 구조 변경이나 파일 분할은 계획 파일을 먼저 저장한 뒤 필요한 경우 사용자 확인을 받는다.
5. rewrite는 global spec을 다시 두껍게 만들지 않는다.
6. missing global core나 temporary core는 warning으로 남길 수 있지만 자동 생성하지 않는다.

## Process

### Step 1: Diagnose the Current Spec

진단 축:

- `Component Separation`
- `Findability`
- `Repo Purpose Clarity`
- `Boundary Clarity`
- `Decision Preservation`
- `Contamination Control`
- `Why/Decision Preservation`
- `Canonical Fit`

`Canonical Fit`에서 특히 본다.

- global spec인지 temporary spec인지 문서 목적이 선명한가
- global spec이면 `배경/개념`, `경계`, `결정`이 선명한가
- feature-level usage/contract/reference/inventory가 global 본문을 오염시키는가
- temporary spec이면 delta / touchpoints / validation linkage가 보이는가
- appendix/reference가 본문을 대체하지 않는가

### Step 2: Write the Rewrite Plan

plan에는 아래를 포함한다.

- main에 남길 내용
- appendix 또는 support surface로 이동할 내용
- split map 또는 파일 재배치 계획 (분할이 필요하면 아래 축 선택 기준 적용)

multi-file 분할이 필요할 때 축 선택:

| repo 성격 | 분할 축 | 예시 |
|-----------|---------|------|
| 독립적인 사용자 기능/endpoint가 여러 개 | domain | `auth.md`, `payments.md` |
| 기능은 단일에 가까우나 repo가 큼 | topic | `architecture.md`, `data-conventions.md` |

어떤 축이든 각 파일에 담는 건 global-level 결정만이다.
- 낮은 점수 metric을 어떻게 개선할지에 대한 rationale
- ambiguity / risk / unresolved decision
- warning만 남길 항목
- rewrite 대상 파일 목록
- 실행 순서와 deviation 기록 규칙

### Step 3: Rewrite the Spec

원칙:

- `spec-rewrite-plan.md`를 실행 기준으로 삼는다.
- index/main은 먼저 고정한다.
- global spec이면 `개념 + 경계 + 결정`을 더 잘 드러내도록 구조를 재배치한다.
- decision-bearing value가 없는 feature inventory는 reference, guide, appendix, code 쪽으로 내린다.
- 없는 canonical content를 새로 만들어 넣지 말고, 누락은 report에 warning으로 남긴다.

### Step 4: Validate and Report

아래를 검증하고 `_sdd/spec/logs/rewrite_report.md`를 작성한다.

- 링크와 파일 경로 유효성
- 핵심 metric scorecard
- canonical-fit 평가
- ambiguity / issue 기록 여부
- pruning / move / split 결과
- `spec-rewrite-plan.md` 대비 실제 실행 결과와 deviation

## Output Contract

- rewritten spec files
- `_sdd/spec/logs/spec-rewrite-plan.md`
- `_sdd/spec/logs/rewrite_report.md`

## Error Handling

| 상황 | 대응 |
|------|------|
| spec 없음 | `/spec-create` 먼저 권장 |
| 잘 구조화된 spec | 불필요한 rewrite를 피하고 개선점만 보고 |
| split 후 링크 깨짐 | 경로 검증 후 수정 |
| 범위가 너무 큼 | index 중심으로 나누고 점진적으로 rewrite |
| canonical core 누락 | 자동 생성하지 말고 rewrite_report에 경고 |

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
