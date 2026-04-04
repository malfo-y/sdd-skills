# Summary Example

## Global Spec Summary

### Executive Summary
이 프로젝트의 global spec은 repo를 어떤 문제/경계/결정으로 읽어야 하는지 고정한다.

### Problem / High-Level Concept
- 배치 수집 파이프라인의 drift를 줄이기 위해 thin global spec + temporary execution model을 사용한다.

### Scope / Non-goals Snapshot
- in scope: repo-wide 판단 기준, shared guardrails
- out of scope: feature별 usage guide, exhaustive inventory

### Key Decisions / Guardrails
- global spec은 `개념 + 경계 + 결정`만 기본 코어로 본다.
- feature-level execution detail은 temporary spec에 둔다.

### Delegated-Out Information Note
- detailed validation, usage examples, and support references live in temporary specs, guides, or docs.

### Status / Issues / Next Steps
- status: 진행중
- next: consumer skill contract 반영 후 downstream sync
