---
name: spec-rewrite
description: This skill should be used when the user asks to "rewrite spec", "refactor spec", "simplify spec", "split spec into files", "clean up spec", "review spec quality", or equivalent phrases indicating they want to reorganize an overly long/complex spec by pruning noise, splitting into hierarchical files, and explicitly listing ambiguities/problems.
version: 1.5.0
---

# spec-rewrite

## Goal

비대하거나 혼란스러운 스펙을 더 읽기 쉽고 유지보수 가능한 구조로 재작성한다. 핵심 내용은 보존하고, 저가치 내용은 appendix로 이동하거나 제거하며, ambiguity와 unresolved issue는 명시적으로 남긴다.

## Acceptance Criteria

> 완료 전 아래 기준을 자체 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

- [ ] AC1: 리라이트 대상과 범위를 진단하고, rewrite plan을 먼저 제시했다.
- [ ] AC2: `_sdd/spec/prev/`에 안전 백업을 남겼다.
- [ ] AC3: rewritten spec가 더 명확한 구조를 가지며, 링크와 파일 경로가 유효하다.
- [ ] AC4: 중요한 rationale과 `Source` 필드는 보존되었다.
- [ ] AC5: ambiguity, conflict, missing decision이 `_sdd/spec/logs/REWRITE_REPORT.md`에 기록되었다.
- [ ] AC6: `references/`와 `examples/`는 유지되고, 본문은 rewrite contract를 concise하게 설명한다.

## SDD Lens

- spec-rewrite는 feature 추가가 아니라 문서 구조 개선 작업이다.
- 정보 손실보다 구조 개선이 중요하지만, why-context를 잃어서는 안 된다.
- “깔끔해 보이게” 만드는 것보다 이후 `implementation-plan`, `spec-summary`, `guide-create`가 읽기 쉽게 만드는 것이 목표다.

## Companion Assets

- `references/template-compact.md`
- `references/spec-format.md`
- `references/rewrite-checklist.md`
- `examples/rewrite-report.md`

## Hard Rules

1. 수정 전 반드시 `_sdd/spec/prev/PREV_<filename>_<timestamp>.md`로 백업한다.
2. 삭제하는 내용에 중요한 rationale이 있으면 `DECISION_LOG.md` 또는 rewrite report에 보존한다.
3. `Source` 필드가 있으면 재구성 후에도 유지한다.
4. 대규모 구조 변경이나 파일 분할은 계획을 먼저 제시하고 필요한 경우 사용자 확인을 받는다.
5. 기존 문서 언어를 따른다. 새 프로젝트는 한국어를 기본으로 한다.
6. 장문 문서나 다중 파일 rewrite는 caller가 먼저 skeleton/섹션 헤더를 직접 기록한 뒤, 같은 흐름에서 내용을 채운다.
7. rewrite는 핵심 계약을 더 선명하게 해야지, 내용을 임의로 확장하면 안 된다.

## Input Sources

우선순위:

1. `_sdd/spec/main.md` 또는 대표 spec
2. linked sub-spec
3. `_sdd/spec/DECISION_LOG.md`
4. `_sdd/implementation/` 산출물

## Process

### Step 1: Diagnose the Current Spec

다음을 진단한다.

- 섹션 길이 불균형
- 중복 설명 / 로그성 텍스트
- appendix로 보내도 되는 저가치 내용
- 파일 분할 필요성
- 모호한 표현과 누락된 결정
- whitepaper 섹션 누락 여부

### Step 2: Propose the Rewrite Plan

실제 수정 전에 아래를 정리해 제시한다.

- main에 남길 내용
- appendix로 이동할 내용
- split map 또는 파일 재배치 계획
- ambiguity / risk / unresolved decision

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
- `Source`와 중요한 rationale은 보존

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

### Step 5: Validate and Report

아래를 검증하고 `_sdd/spec/logs/REWRITE_REPORT.md`를 작성한다.

- 링크와 파일 경로 유효성
- ambiguity / issue 기록 여부
- whitepaper 핵심 섹션 상태
- pruning / move / split 결과
- decision log 추가 여부

## Output Contract

기본 산출물:

- rewritten spec files
- `_sdd/spec/logs/REWRITE_REPORT.md`

리포트에 포함할 내용:

- rewrite summary
- pruned / moved sections
- file split map
- ambiguities and issues
- whitepaper section status
- decision log additions

## Error Handling

| 상황 | 대응 |
|------|------|
| spec 없음 | `/spec-create` 먼저 권장 |
| 잘 구조화된 spec | 불필요한 rewrite를 피하고 개선점만 보고 |
| split 후 링크 깨짐 | 경로 검증 후 수정 |
| DECISION_LOG 없음 | 필요 시 새로 생성 |
| 범위가 너무 큼 | index 중심으로 나누고 점진적으로 rewrite |

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
