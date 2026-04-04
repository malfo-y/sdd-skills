# SDD Quick Start

## 1. 먼저 기억할 것

1. global spec은 repo-wide 판단 기준이다.
2. temporary spec은 변경 실행 청사진이다.
3. code-obvious detail은 global spec에 억지로 넣지 않는다.
4. feature-level usage / contract / validation은 temporary surface나 guide로 보낸다.

## 2. 새 프로젝트에서 시작할 때

global spec에는 아래 세 가지만 먼저 고정하면 된다.

```markdown
## 1. Background and High-Level Concept
## 2. Scope / Non-goals / Guardrails
## 3. Core Design and Key Decisions
```

추가 정보는 필요할 때만 supporting docs로 뺀다.

## 3. 기능 작업을 시작할 때

아래 중 하나를 쓴다.

- 작은 변경: implementation + review
- 중간 이상 변경: feature draft 또는 temporary spec
- 범위가 애매함: discussion 먼저

## 4. Global Spec에 넣지 말 것

- feature-level expected result
- feature별 contract / validation detail
- 사용 가이드 전체
- exhaustive inventory
- 코드만 보면 알 수 있는 설명

## 5. 어디에 둘 것인가

- 실행 계획: temporary spec / implementation plan
- 사용 예시: guide / README
- 환경 상세: README / env docs
- 탐색 힌트: appendix, review note, code comment

## 6. 리뷰할 때

- global spec이면 개념 + 경계 + 결정이 분명한지 본다.
- temporary spec이면 delta와 validation linkage가 분명한지 본다.
- 두 문서를 모두 백과사전처럼 만들려고 하지 않는다.
