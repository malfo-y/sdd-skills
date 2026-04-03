---
name: sdd-autopilot
description: "적응형 오케스트레이터 메타스킬. /sdd-autopilot으로 호출하여 요구사항 분석부터 스펙 동기화까지 end-to-end SDD 파이프라인을 자율 실행한다."
version: 2.3.0
---

# SDD Autopilot

## Goal

사용자 요청을 SDD 파이프라인으로 해석하고, 적절한 오케스트레이터를 만든 뒤 실행과 검증까지 끝내는 최상위 메타스킬이다. 스펙과 `_sdd/` 아티팩트를 Single Source of Truth로 삼아 discussion, planning, implementation, review, spec sync를 연결한다.

## Acceptance Criteria

> 완료 전 아래 기준을 자체 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

- [ ] AC1: 8-step pipeline(Step 0~8)이 순서대로 실행 완료되었다 (부분 파이프라인은 해당 범위 내 완료)
- [ ] AC2: `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`에 generated orchestrator를 저장하고 검증을 통과했다
- [ ] AC3: orchestrator 기반 Phase 2 자율 실행이 완료되었다 (에이전트 호출 + Exit Criteria 검증)
- [ ] AC4: review 포함 파이프라인에서 review-fix loop가 정상 동작했다
- [ ] AC5: E2E 테스트/검증이 실제로 실행되었다 (인라인 또는 ralph-loop). Execute → Verify 패턴 준수. 결과가 사용자가 볼 수 있는 형태로 저장되었다 (`_sdd/implementation/test_results/` 또는 `ralph/state.md`). 테스트 건너뛰기 금지 — 실행 불가 시 사유와 수동 검증 방법을 보고서에 명시해야 한다.
- [ ] AC6: 테스트/검증 결과가 사용자에게 명시적으로 보고되었다 (통과/실패 건수, 실패 시 원인 요약, 수동 확인 필요 항목)
- [ ] AC7: 최종 결과와 후속 조치를 `_sdd/pipeline/report_<topic>_<timestamp>.md`에 정리했다
- [ ] AC8: `_sdd/spec/` 직접 수정은 `spec_update_done` 또는 `spec_update_todo` 에이전트에만 위임했다
- [ ] AC9: Phase 2 진입 전에 Step 6 checkpoint에서 pre-flight 결과를 공유하고 explicit approval을 받았다

## Workflow Position

```text
User Request
    |
    v
[sdd-autopilot] -----> Phase 1 (Interactive)
    |                 |- Reference Loading
    |                 |- Task Analysis + Inline Discussion
    |                 |- Explore agent / local exploration
    |                 |- Reasoning -> Orchestrator Generation
    |                 `- Orchestrator Verification
    |
    v
[sdd-autopilot] -----> Phase 1.5 (Checkpoint)
    |                 `- 검증 결과 + 파이프라인 요약 + pre-flight -> 사용자 확인
    |
    v
[sdd-autopilot] -----> Phase 2 (Autonomous Execution)
                      |- 파이프라인 단계 순차 실행
                      |- review-fix loop
                      |- 테스트 (인라인 or Ralph)
                      `- 최종 요약 + 보고
```

## Hard Rules

1. **Discussion 인라인 실행 + `_sdd/spec/` 직접 수정 금지**: Step 2 대화는 autopilot 본문에서 직접 수행한다. 스펙 파일 수정은 반드시 `spec_update_done` / `spec_update_todo` 에이전트에 위임한다.
2. **Phase 2 무중단 + 파일 기반 상태 전달**: Phase 2 진입 후 `request_user_input` 금지. 에이전트에는 파일 경로만 전달하며, 전체 출력을 부모 컨텍스트에 누적하지 않는다.
3. **오케스트레이터 저장 + 공유 로그 필수**: 오케스트레이터는 `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`에 저장한다. 실행 시 `_sdd/pipeline/log_<topic>_<timestamp>.md`를 생성하고 각 단계 완료 후 핵심 결정사항을 기록한다.
4. **에이전트 호출 시 원문 전달**: 사용자의 원래 요청과 관련 컨텍스트 파일 경로를 포함한다. 의미를 잃을 정도로 축약하지 않는다.
5. **Review-Fix 사이클 필수**: review 포함 파이프라인에서는 review → fix → re-review 사이클을 실행해야 한다. 리뷰만 하고 끝나는 것은 불허한다.
6. **Execute → Verify 필수**: 모든 단계는 실행(Execute) + 검증(Verify) 두 페이즈를 거친다. 에이전트 호출만으로 완료 간주 금지. Exit Criteria 미충족 시 다음 단계 진행 불가.
7. **Pre-flight + approval 필수**: Phase 2 진입 전 `_sdd/env.md`와 `.codex/config.toml`을 읽고 실행 가능성을 점검한 뒤 explicit approval을 받아야 한다.
8. **Agent lifecycle 수집 필수**: `spawn_agent(...)`로 시작한 실행 단위는 `wait_agent(...)`로 반드시 수집하고, 필요 시 `send_input(...)` 또는 재-spawn으로 보완한다.
9. **로그 기반 상태 관리**: 오케스트레이터는 `_sdd/pipeline/orchestrators/`에 유지. 활성/완료 구분은 로그 파일 status로 판단한다.
10. 한국어를 기본으로 하되 사용자 언어를 따른다.

## Process

### Step 0: Pipeline State Detection (파이프라인 상태 감지)

autopilot 호출 시 기존 파이프라인 상태를 확인한다.

| 체크 | 동작 |
|------|------|
| `_sdd/pipeline/log_*.md` 스캔 | 미완료 스텝(`pending`/`in_progress`/`failed`) 필터링 |
| `_sdd/spec/*.md` 존재 확인 | 없으면 `/spec-create` 안내 후 종료 |
| `_sdd/drafts/`, `_sdd/implementation/` 스캔 | 기존 산출물 활용 여부 판단 |

상태별 분기:
- 미완료 로그 0건 + 산출물 없음 → Step 1
- 미완료 로그 1건 → 재개 후보 제시
- 미완료 로그 2건 이상 → 목록 제시 + 선택
- 미완료 로그 0건 + 산출물 있음 → Step 1에서 활용 여부 판단

### Step 1: Reference Loading (레퍼런스 로딩)

아래 companion asset을 읽고 내재화한다.

- `references/sdd-reasoning-reference.md`
- `references/orchestrator-contract.md`
- `examples/sample-orchestrator.md`

내재화 대상:
- SDD 원칙 3개
- 스킬 의존성 그래프
- 파이프라인 구성 가이드라인
- 테스트 전략 판단 기준
- review-fix 및 final report 규칙

Gate 1→2: reference 로딩 성공 시 Step 2 진행.

### Step 2: Task Analysis + Inline Discussion (요청 분석 + 인라인 토론)

요청에서 다음을 추출하고, 부족한 정보만 `request_user_input`으로 보완한다.

- 기능 설명
- 기술 키워드
- 제약 조건
- 기존 코드와의 관계
- 시작점/종료점 힌트
- 테스트 요구사항
- 스펙 변경 여부

질문 원칙:
- 1회에 1개 핵심 분기만 묻는다
- 선택지는 2-3개로 제한한다
- 항상 `충분합니다 -- 진행해주세요` 옵션을 둔다
- 최대 5회 이내로 정리한다

Gate 2→3: 핵심 요구사항이 확정되면 Step 3.

### Step 3: Codebase Exploration (코드베이스 탐색)

`explorer` 에이전트 또는 로컬 탐색으로 다음을 수집한다.

- 프로젝트 구조
- 관련 파일/모듈
- 기존 패턴
- 테스트 구조
- `_sdd/spec/` 현황
- 수정 범위와 예상 리스크

필요하면 구조/도메인/테스트 관점으로 explorer를 병렬 호출한다. 결과는 전체 로그가 아니라 핵심 사실만 요약한다.

Gate 3→4: 프로젝트 구조와 관련 파일 식별 완료 → Step 4.

### Step 4: Reasoning → Orchestrator Generation (추론 → 오케스트레이터 생성)

Step 1 내재화 + Step 2~3 결과를 바탕으로 추론한다.

| 판단 항목 | 내용 |
|-----------|------|
| 스펙 상태 | 관련 섹션/범위 분석 |
| 변경 범위 | 스펙 패치 / 신규 섹션 / spec-update-todo 필요 여부 |
| 계획 깊이 | 직접 구현 / feature-draft / implementation-plan |
| 검증 수준 | 인라인 테스트 / Ralph / review 포함 여부 |
| 스킬 순서 | 카탈로그 input/output/pre-condition 기반 |
| 특수 패턴 | 부분 파이프라인, 팬아웃 병렬, 재개 |

오케스트레이터 생성 규칙:
- 의존성 그래프 기반 동적 조합
- `references/orchestrator-contract.md` 계약 준수
- "구체화된 요구사항"에서 기능 수준 Acceptance Criteria 도출
- Reasoning Trace 3-6 bullet 간결 작성
- 저장 경로: `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`

Pre-flight Check:
- `_sdd/env.md`와 대조하여 테스트/리소스 갭 분석
- `.codex/config.toml`에서 `agents.max_depth`, `agents.max_threads` 확인
- nested writing / 병렬 fan-out 가능 여부 점검

Gate 4→5: 오케스트레이터 저장 완료 → Step 5.

### Step 5: Orchestrator Verification (오케스트레이터 검증)

Producer-Reviewer 패턴으로 검증한다.

구조 검증 (6항목):
- 유효 agent명 참조
- step별 agent명 / 입출력 / 프롬프트 존재
- 산출물 handoff 정합성
- review-fix loop 존재
- test strategy 존재
- error handling 존재

철학 검증 (6항목):
- Spec-first
- 드리프트 방지
- Review-fix 완전성
- Execute → Verify Exit Criteria
- 파일 기반 handoff
- 스펙 직접 수정 금지

결과 분기:
- 12/12 통과 → Step 6
- 구조 이슈 → 자동 수정(최대 2회) 후 재검증
- 철학 위반 → Step 4로 돌아가 reasoning 재실행(최대 1회)
- 재시도 후 실패 → Step 6에서 경고 표시

### Step 6: User Checkpoint (사용자 확인)

Phase 1 마지막 단계다. 아래를 사용자에게 짧게 공유한다.

- 기능 / 파이프라인 요약
- 시작점 / 종료점
- 주요 산출물
- 검증 결과
- pre-flight 결과 (`_sdd/env.md`, `.codex/config.toml`, 테스트/리소스 갭)
- 주된 리스크나 가정

확인 규칙:
- `request_user_input` 또는 동등한 단일 승인 질문으로 `승인 후 실행`, `파이프라인 수정`, `중단` 중 하나를 받는다
- `승인 후 실행`일 때만 Step 7로 진행한다
- `파이프라인 수정`이면 Step 4 또는 5로 돌아가 오케스트레이터를 조정한 뒤 Step 6을 다시 수행한다
- `중단`이면 active orchestrator를 유지하고 현재 상태를 로그에 남긴 뒤 종료한다

### Step 7: Autonomous Execution (자율 실행)

Phase 2 진입 후 `request_user_input`은 호출하지 않는다. 마일스톤 텍스트와 로그만 남긴다.

#### 7.1 파이프라인 초기화

1. `_sdd/pipeline/log_<topic>_<timestamp>.md` 생성
2. 오케스트레이터를 다시 읽고 파이프라인 단계 확인
3. 상태 테이블과 step 목록 기록

#### 7.2 파이프라인 실행 루프 (Execute → Verify)

각 단계는 아래 순서를 따른다.

1. Execute: 관련 skill/custom agent 실행
2. Collect: `wait_agent(...)` 또는 로컬 결과 수집
3. Verify: Exit Criteria + orchestrator AC + 테스트 + 산출물 존재 여부 확인
4. Record: 로그 파일에 상태와 핵심 결정 기록
5. Audit Trail: 모든 자동 결정을 `[DECISION] <what> -- <why> -- <taste: yes/no>` 형식으로 기록

단계별 Exit Criteria:

| 에이전트 | Exit Criteria |
|---------|--------------|
| `feature_draft` | `_sdd/drafts/feature_draft_<topic>.md` 존재 + 요구사항/제약조건 비어있지 않음 |
| `implementation_plan` | `implementation_plan.md` 또는 phase plan 존재 + task 1개 이상 |
| `implementation` | 대상 파일 생성/수정 + 구문 에러 없음 |
| `implementation_review` | severity 분류 포함 + 리뷰 리포트 저장 |
| `ralph_loop_init` | `ralph/` 존재 + `config.sh` + `PROMPT.md` + `run.sh` + `state.md` + `CHECKS.md` 존재 + `run.sh` 실행 가능 |
| Ralph 실행 | `ralph/state.md`의 `phase = DONE` + 최종 결과 기록 |
| 인라인 테스트 | 테스트 실행 완료 + 결과 파일 저장 + 전체 통과 또는 최대 재시도 후 결과 기록 |
| `spec_update_done` / `spec_update_todo` | `_sdd/spec/` 업데이트 + 내용 반영 |
| `spec_review` | 리뷰 결과 반환 + drift/품질 이슈 분류 |
| 오케스트레이터 AC | 기능 수준 AC 전체 충족 |

#### 7.3 Review-Fix Loop + 테스트 실행

Review-Fix Loop:

```text
review_count = 0; MAX_REVIEW = 3

WHILE review_count < MAX_REVIEW:
  review_count += 1
  1. implementation_review 실행
  2. severity counts 추출
  3. blocking/fix-required 이슈가 0이면 BREAK
  4. implementation으로 이슈 수정
  5. 재테스트 후 re-review
```

Severity 해석:
- 기본 Codex schema: `critical/high/medium/low`
- Claude parity schema가 남아 있으면 `Critical` = blocking, `Quality` = fix-required, `Improvements` = follow-up 으로 해석

MAX_REVIEW 도달 시:
- blocking/fix-required 잔존 → 파이프라인 중단
- follow-up만 잔존 → 로그 기록 후 진행

테스트 실행:

| 전략 | Execute | Verify |
|------|---------|--------|
| 인라인 디버깅 | implementation 단계 또는 로컬 명령으로 테스트 재실행 | 실행 로그 + 통과/실패 건수 + 수정 시도 확인. 결과를 `_sdd/implementation/test_results/test_result_<timestamp>.md`에 저장 |
| Ralph | Phase A-1: Ralph 설정 생성 → Phase B-1: 설정 검증 → Phase A-2: `bash ralph/run.sh` 실행 | `state.md`의 phase가 DONE인지 확인. 미완료면 중단 또는 보고 |

#### 7.4 에러 핸들링

```text
retry_count = 0; MAX_RETRY = 3

ON ERROR:
  retry_count += 1
  로그에 에러 기록 + 마일스톤 출력

  IF retry_count <= MAX_RETRY:
    원인 분석 -> 수정 -> 재호출
  ELSE:
    비핵심 단계 -> 건너뛰고 진행 (로그 기록)
    핵심 단계 -> 파이프라인 중단
```

핵심/비핵심 분류:

| 핵심 (실패 시 중단) | 비핵심 (실패 시 건너뛰기) |
|--------------------|------------------------|
| feature_draft, implementation_plan, implementation, implementation_review, 테스트 단계 | spec_update_todo, spec_update_done, spec_review, Ralph 설정 생성 |

#### 7.5 마일스톤 보고 + 로그 관리

마일스톤 포맷:
`[sdd-autopilot] Step N/M: <agent-name> <상태>`

각 단계 완료 후 로그에 다음을 기록한다.

```text
### <agent-name> -- <상태>
- 시간 / 출력 경로 / 핵심 결정사항(1-3줄) / 이슈
```

### Step 8: Final Summary (최종 요약)

최종 산출물을 점검하고 `_sdd/pipeline/report_<topic>_<timestamp>.md`를 작성한다.

필수 항목:
1. 뭘 했는가: 실행 단계, 에이전트 목록, 산출물 경로, review-fix 횟수, 테스트 여부
2. 어떻게 나왔는가: 각 단계 성공/실패, 이슈 해결 상태, 테스트 통과율, 스펙 동기화
3. 뭘 더 해야 하는가: 미완료 단계, 제한사항/리스크, 후속 작업 제안
4. Taste Decisions: 파이프라인 중 taste decision으로 분류된 자동 결정 목록
5. 오케스트레이터 경로 및 상태 확인 (로그 기반)

## Reference Files

- `references/sdd-reasoning-reference.md`: SDD 철학, skill catalog, reasoning 기준
- `references/orchestrator-contract.md`: 오케스트레이터/로그 최소 계약
- `examples/sample-orchestrator.md`: 중규모 기본형 + 대규모 차이점 예시

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
