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

1. **스펙 이외의 코드 파일 수정 금지**: 이 스킬은 `_sdd/spec/` 아래 스펙 문서만 생성한다. 기존 코드 파일을 수정하지 않는다.
2. **한국어 작성**: 스펙 문서 내용은 한국어로 작성한다 (사용자 지정 시 해당 언어 사용).
3. **출력 위치 준수**: `_sdd/spec/` 디렉토리에만 파일을 저장한다.
4. **기존 스펙 보존**: 이미 스펙 파일이 존재하면 덮어쓰기 전 반드시 `prev/PREV_<filename>_<timestamp>.md`로 백업한다.
5. **DECISION_LOG.md 최소화**: 결정 로그는 `DECISION_LOG.md`에만 기록하며, 추가 거버넌스 문서는 사용자 요청 시에만 생성한다.

## Directory Structure

```
_sdd/
├── spec/
│   ├── main.md             # Main spec document (or <project-name>.md)
│   ├── <component>.md      # Component-specific specs (for large projects)
│   ├── user_draft.md        # User requirements (if exists)
│   └── DECISION_LOG.md      # Why/decision rationale log (optional, recommended)
└── implementation/
    └── IMPLEMENTATION_PLAN.md  # Implementation plan (if exists)
```

## Spec Document Creation Process

### Step 1: Gather Information

**Tools**: `Read`, `Glob`, `AskUserQuestion`

Before creating a spec document, collect:

1. **From User Input**: Direct requirements and constraints
2. **From Existing Code**: Analyze codebase structure and patterns
3. **From Documentation**: Read existing README, comments, configs
4. **From Decision Log**: Read `_sdd/spec/DECISION_LOG.md` if it exists
5. **Clarification**: Use AskUserQuestion for ambiguous requirements

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
| 50-200 파일 | 타겟 탐색 | `Grep`/`Glob`으로 후보 식별 → 타겟 `Read` |
| > 200 파일 | 시맨틱 위주 | `Grep`/`Glob` 위주 → 최소한의 `Read` |

**Decision Gate 1→2**:
```
input_sufficient = (사용자 입력 OR user_draft.md OR 기존 문서) 중 하나 이상 존재
project_readable = 프로젝트 코드/README 등 분석 가능한 소스 존재

IF input_sufficient AND project_readable → Step 2 진행
ELSE IF NOT input_sufficient → AskUserQuestion: 프로젝트 설명 요청
ELSE IF NOT project_readable → AskUserQuestion: 프로젝트 경로/접근 방법 확인
```

### Step 2: Analyze the Project

**Tools**: `Grep`, `Glob`, `Read`

Explore the codebase to understand:

- Project structure and file organization
- Main entry points and components
- Dependencies and external integrations
- Data flow and architecture patterns
- Known issues and limitations

### Step 2.5: 분석 결과 확인 (Checkpoint)

**Tools**: `AskUserQuestion`

```
1. 분석 결과 요약 테이블을 사용자에게 제시:
   | 항목 | 파악 내용 |
   |------|----------|
   | 프로젝트 목표 | ... |
   | 주요 컴포넌트 | N개 식별 |
   | 기술 스택 | ... |
   | 이슈/개선사항 | N개 발견 |

2. AskUserQuestion: "분석 결과를 확인해 주세요."
   옵션:
   1. "확인, 스펙 작성 진행" → Step 3
   2. "수정/보완 필요" → 수정 사항 반영 후 재제시 (최대 2라운드)
```

**Decision Gate 2→3**:
```
has_goal = 프로젝트 목표 파악 완료
has_architecture = 아키텍처 구조 파악 완료
has_components = 주요 컴포넌트 식별 완료

IF has_goal AND has_architecture AND has_components → Step 3 진행
ELSE → 미파악 항목에 대해 추가 탐색 또는 AskUserQuestion
```

### Step 3: Write the Spec Document

**Tools**: `Write`, `Bash (mkdir -p)`

Follow the template structure below, adapting sections as needed:

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
2. Analyze project using explore agent or direct reading
3. Write spec following template structure
4. Save as `<project-name>.md` or `main.md`
5. If decisions or trade-offs were made during drafting, create/update `_sdd/spec/DECISION_LOG.md`
6. **출력 검증** (Glob 기반):
   a. `Glob("_sdd/spec/<project>.md")` → 생성 파일 존재 확인
   b. 필수 섹션 포함 확인: Goal, Architecture, Component Details, Environment
   c. 500줄 초과 시 → 모듈 분할 제안
   d. `DECISION_LOG.md` 생성 여부 확인 (결정 사항이 있었을 경우)
   e. 링크/경로 유효성 확인

Minimal decision log entry format:
```markdown
## YYYY-MM-DD - [Decision Title]
- Context:
- Decision:
- Rationale:
- Alternatives considered:
- Impact / follow-up:
```

### Modular Specs for Large Projects

For large projects, split into multiple files:

```
_sdd/spec/
├── main.md              # Overview and cross-references
├── api-spec.md          # API component spec
├── database-spec.md     # Database component spec
└── frontend-spec.md     # Frontend component spec
```

Reference sub-specs from main:
```markdown
## Component Details

See detailed specs:
- [API Specification](./api-spec.md)
- [Database Specification](./database-spec.md)
```

## Best Practices

### Writing Quality

- **Be Specific**: Avoid vague descriptions
- **Use Examples**: Include code snippets and usage examples
- **Stay Current**: Update spec when code changes significantly
- **Link to Code**: Reference file paths and line numbers when helpful

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
- If unclear, use AskUserQuestion to confirm preferred language

## Output Location

Save spec documents to:
- **Default**: `_sdd/spec/<project-name>.md` or `_sdd/spec/main.md`
- **User Specified**: Any path the user requests
- **Create directories**: Automatically create `_sdd/spec/` if needed
- **Decision log**: `_sdd/spec/DECISION_LOG.md` (when decisions/rationale need to be preserved)

## Progressive Disclosure (완료 시)

```
1. 완료 요약 테이블 제시:
   | 항목 | 내용 |
   |------|------|
   | 생성 파일 | `_sdd/spec/<project>.md` |
   | 총 줄 수 | N줄 |
   | 주요 섹션 | Goal, Architecture, Components, ... |
   | Decision Log | 생성됨/미생성 |

2. AskUserQuestion: "상세 내용을 확인하시겠습니까?"
   옵션:
   1. "전체 확인" → 전체 문서 출력
   2. "특정 섹션만" → 섹션 선택 후 해당 부분만 출력
   3. "확인 완료" → 종료
```

## Error Handling

| 상황 | 대응 |
|------|------|
| `_sdd/spec/` 디렉토리 미존재 | 자동 생성 (`mkdir -p _sdd/spec/`) |
| 기존 스펙 파일 존재 | `prev/PREV_<filename>_<timestamp>.md`로 백업 후 새로 생성 |
| 프로젝트 코드 접근 불가 | 사용자에게 경로 확인 요청 |
| user_draft.md 형식 오류 | 파싱 오류 위치 보고, 자유 형식으로 해석 시도 |
| 불완전한 사용자 입력 | AskUserQuestion으로 보완 (최대 2라운드) |
| 대형 프로젝트 (200+ 파일) | `Grep`/`Glob` 위주 탐색, 핵심 컴포넌트만 문서화 |
| 다국어 혼재 | 사용자에게 언어 선호도 확인 |
| DECISION_LOG.md 충돌 | 기존 항목 보존, 새 항목만 추가 |

## Additional Resources

### Reference Files
- **`references/template-full.md`** - Complete template with all sections
- **`references/examples.md`** - Real-world spec examples

### Example Files
- **`examples/simple-project-spec.md`** - Minimal spec for small projects
- **`examples/complex-project-spec.md`** - Full spec for large projects

## Integration with Other Skills

This skill works well with:
- **feature-draft**: Draft feature spec patch + implementation plan (next step in simplified workflow)
- **implementation**: Implement features based on spec
- **spec-update-done**: Sync spec with actual code after implementation
