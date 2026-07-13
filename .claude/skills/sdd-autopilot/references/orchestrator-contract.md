# Orchestrator Contract

`sdd-autopilot`이 생성/실행하는 오케스트레이터와 로그의 최소 계약이다.

## 1. Required Orchestrator Sections

1. 메타데이터
2. 기능 설명
3. Acceptance Criteria
4. Reasoning Trace
5. Pipeline Steps
6. Review-Fix Loop
7. Test Strategy
8. Error Handling

### Generation Boundary

- autopilot의 orchestrator generation 단계에서 실제로 생성 가능한 산출물은 `_sdd/pipeline/orchestrators/orchestrator_<topic>.md` 하나뿐이다.
- `_sdd/drafts/*`, `_sdd/implementation/*`, `_sdd/pipeline/log_*`, `_sdd/pipeline/report_*`, 코드/테스트 출력은 오케스트레이터 안에서 future step의 planned output으로 선언할 수는 있지만, 해당 step이 실행되기 전에는 materialize하면 안 된다.

## 2. Step Contract

step은 세 종류다.

- **custom-agent step**: `Claude subagent_type` 단일 호출. autopilot이 leaf 하나를 spawn하고 결과를 수거한다.
- **dispatch-controller step**: `Step kind: implementation-dispatch-controller`로 선언한다. 단일 호출이 아니라 autopilot이 task 단위로 fan-out하는 dispatch controller이며, wave별 3단계(Stage A/B/C) 실행으로 전개된다. 상세는 아래 `Implementation Dispatch Controller`를 따른다.
- **로컬 step**: autopilot 부모가 직접 실행하는 skill 또는 명령. 별도 agent를 spawn하지 않는다.

각 custom-agent step은 아래 4개 필드를 반드시 가진다.

- `Claude subagent_type`
- `입력 파일`
- `출력 파일`
- `프롬프트`

선택 필드:

- `Execution Mode`
  - `phase-iterative`는 downstream `implementation-dispatch-controller` step이 `task-ordering` output을 소비할 때 사용한다.
  - 이 값이 있으면 phase count와 boundary를 Step 4 generation 시점에 precompute하지 않고 runtime metadata로 해석한다.
- `Phase Source`
  - `Execution Mode: phase-iterative` `implementation-dispatch-controller` step일 때 필수다.
  - 값은 runtime response reference인 정확한 문자열 `task_ordering.response`다. 파일 경로가 아니다.
- `Interaction Mode`
  - `autonomous-no-input` 또는 `interactive-ok`를 허용한다.
  - `sdd-autopilot`의 Phase 2 subagent step은 명시가 없으면 `autonomous-no-input`으로 간주한다.
  - `interactive-ok`는 Phase 2 subagent step에는 사용할 수 없다. Step 6 이전의 interactive phase나 autopilot 바깥의 수동 실행에만 의미가 있다.

허용 `subagent_type`:

아래 canonical `sdd-skills:<agent>-agent` invocation 이름만 허용한다.

- `sdd-skills:feature-draft-agent`
- `sdd-skills:spec-sync-agent`
- `sdd-skills:task-ordering-agent`
- `sdd-skills:plan-review-agent`
- `sdd-skills:test-author-agent`
- `sdd-skills:implementation-agent`
- `sdd-skills:implementation-review-agent`
- `sdd-skills:simplicity-review-agent`
- `sdd-skills:spec-review-agent`
- `sdd-skills:ralph-loop-init-agent`

추가 규칙:

- 최종 `-agent` suffix가 빠진 `sdd-skills:` invocation, prefix 없는 skill 이름, 과거 alias는 모두 unsupported legacy alias다.
- legacy alias는 canonical 이름으로 normalize하지 않는다. Step verification은 해당 orchestrator를 reject하고 canonical `subagent_type`으로 regenerate하도록 요구해야 한다.
- `implementation` step은 단독 완료 step이 아니다. 같은 범위의 `Review-Fix Loop`와 required validation gate가 즉시 뒤따르며, gate가 닫히기 전에는 다음 downstream step으로 진행할 수 없다.
- review가 포함된 path에서는 `implementation`과 `implementation-review`를 항상 subagent step으로 사용한다. autopilot 부모가 local inline implementation/review로 대체하면 안 된다.
- downstream `implementation-dispatch-controller` step이 `task-ordering` output을 소비하면, 해당 step은 `Execution Mode: phase-iterative`와 `Phase Source`를 함께 선언해야 한다.
- 오케스트레이터의 `출력 파일`에 적힌 future artifact는 planned output이며, 현재 실행 중인 step만 자신의 출력물을 materialize할 수 있다.
- `task-ordering` custom-agent step의 `출력 파일`은 required field를 유지하되 반드시 `없음 (transient final response)`으로 선언한다. autopilot은 final Markdown을 수거한 뒤 `task_ordering.response`로 보존하고 agent를 닫는다.
- **Invariant (Phase Source 출처)**: `Execution Mode: phase-iterative`가 선언된 step의 `Phase Source`는 반드시 `task_ordering.response`여야 한다. `feature-draft`나 `implementation_plan` 경로를 직접 사용하면 Step 5 verification에서 reject한다.
- **Invariant (task-ordering 항상 경유)**: autopilot은 single/multi-phase 무관하게 구현 직전 항상 `task-ordering` step을 소유·경유한다. `task-ordering-agent`가 `feature-draft`의 flat task-set을 입력으로 dependency edge·topological parallel wave·multi/single 판정·review checkpoint를 반환하고, autopilot은 final Markdown을 `task_ordering.response`로 downstream `implementation-dispatch-controller`에 hand-off한다. 파일 artifact나 task 본문 사본을 만들지 않는다. controller는 response의 `Source` feature draft에서 task 본문을 읽는다. `feature-draft` → implementation 직행(task-ordering 생략)은 허용되지 않는다.
- `Interaction Mode: autonomous-no-input` step은 `request_user_input` 또는 동등한 사용자 확인을 호출하면 안 된다. 모호성은 기존 코드/스펙/오케스트레이터/사용자 원문 요청에 가장 잘 맞는 권장안으로 해소하고, 그 근거와 가정을 출력 파일에 기록해야 한다.
- `Interaction Mode: autonomous-no-input` step은 안전한 추론이 불가능하면 질문으로 멈추지 말고 `BLOCKED` 상태로 종료한다. 최소 출력은 `blocked_reason`, `why_not_safe_to_assume`, `recommended_next_action`를 포함해야 한다.
- interactive-only skill 또는 사용자 입력이 Hard Rule인 로컬 step은 autopilot Phase 2 step으로 배치하면 안 된다.

### Implementation Dispatch Controller

구현 step은 `Step kind: implementation-dispatch-controller`로 선언한다(단일 custom-agent step으로 선언하지 않는다). 이 kind는 단일 leaf 호출이 아니라 autopilot이 task 단위로 fan-out하는 dispatch controller이며, 선언 자체가 controller 의미를 담는다(재해석 불필요). controller는 task 단위 leaf 호출을 파생한다.

이 kind는 **Stage agents** 3단계로 전개된다.

- **Stage A** = `sdd-skills:test-author-agent` (테스트만 작성, 구현 금지)
- **Stage B** = orchestrator 소유 RED 게이트 (agent 없음 — autopilot 자신이 테스트를 실행해 RED 증거 캡처·falsifiability 점검)
- **Stage C** = `sdd-skills:implementation-agent` (고정 실패 테스트를 입력으로 GREEN→REFACTOR만 수행 — **impl-agent는 RED를 자체 수행하지 않는다**)

task-level leaf는 sub-agent를 spawn하지 않는다. 따라서 autopilot은 phase를 한 leaf에 통째로 넘기지 않고, autopilot 자신이 orchestrator로서 task 단위로 fan-out한다.

- **초기 구현 step**: autopilot이 `task_ordering.response`의 `Execution` 각 phase를 topological parallel wave로 소비하고, `Source`가 가리키는 feature draft에서 phase의 task ID별 본문·Target Files·AC·Validation linkage를 가져온다. autopilot은 fan-out 직전 file-disjoint를 실측 검증한 뒤 각 wave를 다음 **3단계**로 dispatch한다:
  - (a) **test-author 병렬 dispatch**: wave 내 task마다 `sdd-skills:test-author-agent` leaf를 동시 dispatch한다 (테스트만 작성, 구현 금지).
  - (b) **RED 게이트 (orchestrator 소유)**: test-author가 작성한 테스트를 실제 실행해 실패(RED) 증거를 캡처하고 falsifiability를 점검한다(AC 관찰 동작 assertion 실패여야 함; import/collection-only 실패는 RED 미충족으로 test-author 재dispatch). 이 게이트를 닫기 전에는 (c)를 dispatch하지 않는다.
  - (c) **impl 병렬 dispatch**: RED 게이트를 통과한 task마다 `sdd-skills:implementation-agent` leaf를 동시 dispatch한다. 입력으로 고정 실패 테스트 + RED 증거를 전달하며, leaf는 GREEN→REFACTOR만 수행한다.
- **cross-wave 중첩 없음**: wave G의 (c) impl과 wave H의 (a) test-author를 동시에 돌리는 cross-wave 중첩은 도입하지 않는다. 3단계 파이프라인은 wave **내부**에만 적용하고, wave끼리는 한 wave가 GREEN 게이트를 닫은 뒤 다음 wave를 시작하는 순차다. 병렬 불가·저확신이면 동일 3단계 흐름을 task별로 하나씩 순차 dispatch한다(file-disjoint 가드레일 + "확신 없으면 순차").
- **용어 구분**: `Execution` phase는 task 단위 병렬 dispatch wave이고, 별도 `Checkpoints` 목록은 review-fix boundary다. 전자는 "무엇을 동시에 dispatch하나", 후자는 "언제 gate를 닫나"를 정한다.
- **progress/report 소유**: leaf는 결과(SUCCESS/PARTIAL/FAILED·TDD표·파일·테스트·UNPLANNED_DEPENDENCY·CONTRACT_MISMATCH·발견)만 반환한다. `CONTRACT_MISMATCH`는 impl-agent가 고정 실패 테스트의 가정 인터페이스 계약이 틀렸다고 보면(테스트를 수정하지 않고) 보고하는 항목으로, autopilot이 test-author 재dispatch 여부를 판정한다. **실행 주체인 autopilot**이 `_sdd/implementation/<YYYY-MM-DD>_implementation_progress_<slug>.md`·`*_implementation_report_<slug>.md`를 canonical 경로·소비 필드로 작성·소유한다(downstream `spec-sync`·`spec-summary` 호환 유지).

### Planning Producer Review Gate

planning producer step은 `sdd-skills:feature-draft-agent` 하나다. producer output은 downstream 소비 전에 `sdd-skills:plan-review-agent` gate를 통과해야 한다.

- `sdd-skills:feature-draft-agent` 직후 `sdd-skills:plan-review-agent`를 호출해 다음을 검증한다:
  - `Part 1: Spec Delta`의 marker/3-section slim shape
  - `Part 2: Implementation and Validation Plan`의 `Contract/Invariant Delta and Coverage`/`Validation Plan` linkage
  - top-level `Risks/Mitigations and Open Questions`
  - downstream planning 입력 적합성
- `sdd-skills:task-ordering-agent`는 planning producer가 아니라 `feature-draft`의 flat task-set에서 dependency edge·topological parallel wave·review checkpoint를 파생하는 ordering step이다. self-check만 수행하며 `sdd-skills:plan-review-agent` producer review gate를 요구하지 않는다(review-fix gate 면제). final Markdown은 artifact로 저장하지 않고 `task_ordering.response`로 downstream `implementation-dispatch-controller`에 hand-off된다.
- gate가 fail이면 producer output을 소비하지 않는다. autopilot은 같은 producer step을 regenerate하도록 요구하고, review finding을 normalize해서 통과 처리하면 안 된다.
- gate는 canonical `subagent_type` 정책도 검증한다. legacy alias가 발견되면 reject/regenerate 대상이다.
- **Regenerate 상한**: 같은 producer step의 reject/regenerate는 최대 2회다. 상한 도달 시 gate를 통과 처리하지 않고 `BLOCKED`로 종료해 잔존 finding과 함께 사용자 결정을 받는다.
- **오케스트레이터 자체도 producer output이다**: Step 5에서 구조 검증 스크립트(`scripts/validate_orchestrator.py` PASS)와 `sdd-skills:plan-review-agent`의 Orchestrator Review Mode gate(Critical/High = 0)를 통과해야 Phase 2로 진행할 수 있다. 미통과 orchestrator에는 `승인 후 실행` 옵션을 제공하지 않는다.

## 3. Global vs Temporary Spec Contract

- global spec은 장기적 SoT다.
- temporary spec은 실행 청사진이다.
- `feature-draft`는 slim `Part 1: Spec Delta`, execution-facing Part 2, top-level risk surface를 만든다.
- `spec-sync`만 global spec을 수정한다. 동일 `spec-sync`는 구현 전(planned spec delta 반영, 조건부 1회)과 구현 완료 후(implemented evidence 동기화, 1회) 최대 2회 호출될 수 있으며, 같은 진입점이 evidence 차이로 동작을 적응한다.
- temporary execution detail을 global spec 본문으로 복사하는 step은 허용되지 않는다.
- global spec은 thin core를 유지해야 하며, feature-level usage/validation/reference를 기본 본문으로 되돌리면 안 된다.

## 4. Acceptance Criteria Contract

- 각 요구사항을 검증 가능한 조건 1개 이상으로 변환한다.
- 프로세스 완료 여부가 아니라 기능 동작 여부를 검증한다.
- feature draft가 있으면 Part 2 `Contract/Invariant Delta and Coverage`와 `Validation Plan`을 AC와 연결한다.

## 5. Reasoning Trace

최소 설명 항목:

- 왜 이 파이프라인 규모로 판단했는가
- 왜 해당 skill 조합을 선택했는가
- global spec과 temporary spec을 어떻게 다룰 것인가
- 왜 테스트 전략이 inline 또는 `ralph-loop-init`인가
- 어떤 SDD 원칙이 강하게 작동했는가

## 6. Review-Fix Contract

- scope (`global` 또는 `per-group`)
- 최대 반복 횟수
- 종료 조건 (`critical = 0 AND high = 0 AND medium = 0`)
- 수정 대상 (`critical/high/medium`)
- MAX 도달 시 분기: critical/high 잔존 -> 중단, medium만 잔존 -> 로그 기록 후 계속 진행
- agent mapping (review/re-review는 correctness ∥ simplicity 2-reviewer 병렬, exit는 두 report의 합집합; `fix`는 단일):
  - `review = sdd-skills:implementation-review-agent`
  - `review = sdd-skills:simplicity-review-agent`
  - `re-review = sdd-skills:implementation-review-agent`
  - `re-review = sdd-skills:simplicity-review-agent`
  - `fix = sdd-skills:implementation-agent`
  - **fix 정책 (finding 종류별 분기)**: correctness finding(동작 버그)은 test-first로 처리한다 — 먼저 그 버그를 노출하는 실패 테스트를 작성(`sdd-skills:test-author-agent` dispatch + orchestrator RED 게이트로 실패 확인)한 뒤 고정 실패 테스트 + RED 증거를 입력으로 `sdd-skills:implementation-agent` leaf를 재dispatch해 fix한다. simplicity/refactor finding은 실패 테스트 없이 `sdd-skills:implementation-agent` leaf로 직접 fix한다. 어느 경우든 `fix = sdd-skills:implementation-agent` 순차 매핑은 유지된다.

추가 규칙:

- `task_ordering.response`의 `Mode`가 `multi-phase`이면 기본값은 `scope = per-group`이다. `single-phase` path나 direct path만 `scope = global`을 기본으로 둘 수 있다.
- review-fix loop는 파이프라인 후처리 섹션이 아니라 각 group의 immediate completion gate다.
- autopilot은 review-fix loop를 추상 단계로 두지 않는다. small/medium/large review path 모두 review step은 반드시 correctness(`sdd-skills:implementation-review-agent`) ∥ simplicity(`sdd-skills:simplicity-review-agent`) 2-reviewer 병렬 subagent 호출이고(exit는 두 report의 합집합), fix step은 반드시 `sdd-skills:implementation-agent` 재호출이다. local inline fallback은 허용되지 않는다.
- **fix step dispatch granularity**: `fix = sdd-skills:implementation-agent` 재호출은 review finding을 fix-task로 보고 **finding 하나씩 순차로** `sdd-skills:implementation-agent` leaf를 dispatch하는 것이다(finding의 영향 파일 = 그 leaf의 Target Files). 별도 fix 분해 기계장치는 없으며, fix step에는 병렬을 도입하지 않는다(finding 수가 적고 상호작용 가능 → 순차 안전). 초기 구현 step의 병렬 dispatch 그룹(§2)과 달리 fix는 순차다.
- `low` finding은 advisory/logged follow-up이다. 기본 `fix_targets`에 포함하지 않으며, critical/high/medium 종료 조건을 만족한 gate를 막지 않는다.
- single-phase path이거나 `scope = global`이면 해당 `implementation` step 직후 즉시 review -> fix -> re-review gate를 수행하고, 종료 조건 충족 전에는 다음 downstream step으로 진행할 수 없다.
- review가 포함된 path의 review-fix gate(single-phase global / per-group의 group gate / final integration review 모두 포함)에는 gate 직후 실행되는 invocation contract가 명시되어야 한다. 최소한 아래를 포함한다.
  - autopilot이 correctness(`sdd-skills:implementation-review-agent`) ∥ simplicity(`sdd-skills:simplicity-review-agent`) 2-reviewer subagent를 즉시 병렬 호출한다는 사실 (exit는 두 report의 합집합)
  - review 입력에 포함할 파일/증거 (해당 gate 범위의 변경 파일 전체 + 관련 테스트 결과)
  - review 프롬프트 계약
  - fix 재호출 조건과 fix 프롬프트 계약
  - re-review 재호출 조건과 re-review 프롬프트 계약 (correctness ∥ simplicity 각 reviewer에 해당 lens의 기존 review 리포트 경로를 전달해 re-review mode로 진입시킨다 — 새 리포트 생성이 아니라 각 lens 기존 리포트의 `Current Status` 갱신 + `Iteration History` append)
- `scope = per-group`이면 아래 조건을 함께 충족해야 한다.
  - **Group 경계**: `task_ordering.response`의 별도 `Checkpoints` 목록에 지정된 phase 직후 review-fix gate를 닫는다. 마지막 phase는 목록 기재 여부와 무관하게 implicit checkpoint다. 목록이 `없음`이면 마지막 phase만 경계다.
  - **Group 내 phase**(checkpoint 목록에 없는 phase)는 light validation(test/typecheck/exit criteria)만 수행한다. review-fix gate 없이 다음 phase로 진행한다.
  - **Mid-group emergency**: group 내 phase의 light validation이 `critical` 이슈를 잡으면 group boundary forced early로 즉시 review-fix gate를 트리거한다.
  - downstream `implementation-dispatch-controller` step에 `Execution Mode: phase-iterative`와 `Phase Source`가 선언되어 있어야 한다.
  - Review-Fix Loop에 아래 필드를 함께 명시해야 한다.
    - `group exit criteria`
    - `carry-over policy`
    - `group boundary` (`task_ordering.response`의 `Checkpoints`를 runtime에 해석한다는 선언)
- `scope = per-group`이면 각 Checkpoint phase 직후 즉시 같은 group 범위의 review -> fix -> re-review -> group validation gate를 닫아야 한다. gate가 닫히기 전에는 다음 group이나 downstream step으로 진행할 수 없다.
- `medium` 이슈도 기본적으로 group exit blocker다. carry-over는 정책이 명시적으로 허용하는 severity/조건/로그 근거가 있을 때만 가능하다.
- **Final integration review (adaptive)**:
  - 그룹 1개 (`Checkpoints` 해석 결과 마지막 phase gate만 발생): 마지막 group gate가 final integration review를 겸한다. 별도 1회를 추가하지 않는다.
  - 그룹 2개 이상: 마지막 group gate 후 cross-group regression 전용으로 `final integration review`를 1회 추가 실행한다.
- `Review-Fix Loop`에는 가능하면 아래 invocation prompt contract를 함께 명시한다.
  - `review invocation prompt contract`
  - `fix invocation prompt contract`
  - `re-review invocation prompt contract`
  - 그룹 2개 이상인 경우 `final integration review prompt contract` (필수)

## 7. Test Strategy Contract

반드시 포함할 필드:

- 방식 (`inline` 또는 `ralph-loop-init`)
- 실행 명령
- 선택 근거
- 사용자 보고 형식

필수 규칙:

- 테스트/검증 단계는 건너뛸 수 없다.
- temporary spec이 있으면 `Validation Plan`의 `V*` 항목과 테스트 전략의 대응 관계를 설명해야 한다.
- 테스트 결과는 사용자에게 명시적으로 보고한다.

## 8. feature-draft / task-ordering / spec-sync Specific Contract

### feature-draft
- feature draft 파일 존재
- `Part 1: Spec Delta` 존재, `<!-- spec-update-todo-input-start -->` / `<!-- spec-update-todo-input-end -->` 마커 포함
- Part 1 필수 섹션은 `Change Summary`, `Scope Delta`, `Persistent Spec Implications`뿐임
- `Part 2: Implementation and Validation Plan` 존재, `Contract/Invariant Delta and Coverage`와 `Validation Plan` linkage 포함
- `Part 2`는 flat task-set(각 task 정의 + `Target Files`)을 산출한다. dependency edge·phase 분할·실행 순서·Checkpoint는 포함하지 않는다(그것은 `task-ordering` 소관)
- top-level `Risks/Mitigations and Open Questions` 존재

### task-ordering
- 파일 artifact를 생성하지 않고 final Markdown을 부모에게 반환함. `출력 파일` 필드는 `없음 (transient final response)`임
- final Markdown은 `Status`, `Source`, `Mode`, `Execution`, `Dependencies`, `Checkpoints`, `Notes`를 포함함
- `Source`는 task 본문의 authoritative source인 feature draft 경로임
- `Execution`의 각 phase는 dependency를 만족하는 topological parallel wave이며 모든 task ID를 정확히 한 번 포함함
- `Dependencies`는 `dependent ← prerequisites` 방향으로 표기함
- `Checkpoints`는 phase별 metadata가 아닌 별도 review-boundary 목록이며 이유를 함께 적음. 마지막 phase는 implicit checkpoint이므로 생략 가능함
- task 정의·AC·Validation Plan을 복사하거나 재산출하지 않음
- autopilot이 final response를 `task_ordering.response`로 보존하고 downstream `implementation-dispatch-controller`를 `Execution Mode: phase-iterative`, `Phase Source: task_ordering.response`로 연결함
- planning producer가 아니라 ordering 파생 step이므로 self-check만 수행하고 `plan-review` producer review gate를 요구하지 않음

### spec-sync
- global spec 업데이트 완료
- 같은 진입점이 evidence 차이로 동작을 적응한다. 구현 전 planned 호출(조건부)은 planned persistent information만 반영하고, 구현 후 sync 호출은 implemented + verified information만 반영한다.
- temporary execution detail이 global spec 본문으로 누수되지 않음
- 미구현/미검증 delta는 deferred로 남음
- 구현 후 sync 호출의 실행 시점은 모든 required implementation-scoped review-fix gate, required validation/test, 필요한 경우 final integration review가 끝난 뒤여야 함

## 9. Error Handling Contract

필수 필드:

- 재시도 횟수
- 핵심 단계
- 비핵심 단계
- `BLOCKED` 반환 처리 규칙 (`retry`, `stop`, `fallback` 중 어느 분기를 타는지)

공통 규칙 (orchestrator가 달리 명시하지 않는 한 기본값):

- **빈/계약 불일치 반환**: subagent가 빈 결과 또는 출력 계약과 다른 형식을 반환하면 같은 입력으로 1회 재dispatch한다. 재발 시 해당 step을 `failed`로 기록하고, 핵심 단계면 중단·비핵심 단계면 로그 후 계속한다.
- **병렬 dispatch group 부분 실패**: 성공한 leaf의 결과는 보존한다. 실패한 task만 순차로 1회 재시도하고, 잔존 실패가 있으면 group을 `failed`로 닫고 다음 group이나 downstream step으로 진행하지 않는다.
- **timeout**: timeout은 완료가 아니다. 더 기다리거나 controlled stop을 기록한 뒤에만 step 상태를 확정한다.
- 모든 재시도/중단/건너뛰기 결정은 로그에 남긴다.

## 10. Pipeline Log Contract

로그 파일은 아래 블록을 가진다.

### Meta
- request
- orchestrator
- started
- pipeline

### Status Table
- Step
- Agent
- Status
- Output

### Execution Log Entries
- 시간
- 출력
- 핵심 결정사항
- 이슈

### Final Summary
- 완료 시간
- 총 소요 시간
- 실행 결과
- 생성/수정 파일 수
- Review 횟수
- 테스트 결과
- 스펙 동기화 여부
- 잔여 이슈

## 11. Resume Contract

미완료 로그(`pending`/`in_progress`/`failed`)에서 재개할 때 적용한다.

1. **재검증 우선**: 재개 전 해당 orchestrator를 현행 계약으로 다시 검증한다 (Step 5와 동일: 구조 스크립트 + 필요 시 plan-review gate). legacy alias 등 현행 계약 위반이 발견되면 그대로 실행하지 않고 reject/regenerate 후 사용자 확인을 받는다.
2. **completed step**: 재실행하지 않는다. 단, 선언된 materialized output이 실존하는지 확인하고, 없으면 해당 step을 `failed`로 강등해 재실행 대상에 포함한다. `task-ordering`은 artifact 대신 로그에 보존된 `task_ordering.response`가 없으면 재실행한다.
3. **in_progress / failed step**: step은 자신의 선언된 출력만 다시 materialize한다는 전제(idempotent)로 처음부터 재실행한다. 부분 산출물은 신뢰하지 않는다.
4. **gate 상태**: implementation step이 `completed`라도 같은 범위의 review-fix gate가 닫힌 기록이 로그에 없으면 gate부터 재개한다.
5. 재개 사실, 기준 로그, 강등된 step을 새 Execution Log Entry로 기록한다.
