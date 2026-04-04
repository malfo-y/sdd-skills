# SDD Concept

이 문서는 SDD가 정보를 어떤 레이어에 배치하는지 설명한다.

## 1. 핵심 레이어

| Layer | 역할 | 담는 것 |
|------|------|---------|
| Global spec | repo-wide 판단 기준 | 개념, 경계, 핵심 결정 |
| Temporary spec | 변경 실행 청사진 | delta, touchpoints, validation, plan |
| Code/Test | 실제 동작과 세부 truth | 구현, 실행 흐름, 세부 contract |
| Guide/README/Refs | 보조 설명 | 사용 예시, 환경 상세, 참조 정보 |

## 2. Global Spec의 역할

global spec은 repo를 어떤 문제와 관점으로 읽어야 하는지, 어디까지가 scope인지, 어떤 guardrail과 핵심 결정이 유지되어야 하는지를 고정한다.

global spec이 담당하는 것:

- 배경 및 high-level concept
- scope / non-goals / guardrails
- 핵심 설계와 주요 결정

global spec이 기본적으로 담당하지 않는 것:

- feature-level usage guide
- feature-level contract / validation detail
- exhaustive inventory
- 코드에서 바로 복구 가능한 설명

## 3. Temporary Spec의 역할

temporary spec은 변경 하나를 실행하기 위한 문서다.

temporary spec이 담당하는 것:

- 이번 변경이 무엇을 바꾸는가
- 어떤 경계가 달라지는가
- 어떤 contract / invariant delta가 있는가
- 어디를 건드리는가
- 무엇으로 검증할 것인가

즉 global spec이 repo-wide 판단 기준이라면, temporary spec은 작업 단위 청사진이다.

## 4. Guide의 역할

guide는 별도 영구 spec 계층이 아니라, 필요할 때 만드는 companion surface다.

적합한 경우:

- 특정 feature의 사용 흐름을 빠르게 설명해야 할 때
- 리뷰어에게 bounded context가 필요할 때
- 코드만 읽는 것보다 guide가 더 빠른 경우

guide는 global spec을 대체하지 않고, temporary spec을 영구 저장소로 바꾸지도 않는다.

## 5. 정보 배치 원칙

정보를 어디에 둘지 판단할 때는 아래 순서를 따른다.

1. repo-wide 판단 기준인가
2. 특정 feature의 실행 문맥인가
3. supporting reference인가
4. 코드를 보면 바로 복구되는가

판단 기준:

- 1에 가깝다면 global spec 후보다.
- 2에 가깝다면 temporary spec 또는 guide 후보다.
- 3에 가깝다면 README나 별도 docs 후보다.
- 4에 가깝다면 문서보다 code/test/review가 더 적절하다.
