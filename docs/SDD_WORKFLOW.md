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

## 4. `spec-summary`가 쓰이는 시점

`spec-summary`는 사람이 이 repo를 한 문서로 이해해야 할 때 쓰인다.

여기서 다루는 것:

- 무엇을 해결하는가
- 왜 이 접근을 택했는가
- 핵심 설계가 무엇인가
- 실제 코드에서 어디를 보면 되는가
- 어떻게 읽고 무엇을 기대해야 하는가

여기서 본문으로 다루지 않는 것:

- migration memo
- changelog 서사
- 본문을 잠식하는 긴 계획/진행 로그

관련 draft/implementation signal이 있으면 appendix에 짧게 덧붙일 수 있다.

## 5. Review와 Update의 역할

- `spec-review`: global spec이면 개념 + 경계 + 결정을 본다.
- `spec-summary`: `summary.md`를 reader-facing whitepaper로 작성해 문제, 동기, 선택 이유, 핵심 설계, 코드 근거, 사용/기대 결과를 한 문서에서 설명하고, 필요하면 appendix에 계획/진행 상태를 짧게 덧붙인다.
- `spec-rewrite`: global 본문이 feature-level detail로 오염되었는지 먼저 본다.
- `spec-update-todo`, `spec-update-done`: global spec에는 persistent repo-wide information만 올린다.

## 6. Verification 원칙

SDD에서는 실행과 검증이 분리되지 않는다.

원칙:

- Execute -> Verify를 반드시 거친다.
- 검증 수단은 task 성격에 맞게 고른다.
- 문서/skill refactor에서는 diff, grep, review evidence가 유효한 검증이 될 수 있다.

## 7. Drift 방지 원칙

- global spec에 temporary execution detail을 복사하지 않는다.
- supporting information은 README나 별도 docs로 보낸다.
- code-obvious detail은 code/test/review에 맡긴다.
- mirror skill은 의미상 같은 계약을 유지한다.
