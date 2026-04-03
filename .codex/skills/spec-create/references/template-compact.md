# SDD Global Spec Template (Compact)

> Canonical generation template for current SDD global specs. All spec-related skills should treat this as the default global-spec shape. It is intentionally thinner than the old architecture/component-inventory-heavy model.

---

## Writing Rules

> 아래 규칙은 모든 섹션에 적용된다.

**Document Metadata**:
- **Title**: 프로젝트 이름
- **Version**: X.Y.Z
- **Status**: Draft | In Review | Approved | Deprecated
- **Last Updated**: YYYY-MM-DD

**Narrative Rules**:
- 배경과 개념은 사람과 LLM이 같은 경계를 이해하도록 짧고 명료하게 쓴다.
- scope는 할 수 있는 것만이 아니라 책임 범위와 out-of-scope를 함께 고정한다.
- 본문은 decision-bearing structure 중심으로 유지한다.
- 구현 inventory나 단순 파일 목록은 reference 또는 appendix로 내린다.

**Code Reference Rules**:
- inline citation은 필요할 때만 사용한다: `[path/to/file.py:function_name]`
- strategic code map은 appendix-level hint다.
- strategic code map은 manual curated를 기본값으로 한다.
- entrypoint, invariant hotspot, extension point, change hotspot 같은 탐색 힌트를 우선한다.

**CIV Rules**:
- `Contract / Invariants / Verifiability`는 독립 필수 섹션이다.
- Contract ID는 `C1`, Invariant ID는 `I1`, Verifiability ID는 `V1` 형식을 사용한다.
- `Verification Method` enum: `test`, `review`, `runtime-check`, `manual-check`
- 각 셀은 짧은 규범 문장으로 쓴다.

---

# <Project Name>

> One-line description of what this project is for

**Version**: X.Y.Z
**Last Updated**: YYYY-MM-DD
**Status**: Draft | In Review | Approved | Deprecated

## 1. 배경 및 high-level concept

### Problem

[이 프로젝트가 해결하는 문제]

### Why This Matters Now

[왜 이 문제가 중요한가]

### High-Level Concept

[이 프로젝트를 어떤 관점과 아이디어로 이해해야 하는가]

### Alternatives Considered

| Approach | Why Considered | Why Not Chosen |
|----------|----------------|----------------|
| ... | ... | ... |

## 2. Scope / Non-goals / Guardrails

### In Scope

- ...

### Non-goals

- ...

### Guardrails

- ...

## 3. 핵심 설계와 주요 결정

### Core Design

[핵심 아이디어와 유지해야 할 구조]

### Key Decisions

| Decision | Why | What Must Stay True |
|----------|-----|---------------------|
| ... | ... | ... |

## 4. Contract / Invariants / Verifiability

### Contract

| ID | Subject | Inputs/Outputs | Preconditions | Postconditions | Failure Guarantees |
|----|---------|----------------|---------------|----------------|--------------------|
| C1 | ... | ... | ... | ... | ... |

### Invariants

| ID | Scope | Invariant | Why It Matters |
|----|-------|-----------|----------------|
| I1 | ... | ... | ... |

### Verifiability

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, I1 | review | ... |

## 5. 사용 가이드 & 기대 결과

### Scenario: [Name]

**Setup**: ...

**Action**: ...

**Expected Result**: ...

## 6. Decision-bearing structure

- 시스템 경계: ...
- ownership: ...
- cross-component contract: ...
- extension point: ...
- invariant hotspot: ...

## 7. 참조 정보

### Data Models

[조건부]

### API Reference

[조건부]

### Environment & Dependencies

[조건부]

## Appendix A. Strategic Code Map

| Kind | Path / Symbol | Why It Matters |
|------|----------------|----------------|
| Entrypoint | `...` | ... |
| Invariant Hotspot | `...` | ... |
| Extension Point | `...` | ... |
| Change Hotspot | `...` | ... |

## Appendix B. Related Docs & Code References

- ...

---

## Modular Spec Guide

| 규모 | 구조 |
|------|------|
| 소규모 | `main.md` 단일 파일 |
| 중규모 | `main.md` + supporting reference files |
| 대규모 | `main.md` + domain files/directories |

global spec core는 항상 `1~6`을 유지한다. `7`과 appendices는 필요할 때만 추가한다.
