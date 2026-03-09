# User Input File Format Guide

Accepted input format for `spec-update-todo`.

This format also matches Part 1 output from `feature-draft`.

## File Location

```text
_sdd/
└── spec/
    ├── main.md or <project>.md
    ├── user_spec.md
    ├── user_draft.md
    ├── _processed_user_spec.md
    └── _processed_user_draft.md
```

## Basic Structure

~~~markdown
# Spec Update Input

**Date**: YYYY-MM-DD
**Author**: [Name or "User"]
**Target Spec**: [main spec filename]
**Spec Update Classification**: MUST update | NO update | CONSIDER

## New Features
[entries...]

## Improvements
[entries...]

## Bug Reports
[entries...]

## Component Changes
[entries...]

## Environment & Dependency Changes
[entries...]

## Notes
[entries...]

## Open Questions
[entries...]
~~~

## Classification Guide

- `MUST update`: 기능, 경계, 흐름, 계약, 환경 요구사항, 변경 시작점이 바뀌는 경우
- `NO update`: 테스트만 변경, 주석만 변경, 외부 동작과 탐색 지점이 그대로인 내부 리팩터링
- `CONSIDER`: 성능 튜닝, 소규모 의존성 변경, 탐색 영향이 애매한 내부 재구성

If the correct value is `NO update`, the input may omit all change sections and keep only `Notes` plus `Open Questions`.

## Section Formats

### New Features

~~~markdown
## New Features

### Feature: 배치 처리 지원
**Priority**: High
**Target Section**: `_sdd/spec/apify_ig.md` > `Goal > Key Features`
**Affected Components**: `BatchRunner`, `QueueWorker`
**Related Paths**: `src/batch/`, `tests/batch/`

**Description**:
여러 사용자를 한 번에 처리하는 배치 모드를 추가한다.

**Acceptance Criteria**:
- [ ] 사용자 목록 입력 가능
- [ ] 진행 상태 확인 가능

**Spec Impact**:
- Goal: 대량 작업 지원
- Architecture/Flow: 큐 기반 처리 흐름 추가
- Usage/Change Paths: 배치 파이프라인 수정 시작점 명시

**Risks / Invariants**:
- 기존 단일 사용자 흐름과 결과 포맷 호환 유지
~~~

### Improvements

~~~markdown
## Improvements

### Improvement: 다운로드 속도 최적화
**Priority**: High
**Target Section**: `_sdd/spec/apify_ig.md` > `Identified Issues & Improvements`
**Affected Components**: `Downloader`

**Current State**:
동시 2개 다운로드

**Proposed**:
동시 10개 다운로드 + 연결 풀링

**Reason**:
대용량 처리 시간 단축
~~~

### Bug Reports

~~~markdown
## Bug Reports

### Bug: 유니코드 파일명 오류
**Severity**: High
**Target Section**: `_sdd/spec/apify_ig.md` > `Identified Issues & Improvements`
**Affected Components**: `ImageDownloader`
**Location**: `ig_post_image_downloader.py:145`

**Description**:
이모지가 포함된 파일명에서 오류가 발생한다.

**Expected Behavior**:
유니코드 문자를 안전하게 처리한다.
~~~

### Component Changes

~~~markdown
## Component Changes

### New Component: NotificationService
**Target Section**: `_sdd/spec/apify_ig.md` > `Component Details`
**Owned Paths**:
- `src/services/notification_service.py`
- `tests/services/test_notification_service.py`

**Responsibility**:
- 알림 전송
- 메시지 포맷팅

**Interfaces / Contracts**:
- Inputs: 이벤트 타입, 메시지 데이터
- Outputs: 전송 결과
~~~

### Environment & Dependency Changes

~~~markdown
## Environment & Dependency Changes

### Change: NOTIFICATION_WEBHOOK
**Target Section**: `_sdd/spec/apify_ig.md` > `Environment & Dependencies`
**Type**: Environment Variable

**Description**:
Slack/Discord 웹훅 URL 설정 추가
~~~

### Notes / Open Questions

~~~markdown
## Notes

### Context
[context]

### Constraints
[constraints]

### Decision-Log Candidates
- [if any]

### No Spec Change Reason
[only when classification is `NO update`]

## Open Questions
- 이메일 알림 범위 포함 여부 미정
~~~
