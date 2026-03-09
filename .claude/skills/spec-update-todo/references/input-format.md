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

## Classification Guide (SDD §8)

입력 항목을 편집 전에 아래 기준으로 분류한다.

### MUST update

스펙 갱신이 **반드시** 필요한 변경:

| 변경 유형 | 예시 |
|----------|------|
| 사용자 가시 기능/범위 변경 | 새 기능 추가, 기존 기능 동작 변경 |
| 컴포넌트 추가/삭제/이름 변경 | 새 서비스 모듈, 기존 모듈 제거 |
| 외부 계약 변경 | API 엔드포인트, 이벤트 스키마 변경 |
| 아키텍처 구조 변경 | 디렉토리 개편, 새 외부 연동 |
| 런타임 흐름 변경 | 동기→비동기, 새 큐/워커 |
| 환경/의존성 변경 | 새 환경변수, DB 마이그레이션, 주요 라이브러리 교체 |
| 불변 조건 변경 | 상태 전이 규칙, 유효성 검증 조건 |
| 탐색 지점 변경 | 새 변경/디버그 진입점, 소유 경로 이동 |

### NO update

스펙 갱신이 **불필요한** 변경:

| 변경 유형 | 예시 |
|----------|------|
| 내부 구현 리팩토링 | 함수 내부 로직 개선, 변수명 변경 |
| 버그 수정 (계약 불변) | 기존 계약대로 동작하지 않던 것을 수정 |
| 테스트 추가 | 기존 기능에 대한 테스트 보강 |
| 코드 스타일/포맷팅 | lint 수정, import 정리 |
| 주석만 변경 | 코드 주석 추가/수정 |

### CONSIDER

**판단이 필요한** 변경:

| 변경 유형 | 갱신 판단 기준 |
|----------|--------------|
| 새 내부 유틸/헬퍼 추가 | 다른 컴포넌트에서 공유하면 갱신 |
| 에러 핸들링 정책 변경 | 외부로 노출되는 에러 형태가 바뀌면 갱신 |
| 설정값 변경 | 동작 방식이 달라지면 갱신 |
| 의존 라이브러리 업데이트 | 메이저 버전 변경이면 갱신 |
| 성능 최적화 | 외부 인터페이스 불변이면 NO, 동작이 바뀌면 MUST |
| 내부 재구성 | 탐색 영향이 있으면 갱신 |

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
