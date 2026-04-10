# 토론 메모: sdd-autopilot planning 스킬 오케스트레이션 정리

**날짜**: 2026-04-10
**상태**: discussion only, patch 미적용
**관련 문서**:
- `.claude/skills/sdd-autopilot/SKILL.md`
- `.claude/skills/sdd-autopilot/references/sdd-reasoning-reference.md`
- `.claude/skills/sdd-autopilot/references/orchestrator-contract.md`
- `.codex/skills/feature-draft/SKILL.md`
- `.codex/skills/implementation-plan/SKILL.md`
- `.codex/skills/spec-update-todo/SKILL.md`

## 배경

`sdd-autopilot`가 오케스트레이터를 만들 때 `feature-draft`를 건너뛰고 `implementation-plan`으로 대체하는 경우가 반복적으로 관찰되었다.

이번 논의의 핵심은 planning 계열 스킬의 실제 역할을 문서에 더 정확하게 반영하여, 오케스트레이터 reasoning이 잘못된 대체 관계를 만들지 않도록 정리하는 것이다.

## 문제 정의

현재 문서 표현만 보면 `feature-draft`, `implementation-plan`, `spec-update-todo`가 서로 병렬적인 선택지처럼 읽힐 여지가 있다.

하지만 실제 의도는 아래와 같다.

1. `feature-draft`는 논의 내용이나 컨텍스트를 바탕으로 구현 목표/명세와 구현 계획을 함께 작성하는 기본 planning entry다.
2. `implementation-plan`은 특히 구현량이 많고 복잡한 경우, 이미 정리된 delta를 phase/task 단위로 더 세분화하는 확장 단계다.
3. `spec-update-todo`는 복잡한 대규모 구현에서 구현 전에 global spec planned state를 미리 정렬해 두는 것이 유리할 때 사용하는 조건부 단계다.

즉, 일반적으로는 `implementation-plan`이 `feature-draft`의 대체재가 아니라 후속 확장 단계로 이해되어야 한다.

## 현재 문서에서의 원인 추정

### 1. reasoning reference의 오케스트레이션 설명이 관계 중심이 아니라 역할 나열 중심이다

- `feature-draft`, `spec-update-todo`, `implementation-plan`이 각각 무엇을 하는지만 적혀 있고,
- 어떤 조건에서 선행/후행 관계를 가져야 하는지가 충분히 드러나지 않는다.

이 때문에 `implementation-plan`이 독립 planning 진입점처럼 오해될 수 있다.

### 2. autopilot 본문의 판단 표가 대체 관계처럼 읽힌다

`직접 구현 / feature-draft / implementation-plan`을 같은 층위의 선택지로 적어 두어, 모델이 셋 중 하나를 고르는 방식으로 추론할 가능성이 있다.

### 3. orchestrator contract가 implementation-plan의 일반적 선행조건을 명시하지 않는다

`implementation-plan` 자체 산출물 계약은 있지만, 보통 어떤 입력 상태에서 호출해야 하는지에 대한 가이드가 약하다.

## 정리된 의도

### 기본 규칙

1. 비자명한 변경에서 planning이 필요하면 기본 진입점은 `feature-draft`다.
2. 소규모 또는 중간 규모 변경은 `feature-draft` Part 2만으로도 `implementation`에 바로 들어갈 수 있다.
3. 대규모 또는 복잡한 변경은 `feature-draft` 이후 필요 시 `spec-update-todo`, 그리고 `implementation-plan`으로 이어진다.
4. `spec-update-todo`는 항상 필수는 아니지만, 구현 전에 planned persistent global information을 정렬하는 편이 유리한 경우 붙는다.
5. `implementation-plan` standalone 사용은 예외적으로만 허용한다. 예를 들면, 이미 동등한 temporary spec 또는 충분한 feature draft 산출물이 존재하는 경우다.

### 권장 오케스트레이션 패턴

#### 단순/중간 변경

`feature-draft -> implementation -> implementation-review -> spec-update-done`

조건:
- `feature-draft` Part 2가 충분히 구체적임
- task 수가 과도하지 않음
- phase 전략이나 dependency가 이미 명확함

#### 복잡/대규모 변경

`feature-draft -> (optional) spec-update-todo -> implementation-plan -> implementation -> implementation-review -> spec-update-done`

조건:
- 구현 범위가 큼
- phase 분해가 중요함
- unresolved dependency가 많음
- 구현 전에 global spec planned alignment가 작업 효율을 높임

## 제안 패치 범위

### 1. `references/sdd-reasoning-reference.md`

- `오케스트레이션 대상 스킬` 섹션을 역할 설명만이 아니라 선후관계와 사용 조건 중심으로 재서술
- `implementation-plan`은 기본적으로 `feature-draft` 이후의 확장 단계라는 점 명시
- `spec-update-todo`는 복잡한 planned global alignment가 필요한 경우의 조건부 단계라고 명시
- dependency graph 또는 보조 설명에 “small/medium direct path”와 “large/complex expanded path”를 함께 표기

### 2. `sdd-autopilot/SKILL.md`

- Step 4의 `계획 깊이` 항목을 현재의 병렬 선택지 표현에서 관계 중심 표현으로 수정
- 예:
  - trivial: 직접 구현 가능
  - non-trivial: `feature-draft` 선행
  - large/complex: `feature-draft` 후 필요 시 `spec-update-todo` + `implementation-plan`

### 3. `references/orchestrator-contract.md`

- `implementation-plan`의 일반적인 precondition을 보강
- 일반적으로 `feature-draft` 또는 동등한 temporary spec 산출물이 선행되어야 함을 명시
- `spec-update-todo`의 사용 조건을 “global spec planned alignment가 구현 효율과 일관성에 유의미한 경우”로 보강

### 4. 필요 시 sample orchestrator 보강

- 중간 규모 예시는 `feature-draft -> implementation` 경로 유지
- 대규모 예시를 추가한다면 `feature-draft -> spec-update-todo -> implementation-plan` 경로를 보여 주는 것이 바람직함

## 기대 효과

1. `implementation-plan`의 오남용 감소
2. `feature-draft` 누락으로 인한 temporary spec 부재 문제 감소
3. 복잡한 구현에서 `spec-update-todo` 사용 타이밍 명확화
4. autopilot reasoning이 “대체 선택”보다 “단계적 확장”에 가깝게 수렴

## 메모

이번 정리는 아직 discussion 단계다. 실제 패치를 진행할 때는 `.claude/skills/sdd-autopilot/` 문서와 필요 시 `.codex/skills/sdd-autopilot/` mirror도 함께 확인해야 한다.
