---
name: spec-create
description: This skill should be used when the user asks to "create a spec", "write a spec document", "generate SDD", "create software design document", "document the project", "create spec for project", or mentions "_sdd" directory, specification documents, or project documentation needs.
version: 1.4.0
---

# Spec Document Creation and Management

Create and manage Software Design Description (SDD) spec documents for projects. Spec documents provide comprehensive technical documentation including goals, architecture, components, and usage examples.
기존 스펙/문서의 언어를 따른다. 새 프로젝트는 한국어 기본.

## Acceptance Criteria
> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.
- [ ] AC1: 스펙 파일이 `_sdd/spec/` 아래에 생성되었다 (`<project>.md` 또는 `main.md`)
- [ ] AC2: Bootstrap 파일 처리 완료 — `AGENTS.md`, `CLAUDE.md`, `_sdd/env.md` 존재하며 필수 안내 문구 포함
- [ ] AC3: 필수 섹션 §1-§8 포함 (Background & Motivation, Core Design, Architecture, Component Details, Environment 등)
- [ ] AC4: 500줄 초과 시 모듈 분할(인덱스 + 컴포넌트 파일) 적용
- [ ] AC5: 기존 스펙 파일이 있었다면 `prev/PREV_<filename>_<timestamp>.md`로 백업됨
- [ ] AC6: 결정 사항이 있었다면 `DECISION_LOG.md` 생성/갱신됨

## Workflow Position

| Workflow | Position | When |
|----------|----------|------|
| All | Pre-step | 스펙이 없을 때 먼저 실행 |

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
    │   ├── main.md             # 전체 스펙 또는 인덱스
    │   ├── <component>.md      # 컴포넌트별 스펙
    │   ├── user_draft.md       # 사용자 요구사항 (있으면)
    │   └── DECISION_LOG.md     # 결정 로그 (선택, 권장)
    └── implementation/
        └── IMPLEMENTATION_PLAN.md
```

| 규모 | 구조 | 기준 |
|------|------|------|
| 소규모 | `main.md` 단일 파일 | ≤ 500줄 |
| 중규모 | `main.md` (인덱스) + `<component>.md` | 500–1500줄 |
| 대규모 | `main.md` (인덱스) + `<component>/` 서브디렉토리 | > 1500줄 |

## Spec Document Creation Process

### Step 1: Gather Information

**Tools**: `Read`, `Glob`, `AskUserQuestion`

수집 대상:
- 사용자 입력 / `_sdd/spec/user_draft.md`
- 기존 코드·README·설정 파일 분석
- `_sdd/spec/DECISION_LOG.md` (있으면)
- Bootstrap 대상 파일 존재 여부: `AGENTS.md`, `CLAUDE.md`, `_sdd/env.md`
- 불명확한 요구사항 → `AskUserQuestion`

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

#### Codebase Existence Check

`Glob`으로 구현 소스 파일(`*.py`, `*.ts`, `*.java` 등) 존재 여부를 판단한다.
- **있음** → 컴포넌트 테이블에 `Source` 필드 포함
- **없음** (greenfield) → `Source` 필드 생략

#### Exploration

- 프로젝트 구조·파일 조직
- 진입점·주요 컴포넌트
- 의존성·외부 연동
- 데이터 흐름·아키텍처 패턴
- 알려진 이슈·제약

### Step 2.5: 분석 결과 확인 (Checkpoint)

**Tools**: — (보고 단계), `AskUserQuestion` (critical ambiguity only)

**① 분석 결과 테이블을 텍스트로 출력한다:**

```markdown
| 항목 | 파악 내용 |
|------|----------|
| 프로젝트 목표 | (분석 결과) |
| 주요 컴포넌트 | N개 식별: (목록) |
| 기술 스택 | (분석 결과) |
| 아키텍처 패턴 | (분석 결과) |
| 이슈/개선사항 | N개 발견 |
```

**② 진행 규칙:**
- 기본: 보고 후 자동 진행
- `AskUserQuestion` 사용 조건: 목표/범위가 복수 해석 가능 / 출력 구조 판단 근거 부족 / 기존 문서·코드·입력 간 핵심 충돌

**Decision Gate 2→3**:
```
IF has_goal AND has_architecture AND has_components → Step 3 진행
ELSE → 미파악 항목 추가 탐색 또는 Open Questions 기록
```

### Step 3: Bootstrap + Write the Spec Document

**Tools**: `Read`, `Edit`, `Write`, `Bash (mkdir -p)`

#### Step 3-A: Create missing workspace guidance files

1. `_sdd/`, `_sdd/spec/` 디렉토리 확보
2. `AGENTS.md` 미존재 → 표준 안내 문구로 생성:
   ```markdown
   # Workspace Guidance
   - 프로젝트 스펙 문서는 `_sdd/spec/`를 기준으로 확인합니다.
   - 환경 관련 설정/실행 방법은 `_sdd/env.md`를 기준으로 확인합니다.
   ```
3. `CLAUDE.md` 미존재 → 동일 문구로 생성
4. `_sdd/env.md` 미존재 → TODO 주석 포함 템플릿 생성:
   ```markdown
   # Environment Setup Guide
   <!-- TODO: 프로젝트 실행/테스트에 필요한 환경 정보를 여기에 작성하세요. -->
   ## Runtime
   - <!-- 예: Python 3.11 -->
   ## Environment Variables
   - <!-- 예: OPENAI_API_KEY=... -->
   ## Setup Commands
   - <!-- 예: conda activate myenv -->
   ```
5. 기존 파일에 필수 문구 누락 시 → `AskUserQuestion`으로 확인 → 승인 시 최소 추가

#### Step 3-B: Write Spec

`write-phased` 서브에이전트에 위임한다. 호출 시 `references/template-compact.md`의 스펙 템플릿 전체와 Step 2 분석 결과를 프롬프트에 포함한다.

> **`references/template-compact.md`를 Read로 읽는다.** §1-§8 섹션 구조, Writing Rules(코드 발췌/인라인 citation/What-Why-How 트라이어드), Modular Spec Guide가 정의되어 있다.

##### 단일 파일 (소규모, ≤ 500줄)

```
Agent(
  subagent_type="write-phased",
  prompt="파일 경로: [_sdd/spec/<project>.md 또는 _sdd/spec/main.md]
  [references/template-compact.md §1-§8 + Step 2 분석 결과]"
)
```

##### 멀티파일 (중규모 500-1500줄 / 대규모 1500줄+)

**Step 3-B-1**: main.md (인덱스) 순차 작성
```
Agent(subagent_type="write-phased", prompt="main.md 인덱스 작성.
  목표/아키텍처 요약/컴포넌트 링크만.
  [references/template-compact.md + Step 2 분석 결과]")
```

**Step 3-B-2**: 컴포넌트 파일 병렬 작성 (main.md 완성 후)

각 Agent에 포함: 파일 경로, 컴포넌트 분석 결과, §4 템플릿, 언어/스타일, main.md 링크 구조

```
Agent("_sdd/spec/<comp_1>.md [컴포넌트 분석 + §4 템플릿]")  ─┐
Agent("_sdd/spec/<comp_2>.md [컴포넌트 분석 + §4 템플릿]")  ─┤ 동시
Agent("_sdd/spec/<comp_N>.md [컴포넌트 분석 + §4 템플릿]")  ─┘
```

> 독립 컴포넌트 2개 이상이면 병렬 디스패치.

### Step 4: 출력 검증

| 검증 항목 | 기준 |
|-----------|------|
| 스펙 파일 존재 | `_sdd/spec/<project>.md` 또는 `main.md` |
| Split spec 링크 | 분할 시 sub-spec 파일 모두 존재 |
| 필수 섹션 | §1-§8 포함 (Background & Motivation, Core Design, Architecture, Component Details, Environment 등) |
| 모듈 분할 | 500줄 초과 시 분할 적용 |
| Bootstrap 파일 | `AGENTS.md`, `CLAUDE.md`, `_sdd/env.md` 필수 문구 포함 |
| Decision Log | 결정 사항이 있었으면 `DECISION_LOG.md` 생성/갱신 |
| 링크/경로 유효성 | 내부 링크 정상 |

Decision log entry format:
```markdown
## YYYY-MM-DD - [Decision Title]
- Context:
- Decision:
- Rationale:
- Alternatives considered:
- Impact / follow-up:
```

## Progressive Disclosure (완료 시)

완료 요약 테이블을 제시한 후 전체 문서 요약을 바로 출력한다:

| 항목 | 내용 |
|------|------|
| 생성 파일 | `_sdd/spec/<project>.md` |
| 부트스트랩 파일 | `AGENTS.md` / `CLAUDE.md` / `_sdd/env.md` |
| 총 줄 수 | N줄 |
| 주요 섹션 | Goal, Architecture, Components, ... |
| Decision Log | 생성됨/미생성 |

## Error Handling

| 상황 | 대응 |
|------|------|
| `_sdd/spec/` 미존재 | 자동 생성 (`mkdir -p`) |
| `AGENTS.md` / `CLAUDE.md` 미존재 | 표준 안내 문구로 생성 |
| `_sdd/env.md` 미존재 | TODO 템플릿 생성 |
| 기존 Bootstrap 파일에 문구 누락 | `AskUserQuestion` 후 승인 시 최소 추가 |
| 기존 스펙 파일 존재 | `prev/PREV_<filename>_<timestamp>.md` 백업 후 생성 |
| 프로젝트 코드 접근 불가 | 경로 확인 요청 |
| user_draft.md 형식 오류 | 오류 위치 보고, 자유 형식으로 해석 시도 |
| 불완전한 사용자 입력 | 가용 정보로 진행, Open Questions 기록 |
| 대형 프로젝트 (200+ 파일) | `Grep`/`Glob` 위주, 핵심 컴포넌트만 문서화 |
| DECISION_LOG.md 충돌 | 기존 항목 보존, 새 항목만 추가 |

## Additional Resources

- **`references/template-compact.md`** — §1-§8 generation template (What/Why/How triad + Modular Spec Guide)
- **`references/template-full.md`** — Complete template with detailed examples
- **`examples/simple-project-spec.md`** — 소규모 스펙 예시
- **`examples/complex-project-spec.md`** — 대규모 스펙 예시
- **`examples/additional-specs.md`** — CLI, Web API, Data Pipeline 예시

연관 skill: `feature-draft` → `implementation` → `spec-update-done`
