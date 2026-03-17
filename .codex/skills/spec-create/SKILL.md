---
name: spec-create
description: This skill should be used when the user asks to "create a spec", "write a spec document", "generate SDD", "create software design document", "document the project", "create spec for project", or mentions "_sdd" directory, specification documents, or project documentation needs.
version: 1.4.0
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

## Long-form Writing Strategy

장문 스펙 본문(여러 섹션, 상세 표, 긴 예시)이 필요한 경우 `$write-phased` 전략을 우선 적용한다.

- Phase 1: skeleton을 실제 파일에 저장
- Phase 2: section-by-section patch로 채우기
- runtime delegation이 불가능하면 현재 실행 안에서 동일한 skeleton -> fill 절차를 따른다

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

**Tools**: `Read`, `Glob`, `request_user_input`

Before creating a spec document, collect:

1. **From User Input**: Direct requirements and constraints
2. **From Existing Code**: Analyze codebase structure and patterns
3. **From Documentation**: Read existing README, comments, configs
4. **From Decision Log**: Read `_sdd/spec/DECISION_LOG.md` if it exists
5. **Clarification**: Use `request_user_input` for ambiguous requirements that block spec creation
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
| 50-200 파일 | 타겟 탐색 | `rg`/`Glob`으로 후보 식별 → 타겟 `Read` |
| > 200 파일 | 시맨틱 위주 | `rg`/`Glob` 위주 → 최소한의 `Read` |

**Decision Gate 1→2**:
```
input_sufficient = (사용자 입력 OR user_draft.md OR 기존 문서) 중 하나 이상 존재
project_readable = 프로젝트 코드/README 등 분석 가능한 소스 존재

IF input_sufficient AND project_readable → Step 2 진행
ELSE IF NOT input_sufficient → `request_user_input`: 프로젝트 설명 요청
ELSE IF NOT project_readable → `request_user_input`: 프로젝트 경로/접근 방법 확인
```

### Step 2: Analyze the Project

**Tools**: `rg`, `Glob`, `Read`

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

### Step 2.5: 분석 결과 확인 (Checkpoint)

**Tools**: — (보고 단계), `request_user_input` (only if critical ambiguity remains)

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

**② 테이블 출력 직후 진행 규칙을 적용한다:**

- 기본 동작은 보고 후 자동 진행이다.
- 아래 경우에만 `request_user_input`으로 최소 확인한다:
  - 프로젝트 목표/범위가 두 가지 이상으로 해석되어 스펙 방향이 크게 달라지는 경우
  - canonical output structure (`<project>.md` vs `main.md` vs split spec) 판단 근거가 약한 경우
  - 기존 문서/코드/사용자 입력 사이에 핵심 충돌이 있는 경우

**Decision Gate 2→3**:
```
has_goal = 프로젝트 목표 파악 완료
has_architecture = 아키텍처 구조 파악 완료
has_components = 주요 컴포넌트 식별 완료

IF has_goal AND has_architecture AND has_components → Step 3 진행
ELSE → 미파악 항목에 대해 추가 탐색 또는 Open Questions 기록
```

### Step 2.7: Generation Strategy Decision

**Tools**: `rg`, `Glob`

Step 2에서 파악한 코드베이스 규모에 따라 생성 전략을 결정한다.

```
source_files = 구현 파일 수 (`rg --files` 또는 `Glob`) 에서 테스트/설정 파일 제외
# test/, tests/, spec/, __test__, config/, node_modules/, .git, dist/, build/ 등 제외

IF source_files < 30 → 1-페이즈 (Step 3에서 단일 패스로 전체 작성)
IF source_files >= 30 → 2-페이즈 (Step 3에서 골조 생성 → 내용 채우기)
```

> **참고**: 생성 전략(1/2-페이즈)과 저장 전략(파일 분할)은 독립적 관심사이다. 2-페이즈로 생성해도 최종 저장은 기존 규모별 구조(소/중/대규모)를 따른다.

### Step 3: Bootstrap + Write the Spec Document

**Tools**: `Read`, `Edit`, `Write`, `Bash (mkdir -p)`, `multi_tool_use.parallel`

> **먼저 `references/template-full.md`를 Read로 읽는다.** 이 템플릿에 전체 섹션 구조(Background & Motivation, Core Design, Usage Guide & Expected Results 등)와 코드 발취/인라인 citation 형식이 정의되어 있다. 템플릿을 참조하여 스펙을 작성한다.

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
   - If required lines are missing, ask user via `request_user_input`
   - If user approves, append only the missing lines (minimal edit, preserve existing structure).
   - If user declines, keep file unchanged and continue spec creation.

#### Step 3-B: Write Spec

> **1-페이즈** (source_files < 30): 아래 템플릿으로 단일 패스 작성.
> **2-페이즈** (source_files >= 30): 아래 절차를 먼저 수행한 후, 최종 결과를 동일한 템플릿 구조로 저장.

##### 2-페이즈 실행 절차 (source_files >= 30일 때만)

> 1-페이즈인 경우 이 절차를 건너뛰고 아래 템플릿으로 직접 작성한다.

**Phase 1 — 골조(Skeleton) 생성**

§1~§8 각 섹션에 대해 미니 요약(3-5줄)을 작성한다. 골조는 Phase 2의 "계약서" 역할을 한다.

각 섹션의 골조 형식:
```markdown
## §N [Section Title]

**요약**: [핵심 내용 1-2줄]
[추가 맥락 1-2줄]

**코드 참조**: `[주요 파일/디렉토리]`
**다룰 내용**: [이 섹션에서 상세히 다룰 토픽 나열]

<!-- Phase 2에서 상세 작성 -->
```

- 골조 전체는 ~50-80줄로 가볍게 유지한다.
- 골조 작성 시 코드베이스 구조와 Step 2 분석 결과를 참조한다.
- 골조를 컨텍스트에만 보관하지 말고, 실제 target spec 파일에 먼저 저장한다.
- 단일 파일이면 canonical spec 파일에 skeleton을 저장하고, split spec이면 `main.md`/index와 필요한 sub-spec 파일에 placeholder skeleton을 먼저 생성한다.
- Phase 1 결과는 `<!-- Phase 2에서 상세 작성 -->` 주석이 남아 있는 초안 상태로 파일에 존재해야 한다.
- 골조 완료 후 Phase 2로 자동 진행한다 (사용자 리뷰 게이트 없음).

**Phase 2 — 내용 채우기(Fill)**

Phase 1에서 저장한 skeleton 파일들을 다시 읽고, 그 내용을 기준으로 각 섹션의 상세 내용을 작성한다.

실행 순서:
1. **순차 실행**: §1 Background & Motivation → §2 Core Design → §3 Architecture Overview
   - 이 섹션들은 상호 의존성이 있어 순서대로 작성한다.
   - 각 섹션 작성 시 저장된 skeleton + 이전 완성된 섹션 + 코드베이스를 참조한다.
2. **병렬 실행**: §4 Component Details, §5 Usage Guide, §6 Data Models, §7 API Reference, §8 Environment
   - 이 섹션들은 저장된 skeleton만 있으면 독립 작성이 가능하다.
   - `multi_tool_use.parallel`로 독립 섹션 초안 작성을 병렬 처리한다.
   - 각 병렬 작업에는 저장된 skeleton 전체 + 코드베이스 분석 결과 + 해당 섹션의 관련 파일 목록만 제공한다.
   - 병렬 결과를 취합해 최종 스펙으로 조립한다.

Phase 2 완료 후 저장된 spec 파일들에서 `<!-- Phase 2에서 상세 작성 -->` 주석을 모두 제거하고 최종 스펙을 조립한다.
최종 스펙의 구조와 형식은 아래 템플릿과 동일하다.

##### 스펙 템플릿

> **`references/template-compact.md`를 읽는다.** 이 템플릿에 §1-§8 섹션 구조, Writing Rules(코드 발췌/인라인 citation/What-Why-How 트라이어드), 그리고 Modular Spec Guide가 정의되어 있다. 이 템플릿을 참조하여 스펙을 작성한다.

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
10. **출력 검증** (실제 target path 기준):
   a. 생성된 canonical spec 파일 또는 index 파일 존재 확인 (`_sdd/spec/<project>.md` 또는 `_sdd/spec/main.md`)
   b. split spec인 경우 linked sub-spec 파일 존재 확인
   c. 필수 섹션 포함 확인: Background & Motivation, Core Design, Architecture, Component Details, Environment
   d. 500줄 초과 시 → 모듈 분할 제안
   e. `DECISION_LOG.md` 생성 여부 확인 (결정 사항이 있었을 경우)
   f. 링크/경로 유효성 확인
   g. `AGENTS.md`, `CLAUDE.md`, `_sdd/env.md`의 필수 안내 문구 존재 확인 (생성 또는 사용자 승인 기반 최소 추가)

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
- [API](./api.md) 또는 [API](./api/overview.md)
- [Database](./database.md) 또는 [Database](./database/overview.md)
```

## Best Practices

### Writing Quality

- **Be Specific**: Avoid vague descriptions
- **Use Examples**: Include code snippets and usage examples
- **Stay Current**: Update spec when code changes significantly
- **Code Excerpts**: When a codebase exists, include actual code excerpts in the Core Design section. Rule: functions ≤30 lines → full body excerpt; >30 lines → signature + core logic only. Mark each excerpt with `# [filepath:functionName]` comment header.
- **Inline Citations**: Reference code in prose using `[filepath:functionName]` format (e.g., `[src/auth/handler.py:validateToken]`). This maps to the academic `[Author, Year]` pattern for AI-parseable code tracing.
- **Link to Code**: Reference file paths and line numbers when helpful. When a codebase exists, use the **Source** field in component details to map each component to its implementation files. Under a `Source` heading or label, format it as a list:
  ```
  - `<relative/path/to/file>`: ClassName, function_name()
  - `<relative/path/to/other>`: AnotherClass
  ```
  - Wrap file paths in backticks.
  - Use project-root-relative paths.
  - Group classes/functions by file; separate items within the same file with commas.
  - Use one bullet per file for readability.
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
- If unclear and the choice would materially change the spec, use `request_user_input` to confirm preferred language

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
| 기존 `AGENTS.md` / `CLAUDE.md` / `_sdd/env.md`에 필수 문구 누락 | `request_user_input`으로 추가 여부 확인 후 승인 시 최소 추가 |
| 기존 스펙 파일 존재 | `prev/PREV_<filename>_<timestamp>.md`로 백업 후 새로 생성 |
| 프로젝트 코드 접근 불가 | 사용자에게 경로 확인 요청 |
| user_draft.md 형식 오류 | 파싱 오류 위치 보고, 자유 형식으로 해석 시도 |
| 불완전한 사용자 입력 | 가용 정보로 진행, 해결 불가 항목은 스펙에 Open Questions로 기록 |
| 대형 프로젝트 (200+ 파일) | `rg`/`Glob` 위주 탐색, 핵심 컴포넌트만 문서화 |
| 다국어 혼재 | 사용자에게 언어 선호도 확인 |
| DECISION_LOG.md 충돌 | 기존 항목 보존, 새 항목만 추가 |

## Additional Resources

### Reference Files
- **`references/template-compact.md`** - Canonical §1-§8 generation template with What/Why/How triad and Modular Spec Guide
- **`references/template-full.md`** - Complete template with all sections (detailed examples)

### Example Files
- **`examples/simple-project-spec.md`** - Minimal spec for small projects
- **`examples/complex-project-spec.md`** - Full spec for large projects
- **`examples/additional-specs.md`** - CLI, Web API, Data Pipeline spec examples

## Integration with Other Skills

This skill works well with:
- **feature-draft**: Draft feature spec patch + implementation plan (next step in simplified workflow)
- **implementation**: Implement features based on spec
- **spec-update-done**: Sync spec with actual code after implementation
