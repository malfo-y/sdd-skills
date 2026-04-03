# Spec Review Report

**Date**: 2026-04-03 | **Scope**: Spec+Code
**Decision**: **SYNC_REQUIRED**

## Summary

spec-rewrite(v3.9.0)로 구조 개선은 성공적이나, 최근 코드 변경 2건이 스펙에 미반영되어 있다. `pr-spec-patch` 스킬이 `pr-review`로 통합(commit 964c1fe)되었으나 스펙 전반에 12+ 잔존 참조가 남아 있고, `second-opinion` 스킬이 새로 추가(commit cc1dd31)되었으나 스펙에 전혀 문서화되지 않았다. 이 두 건은 Architecture/Feature drift로 즉시 동기화가 필요하다.

## Findings

### High

1. **pr-spec-patch ghost reference (Architecture Drift)**
   - `pr-spec-patch` 스킬이 `pr-review`로 통합됨 (commit `964c1fe`)
   - `.claude/skills/pr-spec-patch/` 디렉토리 삭제됨 — 실존하지 않음
   - 그러나 스펙에 12+ 잔존 참조:
     - `main.md:394` — PR 워크플로우 다이어그램에 `pr-spec-patch → pr-review` 여전히 표시
     - `main.md:428` — Artifact Map에 pr-spec-patch 산출물 잔존
     - `main.md:466` — Category Overview 테이블에 별도 행 유지
     - `main.md:557` — Directory Structure에 `pr-spec-patch/` 디렉토리 표시
     - `main.md:192` — Design Patterns에서 pr-spec-patch 참조
     - `components.md:178-186` — 별도 컴포넌트 섹션 유지
     - `components.md:276` — Code Reference Index에 Source 참조
     - `usage-guide.md:66` — Scenario 3에서 별도 호출 안내
   - **Recommendation**: pr-spec-patch 관련 모든 참조를 제거하고, pr-review에 spec-patch 기능 통합을 반영. Artifact Map의 `spec_patch_draft.md`는 pr-review 산출물로 이관.

2. **second-opinion 스킬 미문서화 (Feature Drift)**
   - `.claude/skills/second-opinion/SKILL.md` 존재 (commit `cc1dd31`)
   - Claude Code 전용 (Codex에는 미존재)
   - 스펙 어디에도 문서화되지 않음 — main.md, components.md, Directory Structure 모두 누락
   - **Recommendation**: components.md에 second-opinion 컴포넌트 추가, main.md Category Overview 테이블에 행 추가, Directory Structure 갱신.

3. **Codex 스킬 수 불일치 (Architecture Drift)**
   - 스펙: "Codex 스킬 20개" (`main.md` Key Features, Platform Differences)
   - 실제: 19개 (pr-spec-patch 삭제로 1개 감소)
   - **Recommendation**: 20개 → 19개로 수정

### Medium

4. **PR 워크플로우 다이어그램 outdated**
   - `main.md:394`: `PR 생성 → pr-spec-patch → pr-review → (merge 후) spec-update-done`
   - 실제: pr-spec-patch가 pr-review에 통합되어 2단계 → 1단계
   - **Recommendation**: `PR 생성 → pr-review → (merge 후) spec-update-done`으로 갱신

5. **Claude 스킬 수 표기 정합성**
   - `main.md` Key Features: "21개 스킬" — 실제 21개(second-opinion 포함)로 숫자는 맞지만, Category Overview에 second-opinion이 빠져 있어 inventory가 불일치
   - `main.md` Architecture: "Claude Code 스킬 21개" — 숫자 맞음
   - `main.md` Platform Differences: 스킬 수 21개 — 맞음. 래퍼 9개 표기도 재확인 필요 (pr-spec-patch 제거로 래퍼 아닌 풀 스킬 수 변동)
   - **Recommendation**: Category Overview에 second-opinion 추가, 풀 스킬/래퍼 비율 갱신 (풀 12 + 래퍼 8 + 메타 1 = 21)

### Low

6. **old SPEC_REVIEW_REPORT.md 위치**
   - `_sdd/spec/SPEC_REVIEW_REPORT.md`가 루트에 있었음 → 이번 리뷰에서 `logs/prev/`로 아카이브 완료
   - 향후 리포트는 `logs/spec_review_report.md`에 저장

7. **Decision Log 내 pr-spec-patch 참조 (historical)**
   - `DECISION_LOG.md`에 과거 결정 기록 중 pr-spec-patch 언급 3건
   - 역사 기록이므로 수정 불필요 — 당시 실제 경로를 보존하는 것이 원칙

## Open Questions

1. `second-opinion` 스킬의 Codex 지원 여부 — 현재 Claude Code 전용이지만, Codex parity 대상인지 확인 필요
2. pr-review가 pr-spec-patch를 흡수한 후 `_sdd/pr/spec_patch_draft.md` 산출물이 여전히 별도 생성되는지, 또는 `pr_review.md`에 통합되었는지 확인 필요

## Code Analysis Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| Top Hotspots | spec-create(41), spec-rewrite(33), spec-review(27) | SKILL.md 기준, 스펙 관련 스킬이 가장 자주 변경 |
| Focus Score | 91.9% | 540/587 변경 파일이 스펙 컴포넌트 관련 |
| Test Coverage | N/A | 마크다운 기반 스킬 프로젝트 — 전통적 테스트 없음 |

## Handoff (SYNC_REQUIRED)

| Priority | Finding | 권장 조치 |
|----------|---------|----------|
| **P1** | pr-spec-patch ghost reference | `/spec-update-done`으로 pr-spec-patch 관련 12+ 참조 제거, pr-review에 통합 반영 |
| **P1** | second-opinion 미문서화 | `/spec-update-done`으로 components.md + main.md에 추가 |
| **P1** | Codex 스킬 수 불일치 | 20 → 19로 수정 |
| **P2** | PR 워크플로우 다이어그램 | main.md:394 갱신 |
| **P2** | 스킬 분류 비율 | 풀 12 / 래퍼 8 / 메타 1로 재확인 |

## Suggested Next Actions

1. `/spec-update-done` 실행하여 P1/P2 항목 동기화
2. `second-opinion` 스킬의 Codex parity 방침 결정
3. pr-review 통합 후 `spec_patch_draft.md` 산출물 경로 확인
