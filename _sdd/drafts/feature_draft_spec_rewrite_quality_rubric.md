# Feature Draft: spec-rewrite 품질 진단 rubric 및 whitepaper 정렬 강화

<!-- spec-update-todo-input-start -->
# Part 1: Spec Patch Draft

# Spec Update Input

**Date**: 2026-04-02
**Author**: Codex
**Target Spec**: `_sdd/spec/main.md`
**Spec Update Classification**: Improvement

## Background & Motivation Updates

### Improvement: spec-rewrite의 목적을 "문서 정리"에서 "품질 진단 기반 재작성"으로 명확화
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Component Details` > `spec-rewrite`
**Current State**: spec-rewrite는 prune/split/appendix 이동 중심의 구조 개선 도구로 설명되어 있으나, 재작성 전에 어떤 품질 축으로 진단해야 하는지 기준이 얕다.
**Proposed**: spec-rewrite를 "8개 핵심 품질 metric과 spec-as-whitepaper 기준으로 현재 스펙을 진단하고, 그 진단을 근거로 재작성 계획과 리포트를 만드는 스킬"로 재정의한다.
**Reason**: 단순 길이/중복 기준만으로는 사용자가 실제로 레포의 기능, 구조, 사용법을 이해할 수 있는지 평가하기 어렵다. 재작성의 목적은 보기 좋게 줄이는 것이 아니라, 사람이 읽고 행동할 수 있는 스펙 구조를 만드는 데 있다.

## Design Changes

### Improvement: Step 1 진단 기준을 8개 핵심 metric 기반 rubric으로 확장
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Component Details` > `spec-rewrite` > `Process`
**Current State**: 현재 진단 기준은 섹션 길이 불균형, 중복, 저가치 appendix 후보, 파일 분할 필요성, 모호성, whitepaper 섹션 누락 여부 정도로 제한되어 있다.
**Proposed**: Step 1에서 아래 8개 핵심 metric을 `0-3` 척도로 평가하도록 계약을 명시한다. 각 metric은 추상 명칭만 두지 않고, 실제 진단에 사용할 질문형 rubric과 함께 정의한다.
- component 분리 적절성
- 탐색성
- 레포 목적 이해도
- 아키텍처 이해도
- 사용법 완결성
- 환경 재현성
- 모호성 수준
- Why/decision 보존도
예시 질문:
- "각 주요 component가 하나의 대표 섹션/파일에 귀속되는가?"
- "main만 읽고 3문장 안에 레포 목적과 핵심 기능을 설명할 수 있는가?"
- "사용자가 핵심 흐름과 component 책임을 혼동 없이 말할 수 있는가?"
- "신규 사용자가 문서만 보고 대표 시나리오를 실행할 수 있는가?"
- "필요한 정보를 main 기준 2-hop 이내에 찾을 수 있는가?"
- "중요한 설계 이유가 삭제되거나 appendix로 밀려나지 않았는가?"
**Reason**: 이 8개 축은 구조 품질, 사용자 이해 가능성, 실행 가능성, 유지보수 가능성을 함께 커버하며, 실제 rewrite 필요성과 방향을 더 일관되게 판단하게 한다.

### Improvement: spec-as-whitepaper 평가를 `docs/SDD_SPEC_DEFINITION.md` 기준과 직접 연결
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Component Details` > `spec-rewrite` > `Validation`
**Current State**: 현재는 §1/§2/§5, citation, code excerpt header 보존 정도만 검사하며, 왜 이 기준이 필요한지와 whitepaper 정의 문서와의 연결이 약하다.
**Proposed**: spec-rewrite가 `docs/SDD_SPEC_DEFINITION.md`를 근거 문서로 사용하여 다음 축을 함께 평가한다고 명시한다.
- 배경 및 동기 설명 여부
- 핵심 설계 서사와 로직 흐름 설명 여부
- 구현 근거와 코드 매핑 존재 여부
- 사용 가이드와 기대 결과 존재 여부
- 참조형 보조 정보와 narrative 섹션의 균형
**Reason**: spec-format.md의 체크리스트가 단순 형식 점검에 그치지 않고, SDD가 정의한 "화이트페이퍼형 Single Source of Truth" 개념을 반영해야 한다.

### Improvement: REWRITE_REPORT를 "무엇을 옮겼는지"뿐 아니라 "왜 다시 썼는지"를 보여주는 진단 리포트로 강화
**Priority**: High
**Target Section**: `_sdd/spec/main.md` > `Component Details` > `spec-rewrite` > `Output`
**Current State**: REWRITE_REPORT는 pruning/move/split 결과와 whitepaper 섹션 상태를 요약하지만, rewrite 전 품질 진단 점수와 사용성 관점의 문제를 구조적으로 드러내지 않는다.
**Proposed**: REWRITE_REPORT에 최소 아래 내용을 추가한다.
- 8개 핵심 metric 점수표 (`0-3`)
- 항목별 주요 근거와 rewrite implication
- `docs/SDD_SPEC_DEFINITION.md` 기준 whitepaper 적합성 평가
- "자동 보강하지 않고 경고만 남긴 항목" 목록
**Reason**: spec-rewrite의 출력은 단순 작업 로그가 아니라, 왜 이 구조 변경이 필요한지와 무엇이 여전히 unresolved인지 후속 스킬이 이해할 수 있는 진단 문서여야 한다.

## Improvements

### Improvement: rewrite-checklist와 spec-format reference를 동일한 진단 계약으로 정렬
**Priority**: Medium
**Target Section**: `_sdd/spec/main.md` > `Component Details` > `spec-rewrite` > `Companion Assets`
**Current State**: SKILL.md, rewrite-checklist.md, spec-format.md, rewrite-report example 사이에 품질 진단 깊이가 완전히 일치하지 않는다.
**Proposed**: companion assets를 아래 역할로 정리한다.
- `rewrite-checklist.md`: 실무용 진단/검증 체크리스트
- `spec-format.md`: whitepaper 구조와 보존 규칙 + SDD 정의와의 연결 요약
- `rewrite-report.md`: metric scoring과 whitepaper 적합성 경고가 포함된 예시
운영 규칙:
- `rewrite-checklist.md`는 각 metric을 질문형 rubric으로 풀어쓴 canonical reference가 된다.
- `SKILL.md`는 축약된 metric 이름과 scoring contract를 유지하되, checklist의 질문형 rubric을 따르도록 연결한다.
**Reason**: 운영 계약이 분산되어 서로 다른 수준의 기준을 말하면 rewrite 결과가 사람/플랫폼마다 달라진다.

### Improvement: `.claude`와 `.codex`의 spec-rewrite 계약을 동일한 품질 기준으로 동기화
**Priority**: Medium
**Target Section**: `_sdd/spec/main.md` > `Architecture Overview` > `Platform Parity`
**Current State**: `.claude/skills/spec-rewrite/`와 `.codex/skills/spec-rewrite/`는 공통 목적을 가지지만, Step 설명과 AC 표현 수준이 다르다.
**Proposed**: 두 플랫폼 모두 동일한 진단 rubric, whitepaper 평가 기준, REWRITE_REPORT 계약을 사용하도록 parity를 명시한다. 플랫폼 차이는 도구 표현 수준으로만 제한한다.
**Reason**: 한쪽만 진단이 강화되면 `spec-summary`, `spec-review`, 후속 rewrite 결과가 플랫폼별로 달라져 spec drift를 다시 만든다.

## Failure Modes

| 시나리오 | 실패 시 | 사용자 가시성 | 처리 방안 |
|----------|---------|---------------|-----------|
| metric 정의만 늘어나고 실제 사용 지침이 없음 | 진단이 길어지기만 하고 rewrite 방향 결정에 도움을 주지 못함 | REWRITE_REPORT가 장황하지만 actionable하지 않음 | 각 metric에 평가 질문과 rewrite implication을 함께 정의 |
| spec-rewrite가 spec-upgrade 역할까지 흡수 | 정리 스킬이 자동 보강/확장까지 하려다 범위가 과도해짐 | 사용자가 "정리"를 요청했는데 내용이 임의로 확장됨 | whitepaper 평가는 보존 + 경고까지만 하고 자동 생성은 하지 않음 |
| `.claude`/`.codex` 기준 불일치 | 플랫폼에 따라 다른 rewrite 판단이 나옴 | 같은 문서에 대해 상반된 진단 가능 | SKILL.md, references, example, version을 양쪽 동시 갱신 |

## Notes

### Context
- 이번 변경의 핵심은 `spec-rewrite`를 구조 정리 도구로 유지하되, 정리 전 진단과 정리 후 검증을 훨씬 더 엄밀하게 만드는 것이다.
- `docs/SDD_SPEC_DEFINITION.md`는 생성 템플릿이 아니라 평가 기준의 상위 정의로만 사용한다.
- 자동 보강은 `spec-create`/`spec-upgrade`의 역할로 남기고, `spec-rewrite`는 평가, 보존, 경고, 재배치에 집중한다.

### Open Questions
- 8개 metric 전체를 `Step 1` 본문에 인라인으로 둘지, `rewrite-checklist.md`를 canonical rubric으로 두고 SKILL.md에서는 축약 요약만 둘지 결정이 필요하다.
- REWRITE_REPORT에서 metric 점수를 절대 점수로 볼지, "rewrite 전 기준선" 성격으로만 쓸지 표현을 정해야 한다.

<!-- spec-update-todo-input-end -->

# Part 2: Implementation Plan

## Overview

`spec-rewrite` 스킬이 현재 스펙을 재작성하기 전에 문서 품질을 구조적으로 진단하도록 강화한다. 핵심은 8개 핵심 metric과 `docs/SDD_SPEC_DEFINITION.md`의 spec-as-whitepaper 정의를 결합해, rewrite plan과 REWRITE_REPORT가 모두 같은 평가 축을 따르도록 만드는 것이다.

이번 작업은 "rewrite가 whitepaper를 자동 생성한다"가 아니라, "rewrite가 whitepaper 성질과 사용자 이해 가능성을 훼손하지 않도록 평가/보존/경고 계약을 강화한다"에 초점을 둔다.

## Scope

### In Scope
- `.codex/skills/spec-rewrite/`의 진단/계획/검증/리포트 계약 강화
- `.claude/skills/spec-rewrite/`와 parity 유지
- `rewrite-checklist.md`, `spec-format.md`, `examples/rewrite-report.md`의 역할 정렬
- `skill.json` 버전 동기화
- `_sdd/spec/main.md`의 spec-rewrite component description 업데이트

### Out of Scope
- `docs/SDD_SPEC_DEFINITION.md` 자체 수정
- `spec-rewrite`에 자동 whitepaper 생성/보강 로직 추가
- 실제 사용자 프로젝트 spec migration 실행

## Components

1. **spec-rewrite / SKILL.md**: 진단 rubric, whitepaper 기준 연결, REWRITE_REPORT 계약
2. **rewrite-checklist.md**: 운영용 품질 체크리스트
3. **spec-format.md**: spec-as-whitepaper 평가 기준 요약
4. **rewrite-report example**: 기대 출력 예시
5. **repo spec sync**: `_sdd/spec/main.md` 내 spec-rewrite 설명

## Implementation Phases

### Phase 1: 진단 계약 재설계
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 1 | spec-rewrite Step 1 rubric과 점수 체계 정의 | P0 | - | SKILL.md |
| 2 | Step 2/Step 5/Output Contract를 새 rubric과 연결 | P0 | 1 | SKILL.md |
| 3 | REWRITE_REPORT에 metric scorecard와 whitepaper 평가 블록 추가 | P0 | 1,2 | example + SKILL.md |

### Phase 2: Reference 정렬 및 플랫폼 parity
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 4 | rewrite-checklist.md를 8개 metric + whitepaper 기준으로 재구성 | P1 | 1 | checklist |
| 5 | spec-format.md를 `docs/SDD_SPEC_DEFINITION.md` 평가 축과 정렬 | P1 | 1 | spec-format |
| 6 | `.claude`/`.codex` 양쪽 spec-rewrite 문서 세트를 동기화 | P1 | 1-5 | parity |

### Phase 3: 리포지토리 스펙/메타데이터 반영
| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 7 | `_sdd/spec/main.md`의 spec-rewrite 설명을 최신 계약으로 갱신 | P2 | 1-6 | repo spec |
| 8 | `skill.json` 버전 갱신 및 간단 검증 수행 | P2 | 6 | metadata |

## Task Details

### Task 1: spec-rewrite Step 1 rubric과 점수 체계 정의
**Component**: spec-rewrite
**Priority**: P0
**Type**: Improvement

**Description**:  
`.codex/skills/spec-rewrite/SKILL.md`와 `.claude/skills/spec-rewrite/SKILL.md`의 진단 단계를 8개 핵심 metric 기반 rubric으로 교체한다. 각 metric은 `0-3` 점수, 평가 질문, rewrite implication을 갖도록 설계한다.

**Acceptance Criteria**:
- [ ] Step 1에 8개 핵심 metric이 명시된다
- [ ] 점수 체계(`0-3`)와 해석 기준이 포함된다
- [ ] "component 분리 적절성", "탐색성", "레포 목적 이해도", "아키텍처 이해도", "사용법 완결성", "환경 재현성", "모호성 수준", "Why/decision 보존도"가 모두 포함된다
- [ ] 각 metric이 질문형 rubric 또는 이를 가리키는 명시적 reference를 가진다
- [ ] 진단 결과가 Step 2 rewrite plan 입력으로 이어지는 흐름이 설명된다

**Target Files**:
- [M] `.codex/skills/spec-rewrite/SKILL.md` -- Diagnose 단계 rubric 확장
- [M] `.claude/skills/spec-rewrite/SKILL.md` -- Diagnose 단계 rubric 확장

**Technical Notes**:
- 단순 체크리스트 나열보다 "metric + guiding question + score interpretation" 구조가 낫다
- `spec-rewrite`의 역할은 평가와 재배치이지 자동 생성이 아님을 Step 1/2에서 분명히 유지해야 한다
- 질문형 rubric의 상세 문구는 `rewrite-checklist.md`를 canonical source로 두고, SKILL.md에는 요약 예시만 남기는 구성이 적합하다

**Dependencies**: -

### Task 2: Step 2/Step 5/Output Contract를 새 rubric과 연결
**Component**: spec-rewrite
**Priority**: P0
**Type**: Improvement

**Description**:  
새 진단 결과가 실제 rewrite plan과 검증 단계에 반영되도록 Step 2, Step 5, Output Contract를 갱신한다. rewrite plan에는 낮은 점수 metric을 우선적으로 다루는 근거가 포함되어야 하고, 검증 단계는 "구조가 더 깔끔해졌는가"가 아니라 "이해/탐색/사용성이 개선되었는가"를 보도록 바꾼다.

**Acceptance Criteria**:
- [ ] Step 2 계획 제시에 metric 기반 rewrite rationale이 포함된다
- [ ] Step 5 검증이 whitepaper 존재 여부만이 아니라 사용성/구조 품질을 함께 확인한다
- [ ] Output Contract가 scorecard, 핵심 이슈, unresolved warning을 요구한다

**Target Files**:
- [M] `.codex/skills/spec-rewrite/SKILL.md` -- Plan/Validate/Output Contract 정렬
- [M] `.claude/skills/spec-rewrite/SKILL.md` -- Plan/Validate/Output Contract 정렬

**Technical Notes**:
- Step 2는 "무엇을 옮길지"뿐 아니라 "왜 이 이동이 필요한지"를 metric 기준으로 설명해야 한다
- Step 5는 `docs/SDD_SPEC_DEFINITION.md`의 정의 축을 최소 요약으로 참조해야 한다

**Dependencies**: 1

### Task 3: REWRITE_REPORT에 metric scorecard와 whitepaper 평가 블록 추가
**Component**: spec-rewrite
**Priority**: P0
**Type**: Feature

**Description**:  
sample rewrite report와 SKILL.md의 report contract를 확장해, 8개 metric 점수표와 `docs/SDD_SPEC_DEFINITION.md` 기반 whitepaper 적합성 평가를 포함한다.

**Acceptance Criteria**:
- [ ] REWRITE_REPORT 예시에 8개 metric scorecard가 포함된다
- [ ] whitepaper 평가가 §1/§2/§5 존재 여부를 넘어서 narrative/code mapping/usage guidance까지 언급한다
- [ ] "자동 보강하지 않고 경고만 남긴 항목"이 별도 블록으로 드러난다

**Target Files**:
- [M] `.codex/skills/spec-rewrite/SKILL.md` -- Report contract 강화
- [M] `.codex/skills/spec-rewrite/examples/rewrite-report.md` -- metric scorecard 예시 추가
- [M] `.claude/skills/spec-rewrite/SKILL.md` -- Report contract 강화
- [M] `.claude/skills/spec-rewrite/examples/rewrite-report.md` -- metric scorecard 예시 추가

**Technical Notes**:
- 점수표는 숫자만 두지 말고 한 줄 근거를 같이 두는 편이 좋다
- report 예시는 "누락 경고는 하지만 자동 생성하지 않는다"는 경계선을 분명히 보여줘야 한다

**Dependencies**: 1, 2

### Task 4: rewrite-checklist.md를 8개 metric + whitepaper 기준으로 재구성
**Component**: spec-rewrite references
**Priority**: P1
**Type**: Improvement

**Description**:  
`rewrite-checklist.md`를 pre-check/prune/split 중심 체크리스트에서, 구조 품질/레포 이해 가능성/실행 가능성/유지보수성/whitepaper 적합성까지 포괄하는 운영용 checklist로 확장한다.

**Acceptance Criteria**:
- [ ] checklist에 8개 핵심 metric이 직접 반영된다
- [ ] component 분리와 사용자 이해 가능성 평가 질문이 포함된다
- [ ] checklist가 REWRITE_REPORT의 metric scorecard와 같은 용어를 사용한다
- [ ] 각 metric마다 1개 이상의 질문형 rubric이 포함된다
- [ ] 최소 예시 질문으로 component 귀속, main-only 목적 이해, 2-hop 탐색성, 대표 시나리오 실행 가능성이 반영된다

**Target Files**:
- [M] `.codex/skills/spec-rewrite/references/rewrite-checklist.md` -- rubric 중심 checklist로 재구성
- [M] `.claude/skills/spec-rewrite/references/rewrite-checklist.md` -- rubric 중심 checklist로 재구성

**Technical Notes**:
- Step 1에서 SKILL.md가 high-level contract를 말하고, checklist가 실제 평가 질문을 더 자세히 담는 형태가 적합하다

**Dependencies**: 1

### Task 5: spec-format.md를 `docs/SDD_SPEC_DEFINITION.md` 평가 축과 정렬
**Component**: spec-format reference
**Priority**: P1
**Type**: Improvement

**Description**:  
`references/spec-format.md`를 단순 §1-§8 체크리스트에서, `docs/SDD_SPEC_DEFINITION.md`가 정의한 "문제/동기/핵심 설계/코드 근거/사용 가이드" 축과 직접 연결된 평가 레퍼런스로 보강한다.

**Acceptance Criteria**:
- [ ] spec-format.md가 `docs/SDD_SPEC_DEFINITION.md`의 핵심 정의를 요약한 평가 축을 포함한다
- [ ] "섹션 존재 여부"와 "설명 품질"을 구분해 적는다
- [ ] 자동 생성 템플릿이 아니라 validation/preservation reference라는 성격이 유지된다

**Target Files**:
- [M] `.codex/skills/spec-rewrite/references/spec-format.md` -- whitepaper 평가 기준 정렬
- [M] `.claude/skills/spec-rewrite/references/spec-format.md` -- whitepaper 평가 기준 정렬

**Technical Notes**:
- `docs/SDD_SPEC_DEFINITION.md`를 그대로 복사하지 말고, spec-rewrite에 필요한 평가 관점만 압축해야 한다

**Dependencies**: 1

### Task 6: `.claude`/`.codex` 양쪽 spec-rewrite 문서 세트를 동기화
**Component**: parity
**Priority**: P1
**Type**: Refactor

**Description**:  
두 플랫폼의 `SKILL.md`, `references/`, `examples/`, `skill.json`이 같은 품질 계약을 표현하도록 정렬한다. 플랫폼별 차이는 툴 이름과 상호작용 표현 정도로만 제한한다.

**Acceptance Criteria**:
- [ ] `.claude`와 `.codex`의 진단 rubric이 동일한 metric 집합을 사용한다
- [ ] references와 example의 핵심 체크 항목이 일치한다
- [ ] 플랫폼별 문서 차이가 의도적 차이인지 설명 가능하다

**Target Files**:
- [M] `.codex/skills/spec-rewrite/SKILL.md` -- parity sync
- [M] `.codex/skills/spec-rewrite/references/rewrite-checklist.md` -- parity sync
- [M] `.codex/skills/spec-rewrite/references/spec-format.md` -- parity sync
- [M] `.codex/skills/spec-rewrite/examples/rewrite-report.md` -- parity sync
- [M] `.codex/skills/spec-rewrite/skill.json` -- version bump
- [M] `.claude/skills/spec-rewrite/SKILL.md` -- parity sync
- [M] `.claude/skills/spec-rewrite/references/rewrite-checklist.md` -- parity sync
- [M] `.claude/skills/spec-rewrite/references/spec-format.md` -- parity sync
- [M] `.claude/skills/spec-rewrite/examples/rewrite-report.md` -- parity sync
- [M] `.claude/skills/spec-rewrite/skill.json` -- version bump

**Technical Notes**:
- `.codex`는 한국어 중심 concise contract, `.claude`는 tool-oriented step wording 차이가 있으나 metric/criteria는 동일해야 한다

**Dependencies**: 1, 2, 3, 4, 5

### Task 7: `_sdd/spec/main.md`의 spec-rewrite 설명을 최신 계약으로 갱신
**Component**: repo spec
**Priority**: P2
**Type**: Improvement

**Description**:  
레포 글로벌 스펙에 `spec-rewrite`의 진단 방식과 whitepaper 평가 관점을 반영해, 현재 구현과 스펙 설명이 어긋나지 않게 한다.

**Acceptance Criteria**:
- [ ] `spec-rewrite` component 설명에 8개 metric 기반 진단이 언급된다
- [ ] whitepaper 보존/경고 원칙이 반영된다
- [ ] REWRITE_REPORT가 단순 작업 로그가 아니라 진단 리포트라는 점이 드러난다

**Target Files**:
- [M] `_sdd/spec/main.md` -- spec-rewrite component details 업데이트
- [M] `_sdd/spec/DECISION_LOG.md` -- 필요 시 변경 rationale 기록

**Dependencies**: 1-6

### Task 8: `skill.json` 버전 갱신 및 간단 검증 수행
**Component**: metadata
**Priority**: P2
**Type**: Infrastructure

**Description**:  
문서 세트가 갱신된 뒤 `.claude`/`.codex` `skill.json` 버전을 올리고, 주요 파일 간 핵심 용어와 section contract가 일치하는지 간단 검증한다.

**Acceptance Criteria**:
- [ ] 양쪽 `skill.json` 버전이 증가한다
- [ ] 8개 metric 명칭이 SKILL.md/checklist/example에서 일관된다
- [ ] `docs/SDD_SPEC_DEFINITION.md` 참조가 구현 범위를 넘지 않고 평가 기준 수준에 머문다

**Target Files**:
- [M] `.codex/skills/spec-rewrite/skill.json` -- version bump
- [M] `.claude/skills/spec-rewrite/skill.json` -- version bump

**Technical Notes**:
- 자동화 테스트가 없다면 최소한 `rg` 기반 용어 정합성 체크를 수행해야 한다

**Dependencies**: 6

## Parallel Execution Summary

- Phase 1은 동일 write set이 많아 순차 진행이 안전하다.
- Phase 2부터는 파일 세트가 분리되므로 `.claude/skills/spec-rewrite/`와 `.codex/skills/spec-rewrite/`를 플랫폼별로 병렬 처리할 수 있다.
- `_sdd/spec/main.md`와 `DECISION_LOG.md`는 마지막 동기화 단계에서만 수정하는 것이 충돌을 줄인다.

## Risks and Mitigations

- metric이 과도하게 많아져 SKILL.md가 다시 비대해질 수 있다.  
  대응: SKILL.md에는 핵심 8개 metric과 scoring contract만 두고, 세부 질문은 checklist로 내린다.

- `spec-rewrite`가 `spec-upgrade` 역할을 침범할 수 있다.  
  대응: 자동 보강 금지, 보존 + 경고 + 재배치에만 집중하도록 Hard Rules와 report wording을 분명히 한다.

- `.claude`/`.codex` 표현 차이로 다시 drift가 생길 수 있다.  
  대응: same metric vocabulary를 공유하고, platform-specific wording은 tool line 정도로만 제한한다.

## Open Questions

- 8개 metric 중 `환경 재현성`을 모든 spec에 항상 적용할지, 환경/운영형 프로젝트에 더 강하게 적용할지 weighting을 둘 필요가 있다.
- REWRITE_REPORT가 rewrite 전 점수만 기록할지, rewrite 후 self-check 점수까지 같이 기록할지 결정이 필요하다.
