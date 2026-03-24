---
name: implementation-plan
description: "This skill should be used when the user asks to \"create an implementation plan\", \"plan the implementation\", \"break down this spec\", \"create a development roadmap\", \"analyze requirements and create tasks\", \"create a parallel implementation plan\", \"plan parallel implementation\", \"병렬 구현 계획\", \"create parallel development roadmap\", or wants a structured implementation plan with Target Files for parallel execution support."
version: 2.0.0
---

# Implementation Plan Creation (Parallel-Ready)

| Workflow | Position | When |
|----------|----------|------|
| Large | Step 3 of 6 | Phase별 구현 계획 수립 (standalone) |
| Medium | — | feature-draft가 통합 처리 |
| Small | — | 직접 구현 |

> `feature-draft`가 스펙 패치 + 구현 계획을 통합 생성하므로, 이 스킬은 계획을 별도 단계로 실행할 때 사용한다.

스펙 문서를 분석하여, **Target Files**가 포함된 단계별 구현 계획을 생성한다.

## Acceptance Criteria

> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] 스펙 분석 → 컴포넌트 식별 → 태스크 정의 (모든 Task에 AC + Target Files 필수)
- [ ] Phase 분해 (MVP-First / Risk-First / Dependency-Driven 자동 선택, 근거 기록)
- [ ] `IMPLEMENTATION_PLAN.md` (≤25 tasks) 또는 phase-split 파일 (>25 tasks) 생성

## Hard Rules

- **Spec Read-Only**: `_sdd/spec/` 하위 파일은 읽기만 가능. 변경 필요 시 Open Questions에 기록하고 `spec-update-todo`로 유도.
- **모든 Task에 AC + Target Files 필수**: 하나라도 누락 시 다음 Step으로 진행 불가.
- **자율 결정**: 모호한 요구사항은 최선 추론 후 진행, 판단 근거를 Plan에 기록. 사용자 확인을 기다리지 않는다.

## Language

기존 스펙/문서의 언어를 따른다. 새 프로젝트(기존 스펙 없음)는 한국어 기본. 사용자 명시 지정 시 해당 언어 사용.

## Input Sources (우선순위 순)

1. **스펙의 📋 항목**: `_sdd/spec/` 내 📋 (계획됨) 상태 마커가 붙은 기능/태스크
2. **Feature Draft Part 2**: `_sdd/drafts/feature_draft_*.md`의 Implementation Plan 섹션
3. **사용자 입력**: 대화 또는 `_sdd/implementation/user_input.md`
4. 위 모두 불명확하면 사용자에게 확인을 요청한다.

`user_input.md` 처리 후 `_processed_user_input.md`로 rename.

## Process

### Step 1: Specification Analysis

**Tools**: `Read`, `Glob`

스펙 문서를 읽고 분석한다:

- **Core Requirements**: 시스템이 해야 할 것
- **Technical Constraints**: 언어, 프레임워크, 통합, 성능 요구
- **Scope Boundaries**: 명시적 범위 내/외
- **Success Criteria**: 완료 측정 기준
- **Unknowns/Risks**: 확인/연구 필요 항목

불명확한 스펙은 가용 정보에서 최선 추론하고, 모호 항목은 Open Questions에 기록한다.

### Step 2: Component Identification

**Tools**: `Glob`, `Grep`, `Read`

시스템을 논리적 컴포넌트로 분해:

- 관련 기능을 모듈로 그룹핑
- 공유 유틸리티 및 공통 패턴 식별
- 외부 의존성/통합 파악
- 데이터 모델 및 저장소 요구사항 파악

### Step 3: Task Definition with Target Files

**Tools**: `Glob`, `Grep`, `Read`

각 컴포넌트에 대해 아래 구조의 Task를 생성한다:

```
### Task [ID]: [액션 중심 제목]
**Component**: [컴포넌트]
**Priority**: [P0-Critical | P1-High | P2-Medium | P3-Low]
**Type**: [Feature | Bug | Refactor | Research | Infrastructure | Test]

**Description**: [상세 설명]

**Acceptance Criteria**:
- [ ] [구체적, 측정 가능한 기준]

**Target Files**:
- [C] `path/to/new_file.py` -- 설명
- [M] `path/to/existing_file.py` -- 변경 내용
- [C] `tests/test_file.py` -- 테스트

**Technical Notes**: [구현 힌트]
**Dependencies**: [blocking task IDs]
```

### Target Files 규격

- 모든 태스크에 `**Target Files**:` 필드 필수
- 마커: `[C]` 생성, `[M]` 수정, `[D]` 삭제
- 형식: `- [마커] \`relative/path/to/file.ext\` -- 설명`
- 충돌 규칙: 동일 파일을 둘 이상의 태스크가 참조하면 마커 종류와 무관하게 충돌 (순차 실행)
- 읽기 전용 참조는 Target Files에 포함하지 않음

### Target Files 검증 (Glob 기반)

a. 모든 Task에 Target Files 필드 존재 확인
b. `[M]` 파일: `Glob`으로 존재 확인 → 미존재 시 `[C]`로 변경 또는 경로 수정
c. `[C]` 파일: `Glob`으로 미존재 확인 → 이미 존재하면 `[M]`으로 변경
d. `[C]` 파일의 상위 디렉토리 존재 확인
e. 전체 Target Files 수집 → 중복 파일 감지 → Parallel Execution Summary에 반영
f. 중복 파일이 있는 Task는 순차 실행으로 표시

Task가 너무 크면 하위 Task로 분할한다. 인프라/테스트/문서 Task도 누락하지 않는다.

### Test Coverage Mapping (조건부)

> `[M]` 마커 대상 파일이 1개 이상일 때만 실행. `[C]` 전용 계획이면 스킵.

`Grep`으로 `[M]` 대상 파일명을 테스트 디렉토리에서 검색하여, 관련 테스트 파일/함수 목록을 해당 Task의 Technical Notes에 기록한다. 테스트 디렉토리 미존재 시 스킵.

### Step 4: Phase Decomposition

**Tools**: — (자율 판단)

정의된 Task들을 분석하여 Phase로 그룹핑한다.

#### Phase 전략 선택 테이블

| 전략 | 자동 추천 조건 | Phase 구조 |
|------|---------------|-----------|
| **MVP-First** | 사용자 대면 기능 존재, 점진적 배포 필요 | Phase 0: 기반 설정 → Phase 1: MVP → Phase 2+: 확장/개선 |
| **Risk-First** | 고위험/불확실 기술 항목 ≥ 30% | Phase 1: 고위험 (가정 검증) → Phase 2: 핵심 → Phase 3: 저위험 확장 |
| **Dependency-Driven** | 의존성 체인 깊이 ≥ 3, 계층 명확 | Phase 1: 기반 (의존 없음) → Phase 2: 핵심 서비스 → Phase 3: 통합 → Phase 4: 마무리 |

**전략 선택 절차**:
1. Task 특성 분석: 의존성 깊이, 위험도 분포, 우선순위 분포, 기반 작업 유무
2. 테이블 기준으로 최적 전략 자동 선택
3. 선택 근거를 Plan에 기록 (사용자 확인을 기다리지 않음)

**Phase 그룹핑 원칙**:
- 각 Phase에 명확한 목표/테마 부여
- Phase 내 Task는 가능한 한 독립적으로 실행 가능
- Phase 간 의존성 최소화 (Phase N은 Phase N-1 완료 후 시작)

Phase 구성 요약 테이블을 Plan에 기록한 후 바로 Step 5로 진행한다.

### Step 5: Dependency Mapping

**Tools**: `Glob` (Target Files 중복 확인)

Task 관계를 매핑한다:

- **Blocks**: 선행 완료 필수
- **Related**: 컨텍스트 공유, 비차단
- **Parallel**: 동시 실행 가능 (Target Files 비중복)

병렬 대상 Task의 Target Files 중복 여부를 검증한다. 순환 의존성 발견 시 Task 분할로 해소.

### Step 6: Plan Output

**Tools**: `Write`, `Bash (mkdir -p)`

#### 파일 작성 위임

`sdd-skills:write-skeleton` 서브에이전트에 위임한다. 반환값이 SKELETON_ONLY이면 Sections Remaining 목록을 보고 Edit으로 채운다.
- 독립 섹션 2개+ → 병렬 Agent dispatch 가능
- 의존 섹션 → 순서대로 Edit
- 완료 후 TODO/Phase 마커 제거

호출 시 Output Format + 수집 정보를 프롬프트에 포함.

**단일 문서 (total_tasks ≤ 25)**:
```
Agent(subagent_type="sdd-skills:write-skeleton", prompt="IMPLEMENTATION_PLAN.md 작성. [Output Format + 수집 정보]")
```

**Phase별 분할 (total_tasks > 25)**:

Step 6-1: 인덱스 파일 순차 작성
```
Agent(subagent_type="sdd-skills:write-skeleton", prompt="IMPLEMENTATION_PLAN.md 인덱스 작성. Overview/Scope/Components/Phase 요약 + Phase 파일 링크")
```

Step 6-2: Phase 파일 병렬 작성 (인덱스 완성 후)
```
Agent("IMPLEMENTATION_PLAN_PHASE_1.md [Phase 1]")  ─┐
Agent("IMPLEMENTATION_PLAN_PHASE_2.md [Phase 2]")  ─┤ 동시
Agent("IMPLEMENTATION_PLAN_PHASE_N.md [Phase N]")  ─┘
```

> 독립 Phase 파일 2개 이상이면 병렬 디스패치.

## Output Format

```markdown
# Implementation Plan: [Project Name]

## Overview
[Brief summary]

## Scope
### In Scope
- [Feature/capability]
### Out of Scope
- [Explicitly excluded]

## Components
1. **[Component Name]**: [Brief description]

## Implementation Phases

### Phase 1: [Foundation/Setup]
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 1  | ...  | P0       | -            | Core      |

### Phase 2: [Core Features]
...

## Task Details
[Expanded task definitions with AC AND Target Files]

## Parallel Execution Summary
| Phase | Total Tasks | Max Parallel | File Conflicts |
|-------|-------------|--------------|----------------|
| 1     | N           | N            | None           |

## Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|

## Open Questions
- [ ] [Question]

## Model Recommendation
[Model recommendation based on complexity — refer "Model aliases" at https://code.claude.com/docs/en/model-config]
```

## Output Location

1. 기존 파일이 있으면 `_sdd/implementation/prev/PREV_IMPLEMENTATION_PLAN_<timestamp>.md`로 아카이브.
2. 기본 저장 경로: `<project_root>/_sdd/implementation/`
3. 사용자 지정 경로가 있으면 해당 경로 사용.

## Error Handling

| 상황 | 대응 |
|------|------|
| 스펙 파일 미발견 | `spec-create` 먼저 실행 권장 |
| 스펙 내용 모호 | 최선 추론, 모호 항목은 Open Questions에 기록 |
| Target Files 경로 확인 불가 | `[TBD] <reason>` 마커 사용 |
| 순환 의존성 발견 | Task 분할로 해소 |
| 기존 Plan 파일 존재 | `prev/`로 아카이브 |
| 모호한 우선순위 | 의존성 분석 기반 자동 배정 |
| user_input.md 형식 오류 | 자유 형식으로 해석 시도 |

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

---

> **Mirror Notice**: 이 스킬의 본문은 `.claude/agents/implementation-plan.md`의 복사본이다.
> 사용자가 직접 호출할 때 중간 과정의 가시성을 확보하기 위해 복붙되었다.
> 내용을 수정할 때는 agent 파일과 이 스킬 파일을 **반드시 함께** 수정해야 한다.
