---
name: spec-update-todo
description: This skill should be used when the user asks to "update spec with features", "add features to spec", "update spec from input", "add requirements to spec", "spec update", "expand spec", "add to-do to spec", "add to-implement to spec", or mentions adding new features, requirements, or planned improvements to an existing specification document.
version: 1.1.0
---

# Spec Update from Planned Input

Apply planned requirements into an existing exploration-first spec.

A good spec is not a copy of the code. It is a searchable map that helps people and LLMs:
- understand what the repository does
- find where a feature or responsibility lives
- decide where to edit safely
- remember non-obvious decisions and invariants

This skill updates `_sdd/spec/` with planned or to-implement items.
It does not implement code. It turns draft requirements into spec entries that help future readers understand:
- what is planned
- where the change affects the system
- which components or paths are involved
- what risks or unknowns remain

## Simplified Workflow

This skill sits between **feature-draft** and **implementation** in the SDD workflow:

```
spec-create -> feature-draft -> spec-update-todo (this) -> implementation -> spec-update-done
```

| Step | Skill | Purpose |
|------|-------|---------|
| 1 | spec-create | Create the initial index-first spec |
| 2 | feature-draft | Draft feature spec patch + implementation plan |
| **3** | **spec-update-todo** | Apply planned items into the spec |
| 4 | implementation | Execute the implementation plan |
| 5 | spec-update-done | Sync spec with actual code |

## Overview

Input can come from:
1. **User conversation**: Direct discussion about new features
2. **Input file**: `_sdd/spec/user_spec.md` or `_sdd/spec/user_draft.md`
3. **Part 1 of a `feature-draft` output**
4. **Decision log**: `_sdd/spec/DECISION_LOG.md` as supporting rationale

After processing input files, rename them with `_processed_`.

## When to Use This Skill

- Adding planned features to an existing spec
- Reflecting feature-draft output into `_sdd/spec/`
- Expanding roadmap or to-implement sections in a structured spec
- Updating component, flow, environment, or change-path documentation before implementation

## Hard Rules

1. **Always backup**: 수정 전 반드시 `_sdd/spec/prev/PREV_<filename>_<timestamp>.md`로 백업한다.
2. **Rename processed input files**: 처리한 입력 파일은 `_processed_` 접두사로 이름 변경한다.
3. **한국어 작성**: 추가 내용은 메인 스펙 언어를 따르되 기본은 한국어다.
4. **DECISION_LOG.md 최소화**: 결정 로그는 `DECISION_LOG.md`에만 기록한다.
5. **탐색형 구조 보존**: 업데이트 후에도 Change Recipes, Component Index, 실제 경로 참조가 유효해야 한다.
6. **앵커 섹션 유지**: `Goal`, `Architecture Overview`, `Component Details`, `Environment & Dependencies`, `Identified Issues & Improvements`, `Usage Examples`, `Open Questions` 섹션명을 유지한다.
7. **추정 명시**: 확인되지 않은 내용은 단정하지 않고 `Open Questions`에 기록한다.
8. **갱신 필요성 판단**: SDD §8 기준에 따라 `MUST update` / `NO update` / `CONSIDER`를 분류한다.
9. **책임 기반 분할 우선**: 분할이 필요하면 `main.md + <component>.md` 형태를 기본으로 한다.
10. **메타데이터 강제 금지**: version/date/changelog는 기존 문서가 이미 그 메타데이터를 사용할 때만 갱신한다.
11. **선택 섹션 최소화**: `Environment & Dependencies`, `Identified Issues & Improvements`, `Usage Examples` 등 선택 섹션은 실제 영향이 있을 때만 추가하거나 수정한다.
12. **빈 선택 섹션 금지**: 비어 있는 선택 섹션, 메타데이터 블록, placeholder 표는 만들지 않는다.
13. **Token-efficient update**: 반복 설명보다 기존 표, 경로 인덱스, 짧은 불릿 갱신을 우선한다.

## SDD §8 갱신 기준 참조

모든 코드 변경이 스펙 갱신을 요구하는 것은 아니다. 입력 항목을 아래 기준으로 분류한다.

| 분류 | 조건 | 예시 |
|------|------|------|
| **MUST update** | 사용자 가시 기능/범위 변경, 새/변경된 런타임 흐름·소유권·계약·경로, 새 환경/셋업 요구사항, 지속적 리스크·불변 조건·미해결 질문 | 컴포넌트 추가/삭제, API 엔드포인트 변경, 아키텍처 구조 변경, 환경변수 추가 |
| **NO update** | 테스트만, 주석만, 포맷팅만, 외부 동작·탐색 지점 불변인 내부 리팩터링 | 함수 내부 로직 개선, 버그 수정(계약 불변), 코드 스타일 수정 |
| **CONSIDER** | 소규모 의존성 변경, 탐색 영향이 애매한 내부 재구성, 성능 튜닝(외부 영향 제한) | 내부 유틸 추가(공유 시 갱신), 에러 핸들링 변경(외부 노출 시 갱신), 메이저 의존성 업데이트 |

## Input Sources

### 1. User Conversation
- feature descriptions
- requirement discussions
- improvement requests
- bug reports to record as planned work

### 2. Input Files
- `_sdd/spec/user_spec.md`
- `_sdd/spec/user_draft.md`

### 3. Decision Log
- `_sdd/spec/DECISION_LOG.md` when previous decisions constrain the planned change

## Update Process

### Step 1: Identify Input Source

**Tools**: `Glob`, `Read`

Load all applicable sources in this order:
1. conversation
2. `user_draft.md`
3. `user_spec.md`

If multiple sources exist, merge them and preserve conflicts or ambiguity in `Open Questions`.

### Step 2: Load Current Spec

**Tools**: `Read`, `Glob`, `Grep`

Treat the spec as a navigation surface.

Read:
- the main spec (`_sdd/spec/<project>.md` or `_sdd/spec/main.md`)
- linked component spec files that will be affected
- `_sdd/spec/DECISION_LOG.md` if present

Prioritize these target areas (앵커 섹션):
- `Goal > Project Snapshot / Key Features / Non-Goals`
- `Architecture Overview > System Boundary / Repository Map / Runtime Map`
- `Component Details > Component Index`
- `Environment & Dependencies`
- `Identified Issues & Improvements`
- `Usage Examples > Common Operations / Common Change Paths`
- `Open Questions`

If the spec lacks these anchors and the change is still local, add missing subsections minimally.
If the spec shape is fundamentally poor, continue with minimal safe updates and note a `spec-rewrite` follow-up in `Open Questions`.

### Step 3: Parse Input

**Tools**: `Read`

Accepted input structure is defined in `references/input-format.md`.

Supported sections:
- `New Features`
- `Improvements`
- `Bug Reports`
- `Component Changes`
- `Environment & Dependency Changes`
- `Notes`
- `Open Questions`

Extract:
- feature name and priority
- spec update classification if provided
- target section hints
- affected components / paths
- acceptance criteria
- risks / invariants
- dependencies and constraints

### Step 4: Classify Whether Spec Edits Are Needed

**Tools**: none

Apply SDD §8 갱신 기준:

- `MUST update`
  - user-visible feature or scope change
  - new or changed runtime flow, ownership, contract, or repository path that affects navigation
  - new environment/setup requirement that affects running or testing
  - new enduring risk, invariant, or unresolved question worth preserving
- `NO update`
  - tests-only, comments-only, formatting-only changes
  - internal refactors that do not change behavior, navigation, contracts, or maintenance entry points
- `CONSIDER`
  - minor dependency bumps
  - internal reorganizations with unclear navigation impact
  - performance tuning with limited user-visible impact

If the input already includes `Spec Update Classification`, verify it against the above rules.
If the correct classification is `NO update`, prepare a no-op summary and skip spec edits.

### Step 5: Categorize and Map Updates

**Tools**: none

Apply the mapping rules from `references/section-mapping.md`.

Default mapping (앵커 섹션 기준):

| Input Type | Preferred Target Section | Update Type |
|------------|--------------------------|-------------|
| New Feature (Core) | `Goal > Key Features` | Add to list |
| New Feature (Component) | `Component Details` | Add component entry |
| Architecture Change | `Architecture Overview` | Update structure |
| Improvement | `Identified Issues & Improvements` | Add with priority |
| Bug Fix | `Identified Issues & Improvements` | Add to issues |
| Component Change | `Component Details` | Update/add section |
| Behavior / Design Intent Change | `Component Spec > Overview` | Update overview |
| Environment/Config | `Environment & Dependencies` | Add options |
| Usage/Change Path | `Usage Examples > Common Change Paths` | Add recipe |
| Uncertainty | `Open Questions` | Add question |

Important rule:
one input item may require updates in **multiple** spec areas.

Example:
- a new feature may require `Goal > Key Features`
- plus `Architecture Overview > Runtime Map`
- plus `Component Details`
- plus `Usage Examples > Common Change Paths`

### Step 6: Generate Update Plan

**Tools**: deterministic defaults (non-interactive)

Before editing, present a concise update plan:

~~~markdown
## Spec Update Plan

**Target Files**:
- `_sdd/spec/main.md`
- `_sdd/spec/notification.md`

**Spec Update Classification**: MUST update

### Planned Changes
- Goal > Key Features: ADD `실시간 알림`
- Architecture Overview > Runtime Map: UPDATE 알림 이벤트 흐름
- Component Details: ADD `NotificationService`
- Usage Examples > Common Change Paths: ADD 알림 관련 변경 시작점
- Open Questions: ADD 이메일 알림 범위 미정
~~~

If classification is `NO update`, present a compact no-op plan instead.

### Step 7: Apply Updates

**Tools**: `Edit`, `Write`, `Bash (mkdir -p)`

Apply planned changes directly to the relevant spec files.

Rules:
1. create a `prev/PREV_...` backup for every modified file
2. preserve existing accurate content
3. if classification is `NO update`, skip spec edits and report why
4. add planned markers such as `📋 계획됨` only where they improve clarity
5. update multiple sections when one feature affects multiple views of the system
6. add or refresh `Component Index`, `Runtime Map`, or `Common Change Paths` when needed for planned changes
7. add or update optional sections only when they materially help future navigation
8. add/merge `Open Questions` for unresolved assumptions
9. update `DECISION_LOG.md` only if the planned direction introduces a meaningful decision
10. update version/date/changelog only if the current spec already uses them

#### New Component Template

When adding a new component, use the SDD component spec structure:

~~~markdown
### 컴포넌트: [이름]
#### Overview
[이 컴포넌트의 동작 방식과 설계 의도]

#### Responsibility
[이 컴포넌트가 하는 일과 하지 않는 일]

#### Owned Paths
- `src/path/to/component/`
- `tests/path/to/component/`

#### Key Symbols / Entry Points
- `ClassName.method()` — 설명

#### Interfaces / Contracts
- Inputs: [입력 설명]
- Outputs: [출력 설명]
- 불변 조건: [깨지면 안 되는 조건]

#### Dependencies
- upstream: [의존하는 컴포넌트]
- downstream: [이 컴포넌트에 의존하는 것]

#### Change Recipes
- [변경 유형]: [시작 파일] → [검증 방법]
~~~

#### Post-Update Navigation Validation

업데이트 적용 후 다음을 검증한다:
- Change Recipes가 업데이트 후에도 유효한가?
- Component Index가 새 컴포넌트를 반영하는가?
- 스펙에 기재된 파일 경로가 실제로 존재하는가?

If the updated content grows too large:
- prefer splitting by responsibility (`auth.md`, `jobs.md`, `billing.md`)
- keep the main spec as the entry point
- record the file map in `Open Questions` if the split is non-obvious

### Step 7.5: Quality Gate (LLM-as-Judge)

업데이트 적용 후, 스펙이 본래 목적을 달성하는지 자체 평가한다.
이 단계는 **판정만** 수행한다. FAIL 시 보강은 이전 작성 단계(Step 7)로 돌아가 수행한다.

**spec-update-todo 특화 적용**:
- **스코프**: 이번에 새로 추가된 계획 항목만 평가 대상이다. 기존 스펙의 레거시 결함은 대상이 아니다.
- 이번 변경 범위와 직접 무관해 판단 근거가 부족한 criterion은 `WEAK`로 기록하고 `FAIL`로 간주하지 않는다.
- Criterion 2(기능 위치 탐색), 3(안전한 수정 판단) 중심으로 검증
- Criterion 1(저장소 이해), 4(비자명한 결정 기억)는 기존 스펙 품질에 의존하므로 WEAK까지 허용

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

1. 업데이트된 스펙에서 **이번에 추가/수정된 계획 항목**을 다시 읽는다
2. 각 criterion에 대해 **이번 추가분 중심**으로 probe 질문을 시도한다
   - Criterion 1: 이번 추가로 Goal > Key Features가 변경되었다면 목적·비목표가 여전히 명확한지 확인
   - Criterion 2: 이번에 추가된 계획 항목 중 1개를 골라 소유 경로/컴포넌트가 명시되었는지 찾는다
   - Criterion 3: 이번에 추가된 항목과 관련된 변경 시나리오로 변경 가이드를 찾는다
   - Criterion 4: 이번 추가에서 새로 발생한 결정/불확실성이 기록되었는지 확인
3. 각 criterion을 PASS / WEAK / FAIL로 판정한다
4. 결과에 따라 행동한다:

| 결과 | 행동 |
|------|------|
| ALL PASS | 검증 통과, 다음 단계 진행 |
| WEAK만 존재 (FAIL 없음) | 개선 포인트를 사용자에게 알리되 진행 허용 |
| FAIL 1개 이상 | FAIL 항목과 근거를 기록 → Step 7로 돌아가 해당 부분만 보강 → 이 단계를 재실행 (최대 1회) |
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

### Step 8: Process Input Files

**Tools**: `Bash (mv)`

Rename processed files:
- `_sdd/spec/user_draft.md` -> `_sdd/spec/_processed_user_draft.md`
- `_sdd/spec/user_spec.md` -> `_sdd/spec/_processed_user_spec.md`

Add processing metadata:

~~~markdown
<!-- Processed: YYYY-MM-DD -->
<!-- Applied by: spec-update-todo -->
<!-- Target Spec: main.md -->
~~~

## Output Summary

After updating, summarize:
- spec update classification
- updated files
- changed sections
- planned items added
- whether `DECISION_LOG.md` changed
- processed input file status
- remaining `Open Questions`

## Context Management

| 스펙 크기 | 전략 |
|-----------|------|
| < 200줄 | 전체 읽기 |
| 200-500줄 | 전체 읽기 가능 |
| 500-1000줄 | TOC 먼저, 관련 섹션만 읽기 |
| > 1000줄 | 인덱스와 타겟 섹션 우선 |

## Error Handling

| Situation | Action |
|-----------|--------|
| Spec file not found | `spec-create` 먼저 실행 권장 |
| Ambiguous input | deterministic defaults + `Open Questions` 기록 |
| Conflicting requirements | 더 보수적인 해석 적용 후 `Open Questions` 기록 |
| Backup dir missing | `mkdir -p _sdd/spec/prev/` |
| Spec structure poor | 최소 안전 업데이트 후 `spec-rewrite` follow-up 기록 |
| Split needed | 책임 기반 분할로 전환 |

## Additional Resources

### Reference Files
- `references/input-format.md` - accepted input shape and MUST/NO/CONSIDER classification guide
- `references/section-mapping.md` - how planned items map into SDD anchor sections

### Example Files
- `examples/user_spec.md` - example input file
- `examples/update-summary.md` - example completion summary

## Integration with Other Skills

```
spec-create -> feature-draft -> spec-update-todo -> implementation -> spec-update-done
```

- `spec-create`: creates the initial index-first spec
- `feature-draft`: produces Part 1 that this skill can consume
- `implementation`: executes planned work after this step
- `spec-update-done`: syncs actual implementation back after completion
