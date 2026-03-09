---
name: spec-create
description: This skill should be used when the user asks to "create a spec", "write a spec document", "generate SDD", "create software design document", "document the project", "create spec for project", or mentions "_sdd" directory, specification documents, or project documentation needs.
version: 1.0.0
---

# Spec Document Creation and Management

Create and manage Software Design Description (SDD) spec documents for projects. Spec documents provide comprehensive technical documentation including goals, architecture, components, and usage examples.
기존 스펙/문서의 언어를 따른다. 새 프로젝트는 한국어 기본.

## Workflow Position

| Workflow | Position | When |
|----------|----------|------|
| All | Pre-step | 스펙이 없을 때 먼저 실행 |

## Overview

Spec documents are stored in the `_sdd/spec/` directory within the project root. They follow a standardized structure to ensure consistency and completeness across different projects.

## When to Use This Skill

- Creating new spec documents for projects
- Breaking down large projects into modular spec files
- Generating documentation from existing code

## Hard Rules

1. **코드 파일 수정 금지**: `src/`, `tests/` 등 구현 코드 파일은 수정하지 않는다.
2. **언어 규칙**: 기존 스펙/문서의 언어를 따른다. 새 프로젝트(기존 스펙 없음)는 한국어 기본. 사용자 명시 지정 시 해당 언어 사용.
3. **출력 위치 준수**: 스펙은 `_sdd/spec/`에 저장하고, 초기 부트스트랩 파일은 `<project_root>/AGENTS.md`, `<project_root>/CLAUDE.md`, `<project_root>/_sdd/env.md`에만 생성한다.
4. **기존 스펙 보존**: 이미 스펙 파일이 존재하면 덮어쓰기 전 반드시 `prev/PREV_<filename>_<timestamp>.md`로 백업한다.
5. **부트스트랩 파일 최소 수정 원칙**: `AGENTS.md`, `CLAUDE.md`, `_sdd/env.md`가 이미 존재할 때 필수 안내 문구가 누락된 경우, 반드시 사용자 확인 후 필요한 문구만 최소 추가한다.
6. **DECISION_LOG.md 최소화**: 결정 로그는 `DECISION_LOG.md`에만 기록하며, 추가 거버넌스 문서는 사용자 요청 시에만 생성한다.

## Directory Structure

```
<project-root>/
├── AGENTS.md             # Codex 작업 가이드 (없으면 생성)
├── CLAUDE.md             # Claude Code 작업 가이드 (없으면 생성)
└── _sdd/
    ├── env.md            # 환경/실행 가이드 (없으면 생성)
    ├── spec/
    │   ├── main.md             # Main spec document (or <project-name>.md)
    │   ├── <component>.md      # Component-specific specs (for large projects)
    │   ├── user_draft.md       # User requirements (if exists)
    │   └── DECISION_LOG.md     # Why/decision rationale log (optional, recommended)
    └── implementation/
        └── IMPLEMENTATION_PLAN.md  # Implementation plan (if exists)
```

Legacy shorthand:
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

분석 완료 후 반드시 다음 두 단계를 순서대로 수행한다:

**① 텍스트 출력으로 분석 결과 테이블을 사용자에게 보여준다:**

아래 형식의 마크다운 테이블을 일반 텍스트로 출력한다 (도구 호출이 아닌 직접 텍스트 출력).

```markdown
| 항목 | 파악 내용 |
|------|----------|
| 프로젝트 목표 | (분석 결과) |
| 주요 컴포넌트 | N개 식별: (목록) |
| 기술 스택 | (분석 결과) |
| 아키텍처 패턴 | (분석 결과) |
| 이슈/개선사항 | N개 발견 |
```

**② 테이블 출력 직후 AskUserQuestion으로 확인을 요청한다:**

- 질문: "분석 결과를 확인해 주세요. 스펙 작성을 진행할까요?"
- "확인" → Step 3 진행
- "수정/보완 필요" → 피드백 반영 후 테이블 재제시 (최대 2라운드)

**Decision Gate 2→3**:
```
has_goal = 프로젝트 목표 파악 완료
has_architecture = 아키텍처 구조 파악 완료
has_components = 주요 컴포넌트 식별 완료

IF has_goal AND has_architecture AND has_components → Step 3 진행
ELSE → 미파악 항목에 대해 추가 탐색 또는 AskUserQuestion
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
   - If required lines are missing, ask user via AskUserQuestion
   - If user approves, append only the missing lines (minimal edit, preserve existing structure).
   - If user declines, keep file unchanged and continue spec creation.

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

### Step 4: Quality Gate (LLM-as-Judge)

스펙 작성 완료 후, 아래 4개 기준으로 품질을 자가 검증한다.

| Criterion | Probe | PASS | WEAK | FAIL |
|-----------|-------|------|------|------|
| **저장소 이해** (Understand) | "이 저장소는 무엇을 하고, 누구를 위한 것이며, 무엇을 하지 않는가?" | Goal 섹션만 읽고 프로젝트 목적, 주요 사용자, 비목표를 구체적으로 답할 수 있다 | 답할 수 있지만 모호하거나 비목표가 누락 | Goal이 없거나 일반론만 있어 이 저장소만의 목적을 파악할 수 없다 |
| **기능 위치 탐색** (Locate) | "X 기능의 코드는 어디에 있는가?" | Component Details에서 실제 파일 경로와 핵심 심볼을 즉시 찾을 수 있다 | 컴포넌트는 기술되어 있으나 실제 경로나 심볼이 부족 | 기능이 어느 컴포넌트/파일에 속하는지 스펙에서 알 수 없다 |
| **안전한 수정 판단** (Change) | "Y를 변경하려면 어디를 수정하고 무엇을 주의해야 하는가?" | Change Recipes 또는 변경 진입점이 있고, 관련 불변 조건/계약이 명시 | 변경 시작점은 있으나 주의사항이 부족 | 변경 가이드가 전혀 없어 코드를 직접 탐색해야 한다 |
| **비자명한 결정 기억** (Remember) | "이 설계에서 왜 Z를 선택했는가?" | Design Decisions, Open Questions, 또는 DECISION_LOG에 실질적 내용이 있다 | 일부 결정/가정이 기록되어 있으나 핵심 불변 조건 누락 | 비자명한 결정이나 불변 조건이 전혀 기록되지 않았다 |

**검증 프로세스**:

| 결과 | 행동 |
|------|------|
| ALL PASS | 검증 통과, 완료 보고 진행 |
| WEAK만 존재 (FAIL 없음) | 개선 포인트를 사용자에게 알리되 진행 허용 |
| FAIL 1개 이상 | FAIL 항목과 근거를 기록 → Step 3로 돌아가 해당 부분만 보강 → 이 단계를 재실행 (최대 1회) |
| 재검증 후에도 FAIL | 사용자에게 보고하고 판단을 맡긴다 |

**검증 결과 출력 형식**:

| Criterion | Probe | 판정 | 근거 |
|-----------|-------|------|------|
| 저장소 이해 | "이 저장소는 무엇을 하는가?" | PASS | (구체적 근거) |
| 기능 위치 탐색 | "X 기능은 어디에?" | PASS | (구체적 근거) |
| 안전한 수정 판단 | "Y를 변경하려면?" | PASS | (구체적 근거) |
| 비자명한 결정 기억 | "왜 Z를 선택?" | PASS | (구체적 근거) |

**종합**: PASS / PASS WITH NOTES / FAIL → FIX

## Spec Management Operations

### Creating a New Spec

1. Create `_sdd/spec/` directory if not exists
2. If missing, create `<project_root>/AGENTS.md` with `_sdd/spec` / `_sdd/env.md` reference lines
3. If missing, create `<project_root>/CLAUDE.md` with `_sdd/spec` / `_sdd/env.md` reference lines
4. If missing, create `<project_root>/_sdd/env.md` with TODO comments for environment details
5. If existing `AGENTS.md` / `CLAUDE.md` / `_sdd/env.md` lack required guidance lines, ask user whether to add them; append only missing lines when approved
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
   f. `AGENTS.md`, `CLAUDE.md`, `_sdd/env.md`의 필수 안내 문구 존재 확인 (생성 또는 사용자 승인 기반 최소 추가)

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
- **Overview First**: 컴포넌트 섹션은 Overview(동작 개요 + 설계 의도)로 시작한다; Overview는 서술형(prose)이 권장되는 유일한 MUST 섹션이다 (2-3 문단 이내)
- **Understand-then-Change**: 독자가 먼저 동작을 이해(Overview)한 후 변경 방법(Change Recipes)을 찾을 수 있도록 구성한다
- **Favor tables with actual paths over long narrative** — **except** in Overview sections, where prose is encouraged

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
- **Bootstrap docs**: `<project_root>/AGENTS.md`, `<project_root>/CLAUDE.md`, `<project_root>/_sdd/env.md` (없으면 생성, 기존 파일은 사용자 승인 시 누락 문구만 최소 추가)
- **Decision log**: `_sdd/spec/DECISION_LOG.md` (when decisions/rationale need to be preserved)

## Progressive Disclosure (완료 시)

```
완료 요약 테이블을 제시한 후 전체 문서 요약을 바로 출력한다 (사용자 확인을 기다리지 않는다):

1. 완료 요약 테이블 제시:
   | 항목 | 내용 |
   |------|------|
   | 생성 파일 | `_sdd/spec/<project>.md` |
   | 부트스트랩 파일 | `AGENTS.md` / `CLAUDE.md` / `_sdd/env.md` (신규 생성 또는 사용자 승인 기반 최소 추가) |
   | 총 줄 수 | N줄 |
   | 주요 섹션 | Goal, Architecture, Components, ... |
   | Decision Log | 생성됨/미생성 |

2. 전체 문서의 섹션별 요약 출력
```

## Error Handling

| 상황 | 대응 |
|------|------|
| `_sdd/spec/` 디렉토리 미존재 | 자동 생성 (`mkdir -p _sdd/spec/`) |
| `AGENTS.md` / `CLAUDE.md` 미존재 | 표준 안내 문구로 새 파일 생성 |
| `_sdd/env.md` 미존재 | TODO 주석이 포함된 템플릿 파일 생성 |
| 기존 `AGENTS.md` / `CLAUDE.md` / `_sdd/env.md`에 필수 문구 누락 | AskUserQuestion으로 추가 여부 확인 후 승인 시 최소 추가 |
| 기존 스펙 파일 존재 | `prev/PREV_<filename>_<timestamp>.md`로 백업 후 새로 생성 |
| 프로젝트 코드 접근 불가 | 사용자에게 경로 확인 요청 |
| user_draft.md 형식 오류 | 파싱 오류 위치 보고, 자유 형식으로 해석 시도 |
| 불완전한 사용자 입력 | 가용 정보로 진행, 해결 불가 항목은 스펙에 Open Questions로 기록 |
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
