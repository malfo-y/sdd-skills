# SDD Workflow

이 문서는 SDD의 기본 작업 흐름과 각 문서 레이어가 어디에서 쓰이는지 설명한다.

## 1. 기본 흐름

```text
discussion
  -> global direction 정리
  -> 계획 (계획 파일 작성 + 계획 리뷰)
  -> 구현 (실패하는 검사 먼저 + 구현 리뷰)
  -> verification
  -> global spec sync
```

discussion 뒤의 단계는 `sdd-orchestrator`가 메인 세션에서 직접 실행한다. 계획 리뷰와 구현 리뷰는 같은 세션이 한 번씩 하고, 찾은 것을 그 자리에서 고친다. 독립 리뷰가 필요하면 PR 시점에 `pr-review`를 쓴다.

## 2. Harness가 쓰이는 시점

하네스(`AGENTS.md`)는 작업 진입·작업 규약 레이어로, global spec 위에 놓인다. 작업 시작 시 하네스를 먼저 읽고 거기서 global spec / `_sdd/env.md` / 진행 중인 temporary spec으로 분기한다.

하네스는 작업 규약(how)만 담고, repo-specific 트리거는 global spec Guardrails가 단일 소스다.

## 3. Global Spec이 쓰이는 시점

global spec은 모든 단계의 출발점이지만, 모든 detail의 저장소는 아니다.

여기서 읽는 것:

- repo-wide framing
- scope / non-goals / guardrails
- 장기적으로 유지할 핵심 결정

여기에 남기지 않는 것:

- feature task breakdown
- execution-level validation detail
- feature-level usage / expected result

## 4. Temporary Spec이 쓰이는 시점

중간 규모 이상 변경은 temporary spec(= feature draft)이 중심이 된다.

여기서 다루는 것:

- change summary
- scope (In/Out)
- 바꿀 자리 / 끝나는 조건과 판정 방법 / 진행 기록

즉 구현에 가까운 질문은 temporary surface에서 해결한다.

## 5. 공통 코어 4축이 쓰이는 시점

`Thinness`, `Decision-bearing truth`, `Anti-duplication`, `Navigation + surface fit`은 spec lifecycle 스킬 전반의 공통 기준선이다.

실무에서는 아래처럼 읽는다.

- create: global spec을 얇게 만들되 판단을 바꾸는 truth만 남긴다
- upgrade(점검): 4축 위반과 코드와의 어긋남을 evidence와 함께 판정한다
- upgrade(고치기): legacy spec을 4축에 맞게 줄이고, 4축이 더 잘 드러나도록 구조를 재배치한다

## 6. 두 lifecycle 스킬의 역할 차이

- `spec-create`: 얇은 global spec을 처음 만든다. 기본값은 `main.md` 단일 파일이고, 분할은 structure rationale이 있을 때만 허용한다.
- `spec-upgrade`: 기존 스펙을 점검하고 current model에 맞게 고친다. 점검만 요청받으면 spec과 하네스를 수정하지 않고 finding을 evidence와 함께 보고한다. global spec의 feature-level 오염은 기본적으로 `Quality`이며, 잘못된 repo-wide truth처럼 판단을 오도할 때만 `Critical`이다. 고칠 때는 구형 포맷을 current model로 옮기고 구조를 재정리하되 rationale, citation, code excerpt header를 보존하고, migration history나 실행 로그성 설명은 body 대신 `decision_log`로 내린다. 고친 뒤에는 하네스(`AGENTS.md`·훅)를 갱신한다.

## 7. Review와 Update의 역할

- `spec-upgrade`의 점검: 품질과 drift를 audit한다. 수정하지 않는다.
- `sdd-orchestrator`의 spec-sync 단계: global spec에는 persistent repo-wide information만 올린다(구현 전 planned alignment / 구현 후 evidence sync를 evidence에 맞춰 처리).
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
