# Feature Draft: 실시간 알림 시스템

**Date**: 2026-02-14
**Author**: 개발팀
**Target Spec**: apify_ig.md
**Status**: Draft

---

<!-- spec-update-todo-input-start -->
# Part 1: 스펙 패치 초안

> 이 패치는 스펙 문서의 해당 섹션에 copy-paste하거나,
> `spec-update-todo` 스킬의 입력으로 사용할 수 있습니다.

# Spec Update Input

**Date**: 2026-02-14
**Author**: 개발팀
**Target Spec**: apify_ig.md

## New Features

### Feature: 실시간 알림
**Priority**: Medium
**Category**: Enhancement
**Target Component**: notification_service.py (신규)
**Target Section**: `_sdd/spec/apify_ig.md` > `목표 > 주요 기능`

**Description**:
다운로드 완료, 오류 발생, 배치 처리 완료 등의 이벤트 발생 시 외부 서비스로 알림을 전송하는 기능.
Slack 웹훅과 Discord 웹훅을 우선 지원하고, 이메일 알림은 추후 확장.

**Acceptance Criteria**:
- [ ] Slack 웹훅으로 알림 전송 가능
- [ ] Discord 웹훅으로 알림 전송 가능
- [ ] 메시지 템플릿 커스터마이징 가능
- [ ] 알림 전송 실패 시 최대 3회 재시도
- [ ] 알림 ON/OFF 설정 가능

**Technical Notes**:
- httpx 또는 requests를 사용한 비동기 웹훅 호출
- 재시도 로직에 exponential backoff 적용
- 알림 실패가 메인 파이프라인을 차단하지 않도록 비동기 처리

**Dependencies**:
- 기존 다운로드 파이프라인의 이벤트 훅 포인트 필요

---

## Improvements

### Improvement: 로깅 구조화
**Priority**: Medium
**Target Section**: `_sdd/spec/apify_ig.md` > `개선 필요사항 > 개선 제안`
**Current State**: 기본 print 문으로 로그 출력
**Proposed**: 구조화된 로깅 (JSON 포맷) + 로그 레벨 지원
**Reason**: 모니터링 및 디버깅 용이, 알림 시스템과의 통합 필요

---

## Component Changes

### New Component: NotificationService
**Target Section**: `_sdd/spec/apify_ig.md` > `컴포넌트 상세`
**Purpose**: 이벤트 기반 외부 알림 전송 서비스
**Input**: 이벤트 타입 (str), 메시지 데이터 (dict), 수신자 설정 (config)
**Output**: 전송 결과 (성공/실패/재시도)

**Planned Methods**:
- `send_slack(message, webhook_url)` - Slack 웹훅 알림 전송
- `send_discord(message, webhook_url)` - Discord 웹훅 알림 전송
- `notify(event_type, data)` - 이벤트 기반 알림 라우팅
- `format_message(template, data)` - 메시지 템플릿 포맷팅

### Update Component: shared_utils.py
**Target Section**: `_sdd/spec/apify_ig.md` > `컴포넌트 상세 > shared_utils.py`
**Change Type**: Enhancement

**Changes**:
- `setup_logger(name, level, format)` 함수 추가 - 구조화된 로거 설정
- `log_to_json(event, data)` 함수 추가 - JSON 형식 로그 출력

---

## Configuration Changes

### New Config: NOTIFICATION_WEBHOOK_SLACK
**Target Section**: `_sdd/spec/apify_ig.md` > `설정`
**Type**: Environment Variable
**Required**: No
**Default**: None (미설정 시 Slack 알림 비활성화)
**Description**: Slack Incoming Webhook URL

### New Config: NOTIFICATION_WEBHOOK_DISCORD
**Target Section**: `_sdd/spec/apify_ig.md` > `설정`
**Type**: Environment Variable
**Required**: No
**Default**: None (미설정 시 Discord 알림 비활성화)
**Description**: Discord Webhook URL

### New Config: NOTIFICATION_ENABLED
**Target Section**: `_sdd/spec/apify_ig.md` > `설정`
**Type**: Environment Variable
**Required**: No
**Default**: true
**Description**: 알림 기능 전역 ON/OFF 스위치

---

## Notes

### Context
대규모 프로필 수집 작업 시 완료/실패 상태를 즉시 파악하기 위한 알림 필요.
현재는 작업 완료 후 수동으로 결과를 확인해야 함.

### Constraints
- 알림 전송 실패가 메인 파이프라인을 중단시키면 안 됨
- 웹훅 URL은 환경 변수로 관리 (코드에 하드코딩 금지)
- 알림 빈도 제한 고려 (분당 최대 호출 수)
<!-- spec-update-todo-input-end -->

---

# Part 2: 구현 계획

## 개요

실시간 알림 시스템을 구현합니다. NotificationService 컴포넌트를 신규 생성하고,
기존 파이프라인에 이벤트 훅을 추가하여 Slack/Discord로 알림을 전송합니다.
부수적으로 로깅 시스템을 구조화합니다.

## 범위

### In Scope
- NotificationService 컴포넌트 구현
- Slack/Discord 웹훅 알림 전송
- 메시지 템플릿 시스템
- 재시도 로직 (exponential backoff)
- 구조화된 로깅 유틸리티
- 환경 변수 기반 설정
- 단위/통합 테스트

### Out of Scope
- 이메일 알림 (추후 Phase)
- 알림 이력 저장/조회 UI
- 알림 스케줄링 (cron 기반)

## 컴포넌트

1. **NotificationService**: 이벤트 기반 알림 전송 서비스 (신규)
2. **LoggingUtility**: 구조화된 로깅 유틸리티 (shared_utils.py 확장)
3. **PipelineHooks**: 기존 파이프라인에 이벤트 훅 추가 (기존 코드 수정)

## 구현 단계

### Phase 1: 기반 설정

| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 1 | 구조화된 로깅 유틸리티 구현 | P1 | - | LoggingUtility |
| 2 | NotificationService 기본 구조 및 설정 로더 구현 | P0 | - | NotificationService |
| 3 | 메시지 템플릿 시스템 구현 | P1 | 2 | NotificationService |

### Phase 2: 핵심 기능

| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 4 | Slack 웹훅 전송 구현 | P0 | 2, 3 | NotificationService |
| 5 | Discord 웹훅 전송 구현 | P0 | 2, 3 | NotificationService |
| 6 | 재시도 로직 구현 (exponential backoff) | P1 | 4 | NotificationService |
| 7 | 기존 파이프라인에 이벤트 훅 추가 | P0 | 4, 5 | PipelineHooks |

### Phase 3: 테스트 및 마무리

| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 8 | NotificationService 단위 테스트 작성 | P1 | 4, 5, 6 | Test |
| 9 | 파이프라인 통합 테스트 작성 | P1 | 7 | Test |
| 10 | 환경 변수 설정 문서화 및 .env.example 업데이트 | P2 | 7 | Documentation |

## 태스크 상세

### Task 1: 구조화된 로깅 유틸리티 구현
**Component**: LoggingUtility
**Priority**: P1
**Type**: Feature

**설명**:
`shared_utils.py`에 구조화된 로깅 함수를 추가합니다. JSON 형식 로그 출력과 로그 레벨 설정을 지원합니다.

**Acceptance Criteria**:
- [ ] `setup_logger(name, level, format)` 함수 구현
- [ ] `log_to_json(event, data)` 함수 구현
- [ ] DEBUG/INFO/WARNING/ERROR 로그 레벨 지원
- [ ] 기존 print 문과 공존 가능 (점진적 마이그레이션)

**Target Files**:
- [M] `src/shared_utils.py` -- setup_logger, log_to_json 함수 추가
- [C] `tests/test_logging_utils.py` -- 로깅 유틸리티 단위 테스트

**Technical Notes**:
- Python 표준 `logging` 모듈 기반
- JSON 포맷터는 `json.dumps` 사용 (외부 의존성 최소화)

**Dependencies**: -

---

### Task 2: NotificationService 기본 구조 및 설정 로더 구현
**Component**: NotificationService
**Priority**: P0
**Type**: Feature

**설명**:
`notification_service.py` 파일을 생성하고, 환경 변수에서 웹훅 URL과 설정을 로드하는 기본 구조를 구현합니다.

**Acceptance Criteria**:
- [ ] `NotificationService` 클래스 생성
- [ ] 환경 변수에서 웹훅 URL 로드 (NOTIFICATION_WEBHOOK_SLACK, NOTIFICATION_WEBHOOK_DISCORD)
- [ ] NOTIFICATION_ENABLED 설정에 따른 전역 ON/OFF
- [ ] 웹훅 URL 미설정 시 해당 채널 자동 비활성화

**Target Files**:
- [C] `src/services/notification_service.py` -- NotificationService 클래스
- [C] `tests/test_notification_config.py` -- 설정 로딩 테스트

**Technical Notes**:
- `os.environ` 또는 `python-dotenv` 사용
- 싱글톤 패턴 또는 모듈 레벨 인스턴스

**Dependencies**: -

---

### Task 3: 메시지 템플릿 시스템 구현
**Component**: NotificationService
**Priority**: P1
**Type**: Feature

**설명**:
이벤트 유형별 메시지 템플릿을 정의하고, 데이터를 바인딩하여 포맷팅하는 시스템을 구현합니다.

**Acceptance Criteria**:
- [ ] `format_message(template, data)` 메서드 구현
- [ ] 기본 템플릿 정의: 다운로드 완료, 오류 발생, 배치 완료
- [ ] 사용자 커스텀 템플릿 지원 (설정 파일 또는 환경 변수)

**Target Files**:
- [M] `src/services/notification_service.py` -- format_message 메서드, 기본 템플릿 추가
- [C] `src/services/message_templates.py` -- 메시지 템플릿 정의
- [C] `tests/test_message_templates.py` -- 템플릿 포맷팅 테스트

**Technical Notes**:
- Python `str.format()` 또는 `string.Template` 사용
- 템플릿에 이모지/마크다운 지원 (Slack/Discord 호환)

**Dependencies**: 2

---

### Task 4: Slack 웹훅 전송 구현
**Component**: NotificationService
**Priority**: P0
**Type**: Feature

**설명**:
Slack Incoming Webhook API를 사용하여 알림 메시지를 전송하는 기능을 구현합니다.

**Acceptance Criteria**:
- [ ] `send_slack(message, webhook_url)` 메서드 구현
- [ ] Slack Block Kit 형식 메시지 지원
- [ ] HTTP 응답 코드에 따른 성공/실패 판별
- [ ] 전송 실패 시 에러 로깅

**Target Files**:
- [M] `src/services/notification_service.py` -- send_slack 메서드 추가
- [C] `tests/test_slack_sender.py` -- Slack 전송 테스트 (mock HTTP)

**Technical Notes**:
- `httpx` 또는 `requests` 사용
- 타임아웃: 10초
- 비동기 처리로 메인 파이프라인 차단 방지

**Dependencies**: 2, 3

---

### Task 5: Discord 웹훅 전송 구현
**Component**: NotificationService
**Priority**: P0
**Type**: Feature

**설명**:
Discord Webhook API를 사용하여 알림 메시지를 전송하는 기능을 구현합니다.

**Acceptance Criteria**:
- [ ] `send_discord(message, webhook_url)` 메서드 구현
- [ ] Discord Embed 형식 메시지 지원
- [ ] HTTP 응답 코드에 따른 성공/실패 판별

**Target Files**:
- [M] `src/services/notification_service.py` -- send_discord 메서드 추가
- [C] `tests/test_discord_sender.py` -- Discord 전송 테스트 (mock HTTP)

**Technical Notes**:
- Discord webhook은 `content` 또는 `embeds` 필드 사용
- Slack과 공통 인터페이스로 추상화 가능

**Dependencies**: 2, 3

---

### Task 6: 재시도 로직 구현
**Component**: NotificationService
**Priority**: P1
**Type**: Feature

**설명**:
알림 전송 실패 시 exponential backoff 방식으로 재시도하는 로직을 구현합니다.

**Acceptance Criteria**:
- [ ] 최대 3회 재시도
- [ ] Exponential backoff (1초, 2초, 4초)
- [ ] 재시도 횟수 및 결과 로깅
- [ ] 최종 실패 시 에러 로그만 남기고 파이프라인 계속 진행

**Target Files**:
- [C] `src/services/retry_handler.py` -- 재시도 로직 모듈
- [C] `tests/test_retry_handler.py` -- 재시도 로직 테스트

**Technical Notes**:
- `tenacity` 라이브러리 또는 직접 구현
- 재시도 가능한 HTTP 상태 코드: 429, 500, 502, 503, 504

**Dependencies**: 4

---

### Task 7: 기존 파이프라인에 이벤트 훅 추가
**Component**: PipelineHooks
**Priority**: P0
**Type**: Feature

**설명**:
기존 다운로드/처리 파이프라인의 주요 지점에 알림 이벤트 훅을 추가합니다.

**Acceptance Criteria**:
- [ ] 다운로드 완료 시 알림 훅
- [ ] 오류 발생 시 알림 훅
- [ ] 배치 처리 완료 시 요약 알림 훅
- [ ] 알림 비활성화 시 훅이 no-op으로 동작

**Target Files**:
- [M] `src/pipeline/downloader.py` -- 다운로드 완료/오류 훅 포인트 추가
- [M] `src/pipeline/batch_processor.py` -- 배치 완료 훅 포인트 추가
- [C] `tests/test_pipeline_hooks.py` -- 훅 동작 테스트

**Technical Notes**:
- `notify(event_type, data)` 호출로 통일
- 기존 코드 최소 변경 (훅 포인트 삽입만)

**Dependencies**: 4, 5

---

### Task 8: NotificationService 단위 테스트
**Component**: Test
**Priority**: P1
**Type**: Test

**설명**:
NotificationService의 각 메서드에 대한 단위 테스트를 작성합니다.

**Acceptance Criteria**:
- [ ] 메시지 포맷팅 테스트
- [ ] Slack 전송 테스트 (mock HTTP)
- [ ] Discord 전송 테스트 (mock HTTP)
- [ ] 재시도 로직 테스트
- [ ] 설정 비활성화 시 동작 테스트

**Target Files**:
- [C] `tests/test_notification_integration.py` -- 통합 단위 테스트
- [M] `tests/conftest.py` -- 공통 fixture 추가

**Technical Notes**:
- `pytest` + `pytest-mock` 사용
- HTTP 호출은 mock으로 대체 (`responses` 또는 `httpx.MockTransport`)

**Dependencies**: 4, 5, 6

---

### Task 9: 파이프라인 통합 테스트
**Component**: Test
**Priority**: P1
**Type**: Test

**설명**:
파이프라인에 알림 훅이 올바르게 동작하는지 통합 테스트를 작성합니다.

**Acceptance Criteria**:
- [ ] 파이프라인 실행 → 알림 전송 확인
- [ ] 알림 실패 시 파이프라인 정상 완료 확인
- [ ] 알림 비활성화 시 전송 시도 없음 확인

**Target Files**:
- [C] `tests/test_pipeline_notification_integration.py` -- 파이프라인-알림 통합 테스트

**Technical Notes**:
- 실제 웹훅 호출 없이 mock으로 검증

**Dependencies**: 7

---

### Task 10: 환경 변수 문서화
**Component**: Documentation
**Priority**: P2
**Type**: Documentation

**설명**:
새로 추가된 환경 변수를 `.env.example` 및 README에 문서화합니다.

**Acceptance Criteria**:
- [ ] `.env.example`에 새 환경 변수 추가 (주석 포함)
- [ ] README 또는 설정 가이드에 알림 설정 방법 기술

**Target Files**:
- [M] `.env.example` -- 알림 관련 환경 변수 추가
- [M] `README.md` -- 알림 설정 섹션 추가

**Dependencies**: 7

---

## 병렬 실행 요약

| Phase | Total Tasks | Max Parallel | Sequential (conflicts) |
|-------|-------------|--------------|----------------|
| 1 | 3 | 2 (Task 1, 2) | `notification_service.py` (Task 2, 3) → Task 3은 Task 2 후 순차 |
| 2 | 4 | 2 (Task 4, 5) | `notification_service.py` (Task 4, 5) → 별도 메서드이나 같은 파일이므로 순차 권장. Task 6은 Task 4 후. |
| 3 | 3 | 2 (Task 8, 9) | `conftest.py` 잠재적 충돌 → Task 8 먼저 실행 권장. Task 10은 독립. |

### Phase 1 병렬 그룹:
- **Group 1**: Task 1 + Task 2 (서로 다른 파일, 동시 실행 가능)
- **Group 2**: Task 3 (Task 2에 의존 + notification_service.py 공유)

### Phase 2 병렬 그룹:
- **Group 1**: Task 4 + Task 5 실행 시 notification_service.py 충돌 → 순차 실행
  - 대안: send_slack, send_discord를 별도 파일로 분리하면 병렬 가능
- **Group 2**: Task 6 (Task 4 의존)
- **Group 3**: Task 7 (Task 4, 5 의존)

### Phase 3 병렬 그룹:
- **Group 1**: Task 9 + Task 10 (서로 다른 파일)
- **Group 2**: Task 8 (conftest.py 수정 필요 → 다른 테스트 task와 충돌 가능)

## 위험 요소 및 대응

| 위험 | 영향 | 대응 |
|------|------|------|
| 웹훅 API 레이트 리밋 | 대량 알림 시 전송 실패 | 알림 병합/배치 전송, 빈도 제한 설정 |
| 알림 전송이 파이프라인 차단 | 전체 처리 속도 저하 | 비동기 처리 + 타임아웃으로 격리 |
| 웹훅 URL 노출 | 보안 위험 | 환경 변수 관리, .gitignore에 .env 추가 |
| 병렬 실행 시 notification_service.py 충돌 | 코드 충돌/덮어쓰기 | Task 4, 5를 순차 실행 또는 메서드를 별도 파일로 분리 |

## 미해결 질문

- [ ] 알림 메시지에 포함할 데이터 범위는? (파일 수, 소요 시간, 에러 목록 등)
- [ ] 배치 처리 시 개별 알림 vs 요약 알림?
- [ ] 향후 이메일 알림 추가 시 SMTP 직접 연결 vs 외부 서비스 (SendGrid 등)?

## 모델 추천

이 구현은 **중간 복잡도** (10개 태스크, 3 Phase)입니다.
- **추천 모델**: `sonnet` (표준 구현 작업에 적합)
- 복잡한 비동기 처리 설계가 필요할 경우 `opus` 고려

---

## 다음 단계

### 스펙 패치 적용 (택 1)
- **방법 A (자동)**: `spec-update-todo` 실행 → 이 파일의 Part 1을 입력으로 사용
- **방법 B (수동)**: Part 1의 각 항목을 Target Section에 직접 copy-paste

### 구현 실행
- **병렬**: `implementation` 스킬 실행 → Part 2를 구현 계획으로 사용
- **순차**: 태스크를 순차적으로 실행 (Target Files 무시됨)

### 모델 추천
- 구현: `sonnet` (표준), 아키텍처 결정 필요 시 `opus`
