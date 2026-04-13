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

## 4. 공통 코어 4축이 쓰이는 시점

`Thinness`, `Decision-bearing truth`, `Anti-duplication`, `Navigation + surface fit`은 spec lifecycle 스킬 전반의 공통 기준선이다.

실무에서는 아래처럼 읽는다.

- create: global spec을 얇게 만들되 판단을 바꾸는 truth만 남긴다
- review: 문서 타입에 맞는 rubric으로 4축 위반을 판정한다
- rewrite: 4축을 더 잘 드러내도록 구조를 재배치한다
- upgrade: legacy spec을 4축에 맞게 줄이되, upgrade 범위를 넘으면 rewrite로 넘긴다

## 5. `spec-summary`가 쓰이는 시점

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

## 6. 네 개 lifecycle 스킬의 역할 차이

- `spec-create`: 얇은 global spec을 처음 만든다. 기본값은 `main.md` 단일 파일이고, 분할은 structure rationale이 있을 때만 허용한다.
- `spec-review`: global/temporary rubric을 분리해서 감사한다. global spec의 feature-level 오염은 기본적으로 `Quality`이며, 문서 타입 혼동이나 잘못된 repo-wide truth처럼 판단을 오도할 때만 `Critical`이다. 모든 finding은 evidence를 가져야 한다.
- `spec-rewrite`: 기존 스펙을 더 나은 구조로 재정리한다. rationale, citation, code excerpt header를 보존하고, migration history나 실행 로그성 설명은 body 대신 `decision_log` 또는 rewrite report로 내린다.
- `spec-upgrade`: 구형 포맷을 current model로 옮긴다. 다만 핵심 문제가 대규모 구조 재설계라면 upgrade로 밀어붙이지 않고 `spec-rewrite`로 분기한다.

## 7. Review와 Update의 역할

- `spec-review`: 품질과 drift를 audit한다. 수정하지 않는다.
- `spec-update-todo`, `spec-update-done`: global spec에는 persistent repo-wide information만 올린다.
- update 계열은 temporary execution detail을 global 본문으로 복사하지 않는다.

## 8. Verification 원칙

SDD에서는 실행과 검증이 분리되지 않는다.

원칙:

- Execute -> Verify를 반드시 거친다.
- 검증 수단은 task 성격에 맞게 고른다.
- 문서/skill refactor에서는 diff, grep, review evidence가 유효한 검증이 될 수 있다.

## 9. Drift 방지 원칙

- global spec에 temporary execution detail을 복사하지 않는다.
- supporting information은 README나 별도 docs로 보낸다.
- code-obvious detail은 code/test/review에 맡긴다.
- mirror skill은 의미상 같은 계약을 유지한다.
