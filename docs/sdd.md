# SDD

SDD는 “spec을 쓴다”보다 “어떤 정보를 어디에 남겨야 판단이 흔들리지 않는가”를 다루는 방식이다.

## 1. 핵심 주장

- global spec은 repo-wide 판단 기준을 고정한다.
- temporary spec은 변경 실행 청사진을 제공한다.
- code-obvious detail은 code/test/review가 더 잘 전달한다.
- supporting information은 guide, README, reference docs로 분리한다.

## 2. Global Spec이 답하는 질문

- 이 repo는 무엇을 해결하는가
- 어디까지가 scope인가
- 무엇이 non-goal인가
- 어떤 guardrail과 핵심 결정이 유지되어야 하는가

## 3. Temporary Spec이 답하는 질문

- 이번 변경은 무엇을 바꾸는가
- 어떤 delta가 있는가
- 어디를 건드리는가
- 무엇으로 검증할 것인가

## 4. 분리 원칙

SDD는 한 문서에 모든 것을 넣는 방식을 택하지 않는다.

- repo-wide 판단 기준은 global spec에 둔다.
- feature-level execution detail은 temporary spec에 둔다.
- 사용 예시와 supporting reference는 guide나 README로 보낸다.
- 코드에서 바로 복구되는 detail은 code/test/review에 맡긴다.

## 5. 실무 규칙

- global spec은 repo-wide 판단 기준에 집중한다.
- temporary spec은 구체적으로 쓴다.
- repo-wide invariant가 정말 필요하면 guardrails나 key decisions에 남긴다.
- guide는 authoritative layer가 아니라 on-demand companion이다.

## 6. 요약

> SDD는 더 많은 문서를 만드는 방식이 아니라, 올바른 정보를 올바른 레이어에 두는 방식이다.
