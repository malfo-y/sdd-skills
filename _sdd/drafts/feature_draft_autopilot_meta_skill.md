# Feature Draft: Autopilot 메타스킬 + 에이전트 전환

**날짜**: 2026-03-16
**근거 토론**: `_sdd/discussion/discussion_autopilot_meta_skill.md`
**후속 토론**: `_sdd/discussion/discussion_autopilot_open_questions.md` (Open Questions 해결)
**변경된 요구사항**: 오케스트레이터 저장 위치 변경 (`.claude/skills/` → `_sdd/pipeline/`)

---

<!-- spec-update-todo-input-start -->

# Part 1: Spec Patch Draft

> 이 패치는 해당 스펙 섹션에 직접 복사-붙여넣기하거나,
> `spec-update-todo` 스킬의 입력으로 사용할 수 있습니다.

# Spec Update Input

**Date**: 2026-03-16
**Author**: feature-draft
**Target Spec**: `_sdd/spec/main.md`
**Spec Update Classification**: MUST update

## Background & Motivation Updates

### Background Update: Agent Layer 도입

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Background & Motivation`

**Current State**:
현재 SDD Skills는 스킬 전용(skills-only) 아키텍처를 사용한다. 19개 스킬이 `.claude/skills/*/SKILL.md` 형태로 정의되어 있으며, 각 스킬은 사용자의 슬래시 커맨드(`/스킬명`)로 직접 호출된다. 스킬 간 자동화된 파이프라인 연결은 없으며, 사용자가 수동으로 다음 스킬을 호출해야 한다. 유일한 에이전트는 `write-phased`로, 문서/코드 작성 전용 서브에이전트이다.

**Proposed**:
스킬 + 에이전트 이중 아키텍처(dual architecture)를 도입한다.
- **에이전트 레이어** (`.claude/agents/*.md`): 파이프라인 필수 스킬 8개를 에이전트로 정의하여 서브에이전트 호출이 가능하도록 한다
- **래퍼 스킬 레이어** (`.claude/skills/*/SKILL.md`): 기존 스킬을 에이전트 위임 래퍼로 전환하여 사용자의 `/스킬명` 호출 인터페이스를 유지한다
- **메타스킬**: `autopilot` 스킬이 에이전트들을 오케스트레이션하여 end-to-end 자율 개발 파이프라인을 실행한다

**Reason**:
현재 사용자가 대규모 기능을 구현하려면 6-7개 스킬을 수동으로 순서대로 호출해야 하며, 중간에 맥락이 유실되거나 단계를 빠뜨릴 위험이 있다. 에이전트 레이어를 도입하면 `autopilot`이 필요한 에이전트를 서브에이전트로 자동 호출하여 전체 파이프라인을 자율적으로 실행할 수 있다. `write-phased` 에이전트가 이미 `tools: ["Agent"]`로 서브에이전트 호출이 가능함을 증명하였다.

**Key Features 업데이트 제안**:
```
- **19개 스킬 + 9개 에이전트**: 스킬은 사용자 인터페이스, 에이전트는 자동화 파이프라인 실행
- **autopilot 메타스킬**: 규모별 적응형 파이프라인 자동 생성 및 실행
```

## Design Changes

### Design Change: Agent Wrapper 패턴 추가

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Core Design` > `Design Patterns`

**Current State**:
`Core Design > Design Patterns`에 Decision Gate, Progressive Disclosure, Target Files, 2-Phase Generation 패턴이 정의되어 있다. 에이전트 위임 패턴은 정의되어 있지 않다.

**Proposed**:
**Agent Wrapper 패턴**을 Design Patterns에 추가한다:

```markdown
**Agent Wrapper 패턴**: 스킬을 에이전트로 전환할 때 적용한다. 스킬의 전체 로직은 `.claude/agents/<name>.md` 에이전트 정의로 이동하고, 기존 `.claude/skills/<name>/SKILL.md`는 에이전트에 위임하는 최소한의 래퍼로 전환한다. 이를 통해:
1. 사용자는 기존처럼 `/스킬명`으로 개별 호출 가능
2. autopilot이나 다른 에이전트가 서브에이전트로 호출 가능
3. 스킬의 full content는 에이전트 정의에 한 곳에서 관리

구조:
- 에이전트 정의: `.claude/agents/<name>.md` (frontmatter + 전체 스킬 로직)
- 래퍼 스킬: `.claude/skills/<name>/SKILL.md` (Agent() 호출만)
- 메타데이터: `.claude/skills/<name>/skill.json` (기존 유지)
```

**Reason**:
`write-phased`에서 이미 검증된 패턴이다. 에이전트 정의와 스킬 인터페이스를 분리함으로써 단일 책임 원칙을 유지하면서 두 가지 호출 경로(사용자 직접 호출, 서브에이전트 호출)를 모두 지원한다.

### Design Change: 2-Phase Orchestration 패턴

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Core Design` > `Design Patterns`

**Current State**:
현재 스킬은 각각 독립적으로 실행되며, 멀티 스킬 파이프라인을 자율적으로 실행하는 패턴이 정의되어 있지 않다.

**Proposed**:
**2-Phase Orchestration 패턴**을 Design Patterns에 추가한다:

```markdown
**2-Phase Orchestration 패턴**: autopilot 메타스킬에서 사용한다. 사용자 인터랙션을 전반부에 집중하고, 후반부는 완전 자율 실행한다.

- Phase 1 (Interactive): 사용자와 인라인 discussion → 코드베이스 탐색 → 규모 판단 → 오케스트레이터 스킬 생성
- Phase 1.5 (Checkpoint): 생성된 오케스트레이터를 사용자에게 제시 → 확인/수정 → 실행 승인
- Phase 2 (Autonomous): 승인된 오케스트레이터 실행 → 각 단계 마일스톤 텍스트 출력 + `_sdd/pipeline/` 로그 기록 → 중단 없이 완료까지 진행

종료 조건:
- Review-fix 루프: 최대 3회, critical/high = 0이면 종료, minor는 로그만
- 에러 핸들링: 상세 로그 → 디버깅 → 3회 재시도 → 실패 시 로그 남기고 사용자에게 보고
```

**Reason**:
토론에서 확정된 "선행 집중형 사용자 인터랙션" 모델을 패턴으로 공식화한다. Phase 2에서 중단 없이 진행함으로써 파이프라인 효율을 극대화하면서, Phase 1.5 체크포인트에서 사용자가 최종 검토할 기회를 보장한다.

## New Features

### Feature: autopilot (적응형 오케스트레이터 생성 메타스킬)

**Priority**: High
**Category**: 메타스킬
**Target Section**: `_sdd/spec/main.md` > `Component Details` (신규 컴포넌트)

**Description**:
사용자가 `/autopilot "기능 설명"`으로 호출하면, 다음 흐름을 자동으로 수행하는 적응형 오케스트레이터 생성 메타스킬이다:

1. **Discussion (인라인)**: 사용자와 대화하여 요구사항을 구체화한다 (에이전트가 아닌 스킬 내 인라인으로 실행)
2. **코드베이스 탐색**: 현재 프로젝트 구조, 스펙, 관련 코드를 분석한다
3. **규모/복잡도 판단**: 분석 결과를 기반으로 소/중/대 규모를 판단한다
4. **오케스트레이터 생성**: 규모에 맞는 맞춤형 오케스트레이터 SKILL.md를 `_sdd/pipeline/`에 생성한다
5. **사용자 확인**: 생성된 오케스트레이터를 사용자에게 제시하여 확인/수정을 받는다
6. **자율 실행**: 승인된 오케스트레이터가 에이전트 파이프라인을 자율적으로 실행한다

**규모별 파이프라인 판단 기준**:

| 규모 | 판단 기준 | 생성되는 파이프라인 |
|------|----------|-------------------|
| 소규모 | 파일 1-3개, 스펙 변경 없음 | implementation → 인라인 테스트 |
| 중규모 | 파일 4-10개, 스펙 패치 필요 | feature-draft → impl-plan → impl → review → 인라인 테스트 → spec-sync |
| 대규모 | 파일 10개+, 신규 스펙 섹션 | full SDD pipeline (모든 agent 사용) |

**테스트 전략 판단**:

| 조건 | 전략 |
|------|------|
| 테스트 iteration < 수 분 | Claude Code 인라인 디버깅 (테스트 → 수정 → 재시도) |
| 테스트 iteration > 수십 분 | ralph-loop-init 에이전트 (장시간 자동 디버깅) |

**Acceptance Criteria**:
- [ ] `/autopilot`으로 호출 가능
- [ ] discussion을 인라인으로 실행하여 요구사항을 수집
- [ ] 코드베이스 탐색을 통해 프로젝트 컨텍스트를 파악
- [ ] 규모별(소/중/대) 적절한 파이프라인을 생성
- [ ] 생성된 오케스트레이터가 SKILL.md 표준 포맷을 준수
- [ ] **Pre-flight Check**: `_sdd/env.md` 기반 확보 리소스 파악 + 파이프라인별 필요 리소스 추정 → 갭 분석 → 사용자 확인
- [ ] 사용자 확인 후 자율 실행 (Phase 1.5 체크포인트)
- [ ] 각 마일스톤에서 텍스트 출력 + `_sdd/pipeline/` 로그 기록
- [ ] review-fix 루프 최대 3회, critical/high = 0이면 종료
- [ ] 에러 발생 시 상세 로그 기록 → 디버깅 → 최대 3회 재시도

### Feature: 파이프라인 로그 시스템

**Priority**: Medium
**Category**: 인프라
**Location**: `_sdd/pipeline/`
**Target Section**: `_sdd/spec/main.md` > `Architecture Overview` > `_sdd/ Artifact Map`

**Description**:
autopilot이 파이프라인을 실행하는 동안 각 단계의 진행 상황과 결과를 기록하는 로그 시스템이다. `_sdd/pipeline/` 디렉토리에 실행별 로그 파일을 생성한다.

**로그 파일 구조**:
```
_sdd/pipeline/
└── log_<feature-name>_<timestamp>.md
```

**로그 내용**:
- 파이프라인 시작 시간 및 설정
- 각 단계(에이전트) 시작/완료 시간
- **각 에이전트의 핵심 결정사항 요약** (autopilot이 에이전트 결과에서 추출하여 기록. 에이전트 자체는 로그를 모름)
- 마일스톤 메시지 (사용자에게도 텍스트로 출력)
- 에러 발생 시 상세 로그
- review-fix 루프 결과 (회차별)
- 최종 요약

**로그 기록 방식**: 공유 로그 파일. autopilot이 `_sdd/pipeline/log_<topic>_<timestamp>.md`를 생성하고, 각 에이전트 결과를 받을 때마다 핵심 결정사항을 추출하여 로그에 추가한다.

**Acceptance Criteria**:
- [ ] `_sdd/pipeline/` 디렉토리에 실행별 로그 파일이 생성됨
- [ ] 각 에이전트 단계의 시작/완료가 기록됨
- [ ] 에러 및 재시도 이력이 기록됨
- [ ] 로그 파일이 마크다운 포맷으로 사람이 읽을 수 있음

## Improvements

### Improvement: 8개 스킬의 에이전트 전환

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Architecture Overview`, `Component Details`

**Current State**:
8개 스킬이 `.claude/skills/*/SKILL.md`에 전체 로직을 포함하고 있으며, 서브에이전트로 호출할 수 없다. `write-phased`만 유일하게 에이전트 전환이 완료되었다.

**Proposed**:
다음 8개 스킬을 Agent Wrapper 패턴으로 전환한다:

| 스킬 | 현재 버전 | 에이전트 필요 도구 | references/ | examples/ |
|------|----------|-------------------|-------------|-----------|
| feature-draft | 1.0.0 | Read, Write, Edit, Glob, Grep, Agent | Yes (4) | Yes (1) |
| implementation-plan | 1.0.0 | Read, Write, Edit, Glob, Grep, Agent | Yes (2) | Yes (1) |
| implementation | 1.0.0 | Read, Write, Edit, Glob, Grep, Bash, Agent | Yes (다수) | Yes (1) |
| implementation-review | 2.0.0 | Read, Glob, Grep, Agent | Yes (다수) | Yes (1) |
| ralph-loop-init | 1.0.0 | Read, Write, Edit, Glob, Grep, Bash | No | Yes (1) |
| spec-update-done | 1.0.0 | Read, Write, Edit, Glob, Grep, Bash | Yes (2) | Yes (2) |
| spec-update-todo | 1.0.0 | Read, Write, Edit, Glob, Grep | Yes | Yes |
| spec-review | 1.0.0 | Read, Glob, Grep, Agent | Yes (1) | Yes (1) |

**전환 작업**:
1. 각 스킬의 SKILL.md 전체 내용을 `.claude/agents/<name>.md`로 이동 (frontmatter 추가)
2. 기존 SKILL.md를 Agent Wrapper 패턴의 래퍼로 교체
3. skill.json은 기존 유지 (description만 필요 시 조정)

**Reason**:
autopilot이 파이프라인을 자동화하려면 각 스킬을 서브에이전트로 호출할 수 있어야 한다. 래퍼 스킬을 유지함으로써 기존 사용자 워크플로우(`/스킬명` 직접 호출)와의 하위 호환성을 보장한다.

## Component Changes

**신규 컴포넌트**:
- `autopilot` 스킬 (`.claude/skills/autopilot/`)
  - SKILL.md, skill.json, references/ (pipeline-templates.md, scale-assessment.md), examples/ (sample-orchestrator.md)

**신규 에이전트 정의** (`.claude/agents/`):
- `feature-draft.md`
- `implementation-plan.md`
- `implementation.md`
- `implementation-review.md`
- `ralph-loop-init.md`
- `spec-update-done.md`
- `spec-update-todo.md`
- `spec-review.md`

**변경 컴포넌트** (래퍼로 전환):
- `.claude/skills/feature-draft/SKILL.md` → 래퍼
- `.claude/skills/implementation-plan/SKILL.md` → 래퍼
- `.claude/skills/implementation/SKILL.md` → 래퍼
- `.claude/skills/implementation-review/SKILL.md` → 래퍼
- `.claude/skills/ralph-loop-init/SKILL.md` → 래퍼
- `.claude/skills/spec-update-done/SKILL.md` → 래퍼
- `.claude/skills/spec-update-todo/SKILL.md` → 래퍼
- `.claude/skills/spec-review/SKILL.md` → 래퍼

**변경 없는 컴포넌트** (스킬로 유지):
- discussion, git, sdd-upgrade, spec-snapshot, spec-create, spec-rewrite, spec-summary, spec-upgrade, pr-review, pr-spec-patch, guide-create

## Configuration Changes

없음. 환경 설정(`_sdd/env.md`) 변경 불필요. 기존 Claude Code 에이전트 인프라(`tools` 설정)만 활용한다.

## Usage Scenarios

### Scenario 1: 대규모 기능 구현 with autopilot

**사용자 요청**: `/autopilot "인증 시스템 구현하고 싶어 — JWT 기반, 로그인/로그아웃/토큰 갱신"`

**Phase 1 (Interactive)**:
1. autopilot이 인라인 discussion을 시작하여 요구사항 구체화 (토큰 만료 정책, 권한 체계, DB 연동 등)
2. 코드베이스 탐색: 기존 프로젝트 구조, 관련 모듈, 스펙 확인
3. 규모 판단: 파일 15개+, 신규 스펙 섹션 필요 → **대규모**
4. 오케스트레이터 생성: `.claude/skills/orchestrator_auth_system/SKILL.md`

**Phase 1.5 (Checkpoint)**:
5. 생성된 파이프라인을 사용자에게 제시:
   ```
   Pipeline: feature-draft → impl-plan → impl → review-fix(max 3) → inline test → spec-sync
   Estimated agents: 6, Review rounds: up to 3
   ```
6. 사용자 확인: "좋아, 진행해"

**Phase 2 (Autonomous)**:
7. feature-draft agent → `_sdd/drafts/feature_draft_auth_system.md`
8. implementation-plan agent → `_sdd/implementation/plan_auth_system.md`
9. implementation agent → 코드 생성 (15+ files)
10. implementation-review agent → 리뷰 리포트
11. review-fix 루프: 1회차에서 critical 2건 → implementation agent로 수정 → 2회차 critical 0 → 종료
12. 인라인 테스트: 테스트 실행 → 2건 실패 → 수정 → 통과
13. spec-update-done agent → 스펙 동기화
14. 최종 요약 출력 + `_sdd/pipeline/log_auth_system_20260316.md` 완성

### Scenario 2: 소규모 버그 수정 with autopilot

**사용자 요청**: `/autopilot "토큰 갱신 시 만료 시간이 갱신되지 않는 버그 수정"`

**Phase 1 (Interactive)**:
1. autopilot이 간단한 discussion: 재현 조건 확인, 관련 파일 식별
2. 코드베이스 탐색: `src/auth/token.py`의 `refresh_token()` 함수에서 `expires_at` 미갱신 확인
3. 규모 판단: 파일 1개, 스펙 변경 없음 → **소규모**
4. 오케스트레이터 생성: 축소된 파이프라인

**Phase 1.5 (Checkpoint)**:
5. 파이프라인 제시:
   ```
   Pipeline: impl → inline test
   Estimated agents: 1, No spec update needed
   ```
6. 사용자 확인

**Phase 2 (Autonomous)**:
7. implementation agent → `refresh_token()` 버그 수정
8. 인라인 테스트: 기존 테스트 + 회귀 테스트 실행 → 통과
9. 최종 요약 출력 + 로그 기록

## Notes

### Context

- 토론 10라운드(`_sdd/discussion/discussion_autopilot_meta_skill.md`)를 통해 결정된 사항을 기반으로 함
- `write-phased` 에이전트가 Agent Wrapper 패턴의 선례로, `tools: ["Agent"]`를 통한 서브에이전트 호출이 검증됨
- 현재 19개 스킬 중 `discussion`은 AskUserQuestion이 핵심이므로 에이전트 전환하지 않음
- autopilot 자체도 스킬로 유지 (사용자 인터랙션 + 오케스트레이션 역할)

### Decision-Log Candidates

- **에이전트 내 서브에이전트 호출**: 에이전트 정의에서 `tools`에 `"Agent"`를 포함하면 가능. write-phased가 증명함.
- **선행 집중형 인터랙션**: Phase 1에서 사용자와 충분히 논의 후 Phase 2는 완전 자율. 이유: 중간 중단이 파이프라인 효율을 저하시킴.
- **스킬 생성형 메타스킬**: autopilot이 맞춤형 오케스트레이터를 동적 생성. 이유: 규모별 최적 파이프라인이 달라 하드코딩 불가.
- **오케스트레이터 = SKILL.md 포맷**: 기존 인프라 활용, Claude가 자연스럽게 해석 가능.
- **Review-fix 최대 3회**: 무한 루프 방지. critical/high = 0이면 즉시 종료.
- **에러 핸들링**: 단순 스킵이 아닌 로그 + 디버깅 + 재시도 방식. 최대 3회 재시도.

### Constraints

- autopilot은 스킬로 유지 (에이전트 전환 불필요) — 사용자 인터랙션이 핵심
- discussion은 스킬로 유지 — AskUserQuestion이 메인 컨텍스트에서 실행되어야 함
- 생성된 오케스트레이터는 `.claude/skills/`에 저장 — 프로젝트 스킬로 재사용 가능
- 에이전트 정의에 references/examples 내용 포함 방식은 구현 시 결정 (inline vs file read)

<!-- spec-update-todo-input-end -->

---

# Part 2: Implementation Plan

## Overview

8개 파이프라인 필수 스킬을 에이전트로 전환(Agent Wrapper 패턴)하고, autopilot 적응형 오케스트레이터 생성 메타스킬을 구현하여, 사용자가 `/autopilot` 한 줄로 end-to-end SDD 파이프라인을 자율 실행할 수 있도록 한다. 파이프라인 실행 로그 인프라(`_sdd/pipeline/`)도 함께 구축한다.

## Scope

### In Scope

- `.claude/agents/` 아래 8개 에이전트 정의 파일 생성
- `.claude/skills/*/SKILL.md` 8개를 래퍼로 전환
- `.claude/skills/autopilot/` 신규 스킬 생성 (SKILL.md, skill.json, references/, examples/)
- `_sdd/pipeline/` 로그 시스템 설계 (autopilot SKILL.md 내 정의)
- 통합 테스트: 단일 에이전트 호출 + autopilot end-to-end

### Out of Scope

- `.codex/skills/` 동기화 (별도 후속 작업)
- 에이전트로 전환하지 않는 스킬 수정 (discussion, git, sdd-upgrade, spec-snapshot 등)
- 스펙 문서(`_sdd/spec/main.md`) 직접 수정 (별도 spec-update-todo 실행 필요)
- 기존 스킬의 로직 변경 (래퍼 전환만, 내용 수정 없음)

## Components

1. **에이전트 정의 생성**: 8개 스킬의 SKILL.md 내용을 에이전트 정의 포맷(frontmatter + 본문)으로 변환
2. **래퍼 스킬 전환**: 기존 SKILL.md를 Agent() 호출 래퍼로 교체
3. **autopilot 메타스킬**: 적응형 오케스트레이터 생성 스킬 (SKILL.md + references + examples)
4. **파이프라인 로그 시스템**: `_sdd/pipeline/` 마일스톤 로그 설계
5. **통합 테스트**: 에이전트 호출 및 autopilot 파이프라인 검증

## Implementation Phases

### Phase 1: Agent 정의 파일 생성 (8개)

모든 [C] Create — `.claude/agents/` 아래 생성. 모든 태스크 독립적 → **Max Parallel = 8**

| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 1  | feature-draft agent 정의 | P0 | - | 에이전트 정의 생성 |
| 2  | implementation-plan agent 정의 | P0 | - | 에이전트 정의 생성 |
| 3  | implementation agent 정의 | P0 | - | 에이전트 정의 생성 |
| 4  | implementation-review agent 정의 | P0 | - | 에이전트 정의 생성 |
| 5  | ralph-loop-init agent 정의 | P1 | - | 에이전트 정의 생성 |
| 6  | spec-update-done agent 정의 | P0 | - | 에이전트 정의 생성 |
| 7  | spec-update-todo agent 정의 | P0 | - | 에이전트 정의 생성 |
| 8  | spec-review agent 정의 | P1 | - | 에이전트 정의 생성 |

### Phase 2: Wrapper 스킬 전환 (8개)

모든 [M] Modify — `.claude/skills/*/SKILL.md` 수정. 모든 태스크 독립적 → **Max Parallel = 8**
각 태스크는 대응하는 Phase 1 에이전트 정의가 존재해야 함.

| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 9  | feature-draft wrapper 전환 | P0 | 1 | 래퍼 스킬 전환 |
| 10 | implementation-plan wrapper 전환 | P0 | 2 | 래퍼 스킬 전환 |
| 11 | implementation wrapper 전환 | P0 | 3 | 래퍼 스킬 전환 |
| 12 | implementation-review wrapper 전환 | P0 | 4 | 래퍼 스킬 전환 |
| 13 | ralph-loop-init wrapper 전환 | P1 | 5 | 래퍼 스킬 전환 |
| 14 | spec-update-done wrapper 전환 | P0 | 6 | 래퍼 스킬 전환 |
| 15 | spec-update-todo wrapper 전환 | P0 | 7 | 래퍼 스킬 전환 |
| 16 | spec-review wrapper 전환 | P1 | 8 | 래퍼 스킬 전환 |

### Phase 3: Autopilot 메타스킬 생성

Task 17은 독립, Task 18-19는 Task 17에 의존 → **순차 실행 (17 → 18, 19 병렬)**

| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 17 | autopilot SKILL.md + skill.json 생성 | P0 | - | autopilot 메타스킬 |
| 18 | autopilot references 작성 (pipeline-templates.md, scale-assessment.md) | P1 | 17 | autopilot 메타스킬 |
| 19 | autopilot examples 작성 (sample-orchestrator.md) | P1 | 17 | autopilot 메타스킬 |

### Phase 4: 파이프라인 인프라 및 통합 테스트

Task 20은 Task 17에 의존, Task 21은 Phase 1-2 완료 후, Task 22는 Phase 3 완료 후.

| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 20 | 파이프라인 로그 시스템 설계 (autopilot SKILL.md 내 정의) | P1 | 17 | 파이프라인 로그 시스템 |
| 21 | 통합 테스트 — 단일 스킬 에이전트 호출 테스트 | P1 | 9-16 | 통합 테스트 |
| 22 | 통합 테스트 — autopilot end-to-end 테스트 | P2 | 17-20 | 통합 테스트 |

## Task Details

### Task 1: feature-draft agent 정의

**Component**: 에이전트 정의 생성
**Priority**: P0-Critical
**Type**: Create

**Description**:
`.claude/skills/feature-draft/SKILL.md`의 전체 내용을 `.claude/agents/feature-draft.md`로 이동한다. 에이전트 frontmatter를 추가하고, references/ 및 examples/ 내용의 참조 방식을 결정한다.

에이전트 frontmatter:
```yaml
---
name: feature-draft
description: "Use this agent when creating a feature draft..."
tools: ["Read", "Write", "Edit", "Glob", "Grep", "Agent"]
model: inherit
---
```

**Acceptance Criteria**:
- [ ] `.claude/agents/feature-draft.md`가 생성됨
- [ ] frontmatter에 name, description, tools, model이 정의됨
- [ ] tools에 Agent가 포함됨 (write-phased 서브에이전트 호출 가능)
- [ ] 기존 SKILL.md의 전체 로직이 에이전트 정의에 포함됨

**Target Files**:
- [C] `.claude/agents/feature-draft.md`

**Technical Notes**:
- **references/examples는 Read로 참조** (결정됨): 에이전트 본문에는 SKILL.md 로직만 포함하고, references/ (4개)와 examples/ (1개)는 기존 `.claude/skills/feature-draft/references/` 경로에서 필요 시 Read로 읽도록 지시
- 현재 SKILL.md에서 references를 `Read` 지시하는 패턴이 있다면 그대로 유지
- write-phased agent 정의를 포맷 참조로 사용

**Dependencies**: -

---

### Task 2: implementation-plan agent 정의

**Component**: 에이전트 정의 생성
**Priority**: P0-Critical
**Type**: Create

**Description**:
`.claude/skills/implementation-plan/SKILL.md`의 전체 내용을 `.claude/agents/implementation-plan.md`로 이동한다.

에이전트 frontmatter:
```yaml
---
name: implementation-plan
description: "Use this agent when creating an implementation plan..."
tools: ["Read", "Write", "Edit", "Glob", "Grep", "Agent"]
model: inherit
---
```

**Acceptance Criteria**:
- [ ] `.claude/agents/implementation-plan.md`가 생성됨
- [ ] frontmatter에 name, description, tools, model이 정의됨
- [ ] tools에 Agent가 포함됨 (write-phased 서브에이전트 호출 가능)
- [ ] 기존 SKILL.md의 전체 로직이 에이전트 정의에 포함됨

**Target Files**:
- [C] `.claude/agents/implementation-plan.md`

**Technical Notes**:
- references/ (2개 파일)와 examples/ (1개 파일) 참조 방식은 Task 1과 동일하게 결정
- feature-draft agent의 출력(`_sdd/drafts/`)을 입력으로 받는 흐름이 에이전트 정의에 명시되어야 함

**Dependencies**: -

---

### Task 3: implementation agent 정의

**Component**: 에이전트 정의 생성
**Priority**: P0-Critical
**Type**: Create

**Description**:
`.claude/skills/implementation/SKILL.md`의 전체 내용을 `.claude/agents/implementation.md`로 이동한다. implementation은 코드 실행이 필요하므로 `Bash` 도구를 포함한다.

에이전트 frontmatter:
```yaml
---
name: implementation
description: "Use this agent when implementing code based on an implementation plan..."
tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "Agent"]
model: inherit
---
```

**Acceptance Criteria**:
- [ ] `.claude/agents/implementation.md`가 생성됨
- [ ] tools에 Bash가 포함됨 (코드 실행, 테스트 실행 필요)
- [ ] tools에 Agent가 포함됨 (write-phased 서브에이전트 호출 가능)
- [ ] 기존 SKILL.md의 전체 로직이 에이전트 정의에 포함됨

**Target Files**:
- [C] `.claude/agents/implementation.md`

**Technical Notes**:
- implementation은 가장 큰 스킬 중 하나로 references/와 examples/가 많음
- Bash 도구가 필요한 이유: 코드 실행, 테스트 실행, 빌드 확인 등
- 컨텍스트 윈도우 소진 위험이 가장 높은 에이전트 — 참조 파일을 필요 시에만 Read하도록 설계

**Dependencies**: -

---

### Task 4: implementation-review agent 정의

**Component**: 에이전트 정의 생성
**Priority**: P0-Critical
**Type**: Create

**Description**:
`.claude/skills/implementation-review/SKILL.md`의 전체 내용을 `.claude/agents/implementation-review.md`로 이동한다. 리뷰 에이전트는 코드를 수정하지 않으므로 Write/Edit/Bash 불필요.

에이전트 frontmatter:
```yaml
---
name: implementation-review
description: "Use this agent when reviewing implementation quality..."
tools: ["Read", "Glob", "Grep", "Agent"]
model: inherit
---
```

**Acceptance Criteria**:
- [ ] `.claude/agents/implementation-review.md`가 생성됨
- [ ] tools에 Read, Glob, Grep, Agent만 포함 (읽기 전용 + 서브에이전트)
- [ ] 기존 SKILL.md의 전체 리뷰 로직이 에이전트 정의에 포함됨
- [ ] 리뷰 결과 포맷이 review-fix 루프에서 파싱 가능하도록 구조화됨

**Target Files**:
- [C] `.claude/agents/implementation-review.md`

**Technical Notes**:
- 현재 버전 2.0.0으로 최근 개선된 스킬
- 리뷰 결과에 critical/high/medium/low 분류가 명시되어야 autopilot의 review-fix 루프 종료 조건 판단이 가능

**Dependencies**: -

---

### Task 5: ralph-loop-init agent 정의

**Component**: 에이전트 정의 생성
**Priority**: P1-High
**Type**: Create

**Description**:
`.claude/skills/ralph-loop-init/SKILL.md`의 전체 내용을 `.claude/agents/ralph-loop-init.md`로 이동한다. ralph-loop-init은 장시간 디버깅 루프를 설정하므로 Bash가 필요하지만, 서브에이전트 호출은 불필요.

에이전트 frontmatter:
```yaml
---
name: ralph-loop-init
description: "Use this agent when setting up a long-running debug loop..."
tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash"]
model: inherit
---
```

**Acceptance Criteria**:
- [ ] `.claude/agents/ralph-loop-init.md`가 생성됨
- [ ] tools에 Bash가 포함됨 (스크립트 생성/실행 필요)
- [ ] tools에 Agent가 포함되지 않음 (서브에이전트 불필요)
- [ ] 기존 SKILL.md의 전체 로직이 에이전트 정의에 포함됨

**Target Files**:
- [C] `.claude/agents/ralph-loop-init.md`

**Technical Notes**:
- references/ 없음, examples/ 1개 파일
- autopilot에서 테스트 iteration이 긴 경우에만 호출됨

**Dependencies**: -

---

### Task 6: spec-update-done agent 정의

**Component**: 에이전트 정의 생성
**Priority**: P0-Critical
**Type**: Create

**Description**:
`.claude/skills/spec-update-done/SKILL.md`의 전체 내용을 `.claude/agents/spec-update-done.md`로 이동한다. 스펙 파일 수정이 필요하므로 Write/Edit, 구현 결과 확인을 위해 Bash가 필요.

에이전트 frontmatter:
```yaml
---
name: spec-update-done
description: "Use this agent when updating spec after implementation is done..."
tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash"]
model: inherit
---
```

**Acceptance Criteria**:
- [ ] `.claude/agents/spec-update-done.md`가 생성됨
- [ ] tools에 Bash가 포함됨 (git diff 등 확인 필요)
- [ ] 기존 SKILL.md의 전체 로직이 에이전트 정의에 포함됨
- [ ] references/ (2개)와 examples/ (2개) 참조 방식이 결정됨

**Target Files**:
- [C] `.claude/agents/spec-update-done.md`

**Technical Notes**:
- 스펙 직접 수정이 허용되는 몇 안 되는 스킬 중 하나
- autopilot 파이프라인의 마지막 단계에서 호출됨

**Dependencies**: -

---

### Task 7: spec-update-todo agent 정의

**Component**: 에이전트 정의 생성
**Priority**: P0-Critical
**Type**: Create

**Description**:
`.claude/skills/spec-update-todo/SKILL.md`의 전체 내용을 `.claude/agents/spec-update-todo.md`로 이동한다. 스펙 파일 수정이 필요하므로 Write/Edit이 필요하지만 Bash는 불필요.

에이전트 frontmatter:
```yaml
---
name: spec-update-todo
description: "Use this agent when updating spec with planned changes..."
tools: ["Read", "Write", "Edit", "Glob", "Grep"]
model: inherit
---
```

**Acceptance Criteria**:
- [ ] `.claude/agents/spec-update-todo.md`가 생성됨
- [ ] tools에 Bash, Agent가 포함되지 않음
- [ ] 기존 SKILL.md의 전체 로직이 에이전트 정의에 포함됨
- [ ] feature-draft 출력(`_sdd/drafts/`)을 입력으로 받는 흐름이 명시됨

**Target Files**:
- [C] `.claude/agents/spec-update-todo.md`

**Technical Notes**:
- feature-draft가 생성한 spec patch draft를 입력으로 받아 실제 스펙에 반영하는 역할
- references/와 examples/ 참조 방식은 다른 에이전트와 동일하게 결정

**Dependencies**: -

---

### Task 8: spec-review agent 정의

**Component**: 에이전트 정의 생성
**Priority**: P1-High
**Type**: Create

**Description**:
`.claude/skills/spec-review/SKILL.md`의 전체 내용을 `.claude/agents/spec-review.md`로 이동한다. 리뷰 전용이므로 읽기 도구만 필요.

에이전트 frontmatter:
```yaml
---
name: spec-review
description: "Use this agent when reviewing spec document quality..."
tools: ["Read", "Glob", "Grep", "Agent"]
model: inherit
---
```

**Acceptance Criteria**:
- [ ] `.claude/agents/spec-review.md`가 생성됨
- [ ] tools에 Read, Glob, Grep, Agent만 포함 (읽기 전용 + 서브에이전트)
- [ ] 기존 SKILL.md의 전체 리뷰 로직이 에이전트 정의에 포함됨
- [ ] references/ (1개)와 examples/ (1개) 참조 방식이 결정됨

**Target Files**:
- [C] `.claude/agents/spec-review.md`

**Technical Notes**:
- Agent 도구는 write-phased 서브에이전트 호출 가능성을 위해 포함
- 스펙 리뷰 결과가 구조화되어 다음 스킬에서 활용 가능해야 함

**Dependencies**: -

---

### Task 9: feature-draft wrapper 전환

**Component**: 래퍼 스킬 전환
**Priority**: P0-Critical
**Type**: Modify

**Description**:
`.claude/skills/feature-draft/SKILL.md`의 전체 내용을 Agent Wrapper 패턴의 래퍼로 교체한다. write-phased 래퍼를 참조 포맷으로 사용한다.

래퍼 내용 (version minor 업: 1.0.0 → 1.1.0):
```markdown
---
name: feature-draft
description: Use this skill when creating a feature draft...
version: 1.1.0
---
# feature-draft (Wrapper)
이 스킬은 `feature-draft` 서브에이전트에 작업을 위임한다.
## 실행 방법
Agent(subagent_type="feature-draft", prompt="[사용자 요청]")
## 규칙
1. 이 스킬에서 직접 파일을 작성하지 않는다.
2. 사용자의 요청을 원문 그대로 서브에이전트에 전달한다.
3. 서브에이전트의 결과를 받아 사용자에게 보고한다.
```

**Acceptance Criteria**:
- [ ] SKILL.md가 래퍼 포맷으로 교체됨
- [ ] Agent() 호출이 feature-draft 에이전트를 지정함
- [ ] skill.json의 description이 기존과 호환됨
- [ ] **skill.json과 SKILL.md frontmatter의 version이 1.1.0으로 업데이트됨**
- [ ] 기존 references/ 및 examples/ 디렉토리는 유지 (에이전트가 Read로 참조)

**Target Files**:
- [M] `.claude/skills/feature-draft/SKILL.md`
- [M] `.claude/skills/feature-draft/skill.json` -- version 1.1.0으로 업데이트

**Technical Notes**:
- **래퍼 전환 시 Minor 버전 업** (결정됨): 1.0.0 → 1.1.0. 기능 동일, 구조 변경 표시
- 기존 SKILL.md의 백업은 에이전트 정의로 이동되었으므로 별도 불필요
- references/ 와 examples/ 파일은 삭제하지 않음 — 에이전트가 필요 시 Read로 참조

**Dependencies**: 1

---

### Task 10: implementation-plan wrapper 전환

**Component**: 래퍼 스킬 전환
**Priority**: P0-Critical
**Type**: Modify

**Description**:
`.claude/skills/implementation-plan/SKILL.md`를 래퍼로 교체한다. Task 9와 동일한 래퍼 패턴 적용.

**Acceptance Criteria**:
- [ ] SKILL.md가 래퍼 포맷으로 교체됨
- [ ] Agent() 호출이 implementation-plan 에이전트를 지정함

**Target Files**:
- [M] `.claude/skills/implementation-plan/SKILL.md`
- [M] `.claude/skills/implementation-plan/skill.json` -- version 1.1.0으로 업데이트

**Technical Notes**:
- Minor 버전 업: 1.0.0 → 1.1.0
- references/ (2개), examples/ (1개) 유지

**Dependencies**: 2

---

### Task 11: implementation wrapper 전환

**Component**: 래퍼 스킬 전환
**Priority**: P0-Critical
**Type**: Modify

**Description**:
`.claude/skills/implementation/SKILL.md`를 래퍼로 교체한다. Task 9와 동일한 래퍼 패턴 적용.

**Acceptance Criteria**:
- [ ] SKILL.md가 래퍼 포맷으로 교체됨
- [ ] Agent() 호출이 implementation 에이전트를 지정함

**Target Files**:
- [M] `.claude/skills/implementation/SKILL.md`
- [M] `.claude/skills/implementation/skill.json` -- version 1.1.0으로 업데이트

**Technical Notes**:
- Minor 버전 업: 1.0.0 → 1.1.0
- 가장 큰 스킬 중 하나 — references/ 다수 파일 유지
- Bash 도구가 필요한 에이전트이므로 래퍼에서는 직접 코드 실행하지 않음

**Dependencies**: 3

---

### Task 12: implementation-review wrapper 전환

**Component**: 래퍼 스킬 전환
**Priority**: P0-Critical
**Type**: Modify

**Description**:
`.claude/skills/implementation-review/SKILL.md`를 래퍼로 교체한다. Task 9와 동일한 래퍼 패턴 적용.

**Acceptance Criteria**:
- [ ] SKILL.md가 래퍼 포맷으로 교체됨
- [ ] Agent() 호출이 implementation-review 에이전트를 지정함

**Target Files**:
- [M] `.claude/skills/implementation-review/SKILL.md`
- [M] `.claude/skills/implementation-review/skill.json` -- version 2.1.0으로 업데이트

**Technical Notes**:
- Minor 버전 업: 2.0.0 → 2.1.0 (결정됨)

**Dependencies**: 4

---

### Task 13: ralph-loop-init wrapper 전환

**Component**: 래퍼 스킬 전환
**Priority**: P1-High
**Type**: Modify

**Description**:
`.claude/skills/ralph-loop-init/SKILL.md`를 래퍼로 교체한다. Task 9와 동일한 래퍼 패턴 적용.

**Acceptance Criteria**:
- [ ] SKILL.md가 래퍼 포맷으로 교체됨
- [ ] Agent() 호출이 ralph-loop-init 에이전트를 지정함

**Target Files**:
- [M] `.claude/skills/ralph-loop-init/SKILL.md`
- [M] `.claude/skills/ralph-loop-init/skill.json` -- version 1.1.0으로 업데이트

**Technical Notes**:
- Minor 버전 업: 1.0.0 → 1.1.0
- references/ 없음, examples/ (1개) 유지

**Dependencies**: 5

---

### Task 14: spec-update-done wrapper 전환

**Component**: 래퍼 스킬 전환
**Priority**: P0-Critical
**Type**: Modify

**Description**:
`.claude/skills/spec-update-done/SKILL.md`를 래퍼로 교체한다. Task 9와 동일한 래퍼 패턴 적용.

**Acceptance Criteria**:
- [ ] SKILL.md가 래퍼 포맷으로 교체됨
- [ ] Agent() 호출이 spec-update-done 에이전트를 지정함

**Target Files**:
- [M] `.claude/skills/spec-update-done/SKILL.md`
- [M] `.claude/skills/spec-update-done/skill.json` -- version 1.1.0으로 업데이트

**Technical Notes**:
- Minor 버전 업: 1.0.0 → 1.1.0
- references/ (2개), examples/ (2개) 유지
- 스펙 직접 수정 권한은 에이전트 정의에서 관리

**Dependencies**: 6

---

### Task 15: spec-update-todo wrapper 전환

**Component**: 래퍼 스킬 전환
**Priority**: P0-Critical
**Type**: Modify

**Description**:
`.claude/skills/spec-update-todo/SKILL.md`를 래퍼로 교체한다. Task 9와 동일한 래퍼 패턴 적용.

**Acceptance Criteria**:
- [ ] SKILL.md가 래퍼 포맷으로 교체됨
- [ ] Agent() 호출이 spec-update-todo 에이전트를 지정함

**Target Files**:
- [M] `.claude/skills/spec-update-todo/SKILL.md`
- [M] `.claude/skills/spec-update-todo/skill.json` -- version 1.1.0으로 업데이트

**Technical Notes**:
- Minor 버전 업: 1.0.0 → 1.1.0
- references/ 및 examples/ 유지

**Dependencies**: 7

---

### Task 16: spec-review wrapper 전환

**Component**: 래퍼 스킬 전환
**Priority**: P1-High
**Type**: Modify

**Description**:
`.claude/skills/spec-review/SKILL.md`를 래퍼로 교체한다. Task 9와 동일한 래퍼 패턴 적용.

**Acceptance Criteria**:
- [ ] SKILL.md가 래퍼 포맷으로 교체됨
- [ ] Agent() 호출이 spec-review 에이전트를 지정함

**Target Files**:
- [M] `.claude/skills/spec-review/SKILL.md`
- [M] `.claude/skills/spec-review/skill.json` -- version 1.1.0으로 업데이트

**Technical Notes**:
- Minor 버전 업: 1.0.0 → 1.1.0
- references/ (1개), examples/ (1개) 유지

**Dependencies**: 8

---

### Task 17: autopilot SKILL.md + skill.json 생성

**Component**: autopilot 메타스킬
**Priority**: P0-Critical
**Type**: Create

**Description**:
autopilot 메타스킬의 핵심 파일을 생성한다:

1. **SKILL.md**: 2-Phase Orchestration 패턴을 구현하는 메타스킬 정의
   - Phase 1 (Interactive): 인라인 discussion + 코드베이스 탐색 + 규모 판단
   - Phase 1.5 (Checkpoint): 오케스트레이터 생성 + 사용자 확인
   - Phase 2 (Autonomous): 오케스트레이터 실행 (에이전트 파이프라인)
   - Hard Rules: review-fix 최대 3회, 에러 3회 재시도, 마일스톤 로그 필수
   - 규모 판단 기준 (소/중/대)
   - 테스트 전략 판단 (인라인 vs ralph-loop-init)

2. **skill.json**: 메타데이터 정의
   ```json
   {
     "name": "autopilot",
     "description": "적응형 오케스트레이터 생성 메타스킬. /autopilot으로 호출하여 end-to-end SDD 파이프라인을 자율 실행한다.",
     "version": "1.0.0"
   }
   ```

**Acceptance Criteria**:
- [ ] `.claude/skills/autopilot/SKILL.md`가 생성됨
- [ ] Phase 1, 1.5, 2가 명확히 구분되어 정의됨
- [ ] 규모 판단 기준 (소/중/대)이 구체적으로 명시됨
- [ ] 오케스트레이터 생성 포맷 (SKILL.md 표준)이 정의됨
- [ ] review-fix 루프 종료 조건이 명시됨
- [ ] 에러 핸들링 절차가 명시됨
- [ ] skill.json이 생성됨

**Target Files**:
- [C] `.claude/skills/autopilot/SKILL.md`
- [C] `.claude/skills/autopilot/skill.json`

**Technical Notes**:
- autopilot은 에이전트가 아닌 스킬로 유지 — 사용자와의 인터랙션(Phase 1)이 핵심
- 오케스트레이터 생성 시 사용 가능한 에이전트 목록을 SKILL.md에 포함해야 함
- `.claude/agents/` 아래의 모든 에이전트 정의를 참조하여 파이프라인 구성

**Dependencies**: -

---

### Task 18: autopilot references 작성

**Component**: autopilot 메타스킬
**Priority**: P1-High
**Type**: Create

**Description**:
autopilot 스킬의 참조 문서를 작성한다:

1. **pipeline-templates.md**: 규모별 파이프라인 템플릿
   - 소규모: implementation → inline test
   - 중규모: feature-draft → impl-plan → impl → review → inline test → spec-sync
   - 대규모: full SDD pipeline (모든 agent)
   - 각 템플릿에 사용 에이전트, 순서, 예상 소요 시간, 중간 산출물 명시

2. **scale-assessment.md**: 규모 판단 가이드라인
   - 파일 수, 스펙 변경 여부, 새로운 컴포넌트 수 등 판단 기준 상세화
   - 경계 사례(edge case) 처리 지침
   - 테스트 전략 판단 기준 (iteration 시간 기반)

**Acceptance Criteria**:
- [ ] `references/pipeline-templates.md`가 생성됨
- [ ] 소/중/대 3가지 파이프라인 템플릿이 구체적으로 정의됨
- [ ] `references/scale-assessment.md`가 생성됨
- [ ] 규모 판단 기준이 수치적으로 명시됨

**Target Files**:
- [C] `.claude/skills/autopilot/references/pipeline-templates.md`
- [C] `.claude/skills/autopilot/references/scale-assessment.md`

**Technical Notes**:
- 토론에서 합의된 규모 기준을 기반으로 하되, 실제 프로젝트 적용을 위해 구체화
- 파이프라인 템플릿은 오케스트레이터 생성 시 직접 참조됨

**Dependencies**: 17

---

### Task 19: autopilot examples 작성

**Component**: autopilot 메타스킬
**Priority**: P1-High
**Type**: Create

**Description**:
autopilot 스킬의 예시 문서를 작성한다:

**sample-orchestrator.md**: autopilot이 생성하는 오케스트레이터의 실제 예시
- 중규모 기능(인증 시스템)에 대한 완성된 오케스트레이터 SKILL.md 예시
- 각 단계의 에이전트 호출, 조건 분기, 에러 핸들링, 마일스톤 로그가 포함된 실전 예시
- autopilot이 이 예시를 참조하여 오케스트레이터를 생성

**Acceptance Criteria**:
- [ ] `examples/sample-orchestrator.md`가 생성됨
- [ ] SKILL.md 표준 포맷을 준수하는 완성된 오케스트레이터 예시 포함
- [ ] 에이전트 호출 순서, review-fix 루프, 에러 핸들링이 모두 예시에 포함됨
- [ ] 마일스톤 텍스트 출력 및 로그 기록 예시 포함

**Target Files**:
- [C] `.claude/skills/autopilot/examples/sample-orchestrator.md`

**Technical Notes**:
- 이 예시가 autopilot의 오케스트레이터 생성 품질을 결정하므로 높은 완성도 필요
- SKILL.md 표준 포맷: frontmatter + Hard Rules + Process Steps + Output Format

**Dependencies**: 17

---

### Task 20: 파이프라인 로그 시스템 설계

**Component**: 파이프라인 로그 시스템
**Priority**: P1-High
**Type**: Modify

**Description**:
autopilot SKILL.md에 파이프라인 로그 시스템 설계를 추가한다. 이는 별도 코드가 아니라 autopilot 스킬의 프로세스 정의 내에 로그 기록 지시사항으로 포함된다.

로그 시스템 설계:
- **로그 파일 경로**: `_sdd/pipeline/log_<feature>_<timestamp>.md`
- **생성 시점**: autopilot Phase 2 시작 시 로그 파일 생성
- **기록 내용**: 각 에이전트 시작/완료, 마일스톤, 에러, review 결과
- **포맷**: 마크다운 체크리스트 형태

```markdown
# Pipeline Log: <feature-name>
**시작**: <timestamp>
**규모**: <소/중/대>
**파이프라인**: <agent1> → <agent2> → ...

## 실행 로그
- [x] feature-draft — 완료 (2m 30s) — `_sdd/drafts/feature_draft_xxx.md`
- [x] implementation-plan — 완료 (1m 45s) — `_sdd/implementation/plan_xxx.md`
- [ ] implementation — 진행 중...
```

**Acceptance Criteria**:
- [ ] autopilot SKILL.md에 로그 기록 절차가 추가됨
- [ ] 로그 파일 경로 규칙이 정의됨
- [ ] 로그 포맷이 마크다운으로 사람이 읽을 수 있음
- [ ] 에러 및 재시도 이력이 로그에 포함됨

**Target Files**:
- [M] `.claude/skills/autopilot/SKILL.md`

**Technical Notes**:
- 로그는 autopilot 스킬이 직접 Write/Edit으로 기록 (별도 시스템 불필요)
- 각 에이전트 호출 전후로 로그 업데이트 지시사항을 프로세스에 포함

**Dependencies**: 17

---

### Task 21: 통합 테스트 - 단일 스킬 에이전트 호출

**Component**: 통합 테스트
**Priority**: P1-High
**Type**: Test

**Description**:
에이전트 전환이 올바르게 작동하는지 단일 스킬 레벨에서 테스트한다:

1. **래퍼 → 에이전트 위임 테스트**: `/feature-draft`를 호출했을 때 래퍼가 feature-draft 에이전트에 올바르게 위임하는지 확인
2. **에이전트 독립 실행 테스트**: feature-draft 에이전트를 직접 Agent()로 호출했을 때 정상 동작하는지 확인
3. **서브에이전트 호출 테스트**: feature-draft 에이전트 내에서 write-phased 서브에이전트가 정상 호출되는지 확인
4. **references/examples 접근 테스트**: 에이전트가 기존 스킬 디렉토리의 참조 파일을 Read로 접근할 수 있는지 확인

**Acceptance Criteria**:
- [ ] 래퍼 스킬을 통한 에이전트 위임이 정상 동작
- [ ] 에이전트 직접 호출이 정상 동작
- [ ] 서브에이전트 호출(Agent 도구)이 정상 동작
- [ ] 에이전트가 references/ 및 examples/ 파일을 Read로 접근 가능

**Target Files**:
- (테스트 실행 — 파일 수정 없음)

**Technical Notes**:
- 8개 에이전트 중 대표적으로 feature-draft 하나를 상세 테스트
- 나머지 7개는 래퍼 → 에이전트 위임만 확인 (스모크 테스트)
- 인라인 디버깅으로 진행 (짧은 iteration)

**Dependencies**: 9-16 (모든 래퍼 전환 완료 후)

---

### Task 22: 통합 테스트 - autopilot end-to-end

**Component**: 통합 테스트
**Priority**: P2-Medium
**Type**: Test

**Description**:
autopilot 메타스킬의 end-to-end 동작을 테스트한다:

1. **소규모 시나리오**: 단순 버그 수정 요청 → 규모 판단(소) → 축소 파이프라인 생성 → 사용자 확인 → 자율 실행
2. **중규모 시나리오**: 4-10 파일 변경 기능 요청 → 규모 판단(중) → 표준 파이프라인 생성 → 사용자 확인 → 자율 실행
3. **오케스트레이터 품질 검증**: 생성된 오케스트레이터가 SKILL.md 포맷을 준수하는지 확인
4. **파이프라인 로그 검증**: `_sdd/pipeline/` 로그 파일이 올바르게 생성되고 기록되는지 확인
5. **에러 핸들링 검증**: 의도적 에러 상황에서 로그 + 재시도가 동작하는지 확인

**Acceptance Criteria**:
- [ ] 소규모 시나리오에서 축소 파이프라인이 올바르게 생성 및 실행됨
- [ ] 중규모 시나리오에서 표준 파이프라인이 올바르게 생성 및 실행됨
- [ ] 오케스트레이터가 SKILL.md 표준 포맷을 준수함
- [ ] `_sdd/pipeline/` 로그 파일이 생성되고 마일스톤이 기록됨

**Target Files**:
- (테스트 실행 — 파일 수정 없음, 테스트 산출물은 `_sdd/pipeline/`에 생성)

**Technical Notes**:
- 실제 프로젝트에서 테스트하므로 안전한 테스트 기능을 선정해야 함
- 대규모 시나리오는 시간/비용 이유로 이번 테스트에서 제외 가능
- 실패 시 autopilot SKILL.md 또는 references를 조정

**Dependencies**: 17-20 (autopilot 스킬 + 로그 시스템 완료 후)

---

## Parallel Execution Summary

| Phase | Total Tasks | Max Parallel | Sequential (conflicts) | 설명 |
|-------|-------------|--------------|----------------------|------|
| 1 (Agent 정의) | 8 | 8 | 0 | 모든 에이전트 독립적으로 생성 가능 |
| 2 (Wrapper 전환) | 8 | 8 | 0 | 각 스킬 독립적 (SKILL.md + skill.json), 단 Phase 1 의존 |
| 3 (Autopilot) | 3 | 2 | Task 17 먼저 | Task 18, 19는 17 완료 후 병렬 가능 |
| 4 (인프라+테스트) | 3 | 1 | 순차 | 20→21→22 순서 필요 |

> **총 태스크**: 22개
> **이론적 최소 실행 시간**: Phase 1 (1 round) + Phase 2 (1 round) + Phase 3 (2 rounds) + Phase 4 (3 rounds) = **7 rounds**
> **Phase 1-2는 독립적이지 않음**: Phase 2의 각 래퍼는 대응하는 Phase 1 에이전트에 의존하지만, Phase 1이 모두 병렬이므로 한 라운드에 완료되면 Phase 2도 바로 시작 가능

## Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| 에이전트 컨텍스트 윈도우 소진 | 대형 스킬(feature-draft, implementation)의 에이전트 정의가 너무 커서 실행 중 컨텍스트 부족 | Medium | references/examples는 Read로 참조하도록 결정됨. 에이전트 본문에는 SKILL.md 로직만 포함 |
| 서브에이전트 중첩 깊이 | autopilot → orchestrator → agent → sub-agent (write-phased) 최대 3-4단계 중첩 시 지연 | Low | 중첩 깊이 3단계 이하로 제한, 불필요한 중첩 회피 |
| 생성된 오케스트레이터 품질 | LLM이 생성하는 오케스트레이터의 에이전트 호출 순서나 조건 분기가 부정확할 수 있음 | Medium | sample-orchestrator.md 예시를 높은 완성도로 작성, Phase 1.5에서 사용자 검토 |
| 래퍼 전환 시 기존 기능 퇴행 | 래퍼 전환 과정에서 기존 스킬의 동작이 변경될 수 있음 | Low | 전환 후 단일 스킬 테스트(Task 21)로 검증, references/examples 유지 |
| Codex 스킬과의 드리프트 확대 | Claude Code만 에이전트 전환하면 `.codex/skills/`와의 차이가 확대됨 | Medium | **결정됨**: Codex는 기존 풀 SKILL.md 유지. Agent 도구 제한으로 래퍼 패턴 불가. Codex 동기화는 별도 후속 작업 |

## Open Questions (Resolved)

> 모든 Open Questions는 후속 토론 (`_sdd/discussion/discussion_autopilot_open_questions.md`)에서 해결됨.

| # | 질문 | 결정 |
|---|------|------|
| 1 | Codex 스킬 동기화 | **Codex는 기존 유지** — `.codex/skills/`는 풀 SKILL.md 유지. 에이전트 전환은 Claude Code 전용. Codex는 Agent 도구를 제한적으로 지원하므로 래퍼 패턴이 동일하게 동작하지 않음 |
| 2 | Agent 정의에 references/examples 포함 방식 | **Read로 참조** — 에이전트 본문에는 SKILL.md 로직만 포함. references/examples는 기존 `.claude/skills/<name>/references/` 경로에서 Read로 읽도록 지시 |
| 3 | 래퍼 스킬 버전 관리 | **Minor 버전 업** — 래퍼 전환 시 `1.0.0 → 1.1.0`. 기능 동일, 구조 변경 표시. skill.json도 함께 업데이트 |
| 4 | 오케스트레이터 생성 위치 | **`_sdd/pipeline/`에 저장** — 일회성 실행 계획이므로 `.claude/skills/`를 오염시키지 않음. 로그와 함께 관리. (**이전 토론 결정 #12 변경**) |
| 5 | 대규모 파이프라인 컨텍스트 관리 | **파일 기반 전달로 충분** — 부모(autopilot)는 각 에이전트에 파일 경로만 전달. 에이전트는 자체 컨텍스트에서 파일을 Read. 부모 컨텍스트 누적 최소화 |
| 6 | 파이프라인 실행 로그 (추가 논의) | **공유 로그 파일** — autopilot이 로그 파일을 생성하고, 각 에이전트 결과를 받을 때마다 핵심 결정사항을 추출하여 로그에 추가. 에이전트는 로그를 모름 |

## Model Recommendation

| Phase | 권장 모델 | 근거 |
|-------|----------|------|
| Phase 1: Agent 정의 생성 (Task 1-8) | **Sonnet** | 패턴 반복 작업. 기존 SKILL.md를 에이전트 포맷으로 변환하는 규칙적 작업이므로 높은 처리량이 중요 |
| Phase 2: Wrapper 전환 (Task 9-16) | **Sonnet** | write-phased 래퍼 패턴을 동일하게 8회 적용하는 반복 작업 |
| Phase 3: Autopilot 스킬 작성 (Task 17-19) | **Opus** | 복잡한 메타스킬 설계, 자연어 프롬프트 엔지니어링, 오케스트레이터 예시 작성에 높은 추론 능력 필요 |
| Phase 4: 인프라 + 테스트 (Task 20-22) | **Opus** | 로그 시스템 설계 + end-to-end 통합 테스트에 종합적 판단 필요 |
