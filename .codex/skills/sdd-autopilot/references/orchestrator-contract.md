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

## 2. Step Contract

각 custom-agent step은 아래 4개 필드를 반드시 가진다.

- `Codex agent_type`
- `입력 파일`
- `출력 파일`
- `프롬프트`

허용 `agent_type`:

- `feature_draft`
- `spec_update_todo`
- `implementation_plan`
- `implementation`
- `implementation_review`
- `spec_update_done`
- `spec_review`
- `ralph_loop_init`

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

- 최대 반복 횟수
- 종료 조건 (`critical = 0 AND high = 0 AND medium = 0`)
- 수정 대상 (`critical/high/medium/low`)
- MAX 도달 시 분기: critical/high 잔존 -> 중단, medium만 잔존 -> 로그 기록 후 계속 진행

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

### spec_update_todo
- global spec 업데이트 완료
- planned persistent information만 반영됨
- temporary execution detail이 global spec 본문으로 누수되지 않음

### spec_update_done
- global spec 업데이트 완료
- implemented + verified information만 반영됨
- 미구현/미검증 delta는 deferred로 남음

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
