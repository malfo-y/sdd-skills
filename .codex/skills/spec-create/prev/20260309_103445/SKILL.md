---
name: spec-create
description: This skill should be used when the user asks to "create a spec", "write a spec document", "generate SDD", "create software design document", "document the project", "create spec for project", or mentions "_sdd" directory, specification documents, or project documentation needs.
version: 1.1.0
---

# Spec Document Creation and Management

Create exploration-first Software Design Description (SDD) documents.

A good spec is not a copy of the code. It is a searchable map that helps people and LLMs:
- understand what the repository does
- find where a feature or responsibility lives
- decide where to edit safely
- remember non-obvious decisions and invariants

Use Korean (한국어) for the spec document unless the user explicitly requests another language.

## Simplified Workflow

This skill is **Step 1 of 4** in the simplified SDD workflow:

```
spec (this) -> feature-draft -> implementation -> spec-update-done
```

| Step | Skill | Purpose |
|------|-------|---------|
| **1** | **spec-create** | Create the initial index-first spec |
| 2 | feature-draft | Draft feature spec patch + implementation plan |
| 3 | implementation | Execute the implementation plan (TDD) |
| 4 | spec-update-done | Sync spec with actual code |

> **Workflow**: spec -> feature-draft -> implementation -> spec-update-done

## Overview

Spec documents are stored in the `_sdd/spec/` directory within the project root.

Default output shape:
- `main.md` (or `<project-name>.md`) as the main entry point
- optional component spec files for complex or frequently changed areas
- `DECISION_LOG.md` only when rationale needs to be preserved

## When to Use This Skill

- Creating a new project spec from an existing codebase
- Bootstrapping `_sdd/spec/` for a repository that lacks structured documentation
- Producing a change-oriented map for a large project
- Splitting an initial spec into a main index plus component specs

## Hard Rules

1. **코드 파일 수정 금지**: `src/`, `tests/` 등 구현 코드 파일은 수정하지 않는다.
2. **한국어 작성**: 스펙 문서 내용은 한국어로 작성한다. 언어가 불명확하면 저장소 문서 기준 언어를 따르고, 판단 근거가 약하면 `Open Questions`에 남긴다.
3. **출력 위치 준수**: 스펙은 `_sdd/spec/`에 저장하고, 초기 부트스트랩 파일은 `<project_root>/AGENTS.md`, `<project_root>/CLAUDE.md`, `<project_root>/_sdd/env.md`에만 생성한다.
4. **기존 스펙 보존**: 이미 스펙 파일이 존재하면 덮어쓰기 전 반드시 `prev/PREV_<filename>_<timestamp>.md`로 백업한다.
5. **부트스트랩 파일 최소 수정 원칙**: `AGENTS.md`, `CLAUDE.md`, `_sdd/env.md`가 이미 존재할 때 필수 안내 문구가 누락된 경우, 필요한 문구만 최소 추가한다.
6. **DECISION_LOG.md 최소화**: 결정 로그는 `DECISION_LOG.md`에만 기록하며, 추가 거버넌스 문서는 사용자 요청 시에만 생성한다.
7. **호환 가능한 앵커 섹션 유지**: 기본적으로 `Goal`, `Architecture Overview`, `Component Details`, `Environment & Dependencies`, `Identified Issues & Improvements`, `Usage Examples`, `Open Questions` 섹션명을 유지한다. 내부 구조는 탐색형으로 재구성한다.
8. **실제 경로 우선**: 주요 컴포넌트와 변경 지점에는 가능하면 실제 파일/디렉토리 경로를 적는다.
9. **추정은 명시**: 확인되지 않은 내용은 단정하지 말고 `Open Questions`에 기록한다.
10. **요약 우선**: 코드 구조를 그대로 복사하지 말고 `의도`, `경계`, `계약`, `변경 지점`, `불변 조건`을 압축해서 정리한다.

## Directory Structure

```
<project-root>/
├── AGENTS.md
├── CLAUDE.md
└── _sdd/
    ├── env.md
    ├── spec/
    │   ├── main.md
    │   ├── <project-name>.md
    │   ├── <component>.md
    │   ├── user_draft.md
    │   └── DECISION_LOG.md
    └── implementation/
        └── IMPLEMENTATION_PLAN.md
```

## Required Deliverables

### 1. Main Spec (required)

The main spec must act as the repository entry point and change map.

Required top-level sections:
- `Goal`
- `Architecture Overview`
- `Component Details`
- `Environment & Dependencies`
- `Identified Issues & Improvements`
- `Usage Examples`
- `Open Questions`

Required inner content:
- `Goal`: project snapshot, key features, users/use cases, non-goals
- `Architecture Overview`: system boundary, repository map, runtime map, technology stack, cross-cutting invariants
- `Component Details`: component index plus detailed entries or links to split component files
- `Usage Examples`: running commands, common operations, and common change/debug entry points

### 2. Component Specs (optional but recommended for large projects)

Create a separate component spec when a component:
- spans multiple directories or layers
- owns an important contract or lifecycle
- is a frequent change hotspot
- has non-obvious invariants or operational risks

### 3. Decision Log (optional)

Use `_sdd/spec/DECISION_LOG.md` only when the spec needs to preserve why a direction, trade-off, or constraint exists.

## Spec Document Creation Process

### Step 1: Gather Information

**Tools**: `Read`, `Glob`, `rg`, deterministic defaults (non-interactive)

Collect:
1. **From User Input**: direct requirements, constraints, terminology
2. **From Existing Docs**: README, docs, config comments, architecture notes
3. **From Existing Spec Files**: `_sdd/spec/*.md`, especially `user_draft.md` and `DECISION_LOG.md`
4. **From Code**: entry points, key directories, dominant flows, component boundaries
5. **From Workspace Guidance**: `AGENTS.md`, `CLAUDE.md`, `_sdd/env.md` existence and completeness

User input includes the current conversation and user-specified files (default: `_sdd/spec/user_draft.md` if present).

#### Context Management (Step 1 after load)

| 스펙 크기 | 전략 | 구체적 방법 |
|-----------|------|-------------|
| < 200줄 | 전체 읽기 | 전체 파일 읽기 |
| 200-500줄 | 전체 읽기 가능 | 전체 읽기 후 필요한 섹션 재확인 |
| 500-1000줄 | TOC 먼저 | 상위 TOC 확인 후 관련 섹션만 읽기 |
| > 1000줄 | 인덱스 우선 | 인덱스/TOC와 핵심 섹션만 읽기 |

| 코드베이스 크기 | 전략 | 구체적 방법 |
|----------------|------|-------------|
| < 50 파일 | 자유 탐색 | `rg` + `Read` 중심 탐색 |
| 50-200 파일 | 타겟 탐색 | 파일 후보 식별 후 필요한 파일만 읽기 |
| > 200 파일 | 시맨틱 탐색 | `rg`, 디렉토리 맵, 엔트리포인트, 핵심 경로 위주로 요약 |

**Decision Gate 1->2**:
```
input_sufficient = (사용자 입력 OR user_draft.md OR 기존 문서) 중 하나 이상 존재
project_readable = 프로젝트 코드/README/설정 등 분석 가능한 소스 존재

IF input_sufficient AND project_readable -> Step 2
ELSE IF NOT input_sufficient -> deterministic defaults (non-interactive): 현재 저장소 관측 내용 기반 초안 작성
ELSE IF NOT project_readable -> deterministic defaults (non-interactive): 문서 기반 스펙으로 폴백하고 제약을 Open Questions에 기록
```

### Step 2: Analyze the Project

**Tools**: `rg`, `Glob`, `Read`, `Bash`

Extract the minimum map needed to support understanding and change:

| 항목 | 반드시 파악할 내용 |
|------|-------------------|
| 프로젝트 목표 | 저장소가 해결하는 문제, 주요 사용자, 비목표 |
| 시스템 경계 | 이 저장소가 책임지는 것 / 외부 시스템에 맡기는 것 |
| 주요 진입점 | 앱 시작점, CLI 엔트리포인트, 라우터, 배치 시작점 |
| 런타임 흐름 | 요청/이벤트/배치 기준 주요 흐름 |
| 저장소 구조 | 주요 디렉토리, 핵심 파일, 설정 위치 |
| 컴포넌트 경계 | 책임 단위, 핵심 심볼, 소유 경로 |
| 변경 핫스팟 | 자주 수정하는 영역, 계약 변경 시 영향 범위 |
| 불변 조건 | 깨지면 안 되는 계약, 순서, 상태 전이, 데이터 가정 |
| 미확인 영역 | 정보 부족, 추정, 신뢰도 낮은 부분 |

Prefer:
- `rg --files`, `rg <term>` for discovery
- targeted file reads instead of full-repo dumping
- explicit path references over generic prose

### Step 2.5: Internal Quality Gate

Before writing, check:
1. 신규 기여자가 이 문서만 보고 5분 안에 프로젝트의 목적과 큰 구조를 이해할 수 있는가?
2. 특정 기능 변경 시 어디부터 찾아야 하는지 시작 지점을 제시할 수 있는가?
3. 주요 컴포넌트에 실제 경로 또는 심볼이 연결되어 있는가?
4. 불변 조건과 외부 계약이 드러나는가?
5. 확신이 낮은 내용이 `Open Questions`에 분리되어 있는가?

If any answer is "no", continue exploration before drafting.

### Step 3: Bootstrap + Write the Spec Document

**Tools**: `Read`, `Edit`, `Write`, `Bash (mkdir -p)`

#### Step 3-A: Create Missing Workspace Guidance Files

1. Ensure `_sdd/` and `_sdd/spec/` directories exist.
2. If `<project_root>/AGENTS.md` is missing, create:

```markdown
# Workspace Guidance

- 프로젝트 스펙 문서는 `_sdd/spec/`를 기준으로 확인합니다.
- 환경 관련 설정/실행 방법은 `_sdd/env.md`를 기준으로 확인합니다.
```

3. If `<project_root>/CLAUDE.md` is missing, create:

```markdown
# Workspace Guidance

- 프로젝트 스펙 문서는 `_sdd/spec/`를 기준으로 확인합니다.
- 환경 관련 설정/실행 방법은 `_sdd/env.md`를 기준으로 확인합니다.
```

4. If `<project_root>/_sdd/env.md` is missing, create:

```markdown
# Environment Setup Guide

<!-- TODO: 프로젝트 실행/테스트에 필요한 환경 정보를 여기에 작성하세요. -->
<!-- 예: Python/Node 버전, 가상환경, 필수 환경변수, 실행 전 준비 서비스 -->

## Runtime
- <!-- 예: Python 3.11 -->

## Environment Variables
- <!-- 예: OPENAI_API_KEY=... -->

## Setup Commands
- <!-- 예: conda activate myenv -->
- <!-- 예: npm install -->
```

5. If files already exist:
   - verify required guidance lines exist
   - append only missing lines
   - preserve existing structure

#### Step 3-B: Write Order

1. **Write the main spec first** using `references/template-full.md`.
2. **Keep legacy top-level headings** but structure them as an index:
   - `Goal` -> project snapshot and scope
   - `Architecture Overview` -> system boundary, repository map, runtime map
   - `Component Details` -> component index and change-oriented details
3. **Split component specs only when needed**:
   - use the component template in `references/template-full.md`
   - link split files from the main spec
4. **Add optional sections only when materially relevant**:
   - use `references/optional-sections.md`
   - examples: API surface, data models, security, performance, deployment
5. **Record rationale separately** in `_sdd/spec/DECISION_LOG.md` when trade-offs matter.

#### Step 3-C: Writing Guidance

- Start with the repository map and runtime map before writing detailed component prose.
- Favor tables with actual paths over long narrative.
- For each important component, include:
  - responsibility
  - owned paths
  - key symbols or entry points
  - interfaces or contracts
  - change recipes
  - tests or observability pointers
  - risks or invariants
- Under `Usage Examples`, include:
  - how to run
  - how to test
  - common operations
  - common change/debug entry points

### Step 4: Output Validation

Validate:
1. Main spec file exists in `_sdd/spec/`.
2. Required top-level sections exist:
   - `Goal`
   - `Architecture Overview`
   - `Component Details`
   - `Environment & Dependencies`
   - `Identified Issues & Improvements`
   - `Usage Examples`
   - `Open Questions`
3. `Architecture Overview` includes a repository map and runtime map.
4. `Component Details` includes a component index with real paths or linked component spec files.
5. `Usage Examples` includes run/test instructions and at least one change/debug entry point.
6. Bootstrap guidance files exist and contain required lines.
7. `DECISION_LOG.md` exists if the drafting process introduced non-obvious decisions.
8. If the main spec becomes too large or component count is high, split it.

## Split Guidance

Split the spec when any of the following is true:
- the main spec exceeds roughly 350 lines and feels dense
- the repository has more than 7 major components
- a component owns an important contract and needs its own change guide
- one section starts turning into a mini-manual

Suggested split shape:

```
_sdd/spec/
├── main.md
├── auth.md
├── billing.md
├── jobs.md
└── DECISION_LOG.md
```

`main.md` should remain the entry point and link to component files.

## Best Practices

### Writing Quality

- **Fast first read**: make the first 30 lines answer "what is this repo?"
- **Change-oriented detail**: prioritize "where to edit" over exhaustive explanation
- **Path-first references**: include concrete directories, files, commands, and symbols
- **Trace unknowns**: uncertainty belongs in `Open Questions`, not hidden in confident prose

### Organization

- Keep stable top-level headings for downstream skill compatibility
- Put deep detail into component specs, not the main overview
- Use tables and bullet lists where they reduce scanning time

### Decision Traceability

- Record only meaningful decisions in `_sdd/spec/DECISION_LOG.md`
- Keep entries short and comparable over time
- Add a new entry when assumptions or trade-offs change

## Language Preference

Follow the user's language preference for spec content.
- Default: Korean
- If the repository is already documented in another language, align with that language
- If ambiguous, choose one language consistently and explain the assumption in `Open Questions`

## Output Location

Save spec documents to:
- **Default**: `_sdd/spec/<project-name>.md` or `_sdd/spec/main.md`
- **User specified**: any path the user explicitly asks for
- **Bootstrap docs**: `<project_root>/AGENTS.md`, `<project_root>/CLAUDE.md`, `<project_root>/_sdd/env.md`
- **Decision log**: `_sdd/spec/DECISION_LOG.md`

## Progressive Disclosure (완료 시)

Report:

| 항목 | 내용 |
|------|------|
| 생성 파일 | `_sdd/spec/<project>.md`, component specs |
| 부트스트랩 파일 | `AGENTS.md`, `CLAUDE.md`, `_sdd/env.md` |
| 컴포넌트 수 | N개 |
| 분할 여부 | 단일 문서 / 다중 문서 |
| Open Questions | N개 |
| Decision Log | 생성됨 / 미생성 |

Also summarize:
- 프로젝트 목표와 경계
- 핵심 컴포넌트와 변경 핫스팟
- 남아 있는 불확실성

## Error Handling

| 상황 | 대응 |
|------|------|
| `_sdd/spec/` 디렉토리 미존재 | 자동 생성 |
| `AGENTS.md` / `CLAUDE.md` / `_sdd/env.md` 미존재 | 표준 파일 생성 |
| 기존 가이드 파일에 필수 문구 누락 | 누락 문구만 최소 추가 |
| 기존 스펙 파일 존재 | `prev/PREV_<filename>_<timestamp>.md`로 백업 후 생성 |
| 프로젝트 코드 접근 불가 | 문서 기반 스펙으로 폴백하고 제약을 `Open Questions`에 기록 |
| 대형 프로젝트 | 핵심 경로와 컴포넌트 위주로 요약, 필요 시 분할 |
| 신뢰도 낮은 추정 | `Open Questions`에 분리 기록 |
| DECISION_LOG.md 충돌 | 기존 항목 보존, 새 항목만 추가 |

## Additional Resources

### Reference Files
- `references/template-full.md` - index-first main spec and component spec templates
- `references/optional-sections.md` - optional appendices for APIs, data models, security, performance, deployment
- `references/examples.md` - guidance on choosing and reading the examples

### Example Files
- `examples/simple-project-spec.md` - small project example with one main spec
- `examples/complex-project-spec.md` - large project example with index-first structure

## Integration with Other Skills

This skill works well with:
- **feature-draft**: uses `Goal > Key Features` and `Component Details` as patch targets
- **implementation**: implements against the spec
- **spec-update-done**: updates the spec after completed implementation
- **spec-summary**: summarizes the stable top-level sections created here
