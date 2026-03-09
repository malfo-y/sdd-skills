# Optional Rewrite Report Example

Use this only when the rewrite is large enough that the normal completion summary is insufficient.

## Rewrite Summary

- **Target Document**: `_sdd/spec/apify_ig.md`
- **Execution Date**: 2026-03-09
- **Rewrite Goal**: 긴 스펙을 탐색형 스펙으로 재구성하여 이해와 변경 시작점을 빠르게 찾을 수 있게 함

## What Became Easier to Understand

- 메인 문서 첫 화면에서 프로젝트 목적, 시스템 경계, 핵심 흐름이 바로 보이도록 정리했다.
- 분산되어 있던 아키텍처 설명을 `Repository Map`과 `Runtime Map`으로 재구성하고, 사용자 관점 흐름 설명을 추가했다.
- 핵심 책임 단위를 `Component Index`로 요약해 전체 구조를 먼저 볼 수 있게 했다.
- 주요 컴포넌트마다 `Overview`를 추가해 동작 개요와 설계 의도를 바로 읽을 수 있게 했다.

## What Became Easier to Change

- `Usage Examples`에 `Common Change Paths`를 추가해 새 기능 추가와 기존 동작 변경의 시작 지점을 명시했다.
- 주요 컴포넌트마다 실제 경로와 핵심 심볼을 연결했다.
- 관련 테스트와 운영 디버깅 포인트를 문서에서 바로 찾을 수 있게 했다.

## File Shape After Rewrite

```text
_sdd/spec/
├── apify_ig.md
├── ingestion.md
├── sync_jobs.md
└── DECISION_LOG.md
```

## Main Spec Changes

- `Goal` 섹션을 `Project Snapshot`, `Key Features`, `Non-Goals` 중심으로 재구성
- `Architecture Overview`에 `System Boundary`, `Repository Map`, `Runtime Map` 추가
- `Component Details`에 `Component Index` 추가
- 핵심 컴포넌트에 `Overview` 추가
- `Usage Examples`에 `Common Change Paths` 추가
- `Open Questions`로 미확인 사항 분리

## What Was Moved Out of the Main Flow

- 긴 실행 로그 2개 섹션
- 중복 API 예시 표 3개
- 현재 판단과 직접 관계없는 과거 설계 회고 문단

## Open Questions

- rate limit 정책의 최종 기준값이 아직 문서 간 완전히 일치하지 않음
- 장애 알림 소유 팀 정보가 코드/문서에서 명확하지 않음

## Decision Log Additions

- **Entry**: polling 기반 sync 유지
- **Why**: 이벤트 기반 대안보다 운영 제어 가능성이 높아 현재 구조를 유지

## Validation Result

- 메인 문서 길이: 1180줄 -> 290줄
- Component Index: 추가됨
- Repository Map: 추가됨
- Component Overview: 추가됨
- Common Change Paths: 추가됨
- broken links: 0
