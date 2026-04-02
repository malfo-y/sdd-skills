---
name: implementation-plan
description: This skill should be used when the user asks to "create an implementation plan", "plan the implementation", "break down this spec", "create a development roadmap", "analyze requirements and create tasks", "create a parallel implementation plan", "plan parallel implementation", "병렬 구현 계획", "create parallel development roadmap", or wants a structured implementation plan with Target Files for parallel execution support.
version: 2.1.0
---

# Implementation Plan Creation

| Workflow | Position | When |
|----------|----------|------|
| Large | Step 2 of 6 | feature draft 이후 상세 구현 계획 |
| Medium | Step 2 of 3 | 구현 로드맵 필요 |
| Small | Optional | 구현 전 리스크/순서 정리 |

이 agent는 `_sdd/implementation/implementation_plan.md`를 생성한다. 목표는 실행 가능한 plan을 만들되, `implementation`이 바로 읽을 수 있도록 task / dependency / target files를 명시하는 것이다.

## Acceptance Criteria

> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] `_sdd/implementation/implementation_plan.md`가 생성된다.
- [ ] 모든 task에 `**Target Files**`가 포함된다.
- [ ] phase, dependency, risk, open question이 빠지지 않는다.
- [ ] `_sdd/spec/`는 읽기만 하고 직접 수정하지 않는다.

## Hard Rules

1. 이 agent는 스펙을 입력으로 읽을 수 있지만 `_sdd/spec/` 파일은 수정하지 않는다.
2. 구현에 필요한 정보가 부족해도 멈추지 않고 deterministic defaults로 진행한다.
3. 모든 task는 action-oriented title, acceptance criteria, target files, dependencies를 가져야 한다.
4. 언어는 기존 스펙/문서의 언어를 따른다. 스펙이 없으면 한국어를 기본으로 사용한다.
5. spec 변경이 필요해 보이면 plan의 `Open Questions`에 기록하고 `spec-update-todo` 후속 사용을 제안한다.
6. 결과 파일은 lowercase canonical 경로에 저장한다. transition 기간에는 legacy uppercase artifact를 입력 fallback으로 허용한다.

## Input Sources

우선순위:
1. 사용자 요청
2. `_sdd/implementation/user_input.md` (있다면)
3. `_sdd/drafts/feature_draft_<name>.md`
4. `_sdd/spec/*.md`
5. 코드베이스 구조 및 현재 파일 패턴

`user_input.md`를 사용했다면 처리 후 `_processed_user_input.md`로 이름을 바꾼다.

## Target Files Rules

```markdown
**Target Files**:
- [C] `path/to/new_file.ts`
- [M] `path/to/existing.ts`
- [D] `path/to/old.ts`
- [TBD] 경로 미정 -- 사유
```

- `[C]` Create, `[M]` Modify, `[D]` Delete
- 읽기 전용 참조 파일은 포함하지 않는다.
- 동일 파일이 여러 task에 반복되면 병렬 충돌 가능성을 고려해 phase/dependency를 조정한다.

## Process

### Step 1: Analyze Inputs

다음 정보를 정리한다.
- 구현 대상 기능/범위
- 필수 제약과 acceptance criteria
- 관련 컴포넌트/모듈
- 환경/테스트/배포 영향

### Step 2: Read Spec and Code Context

필요 시 아래를 읽는다.
- `_sdd/spec/*.md`
- `_sdd/spec/decision_log.md`
- 관련 코드/테스트/설정 파일

목적:
- 현재 설계와 컴포넌트 경계 파악
- naming convention과 파일 구조 파악
- task별 Target Files 후보 도출

### Step 3: Identify Components

요구사항을 구현 컴포넌트로 나눈다.
- core module
- shared utilities
- integration points
- tests
- configuration / migration / docs

### Step 4: Define Tasks

task는 실행 가능한 단위여야 한다.

각 task 필수 필드:
- Component
- Priority
- Type
- Description
- Acceptance Criteria
- Target Files
- Technical Notes
- Dependencies

task를 나눌 때 원칙:
- 하나의 task는 하나의 명확한 목적을 가진다.
- file overlap이 적도록 자른다.
- setup/common groundwork는 별도 task로 분리한다.

### Test Coverage Mapping (조건부)

> `[M]` 마커 대상 파일이 1개 이상일 때만 실행. `[C]` 전용 계획이면 스킵.

`Grep`으로 `[M]` 대상 파일명을 테스트 디렉토리에서 검색하여, 관련 테스트 파일/함수 목록을 해당 Task의 Technical Notes에 기록한다. 테스트 디렉토리 미존재 시 스킵.

### Step 5: Build Phases

Phase 전략 선택:

| 전략 | 자동 추천 조건 | Phase 구조 |
|------|---------------|-----------|
| **MVP-First** | 사용자 대면 기능 존재, 점진적 배포 필요 | Phase 0: 기반 설정 → Phase 1: MVP → Phase 2+: 확장/개선 |
| **Risk-First** | 고위험/불확실 기술 항목 ≥ 30% | Phase 1: 고위험 (가정 검증) → Phase 2: 핵심 → Phase 3: 저위험 확장 |
| **Dependency-Driven** | 의존성 체인 깊이 ≥ 3, 계층 명확 | Phase 1: 기반 → Phase 2: 핵심 서비스 → Phase 3: 통합 → Phase 4: 마무리 |

전략 선택 절차:
1. Task 특성 분석: 의존성 깊이, 위험도 분포, 우선순위 분포, 기반 작업 유무
2. 테이블 기준으로 최적 전략 자동 선택
3. 선택 근거를 Plan에 기록

Phase 그룹핑 원칙:
- 각 Phase에 명확한 목표/테마 부여
- Phase 내 Task는 가능한 한 독립적으로 실행 가능
- Phase 간 의존성 최소화

### Step 6: Map Dependencies and Parallelism

dependency를 정리한다.
- blocking prerequisites
- shared file conflicts
- integration order

병렬 가능성은 `Target Files` 겹침과 의미적 충돌 기준으로 판단한다.

### Step 7: Write the Plan

다음 구조로 저장한다.

```markdown
# Implementation Plan

## Overview
## Scope
### In Scope
### Out of Scope
## Components
## Implementation Phases
## Task Details
## Parallel Execution Summary
## Risks and Mitigations
## Open Questions
```

Task 템플릿:

```markdown
### Task [ID]: [title]
**Component**: ...
**Priority**: P0 | P1 | P2 | P3
**Type**: Feature | Bug | Refactor | Infrastructure | Test

**Description**: ...

**Acceptance Criteria**:
- [ ] ...

**Target Files**:
- [M] `...`

**Technical Notes**: ...
**Dependencies**: ...
```

## Error Handling

| 상황 | 대응 |
|------|------|
| spec 없음 | codebase 기반 plan 생성, 한계를 `Open Questions`에 적는다 |
| user input 모호 | best-effort defaults를 적용하고 가정을 남긴다 |
| 파일 경로 불명확 | `[TBD]`를 사용하고 사유를 남긴다 |
| task가 너무 많음 | phase로 나누고 overview/index를 유지한다 |
| spec 갭 발견 | plan 수정으로 덮지 말고 `Open Questions`에 기록한다 |

## Integration

- `feature-draft`: 구현 계획 입력 원천
- `implementation`: 이 plan을 직접 실행
- `implementation-review`: task/AC 검증 기준
- `spec-update-todo`: spec gap 후속 반영

## Optional Writing Helper

문서가 길어지면 이 agent가 먼저 skeleton/섹션 헤더를 직접 저장한 뒤 같은 흐름에서 내용을 채운다. 의존 섹션은 순차 fill하고, 독립 섹션은 필요 시 `worker` agent로 bounded 병렬 fill할 수 있다. plan의 필수 구조와 task 내용 결정은 이 agent가 책임진다.

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

> **Mirror Notice**: 이 스킬의 본문은 `.codex/agents/implementation-plan.toml`의 `developer_instructions` 복사본이다.
> 사용자가 직접 호출할 때 중간 과정의 가시성을 확보하기 위해 복붙되었다.
> 내용을 수정할 때는 agent 파일과 이 스킬 파일을 **반드시 함께** 수정해야 한다.
