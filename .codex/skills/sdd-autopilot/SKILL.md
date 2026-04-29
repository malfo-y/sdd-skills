---
name: sdd-autopilot
description: "적응형 오케스트레이터 메타스킬. /sdd-autopilot으로 호출하여 요구사항 분석부터 스펙 동기화까지 end-to-end SDD 파이프라인을 자율 실행한다."
version: 2.3.6
---

# SDD Autopilot

## Goal

사용자 요청을 SDD 파이프라인으로 해석하고, 적절한 오케스트레이터를 만든 뒤 실행과 검증까지 끝내는 최상위 메타스킬이다. global spec은 장기적 SoT로, temporary spec은 실행 청사진으로 취급하며 `_sdd/` 아티팩트를 중심으로 discussion, planning, implementation, review, spec sync를 연결한다.

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
                      |- implementation-scoped review-fix gate 즉시 실행
                      |- 테스트 (인라인 or Ralph)
                      `- 최종 요약 + 보고
```

## Hard Rules

1. **Discussion 인라인 실행 + `_sdd/spec/` 직접 수정 금지**: Step 2 대화는 autopilot 본문에서 직접 수행한다. global spec 수정은 반드시 `spec_update_done` / `spec_update_todo` 에이전트에 위임한다.
2. **Phase 2 무중단 + 파일 기반 상태 전달**: Phase 2 진입 후 `request_user_input` 금지. 에이전트에는 파일 경로만 전달하며, 전체 출력을 부모 컨텍스트에 누적하지 않는다. Phase 2의 custom-agent step은 기본적으로 `Interaction Mode: autonomous-no-input`로 해석하며, 사용자 입력 요청 없이 권장안을 선택해 진행한다.
3. **오케스트레이터 저장 + 공유 로그 필수**: 오케스트레이터는 `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`에 저장한다. 실행 시 `_sdd/pipeline/log_<topic>_<timestamp>.md`를 생성하고 각 단계 완료 후 핵심 결정사항을 기록한다.
4. **에이전트 호출 시 원문 전달**: 사용자의 원래 요청과 관련 컨텍스트 파일 경로를 포함한다. 의미를 잃을 정도로 축약하지 않는다.
5. **Review-Fix 사이클 필수**: review 포함 파이프라인에서는 `implementation_review` agent로 review를 수행하고, 이슈 수정이 필요하면 `implementation` agent를 다시 호출해 fix를 적용한 뒤, 다시 `implementation_review` agent로 re-review를 수행해야 한다. 리뷰만 하고 끝나는 것은 불허한다.
6. **Implementation 직후 즉시 Gate**: 각 `implementation` 실행 단위는 단독으로 완료 처리하지 않는다. single-phase면 해당 `implementation` 직후, multi-phase면 각 phase의 `implementation` 직후 같은 범위의 review-fix gate를 즉시 닫아야 하며, 종료 전까지 다음 phase나 downstream step으로 진행할 수 없다.
7. **Execute → Verify 필수**: 모든 단계는 실행(Execute) + 검증(Verify) 두 페이즈를 거친다. 에이전트 호출만으로 완료 간주 금지. Exit Criteria 미충족 시 다음 단계 진행 불가.
8. **Pre-flight + approval 필수**: Phase 2 진입 전 `_sdd/env.md`와 `.codex/config.toml`을 읽고 실행 가능성을 점검한 뒤 explicit approval을 받아야 한다.
9. **Agent lifecycle 수집 필수**: `spawn_agent(...)`로 시작한 실행 단위는 `wait_agent(...)`로 반드시 수집하고, 필요 시 `send_input(...)` 또는 재-spawn으로 보완한다.
10. **로그 기반 상태 관리**: 오케스트레이터는 `_sdd/pipeline/orchestrators/`에 유지. 활성/완료 구분은 로그 파일 status로 판단한다.
11. 한국어를 기본으로 하되 사용자 언어를 따른다.
12. spec-less repo에서도 중단하지 않는다. `_sdd/spec/`가 없으면 `_sdd/` workspace bootstrap + code-first fallback reasoning으로 계속 진행하고, 적절한 시점에 `spec-create` 또는 spec sync 단계를 파이프라인에 포함한다.

## Execution Profile Reference

- step별 `model` / `reasoning_effort` 기본값과 조정 규칙은 `references/execution-profile-policy.md`를 따른다.
- 기본 원칙은 고정 프로파일이며, 명시적 override가 없는 한 동일하게 적용한다.
- 설계 단계, phase/task planning, final integration review는 실패 비용이 크므로 보수적으로 유지한다.
- 실행 중 프로파일 변경이 필요하면 기존 agent를 재사용하지 말고 새로 `spawn_agent(...)` 한다.

## Process

### Step 0: Pipeline State Detection (파이프라인 상태 감지)

autopilot 호출 시 기존 파이프라인 상태를 확인한다.

| 체크 | 동작 |
|------|------|
| `_sdd/pipeline/log_*.md` 스캔 | 미완료 스텝(`pending`/`in_progress`/`failed`) 필터링 |
| `_sdd/spec/*.md` 존재 확인 | 없으면 spec-less mode로 계속 진행하고, `_sdd/` bootstrap 및 `spec-create`/spec sync 필요성을 오케스트레이터에 기록 |
| `_sdd/drafts/`, `_sdd/implementation/` 스캔 | 기존 산출물 활용 여부 판단 |

상태별 분기:
- 미완료 로그 0건 + `_sdd/spec/` 없음 → spec-less mode로 Step 1
- 미완료 로그 0건 + 산출물 없음 → Step 1
- 미완료 로그 1건 → 재개 후보 제시
- 미완료 로그 2건 이상 → 목록 제시 + 선택
- 미완료 로그 0건 + 산출물 있음 → Step 1에서 활용 여부 판단

### Step 1: Reference Loading (레퍼런스 로딩)

아래 companion asset을 읽고 내재화한다.

- `references/sdd-reasoning-reference.md`
- `references/orchestrator-contract.md`
- `references/execution-profile-policy.md`
- `examples/sample-orchestrator.md`

내재화 대상:
- SDD 원칙 3개
- 스킬 의존성 그래프
- 파이프라인 구성 가이드라인
- step별 execution profile 고정 기본값과 override 규칙
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
| 스펙 상태 | global spec 존재 여부와 thin-core relevance 분석. 없으면 spec-less 모드로 진행하되, 사용자에게 `spec-create`로 global spec을 만드는 것을 추천 |
| 변경 범위 | temporary spec 필요 여부 / planned global update 필요 여부 |
| 계획 깊이 | 아래 planning precedence 참조. feature-draft는 기본 포함이며, 스킵 조건이 엄격하다 |
| 검증 수준 | 인라인 테스트 / Ralph / review 포함 여부 |
| 스킬 순서 | 카탈로그 input/output/pre-condition 기반 |
| 특수 패턴 | 부분 파이프라인, 팬아웃 병렬, 재개 |

spec-less mode 참고:
- spec이 없으면 spec-less 모드로 진행한다. `spec-create`를 파이프라인에 자동 배치하지 않고, 사용자에게 구현 완료 후 global spec을 만드는 것을 추천한다. 코드가 먼저 존재해야 spec이 실제 구조를 반영할 수 있기 때문이다.
- spec-less인 경우에도 feature-draft의 Part 1 temporary spec은 생성할 수 있다. global spec 없이도 delta 기반 reasoning은 가능하다.

planning precedence 메모:
- **`feature-draft`는 기본 포함이다.** 다음 두 조건 중 하나를 만족할 때만 스킵할 수 있다: (1) 정말 간단한 디버깅 수준의 수정(typo fix, config 값 변경, 로그 한 줄 추가 등)이거나, (2) 해당 주제의 feature-draft artifact가 `_sdd/drafts/`에 이미 존재하는 경우. 그 외에는 small/medium/large 무관하게 `feature-draft`를 반드시 거친다.
- non-trivial change의 기본 planning entry는 `feature-draft`다. single-phase medium path에서 Part 2가 충분히 명확하면 그대로 `implementation` 입력으로 사용한다.
- `implementation-plan`은 **multi-phase 실행으로 판단되면 반드시 포함한다.** feature-draft → implementation 직행은 single-phase 경로에 한정한다. large/complex 변경, medium이라도 multi-phase execution gate가 필요한 경우 모두 해당한다.
- `spec-update-todo`는 planned persistent global alignment가 실제로 필요한 경우에만 `feature-draft`와 `implementation-plan` 사이에 조건부로 넣는다.
- standalone `implementation-plan`은 기존 feature draft/temporary spec/기존 plan artifact가 이미 있고, 이를 phase/task 수준으로 보강하거나 재개해야 하는 예외 상황에서만 사용한다.

오케스트레이터 생성 규칙:
- 의존성 그래프 기반 동적 조합
- `references/orchestrator-contract.md` 계약 준수
- "구체화된 요구사항"에서 기능 수준 Acceptance Criteria 도출
- temporary spec이 예상되면 `Contract/Invariant Delta`와 `Validation Plan` linkage를 pipeline reasoning에 반영
- Step 4에서 실제로 materialize할 수 있는 산출물은 `_sdd/pipeline/orchestrators/orchestrator_<topic>.md` 하나뿐이다.
- `_sdd/drafts/*`, `_sdd/implementation/*`, `_sdd/pipeline/log_*`, `_sdd/pipeline/report_*`, 코드/테스트 출력은 future step의 planned output으로 선언할 수는 있지만 이 단계에서 미리 생성하면 안 된다.
- 각 `implementation` step에는 같은 범위의 review-fix gate가 즉시 붙어야 한다.
- `implementation-plan` output을 downstream `implementation`이 소비하는 expanded path면 해당 `implementation` step을 flat single-shot으로 쓰지 않고 `Execution Mode: phase-iterative`와 `Phase Source`를 명시한다.
- Phase 2의 custom-agent step에는 `Interaction Mode: autonomous-no-input`을 기본으로 명시한다. 이 계약에는 `request_user_input` 금지, 권장안 우선 판단, 가정/근거 기록, 안전한 추론이 불가능할 때 질문 대신 `BLOCKED`로 종료하는 fallback이 포함된다.
- review가 포함된 모든 path에서는 `implementation`/`implementation_review`/re-review를 모두 Codex custom agent step으로 유지한다. 부모 autopilot이 로컬 구현/로컬 리뷰로 대체하면 안 된다.
- Reasoning Trace 3-6 bullet 간결 작성
- 저장 경로: `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`

Pre-flight Check:
- `_sdd/env.md`와 대조하여 테스트/리소스 갭 분석
- `.codex/config.toml`에서 `agents.max_depth`, `agents.max_threads` 확인
- nested writing / 병렬 fan-out 가능 여부 점검

Gate 4→5: 오케스트레이터 저장 완료 → Step 5.

### Step 5: Orchestrator Verification (오케스트레이터 검증)

Producer-Reviewer 패턴으로 검증한다.

구조 검증:
- 유효 `agent_type` 참조
- step별 `agent_type` / 입출력 / 프롬프트 존재
- Phase 2 custom-agent step의 `Interaction Mode`가 해석 가능하고, `autonomous-no-input` runtime contract와 모순되지 않는가
- 산출물 handoff 정합성
- `Review-Fix Loop` section/contract 존재
- 각 `implementation` step 뒤에 같은 범위의 immediate review-fix gate가 해석 가능함
- Step 4가 orchestrator file 외 downstream artifact를 materialize하지 않았는가
- expanded path면 downstream `implementation` step에 `Execution Mode: phase-iterative`와 `Phase Source`가 선언되었는가
- `Execution Mode: phase-iterative` path면 per-group gate semantics(`Checkpoint` boundary)와 `final integration review` adaptive 처리가 해석 가능한가
- phase-iterative path의 `Phase Source`가 `implementation-plan` output인가 (`feature-draft` 산출물 금지). 위반 시 reject하고 `feature-draft` step 직후에 `implementation-plan` step 삽입.
- review 포함 path에서 `implementation`/`implementation_review`가 custom agent step으로만 매핑되는가
- test strategy 존재
- error handling 존재

추가 검증:
- `Execution Profiles` section 또는 step-level `Execution profile`이 있으면 `references/execution-profile-policy.md`와 정합해야 한다.
- `profile_key`를 쓴 경우 step 참조와 loop 참조가 해석 가능해야 한다.
- section-level 기본값과 step-level / loop-level override가 동시에 있으면 우선순위가 모호하지 않아야 한다.

철학 검증:
- Spec-first
- 드리프트 방지
- Review-fix 완전성
- Execute → Verify Exit Criteria
- 파일 기반 handoff
- 스펙 직접 수정 금지

결과 분기:
- 모든 구조/철학 검증 통과 → Step 6
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

Phase 2 진입 후 `request_user_input`은 호출하지 않는다. 마일스톤 텍스트와 로그만 남긴다. custom-agent step은 `Interaction Mode: autonomous-no-input`을 기본값으로 사용하며, 질문 대신 권장안 또는 `BLOCKED` 중 하나를 반환해야 한다.

#### 7.1 파이프라인 초기화

1. `_sdd/pipeline/log_<topic>_<timestamp>.md` 생성
2. 오케스트레이터를 다시 읽고 파이프라인 단계 확인
3. 상태 테이블과 step 목록 기록

#### 7.2 파이프라인 실행

`_sdd/pipeline/orchestrators/orchestrator_<topic>.md`를 다시 읽고, 정의된 `Pipeline Steps`를 순서대로 실행한다.

각 step은 `Execute -> Collect -> Verify -> Record` 순서를 따른다.

- custom-agent step이면 오케스트레이터에 적힌 Codex `agent_type`으로 호출한다.
- custom-agent step이면 오케스트레이터의 `Interaction Mode`를 함께 해석한다. 값이 없으면 `autonomous-no-input`으로 간주한다.
- 프로파일 우선순위는 `step-level Execution profile` -> `Execution Profiles` section 기본값 -> `references/execution-profile-policy.md` 기본값 순서다.
- 로컬 step이면 오케스트레이터에 적힌 skill 또는 명령을 실행한다.
- step별 필드, 허용 `agent_type`, Exit Criteria, Acceptance Criteria는 오케스트레이터 본문과 `references/orchestrator-contract.md`를 그대로 따른다.
- 오케스트레이터에 적힌 출력 파일은 현재 step이 실제로 생성한 materialized output과 future step의 planned output을 구분해 해석한다. 각 step은 자신의 선언된 출력만 materialize하며, 아직 실행되지 않은 downstream step의 planned output을 미리 생성하지 않는다.
- `autonomous-no-input` step을 호출할 때는 런타임 지시를 함께 준다: `request_user_input` 또는 동등한 사용자 확인 금지, 기존 코드/스펙/오케스트레이터/원문 요청에 가장 잘 맞는 권장안을 우선 선택, 모든 핵심 가정과 판단 근거를 출력 파일에 기록, 안전한 추론이 불가능하면 질문 대신 `BLOCKED` 상태와 `blocked_reason`, `why_not_safe_to_assume`, `recommended_next_action`을 남긴다.
- `autonomous-no-input` step이 사용자 질문만 남기거나 입력 대기를 유도하면 contract violation으로 간주한다. autopilot은 더 강한 no-input 지시로 최대 1회 재-spawn할 수 있고, 재발하면 해당 step을 `BLOCKED` 또는 `failed`로 기록한다.
- review 포함 path에서는 `implementation`/`implementation_review`를 항상 Codex custom agent 호출로 실행한다. 부모 autopilot이 local implementation/review로 대체하지 않는다.
- `implementation` step은 단독 완료가 아니다. 같은 범위의 `Review-Fix Loop` exit condition과 required validation이 닫혀야만 해당 step을 `completed`로 기록할 수 있다.
- single-phase path이거나 `Review-Fix Loop.scope = global`이면 `implementation` step 직후 즉시 global review-fix loop를 수행한다. 이 gate가 닫히기 전에는 `spec_update_done`을 포함한 다음 downstream step으로 진행할 수 없다.
- `implementation-plan` output을 downstream `implementation`이 소비하고 해당 step이 `Execution Mode: phase-iterative`로 선언되어 있으면, autopilot은 `Phase Source`를 읽어 phase count와 boundary를 runtime-resolved metadata로 해석한다. Step 4가 추측한 flat phase list로 실행하지 않는다.
- `scope = per-group`이면 `Phase Source`의 각 phase `Checkpoint` 필드를 읽어 group boundary를 결정한다. `Checkpoint=true` phase가 group의 마지막 phase이며, 해당 phase 직후 같은 group 범위의 review-fix gate를 닫는다. `Checkpoint=false` phase는 light validation(test/typecheck/exit criteria)만 수행하고 다음 phase로 진행한다. 마지막 phase는 explicit 값과 무관하게 implicit `Checkpoint=true`로 처리한다. **Backward compat**: plan에 `Checkpoint` 필드가 없는 경우 모든 phase를 `Checkpoint=false`로 간주하고 마지막 phase의 implicit `Checkpoint=true` 1회만 gate를 닫는다 — 단일 group 동작과 동등하다.
- group 내 phase의 light validation이 `critical` 이슈를 잡으면 group boundary forced early로 즉시 review-fix gate를 트리거한다 (mid-group emergency).
- group review-fix gate에서는 group 범위(Checkpoint=false phase들 + 해당 Checkpoint=true phase) 전체를 scope로 `implementation_review` agent 실행 -> 필요 시 `implementation` agent fix -> re-review 순서를 닫은 뒤 다음 group으로 간다.
- 현재 group exit criteria가 충족되지 않으면 다음 group으로 넘어가지 않는다. `medium` 이슈도 기본적으로 exit blocker이며, carry-over는 현재 group policy가 명시적으로 허용할 때만 로그와 근거를 남기고 진행한다.

#### 7.3 Review-Fix Loop 해석 + 테스트 실행

오케스트레이터에 `Review-Fix Loop`와 `Test Strategy` section이 있으면, autopilot은 그 선언을 그대로 집행한다. 이 섹션은 파이프라인 마지막에 사후 정리용으로 도는 것이 아니라, 7.2에서 각 `implementation` 실행 직후 붙는 immediate completion gate의 해석 규칙이다.
- multi-phase path에서 `scope = per-group`이면 각 Checkpoint phase 직후 해당 group 범위로 review-fix와 validation을 즉시 수행한다. **Final integration review (adaptive)**: 그룹 1개면 마지막 group gate가 final을 겸하고, 그룹 2개 이상이면 마지막 group gate 후 cross-group regression 전용으로 1회 추가 실행한다.
- single-phase path이거나 `scope = global`이면 해당 `implementation` step 직후 즉시 global review-fix loop를 수행한다.
- review-fix loop의 agent 매핑은 small/medium/large review path 모두 고정이다: `review = implementation_review`, `fix = implementation`, `re-review = implementation_review`.
- `scope = global`이든 `scope = per-group`이든 review/fix/re-review를 local inline work로 대체하지 않는다.
- review-fix loop 프로파일 우선순위는 `review_profile` / `fix_profile` / `final_integration_review_profile` -> `Execution Profiles` section의 해당 agent_type 기본값 -> `references/execution-profile-policy.md` 기본값 순서다.
- `final_integration_review_profile`은 실제로 final integration review를 수행하는 경우에만 의미가 있다. `scope = per-group`에서 그룹 2개 이상일 때 사용하며, 그룹 1개나 `scope = global`에서는 별도 final integration review step 또는 명시적 global final integration review 선언이 없으면 사용하지 않는다.
- `spec_update_done`은 모든 required implementation-scoped review-fix gate, required validation, 그리고 필요한 경우 final integration review가 닫힌 뒤에만 실행할 수 있다.
- 이 섹션에서 별도 loop 규칙이나 테스트 규칙을 다시 정의하지 않는다.

#### 7.4 에러 핸들링

에러 처리는 오케스트레이터의 `Error Handling` section과 `references/orchestrator-contract.md`를 따른다.
`autonomous-no-input` step의 `BLOCKED` 반환은 hang이 아니라 유효한 controlled stop으로 해석하며, autopilot은 `blocked_reason`과 권장 후속 조치를 로그/보고서에 기록한 뒤 오케스트레이터의 분기 규칙에 따라 재시도 또는 중단을 결정한다.
재시도, 중단, 건너뛰기 결정은 모두 로그에 남긴다.

#### 7.5 마일스톤 보고 + 로그 관리

실행 중에는 마일스톤 텍스트를 출력하고, 상태와 결과를 `_sdd/pipeline/log_<topic>_<timestamp>.md`에 기록한다.
실행이 끝나면 `_sdd/pipeline/report_<topic>_<timestamp>.md`에 최종 결과를 정리한다.
로그와 보고서 schema는 오케스트레이터 본문과 `references/orchestrator-contract.md`를 따른다.

### Step 8: Final Summary (최종 요약)

최종 산출물을 점검하고 `_sdd/pipeline/report_<topic>_<timestamp>.md`를 작성한다.

필수 항목:
1. 뭘 했는가: 실행 단계, 에이전트 목록, 산출물 경로, review-fix 횟수, 테스트 여부
2. 어떻게 나왔는가: 각 단계 성공/실패, 이슈 해결 상태, 테스트 통과율, 스펙 동기화
3. 뭘 더 해야 하는가: 미완료 단계, 제한사항/리스크, 후속 작업 제안
4. Taste Decisions: 파이프라인 중 taste decision으로 분류된 자동 결정 목록
5. 오케스트레이터 경로 및 상태 확인 (로그 기반)
6. spec-less로 시작했다면 `spec-create` 또는 spec sync가 완료되었는지, 아니면 후속 작업으로 남는지 명시

## Reference Files

- `references/sdd-reasoning-reference.md`: SDD 철학, skill catalog, reasoning 기준
- `references/orchestrator-contract.md`: 오케스트레이터/로그 최소 계약
- `references/execution-profile-policy.md`: step별 모델/effort 고정 기본값과 override 규칙
- `examples/sample-orchestrator.md`: 중규모 기본형 + 대규모 차이점 예시

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
