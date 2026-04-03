# SDD 스펙의 정의

SDD에서 말하는 "스펙"이 무엇인지, 왜 단순한 문서가 아닌지, 어떤 구조와 성질을 가져야 하는지 정리한 문서입니다.

관련 문서:
- [SDD_CONCEPT.md](SDD_CONCEPT.md): 글로벌 스펙과 임시 스펙의 두 단계 구조
- [SDD_WORKFLOW.md](SDD_WORKFLOW.md): 스펙이 실제 개발 루프에서 어떻게 쓰이는가
- [sdd.md](sdd.md): SDD 전체 철학과 문제의식

---

## 1. 왜 "스펙의 정의"가 따로 필요한가

SDD에서 스펙은 단순한 문서가 아닙니다. AI 에이전트와 사람이 함께 개발할 때, 스펙은 무엇을 만들지, 왜 그렇게 설계했는지, 무엇을 바꾸면 안 되는지를 고정하는 기준점입니다.

스펙의 정의가 약하면 다음 문제가 반복됩니다.

- 스펙이 컴포넌트 목록이나 API 목록으로 축소된다
- 구현 이유와 설계 맥락이 빠져, 사람과 AI가 매번 다시 추측한다
- 사용법과 기대 결과가 없어 검증 기준이 흐려진다
- 코드와 문서의 연결이 약해 drift를 관리하기 어렵다

그래서 SDD에서 스펙은 "무엇이 들어가야 하는 문서인가"를 명시적으로 정의해야 합니다.

---

## 2. SDD에서 스펙은 무엇이 아닌가

SDD의 스펙은 아래와 같은 문서로 축소되지 않습니다.

- 단순한 기능 목록
- API/CLI/설정값 레퍼런스 모음
- 구현이 끝난 뒤 뒤늦게 적는 사후 보고서
- 코드가 이미 말해주는 사실만 옮겨 적은 매뉴얼

이런 문서도 필요하지만, 그것만으로는 "왜 이 구조인지", "핵심 아이디어가 무엇인지", "어떤 결과를 기대해야 하는지"를 설명하지 못합니다.

---

## 3. SDD에서 스펙은 무엇인가

SDD에서 스펙은 다음 성질을 가진 문서입니다.

> 스펙은 프로젝트의 문제, high-level concept, scope, non-goals, guardrails, 핵심 결정, Contract / Invariants / Verifiability, 기대 결과, 그리고 필요 시 코드로 진입할 전략적 힌트를 담아 사람과 AI를 정렬하는 화이트페이퍼형 Single Source of Truth다.

즉, 스펙은 다음을 동시에 해야 합니다.

- 문제와 개념을 설명한다: 이 프로젝트가 무엇을 해결하며, 어떤 관점으로 접근하는가
- scope를 고정한다: 무엇을 제공하고 무엇을 제공하지 않는가
- guardrail을 명시한다: 무엇을 하면 안 되고, 어떤 결정은 깨면 안 되는가
- 핵심 설계를 설명한다: 어떤 아이디어와 구조를 유지해야 하는가
- 계약과 불변조건을 고정한다: 무엇이 반드시 성립해야 하며, 어떻게 검증할 수 있는가
- 구현 진입점을 제공한다: 필요할 때 실제 코드 어디를 보면 되는가
- 사용과 검증을 안내한다: 어떻게 써야 하고 어떤 결과가 나와야 하는가

이 관점에서 스펙은 "소프트웨어 매뉴얼"보다 "기술 화이트페이퍼"에 가깝지만, 전통적인 상세 설명서와는 다릅니다. SDD의 스펙은 사람에게는 방향과 경계를 주고, AI에게는 추측을 줄이기 위한 기준점, 계약, 탐색 힌트를 주는 문서입니다.

---

## 4. 왜 화이트페이퍼 스타일인가

화이트페이퍼나 기술 논문은 단순히 결과만 나열하지 않습니다. 배경과 문제의식이 있고, 핵심 방법이 있으며, 구현과 결과가 이어집니다. SDD의 스펙도 같은 흐름을 가져야 합니다.

그 이유는 명확합니다.

- 사람은 배경, 개념, scope를 통해 설계 판단과 책임 범위를 이해한다
- AI는 명시된 의도, scope, guardrail을 통해 추측 대신 정렬된 구현을 한다
- 리뷰어는 기대 결과와 핵심 결정, contract/invariant, 전략적 코드 힌트를 통해 검증 경로를 잡는다

다만 여기서 중요한 점이 있습니다. 사람과 LLM은 같은 문서를 읽어도 필요한 정보 밀도가 다릅니다.

- 사람은 먼저 introduction 수준의 설명, 핵심 개념, scope, non-goals, guardrail이 필요합니다.
- LLM은 구현 디테일 전체를 문서로 읽기보다, 필요할 때 코드를 직접 탐색하고 재구성하는 편이 더 효율적입니다.
- 따라서 SDD의 글로벌 화이트페이퍼는 "모든 구현 상세를 담은 문서"가 아니라, 얇은 서사, 경계 정의, 계약, 그리고 선택적 navigation hint를 담는 기준 문서에 가깝습니다.
- 반대로 임시 스펙은 실행 청사진이므로 글로벌 스펙보다 더 직접적인 delta와 실행 정보를 담습니다.

즉, 화이트페이퍼 스타일은 미적인 선택이 아니라, 설계 의도를 잃지 않으면서도 사람과 AI가 각자 다른 방식으로 빠르게 정렬되게 하는 구조적 장치입니다.

---

## 5. 논문 요소와 코드 스펙의 대응

| 학술 문서 요소 | SDD 스펙에서의 대응 |
|----------------|---------------------|
| Abstract | 프로젝트 개요, high-level concept, 핵심 가치 |
| Introduction / Motivation | 배경, 문제 정의, 왜 이 프로젝트인가 |
| Related Work | 대안 접근과 선택 이유 |
| Core Method / Algorithm | 핵심 설계, 유지해야 할 구조, 주요 결정 |
| Implementation Details | decision-bearing structure, temporary spec의 touchpoints / implementation plan, 또는 부록 수준의 전략적 code map |
| Experiments | 사용 시나리오, validation plan, 검증 시나리오 |
| Results | 기대 결과, acceptance criteria, 관찰 가능한 동작, failure guarantees |
| References | 코드 citation, 관련 문서 링크, 부록 참조 |

핵심은 논문 형식을 그대로 흉내 내는 것이 아니라, 논문이 가진 설명 구조를 코드 세계에 맞게 번역하는 것입니다.

---

## 6. SDD 스펙이 반드시 담아야 하는 것

SDD의 스펙은 공통 코어를 공유하되 global spec과 temporary spec의 정보 밀도는 다르게 가져갑니다.

### 1) 모든 스펙이 공유하는 공통 코어

#### a. 배경 및 high-level concept

- 해결하려는 문제
- 이 문제를 왜 지금 풀어야 하는지
- 이 프로젝트를 어떤 관점과 아이디어로 이해해야 하는지
- 대안 대비 현재 접근의 이유

#### b. Scope / Non-goals / Guardrails

- 어떤 핵심 기능을 제공하는가
- 어떤 책임 범위를 가지는가
- 무엇은 의도적으로 하지 않는가
- 어떤 제약과 금지사항을 지켜야 하는가

scope는 단순한 기능 목록이 아닙니다. scope는 "무엇을 할 수 있는가"와 함께 "어디까지를 책임지며 무엇은 하지 않는가"를 고정하는 경계 선언입니다.

#### c. 핵심 설계와 주요 결정

- 시스템의 핵심 아이디어
- 주요 로직 또는 알고리즘의 흐름
- 왜 이런 구조를 택했는지에 대한 설명
- 다음 변경에서도 유지해야 할 핵심 결정

#### d. Contract / Invariants / Verifiability

이 축은 더 얇아진 스펙에서 오히려 더 중요합니다. 구현 디테일을 줄이더라도, 무엇이 반드시 성립해야 하는지는 더 명시적으로 남아야 합니다.

이 축은 모든 스펙에 적용되지만, 표현 방식은 다를 수 있습니다. 글로벌 스펙에서는 독립 필수 섹션으로 두고, temporary spec에서는 `Contract/Invariant Delta`와 `Validation Plan`으로 구현합니다.

글로벌 스펙의 `Contract / Invariants / Verifiability`는 아래 3블록 구조를 canonical shape로 사용합니다.

**Contract**

| ID | Subject | Inputs/Outputs | Preconditions | Postconditions | Failure Guarantees |
|----|---------|----------------|---------------|----------------|--------------------|
| C1 | ... | ... | ... | ... | ... |

- 각 셀은 짧은 규범 문장으로 씁니다.
- `Inputs/Outputs`만으로 끝내지 말고, `Preconditions`, `Postconditions`, `Failure Guarantees`까지 적어야 합니다.

**Invariants**

| ID | Scope | Invariant | Why It Matters |
|----|-------|-----------|----------------|
| I1 | ... | ... | ... |

- 글로벌 스펙에는 시스템/도메인 차원의 핵심 불변조건만 남깁니다.
- 로컬 구현 불변식은 코드와 온디맨드 분석에 맡기는 편이 낫습니다.

**Verifiability**

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, I1 | test | ... |

- `Verification Method`는 canonical enum을 사용합니다: `test`, `review`, `runtime-check`, `manual-check`
- 다중 target이나 복합 검증 방법의 표면 문법은 엄격히 고정하지 않습니다. 핵심은 ID와 enum이 보존되는 것입니다.

#### e. 사용 가이드와 기대 결과

- 어떤 시나리오로 사용되는가
- 사용하면 어떤 결과가 나와야 하는가
- 실패/예외 상황에서 무엇이 보장되는가

### 2) 글로벌 스펙에 추가로 필요한 것

#### a. Decision-bearing structure

글로벌 스펙은 architecture/component의 전수 inventory를 유지하는 문서가 아닙니다. 대신 아래 같은 구조 판단을 남겨야 합니다.

- 시스템 경계
- ownership
- cross-component contract
- extension point
- invariant hotspot

즉, 글로벌 스펙에 남겨야 하는 구조 정보는 inventory가 아니라 decision-bearing structure입니다.

#### b. 보조 참조 정보

- 데이터 모델
- API 참조
- 환경 및 설정

#### c. Appendix-level strategic code map

- 설명이 실제 코드와 연결되어야 한다
- 하지만 코드 전체를 문서로 복제할 필요는 없다
- 문서만 읽고도 "어디를 보면 되는가"를 파악할 수 있어야 한다
- 특히 entrypoint, invariant hotspot, extension point, change hotspot 같은 정보가 유용하다

전략적 code map은 글로벌 스펙 본문보다 부록/후반부 보조 영역에 두는 편이 적합합니다.

### 3) 임시 스펙에 추가로 필요한 것

temporary spec은 글로벌 스펙의 요약 복사본이 아니라, 변경을 실행하기 위한 청사진입니다. 따라서 global background 전체를 반복하지 않고, 변경 관련 코어만 짧게 재서술한 뒤, 아래 실행 블록을 추가해야 합니다.

- Change Summary
- Scope Delta
- Contract/Invariant Delta
- Touchpoints
- Implementation Plan
- Validation Plan
- Risks / Open Questions

여기서 중요한 점:

- `Touchpoints`는 필수입니다.
- `Implementation Plan`은 요약+링크형이 적합합니다.
- `Validation Plan`은 `Contract/Invariant Delta`의 ID와 직접 매핑되어야 합니다.
- invariant 변화는 `Contract Delta` 안에 숨기지 말고 `Contract/Invariant Delta`로 명시합니다.

---

## 7. 권장되는 스펙 구조

SDD의 canonical model에서 global spec과 temporary spec은 아래처럼 다른 구조를 가집니다.

```markdown
# 프로젝트명 글로벌 스펙

## 1. 배경 및 high-level concept
## 2. Scope / Non-goals / Guardrails
## 3. 핵심 설계와 주요 결정
## 4. Contract / Invariants / Verifiability
## 5. 사용 가이드 & 기대 결과
## 6. Decision-bearing structure
## 7. 참조 정보
### 데이터 모델
### API 참조
### 환경 및 설정

## 부록 A. Strategic Code Map
## 부록 B. 관련 문서 및 코드 레퍼런스
```

```markdown
# 기능명 Temporary Spec

## 1. Change Summary
## 2. Scope Delta
## 3. Contract/Invariant Delta
## 4. Touchpoints
## 5. Implementation Plan
## 6. Validation Plan
## 7. Risks / Open Questions
```

중요한 점은 architecture detail이나 component detail 같은 참조형 내용을 완전히 버리자는 뜻이 아니라, 그것들을 더 이상 글로벌 스펙의 기본 본문 구조로 강제하지 않는다는 점입니다. 필요한 경우에는 decision-bearing structure나 appendix-level reference로 다룹니다.

---

## 8. 코드와 연결되는 방식

SDD 스펙은 코드와 느슨하게 연결된 문서가 아니라, 코드와 직접 대화할 수 있는 문서여야 합니다.

권장 원칙:

- 핵심 설계는 실제 코드와 연결한다
- 그러나 코드베이스 전체를 문서로 다시 매핑하려 하지 않는다
- global spec의 code map은 appendix-level strategic hint로 제한한다
- architecture/component 정보는 전수 inventory가 아니라 decision-bearing structure 중심으로 남긴다
- 인라인 citation은 `[filepath:functionName]` 같은 형식을 사용할 수 있다
- 코드 발췌는 숨은 제약이나 핵심 invariant를 설명할 때만 선택적으로 사용한다
- routine implementation detail은 문서보다 코드 탐색과 온디맨드 요약에 맡긴다
- temporary spec에서는 `Touchpoints`를 통해 변경할 파일과 hotspot을 직접 가리킨다
- temporary spec의 `Validation Plan`은 `Contract/Invariant Delta`의 ID를 기준으로 검증 항목을 추적한다

이 방식은 사람에게는 탐색 경로를 주고, AI에게는 빠른 진입점을 제공합니다. 동시에 문서가 코드의 그림자 복사본으로 변질되는 것을 막아 drift 비용도 줄입니다.

---

## 9. 글로벌 스펙과 임시 스펙의 관계

SDD에는 글로벌 스펙과 임시 스펙이 있습니다. 둘은 공통 코어를 공유하지만, 같은 밀도로 작성되지는 않습니다.

### 글로벌 스펙

- 프로젝트의 안정된 Single Source of Truth
- 현재 상태의 개념, scope, guardrail, 핵심 결정, contract/invariant를 담는다
- decision-bearing structure를 유지한다
- appendix-level strategic code map을 선택적으로 포함할 수 있다
- implementation detail inventory로 비대해지지 않아야 한다
- 구현 후 `spec-update-done`으로 코드와 다시 정렬된다

### 임시 스펙

- 변경의 청사진
- global spec 전체를 반복하지 않고, 변경 관련 코어만 짧게 재서술한다
- 무엇을 바꿀지와 어떻게 구현할지를 미리 고정한다
- `Contract/Invariant Delta`, `Touchpoints`, `Implementation Plan`, `Validation Plan`, `Risks / Open Questions`를 통해 실행 정보를 직접 제공한다
- 검증 후 구현으로 이어지고, 완료되면 글로벌 스펙에 병합된다

즉, 임시 스펙은 "변경 제안서"이면서 동시에 "구현용 화이트페이퍼"여야 합니다. 다만 독립적인 백서를 다시 쓰는 것이 아니라, global spec 위에서 delta와 execution을 정렬하는 문서에 가깝습니다.

---

## 10. 좋은 스펙의 판단 기준

좋은 스펙은 다음 질문에 답할 수 있어야 합니다.

- 이 프로젝트나 기능은 왜 존재하는가
- 이 프로젝트는 어디까지를 책임지고, 어디부터는 하지 않는가
- 무엇을 반드시 보장해야 하는가
- 무엇을 하면 안 되는가
- 핵심 설계와 핵심 결정은 무엇인가
- 어떤 contract와 invariant가 이 시스템을 규정하는가
- 그것이 어떻게 검증되는가
- 실제 코드에서 어디부터 보면 되는가
- 사용자는 어떤 결과를 기대해야 하는가
- 다음 변경을 할 때 무엇을 깨면 안 되는가

temporary spec이라면 추가로 아래 질문에도 답해야 합니다.

- 이번 변경에서 무엇이 달라지는가
- 어떤 contract/invariant가 바뀌는가
- 어디를 건드려야 하는가
- 무엇으로 검증할 것인가
- 남아 있는 리스크와 미결 질문은 무엇인가

이 질문에 답하지 못한다면, 문서는 길어도 아직 SDD의 스펙이라고 부르기 어렵습니다.

---

## 11. 한 문장 정의

SDD에서 스펙은 단순한 설명서가 아니라, 문제와 개념, scope와 guardrail, 핵심 결정, Contract / Invariants / Verifiability, 기대 결과, 그리고 필요 시 코드로 진입할 전략적 힌트를 담아 사람과 AI의 구현·리뷰·동기화를 정렬하는 화이트페이퍼형 기준 문서다.
