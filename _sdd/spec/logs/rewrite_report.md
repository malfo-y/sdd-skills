# Spec Rewrite Report

**Target**: `_sdd/spec/main.md` (v3.8.2 → v3.9.0)
**Executed**: 2026-04-03
**Plan**: `_sdd/spec/logs/spec-rewrite-plan.md`

---

## Rewrite Summary

1206줄 단일 파일이었던 main.md를 **인덱스(668줄) + 3개 분리 파일**로 재구성. 핵심 narrative(§1-§3)는 main.md에 인라인 유지하고, Component Details, Usage Guide, Changelog를 별도 파일로 분리.

## File Split Map

| 파일 | 줄 수 | 내용 |
|------|-------|------|
| `main.md` | 668 (was 1206) | 인덱스: §1-§3 인라인, §4 요약 + 에이전트 목록, §7 Environment, §8 Issues, Appendix 링크 |
| `components.md` | 303 (신규) | §4 Component Details 상세 + Appendix: Code Reference Index |
| `usage-guide.md` | 84 (신규) | §5 Usage Guide & Expected Results (4개 시나리오) |
| `logs/changelog.md` | 152 (이동) | v2.1.0 ~ v3.8.2 전체 Changelog |

## Pruned / Moved Sections

| 대상 | 조치 | 이유 |
|------|------|------|
| Component Details (20+ 컴포넌트 상세 테이블) | `components.md`로 이동 | main 경량화, 컴포넌트별 파일 귀속 |
| Usage Guide (4개 시나리오) | `usage-guide.md`로 이동 | 독립 참조 가능하도록 분리 |
| Changelog (v2.1.0~v3.8.2) | `logs/changelog.md`로 이동 | 역사 기록은 main에서 제거 |
| Code Reference Index | `components.md` 하단으로 이동 | 코드 참조와 컴포넌트 상세를 함께 관리 |
| 해결 완료 이슈 (#1-4, #8-16) | 삭제 | changelog에서 이미 추적 가능, 본문 중복 제거 |

## Metric Scorecard (0-3)

| Metric | Before | After | 근거 |
|--------|--------|-------|------|
| Component Separation | 2 | 3 | 20+ 컴포넌트가 `components.md` 전용 파일에 귀속. main에서는 요약 테이블 + 에이전트 목록만 유지 |
| Findability | 2 | 3 | main(668줄) → components.md/usage-guide.md로 2-hop 이내 도달. TOC에 링크 명시 |
| Repo Purpose Clarity | 3 | 3 | §1 변경 없음. main 상단에서 레포 목적 즉시 파악 가능 |
| Architecture Clarity | 3 | 3 | §2-§3 변경 없음. 시스템 다이어그램, 데이터 흐름, 워크플로우 모두 main에 인라인 유지 |
| Usage Completeness | 3 | 3 | 4개 시나리오 모두 보존 (usage-guide.md로 이동, 내용 동일) |
| Environment Reproducibility | 2 | 2 | §7 변경 없음. env.md 참조 의존은 content 이슈로 rewrite scope 밖 |
| Ambiguity Control | 2 | 2 | Hard Rules, 에이전트 목록 등 기존 content 유지. 스킬 수 불일치는 content 수정 필요 (scope 밖) |
| Why/Decision Preservation | 3 | 3 | 모든 컴포넌트의 Why 필드, Design Rationale 테이블 보존. DECISION_LOG.md 변경 없음 |

## Whitepaper Fit Assessment

| 섹션 | 존재 | 품질 | 위치 |
|------|------|------|------|
| §1 Background & Motivation | Yes | Strong | main.md (인라인) |
| §2 Core Design | Yes | Strong | main.md (인라인) |
| §3 Architecture Overview | Yes | Strong | main.md (인라인) |
| §4 Component Details | Yes | Comprehensive | components.md (분리) |
| §5 Usage Guide & Expected Results | Yes | Good | usage-guide.md (분리) |
| §6 Data Models / API Reference | N/A | — | 해당 없음 (마크다운 스킬 프로젝트) |
| §7 Environment & Dependencies | Yes | Adequate | main.md (인라인) |
| §8 Issues & Appendix | Yes | Adequate | main.md (인라인) |

**누락된 whitepaper narrative**: 없음. 모든 핵심 섹션 존재.

## Ambiguities and Issues

1. main.md 내 "21개 스킬"과 "20개 스킬" 표현 혼재 — content 정합성 이슈로 rewrite scope 밖
2. Environment Reproducibility(2점) — env.md 참조 의존. content 보강은 spec-update-todo/spec-upgrade 역할

## Warnings Intentionally Left Unresolved

- 스킬 수 불일치 표현은 실제 파일 구조 확인 후 별도 content 수정 필요
- §6 Data Models / API Reference 섹션 미존재 — 해당 프로젝트 특성상 N/A

## Notable Deviations from spec-rewrite-plan.md

| 항목 | Plan | 실제 | 이유 |
|------|------|------|------|
| main.md 줄 수 | ~530줄 | 668줄 | §4 Category Overview + 에이전트 목록 테이블(~60줄)을 main에 유지한 것이 예상보다 길었음. 컴포넌트 탐색의 진입점 역할을 위해 main에 유지하는 것이 합리적 |
| Scenario 번호 | 기존 Scenario 4 | Scenario 3b로 변경 | usage-guide.md에서 번호 정리 (PR=3, 현황=3b) |

## Decision Log Additions

이번 rewrite에서 rationale 삭제 없음. 모든 Why 필드, Design Rationale 테이블, DECISION_LOG.md 항목이 원본 그대로 보존됨.
