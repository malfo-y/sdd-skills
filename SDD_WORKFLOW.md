# 스펙 기반 개발 (SDD) 워크플로우 가이드

**버전**: 1.3.0
**날짜**: 2026-02-14

Claude와 함께하는 소프트웨어 개발을 위한 SDD 스킬 종합 가이드

---

## 목차

1. [핵심 개념](#1-핵심-개념)
2. [시작하기](#2-시작하기)
3. [구현 및 스펙 유지보수](#3-구현-및-스펙-유지보수)
4. [리뷰 프로세스](#4-리뷰-프로세스)
5. [빠른 참조](#5-빠른-참조)

---

## 1. 핵심 개념

### 스펙 기반 개발(SDD)이란?

스펙 기반 개발(Spec-Driven Development, SDD)은 **스펙 문서**가 소프트웨어 개발 생명주기 전반에 걸쳐 단일 진실 공급원(Single Source of Truth) 역할을 하는 방법론입니다. 코드와 함께 진화하는 살아있는 문서를 유지하여 요구사항과 구현 사이의 간극을 메웁니다.

### SDD 철학

```
┌─────────────────────────────────────────────────────────────────────┐
│                     스펙 = 진실의 단일 공급원                          │
│                                                                      │
│    요구사항 ──→ 스펙 ──→ 계획 ──→ 코드 ──→ 리뷰 ──→ 스펙 업데이트     │
│         ↑                                                    │      │
│         └────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────────┘
```

### 현재 제공 SDD 스킬(13개)

| 스킬 | 트리거 | 목적 |
|------|--------|------|
| **spec-create** | "스펙 생성", "프로젝트 문서화" | 코드 분석 또는 초안에서 스펙 생성 |
| **spec-draft** (레거시) | "스펙 초안", "스펙 드래프트" | 스펙 업데이트 입력(user_draft.md) 초안 생성 (Spec Update Input 포맷) |
| **feature-draft** **(권장)** | "기능 초안", "feature draft" | **통합 스킬**: 스펙 패치 초안 + 구현 계획을 한 번에 생성 |
| **spec-update-todo** (레거시) | "스펙에 기능 추가", "스펙 업데이트" | 스펙에 새 요구사항 추가 |
| **spec-update-done** | "완료 항목 반영", "스펙 동기화" | 구현 변경사항과 스펙 동기화 |
| **spec-review** | "스펙 리뷰", "드리프트 점검" | 보조 검증용 strict 리뷰 (리포트 전용) |
| **spec-summary** | "스펙 요약", "프로젝트 개요" | 스펙의 요약본 생성 (현황 파악용) |
| **spec-rewrite** | "스펙 리라이트", "스펙 정리" | 긴/복잡한 스펙을 구조 재정리(파일 분할/부록 이동) + 이슈 리포트 |
| **pr-spec-patch** | "PR 스펙 패치", "PR 리뷰 준비" | PR과 스펙 비교하여 패치 초안 생성 |
| **pr-review** | "PR 리뷰", "PR 검증" | PR 구현을 스펙 대비 검증 및 판정 |
| **implementation-plan** (레거시) | "구현 계획 생성" | 스펙에서 실행 가능한 작업 생성 |
| **implementation** | "계획 구현", "구현 시작" | TDD 방식으로 작업 실행 |
| **implementation-review** (레거시) | "구현 리뷰", "진행 상황 확인" | 계획 대비 구현 검증 |

### 간소화된 워크플로우 (권장)

`feature-draft`는 기존의 `spec-draft` + `spec-update-todo` + `implementation-plan`을 하나로 통합한 스킬입니다. 이를 통해 기능 추가 워크플로우가 **7단계에서 4단계**로 간소화됩니다:

```
spec-create → feature-draft → implementation → spec-update-done
```

| | 기존 워크플로우 (7단계) | 간소화된 워크플로우 (4단계) |
|---|---|---|
| 1단계 | spec-draft (초안 생성) | **spec-create** (스펙 생성/확인) |
| 2단계 | spec-update-todo (스펙에 추가) | **feature-draft** (패치 초안 + 구현 계획) |
| 3단계 | implementation-plan (계획 수립) | **implementation** (TDD 구현) |
| 4단계 | implementation (구현) | **spec-update-done** (스펙 동기화) |
| 5단계 | implementation-review (리뷰) | — |
| 6단계 | spec-update-done (동기화) | — |
| 7단계 | spec-review (검증) | — |

> **참고**: `implementation` 스킬에 페이즈별 리뷰가 내장되어 있어 별도의 `implementation-review`가 불필요합니다. 기존 워크플로우는 세밀한 단계별 제어가 필요한 경우에 레거시로 사용할 수 있습니다.

### 디렉토리 구조

```
project/
├── _sdd/
│   ├── spec/
	│   │   ├── main.md                   # 메인 스펙 문서 (또는 <project>.md)
	│   │   ├── user_spec.md              # 스펙 업데이트 입력(자유 형식 가능)
	│   │   ├── user_draft.md             # 스펙 업데이트 입력(권장 포맷; spec-draft가 생성)
	│   │   ├── _processed_user_spec.md   # 처리된 입력 (아카이브; spec-update-todo가 rename)
	│   │   ├── _processed_user_draft.md  # 처리된 입력 (아카이브; spec-update-todo가 rename)
	│   │   ├── SUMMARY.md                # 스펙 요약 (spec-summary)
	│   │   ├── SPEC_REVIEW_REPORT.md     # 스펙 리뷰 리포트 (spec-review)
	│   │   ├── DECISION_LOG.md           # (선택) 결정/근거 기록
	│   │   └── prev/                      # 스펙 백업 (PREV_*.md)
│   │
│   ├── pr/
	│   │   ├── spec_patch_draft.md       # PR 기반 스펙 패치 초안 (스펙 반영은 spec-update-todo로)
│   │   ├── PR_REVIEW.md              # PR 리뷰 리포트
│   │   └── prev/                      # PR 리포트 백업 (PREV_*.md)
│   │
│   ├── implementation/
│   │   ├── IMPLEMENTATION_PLAN.md     # 구현 계획 (인덱스/요약; 필요 시 phase 파일로 분할)
│   │   ├── IMPLEMENTATION_PLAN_PHASE_<n>.md     # (선택) phase별 구현 계획
│   │   ├── IMPLEMENTATION_PROGRESS.md           # 진행 상황 추적 (전체/요약)
│   │   ├── IMPLEMENTATION_PROGRESS_PHASE_<n>.md  # (선택) phase별 진행 리포트
│   │   ├── IMPLEMENTATION_REVIEW.md   # 리뷰 결과
│   │   ├── TEST_SUMMARY.md            # 테스트 현황
│   │   ├── user_input.md              # 구현 요청 (입력)
│   │   └── prev/                      # 구현 문서 백업 (PREV_*.md)
│   │
│   ├── drafts/                          # feature-draft 출력
│   │   ├── feature_draft_*.md           # 스펙 패치 + 구현 계획 통합 파일
│   │   └── prev/                        # 아카이브
│   │
│   └── env.md                         # 환경 설정
│
└── src/                               # 소스 코드
```

---

## 2. 시작하기

### 스펙 생성의 시작점

스펙은 두 가지 방식으로 생성할 수 있습니다:

```
┌─────────────────────────────────────────────────────────────────────┐
│                      스펙 생성 시작점                                 │
│                                                                      │
│   ┌─────────────────────┐         ┌─────────────────────┐           │
│   │  A. 기존 코드 분석   │         │  B. 사용자 초안 기반  │           │
│   │                     │         │                     │           │
│   │  • 레거시 프로젝트   │         │  • 기획서 존재       │           │
│   │  • 코드 먼저 개발    │         │  • 요구사항 문서화됨  │           │
│   │  • 문서화 필요       │         │  • 새 프로젝트       │           │
│   └──────────┬──────────┘         └──────────┬──────────┘           │
│              │                               │                       │
│              ▼                               ▼                       │
│   ┌─────────────────────────────────────────────────────┐           │
│   │                    spec-create                       │           │
│   │              → _sdd/spec/main.md 생성                │           │
│   └─────────────────────────────────────────────────────┘           │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

#### A. 기존 코드 분석으로 시작

기존 코드베이스가 있을 때 사용:

```bash
# 코드 분석하여 스펙 생성
/spec-create

# Claude가 다음을 수행:
# 1. 코드베이스 구조 분석
# 2. 컴포넌트 식별
# 3. 아키텍처 파악
# 4. 스펙 문서 생성
```

**적합한 경우:**
- 레거시 프로젝트 문서화
- 코드 먼저 개발 후 문서 작성
- 인수인계를 위한 문서화

#### B. 사용자 초안 기반으로 시작

기획서나 요구사항 문서가 있을 때 사용:

```bash
# 1. 초안/요구사항 입력 준비
# - 간단히 적을 때: _sdd/spec/user_spec.md
# - 권장 포맷으로 만들 때: /spec-draft  (=> _sdd/spec/user_draft.md 생성)

# 2. 스펙 생성 요청
"이 초안을 기반으로 스펙을 생성해줘"
/spec-create
```

**초안 파일 예시:**
```markdown
# 프로젝트 초안

## 목표
사용자 인증이 있는 작업 관리 API 구축

## 필요한 기능
- JWT 기반 로그인/회원가입
- 작업 CRUD
- 마감일 알림

## 기술 스택
- Python + FastAPI
- PostgreSQL
```

**적합한 경우:**
- PM/기획자가 요구사항 제공
- 새 프로젝트 시작
- 명확한 요구사항이 있을 때

---

### 구현 경로 선택

기능의 복잡도와 상황에 따라 경로를 선택합니다:

```
┌─────────────────────────────────────────────────────────────────────┐
│                        구현 경로 선택                                 │
│                                                                      │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │            경로 A: Feature Draft (권장 — 4단계)                 │  │
│  │                                                               │  │
│  │  복잡도: 높음 | 큰 기능, 아키텍처 변경, 문서화 중요             │  │
│  │                                                               │  │
│  │  spec-create → feature-draft → implementation → spec-update-done  │  │
│  │       │            │                │                │        │  │
│  │       ▼            ▼                ▼                ▼        │  │
│  │  스펙 생성/    패치 초안 +     TDD로 구현       스펙 동기화     │  │
│  │  확인          구현 계획                                      │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │        경로 A' (레거시): Spec-First (전체 7단계 프로세스)        │  │
│  │                                                               │  │
│  │  세밀한 단계별 제어가 필요할 때 사용                             │  │
│  │                                                               │  │
│  │  spec-update-todo → implementation-plan → implementation           │  │
│  │       │              │                    │                   │  │
│  │       ▼              ▼                    ▼                   │  │
│  │  스펙에 기능    계획 수립 및      TDD로 구현                    │  │
│  │  추가/업데이트   작업 분해                                     │  │
│  │                                           │                   │  │
│  │                                           ▼                   │  │
│  │  spec-update-done ← implementation-review ←────┘                   │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                  경로 B: Direct Plan (중간 프로세스)             │  │
│  │                                                               │  │
│  │  복잡도: 중간 | 명확한 요구사항, 중간 규모 기능                  │  │
│  │                                                               │  │
│  │  사용자 입력 → implementation-plan → implementation            │  │
│  │       │              │                    │                   │  │
│  │       ▼              ▼                    ▼                   │  │
│  │  "이 기능을     계획 생성           TDD로 구현                  │  │
│  │   구현해줘"                                                    │  │
│  │                                           │                   │  │
│  │                                           ▼                   │  │
│  │  (선택적) spec-update-done ← implementation-review ←───┘            │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                  경로 C: Simple/Direct (간단 프로세스)           │  │
│  │                                                               │  │
│  │  복잡도: 낮음 | 버그 수정, 작은 기능, 긴급 수정                  │  │
│  │                                                               │  │
│  │  사용자 입력 ──────────→ implementation (직접)                  │  │
│  │       │                         │                             │  │
│  │       ▼                         ▼                             │  │
│  │  "이 버그를                 바로 수정                          │  │
│  │   고쳐줘"                                                      │  │
│  │                                 │                             │  │
│  │                                 ▼                             │  │
│  │  (선택적) spec-update-done ← implementation-review ←───┘            │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 경로 선택 가이드

| 상황 | 권장 경로 | 이유 |
|------|----------|------|
| 새로운 대규모 기능 | A: Feature Draft (권장) | 4단계로 문서화 및 구현 완료 |
| 아키텍처 변경 | A: Feature Draft (권장) | 패치 초안 + 구현 계획을 한 번에 |
| 세밀한 단계별 제어 | A' (레거시): Spec-First | 각 단계를 개별 확인 필요 시 |
| 중간 규모 기능 | B: Direct Plan | 계획은 필요하나 스펙 업데이트는 나중에 |
| 명확한 작은 기능 | B: Direct Plan | 계획 수립 후 빠른 구현 |
| 버그 수정 | C: Simple | 바로 수정, 리뷰로 확인 |
| 긴급 핫픽스 | C: Simple | 속도 우선 |
| 간단한 개선 | C: Simple | 오버헤드 최소화 |

---

### 시나리오별 시작하기

#### 시나리오 1: 레거시 프로젝트 문서화

```bash
# 1. 코드 분석으로 스펙 생성
/spec-create
# Claude가 코드베이스를 분석하여 스펙 생성

# 2. 필요시 스펙 보완
/spec-update-todo
```

#### 시나리오 2: 기획서 기반 새 프로젝트

```bash
# 1. 기획서/초안을 user_spec.md에 작성
vim _sdd/spec/user_spec.md

# 2. 스펙 생성
/spec-create

# 3. 기능 초안 + 구현 계획 (통합)
/feature-draft

# 4. 구현 시작
/implementation

# 5. 스펙 동기화
/spec-update-done
```

#### 시나리오 3: 새 기능 추가 (Feature Draft — 권장)

```bash
# 1. 기능 초안 + 구현 계획 (통합)
/feature-draft
# 스펙 패치 초안(Part 1)과 구현 계획(Part 2)을 단일 파일로 생성

# 2. 구현
/implementation

# 3. 스펙 동기화
/spec-update-done
```

#### 시나리오 3': 새 기능 추가 (레거시: Spec-First)

> 세밀한 단계별 제어가 필요한 경우에만 사용합니다.

```bash
# 1. 스펙에 기능 추가
/spec-update-todo

# 2. 구현 계획 수립
/implementation-plan

# 3. 구현
/implementation

# 4. 리뷰
/implementation-review

# 5. 스펙 동기화
/spec-update-done

# 6. (선택) 보조 검증 리뷰
/spec-review
```

#### 시나리오 4: 중간 규모 기능 (Direct Plan)

```bash
# 1. 직접 계획 요청
"로그인 기능을 구현해줘. JWT 기반으로."
/implementation-plan

# 2. 구현
/implementation

# 3. 리뷰
/implementation-review

# 4. (선택적) 스펙 동기화
/spec-update-done
```

#### 시나리오 5: 간단한 버그 수정 (Simple)

```bash
# 1. 직접 수정 요청
"이 파일의 널 포인터 버그를 고쳐줘"

# 2. (선택적) 리뷰
/implementation-review
```

#### 시나리오 6: 스펙 현황 파악 (Spec Status Check)

```bash
# 스펙 요약 생성
/spec-summary
# Claude가 SUMMARY.md 생성 (진행률, 이슈, 추천사항 포함)

# 용도:
# - 스테이크홀더 미팅 전
# - 새 팀원 온보딩
# - 주기적 현황 점검
# - 다음 작업 우선순위 결정
```

---

## 3. 구현 및 스펙 유지보수

### TDD 구현 워크플로우

implementation 스킬은 테스트 주도 개발(TDD)을 사용합니다:

```
┌─────────────────────────────────────────────────────────────────┐
│                    작업별 TDD 사이클                              │
│                                                                  │
│  각 수용 기준(Acceptance Criterion)에 대해:                       │
│                                                                  │
│  ┌─────────┐      ┌─────────┐      ┌──────────┐                │
│  │  RED    │ ───→ │  GREEN  │ ───→ │ REFACTOR │                │
│  │실패하는 │      │테스트를 │      │테스트를   │                │
│  │테스트   │      │통과하는 │      │유지하며   │                │
│  │작성     │      │최소 코드 │      │정리      │                │
│  └─────────┘      └─────────┘      └──────────┘                │
│       │                                   │                     │
│       └────────── 반복 ───────────────────┘                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 스펙 유지보수 전략

#### 구현 중 스펙 업데이트 시점

| 상황 | 조치 |
|------|------|
| 더 나은 접근법 발견 | 진행 상황에 기록, 페이즈 후 스펙 업데이트 |
| 새 요구사항 발견 | `/feature-draft`로 통합 초안 생성 (또는 레거시: `/spec-update-todo`로 스펙에 추가) |
| 계획된 기능 제거 | `/feature-draft`로 패치 초안 생성 (또는 레거시: `/spec-update-todo`로 스펙 업데이트) |
| API 변경 | 스펙의 컴포넌트 상세 업데이트 |
| PR 생성 후 스펙 반영 | `/pr-spec-patch` 생성 → `/pr-review` → (패치 초안을 입력으로) `/spec-update-todo` |
| PR 머지 전 스펙 기반 검증 | `/pr-spec-patch` → `/pr-review`로 검증 후 머지 |
| 결과가 이상하거나 모호함 | `/spec-review`로 보조 검증 (리포트 전용) |
| 대규모 업데이트 직후 최종 점검 | `/spec-update-done` 완료 후 `/spec-review` 실행 권장 |

#### 구현 페이즈 완료 후

```bash
# 스펙과 코드 동기화
/spec-update-done

# (선택) 보조 검증
# 사용자가 이상함을 느끼거나 대규모 업데이트 직후
/spec-review

# Claude가 수행하는 작업:
# 1. 구현 로그 읽기
# 2. 스펙과 실제 코드 비교
# 3. 드리프트 리포트 생성
# 4. 승인 후 스펙 업데이트
```

### 파일 관리

#### 입력 파일

| 파일 | 용도 | 처리 후 |
|------|------|---------|
| `_sdd/spec/user_spec.md` | 사용자 입력 (드래프트 스펙, 새 기능/요구사항 등) | → `_processed_user_spec.md` |
| `_sdd/spec/user_draft.md` | 사용자 입력 (권장 포맷; Spec Update Input) | → `_processed_user_draft.md` |
| `_sdd/pr/spec_patch_draft.md` | PR 기반 스펙 패치 초안 | 스펙 반영은 `/spec-update-todo`로 진행 |
| `_sdd/implementation/user_input.md` | 구현 요청 | → `_processed_user_input.md` |

> 참고: `_sdd/pr/spec_patch_draft.md`의 내용은 그대로 스펙에 자동 반영되지 않습니다.
> 패치 내용을 `_sdd/spec/user_draft.md`(권장) 또는 `_sdd/spec/user_spec.md`로 옮긴 뒤 `/spec-update-todo`를 실행해 반영합니다.

#### PREV 백업 저장 위치 규칙

- `_sdd/spec/prev/PREV_<파일명>_<timestamp>.md`
- `_sdd/pr/prev/PREV_<파일명>_<timestamp>.md`
- `_sdd/implementation/prev/PREV_<파일명>_<timestamp>.md`

`prev/`가 없으면 먼저 생성한 뒤 저장합니다.

#### 버전 히스토리

이전 버전은 자동으로 아카이브됩니다:

```
_sdd/implementation/
├── IMPLEMENTATION_PLAN.md                      # 현재 (인덱스/요약)
├── IMPLEMENTATION_PLAN_PHASE_1.md              # (선택) phase 1 상세 계획
├── IMPLEMENTATION_PROGRESS.md                  # 진행 추적 (전체/요약)
├── IMPLEMENTATION_PROGRESS_PHASE_1.md          # (선택) phase 1 진행 리포트
└── prev/
    ├── PREV_IMPLEMENTATION_PLAN_20260204_150502.md # 이전
    ├── PREV_IMPLEMENTATION_PLAN_20260204_194934.md # 더 이전
    ├── PREV_IMPLEMENTATION_PROGRESS_20260204_150502.md # 이전 진행 추적
    └── PREV_IMPLEMENTATION_PROGRESS_20260204_194934.md # 더 이전 진행 추적
```

### 스펙의 상태 마커

기능 상태 추적을 위한 마커:

| 마커 | 의미 |
|------|------|
| 📋 계획됨 | 아직 구현되지 않음 |
| 🚧 진행중 | 현재 구현 중 |
| ✅ 완료 | 구현 완료 |
| ⏸️ 보류 | 일시 중단 |

스펙 예시:
```markdown
### 주요 기능
1. **데이터 스크래핑**: Apify Actor 연동 ✅
2. **이미지 다운로드**: 병렬 다운로드 지원 ✅
3. **스케줄러 통합**: 예약 실행 📋 계획됨
4. **웹 대시보드**: 모니터링 UI 📋 계획됨
```

---

## 4. 리뷰 프로세스

### 구현 리뷰 (Implementation Review)

> **참고**: `implementation` 스킬에 페이즈별 리뷰가 내장되어 있으므로, 간소화된 워크플로우(경로 A)에서는 별도의 `/implementation-review` 실행이 선택 사항입니다. 레거시 워크플로우(경로 A')나 세밀한 검증이 필요한 경우에 사용합니다.

**사용 시점**: 작업 또는 페이즈 완료 후

```bash
/implementation-review  또는  "진행 상황 확인"
```

**수행 내용**:

1. **인벤토리**: 계획된 모든 작업 나열
2. **검증**: 실제 구현된 내용 확인
3. **평가**: 수용 기준 충족 여부 검증
4. **이슈**: 문제점과 갭 식별
5. **요약**: 다음 단계 제시

**출력 위치**: `_sdd/implementation/IMPLEMENTATION_REVIEW.md`

### 스펙 동기화 (Spec Sync)

**사용 시점**: 구현 변경 후

```bash
/spec-update-done  또는  "스펙 동기화"
```

**수행 내용**:

1. **컨텍스트 수집**: 구현 로그, git 히스토리 읽기
2. **드리프트 식별**: 스펙과 코드 비교
3. **리포트 생성**: 필요한 변경사항 목록
4. **업데이트 적용**: 승인 후 스펙 업데이트

### 보조 스펙 리뷰 (Spec Review, 선택)

**사용 시점**:
- 사용자가 결과에 이상함/모호함을 느낄 때
- 대규모 업데이트를 `/spec-update-done`으로 반영한 직후 최종 검증이 필요할 때

```bash
/spec-review  또는  "스펙 드리프트 점검"
```

**수행 내용**:
1. **리뷰 전용 점검**: 스펙 품질/드리프트 확인
2. **리포트 생성**: `_sdd/spec/SPEC_REVIEW_REPORT.md`에 기록
3. **본문 미수정**: 스펙 파일은 직접 수정하지 않음

**감지되는 드리프트 유형**:

| 유형 | 예시 |
|------|------|
| 아키텍처 | 문서화되지 않은 새 컴포넌트 |
| 기능 | 스펙에 없는 구현된 기능 |
| 이슈 | 해결됐지만 여전히 열려있는 버그 |
| 설정 | 추가된 새 환경 변수 |

### 리뷰 사이클

```
┌─────────────────────────────────────────────────────────────┐
│                      리뷰 사이클                              │
│                                                              │
│    ┌───────────────┐         ┌────────────────┐             │
│    │implementation-│         │  spec-update-done   │             │
│    │    review     │         │                │             │
│    └───────┬───────┘         └────────┬───────┘             │
│            │                          │                      │
│            ▼                          ▼                      │
│    ┌───────────────┐         ┌────────────────┐             │
│    │ 코드를 계획   │         │ 스펙을 코드    │             │
│    │ 대비 검증     │         │ 대비 검증      │             │
│    └───────────────┘         └────────────────┘             │
│            │                          │                      │
│            ▼                          ▼                      │
│    PROGRESS.md 업데이트       SPEC.md 업데이트               │
│    갭 식별                    드리프트 식별                  │
│    다음 단계 제안             문서 동기화                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

필요 시(이상 징후 또는 대규모 변경 직후) `/spec-review`를 추가로 실행해 최종 검증합니다.

---

## 5. 빠른 참조

### 명령어 치트시트

| 명령어 | 사용 시점 |
|--------|----------|
| `/spec-create` | 새 프로젝트 시작 또는 기존 코드 문서화 |
| `/spec-draft` (레거시) | 스펙 업데이트 입력(user_draft.md) 초안 생성 |
| `/feature-draft` **(권장)** | 스펙 패치 초안 + 구현 계획 통합 생성 |
| `/spec-update-todo` (레거시) | 스펙에 새 기능/요구사항 추가 |
| `/spec-update-done` | 구현 변경사항과 스펙 동기화 |
| `/spec-review` | 선택적 보조 검증 (이상 징후/대규모 업데이트 후) |
| `/spec-summary` | 스펙 현황 파악 및 요약본 생성 |
| `/spec-rewrite` | 긴/복잡한 스펙 구조 재정리(파일 분할/부록 이동) |
| `/pr-spec-patch` | PR과 스펙 비교하여 패치 초안 생성 |
| `/pr-review` | PR 구현을 스펙/패치 초안 대비 검증 및 판정 |
| `/implementation-plan` (레거시) | 스펙에서 작업 생성 |
| `/implementation` | TDD로 작업 실행 |
| `/implementation-review` (레거시) | 진행 상황 확인 및 기준 검증 |

### 경로별 워크플로우 요약

#### 경로 A: Feature Draft (권장 — 4단계)

```bash
/spec-create → /feature-draft → /implementation → /spec-update-done
```

#### 경로 A' (레거시): Spec-First (7단계)

```bash
/spec-update-todo → /implementation-plan → /implementation → /implementation-review → /spec-update-done → (필요 시) /spec-review
```

#### 경로 B: Direct Plan (중간)

```bash
사용자 입력 → /implementation-plan → /implementation → /implementation-review → (선택적) /spec-update-done
```

#### 경로 C: Simple (간단)

```bash
사용자 입력 → 직접 구현 → (선택적) /implementation-review
```

### 파일 위치

| 용도 | 기본 경로 |
|------|----------|
| 메인 스펙 | `_sdd/spec/main.md` 또는 `_sdd/spec/<프로젝트>.md` |
| 스펙 입력 | `_sdd/spec/user_spec.md` |
| 스펙 입력(권장 포맷) | `_sdd/spec/user_draft.md` |
| 스펙 요약 | `_sdd/spec/SUMMARY.md` |
| 스펙 리뷰 리포트 | `_sdd/spec/SPEC_REVIEW_REPORT.md` |
| 결정/근거 로그(선택) | `_sdd/spec/DECISION_LOG.md` |
| PR 패치 초안 | `_sdd/pr/spec_patch_draft.md` |
| PR 리뷰 리포트 | `_sdd/pr/PR_REVIEW.md` |
| 구현 계획 (인덱스) | `_sdd/implementation/IMPLEMENTATION_PLAN.md` |
| 구현 계획 (phase 분할 시) | `_sdd/implementation/IMPLEMENTATION_PLAN_PHASE_<n>.md` |
| 진행 추적 (전체/요약) | `_sdd/implementation/IMPLEMENTATION_PROGRESS.md` |
| 진행 추적 (phase 분할 시) | `_sdd/implementation/IMPLEMENTATION_PROGRESS_PHASE_<n>.md` |
| 리뷰 결과 | `_sdd/implementation/IMPLEMENTATION_REVIEW.md` |
| 환경 설정 | `_sdd/env.md` |

### 전체 워크플로우 다이어그램

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SDD 전체 워크플로우                           │
│                                                                      │
│                    ┌──────────────────────┐                         │
│                    │      시작점 선택      │                         │
│                    └──────────┬───────────┘                         │
│                               │                                      │
│              ┌────────────────┼────────────────┐                    │
│              ▼                ▼                ▼                    │
│      ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│      │ 기존 코드    │  │ 사용자 초안  │  │ 직접 요청   │             │
│      │ 분석        │  │ 기반        │  │ (간단한 것) │             │
│      └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
│             │                │                │                     │
│             └────────┬───────┘                │                     │
│                      ▼                        │                     │
│              ┌─────────────┐                  │                     │
│              │ spec-create │                  │                     │
│              └──────┬──────┘                  │                     │
│                     │                         │                     │
│         ┌───────────┼─────────────────────────┤                     │
│         │           │                         │                     │
│         ▼           ▼                         ▼                     │
│   ┌──────────┐ ┌──────────┐           ┌────────────────────┐       │
│   │Feature   │ │Direct    │           │     Simple         │       │
│   │Draft(권장)│ │Plan 경로B│           │     경로 C         │       │
│   │ 경로 A   │ └────┬─────┘           └─────────┬──────────┘       │
│   └────┬─────┘      │                          │                   │
│        │            │                          │                   │
│        ▼            ▼                          │                   │
│   ┌──────────┐ ┌─────────────────┐             │                   │
│   │feature-  │ │implementation-  │             │                   │
│   │  draft   │ │     plan        │             │                   │
│   └────┬─────┘ └────────┬────────┘             │                   │
│        │                │                      │                   │
│        └────────┬───────┘                      │                   │
│                 ▼                               │                   │
│        ┌─────────────────┐                     │                   │
│        │ implementation  │ ←───────────────────┘                   │
│        │    (TDD)        │                                          │
│        └────────┬────────┘                                          │
│                 │                                                   │
│                 ▼                                                   │
│        ┌─────────────────┐                                          │
│        │  spec-update-done    │────────→ (사이클 반복)                    │
│        └─────────────────┘                                          │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 모범 사례

1. **Feature Draft First (가능하면)**: 큰 구현 전에 `/feature-draft`로 패치 초안 + 구현 계획을 한 번에 생성
2. **자주 리뷰**: `implementation` 스킬에 페이즈별 리뷰가 내장되어 있으며, 필요 시 `/implementation-review`로 추가 검증
3. **큰 계획은 phase 분할**: `IMPLEMENTATION_PLAN.md`는 인덱스/요약으로 두고 `IMPLEMENTATION_PLAN_PHASE_<n>.md`로 분할 (진행 리포트도 `IMPLEMENTATION_PROGRESS_PHASE_<n>.md` 사용)
4. **동기화 유지**: 기본은 spec-update-done, 이상 징후/대규모 변경 후에는 spec-review로 보조 검증
5. **히스토리 보존**: 프로젝트 안정화 전까지 `prev/` 아래 PREV_* 파일 삭제 금지
6. **상태 표시**: 스펙에 상태 마커(📋, 🚧, ✅) 사용
7. **테스트 먼저**: implementation 스킬에서 TDD 준수

---

## 부록: 스킬 트리거

### spec-create
- "스펙 생성", "스펙 만들어줘"
- "프로젝트 문서화"
- "SDD 생성"
- "create a spec", "document the project"

### spec-draft (레거시)
- "스펙 초안"
- "스펙 드래프트"
- "스펙 업데이트 입력 만들어줘"
- "draft spec update input", "spec draft"

### feature-draft (권장)
- "기능 초안", "기능 계획"
- "feature draft", "feature plan"
- "초안과 계획", "draft and plan"
- "feature spec and plan"
- "기능 스펙과 계획"

### spec-update-todo (레거시)
> 간소화된 워크플로우에서는 `feature-draft`가 이 역할을 대체합니다.
- "스펙에 기능 추가"
- "스펙 업데이트"
- "요구사항 추가"
- "add features to spec", "update spec"

### spec-update-done
- "완료 항목 반영"
- "스펙 동기화"
- "구현 반영"
- "sync spec with code", "update done items in spec"

### spec-review
- "스펙 리뷰"
- "스펙 드리프트 확인"
- "이상한데 검증해줘"
- "review spec", "spec drift check", "verify spec quality"

### spec-summary
- "스펙 요약"
- "스펙 개요"
- "스펙 현황"
- "프로젝트 개요"
- "현재 상태는"
- "summarize spec", "spec summary", "show spec overview"

### spec-rewrite
- "스펙 리라이트"
- "스펙 정리"
- "스펙을 파일로 쪼개줘"
- "rewrite spec", "refactor spec", "split spec"

### pr-spec-patch
- "PR 스펙 패치"
- "PR 리뷰 준비"
- "스펙 패치 생성"
- "PR 변경사항 스펙 반영"
- "create spec patch from PR", "compare PR with spec"

### pr-review
- "PR 리뷰"
- "PR 검증"
- "스펙 기반 PR 리뷰"
- "PR 승인 검토"
- "review PR", "review PR against spec", "PR review"

### implementation-plan (레거시)
> 간소화된 워크플로우에서는 `feature-draft`가 구현 계획을 포함합니다.
- "구현 계획 생성"
- "구현 계획 만들어줘"
- "계획 수립"
- "create implementation plan"

### implementation
- "계획 구현"
- "구현 시작"
- "작업 실행"
- "implement the plan", "start implementation"

### implementation-review (레거시)
> `implementation` 스킬에 페이즈별 리뷰가 내장되어 있어 별도 실행은 선택 사항입니다.
- "구현 리뷰"
- "진행 상황 확인"
- "뭐가 완료됐어?"
- "review implementation", "check progress"
