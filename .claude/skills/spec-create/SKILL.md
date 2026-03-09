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
5. **부트스트랩 파일 최소 수정 원칙**: `AGENTS.md`, `CLAUDE.md`, `_sdd/env.md`가 이미 존재할 때 필수 안내 문구가 누락된 경우, `AskUserQuestion`으로 사용자 승인 후 필요한 문구만 최소 추가한다.
6. **DECISION_LOG.md 최소화**: 결정 로그는 `DECISION_LOG.md`에만 기록하며, 추가 거버넌스 문서는 사용자 요청 시에만 생성한다.
7. **호환 가능한 앵커 섹션 유지**: 기본적으로 `Goal`, `Architecture Overview`, `Component Details`, `Environment & Dependencies`, `Identified Issues & Improvements`, `Usage Examples`, `Open Questions` 섹션명을 유지한다. 내부 구조는 탐색형으로 재구성한다.
8. **실제 경로 우선**: 주요 컴포넌트와 변경 지점에는 가능하면 실제 파일/디렉토리 경로를 적는다.
9. **추정은 명시**: 확인되지 않은 내용은 단정하지 말고 `Open Questions`에 기록한다.
10. **요약 우선**: 코드 구조를 그대로 복사하지 말고 `의도`, `경계`, `계약`, `변경 지점`, `불변 조건`을 압축해서 정리한다.

## Directory Structure

기본 구조는 플랫 분할이다. Subdirectory는 플랫 분할로 관리가 어려워질 때만 도입한다.

### 기본 (플랫) 구조

```
<project-root>/
├── AGENTS.md
├── CLAUDE.md
└── _sdd/
    ├── env.md
    ├── spec/
    │   ├── main.md
    │   ├── <component>.md
    │   ├── user_draft.md
    │   └── DECISION_LOG.md
    └── implementation/
        └── IMPLEMENTATION_PLAN.md
```

### Subdirectory 구조 (조건 충족 시)

아래 조건 중 **2개 이상** 해당하면 subdirectory 분할을 고려한다:

| 조건 | 설명 |
|------|------|
| **컴포넌트 내부 분할** | 한 컴포넌트가 2개 이상의 스펙 파일을 필요로 한다 (예: auth → `auth.md`, `oauth-providers.md`, `session.md`) |
| **파일 수 과다** | `_sdd/spec/` 아래 컴포넌트 스펙 파일이 10개를 넘어 탐색이 어렵다 |
| **도메인 경계 존재** | 컴포넌트들이 명확한 도메인 그룹을 형성한다 (예: payments 도메인 아래 결제, 구독, 정산이 각각 독립 계약을 가짐) |
| **독립 변경 단위** | subdirectory 내 파일들이 함께 변경되는 경향이 있고, 다른 subdirectory와는 독립적으로 변경된다 |

```
<project-root>/
└── _sdd/
    └── spec/
        ├── main.md                      # 항상 최상위 entry point
        ├── DECISION_LOG.md              # 항상 최상위
        ├── auth/
        │   ├── auth.md                  # 도메인 entry point
        │   ├── oauth-providers.md
        │   └── session-management.md
        ├── billing/
        │   ├── billing.md
        │   ├── subscription.md
        │   └── payment-gateway.md
        └── jobs/
            └── jobs.md
```

Subdirectory 규칙:
- `main.md`와 `DECISION_LOG.md`는 항상 `_sdd/spec/` 루트에 둔다
- 각 subdirectory에는 디렉토리명과 동일한 entry point 파일을 둔다 (`auth/auth.md`)
- `main.md`의 Component Index에서 subdirectory entry point로 링크한다
- 단일 파일로 충분한 컴포넌트는 subdirectory 없이 루트에 둬도 된다
- 2단계 이상 중첩하지 않는다 (`auth/oauth/google.md` 같은 구조 금지)
- 파일이 1개뿐인 subdirectory는 만들지 않는다 — 루트에 둔다

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

**Tools**: `Read`, `Glob`, `Grep`, `AskUserQuestion`

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
| < 50 파일 | 자유 탐색 | `Grep` + `Read` 중심 탐색 |
| 50-200 파일 | 타겟 탐색 | 파일 후보 식별 후 필요한 파일만 읽기 |
| > 200 파일 | 시맨틱 탐색 | `Grep`, 디렉토리 맵, 엔트리포인트, 핵심 경로 위주로 요약 |

**Decision Gate 1->2**:
```
input_sufficient = (사용자 입력 OR user_draft.md OR 기존 문서) 중 하나 이상 존재
project_readable = 프로젝트 코드/README/설정 등 분석 가능한 소스 존재

IF input_sufficient AND project_readable -> Step 2
ELSE IF NOT input_sufficient -> AskUserQuestion: 프로젝트 설명 요청
ELSE IF NOT project_readable -> AskUserQuestion: 프로젝트 경로/접근 방법 확인
```

### Step 2: Analyze the Project

**Tools**: `Grep`, `Glob`, `Read`

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
- `Grep` for keyword and pattern discovery
- targeted file reads instead of full-repo dumping
- explicit path references over generic prose

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
- "수정/보완 필요" → 피드백 반영 후 테이블 재제시

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
   - if missing, use `AskUserQuestion` to ask user for approval
   - if approved, append only missing lines
   - if declined, keep file unchanged and continue spec creation

#### Step 3-B: Write Order

1. **Write the main spec first** using `references/template-full.md`.
2. **Keep anchor section headings** and structure them as an index:
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

### Step 4.5: Quality Gate (LLM-as-Judge)

구조 검증(Step 4) 통과 후, 스펙이 본래 목적을 달성하는지 자체 평가한다.
이 단계는 **판정만** 수행한다. FAIL 시 보강은 이전 작성 단계(Step 3)로 돌아가 수행한다.

#### 검증 기준 (4 Criteria)

**Criterion 1 — 저장소 이해 (Understand)**
> Probe: "이 저장소는 무엇을 하고, 누구를 위한 것이며, 무엇을 하지 않는가?"

| 판정 | 기준 |
|------|------|
| **PASS** | Goal 섹션만 읽고 프로젝트 목적, 주요 사용자, 비목표를 구체적으로 답할 수 있다 |
| **WEAK** | 답할 수 있지만 모호하거나 비목표가 누락되어 있다 |
| **FAIL** | Goal이 없거나 일반론만 있어 이 저장소만의 목적을 파악할 수 없다 |

**Criterion 2 — 기능 위치 탐색 (Locate)**
> Probe: "X 기능의 코드는 어디에 있는가?" (X = 스펙에 기술된 주요 기능 중 하나)

| 판정 | 기준 |
|------|------|
| **PASS** | Component Details/Component Index에서 실제 파일 경로와 핵심 심볼을 즉시 찾을 수 있다 |
| **WEAK** | 컴포넌트는 기술되어 있으나 실제 경로나 심볼이 부족하다 |
| **FAIL** | 기능이 어느 컴포넌트/파일에 속하는지 스펙에서 알 수 없다 |

**Criterion 3 — 안전한 수정 판단 (Change)**
> Probe: "Y를 변경하려면 어디를 수정하고 무엇을 주의해야 하는가?" (Y = 대표적 변경 시나리오)

| 판정 | 기준 |
|------|------|
| **PASS** | Change Recipes, 변경 핫스팟, 또는 변경 진입점이 있고, 관련 불변 조건/계약이 명시되어 있다 |
| **WEAK** | 변경 시작점은 있으나 주의사항(불변 조건, 영향 범위)이 부족하다 |
| **FAIL** | 변경 가이드가 전혀 없어 코드를 직접 탐색해야 한다 |

**Criterion 4 — 비자명한 결정 기억 (Remember)**
> Probe: "이 설계에서 왜 Z를 선택했는가?" 또는 "깨지면 안 되는 가정은 무엇인가?"

| 판정 | 기준 |
|------|------|
| **PASS** | Cross-Cutting Invariants, Open Questions, 또는 DECISION_LOG에 실질적 내용이 있다 |
| **WEAK** | 일부 결정/가정이 기록되어 있으나 핵심 불변 조건이 누락되어 있다 |
| **FAIL** | 비자명한 결정이나 불변 조건이 전혀 기록되지 않았다 |

#### 검증 프로세스

1. 생성된 스펙 전체를 다시 읽는다
2. 각 criterion에 대해 probe 질문을 시도한다
   - Criterion 1: Goal 섹션에서 프로젝트 목적, 사용자, 비목표를 찾는다
   - Criterion 2: 주요 기능 1개를 골라 해당 경로/심볼을 찾는다
   - Criterion 3: 대표적 변경 시나리오 1개를 설정하고 변경 가이드를 찾는다
   - Criterion 4: 불변 조건, 설계 결정, Open Questions를 찾는다
3. 각 criterion을 PASS / WEAK / FAIL로 판정한다
4. 결과에 따라 행동한다:

| 결과 | 행동 |
|------|------|
| ALL PASS | 검증 통과, 다음 단계 진행 |
| WEAK만 존재 (FAIL 없음) | 개선 포인트를 사용자에게 알리되 진행 허용 |
| FAIL 1개 이상 | FAIL 항목과 근거를 기록 → Step 3로 돌아가 해당 부분만 보강 → 이 단계를 재실행 (최대 1회) |
| 재검증 후에도 FAIL | 사용자에게 보고하고 판단을 맡긴다 |

#### 판정 결과 출력

스펙 작업 완료 시 아래 테이블을 텍스트로 출력한다:

| Criterion | Probe | 판정 | 근거 |
|-----------|-------|------|------|
| 저장소 이해 | "이 저장소는 무엇을 하는가?" | PASS | (구체적 근거) |
| 기능 위치 탐색 | "X 기능은 어디에?" | PASS | (구체적 근거) |
| 안전한 수정 판단 | "Y를 변경하려면?" | PASS | (구체적 근거) |
| 비자명한 결정 기억 | "왜 Z를 선택?" | PASS | (구체적 근거) |

**종합**: PASS / PASS WITH NOTES / FAIL → FIX

## Split Guidance

### 플랫 분할 (기본값)

플랫 분할(`main.md + auth.md + billing.md`)이 기본값이다. 아래 조건 중 하나 이상이면 분할한다:
- 메인 스펙이 약 350줄을 넘으며 밀도가 높다
- 저장소에 주요 컴포넌트가 7개를 넘는다
- 한 컴포넌트가 독립적인 계약이나 변경 가이드를 필요로 한다
- 한 섹션이 미니 매뉴얼 수준으로 길어진다

```
_sdd/spec/
├── main.md
├── auth.md
├── billing.md
├── jobs.md
└── DECISION_LOG.md
```

`main.md`는 항상 entry point이며 컴포넌트 파일로 링크한다.

### Subdirectory 분할 (조건부)

Subdirectory는 플랫 분할로 관리가 어려워질 때만 도입한다. 아래 조건 중 **2개 이상** 해당하면 고려한다:

| 조건 | 설명 |
|------|------|
| **컴포넌트 내부 분할** | 한 컴포넌트가 2개 이상의 스펙 파일을 필요로 한다 |
| **파일 수 과다** | `_sdd/spec/` 아래 컴포넌트 스펙 파일이 10개를 넘는다 |
| **도메인 경계 존재** | 컴포넌트들이 명확한 도메인 그룹을 형성한다 |
| **독립 변경 단위** | subdirectory 내 파일들이 함께 변경되고, 다른 subdirectory와는 독립적이다 |

```
_sdd/spec/
├── main.md
├── DECISION_LOG.md
├── auth/
│   ├── auth.md
│   ├── oauth-providers.md
│   └── session-management.md
└── billing/
    ├── billing.md
    └── subscription.md
```

Subdirectory 규칙:
- `main.md`와 `DECISION_LOG.md`는 항상 루트에 둔다
- 각 subdirectory에는 디렉토리명과 동일한 entry point를 둔다
- `main.md`의 Component Index에서 subdirectory entry point로 링크한다
- 2단계 이상 중첩 금지 (`auth/oauth/google.md` 불가)
- 파일이 1개뿐인 subdirectory는 만들지 않는다 — 루트에 둔다
- subdirectory 분할만을 위해 기존 플랫 구조를 강제 마이그레이션하지 않는다

## Best Practices

### Writing Quality

- **Fast first read**: make the first 30 lines answer "what is this repo?"
- **Change-oriented detail**: prioritize "where to edit" over exhaustive explanation
- **Path-first references**: include concrete directories, files, commands, and symbols
- **Trace unknowns**: uncertainty belongs in `Open Questions`, not hidden in confident prose

### LLM Token Efficiency

- **구조화된 포맷 선호**: 산문 나열보다 테이블과 리스트를 사용한다. LLM은 구조화된 포맷을 더 정확하게 파싱한다.
- **경로/심볼은 코드블록**: 경로와 심볼은 `` ` ``로 감싸서 일반 텍스트와 구분한다.
- **메인 스펙 분량 제한**: 메인 스펙은 LLM이 한 번에 읽고 전체 그림을 잡을 수 있는 분량이어야 한다. 상세는 컴포넌트 스펙으로 분리한다.
- **중복 기술 금지**: 같은 정보를 여러 섹션에 반복하지 않는다. 참조 링크를 사용한다.

### Anti-Pattern Reference

| 안티패턴 | 왜 문제인가 | 대안 |
|---------|------------|------|
| 코드를 그대로 복사한 문서 | 코드가 바뀌면 즉시 불일치 | 계약과 의도만 남기고 구현은 코드에 맡긴다 |
| 실제 경로/심볼이 없는 문서 | 검색 시작점이 없음 | Owned Paths, Key Symbols 명시 |
| 변경 포인트가 없는 문서 | "어디를 고치지?"에 답 불가 | Change Recipes 섹션 추가 |
| 불확실한 내용을 사실처럼 작성 | 잘못된 정보 신뢰 위험 | Open Questions로 분리 |
| 모든 프로젝트에 보안/성능 무조건 포함 | 관련 없는 정보가 핵심을 가림 | 해당하는 항목만 포함 |
| 메인 문서에 모든 것을 몰아넣음 | LLM 컨텍스트 초과, 사람도 길 잃음 | main + component spec 분할 |

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
| 기존 가이드 파일에 필수 문구 누락 | `AskUserQuestion`으로 추가 여부 확인 후 승인 시 최소 추가 |
| 기존 스펙 파일 존재 | `prev/PREV_<filename>_<timestamp>.md`로 백업 후 생성 |
| 프로젝트 코드 접근 불가 | `AskUserQuestion`으로 프로젝트 경로/접근 방법 확인 |
| 대형 프로젝트 | 핵심 경로와 컴포넌트 위주로 요약, 필요 시 분할 |
| 신뢰도 낮은 추정 | `Open Questions`에 분리 기록 |
| DECISION_LOG.md 충돌 | 기존 항목 보존, 새 항목만 추가 |

## Additional Resources

### Reference Files
- `references/template-full.md` - index-first main spec and component spec templates
- `references/optional-sections.md` - optional appendices for APIs, data models, security, performance, deployment
- `references/examples.md` - guidance on choosing and reading the examples, plus section-level good/bad quality comparisons

### Example Files
- `examples/simple-project-spec.md` - small project example with one main spec
- `examples/complex-project-spec.md` - large project example with index-first structure

## Integration with Other Skills

This skill works well with:
- **feature-draft**: uses `Goal > Key Features` and `Component Details` as patch targets
- **implementation**: implements against the spec
- **spec-update-done**: updates the spec after completed implementation
- **spec-summary**: summarizes the stable top-level sections created here
