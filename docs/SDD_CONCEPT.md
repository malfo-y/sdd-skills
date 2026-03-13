# SDD 핵심 컨셉: 두 단계 스펙 구조

스펙 기반 개발(SDD)을 처음 접하는 사용자를 위한 핵심 컨셉 안내

---

## 1. SDD란? — CLAUDE.md를 대체하는 글로벌 스펙

일반적으로 Claude Code 프로젝트에서는 `CLAUDE.md`에 프로젝트 컨텍스트를 적습니다. 하지만 프로젝트가 커지면 `CLAUDE.md`만으로는 아키텍처, 컴포넌트 상세, 요구사항, 이슈 추적 등을 담기 어렵습니다.

SDD에서는 `CLAUDE.md`를 **포인터**로만 사용하고, 실질적인 프로젝트 문서는 **글로벌 스펙** (`_sdd/spec/main.md`)에 담습니다.

```
CLAUDE.md                          _sdd/spec/main.md (글로벌 스펙)
┌─────────────────────┐            ┌─────────────────────────────┐
│ "프로젝트 스펙 문서는 │            │ Goal, Architecture,         │
│  _sdd/spec/를 기준   │──가리킴──▶│ Component Details,          │
│  으로 확인합니다"     │            │ Issues, Usage Examples ...  │
└─────────────────────┘            └─────────────────────────────┘
    포인터 (간략)                      Single Source of Truth (상세)
```

**글로벌 스펙이 하는 일:**
- 프로젝트의 목표, 아키텍처, 컴포넌트 상세를 문서화
- 모든 SDD 스킬이 이 문서를 기준으로 판단
- 코드와 함께 진화하는 살아있는 문서 (구현 후 동기화)

스펙 자체를 어떤 문서로 정의하는지에 대한 설명은 [SDD_SPEC_DEFINITION.md](SDD_SPEC_DEFINITION.md)를 참고하세요.

---

## 2. 두 단계 스펙 구조 — Git 브랜치처럼 생각하기

SDD에서 글로벌 스펙은 **직접 수정하지 않습니다**. 대신 **임시 스펙**(구현의 청사진)을 먼저 만들고, 검증한 뒤, 그 스펙에 맞춰 기능을 구현하고, 완료 후 글로벌 스펙에 병합합니다.

임시 스펙은 단순한 "문서 변경 제안서"가 아닙니다. **기능을 구현하기 위한 청사진**입니다. 임시 스펙에는 무엇을 만들지(스펙 패치)와 어떻게 만들지(구현 계획)가 함께 담깁니다.

이 구조는 Git 브랜치와 같은 원리입니다:

```
Git 워크플로우                      SDD 워크플로우
─────────────                      ─────────────

main 브랜치          ←→           글로벌 스펙 (main.md)
  │                                   │
  ├─ feature branch  ←→           임시 스펙 (feature_draft, spec_patch_draft)
  │    │                               │
  │    ├─ 개발        ←→           구현 (/implementation)
  │    │                               │
  │    └─ PR 리뷰    ←→           사용자 검증
  │         │                          │
  └─ merge  ←────────→           글로벌 스펙에 병합 (spec-update-done)
       │                               │
  branch 삭제         ←→           아카이브 (_processed_*, prev/)
```

**왜 직접 수정하지 않는가?**
- **구현 기반 확보**: 임시 스펙이 구현의 청사진 역할을 하므로, 구현 전에 명확한 기준이 생김
- **변경 추적**: 무엇이 왜 바뀌었는지 기록이 남음
- **사용자 검증**: 구현 전에 변경 내용을 확인할 수 있음
- **원본 보존**: 문제가 생기면 이전 버전(`prev/`)으로 복구 가능

---

## 3. 임시 스펙의 생명주기

임시 스펙은 생성되고, 검증을 거쳐, **그 스펙에 맞춰 기능을 구현**한 뒤, 글로벌 스펙에 병합되고 아카이브됩니다.

```
생성               검증              구현               병합               아카이브
─────             ─────             ─────             ─────              ─────

/feature-draft → 사용자 확인  → /implementation → /spec-update-done → prev/로 이동
  feature_draft     (대화로 정제)    코드 구현           main.md 업데이트
```

규모에 따라 두 가지 경로가 있습니다:

### 중규모: 구현 후 병합

가장 기본적인 흐름입니다. 임시 스펙을 만들고, 구현한 뒤, 결과를 글로벌 스펙에 반영합니다.

```
/feature-draft → 사용자 검증 → /implementation → /spec-update-done
  (청사진 생성)    (내용 확인)    (코드 구현)       (글로벌 스펙에 결과 반영)
```

1. `/feature-draft` → `_sdd/drafts/feature_draft_<name>.md` 생성 (스펙 패치 + 구현 계획)
2. 사용자가 내용 확인 및 정제
3. `/implementation` → 임시 스펙을 기준으로 코드 구현
4. `/spec-update-done` → 구현 결과를 글로벌 스펙에 반영

### 대규모: 사전 반영 후 구현

대규모 기능은 임시 스펙을 먼저 글로벌 스펙에 **계획 상태로 사전 반영**한 뒤 구현합니다. 장기간 구현하는 동안 글로벌 스펙과의 드리프트를 방지하기 위한 경로입니다.

```
/feature-draft → /spec-update-todo → /implementation-plan → /implementation → /spec-update-done
  (청사진 생성)    (글로벌 스펙에        (phase별 계획)        (코드 구현)       (상태를 ✅완료로)
                   📋계획됨으로 반영)
```

1. `/feature-draft` → 임시 스펙 생성
2. `/spec-update-todo` → 글로벌 스펙에 계획 상태(📋)로 사전 반영
3. `/implementation-plan` → phase별 상세 구현 계획 수립
4. `/implementation` → phase별 구현 (반복)
5. `/spec-update-done` → 구현 완료된 항목의 상태를 ✅완료로 업데이트

> **차이점 요약**: 중규모는 구현이 끝난 뒤 글로벌 스펙에 반영하고, 대규모는 구현 전에 계획을 먼저 글로벌 스펙에 등록합니다.

### PR 기반 스펙 반영

PR에서 발생한 변경사항을 스펙에 반영하는 경로입니다.

1. `/pr-spec-patch` → `_sdd/pr/spec_patch_draft.md` 생성
2. 사용자가 내용 확인 및 정제
3. 패치 내용을 `_sdd/spec/user_draft.md`로 옮김
4. `/spec-update-todo` → 글로벌 스펙에 병합

---

## 4. 스펙 파일 구분 — 영구 vs 임시

`_sdd/` 아래 파일들은 **영구 문서**와 **임시 입력**으로 구분됩니다.

### 영구 문서 (항상 유지)

| 파일 | 역할 |
|------|------|
| `_sdd/spec/main.md` | 글로벌 스펙 (Single Source of Truth) |
| `_sdd/spec/DECISION_LOG.md` | 결정 사항과 근거 기록 |
| `_sdd/spec/SUMMARY.md` | 스펙 요약 (spec-summary가 생성) |
| `_sdd/spec/prev/PREV_*.md` | 이전 버전 백업 |
| `_sdd/env.md` | 환경 설정 가이드 |

### 임시 입력 (생성 → 처리 → 아카이브)

| 파일 | 역할 | 처리 후 |
|------|------|---------|
| `_sdd/spec/user_draft.md` | 사용자 입력 (권장 포맷) | `_processed_user_draft.md` |
| `_sdd/spec/user_spec.md` | 사용자 입력 (자유 형식) | `_processed_user_spec.md` |
| `_sdd/drafts/feature_draft_*.md` | 기능 초안 (패치+계획) | `_sdd/drafts/prev/`로 이동 |
| `_sdd/pr/spec_patch_draft.md` | PR 기반 패치 초안 | `_sdd/pr/prev/`로 이동 |

### 핵심 규칙

- **영구 문서**는 정해진 스킬만 수정할 수 있음 (`spec-update-todo`, `spec-update-done`)
- **임시 입력**은 처리 후 반드시 아카이브됨 (재처리 방지)
- **이전 버전**은 프로젝트 안정화 전까지 삭제 금지

---

## 요약

```
CLAUDE.md (포인터)
    │
    ▼
글로벌 스펙 (main.md) ◀──── Single Source of Truth
    ▲                          │
    │ 병합                     │ 참조
    │                          ▼
임시 스펙 (청사진) ────→ 구현 ────→ 글로벌 스펙에 반영
(feature_draft)         (코드 작성)    (spec-update-done)
```

자세한 워크플로우와 스킬 사용법: [SDD_WORKFLOW.md](SDD_WORKFLOW.md)
