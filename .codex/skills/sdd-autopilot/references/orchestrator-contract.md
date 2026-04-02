# Orchestrator Contract

`sdd-autopilot`이 생성/실행하는 오케스트레이터와 로그의 최소 계약이다.
상세 철학/스킬 카탈로그는 `sdd-reasoning-reference.md`, 품질 감은 `examples/sample-orchestrator.md`를 따른다.

## 1. Required Orchestrator Sections

오케스트레이터는 아래 섹션을 이 순서대로 포함해야 한다.

1. 메타데이터: 기능명, 생성일, 생성자, 필요 시 규모
2. 기능 설명: 사용자 요청 원문 + 구체화된 요구사항 + 제약 조건
3. Acceptance Criteria: 기능 수준 검증 기준
4. Reasoning Trace: 3-6개 bullet
5. Pipeline Steps
6. Review-Fix Loop
7. Test Strategy
8. Error Handling

## 2. Step Contract

각 custom-agent step은 아래 4개 필드를 반드시 가진다.

- `에이전트`
- `입력 파일`
- `출력 파일`
- `프롬프트`

허용 agent_type:

- `feature_draft`
- `spec_update_todo`
- `implementation_plan`
- `implementation`
- `implementation_review`
- `spec_update_done`
- `spec_review`
- `ralph_loop_init`

## 3. Control Phases

아래는 오케스트레이터에 이름은 나타날 수 있지만, 새 custom agent를 뜻하지 않는다.

- `review-fix loop`
- `inline test`
- `ralph-loop`의 실제 실행 단계

규칙:

- review가 포함되면 `review -> fix -> re-review`를 명시해야 한다.
- 테스트는 항상 `Execute -> Verify` 구조를 가진다.
- `ralph_loop_init`은 설정 생성까지만이 아니라 실제 실행 검증까지 포함해야 한다.

## 4. Acceptance Criteria Contract

오케스트레이터는 "구체화된 요구사항"에서 도출한 기능 수준 AC를 포함해야 한다.

생성 규칙:

- 각 요구사항을 검증 가능한 조건 1개로 변환한다
- 프로세스 완료 여부(에이전트 실행됨)가 아니라 기능 동작 여부(결과가 맞음)를 검증한다
- 테스트로 확인 가능한 항목은 테스트 명령과 연결한다

autopilot은 오케스트레이터 AC를:

- review-fix loop의 리뷰 기준으로 사용한다
- 테스트 검증의 통과 기준으로 사용한다
- 최종 보고서에서 충족 여부를 체크한다

## 5. Reasoning Trace

Reasoning Trace는 최소한 아래를 설명해야 한다.

- 왜 이 파이프라인 규모로 판단했는가
- 왜 해당 skill 조합을 선택했는가
- 왜 테스트 전략이 inline 또는 `ralph_loop_init`인가
- 어떤 SDD 원칙이 강하게 작동했는가

## 6. Review-Fix Contract

반드시 포함할 필드:

- 최대 반복 횟수
- 종료 조건 (`critical = 0 AND high = 0 AND medium = 0`)
- 수정 대상 (`critical/high/medium`)
- MAX 도달 시 분기: critical/high 잔존 → 중단, medium만 잔존 → 로그 기록 후 계속 진행

리뷰 프롬프트는 심각도 분류를 강제해야 한다.
fix 프롬프트는 critical/high/medium 이슈를 수정 대상으로 한다.

## 7. Test Strategy Contract

### E2E 테스트 포함 조건

오케스트레이터에 E2E 테스트 단계를 포함하려면 아래 4가지를 모두 충족해야 한다:

1. **리소스 준비됨**: 입력 데이터, API key, 환경변수, GPU 등이 `_sdd/env.md` 또는 프로젝트 설정에서 확인됨
2. **E2E가 필요함**: 단위 테스트만으로 기능 검증 불충분
3. **실행 명령 명확**: `_sdd/env.md` 또는 스펙에서 테스트 명령 도출 가능
4. **자율 실행 가능**: 사용자 인터랙션 불필요

미충족 항목이 있으면 테스트 단계를 넣되 "실행 불가 — 사유: X, 수동 검증 방법: Y"로 보고서에 명시한다.

### 반드시 포함할 필드

- 방식 (`inline` 또는 `ralph_loop_init`)
- 실행 명령 (테스트, 학습, 빌드 등)
- 선택 근거 (프로세스 특성 기반)
- 사용자 보고 형식 (통과/실패 건수, 실패 원인, 수동 확인 필요 항목)

> 자율 판단 노트: 방식 선택은 프로세스 특성(실행 시간, 반복 검증 필요성, 환경 격리 필요성)에 기반한다. 인라인은 수분 이내 완료되는 경우, ralph_loop_init은 장시간/반복 사이클이 필요한 경우 (타임아웃 제약 없음, background 실행).

필수 규칙:

- 테스트/검증 단계는 **건너뛸 수 없다**. 실행 불가 시 사유와 수동 검증 방법을 보고서에 명시해야 한다.
- inline 테스트: 실제 테스트 실행 여부와 통과 결과를 검증한다.
- `ralph_loop_init`: setup 검증과 run 결과 검증을 모두 가진다.
- 테스트 결과는 사용자에게 명시적으로 보고한다 (AC6).

## 8. Error Handling Contract

반드시 포함할 필드:

- 재시도 횟수
- 핵심 단계
- 비핵심 단계

핵심 단계 실패 시 파이프라인은 중단한다.
비핵심 단계 실패는 로그 기록 후 건너뛸 수 있다.

## 9. Pipeline Log Contract

로그 파일은 아래 4개 블록만 있으면 충분하다.

### 8.1 Meta

- request
- orchestrator
- started
- pipeline

### 8.2 Status Table

필수 컬럼:

- Step
- Agent
- Status
- Output

허용 상태:

- `pending`
- `in_progress`
- `completed`
- `failed`
- `skipped`

### 8.3 Execution Log Entries

각 단계 완료 시 최소 필드:

- 시간
- 출력
- 핵심 결정사항
- 이슈

추가 엔트리:

- `review-fix -- Round N/3`
- `ERROR: <agent-name> -- retry N/3`

### 8.4 Final Summary

최종 요약에는 아래만 있으면 된다.

- 완료 시간
- 총 소요 시간
- 실행 결과
- 생성/수정 파일 수
- Review 횟수
- 테스트 결과
- 스펙 동기화 여부
- 잔여 이슈

## 10. State Handoff

상태 전달은 파일 경로만 사용한다.

대표 흐름:

- `_sdd/drafts/feature_draft_<topic>.md` -> `implementation` 또는 `implementation_plan`
- `_sdd/implementation/implementation_plan.md` -> `implementation`
- `.codex/skills/orchestrator_<topic>/SKILL.md` -> autopilot 실행 입력
- `_sdd/pipeline/log_<topic>_<timestamp>.md` -> autopilot 관리 로그
