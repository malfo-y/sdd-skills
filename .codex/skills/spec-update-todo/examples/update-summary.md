# Example: Spec Update Summary

This is an example summary after applying planned updates into an exploration-first spec.

---

# Spec Update Complete

**Updated Files**:
- `_sdd/spec/apify_ig.md`
- `_sdd/spec/notification.md`

**Input Source**: `_sdd/spec/user_spec.md`
**Date**: 2026-03-09
**Spec Update Classification**: MUST update

## Applied Changes

| File | Section | Change |
|------|---------|--------|
| `apify_ig.md` | `Goal > Key Features` | `실시간 알림` planned feature 추가 |
| `apify_ig.md` | `Architecture Overview > Runtime Map` | 알림 이벤트 흐름 추가 |
| `notification.md` | `Component Details` | `NotificationService` planned component 생성 |
| `apify_ig.md` | `Usage Examples > Common Change Paths` | 알림 관련 변경 시작점 추가 |
| `apify_ig.md` | `Open Questions` | 이메일 알림 범위 미정 항목 추가 |

## Planned Markers Added

- `📋 계획됨` 표기를 사용자 가치, 컴포넌트 책임, 환경 변경 지점에 추가

## Processed Input Files

| Original | New Name |
|----------|----------|
| `_sdd/spec/user_spec.md` | `_sdd/spec/_processed_user_spec.md` |

## Decision Log

- 없음

## Remaining Open Questions

- 이메일 알림을 이번 범위에 포함할지 확정 필요

## Next Steps

1. `implementation`으로 계획 실행
2. 구현 완료 후 `spec-update-done` 실행
