# Specification Summary Template

탐색형 스펙 요약은 "설명"보다 "이해와 탐색 시작점"을 우선한다.

## Core Rules

- 짧게 쓴다. 메인 요약은 보통 2-4 화면 이내가 좋다.
- 실제 경로와 컴포넌트 이름을 포함한다.
- `Repository Map`, `Runtime Map`, `Component Index`, `Common Change Paths`, `Open Questions`를 우선한다.
- 스펙에 없는 버전/퍼센트/로드맵을 임의로 만들지 않는다.

## Template

```md
# [Project Name] - Specification Summary

**생성일**: [YYYY-MM-DD HH:MM]
**메인 스펙**: `_sdd/spec/[main.md or project].md`
[선택] **참고 구현 문서**: `_sdd/implementation/IMPLEMENTATION_REVIEW.md`

---

## Project Snapshot

- **무엇을 하는가**: [1-2문장]
- **핵심 사용자/대상**: [짧게]
- **핵심 기능**:
  - [기능 1]
  - [기능 2]
  - [기능 3]
- **Non-Goals**:
  - [있을 때만]

## System Boundary

- **이 저장소가 책임지는 것**:
  - [항목]
- **외부 시스템/서비스**:
  - [항목]

## Repository Map

| 경로 | 역할 | 메모 |
|------|------|------|
| `src/...` | [역할] | [메모] |
| `tests/...` | [역할] | [메모] |

## Runtime Map

### Primary Flow
1. [진입점]
2. [핵심 처리]
3. [저장/외부 호출]
4. [응답/후속 이벤트]

[선택] 간단한 ASCII diagram

## Component Index

| 컴포넌트 | 책임 | 주요 경로 | 관련 스펙 |
|---------|------|----------|----------|
| [이름] | [책임] | `path` | `_sdd/spec/[component].md` |

## Current Status

- **완료/진행/계획 요약**: [status marker나 구현 문서 기준]
- **현재 집중 영역**: [있으면]
- **주요 리스크**: [1-3개]

## Common Change Paths

### [자주 하는 변경 1]
- 먼저 볼 곳: `path`
- 같이 확인할 곳: `path`
- 검증 포인트: [테스트/로그/리뷰 문서]

### [자주 하는 변경 2]
- 먼저 볼 곳: `path`
- 같이 확인할 곳: `path`
- 검증 포인트: [테스트/로그/리뷰 문서]

## Risks / Improvements

- [리스크 또는 개선 포인트]
- [리스크 또는 개선 포인트]

## Open Questions

- [미확인 사항]
- [미확인 사항]

## Quick Reference

- **메인 스펙**: `_sdd/spec/[main.md or project].md`
- **컴포넌트 스펙**: `_sdd/spec/[component].md`
- **환경 문서**: `_sdd/env.md`
- **구현 계획**: `_sdd/implementation/IMPLEMENTATION_PLAN.md`
- **최신 구현 리뷰**: `_sdd/implementation/IMPLEMENTATION_REVIEW.md`
```

## Optional README Block

README sync를 요청받은 경우에만 아래 marker block을 갱신한다.

```md
<!-- spec-summary:start -->
## Project Snapshot

- 무엇을 하는가: [한 줄]
- 현재 집중 영역: [한 줄]
- 어디부터 볼까: `_sdd/spec/main.md`, `_sdd/spec/[component].md`

더 자세한 내용: [`_sdd/spec/SUMMARY.md`](_sdd/spec/SUMMARY.md)
<!-- spec-summary:end -->
```
