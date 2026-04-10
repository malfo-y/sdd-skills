# 토론 메모: sdd-autopilot 대규모 구현의 phase별 review-fix 루프

**날짜**: 2026-04-10
**상태**: discussion only, patch 미적용
**참여 방식**: 구조화된 토론 (discussion skill)
**결정 방향**: 최소 수정
**관련 문서**:
- `.claude/skills/sdd-autopilot/SKILL.md`
- `.claude/skills/sdd-autopilot/references/orchestrator-contract.md`
- `.claude/skills/sdd-autopilot/examples/sample-orchestrator.md`
- `.codex/skills/implementation-plan/SKILL.md`

## 핵심 논점

1. 대규모 구현에서 `implementation-plan`의 phase 구조를 실제 실행 루프에 반영해야 하는가
2. 현재 `sdd-autopilot`의 review-fix loop가 전체 구현 후 1회 루프에 치우쳐 있는가
3. 구조를 크게 바꾸지 않고도 phase별 검증 게이트를 도입할 수 있는가

## 현재 상태 요약

- 현재 autopilot 실행 규칙은 `Pipeline Steps`를 순서대로 수행하고, `Review-Fix Loop` section을 오케스트레이터 선언대로 집행한다.
- 하지만 contract와 sample orchestrator 모두 review-fix를 파이프라인 전역 후처리에 가깝게 표현하고 있다.
- `implementation-plan`은 phase 중심 계획을 만들 수 있지만, autopilot 실행 계약은 그 phase를 review gate로 소비하는 규칙이 약하다.

## 결정 사항

| # | 결정 | 근거 |
|---|------|------|
| 1 | 대규모/복잡 구현은 phase별 `implementation -> review -> fix -> phase validation` 루프가 기본이 되어야 한다 | phase 계획을 실제 실행 제어에 반영하지 않으면 `implementation-plan`의 가치가 줄고, 결함이 뒤 phase까지 전파되기 쉽다 |
| 2 | 첫 수정은 구조 개편보다 최소 수정으로 간다 | 현재 flat `Pipeline Steps`와 실행기 구조를 크게 뒤흔들지 않고도 phase gate semantics를 추가할 수 있다 |
| 3 | small/medium 경로는 기존 단일 review-fix loop를 유지할 수 있다 | 모든 작업에 phase gate를 강제할 필요는 없고, large/complex에서만 비용 대비 효과가 크다 |
| 4 | `per-phase` 경로에서도 마지막 `final integration review`를 항상 강제한다 | phase별 루프가 국소 리스크를 줄여도 cross-phase 통합 이슈는 마지막에 별도로 확인해야 한다 |
| 5 | phase exit criteria에서 `medium`은 기본적으로 다음 phase 진행을 막되, 근거 있는 예외만 carry-over 허용한다 | 안전성을 기본값으로 두면서도 phase 성격상 다음 단계에서 함께 정리하는 편이 더 합리적인 경우를 허용할 수 있다 |
| 6 | `implementation-plan` 문서에는 phase gate 실행용 필드를 명시적으로 추가한다 | autopilot이 phase별 실행과 검증을 안정적으로 읽고 집행하려면 phase goal / exit criteria / validation focus가 문서에 드러나야 한다 |

## 제안 설계

### 목표 동작

large/complex 구현에서는 아래 흐름을 기본으로 한다.

`feature-draft -> (optional) spec-update-todo -> implementation-plan -> phase 1 implementation -> phase 1 review/fix -> phase 2 implementation -> phase 2 review/fix -> ... -> final integration review -> spec-update-done`

### 최소 수정 원칙

1. 오케스트레이터의 flat step 구조는 유지한다.
2. 대신 large/complex 계획일 때는 step 메타데이터에 `phase` 개념과 `phase exit criteria`를 추가한다.
3. `Review-Fix Loop` section에 `scope: global | per-phase`를 도입한다.
4. `scope = per-phase`이면 autopilot은 같은 phase의 구현 step 완료 직후 review-fix를 닫고 다음 phase로 넘어간다.

## 구체 패치 아이디어

### 1. `references/orchestrator-contract.md`

`Review-Fix Contract`에 아래 필드를 추가한다.

- `scope`: `global` 또는 `per-phase`
- `phase boundary source`: `implementation-plan` 또는 오케스트레이터 step 정의
- `phase exit criteria`: 다음 phase로 넘어가기 위한 기준
- `carry-over policy`: medium/low 이슈를 다음 phase로 넘길 수 있는지 여부

추가 규칙:

- large/complex 경로에서 `implementation-plan`이 multi-phase면 기본값은 `scope = per-phase`
- `scope = per-phase`일 때는 현재 phase의 exit criteria 충족 전 다음 phase 진입 금지

### 2. `sdd-autopilot/SKILL.md`

Step 7 실행 규칙을 보강한다.

- `Review-Fix Loop.scope = per-phase`면 implementation phase 단위로 `Execute -> Collect -> Review/Fix -> Validate -> Record`를 반복
- phase 종료 시점마다 로그에 phase status와 잔여 이슈를 기록
- 전체 구현 종료 후에는 `final integration review`를 반드시 1회 수행

### 3. sample orchestrator 보강

대규모 예시를 추가하거나, 기존 예시에 아래와 같은 패턴을 보인다.

- Step 3: implementation (Phase 1)
- Step 4: review-fix loop (Phase 1)
- Step 5: implementation (Phase 2)
- Step 6: review-fix loop (Phase 2)

중간 규모 예시는 기존처럼 전체 구현 후 단일 review-fix loop를 유지한다.

### 4. `implementation-plan` 연동

phase별 실행을 제대로 하려면 implementation-plan 쪽에서도 아래 정보가 autopilot이 읽기 좋게 드러나야 한다.

- phase goal
- phase별 task 집합
- phase별 dependency closure
- phase별 validation focus
- phase별 exit criteria
- phase별 carry-over policy
- 다음 phase 진입 전 반드시 만족해야 할 조건

## 기대 효과

1. 큰 구현에서 결함 확산을 조기에 차단
2. review 결과가 현재 phase 범위에 집중되어 수정 효율 상승
3. `implementation-plan`의 phase 구조가 실제 execution control로 연결
4. small/medium 경로는 유지하여 복잡도 증가를 제한

## 남은 질문

없음. 핵심 설계 질문 3개는 아래와 같이 정리되었다.

1. `per-phase` 경로에서도 마지막 `final integration review`는 항상 강제한다.
2. `medium` 이슈는 기본적으로 phase exit를 막되, 명시적 carry-over 조건이 있을 때만 예외 허용한다.
3. `implementation-plan`에는 phase gate 실행용 필드를 명시적으로 추가한다.

## 실행 항목

| # | 항목 | 우선순위 | 설명 |
|---|------|---------|------|
| 1 | orchestrator contract 보강안 작성 | High | `Review-Fix Contract`에 per-phase semantics 추가 |
| 2 | autopilot 실행 규칙 보강안 작성 | High | Step 7에서 phase gate 집행 로직 명문화 |
| 3 | sample orchestrator 대규모 예시 추가 | Medium | phase별 implementation/review-fix 패턴 예시화 |
| 4 | implementation-plan 포맷 보강안 작성 | High | phase goal / exit criteria / validation focus / carry-over policy를 문서 구조에 반영 |
