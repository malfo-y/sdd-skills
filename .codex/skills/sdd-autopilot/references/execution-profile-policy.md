# Execution Profile Policy

`sdd-autopilot`이 `spawn_agent(...)`를 호출할 때 적용하는 기본 `model` / `reasoning_effort` 정책이다.

이 문서는 오케스트레이터 계약을 대체하지 않는다. 오케스트레이터는 여전히 step의 목적, 입력/출력, 프롬프트, exit criteria를 중심으로 정의하고, 실행기는 이 문서의 프로파일 규칙을 사용해 각 step의 호출 강도를 정한다.

## 1. Policy Goals

- 기본값은 비용 최적화보다 품질 안정성을 우선한다.
- 단, small/simple 작업은 조건부 감등을 허용한다.
- 설계 오류가 후속 단계를 오염시키는 step은 보수적으로 유지한다.
- phase boundary와 final integration review는 국소 최적화보다 전체 정합성을 우선한다.
- 이미 생성한 agent의 `model` / `reasoning_effort`는 변경하지 않는다. 변경이 필요하면 새 agent를 `spawn_agent(...)` 한다.

## 2. Default Step Profiles

| 용도 | agent_type | 기본 모델 | 기본 effort |
|---|---|---|---|
| 구조 탐색 빠른 스캔 | `explorer` | `gpt-5.4-mini` | `low` |
| 도메인/리스크 탐색 | `explorer` | `gpt-5.4-mini` | `medium` |
| feature draft 생성 | `feature_draft` | `gpt-5.4` | `xhigh` |
| planned spec 반영 | `spec_update_todo` | `gpt-5.4` | `medium` |
| phase/task 분해 계획 | `implementation_plan` | `gpt-5.4` | `xhigh` |
| 실제 구현 기본 | `implementation` | `gpt-5.4` | `high` |
| 복잡한 fix 재시도 | `implementation` | `gpt-5.4` | `high` |
| 구현 리뷰 | `implementation_review` | `gpt-5.4` | `high` |
| final integration review | `implementation_review` | `gpt-5.4` | `xhigh` |
| done spec sync | `spec_update_done` | `gpt-5.4` | `medium` |
| spec 감사성 검토 | `spec_review` | `gpt-5.4` | `high` |
| 장기 검증 루프 초기화 | `ralph_loop_init` | `gpt-5.4` | `xhigh` |

## 3. Selection Principles

### 3.1 Quality-first baseline

- `feature_draft`, `implementation_plan`, `implementation`, `implementation_review`는 autopilot의 핵심 실패 전파 경로다.
- 이 네 단계는 특별한 감등 근거가 없으면 기본 프로파일을 유지한다.
- `final integration review`는 기본적으로 가장 엄격한 검증 단계로 취급한다.

### 3.2 Cost optimization is secondary

- 병렬 탐색이나 빠른 사실 수집처럼 실패 비용이 낮은 단계에서만 `mini` 또는 낮은 effort를 우선 고려한다.
- 구현, 리뷰, 설계 단계는 토큰 절감보다 재작업 비용 감소를 우선한다.

## 4. Downgrade Rules

아래 조건이 명확할 때만 감등한다. 감등 시에는 로그에 근거를 남긴다.

### 4.1 `feature_draft`

기본: `gpt-5.4 / xhigh`

감등 가능:
- single-file 또는 문서 위주 변경
- invariant 변화가 거의 없음
- 기존 패턴 복제에 가깝고 신규 추상화가 없음
- single-phase medium 이하이며 temporary spec이 compact linkage로 충분함

권장 감등:
- `gpt-5.4 / high`

### 4.2 `implementation_plan`

기본: `gpt-5.4 / xhigh`

감등 가능:
- multi-phase 분해가 불필요함
- `feature_draft` Part 2만으로 task/dependency/validation linkage가 충분함
- 재개용 보강 plan이 아니라 단순 정리 수준의 계획만 필요함

권장 감등:
- `gpt-5.4 / high`

### 4.3 `implementation`

기본: `gpt-5.4 / high`

감등 가능:
- 수정 범위가 매우 국소적임
- 기존 코드 패턴과 테스트 패턴이 명확함
- 새 경계/추상화/상태 모델을 만들지 않음
- review-fix loop 이전의 초기 구현이고 실패 비용이 낮음

권장 감등:
- `gpt-5.4 / medium`

### 4.4 `implementation_review`

기본: `gpt-5.4 / high`

감등 가능:
- phase gate가 아닌 경량 중간 점검
- 변경 범위가 작고 영향 범위가 제한적임

권장 감등:
- `gpt-5.4 / medium`

### 4.5 `final integration review`

기본: `gpt-5.4 / xhigh`

감등 가능:
- single-phase small direct path
- cross-boundary interaction이 사실상 없음
- 변경 범위가 명백히 local이며 회귀면이 좁음

권장 감등:
- `gpt-5.4 / high`

### 4.6 `ralph_loop_init`

기본: `gpt-5.4 / xhigh`

감등 가능:
- loop 골격 생성만 필요함
- 실패 분석이나 자동 remediation 설계까지 요구하지 않음
- 실행 환경이 단순하고 검증 축이 1개뿐임

권장 감등:
- `gpt-5.4 / high`

## 5. Escalation Rules

아래 조건이 있으면 기본값을 유지하거나, 감등을 취소하고 상위 프로파일로 되돌린다.

- cross-cutting 변경이다.
- 기존 spec가 얇고 ambiguity가 크다.
- 신규 invariant 또는 contract delta가 포함된다.
- multi-phase dependency chain이 깊다.
- review에서 `medium` 이상 이슈가 반복된다.
- 구현이 기존 패턴 복제가 아니라 새 추상화 설계를 요구한다.
- integration boundary가 핵심 리스크다.
- spec sync가 repo-wide guardrail 또는 key decision을 건드린다.

## 6. Review-Fix Escalation Policy

- 첫 구현은 해당 step의 기본 프로파일을 사용한다.
- review에서 `critical` / `high` / 반복 `medium` 이슈가 나오면 fix step은 감등 없이 `implementation = gpt-5.4 / high`를 유지한다.
- 동일 범주의 이슈가 두 번 이상 반복되면 기존 implementation agent를 재사용하지 않고 새 agent를 spawn한다.
- final integration review에서 이슈가 나오면 후속 fix는 local patch로 끝내지 말고 관련 phase boundary까지 다시 확인한다.

## 7. Spawn Policy

실행기는 아래 규칙으로 step 프로파일을 적용한다.

1. step 실행 우선순위는 `step-level Execution profile` -> `Execution Profiles` section 기본값 -> policy 기본값이다.
2. review-fix loop 우선순위는 `review_profile` / `fix_profile` / `final_integration_review_profile` -> `Execution Profiles` section 기본값 -> policy 기본값이다.
3. 실제 호출은 `spawn_agent(model=..., reasoning_effort=...)`로 명시한다.
4. 프로파일 변경이 필요하면 `send_input(...)`로 덮어쓰지 말고 새 agent를 spawn한다.
5. 병렬 `explorer` fan-out은 작은 모델을 우선하되, synthesis는 상위 프로파일에서 처리한다.
6. review-fix loop에서 severity가 누적되면 감등을 해제하고 기본 보수 프로파일로 복귀한다.
7. `final_integration_review_profile`은 실제 final integration review를 수행할 때만 소비한다. global path에서 final integration review를 별도 선언하지 않았다면 무시되는 값으로 두지 말고 아예 쓰지 않는다.

## 8. Suggested Profile Keys

```yaml
profiles:
  explore_fast:
    model: gpt-5.4-mini
    reasoning_effort: low
  explore_risk:
    model: gpt-5.4-mini
    reasoning_effort: medium
  draft_strict:
    model: gpt-5.4
    reasoning_effort: xhigh
  plan_strict:
    model: gpt-5.4
    reasoning_effort: xhigh
  impl_default:
    model: gpt-5.4
    reasoning_effort: high
  review_default:
    model: gpt-5.4
    reasoning_effort: high
  review_integration_strict:
    model: gpt-5.4
    reasoning_effort: xhigh
  spec_sync_default:
    model: gpt-5.4
    reasoning_effort: medium
  ralph_strict:
    model: gpt-5.4
    reasoning_effort: xhigh
```

## 9. Example Heuristics

### 9.1 Small direct path

- `explorer`: `gpt-5.4-mini / low`
- `implementation`: `gpt-5.4 / medium`
- `implementation_review`: `gpt-5.4 / medium`
- `final integration review`: `gpt-5.4 / high`

### 9.2 Single-phase medium path

- `feature_draft`: `gpt-5.4 / high` 또는 `xhigh`
- `implementation`: `gpt-5.4 / high`
- `implementation_review`: `gpt-5.4 / high`
- `spec_update_done`: `gpt-5.4 / medium`

### 9.3 Multi-phase large path

- `feature_draft`: `gpt-5.4 / xhigh`
- `implementation_plan`: `gpt-5.4 / xhigh`
- phase별 `implementation`: `gpt-5.4 / high`
- phase별 `implementation_review`: `gpt-5.4 / high`
- `final integration review`: `gpt-5.4 / xhigh`
- `ralph_loop_init`: `gpt-5.4 / xhigh`
