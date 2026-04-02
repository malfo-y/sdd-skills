---
name: spec-rewrite
description: This skill should be used when the user asks to "rewrite spec", "refactor spec", "simplify spec", "split spec into files", "clean up spec", "review spec quality", or equivalent phrases indicating they want to reorganize an overly long/complex spec by pruning noise, splitting into hierarchical files, and explicitly listing ambiguities/problems.
version: 1.6.0
---

# spec-rewrite

## Goal

비대하거나 혼란스러운 스펙을 더 읽기 쉽고 유지보수 가능한 구조로 재작성한다. 재작성 전에 현재 스펙을 8개 핵심 품질 metric과 spec-as-whitepaper 기준으로 진단하고, 그 진단을 근거로 rewrite plan과 `REWRITE_REPORT.md`를 만든다.

핵심 내용은 보존하고, 저가치 내용은 appendix로 이동하거나 제거하며, ambiguity와 unresolved issue는 명시적으로 남긴다. `spec-rewrite`는 정리/재배치 도구이지, 누락된 whitepaper 섹션을 자동 생성하는 스킬이 아니다.

## Acceptance Criteria

> 완료 전 아래 기준을 자체 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

- [ ] AC1: 리라이트 대상과 범위를 8개 핵심 metric으로 진단하고, 점수 또는 동등한 판단 근거를 남겼다.
- [ ] AC2: rewrite plan이 metric 기반 rationale, split map, ambiguity/risk를 포함한 상태로 먼저 제시되었다.
- [ ] AC3: `_sdd/spec/prev/`에 안전 백업을 남겼다.
- [ ] AC4: rewritten spec가 더 명확한 구조를 가지며, 링크와 파일 경로가 유효하다.
- [ ] AC5: 중요한 rationale, `Why`, `Source`, inline citation, code excerpt header는 보존되었다.
- [ ] AC6: `REWRITE_REPORT.md`가 metric scorecard, whitepaper 적합성 평가, unresolved warning을 포함한다.
- [ ] AC7: `references/`와 `examples/`는 유지되고, 본문은 rewrite contract를 concise하게 설명한다.

## SDD Lens

- spec-rewrite는 feature 추가가 아니라 문서 구조 개선 작업이다.
- 정보 손실보다 구조 개선이 중요하지만, why-context를 잃어서는 안 된다.
- “깔끔해 보이게” 만드는 것보다 이후 `implementation-plan`, `spec-summary`, `guide-create`가 읽기 쉽게 만드는 것이 목표다.
- `docs/SDD_SPEC_DEFINITION.md`가 말하는 화이트페이퍼형 Single Source of Truth를 훼손하지 않는지가 핵심 검증 축이다.

## Companion Assets

- `references/template-compact.md`
- `references/spec-format.md`
- `references/rewrite-checklist.md`
- `examples/rewrite-report.md`
- `docs/SDD_SPEC_DEFINITION.md`

## Hard Rules

1. 수정 전 반드시 `_sdd/spec/prev/PREV_<filename>_<timestamp>.md`로 백업한다.
2. 삭제하는 내용에 중요한 rationale이 있으면 `DECISION_LOG.md` 또는 rewrite report에 보존한다.
3. `Source`, component-level `Why`, inline citation, code excerpt header가 있으면 재구성 후에도 유지한다.
4. 대규모 구조 변경이나 파일 분할은 계획을 먼저 제시하고 필요한 경우 사용자 확인을 받는다.
5. 기존 문서 언어를 따른다. 새 프로젝트는 한국어를 기본으로 한다.
6. 장문 문서나 다중 파일 rewrite는 caller가 먼저 skeleton/섹션 헤더를 직접 기록한 뒤, 같은 흐름에서 내용을 채운다.
7. rewrite는 핵심 계약을 더 선명하게 해야지, 내용을 임의로 확장하면 안 된다.
8. §1, §2, §5 같은 whitepaper 핵심 narrative 섹션이 원문에 존재하면 prune/appendix 이동으로 약화시키지 않는다.
9. 누락된 whitepaper 섹션은 경고할 수 있지만 자동 생성하지 않는다. 생성/보강은 `spec-create` 또는 `spec-upgrade`의 역할이다.

## Input Sources

우선순위:

1. `_sdd/spec/main.md` 또는 대표 spec
2. linked sub-spec
3. `_sdd/spec/DECISION_LOG.md`
4. `_sdd/implementation/` 산출물
5. `docs/SDD_SPEC_DEFINITION.md`

## Process

### Step 1: Diagnose the Current Spec

먼저 다음 reference를 읽는다.

- `references/template-compact.md`
- `references/spec-format.md`
- `references/rewrite-checklist.md`
- `docs/SDD_SPEC_DEFINITION.md`

진단은 아래 8개 핵심 metric을 기준으로 수행한다. 상세 질문형 rubric은 `references/rewrite-checklist.md`를 canonical source로 사용한다.

평점 기준:

- `0`: 거의 없음. 사용자가 이 정보로 판단/행동하기 어렵다.
- `1`: 일부 존재하지만 불완전하거나 많이 흩어져 있다.
- `2`: 대체로 충분하지만 핵심 공백이나 혼동 지점이 있다.
- `3`: 명확하고 일관되며, 사용자가 쉽게 이해하고 활용할 수 있다.

핵심 metric:

- `Component Separation` (`component 분리 적절성`): 각 주요 component가 대표 섹션/파일에 귀속되는가
- `Findability` (`탐색성`): 필요한 정보를 main 기준 2-hop 이내에 찾을 수 있는가
- `Repo Purpose Clarity` (`레포 목적 이해도`): main만 읽고 3문장 안에 레포 목적과 핵심 기능을 설명할 수 있는가
- `Architecture Clarity` (`아키텍처 이해도`): 핵심 흐름과 component 책임을 혼동 없이 설명할 수 있는가
- `Usage Completeness` (`사용법 완결성`): 신규 사용자가 대표 시나리오를 문서만 보고 실행할 수 있는가
- `Environment Reproducibility` (`환경 재현성`): 실행 조건, 의존성, 설정을 문서만으로 재현할 수 있는가
- `Ambiguity Control` (`모호성 수준`): 측정 불가능한 표현, 책임 불명확, 미정의 용어가 적절히 통제되는가
- `Why/Decision Preservation` (`Why/decision 보존도`): 중요한 설계 이유와 결정 배경이 삭제되거나 appendix로 밀려나지 않았는가

추가로 `docs/SDD_SPEC_DEFINITION.md` 기준 whitepaper 적합성을 함께 본다.

- 배경 및 동기 설명 여부
- 핵심 설계 서사와 로직 흐름 설명 여부
- 구현 근거와 코드 매핑 존재 여부
- 사용 가이드와 기대 결과 존재 여부
- 참조형 보조 정보와 narrative 섹션의 균형

### Step 2: Propose the Rewrite Plan

실제 수정 전에 아래를 정리해 제시한다.

- main에 남길 내용
- appendix로 이동할 내용
- split map 또는 파일 재배치 계획
- 낮은 점수 metric을 어떻게 개선할지에 대한 rationale
- ambiguity / risk / unresolved decision
- whitepaper 기준에서 경고만 남길 항목

대규모 구조 변경이면 여기서 사용자 확인을 받는다.

### Step 3: Create Safety Backups

- `_sdd/spec/prev/` 생성
- 대상 파일 백업

### Step 4: Rewrite the Spec

원칙:

- index/main은 먼저 고정
- 이동 대상과 신규 파일 경로를 확정
- 필요 시 파일별 rewrite를 병렬화
- appendix 이동, split, pruning을 수행
- `Source`, `Why`, 중요한 rationale, inline citation, code excerpt header는 보존
- 없는 whitepaper narrative를 새로 만들어 넣지 말고, 누락은 report에 경고로 남김

장문 rewrite는 다음 순서를 따른다.

1. 대상 파일 skeleton/섹션 헤더를 직접 작성
2. 같은 흐름에서 각 섹션 내용을 채움
3. TODO/placeholder를 제거하고 finalize
4. 의존 섹션은 `default`, 독립 파일/섹션은 `worker`로 채운다

구조 개선의 대표 패턴:

- 중복 내용 제거
- 긴 역사/로그는 appendix나 report로 이동
- component별 파일 분리
- 인덱스 문서에서 전체 구조와 링크를 명확히 함
- 레포 목적, 핵심 흐름, 사용법이 main에서 더 빨리 파악되도록 정보 재배치

### Step 5: Validate and Report

아래를 검증하고 `_sdd/spec/logs/REWRITE_REPORT.md`를 작성한다.

- 링크와 파일 경로 유효성
- 8개 핵심 metric scorecard
- whitepaper 적합성 평가
- ambiguity / issue 기록 여부
- pruning / move / split 결과
- decision log 추가 여부
- 자동 보강하지 않고 경고만 남긴 항목

## Output Contract

기본 산출물:

- rewritten spec files
- `_sdd/spec/logs/REWRITE_REPORT.md`

리포트에 포함할 내용:

- rewrite summary
- pruned / moved sections
- file split map
- metric scorecard (`0-3`)와 핵심 근거
  - `Component Separation`
  - `Findability`
  - `Repo Purpose Clarity`
  - `Architecture Clarity`
  - `Usage Completeness`
  - `Environment Reproducibility`
  - `Ambiguity Control`
  - `Why/Decision Preservation`
- ambiguities and issues
- whitepaper fit assessment
- warnings intentionally left unresolved
- decision log additions

## Error Handling

| 상황 | 대응 |
|------|------|
| spec 없음 | `/spec-create` 먼저 권장 |
| 잘 구조화된 spec | 불필요한 rewrite를 피하고 개선점만 보고 |
| split 후 링크 깨짐 | 경로 검증 후 수정 |
| DECISION_LOG 없음 | 필요 시 새로 생성 |
| 범위가 너무 큼 | index 중심으로 나누고 점진적으로 rewrite |
| whitepaper narrative 누락 | 자동 생성하지 말고 REWRITE_REPORT에 경고 |

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
