---
name: spec-summary
description: This skill should be used when the user asks to "summarize spec", "spec summary", "show spec overview", "스펙 요약", "스펙 개요", "show spec status", "스펙 현황", "project overview", "프로젝트 개요", "what's the current state", "현재 상태는", or wants a human-readable summary of the current specification for quick understanding.
---

# Specification Summary Generator

Generate a stakeholder-friendly summary from SDD spec documents and implementation evidence.

## Output

- Primary: `_sdd/spec/SUMMARY.md`
- Optional: `README.md` (only when user explicitly requests README sync)

## Inputs

### Required

- Main/index spec:
  - `_sdd/spec/<project>.md` (preferred)
  - `_sdd/spec/main.md` (legacy)

### Optional

- Linked sub-spec files from the index
- `_sdd/implementation/IMPLEMENTATION_PROGRESS*.md`
- `_sdd/implementation/IMPLEMENTATION_REVIEW.md`
- `_sdd/env.md` (only if runtime/test evidence is needed)

Always exclude generated backups:

- `_sdd/spec/SUMMARY.md`
- `_sdd/spec/prev/PREV_*.md`

## Workflow

### 1) Locate Summary Scope

- Identify the index/main spec.
- If multiple plausible index files exist, ask the user directly.
- If spec is split, follow links from the index and include linked sub-specs.

### 2) Extract Core Signals

Extract and normalize:

- Project goals and scope boundaries
- Key features and current status markers
- Architecture highlights (major components + responsibilities)
- Open issues / improvements
- Implementation progress signals (if files exist)

### 3) Compute Status Metrics

Use markers when present:

- `✅` completed
- `🚧` in progress
- `📋` planned
- `⏸️` on hold (exclude from completion denominator)

Completion formula:

`completed / (completed + in_progress + planned)`

If markers are missing, report `status unknown` instead of guessing.

### 4) Compose Summary

Follow the summary template contract in `references/summary-template.md`.

Required sections:

1. Executive Summary
2. Key Feature Explanations
3. Architecture at a Glance
4. Feature Status Dashboard
5. Open Issues & Improvements
6. Recommended Next Steps
7. Quick Reference

### 5) Write and Archive

- If `_sdd/spec/SUMMARY.md` exists, archive to `_sdd/spec/prev/PREV_SUMMARY_<timestamp>.md`.
- Write the new summary.
- Keep links and paths valid.

### 6) Optional README Sync

If requested:

- Update only summary-related portions.
- Avoid overwriting unrelated README sections.
- Note which sections were touched.

## Quality Gates

Before finalizing:

- Summary reflects current spec structure (including split specs).
- All claims are traceable to spec/progress/review evidence.
- Recommendations are prioritized and actionable.
- Ambiguities are stated explicitly.

## Error Handling

- No spec found: ask user to create/identify spec (typically via `spec-create`).
- Multiple candidate specs: ask user which index to use.
- Empty/minimal spec: generate minimal summary with explicit warning.

## Integration

- Upstream maintenance: `spec-update-todo`, `spec-update-done`
- Planning handoff: `implementation-plan`

## References

- `references/summary-template.md` for full output skeleton and detailed extraction rules.
- `examples/summary-output.md` for expected tone and depth.
