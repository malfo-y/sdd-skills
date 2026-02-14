# Implementation Plan: `feature-draft` 스킬

## 개요

`spec-draft` + `spec-update-todo` + `implementation-plan` 세 스킬의 기능을 하나로 합친 새 스킬.
사용자와 대화를 통해 요구사항을 수집하고, 스펙 패치 초안과 구현 계획을 **단일 파일**로 출력합니다.
기존 3단계 워크플로우(3x 토큰)를 1단계(~1x 토큰)로 축소하는 것이 목표입니다.

## 범위

### In Scope

- 스킬 디렉토리 구조 생성 (`.claude/skills/feature-draft/`)
- SKILL.md 메인 프롬프트 작성 (7단계 프로세스)
- 참조 문서 작성 (adaptive-questions.md, output-format.md)
- 예시 파일 작성 (feature_draft.md)
- SDD_QUICK_START.md 업데이트 (워크플로우에 feature-draft 추가)

### Out of Scope

- `.codex/skills/` 버전 (사용자 결정에 따라 제외)
- 기존 스킬 수정 (spec-draft, spec-update-todo, implementation-plan은 그대로 유지)
- 자동화 스크립트

## 설계 결정 사항

| 결정 | 선택 | 근거 |
|------|------|------|
| 스펙 수정 방식 | 패치 초안만 출력 (read-only) | 안전하고 리뷰 가능 |
| 입력 수집 방식 | Adaptive (상세하면 skip, 모호하면 질문) | 토큰 절약과 완성도 균형 |
| 출력 형식 | 단일 파일 (Part 1 + Part 2) | 간단하고 리뷰 용이 |
| 출력 위치 | `_sdd/drafts/` | 전용 디렉토리로 깔끔한 분리 |
| spec-update-todo 호환 | Part 1이 "Spec Update Input" 형식 준수 | 자동 적용 가능 |
| 복수 기능 지원 | 지원하되 사용자에게 먼저 확인 | 유연성 + 명시적 동의 |
| 파일명 형식 | `feature_draft_<feature_name>.md` (lowercase) | 사용자 선호 |
| Codex 지원 | Claude only | 사용자 결정 |

## 컴포넌트

1. **SKILL.md**: 메인 스킬 정의 (프로세스 7단계, 규칙, 가이드라인)
2. **references/adaptive-questions.md**: Adaptive 모드 질문 가이드 (입력 완성도 판단 기준 + 유형별 핵심 질문)
3. **references/output-format.md**: 출력 파일 상세 포맷 명세
4. **examples/feature_draft.md**: 완성된 출력 예시 파일

## 구현 단계

### Phase 1: 스킬 구조 설정

| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 1 | `.claude/skills/feature-draft/` 디렉토리 구조 생성 | P0 | - | Infrastructure |
| 2 | SKILL.md 메타데이터 및 개요 섹션 작성 | P0 | 1 | SKILL.md |

### Phase 2: 핵심 프로세스 작성

| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 3 | SKILL.md Step 1-3 작성 (입력 분석, 컨텍스트 수집, Adaptive 질문) | P0 | 2 | SKILL.md |
| 4 | SKILL.md Step 4-5 작성 (피처 설계, 스펙 패치 생성) | P0 | 3 | SKILL.md |
| 5 | SKILL.md Step 6-7 작성 (구현 계획 생성, 확인 및 완료) | P0 | 4 | SKILL.md |
| 6 | references/adaptive-questions.md 작성 | P1 | 3 | References |
| 7 | references/output-format.md 작성 | P1 | 4, 5 | References |

### Phase 3: 예시 및 통합

| ID | Task | Priority | Dependencies | Component |
|----|------|----------|--------------|-----------|
| 8 | examples/feature_draft.md 작성 (완성된 출력 예시) | P1 | 7 | Examples |
| 9 | SDD_QUICK_START.md 업데이트 (feature-draft 워크플로우 추가) | P2 | 8 | Documentation |

## 태스크 상세

### Task 1: 디렉토리 구조 생성

**Component**: Infrastructure
**Priority**: P0
**Type**: Infrastructure

**설명**:
`.claude/skills/feature-draft/` 디렉토리와 하위 디렉토리를 생성합니다.

**구조**:
```
.claude/skills/feature-draft/
├── SKILL.md
├── references/
│   ├── adaptive-questions.md
│   └── output-format.md
└── examples/
    └── feature_draft.md
```

**Acceptance Criteria**:
- [ ] 디렉토리 구조가 기존 스킬과 동일한 패턴
- [ ] references/, examples/ 하위 디렉토리 존재

---

### Task 2: SKILL.md 메타데이터 및 개요 작성

**Component**: SKILL.md
**Priority**: P0
**Type**: Feature
**Dependencies**: 1

**설명**:
SKILL.md의 frontmatter (name, description, version)와 Overview, When to Use, Input Sources, Output, Hard Rules 섹션을 작성합니다.

**핵심 내용**:
- **name**: `feature-draft`
- **description**: 트리거 키워드 포함 ("feature draft", "기능 초안", "feature plan", "기능 계획", "draft and plan", "초안과 계획")
- **Hard Rules**:
  - 스펙 파일 수정 금지 (read-only)
  - 출력 파일은 `_sdd/drafts/` 디렉토리
  - 결과 파일 내용은 한국어로 작성
- **Input Sources**: 사용자 대화, 기존 파일 (user_draft.md, user_spec.md, user_input.md), 코드 변경사항
- **Output**: `_sdd/drafts/feature_draft_<feature_name>.md`
- **복수 기능**: 지원하되, 반드시 사용자에게 먼저 확인 ("여러 기능을 한 파일에 포함하시겠습니까?")

**Acceptance Criteria**:
- [ ] frontmatter가 기존 스킬 패턴과 일관성 유지
- [ ] 트리거 키워드가 기존 스킬과 충돌하지 않음
- [ ] Hard Rules 명확히 정의됨

---

### Task 3: Step 1-3 작성 (입력 분석 ~ Adaptive 질문)

**Component**: SKILL.md
**Priority**: P0
**Type**: Feature
**Dependencies**: 2

**설명**:
프로세스의 앞부분 3단계를 작성합니다.

**Step 1: 입력 분석 (Input Analysis)**
- 사용자 대화 내용 확인
- 기존 파일 확인: `_sdd/spec/user_draft.md`, `_sdd/spec/user_spec.md`, `_sdd/implementation/user_input.md`
- 코드 변경사항 확인 (git diff 등)
- 입력 완성도 레벨 판정: HIGH / MEDIUM / LOW

**Step 2: 컨텍스트 수집 (Context Gathering)**
- 기존 스펙 읽기 (read-only): `_sdd/spec/<project>.md` 또는 `main.md`
- 스펙 구조 파악 (섹션 목록, 컴포넌트 목록, 기존 기능 목록)
- 기존 DECISION_LOG.md 확인 (존재 시)

**Step 3: Adaptive 질문 (Adaptive Clarification)**
- HIGH: 질문 없이 바로 진행
- MEDIUM: 1-3개 핵심 질문만 (우선순위, 수용 기준, 기술 제약)
- LOW: 유형별 필수 질문 수행 (references/adaptive-questions.md 참조)
- AskUserQuestion 도구 활용

**Acceptance Criteria**:
- [ ] 입력 완성도 판정 기준이 명확
- [ ] Adaptive 질문 로직이 3단계로 분류됨
- [ ] 기존 스펙 read-only 접근 명시

---

### Task 4: Step 4-5 작성 (피처 설계 ~ 스펙 패치)

**Component**: SKILL.md
**Priority**: P0
**Type**: Feature
**Dependencies**: 3

**설명**:
피처 분석과 스펙 패치 초안 생성 단계를 작성합니다.

**Step 4: 피처 설계 (Feature Design)**
- 요구사항을 기능/개선/버그/컴포넌트/설정으로 분류
- 각 항목의 대상 스펙 섹션 매핑 (section-mapping 참조)
- 컴포넌트 식별 및 의존성 파악

**Step 5: 스펙 패치 생성 (Spec Patch Generation) = Part 1**
- "Spec Update Input" 형식으로 작성 (spec-update-todo 호환)
- 각 항목에 `**Target Section**` 어노테이션 추가 (수동 copy-paste 용)
- 상태 마커 사용: 📋 계획됨
- 스펙의 기존 스타일/언어에 맞춤

**Acceptance Criteria**:
- [ ] "Spec Update Input" 형식 완전 준수
- [ ] Target Section 어노테이션이 section-mapping 규칙 따름
- [ ] spec-update-todo에 바로 입력 가능한 포맷

---

### Task 5: Step 6-7 작성 (구현 계획 ~ 완료)

**Component**: SKILL.md
**Priority**: P0
**Type**: Feature
**Dependencies**: 4

**설명**:
구현 계획 생성과 확인/완료 단계를 작성합니다.

**Step 6: 구현 계획 생성 (Implementation Plan Generation) = Part 2**
- 컴포넌트 식별 (Part 1의 분석 결과 재활용)
- 태스크 정의 (Title, Component, Priority, Type, Description, Acceptance Criteria, Technical Notes, Dependencies)
- 의존성 매핑 및 단계 분리 (Phase 1, 2, 3...)
- 위험 요소 및 대응 방안
- 미해결 질문 (Open Questions)
- 모델 추천 (complexity 기반)

**Step 7: 확인 및 완료 (Review & Confirm)**
- 생성된 초안을 사용자에게 보여줌
- 수정 사항 반영
- `_sdd/drafts/` 디렉토리 생성 (없으면)
- 파일 저장: `_sdd/drafts/feature_draft_<feature_name>.md`
- 기존 파일이 있으면 `_sdd/drafts/prev/prev_feature_draft_<name>_<timestamp>.md`로 아카이브
- 입력 파일 처리: `user_draft.md` → `_processed_user_draft.md` 등 (사용된 경우)
- 다음 단계 안내

**Acceptance Criteria**:
- [ ] 구현 계획 형식이 implementation 스킬에서 바로 사용 가능
- [ ] 파일 아카이브 규칙이 기존 스킬과 일관성 유지
- [ ] 다음 단계 안내에 2가지 경로 제시 (수동 copy-paste vs spec-update-todo)

---

### Task 6: references/adaptive-questions.md 작성

**Component**: References
**Priority**: P1
**Type**: Feature
**Dependencies**: 3

**설명**:
Adaptive 모드의 질문 가이드를 작성합니다. spec-draft의 `question-guide.md`를 기반으로 하되, 3단계 완성도 레벨에 맞게 재구성합니다.

**핵심 내용**:

1. **입력 완성도 판정 기준**:
   - HIGH: 기능명 + 설명 + 수용 기준 + 우선순위 모두 있음
   - MEDIUM: 기능명 + 설명은 있으나 수용 기준이나 우선순위 부족
   - LOW: 모호한 아이디어 수준 ("이런 기능 추가하고 싶어")

2. **레벨별 질문 전략**:
   - HIGH → 질문 없이 진행 (확인만)
   - MEDIUM → 핵심 1-3개: 우선순위, acceptance criteria, 기술 제약
   - LOW → 유형 확인 후 필수 질문 (spec-draft 질문 가이드의 축약 버전)

3. **유형별 핵심 질문** (LOW 레벨용):
   - 새 기능: 이름, 우선순위, 설명, 수용 기준
   - 개선: 현재 상태, 제안, 이유
   - 버그: 심각도, 위치, 재현 방법

**Acceptance Criteria**:
- [ ] 3단계 완성도 레벨이 명확히 정의됨
- [ ] 레벨별 질문 수가 최소화됨 (토큰 절약 목적)
- [ ] spec-draft의 question-guide.md 핵심 내용 포함

---

### Task 7: references/output-format.md 작성

**Component**: References
**Priority**: P1
**Type**: Feature
**Dependencies**: 4, 5

**설명**:
출력 파일의 상세 포맷 명세를 작성합니다.

**핵심 내용**:

1. **파일 구조**:
   - 헤더 (Feature Name, Date, Author, Target Spec, Status)
   - Part 1: Spec Patches ("Spec Update Input" 형식 + Target Section 어노테이션)
   - Part 2: Implementation Plan (표준 구현 계획 형식)
   - Next Steps 섹션

2. **Part 1 상세 형식**:
   - "Spec Update Input" 형식의 완전한 명세
   - Target Section 어노테이션 규칙
   - section-mapping 참조 테이블 (축약본)
   - 상태 마커 규칙

3. **Part 2 상세 형식**:
   - Overview, Scope, Components
   - Phase별 태스크 테이블
   - Task Details (acceptance criteria 포함)
   - Risks & Mitigations
   - Open Questions
   - 모델 추천

4. **파일 관리 규칙**:
   - 파일명: `feature_draft_<feature_name>.md`
   - 아카이브: `prev/prev_feature_draft_<name>_<timestamp>.md`
   - 입력 파일 처리 규칙

**Acceptance Criteria**:
- [ ] Part 1이 spec-update-todo input-format.md와 호환
- [ ] Part 2가 implementation-plan의 출력 형식과 호환
- [ ] 파일 관리 규칙이 기존 스킬과 일관성 유지

---

### Task 8: examples/feature_draft.md 작성

**Component**: Examples
**Priority**: P1
**Type**: Feature
**Dependencies**: 7

**설명**:
완성된 출력의 구체적인 예시 파일을 작성합니다. 실제 프로젝트에서 사용될 수 있는 현실적인 예시로 작성합니다.

**예시 시나리오**: "실시간 알림 시스템" 기능 추가 (spec-draft 예시와 연계)

**Acceptance Criteria**:
- [ ] Part 1과 Part 2 모두 포함
- [ ] 현실적이고 구체적인 내용
- [ ] 모든 포맷 규칙 준수

---

### Task 9: SDD_QUICK_START.md 업데이트

**Component**: Documentation
**Priority**: P2
**Type**: Documentation
**Dependencies**: 8

**설명**:
SDD_QUICK_START.md에 feature-draft 스킬을 추가합니다.

**변경 사항**:
- 스킬 목록에 `feature-draft` 추가
- 워크플로우 다이어그램에 shortcut 경로 추가
- 사용 시나리오 예시 추가

**Acceptance Criteria**:
- [ ] feature-draft가 스킬 목록에 포함됨
- [ ] 기존 워크플로우와 shortcut 워크플로우 모두 표시됨
- [ ] 기존 문서 스타일과 일관성 유지

---

## 위험 요소 및 대응

| 위험 | 영향 | 대응 |
|------|------|------|
| spec-update-todo 입력 형식과 불일치 | Part 1을 spec-update-todo에 넣으면 오류 | input-format.md를 정확히 참조하여 작성 |
| 단일 파일이 너무 길어짐 | 가독성 저하 | 25 태스크 초과 시 Phase별 분리 옵션 제공 |
| 기존 스킬 트리거와 키워드 충돌 | 잘못된 스킬 활성화 | 고유한 트리거 키워드 선정 |
| Adaptive 질문이 너무 적어 품질 저하 | 불완전한 초안 | MEDIUM 레벨에서 핵심 질문 반드시 포함 |

## 미해결 질문

- [x] ~~`feature-draft`가 여러 기능을 한 번에 처리할 수 있어야 하는가?~~ → 복수 기능 지원, 사용자에게 먼저 확인
- [x] ~~파일명 형식~~ → `feature_draft_<feature_name>.md` (lowercase)
- [ ] Part 1과 Part 2 사이의 분리선을 어떻게 명확히 할 것인가? (현재: `---` 구분)

## 모델 추천

이 구현은 주로 **문서 작성 작업**이므로 `sonnet` 모델이 적합합니다.
복잡한 아키텍처 결정이 필요한 경우 `opus`를 고려할 수 있습니다.
