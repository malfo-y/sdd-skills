# SDD Workflow

이 문서는 SDD의 기본 작업 흐름과 각 문서 레이어가 어디에서 쓰이는지 설명한다.

## 1. 기본 흐름

```text
discussion
  -> global direction 정리
  -> temporary spec 또는 feature draft
  -> implementation plan
  -> implementation
  -> review-fix loop
  -> verification
  -> global spec sync
```

## 2. Global Spec이 쓰이는 시점

global spec은 모든 단계의 출발점이지만, 모든 detail의 저장소는 아니다.

여기서 읽는 것:

- repo-wide framing
- scope / non-goals / guardrails
- 장기적으로 유지할 핵심 결정

여기에 남기지 않는 것:

- feature task breakdown
- execution-level validation detail
- feature-level usage / expected result

## 3. Temporary Spec이 쓰이는 시점

중간 규모 이상 변경은 temporary spec 또는 feature draft가 중심이 된다.

여기서 다루는 것:

- change summary
- scope delta
- contract / invariant delta
- touchpoints
- implementation plan
- validation plan

즉 구현에 가까운 질문은 temporary surface에서 해결한다.

## 4. Review와 Update의 역할

- `spec-review`: global spec이면 개념 + 경계 + 결정을 본다.
- `spec-summary`: global summary는 개념 + 경계 + 결정 중심으로 압축한다.
- `spec-rewrite`: global 본문이 feature-level detail로 오염되었는지 먼저 본다.
- `spec-update-todo`, `spec-update-done`: global spec에는 persistent repo-wide information만 올린다.

## 5. Verification 원칙

SDD에서는 실행과 검증이 분리되지 않는다.

원칙:

- Execute -> Verify를 반드시 거친다.
- 검증 수단은 task 성격에 맞게 고른다.
- 문서/skill refactor에서는 diff, grep, review evidence가 유효한 검증이 될 수 있다.

## 6. Drift 방지 원칙

- global spec에 temporary execution detail을 복사하지 않는다.
- supporting information은 README나 별도 docs로 보낸다.
- code-obvious detail은 code/test/review에 맡긴다.
- mirror skill은 의미상 같은 계약을 유지한다.
