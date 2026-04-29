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

각 custom-agent step은 아래 4개 필드를 반드시 가진다.

- `Claude subagent_type`
- `입력 파일`
- `출력 파일`
- `프롬프트`

선택 필드:

- `Execution Mode`
  - `phase-iterative`는 downstream `implementation` step이 `implementation-plan` output을 소비할 때 사용한다.
  - 이 값이 있으면 phase count와 boundary를 Step 4 generation 시점에 precompute하지 않고 runtime metadata로 해석한다.
- `Phase Source`
  - `Execution Mode: phase-iterative` implementation step일 때 필수다.
  - 값은 runtime에 읽을 `implementation-plan` output 경로다.

허용 `subagent_type`:

- `feature-draft`
- `spec-update-todo`
- `implementation-plan`
- `implementation`
- `implementation-review`
- `spec-update-done`
- `spec-review`
- `ralph-loop-init`

추가 규칙:

- `implementation` step은 단독 완료 step이 아니다. 같은 범위의 `Review-Fix Loop`와 required validation gate가 즉시 뒤따르며, gate가 닫히기 전에는 다음 downstream step으로 진행할 수 없다.
- review가 포함된 path에서는 `implementation`과 `implementation-review`를 항상 subagent step으로 사용한다. autopilot 부모가 local inline implementation/review로 대체하면 안 된다.
- downstream `implementation` step이 `implementation-plan` output을 소비하면, 해당 step은 `Execution Mode: phase-iterative`와 `Phase Source`를 함께 선언해야 한다.
- 오케스트레이터의 `출력 파일`에 적힌 future artifact는 planned output이며, 현재 실행 중인 step만 자신의 출력물을 materialize할 수 있다.
- **Invariant (Phase Source 출처)**: `Execution Mode: phase-iterative`가 선언된 step의 `Phase Source`는 반드시 `implementation-plan` output이어야 한다. `feature-draft` 산출물을 `Phase Source`로 사용하면 Step 5 verification에서 reject하고 `implementation-plan` step을 파이프라인에 삽입한다.
- **Invariant (multi-phase ⇒ implementation-plan 의무)**: 오케스트레이터 생성 시 multi-phase 실행으로 판단되면, planning precedence에서 `implementation-plan`을 반드시 포함한다. feature-draft → implementation 직행은 single-phase 경로에 한정한다.

### Model Routing

각 subagent 호출 시 아래 모델을 `model` 파라미터로 명시한다. 에이전트 정의 파일의 프론트매터는 `model: inherit`이므로 부모(autopilot)가 호출 시점에 전달한 `model` 값이 그대로 사용된다. 오케스트레이터는 step별로 모델을 명시해 이 표를 그대로 집행한다.

| subagent_type          | model    | 근거                              |
|------------------------|----------|-----------------------------------|
| `feature-draft`        | `opus`   | 설계 판단, 스펙 구조화             |
| `implementation-plan`  | `opus`   | 의존성 분석, 실행 순서 설계         |
| `implementation`       | `sonnet` | 코드 작성·반복 적용 (효율 최적화)   |
| `implementation-review`| `opus`   | 구현 깊이 분석, 결함 발견           |
| `ralph-loop-init`      | `opus`   | 테스트 전략 설계, 고수준 판단       |
| `spec-update-todo`     | `sonnet` | diff 기반 스펙 반영                |
| `spec-update-done`     | `sonnet` | diff 기반 스펙 반영                |
| `spec-review`          | `sonnet` | 스펙 간 비교 분석                  |

#### Review-Fix Gate Model Assignment

review-fix gate(single-phase global, multi-phase per-group, final integration review 모두 포함)에서는 호출 역할마다 모델을 분리해서 명시한다.

- `review` / `re-review` -> `implementation-review` (`opus`)
- `fix` -> `implementation` (`sonnet`)
- `final integration review` -> `implementation-review` (`opus`)

오케스트레이터의 `agent_mapping`은 모델을 함께 표기한다. 예: `review = implementation-review (model: opus)`, `fix = implementation (model: sonnet)`, `re-review = implementation-review (model: opus)`. autopilot이 gate를 집행할 때 표기된 모델을 그대로 `model` 파라미터로 전달한다.

## 3. Global vs Temporary Spec Contract

- global spec은 장기적 SoT다.
- temporary spec은 실행 청사진이다.
- `feature-draft`는 temporary spec 7섹션을 만든다.
- `spec-update-todo`와 `spec-update-done`만 global spec을 수정한다.
- temporary execution detail을 global spec 본문으로 복사하는 step은 허용되지 않는다.
- global spec은 thin core를 유지해야 하며, feature-level usage/validation/reference를 기본 본문으로 되돌리면 안 된다.

## 4. Acceptance Criteria Contract

- 각 요구사항을 검증 가능한 조건 1개 이상으로 변환한다.
- 프로세스 완료 여부가 아니라 기능 동작 여부를 검증한다.
- temporary spec이 있으면 `Contract/Invariant Delta`와 `Validation Plan`을 AC와 연결한다.

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
- 수정 대상 (`critical/high/medium/low`)
- MAX 도달 시 분기: critical/high 잔존 -> 중단, medium만 잔존 -> 로그 기록 후 계속 진행
- agent mapping: `review = implementation-review`, `fix = implementation`, `re-review = implementation-review`

추가 규칙:

- multi-phase `implementation-plan`을 소비하면 기본값은 `scope = per-group`이다. single-phase path나 direct path만 `scope = global`을 기본으로 둘 수 있다.
- review-fix loop는 파이프라인 후처리 섹션이 아니라 각 group의 immediate completion gate다.
- autopilot은 review-fix loop를 추상 단계로 두지 않는다. small/medium/large review path 모두 review step은 반드시 `implementation-review` subagent 호출이고, fix step은 반드시 `implementation` subagent 재호출이다. local inline fallback은 허용되지 않는다.
- single-phase path이거나 `scope = global`이면 해당 `implementation` step 직후 즉시 review -> fix -> re-review gate를 수행하고, 종료 조건 충족 전에는 다음 downstream step으로 진행할 수 없다.
- review가 포함된 path의 review-fix gate(single-phase global / per-group의 group gate / final integration review 모두 포함)에는 gate 직후 실행되는 invocation contract가 명시되어야 한다. 최소한 아래를 포함한다.
  - autopilot이 `implementation-review` subagent를 즉시 호출한다는 사실
  - review 입력에 포함할 파일/증거 (해당 gate 범위의 변경 파일 전체 + 관련 테스트 결과)
  - review 프롬프트 계약
  - fix 재호출 조건과 fix 프롬프트 계약
  - re-review 재호출 조건과 re-review 프롬프트 계약
- `scope = per-group`이면 아래 조건을 함께 충족해야 한다.
  - **Group 경계**: `implementation-plan` output의 각 phase에 `Checkpoint: true/false` 필드가 있다. `Checkpoint=true` phase 직후에 review-fix gate를 닫는다. 마지막 phase는 explicit 값과 무관하게 implicit `Checkpoint=true`로 처리한다.
  - **Group 내 phase**(Checkpoint=false)는 light validation(test/typecheck/exit criteria)만 수행한다. review-fix gate 없이 다음 phase로 진행한다.
  - **Mid-group emergency**: group 내 phase의 light validation이 `critical` 이슈를 잡으면 group boundary forced early로 즉시 review-fix gate를 트리거한다.
  - downstream `implementation` step에 `Execution Mode: phase-iterative`와 `Phase Source`가 선언되어 있어야 한다.
  - Review-Fix Loop에 아래 필드를 함께 명시해야 한다.
    - `group exit criteria`
    - `carry-over policy`
    - `group boundary` (Checkpoint=true phase 목록 또는 "마지막 phase 1회" 같은 표현)
- `scope = per-group`이면 각 Checkpoint phase 직후 즉시 같은 group 범위의 review -> fix -> re-review -> group validation gate를 닫아야 한다. gate가 닫히기 전에는 다음 group이나 downstream step으로 진행할 수 없다.
- `medium` 이슈도 기본적으로 group exit blocker다. carry-over는 정책이 명시적으로 허용하는 severity/조건/로그 근거가 있을 때만 가능하다.
- **Final integration review (adaptive)**:
  - 그룹 1개 (전체 plan의 Checkpoint gate가 1회만 발생): 마지막 group gate가 final integration review를 겸한다. 별도 1회를 추가하지 않는다.
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

## 8. feature-draft / implementation-plan / spec-update-* Specific Contract

### feature-draft
- feature draft 파일 존재
- Part 1 temporary spec 7섹션 존재
- `Contract/Invariant Delta`와 `Validation Plan` linkage 존재

### implementation-plan
- implementation plan 존재
- `Contract/Invariant Delta Coverage` 존재
- task와 `Target Files`가 정의됨
- `feature-draft` 이후 확장 단계인지, 또는 standalone 예외인지가 드러남
- 각 phase에 `goal`, `task set / dependency closure`, `validation focus`, `exit criteria`, `carry-over policy`, `checkpoint`가 포함됨
- `Checkpoint=true` phase는 이유를 설명하는 `Checkpoint Reason` 한 줄을 동반함
- downstream `implementation` step이 이 artifact를 소비할 때는 `Execution Mode: phase-iterative`와 `Phase Source`로 연결되어야 함

### spec-update-todo
- global spec 업데이트 완료
- planned persistent information만 반영됨
- temporary execution detail이 global spec 본문으로 누수되지 않음

### spec-update-done
- global spec 업데이트 완료
- implemented + verified information만 반영됨
- 미구현/미검증 delta는 deferred로 남음
- 실행 시점은 모든 required implementation-scoped review-fix gate, required validation/test, 필요한 경우 final integration review가 끝난 뒤여야 함

## 9. Error Handling Contract

- 재시도 횟수
- 핵심 단계
- 비핵심 단계

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
