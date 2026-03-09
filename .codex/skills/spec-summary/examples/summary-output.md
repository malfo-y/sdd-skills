# Task Management - Specification Summary

**생성일**: 2026-03-09 10:20
**메인 스펙**: `_sdd/spec/main.md`
**참고 구현 문서**: `_sdd/implementation/IMPLEMENTATION_REVIEW.md`

---

## Project Snapshot

- **무엇을 하는가**: 팀이 작업을 생성, 배정, 추적, 완료할 수 있게 해 주는 태스크 관리 서비스다.
- **핵심 사용자/대상**: 내부 운영팀, 프로젝트 매니저, 협업 팀원
- **핵심 기능**:
  - 작업 생성/수정/상태 전이
  - 담당자 배정과 마감일 관리
  - 댓글, 알림, 검색
  - 반복 작업과 의존 관계
- **Non-Goals**:
  - 회계/정산 기능
  - 장기 문서 협업 편집

## System Boundary

- **이 저장소가 책임지는 것**:
  - 태스크 도메인 로직
  - 웹 API와 프론트엔드 UI
  - 사용자 인증과 권한
- **외부 시스템/서비스**:
  - PostgreSQL
  - Redis
  - 이메일 전송 서비스

## Repository Map

| 경로 | 역할 | 메모 |
|------|------|------|
| `frontend/src/` | 사용자 UI | 보드/리스트/상세 화면 |
| `src/api/` | HTTP 엔드포인트 | 인증, 태스크, 팀 API |
| `src/domain/` | 핵심 비즈니스 로직 | 태스크 상태 전이, 의존 관계 |
| `src/infra/` | DB/외부 연동 | Prisma, Redis, 메일 |
| `tests/` | 통합/단위 테스트 | API와 도메인 검증 |

## Runtime Map

### Primary Flow
1. 사용자가 `frontend/src/features/tasks/`에서 작업을 생성한다.
2. 요청은 `src/api/routes/tasks.ts`로 들어간다.
3. 비즈니스 로직은 `src/domain/task/TaskService.ts`에서 수행된다.
4. 저장은 `src/infra/db/taskRepository.ts`가 담당한다.
5. 후속 알림은 `src/infra/notifications/`로 전달된다.

## Component Index

| 컴포넌트 | 책임 | 주요 경로 | 관련 스펙 |
|---------|------|----------|----------|
| Task API | 태스크 HTTP 계약 | `src/api/routes/tasks.ts` | `_sdd/spec/task-api.md` |
| Task Domain | 상태 전이와 규칙 | `src/domain/task/` | `_sdd/spec/task-domain.md` |
| Auth | 인증/권한 | `src/api/routes/auth.ts`, `src/domain/auth/` | `_sdd/spec/auth.md` |
| Notifications | 메일/이벤트 알림 | `src/infra/notifications/` | `_sdd/spec/notifications.md` |

## Current Status

- **완료/진행/계획 요약**: 기본 CRUD, 댓글, 검색은 완료. 반복 작업과 의존 관계는 진행 중.
- **현재 집중 영역**: 의존 관계 edge case와 권한 정책 정리
- **주요 리스크**:
  - 대량 태스크 조회 성능
  - 토큰 갱신 UX
  - 고급 권한 정책 테스트 부족

> 이 예시는 구현 문서가 있어 `Current Status`를 포함한다. 작은 프로젝트에서 해당 정보가 없으면 이 섹션은 생략해도 된다.

## Common Change Paths

### 새 태스크 필드 추가
- 먼저 볼 곳: `src/domain/task/Task.ts`, `src/api/routes/tasks.ts`
- 같이 확인할 곳: `frontend/src/features/tasks/`, `tests/api/tasks.test.ts`
- 검증 포인트: API contract test, 프론트 폼 검증

### 권한 정책 변경
- 먼저 볼 곳: `src/domain/auth/Policy.ts`
- 같이 확인할 곳: `src/api/middleware/auth.ts`, `tests/auth/`
- 검증 포인트: role별 접근 테스트, 401/403 응답 확인

### 알림 동작 수정
- 먼저 볼 곳: `src/infra/notifications/`
- 같이 확인할 곳: `src/domain/task/TaskService.ts`
- 검증 포인트: 이벤트 발행 여부, 메일 큐 처리 로그

## Risks / Improvements

- 태스크 목록 조회에 pagination과 인덱스 전략이 더 필요하다.
- 반복 작업 스케줄링 규칙이 문서상 일부만 정의되어 있다.
- 프론트와 API 에러 응답 형식이 아직 완전히 표준화되지 않았다.

## Open Questions

- 반복 작업의 시간대 기준은 사용자별인지 워크스페이스별인지 확정이 필요하다.
- 의존 관계가 순환될 때 UX와 API 에러 코드를 어떻게 통일할지 결정이 필요하다.

## Quick Reference

- **메인 스펙**: `_sdd/spec/main.md`
- **컴포넌트 스펙**: `_sdd/spec/task-domain.md`, `_sdd/spec/auth.md`
- **환경 문서**: `_sdd/env.md`
- **구현 계획**: `_sdd/implementation/IMPLEMENTATION_PLAN.md`
- **최신 구현 리뷰**: `_sdd/implementation/IMPLEMENTATION_REVIEW.md`
