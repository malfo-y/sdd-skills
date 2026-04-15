# Sample Orchestrator

이 파일은 autopilot이 생성하는 오케스트레이터의 품질 기준 예시다.

review가 포함된 small/medium/large 모든 path에서는 `implementation`과 `implementation-review`가 항상 subagent mapping으로 실행된다. 경로가 단순하더라도 부모 autopilot이 local implementation/review로 대체하지 않는다.

## Example A: single-phase medium direct path

사용자 요청: `/autopilot JWT 기반 인증 시스템 구현`

```markdown
# Orchestrator: JWT 인증 시스템

**생성일**: 2026-04-10T14:30:00
**규모**: 중규모
**생성자**: autopilot

## 기능 설명

JWT 기반 인증 시스템을 구현한다. 로그인, 로그아웃, 토큰 갱신 기능을 포함한다.

## Acceptance Criteria
- [ ] 로그인 성공 시 access/refresh token이 발급된다.
- [ ] refresh token 갱신이 동작하고 만료 정책이 적용된다.
- [ ] 로그아웃 시 refresh token이 무효화된다.
- [ ] 관련 검증이 테스트 또는 리뷰 evidence와 연결된다.

## Reasoning Trace

- non-trivial change라 planning entry는 `feature-draft`로 시작한다.
- feature draft Part 2가 task/dependency/validation을 충분히 제공하므로 `implementation-plan`은 생략한다.
- single-phase medium path라 `Review-Fix Loop.scope`는 `global`로 유지하되, `implementation` 직후 즉시 completion gate로 닫는다.
- review가 포함된 direct path이므로 구현과 리뷰 모두 subagent mapping으로 유지한다.
- 테스트는 짧은 API/서비스 검증 중심이라 인라인 전략을 선택한다.

## Pipeline Steps

### Step 1: feature-draft
**Claude subagent_type**: `feature-draft`
**입력 파일**: `_sdd/spec/main.md`
**출력 파일**: `_sdd/drafts/2026-04-10_feature_draft_jwt_auth.md`

**프롬프트**:
JWT 기반 인증 시스템에 대한 feature draft를 작성하세요.
Part 1에는 temporary spec 7섹션을 포함하고, `Contract/Invariant Delta`와 `Validation Plan`을 ID로 연결하세요.
Part 2에는 implementation이 직접 읽을 수 있는 Target Files, dependency, validation detail을 포함하세요.

### Step 2: implementation
**Claude subagent_type**: `implementation`
**입력 파일**:
- `_sdd/drafts/2026-04-10_feature_draft_jwt_auth.md`
- `_sdd/spec/main.md`
**출력 파일**:
- `src/middleware/auth.js`
- `src/routes/auth.js`
- `src/services/auth-service.js`
- `src/services/token-service.js`
- `src/models/user.js`
- `test/services/auth-service.test.js`

**프롬프트**:
feature draft를 기반으로 구현을 진행하세요.
temporary spec의 `Contract/Invariant Delta`와 `Validation Plan`을 기준으로 TDD 방식으로 진행하세요.

**Immediate review-fix gate (must finish before Step 3)**:
- `scope`: `global`
- `max_rounds`: 3
- `exit_condition`: `critical = 0 AND high = 0 AND medium = 0`
- `fix_targets`: `critical/high/medium/low`
- `timing`: Step 2 `implementation` 직후 즉시 실행하는 completion gate
- `agent_mapping`: `review = implementation-review`, `fix = implementation`, `re-review = implementation-review`
- `execution_sequence`: `implementation -> implementation-review -> implementation (if needed) -> implementation-review`
- autopilot은 Step 2 구현 직후 같은 범위로 `implementation-review` subagent를 즉시 호출한다.
- review 입력에는 최소한 `_sdd/drafts/2026-04-10_feature_draft_jwt_auth.md`, `_sdd/spec/main.md`, 현재 변경 파일 목록, 관련 테스트 결과를 포함한다.
- `review invocation prompt contract`:
  - "방금 끝난 JWT 인증 구현 범위만 검토하세요. 응답은 findings first여야 하며, 각 finding은 severity, 파일/라인, 관련 Acceptance Criteria 또는 temporary spec linkage, 근거, 권장 수정 방향을 포함해야 합니다."
- `fix invocation prompt contract`:
  - "직전 `implementation-review` finding 중 `critical/high/medium`만 닫으세요. unrelated dirty changes를 되돌리지 말고, 수정 후 관련 테스트가 다시 실행 가능한 상태를 유지하세요."
- `re-review invocation prompt contract`:
  - "직전 review finding이 실제로 해소되었는지 먼저 검증하고, 같은 범위에서 새 `critical/high/medium`이 남는지만 다시 보고하세요. findings first 형식을 유지하세요."
- `implementation-review` 결과에 `critical/high/medium`이 하나라도 있으면 autopilot은 그 finding만 입력으로 묶어 같은 범위의 `implementation` subagent를 다시 호출한다.
- fix 후 autopilot은 같은 scope로 `implementation-review` subagent를 재호출한다.
- 이 gate와 required inline validation이 모두 닫힌 뒤에만 Step 3으로 진행한다.

### Step 3: spec-update-done
**Claude subagent_type**: `spec-update-done`
**입력 파일**:
- `_sdd/spec/main.md`
- `_sdd/drafts/2026-04-10_feature_draft_jwt_auth.md`
- 구현된 코드 파일
**출력 파일**: `_sdd/spec/main.md`

**프롬프트**:
JWT 인증 시스템 구현 완료 기준으로 global spec을 실제 코드와 동기화하세요.
temporary spec의 실행 정보는 버리고, 구현되어 검증된 persistent repo-wide information만 global spec에 반영하세요.

**Precondition**:
Step 2에 연결된 immediate review-fix gate와 required inline validation이 모두 닫힌 뒤에만 실행한다.

## Review-Fix Loop

- 이 오케스트레이터의 authoritative 순서와 프롬프트 계약은 Step 2의 `Immediate review-fix gate`에 인라인으로 고정한다.
- 별도 후처리 loop는 없고, Step 2 gate가 닫히기 전에는 `spec-update-done`으로 진행할 수 없다.

## Test Strategy

- `mode`: `inline`
- `commands`: 관련 서비스 테스트 + 인증 라우트 smoke 검증
- `rationale`: 변경 범위가 서비스/라우트 단위에 닫혀 있어 인라인 검증만으로도 `Validation Plan`을 닫을 수 있다.
- `reporting`: 통과/실패 건수와 잔여 수동 확인 항목을 `_sdd/pipeline/report_<topic>_<timestamp>.md`에 기록

## Error Handling

- `retries`: feature-draft/spec-update-done는 1회, implementation/review-fix loop는 최대 3회 재시도
- `critical_steps`: Step 2 immediate review-fix gate, inline test
- `non_critical_steps`: spec wording polish
- `failure_policy`: review-fix gate를 닫지 못하거나 inline test가 실패하면 Step 3으로 진행하지 않고 보고서와 로그에 blocker를 남긴다
```

## Example B: multi-phase expanded path

사용자 요청: `/autopilot 결제 시스템 전체 구현`

```markdown
# Orchestrator: 결제 시스템

**생성일**: 2026-04-10T16:00:00
**규모**: 대규모
**생성자**: autopilot

## 기능 설명

Stripe 기반 결제 시스템을 구현한다. 결제 생성, 웹훅 처리, 환불 로직, 운영 상태 동기화를 포함한다.

## Acceptance Criteria
- [ ] 결제 생성과 상태 전환이 Stripe 계약과 일치한다.
- [ ] 웹훅 서명 검증과 재시도 처리가 구현된다.
- [ ] 환불/실패/보상 흐름이 테스트 또는 리뷰 evidence로 검증된다.
- [ ] multi-phase implementation에서 phase exit criteria와 최종 통합 리뷰가 모두 충족된다.

## Reasoning Trace

- non-trivial planning entry는 `feature-draft`로 고정한다.
- planned persistent global alignment가 있으므로 `spec-update-todo`를 조건부로 추가한다.
- 구현 범위가 크고 dependency chain이 깊어서 `implementation-plan`으로 phase/task breakdown을 확장한다.
- Step 4 generation 시점에는 orchestrator file만 생성하고 phase count/boundary는 아직 runtime metadata라서, downstream `implementation` step을 flat single-shot으로 쓰지 않고 `Execution Mode: phase-iterative` + `Phase Source`로 선언한다.
- multi-phase plan이므로 `Review-Fix Loop.scope = per-phase`를 사용하고 각 phase `implementation` 직후 immediate gate를 닫은 뒤, 마지막에 `final integration review` 후 `spec-update-done`까지 연결한다.

## Pipeline Steps

### Step 1: feature-draft
**Claude subagent_type**: `feature-draft`
**입력 파일**:
- `_sdd/spec/main.md`
- `_sdd/spec/components.md`
**출력 파일**: `_sdd/drafts/2026-04-10_feature_draft_payment_system.md`

**프롬프트**:
Stripe 기반 결제 시스템에 대한 feature draft를 작성하세요.
Part 1에는 temporary spec 7섹션과 `Contract/Invariant Delta`, `Validation Plan` ID linkage를 포함하세요.
Part 2에는 후속 `implementation-plan`이 phase/task 수준으로 확장할 수 있도록 Target Files, dependency, validation detail을 남기세요.

### Step 2: spec-update-todo
**Claude subagent_type**: `spec-update-todo`
**입력 파일**:
- `_sdd/spec/main.md`
- `_sdd/drafts/2026-04-10_feature_draft_payment_system.md`
**출력 파일**: `_sdd/spec/main.md`

**프롬프트**:
결제 시스템 구현 전에 필요한 persistent global alignment만 global spec에 반영하세요.
temporary execution detail은 넣지 말고, 이후 `implementation-plan`과 `implementation`이 읽어야 할 repo-wide invariant만 정리하세요.

### Step 3: implementation-plan
**Claude subagent_type**: `implementation-plan`
**입력 파일**:
- `_sdd/drafts/2026-04-10_feature_draft_payment_system.md`
- `_sdd/spec/main.md`
**출력 파일**: `_sdd/implementation/2026-04-10_implementation_plan_payment_system.md`

**프롬프트**:
feature draft 이후 확장 단계로서 multi-phase implementation plan을 작성하세요.
각 phase마다 `goal`, `task set / dependency closure`, `validation focus`, `exit criteria`, `carry-over policy`를 명시하고, downstream `implementation`이 phase-iterative로 소비할 수 있게 구조화하세요.

### Step 4: implementation
**Claude subagent_type**: `implementation`
**Execution Mode**: `phase-iterative`
**Phase Source**: `_sdd/implementation/2026-04-10_implementation_plan_payment_system.md`
**입력 파일**:
- `_sdd/implementation/2026-04-10_implementation_plan_payment_system.md`
- `_sdd/spec/main.md`
**출력 파일**:
- 결제 서비스/웹훅/환불 관련 코드 및 테스트 파일

**프롬프트**:
`Phase Source`의 현재 phase만 읽고 해당 phase의 `goal`, `task set / dependency closure`, `validation focus`, `exit criteria`, `carry-over policy`를 기준으로 구현하세요.
각 phase 구현 직후에는 같은 phase 범위의 `implementation-review` gate를 즉시 닫아야 하며, gate가 열려 있으면 다음 phase로 진행하지 마세요.

**Per-phase review-fix gate (must finish before Step 5)**:
- `scope`: `per-phase`
- `max_rounds_per_phase`: 3
- `timing`: 각 phase `implementation` 직후 즉시 실행하는 completion gate
- `Phase Source`: `_sdd/implementation/2026-04-10_implementation_plan_payment_system.md`
- `phase exit criteria`:
  - Phase 1: 결제 도메인 모델과 Stripe client abstraction이 테스트 통과 상태로 고정된다.
  - Phase 2: 결제 생성/승인/실패 흐름과 웹훅 검증이 통과한다.
  - Phase 3: 환불/운영 보정 흐름과 observability가 통합 검증된다.
- `carry-over policy`:
  - Default: `None`
  - `critical/high/medium` 이슈는 phase exit를 막는다.
  - 예외 carry-over는 plan에 명시된 항목만 허용하고, 로그에 근거와 후속 phase absorb point를 남긴다.
- `agent_mapping`:
  - `review = implementation-review`
  - `fix = implementation`
  - `re-review = implementation-review`
- `execution_sequence_per_phase`: `implementation -> implementation-review -> implementation (if needed) -> implementation-review -> phase validation`
- autopilot은 각 phase 구현 직후 현재 phase 범위로 `implementation-review` subagent를 즉시 호출한다.
- review 입력에는 최소한 `_sdd/implementation/2026-04-10_implementation_plan_payment_system.md`, `_sdd/drafts/2026-04-10_feature_draft_payment_system.md`, 현재 phase의 task/finding 목록, 현재 phase의 실제 변경 파일, focused test 결과를 포함한다.
- `review invocation prompt contract`:
  - "현재 phase 범위만 검토하세요. 응답은 findings first여야 하며, 각 finding은 severity, 파일/라인, 관련 phase task 또는 temporary spec linkage, 근거, 권장 수정 방향을 포함해야 합니다. unrelated dirty change는 회귀 위험이 아니면 finding으로 확장하지 마세요."
- `fix invocation prompt contract`:
  - "직전 `implementation-review` finding 중 현재 phase 범위의 `critical/high/medium`만 닫으세요. unrelated dirty changes를 되돌리지 말고, 수정 후 focused tests와 repo gate 준비 상태를 유지하세요."
- `re-review invocation prompt contract`:
  - "직전 review finding이 실제로 해소되었는지 먼저 검증하고, 같은 phase 범위에서 새 `critical/high/medium`이 남는지만 다시 보고하세요. findings first 형식을 유지하세요."
- `implementation-review` 결과에 `critical/high/medium`이 하나라도 있으면 autopilot은 그 finding만 입력으로 묶어 같은 phase 범위의 `implementation` subagent를 다시 호출한다.
- fix 후 autopilot은 같은 phase scope로 `implementation-review` subagent를 재호출한다.
- `final integration review`:
  - 마지막 phase 이후 `implementation-review`를 1회 더 실행해 cross-phase regressions를 점검한다.
- `final integration review prompt contract`:
  - "phase 경계를 넘는 회귀와 남은 cross-phase gap을 검토하세요. 응답은 findings first 형식이며, overall integration readiness와 spec sync readiness를 함께 평가해야 합니다."
- 현재 phase gate와 마지막 `final integration review`, required inline test가 모두 닫힌 뒤에만 Step 5로 진행한다.

### Step 5: spec-update-done
**Claude subagent_type**: `spec-update-done`
**입력 파일**:
- `_sdd/spec/main.md`
- `_sdd/implementation/2026-04-10_implementation_plan_payment_system.md`
- `_sdd/pipeline/report_payment_system_<timestamp>.md`
- 구현된 코드 파일
**출력 파일**: `_sdd/spec/main.md`

**프롬프트**:
모든 phase gate와 final integration review를 통과한 뒤, 구현되어 검증된 결제 시스템 정보를 global spec에 동기화하세요.
temporary phase execution detail은 제외하고 persistent contract와 운영 기준만 반영하세요.

**Precondition**:
모든 phase의 immediate review-fix gate와 phase validation, 마지막 `final integration review`, required inline test가 모두 닫힌 뒤에만 실행한다.

## Review-Fix Loop

- 이 오케스트레이터의 authoritative 순서와 프롬프트 계약은 Step 4의 `Per-phase review-fix gate`에 인라인으로 고정한다.
- 별도 후처리 loop는 없고, 각 phase gate와 마지막 `final integration review`가 닫히기 전에는 `spec-update-done`으로 진행할 수 없다.

## Test Strategy

- `mode`: `inline`
- `commands`: phase별 서비스/통합 테스트 + 마지막 전체 흐름 검증
- `rationale`: phase별 exit criteria를 빠르게 닫고 마지막 cross-phase 회귀까지 확인해야 하므로, 각 phase 테스트와 최종 통합 검증을 함께 묶은 인라인 전략을 사용한다.
- `reporting`: phase별 결과와 final integration review 결과를 `_sdd/pipeline/report_<topic>_<timestamp>.md`에 남긴다.

## Error Handling

- `retries`: feature-draft/spec-update-*는 1회, implementation-plan은 1회, 각 phase review-fix gate는 phase당 최대 3회
- `critical_steps`: Step 4 per-phase review-fix gate, final integration review, inline integration test
- `non_critical_steps`: spec wording polish, report formatting
- `failure_policy`: 특정 phase gate를 닫지 못하면 다음 phase와 Step 5를 중단하고, 실패한 phase와 잔여 이슈를 로그/보고서에 남긴다
```
