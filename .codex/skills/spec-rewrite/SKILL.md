---
name: spec-rewrite
description: This skill should be used when the user asks to "rewrite spec", "refactor spec", "simplify spec", "split spec into files", "clean up spec", "review spec quality", or equivalent phrases indicating they want to reorganize an overly long/complex spec by pruning noise, splitting into hierarchical files, and explicitly listing ambiguities/problems.
version: 1.8.0
---

# spec-rewrite

## Goal

비대하거나 혼란스러운 스펙을 current canonical model에 더 잘 맞는 구조로 재작성한다. 재작성 전에 현재 스펙을 핵심 품질 metric과 canonical-fit 기준으로 진단하고, 그 진단을 근거로 `_sdd/spec/logs/spec-rewrite-plan.md`와 `rewrite_report.md`를 만든다.

핵심 내용은 보존하고, 저가치 내용은 appendix로 이동하거나 제거하며, ambiguity와 unresolved issue는 명시적으로 남긴다. `spec-rewrite`는 missing content authoring 도구가 아니라 구조 개선 도구다.

## Acceptance Criteria

> 완료 전 아래 기준을 자체 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

- [ ] AC1: 리라이트 대상과 범위를 핵심 metric으로 진단하고 근거를 남겼다.
- [ ] AC2: `_sdd/spec/logs/spec-rewrite-plan.md`가 canonical-fit rationale, split map, ambiguity/risk를 포함한 상태로 먼저 저장되었다.
- [ ] AC3: `_sdd/spec/prev/`에 안전 백업을 남겼다.
- [ ] AC4: rewritten spec가 현재 canonical model에 더 잘 맞는 구조를 가진다.
- [ ] AC5: 중요한 rationale, `Why`, inline citation, code excerpt header는 보존되었다.
- [ ] AC6: `rewrite_report.md`가 metric scorecard, canonical-fit 평가, unresolved warning, plan 대비 주요 deviation을 포함한다.
- [ ] AC7: 누락된 내용을 임의로 창작하지 않고, 필요한 경우 warning으로 남겼다.

## SDD Lens

- spec-rewrite는 feature 추가가 아니라 문서 구조 개선 작업이다.
- current canonical model에서 global spec은 얇은 기준 문서이고, temporary spec은 실행 청사진이다.
- rewrite의 목적은 inventory-heavy 문서를 decision-bearing structure와 explicit CIV 중심 문서로 정렬하는 것이다.
- appendix와 reference information은 장려되지만, 본문 핵심을 대체하면 안 된다.

## Companion Assets

- `references/template-compact.md`
- `references/spec-format.md`
- `references/rewrite-checklist.md`
- `examples/rewrite-plan.md`
- `examples/rewrite-report.md`
- `docs/SDD_SPEC_DEFINITION.md`

## Hard Rules

1. 수정 전 반드시 `_sdd/spec/prev/prev_<filename>_<timestamp>.md`로 백업한다.
2. 삭제하는 내용에 중요한 rationale이 있으면 `decision_log.md` 또는 rewrite report에 보존한다.
3. `Source`, component-level `Why`, inline citation, code excerpt header가 있으면 재구성 후에도 유지한다.
4. `_sdd/spec/logs/spec-rewrite-plan.md`를 rewrite 시작 전에 반드시 저장하고, 이후 실행은 이 파일을 기준으로 진행한다.
5. 대규모 구조 변경이나 파일 분할은 계획 파일을 먼저 저장한 뒤 필요한 경우 사용자 확인을 받는다.
6. rewrite 도중 scope, split map, prune 기준이 크게 바뀌면 plan 파일부터 갱신한 후 계속 진행한다.
7. 기존 문서 언어를 따른다. 새 프로젝트는 한국어를 기본으로 한다.
8. 장문 문서나 다중 파일 rewrite는 caller가 먼저 skeleton/섹션 헤더를 직접 기록한 뒤, 같은 흐름에서 내용을 채운다.
9. rewrite는 핵심 계약을 더 선명하게 해야지, 내용을 임의로 확장하면 안 된다.
10. missing global spec core 또는 temporary spec core는 경고할 수 있지만 자동 생성하지 않는다. 생성/보강은 `spec-create` 또는 `spec-upgrade`의 역할이다.

## Input Sources

우선순위:

1. `_sdd/spec/main.md` 또는 대표 spec
2. linked sub-spec
3. `_sdd/spec/decision_log.md`
4. `_sdd/implementation/` 산출물
5. `docs/SDD_SPEC_DEFINITION.md`

## Process

### Step 1: Diagnose the Current Spec

먼저 다음 reference를 읽는다.

- `references/template-compact.md`
- `references/spec-format.md`
- `references/rewrite-checklist.md`
- `docs/SDD_SPEC_DEFINITION.md`

진단은 아래 축을 기준으로 수행한다.

- `Component Separation`
- `Findability`
- `Repo Purpose Clarity`
- `Architecture Clarity`
- `Usage Completeness`
- `Environment Reproducibility`
- `Ambiguity Control`
- `Why/Decision Preservation`
- `Canonical Fit`

`Canonical Fit`에서 특히 본다.

- global spec인지 temporary spec인지 문서 목적이 선명한가
- global spec이면 CIV, decision-bearing structure, usage가 보이는가
- temporary spec이면 delta / touchpoints / validation linkage가 보이는가
- appendix/reference가 본문을 대체하지 않는가

### Step 2: Write the Rewrite Plan

실제 수정 전에 `_sdd/spec/logs/`를 준비하고 `_sdd/spec/logs/spec-rewrite-plan.md`를 저장한다.

plan에는 아래를 포함한다.

- main에 남길 내용
- appendix로 이동할 내용
- split map 또는 파일 재배치 계획
- 낮은 점수 metric을 어떻게 개선할지에 대한 rationale
- ambiguity / risk / unresolved decision
- canonical-fit 기준에서 warning만 남길 항목
- rewrite 대상 파일 목록
- 실행 순서와 deviation 기록 규칙

### Step 3: Create Safety Backups

- `_sdd/spec/prev/` 생성
- 대상 파일 백업

### Step 4: Rewrite the Spec

원칙:

- `spec-rewrite-plan.md`를 실행 기준으로 삼는다.
- index/main은 먼저 고정한다.
- 필요한 경우 global spec core를 더 잘 드러내도록 구조를 재배치한다.
- decision-bearing value가 없는 inventory는 reference 또는 appendix로 내린다.
- `Source`, `Why`, 중요한 rationale, inline citation, code excerpt header는 보존한다.
- 없는 canonical content를 새로 만들어 넣지 말고, 누락은 report에 warning으로 남긴다.

장문 rewrite는 다음 순서를 따른다.

1. 대상 파일 skeleton/섹션 헤더를 직접 작성
2. 같은 흐름에서 각 섹션 내용을 채움
3. TODO/placeholder를 제거하고 finalize
4. 의존 섹션은 `default`, 독립 파일/섹션은 `worker`로 채운다

### Step 5: Validate and Report

아래를 검증하고 `_sdd/spec/logs/rewrite_report.md`를 작성한다.

- 링크와 파일 경로 유효성
- 핵심 metric scorecard
- canonical-fit 평가
- ambiguity / issue 기록 여부
- pruning / move / split 결과
- `spec-rewrite-plan.md` 대비 실제 실행 결과와 deviation
- 자동 보강하지 않고 warning만 남긴 항목

## Output Contract

기본 산출물:

- rewritten spec files
- `_sdd/spec/logs/spec-rewrite-plan.md`
- `_sdd/spec/logs/rewrite_report.md`

## Error Handling

| 상황 | 대응 |
|------|------|
| spec 없음 | `/spec-create` 먼저 권장 |
| 잘 구조화된 spec | 불필요한 rewrite를 피하고 개선점만 보고 |
| split 후 링크 깨짐 | 경로 검증 후 수정 |
| decision_log 없음 | 필요 시 새로 생성 |
| 범위가 너무 큼 | index 중심으로 나누고 점진적으로 rewrite |
| canonical core 누락 | 자동 생성하지 말고 rewrite_report에 경고 |

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
