# PR Review Report

**PR**: #42 - 사용자 인증 시스템 구현 및 세션 관리 버그 수정
**PR Author**: developer-kim
**Review Date**: 2026-03-09
**Reviewer**: Codex
**Patch Draft**: Found

## Verdict

**REQUEST CHANGES**

- 토큰 갱신 criterion 1건이 실패했다.
- 인증 미들웨어 컨텍스트 주입 테스트가 없다.
- PR에는 반영됐지만 스펙 패치 초안에 빠진 설정 변경이 있다.

## Metrics Summary

| Item | Count |
|------|-------|
| Total acceptance criteria | 10 |
| Met (✓) | 8 |
| Not met (✗) | 1 |
| Partial (△) | 1 |
| Spec violations | 0 |
| Pre-merge blockers | 2 |
| Spec sync `MUST update` | 3 |
| Spec sync `CONSIDER` | 1 |
| Spec sync `NO update` | 1 |

## Acceptance Criteria Verification

### Feature: JWT 기반 사용자 인증

| # | Criterion | Implementation | Test | Status | Notes |
|---|-----------|----------------|------|--------|-------|
| 1 | 로그인 시 access/refresh 토큰 발급 | `src/services/auth_service.py:45` | `test_login_returns_tokens` | ✓ | |
| 2 | refresh 시 새 만료 시간 발급 | `src/services/auth_service.py:89` | `test_refresh_token` | ✗ | 새 exp 미갱신 |
| 3 | 로그아웃 시 refresh 토큰 무효화 | `src/services/auth_service.py:110` | `test_logout_invalidates_token` | ✓ | |

### Feature: 인증 미들웨어

| # | Criterion | Implementation | Test | Status | Notes |
|---|-----------|----------------|------|--------|-------|
| 1 | Bearer token 추출 | `src/middleware/auth.py:12` | `test_extract_bearer_token` | ✓ | |
| 2 | 사용자 컨텍스트 주입 | `src/middleware/auth.py:47` | - | △ | 테스트 누락 |

## Spec Compliance Verification

- 기존 인증 정책과 충돌하는 breaking change는 발견되지 않았다.
- `401`/`403` 경계는 코드상 유지되지만, 스펙에는 미들웨어 흐름이 충분히 문서화되어 있지 않다.

## Exploration-First Spec Impact

- `Runtime Map`: 로그인과 토큰 갱신 플로우가 추가되어야 한다.
- `Component Index`: `Auth Middleware`와 `Auth Service` 경로가 더 분명히 적혀야 한다.
- `Common Change Paths`: "인증 정책 변경" 시작 지점이 필요하다.
- `Open Questions`: 토큰 만료 정책, CORS 허용 범위가 아직 문서상 미확정이다.

## Gap Analysis

### In patch but not fully implemented

1. refresh 토큰 갱신의 새 만료 시간 발급

### In PR but not captured in patch

1. `config/settings.py:45`의 CORS 헤더 허용 범위 변경
2. `.env.example:12`의 JWT 관련 환경변수 추가

### Test / Documentation Gaps

1. 인증 미들웨어 컨텍스트 주입 테스트 없음
2. 새 환경변수의 스펙 반영 위치 미정

## Merge Blockers

1. refresh 토큰 갱신의 새 만료 시간 발급 실패
2. 인증 미들웨어 컨텍스트 주입 테스트 누락

## Post-Merge Spec Sync

1. `Architecture Overview > Runtime Map` 갱신
   - Classification: `MUST update`
2. `Component Details > Component Index` 갱신
   - Classification: `MUST update`
3. `Usage Examples > Common Change Paths` 보강
   - Classification: `CONSIDER`
4. `src/utils/password.py` 내부 helper 분리
   - Classification: `NO update`
   - Reason: 계약과 탐색성 변화 없음

## Items Requiring Spec Update

1. `Architecture Overview > Runtime Map` (`MUST update`)
2. `Component Details > Component Index` (`MUST update`)
3. `Usage Examples > Common Change Paths` (`CONSIDER`)
4. `Open Questions` (`MUST update`)

## Open Questions

1. 토큰 만료 정책은 메인 스펙에 둘지 `auth.md`로 내릴지 결정 필요
2. CORS 변경을 `Environment & Dependencies`에 반영할지 확인 필요

## Next Steps

1. refresh 토큰 버그 수정
2. 인증 미들웨어 테스트 추가
3. `/pr-spec-patch` 초안 보완
4. merge 후 `/spec-update-done` 실행
