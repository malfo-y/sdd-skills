# Adaptive Questions Guide

Use this guide to minimize unnecessary questions while collecting enough detail for both patch drafting and implementation planning.

## Completeness Levels

### HIGH

Criteria:

- feature/change objective is explicit
- priority is explicit or obvious
- acceptance criteria are explicit or directly inferable

Action:

- ask no blocking questions
- provide a short confirmation summary

### MEDIUM

Criteria:

- objective exists, but one or more key fields are missing

Action:

- ask only targeted questions for missing fields

Recommended question types:

1. Priority: `High / Medium / Low`
2. Acceptance criteria: at least 2 measurable checks
3. Technical constraints: dependencies, infra, architecture boundaries

### LOW

Criteria:

- idea-level request, broad/ambiguous wording

Action:

- identify request type first
- then ask mandatory type-specific questions

## Type Identification

Ask user to choose one primary type:

- New Feature
- Improvement
- Bug Report
- Component Change
- Configuration Change

## Required Questions by Type

### New Feature

- What is the feature name?
- What should it do?
- What is the priority?
- What are acceptance criteria (min 2)?

### Improvement

- What is the current state?
- What should improve?
- Why is this needed?
- What priority should it have?

### Bug Report

- What is the bug title?
- What is severity?
- How to reproduce?
- What is expected behavior?

### Component Change

- Which component is affected?
- Is it new or existing?
- What interface/behavior changes?
- Any compatibility constraints?

### Configuration Change

- Config name/key?
- Type (`env`, config file, CLI arg)?
- What does it control?
- Required or optional; default value?

## Efficiency Rules

- Never re-ask known information from chat/context files.
- Prefer one concise multi-part prompt over many tiny prompts.
- If uncertainty remains, document it under open questions rather than guessing.
