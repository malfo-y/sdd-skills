# Spec Update Input

**Date**: 2026-02-04
**Author**: 개발팀
**Target Spec**: apify_ig.md

---

## New Features

### Feature: 스케줄러 통합
**Priority**: High
**Category**: Core Feature
**Target Component**: ig_username_crawler.py

**Description**:
정해진 시간에 자동으로 프로필 데이터 수집 실행.
cron 표현식 또는 간격 기반 스케줄링 지원.

**Acceptance Criteria**:
- [ ] cron 표현식으로 스케줄 설정 가능
- [ ] 간격 기반 스케줄 (매 N시간)
- [ ] 스케줄 상태 확인 명령어
- [ ] 실행 히스토리 조회

**Technical Notes**:
- APScheduler 라이브러리 사용 고려
- 상태 저장을 위한 SQLite 또는 Redis

**Dependencies**:
- 현재 파이프라인 안정화 완료 필요

---

### Feature: 데이터 내보내기 형식 확장
**Priority**: Medium
**Category**: Enhancement

**Description**:
NDJSON 외에 CSV, Parquet 형식 지원 추가.
데이터 분석 도구와의 호환성 향상.

**Acceptance Criteria**:
- [ ] CSV 내보내기 (`--format csv`)
- [ ] Parquet 내보내기 (`--format parquet`)
- [ ] 형식별 필드 매핑 설정 가능
- [ ] 대용량 파일 스트리밍 처리

---

### Feature: 웹 대시보드
**Priority**: Low
**Category**: UI/UX

**Description**:
작업 상태 모니터링을 위한 간단한 웹 인터페이스.

**Acceptance Criteria**:
- [ ] 현재 실행 중인 작업 표시
- [ ] 완료된 작업 히스토리
- [ ] 다운로드 통계 차트

---

## Improvements

### Improvement: 다운로드 병렬화 강화
**Priority**: High
**Current State**: 동시 2개 다운로드, 고정 worker 수
**Proposed**: 동시 10개 다운로드, 동적 조절
**Reason**: 대용량 처리 시 시간 단축 (예상 5배 향상)

---

### Improvement: 연결 풀링
**Priority**: Medium
**Current State**: 요청마다 새 연결
**Proposed**: requests.Session 기반 연결 재사용
**Reason**: 오버헤드 감소, 안정성 향상

---

### Improvement: CLI 자동완성
**Priority**: Low
**Current State**: 수동 명령어 입력
**Proposed**: bash/zsh 자동완성 스크립트
**Reason**: 사용자 편의성

---

## Bug Reports

### Bug: 타임아웃 후 재시도 실패
**Severity**: High
**Location**: ig_username_crawler.py:234

**Description**:
Apify Actor 타임아웃(10분) 후 재시도 시 세션 복구 실패.
새 Actor 실행 대신 기존 실패한 실행 참조.

**Reproduction**:
1. 큰 results_limit (500+) 설정
2. 타임아웃 발생 대기
3. 자동 재시도 관찰
4. KeyError 또는 None 반환

**Expected Behavior**:
타임아웃 시 새 Actor 실행으로 폴백

**Workaround**:
수동으로 재실행 필요

---

### Bug: 캐러셀 11번째 이미지 누락
**Severity**: Medium
**Location**: ig_post_image_downloader.py

**Description**:
11개 이상 이미지가 있는 캐러셀 게시물에서 첫 10개만 다운로드.

**Root Cause**:
Apify Actor의 childPosts 배열이 10개로 제한됨 (API 제한)

---

## Component Changes

### New Component: SchedulerService
**Purpose**: 예약 작업 관리
**Input**: 스케줄 설정 (cron/interval), 작업 파라미터
**Output**: 스케줄 ID, 실행 결과

**Planned Methods**:
- `schedule_job(config)` - 새 스케줄 등록
- `cancel_job(job_id)` - 스케줄 취소
- `list_jobs()` - 등록된 스케줄 목록
- `get_history(job_id)` - 실행 히스토리

---

### Update Component: shared_utils.py
**Change Type**: Enhancement

**New Functions**:
- `setup_logger(name, level, format)` - 구조화된 로거 설정
- `log_to_json(event, data)` - JSON 형식 로그 출력

---

## Configuration Changes

### New Config: SCHEDULER_ENABLED
**Type**: Environment Variable
**Required**: No
**Default**: false
**Description**: 스케줄러 기능 활성화

### New Config: MAX_WORKERS
**Type**: Config File (config.yaml)
**Required**: No
**Default**: 2
**Valid Range**: 1-20
**Description**: 동시 다운로드 스레드 수

### New Config: LOG_FORMAT
**Type**: Environment Variable
**Required**: No
**Default**: "text"
**Valid Values**: "text", "json"
**Description**: 로그 출력 형식

---

## Notes

### Context
다음 분기 목표:
- 일일 10,000 프로필 처리 용량 확보
- 자동화된 데이터 수집 파이프라인 구축
- 운영 모니터링 체계 수립

### Constraints
- 현재 인프라 비용 $500/월 이내 유지
- Apify 프리미엄 요금제 한도 (월 100만 호출)
- 단일 서버 환경 (분산 처리 미지원)

### Timeline (예상)
- Phase 1 (2주): 스케줄러 기본 구현
- Phase 2 (1주): 내보내기 형식 확장
- Phase 3 (2주): 최적화 (병렬화, 연결 풀링)
- Phase 4 (3주): 웹 대시보드 (선택적)

### References
- APScheduler 문서: https://apscheduler.readthedocs.io/
- Parquet 포맷: https://parquet.apache.org/
- Apify API 제한: https://docs.apify.com/platform/limits
