# SDD Quick Start

## 1. What to remember first

1. The global spec is the repo-wide judgment layer.
2. The temporary spec is the execution blueprint for a change.
3. Do not force code-obvious detail into the global spec.
4. Put feature-level usage / contract / validation into temporary surfaces or guides.

## 2. Starting a new project

Start by fixing only these three parts in the global spec.

```markdown
## 1. Background and High-Level Concept
## 2. Scope / Non-goals / Guardrails
## 3. Core Design and Key Decisions
```

Move additional information into supporting docs only when needed.

## 3. Starting feature work

Use one of these:

- small change: implementation + review
- medium or larger change: feature draft or temporary spec
- ambiguous scope: discussion first

## 4. What not to put in the global spec

- feature-level expected result
- per-feature contract / validation detail
- complete usage guides
- exhaustive inventory
- explanations that are obvious from code

## 5. Where that information goes instead

- execution planning: temporary spec / implementation plan
- usage examples: guide / README
- environment detail: README / env docs
- navigation hints: appendix, review note, code comment

## 6. When reviewing

- for a global spec, check whether concept + boundaries + decisions are clear
- for a temporary spec, check whether delta and validation linkage are clear
- do not try to turn both documents into encyclopedias
