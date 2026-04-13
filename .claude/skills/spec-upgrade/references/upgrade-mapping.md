# Upgrade Mapping

## Keep or Move

| Legacy Content | New Destination | Rule |
|----------------|-----------------|------|
| Problem / vision | Background & High-Level Concept | keep in global |
| Scope / non-goals | Scope / Non-goals / Guardrails | keep in global |
| Architecture rationale | Core Design & Key Decisions | keep only decision-bearing parts |
| Standalone CIV table | Guardrails / Key Decisions / Temporary Spec | keep only truly repo-wide rules in global |
| Usage guide | Guide / README / Temporary Spec | do not force into global core |
| Expected results | Guide / Temporary Spec / tests | keep near execution or user-facing context |
| Reference info | supporting docs | do not force into main body |
| Strategic code map | optional appendix | only if manual navigation hints are genuinely useful |
| Exhaustive inventory | code or supporting docs | remove from default global body |

## Upgrade vs Rewrite Boundary

Step 1 경계 판정을 빠르게 대조할 때만 사용한다. 별도 source-of-truth가 아니라 본문 Step 1의 보조 표다.

| Signal | Recommended Tool | Why |
|--------|------------------|-----|
| old sections need thinning into current model | `spec-upgrade` | canonical migration is the main task |
| inventory-heavy body must be reduced without major repartition | `spec-upgrade` | migration can handle the reduction |
| domain/topic repartition across multiple files is the main change | `spec-rewrite` | structure redesign is primary |
| migration requires saving rationale while moving large history/log blocks out of body | `spec-rewrite` | body/log placement is primary |
| role of index/supporting files must be re-authored, not just remapped | `spec-rewrite` | rewrite scope exceeds format upgrade |
