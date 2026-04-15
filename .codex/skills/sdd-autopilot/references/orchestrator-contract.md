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

선택 섹션:

- `Execution Profiles`
  - step별 `model` / `reasoning_effort` 기본값 또는 `profile_key`를 선언할 수 있다.
  - 이 섹션을 사용할 때는 `references/execution-profile-policy.md`와 정합해야 한다.
  - 모든 step과 review-fix loop가 policy 기본값을 그대로 따를 때는 생략할 수 있다.
  - 이 섹션은 기본값 레이어다. step-level 또는 loop-level 프로파일이 있으면 더 좁은 범위의 선언이 우선한다.
  - 기본 policy에서 벗어나는 선언은 사용자 요청이 있을 때만 허용한다.
  - 아래 중 하나라도 해당하면 명시를 권장하는 것이 아니라 사실상 필수로 본다.
    - policy 기본값에서 감등 또는 승격이 발생한다.
    - 같은 `agent_type`이라도 step별로 서로 다른 프로파일을 사용한다.
    - review-fix loop 또는 `final integration review`에 별도 프로파일을 선언한다.
    - multi-phase path라 phase gate 해석을 문서에 남겨야 한다.
    - 재실행 재현성이나 품질 게이트 근거를 오케스트레이터 자체에 남겨야 한다.

### Generation Boundary

- autopilot의 orchestrator generation 단계에서 실제로 생성 가능한 산출물은 `_sdd/pipeline/orchestrators/orchestrator_<topic>.md` 하나뿐이다.
- `_sdd/drafts/*`, `_sdd/implementation/*`, `_sdd/pipeline/log_*`, `_sdd/pipeline/report_*`, 코드/테스트 출력은 오케스트레이터 안에서 future step의 planned output으로 선언할 수는 있지만, 해당 step이 실행되기 전에는 materialize하면 안 된다.

## 2. Step Contract

각 custom-agent step은 아래 4개 필드를 반드시 가진다.

- `Codex agent_type`
- `입력 파일`
- `출력 파일`
- `프롬프트`

선택 필드:

- `Execution profile`
  - `profile_key` 또는 `model / reasoning_effort` 표시를 허용한다.
  - 예: `draft_strict` (`gpt-5.4 / xhigh`)
  - step-level 프로파일은 전체 `Execution Profiles` section을 생략한 경우에도 사용할 수 있다.
  - 기본 policy와 완전히 동일하고 해석 여지가 없으면 step-level 표기도 생략할 수 있다.
  - step-level 프로파일은 같은 agent_type에 대한 section-level 기본값보다 우선한다.
- `Execution Mode`
  - `phase-iterative`는 downstream `implementation` step이 `implementation_plan` output을 소비할 때 사용한다.
  - 이 값이 있으면 phase count와 boundary를 Step 4 generation 시점에 precompute하지 않고 runtime metadata로 해석한다.
- `Phase Source`
  - `Execution Mode: phase-iterative` implementation step일 때 필수다.
  - 값은 runtime에 읽을 `implementation_plan` output 경로다.

허용 `agent_type`:

- `feature_draft`
- `spec_update_todo`
- `implementation_plan`
- `implementation`
- `implementation_review`
- `spec_update_done`
- `spec_review`
- `ralph_loop_init`

추가 규칙:

- `implementation` step은 단독 완료 step이 아니다. 같은 범위의 `Review-Fix Loop`와 required validation gate가 즉시 뒤따르며, gate가 닫히기 전에는 다음 downstream step으로 진행할 수 없다.
- review가 포함된 path에서는 `implementation`과 `implementation_review`를 항상 custom-agent step으로 사용한다. autopilot 부모가 local inline implementation/review로 대체하면 안 된다.
- downstream `implementation` step이 `implementation_plan` output을 소비하면, 해당 step은 `Execution Mode: phase-iterative`와 `Phase Source`를 함께 선언해야 한다.
- 오케스트레이터의 `출력 파일`에 적힌 future artifact는 planned output이며, 현재 실행 중인 step만 자신의 출력물을 materialize할 수 있다.

## 3. Global vs Temporary Spec Contract

- global spec은 장기적 SoT다.
- temporary spec은 실행 청사진이다.
- `feature_draft`는 temporary spec 7섹션을 만든다.
- `spec_update_todo`와 `spec_update_done`만 global spec을 수정한다.
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
- 왜 테스트 전략이 inline 또는 `ralph_loop_init`인가
- 어떤 SDD 원칙이 강하게 작동했는가

## 6. Review-Fix Contract

- scope (`global` 또는 `per-phase`)
- 최대 반복 횟수
- 종료 조건 (`critical = 0 AND high = 0 AND medium = 0`)
- 수정 대상 (`critical/high/medium/low`)
- MAX 도달 시 분기: critical/high 잔존 -> 중단, medium만 잔존 -> 로그 기록 후 계속 진행
- agent mapping: `review = implementation_review`, `fix = implementation`, `re-review = implementation_review`

추가 규칙:

- multi-phase `implementation_plan`을 소비하면 기본값은 `scope = per-phase`다. single-phase path나 direct path만 `scope = global`을 기본으로 둘 수 있다.
- review-fix loop는 파이프라인 후처리 섹션이 아니라 각 `implementation` 실행 단위의 immediate completion gate다.
- autopilot은 review-fix loop를 추상 단계로 두지 않는다. small/medium/large review path 모두 review step은 반드시 `implementation_review` agent 호출이고, fix step은 반드시 `implementation` agent 재호출이다. local inline fallback은 허용되지 않는다.
- single-phase path이거나 `scope = global`이면 해당 `implementation` step 직후 즉시 review -> fix -> re-review gate를 수행하고, 종료 조건 충족 전에는 다음 downstream step으로 진행할 수 없다.
- review가 포함된 path의 `implementation` step에는 implementation 직후 실행되는 invocation contract가 명시되어야 한다. 최소한 아래를 포함한다.
  - autopilot이 `implementation_review` agent를 즉시 호출한다는 사실
  - review 입력에 포함할 파일/증거
  - review 프롬프트 계약
  - fix 재호출 조건과 fix 프롬프트 계약
  - re-review 재호출 조건과 re-review 프롬프트 계약
- `scope = per-phase`면 아래 조건을 함께 충족해야 한다.
  - downstream `implementation` step에 `Execution Mode: phase-iterative`와 `Phase Source`가 선언되어 있어야 한다.
  - Review-Fix Loop에 아래 필드를 함께 명시해야 한다.
  - `phase exit criteria`
  - `carry-over policy`
  - `final integration review`
- `scope = per-phase`면 각 phase의 `implementation` 직후 즉시 같은 범위의 review -> fix -> re-review -> phase validation gate를 닫아야 한다. gate가 닫히기 전에는 다음 phase나 downstream step으로 진행할 수 없다.
- 필요하면 아래 선택 필드를 함께 명시할 수 있다.
  - `review_profile`
  - `fix_profile`
  - `final_integration_review_profile`
- loop-level 프로파일은 같은 agent_type에 대한 section-level 기본값보다 우선한다.
- `final_integration_review_profile`은 실제 final integration review가 존재할 때만 유효하다.
- `scope = global`에서 이 필드를 쓰려면 아래 둘 중 하나가 오케스트레이터에 명시되어야 한다.
  - 별도 global `final integration review` 실행 선언
  - final integration review를 수행하는 독립 `implementation_review` step
- `medium` 이슈도 기본적으로 phase exit blocker다. carry-over는 정책이 명시적으로 허용하는 severity/조건/로그 근거가 있을 때만 가능하다.
- `final integration review`는 마지막 phase 이후에 반드시 1회 실행한다.
- `Review-Fix Loop`에는 가능하면 아래 invocation prompt contract를 함께 명시한다.
  - `review invocation prompt contract`
  - `fix invocation prompt contract`
  - `re-review invocation prompt contract`
  - multi-phase path인 경우 `final integration review prompt contract`

## 7. Test Strategy Contract

반드시 포함할 필드:

- 방식 (`inline` 또는 `ralph_loop_init`)
- 실행 명령
- 선택 근거
- 사용자 보고 형식

필수 규칙:

- 테스트/검증 단계는 건너뛸 수 없다.
- temporary spec이 있으면 `Validation Plan`의 `V*` 항목과 테스트 전략의 대응 관계를 설명해야 한다.
- 테스트 결과는 사용자에게 명시적으로 보고한다.

## 8. feature_draft / implementation_plan / spec-update-* Specific Contract

### feature_draft
- feature draft 파일 존재
- Part 1 temporary spec 7섹션 존재
- `Contract/Invariant Delta`와 `Validation Plan` linkage 존재

### implementation_plan
- implementation plan 존재
- `Contract/Invariant Delta Coverage` 존재
- task와 `Target Files`가 정의됨
- `feature-draft` 이후 확장 단계인지, 또는 standalone 예외인지가 드러남
- 각 phase에 `goal`, `task set / dependency closure`, `validation focus`, `exit criteria`, `carry-over policy`가 포함됨
- downstream `implementation` step이 이 artifact를 소비할 때는 `Execution Mode: phase-iterative`와 `Phase Source`로 연결되어야 함

### spec_update_todo
- global spec 업데이트 완료
- planned persistent information만 반영됨
- temporary execution detail이 global spec 본문으로 누수되지 않음

### spec_update_done
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
