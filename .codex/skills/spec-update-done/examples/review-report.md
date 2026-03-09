# Example: Spec Sync Report

This is an example sync report before applying spec updates.

---

# Spec Sync Report: Instagram Data Pipeline

**Review Date**: 2026-03-09
**Reviewer**: Codex
**Target Spec**: `_sdd/spec/apify_ig.md`

## Summary

- 변경 파일: 2개
- 주요 탐색 업데이트: 4개
- 기능/계약 업데이트: 3개
- 남는 Open Questions: 1개

## Navigation Updates

1. `Architecture Overview > Repository Map`에 `src/services/notification_service.py` 관련 경로가 없음
2. `Architecture Overview > Runtime Map`에 배치 종료 이벤트 -> NotificationService 흐름이 없음
3. `Component Details > Component Index`에 `NotificationService`가 없음
4. `Component Details > Overview`에 NotificationService의 실패 격리 설계 의도가 없음
5. `Usage Examples > Common Change Paths`에 알림 기능 수정 시작점이 없음

## Behavior / Contract Updates

1. `실시간 알림` 기능이 계획 상태가 아니라 구현 완료 상태임
2. NotificationService는 실제로 Slack/Discord 채널 비활성화 fallback을 지원함
3. 알림 실패가 파이프라인 종료 상태를 바꾸지 않는 invariant가 코드로 확인됨

## Environment Updates

1. `NOTIFICATION_WEBHOOK_SLACK`, `NOTIFICATION_WEBHOOK_DISCORD`, `NOTIFICATION_ENABLED` 환경 변수 문서화 필요

## Issue / Unknown Updates

1. 이메일 알림 범위는 아직 구현되지 않았으므로 `Open Questions` 유지
2. 기존 `Open Questions` 중 “알림 실패 시 파이프라인 영향” 항목은 해결되어 제거 가능
