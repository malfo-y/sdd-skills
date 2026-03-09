---
name: implementation-plan
description: This skill should be used when the user asks to "create an implementation plan", "plan the implementation", "break down this spec", "create a development roadmap", "analyze requirements and create tasks", "create a parallel implementation plan", "plan parallel implementation", "병렬 구현 계획", "create parallel development roadmap", or wants a structured implementation plan with Target Files for parallel execution support.
version: 1.3.0
---

# Implementation Plan Creation (Parallel-Ready)

Create structured, actionable implementation plans from user specifications — with **Target Files** on every task to enable parallel execution via `implementation`.

## Hard Rule: Spec Documents Are Read-Only

- This skill may **read** the spec as input, but it **MUST NOT** modify any files under `_sdd/spec/`.
- Read the spec as a navigation map first: `Goal`, `Architecture Overview` (`Repository Map`, `Runtime Map`), `Component Details` (`Component Index`, `Overview`), `Open Questions`를 우선 추출한다.
- If the plan reveals missing or outdated spec information, classify it as:
  - `MUST update`: planning depends on missing behavior, boundary, flow, ownership, or environment context
  - `CONSIDER`: planning can proceed, but later spec sync will likely be needed
  - `NO update`: implementation planning is unaffected
- If a `MUST update` spec gap blocks safe planning, record it under `Spec Gaps` and recommend `spec-update-todo` before execution.
- If planning can proceed, keep the gap in `Open Questions` / `Spec Gaps` and continue with deterministic defaults.

## Implementation spec

1. Refer to the user input.
2. If the user input is not clear, refer to `_sdd/implementation/user_input.md` for the user specification.
3. If information remains unclear and there is no user specification:
   - Apply deterministic defaults.
   - Record conservative assumptions and unresolved points in `Open Questions`.

After processing `user_input.md`, rename it to `_processed_user_input.md` to mark it as processed inputs.

## Language

결과로 나오는 .md 파일의 내용은 한국어로 작성합니다.

## Process Overview

1. **Analyze the Specification** - Understand scope, requirements, and constraints
2. **Identify Components** - Break down into logical modules/features
3. **Define Tasks with Target Files** - Create granular, actionable work items with file-level scope
4. **Decompose into Phases** - Analyze task characteristics, auto-select strategy, group tasks into phases
5. **Establish Dependencies** - Map task relationships and critical path
6. **Output the Plan** - Present in structured, trackable format

## Interaction Rule (Non-Interactive)

- Do not ask mid-process questions.
- When requirements are ambiguous, continue with explicit assumptions and record unresolved items in `Open Questions`.
- Do not pause for phase strategy approval; phase grouping strategy is auto-selected by AI.

## Step 1: Specification Analysis

**Tools**: `Read`, `Glob`, `rg`, `Bash`

Read and analyze the provided specification as an exploration-first map:

- `Goal` → `Project Snapshot`, `Key Features`, `Non-Goals`
- `Architecture Overview` → `System Boundary`, `Repository Map`, `Runtime Map` (사용자/운영자 관점 서술 포함 시 우선)
- `Component Details` → `Component Index`, `Overview`
- `Usage Examples` → `Common Change Paths` (있으면)
- `Open Questions`

Then derive:
- **Core Requirements**: What must the system do?
- **Technical Constraints**: Languages, frameworks, integrations, performance requirements
- **Scope Boundaries**: What is explicitly in/out of scope?
- **Spec Gaps**: What information is missing from the spec but needed for planning? 특히 런타임 흐름 설명, 컴포넌트 동작 개요, 설계 의도 누락을 확인한다.
- **Unknowns/Risks**: What needs clarification or research?

If the specification is unclear or incomplete:
- proceed with assumptions and log unresolved points in `Open Questions`.

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
| 50-200 파일 | 타겟 탐색 | `rg`, `Glob`, `Read`, `Bash`로 후보 식별 → 타겟 `Read` |
| > 200 파일 | 타겟 탐색 | `rg`, `Glob`, `Read`, `Bash` 위주 → 최소한의 `Read` |

**Decision Gate 1→2**:
```
spec_loaded = 스펙 문서 읽기 완료
requirements_clear = 핵심 요구사항 파악 완료
scope_defined = 스코프 경계 정의 완료

IF spec_loaded AND requirements_clear AND scope_defined → Step 2 진행
ELSE IF NOT requirements_clear → 가정으로 진행하고 Open Questions에 미확정 항목 기록
ELSE → 미파악 항목 추가 분석 후 재평가
```

## Step 2: Component Identification

**Tools**: `rg`, `Glob`, `Read`, `Bash`

Break the system into logical components:

- Start from the spec's `Component Index` and `Overview` when available
- Group related functionality into modules
- Identify shared utilities and common patterns
- Note external dependencies and integrations
- Consider data models and storage requirements
- Map user-facing features vs internal services

## Step 3: Task Definition with Target Files

**Tools**: `rg`, `Glob`, `Read`, `Bash`

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

**Decision Gate 3→4**:
```
all_tasks_have_target_files = 모든 Task에 Target Files 매핑 완료
acceptance_criteria_defined = 모든 Task에 Acceptance Criteria 정의

IF all_tasks_have_target_files AND acceptance_criteria_defined → Step 4 진행
ELSE → 누락 항목 보완 후 재확인
```

## Step 4: Phase Decomposition (Auto Strategy)

**Tools**: `Read`, `rg`, `Glob`, `Bash`

정의된 Task들을 분석해 Phase 전략을 자동 선택하고 Phase로 그룹핑한다.

### 4.1 Task 특성 분석

정의된 Task 목록에서 다음 특성을 분석한다:

| 분석 항목 | 확인 내용 |
|-----------|----------|
| 의존성 깊이 | Task 간 의존 체인의 최대 깊이 |
| 위험도 분포 | 고위험/불확실 기술 항목 비율 |
| 우선순위 분포 | P0-P3 분포 |
| 기반 작업 유무 | 다른 Task의 전제가 되는 인프라/설정 Task 존재 여부 |
| 사용자 가치 분포 | 사용자 대면 기능 Task 비율 및 MVP 구성 가능성 |

### 4.2 Phase 전략 자동 선택

아래 우선순위 규칙으로 전략을 자동 결정한다:

```
risk_ratio = 고위험 Task 수 / 전체 Task 수
dep_depth = 최대 의존성 체인 깊이
has_user_facing = 사용자 대면 기능 Task 존재 여부
needs_incremental_release = 점진 배포/MVP 요구 여부

IF risk_ratio >= 0.30:
  strategy = Risk-First
ELSE IF dep_depth >= 3:
  strategy = Dependency-Driven
ELSE IF has_user_facing OR needs_incremental_release:
  strategy = MVP-First
ELSE:
  strategy = Dependency-Driven
```

전략별 기본 Phase 구조:

| 전략 | Phase 구조 |
|------|-----------|
| **MVP-First** | Phase 0: 기반 설정 → Phase 1: MVP → Phase 2+: 확장/개선 |
| **Risk-First** | Phase 1: 고위험 항목 검증 → Phase 2: 핵심 기능 → Phase 3: 저위험 확장 |
| **Dependency-Driven** | Phase 1: 기반 → Phase 2: 핵심 서비스 → Phase 3: 통합 → Phase 4: 마무리 |

> 상세 패턴 및 예시: `references/advanced-patterns.md`의 "Phase Planning Strategies" 참조

### 4.3 Phase 그룹핑

선택된 전략에 따라 Task를 Phase로 배치한다:

- 각 Phase에 명확한 목표/테마를 부여 (예: "기반 설정", "핵심 인증", "OAuth 통합")
- Phase 내 Task는 가능한 한 독립적으로 실행 가능하도록 배치
- Phase 간 의존성이 최소화되도록 구성 (Phase N의 Task는 Phase N-1 완료 후 시작 가능)
- 전략 선택 근거를 Plan 본문에 명시 (risk_ratio/dep_depth 등 핵심 지표 포함)

**Decision Gate 4→5**:
```
phases_defined = 모든 Task가 Phase에 배치 완료
phase_goals_clear = 각 Phase에 명확한 목표/테마 부여
strategy_rationale_recorded = 전략 선택 근거를 문서에 기록

IF phases_defined AND phase_goals_clear AND strategy_rationale_recorded → Step 5 진행
ELSE → 미완료 항목 보완 후 재확인
```

## Step 5: Dependency Mapping

**Tools**: `Glob` (Target Files 중복 확인)

Establish task relationships:

- **Blocks**: Tasks that must complete before others can start
- **Related**: Tasks that share context but aren't blocking
- **Parallel**: Tasks that can be worked on simultaneously (when Target Files don't overlap)

Create a dependency graph or critical path when complexity warrants.

**Parallel-specific**: After mapping dependencies, verify that tasks marked as parallel-eligible don't have overlapping Target Files.

**Decision Gate 5→6**:
```
dependencies_mapped = 모든 Task 간 의존성 매핑 완료
no_circular_deps = 순환 의존성 없음
parallel_groups_identified = 병렬 실행 가능 그룹 식별 완료

IF dependencies_mapped AND no_circular_deps AND parallel_groups_identified → Step 6 진행
ELSE IF circular_deps → 순환 의존성 해소 후 재매핑
ELSE → 미완료 항목 보완
```

## Step 6: Plan Output Format

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

## Spec Inputs Used
- **Goal**: [key feature / scope note]
- **Runtime Map**: [relevant flow + user-facing scenario]
- **Component Index**: [relevant component/path]
- **Component Overview**: [relevant behavior / design intent]
- **Common Change Paths**: [if relevant]

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

## Spec Gaps
- [ ] [planning에 영향 있는 spec gap]

## Expected Spec Sync Follow-ups
- `MUST update` / `CONSIDER`: [section] - [why]

## Open Questions
- [ ] [Question requiring clarification]

## Model Recommendation
[Model recommendation based on implementation complexity]
```

## Best Practices

- **Be Specific**: Vague tasks lead to scope creep
- **Spec-aware planning**: derive tasks from `Key Features`, `Runtime Map`, `Component Index`, `Overview`, and real paths
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

## Clarification Handling

If any of the following is encountered:

- Ambiguous requirements with multiple valid interpretations
- Missing technical constraints (language, framework, etc.)
- Unclear priority between competing features
- Unknown integration requirements
- Incomplete success criteria
- Uncertain file paths for Target Files

Then apply this rule:
- do not ask; continue with documented assumptions and list unresolved items in `Open Questions`.

## LLM Model to use

Use the following fixed mapping when users mention Opus/Sonnet/Haiku labels:

- `Opus` → `gpt-5.3-codex` (`reasoning effort: extra high`)
- `Sonnet` → `gpt-5.3-codex` (`reasoning effort: high`)
- `Haiku` → `gpt-5.3-codex` (`reasoning effort: medium`)

If the user does not specify a model family, default to `gpt-5.3-codex` and set reasoning effort based on implementation complexity.

## Output Location

After creating the plan, offer to:

1. Display in conversation (for review/discussion)
2. Save to a file to the user provided path, or default to `<project_root>/_sdd/implementation/IMPLEMENTATION_PLAN.md`
    - If the file already exists, archive it as `<project_root>/_sdd/implementation/prev/PREV_IMPLEMENTATION_PLAN_<timestamp>.md` (create `prev/` if needed) and create a new one.
3. If the plan is too large to fit comfortably in one file (e.g. >25 tasks), split the plan into multiple files:
    - Keep `IMPLEMENTATION_PLAN.md` as an index/overview and link to the phase files
    - Name phase files as `IMPLEMENTATION_PLAN_PHASE_1.md`, `IMPLEMENTATION_PLAN_PHASE_2.md`, etc.
4. Create tasks using plan document task table for tracking

Output format selection rule:
- use the user-specified path/format if given; otherwise use default path and sensible split policy.

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

2. 기본 동작으로 전체 Plan을 바로 출력한다.
3. 사용자가 특정 Phase 재출력/파일 저장 경로를 명시 요청한 경우에만 해당 요청을 반영한다.
```

## Error Handling

| 상황 | 대응 |
|------|------|
| 스펙 파일 미발견 | `spec-create` 먼저 실행 권장 |
| 스펙 내용 모호 | 가정으로 진행 + `Open Questions` 기록 |
| Target Files 경로 확인 불가 | 휴리스틱 추론 후 `TBD` + `Open Questions` 기록 |
| 순환 의존성 발견 | Task 분할로 해소, 해소 불가 시 `Open Questions`에 의사결정 필요 항목 기록 |
| 기존 Plan 파일 존재 | `prev/PREV_IMPLEMENTATION_PLAN_<timestamp>.md`로 아카이브 |
| Plan이 25+ Task | Phase별 파일 분할 (IMPLEMENTATION_PLAN_PHASE_N.md) |
| 모호한 우선순위 | 근거 기반 임시 우선순위 + `Open Questions` 기록 |
| user_input.md 형식 오류 | 파싱 오류 보고, 자유 형식으로 해석 시도 |

## Additional Resources

### Reference Files
- **`references/advanced-patterns.md`** - Advanced planning patterns (microservices, migrations, risk-based)
- **`references/target-files-spec.md`** - Target Files field detailed specification

### Example Files
- **`examples/sample-plan-parallel.md`** - Complete implementation plan example with Target Files
