# Sample Orchestrator

이 파일은 autopilot이 생성하는 오케스트레이터의 품질 기준 예시다.

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

- non-trivial change라 planning entry는 `feature_draft`로 시작한다.
- feature draft Part 2가 task/dependency/validation을 충분히 제공하므로 `implementation_plan`은 생략한다.
- single-phase medium path라 `Review-Fix Loop.scope`는 `global`로 유지한다.
- 테스트는 짧은 API/서비스 검증 중심이라 인라인 전략을 선택한다.

## Pipeline Steps

### Step 1: feature_draft
**Codex agent_type**: `feature_draft`
**입력 파일**: `_sdd/spec/main.md`
**출력 파일**: `_sdd/drafts/2026-04-10_feature_draft_jwt_auth.md`

**프롬프트**:
JWT 기반 인증 시스템에 대한 feature draft를 작성하세요.
Part 1에는 temporary spec 7섹션을 포함하고, `Contract/Invariant Delta`와 `Validation Plan`을 ID로 연결하세요.
Part 2에는 implementation이 직접 읽을 수 있는 Target Files, dependency, validation detail을 포함하세요.

### Step 2: implementation
**Codex agent_type**: `implementation`
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

### Step 3: spec_update_done
**Codex agent_type**: `spec_update_done`
**입력 파일**:
- `_sdd/spec/main.md`
- `_sdd/drafts/2026-04-10_feature_draft_jwt_auth.md`
- 구현된 코드 파일
**출력 파일**: `_sdd/spec/main.md`

**프롬프트**:
JWT 인증 시스템 구현 완료 기준으로 global spec을 실제 코드와 동기화하세요.
temporary spec의 실행 정보는 버리고, 구현되어 검증된 persistent repo-wide information만 global spec에 반영하세요.

## Review-Fix Loop

- `scope`: `global`
- `max_rounds`: 3
- `exit_condition`: `critical = 0 AND high = 0 AND medium = 0`
- `fix_targets`: `critical/high/medium/low`
- `agent_mapping`: `review = implementation_review`, `fix = implementation`, `re-review = implementation_review`

## Test Strategy

- `mode`: `inline`
- `commands`: 관련 서비스 테스트 + 인증 라우트 smoke 검증
- `reporting`: 통과/실패 건수와 잔여 수동 확인 항목을 `_sdd/pipeline/report_<topic>_<timestamp>.md`에 기록
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

- non-trivial planning entry는 `feature_draft`로 고정한다.
- planned persistent global alignment가 있으므로 `spec_update_todo`를 조건부로 추가한다.
- 구현 범위가 크고 dependency chain이 깊어서 `implementation_plan`으로 phase/task breakdown을 확장한다.
- multi-phase plan이므로 `Review-Fix Loop.scope = per-phase`를 사용하고 마지막에 `final integration review`를 추가한다.

## Pipeline Steps

### Step 1: feature_draft
**Codex agent_type**: `feature_draft`
**입력 파일**:
- `_sdd/spec/main.md`
- `_sdd/spec/components.md`
**출력 파일**: `_sdd/drafts/2026-04-10_feature_draft_payment_system.md`

### Step 2: spec_update_todo
**Codex agent_type**: `spec_update_todo`
**입력 파일**:
- `_sdd/spec/main.md`
- `_sdd/drafts/2026-04-10_feature_draft_payment_system.md`
**출력 파일**: `_sdd/spec/main.md`

### Step 3: implementation_plan
**Codex agent_type**: `implementation_plan`
**입력 파일**:
- `_sdd/drafts/2026-04-10_feature_draft_payment_system.md`
- `_sdd/spec/main.md`
**출력 파일**: `_sdd/implementation/2026-04-10_implementation_plan_payment_system.md`

### Step 4: implementation
**Codex agent_type**: `implementation`
**입력 파일**:
- `_sdd/implementation/2026-04-10_implementation_plan_payment_system.md`
- `_sdd/spec/main.md`
**출력 파일**:
- 결제 서비스/웹훅/환불 관련 코드 및 테스트 파일

### Step 5: spec_update_done
**Codex agent_type**: `spec_update_done`
**입력 파일**:
- `_sdd/spec/main.md`
- `_sdd/implementation/2026-04-10_implementation_plan_payment_system.md`
- `_sdd/pipeline/report_payment_system_<timestamp>.md`
- 구현된 코드 파일
**출력 파일**: `_sdd/spec/main.md`

## Review-Fix Loop

- `scope`: `per-phase`
- `max_rounds_per_phase`: 3
- `phase boundary source`: `_sdd/implementation/2026-04-10_implementation_plan_payment_system.md`
- `phase exit criteria`:
  - Phase 1: 결제 도메인 모델과 Stripe client abstraction이 테스트 통과 상태로 고정된다.
  - Phase 2: 결제 생성/승인/실패 흐름과 웹훅 검증이 통과한다.
  - Phase 3: 환불/운영 보정 흐름과 observability가 통합 검증된다.
- `carry-over policy`:
  - Default: `None`
  - `critical/high/medium` 이슈는 phase exit를 막는다.
  - 예외 carry-over는 plan에 명시된 항목만 허용하고, 로그에 근거와 후속 phase absorb point를 남긴다.
- `agent_mapping`:
  - `review = implementation_review`
  - `fix = implementation`
  - `re-review = implementation_review`
- `final integration review`:
  - 마지막 phase 이후 `implementation_review`를 1회 더 실행해 cross-phase regressions를 점검한다.

## Test Strategy

- `mode`: `inline`
- `commands`: phase별 서비스/통합 테스트 + 마지막 전체 흐름 검증
- `reporting`: phase별 결과와 final integration review 결과를 `_sdd/pipeline/report_<topic>_<timestamp>.md`에 남긴다.
```
