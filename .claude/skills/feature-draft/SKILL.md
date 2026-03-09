---
name: feature-draft
description: This skill should be used when the user asks to "feature draft", "draft feature", "feature plan", "plan feature", "draft and plan", "feature draft parallel", "parallel feature draft", "병렬 기능 초안", "parallel feature plan", or wants to combine requirements gathering, spec patch drafting, and implementation planning with Target Files for parallel execution support.
version: 1.1.0
---

# Feature Draft - Exploration-First Spec Patch + Implementation Plan

좋은 스펙은 코드를 복사한 것이 아니다. 사람과 LLM이 다음을 할 수 있게 돕는 **탐색 가능한 지도**이다:
- 저장소가 무엇을 하는지 이해한다
- 기능이나 책임이 어디에 있는지 찾는다
- 어디를 안전하게 수정할 수 있는지 판단한다
- 비자명한 결정과 불변 조건을 기억한다

이 스킬은 기존 스펙을 읽고, 계획된 변경을 분석하여, **스펙 패치 초안(Part 1)** + **구현 계획(Part 2)**을 하나의 파일로 생성한다. Part 2의 모든 태스크에는 **Target Files** 필드가 포함되어 병렬 실행을 지원한다.

## Simplified Workflow

This skill is **Step 2 of 4** in the SDD workflow:

```
spec-create -> feature-draft (this) -> implementation -> spec-update-done
```

| Step | Skill | Purpose |
|------|-------|---------|
| 1 | spec-create | Create the initial index-first spec |
| **2** | **feature-draft** | Draft planned spec changes + implementation plan |
| 3 | implementation | Execute the plan |
| 4 | spec-update-done | Sync actual implementation back to spec |

> **Workflow**: spec-create -> feature-draft -> implementation -> spec-update-done

## Overview

This skill integrates spec patch drafting + implementation planning into a single step.
기존 스펙을 읽고 사용자 요구사항을 수집하여, 스펙 패치 초안(Part 1)과 Target Files가 포함된 구현 계획(Part 2)을 동시에 생성한다.

**This skill**: `feature-draft` (1 invocation, shared context)

## When to Use This Skill

- 새 기능을 계획하고 **병렬 실행 가능한** 구현 계획을 한 번에 만들고 싶을 때
- 스펙 패치와 구현 계획을 동시에 작성하고 싶을 때
- 스펙 패치 + 구현 계획을 하나의 단계로 처리하고 싶을 때
- 구현이 병렬 서브 에이전트 실행의 이점을 얻을 것으로 예상될 때

## Hard Rules

1. **No spec file modifications**: Files under `_sdd/spec/` are **read-only**. Never modify them.
2. **Output location**: Save to `_sdd/drafts/` directory.
3. **Write in Korean**: Output file content must be written in Korean.
4. **Multiple features supported**: Multiple features can be included in one file, but always confirm with the user first. Grouping rationale은 `Open Questions`에 기록한다.
5. **spec-update-todo compatible**: Part 1 must follow the `Spec Update Input` format defined in `references/output-format.md`.
6. **Target Files required**: Every task in Part 2 MUST include a `**Target Files**` field.
7. **[TBD] 허용**: Target Files에서 경로 미결정 시 `[TBD] <reason>` 마커를 사용할 수 있다.
8. **앵커 인식 드래프팅**: Target Section은 SDD 앵커 섹션(`Goal`, `Architecture Overview`, `Component Details`, `Environment & Dependencies`, `Identified Issues & Improvements`, `Usage Examples`, `Open Questions`)을 참조해야 한다.
9. **추정 명시**: 확인되지 않은 내용은 단정하지 않고 `Open Questions`에 기록한다.
10. **스펙 갱신 기준 적용**: Part 1 시작 전에 각 변경을 `MUST update`, `NO update`, `CONSIDER`로 분류한다.
11. **Change-oriented output**: Part 1 must help later readers understand what changes, where it changes, and what risks or invariants matter.
12. **실제 경로 우선**: 주요 컴포넌트와 변경 지점에는 실제 또는 강하게 추론된 파일/디렉토리 경로를 적는다.
13. **결정 로그 후보만 기록**: `DECISION_LOG.md`를 직접 쓰지 말고, 필요한 rationale은 draft 안의 `Decision-Log Candidates`로 남긴다.
14. **Token-efficient drafting**: 빈 선택 섹션은 만들지 않고, 반복 설명보다 경로, 표, 짧은 불릿을 우선한다.

## Input Sources

1. **User conversation (current session)**: Real-time requirements collection (primary)
2. **Existing draft files**: `_sdd/spec/user_draft.md` or `_sdd/spec/user_spec.md`
3. **Existing implementation input**: `_sdd/implementation/user_input.md`
4. **User-modified code**: Analyze changes via git diff etc.
5. **Other user-specified files**: Reference documents or notes
6. **Existing decision log**: `_sdd/spec/DECISION_LOG.md` (if present)

## Output

**File location**: `_sdd/drafts/feature_draft_<feature_name>.md`

**File structure** (single file, 2 parts):
- **Part 1**: Spec patch draft ("Spec Update Input" format + Target Section annotations)
- **Part 2**: Implementation plan with **Target Files** (per-phase tasks, details, risks)

**Optional**: `Decision-Log Candidates`를 draft 파일 내 `Notes` 섹션에 포함 (직접 `DECISION_LOG.md` 수정하지 않음)

## Process

### Step 1: Input Analysis

**Tools**: `Read`, `Glob`, `Bash (git diff)`

```
1. Review user conversation content
2. Check for existing files:
   - Glob("_sdd/spec/user_draft.md") (사용자 작성 초안)
   - Glob("_sdd/spec/user_spec.md") (user-authored)
   - Glob("_sdd/implementation/user_input.md") (implementation input)
3. Check code changes: Bash("git diff --name-only")
4. Read discovered input files
5. Consolidate requirements from all sources
6. Determine input completeness level (see references/adaptive-questions.md):
   - HIGH: Feature name + description + acceptance criteria + priority all present
   - MEDIUM: Feature name + description present but acceptance criteria or priority missing
   - LOW: Vague idea level
```

**Decision Gate 1→2**:
```
spec_exists = Glob("_sdd/spec/*.md") 중 프로젝트 스펙 파일 존재 여부
  (user_draft.md, user_spec.md, DECISION_LOG.md 제외)

IF spec_exists → Step 2 진행
ELSE → AskUserQuestion:
  1. "spec-create 먼저 실행" — 스킬 종료
  2. "Part 2만 생성" — Part 1 생략 모드로 진행
```

### Step 2: Context Gathering

**Tools**: `Glob`, `Read`, `Grep`

```
1. Read existing spec (read-only):
   - Glob("_sdd/spec/*.md")로 스펙 파일 목록 확인
   - Read로 스펙 읽기 (크기별 전략은 아래 Context Management 참조)
   - If spec is split, follow links from the index
2. Understand spec structure:
   - Section list (to determine where patches go)
   - Component list (to understand relationships with existing components)
   - Existing feature list (to prevent duplication)
   - Verify spec language/style (so patches match existing style)
3. Check Glob("_sdd/spec/DECISION_LOG.md") (if present):
   - Review existing decisions/rationale
   - Ensure new feature doesn't conflict with existing decisions
4. **Explore codebase** for Target Files:
   - Grep/Glob: 프로젝트 구조, 기존 패턴 파악
   - Glob: 소스/테스트/설정 파일 위치 확인
   - Note naming conventions for new files
   - Map which existing files will need modification
```

#### Context Management (Step 2 후 적용)

스펙과 코드베이스 크기에 따라 읽기 전략을 조절한다. 상세 전략은 `references/tool-and-gates.md` 참조.

| 스펙 크기 | 전략 |
|-----------|------|
| < 200줄 | 전체 읽기 |
| 200-500줄 | 전체 읽기 가능 |
| 500-1000줄 | TOC 먼저, 관련 섹션만 읽기 |
| > 1000줄 | 인덱스만, 타겟 섹션 최대 3개 |

| 코드베이스 크기 | 전략 |
|----------------|------|
| < 50 파일 | `Glob` + `Read` 자유 탐색 |
| 50-200 파일 | `Grep`/`Glob` + 타겟 `Read` |
| > 200 파일 | `Grep`/`Glob` 위주 |

### Step 3: Adaptive Clarification

**Tools**: `AskUserQuestion`

Apply different question strategies based on input completeness level:

**HIGH (detailed input)**: Proceed directly without questions. Only confirm collected information.

**MEDIUM (partial input)**: Ask only 1-3 key questions:
- Priority (High/Medium/Low)
- Acceptance Criteria
- Technical constraints

**LOW (vague input)**: Confirm type first, then ask required questions:
1. Confirm requirement type (new feature/improvement/bug/component/configuration)
2. Type-specific required questions (see references/adaptive-questions.md)
3. Use AskUserQuestion tool

**Multiple features check**:
- If multiple features are detected in user input:
  - Use AskUserQuestion to confirm: "It seems like multiple features are included. Would you like to include them all in one file, or separate them into individual files?"
  - Proceed based on user's choice

**Decision Gate 3→4**:
```
has_feature_name = 기능명이 명확한가?
has_description = 기능 설명이 충분한가?
has_type = 유형 분류가 가능한가? (New Feature / Improvement / Bug / etc.)

IF 모두 충족 → Step 4 진행
ELSE → 미충족 항목에 대해 AskUserQuestion (최대 2라운드)
  → 2라운드 후에도 미충족 시 → 가용 정보로 진행, 누락 항목은 Open Questions에 기록
```

### Step 4: Classify Spec Update Need

**Tools**: deterministic defaults (non-interactive)

Part 1 시작 전에 계획된 변경을 SDD §8 갱신 기준에 따라 분류한다.

| 분류 | 기준 | 예시 |
|------|------|------|
| `MUST update` | 사용자 가시 동작, 시스템 경계, 런타임 흐름, 소유권/계약 변경 | 새 API, 새 컴포넌트, 환경 요구사항 추가 |
| `NO update` | 내부 리팩토링, 테스트만 추가, 포맷팅/스타일 변경 | 함수 내부 로직 개선, lint 수정 |
| `CONSIDER` | 성능 튜닝, 마이너 의존성 업데이트, 내부 재조직 | 캐시 추가, 패치 버전 업데이트 |

- `NO update`인 경우, Part 1은 최소한의 no-op 노트(rationale 포함)로 대체할 수 있다.
- `CONSIDER`인 경우, 외부 노출 여부를 기준으로 판단하고 판단 근거를 `Open Questions`에 남긴다.

### Step 5: Feature Design

**Tools**: `Grep`, `Glob`

```
1. Classify requirements by type:
   - New Features
   - Improvements
   - Bug Reports
   - Component Changes
   - Environment & Dependency Changes

2. Map each item to target spec section (SDD 앵커 섹션 기준):
   | Type | Target Section |
   |------|----------------|
   | New Feature (Core) | Goal > Key Features |
   | New Feature (Component) | Component Details |
   | Architecture Change | Architecture Overview |
   | Improvement | Identified Issues & Improvements |
   | Bug Fix | Identified Issues & Improvements |
   | Performance | Identified Issues & Improvements |
   | Configuration | Environment & Dependencies |
   | Dependency | Environment & Dependencies |
   | API Change | Component Details > Interfaces |
   | Test Addition | (no spec update needed) |
   | Usage/Change Path | Usage Examples |

3. Identify implementation components:
   - Group related features into modules
   - Identify shared utilities/common patterns
   - Check external dependencies and integration points
   - Consider data model/storage requirements

4. **Map Target Files per task**:
   - For each task, identify which files will be created/modified/deleted
   - Grep: "이 기능과 관련된 기존 코드는?" 형태의 패턴 검색
   - Glob: 후보 파일 경로 존재 여부 검증
   - Verify no unnecessary file overlaps between tasks
   - Apply Target Files markers: [C] Create, [M] Modify, [D] Delete
   - 충돌 최소화: 5+ tasks/phase이고 파일 겹침 시 Step 7의 Conflict minimization patterns 참조
```

**Decision Gate 5→6**:
```
IF 요구사항 유형별 분류 완료
   AND 각 항목에 Target Section 매핑 완료 (SDD 앵커 섹션 기준)
   AND Target Files 초안 작성 완료
→ Step 6 진행
ELSE → 미완료 항목 보완 후 재확인
```

### Step 6: Spec Patch Generation = Part 1

**Tools**: — (출력 생성 단계, 도구 불필요)

Part 1 follows the `Spec Update Input` format with `**Target Section**` annotations added to each item.
Part 1의 시작과 끝에 호환성 마커를 포함한다:
- 시작: `<!-- spec-update-todo-input-start -->`
- 끝: `<!-- spec-update-todo-input-end -->`

**Format rules**:
- Full compliance with `Spec Update Input` format (spec-update-todo compatible)
- state `Spec Update Classification` (Step 4에서 결정한 MUST/NO/CONSIDER)
- Add `**Target Section**` to each item (SDD 앵커 섹션 기준)
- every meaningful item states affected components or paths
- behavior changes include acceptance criteria
- risky changes include `Risks / Invariants`
- decision-log-worthy rationale stays in `Notes > Decision-Log Candidates`
- unresolved assumptions are collected in `Open Questions`
- Match existing spec style/language
- See `references/output-format.md` for detailed format

**Change Recipes / Component Index 영향 체크**:
- 이 변경이 기존 Change Recipes에 영향을 주는가? → 해당 Change Recipe 업데이트 항목 추가
- 새 컴포넌트가 추가되는가? → Component Index 업데이트 항목 추가

If classification is `NO update`:
- keep Part 1 minimal
- explain why the spec does not need to change
- still record any follow-up uncertainty in `Open Questions`

```markdown
# Part 1: Spec Patch Draft

> This patch can be copy-pasted into the corresponding spec section,
> or used as input for the `spec-update-todo` skill.

# Spec Update Input

**Date**: YYYY-MM-DD
**Author**: [author]
**Target Spec**: [target spec filename]
**Spec Update Classification**: MUST update | NO update | CONSIDER

## New Features

### Feature: [feature name]
**Priority**: High/Medium/Low
**Category**: [category]
**Target Component**: [target component]
**Target Section**: `_sdd/spec/xxx.md` > `Goal > Key Features`

**Description**:
[feature description]

**Acceptance Criteria**:
- [ ] criterion 1
- [ ] criterion 2

**Technical Notes**:
[technical notes]

**Dependencies**:
[dependencies]

---

## Improvements

### Improvement: [improvement name]
**Priority**: High/Medium/Low
**Target Section**: `_sdd/spec/xxx.md` > `Identified Issues & Improvements`
**Current State**: [current state]
**Proposed**: [proposed change]
**Reason**: [reason]

---

## Bug Reports

### Bug: [bug name]
**Severity**: High/Medium/Low
**Target Section**: `_sdd/spec/xxx.md` > `Identified Issues & Improvements`
**Location**: [file:line]
**Description**: [bug description]
**Reproduction**: [steps]
**Expected Behavior**: [expected]

---

## Component Changes

### New Component: [component name]
**Target Section**: `_sdd/spec/xxx.md` > `Component Details`
**Owned Paths**:
- `src/...`
- `tests/...`

**Responsibility**:
- [what it does]

**Interfaces / Contracts**:
- Inputs: ...
- Outputs: ...

**Change Recipes**:
- [where future edits would begin]

---

## Environment & Dependency Changes

### Change: [name]
**Target Section**: `_sdd/spec/xxx.md` > `Environment & Dependencies`
**Type**: Dependency / Environment Variable / Runtime / Tooling / Setup Command

**Description**:
[what changes]

**Impact**:
- [setup/test/runtime impact]

---

## Notes

### Context
[additional context]

### Constraints
[constraints]

### Decision-Log Candidates
[rationale for non-obvious decisions]
```

> **상세 포맷**: 각 섹션의 전체 필드 목록과 선택/필수 구분은 `references/output-format.md`를 참고하세요.

### Step 6.5: Part 1 요약

Part 1 요약 테이블을 사용자에게 제시한 후 바로 Step 6으로 진행한다 (사용자 확인을 기다리지 않는다):

```
| 섹션 | 항목 수 | 주요 내용 |
|------|---------|----------|
| New Features | N | ... |
| Improvements | N | ... |
| ... | ... | ... |
```

### Step 7: Implementation Plan Generation = Part 2

**Tools**: — (출력 생성 단계, 도구 불필요)

Reuse the components and analysis results from Step 4 to create the implementation plan.
**Key requirement**: Every task includes a `**Target Files**` field.

**Implementation plan structure**:

```markdown
# Part 2: Implementation Plan

## Overview
[summary of what to implement]

## Scope
### In Scope
- [included items]

### Out of Scope
- [excluded items]

## Components
1. **[component name]**: description
2. **[component name]**: description

## Implementation Phases

### Phase 1: [phase name]
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 1  | ...  | P0       | -            | ...       |

### Phase 2: [phase name]
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 2  | ...  | P1       | 1            | ...       |

## Task Details

### Task 1: [clear, action-oriented title]
**Component**: [parent component]
**Priority**: [P0-Critical | P1-High | P2-Medium | P3-Low]
**Type**: [Feature | Bug | Refactor | Research | Infrastructure | Test]

**Description**:
[detailed description of work to be done]

**Acceptance Criteria**:
- [ ] [specific, measurable criterion]
- [ ] [additional criterion]

**Target Files**:
- [C] `src/services/new_service.py` -- 새 서비스 클래스
- [M] `src/config/settings.py` -- 설정 항목 추가
- [C] `tests/test_new_service.py` -- 단위 테스트

**Technical Notes**:
- [implementation hints, patterns to use]

**Dependencies**: [blocking task ID list]

## Parallel Execution Summary
| Phase | Total Tasks | Max Parallel | Sequential (conflicts) |
|-------|-------------|--------------|----------------------|
| 1     | N           | N            | 0                    |
| 2     | N           | N            | N                    |

## Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| ...  | ...    | ...        |

## Open Questions
- [ ] [question needing clarification]

## Model Recommendation
[model recommendation based on implementation complexity]
```

**Conflict minimization patterns** (5+ tasks/phase이고 파일 겹침이 많을 때 적용 권장):

| 패턴 | 상황 | 해결 |
|------|------|------|
| **Split-by-method** | 같은 파일에 독립 메서드 추가 | 별도 파일로 분리하여 각 태스크에 배정 |
| **Shared-config 격리** | 여러 태스크가 settings.py 수정 | 설정 전용 태스크로 통합 |
| **Test fixture 격리** | conftest.py 충돌 위험 | 디렉토리별 conftest 또는 setup 태스크 통합 |
| **Interface-first** | 공유 계약(인터페이스) 필요 | 인터페이스 정의 태스크를 먼저 실행 |

**Task definition rules**:
- Each task should be completable in a single work session
- Split into subtasks if too large
- Include infrastructure/setup tasks (CI/CD, environment configuration, etc.)
- Include test tasks (unit, integration, E2E)
- Include documentation tasks
- **Every task MUST have Target Files** (see `references/target-files-spec.md`)

**Target Files guidelines**:
- List ALL files the task will create, modify, or delete
- Use exact file paths (project root relative)
- Minimize overlap between tasks to maximize parallelization
- When overlap is unavoidable, note it in Technical Notes

**Dependency mapping**:
- **Blocks**: Tasks that cannot start until this task is complete
- **Related**: Shares context but no blocking relationship
- **Parallel**: Can be worked on concurrently (when Target Files don't overlap)

**Phase strategy** (choose based on complexity):
- **MVP-First**: Foundation → MVP → Core → Nice-to-Have
- **Risk-First**: High-risk items → Core → Low-risk items
- **Dependency-Driven**: Foundation → Services → Integration → Polish

**Model recommendation**:
Estimate implementation scale and complexity to recommend an appropriate model.
See "Model aliases" at https://code.claude.com/docs/en/model-config.

**Decision Gate 7→8**:
```
IF Part 1 (또는 Part 2 only 모드) + Part 2 + 병렬 실행 요약 모두 생성 완료
→ Step 8 진행
ELSE → 미완료 파트 생성 후 재확인
```

### Step 8: Review, Save, and Finalize

**Tools**: `Write`, `Bash (mkdir/mv)`, `Glob`

```
1. 요약 테이블 제시 (Part 1 항목 수 + Part 2 Phase/Tasks/병렬도)
2. **Verify Target Files** (Glob 기반 검증):
   a. Every task has Target Files
   b. [M] 파일: Glob으로 존재 확인 → 미존재 시 [C]로 변경 또는 경로 수정
   c. [C] 파일: Glob으로 미존재 확인 → 이미 존재하면 [M]으로 변경
   d. [C] 파일의 상위 디렉토리 존재 확인
   e. 전체 Target Files 수집 → 중복 파일 감지 → 병렬 실행 요약에 반영
   f. Review overlaps and note which tasks must be sequential

5. Save file:
   a. Create `_sdd/drafts/` directory (if it doesn't exist)
   b. Archive existing file (if a file with the same name exists):
      - `_sdd/drafts/prev/prev_feature_draft_<name>_<timestamp>.md`
   c. Save: `_sdd/drafts/feature_draft_<feature_name>.md`

6. Process input files (드래프트 저장 성공 후에만 실행):
   - `user_draft.md` → `_processed_user_draft.md`
   - `user_spec.md` → `_processed_user_spec.md`
   - `user_input.md` → `_processed_user_input.md`
   Add processing metadata:
   <!-- Processed: YYYY-MM-DD -->
   <!-- Applied to: feature_draft_<name>.md -->

7. Provide next steps guidance:
```

**Completion message template**:

```markdown
## Feature Draft Complete (Parallel-Ready)

**File**: `_sdd/drafts/feature_draft_<name>.md`
**Date**: YYYY-MM-DD

### Contents
| Part | Content | Item Count |
|------|---------|------------|
| Part 1 | Spec patch draft | N items |
| Part 2 | Implementation plan (with Target Files) | N tasks (M phases) |

### Parallel Execution Summary
| Phase | Total Tasks | Max Parallel | Sequential (conflicts) |
|-------|-------------|--------------|----------------------|
| 1     | N           | N            | 0                    |
| 2     | N           | N            | N                    |

> `Max Parallel = Total Tasks - Sequential(conflict)`. Conflict = 동일 파일에 [M] 마커를 포함하는 Task 쌍.

### Input Files Processed
- [x] `user_draft.md` → `_processed_user_draft.md` (if used)
- [x] `user_spec.md` → `_processed_user_spec.md` (if used)

### Next Steps
Apply spec patch (choose one):
- **Method A (automatic)**: Run `spec-update-todo` → use Part 1 as input
- **Method B (manual)**: Copy-paste each patch from Part 1 to the target section

Execute implementation:
- **Parallel**: Run `implementation` skill → use Part 2 as implementation plan
- **Sequential**: Execute tasks sequentially (Target Files ignored)

### Model Recommendation
[model recommendation for implementation]
```

## File Management Rules

### Output Filename
- Format: `feature_draft_<feature_name>.md`
- `<feature_name>`: lowercase English, underscore-separated (e.g., `real_time_notification`)
- For multiple features: use representative feature name or group name (e.g., `feature_draft_v2_features.md`)

### Archive
- Location: `_sdd/drafts/prev/`
- Format: `prev_feature_draft_<name>_<timestamp>.md`
- Archive only when a file with the same name already exists

### File Size Management
- When exceeding 25 tasks, suggest per-phase split option to user:
  - Main file: `feature_draft_<name>.md` (index + Part 1)
  - Phase files: `feature_draft_<name>_phase_1.md`, `feature_draft_<name>_phase_2.md`, ...

## Best Practices

### Effective Requirements Gathering
- **Be specific**: Provide clear criteria rather than vague expressions
- **Include examples**: Collect concrete usage examples when possible
- **Specify priority**: Assign priority to all items
- **Explain context**: Record why something is needed

### Spec Patch Quality
- **Style consistency**: Match the existing spec's language/format
- **앵커 섹션 정확성**: Target Section은 SDD 앵커 섹션(`Goal`, `Architecture Overview`, `Component Details`, `Environment & Dependencies`, `Identified Issues & Improvements`, `Usage Examples`, `Open Questions`)을 기준으로 매핑
- **Status markers**: Use 📋 Planned marker
- **Compatibility**: Full compliance with spec-update-todo input format
- **Change Recipes / Component Index**: 변경이 기존 Change Recipes에 영향을 주거나 새 컴포넌트가 추가되면 해당 업데이트 항목 포함

### Implementation Plan Quality
- **Specific tasks**: Vague tasks cause scope creep
- **Include infrastructure**: CI/CD, environment configuration, tool setup
- **Include tests**: Unit, integration, E2E test tasks
- **Consider operations**: Monitoring, logging, deployment procedures
- **Document decisions**: Record reasons for choosing specific approaches
- **Identify MVP**: Mark tasks essential for initial release

### Target Files Quality (Parallel-Specific)
- **Be precise**: Use exact file paths, not directory names
- **Minimize overlaps**: Design tasks to touch different files when possible
- **Include tests**: Always list the test file alongside the source file
- **Think about configs**: Don't forget shared config/settings files that multiple tasks may need
- **Verify with codebase**: Check actual project structure before naming files

## Error Handling

| Situation | Response |
|-----------|----------|
| `_sdd/spec/` directory missing | Recommend running `spec-create` first |
| Spec file missing | Can generate Part 2 only without spec (Part 1 requires spec) |
| `_sdd/drafts/` directory missing | Create automatically |
| Existing feature_draft file | Archive to `prev/` then create new |
| Incomplete information | Supplement with adaptive questions |
| User interrupts | Save content gathered so far |
| Multiple features detected in input | Confirm with user (single file vs separate) |
| Cannot determine Target Files | Ask user for file paths, or note as TBD |

## Workflow Integration

```
spec-create -> feature-draft -> implementation -> spec-update-done

Parallel workflow:
  feature-draft
       ↓
  _sdd/drafts/feature_draft_<name>.md
       ↓                        ↓
       ↓    spec-update-todo    ↓
       ↓                        ↓
  implementation ←─────┘
       ↓
  spec-update-done

Non-parallel fallback:
  Output is compatible with sequential execution mode (Target Files ignored)
```

## Additional Resources

### Reference Files
- **`references/adaptive-questions.md`** - Adaptive mode question guide (completeness level assessment + type-specific questions)
- **`references/output-format.md`** - Output file detailed format specification (with Target Files extension)
- **`references/target-files-spec.md`** - Target Files field detailed specification
- **`references/tool-and-gates.md`** - Step별 도구 매핑, Decision Gates, Context Management 전략

### Example Files
- **`examples/feature_draft_parallel.md`** - Completed output example file with Target Files
