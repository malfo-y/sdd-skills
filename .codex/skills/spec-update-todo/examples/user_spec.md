# Spec Update Input

**Date**: 2026-03-09
**Author**: 개발팀
**Target Spec**: apify_ig.md
**Spec Update Classification**: MUST update

## New Features

### Feature: 실시간 알림
**Priority**: Medium
**Target Section**: `_sdd/spec/apify_ig.md` > `Goal > Key Features`
**Affected Components**: `NotificationService`, `PipelineHooks`
**Related Paths**: `src/services/notification_service.py`, `src/pipeline/`

**Description**:
배치 완료, 실패, 중요 경고를 외부 알림 채널로 전송한다.

**Acceptance Criteria**:
- [ ] Slack 웹훅 알림
- [ ] Discord 웹훅 알림
- [ ] 알림 실패가 파이프라인을 중단시키지 않음

**Spec Impact**:
- Goal: 운영자가 결과를 즉시 확인할 수 있음
- Architecture/Flow: 이벤트 훅 -> NotificationService 흐름 추가
- Usage/Change Paths: 알림 동작 변경 시작점 명시

**Risks / Invariants**:
- 파이프라인 상태와 알림 전송 상태는 분리되어야 함

## Improvements

### Improvement: 구조화된 로깅
**Priority**: Medium
**Target Section**: `_sdd/spec/apify_ig.md` > `Identified Issues & Improvements`
**Affected Components**: `shared_utils.py`

**Current State**:
기본 텍스트 로그 위주

**Proposed**:
JSON 로그 + 로그 레벨 지원

**Reason**:
운영 추적성과 디버깅 시작점 개선

## Component Changes

### New Component: NotificationService
**Target Section**: `_sdd/spec/notification.md` > `Component Details`
**Owned Paths**:
- `src/services/notification_service.py`
- `tests/services/test_notification_service.py`

**Responsibility**:
- 외부 알림 전송
- 메시지 템플릿 포맷팅

**Interfaces / Contracts**:
- Inputs: 이벤트 타입, 메시지 데이터
- Outputs: 전송 성공/실패 결과

## Environment & Dependency Changes

### Change: NOTIFICATION_WEBHOOK
**Target Section**: `_sdd/spec/apify_ig.md` > `Environment & Dependencies`
**Type**: Environment Variable

**Description**:
Slack/Discord 웹훅 URL 환경 변수 추가

## Notes

### Context
배치 작업이 길어 수동 확인 비용이 크다.

### Constraints
- 알림 실패는 메인 파이프라인 성공 여부를 바꾸면 안 된다.

### Decision-Log Candidates
- 알림 실패와 메인 파이프라인 상태를 분리하는 정책은 이후에도 유지해야 한다.

## Open Questions

- 이메일 알림을 같은 컴포넌트에 포함할지 별도 후속으로 둘지 미정
