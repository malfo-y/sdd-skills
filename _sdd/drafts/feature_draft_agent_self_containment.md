# Feature Draft: Agent Self-Containment (에이전트 자급자족 리팩토링)

**날짜**: 2026-03-19
**요청 배경**: Agent wrapper 스킬 구조에서, agent가 skill의 references/examples 파일에 접근 불가능한 문제 발견. Plugin 설치 환경에서도 마찬가지. 이 기회에 agent 파일 자체도 SDD 철학에 맞게 간결하게 재작성한다.

---

<!-- spec-update-todo-input-start -->

# Part 1: Spec Patch Draft

> 이 패치는 해당 스펙 섹션에 직접 복사-붙여넣기하거나,
> `spec-update-todo` 스킬의 입력으로 사용할 수 있습니다.

## Spec Update Input

**Date**: 2026-03-19
**Author**: feature-draft
**Target Spec**: `_sdd/spec/main.md`
**Spec Update Classification**: SHOULD update

## Background & Motivation Updates

### Background Update: Agent Self-Containment 원칙 + AC-First 재작성

**Priority**: High
**Target Section**: `_sdd/spec/main.md` > Architecture / Agent Layer

**Current State**:
현재 9개 agent가 `.claude/agents/*.md`에 정의되어 있고, 대응하는 wrapper skill이 `.claude/skills/*/SKILL.md`에 있다. 두 가지 문제가 있다:

1. **외부 참조 불가**: 5개 agent가 skill 디렉토리의 `references/`를 명시적으로 참조하지만, subagent로 실행 시 해당 파일에 접근 불가. Plugin 환경에서도 동일.
2. **Agent 비대화**: 5개 agent가 448~678줄로 비대. 장황한 설명, 중복된 Context Management 테이블, NICE-TO-HAVE 섹션(Best Practices, Automation Patterns 등)이 핵심 로직을 묻고 있음.

**Proposed**:
Agent 파일을 SDD 철학에 맞게 전면 재작성한다:

1. **AC-First**: 각 agent의 목표에 맞는 Acceptance Criteria를 먼저 정의하고, 이를 만족시키는 최소 구조로 작성
2. **Self-Contained**: Reference 핵심 로직을 정제하여 인라인 (원본 대비 70%+ 압축)
3. **Concise**: 장황한 설명 → 테이블/체크리스트, 중복 제거, NICE-TO-HAVE 섹션 삭제
4. **핵심 보존**: Hard Rules, Decision Gates, 출력 형식 등 핵심 요소는 유지

**Reason**:
1. Agent가 subagent로 호출 시 skill의 references/ 경로에 접근 불가
2. Plugin으로 다른 프로젝트에 설치 시 상대경로 해석 실패
3. 5/9 agent가 핵심 로직이 reference에 있어 사실상 제대로 동작 못함
4. 비대한 agent 파일이 LLM의 컨텍스트 윈도우를 불필요하게 소비

## Improvement Changes

### Improvement: Agent 전면 재작성 (AC-First + Self-Contained)

**Priority**: High

#### 현재 상태 vs 목표

| Agent | 현재 줄수 | 목표 줄수 | 감축률 | 외부 참조 | 주요 bloat |
|-------|----------|----------|--------|----------|-----------|
| implementation | 664 | ~310 | 53% | 3개 (parallel-exec, review-checklist, best-practices) | Step 3-4 pseudo-code, TDD 장문 설명, Best Practices |
| feature-draft | 678 | ~350 | 48% | 4개 (output-format, target-files, adaptive-q, tool-gates) | Step 5 형식 템플릿, Step 6 plan 형식 중복, Best Practices |
| spec-update-done | 486 | ~300 | 38% | 2개 (drift-patterns, update-strategies) | 출력 형식 3중 템플릿, Automation Patterns, Best Practices |
| implementation-plan | 448 | ~310 | 31% | 2개 (target-files, advanced-patterns) | Phase 전략 설명, 형식+위임 섹션, Context Mgmt 중복 |
| ralph-loop-init | 384 | ~260 | 32% | 3개 (ralph-concept, run.sh.example, state.md.example) | Step 0-1 장문 설명, Step 3 예시 과다, Context Mgmt 중복 |
| **합계** | **2,660** | **~1,530** | **42%** | **14개** | |

#### 재작성 원칙

1. **AC-First 구조**: 각 agent 파일을 아래 구조로 통일
   ```
   ---
   frontmatter (name, description, tools)
   ---
   # [Agent Name]
   ## Goal (1-2문장)
   ## Acceptance Criteria (체크리스트)
   ## Hard Rules
   ## Process (Steps — 테이블/체크리스트 위주)
   ## Output Format (간결한 템플릿)
   ```

2. **제거 대상 (5개 agent 공통)**
   - `Best Practices` 섹션 → 삭제 (agent가 판단할 사항)
   - `Context Management` 테이블 → 삭제 (4개 agent에 중복)
   - `Integration with Other Skills` → 삭제 (wrapper skill에서 관리)
   - `Additional Resources` → 삭제 (접근 불가한 references 링크)
   - `When to Use` → 삭제 (description에 이미 있음)
   - 장황한 prose 설명 → Decision Gate 테이블로 압축

3. **인라인 대상 (CORE reference만)**

   | Reference 파일 | 원본 | 인라인 목표 | 방법 |
   |---------------|------|-----------|------|
   | target-files-spec.md | 163줄 | ~20줄 | 마커 정의 + 충돌 규칙 (3개 agent 공통) |
   | drift-patterns.md | 446줄 | ~30줄 | 9패턴 테이블 (감지기준+해결방향) |
   | output-format.md | 561줄 | ~80줄 | Part1+Part2 필수 구조만 |
   | parallel-execution.md | 361줄 | ~25줄 | 충돌 매트릭스 + 의미적 충돌 5가지 |
   | ralph-loop-concept.md | ~100줄 | ~30줄 | 상태 머신 + 전환 규칙 |
   | run.sh.example | ~50줄 | ~50줄 | 전문 인라인 (템플릿 충실도 필수) |
   | state.md.example | 8줄 | 8줄 | 전문 인라인 |

4. **생략 대상 (NICE-TO-HAVE reference)**
   - update-strategies.md (361줄) — 기본 로직 이미 agent에 존재
   - adaptive-questions.md (181줄) — 기본 로직 이미 agent에 존재
   - tool-and-gates.md (170줄) — 도구 선택은 LLM 판단 영역
   - review-checklist.md (170줄) — 보조 자료
   - best-practices.md (416줄) — 보조 자료
   - advanced-patterns.md (248줄) — 복잡 프로젝트용 보조 자료

#### Acceptance Criteria (전체)

- [ ] AC1: 5개 agent가 AC-First 구조 (Goal → AC → Hard Rules → Process → Output Format)를 따름
- [ ] AC2: 5개 agent 파일에서 `references/` 또는 `examples/` 필수 참조 구문이 없음 (있어도 "optional")
- [ ] AC3: 각 agent가 reference 없이 단독 실행 시 핵심 출력물을 정상 생성
  - ralph-loop-init: ralph/ 디렉토리 5개 파일 생성, 상태 머신 정상 전환
  - spec-update-done: 9가지 드리프트 패턴 감지 및 분류
  - feature-draft: Part 1 (spec patch) + Part 2 (impl plan with Target Files) 생성
  - implementation: Target Files 기반 병렬 그룹핑 및 충돌 감지
  - implementation-plan: Target Files 포함 plan 생성
- [ ] AC4: 5개 agent 전체 합계 줄수가 현재 2,660줄에서 1,700줄 이하로 감축 (36%+)
- [ ] AC5: 기존 wrapper skill 및 다른 agent에서의 호출이 깨지지 않음
- [ ] AC6: 변경하지 않는 4개 agent (write-phased, implementation-review, spec-review, spec-update-todo)는 영향 없음

<!-- spec-update-todo-input-end -->

---

# Part 2: Implementation Plan

## Overview

| Item | Detail |
|------|--------|
| 대상 | `.claude/agents/` 하위 5개 agent 파일 |
| 작업 유형 | AC-First 전면 재작성 + Reference 핵심 인라인 |
| 총 태스크 | 5개 (agent당 1태스크, 각 태스크 내에서 reference 인라인 포함) |
| 예상 변경 규모 | 현재 2,660줄 → ~1,530줄 (42% 감축) |

## 재작성 공통 가이드

### AC-First Agent 구조 (모든 agent 공통)

```
---
frontmatter (name, description, tools, model)
---
# [Agent Name]
[1-2문장 Goal]

## Acceptance Criteria
- [ ] AC1: ...
- [ ] AC2: ...

## Hard Rules
1. ...

## Process
### Step 1: ...
### Step 2: ...

## Output Format
[간결한 템플릿]
```

### 공통 제거 대상

모든 agent에서 아래 섹션을 삭제한다:
- `Best Practices` — agent가 판단할 사항
- `Context Management` 테이블 — 4개 agent에 중복, LLM 판단 영역
- `Integration with Other Skills` — wrapper skill에서 관리
- `Additional Resources` / `References` — 접근 불가한 링크
- `When to Use This Skill` — description에 이미 있음
- `Automation Patterns` — 보조 자료

### 공통 인라인: Target Files 규격 (~20줄)

feature-draft, implementation, implementation-plan 3개 agent에 아래 블록을 인라인:

```markdown
### Target Files 규격
- 모든 태스크에 `**Target Files**:` 필드 필수
- 마커: `[C]` 생성, `[M]` 수정, `[D]` 삭제
- 형식: `- [마커] relative/path/to/file.ext`
- 충돌 규칙: 동일 파일에 같은 마커 → 같은 그룹(순차), 다른 마커 → 병렬 가능
- 읽기 전용 참조는 Target Files에 포함하지 않음
```

## 태스크 (전체 병렬 가능 — 파일 간 의존 없음)

### Task 1: ralph-loop-init 재작성

**Target Files**:
- [M] `.claude/agents/ralph-loop-init.md`

**현재**: 384줄 → **목표**: ~260줄

**Goal**: 대상 프로젝트의 장기 실행 프로세스를 위한 ralph/ 디렉토리를 생성한다.

**Agent AC**:
- [ ] ralph/ 디렉토리에 5개 파일 생성 (config.sh, PROMPT.md, run.sh, state.md, CHECKS.md)
- [ ] 상태 머신이 SETUP → SMOKE_TEST → 실행 → 분석 → DONE 으로 정상 전환
- [ ] run.sh가 while-loop + LLM 진단 패턴을 정확히 구현

**재작성 방향**:
| 영역 | 현재 | 변경 |
|------|------|------|
| Step 0-1 장문 설명 | 60줄 prose | ~20줄 체크리스트 |
| Step 3 config 예시 | 3개 예시 (25줄) | 1개 예시 (8줄) |
| ralph-loop-concept.md 참조 | Glob으로 외부 파일 탐색 | 상태 머신 테이블 + 전환 규칙 ~30줄 인라인 |
| run.sh.example 참조 | Glob으로 외부 파일 탐색 | 템플릿 전문 ~50줄 인라인 |
| state.md.example 참조 | Glob으로 외부 파일 탐색 | 8줄 인라인 |
| Context Management | 중복 테이블 | 삭제 |

### Task 2: spec-update-done 재작성

**Target Files**:
- [M] `.claude/agents/spec-update-done.md`

**현재**: 486줄 → **목표**: ~300줄

**Goal**: 코드 변경사항을 스펙에 반영하고, 드리프트를 감지하여 스펙을 동기화한다.

**Agent AC**:
- [ ] 코드/로그에서 9가지 드리프트 패턴을 감지 및 분류
- [ ] Change Report 테이블 생성 후 스펙에 업데이트 적용
- [ ] 구현 산출물을 feature별로 아카이브 (`_sdd/implementation/features/`)

**재작성 방향**:
| 영역 | 현재 | 변경 |
|------|------|------|
| drift-patterns.md 참조 | `Read로 읽는다` (접근 불가) | 9패턴 테이블 ~30줄 인라인 |
| Output Format 3중 템플릿 | 89줄 | 1개 템플릿 ~25줄 |
| Automation Patterns | 34줄 | 삭제 |
| Best Practices | 27줄 | 삭제 |
| Input Sources 장문 | 47줄 | ~15줄 테이블 |

### Task 3: feature-draft 재작성

**Target Files**:
- [M] `.claude/agents/feature-draft.md`

**현재**: 678줄 → **목표**: ~350줄

**Goal**: 사용자 요구사항으로부터 spec patch draft (Part 1) + implementation plan (Part 2)을 한 번에 생성한다.

**Agent AC**:
- [ ] Part 1: spec-update-todo 호환 형식의 spec patch 생성
- [ ] Part 2: Target Files가 포함된 implementation plan 생성
- [ ] `_sdd/drafts/feature_draft_<name>.md`에 저장

**재작성 방향**:
| 영역 | 현재 | 변경 |
|------|------|------|
| output-format.md 참조 | 외부 561줄 파일 참조 | Part1+Part2 필수 구조 ~80줄 인라인 |
| target-files-spec.md 참조 | 외부 파일 참조 | 공통 Target Files 규격 ~20줄 인라인 |
| Step 5 형식 템플릿 | 137줄 verbose | ~50줄 간결 템플릿 |
| Step 2 Context Gathering | Step 1과 중복 | 병합 |
| Best Practices / File Mgmt | 39줄 | 삭제 |
| adaptive-questions.md | 외부 참조 | 삭제 (기본 로직 agent에 이미 존재) |
| tool-and-gates.md | 외부 참조 | 삭제 (LLM 판단 영역) |

### Task 4: implementation 재작성

**Target Files**:
- [M] `.claude/agents/implementation.md`

**현재**: 664줄 → **목표**: ~310줄

**Goal**: Implementation plan을 TDD 방식으로 병렬 실행한다.

**Agent AC**:
- [ ] Plan에서 태스크를 파싱하고 Target Files 기반 병렬 그룹 생성
- [ ] 충돌 감지 (파일 충돌 + 의미적 충돌) 정상 동작
- [ ] Phase별 실행 → 검증 → 리뷰 사이클 완료
- [ ] `IMPLEMENTATION_REPORT.md` 생성

**재작성 방향**:
| 영역 | 현재 | 변경 |
|------|------|------|
| parallel-execution.md 참조 | 외부 361줄 파일 참조 | 충돌 매트릭스 + 의미적 충돌 5가지 ~25줄 인라인 |
| target-files-spec.md 참조 | 외부 파일 참조 | 공통 Target Files 규격 ~20줄 인라인 |
| TDD 설명 (Core Principle) | 17줄 flowchart + prose | 1문장: "각 AC에 대해 Red-Green-Refactor" |
| Step 3 pseudo-code | 96줄 | ~40줄 (Decision Gate 테이블) |
| Step 4 Sub-Agent Prompt | 102줄 | ~40줄 (핵심 필드만) |
| TDD Guidelines | 98줄 | 삭제 (Best Practices 성격) |
| Best Practices / Common Situations | 47줄 | 삭제 |

### Task 5: implementation-plan 재작성

**Target Files**:
- [M] `.claude/agents/implementation-plan.md`

**현재**: 448줄 → **목표**: ~310줄

**Goal**: 스펙으로부터 Target Files가 포함된 단계별 구현 계획을 생성한다.

**Agent AC**:
- [ ] 스펙 분석 → 컴포넌트 식별 → 태스크 정의 (Target Files 필수)
- [ ] Phase 분해 (MVP-First / Risk-First / Dependency-Driven 자동 선택)
- [ ] `IMPLEMENTATION_PLAN.md` 또는 phase-split 파일 생성

**재작성 방향**:
| 영역 | 현재 | 변경 |
|------|------|------|
| target-files-spec.md 참조 | 외부 파일 참조 | 공통 Target Files 규격 ~20줄 인라인 |
| Step 4 Phase 전략 설명 | 74줄 verbose | ~35줄 (전략 선택 테이블) |
| Step 6 형식+위임 | 93줄 | ~40줄 (간결 템플릿) |
| Context Management | 중복 테이블 | 삭제 |
| Best Practices / Progressive Disclosure | 33줄 | 삭제 |
| advanced-patterns.md | 외부 참조 | 삭제 (기본 전략 agent에 이미 존재) |

## Parallel Execution Summary

```
Phase 1: [Task 1] [Task 2] [Task 3] [Task 4] [Task 5]  ← 전체 병렬 (파일 간 의존 없음)
```

## 변경하지 않는 파일

- `.claude/agents/write-phased.md` — 외부 참조 없음, 이미 간결
- `.claude/agents/implementation-review.md` — 외부 참조 없음
- `.claude/agents/spec-review.md` — fallback 로직 있음
- `.claude/agents/spec-update-todo.md` — fallback 로직 있음
- `.claude/skills/*/references/*` — 삭제하지 않음 (skill 직접 사용 시 보조 자료로 유지)
- `.claude/skills/*/SKILL.md` — wrapper 구조 유지

## Next Steps

1. 이 draft를 리뷰하고 승인
2. `/implementation` 으로 5개 태스크 병렬 실행
3. 완료 후 각 agent의 AC 수동 검증
4. `/spec-update-done` 으로 스펙 동기화
