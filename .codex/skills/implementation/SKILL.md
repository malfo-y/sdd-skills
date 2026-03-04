---
name: implementation
description: Use this skill when the user wants to execute an implementation plan, start implementing tasks from a plan, work through a development roadmap, says "implement the plan", "start implementation", "execute the plan", "work on the tasks", or explicitly asks for "implement parallel", "parallel implementation", "병렬 구현", "병렬로 구현". Uses conflict-aware parallel execution when Target Files are available.
version: 1.0.0
---

# Implementation Execution (Parallel TDD Approach)

Execute implementation plans systematically using Test-Driven Development (TDD), with **parallel sub-agent dispatch** for independent tasks within each phase. Tasks without file conflicts are executed concurrently via parallel sub-agent calls.

## Simplified Workflow

This skill is **Step 3 of 4** in the parallel SDD workflow:

```
spec → feature-draft → implementation (this) → spec-update-done
```

| Step | Skill | Purpose |
|------|-------|---------|
| 1 | spec-create | Create the initial spec document |
| 2 | feature-draft | Draft feature spec patch + implementation plan (with Target Files) |
| **3** | **implementation** | Execute the plan with parallel sub-agents (TDD) |
| 4 | spec-update-done | Sync spec with actual code |

> Also compatible with plans without Target Files (falls back to sequential execution).

## Hard Rule: Never Modify Spec Files

- This skill **MUST NOT** create/edit/delete any spec documents under `<project_root>/_sdd/spec/`.
- If implementation reveals spec drift, ambiguity, or missing requirements:
  - Report it in the progress report / chat, and
  - Ask the user to update the spec via `spec-update-todo` (or run a spec audit via `spec-update-done`).

## Core Principle: Test-Driven Development

All implementation follows the **Red-Green-Refactor** cycle:

```
┌─────────────────────────────────────────────────────────┐
│  1. RED: Write a failing test for the desired behavior  │
│              ↓                                          │
│  2. GREEN: Write minimal code to make the test pass     │
│              ↓                                          │
│  3. REFACTOR: Clean up while keeping tests green        │
│              ↓                                          │
│  (Repeat for each acceptance criterion)                 │
└─────────────────────────────────────────────────────────┘
```

Each sub-agent follows this same TDD protocol independently.

## Prerequisites

Before starting implementation:

1. **Locate the Implementation Plan**: Check for plan at:
   - User-specified path
   - `<project_root>/_sdd/implementation/IMPLEMENTATION_PLAN.md` (preferred entry point; may link to phase files)
   - `<project_root>/_sdd/implementation/IMPLEMENTATION_PLAN_PHASE_<phase-number>.md` (when the plan is split by phase)
   - `<project_root>/_sdd/drafts/feature_draft_<feature_name>.md` (produced by `feature-draft` skill; use Part 2: 구현 계획 as the implementation plan)
   - Recent conversation context

If multiple plan files exist and the user did not specify a starting point:
- If only one source exists (IMPLEMENTATION_PLAN or a single feature draft), start from it.
- If both `IMPLEMENTATION_PLAN.md` and feature draft(s) exist, compare whether they describe the same feature. If they do, prefer `IMPLEMENTATION_PLAN.md`. If they describe different features, ask the user which to implement.
- If multiple feature drafts exist and no `IMPLEMENTATION_PLAN.md`, ask the user which feature draft to implement.
- For phase-split plans, ask the user which phase to start/resume (default: Phase 1).

2. **Verify Plan Exists**: If no plan is found, suggest using the `implementation-plan` or `feature-draft` skill first.

3. **Check for Target Files**: Examine whether tasks have `**Target Files**` fields.
   - **Present**: Enable parallel execution (this skill's main advantage)
   - **Absent**: Fall back to sequential mode with optional Target Files inference (see Step 3)

4. **Understand the Codebase**: Use `rg`/`Glob` exploration to understand:
   - Existing code patterns
   - **Testing framework and conventions** (critical for TDD)
   - Test file locations and naming conventions

5. **Load the execution/test environment guide** before running any code or tests:
   - User-specified path
   - `<project_root>/_sdd/env.md` (source of environment variables, conda env, required setup commands)
   - Recent conversation context

If `_sdd/env.md` exists, apply its setup instructions first (for example: `conda activate ...`, required `export` variables, required local services).

## Process Overview

1. **Load the Plan** - Read and parse the implementation plan
2. **Initialize Task Tracking** - Create tasks in the task system
3. **Analyze Parallelization** - Build conflict graph, form parallel groups
4. **Execute by Phase (Parallel)** - Dispatch sub-agents for each group
5. **Integrate & Verify** - Post-group verification, handle failures
6. **Phase Review** - Quality checks after each phase
7. **Final Review & Report** - Comprehensive review and combined report

## Step 1: Load the Plan

Read the implementation plan file and extract:

- **Components**: The modules/features being built
- **Phases**: The ordered implementation stages
- **Tasks**: Individual work items with details
- **Dependencies**: Task relationships and blocking items
- **Target Files**: Per-task file lists (for parallel scheduling)

```markdown
Key sections to parse:
- ## Components
- ## Implementation Phases
- ## Task Details (including Target Files)
- ## Open Questions (address before proceeding)
```

If the plan has **Open Questions**, use `request_user_input` in Plan mode, otherwise ask a short direct question in Default mode.

## Step 2: Initialize Task Tracking

Initialize tracking in the plan/progress document for visibility:

```
For each task in the plan:
1. Add a tracking row in `_sdd/implementation/IMPLEMENTATION_PROGRESS.md`:
   - task_id, title, phase, dependencies, status, owner/sub-agent, notes
2. Set initial status:
   - BLOCKED (if dependencies exist)
   - READY (if no dependencies)
3. Keep a stable mapping between plan IDs and tracking rows.
```

### Task ID Mapping

Maintain a mapping between plan task IDs and tracking table rows:
```
Plan ID 1 → Progress Row #1
Plan ID 2 → Progress Row #2
```

## Step 3: Analyze Parallelization

This is the **key step** that differentiates parallel execution from sequential execution.

### 3.1 Check Target Files Availability

```
IF all tasks have Target Files:
    → Proceed with full parallel analysis
ELSE IF some tasks have Target Files:
    → Parallel for tasks with Target Files, sequential for others
ELSE (no Target Files at all):
    → Attempt inference (see 3.2) or fall back to sequential
```

### 3.2 Target Files Inference (when absent)

If a plan lacks Target Files:

```
For each task:
1. Analyze Description and Technical Notes for file path mentions
2. Use `rg`/`Glob` to identify related files
3. Infer Target Files with [C] or [M] markers

Present inferred Target Files to user:
  "Task 1의 Target Files를 다음과 같이 추론했습니다:
   - [C] src/services/auth.py
   - [C] tests/test_auth.py
   확인하시겠습니까?"

IF user confirms → Use for parallel scheduling
IF user declines or uncertain → Execute that task sequentially
```

### 3.3 Build Conflict Graph

For each pair of unblocked tasks in a phase, check **both** file-level and semantic conflicts:

```
For task_a, task_b in unblocked_tasks:
    files_a = set(task_a.target_files.paths)
    files_b = set(task_b.target_files.paths)

    # 1단계: 파일 수준 충돌
    IF files_a ∩ files_b ≠ ∅:
        mark_conflict(task_a, task_b)
        continue

    # 2단계: 의미적 충돌 (파일이 겹치지 않아도 발생 가능)
    IF task_a creates model/type that task_b imports or depends on:
        mark_conflict(task_a, task_b)
    IF both tasks create DB migrations:
        mark_conflict(task_a, task_b)
    IF both tasks assume shared config/env values:
        mark_conflict(task_a, task_b)
    IF task_a defines API contract that task_b consumes:
        mark_conflict(task_a, task_b)
```

> **Note**: 의미적 충돌은 Acceptance Criteria, Technical Notes, Description에서 추론합니다. 불확실한 경우 순차 실행이 안전합니다. 상세 규칙은 `references/parallel-execution.md`의 "의미적 충돌" 섹션을 참조하세요.

### 3.4 Form Parallel Groups

See `references/parallel-execution.md` for the full algorithm.

```
function buildParallelGroups(unblockedTasks):
    groups = []
    remaining = sort(unblockedTasks, by=[priority DESC, id ASC])

    while remaining is not empty:
        currentGroup = []
        usedFiles = {}

        for task in remaining:
            if task.targetFiles ∩ usedFiles == ∅:
                currentGroup.append(task)
                usedFiles = usedFiles ∪ task.targetFiles

        groups.append(currentGroup)
        remaining = remaining - currentGroup

    return groups
```

### 3.5 Report Parallelization Plan

Before executing, show the user the parallel dispatch plan:

```markdown
## Phase 1 병렬 실행 계획

### Group 1 (동시 실행):
- Task 1: 데이터베이스 스키마 설정 [P0]
- Task 2: 비밀번호 해싱 유틸리티 [P0]
- Task 4: 레이트 제한 미들웨어 [P1]

### Group 2 (Group 1 완료 후):
- Task 3: JWT 유틸리티 (Task 1과 config.py 충돌)

예상 효율: 4 tasks → 2 groups (2x speedup)
```

## Step 4: Execute by Phase (Parallel)

For each phase, execute parallel groups in order:

```
For each phase:
  1. Compute parallel groups (Step 3)
  2. For each group:
     a. Dispatch sub-agents via parallel sub-agent calls (concurrent)
     b. Wait for all sub-agents in group to complete
     c. Run post-group verification (Step 5)
     d. Handle failures and unplanned dependencies
  3. Proceed to next group
  4. When all groups complete → Phase Review (Step 6)
```

### 4.1 Sub-Agent Dispatch

For each task in a parallel group, call sub-agents **simultaneously**:

```
Task(
  subagent_type="general-purpose",
  model="gpt-5.3-codex",
  reasoning_effort="high",
  prompt="[Sub-Agent Prompt - see below]"
)
```

**Call all tasks in the same group as parallel sub-agent calls in a single message.**

### 4.2 Sub-Agent Prompt Template

Each sub-agent receives:

```
당신은 TDD 구현 sub-agent입니다. 아래 task를 구현하세요.

## 담당 Task
### Task {id}: {title}
**Component**: {component}
**Priority**: {priority}

**Description**:
{description}

**Acceptance Criteria**:
{acceptance_criteria}

**Technical Notes**:
{technical_notes}

## 수정 허용 파일 (Target Files)
{target_files_list}

## TDD 프로토콜
각 Acceptance Criterion마다:
1. **RED**: 실패하는 테스트 작성 → 테스트 실행 → 실패 확인
2. **GREEN**: 최소한의 코드로 테스트 통과 → 테스트 실행 → 통과 확인
3. **REFACTOR**: 코드 정리 → 전체 테스트 실행 → 통과 확인

## 파일 경계 규칙
- 위의 Target Files만 생성/수정/삭제 가능
- 다른 파일은 읽기(Read)만 가능
- Target Files 외 파일 수정이 필요하면:
  수정하지 말고 보고: "UNPLANNED_DEPENDENCY: {파일경로} - {필요한 변경 설명}"

## 환경
{env_setup}

## 테스트 프레임워크
{test_framework_info}

## 완료 시 보고 형식
아래 형식으로 결과를 보고하세요:

## Task {id} 완료 보고
### 결과: SUCCESS / PARTIAL / FAILED
### TDD 진행 상황
| Criterion | RED | GREEN | REFACTOR | 상태 |
|-----------|-----|-------|----------|------|
| (criterion name) | ✓/✗ | ✓/✗ | ✓/✗ | 완료/실패 |
### 생성/수정된 파일
- [C/M] `path` (N lines)
### 테스트 결과
- 새 테스트: N개
- 전체 통과: Yes/No
### Unplanned Dependencies (있는 경우)
- UNPLANNED_DEPENDENCY: `path` - 설명
### 발견 사항
- 특이사항
```

### 4.3 Sequential Fallback

When tasks cannot be parallelized (conflicts or missing Target Files), execute them sequentially using the same TDD approach as sequential execution:

```
1. Update tracking table: status = "IN_PROGRESS"
2. Read task details
3. For each acceptance criterion: RED → GREEN → REFACTOR
4. Update tracking table: status = "COMPLETED"
```

## Step 5: Integrate & Verify (Post-Group)

After each parallel group completes:

### 5.1 Run Full Test Suite

```
1. Execute all tests (new + existing)
2. Check for regressions
3. If tests fail:
   a. Identify which sub-agent's changes caused the failure
   b. Fix or re-run that task sequentially
```

### 5.2 Process Unplanned Dependencies

```
1. Collect UNPLANNED_DEPENDENCY reports from all sub-agents
2. For each unplanned dependency:
   a. Assess if the dependency is valid
   b. If valid: resolve it directly (sequential) → re-verify
   c. If invalid: note as non-issue
3. Re-run affected tests after resolution
```

### 5.3 Handle Sub-Agent Failures

```
IF a sub-agent reports FAILED or PARTIAL:
  1. Other sub-agents' results are NOT affected
  2. Mark failed task as needs_retry
  3. After group completes, retry failed task sequentially
  4. If retry also fails: report to user, skip task
```

### 5.4 Verify File Integrity

```
1. Check that no sub-agent modified files outside their Target Files
2. If violations found:
   a. Revert unauthorized changes
   b. Re-run the task sequentially with stricter instructions
```

### 5.5 Update Task Status

```
For each task in the completed group:
  IF success → tracking status = "COMPLETED"
  IF failed → tracking status = "IN_PROGRESS" (for retry)
  IF partial → Note incomplete criteria for follow-up
```

## Step 6: Phase Review

After completing all tasks in a phase, run a lightweight quality review.

### 6.1 Collect Phase Context

Reuse data already tracked during TDD — **no re-discovery needed**:
- Files created/modified during this phase (from all sub-agents)
- Tests written and their pass/fail status
- Acceptance criteria met
- Any notes or blockers encountered

### 6.2 Cross-Cutting Quality Checks

Run the following checks on all files touched in this phase. Reference `references/review-checklist.md` for detailed criteria.

| Category | What to Check |
|----------|---------------|
| **Security** | SQL injection, XSS, hardcoded secrets, missing auth, input validation |
| **Error Handling** | Consistent response format, logging, graceful degradation |
| **Code Patterns** | Naming conventions, abstraction level, duplication, project conventions |
| **Performance** | N+1 queries, missing indexes, async blocking, resource cleanup |
| **Test Quality** | Independent, deterministic, behavior-focused |
| **Cross-Task Integration** | Tasks within this phase work together correctly |
| **Parallel Integration** | Sub-agent outputs are consistent with each other |

### 6.3 Categorize Issues

- **Critical**: Security vulnerability, data loss risk, core functionality broken → **must fix before next phase**
- **Quality**: Missing edge-case tests, inconsistent error handling → document, proceed
- **Improvement**: Performance optimization, readability enhancement → note for later

### 6.4 Decision Gate

```
IF critical issues found:
    Fix using TDD (write test exposing the issue → fix → verify)
    Re-run phase review on fixed areas
ELSE IF quality issues only:
    Document findings, proceed to next phase
ELSE:
    Phase is clean — proceed
```

### 6.5 Phase Review Output

Save per-phase report under `<project-root>/_sdd/implementation/IMPLEMENTATION_REPORT_PHASE_<phase-number>.md`.

## Step 7: Final Review & Report

After all phases complete, run a comprehensive quality review across the **entire implementation**, then produce a combined report.

### 7.1 Comprehensive Quality Review

Apply the same checklists from Step 6.2 but with **cross-phase scope**:
- Do modules from different phases integrate correctly?
- Are there inconsistent patterns between early and late phases?
- Do security boundaries hold across the full system?
- Are there performance issues that only appear at full scale?

### 7.2 Final Decision Gate

Same rules as Step 6.4. Critical issues must be fixed with TDD before declaring completion.

### 7.3 Generate Combined Report

Save the report under a user-specified file (default: `<project-root>/_sdd/implementation/IMPLEMENTATION_REPORT.md`).
- If the file already exists, archive it as `<project-root>/_sdd/implementation/prev/PREV_IMPLEMENTATION_REPORT_<timestamp>.md` (create `prev/` if needed) and create a new one.

The combined report should include:

### Progress Summary
```markdown
## Implementation Report (Parallel Execution)

### Progress Summary
- Total Tasks: X
- Completed: X
- Tests Added: X
- All Passing: Yes/No

### Parallel Execution Stats
- Total Groups Dispatched: X
- Tasks Run in Parallel: X
- Sequential Fallbacks: X
- Sub-agent Failures: X (retried: Y, resolved: Z)

### Completed
- [x] Task 1: Set up database schema (3 tests) [parallel: group 1]
- [x] Task 2: Implement password hashing (5 tests) [parallel: group 1]

### Test Summary
- New tests added: N
- All tests passing: Yes
- Coverage: X%
```

### Quality Assessment
```markdown
### Quality Assessment

#### Phase Reviews
| Phase | Critical | Quality | Improvements | Parallel Groups | Status |
|-------|----------|---------|--------------|-----------------|--------|
| 1: Foundation | 0 | 1 | 2 | 2 | Clean |
| 2: Core Auth | 1 (fixed) | 0 | 1 | 3 | Fixed |

#### Cross-Phase Review
- Integration: All modules communicate correctly
- Security: Auth boundaries verified across all endpoints
- Performance: No N+1 queries detected
- Parallel Consistency: No conflicting changes between sub-agents

#### Issues Found
| # | Severity | Description | Phase | Status |
|---|----------|-------------|-------|--------|
| 1 | Critical | Rate limiter not applied to OAuth routes | Cross-phase | Fixed |

#### Recommendations
1. [recommendation]

### Conclusion
[Overall assessment: READY / NEEDS WORK / BLOCKED]
```

## TDD Guidelines

### Testing environment

Before running any test or executable command, read `_sdd/env.md` and apply the listed setup.
If `_sdd/env.md` is missing, ask the user for the required runtime/test environment instead of guessing.

### What to Test

| Task Type | Test Focus |
|-----------|------------|
| API Endpoint | Request/response, status codes, validation |
| Service/Logic | Business rules, edge cases, error handling |
| Data Layer | CRUD operations, constraints, queries |
| Utility | Input/output transformations, edge cases |

### Test Naming Convention

Follow the project's existing convention, or use:
```
test_<unit>_<scenario>_<expected_result>
```

### Test Structure (Arrange-Act-Assert)

```python
def test_something():
    # Arrange - Set up test data and conditions
    user = create_test_user()

    # Act - Perform the action being tested
    result = perform_action(user)

    # Assert - Verify the expected outcome
    assert result.status == "success"
```

### When TDD is Difficult

Some tasks don't fit pure TDD. Adapt the approach:

| Situation | Approach |
|-----------|----------|
| Database migrations | Write migration, then test the schema |
| Configuration/setup | Verify setup works, add smoke tests |
| UI components | Use component testing or integration tests |
| External integrations | Mock the external service in tests |

## Handling Common Situations

### Parallel-Specific

#### Sub-agent modifies wrong file
```
1. Revert the unauthorized change
2. Re-run the task sequentially with explicit file boundary warnings
3. If still fails, ask user for guidance
```

#### Multiple sub-agents report conflicting patterns
```
1. Identify the inconsistency during Phase Review
2. Choose one pattern as canonical
3. Fix the other tasks to match (using TDD)
```

#### Sub-agent blocked by unplanned dependency
```
1. Sub-agent completes what it can, reports UNPLANNED_DEPENDENCY
2. Main agent resolves the dependency after group completes
3. Re-run the incomplete parts of the task
```

### General

#### Test is Hard to Write
```
1. Simplify the acceptance criterion
2. Break into smaller, testable pieces
3. Consider if the design needs adjustment (TDD feedback)
4. Ask user if criterion can be clarified
```

#### Test Passes Immediately
```
1. Feature may already exist - verify
2. Test may be wrong - review the assertion
3. Test may be testing the wrong thing - rewrite
```

#### Task is Blocked by External Dependency
```
1. Write tests with mocks for the external dependency
2. Implement code against the mocks
3. Note that integration test needed when dependency available
4. Move to next task
```

## Implementation Best Practices

### Code Quality
- **Test first, always**: No production code without a failing test
- **Minimal code**: Write only enough to pass the test
- **Follow existing patterns**: Match the codebase's style and conventions
- **Refactor fearlessly**: Tests give confidence to improve code

### Parallel Execution
- **Trust sub-agents**: Don't re-do their work; verify through tests
- **Fix forward**: If a sub-agent's output has minor issues, fix in place rather than re-running
- **Maximize concurrency**: Dispatch all non-conflicting tasks simultaneously
- **Fail gracefully**: One sub-agent's failure doesn't stop others

### Communication
- **Report parallel progress**: Show which groups are executing/completed
- **Surface blockers**: Alert user to issues requiring decisions
- **Confirm scope changes**: Ask before deviating from the plan

## When to Pause and Ask

Use `request_user_input` in Plan mode, otherwise ask a short direct question in Default mode, when:

- **Target Files unclear**: Can't determine file boundaries for parallelization
- **Inference uncertain**: Inferred Target Files need user confirmation
- **Test unclear**: Can't determine what to assert
- **Ambiguous requirements**: Multiple valid interpretations
- **Scope decisions**: Discovered work that may or may not be in scope
- **Technical choices**: Multiple valid approaches with trade-offs
- **Blockers**: External dependencies or issues requiring user action

## Integration with Other Skills

- **implementation-plan**: Creates plans with Target Files that this skill consumes
- **feature-draft**: Also produces plans with Target Files (Part 2: 구현 계획)
- Plans without Target Files → sequential fallback
- **implementation-review**: Available for standalone audits

## Quick Start

When user says "implement the plan in parallel":

1. Acquire implementation plan (from `feature-draft`, `implementation-plan`, or existing plan files)
2. Parse the plan and check for Target Files
3. If Target Files absent: infer → confirm → or fall back to sequential
4. Create task tracking
5. **Identify testing framework** used in the project
6. For each phase:
   a. Build parallel groups from unblocked tasks + Target Files
   b. Show dispatch plan to user
   c. **Dispatch sub-agents for each group** (parallel sub-agent calls)
   d. After each group: **run full test suite**, handle failures
   e. After all groups in phase: **run phase review**
   f. Fix any **critical issues** (using TDD)
7. After all phases: Run **final review**, generate `IMPLEMENTATION_REPORT.md`
