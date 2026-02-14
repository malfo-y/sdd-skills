---
name: spec-rewrite
description: This skill should be used when the user asks to "rewrite spec", "refactor spec", "simplify spec", "split spec into files", "clean up spec", "review spec quality", or equivalent phrases indicating they want to reorganize an overly long/complex spec by pruning noise, splitting into hierarchical files, and explicitly listing ambiguities/problems.
---

# Spec Rewrite - Restructure Long or Complex Specs

Rewrite long or complex specs into a clearer structure by pruning unnecessary content (delete or move to appendix), splitting into hierarchical files, and explicitly documenting ambiguities and quality issues.

## Overview

This skill treats `_sdd/spec/` as a documentation refactoring target, not a feature-expansion task.

Primary goals:
1. Remove low-value content or move it to appendices
2. Split content into multiple files with a clear hierarchy
3. Explicitly report ambiguities, conflicts, and missing decisions

## When to Use This Skill

- The spec is too long to scan and maintain effectively
- Core sections are mixed with logs, verbose historical notes, or repeated details
- Topic-based separation is needed, but the current file layout is flat or unclear
- Spec quality needs cleanup before implementation planning starts

## Input Sources

### Primary
- `_sdd/spec/main.md` or `_sdd/spec/<project>.md`

### Secondary
- Sub-spec files linked from the main spec
- `_sdd/implementation/` outputs (plan/progress/review) for ambiguity validation
- `_sdd/spec/DECISION_LOG.md` (if present, for preserving rationale context)

## Rewrite Process

### Step 1: Diagnose Document Quality

First identify structural quality issues in the current spec.

- Section length imbalance (single section dominates document size)
- Duplicated explanations, tables, or checklists
- Out-of-scope content (ops logs, temporary notes, long historical narratives)
- Broken links, inconsistent filenames, missing references
- Ambiguous wording ("as needed", "fast", "appropriately")
- Missing acceptance or completion criteria

### Step 2: Propose Rewrite Plan First

Present a rewrite plan before making changes.

```markdown
## Spec Rewrite Plan

**Target**: `_sdd/spec/<project>.md`

### 1) Keep in Main
- [Core goal/scope/architecture summary]

### 2) Move to Appendix
- [Sections to move and rationale]

### 3) Split Map (Hierarchical)
- `_sdd/spec/<project>.md` (index)
- `_sdd/spec/<project>/01-overview.md`
- `_sdd/spec/<project>/02-architecture.md`
- `_sdd/spec/<project>/03-components.md`
- `_sdd/spec/<project>/04-api.md`
- `_sdd/spec/<project>/appendix.md`

### 4) Ambiguities / Risks to Resolve
- [Ambiguous/conflicting/missing items]
```

For large structural changes (file splits and bulk moves), get user confirmation first.

### Step 3: Create Safety Backups

For every existing file you modify, create a backup under `_sdd/spec/prev/` using `prev/PREV_<filename>_<timestamp>.md` (create `_sdd/spec/prev/` first if missing).

### Step 4: Prune and Appendix Migration

Rules:
- Keep only decision-driving and execution-critical content in the main document
- Move long examples, verbose logs, and reference-only material to appendix (`appendix.md` or `<project>_APPENDIX.md`)
- Keep one canonical version of repeated content and replace duplicates with links
- Do not drop important "why" context silently; preserve it in `_sdd/spec/DECISION_LOG.md` when needed

### Step 4.5: Preserve Decision Context

If rewriting removes narrative sections that contain meaningful rationale:
- Add a concise entry to `_sdd/spec/DECISION_LOG.md`
- Keep the rewritten main spec concise, and keep detailed rationale in the decision log
- Do not create additional side documents by default; keep rationale tracking in `DECISION_LOG.md`

### Step 5: Hierarchical Split

Default structure:

```
_sdd/spec/
├── <project>.md                  # index (summary + link hub)
└── <project>/
    ├── 01-overview.md
    ├── 02-architecture.md
    ├── 03-components.md
    ├── 04-interfaces.md
    ├── 05-operational-guides.md
    └── appendix.md
```

Rules:
- Keep only concise summaries and links in the index file
- Each sub-file should have a single topic responsibility
- Standardize relative links and fix all broken links
- Keep section and filename naming conventions consistent

### Step 6: Ambiguity and Problem Reporting

Always call out these issue types explicitly.

- **Ambiguous Requirement**: requirement has multiple valid interpretations
- **Missing Acceptance Criteria**: no clear done condition
- **Conflicting Statements**: contradictory rules inside the spec
- **Undefined Ownership**: no clear owner/team/component responsibility
- **Outdated Claim**: statement no longer matches code or recent decisions

If needed, add `## Open Questions` to the index and keep detailed items in the report file.

## Output Format

### 1) Rewritten Spec Files

- List of rewritten files
- List of newly created sub-files
- List of sections moved to appendix

### 2) Rewrite Report

Create or update `_sdd/spec/REWRITE_REPORT.md` with:

```markdown
## Rewrite Summary
- Target document:
- Execution timestamp:
- Key changes:

## What Was Pruned or Moved
- [item] -> [appendix/file]

## File Split Map
- [index + sub-file tree]

## Ambiguities and Issues
- [Priority] [Type] description
- Suggested resolution

## Decision Log Additions
- [Entry title] (if any)
- Why this was recorded
```

## Quality Checklist

- Can a reader understand goal/scope/acceptance criteria quickly from the index?
- Are detailed sections separated by topic into dedicated files?
- Are links and paths valid?
- Are ambiguities/conflicts/missing items explicitly documented?
- Is unnecessary duplication removed?
- Is essential rationale preserved (in spec or `_sdd/spec/DECISION_LOG.md`)?

## Language Preference

- Keep the existing spec language by default
- For mixed-language specs, follow the index document language
- If requested by the user, normalize output to a single language

## Additional Resources

### Reference Files
- `references/rewrite-checklist.md` - diagnosis/splitting/report checklist

### Example Files
- `examples/rewrite-report.md` - sample rewrite result report

## Integration with Other Skills

- **spec-update-done**: validate against code-level reality
- **spec-summary**: regenerate summary after rewrite
- **implementation-plan**: plan implementation from cleaned spec
