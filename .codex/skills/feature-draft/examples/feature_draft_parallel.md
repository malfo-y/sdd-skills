# Feature Draft: 실시간 알림 및 작업 상태 추적

**Date**: 2026-03-09
**Author**: 개발팀
**Target Spec**: apify_ig.md
**Status**: Draft

---

# Part 1: Spec Patch Draft

> 이 패치는 `spec-update-todo` 입력으로 사용할 수 있습니다.

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
**Related Paths**: `src/services/notification_service.py`, `src/pipeline/`, `tests/`

**Description**:
다운로드 완료, 오류 발생, 배치 종료 시 외부 채널로 알림을 전송한다.

**Acceptance Criteria**:
- [ ] Slack 웹훅 알림 전송 가능
- [ ] Discord 웹훅 알림 전송 가능
- [ ] 알림 실패가 메인 파이프라인을 차단하지 않음

**Spec Impact**:
- Goal: 운영자가 작업 결과를 즉시 확인할 수 있다.
- Architecture/Flow: 배치 종료/실패 이벤트가 NotificationService로 전달된다.
- Usage/Change Paths: 알림 동작 변경 시 `PipelineHooks`와 `NotificationService`부터 확인한다.

**Risks / Invariants**:
- 알림 실패가 수집 성공/실패 상태를 왜곡하면 안 된다.

**Dependencies**:
- 기존 파이프라인 이벤트 훅 필요

## Improvements

### Improvement: 구조화된 로깅
**Priority**: Medium
**Target Section**: `_sdd/spec/apify_ig.md` > `Identified Issues & Improvements`
**Affected Components**: `shared_utils.py`, `NotificationService`

**Current State**:
기본 텍스트 로그 위주로 출력한다.

**Proposed**:
JSON 로그와 로그 레벨을 지원해 운영 관측성과 디버깅 시작점을 개선한다.

**Reason**:
알림 기능과 장애 분석 시 이벤트 단위 추적이 필요하다.

**Related Paths**:
- `src/shared_utils.py`
- `tests/test_logging_utils.py`

## Component Changes

### New Component: NotificationService
**Target Section**: `_sdd/spec/apify_ig.md` > `Component Details`
**Owned Paths**:
- `src/services/notification_service.py`
- `tests/services/test_notification_service.py`

**Responsibility**:
- 이벤트 기반 외부 알림 전송
- 채널별 메시지 포맷팅과 재시도 처리

**Overview**:
- 동작 개요: 파이프라인 훅이 전달한 이벤트를 채널별 메시지로 변환하고, Slack/Discord 웹훅 호출 결과를 성공/실패 상태로 정리한다.
- 설계 의도: 파이프라인 종료 상태와 알림 전달 상태를 분리해 운영 알림 실패가 본 작업 결과를 왜곡하지 않게 한다.

**Interfaces / Contracts**:
- Inputs: `event_type`, 메시지 데이터, 채널 설정
- Outputs: 전송 성공/실패 결과, 재시도 상태

**Change Recipes**:
- 새 채널 추가 시 `NotificationService`와 설정 로더를 먼저 본다.

### Update Component: PipelineHooks
**Target Section**: `_sdd/spec/apify_ig.md` > `Component Details`
**Change Type**: Enhancement

**Changes**:
- 배치 완료/오류 이벤트를 NotificationService로 전달
- 알림 실패가 파이프라인 종료 상태를 바꾸지 않도록 분리

**Overview Update**:
- 동작 개요: 배치 성공/실패/경고 이벤트를 한 곳에서 정규화해 NotificationService로 넘긴다.
- 설계 의도: 파이프라인 훅이 이벤트 방출만 담당하고, 채널별 전송 정책은 NotificationService에 위임한다.

**Risks / Invariants**:
- 파이프라인 성공 여부와 알림 성공 여부는 분리되어야 한다.

## Environment & Dependency Changes

### Change: 알림 웹훅 설정
**Target Section**: `_sdd/spec/apify_ig.md` > `Environment & Dependencies`
**Type**: Environment Variable

**Description**:
Slack/Discord 웹훅과 전역 알림 활성화 스위치를 추가한다.

**Impact**:
- 로컬 및 운영 환경의 설정 문서와 `.env.example` 갱신 필요

## Notes

### Context
대규모 배치 작업 결과를 수동으로 확인하는 운영 부담이 크다.

### Constraints
- 알림 실패가 수집 파이프라인을 중단시키면 안 된다.
- 웹훅 URL은 코드가 아닌 환경 변수에서 관리한다.

## Open Questions
- 이메일 알림을 이번 범위에 포함할지 후속 단계로 미룰지 미정이다.

---

# Part 2: Implementation Plan

## Overview

실시간 알림 서비스와 구조화된 로깅을 추가한다. 배치 종료/실패 이벤트가 NotificationService로 전달되고, 운영자는 Slack/Discord를 통해 상태를 즉시 확인할 수 있다. 파이프라인 훅은 이벤트 방출에 집중하고, 채널별 전송 정책과 실패 격리는 NotificationService가 담당한다.

## Scope

### In Scope
- NotificationService 구현
- Slack/Discord 웹훅 전송
- 메시지 포맷팅 및 재시도
- 구조화된 로깅
- 파이프라인 이벤트 훅 연결
- 단위/통합 테스트

### Out of Scope
- 이메일 알림
- 알림 이력 UI

## Components
1. **NotificationService**: 외부 알림 전송
2. **PipelineHooks**: 기존 파이프라인 이벤트 방출
3. **LoggingUtility**: 구조화된 로깅

## Implementation Phases

### Phase 1: Foundation
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 1 | 구조화된 로깅 유틸리티 추가 | P1 | - | LoggingUtility |
| 2 | NotificationService 기본 구조와 설정 로더 구현 | P0 | - | NotificationService |

### Phase 2: Core Integration
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 3 | Slack/Discord 전송 구현 | P0 | 2 | NotificationService |
| 4 | 파이프라인 이벤트 훅 연결 | P0 | 1, 2, 3 | PipelineHooks |

### Phase 3: Verification
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 5 | NotificationService 단위 테스트 | P1 | 3 | Test |
| 6 | 파이프라인 통합 테스트 및 환경 문서 반영 | P1 | 4, 5 | Test/Docs |

## Task Details

### Task 1: 구조화된 로깅 유틸리티 추가
**Component**: LoggingUtility
**Priority**: P1
**Type**: Feature

**Description**:
기존 텍스트 로그에 JSON 포맷과 로그 레벨 구성을 추가한다.

**Acceptance Criteria**:
- [ ] JSON 로그 출력 지원
- [ ] DEBUG/INFO/WARNING/ERROR 레벨 지원

**Target Files**:
- [M] `src/shared_utils.py` -- 로거 초기화 및 JSON 로그 유틸리티 추가
- [C] `tests/test_logging_utils.py` -- 로깅 유틸리티 단위 테스트

**Technical Notes**:
- 표준 `logging` 모듈을 우선 사용한다.

**Dependencies**: -

### Task 2: NotificationService 기본 구조와 설정 로더 구현
**Component**: NotificationService
**Priority**: P0
**Type**: Feature

**Description**:
웹훅 설정을 읽고 채널 활성화 상태를 판단하는 NotificationService 기본 구조를 구현한다.

**Acceptance Criteria**:
- [ ] Slack/Discord 웹훅 설정 로드
- [ ] 전역 알림 ON/OFF 지원
- [ ] 채널 미설정 시 안전하게 비활성화

**Target Files**:
- [C] `src/services/notification_service.py` -- NotificationService 클래스 추가
- [C] `tests/services/test_notification_config.py` -- 설정 로딩 테스트

**Technical Notes**:
- 환경 변수 로더는 기존 설정 패턴을 따른다.

**Dependencies**: -

## Parallel Execution Summary

| Phase | Total Tasks | Max Parallel | File Conflicts |
|-------|-------------|--------------|----------------|
| 1 | 2 | 2 | None |
| 2 | 2 | 1 | `src/services/notification_service.py` related sequencing |
| 3 | 2 | 2 | None |

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| 알림 실패가 파이프라인 실패로 오인됨 | 운영 혼선 | 상태 경로를 분리하고 로그 필드 명확화 |
| 설정 누락 | 런타임 혼선 | 기본 비활성화 + 명시적 로그 |

## Open Questions

- [ ] 이메일 알림을 같은 컴포넌트에 포함할지 분리할지 추후 결정 필요

## Model Recommendation

`gpt-5.3-codex` (`reasoning effort: high`)

---

## Next Steps

### Apply Spec Patch
- `spec-update-todo`를 실행해 Part 1을 `_sdd/spec/`에 반영

### Execute Implementation
- `implementation`을 실행해 Part 2를 구현 계획으로 사용

### Sync After Completion
- 구현 완료 후 `spec-update-done` 실행
