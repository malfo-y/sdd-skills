# Spec Format Reference (Whitepaper Style)

Checklist-style reference for the expected spec section structure and preservation rules.
This is NOT a generation template — it defines "what sections should exist" for validation and preservation.

---

## Expected Section Structure

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

## Preservation Rules

These elements MUST be preserved during spec rewrite/restructuring:

### Section Preservation
- **Background & Motivation** (§1): Problem statement, approach rationale, and core value proposition must not be pruned or moved to appendix
- **Core Design** (§2): Key idea narrative and design rationale must remain in main document
- **Usage Guide & Expected Results** (§5): Scenario-based expected results must not be removed

### Code Excerpt Preservation
- **Inline citations**: `[filepath:functionName]` references in prose must be preserved during restructuring
- **Code blocks with citation headers**: Blocks starting with `# [filepath:functionName]` must be kept intact
- **30-line rule**: Code excerpts follow the 30-line rule (≤30 lines: full body; >30 lines: signature + core logic)
- **Code Reference Index**: The appendix table mapping files to citations must be updated if sections are moved

### Component Preservation
- **Why fields**: Component-level "Why" fields must remain inline (not moved to DECISION_LOG or appendix)
- **Source fields**: Implementation file mappings must be preserved during section moves
