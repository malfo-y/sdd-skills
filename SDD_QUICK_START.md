# SDD 빠른 시작 가이드

스펙 기반 개발(Spec-Driven Development) 빠른 참조

---

## 사용 가능한 스킬

| 스킬 | 트리거 | 용도 |
|------|--------|------|
| `/spec-create` | "스펙 생성" | 코드 분석 또는 초안에서 스펙 생성 |
| `/spec-update-todo` | "스펙에 기능 추가" | 새 기능/요구사항을 스펙에 추가 |
| `/spec-update-done` | "스펙 동기화" | 구현 후 스펙과 코드 동기화 |
| `/spec-review` | "스펙 리뷰", "드리프트 점검" | 선택적 보조 검증 (리포트 전용, 스펙 본문 미수정) |
| `/pr-spec-patch` | "PR 스펙 패치" | PR과 스펙 비교하여 패치 초안 생성 |
| `/pr-review` | "PR 리뷰" | PR 구현을 스펙/패치 초안 대비 검증 및 판정 |
| `/implementation-plan` | "구현 계획 생성" | 스펙에서 실행 가능한 작업 생성 |
| `/implementation` | "구현 시작" | TDD로 작업 실행 |
| `/implementation-review` | "진행 상황 확인" | 계획 대비 구현 검증 |

---

## 스펙 생성 시작점

```
┌─────────────────────┐         ┌─────────────────────┐
│  A. 기존 코드 분석   │         │  B. 사용자 초안 기반  │
│  • 레거시 프로젝트   │         │  • 기획서 존재       │
│  • 문서화 필요       │         │  • 새 프로젝트       │
└──────────┬──────────┘         └──────────┬──────────┘
           │                               │
           └───────────────┬───────────────┘
                           ▼
                    ┌─────────────┐
                    │ spec-create │
                    └─────────────┘
```

---

## 구현 경로 선택

| 경로 | 복잡도 | 사용 시점 | 워크플로우 |
|------|--------|----------|-----------|
| **A: Spec-First** | 높음 | 큰 기능, 아키텍처 변경 | spec-update-todo → plan → impl → review → spec-update-done |
| **B: Direct Plan** | 중간 | 명확한 중간 규모 기능 | 입력 → plan → impl → review → (선택) spec-update-done |
| **C: Simple** | 낮음 | 버그 수정, 작은 기능 | 입력 → 직접 구현 → review |

### spec-review 사용 원칙 (선택)

- 기본 루프에서는 `/spec-update-done`으로 동기화합니다.
- `/spec-review`는 아래 경우에만 보조적으로 사용합니다:
  - 결과가 이상하거나 모호하다고 느낄 때
  - 대규모 업데이트를 `/spec-update-done`까지 완료한 뒤 최종 검증할 때

---

## 빠른 시작 시나리오

### 1. 레거시 프로젝트 문서화

```bash
/spec-create
```

### 2. 기획서 기반 새 프로젝트

```bash
# 초안 작성 후
/spec-create → /implementation-plan → /implementation
```

### 3. 새 기능 추가 (Spec-First)

```bash
/spec-update-todo → /implementation-plan → /implementation → /implementation-review → /spec-update-done → (필요 시) /spec-review
```

### 4. 중간 규모 기능 (Direct Plan)

```bash
"이 기능을 구현해줘" → /implementation-plan → /implementation → /implementation-review → (선택적) /spec-update-done
```

### 5. 버그 수정 (Simple)

```bash
"이 버그를 고쳐줘" → (선택적) /implementation-review
```

### 6. PR 기반 스펙 패치 및 리뷰

```bash
/pr-spec-patch → (대화로 정제) → /pr-review → (수정 후 재리뷰) → 머지 → /spec-update-done → (필요 시) /spec-review
```

---

## 디렉토리 구조

```
_sdd/
├── spec/
│   ├── apify_ig.md              # 메인 스펙
│   ├── user_spec.md             # 사용자 입력
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

| 상황 | 권장 경로 |
|------|----------|
| 새로운 대규모 기능 | A: Spec-First |
| 아키텍처 변경 | A: Spec-First |
| 중간 규모 기능 | B: Direct Plan |
| 버그 수정 | C: Simple |
| 긴급 핫픽스 | C: Simple |

---

## 자세한 내용

전체 워크플로우 가이드: `SDD_WORKFLOW.md`
