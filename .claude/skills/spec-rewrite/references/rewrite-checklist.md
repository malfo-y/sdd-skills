# Spec Rewrite Checklist

Checklist to reduce omissions when turning an existing spec into an exploration-first spec.

## 1) Pre-Check

- [ ] Identify the main target spec file (`_sdd/spec/main.md` or `_sdd/spec/<project>.md`)
- [ ] Collect linked sub-spec files
- [ ] Confirm backup policy (`_sdd/spec/prev/PREV_<filename>_<timestamp>.md`)
- [ ] Load `_sdd/spec/DECISION_LOG.md` if present
- [ ] Check whether the main spec already uses stable anchors (`Goal`, `Architecture Overview`, `Component Details`, `Open Questions`)
- [ ] Check whether the current spec is hard to navigate, not merely long

## 2) Navigation Diagnosis (SDD 탐색 품질 기준)

- [ ] Can a newcomer understand the project purpose within 5 minutes?
- [ ] Is system boundary visible?
- [ ] Is there a repository map?
- [ ] Is there a runtime map?
- [ ] Is there a component index?
- [ ] Are major components tied to real paths or symbols?
- [ ] Are change/debug entry points visible?
- [ ] Are Change Recipes present (변경 지향성)?
- [ ] Are invariants and risks visible (계약 가시화)?
- [ ] Are unknowns separated into `Open Questions`?
- [ ] 탐색 가능성: 기능이나 책임이 어디에 있는지 빠르게 찾을 수 있는가?
- [ ] 변경 지향성: 변경 시작 지점과 영향 범위가 명확한가?
- [ ] 계약 가시화: 계약, 상태 전이, 불변 조건이 묻혀 있지 않은가?

## 3) 앵커 섹션 검증

- [ ] `Goal` 섹션이 존재하고 Project Snapshot / Key Features / Non-Goals를 포함하는가?
- [ ] `Architecture Overview` 섹션이 존재하고 System Boundary / Repository Map / Runtime Map을 포함하는가?
- [ ] `Component Details` 섹션이 존재하고 Component Index를 포함하는가?
- [ ] `Open Questions` 섹션이 존재하고 미확인 사항이 분리되어 있는가?
- [ ] 선택 섹션(`Environment & Dependencies`, `Identified Issues & Improvements`, `Usage Examples`)은 가치가 있을 때만 유지되는가?

## 4) Rewrite Target Shape

Keep these in the main spec:
- Goal -> Project Snapshot / Key Features / Non-Goals
- Architecture Overview -> System Boundary / Repository Map / Runtime Map
- Component Details -> Component Index + brief component summaries
- Open Questions

Add these only when materially relevant:
- Architecture Overview -> Technology Stack / Cross-Cutting Invariants
- Environment & Dependencies
- Identified Issues & Improvements
- Usage Examples -> Running / Common Operations / Common Change Paths

Split out by responsibility when needed:
- auth
- billing
- jobs
- ingestion
- api

Move out of the main flow only when necessary:
- long execution logs
- repeated tables
- reference-only detail
- low-value historical narrative

## 5) Split Rules

- [ ] Prefer `main.md + <component>.md` over numbered topic files
- [ ] Each split file has one responsibility
- [ ] Every split file is reachable from the main spec
- [ ] Links are valid
- [ ] Naming is consistent
- [ ] Appendix files exist only when truly useful

## 6) Rationale and Unknowns

- [ ] Important removed rationale is preserved in `_sdd/spec/DECISION_LOG.md`
- [ ] Unverified claims are moved to `Open Questions`
- [ ] No uncertain statement is left as confident prose

## 7) Exit Criteria (SDD 품질 포함)

- [ ] The main spec works as a 5-minute entry point
- [ ] Repository Map exists
- [ ] Runtime Map exists
- [ ] Component Index exists
- [ ] Change Recipes 또는 변경 진입점이 존재
- [ ] Important areas include real paths or symbols
- [ ] Tests/logs/debug entry points are discoverable
- [ ] Duplication is reduced
- [ ] Main risks and invariants are visible
- [ ] Empty optional sections and low-value metadata were removed
- [ ] The main spec stays compact enough for one focused read
- [ ] The rewritten spec is easier to understand and easier to modify against
- [ ] 앵커 섹션(`Goal`, `Architecture Overview`, `Component Details`, `Open Questions`)이 보존됨
- [ ] 실제 경로가 주요 컴포넌트에 연결되어 있음
