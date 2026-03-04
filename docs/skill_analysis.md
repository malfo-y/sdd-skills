# Codex 스킬 정합성 재평가 보고서

- 작성일: 2026-03-04
- 범위: `.codex/skills`의 11개 대상 스킬 + 본 문서
- 대상 스킬:
  - `implementation-plan`
  - `implementation-review`
  - `pr-review`
  - `pr-spec-patch`
  - `spec-create`
  - `spec-review`
  - `spec-rewrite`
  - `spec-summary`
  - `spec-update-done`
  - `spec-update-todo`
  - `feature-draft`

## 1. 평가 프레임

### 1.1 분석 기준 (11개 유지)

| ID | 차원 | 기준 | 판정 질문 |
|---|---|---|---|
| P1 | Purpose | 목적 명확성 | 스킬 목적/트리거가 명확히 정의되어 있는가 |
| P2 | Purpose | 출력 포맷 명세 | 산출물 형식이 구체적으로 제시되어 있는가 |
| P3 | Purpose | Hard Rules 명시 | 금지/제약 규칙이 명확한가 |
| P4 | Purpose | 워크플로우 위치 | 전체 흐름에서의 역할이 정의되어 있는가 |
| O1 | Orchestration | Step별 도구 매핑 | Step 단위로 실행 도구가 명시되어 있는가 |
| O2 | Orchestration | Decision Gates | IF/ELSE 기반 진입/전이 조건이 있는가 |
| O3 | Orchestration | 체크포인트 | 사용자 확인 지점이 정의되어 있는가 |
| O4 | Orchestration | 검증 방법 | 파일/근거/결과를 검증하는 절차가 있는가 |
| O5 | Orchestration | 컨텍스트 관리 | 스펙/코드/PR 크기별 읽기 전략이 있는가 |
| O6 | Orchestration | 점진적 공개 | 요약→상세 공개 전략이 있는가 |
| O7 | Orchestration | 에러 복구 | 실패/예외 상황별 대응이 정의되어 있는가 |

### 1.2 채점 규칙

- `✅`: 기준을 직접 충족(명시적 섹션/표/절차 존재)
- `⚠️`: 부분 충족(핵심은 있으나 누락/약함)
- `❌`: 기준 미충족
- 총점: `✅` 개수(최대 11점)

### 1.3 O1 엄격 판정 규칙 (재명문화)

- `✅` 조건:
  - 번호형 주요 Step(예: Step 1..N)마다 `**Tools**`가 명시됨
  - 도구가 실제 실행 가능한 로컬 체인(`rg/Glob/Read/Bash/Edit/Write/gh`)으로 구성됨
- `⚠️` 조건:
  - 일부 Step만 도구가 있고, 일부는 `도구 불필요`로 처리되어 실행 경로가 약함
- `❌` 조건:
  - Step별 도구 매핑이 거의 없거나, 실사용 불가능한 도구 가정에 의존

## 2. Codex 적합성 별도 축 (C1~C4)

| ID | 항목 | 판정 기준 |
|---|---|---|
| C1 | 도구 실사용 가능성 | 문서의 도구 지시가 Codex에서 실제 실행 가능한가 |
| C2 | 모델/브랜딩 중립성 | Claude 전용 브랜딩 없이 `gpt-5.3-codex + reasoning effort` 규칙과 양립하는가 |
| C3 | deprecated 참조 무결성 | 현재 제거된 스킬/도구 참조가 현행 선택지처럼 남아있지 않은가 |
| C4 | 실행 모드 호환성 | Plan mode(`request_user_input`) / Default mode(직접 질문) 규칙이 적용되는가 |

## 3. 11개 기준 재채점 결과

| Skill | P1 | P2 | P3 | P4 | O1 | O2 | O3 | O4 | O5 | O6 | O7 | Score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| implementation-plan | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **11** |
| implementation-review | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **11** |
| pr-review | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **11** |
| pr-spec-patch | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **11** |
| spec-create | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **11** |
| spec-review | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **10** |
| spec-rewrite | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | **10** |
| spec-summary | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | **9** |
| spec-update-done | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **10** |
| spec-update-todo | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | **9** |
| feature-draft | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **10** |

### 3.1 요약

- 평균 점수: `113 / 11 = 10.27`
- `11/11`: `implementation-plan`, `implementation-review`, `pr-review`, `pr-spec-patch`, `spec-create`
- `10/11`: `spec-review`, `spec-rewrite`, `spec-update-done`, `feature-draft`
- `9/11`: `spec-summary`, `spec-update-todo`

### 3.2 기준별 충족률 (`✅` 기준)

| 기준 | ✅/11 | 비고 |
|---|---|---|
| P1 | 11/11 | 전 스킬 충족 |
| P2 | 11/11 | 전 스킬 충족 |
| P3 | 11/11 | 전 스킬 충족 |
| P4 | 11/11 | 전 스킬 충족 |
| O1 | 6/11 | `pr-review`, `pr-spec-patch` 보강 반영 |
| O2 | 11/11 | 전 스킬 조건 분기 정의 |
| O3 | 11/11 | 전 스킬 확인 지점 존재 |
| O4 | 10/11 | `spec-rewrite`는 체크리스트 중심(부분 충족) |
| O5 | 10/11 | `spec-summary`만 부분 충족 |
| O6 | 10/11 | `spec-update-todo`만 부분 충족 |
| O7 | 11/11 | 전 스킬 에러 처리 존재 |

## 4. 과대평가 가능 항목 재판정 메모

### 4.1 `pr-spec-patch` (재판정: 11)

- O1 `✅`: Step 1~6 + Mode 2 Step 1~4에 `**Tools**` 명시 완료
  - 근거: `pr-spec-patch/SKILL.md`의 각 Step에 도구 라인 추가
- O6 `✅`: Step 6에 `Progressive Disclosure`와 사용자 선택 분기 추가
  - 근거: Step 6 요약 테이블 + 상세 확인 옵션

### 4.2 `pr-review` (재판정: 11)

- O1 `✅`: Mode 1 Step 1~7에 `**Tools**` 명시 완료
  - 근거: `pr-review/SKILL.md`의 각 Step 도구 라인 추가
- O2 `✅`: Step 1→2, 2→3, 5→6, 6→7 Decision Gate 명문화
  - 근거: 단계 전이 조건 블록 추가

### 4.3 `spec-rewrite` (11 → 10)

- O4 `⚠️`: 검증이 주로 품질 체크리스트 중심이며 자동/반자동 검증 절차는 상대적으로 약함
  - 근거: `Quality Checklist` + 일부 링크 검증 지시 (`spec-rewrite/SKILL.md:199,237`)

### 4.4 `spec-update-todo` (11 → 9)

- O1 `⚠️`: `Step 4`가 `Tools: —`로 처리되어 엄격 O1에서 감점
  - 근거: `Step 4: Categorize Updates` (`spec-update-todo/SKILL.md:167,169`)
- O6 `⚠️`: `Plan → Approve → Apply`는 있으나 별도 점진 공개 섹션/선택지 구조는 약함
  - 근거: `Step 5`, `Decision Gate 5→6` (`spec-update-todo/SKILL.md:180,209`)

## 5. Codex 적합성 (C1~C4) 결과

| Skill | C1 | C2 | C3 | C4 |
|---|---|---|---|---|
| implementation-plan | ✅ | ✅ | ✅ | ✅ |
| implementation-review | ✅ | ✅ | ✅ | ✅ |
| pr-review | ✅ | ✅ | ✅ | ✅ |
| pr-spec-patch | ✅ | ✅ | ✅ | ✅ |
| spec-create | ✅ | ✅ | ✅ | ✅ |
| spec-review | ✅ | ✅ | ✅ | ✅ |
| spec-rewrite | ✅ | ✅ | ✅ | ✅ |
| spec-summary | ✅ | ✅ | ✅ | ✅ |
| spec-update-done | ✅ | ✅ | ✅ | ✅ |
| spec-update-todo | ✅ | ✅ | ✅ | ✅ |
| feature-draft | ✅ | ✅ | ✅ | ✅ |

### 5.1 Codex 적합성 요약

- C1/C2/C3/C4 모두 대상 11개 스킬 충족

## 6. 정합화 패치 검증

### 6.1 금칙어/잔여 참조 검사

```bash
rg "AskUserQuestion|codebase-retrieval|TaskCreate|Opus 4.5|Reviewer\*\*: Claude|spec-draft|implementation-sequential|feature-draft-sequential|implementation-plan-sequential|code\.claude\.com" \
  .codex/skills/implementation-plan/SKILL.md \
  .codex/skills/implementation-review/SKILL.md \
  .codex/skills/pr-review/SKILL.md \
  .codex/skills/pr-spec-patch/SKILL.md \
  .codex/skills/spec-create/SKILL.md \
  .codex/skills/spec-review/SKILL.md \
  .codex/skills/spec-rewrite/SKILL.md \
  .codex/skills/spec-summary/SKILL.md \
  .codex/skills/spec-update-done/SKILL.md \
  .codex/skills/spec-update-todo/SKILL.md \
  .codex/skills/feature-draft/SKILL.md
```

- 결과: 대상 스킬 범위에서 잔여 0건

### 6.2 모델 매핑 검사

```bash
rg "Opus|Sonnet|Haiku|reasoning effort" \
  .codex/skills/implementation-plan/SKILL.md \
  .codex/skills/implementation-review/SKILL.md \
  .codex/skills/pr-review/SKILL.md \
  .codex/skills/pr-spec-patch/SKILL.md \
  .codex/skills/spec-create/SKILL.md \
  .codex/skills/spec-review/SKILL.md \
  .codex/skills/spec-rewrite/SKILL.md \
  .codex/skills/spec-summary/SKILL.md \
  .codex/skills/spec-update-done/SKILL.md \
  .codex/skills/spec-update-todo/SKILL.md \
  .codex/skills/feature-draft/SKILL.md
```

- 결과: 매핑 섹션 존재 파일에서 아래 규칙으로 통일
  - `Opus` → `gpt-5.3-codex` (`reasoning effort: extra high`)
  - `Sonnet` → `gpt-5.3-codex` (`reasoning effort: high`)
  - `Haiku` → `gpt-5.3-codex` (`reasoning effort: medium`)

### 6.3 모드 호환성 검사

```bash
rg "request_user_input \(Plan mode\) / direct question \(Default mode\)" .codex/skills/{implementation-plan,implementation-review,pr-review,pr-spec-patch,spec-create,spec-review,spec-rewrite,spec-summary,spec-update-done,spec-update-todo,feature-draft}/SKILL.md
```

- 결과: 대상 11개 스킬 모두 Plan/Default 이중 규칙 반영

## 7. 결론

- 본 라운드의 핵심 목표(1단계 Codex 정합화, 2단계 deprecated 정리, 3단계 재채점/문서 동기화)는 대상 범위 내에서 완료됨.
- 기존 `11/11` 일괄 평가를 유지하지 않고, O1 엄격 규칙을 적용해 `9~11점` 분포로 재산정함.
- 보고서가 이제 `분석 기준 충족(P1~O7)`과 `Codex 적합성(C1~C4)`을 분리해 제시하므로, 문서 품질과 실행 적합성 판단이 분리 가능해짐.
