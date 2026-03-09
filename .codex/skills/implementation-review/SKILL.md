---
name: implementation-review
description: Use this skill to review implementation progress against the plan, verify acceptance criteria, identify issues, and determine next steps. Triggered by "review implementation", "check progress", "verify implementation", "what's done", "implementation status", or "audit the code".
version: 1.3.0
---

# Implementation Review

구현 계획 대비 현재 구현 상태를 검증하고, 다음 작업과 필요한 스펙 동기화 포인트를 정리한다.

이 스킬은 구현 리뷰를 하되, 결과를 탐색형 스펙과 연결해야 한다. 즉 "무엇이 구현되었는가"뿐 아니라 "어떤 스펙 섹션이 후속 업데이트 대상인가", "컴포넌트가 어떻게 동작하고 왜 그렇게 구성됐는지 설명이 달라졌는가"까지 판단한다.

## Hard Rules

1. `_sdd/spec/` 아래 스펙은 직접 수정하지 않는다.
2. 스펙 변경이 필요하면 리뷰 리포트의 `Spec Sync Follow-ups`에만 기록한다.
3. acceptance criteria 검증은 가능한 한 코드 근거와 테스트 근거로 연결한다.
4. 로컬 실행이 필요하면 먼저 `_sdd/env.md`를 확인한다.
5. 불확실한 항목은 `Open Questions`에 남긴다.
6. 각 spec sync follow-up은 `MUST update / CONSIDER / NO update`로 분류한다.
7. 기본 후속 액션은 `spec-update-done`이며, plan/scope 재정의가 필요할 때만 `spec-update-todo`를 권장한다.

## Inputs

- `_sdd/implementation/IMPLEMENTATION_PLAN.md`
- `_sdd/implementation/IMPLEMENTATION_PROGRESS*.md`
- `_sdd/implementation/IMPLEMENTATION_REVIEW.md` (있으면 참고)
- 현재 코드 상태
- 현재 스펙: `_sdd/spec/main.md` 또는 `_sdd/spec/<project>.md`
- 링크된 컴포넌트 스펙
- `_sdd/env.md`

## Review Focus

### 1. Plan Progress

- 어떤 task가 complete / partial / missing 인가
- 어떤 acceptance criteria가 met / not met / untested 인가

### 2. Quality and Risk

- blocker가 있는가
- 테스트/에러 처리/보안/성능 리스크가 있는가

### 3. Spec Sync Follow-up

구현 결과가 아래 섹션 업데이트를 요구하는지 본다.

- `Goal`
- `Architecture Overview > Runtime Map`
- `Component Details > Component Index`
- `Component Details > Overview`
- `Usage Examples > Common Change Paths`
- `Environment & Dependencies`
- `Open Questions`
- `DECISION_LOG.md` proposal

## Process

### Step 1: Load plan and review scope

1. 구현 계획 식별
2. phase 파일이 여러 개면 최신 phase 우선
3. 현재 검토 범위를 명시
4. 스펙 entry point도 함께 식별

### Step 2: Verify implementation

각 task에 대해 아래를 정리한다.

- 기대 산출물
- 실제 구현 위치
- 테스트 위치와 상태
- 상태: `COMPLETE` / `PARTIAL` / `MISSING`

### Step 3: Check acceptance criteria

각 criterion에 대해 아래를 남긴다.

- Evidence: `file:line`
- Test
- Status: `MET` / `NOT MET` / `UNTESTED`
- Notes

### Step 4: Classify issues

세 가지로 나눈다.

- `Critical`
- `Quality`
- `Improvement`

### Step 5: Determine spec sync follow-ups

구현 결과를 보고 아래를 묻는다.

- 새 기능이 `Goal`에 반영되어야 하는가
- 새 흐름과 사용자/운영자 관점 설명이 `Runtime Map`에 반영되어야 하는가
- 새 컴포넌트/경로가 `Component Index`에 반영되어야 하는가
- 컴포넌트 동작 개요나 설계 의도가 `Component Details > Overview`에 반영되어야 하는가
- 새 운영/디버깅 시작점이 `Common Change Paths`에 반영되어야 하는가
- 문서로 아직 확정하지 못한 항목이 `Open Questions`에 남아야 하는가

각 follow-up은 아래로 분류한다.

- `MUST update`: 구현 완료 후 문서 sync 없이는 탐색성, 계약 이해, 또는 why-context 이해가 깨짐
- `CONSIDER`: 있으면 좋은 보강이나 blocker는 아님
- `NO update`: 내부 구현 차이만 있고 문서 수준 변화 없음

### Step 6: Write review report

리포트에는 아래가 있어야 한다.

1. Progress Overview
2. Acceptance Criteria Assessment
3. Issues Found
4. Test Status
5. Spec Sync Follow-ups
6. Recommended Spec Action
7. Recommended Next Steps
8. Open Questions

## References

- 체크리스트: [`references/review-checklist.md`](references/review-checklist.md)
- 예시: [`examples/sample-review.md`](examples/sample-review.md)
