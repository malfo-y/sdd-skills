# Spec Rewrite Report

**Target**: `_sdd/spec/main.md`, `_sdd/spec/components.md` (v4.0.1 -> v4.1.1 active spec surface)
**Executed**: 2026-04-04
**Plan**: `_sdd/spec/logs/spec-rewrite-plan.md`

---

## Rewrite Summary

2단계 리라이트를 수행했다. 먼저 `main.md`를 current global thin 기준에 맞춰 다시 압축해 standalone `Contract / Invariants / Verifiability`, usage summary, decision-bearing structure table, reference/code-map appendix를 제거하고, repo-wide 판단 기준만 `Scope / Non-goals / Guardrails`와 `핵심 설계와 주요 결정`에 흡수했다. 이어서 `components.md`를 reference-only compact catalog로 재구성해 Purpose/Why/Source와 최소 navigation note만 남겼다.

## File Impact

| 파일 | 변경 | 결과 |
|------|------|------|
| `_sdd/spec/main.md` | 전면 재작성 + version bump | 257줄 -> 111줄. 3개 mandatory core + 짧은 supporting surface index만 유지 |
| `_sdd/spec/components.md` | 전면 재작성 | 284줄 -> 71줄. category-based compact catalog + strategic code map만 유지 |
| `_sdd/spec/usage-guide.md` | 도입부 보정 | `main.md`의 legacy §5 참조 제거, usage/expected result surface 역할 명시 |
| `_sdd/spec/logs/spec-rewrite-plan.md` | 갱신 | thin rewrite 기준과 prune rationale 기록 |
| `_sdd/spec/DECISION_LOG.md` | 갱신 | 구조 판단 이력 추가 |
| `_sdd/spec/logs/changelog.md` | 갱신 | v4.1.0 변경 이력 추가 |

## Pruned / Absorbed from Main

| 대상 | 조치 | 보존 방식 |
|------|------|----------|
| standalone CIV table | 본문 제거 | artifact contract, verification discipline, backup rule을 `Guardrails`로 흡수 |
| usage summary table | 본문 제거 | `usage-guide.md` 링크로 대체 |
| decision-bearing structure 대형 표 | 본문 제거 | layered design, rollout order, supporting-doc rule을 §3에 흡수 |
| reference section + appendix code map | 본문 제거 | supporting surface index와 외부 기준 문서 링크만 유지 |
| component별 Input/Output/Process/완료 이력 | `components.md`에서 제거 | 원문 재복제 대신 compact reference와 source 링크만 유지 |

## Metric Scorecard

| Metric | Before | After | 근거 |
|--------|--------|-------|------|
| Component Separation | 3 | 3 | component detail은 계속 `components.md`에 남아 있다 |
| Findability | 3 | 3 | main이 더 짧아졌고, supporting surface 링크가 상단과 하단에 고정돼 있다 |
| Repo Purpose Clarity | 3 | 3 | §1 narrative는 유지됐다 |
| Boundary Clarity | 2 | 3 | repo-wide operating rule이 §2에 직접 모였다 |
| Decision Preservation | 3 | 3 | layered design, key decisions, rollout order를 유지했다 |
| Contamination Control | 1 | 3 | usage/reference/appendix/CIV detail을 main body에서 제거했다 |
| Canonical Fit | 1 | 3 | main body가 `Background / Scope / Core Design` 중심으로 재구성됐다 |

## Components Surface Assessment

| Metric | Before | After | 근거 |
|--------|--------|-------|------|
| Reference Density | 1 | 3 | component별 상세 runtime prose를 compact table로 정리했다 |
| Findability | 2 | 3 | 카테고리 기준으로 필요한 스킬을 더 빨리 찾을 수 있다 |
| Why Preservation | 3 | 3 | 모든 컴포넌트에 Why 열을 유지했다 |
| Source Preservation | 3 | 3 | primary source와 platform note를 유지했다 |

## Canonical-Fit Assessment

| 항목 | 상태 | 비고 |
|------|------|------|
| Background & High-Level Concept | Yes | §1 유지 |
| Scope / Non-goals / Guardrails | Yes | §2 유지, repo-wide invariants 흡수 |
| Core Design & Key Decisions | Yes | §3 유지, 구조적 판단 흡수 |
| usage / expected result detail | Moved out | `usage-guide.md` |
| component reference / code navigation | Moved out | `components.md` compact catalog + appendix |
| decision log / release history | Moved out | `DECISION_LOG.md`, `logs/changelog.md` |

## Validation

- `prev/` 백업 확인: `prev_main_20260404_130259.md`, `prev_components_20260404_130259.md`, `prev_usage-guide_20260404_130259.md`, `prev_DECISION_LOG_20260404_130259.md`
- 2차 백업 확인: `prev_components_20260404_130827.md`, `prev_spec-rewrite-plan_20260404_130827.md`, `prev_rewrite_report_20260404_130827.md`, `prev_DECISION_LOG_20260404_130827.md`, `prev_changelog_20260404_130827.md`
- `main.md`, `components.md`, `usage-guide.md`에서 legacy `main.md` section/appendix 참조가 남지 않았는지 `rg`로 확인
- 줄 수 확인: `main.md 111`, `components.md 71`, `usage-guide.md 85`

## Warnings Intentionally Left Unresolved

1. supporting reference 안의 platform count나 일부 세부 수치는 stale할 수 있다. 이번 작업은 thin/compact rewrite가 우선이었다
2. standalone CIV table은 제거됐지만, repo-wide invariant 자체는 guardrails와 key decisions에만 압축 보존돼 있다. 더 상세한 execution-level validation은 global main에 다시 복구하지 않는다

## Notable Deviation from Plan

- 계획상 supporting surface 안내는 짧은 링크 수준을 목표로 했지만, 실제로는 `Supporting Surfaces` 섹션을 별도로 남겼다. 본문 오염을 늘리지 않으면서 탐색 진입점을 분명히 하는 편이 유지보수에 유리하다고 판단했다
- `components.md`는 처음에는 도입부 보정만 계획했지만, 사용자 요청에 따라 compact catalog 단계까지 확장했다. 변경 전 계획 파일을 addendum으로 먼저 갱신했다

## Decision Preservation Check

- `SKILL.md` 중심 구조
- Claude/Codex dual bundle
- skill entrypoint + reusable agent split
- `_sdd/` artifact handoff
- AC-First + explicit verification
- producer-owned inline 2-phase writing
- reasoning-based `sdd-autopilot`
- thin global spec + execution-focused temporary spec
