---
name: sdd-autopilot
description: "적응형 오케스트레이터 메타스킬. /sdd-autopilot으로 호출하여 요구사항 분석부터 스펙 동기화까지 end-to-end SDD 파이프라인을 자율 실행한다."
version: 2.4.0
---

# SDD Autopilot

## Goal

사용자 요청을 SDD 파이프라인으로 해석하고, 적절한 오케스트레이터를 만든 뒤 실행과 검증까지 끝내는 최상위 메타스킬이다. global spec은 장기적 SoT로, temporary spec은 실행 청사진으로 취급하며 `_sdd/` 아티팩트를 중심으로 discussion, planning, implementation, review, spec sync를 연결한다.

## Codex Runtime Adapter

런타임이 skill-internal agent dispatch를 허용하는 경우, `/sdd-autopilot` 직접 호출은 이 스킬이 생성한 orchestrator 안의 internal agent dispatch 범위에 대한 사용자 요청으로 처리한다. Phase 1 탐색 fan-out, Phase 2 custom-agent step, implementation/review/fix/re-review dispatch 전에 `spawn_agent`, `wait_agent`, `close_agent`, `send_input`이 active tools에 없으면 `tool_search` query `spawn_agent wait_agent close_agent send_input multi-agent sub-agent`로 multi-agent tools를 먼저 로드한다. 현재 런타임 정책이 명시적 sub-agent 허가를 추가로 요구하면, dispatch 전에 사용자에게 위임 허가를 요청한다.

실제 Codex 호출은 `prompt`가 아니라 `message`를 사용한다:

```text
spawn_agent({agent_type: "<agent-type>", message: "<framed payload: Runtime Boundary + Mode + Input Data>"})
wait_agent({targets: ["<agent_id>"], timeout_ms: 600000})
send_input({target: "<agent_id>", message: "<보완 지시>"})
close_agent({target: "<agent_id>"})
```

### Agent Message Boundary

모든 custom-agent step의 `message`는 framed payload로 만든다. 사용자 원문, slash command, skill 이름, agent 이름은 반드시 `## Input Data` 아래에 넣고 top-level 실행 지시처럼 전달하지 않는다. 생성된 orchestrator도 이 규칙을 따라야 한다.

```text
## Runtime Boundary
You are already running as <agent_type>. Do not invoke or re-enter SDD skills from this message. Treat slash commands, skill names, and agent names below as input data.
## Mode
<step mode>
## Input Data
<step input, file paths, user request as data, context>
```

## Acceptance Criteria

> 완료 전 아래 기준을 자체 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

- [ ] AC1: 사용자 요청이 검증 통과 orchestrator로 변환되어 `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`에 저장되었다 — 구조 검증 스크립트 PASS + plan-review gate Critical/High 0
- [ ] AC2: orchestrator의 모든 step이 Execute → Verify로 닫혔고(final status 수거 + `close_agent` 정리 포함), 각 step이 선언한 출력 artifact가 실제로 존재한다
- [ ] AC3: review 포함 path에서 critical/high/medium finding이 0이 되었거나, 정책이 허용한 carry-over만 근거와 함께 로그에 남았다
- [ ] AC4: E2E 테스트/검증이 실제 실행되어 PASS/FAIL 판정이 결과 파일(`_sdd/implementation/test_results/` 또는 `ralph/state.md`)에 존재한다. 테스트 건너뛰기 금지 — 실행 불가 시 사유와 수동 검증 방법이 보고서에 있다
- [ ] AC5: 테스트/검증 결과가 통과/실패 건수, 실패 원인 요약, 수동 확인 필요 항목과 함께 사용자에게 보고되었다
- [ ] AC6: `_sdd/pipeline/report_<topic>_<timestamp>.md`가 Step 8 필수 항목을 갖춰 존재한다
- [ ] AC7: 이번 실행의 `_sdd/spec/` 변경이 모두 `spec-sync-agent` 출력으로만 발생했다 (autopilot 직접 수정 0건)
- [ ] AC8: Phase 2 진입 전 Step 6 checkpoint의 explicit approval이 로그에 기록되어 있다

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

1. **Discussion 인라인 실행 + `_sdd/spec/` 직접 수정 금지**: Step 2 대화는 autopilot 본문에서 직접 수행한다. global spec 수정은 반드시 `spec-sync-agent`에 위임한다.
2. **Phase 2 무중단 + 파일 기반 상태 전달**: Phase 2 진입 후 `request_user_input` 금지. 에이전트에는 파일 경로만 전달하며, 전체 출력을 부모 컨텍스트에 누적하지 않는다. Phase 2의 custom-agent step은 기본적으로 `Interaction Mode: autonomous-no-input`로 해석하며, 사용자 입력 요청 없이 권장안을 선택해 진행한다.
3. **오케스트레이터 저장 + 공유 로그 필수**: 오케스트레이터는 `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`에 저장한다. 실행 시 `_sdd/pipeline/log_<topic>_<timestamp>.md`를 생성하고 각 단계 완료 후 핵심 결정사항을 기록한다.
4. **에이전트 호출 시 원문 전달**: 사용자의 원래 요청과 관련 컨텍스트 파일 경로를 포함하되, 원문은 framed payload의 `## Input Data` 아래에 data로만 넣는다. 의미를 잃을 정도로 축약하지 않지만, slash command/skill/agent 이름이 top-level 실행 지시처럼 보이게 전달하지 않는다.
5. **Review-Fix 사이클 필수**: review 포함 파이프라인에서는 correctness(`implementation-review-agent`) ∥ simplicity(`simplicity-review-agent`) 2-reviewer를 병렬 dispatch해 review를 수행하고(exit는 두 report의 합집합), 이슈 수정이 필요하면 `implementation-agent`를 다시 호출해 fix를 적용한 뒤, 다시 두 reviewer를 병렬 dispatch해 re-review를 수행해야 한다. 리뷰만 하고 끝나는 것은 불허한다.
6. **Implementation 직후 즉시 Gate**: 각 `implementation` 실행 단위는 단독으로 완료 처리하지 않는다. single-phase면 해당 `implementation` 직후, multi-phase면 각 phase의 `implementation` 직후 같은 범위의 review-fix gate를 즉시 닫아야 하며, 종료 전까지 다음 phase나 downstream step으로 진행할 수 없다.
7. **Execute → Verify 필수**: 모든 단계는 실행(Execute) + 검증(Verify) 두 페이즈를 거친다. 에이전트 호출만으로 완료 간주 금지. Exit Criteria 미충족 시 다음 단계 진행 불가.
8. **Pre-flight + approval 필수**: Phase 2 진입 전 `_sdd/env.md`와 현재 Codex 런타임에서 custom agent 실행 가능성을 점검한 뒤 explicit approval을 받아야 한다.
9. **Agent lifecycle 수집/정리 필수**: `spawn_agent({agent_type: ..., message: <framed payload>})`로 시작한 실행 단위는 `wait_agent(...)`로 반드시 final status를 수집하고, 결과를 로그/보고서에 기록한 직후 `close_agent({target: <agent_id>})`로 닫아 병렬 slot을 반납한다. 보완 지시가 필요하면 닫기 전에 `send_input({target: <agent_id>, message: ...})`을 사용하고, 이미 닫은 뒤 추가 작업이 필요하면 새로 `spawn_agent({agent_type: ..., message: <framed payload>})` 한다. `wait_agent` timeout은 수집 완료가 아니므로 더 기다리거나 controlled stop/abandon을 기록한 뒤에만 닫는다. 여러 agent를 병렬 spawn한 단계는 remaining agent ids를 유지하고, final status가 반환된 handle만 기록·닫은 뒤 remaining이 빌 때까지 `wait_agent({targets: remaining, ...})`를 반복한다.
10. **로그 기반 상태 관리**: 오케스트레이터는 `_sdd/pipeline/orchestrators/`에 유지. 활성/완료 구분은 로그 파일 status로 판단한다.
11. 한국어를 기본으로 하되 사용자 언어를 따른다.
12. spec-less repo에서도 중단하지 않는다. `_sdd/spec/`가 없으면 `_sdd/` workspace bootstrap + code-first fallback reasoning으로 계속 진행하고, 적절한 시점에 `spec-create` 또는 spec sync 단계를 파이프라인에 포함한다.
13. **계약 우선순위**: 규칙의 canonical home은 `references/orchestrator-contract.md`다. 이 SKILL.md 또는 example과 contract가 충돌하면 contract가 우선한다.

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

재개를 선택하면 `references/orchestrator-contract.md`의 Resume Contract를 따른다: orchestrator를 현행 계약으로 재검증 → completed step의 출력 artifact 실존 확인 → 미완료/실패 step만 재실행.

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

필요하면 구조/도메인/테스트 관점으로 explorer를 병렬 호출한다. 각 explorer는 `wait_agent`가 final status를 반환한 뒤에만 핵심 사실을 요약하고 `close_agent({target: <agent_id>})`로 닫는다. 병렬 호출 시 remaining agent ids가 빌 때까지 반복 수거한다. 결과는 전체 로그가 아니라 핵심 사실만 요약한다.

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
- spec-less인 경우에도 feature-draft의 `Part 1: Spec Delta`는 생성할 수 있다. global spec 없이도 delta 기반 reasoning은 가능하다.

planning precedence 메모:
- **`feature-draft`는 기본 포함이다.** 다음 두 조건 중 하나를 만족할 때만 스킵할 수 있다: (1) 정말 간단한 디버깅 수준의 수정(typo fix, config 값 변경, 로그 한 줄 추가 등)이거나, (2) 해당 주제의 feature-draft artifact가 `_sdd/drafts/`에 이미 존재하는 경우. 그 외에는 small/medium/large 무관하게 `feature-draft`를 반드시 거친다.
- non-trivial change의 기본 planning entry는 `feature-draft`다. single-phase medium path에서 Part 2가 충분히 명확하면 그대로 `implementation` 입력으로 사용한다.
- `implementation-plan`은 **multi-phase 실행으로 판단되면 반드시 포함한다.** feature-draft → implementation 직행은 single-phase 경로에 한정한다. large/complex 변경, medium이라도 multi-phase execution gate가 필요한 경우 모두 해당한다.
- `spec-sync`(planned 호출)는 planned persistent global alignment가 실제로 필요한 경우에만 `feature-draft`와 `implementation-plan` 사이에 조건부로 넣는다. 동일 `spec-sync`는 구현 전 planned 반영(조건부 1회)과 구현 완료 후 sync(1회)로 최대 2회 호출될 수 있으며, 같은 진입점이 evidence 차이로 동작을 적응한다.
- standalone `implementation-plan`은 기존 feature draft/temporary spec/기존 plan artifact가 이미 있고, 이를 phase/task 수준으로 보강하거나 재개해야 하는 예외 상황에서만 사용한다.

오케스트레이터 생성 규칙:
- 의존성 그래프 기반 동적 조합
- `references/orchestrator-contract.md` 계약 준수
- "구체화된 요구사항"에서 기능 수준 Acceptance Criteria 도출
- feature draft가 예상되면 아래 downstream linkage를 pipeline reasoning에 반영:
  - `Part 1: Spec Delta`
  - `Part 2: Implementation and Validation Plan`
  - top-level `Risks/Mitigations and Open Questions`
- Step 4에서 실제로 materialize할 수 있는 산출물은 `_sdd/pipeline/orchestrators/orchestrator_<topic>.md` 하나뿐이다.
- `_sdd/drafts/*`, `_sdd/implementation/*`, `_sdd/pipeline/log_*`, `_sdd/pipeline/report_*`, 코드/테스트 출력은 future step의 planned output으로 선언할 수는 있지만 이 단계에서 미리 생성하면 안 된다.
- 각 `implementation` step에는 같은 범위의 review-fix gate가 즉시 붙어야 한다.
- planning producer(`feature-draft-agent`, `implementation-plan-agent`) output은 downstream 소비 전에 `plan-review-agent` producer review gate를 통과해야 한다. gate 실패 시 finding을 normalize하지 않고 producer 산출물을 reject/regenerate한다.
- `implementation-plan` output을 downstream `implementation`이 소비하는 expanded path면 해당 `implementation` step을 flat single-shot으로 쓰지 않고 `Execution Mode: phase-iterative`와 `Phase Source`를 명시한다.
- Phase 2의 custom-agent step에는 `Interaction Mode: autonomous-no-input`을 기본으로 명시한다. 이 계약에는 `request_user_input` 금지, 권장안 우선 판단, 가정/근거 기록, 안전한 추론이 불가능할 때 질문 대신 `BLOCKED`로 종료하는 fallback이 포함된다.
- review가 포함된 모든 path에서는 `implementation-agent`/correctness(`implementation-review-agent`) ∥ simplicity(`simplicity-review-agent`) 2-reviewer/re-review를 모두 Codex custom agent step으로 유지한다. 부모 autopilot이 로컬 구현/로컬 리뷰로 대체하면 안 된다.
- Implementation Dispatch Controller: `implementation-agent`는 단일 task leaf다(`references/orchestrator-contract.md` §2 Implementation Dispatch Granularity). 따라서 `implementation` step은 phase를 한 agent에 통째로 넘기지 않고, autopilot이 phase의 task를 **병렬 dispatch 그룹**으로 파생해 task당 leaf를 spawn한다(초기 구현=group 병렬, fix=finding 순차). 각 leaf는 final status 수거와 progress 기록 직후 `close_agent({target: <agent_id>})`로 닫는다. 이 phase-내부 병렬 dispatch 그룹은 review-fix gate의 Checkpoint 리뷰 그룹과 다른 중첩 개념이며, progress/report는 autopilot이 canonical 경로로 소유한다.
- `implementation-agent` dispatch controller semantics는 generic custom-agent dispatch 규칙보다 우선한다. 오케스트레이터는 이 special case가 runtime에 task-level leaf spawn으로 해석된다는 점을 명시해야 한다.
- canonical kebab-case custom agent 이름만 허용한다. legacy alias를 발견하면 canonical 이름으로 normalize하지 않고 해당 오케스트레이터를 reject/regenerate한다.
- Reasoning Trace 3-6 bullet 간결 작성
- 저장 경로: `_sdd/pipeline/orchestrators/orchestrator_<topic>.md`

Pre-flight Check:
- `_sdd/env.md`와 대조하여 테스트/리소스 갭 분석
- `.codex/agents/` custom agent 사용 가능 여부와 병렬 fan-out 리소스 점검
- 사용자 전역 `~/.codex/config.toml`의 agent depth/concurrency 값은 전제하거나 수정하지 않는다

Gate 4→5: 오케스트레이터 저장 완료 → Step 5.

### Step 5: Orchestrator Verification (오케스트레이터 검증)

오케스트레이터도 planning producer output이다. 구조는 스크립트로, 철학/품질은 reviewer agent로 검증한다. autopilot 본인이 인라인 자기 검증으로 대체하지 않는다.

#### 5.1 구조 검증 (기계)

이 스킬 디렉토리의 `scripts/validate_orchestrator.py`를 실행한다:

```bash
python3 <skill_dir>/scripts/validate_orchestrator.py _sdd/pipeline/orchestrators/orchestrator_<topic>.md
```

스크립트가 검사하는 항목(필수 섹션, canonical kebab-case agent 이름, step 필수 필드, phase-iterative ⇒ Phase Source invariant, review-fix gate 필드와 고정 agent 매핑, `fix_targets`의 `low` 미포함, per-group 필수 필드, `Interaction Mode` 값)은 스크립트가 단일 소스다.

- FAIL → finding 기반으로 오케스트레이터를 수정 후 재실행 (최대 2회)
- 2회 후에도 FAIL → Step 4로 돌아가 재생성 (최대 1회)
- 그래도 FAIL → BLOCKED. Step 6에서 실행 불가로 보고한다

#### 5.2 철학/품질 검증 (plan-review gate)

구조 검증 PASS 후, `spawn_agent({agent_type: "plan-review-agent", message: <framed payload: Runtime Boundary + orchestrator-review mode + Input Data(orchestrator 경로, references/orchestrator-contract.md 경로, 사용자 원문 요청 data, "Orchestrator Review Mode로 검토")>})`로 dispatch하고 `wait_agent`로 final status를 수거한다. final status가 반환된 뒤에만 결과를 기록하고 `close_agent({target: <agent_id>})`로 닫는다. 검토 rubric(기능 수준 AC, Reasoning Trace 정당화, planning precedence, immediate gate/dispatch controller 해석 가능성, 산출물 handoff 정합성, generation boundary, spec 직접 수정 금지, 입출력 비대)은 plan-review-agent의 Orchestrator Review Mode 계약이 단일 소스다.

결과 분기:
- Critical/High 없음 → Step 6
- Critical/High 있음 → Step 4 reject/regenerate (최대 2회). finding을 normalize해서 통과 처리하지 않는다
- regenerate 상한 도달 → BLOCKED. Step 6에서 잔존 finding과 함께 실행 불가로 보고하고 사용자 결정을 받는다

### Step 6: User Checkpoint (사용자 확인)

Phase 1 마지막 단계다. 아래를 사용자에게 짧게 공유한다.

- 기능 / 파이프라인 요약
- 시작점 / 종료점
- 주요 산출물
- 검증 결과
- pre-flight 결과 (`_sdd/env.md`, custom agent 사용 가능성, 테스트/리소스 갭)
- 주된 리스크나 가정

확인 규칙:
- `request_user_input` 또는 동등한 단일 승인 질문으로 `승인 후 실행`, `파이프라인 수정`, `중단` 중 하나를 받는다
- Step 5 검증을 통과하지 못한(BLOCKED) 오케스트레이터에는 `승인 후 실행` 옵션을 제공하지 않는다. 잔존 finding을 보여주고 `파이프라인 수정` 또는 `중단`만 제시한다
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

각 step은 `Execute -> Collect -> Record -> Close -> Verify` 순서를 따른다.

- custom-agent step이면 오케스트레이터에 적힌 Codex `agent_type`으로 호출한다.
- custom-agent step이면 `wait_agent`가 final status를 반환한 뒤에만 step output/log를 기록하고 `close_agent({target: <agent_id>})`로 handle을 닫는다. 여러 agent를 병렬 spawn한 step은 remaining agent ids를 반복 수거하고, 모든 handle이 final status로 정리된 뒤에만 다음 dispatch group 또는 downstream step으로 진행한다.
- custom-agent step이면 오케스트레이터의 `Interaction Mode`를 함께 해석한다. 값이 없으면 `autonomous-no-input`으로 간주한다.
- 단, `implementation-agent` step은 generic custom-agent dispatch보다 먼저 Implementation Dispatch Controller로 해석한다. phase나 feature 전체를 한 번에 넘기지 않고 phase의 task를 dependency와 Target Files 기준 dispatch 그룹으로 나누어 task당 leaf를 spawn한다.
- 로컬 step이면 오케스트레이터에 적힌 skill 또는 명령을 실행한다.
- step별 필드, 허용 `agent_type`, Exit Criteria, Acceptance Criteria는 오케스트레이터 본문과 `references/orchestrator-contract.md`를 그대로 따른다.
- 오케스트레이터에 적힌 출력 파일은 현재 step이 실제로 생성한 materialized output과 future step의 planned output을 구분해 해석한다. 각 step은 자신의 선언된 출력만 materialize하며, 아직 실행되지 않은 downstream step의 planned output을 미리 생성하지 않는다.
- `autonomous-no-input` step을 호출할 때는 framed payload 안에 런타임 지시를 함께 준다: `request_user_input` 또는 동등한 사용자 확인 금지, SDD skill 재진입 금지, 기존 코드/스펙/오케스트레이터/원문 요청에 가장 잘 맞는 권장안을 우선 선택, 모든 핵심 가정과 판단 근거를 출력 파일에 기록, 안전한 추론이 불가능하면 질문 대신 `BLOCKED` 상태와 `blocked_reason`, `why_not_safe_to_assume`, `recommended_next_action`을 남긴다.
- `autonomous-no-input` step이 사용자 질문만 남기거나 입력 대기를 유도하면 contract violation으로 간주한다. autopilot은 더 강한 no-input 지시로 최대 1회 재-spawn할 수 있고, 재발하면 해당 step을 `BLOCKED` 또는 `failed`로 기록한다.
- review 포함 path에서는 `implementation-agent`와 correctness(`implementation-review-agent`) ∥ simplicity(`simplicity-review-agent`) 2-reviewer 병렬 호출을 항상 Codex custom agent 호출로 실행한다(exit는 두 report의 합집합). 부모 autopilot이 local implementation/review로 대체하지 않는다.
- `implementation` step은 단독 완료가 아니다. 같은 범위의 `Review-Fix Loop` exit condition과 required validation이 닫혀야만 해당 step을 `completed`로 기록할 수 있다.
- single-phase path이거나 `Review-Fix Loop.scope = global`이면 `implementation` step 직후 즉시 global review-fix loop를 수행한다. 이 gate가 닫히기 전에는 `spec-sync-agent`(post-implementation 호출)를 포함한 다음 downstream step으로 진행할 수 없다.
- `implementation-plan` output을 downstream `implementation`이 소비하고 해당 step이 `Execution Mode: phase-iterative`로 선언되어 있으면, autopilot은 `Phase Source`를 읽어 phase count와 boundary를 runtime-resolved metadata로 해석한다. Step 4가 추측한 flat phase list로 실행하지 않는다.
- `scope = per-group`이면 `Phase Source`의 각 phase `Checkpoint` 필드를 읽어 group boundary를 결정한다. `Checkpoint=true` phase가 group의 마지막 phase이며, 해당 phase 직후 같은 group 범위의 review-fix gate를 닫는다. `Checkpoint=false` phase는 light validation(test/typecheck/exit criteria)만 수행하고 다음 phase로 진행한다. 마지막 phase는 explicit 값과 무관하게 implicit `Checkpoint=true`로 처리한다. 마지막 phase를 제외한 phase에 `Checkpoint` 필드가 없으면 plan schema violation으로 보고 downstream 구현을 시작하지 않으며, producer review gate/Step 5 verification에서 `implementation-plan-agent` 산출물을 reject/regenerate한다.
- group 내 phase의 light validation이 `critical` 이슈를 잡으면 group boundary forced early로 즉시 review-fix gate를 트리거한다 (mid-group emergency).
- group review-fix gate에서는 group 범위(Checkpoint=false phase들 + 해당 Checkpoint=true phase) 전체를 scope로 correctness(`implementation-review-agent`) ∥ simplicity(`simplicity-review-agent`) 2-reviewer 병렬 실행(exit는 두 report의 합집합) -> 필요 시 `implementation-agent` fix -> 두 reviewer 병렬 re-review 순서를 닫은 뒤 다음 group으로 간다.
- 현재 group exit criteria가 충족되지 않으면 다음 group으로 넘어가지 않는다. `medium` 이슈도 기본적으로 exit blocker이며, carry-over는 현재 group policy가 명시적으로 허용할 때만 로그와 근거를 남기고 진행한다.

#### 7.3 Review-Fix Loop 해석 + 테스트 실행

오케스트레이터에 `Review-Fix Loop`와 `Test Strategy` section이 있으면, autopilot은 그 선언을 그대로 집행한다. 이 섹션은 파이프라인 마지막에 사후 정리용으로 도는 것이 아니라, 7.2에서 각 `implementation` 실행 직후 붙는 immediate completion gate의 해석 규칙이다.
- multi-phase path에서 `scope = per-group`이면 각 Checkpoint phase 직후 해당 group 범위로 review-fix와 validation을 즉시 수행한다. **Final integration review (adaptive)**: 그룹 1개면 마지막 group gate가 final을 겸하고, 그룹 2개 이상이면 마지막 group gate 후 cross-group regression 전용으로 1회 추가 실행한다.
- single-phase path이거나 `scope = global`이면 해당 `implementation` step 직후 즉시 global review-fix loop를 수행한다.
- review-fix loop의 agent 매핑은 small/medium/large review path 모두 고정이다(correctness ∥ simplicity 2-reviewer 병렬, exit는 두 report의 합집합):
  - `review = implementation-review-agent`
  - `review = simplicity-review-agent`
  - `re-review = implementation-review-agent`
  - `re-review = simplicity-review-agent`
  - `fix = implementation-agent`
- `scope = global`이든 `scope = per-group`이든 review/fix/re-review를 local inline work로 대체하지 않는다.
- fix 단계의 `implementation-agent` 재호출은 review finding 하나를 단일 task leaf로 보는 순차 spawn이다. finding의 영향 파일만 Target Files로 전달하며, 초기 구현 dispatch 그룹처럼 병렬화하지 않는다. 각 fix leaf도 `wait_agent`가 final status를 반환한 뒤에만 결과를 기록하고 `close_agent({target: <agent_id>})`로 닫는다.
- `low` finding은 advisory/logged follow-up으로 기록하며 기본 fix 대상과 gate blocker에 포함하지 않는다.
- `spec-sync-agent`(post-implementation 호출)는 모든 required implementation-scoped review-fix gate, required validation, 그리고 필요한 경우 final integration review가 닫힌 뒤에만 실행할 수 있다.
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
- `examples/sample-orchestrator.md`: 중규모 기본형 + 대규모 차이점 예시

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.
