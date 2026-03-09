---
name: spec-rewrite
description: This skill should be used when the user asks to "rewrite spec", "refactor spec", "simplify spec", "split spec into files", "clean up spec", or equivalent phrases indicating they want to reorganize an overly long or hard-to-navigate spec into an exploration-first, change-oriented structure.
version: 1.1.0
---

# Spec Rewrite - Rebuild Specs for Fast Understanding and Safe Change

Rewrite existing spec documents into an exploration-first structure.

A good spec is not a copy of the code. It is a searchable map that helps people and LLMs:
- understand what the repository does quickly
- find where a feature or responsibility lives
- identify where to edit safely
- preserve non-obvious decisions and invariants
- separate unknowns explicitly

This skill does not exist merely to shorten or prettify documents.
Its purpose is to turn a hard-to-navigate spec into a **탐색형 지도** that makes understanding and change fast.

## Simplified Workflow

This skill is a **maintenance utility** that can be invoked at any point:

```
spec-create -> feature-draft -> implementation -> spec-update-done
                                                       ↑
                                              spec-rewrite (anytime)
```

| Step | Skill | Purpose |
|------|-------|---------|
| 1 | spec-create | Create the initial index-first spec |
| 2 | feature-draft | Draft feature spec patch + implementation plan |
| 3 | implementation | Execute the implementation plan (TDD) |
| 4 | spec-update-done | Sync spec with actual code |
| **—** | **spec-rewrite** | **Rebuild spec as exploration-first map** |

## Overview

This skill treats `_sdd/spec/` as a navigation and maintenance surface.

Primary goals:
1. Rebuild the main spec as a fast entry point
2. Restore or create repository and component maps
3. Make change paths, contracts, and invariants visible
4. Split by responsibility when one file is too dense
5. Preserve rationale in `DECISION_LOG.md`
6. Move uncertainty into `Open Questions`

## When to Use This Skill

- The spec is too long, noisy, or hard to scan
- Main ideas are buried under logs, history, or duplicated detail
- A reader cannot quickly find where a feature lives or where to edit
- The main spec should become an index plus focused component docs
- The spec needs cleanup before feature planning or implementation work

## Hard Rules

1. **Always backup**: 수정 전 반드시 `_sdd/spec/prev/PREV_<filename>_<timestamp>.md`로 백업한다.
2. **호환 가능한 앵커 섹션 보존**: `Goal`, `Architecture Overview`, `Component Details`, `Environment & Dependencies`, `Identified Issues & Improvements`, `Usage Examples`, `Open Questions` 섹션명을 유지한다. 내부 구조는 탐색형으로 재구성한다.
3. **탐색 우선**: 리라이트 결과는 프로젝트 이해와 변경 탐색을 더 쉽게 만들어야 한다.
4. **실제 경로 우선**: 주요 컴포넌트, 변경 지점, 검증 지점에는 실제 파일/디렉토리 경로 또는 핵심 심볼을 포함한다.
5. **요약 우선**: 코드를 그대로 복사하지 말고 의도, 경계, 계약, 변경 지점, 불변 조건을 압축해서 정리한다.
6. **변경 지향성 유지**: 메인 스펙 또는 컴포넌트 스펙에는 Change Recipes 또는 변경 가이드 성격의 정보가 포함되어야 한다.
7. **Preserve decision context**: 삭제하거나 축약하는 과정에서 중요한 "why" 컨텍스트가 사라지면 `DECISION_LOG.md`에 보존한다.
8. **추정 명시**: 확인되지 않은 내용은 단정하지 않고 `Open Questions`에 기록한다.
9. **탐색형 구조 강화**: 리라이트 결과는 탐색 가능한 지도(Change Recipes, Component Index, 실제 경로)를 반드시 포함해야 한다.
10. **한국어 작성**: 수정 내용은 한국어로 작성한다. 기존 문서가 다른 언어라면 메인 문서 언어에 맞추되, 혼재 시 하나로 정리하고 근거가 약하면 `Open Questions`에 남긴다.
11. **최소 산출물**: `DECISION_LOG.md` 외 추가 거버넌스 문서는 사용자 요청 시에만 생성한다.
12. **분할 기본값**: 번호형 토픽 분할보다 책임 기반 분할(`main.md + auth.md + jobs.md`)을 기본으로 한다. 기존 구조가 이미 일관되면 최소 수정으로 유지한다.
13. **LLM 효율 유지**: 리라이트 결과는 한 번에 읽기 쉬운 길이와 밀도를 목표로 하며, 중복 서술보다 표, 경로, 링크를 우선한다.

## Input Sources

### Primary
- `_sdd/spec/main.md` or `_sdd/spec/<project>.md`

### Secondary
- linked sub-spec files
- `_sdd/spec/DECISION_LOG.md`
- `_sdd/env.md` (run/test/context validation)
- code/config paths only when needed to verify outdated or ambiguous claims

## Rewrite Process

### Step 1: Diagnose Navigation and Changeability

**Tools**: `Read`, `Glob`, `Grep`

First identify why the current spec is hard to use.

Check for:
- 프로젝트 목적과 시스템 경계가 빠르게 보이지 않음
- `Repository Map`, `Runtime Map`, `Component Index`가 없음
- 기능 변경 시 어디부터 봐야 하는지 찾기 어려움 (탐색 가능성 부재)
- 계약, 상태 전이, 불변 조건이 묻혀 있음 (계약 가시화 부재)
- 실제 경로/심볼 없이 일반론만 많음
- Change Recipes 또는 변경 진입점이 없음 (변경 지향성 부재)
- 긴 로그, 참고용 예시, 역사 서술이 메인 흐름을 방해함
- 중복 표, 중복 설명, 깨진 링크가 많음
- 미확인 정보가 사실처럼 섞여 있음

**Decision Gate 1->2**:
```
navigation_issues_identified = 탐색성 저하 원인 식별 완료
rewrite_scope_clear = 리라이트 범위와 대상 문서 명확

IF navigation_issues_identified AND rewrite_scope_clear -> Step 2
ELSE -> 추가 진단 후 범위 보정
```

### Step 2: Propose Rewrite Target Shape First

**Tools**: deterministic defaults (non-interactive)

Present the rewrite target shape before editing. 리라이트의 목표는 **탐색형 지도로 재구성**하는 것이다.

```markdown
## Spec Rewrite Plan

**Target**: `_sdd/spec/<project>.md`
**Rewrite Goal**: 탐색형 지도로 재구성

### Keep in Main
- Goal -> Project Snapshot / Key Features / Non-Goals
- Architecture Overview -> System Boundary / Repository Map / Runtime Map
- Component Details -> Component Index + 핵심 컴포넌트 요약
- Usage Examples -> Running / Common Operations / Common Change Paths
- Open Questions

### Split by Responsibility
- `_sdd/spec/main.md`
- `_sdd/spec/auth.md`
- `_sdd/spec/jobs.md`
- `_sdd/spec/billing.md`

### Move Out of Main
- 긴 로그
- 반복 표
- 참고용 상세 예시
- 현재 판단에 영향이 적은 역사 서술

### Preserve Separately
- 중요한 rationale -> `DECISION_LOG.md`

### Risks / Unknowns
- [item]
```

The plan is good only if it clearly improves understanding and changeability, not just brevity.

### Step 3: Create Safety Backups

**Tools**: `Bash (mkdir -p, cp)`

For every modified file, create a backup under `_sdd/spec/prev/`.

### Step 4: Rewrite the Main Spec as an Entry Point

**Tools**: `Read`, `Edit`, `Write`

The rewritten main spec should answer these quickly:
- 이 저장소는 무엇을 하는가?
- 어디가 시스템 경계인가?
- 어떤 컴포넌트가 어디에 있는가?
- 어떤 변경은 어디부터 시작하는가?
- 무엇을 깨면 안 되는가?
- 아직 무엇이 불확실한가?

Core target shape for the main spec:
- `Goal` -> `Project Snapshot`, `Key Features`, `Non-Goals`
- `Architecture Overview` -> `System Boundary`, `Repository Map`, `Runtime Map`
- `Component Details` -> `Component Index` + 핵심 컴포넌트 요약 또는 링크
- `Open Questions`

Add optional sections only when they materially help maintenance:
- `Architecture Overview` -> `Technology Stack`, `Cross-Cutting Invariants`
- `Environment & Dependencies`
- `Identified Issues & Improvements`
- `Usage Examples` -> `Running the Project`, `Common Operations`, `Common Change Paths`

If `Usage Examples` is omitted, ensure common change entry points still appear in component `Change Recipes` or an equivalent change guide.

### Step 4.5: Prune and De-duplicate

**Tools**: `Edit`, `Write`

Rules:
- keep decision-driving and execution-critical content in the main spec
- move long logs, duplicated tables, and reference-only detail out of the main flow only when needed
- remove empty optional sections and low-value metadata instead of preserving placeholders
- do not create appendix files by default; use them only if the detail is still worth keeping and does not belong in a component spec
- prefer component-specific files over generic appendix dumps
- prefer compact tables, file maps, and links over repeated prose

### Step 5: Split by Responsibility, Not by Numbered Topic

**Tools**: `Write`, `Glob`

Preferred default structure:

```
_sdd/spec/
├── main.md
├── auth.md
├── billing.md
├── jobs.md
└── DECISION_LOG.md
```

Rules:
- main spec remains the entry point
- split files should be responsibility-based
- every split file must be reachable from the main spec
- keep filename patterns consistent
- if the existing repository already has a stable hierarchical structure, normalize only where it materially improves navigation

### Step 6: Preserve Rationale and Unknowns

**Tools**: `Read`, `Edit`

If the rewrite removes narrative sections that contain meaningful rationale:
- add a concise entry to `_sdd/spec/DECISION_LOG.md`
- keep the main spec concise
- keep unresolved ambiguity in `Open Questions`

### Step 7: Validate the Rewrite

**Tools**: `Glob`, `Read`

Validate:
- the main spec works as a 5-minute entry point
- `Repository Map`, `Runtime Map`, and `Component Index` exist
- key components have real paths or symbols
- Change Recipes 또는 변경 진입점이 존재
- 앵커 섹션(`Goal`, `Architecture Overview`, `Component Details`, `Open Questions`)이 보존됨
- optional sections appear only when relevant and are not empty
- duplication is reduced
- links are valid
- rationale is preserved
- unknowns are explicit
- the rewritten main spec is token-efficient enough to scan in one focused read

### Step 7.5: Quality Gate (LLM-as-Judge)

구조 검증(Step 7) 통과 후, 리라이트된 스펙이 본래 목적을 달성하는지 자체 평가한다.
이 단계는 **판정만** 수행한다. FAIL 시 보강은 이전 작성 단계(Step 4-6)로 돌아가 수행한다.
기준은 기존 리라이트 체크리스트(Step 7)와 정합하며, 그보다 과도한 요구를 하지 않는다.

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
| **PASS** | Component Details/Component Index에서 실제 파일 경로 또는 핵심 심볼을 찾을 수 있다 |
| **WEAK** | 컴포넌트는 기술되어 있으나 경로도 심볼도 부족하다 |
| **FAIL** | 기능이 어느 컴포넌트/파일에 속하는지 스펙에서 알 수 없다 |

**Criterion 3 — 안전한 수정 판단 (Change)**
> Probe: "Y를 변경하려면 어디를 수정하고 무엇을 주의해야 하는가?" (Y = 대표적 변경 시나리오)

| 판정 | 기준 |
|------|------|
| **PASS** | Change Recipes, 변경 핫스팟, 또는 변경 진입점이 있다 |
| **WEAK** | 변경 시작점은 있으나 주의사항(불변 조건, 영향 범위)이 부족하다 |
| **FAIL** | 변경 가이드가 전혀 없어 코드를 직접 탐색해야 한다 |

**Criterion 4 — 비자명한 결정 기억 (Remember)**
> Probe: "이 설계에서 왜 Z를 선택했는가?" 또는 "깨지면 안 되는 가정은 무엇인가?"

| 판정 | 기준 |
|------|------|
| **PASS** | Open Questions에 실질적 미결 사항이 있거나, 불변 조건/DECISION_LOG에 내용이 있다 |
| **WEAK** | 일부 기록은 있으나 리라이트 과정에서 삭제된 rationale이 보존되지 않았을 수 있다 |
| **FAIL** | Open Questions도 비어 있고, 리라이트 전에 있던 결정 맥락이 유실되었다 |

#### 검증 프로세스

1. 리라이트된 스펙 전체를 다시 읽는다
2. 각 criterion에 대해 probe 질문을 시도한다
   - Criterion 1: Goal 섹션에서 프로젝트 목적, 사용자, 비목표를 찾는다
   - Criterion 2: 주요 기능 1개를 골라 해당 경로 또는 심볼을 찾는다
   - Criterion 3: 대표적 변경 시나리오 1개를 설정하고 변경 진입점을 찾는다
   - Criterion 4: 불변 조건, 설계 결정, Open Questions를 찾는다
3. 각 criterion을 PASS / WEAK / FAIL로 판정한다
4. 결과에 따라 행동한다:

| 결과 | 행동 |
|------|------|
| ALL PASS | 검증 통과, 다음 단계 진행 |
| WEAK만 존재 (FAIL 없음) | 개선 포인트를 사용자에게 알리되 진행 허용 |
| FAIL 1개 이상 | FAIL 항목과 근거를 기록 → Step 4-6으로 돌아가 해당 부분만 보강 → 이 단계를 재실행 (최대 1회) |
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

## Output Format

### 1) Rewritten Spec Files

- list of rewritten files
- list of newly created split files
- list of sections moved out of the main flow

### 2) Rewrite Summary

Provide a concise summary in the completion output:
- what became easier to understand
- what became easier to change
- what was split out and why
- what remains uncertain

### 3) Optional Rewrite Report

Create `_sdd/spec/REWRITE_REPORT.md` only if:
- the user explicitly asks for it, or
- the rewrite is large enough that inline summary is insufficient

If created, include:
- target document
- split map
- key navigation changes
- unresolved issues
- decision-log additions

## Quality Checklist

- Can a reader understand project purpose and boundary quickly from the main spec?
- Does the main spec contain a repository map and runtime map?
- Does `Component Details` include a component index?
- Can a reader find likely edit points for common changes (Change Recipes)?
- Are actual paths or symbols present for important areas?
- Are tests, logs, or debugging starting points discoverable?
- Are major invariants and risks visible?
- Are unresolved ambiguities explicitly documented?
- Is essential rationale preserved in `DECISION_LOG.md` when removed from the main spec?
- Are anchor sections (`Goal`, `Architecture Overview`, `Component Details`, `Open Questions`) preserved?

## Language Preference

- Follow the main spec language by default
- For mixed-language specs, normalize toward the main spec language
- If that choice is uncertain, record the assumption in `Open Questions`

## Context Management

| 스펙 크기 | 전략 | 구체적 방법 |
|-----------|------|-------------|
| < 200줄 | 전체 읽기 | 전체 파일 읽기 |
| 200-500줄 | 전체 읽기 가능 | 전체 읽기 후 필요한 섹션 재확인 |
| 500-1000줄 | TOC 먼저 | 상위 TOC 확인 후 관련 섹션만 읽기 |
| > 1000줄 | 인덱스 우선 | 메인 인덱스와 타겟 섹션만 선택적으로 읽기 |

## Error Handling

| 상황 | 대응 |
|------|------|
| 스펙 파일 미발견 | `spec-create` 먼저 실행 권장 |
| 백업 디렉토리 미존재 | `mkdir -p _sdd/spec/prev/` 자동 생성 |
| 스펙이 이미 탐색형으로 잘 구조화됨 | 불필요한 리라이트를 지양하고 작업 로그에 보고 |
| 분할 후 링크 깨짐 | 경로 검증 후 자동 수정 |
| DECISION_LOG.md 미존재 | 필요 시 새로 생성 |
| 대형 스펙 (1000줄+) | 메인 인덱스와 핵심 섹션 위주로 점진 처리 |
| 추정 신뢰도 낮음 | `Open Questions`로 분리 |

## Additional Resources

### Reference Files
- `references/rewrite-checklist.md` - rewrite exit criteria and diagnostics

### Example Files
- `examples/rewrite-report.md` - optional rewrite summary example

## Integration with Other Skills

- **spec-create**: target shape reference for exploration-first specs
- **feature-draft**: benefits from stable `Goal` and `Component Details`
- **spec-summary**: benefits from preserved top-level anchors
- **spec-update-done**: sync rewritten spec with actual implementation state
