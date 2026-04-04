# Spec Rewrite Plan

## Rewrite Context

- **대상**: `_sdd/spec/main.md` (v4.0.1, 257줄)
- **보조 수정**: `_sdd/spec/components.md`, `_sdd/spec/usage-guide.md`
- **근거 기준**: `docs/SDD_SPEC_DEFINITION.md`, `docs/SDD_WORKFLOW.md`, `.codex/skills/spec-rewrite/references/spec-format.md`
- **실행일**: 2026-04-04
- **목표**: current global spec을 `개념 + 경계 + 결정` 중심의 thin 기준 문서로 더 압축

### Addendum: components.md compact rewrite

- **추가 대상**: `_sdd/spec/components.md` (284줄)
- **추가 목표**: reference-only surface에 맞게 `Purpose / Why / Source` 중심 catalog로 압축
- **추가 범위**: component별 Input/Output/Process/완료 이력/세부 제약을 정리하고, navigation-critical note만 남긴다

## Diagnosis Summary

| Metric | Before | Target | 근거 |
|--------|--------|--------|------|
| Component Separation | 3 | 3 | component inventory는 이미 `components.md`로 분리돼 있다 |
| Findability | 3 | 3 | 멀티파일 구조는 양호하다. 다만 main 본문 책임이 더 선명해져야 한다 |
| Repo Purpose Clarity | 3 | 3 | §1은 이미 간결하고 repo 목적을 잘 설명한다 |
| Boundary Clarity | 2 | 3 | 경계 정보는 있으나 standalone CIV/structure 표에 분산돼 있다 |
| Decision Preservation | 3 | 3 | 주요 결정과 rationale은 유지 가치가 높다 |
| Contamination Control | 1 | 3 | usage/verification/reference/code-map 성격의 내용이 global main body를 다시 두껍게 만들고 있다 |
| Canonical Fit | 1 | 3 | current definition은 3개 mandatory core를 요구하지만, 현행 main은 7개 섹션 + appendix 중심이다 |

## Keep in Main

main.md에 직접 남길 내용:

- repo 문제 정의와 high-level concept
- scope / non-goals / guardrails
- layered design, 유지해야 할 구조적 결정, 운영 제약
- supporting surface로 내려간 문서의 역할을 가리키는 짧은 안내

## Move / Prune / Absorb

| 대상 | 현재 위치 | 조치 | 이유 |
|------|----------|------|------|
| `Contract / Invariants / Verifiability` 독립 표 | `main.md` §4 | 삭제 후 guardrails / key decisions에 흡수 | definition 문서에서 standalone CIV table은 global 기본 코어가 아니다 |
| `사용 가이드 & 기대 결과` 요약 표 | `main.md` §5 | 본문에서 제거하고 `usage-guide.md` 링크만 유지 | usage/expected result는 supporting surface 성격이다 |
| `Decision-bearing structure` 독립 섹션 | `main.md` §6 | 핵심만 §3으로 흡수 | boundary/extension 판단은 남기되 별도 대형 표 구조는 제거 |
| `참조 정보`와 appendix code map | `main.md` §7, 부록 A/B | 본문에서 제거하고 supporting surface 링크로 축약 | reference/code-map은 global mandatory core가 아니다 |
| supporting file의 legacy section reference | `components.md`, `usage-guide.md` 도입부 | thin spec 기준에 맞게 문구 보정 | `main.md`가 더 이상 §5/§7/appendix 중심 구조가 아니게 된다 |
| component별 Input/Output/Process/완료 이력 상세 | `components.md` 각 섹션 | compact catalog로 축약 | reference-only surface에서 원문 재복제 비중이 과하다 |
| component별 wrapper/runtime 세부 | `components.md` 각 섹션 | `Notes` 열로 최소 보존 | 중요한 차이만 남기고 탐색성을 높인다 |

## Split Map

새 파일 분할은 하지 않는다. 역할만 더 선명히 한다.

- `_sdd/spec/main.md`: thin global spec core + supporting surface index
- `_sdd/spec/components.md`: reference-only component catalog + strategic code map
- `_sdd/spec/usage-guide.md`: scenario-oriented usage surface
- `_sdd/spec/DECISION_LOG.md`: rewrite 포함 구조 판단 이력
- `_sdd/spec/logs/rewrite_report.md`: 실행 결과 및 deviation 기록

## Metric Improvement Rationale

- **Boundary Clarity (2→3)**: CIV/structure 표의 반복을 걷어내고, repo-wide operating rule만 §2와 §3에 직접 남긴다
- **Contamination Control (1→3)**: usage/reference/code-map/verification 상세를 main body에서 제거해 mandatory core만 남긴다
- **Canonical Fit (1→3)**: 본문을 `Background / Scope / Core Design` 3개 축으로 재정렬한다
- **components Findability 유지**: component reference를 category-based compact table로 바꿔 필요한 항목을 더 빨리 찾게 한다

## Ambiguities / Risks / Unresolved Decisions

1. platform count 같은 세부 수치(`21 skills`, `19 skills`)는 supporting reference에서 stale할 수 있다. 이번 작업은 thin rewrite가 우선이며, 발견 시 최소 범위에서만 정리한다
2. 상세 verification evidence를 main에서 내리면, future maintainer가 supporting surface를 함께 읽어야 한다. 대신 definition 기준 적합성이 높아진다
3. global core 밖 상세를 어디까지 남길지 경계가 애매하면, 새 내용을 만들지 말고 더 얇은 쪽을 우선한다
4. `components.md`를 너무 얇게 만들면 entrypoint 차이나 wrapper 여부를 잃을 수 있으므로, 탐색에 필요한 runtime note는 남긴다

## Rewrite Target Files

1. `_sdd/spec/main.md`
2. `_sdd/spec/components.md`
3. `_sdd/spec/usage-guide.md`
4. `_sdd/spec/logs/spec-rewrite-plan.md`
5. `_sdd/spec/logs/rewrite_report.md`
6. `_sdd/spec/DECISION_LOG.md`

## Execution Order

1. 대상 파일 백업 생성
2. `main.md`를 thin global spec 구조로 재작성
3. `components.md`, `usage-guide.md` 도입부 정합성 보정
4. `components.md`를 compact catalog 구조로 재작성
5. 링크/경로/section responsibility 검증
6. `rewrite_report.md`와 `DECISION_LOG.md` 기록

## Plan Deviation Rules

- 새 supporting file이 꼭 필요하다고 판단되면, 먼저 이 계획 파일에 이유를 반영한 뒤 진행
- repo-wide 결정 보존을 위해 본문에 남긴 항목은 `rewrite_report.md`에 별도 기록
- 누락된 내용을 추정으로 채우지 않고 warning으로 남긴다
