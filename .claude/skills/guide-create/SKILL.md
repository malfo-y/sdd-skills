---
name: guide-create
description: This skill should be used when the user asks to "guide create", "create guide", "feature guide", "write guide", "가이드 작성", "기능 가이드", "가이드 문서 만들어줘", or wants to generate an implementation/review guide document for a specific feature from spec and code context.
version: 1.0.0
---

# Guide Create - Feature Guide Generator

| Workflow | Position | When |
|----------|----------|------|
| Any | Standalone | 기능별 구현/리뷰 가이드 문서 생성 |
| Any | Post-spec-create | 스펙 작성 후 구현 착수 전 가이드 정리 |

## Overview

The `guide-create` skill generates a feature-focused guide document for implementation and review work.
It reads `_sdd/spec/` as the primary source of truth, inspects related code as supporting evidence, and writes a practical guide under `_sdd/guides/`.

This v1 scope is intentionally narrow:

- **Target type**: feature only
- **Mode**: non-interactive by default
- **Primary use**: implementation/review guidance, not spec editing

Use this skill when the user wants a document that explains how a feature should be built, checked, and referenced without modifying the spec itself.

## Hard Rules

1. **Spec and code are read-only**: Never modify `_sdd/spec/`, application code, configuration files, or tests.
2. **Allowed outputs are limited**: You may create or replace only:
   - `_sdd/guides/guide_<slug>.md`
   - `_sdd/guides/prev/PREV_guide_<slug>_<timestamp>.md`
3. **Feature-only in v1**: Do not create component guides in this version.
4. **Non-interactive by default**: Infer missing details with deterministic defaults. Do not ask follow-up questions unless the user explicitly requests discussion.
5. **Spec-first grounding**: Treat `_sdd/spec/` as the primary source. Use code only to refine implementation detail, naming, file references, and symbol references.
6. **No fake certainty**: If evidence is incomplete, state assumptions or unknowns explicitly in the guide.
7. **Per-feature output**: If multiple features are detected, generate one guide file per feature instead of combining them into a single document.
8. **Backup before overwrite**: If the target guide already exists, create a timestamped backup in `_sdd/guides/prev/` before writing the new file.
9. **Language rule**: 기존 스펙/문서의 언어를 따른다. 사용자 명시 지정 시 해당 언어 사용. 새 프로젝트(기존 스펙 없음)는 한국어 기본.

## When to Use This Skill

- When the user wants a **feature implementation guide**
- When the user wants a **feature review checklist document**
- When a feature exists in spec but needs a clearer execution document
- When a team wants a derived guide without changing the SSOT spec
- When implementation or review work would benefit from a feature-specific rules/checklist/example document

### Trigger Phrases

Examples of requests that should trigger this skill:

- "guide create"
- "create guide"
- "feature guide"
- "write guide for this feature"
- "가이드 작성"
- "기능 가이드"
- "가이드 문서 만들어줘"
- "이 기능 구현 가이드 써줘"
- "이 스펙 기준으로 리뷰 가이드 정리해줘"

## Input Sources

### Primary Sources

1. **User conversation**
   - feature name
   - target scope
   - explicit constraints
2. **Spec documents**
   - `_sdd/spec/<project>.md`
   - `_sdd/spec/main.md`
   - linked or split sub-specs under `_sdd/spec/`

### Supporting Sources

3. **Relevant code**
   - source files that implement or partially implement the feature
   - tests that reveal intended behavior
   - interfaces, types, or schemas referenced by the feature
4. **Optional execution context**
   - `_sdd/env.md` when command or validation context is relevant

### Exclusions

- Ignore generated or backup documents such as:
  - `_sdd/guides/prev/PREV_*.md`
  - `_sdd/spec/prev/PREV_*.md`
  - `_sdd/spec/SUMMARY.md`

## Process

### Step 1: Identify the Target Feature

**Tools**: `Read`, `Glob`, `Grep`, `Bash (read-only)`

1. Parse the user request and detect target feature candidates.
2. If multiple features are requested, keep all candidates and plan one output file per feature.
3. Normalize each output name to an English slug for `guide_<slug>.md`.
4. Determine the user's active language for the output.

### Step 2: Locate and Validate Spec Context

**Tools**: `Read`, `Glob`, `Grep`

1. Find the main spec in `_sdd/spec/`.
2. If the spec is split, follow linked or convention-based sub-specs relevant to the feature.
3. Extract the most relevant feature description, related sections, constraints, and acceptance-style language.
4. If no usable spec exists:
   - `AskUserQuestion`으로 사용자에게 선택지 제공 (spec-create 실행 / 스펙 없이 Low 신뢰도로 계속)

> **Decision Gate 2→3**: See `references/tool-and-gates.md` § Gate 2→3: Spec Grounding

### Step 3: Gather Code Evidence

**Tools**: `Grep`, `Glob`, `Read`, `Bash (read-only)`

1. Search for related implementation files, tests, interfaces, schemas, and symbols.
2. Capture only evidence that helps make the guide actionable:
   - file paths
   - function/class/component/type names
   - test cases or existing patterns
3. Distinguish between:
   - confirmed implementation behavior
   - partially implemented behavior
   - spec-only intended behavior

### Step 4: Resolve Gaps with Deterministic Defaults

**Tools**: deterministic defaults (non-interactive)

When information is missing, fill gaps conservatively:

- **Feature name unclear**: derive from the most explicit spec heading or user phrase
- **User value unclear**: summarize from the goal/problem statement in spec
- **Implementation rule unclear**: prefer existing codebase conventions over generic best practice
- **Example weak**: create one positive example grounded in the spec and mark assumptions
- **Reference incomplete**: include the best available file/section references and explicitly mark unknown symbols

Never invent confirmed behavior that is unsupported by spec or code.

### Step 5: Generate the Guide Document

**Tools**: write output only

Write one guide per feature using the required structure from `references/output-format.md`.

Required sections:

1. **설명 / Explanation**
   - feature purpose
   - user value
   - scope
   - prerequisites or dependencies
2. **규칙 / Rules**
   - implementation rules
   - interface/API rules
   - state/error/data handling rules
3. **체크리스트 / Checklist**
   - before implementation
   - during implementation
   - before review or completion
4. **예시 / Examples**
   - at least one positive example
   - include anti-patterns when evidence supports them

Optional appendix:

- spec references with section names
- code references with file + symbol names
- assumptions / open points

### Step 6: Save with Backup Semantics

**Tools**: `Bash (mkdir -p, cp/mv)`, `Write`

For each feature guide:

1. Ensure `_sdd/guides/` exists.
2. If target file exists:
   - ensure `_sdd/guides/prev/` exists
   - create `PREV_guide_<slug>_<timestamp>.md`
3. Write the new `guide_<slug>.md`
4. Report the generated path(s) to the user

## Output Format

### File Location

- `_sdd/guides/guide_<slug>.md`

### Required Document Schema

```markdown
# 기능 가이드: <feature>

**생성일**: YYYY-MM-DD
**입력 소스**: [conversation/spec/code]
**대상 기능**: <feature>
**신뢰도**: High/Medium/Low

## 설명
...

## 규칙
...

## 체크리스트
...

## 예시
...

## 부록 (선택)
...
```

Full formatting details, slug rules, backup rules, and reference notation rules are defined in `references/output-format.md`.

## Error Handling

| Situation | Response |
|----------|----------|
| `_sdd/spec/` missing | `AskUserQuestion`으로 사용자에게 선택지 제공 (spec-create 실행 / 스펙 없이 Low 신뢰도로 계속) |
| Main spec not found | `AskUserQuestion`으로 사용자에게 선택지 제공 (spec-create 실행 / 스펙 없이 Low 신뢰도로 계속) |
| Feature is too ambiguous | Use the strongest available spec phrasing and record assumptions |
| Code evidence is missing | Generate a spec-grounded guide and mark code references as unavailable |
| Multiple features requested | Generate separate guide files per feature |
| Existing guide file found | Backup to `_sdd/guides/prev/` before overwriting |
| Mixed language signals | 기존 스펙/문서의 언어를 따른다. 사용자 명시 지정 시 해당 언어 사용. 새 프로젝트는 한국어 기본. |

## Additional Resources

- `references/output-format.md` — required guide structure and notation rules
- `references/tool-and-gates.md` — tool mapping, decision gates, and context management
- `examples/feature-guide-example.md` — sample output (Medium confidence, spec+code mixed)
- `examples/feature-guide-example-high.md` — sample output (High confidence, spec+code fully confirmed)
- `examples/feature-guide-example-low.md` — sample output (Low confidence, spec-only, no code evidence)
