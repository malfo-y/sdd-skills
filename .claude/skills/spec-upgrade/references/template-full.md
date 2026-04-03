# Complete Global Spec Template

This is the richer template for current SDD global specs. Use it when the project is large enough that the compact template would become ambiguous, but keep the same canonical section order and philosophy.

---

# <Project Name>

> One-line description of what this project is for

**Version**: X.Y.Z
**Last Updated**: YYYY-MM-DD
**Status**: Draft | In Review | Approved | Deprecated

## Table of Contents

- [1. Background & High-Level Concept](#1-background--high-level-concept)
- [2. Scope / Non-goals / Guardrails](#2-scope--non-goals--guardrails)
- [3. Core Design & Key Decisions](#3-core-design--key-decisions)
- [4. Contract / Invariants / Verifiability](#4-contract--invariants--verifiability)
- [5. Usage Guide & Expected Results](#5-usage-guide--expected-results)
- [6. Decision-Bearing Structure](#6-decision-bearing-structure)
- [7. Reference Information](#7-reference-information)
- [Appendix A. Strategic Code Map](#appendix-a-strategic-code-map)
- [Appendix B. Related Docs & Code References](#appendix-b-related-docs--code-references)

---

## 1. Background & High-Level Concept

### Problem Statement

[What problem exists today and what pain or cost does it create?]

### Why This Matters Now

[Why the problem is worth solving now, not later.]

### High-Level Concept

[Describe the framing or insight that makes this project coherent.]

### Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| Proposed approach | ... | ... | Chosen |
| Alternative A | ... | ... | Rejected: ... |
| Alternative B | ... | ... | Rejected: ... |

### Core Value

[One concise paragraph explaining the key value delivered.]

---

## 2. Scope / Non-goals / Guardrails

### In Scope

- ...
- ...

### Non-goals

- ...
- ...

### Guardrails

- ...
- ...

### Scope Notes

[Clarify boundaries that may be confused with adjacent work.]

---

## 3. Core Design & Key Decisions

### Core Design Narrative

[Explain the main structure or flow that must be preserved.]

### Key Decisions

| Decision | Why It Was Chosen | What Must Stay True |
|----------|-------------------|---------------------|
| ... | ... | ... |

### Failure-Sensitive Decisions

| Area | Sensitive Assumption | Consequence If Broken |
|------|----------------------|-----------------------|
| ... | ... | ... |

---

## 4. Contract / Invariants / Verifiability

### Contract

| ID | Subject | Inputs/Outputs | Preconditions | Postconditions | Failure Guarantees |
|----|---------|----------------|---------------|----------------|--------------------|
| C1 | ... | ... | ... | ... | ... |
| C2 | ... | ... | ... | ... | ... |

### Invariants

| ID | Scope | Invariant | Why It Matters |
|----|-------|-----------|----------------|
| I1 | ... | ... | ... |
| I2 | ... | ... | ... |

### Verifiability

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, I1 | test | ... |
| V2 | C2 | review | ... |

`Verification Method`는 `test`, `review`, `runtime-check`, `manual-check` 중 하나 이상을 사용한다.

---

## 5. Usage Guide & Expected Results

### Scenario: [Primary Flow]

**Setup**: ...

**Action**: ...

**Expected Result**: ...

### Scenario: [Failure or Edge Case]

**Setup**: ...

**Action**: ...

**Expected Result**: ...

---

## 6. Decision-Bearing Structure

### System Boundary

[What is inside and outside the system boundary?]

### Ownership

| Area | Owner / Responsible Layer | Why |
|------|---------------------------|-----|
| ... | ... | ... |

### Cross-Component Contracts

| Boundary | Contract | Risk If Broken |
|----------|----------|----------------|
| ... | ... | ... |

### Extension Points

- ...

### Invariant Hotspots

- ...

---

## 7. Reference Information

### Data Models

[Only if materially useful.]

### API Reference

[Only if materially useful.]

### Environment & Dependencies

| Category | Item | Why It Matters |
|----------|------|----------------|
| Runtime | ... | ... |
| External | ... | ... |

### Configuration

| Key | Required | Purpose |
|-----|----------|---------|
| ... | ... | ... |

---

## Appendix A. Strategic Code Map

Use this only when it materially improves navigation. Keep it manual curated and selective.

| Kind | Path / Symbol | Why It Matters | When to Read It |
|------|----------------|----------------|-----------------|
| Entrypoint | `...` | ... | ... |
| Invariant Hotspot | `...` | ... | ... |
| Extension Point | `...` | ... | ... |
| Change Hotspot | `...` | ... | ... |

## Appendix B. Related Docs & Code References

- `...`

---

## Temporary Spec Note

Global spec과 별도로, 실행 청사진이 필요한 변경 작업은 temporary spec을 사용한다. Temporary spec의 canonical shape는 아래와 같다.

1. `Change Summary`
2. `Scope Delta`
3. `Contract/Invariant Delta`
4. `Touchpoints`
5. `Implementation Plan`
6. `Validation Plan`
7. `Risks / Open Questions`
