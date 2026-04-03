# Spec Rewrite Plan

## Rewrite Context

- **대상**: `_sdd/spec/main.md` (v3.8.2, 1206줄, 32,933 토큰)
- **보조**: `_sdd/spec/DECISION_LOG.md` (452줄, 변경 없음)
- **실행일**: 2026-04-03
- **규모 판정**: 중규모 (500-1500줄) → 인덱스 + 컴포넌트 파일 구조 적용

## Diagnosis Summary

| Metric | Before | Target | 근거 |
|--------|--------|--------|------|
| Component Separation | 2 | 3 | 20+ 컴포넌트가 단일 파일에 밀집. 분리하면 각 컴포넌트를 대표 파일에서 관리 가능 |
| Findability | 2 | 3 | TOC 존재하지만 1206줄 단일 파일에서 스크롤 필요. 파일 분리로 2-hop 이내 탐색 가능 |
| Repo Purpose Clarity | 3 | 3 | §1이 명확하고 간결. 유지 |
| Architecture Clarity | 3 | 3 | 시스템 다이어그램, 데이터 흐름, 워크플로우 모두 명확. 유지 |
| Usage Completeness | 3 | 3 | 4개 시나리오 + Setup/Action/Expected Result. 유지 |
| Environment Reproducibility | 2 | 2 | env.md 참조 의존. rewrite 범위 밖 (content 보강은 spec-update-todo/spec-upgrade 역할) |
| Ambiguity Control | 2 | 2 | Hard Rules 명확. 일부 숫자 불일치(21개/20개) 존재하나 실제 구조 확인 필요 — content 수정은 scope 밖 |
| Why/Decision Preservation | 3 | 3 | 모든 컴포넌트에 Why 필드, Design Rationale 테이블, DECISION_LOG.md. 유지 |

**종합**: 현재 스펙은 whitepaper 기준으로 §1-§8 모두 양호. 주요 이슈는 **구조적 비대함**(단일 파일 1206줄)이며, content 품질은 이미 높다.

## Keep in Main

main.md를 인덱스로 전환하여 아래를 인라인 유지:

- §1 Background & Motivation (lines 22-68, ~47줄)
- §2 Core Design (lines 70-239, ~170줄) — Key Idea, 구조 다이어그램, Design Patterns, Common Hard Rules, Design Rationale
- §3 Architecture Overview (lines 241-444, ~204줄) — System Diagram, Loading Structure, Data Flow, Workflow, Artifact Map, Tech Stack
- §4 Category Overview 테이블 (lines 449-475, ~27줄) — 인덱스 역할의 요약 테이블만 유지
- §4 Component links → 분리된 파일로 링크

## Move / Prune / Appendix

| 대상 | 현재 위치 | 이동 | 이유 |
|------|----------|------|------|
| Component Details 상세 (sdd-autopilot~spec-snapshot) | main.md:507-756 | `_sdd/spec/components.md` | ~250줄의 컴포넌트 테이블을 분리하여 main 경량화 |
| Usage Guide & Expected Results | main.md:760-839 | `_sdd/spec/usage-guide.md` | ~80줄. 별도 파일로 분리하면 온보딩/참조 시 직접 접근 가능 |
| Changelog (v2.1.0~v3.8.2) | main.md:1057-1206 | `_sdd/spec/logs/changelog.md` | ~150줄의 역사 기록. main에서 제거하고 logs/로 이동 |
| 해결 완료 이슈 (~~strikethrough~~) | main.md:960-1002 | 삭제 (changelog에 이미 기록됨) | 해결된 이슈는 changelog에서 추적 가능. 본문 중복 제거 |
| Code Reference Index | main.md:1012-1054 | `_sdd/spec/components.md` 하단에 병합 | 코드 참조 인덱스는 컴포넌트 상세와 함께 관리하는 것이 자연스러움 |

## Split Map

```
_sdd/spec/
├── main.md              # 인덱스 (~530줄 예상)
│   ├── §1 Background & Motivation (인라인)
│   ├── §2 Core Design (인라인)
│   ├── §3 Architecture Overview (인라인)
│   ├── §4 Category Overview 요약 테이블 + 링크
│   ├── §5 Usage Guide 링크
│   ├── §7 Environment & Dependencies (인라인)
│   └── §8 Identified Issues — 활성 이슈만 (3개)
├── components.md        # 신규: §4 상세 + Appendix Code Reference Index (~320줄 예상)
├── usage-guide.md       # 신규: §5 Usage Guide & Expected Results (~90줄 예상)
├── DECISION_LOG.md      # 기존 유지 (변경 없음)
├── logs/
│   ├── changelog.md     # 신규: main에서 이동한 Changelog
│   ├── spec-rewrite-plan.md   # 이 파일
│   └── rewrite_report.md      # rewrite 후 생성
└── prev/                # 백업
```

## Metric Improvement Rationale

- **Component Separation (2→3)**: Component Details를 `components.md`로 분리하면 각 컴포넌트가 전용 파일의 대표 섹션에 귀속
- **Findability (2→3)**: main.md가 인덱스 역할로 경량화되면 필요한 정보를 2-hop 이내에 도달 가능 (main → components.md → 컴포넌트 섹션)
- **나머지 metric**: 이미 2-3점이며 content 변경 없이 구조 개선만으로는 추가 향상 제한적

## Ambiguities / Risks / Unresolved Decisions

1. **스킬 수 불일치**: main.md 내에서 "21개 스킬"과 "20개 스킬" 표현이 혼재. 이는 content 정합성 이슈로 rewrite scope 밖 (spec-update-done 또는 별도 content 수정 필요)
2. **Environment Reproducibility**: env.md 참조 의존은 구조 rewrite로 해결할 수 없음. 별도 content 보강 필요

## Whitepaper Warnings

- 모든 §1-§8 핵심 섹션이 존재하고 양호함. 누락된 whitepaper narrative 없음.
- §6 Data Models / API Reference는 N/A (마크다운 기반 스킬 프로젝트 특성상 해당 없음)

## Rewrite Target Files

1. `_sdd/spec/main.md` — 인덱스로 재구성
2. `_sdd/spec/components.md` — 신규 생성 (Component Details + Code Reference Index)
3. `_sdd/spec/usage-guide.md` — 신규 생성 (Usage Guide & Expected Results)
4. `_sdd/spec/logs/changelog.md` — 신규 생성 (Changelog 이동)

## Execution Order

1. 백업: `_sdd/spec/prev/prev_main.md_20260403_*.md`
2. `_sdd/spec/logs/changelog.md` 생성 (main.md에서 Changelog 추출)
3. `_sdd/spec/components.md` skeleton → fill (Component Details + Code Reference Index)
4. `_sdd/spec/usage-guide.md` skeleton → fill
5. `_sdd/spec/main.md` 재구성 (분리된 섹션 제거, 링크 추가, 이슈 정리)
6. 링크 검증
7. `_sdd/spec/logs/rewrite_report.md` 작성

## Plan Deviation Rules

- split map이나 prune 기준이 크게 변경되면 이 파일을 먼저 갱신 후 진행
- 실행 중 발견된 deviation은 rewrite_report.md에 기록

## Approval Status

**승인됨** — 2026-04-03 사용자 확인 완료. 실행 완료.
