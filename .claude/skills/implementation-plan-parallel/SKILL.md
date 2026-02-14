---
name: implementation-plan-parallel
description: This skill should be used when the user asks to "create a parallel implementation plan", "plan parallel implementation", "병렬 구현 계획", "create parallel development roadmap", or wants a structured implementation plan with Target Files for parallel execution support.
version: 1.0.0
---

# Implementation Plan Creation (Parallel-Ready)

> **Simplified Workflow Note**: This skill is part of the **legacy workflow** with parallel extension.
> In the simplified 4-step workflow, consider using `feature-draft-parallel` instead,
> which combines `spec-draft` + `spec-update-todo` + `implementation-plan` into a single step with Target Files.

Create structured, actionable implementation plans from user specifications — with **Target Files** on every task to enable parallel execution via `implementation-parallel`.

## Relationship to `implementation-plan`

This skill extends `implementation-plan` with one key addition: **Target Files** on each task.

| Aspect | `implementation-plan` | `implementation-plan-parallel` (this) |
|--------|----------------------|--------------------------------------|
| Task template | Standard | **Target Files 포함** |
| Execution target | `implementation` | `implementation-parallel` |
| Everything else | Identical | Identical |

## Hard Rule: Spec Documents Are Read-Only

- This skill may **read** the spec as input, but it **MUST NOT** modify any files under `_sdd/spec/`.
- If you think the spec should change, capture it as **Open Questions / Spec gaps** in the plan and direct the user to `spec-update-todo`.

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
3. **Define Tasks with Target Files** - Create granular, actionable work items with file-level scope
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

## Step 3: Task Definition with Target Files

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

**Target Files**:
- [C] `path/to/new_file.py` -- 설명
- [M] `path/to/existing_file.py` -- 변경 내용 설명
- [C] `tests/test_new_file.py` -- 테스트

**Technical Notes**:
- [Implementation hints, patterns to use, files to modify]

**Dependencies**: [List of blocking tasks by ID]
```

### Target Files Guidelines

See `references/target-files-spec.md` for the full specification.

Key rules:
- **Every task MUST have Target Files**
- Use markers: `[C]` Create, `[M]` Modify, `[D]` Delete
- Use project-root relative paths
- Include both source and test files
- Minimize overlaps between tasks for maximum parallelization
- When overlaps are unavoidable, note which tasks must be sequential

### Exploring the Codebase for Target Files

Before assigning Target Files, explore the codebase to understand:
- Existing file structure and naming conventions
- Where source files, tests, and configs live
- Which existing files will need modification
- What new files need to be created

### Task Sizing Guidelines

- Each task should be completable in a focused work session
- If a task seems too large, split into subtasks
- Include setup/infrastructure tasks often overlooked
- Don't forget documentation and testing tasks

## Step 4: Dependency Mapping

Establish task relationships:

- **Blocks**: Tasks that must complete before others can start
- **Related**: Tasks that share context but aren't blocking
- **Parallel**: Tasks that can be worked on simultaneously (when Target Files don't overlap)

Create a dependency graph or critical path when complexity warrants.

**Parallel-specific**: After mapping dependencies, verify that tasks marked as parallel-eligible don't have overlapping Target Files.

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
[Expanded task definitions with acceptance criteria AND Target Files]

## Parallel Execution Summary
| Phase | Total Tasks | Max Parallel | File Conflicts |
|-------|-------------|--------------|----------------|
| 1     | N           | N            | None           |
| 2     | N           | N            | config.py (Task 3, 5) |

## Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| ...  | ...    | ...        |

## Open Questions
- [ ] [Question requiring clarification]

## Model Recommendation
[Model recommendation based on implementation complexity]
```

## Best Practices

- **Be Specific**: Vague tasks lead to scope creep
- **Include Infrastructure**: Don't forget CI/CD, environments, tooling
- **Plan for Testing**: Include unit, integration, and E2E test tasks
- **Consider Operations**: Monitoring, logging, deployment procedures
- **Document Decisions**: Capture why certain approaches were chosen
- **Identify MVP**: Mark which tasks are essential for initial release
- **Minimize File Overlaps**: Design tasks to touch different files when possible
- **Verify Target Files**: Check file paths against actual codebase structure

## When to Ask for Clarification

Use AskUserQuestion when encountering:

- Ambiguous requirements with multiple valid interpretations
- Missing technical constraints (language, framework, etc.)
- Unclear priority between competing features
- Unknown integration requirements
- Incomplete success criteria
- Uncertain file paths for Target Files

## LLM Model to use

Try to estimate the size and complexity of the implementation.
Inform user which model would fit for the implementation by referring "Model aliases" under https://code.claude.com/docs/en/model-config.

## Output Location

After creating the plan, offer to:

1. Display in conversation (for review/discussion)
2. Save to a file to the user provided path, or default to `<project_root>/_sdd/implementation/IMPLEMENTATION_PLAN.md`
    - If the file already exists, archive it as `<project_root>/_sdd/implementation/prev/PREV_IMPLEMENTATION_PLAN_<timestamp>.md` (create `prev/` if needed) and create a new one.
3. If the plan is too large to fit comfortably in one file (e.g. >25 tasks), split the plan into multiple files:
    - Keep `IMPLEMENTATION_PLAN.md` as an index/overview and link to the phase files
    - Name phase files as `IMPLEMENTATION_PLAN_PHASE_1.md`, `IMPLEMENTATION_PLAN_PHASE_2.md`, etc.
4. Create tasks using TaskCreate tool for tracking

Always confirm with the user which output format they prefer.

## Additional Resources

### Reference Files
- **`references/advanced-patterns.md`** - Advanced planning patterns (microservices, migrations, risk-based)
- **`references/target-files-spec.md`** - Target Files field detailed specification

### Example Files
- **`examples/sample-plan-parallel.md`** - Complete implementation plan example with Target Files
