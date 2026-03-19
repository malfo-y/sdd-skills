---
name: pr-review
description: This skill should be used when the user asks to "review PR", "PR review", "review PR against spec", "PR 리뷰", "PR 검증", "스펙 기반 PR 리뷰", "PR 승인 검토", or wants to verify a pull request's implementation against the specification and spec patch draft.
version: 1.2.0
---

# pr-review

## Goal

PR 구현을 현재 스펙과 spec patch draft 기준으로 검증하고 `_sdd/pr/PR_REVIEW.md`에 structured review report를 만든다. verdict와 blocker를 명확히 제시하되, 스펙 수정은 직접 하지 않는다.

## Acceptance Criteria

> 완료 전 아래 기준을 자체 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

- [ ] AC1: PR metadata, diff, baseline spec를 읽었다.
- [ ] AC2: patch draft가 있으면 preferred mode, 없으면 degraded mode로 실행했다.
- [ ] AC3: `_sdd/pr/PR_REVIEW.md`를 생성하거나 갱신했다.
- [ ] AC4: verdict가 `APPROVE`, `REQUEST CHANGES`, `NEEDS DISCUSSION` 중 하나로 명확히 결정되었다.
- [ ] AC5: acceptance criteria verification, spec compliance, gap analysis, recommendations가 보고서에 포함되었다.
- [ ] AC6: spec update가 필요한 항목은 보고서에만 기록하고 실제 수정은 하지 않았다.

## SDD Lens

- PR review는 단순 코드 리뷰가 아니라 spec과 구현의 정합성 검증이다.
- patch draft가 있으면 “주장된 변경”과 “실제 구현”을 비교하고, 없으면 PR과 spec만 비교한다.
- 보고서는 findings-first여야 하고 merge decision에 직접 도움이 되어야 한다.

## Companion Assets

- `references/review-checklist.md`
- `examples/sample-review.md`

## Hard Rules

1. `_sdd/spec/`는 읽기 전용이다.
2. 기본 산출물은 `_sdd/pr/PR_REVIEW.md` 하나다.
3. spec update가 필요해도 이 스킬에서 직접 수정하지 않는다.
4. 기본 출력 언어는 한국어로 하되, 사용자/스펙 언어에 맞출 수 있다.
5. patch draft가 없으면 degraded mode로 계속 진행하되, 낮은 신뢰도를 명시한다.
6. 긴 보고서나 finding이 많은 경우 `$write-phased`를 우선 사용할 수 있다.
7. 로컬 테스트를 돌릴 때는 `_sdd/env.md`를 먼저 확인한다.

## Model Hint

사용자가 Opus/Sonnet/Haiku 같은 라벨을 언급하면 `gpt-5.3-codex` 계열 reasoning 수준으로 매핑하되, 보고서 계약은 동일하다.

## Input Sources

1. `_sdd/spec/`
2. `_sdd/pr/spec_patch_draft.md`
3. `gh` CLI 기반 PR 데이터
4. test results / CI or local execution
5. `_sdd/env.md`

## Process

### Step 1: Verify Prerequisites

- `gh auth status` 확인
- PR 번호 확인
- `_sdd/pr/` 디렉토리 준비
- baseline spec와 patch draft 존재 여부 확인
- 로컬 테스트 예정이면 `_sdd/env.md` 확인

### Step 2: Choose Review Mode

- preferred mode: patch draft 있음
- degraded mode: patch draft 없음

degraded mode에서는 다음을 명시한다.

- patch draft 없음
- acceptance criteria는 PR description / commits / diff에서 추론
- 전체 신뢰도 낮음

### Step 3: Gather Evidence

다음을 수집한다.

- PR metadata와 changed files
- baseline spec 요구사항
- patch draft의 claimed changes
- 실제 구현 evidence
- 테스트 상태

대형 PR이면:

- spec / patch draft / PR diff / tests를 병렬로 수집
- acceptance / violation / gap 관점으로 finding lane을 나눈다

### Step 4: Assess the PR

다음 관점으로 검증한다.

- acceptance criteria fulfillment
- spec compliance
- patch draft vs implementation gap
- test gaps
- blocker / recommended / optional follow-up

verdict 기준:

- `APPROVE`: blocker 없음, 핵심 요구 충족
- `REQUEST CHANGES`: merge 전 수정 필요
- `NEEDS DISCUSSION`: 요구 해석, spec, 설계 결정이 모호함

### Step 5: Write the Review Report

`_sdd/pr/PR_REVIEW.md`에 다음을 정리한다.

- verdict
- metrics summary
- acceptance criteria verification
- spec compliance verification
- gap analysis
- test status
- recommendations
- items requiring spec update

기존 보고서가 있으면 `_sdd/pr/prev/PREV_PR_REVIEW_<timestamp>.md`로 백업 후 갱신한다.

## Output Contract

기본 산출물:

- `_sdd/pr/PR_REVIEW.md`

핵심 섹션:

- Verdict
- Metrics Summary
- Acceptance Criteria Verification
- Spec Compliance Verification
- Gap Analysis
- Test Status
- Recommendations
- Items Requiring Spec Update

최종 사용자 보고에는 아래가 포함되어야 한다.

- verdict
- blocker 개수와 핵심 finding
- 테스트 상태
- spec update 필요 여부

## Error Handling

| 상황 | 대응 |
|------|------|
| `gh` 인증 실패 | 인증 필요 사실을 보고하고 중단 |
| patch draft 없음 | degraded mode로 진행 |
| PR 번호 미확정 | 자동 감지 시도, 실패 시 사용자 확인 |
| 테스트 환경 불명확 | `_sdd/env.md` 확인 후 미실행 사실을 기록 |
| diff가 너무 큼 | evidence를 lane별로 분리해 수집 후 통합 |

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

