---
name: spec-create
description: This skill should be used when the user asks to "create a spec", "write a spec document", "generate SDD", "create software design document", "document the project", "create spec for project", or mentions "_sdd" directory, specification documents, or project documentation needs.
version: 1.0.0
---

# Spec Document Creation and Management

Create and manage Software Design Description (SDD) spec documents for projects. Spec documents provide comprehensive technical documentation including goals, architecture, components, and usage examples.
Use Korean (한국어) for the spec document.

## Simplified Workflow

This skill is **Step 1 of 4** in the simplified SDD workflow:

```
spec (this) → feature-draft → implementation → spec-update-done
```

| Step | Skill | Purpose |
|------|-------|---------|
| **1** | **spec-create** | Create the initial spec document |
| 2 | feature-draft | Draft feature spec patch + implementation plan |
| 3 | implementation | Execute the implementation plan (TDD) |
| 4 | spec-update-done | Sync spec with actual code |

> **Workflow**: spec → feature-draft → implementation → spec-update-done

## Overview

Spec documents are stored in the `_sdd/spec/` directory within the project root. They follow a standardized structure to ensure consistency and completeness across different projects.

## When to Use This Skill

- Creating new spec documents for projects
- Breaking down large projects into modular spec files
- Generating documentation from existing code

## Hard Rules

1. **코드 파일 수정 금지**: `src/`, `tests/` 등 구현 코드 파일은 수정하지 않는다.
2. **한국어 작성**: 스펙 문서 내용은 한국어로 작성한다 (사용자 지정 시 해당 언어 사용).
3. **출력 위치 준수**: 스펙은 `_sdd/spec/`에 저장하고, 초기 부트스트랩 파일은 `<project_root>/AGENTS.md`, `<project_root>/CLAUDE.md`, `<project_root>/_sdd/env.md`에만 생성한다.
4. **기존 스펙 보존**: 이미 스펙 파일이 존재하면 덮어쓰기 전 반드시 `prev/PREV_<filename>_<timestamp>.md`로 백업한다.
5. **부트스트랩 파일 최소 수정 원칙**: `AGENTS.md`, `CLAUDE.md`, `_sdd/env.md`가 이미 존재할 때 필수 안내 문구가 누락된 경우, 반드시 자동 검증 후 필요한 문구만 최소 추가한다.
6. **DECISION_LOG.md 최소화**: 결정 로그는 `DECISION_LOG.md`에만 기록하며, 추가 거버넌스 문서는 사용자 요청 시에만 생성한다.

## Directory Structure

```
<project-root>/
├── AGENTS.md             # Codex 작업 가이드 (없으면 생성)
├── CLAUDE.md             # Claude Code 작업 가이드 (없으면 생성)
└── _sdd/
    ├── env.md            # 환경/실행 가이드 (없으면 생성)
    ├── spec/
    │   ├── main.md             # 프로젝트 전체 스펙 (소규모) 또는 인덱스 (중/대규모)
    │   ├── <component>.md      # 컴포넌트별 스펙 (중규모)
    │   ├── <component>/        # 컴포넌트 서브디렉토리 (대규모)
    │   │   ├── overview.md
    │   │   └── ...
    │   ├── user_draft.md       # User requirements (if exists)
    │   └── DECISION_LOG.md     # Why/decision rationale log (optional, recommended)
    └── implementation/
        └── IMPLEMENTATION_PLAN.md  # Implementation plan (if exists)
```

### Spec Structure by Project Complexity

| 규모 | 구조 | 기준 |
|------|------|------|
| 소규모 | `main.md` 단일 파일 | 스펙 500줄 이하 |
| 중규모 | `main.md` (인덱스) + `<component>.md` | 스펙 500–1500줄 |
| 대규모 | `main.md` (인덱스) + `<component>/` 서브디렉토리 | 스펙 1500줄 초과 |

**소규모** — 단일 파일:
```
_sdd/spec/
└── main.md
```

**중규모** — main.md + 컴포넌트 파일:
```
_sdd/spec/
├── main.md              # 인덱스 (목표, 아키텍처 요약, 컴포넌트 링크)
├── api.md               # API 컴포넌트 스펙
├── database.md          # DB 컴포넌트 스펙
└── frontend.md          # 프론트엔드 컴포넌트 스펙
```

**대규모** — main.md + 컴포넌트 서브디렉토리:
```
_sdd/spec/
├── main.md              # 인덱스 (목표, 아키텍처 요약, 컴포넌트 링크)
├── api/                 # API 컴포넌트 디렉토리
│   ├── overview.md
│   ├── endpoints.md
│   └── auth.md
├── database/            # DB 컴포넌트 디렉토리
│   ├── overview.md
│   └── schema.md
└── frontend/            # 프론트엔드 컴포넌트 디렉토리
    ├── overview.md
    └── components.md
```

## Spec Document Creation Process

### Step 1: Gather Information

**Tools**: `Read`, `Glob`, `deterministic defaults (non-interactive)`

Before creating a spec document, collect:

1. **From User Input**: Direct requirements and constraints
2. **From Existing Code**: Analyze codebase structure and patterns
3. **From Documentation**: Read existing README, comments, configs
4. **From Decision Log**: Read `_sdd/spec/DECISION_LOG.md` if it exists
5. **Clarification**: Use deterministic defaults (non-interactive) for ambiguous requirements
6. **Bootstrap targets check**: `AGENTS.md`, `CLAUDE.md`, `_sdd/env.md` 존재 여부 확인

User input includes user conversation and user-specified files (defaults to `_sdd/spec/user_draft.md`).

#### Context Management (Step 1 후 적용)

| 스펙 크기 | 전략 | 구체적 방법 |
|-----------|------|-------------|
| < 200줄 | 전체 읽기 | `Read`로 전체 파일 읽기 |
| 200-500줄 | 전체 읽기 가능 | `Read`로 전체 읽기, 필요 시 섹션별 |
| 500-1000줄 | TOC 먼저, 관련 섹션만 | 상위 50줄(TOC) 읽기 → 관련 섹션만 `Read(offset, limit)` |
| > 1000줄 | 인덱스만, 타겟 최대 3개 | 인덱스/TOC만 읽기 → 타겟 섹션 최대 3개 선택적 읽기 |

| 코드베이스 크기 | 전략 | 구체적 방법 |
|----------------|------|-------------|
| < 50 파일 | 자유 탐색 | `Glob` + `Read` 자유롭게 사용 |
| 50-200 파일 | 타겟 탐색 | `rg`/`Glob`/`Read`/`Bash`으로 후보 식별 → 타겟 `Read` |
| > 200 파일 | 시맨틱 위주 | `rg`/`Glob`/`Read`/`Bash` 위주 → 최소한의 `Read` |

**Decision Gate 1→2**:
```
input_sufficient = (사용자 입력 OR user_draft.md OR 기존 문서) 중 하나 이상 존재
project_readable = 프로젝트 코드/README 등 분석 가능한 소스 존재

IF input_sufficient AND project_readable → Step 2 진행
ELSE IF NOT input_sufficient → deterministic defaults (non-interactive): 프로젝트 설명 요청
ELSE IF NOT project_readable → deterministic defaults (non-interactive): 프로젝트 경로/접근 방법 확인
```

### Step 2: Analyze the Project

**Tools**: `rg`, `Glob`, `Read`, `Bash`, `Read`

#### Codebase Existence Check

Determine whether an actual codebase exists for this project. A codebase is considered **present** when implementation source files (e.g., `*.py`, `*.ts`, `*.java`, `*.go`, `*.rs`, etc.) are found in the project directory via `Glob`. A project with only documentation, config stubs, or empty scaffolding is treated as **no codebase**.

- **Codebase exists** → populate `Source` fields in component tables during Step 3.
- **No codebase** (spec-only / greenfield project) → omit `Source` fields entirely from component tables.

#### Exploration

Explore the codebase to understand:

- Project structure and file organization
- Main entry points and components
- Dependencies and external integrations
- Data flow and architecture patterns
- Known issues and limitations

### Step 2.5: 분석 결과 확인 (Internal Check)

**Tools**: `deterministic defaults (non-interactive)`

```
1. 분석 결과 요약 테이블을 작업 로그로 제시:
   | 항목 | 파악 내용 |
   |------|----------|
   | 프로젝트 목표 | ... |
   | 주요 컴포넌트 | N개 식별 |
   | 기술 스택 | ... |
   | 이슈/개선사항 | N개 발견 |

2. deterministic defaults (non-interactive): "분석 결과를 확인해 주세요."
   자동 처리:
   - 스펙 작성을 바로 진행한다.
   - 분석 신뢰도가 낮은 항목은 보완 후 `Open Questions`에 기록한다.
```

**Decision Gate 2→3**:
```
has_goal = 프로젝트 목표 파악 완료
has_architecture = 아키텍처 구조 파악 완료
has_components = 주요 컴포넌트 식별 완료

IF has_goal AND has_architecture AND has_components → Step 3 진행
ELSE → 미파악 항목에 대해 추가 탐색 또는 deterministic defaults (non-interactive)
```

### Step 3: Bootstrap + Write the Spec Document

**Tools**: `Read`, `Edit`, `Write`, `Bash (mkdir -p)`

Before writing the spec, bootstrap guidance files if missing:

#### Step 3-A: Create missing workspace guidance files

1. Ensure `_sdd/` and `_sdd/spec/` directories exist.
2. If `<project_root>/AGENTS.md` is missing, create with:

```markdown
# Workspace Guidance

- 프로젝트 스펙 문서는 `_sdd/spec/`를 기준으로 확인합니다.
- 환경 관련 설정/실행 방법은 `_sdd/env.md`를 기준으로 확인합니다.
```

3. If `<project_root>/CLAUDE.md` is missing, create with:

```markdown
# Workspace Guidance

- 프로젝트 스펙 문서는 `_sdd/spec/`를 기준으로 확인합니다.
- 환경 관련 설정/실행 방법은 `_sdd/env.md`를 기준으로 확인합니다.
```

4. If `<project_root>/_sdd/env.md` is missing, create with TODO comments:

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
   - Check whether required guidance lines already exist:
     - `AGENTS.md` / `CLAUDE.md`: `_sdd/spec/` 참조 + `_sdd/env.md` 참조 문구
     - `_sdd/env.md`: 환경 정보 작성용 TODO 주석/섹션
  - If required lines are missing, append only the missing lines (minimal edit, preserve existing structure).
  - If confidence is low, keep a note in `Open Questions`.

Then write the spec document using the template structure below, adapting sections as needed:

```markdown
# <Project Name>

## Goal

Describe project goals in detail:
- Primary objective
- Key features
- Target users/use cases
- Success criteria

## Architecture Overview

Describe project architecture:
- High-level system design
- Component interactions
- Data flow diagrams (use text or ASCII art)
- Technology stack

## Component Details

### <Component Name>

For each major component, include:

| Aspect | Description |
|--------|-------------|
| **Purpose** | What this component does |
| **Input** | Expected inputs and formats |
| **Output** | Produced outputs and formats |
| **Dependencies** | Other components or external deps |
| **Source** | _(Include only when codebase exists)_ Mapped source files, classes, and functions. See Source field format in Best Practices > Writing Quality. |

**Architecture Details:**
- Implementation approach
- Key classes/functions
- Design patterns used

**How to Use:**
- API/interface examples
- Configuration options

**Known Issues:**
- Current limitations
- Planned improvements

## Environment & Dependencies

### Directory Structure
```
project/
├── src/
├── tests/
└── ...
```

### Dependencies
- Runtime dependencies
- Development dependencies
- Environment requirements

### Configuration
- Environment variables
- Config files
- Required credentials

## Identified Issues & Improvements

### Critical Bugs
- [ ] Issue description and location

### Code Quality Issues
- [ ] Technical debt items

### Missing Features
- [ ] Feature gaps

### Robustness & Reliability
- [ ] Error handling improvements needed

## Usage Examples

### Running the Project
```bash
# Command to run
```

### Common Operations
- Example 1: Description
- Example 2: Description

### Output Interpretation
- How to interpret results
```

## Spec Management Operations

### Creating a New Spec

1. Create `_sdd/spec/` directory if not exists
2. If missing, create `<project_root>/AGENTS.md` with `_sdd/spec` / `_sdd/env.md` reference lines
3. If missing, create `<project_root>/CLAUDE.md` with `_sdd/spec` / `_sdd/env.md` reference lines
4. If missing, create `<project_root>/_sdd/env.md` with TODO comments for environment details
5. If existing `AGENTS.md` / `CLAUDE.md` / `_sdd/env.md` lack required guidance lines, append only missing lines automatically
6. Analyze project using explore agent or direct reading
7. Write spec following template structure
8. Save as `<project-name>.md` or `main.md`
9. If decisions or trade-offs were made during drafting, create/update `_sdd/spec/DECISION_LOG.md`
10. **출력 검증** (Glob 기반):
   a. `Glob("_sdd/spec/<project>.md")` → 생성 파일 존재 확인
   b. 필수 섹션 포함 확인: Goal, Architecture, Component Details, Environment
   c. 500줄 초과 시 → 모듈 분할 제안
   d. `DECISION_LOG.md` 생성 여부 확인 (결정 사항이 있었을 경우)
   e. 링크/경로 유효성 확인
   f. `AGENTS.md`, `CLAUDE.md`, `_sdd/env.md`의 필수 안내 문구 존재 확인 (생성 또는 자동 최소 추가)

Minimal decision log entry format:
```markdown
## YYYY-MM-DD - [Decision Title]
- Context:
- Decision:
- Rationale:
- Alternatives considered:
- Impact / follow-up:
```

### Modular Specs (중규모 이상)

스펙이 500줄을 초과하면 컴포넌트별로 분할한다:

**중규모** — `main.md` + 컴포넌트 파일:
```
_sdd/spec/
├── main.md              # 인덱스 (목표, 아키텍처 요약, 컴포넌트 링크)
├── api.md
├── database.md
└── frontend.md
```

**대규모** — `main.md` + 컴포넌트 서브디렉토리:
```
_sdd/spec/
├── main.md              # 인덱스
├── api/
│   ├── overview.md
│   └── endpoints.md
└── database/
    ├── overview.md
    └── schema.md
```

Reference sub-specs from main:
```markdown
## Component Details

See detailed specs:
- `api.md` 또는 `api/overview.md`
- `database.md` 또는 `database/overview.md`
```

## Best Practices

### Writing Quality

- **Be Specific**: Avoid vague descriptions
- **Use Examples**: Include code snippets and usage examples
- **Stay Current**: Update spec when code changes significantly
- **Link to Code**: Reference file paths and line numbers when helpful. When a codebase exists, use the **Source** field in component tables to map each component to its implementation files. Source field format:
  ```
  | **Source** | `<relative/path/to/file>`: ClassName, function_name() |
  |            | `<relative/path/to/other>`: AnotherClass              |
  ```
  - Wrap file paths in backticks.
  - Use project-root-relative paths.
  - Group classes/functions by file; separate items within the same file with commas.
  - Use a new table row (`|            |`) per file for readability.
  - Omit the Source field entirely for spec-only / greenfield projects with no codebase (see Step 2 Codebase Existence Check).

### Organization

- **Logical Flow**: Start with overview, then details
- **Consistent Format**: Use same structure across components
- **Table of Contents**: Include for documents over 500 lines

### Completeness

- **All Components**: Document every major component
- **Error Cases**: Document error handling and edge cases
- **Dependencies**: List all external dependencies
- **Configuration**: Document all config options

### Decision Traceability

- **Record Why**: Capture non-obvious decisions in `_sdd/spec/DECISION_LOG.md`
- **Keep It Minimal**: A short rationale entry is enough; avoid verbose narrative
- **Update on Change**: Add a new entry when direction/assumption changes
- **Artifact Scope**: Default to `DECISION_LOG.md` only; do not create extra governance docs unless the user explicitly asks

## Language Preference

Follow user's language preference for spec content:
- Default to the language used in existing project documentation
- If unclear, infer preferred language from repository docs and record fallback choice in `Open Questions`

## Output Location

Save spec documents to:
- **Default**: `_sdd/spec/<project-name>.md` or `_sdd/spec/main.md`
- **User Specified**: Any path the user requests
- **Create directories**: Automatically create `_sdd/spec/` if needed
- **Bootstrap docs**: `<project_root>/AGENTS.md`, `<project_root>/CLAUDE.md`, `<project_root>/_sdd/env.md` (없으면 생성, 기존 파일은 누락 문구만 자동 최소 추가)
- **Decision log**: `_sdd/spec/DECISION_LOG.md` (when decisions/rationale need to be preserved)

## Progressive Disclosure (완료 시)

```
1. 완료 요약 테이블 제시:
   | 항목 | 내용 |
   |------|------|
   | 생성 파일 | `_sdd/spec/<project>.md` |
| 부트스트랩 파일 | `AGENTS.md` / `CLAUDE.md` / `_sdd/env.md` (신규 생성 또는 자동 최소 추가) |
   | 총 줄 수 | N줄 |
   | 주요 섹션 | Goal, Architecture, Components, ... |
   | Decision Log | 생성됨/미생성 |

2. 내부 자동 처리:
   - 전체 문서 출력
   - 중요 섹션(Goal/Architecture/Components) 별도 요약 출력
```

## Error Handling

| 상황 | 대응 |
|------|------|
| `_sdd/spec/` 디렉토리 미존재 | 자동 생성 (`mkdir -p _sdd/spec/`) |
| `AGENTS.md` / `CLAUDE.md` 미존재 | 표준 안내 문구로 새 파일 생성 |
| `_sdd/env.md` 미존재 | TODO 주석이 포함된 템플릿 파일 생성 |
| 기존 `AGENTS.md` / `CLAUDE.md` / `_sdd/env.md`에 필수 문구 누락 | 누락 문구 자동 최소 추가 |
| 기존 스펙 파일 존재 | `prev/PREV_<filename>_<timestamp>.md`로 백업 후 새로 생성 |
| 프로젝트 코드 접근 불가 | 코드 접근 불가 원인 기록 후 문서 기반 스펙 생성으로 폴백 |
| user_draft.md 형식 오류 | 파싱 오류 위치 보고, 자유 형식으로 해석 시도 |
| 불완전한 사용자 입력 | deterministic defaults (non-interactive)으로 보완 (최대 2라운드) |
| 대형 프로젝트 (200+ 파일) | `rg`/`Glob`/`Read`/`Bash` 위주 탐색, 핵심 컴포넌트만 문서화 |
| 다국어 혼재 | 저장소 문서 기준 언어로 통일, 예외는 `Open Questions` 기록 |
| DECISION_LOG.md 충돌 | 기존 항목 보존, 새 항목만 추가 |

## Additional Resources

### Reference Files
- **`references/template-full.md`** - Complete template with all sections

### Example Files
- **`examples/simple-project-spec.md`** - Minimal spec for small projects
- **`examples/complex-project-spec.md`** - Full spec for large projects
- **`examples/additional-specs.md`** - CLI, Web API, Data Pipeline spec examples

## Integration with Other Skills

This skill works well with:
- **feature-draft**: Draft feature spec patch + implementation plan (next step in simplified workflow)
- **implementation**: Implement features based on spec
- **spec-update-done**: Sync spec with actual code after implementation
