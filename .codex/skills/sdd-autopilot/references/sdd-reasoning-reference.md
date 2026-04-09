# SDD Reasoning Reference

## Part 1: SDD 철학

### 1.1 핵심 원칙

1. **Spec is Source of Truth**: 코드는 결과물이고, global spec은 장기적 의도를 고정한다.
2. **Global spec과 temporary spec은 역할이 다르다**: global spec은 얇은 repo-wide 판단 기준이고, temporary spec은 실행 청사진이다.
3. **검증은 실행 surface에 더 가깝게 둔다**: feature-level contract와 validation은 temporary spec, code, review evidence에 가깝게 둔다.

운영 대원칙: **AI가 만든 spec도 사람 승인 없이는 확정하지 않는다.**

### 1.2 사람과 LLM이 spec에서 필요로 하는 것

- 사람은 high-level concept, scope, non-goals, guardrails, key decisions가 먼저 필요하다.
- LLM은 코드를 빠르게 탐색할 수 있으므로 code-obvious inventory보다 경계와 결정이 더 중요하다.
- 따라서 global spec은 두꺼운 구현 해설서가 아니라 얇은 decision memo여야 한다.
- 상세 implementation inventory와 feature-level execution detail은 코드, temporary spec, guide, supporting docs에 맡긴다.

### 1.3 핵심 용어

| 용어 | 의미 |
|------|------|
| **Global Spec** | 장기적 SoT. 문제 framing, scope/non-goals/guardrails, key decisions를 유지하는 문서 |
| **Temporary Spec** | 변경 하나를 실행하기 위한 청사진. delta, touchpoints, plan, validation을 담는 문서 |
| **Repo-wide Invariant** | 여러 feature에 공통으로 적용되고, 틀리면 repo-level 판단이 어긋나는 operating rule |
| **Guide** | 필요할 때 만드는 feature-level companion surface |
| **Supporting Reference** | README, 환경 문서, appendix, code map 같은 보조 정보 |

### 1.4 Global Spec Canonical Shape

global spec core는 아래 순서를 유지한다.

1. `배경 및 high-level concept`
2. `Scope / Non-goals / Guardrails`
3. `핵심 설계와 주요 결정`

선택 정보:

- supporting reference
- guide 링크
- appendix-level code map
- repo-wide invariant note

global spec 규칙:

- scope는 책임 범위와 out-of-scope를 함께 고정한다.
- repo-wide invariant가 필요하면 guardrails 또는 key decisions에 흡수한다.
- usage guide, expected result, feature-level contract/validation은 기본 global core가 아니다.
- architecture/component inventory를 본문 필수로 강제하지 않는다.

### 1.5 Temporary Spec Canonical Shape

temporary spec은 global spec의 축약 복사본이 아니다. 변경 작업을 위한 실행 청사진이다.

canonical 7섹션:

1. `Change Summary`
2. `Scope Delta`
3. `Contract/Invariant Delta`
4. `Touchpoints`
5. `Implementation Plan`
6. `Validation Plan`
7. `Risks / Open Questions`

핵심 규칙:

- `Contract/Invariant Delta`는 `C*`, `I*` ID를 사용한다.
- `Validation Plan`은 `V*` ID를 사용하고 delta ID를 `Targets`로 연결한다.
- 작은 변경이면 `C1/I1/V1` 수준의 compact linkage로 충분하다. traceability를 위해 ID는 유지하되 형식적 분해를 늘리지 않는다.
- `Touchpoints`는 전수형 파일 목록이 아니라 전략적 change hotspot이다.
- temporary spec의 실행 정보는 global spec에 그대로 병합하지 않는다.

### 1.6 spec-update-todo / done의 역할

- `spec-update-todo`: temporary spec이나 user input을 읽고, global spec에 남아야 할 planned persistent information만 올린다.
- `spec-update-done`: 실제 구현과 validation evidence를 읽고, global spec에 남아야 할 implemented persistent information만 올린다.

즉:

- temporary spec의 task breakdown, validation 실행 메모, transient risk log는 global spec 본문으로 가지 않는다.
- global spec으로 올라가는 것은 shared scope, guardrails, key decisions, repo-wide invariant note 같은 정보다.

### 1.7 파이프라인 구성 원칙

1. **Spec-optional**: global spec이 있으면 활용하고, 없으면 spec-less 모드로 진행한다. `spec-create`는 파이프라인 필수 선행이 아니라 사용자에게 추천하는 가이드 수준이다.
2. **Delta-first for non-trivial changes**: 추가적인 계획이 필요한 모든 변경은 temporary spec 또는 `feature-draft`를 선행.
3. **Review-fix 필수**: review만 하고 끝나지 않는다.
4. **Execute -> Verify**: 에이전트 호출 != 완료. evidence까지 확인해야 한다.
5. **파일 기반 handoff**: 상태 전달은 artifact 파일 경로 중심.
6. **Global spec 직접 수정 금지**: spec 변경은 `spec-update-todo` / `spec-update-done`에 위임.

---

## Part 2: 스킬 카탈로그

### 2.1 스킬 의존성 그래프

```text
(spec-create) -> feature-draft -> spec-update-todo -> implementation-plan -> implementation -> implementation-review -> spec-update-done
                                                                                             |  (review-fix loop)
                                                                                   ralph-loop-init (장시간 테스트)
```

`spec-review`는 파이프라인 끝이나 중간의 감사 단계로 선택적으로 추가한다.
`spec-update-done`은 global spec이 없으면 수행하지 않는다.
`spec-summary`와 `spec-rewrite`는 비오케스트레이션 보조 스킬이다.

### 2.2 오케스트레이션 대상 스킬

#### feature-draft
- Role: temporary spec draft + implementation plan 통합 생성
- Reasoning note: feature-level execution surface를 먼저 고정한다. global spec이 thin core면 관련 코드 탐색이 필수다. Part 2가 충분히 명확하면 별도 implementation-plan 없이도 implementation 입력으로 쓸 수 있다.

#### spec-update-todo
- Role: planned persistent global change 반영
- Reasoning note: temporary execution detail은 global에 올리지 않는다.

#### implementation-plan
- Role: temporary spec delta를 phase/task 중심 계획으로 세분화
- Reasoning note: task와 validation linkage를 정리한다. `feature-draft` Part 2가 충분하지 않을 때만 deeper breakdown을 추가한다.

#### implementation
- Role: actual code generation/modification 단계

#### implementation-review
- Role: 구현 결과를 계획/스펙 대비 리뷰

#### spec-update-done
- Role: 구현/검증 완료 후 global spec 동기화
- Reasoning note: temporary execution detail은 버리고 persistent truth만 남긴다.

#### spec-review
- Role: global/temporary spec 품질 및 drift 감사
- Reasoning note: thin global model 기준으로 품질을 검증한다.

#### ralph-loop-init
- Role: 장시간 반복 검증 루프 생성 및 실행 지원

### 2.3 비오케스트레이션 스킬

| 스킬 | 용도 |
|------|------|
| spec-create | global spec 최초 생성 |
| discussion | 방향성과 개념 토론 |
| guide-create | 구현/리뷰 가이드 생성 |
| write-phased | inline phased writing helper |
| spec-summary | global/temporary spec 요약 |
| spec-rewrite | canonical model에 맞춰 spec 구조 재정리 |
| spec-upgrade | 구형 spec을 current model로 변환 |
