# User Input File Format Guide

Detailed specification for spec update input files.

---

## File Location

```
_sdd/
└── spec/
    ├── apify_ig.md              # Main spec document
    ├── user_spec.md             # User-written input (to be processed)
    ├── user_draft.md            # 사용자 작성 초안 (to be processed)
    ├── _processed_user_spec.md  # Processed user_spec (archived)
    └── _processed_user_draft.md # Processed user_draft (archived)
```

## Input File Types

| File | Source | Description |
|------|--------|-------------|
| `user_spec.md` | 사용자 직접 작성 | User-written specification input |
| `user_draft.md` | 사용자 작성 | 사용자 작성 초안 (draft) |

Both files use the same "Spec Update Input" format.

---

## Basic Structure

```markdown
# Spec Update Input

**Date**: YYYY-MM-DD
**Author**: [Name or "User"]
**Target Spec**: [spec filename, e.g., apify_ig.md]

## New Features

[Feature entries...]

## Improvements

[Improvement entries...]

## Bug Reports

[Bug entries...]

## Component Changes

[Component entries...]

## Configuration Changes

[Config entries...]

## Notes

[Additional context...]
```

---

## Section Formats

### New Features Section

Full format with all fields:

```markdown
## New Features

### Feature: 배치 처리 지원
**Priority**: High
**Category**: Core Feature
**Target Component**: ig_username_crawler.py

**Description**:
여러 사용자의 데이터를 한 번에 처리할 수 있는 배치 모드 추가.
큐 기반으로 작업을 관리하고 진행률을 추적.

**Acceptance Criteria**:
- [ ] 사용자 목록을 파일로 입력받을 수 있음
- [ ] 각 사용자별 진행 상태 표시
- [ ] 실패한 작업 자동 재시도
- [ ] 완료 후 요약 리포트 생성

**Technical Notes**:
- asyncio 또는 multiprocessing 고려
- 메모리 사용량 모니터링 필요

**Dependencies**:
- 기존 single-user 파이프라인 완료 필요

---

### Feature: 실시간 알림
**Priority**: Medium
**Category**: Enhancement

**Description**:
다운로드 완료 또는 오류 발생 시 알림 전송.

**Acceptance Criteria**:
- [ ] Slack 웹훅 지원
- [ ] Discord 웹훅 지원
- [ ] 이메일 알림 (선택적)
```

Minimal format (required fields only):

```markdown
### Feature: 캐싱 레이어
**Priority**: Low

**Description**:
자주 조회하는 프로필 데이터 캐싱으로 API 호출 최소화.
```

### Improvements Section

```markdown
## Improvements

### Improvement: 다운로드 속도 최적화
**Priority**: High
**Current State**: 동시 2개 다운로드
**Proposed**: 동시 10개 다운로드 + 연결 풀링
**Reason**: 대용량 처리 시 시간 단축

---

### Improvement: 로깅 강화
**Priority**: Medium
**Current State**: 기본 print 문
**Proposed**: 구조화된 로깅 (JSON 포맷)
**Reason**: 모니터링 및 디버깅 용이
```

List format (simpler):

```markdown
## Improvements

- **높음**: 다운로드 병렬화 10개로 증가
- **중간**: 진행률 바 추가
- **낮음**: 설정 파일 YAML 지원
```

### Bug Reports Section

```markdown
## Bug Reports

### Bug: 유니코드 파일명 오류
**Severity**: High
**Location**: ig_post_image_downloader.py:145
**Reproduction**:
1. 한글 캡션이 포함된 게시물 다운로드
2. 파일명에 이모지 포함 시
3. FileNotFoundError 발생

**Expected Behavior**:
유니코드 문자를 안전하게 처리하여 저장

**Workaround**:
현재 수동으로 파일명 변경 필요

---

### Bug: 메모리 누수
**Severity**: Medium
**Location**: ig_image_organizer.py
**Description**: 대용량 처리 시 메모리 지속 증가
```

### Component Changes Section

```markdown
## Component Changes

### New Component: NotificationService
**Purpose**: 작업 완료/실패 알림 전송
**Input**: 이벤트 타입, 메시지, 수신자 설정
**Output**: 알림 전송 결과

**Planned Methods**:
- `send_slack(message, webhook_url)`
- `send_discord(message, webhook_url)`
- `send_email(message, recipients)`

---

### Update Component: shared_utils.py
**Change Type**: Enhancement
**Description**: 로깅 유틸리티 추가

**New Functions**:
- `setup_logger(name, level, format)`
- `log_to_json(event, data)`
```

### Configuration Changes Section

```markdown
## Configuration Changes

### New Config: NOTIFICATION_WEBHOOK
**Type**: Environment Variable
**Required**: No
**Default**: None
**Description**: Slack/Discord 웹훅 URL

### New Config: MAX_WORKERS
**Type**: Config File
**Required**: No
**Default**: 2
**Valid Range**: 1-20
**Description**: 동시 다운로드 스레드 수
```

### Notes Section

```markdown
## Notes

### Context
이 업데이트는 대규모 인플루언서 분석 프로젝트를 위한 것.
수천 개의 프로필을 효율적으로 처리해야 함.

### Constraints
- API 레이트 리밋 고려 필요
- 스토리지 비용 최소화
- 한국 시간대 기준 스케줄링

### References
- 유사 프로젝트: https://github.com/example/similar
- API 문서: https://apify.com/docs

### Timeline
- Phase 1 (2주): 배치 처리 기본 구현
- Phase 2 (1주): 알림 시스템
- Phase 3 (1주): 최적화 및 테스트
```

---

## Priority Levels

| Level | Korean | English | Description |
|-------|--------|---------|-------------|
| P0 | 긴급 | Critical | 즉시 처리 필요, 시스템 장애 |
| P1 | 높음 | High | 다음 릴리스에 포함 |
| P2 | 중간 | Medium | 계획된 개선 사항 |
| P3 | 낮음 | Low | 있으면 좋은 기능 |

---

## Category Tags

| Category | Description | Maps to Spec Section |
|----------|-------------|---------------------|
| Core Feature | 핵심 기능 | 목표 > 주요 기능 |
| Enhancement | 기존 기능 개선 | 개선 필요사항 |
| Bug Fix | 버그 수정 | 발견된 이슈 |
| Performance | 성능 개선 | 개선 필요사항 |
| Security | 보안 관련 | 보안 고려사항 |
| Documentation | 문서 개선 | 해당 섹션 |
| Testing | 테스트 추가 | 테스트 섹션 |
| Infrastructure | 인프라/환경 | 환경 및 의존성 |

---

## Validation Rules

### Required Fields

**For Features:**
- Feature name (in header)
- Priority
- Description

**For Bugs:**
- Bug name (in header)
- Severity
- Description or reproduction steps

**For Improvements:**
- Description
- Priority (in description or separate field)

### Optional but Recommended

- Acceptance criteria
- Technical notes
- Dependencies
- Target component/file

---

## Example Complete File

```markdown
# Spec Update Input

**Date**: 2026-02-04
**Author**: 개발팀
**Target Spec**: apify_ig.md

## New Features

### Feature: 스케줄러 통합
**Priority**: High
**Category**: Core Feature

**Description**:
정해진 시간에 자동으로 프로필 데이터 수집 실행.
cron 표현식 또는 간격 기반 스케줄링 지원.

**Acceptance Criteria**:
- [ ] cron 표현식으로 스케줄 설정 가능
- [ ] 간격 기반 스케줄 (매 N시간)
- [ ] 스케줄 상태 확인 명령어
- [ ] 실행 히스토리 조회

---

### Feature: 데이터 내보내기 형식 확장
**Priority**: Medium
**Category**: Enhancement

**Description**:
NDJSON 외에 CSV, Parquet 형식 지원 추가.

**Acceptance Criteria**:
- [ ] CSV 내보내기
- [ ] Parquet 내보내기
- [ ] 형식별 필드 매핑 설정

## Improvements

- **높음**: 프록시 풀 관리 자동화
- **중간**: 실패 작업 대시보드
- **낮음**: CLI 자동완성 지원

## Bug Reports

### Bug: 타임아웃 후 재시도 실패
**Severity**: High
**Location**: ig_username_crawler.py:234

**Description**:
Apify Actor 타임아웃 후 재시도 시 세션이 복구되지 않음.

## Notes

### Context
다음 분기 목표: 일일 10,000 프로필 처리 용량 확보

### Constraints
- 현재 인프라 비용 $500/월 이내 유지
- Apify 요금제 한도 고려
```

---

## After Processing

When processed, files are renamed and metadata is added:

| Before | After |
|--------|-------|
| `_sdd/spec/user_spec.md` | `_sdd/spec/_processed_user_spec.md` |
| `_sdd/spec/user_draft.md` | `_sdd/spec/_processed_user_draft.md` |

Added metadata:
```markdown
<!--
Processing Metadata
==================
Processed: 2026-02-04 14:30:00
Applied to: apify_ig.md
Version: 1.0.0 → 1.0.1
Processor: spec-update-todo skill

Applied Changes:
- Feature: 스케줄러 통합 → 목표 > 주요 기능
- Feature: 데이터 내보내기 형식 확장 → 목표 > 주요 기능
- Improvement: 프록시 풀 관리 → 개선 제안
- Improvement: 실패 작업 대시보드 → 개선 제안
- Improvement: CLI 자동완성 → 개선 제안
- Bug: 타임아웃 후 재시도 실패 → 발견된 이슈
-->

# Spec Update Input
...
```
