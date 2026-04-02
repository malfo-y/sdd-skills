---
name: sdd-autopilot
description: "적응형 오케스트레이터 메타스킬. /sdd-autopilot으로 호출하여 요구사항 분석부터 스펙 동기화까지 end-to-end SDD 파이프라인을 자율 실행한다."
version: 2.3.0
---

# SDD Autopilot -- 적응형 오케스트레이터 메타스킬

## Acceptance Criteria
> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.
- [ ] AC1: 8-step pipeline(Step 0~8)이 순서대로 실행 완료되었다 (부분 파이프라인은 해당 범위 내 완료)
- [ ] AC2: orchestrator SKILL.md가 `.claude/skills/orchestrator_<topic>/`에 생성되고, 검증(12항목)을 통과했다
- [ ] AC3: orchestrator 기반 Phase 2 자율 실행이 완료되었다 (에이전트 호출 + Exit Criteria 검증)
- [ ] AC4: review-fix loop가 정상 동작했다 (이슈 발견 시 fix → re-review 사이클 실행, critical/high 0건 또는 MAX_REVIEW 도달 시 중단)
- [ ] AC5: E2E 테스트/검증이 실제로 실행되었다 (인라인 또는 ralph-loop). Execute → Verify 패턴 준수. 결과가 사용자가 볼 수 있는 형태로 저장되었다 (`_sdd/implementation/test_results/` 또는 `ralph/state.md`). 테스트 건너뛰기 금지 — 실행 불가 시 사유와 수동 검증 방법을 보고서에 명시해야 한다.
- [ ] AC6: 테스트/검증 결과가 사용자에게 명시적으로 보고되었다 (통과/실패 건수, 실패 시 원인 요약, 수동 확인 필요 항목)
- [ ] AC7: 최종 요약 보고서(`_sdd/pipeline/report_<topic>_<timestamp>.md`)가 작성되고 사용자에게 보고되었다
- [ ] AC8: `_sdd/spec/` 직접 수정은 `spec-update-done` / `spec-update-todo` 에이전트에만 위임했다
- [ ] AC9: Phase 2 진입 전에 Step 6 checkpoint에서 pre-flight 결과를 공유하고 explicit approval을 받았다
- [ ] AC10: 완료된 active orchestrator를 `_sdd/pipeline/orchestrators/<topic>_<timestamp>/`에 아카이브했다

## Workflow Position

```
User Request
    |
    v
[sdd-autopilot] -----> Phase 1 (Interactive)
    |                 ├── Reference Loading
    |                 ├── Task Analysis + Inline Discussion
    |                 ├── Explore agent (코드베이스 탐색)
    |                 ├── Reasoning → Orchestrator Generation
    |                 └── Orchestrator Verification
    |
    v
[sdd-autopilot] -----> Phase 1.5 (Checkpoint)
    |                 └── 검증 결과 + 파이프라인 요약 → 사용자 확인
    |
    v
[sdd-autopilot] -----> Phase 2 (Autonomous Execution)
                      ├── 파이프라인 단계 순차 실행
                      ├── review-fix loop
                      ├── 테스트 (인라인 or ralph)
                      └── 최종 요약 + 보고
```

**입력**: 사용자의 기능 요청 (자연어)
**출력**: 구현 완료된 코드 + 동기화된 스펙 + 파이프라인 로그 + 최종 정리 보고서 (`_sdd/pipeline/`)

## Hard Rules

1. **Discussion 인라인 실행 + `_sdd/spec/` 직접 수정 금지**: Step 2 대화는 autopilot 내 `AskUserQuestion`으로 직접 수행한다. 스펙 파일 수정은 반드시 `spec-update-done` / `spec-update-todo` 에이전트에 위임한다.
2. **Phase 2 무중단 + 파일 기반 상태 전달**: Phase 2 진입 후 `AskUserQuestion` 금지. 에이전트에는 파일 경로만 전달하며, 전체 출력을 부모 컨텍스트에 누적하지 않는다.
3. **오케스트레이터 저장 + 공유 로그 필수**: 오케스트레이터는 `.claude/skills/orchestrator_<topic>/SKILL.md`에 저장. 실행 시 `_sdd/pipeline/log_<topic>_<timestamp>.md`를 생성하고 각 에이전트 완료 후 핵심 결정사항을 기록한다.
4. **에이전트 호출 시 원문 전달**: 사용자의 원래 요청과 관련 컨텍스트 파일 경로를 포함한다. 요약하지 않는다.
5. **Review-Fix 사이클 필수**: review 포함 파이프라인에서는 review → fix → re-review 사이클을 실행해야 한다. 리뷰만 하고 끝나는 것은 불허. 전체/부분/재개 파이프라인 모두 적용. `implementation-review`는 핵심 단계로 취급하며 실패 시 건너뛸 수 없다.
6. **Execute → Verify 필수**: 모든 단계는 실행(Execute) + 검증(Verify) 두 페이즈를 거친다. 에이전트 호출만으로 완료 간주 금지. Exit Criteria 미충족 시 다음 단계 진행 불가. 생성 에이전트(ralph-loop-init 등)에도 동일 적용 -- 설정 생성 후 실제 실행하여 결과 확인 필수.
7. **Pre-flight + approval 필수**: Phase 2 진입 전 `_sdd/env.md`를 읽고 실행 가능성을 점검한 뒤 explicit approval을 받아야 한다.
8. **Archive 필수**: 완료된 active orchestrator는 `_sdd/pipeline/orchestrators/<topic>_<timestamp>/`에 아카이브한다.
9. 한국어를 기본으로 하되 사용자 언어를 따른다.

## Process

### Step 0: Pipeline State Detection (파이프라인 상태 감지)

**Tools**: `Glob`, `Read`

autopilot 호출 시 기존 파이프라인 상태를 확인한다.

| 체크 | 동작 |
|------|------|
| `_sdd/pipeline/log_*.md` 스캔 | 미완료 스텝(`pending`/`in_progress`/`failed`) 필터링 |
| `_sdd/spec/*.md` 존재 확인 | 없으면 → "`/spec-create`로 스펙을 먼저 생성해주세요" → 종료 |
| `_sdd/drafts/`, `_sdd/implementation/` 스캔 | 기존 산출물 활용 여부 판단 |

**상태별 분기**:
- 미완료 로그 0건 + 산출물 없음 → Step 1 (새 파이프라인)
- 미완료 로그 1건 → 사용자에게 재개/새로 시작 선택 제시 → 재개 시 Step 7
- 미완료 로그 2건+ → 목록 제시 + 선택
- 미완료 로그 0건 + 산출물 있음 → Step 1에서 활용 여부 판단

### Step 1: Reference Loading (레퍼런스 로딩)

**Tools**: `Read`

```
Read: references/sdd-reasoning-reference.md  (철학 + 스킬 카탈로그)
Read: references/orchestrator-contract.md    (오케스트레이터/로그 최소 계약)
Read: examples/sample-orchestrator.md        (오케스트레이터 품질 기준)
```

내재화 대상: SDD 원칙 3개, 스킬 의존성 그래프, 파이프라인 구성 가이드라인, 테스트 전략 판단 기준.

**Gate 1→2**: reference 로딩 성공 시 Step 2 진행.

### Step 2: Task Analysis + Discussion (요청 분석 + 인라인 토론)

**Tools**: `AskUserQuestion`

> 서브에이전트가 아닌 autopilot 내 인라인 실행. Discussion 에이전트를 호출하지 않는다.

#### 2.1 요청 파싱

사용자 입력에서 추출:
- 기능 설명, 기술 키워드, 제약 조건, 기존 코드 관계 (신규/수정/확장)
- 시작점/종료점 힌트 ("구현부터", "리뷰까지만" 등)
- 기존 산출물 관련성 판단 (`_sdd/drafts/`, `_sdd/implementation/`)
- Review-Fix 사이클 필수 검증: review 포함 시 implementation + review-fix loop 강제

#### 2.2 인라인 토론

요청 명확도에 따라 1-5회 질문. 매 질문에 "충분합니다 -- 진행해주세요" 옵션 필수 포함.

**수집 대상**: 기능 범위, 기술 제약, 우선순위, 테스트 요구사항, 스펙 변경 여부.

**Gate 2→3**: 핵심 요구사항 1개+ 확정 AND 사용자 ready → Step 3.

### Step 3: Codebase Exploration (코드베이스 탐색)

**Tools**: `Agent` (Explore), `Read`, `Glob`, `Grep`

#### 3.1 Explore 에이전트 호출

프로젝트 구조, 관련 파일/모듈, 기존 패턴, 의존성 관계, 테스트 구조, `_sdd/spec/` 현황을 수집.

#### 3.2 직접 탐색 (보조)

Explore 결과 부족 시 `Glob`/`Grep`/`Read`로 보완.

#### 3.3 분석 결과 정리

```
codebase_analysis = {
  project_structure, related_files, existing_patterns,
  test_structure, spec_status, estimated_file_count,
  new_components, spec_change_needed
}
```

**Gate 3→4**: 프로젝트 구조와 관련 파일 식별 완료 → Step 4.

### Step 4: Reasoning → Orchestrator Generation (추론 → 오케스트레이터 생성)

**Tools**: `Write`

#### 4.1 Reasoning (reference 기반)

Step 1 내재화 + Step 2-3 결과를 바탕으로 추론:

| 판단 항목 | 내용 |
|-----------|------|
| 스펙 상태 | 관련 섹션/범위 분석 |
| 변경 범위 | 스펙 패치? 신규 섹션? → spec-update-todo 필요 여부 |
| 계획 깊이 | 직접 구현? feature-draft? impl-plan? |
| 검증 수준 | 인라인 테스트? ralph-loop? review 포함? |
| 스킬 순서 | 카탈로그 input/output/pre-condition 기반 |
| 특수 패턴 | 부분 파이프라인, 팬아웃 병렬, 재개 |

#### 4.2 오케스트레이터 생성

- 의존성 그래프 기반 동적 조합 (템플릿 아님)
- `references/orchestrator-contract.md` 계약 준수
- "구체화된 요구사항"에서 기능 수준 Acceptance Criteria를 도출하여 오케스트레이터에 포함
- `Reasoning Trace` 3-6 bullet 간결 작성
- 파일 경로: `.claude/skills/orchestrator_<topic>/SKILL.md`

#### 4.3 Pre-flight Check

오케스트레이터 생성 후 `_sdd/env.md`와 대조하여 리소스 갭 분석.

| 에이전트 | 필요 리소스 |
|---------|------------|
| implementation | 런타임, 패키지 매니저, 테스트 프레임워크, 외부 서비스, 환경 변수 |
| ralph-loop-init | 장시간 실행 환경, 반복 디버깅 프로세스 |
| spec-update-done | git (diff 확인용) |
| feature-draft, impl-plan, impl-review | 추가 리소스 불필요 |

결과는 Step 6에서 사용자에게 제시.

**Gate 4→5**: 오케스트레이터 파일 저장 완료 → Step 5.

### Step 5: Orchestrator Verification (오케스트레이터 검증)

**Tools**: `Read`

Producer-Reviewer 패턴으로 검증.

**구조 검증 (6항목)**: a) 유효 에이전트명 참조 b) step별 에이전트명/입출력/프롬프트 존재 c) 산출물 handoff 정합성 d) review-fix loop 존재 e) test strategy 존재 f) error handling 존재

**철학 검증 (6항목)**: a) Spec-first b) 드리프트 방지 c) Review-fix 완전성 d) Execute→Verify Exit Criteria e) 파일 기반 handoff f) 스펙 직접 수정 금지

**결과 분기**:
- 12/12 통과 → Step 6
- 구조 이슈 → 자동 수정 (최대 2회) → 재검증
- 철학 위반 → Step 4.1 재실행 (최대 1회)
- 재시도 후 실패 → Step 6에서 경고 표시

### Step 6: User Checkpoint (사용자 확인)

**Tools**: `AskUserQuestion`, `Read`, `Edit`

> Phase 1(Interactive) 마지막. 승인 후 Phase 2(Autonomous) 진입 -- 사용자 중단 없이 완료까지 진행.

#### 6.1 파이프라인 요약 + Pre-flight Check 제시

```
| 항목 | 내용 |
|------|------|
| 기능 / 파이프라인 / 검증 결과 / 예상 에이전트 수 / Review 최대 횟수 / 테스트 전략 / 오케스트레이터 경로 |

| 리소스 | 상태 | 출처 | 필요 단계 |
|--------|------|------|----------|
```

#### 6.2 사용자 확인

옵션: 실행 / env.md 추가 정보 / 미확인 리소스 없이 진행(mock) / 취소

#### 6.3 수정 처리

수정 요청 시 오케스트레이터 `Edit` → 재제시 (최대 3회).

**Gate 6→7**: 승인 → Step 7. 취소 → 종료 (오케스트레이터 유지).

### Step 7: Autonomous Execution (자율 실행)

**Tools**: `Agent`, `Read`, `Write`, `Edit`, `Glob`, `Grep`, `Bash`

> **Phase 2 진입**: `AskUserQuestion` 호출 금지. 마일스톤 텍스트 출력만 수행.

#### 7.1 파이프라인 초기화

1. 로그 파일 생성: `_sdd/pipeline/log_<topic>_<timestamp>.md` (계약 준수)
2. 오케스트레이터 `Read` → 파이프라인 단계 확인
3. 마일스톤 출력

#### 7.2 파이프라인 실행 루프 (Execute → Verify)

```
FOR EACH step IN pipeline_steps:

  ## Phase A: Execute
  1. 마일스톤 출력
  2. 로그 기록 (시작 시간)
  3. 에이전트 호출 (오케스트레이터 프롬프트 + 컨텍스트 파일 경로 + 사용자 원문)

  ## Phase B: Verify
  4. Exit Criteria 검증 (아래 테이블 참조)
  5. 통과 → 로그 완료 기록 + 다음 단계
     미충족 → 에러 핸들링(7.4) → 재시도 또는 중단

  ## Audit Trail
  6. 모든 자동 결정을 로그에 기록: `[DECISION] <what> -- <why> -- <taste: yes/no>`
     - Taste decision = "합리적으로 다르게 판단할 수 있는 것" (예: 테스트 전략 선택, 병렬 vs 순차 결정, 에러 복구 방식)
```

**단계별 Exit Criteria**:

| 에이전트 | Exit Criteria |
|---------|--------------|
| `sdd-skills:feature-draft` | `_sdd/drafts/feature_draft_<topic>.md` 존재 + 요구사항/제약조건 비어있지 않음 |
| `sdd-skills:implementation-plan` | `implementation_plan.md` 존재 + 태스크 1개+ |
| `sdd-skills:implementation` | 대상 파일 생성/수정 + 구문 에러 없음 |
| `sdd-skills:implementation-review` | 심각도 분류(critical/high/medium/low) 포함 |
| `sdd-skills:ralph-loop-init` | `ralph/` + `run.sh` 실행 가능 + `state.md` 존재 |
| ralph loop 실행 | `state.md` phase=DONE + 최종 결과 기록 |
| 인라인 테스트 | 테스트 실행 완료 + 결과 파일 저장 (`_sdd/implementation/test_results/`) + 전체 통과 (또는 최대 재시도 후 결과 기록) |
| `sdd-skills:spec-update-done/todo` | `_sdd/spec/` 업데이트 + 내용 반영 |
| `sdd-skills:spec-review` | 리뷰 결과 반환 + 드리프트/품질 이슈 분류 |
| 오케스트레이터 AC | 기능 수준 AC 전체 충족 (테스트 통과 + 리뷰 통과 기준) |

#### 7.3 Review-Fix Loop + 테스트 실행 (통합)

> Hard Rule #5, #6 적용.

**Review-Fix Loop**:

```
review_count = 0; MAX_REVIEW = 3

WHILE review_count < MAX_REVIEW:
  review_count += 1
  1. implementation-review 에이전트 호출
  2. critical/high/medium 이슈 수 추출 → 로그 기록
  3. critical==0 AND high==0 AND medium==0 → BREAK (리뷰 통과)
  4. Fix: implementation 에이전트로 critical/high/medium 수정 (low는 로그에만 기록)
  5. → re-review (루프 반복)

MAX_REVIEW 도달 시:
  critical/high > 0 → 파이프라인 중단
  medium만 잔존 → 로그 기록 후 파이프라인 계속 진행
```

부분 파이프라인("리뷰만 해줘")에서도 이슈 발견 시 fix → re-review 사이클 강제.

**테스트 실행** (리뷰 완료 후):

| 전략 | Execute | Verify |
|------|---------|--------|
| **인라인 디버깅** | implementation 에이전트에 테스트 포함 호출 (수정-재실행 최대 5회) | 테스트 실행 로그 + 통과/실패 건수 + 수정 시도 확인. 결과를 `_sdd/implementation/test_results/test_result_<timestamp>.md`에 저장. 전체 통과 → 다음 단계. 최대 재시도 후 실패 → 중단 |
| **ralph-loop-init** | Phase A-1: 설정 생성 → Phase B-1: 설정 검증 (ralph/, run.sh, state.md) → Phase A-2: `bash ralph/run.sh` background 실행 | Phase B-2: 완료 알림 후 state.md phase 확인. DONE → 다음 단계. 미완료 → 중단 |

#### 7.4 에러 핸들링

```
retry_count = 0; MAX_RETRY = 3

ON ERROR:
  retry_count += 1
  로그에 에러 기록 + 마일스톤 출력

  IF retry_count <= MAX_RETRY:
    원인 분석 → 수정 → 재호출
  ELSE:
    비핵심 단계 → 건너뛰고 진행 (로그 기록)
    핵심 단계 → 파이프라인 중단
```

**핵심/비핵심 분류**:

| 핵심 (실패 시 중단) | 비핵심 (실패 시 건너뛰기) |
|--------------------|------------------------|
| feature-draft, implementation-plan, implementation, implementation-review, 테스트 단계 | spec-update-todo, spec-update-done, spec-review |

**파이프라인 중단 시 보고**: 중단 원인, 재시도 횟수, 완료/미완료 단계, 로그 파일 경로, 부분 산출물 목록, 권장 후속 조치.

#### 7.5 마일스톤 보고 + 로그 관리

마일스톤 포맷: `[sdd-autopilot] Step N/M: <agent-name> <상태>`

각 에이전트 완료 후 로그 `Edit`:
```
### <agent-name> -- <상태>
- 시간 / 출력 경로 / 핵심 결정사항 (1-3줄) / 이슈
```

### Step 8: Final Summary (최종 요약)

**Tools**: `Edit`, `Write`

#### 8.1 로그 마무리

최종 요약 섹션 추가: 완료 시간, 총 소요, 실행 결과, 파일 수, Review 횟수, 테스트 결과, 스펙 동기화, 잔여 이슈.

#### 8.2 최종 정리 보고서

`_sdd/pipeline/report_<topic>_<timestamp>.md` 작성. 필수 항목:

1. **뭘 했는가**: 실행 단계, 에이전트 목록, 산출물 경로, review-fix 횟수, 테스트 여부
2. **어떻게 나왔는가**: 각 단계 성공/실패, 이슈 해결 상태, 테스트 통과율, 스펙 동기화
3. **뭘 더 해야 하는가**: 미완료 단계, 제한사항/리스크, 후속 작업 제안
4. **Taste Decisions**: 파이프라인 중 taste decision으로 분류된 자동 결정 목록 (what/why/대안)

> 실패/중단 시에도 반드시 보고서 작성.

#### 8.3 사용자 최종 보고

```
## SDD Autopilot 실행 완료

| 항목 | 결과 |
|------|------|
| 기능 / 파이프라인 / 생성·수정 파일 / Review 결과 / 테스트 / 스펙 동기화 / 로그 / 보고서 / 오케스트레이터 |

### 주요 산출물 / 잔여 이슈 / 후속 작업 제안
```

## Reference Files

- `references/sdd-reasoning-reference.md`: SDD 철학, skill catalog, 규모별 reasoning 기준
- `references/orchestrator-contract.md`: 오케스트레이터/로그 최소 계약
- `examples/sample-orchestrator.md`: 중규모 기본형 + 대규모 차이점 예시

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

