---
name: implementation-plan
description: This skill should be used when the user asks to "create an implementation plan", "plan the implementation", "break down this spec", "create a development roadmap", "analyze requirements and create tasks", "create a parallel implementation plan", "plan parallel implementation", "병렬 구현 계획", "create parallel development roadmap", or wants a structured implementation plan with Target Files for parallel execution support.
version: 1.0.0
---

# Implementation Plan Creation (Parallel-Ready)

> **Workflow Note**: In the simplified 4-step workflow, `feature-draft` is the default
> when you want requirement clarification + spec patch drafting + planning in one run.
> Use this skill when planning should be executed as a standalone step.

Create structured, actionable implementation plans from user specifications — with **Target Files** on every task to enable parallel execution via `implementation`.

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

**Tools**: `Read`, `Glob`, `AskUserQuestion`

Read and analyze the provided specification thoroughly:

- **Core Requirements**: What must the system do?
- **Technical Constraints**: Languages, frameworks, integrations, performance requirements
- **Scope Boundaries**: What is explicitly in/out of scope?
- **Success Criteria**: How will completion be measured?
- **Unknowns/Risks**: What needs clarification or research?

If the specification is unclear or incomplete, use the AskUserQuestion tool to clarify before proceeding.

#### Context Management

| 스펙 크기 | 전략 | 구체적 방법 |
|-----------|------|-------------|
| < 200줄 | 전체 읽기 | `Read`로 전체 파일 읽기 |
| 200-500줄 | 전체 읽기 가능 | `Read`로 전체 읽기, 필요 시 섹션별 |
| 500-1000줄 | TOC 먼저, 관련 섹션만 | 상위 50줄(TOC) 읽기 → 관련 섹션만 `Read(offset, limit)` |
| > 1000줄 | 인덱스만, 타겟 최대 3개 | 인덱스/TOC만 읽기 → 타겟 섹션 최대 3개 선택적 읽기 |

| 코드베이스 크기 | 전략 | 구체적 방법 |
|----------------|------|-------------|
| < 50 파일 | 자유 탐색 | `Glob` + `Read` 자유롭게 사용 |
| 50-200 파일 | 타겟 탐색 | `Grep`/`Glob`으로 후보 식별 → 타겟 `Read` |
| > 200 파일 | 타겟 탐색 | `Grep`/`Glob` 위주 → 최소한의 `Read` |

**Decision Gate 1→2**:
```
spec_loaded = 스펙 문서 읽기 완료
requirements_clear = 핵심 요구사항 파악 완료
scope_defined = 스코프 경계 정의 완료

IF spec_loaded AND requirements_clear AND scope_defined → Step 2 진행
ELSE IF NOT requirements_clear → AskUserQuestion: 모호한 요구사항 질문
ELSE → 미파악 항목 추가 분석 후 재평가
```

## Step 2: Component Identification

**Tools**: `Glob`, `Grep`, `Read`

Break the system into logical components:

- Group related functionality into modules
- Identify shared utilities and common patterns
- Note external dependencies and integrations
- Consider data models and storage requirements
- Map user-facing features vs internal services

## Step 3: Task Definition with Target Files

**Tools**: `Glob`, `Grep`, `Read`

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

### Step 3.5: Task 목록 확인 (Checkpoint)

**Tools**: `AskUserQuestion`

```
1. Task 목록 요약 테이블을 사용자에게 제시:
   | Phase | Task 수 | P0 | P1 | P2 | P3 | Target Files 유무 |
   |-------|---------|----|----|----|----|-------------------|
   | 1     | N       | X  | Y  | Z  | W  | 모두 있음/N개 누락 |
   | 2     | N       | X  | Y  | Z  | W  | 모두 있음/N개 누락 |

2. AskUserQuestion: "Task 목록을 확인해 주세요."
   옵션:
   1. "확인, 의존성 매핑 진행" → Step 4
   2. "수정 필요" → 수정 사항 반영 (최대 2라운드)
```

**Decision Gate 3→4**:
```
all_tasks_have_target_files = 모든 Task에 Target Files 매핑 완료
acceptance_criteria_defined = 모든 Task에 Acceptance Criteria 정의

IF all_tasks_have_target_files AND acceptance_criteria_defined → Step 4 진행
ELSE → 누락 항목 보완 후 재확인
```

## Step 4: Dependency Mapping

**Tools**: `Glob` (Target Files 중복 확인)

Establish task relationships:

- **Blocks**: Tasks that must complete before others can start
- **Related**: Tasks that share context but aren't blocking
- **Parallel**: Tasks that can be worked on simultaneously (when Target Files don't overlap)

Create a dependency graph or critical path when complexity warrants.

**Parallel-specific**: After mapping dependencies, verify that tasks marked as parallel-eligible don't have overlapping Target Files.

**Decision Gate 4→5**:
```
dependencies_mapped = 모든 Task 간 의존성 매핑 완료
no_circular_deps = 순환 의존성 없음
parallel_groups_identified = 병렬 실행 가능 그룹 식별 완료

IF dependencies_mapped AND no_circular_deps AND parallel_groups_identified → Step 5 진행
ELSE IF circular_deps → 순환 의존성 해소 후 재매핑
ELSE → 미완료 항목 보완
```

## Step 5: Plan Output Format

**Tools**: `Write`, `Bash (mkdir -p)`

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
- **Glob 기반 Target Files 검증**:
  a. 모든 Task에 Target Files 필드 존재 확인
  b. `[M]` 파일: `Glob`으로 존재 확인 → 미존재 시 `[C]`로 변경 또는 경로 수정
  c. `[C]` 파일: `Glob`으로 미존재 확인 → 이미 존재하면 `[M]`으로 변경
  d. `[C]` 파일의 상위 디렉토리 존재 확인
  e. 전체 Target Files 수집 → 중복 파일 감지 → Parallel Execution Summary에 반영
  f. 중복 파일이 있는 Task는 순차 실행으로 표시

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

## Progressive Disclosure (Plan 출력 시)

```
1. Plan 요약 테이블 제시:
   | 항목 | 내용 |
   |------|------|
   | 총 Phase 수 | N |
   | 총 Task 수 | N |
   | 최대 병렬 실행 | N tasks |
   | 예상 File Conflicts | N개 |
   | 모델 추천 | ... |

2. AskUserQuestion: "상세 내용을 확인하시겠습니까?"
   옵션:
   1. "전체 Plan 확인" → 전체 출력
   2. "특정 Phase만" → 해당 Phase 상세 출력
   3. "파일로 저장" → IMPLEMENTATION_PLAN.md 저장
```

## Error Handling

| 상황 | 대응 |
|------|------|
| 스펙 파일 미발견 | `spec-create` 먼저 실행 권장 |
| 스펙 내용 모호 | AskUserQuestion으로 명확화 (최대 2라운드) |
| Target Files 경로 확인 불가 | 사용자에게 경로 확인 요청, TBD로 표시 |
| 순환 의존성 발견 | Task 분할 또는 사용자에게 우선순위 확인 |
| 기존 Plan 파일 존재 | `prev/PREV_IMPLEMENTATION_PLAN_<timestamp>.md`로 아카이브 |
| Plan이 25+ Task | Phase별 파일 분할 (IMPLEMENTATION_PLAN_PHASE_N.md) |
| 모호한 우선순위 | 사용자에게 P0-P3 확인 요청 |
| user_input.md 형식 오류 | 파싱 오류 보고, 자유 형식으로 해석 시도 |

## Additional Resources

### Reference Files
- **`references/advanced-patterns.md`** - Advanced planning patterns (microservices, migrations, risk-based)
- **`references/target-files-spec.md`** - Target Files field detailed specification

### Example Files
- **`examples/sample-plan-parallel.md`** - Complete implementation plan example with Target Files
