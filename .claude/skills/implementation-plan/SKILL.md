---
name: implementation-plan
description: This skill should be used when the user asks to "create an implementation plan", "plan the implementation", "break down this spec", "create a development roadmap", "analyze requirements and create tasks", or provides a specification document and asks for a structured plan.
version: 1.0.0
---

# Implementation Plan Creation

Create structured, actionable implementation plans from user specifications. Follow this systematic approach to transform requirements into executable development tasks.

## Hard Rule: Spec Documents Are Read-Only

- This skill may **read** the spec as input, but it **MUST NOT** modify any files under `_sdd/spec/`.
- If you think the spec should change, capture it as **Open Questions / Spec gaps** in the plan and direct the user to `spec-update`.

## Implementation spec

1. Refer to the user input.
2. If the user input is not clear, refer to `_sdd/implementation/user_input.md` for the user specification.
3. If the user input is not clear and there is no user specification, ask the user for clarification.

After processing `user_input.md`, rename it to `_processed_user_input.md` to mark it as processed inputs.

## Language

결과로 나오는 .md 파일의 내용은 한국어로 작성합니다. 

## Process Overview

1. **Analyze the Specification** - Understand scope, requirements, and constraints
2. **Identify Components** - Break down into logical modules/features
3. **Define Tasks** - Create granular, actionable work items
4. **Establish Dependencies** - Map task relationships and critical path
5. **Output the Plan** - Present in structured, trackable format

## Step 1: Specification Analysis

Read and analyze the provided specification thoroughly:

- **Core Requirements**: What must the system do?
- **Technical Constraints**: Languages, frameworks, integrations, performance requirements
- **Scope Boundaries**: What is explicitly in/out of scope?
- **Success Criteria**: How will completion be measured?
- **Unknowns/Risks**: What needs clarification or research?

If the specification is unclear or incomplete, use the AskUserQuestion tool to clarify before proceeding.

## Step 2: Component Identification

Break the system into logical components:

- Group related functionality into modules
- Identify shared utilities and common patterns
- Note external dependencies and integrations
- Consider data models and storage requirements
- Map user-facing features vs internal services

## Step 3: Task Definition

For each component, create granular tasks following this structure:

```
### Task: [Clear, action-oriented title]
**Component**: [Parent component/module]
**Priority**: [P0-Critical | P1-High | P2-Medium | P3-Low]
**Type**: [Feature | Bug | Refactor | Research | Infrastructure | Test]

**Description**:
[Detailed description of what needs to be done]

**Acceptance Criteria**:
- [ ] [Specific, measurable criterion]
- [ ] [Another criterion]

**Technical Notes**:
- [Implementation hints, patterns to use, files to modify]

**Dependencies**: [List of blocking tasks by ID]
```

### Task Sizing Guidelines

- Each task should be completable in a focused work session
- If a task seems too large, split into subtasks
- Include setup/infrastructure tasks often overlooked
- Don't forget documentation and testing tasks

## Step 4: Dependency Mapping

Establish task relationships:

- **Blocks**: Tasks that must complete before others can start
- **Related**: Tasks that share context but aren't blocking
- **Parallel**: Tasks that can be worked on simultaneously

Create a dependency graph or critical path when complexity warrants.

## Step 5: Plan Output Format

Present the final plan in this structure:

```markdown
# Implementation Plan: [Project Name]

## Overview
[Brief summary of what will be built]

## Scope
### In Scope
- [Feature/capability]

### Out of Scope
- [Explicitly excluded items]

## Components
1. **[Component Name]**: [Brief description]
2. **[Component Name]**: [Brief description]

## Implementation Phases

### Phase 1: [Foundation/Setup]
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 1  | ...  | P0       | -            | Core      |

### Phase 2: [Core Features]
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 2  | ...  | P1       | 1            | Feature A |

### Phase 3: [Polish/Integration]
...

## Task Details
[Expanded task definitions with acceptance criteria]

## Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| ...  | ...    | ...        |

## Open Questions
- [ ] [Question requiring clarification]
```

## Best Practices

- **Be Specific**: Vague tasks lead to scope creep
- **Include Infrastructure**: Don't forget CI/CD, environments, tooling
- **Plan for Testing**: Include unit, integration, and E2E test tasks
- **Consider Operations**: Monitoring, logging, deployment procedures
- **Document Decisions**: Capture why certain approaches were chosen
- **Identify MVP**: Mark which tasks are essential for initial release

## When to Ask for Clarification

Use AskUserQuestion when encountering:

- Ambiguous requirements with multiple valid interpretations
- Missing technical constraints (language, framework, etc.)
- Unclear priority between competing features
- Unknown integration requirements
- Incomplete success criteria

## LLM Model to use

Try to estimate the size and complexity of the implementation.
Inform user which model would fit for the implementation by referring "Model aliases" under https://code.claude.com/docs/en/model-config.

## Output Location

After creating the plan, offer to:

1. Display in conversation (for review/discussion)
2. Save to a file to the user provided path, or default to `<project_root>/_sdd/implementation/IMPLEMENTATION_PLAN.md`
    - If the file already exists, rename it to `PREV_IMPLEMENTATION_PLAN_<timestamp>.md` and create a new one.
3. If the plan is too large to fit comfortably in one file (e.g. >25 tasks), split the plan into multiple files:
    - Keep `IMPLEMENTATION_PLAN.md` as an index/overview and link to the phase files
    - Name phase files as `IMPLEMENTATION_PLAN_PHASE_1.md`, `IMPLEMENTATION_PLAN_PHASE_2.md`, etc.
4. Create tasks using TaskCreate tool for tracking

Always confirm with the user which output format they prefer.
