# Execution Profile Policy

`sdd-autopilot`의 기본 `model` / `reasoning_effort` 정책이다.
기본값은 고정하며, override는 사용자 요청이 있을 때만 오케스트레이터에 명시한다.

## Fixed Profiles

| 용도 | agent_type | model | effort |
|---|---|---|---|
| 구조 탐색 빠른 스캔 | `explorer` | `gpt-5.5` | `low` |
| 도메인/리스크 탐색 | `explorer` | `gpt-5.5` | `medium` |
| feature draft 생성 | `feature_draft` | `gpt-5.5` | `xhigh` |
| planned spec 반영 | `spec_update_todo` | `gpt-5.5` | `medium` |
| phase/task 분해 계획 | `implementation_plan` | `gpt-5.5` | `xhigh` |
| 실제 구현 | `implementation` | `gpt-5.5` | `high` |
| 구현 리뷰 | `implementation_review` | `gpt-5.5` | `high` |
| final integration review | `implementation_review` | `gpt-5.5` | `xhigh` |
| done spec sync | `spec_update_done` | `gpt-5.5` | `medium` |
| spec 감사성 검토 | `spec_review` | `gpt-5.5` | `high` |
| 장기 검증 루프 초기화 | `ralph_loop_init` | `gpt-5.5` | `xhigh` |

## Precedence

- step 실행: `step-level Execution profile` -> `Execution Profiles` section -> policy 기본값
- review-fix loop: `review_profile` / `fix_profile` / `final_integration_review_profile` -> `Execution Profiles` section -> policy 기본값

## Override Rules

- override는 사용자 요청이 있을 때만 사용한다.
- 기본값에서 벗어날 때만 오케스트레이터에 명시한다.
- `final_integration_review_profile`은 실제 final integration review가 있을 때만 유효하다.
- 프로파일 변경이 필요하면 기존 agent를 재사용하지 말고 새로 `spawn_agent(...)` 한다.
