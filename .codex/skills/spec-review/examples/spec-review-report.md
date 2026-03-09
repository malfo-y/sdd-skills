# Spec Review Report

**Date**: 2026-03-09
**Reviewer**: Codex
**Scope**: Spec+Code
**Spec Files**:
- `_sdd/spec/main.md`
- `_sdd/spec/auth.md`
- `_sdd/spec/jobs.md`
**Decision**: SYNC_REQUIRED

## Executive Summary

메인 스펙은 프로젝트 목적과 컴포넌트 구성을 대체로 설명하지만, `Runtime Map`, `Component Overview`, `Common Change Paths`가 현재 구현을 충분히 따라가지 못한다. 특히 인증 흐름과 백그라운드 작업 경로가 코드 기준으로 확장됐는데 문서에는 반영이 부족하다.

## Findings by Severity

### High

1. 인증 미들웨어 흐름이 메인 스펙 `Runtime Map`에 없다
   - Evidence: `src/api/middleware/auth.ts:1`, `src/api/routes/auth.ts:12`
   - Impact: 인증 관련 변경 시 영향 범위를 잘못 판단할 수 있다
   - Recommendation: 로그인/토큰 검증/컨텍스트 주입 흐름을 추가한다

### Medium

1. `Component Index`에 jobs worker 경로가 빠져 있다
   - Evidence: `src/jobs/worker.ts:1`
   - Impact: 배치/큐 이슈를 찾기 어렵다
   - Recommendation: `jobs.md`와 메인 `Component Index`에 worker 경로를 추가한다

2. `Common Change Paths`가 사용자 권한 정책 변경 경로를 제공하지 않는다
   - Evidence: `_sdd/spec/main.md:120`, `src/domain/auth/Policy.ts:1`
   - Impact: 권한 변경 시 관련 테스트/미들웨어를 놓치기 쉽다
   - Recommendation: 정책 변경용 change path를 추가한다

3. `auth.md`에 인증 미들웨어의 `Overview`가 없다
   - Evidence: `_sdd/spec/auth.md:1`, `src/api/middleware/auth.ts:1`
   - Impact: 요청이 어떻게 보호되고 왜 middleware-first 구조를 택했는지 파악하기 어렵다
   - Recommendation: Bearer token 추출 -> 검증 -> 사용자 컨텍스트 주입 흐름과 설계 의도를 `Overview`에 추가한다

### Low

1. `Open Questions`에 이미 해결된 Redis queue naming 이슈가 남아 있다
   - Evidence: `_sdd/spec/main.md:188`, `src/jobs/config.ts:14`
   - Recommendation: 질문을 제거하거나 resolved note로 바꾼다

## Entry Point / Navigation Notes

- `Project Snapshot`과 `System Boundary`는 충분히 짧고 명확하다.
- `Repository Map`은 있으나 jobs 관련 경로가 일부 누락되어 있다.
- `Runtime Map`은 API 요청 중심이라 background job 흐름이 약하다.
- `Environment & Dependencies` 상세가 짧지만, 현재 범위에서는 optional 누락으로 보지 않는다.

## Explanation Quality Notes

- 메인 `Runtime Map`은 화살표 흐름은 있으나 인증/worker 흐름의 사용자 관점 설명이 부족하다.
- `auth.md`가 책임/경로/계약은 보여주지만, middleware-first 설계 의도를 설명하는 `Overview`가 없다.

## Changeability Notes

- 새 API 필드 추가 경로는 문서에 있다.
- 권한 정책 변경과 worker retry 정책 변경의 시작점은 문서에 약하다.
- 테스트/로그 시작점 연결이 일부 컴포넌트에서 빠져 있다.

## Spec-to-Code Drift Notes

- 인증 흐름과 jobs worker 경로가 구현보다 문서가 뒤처진다.
- `Open Questions` 일부가 stale 상태다.

## Open Questions

1. jobs retry 정책은 메인 스펙에 둘지 `jobs.md`에만 둘지 결정 필요

## Suggested Next Actions

1. `/spec-update-done`으로 `Runtime Map`, `Component Index`, `auth.md > Overview`를 갱신한다.
2. 권한 정책과 worker retry 변경 경로를 `Common Change Paths`에 추가한다.
3. stale `Open Questions`를 정리한다.

## LLM Efficiency Notes

- 메인 스펙이 핵심 경로 중심으로 짧게 유지되어 전체 소비 비용은 적절하다.
- 다만 jobs 흐름 설명이 흩어져 있어 background job 변경 시 추가 탐색 비용이 든다.

## Decision Log Follow-up Proposal

- Proposed entry: "Auth middleware became part of the canonical request flow"
  - Context: 구현상 인증 미들웨어가 공통 경로가 되었지만 문서 반영이 늦어짐
  - Decision: 로그인 이후 보호된 요청은 middleware-first flow로 설명
  - Rationale: 코드 탐색과 변경 영향 판단 정확도를 높이기 위해
