# Spec Update Input

**Date**: 2026-02-05
**Author**: 개발팀
**Target Spec**: apify_ig.md

---

## New Features

### Feature: 실시간 알림 시스템
**Priority**: Medium
**Category**: Enhancement
**Target Component**: shared_utils.py

**Description**:
다운로드 완료, 오류 발생, 배치 작업 완료 시 알림 전송.
Slack 웹훅을 통한 알림 지원, 추후 Discord, 이메일 확장 가능.

**Acceptance Criteria**:
- [ ] Slack 웹훅 URL 설정 가능
- [ ] 다운로드 완료 시 알림 전송
- [ ] 오류 발생 시 알림 전송 (오류 내용 포함)
- [ ] 알림 메시지 템플릿 커스터마이징
- [ ] 알림 on/off 설정

**Technical Notes**:
- requests 라이브러리로 웹훅 호출
- 비동기 전송으로 메인 프로세스 블로킹 방지
- 재시도 로직 포함 (3회)

**Dependencies**:
- 없음 (독립적으로 구현 가능)

---

### Feature: 프로필 비교 기능
**Priority**: Low
**Category**: Core Feature

**Description**:
두 시점의 프로필 데이터를 비교하여 변경 사항 확인.
팔로워 수 변화, 게시물 추가/삭제 등 추적.

**Acceptance Criteria**:
- [ ] 두 날짜의 프로필 데이터 비교
- [ ] 팔로워/팔로잉 수 변화 표시
- [ ] 새 게시물 목록 표시
- [ ] 비교 결과 리포트 생성

---

## Improvements

### Improvement: 로깅 구조화
**Priority**: High
**Current State**: print 문 기반 로깅, 일관성 없는 형식
**Proposed**: Python logging 모듈 사용, JSON 형식 지원
**Reason**:
- 로그 레벨별 필터링 가능
- 외부 모니터링 도구 연동 용이
- 디버깅 시 문제 추적 편의

---

### Improvement: 설정 파일 통합
**Priority**: Medium
**Current State**: 환경 변수와 하드코딩된 값 혼재
**Proposed**: config.yaml 또는 .env 파일로 모든 설정 통합
**Reason**:
- 설정 관리 일원화
- 환경별 설정 파일 분리 가능
- 설정 변경 시 코드 수정 불필요

---

## Bug Reports

### Bug: 대용량 배치 처리 시 메모리 증가
**Severity**: Medium
**Location**: ig_username_crawler.py

**Description**:
100개 이상의 사용자를 연속 처리할 때 메모리 사용량이 지속적으로 증가.
처리 완료 후에도 메모리가 해제되지 않음.

**Reproduction**:
1. 200개 사용자 목록 준비
2. 배치 모드로 순차 처리 실행
3. 시스템 모니터로 메모리 사용량 관찰
4. 처리 진행에 따라 메모리 증가 확인

**Expected Behavior**:
각 사용자 처리 완료 후 관련 데이터가 메모리에서 해제되어야 함.

**Workaround**:
배치를 50개 단위로 나누어 실행 후 프로세스 재시작

---

## Component Changes

### New Component: NotificationService
**Purpose**: 다양한 채널로 알림 전송
**Input**: 이벤트 타입, 메시지 데이터, 수신 설정
**Output**: 전송 결과 (성공/실패, 오류 메시지)

**Planned Methods**:
- `send_slack(message, webhook_url)` - Slack 알림 전송
- `send_discord(message, webhook_url)` - Discord 알림 전송
- `notify(event_type, data)` - 설정에 따라 적절한 채널로 알림

---

### Update Component: shared_utils.py
**Change Type**: Enhancement

**New Functions**:
- `setup_logger(name, level, format)` - 구조화된 로거 설정
- `get_config(key, default)` - 설정값 조회 유틸리티

---

## Configuration Changes

### New Config: SLACK_WEBHOOK_URL
**Type**: Environment Variable
**Required**: No
**Default**: None
**Description**: Slack 알림 웹훅 URL

### New Config: NOTIFICATION_ENABLED
**Type**: Environment Variable
**Required**: No
**Default**: false
**Description**: 알림 기능 활성화 여부

### New Config: LOG_LEVEL
**Type**: Environment Variable
**Required**: No
**Default**: INFO
**Valid Values**: DEBUG, INFO, WARNING, ERROR
**Description**: 로그 출력 레벨

---

## Notes

### Context
현재 프로젝트는 수동 실행 기반이며, 운영 환경에서의 모니터링이 어려움.
알림 시스템과 구조화된 로깅을 통해 운영 편의성 향상 목표.

### Constraints
- 외부 서비스 의존성 최소화 (Slack 웹훅은 옵션)
- 기존 코드 변경 최소화
- 하위 호환성 유지

### References
- Slack Incoming Webhooks: https://api.slack.com/messaging/webhooks
- Python logging 모듈: https://docs.python.org/3/library/logging.html
