# SDD 빠른 시작 가이드

스펙 기반 개발(Spec-Driven Development) 빠른 참조

---

> **두 단계 스펙 구조**: SDD는 **글로벌 스펙**(main.md = Single Source of Truth)과 **임시 스펙**(feature_draft, spec_patch_draft = 변경 제안서)으로 문서를 관리합니다. 임시 스펙을 먼저 만들고, 검증 후 글로벌 스펙에 병합합니다. 상세: [SDD_CONCEPT.md](SDD_CONCEPT.md)

> **스펙의 정의**: SDD에서 스펙은 단순한 매뉴얼이 아니라, 배경/동기, 핵심 설계, 기대 결과, 코드 근거를 함께 담는 화이트페이퍼형 기준 문서입니다. 상세: [SDD_SPEC_DEFINITION.md](SDD_SPEC_DEFINITION.md)

> **스킬 사용의 핵심**: 스킬은 구조화된 워크플로우 템플릿이지, 마법이 아닙니다. **입력의 질이 출력의 질을 결정합니다.** 스킬을 호출할 때 **What**(무엇을 만들 것인지), **Why**(왜 필요한지), **Constraints**(제약조건/경계조건)를 명시하세요.
>
> 스킬별 좋은/나쁜 입력 비교 예시와 상세 가이드: [SDD_WORKFLOW.md > 2. 효과적인 스킬 사용법](SDD_WORKFLOW.md#2-효과적인-스킬-사용법)

---

## 사용 가능한 스킬

각 스킬의 트리거 키워드와 사용 예시는 [SDD_WORKFLOW.md > 부록: 스킬별 설명](SDD_WORKFLOW.md#부록-스킬별-설명)을 참고하세요.

| 스킬 | 용도 |
|------|------|
| `/spec-create` | 코드 분석 또는 초안에서 스펙 생성 |
| `/feature-draft` | 스펙 패치 초안 + 구현 계획을 한 번에 생성 |
| `/spec-update-todo` | 스펙에 새 기능/요구사항을 사전 반영 (대규모 구현 시 드리프트 방지) |
| `/spec-update-done` | 구현 후 스펙과 코드 동기화 |
| `/spec-review` | 선택적 보조 검증 (리포트 전용, 스펙 본문 미수정) |
| `/spec-summary` | 스펙 요약본 생성(현황 파악/온보딩) |
| `/spec-rewrite` | 너무 긴/복잡한 스펙을 구조 재정리(파일 분할/부록 이동) |
| `/spec-upgrade` | 구 형식 스펙을 whitepaper §1-§8 형식으로 변환 (migration) |
| `/pr-spec-patch` | PR과 스펙 비교하여 패치 초안 생성 |
| `/pr-review` | PR 구현을 스펙/패치 초안 대비 검증 및 판정 |
| `/implementation-plan` | phase별 구현 계획 생성 (대규모 구현 시) |
| `/implementation` | TDD 기반 구현 실행 |
| `/implementation-review` | 계획 대비 구현 검증 (대규모 phase별 검증) |
| `/ralph-loop-init` | 장시간 실행 프로세스 자동 디버그 루프 생성 |
| `/discussion` | 구조화 의사결정 토론: 맥락 수집 + 선택지 비교 + 결정/미결/실행항목 정리 |
| `/guide-create` | 스펙+코드 기반 기능별 구현/리뷰 가이드 문서 생성 |
| `/sdd-autopilot` | 전체 SDD 파이프라인 자율 오케스트레이션 |

### 언제 `/discussion`을 먼저 쓰나

- 요구사항/방향이 아직 모호할 때
- 기술 선택지 트레이드오프를 빠르게 합의해야 할 때
- 구현 전에 리스크/검증 포인트를 정리할 때

출력: 핵심 논점, 결정 사항, 미결 질문, 실행 항목, (선택) Save Handoff

---

## 스펙 생성 시작점

```mermaid
flowchart LR
    A["A. 기존 코드 분석<br/>• 기존 프로젝트<br/>• 문서화 필요"]:::choice
    B["B. 사용자 초안 기반<br/>• 기획서 존재<br/>• 새 프로젝트"]:::choice
    SC["spec-create"]:::action
    Out["_sdd/spec/main.md 생성"]:::output

    A --> SC
    B --> SC
    SC --> Out

    classDef choice fill:#E3F2FD,stroke:#1565C0,stroke-width:2px,color:#0D47A1;
    classDef action fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px,color:#1B5E20;
    classDef output fill:#F5F5F5,stroke:#616161,stroke-width:1.5px,color:#212121;
```

---

## 구현 경로 선택

대부분의 기능 구현은 `/sdd-autopilot`으로 시작하면 됩니다. 방향이 불확실하면 `/discussion`으로 먼저 정리한 뒤 `/sdd-autopilot`을 호출합니다.

```bash
# 방향이 명확할 때
/sdd-autopilot 이 기능 구현해줘: [기능 설명]

# 방향이 불확실할 때
/discussion → (합의 후) → /sdd-autopilot
```

개별 스킬을 수동으로 조합하고 싶다면 아래 규모별 경로를 사용합니다:

| 규모 | 워크플로우 |
|------|-----------|
| **대규모** | feature-draft → spec-update-todo → implementation-plan → implementation (phase 반복) → implementation-review → spec-update-done (→ spec-review) |
| **중규모** | feature-draft → implementation → spec-update-done |
| **소규모** | 직접 구현 (→ implementation-review) (→ spec-update-done) |

> **참고**: 스펙이 없는 경우 먼저 `/spec-create`로 스펙을 생성합니다.

### spec-review 사용 원칙 (선택)

- 기본 루프에서는 `/spec-update-done`으로 동기화합니다.
- `/spec-review`는 아래 경우에만 보조적으로 사용합니다:
  - 결과가 이상하거나 모호하다고 느낄 때
  - 대규모 업데이트를 `/spec-update-done`까지 완료한 뒤 최종 검증할 때
  - 결과물: `_sdd/spec/SPEC_REVIEW_REPORT.md` (리포트만 생성)

---

## 빠른 시작 시나리오

### 1. 기존 프로젝트 문서화

```bash
/spec-create
# 코드베이스를 분석하여 스펙 생성
```

### 2. 구현 전 의사결정 토론

```bash
/discussion
# 토픽 선택 → 맥락 수집 → 반복 질문 → 요약 출력
```

후속 스킬 연결:
- `/feature-draft`: 합의된 방향으로 기능 초안 작성
- `/implementation-plan`: 결정된 구조로 phase 계획 수립
- `/spec-create`: 요구사항이 정리된 새 프로젝트 스펙 생성

> 토론 결과 요약은 사용자 선택에 따라 `_sdd/discussion/discussion_<title>.md`로 저장할 수 있습니다.

### 3. 자동 오케스트레이션 (Autopilot) — 추천

대부분의 기능 구현에서 **기본 경로**입니다. 스킬 조합을 자동으로 판단하여 전체 파이프라인을 실행합니다.

```bash
/sdd-autopilot
이 기능 구현해줘: [기능 설명]
# 요구사항 분석부터 스펙 동기화까지 전체 파이프라인을 자동 실행
```

> 개별 스킬을 수동으로 조합하고 싶다면 아래 시나리오 4~6을 참고하세요.

### 4. 대규모 기능 구현 (수동)

```bash
# 1. 스펙 패치 초안 + 구현 계획 생성
/feature-draft

# 2. 스펙에 사전 반영 (드리프트 방지)
/spec-update-todo

# 3. phase별 구현 계획 수립
/implementation-plan

# 4. 구현 (phase별 반복)
/implementation

# 5. phase별 검증
/implementation-review

# 6. 스펙 동기화
/spec-update-done

# 7. (선택) 최종 보조 검증
/spec-review
```

> 스펙이 없으면 먼저 `/spec-create`를 실행합니다.

### 5. 중규모 기능 구현 (수동)

```bash
# 1. 스펙 패치 초안 + 구현 계획 생성
/feature-draft

# 2. 구현
/implementation

# 3. 스펙 동기화
/spec-update-done
```

> `feature-draft`가 스펙 패치 초안(Part 1)과 구현 계획(Part 2)을 한 번에 생성하므로 별도의 `implementation-plan`이 불필요합니다.

### 6. 소규모 / 버그 수정

```bash
# 1. 직접 수정 요청
"이 버그를 고쳐줘"

# 2. (선택) 검증
/implementation-review

# 3. (선택) 스펙에 영향 있으면 동기화
/spec-update-done
```

### 7. 장시간 실행 디버그 루프

```bash
/ralph-loop-init
# ralph/ 디렉토리에 자동 디버그 루프 구조 생성
```

> LLM 기반 자동 ML 트레이닝 디버깅을 위한 루프 구조를 생성합니다.

### 8. PR 기반 스펙 패치 및 리뷰

```bash
/pr-spec-patch → (대화로 정제) → /pr-review → (스펙 반영은 /spec-update-todo) → (필요 시) /spec-update-done
```

**중요 규칙(스킬 기준)**: PR에서 나온 스펙 변경사항 반영은 **반드시** `/spec-update-todo`로 진행합니다.
(`_sdd/pr/spec_patch_draft.md` 내용을 `_sdd/spec/user_draft.md` 또는 `_sdd/spec/user_spec.md`로 옮겨서 실행)

### 9. 기능 가이드 생성

```bash
/guide-create
# 스펙과 코드를 분석하여 기능별 구현/리뷰 가이드 문서 생성
# 출력: _sdd/guides/guide_<slug>.md
```

> 스펙이 있으면 스펙 기반으로, 코드만 있으면 Low 신뢰도로 가이드를 생성합니다.

### 10. 스펙 현황 파악

```bash
/spec-summary
# SUMMARY.md 생성 (진행률, 이슈, 추천사항 포함)
```

---

## 디렉토리 구조

```
_sdd/
├── spec/
│   ├── main.md                  # 메인 스펙 (또는 <project>.md)
│   ├── user_spec.md             # 스펙 업데이트 입력(자유 형식 가능)
│   ├── user_draft.md            # 스펙 업데이트 입력(권장 포맷)
│   ├── _processed_user_spec.md  # 처리된 입력 아카이브(/spec-update-todo가 rename)
│   ├── _processed_user_draft.md # 처리된 입력 아카이브(/spec-update-todo가 rename)
│   ├── SUMMARY.md               # 스펙 요약(/spec-summary)
│   ├── SPEC_REVIEW_REPORT.md    # 스펙 리뷰 리포트(/spec-review)
│   ├── DECISION_LOG.md          # (선택) 결정/근거 기록
│   └── prev/                    # PREV_* 백업
│
├── pr/
│   ├── spec_patch_draft.md      # PR 기반 스펙 패치 초안
│   ├── PR_REVIEW.md             # PR 리뷰 리포트
│   └── prev/                    # PREV_* 백업
│
├── implementation/
│   ├── IMPLEMENTATION_PLAN.md   # 구현 계획
│   ├── IMPLEMENTATION_PROGRESS.md
│   ├── IMPLEMENTATION_REVIEW.md
│   ├── user_input.md            # 구현 요청 (입력)
│   └── prev/                    # PREV_* 백업
│
├── drafts/                      # feature-draft 출력
│   ├── feature_draft_*.md       # 스펙 패치 + 구현 계획 통합 파일
│   └── prev/                    # 아카이브
│
├── guides/                      # guide-create 출력
│   ├── guide_<slug>.md          # 기능별 구현/리뷰 가이드
│   └── prev/                    # PREV_* 백업
│
└── env.md                       # 환경 설정
```

백업 파일은 각 영역의 `prev/`에 저장:
- `_sdd/spec/prev/PREV_<파일명>_<timestamp>.md`
- `_sdd/pr/prev/PREV_<파일명>_<timestamp>.md`
- `_sdd/implementation/prev/PREV_<파일명>_<timestamp>.md`

---

## 상태 마커

| 마커 | 의미 |
|------|------|
| 📋 | 계획됨 (Planned) |
| 🚧 | 진행중 (In Progress) |
| ✅ | 완료 (Completed) |
| ⏸️ | 보류 (On Hold) |

---

## 경로 선택 가이드

| 상황 | 경로 |
|------|------|
| 대규모 기능, 아키텍처 변경 | 대규모 |
| 중간 규모 기능 | 중규모 |
| 버그 수정, 긴급 핫픽스 | 소규모 |
| 장시간 실행 디버그 (ML, e2e, 빌드 등) | ralph-loop-init |
| **전체 자동화 (추천)** | **sdd-autopilot** |

---

## 자세한 내용

전체 워크플로우 가이드: `SDD_WORKFLOW.md`
