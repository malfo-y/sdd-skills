# Spec / Implementation / PR 스킬 가이드

이 문서는 현재 저장소의 스킬들을 `spec`, `implementation`, `pr` 3개 그룹으로 나누어 기능과 역할을 정리한 문서입니다.

기준 문서:
- `.claude/skills/*/SKILL.md`
- `SDD_QUICK_START.md`
- `SDD_WORKFLOW.md`

---

## 1. 전체 구조 한눈에 보기

### 1-1. 스킬 그룹별 역할

| 그룹 | 핵심 역할 | 대표 산출물 |
|------|-----------|-------------|
| `spec` | 요구사항/설계 문서 생성, 갱신, 검증, 요약 | `_sdd/spec/*.md` |
| `implementation` | 계획 수립, TDD 구현 실행, 진행 리뷰 | `_sdd/implementation/*.md` |
| `pr` | PR 변경사항을 스펙 관점으로 정리/검증 | `_sdd/pr/*.md` |

### 1-2. 권장 흐름 (Spec-First 기준)

```text
병렬 기본 통합 흐름:
feature-draft -> implementation -> spec-update-done

spec-draft (선택) -> spec-update-todo -> implementation-plan -> implementation -> implementation-review -> spec-update-done -> spec-summary (선택)

PR 단위 흐름:
pr-spec-patch -> pr-review -> (머지 후) spec-update-done

레거시 순차 흐름(필요 시):
feature-draft-sequential -> implementation-sequential -> spec-update-done

레거시 단계 분리 흐름(필요 시):
spec-update-todo -> implementation-plan-sequential -> implementation-sequential -> implementation-review -> spec-update-done
```

---

## 2. 공통 운영 원칙

### 2-1. 공통 하드 룰

- 리뷰/계획/PR 계열 스킬은 대부분 `_sdd/spec/`를 직접 수정하지 않거나(리뷰 전용), 수정 권한이 명확히 제한됩니다.
- 스펙 변경은 보통 `spec-update-todo` 또는 `spec-update-done`에서만 수행합니다.
- 변경 전 백업(`prev/PREV_<...>_<timestamp>.md`)을 남기는 패턴이 반복적으로 사용됩니다.

### 2-2. 표준 경로

- 스펙: `_sdd/spec/`
- 구현 계획/진행/리뷰: `_sdd/implementation/`
- PR 패치/리뷰: `_sdd/pr/`
- 실행 환경 가이드: `_sdd/env.md`

### 2-3. 상태 마커(스펙/요약에서 공통)

| 마커 | 의미 |
|------|------|
| 📋 | 계획됨 |
| 🚧 | 진행중 |
| ✅ | 완료 |
| ⏸️ | 보류 |

---

## 3. Spec 계열 스킬 상세

대상 스킬:
- `spec-create`
- `spec-draft`
- `spec-update-todo`
- `spec-update-done`
- `spec-review`
- `spec-summary`
- `spec-rewrite`

### 3-1. 빠른 비교표

| 스킬 | 주 목적 | 입력 | 출력 | 성격 |
|------|---------|------|------|------|
| `spec-create` | 초기 스펙 생성 | 대화, 코드베이스, 문서 | `_sdd/spec/<project>.md` 또는 `main.md` | 생성 |
| `spec-draft` | 요구사항 수집 초안화 | 사용자 대화/수정 코드 | `_sdd/spec/user_draft.md` | 입력 정리 |
| `spec-update-todo` | 스펙에 계획 항목 추가 | 대화 + `user_spec.md`/`user_draft.md` | 스펙 본문 업데이트 | 계획 반영 |
| `spec-update-done` | 구현 결과를 스펙과 동기화 | 구현 로그 + 코드 diff + 스펙 | 스펙 본문 업데이트 | 완료 반영 |
| `spec-review` | 스펙 품질/드리프트 리뷰만 수행 | 스펙, 구현 문서, 코드 상태 | `_sdd/spec/SPEC_REVIEW_REPORT.md` | 리뷰 전용 |
| `spec-summary` | 비기술/기술 공용 요약 생성 | 스펙 + 구현 진행 문서(선택) | `_sdd/spec/SUMMARY.md` | 커뮤니케이션 |
| `spec-rewrite` | 장문 스펙 구조 개선/분할 | 기존 스펙 + 구현 문서(선택) | 재구성된 스펙 + `REWRITE_REPORT.md` | 문서 리팩토링 |

### 3-2. `spec-create`

핵심 기능:
- 프로젝트 스펙을 처음 만들 때 사용
- 코드 분석/기존 문서/대화 입력을 종합해 `Goal`, `Architecture`, `Component Details`, `Dependencies`, `Issues` 등을 포함한 기본 스펙 생성
- 필요 시 `DECISION_LOG.md`에 의사결정 근거 기록

언제 쓰나:
- 프로젝트 시작 시
- 레거시 코드 문서화 시작 시

산출물:
- 기본: `_sdd/spec/<project-name>.md` 또는 `_sdd/spec/main.md`
- 선택: `_sdd/spec/DECISION_LOG.md`

### 3-3. `spec-draft`

핵심 기능:
- 사용자와 대화하면서 기능 요청/개선/버그를 구조화
- 출력 형식을 `spec-update-todo` 입력 포맷("Spec Update Input")에 맞춤

언제 쓰나:
- 아직 메인 스펙에 반영하기 전, 요구사항을 모으는 단계
- 제품/PO/개발자 간 요구사항 인터뷰 단계

산출물:
- `_sdd/spec/user_draft.md`
- 선택: `_sdd/spec/DECISION_LOG.md` (결정 근거가 생긴 경우)

포인트:
- `spec-draft`는 스펙 본문을 업데이트하지 않고, 업데이트 가능한 입력 파일을 만드는 역할입니다.

### 3-4. `spec-update-todo`

핵심 기능:
- 신규 기능/개선/버그 수정 계획을 현재 스펙에 반영
- 입력 소스(대화, `user_draft.md`, `user_spec.md`)를 파싱해 섹션별로 삽입
- 변경 전 `prev` 백업 생성, 변경 후 버전/수정일/changelog 반영
- 사용한 입력 파일을 `_processed_*`로 rename

언제 쓰나:
- 구현 이전 단계에서 “앞으로 할 일(To-Do)”를 스펙에 반영할 때

산출물:
- 업데이트된 `_sdd/spec/*.md`
- 처리된 입력 파일: `_sdd/spec/_processed_user_draft.md`, `_sdd/spec/_processed_user_spec.md`

주의:
- 스펙이 과도하게 커졌을 때 파일 분할을 제안하는 로직을 포함

### 3-5. `spec-update-done`

핵심 기능:
- 구현 결과(실제 코드/로그/리뷰 결과)를 기준으로 스펙 동기화
- 드리프트(스펙과 실제 불일치) 식별 후 반영
- 필요 시 `DECISION_LOG.md` 갱신

언제 쓰나:
- 구현 페이즈 종료 후
- “코드가 바뀌었으니 스펙도 맞춰야 하는” 시점

산출물:
- 동기화된 `_sdd/spec/*.md`
- 변경 백업: `_sdd/spec/prev/PREV_<...>.md`

핵심 차이(`spec-update-todo` 대비):
- `todo`는 “앞으로 할 일 추가”, `done`은 “이미 구현된 결과 반영”입니다.

### 3-6. `spec-review`

핵심 기능:
- 스펙 품질 및 스펙-코드 정합성을 엄격히 리뷰
- 심각도(`High/Medium/Low`)와 결론(`SPEC_OK`, `SYNC_REQUIRED`, `NEEDS_DISCUSSION`)을 제시

하드 룰:
- 스펙 본문 편집 금지(리뷰 전용)
- 변경 필요사항은 권고로만 작성하고 실제 수정은 `spec-update-done`으로 넘김

산출물:
- `_sdd/spec/SPEC_REVIEW_REPORT.md`

언제 쓰나:
- 대규모 변경 직후 최종 검증
- 품질 감사/드리프트 점검

### 3-7. `spec-summary`

핵심 기능:
- 스펙을 이해관계자 친화적으로 요약
- `What/Why/Status`, 핵심 기능 설명, 아키텍처 개요, 이슈 우선순위, 다음 액션 제시
- 진행률(완료/진행/계획) 계산
- 요청 시 README의 marker block만 안전하게 업데이트

산출물:
- 기본: `_sdd/spec/SUMMARY.md`
- 선택: `README.md` 내 `<!-- spec-summary:start/end -->` 블록

언제 쓰나:
- 세미나/주간 공유/온보딩/현황 보고

### 3-8. `spec-rewrite`

핵심 기능:
- 너무 길거나 복잡한 스펙을 정보구조 중심으로 재작성
- 본문은 핵심 의사결정 중심으로 압축, 장문/중복/부록성 내용은 appendix로 이동
- 계층적 분할(인덱스 + 하위 파일)로 재구성

산출물:
- 재작성된 스펙 파일들
- `_sdd/spec/REWRITE_REPORT.md`

언제 쓰나:
- “스펙이 너무 커서 못 읽겠다” 상태
- 구현 계획 전에 문서 품질을 먼저 정리해야 할 때

---

## 4. Implementation 계열 스킬 상세

대상 스킬:
- `implementation-plan`
- `implementation`
- `implementation-plan-sequential` (레거시)
- `implementation-sequential` (레거시)
- `implementation-review`

### 4-1. 빠른 비교표

| 스킬 | 주 목적 | 입력 | 출력 | 하드 룰 |
|------|---------|------|------|---------|
| `implementation-plan` | 스펙/요구사항을 Target Files 포함 작업 단위로 분해 (병렬 기본) | 스펙 + 대화 + `user_input.md` | `IMPLEMENTATION_PLAN.md` | `_sdd/spec/` 수정 금지 |
| `implementation` | 계획 실행(TDD, 병렬 그룹 기본) | 구현 계획 + 코드베이스 + env | 코드/테스트 + `IMPLEMENTATION_PROGRESS*.md` | `_sdd/spec/` 수정 금지 |
| `implementation-plan-sequential` (레거시) | 스펙/요구사항을 순차 실행용 작업 단위로 분해 | 스펙 + 대화 + `user_input.md` | `IMPLEMENTATION_PLAN.md` | `_sdd/spec/` 수정 금지 |
| `implementation-sequential` (레거시) | 계획 실행(TDD, 순차) | 구현 계획 + 코드베이스 + env | 코드/테스트 + `IMPLEMENTATION_PROGRESS*.md` | `_sdd/spec/` 수정 금지 |
| `implementation-review` | 계획 대비 구현 검증 | 계획/진행 파일 + 코드 + 테스트 결과 | `IMPLEMENTATION_REVIEW.md` | 스펙 본문 수정 금지(리뷰 전용) |

### 4-2. `implementation-plan`

핵심 기능:
- 요구사항을 페이즈/태스크/의존성 단위로 구조화
- 각 태스크에 우선순위, 타입, 수용 기준, 기술 노트 부여
- 리스크/완화책, 오픈 질문까지 포함한 실행 계획 생성

입력 특성:
- 대화가 모호하면 `_sdd/implementation/user_input.md`를 참조
- 처리 후 `_processed_user_input.md`로 rename

산출물:
- 기본: `_sdd/implementation/IMPLEMENTATION_PLAN.md`
- 대형 계획은 `IMPLEMENTATION_PLAN_PHASE_<n>.md`로 분할 가능

### 4-3. `implementation`

핵심 기능:
- 계획을 실제 코드/테스트로 실행
- TDD(`RED -> GREEN -> REFACTOR`)를 수용 기준 단위로 반복
- 페이즈별 진행률과 테스트 수를 리포트

중요 포인트:
- 테스트 프레임워크/관례 파악이 필수
- 실행 전 `_sdd/env.md` 적용
- 스펙 드리프트 발견 시 스펙을 직접 고치지 않고 `spec-update-todo`/`spec-update-done`로 에스컬레이션

산출물:
- 코드 + 테스트
- `_sdd/implementation/IMPLEMENTATION_PROGRESS.md`
- 필요 시 `_sdd/implementation/IMPLEMENTATION_PROGRESS_PHASE_<n>.md`

### 4-4. `implementation-review`

핵심 기능:
- 계획 대비 구현 여부를 증거 기반으로 검증
- 수용 기준별로 `MET / NOT MET / UNTESTED` 판정
- 블로커/품질 이슈/개선 항목 분리
- 즉시 조치해야 할 우선순위 액션 제안

산출물:
- `_sdd/implementation/IMPLEMENTATION_REVIEW.md`

주의:
- 리뷰 결과에서 스펙 수정 필요가 보이면 “제안”만 하고 실제 반영은 spec 계열로 넘김

---

## 5. PR 계열 스킬 상세

대상 스킬:
- `pr-spec-patch`
- `pr-review`

### 5-1. 빠른 비교표

| 스킬 | 목적 | 기준 비교 | 출력 |
|------|------|-----------|------|
| `pr-spec-patch` | PR 변경사항을 스펙 반영 초안으로 변환 | PR vs 현재 스펙 | `_sdd/pr/spec_patch_draft.md` |
| `pr-review` | PR 구현을 수용 기준/스펙 기준으로 판정 | PR vs 스펙 + 패치 초안 | `_sdd/pr/PR_REVIEW.md` |

### 5-2. `pr-spec-patch`

핵심 기능:
- `gh` CLI로 PR 메타데이터/디프를 수집
- 변경사항을 `New Features / Improvements / Bug Fixes / Component Changes / Config Changes`로 구조화
- 결과를 `spec-update-todo` 호환 포맷으로 생성

하드 룰:
- `_sdd/spec/` 직접 수정 금지
- 산출물은 오직 `_sdd/pr/spec_patch_draft.md`

언제 쓰나:
- PR 머지 전, “이 PR을 스펙에 어떻게 반영할지” 먼저 정리할 때

### 5-3. `pr-review`

핵심 기능:
- 패치 초안의 수용 기준을 PR 구현/테스트와 대조
- 기존 스펙 위반 여부, 테스트 갭, 문서 갭까지 함께 분석
- 최종 판정: `APPROVE` / `REQUEST CHANGES` / `NEEDS DISCUSSION`

모드:
- Preferred: 패치 초안 있음(정확도 높음)
- Degraded: 패치 초안 없음(PR diff 기반 추론 리뷰)

하드 룰:
- `_sdd/spec/` 직접 수정 금지
- 변경 필요사항은 리뷰 리포트의 권고로만 제시

산출물:
- `_sdd/pr/PR_REVIEW.md`

---

## 6. 핵심 메시지

### 6-1. 각 그룹의 책임 경계

- `spec`: “무엇을/왜”를 문서로 정의하고 갱신
- `implementation`: “어떻게”를 계획하고 TDD로 구현/검증
- `pr`: 변경 단위(PR)를 스펙 계약 관점에서 검증

### 6-2. 자주 생기는 혼동 정리

- `spec-update-todo` vs `spec-update-done`
  - `todo`: 구현 전 계획 반영
  - `done`: 구현 후 실제 반영
- `spec-review` vs `spec-update-done`
  - `review`: 리포트만 생성
  - `update-done`: 실제 스펙 수정 수행
- `pr-spec-patch` vs `pr-review`
  - `spec-patch`: 반영 초안 생성
  - `pr-review`: 품질/수용기준 판정

### 6-3. 팀 적용 최소 루프

```text
(요구 수집) spec-draft
-> (스펙 반영) spec-update-todo
-> (계획) implementation-plan
-> (구현) implementation
-> (검증) implementation-review
-> (동기화) spec-update-done
-> (공유) spec-summary
```

PR 중심으로는:

```text
pr-spec-patch -> pr-review -> merge -> spec-update-done
```

---

## 7. 부록: 스킬별 대표 산출물 경로

| 스킬 | 대표 산출물 |
|------|-------------|
| `spec-create` | `_sdd/spec/<project>.md` 또는 `_sdd/spec/main.md` |
| `spec-draft` | `_sdd/spec/user_draft.md` |
| `spec-update-todo` | `_sdd/spec/*.md` (업데이트) |
| `spec-update-done` | `_sdd/spec/*.md` (동기화 업데이트) |
| `spec-review` | `_sdd/spec/SPEC_REVIEW_REPORT.md` |
| `spec-summary` | `_sdd/spec/SUMMARY.md` |
| `spec-rewrite` | `_sdd/spec/REWRITE_REPORT.md` + 재구성된 스펙 파일 |
| `implementation-plan` | `_sdd/implementation/IMPLEMENTATION_PLAN.md` |
| `implementation` | 코드/테스트 + `_sdd/implementation/IMPLEMENTATION_PROGRESS*.md` |
| `implementation-review` | `_sdd/implementation/IMPLEMENTATION_REVIEW.md` |
| `pr-spec-patch` | `_sdd/pr/spec_patch_draft.md` |
| `pr-review` | `_sdd/pr/PR_REVIEW.md` |
