# Spec Format Reference (Whitepaper Style)

Validation and preservation reference aligned with `docs/SDD_SPEC_DEFINITION.md`.
This is NOT a generation template. It defines what qualities and sections a rewrite must preserve or evaluate.

---

## 1) SDD Definition Lens

According to `docs/SDD_SPEC_DEFINITION.md`, a good SDD spec is a whitepaper-style single source of truth that explains:

- the problem and motivation
- the core design and logic flow
- the code grounding / implementation mapping
- the usage path and expected results
- the supporting reference information without letting reference sections replace the narrative

Presence alone is not enough. The rewrite should validate both section existence and explanation quality.

## 2) Expected Section Structure

| # | Section | Purpose | Required |
|---|---------|---------|----------|
| 1 | Background & Motivation | Problem, why this approach, core value proposition | Yes |
| 2 | Core Design | Key idea narrative, algorithm/logic flow with code excerpts, design rationale | Yes |
| 3 | Architecture Overview | System diagram, technology stack, high-level design | Yes |
| 4 | Component Details | Per-component purpose/why/responsibility/interface/source | Yes |
| 5 | Usage Guide & Expected Results | Scenario-based usage with expected outcomes | Yes |
| 6 | Data Models | Entity definitions, constraints, indexes | If applicable |
| 7 | API Reference | Endpoints, request/response schemas | If applicable |
| 8 | Environment & Dependencies | Directory structure, dependencies, configuration | Yes |
| - | Appendix: Code Reference Index | All inline citations organized by file | If code excerpts exist |

## 3) Explanation Quality Checks

### 3.1 Problem / Motivation

- Does the spec explain what problem the project solves?
- Does it explain why this approach was chosen?
- Can a reader understand the repo purpose without reading code first?

### 3.2 Core Design Narrative

- Does the spec describe the main logic as a narrative or flow rather than only tables?
- Does it explain why the structure works?
- Are the key design decisions visible to a reviewer?

### 3.3 Code Grounding

- Does the explanation point to real code or `Source` mappings?
- Are inline citations preserved?
- If code excerpts exist, is the appendix index maintained?

### 3.4 Usage and Expected Results

- Does the spec show how the project is used?
- Does it describe expected outputs or observable outcomes?
- Are failure or exception paths covered where they matter?

### 3.5 Reference Balance

- Are API/data/config sections supporting the narrative rather than replacing it?
- Can the reader understand the product without starting from raw reference tables?

## 4) Preservation Rules

These elements MUST be preserved during spec rewrite/restructuring.

### Section Preservation

- **Background & Motivation** (§1): problem statement, approach rationale, and core value proposition must not be pruned or moved to appendix if already present
- **Core Design** (§2): key idea narrative and design rationale must remain in the main document if already present
- **Usage Guide & Expected Results** (§5): scenario-based expected results must not be removed if already present

### Code Excerpt Preservation

- **Inline citations**: `[filepath:functionName]` references in prose must be preserved during restructuring
- **Code blocks with citation headers**: blocks starting with `# [filepath:functionName]` must be kept intact
- **30-line rule**: code excerpts follow the 30-line rule (≤30 lines: full body; >30 lines: signature + core logic)
- **Code Reference Index**: the appendix table mapping files to citations must be updated if sections are moved

### Component Preservation

- **Why fields**: component-level `Why` fields must remain inline, not moved to `decision_log.md` or appendix
- **Source fields**: implementation file mappings must be preserved during section moves

## 5) Rewrite Boundary

`spec-rewrite` should:

- preserve what already exists
- improve clarity, structure, findability, and readability
- warn when whitepaper qualities are missing

`spec-rewrite` should NOT:

- invent missing whitepaper narrative out of thin air
- act as `spec-create` or `spec-upgrade`
- silently convert a weak spec into a richer spec without calling out that the content was missing
