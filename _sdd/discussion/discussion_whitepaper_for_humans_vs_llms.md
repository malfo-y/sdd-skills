# 토론 요약: 사람용 whitepaper와 LLM용 whitepaper는 같은가

**날짜**: 2026-04-03
**라운드 수**: 28
**참여 방식**: 구조화된 토론 (discussion skill)

## 핵심 논점 (Key Discussion Points)

1. **소비자별 정보 우선순위 차이**: 사람은 문서를 읽고 개념과 범위를 먼저 이해한 뒤 코드를 탐색하지만, LLM은 코드를 즉시 검색하고 필요한 상세를 빠르게 재구성할 수 있다.
2. **사람에게 필요한 지속 문서의 축소**: 사람용 지속 스펙은 full implementation narrative보다 high-level concept, scope, non-goals, guardrails, 핵심 결정에 집중하는 편이 더 실용적이다.
3. **scope의 의미는 기능 목록보다 넓다**: scope는 단순히 "무엇을 할 수 있는가"만이 아니라, 프로젝트가 책임지는 문제 영역, 제공하는 핵심 기능, 하지 않는 것, 인접하지만 제외되는 요구를 함께 정의한다.
4. **LLM에게 필요한 코드지도는 전수 목록이 아님**: LLM은 일반적인 파일 트리나 컴포넌트 목록보다, 엔트리포인트, invariant hotspot, extension point, 변경 hotspot 같은 전략적 탐색 힌트에서 더 큰 도움을 받는다.
5. **구현 상세의 저장 위치 문제**: 구현 디테일을 스펙에 지속적으로 적재하기보다, 필요 시 LLM이 코드에서 재탐색하고 요약하는 방식이 더 agent-native하다.
6. **whitepaper 개념의 재해석 필요**: `whitepaper`를 인간 독자용 상세 설명서로 이해하면 과도해진다. SDD에서는 얇은 서사와 선택적 navigation hint를 함께 담는 기준 문서로 재정의하는 편이 맞다.
7. **글로벌 스펙의 구조 정보는 inventory가 아니라 decision-bearing structure여야 한다**: 전수형 architecture/component 설명보다 시스템 경계, ownership, cross-component contract, extension point, invariant hotspot 같은 구조 판단이 더 가치 있다.
8. **더 얇아진 글로벌 스펙일수록 계약 축이 더 중요해진다**: 구현 디테일을 줄이는 대신 Contract / Invariants / Verifiability를 별도 필수 축으로 올려야 executable spec 성격이 유지된다.
9. **임시 스펙은 구현용 상세 설명서보다 실행 청사진에 가깝다**: temporary spec은 변경 scope, contract delta, 구현 계획, 검증 계획을 묶은 실행 문서로 정의하는 편이 맞다.
10. **전략적 code map은 본문보다 부록에 두는 편이 적합하다**: 글로벌 스펙 본문은 얇게 유지하고, 탐색 힌트는 appendix 또는 후반부 보조 영역으로 분리하는 것이 목적에 더 부합한다.
11. **Contract / Invariants / Verifiability는 한 섹션 아래 3블록 구조가 적합하다**: 세 축을 분리하되 한 자리에서 읽히게 해야 executable spec의 성격이 선명해진다.
12. **Contract는 입출력보다 넓은 약속이어야 한다**: Inputs/Outputs만이 아니라 Preconditions, Postconditions, Failure Guarantees까지 포함해야 검증 가능한 기준이 된다.
13. **글로벌 스펙의 invariant는 상위 핵심 불변조건만 남겨야 한다**: 시스템/도메인 의미를 규정하는 invariants만 유지하고, 로컬 구현 불변식은 코드와 온디맨드 분석에 맡기는 편이 맞다.
14. **Verifiability는 자유 서술보다 매핑 표가 낫다**: 각 contract/invariant가 테스트, 리뷰 체크, 런타임 확인 중 어떤 방식으로 검증되는지 명시적으로 연결해야 한다.
15. **추적성을 위해 고정 ID가 필요하다**: Contract, Invariant, Verifiability 항목은 C1/I1/V1 같은 ID를 가져야 리뷰, 테스트, temporary spec delta와 연결하기 쉽다.
16. **Contract 표는 6컬럼 기본형이 적합하다**: Notes 같은 설명용 컬럼을 기본에서 제거해야 contract 문장이 느슨해지지 않는다.
17. **Invariants 표는 4컬럼 기본형이 적합하다**: invariant 정의와 그 중요성을 압축해서 유지하고, 위반 영향의 장황한 설명은 기본 템플릿에서 제외한다.
18. **Verifiability 표는 4컬럼 기본형이 적합하다**: 추적 대상과 검증 방법, 근거를 잇는 최소 구조면 충분하다.
19. **표 셀은 짧은 규범 문장으로 써야 한다**: 키워드 나열보다 판정 가능한 문장을 써야 executable spec으로 작동한다.
20. **Verification Method는 고정 enum을 써야 한다**: 검증 방식은 자유 서술이 아니라 제한된 값 집합으로 관리해야 일관성과 기계적 활용성이 높아진다.
21. **표면 문법은 과도하게 고정할 필요가 없다**: ID와 enum만 고정되면, 다중 target 표기나 복합 검증 방법 표기는 LLM이 문맥상 충분히 해석할 수 있다.
22. **global spec과 temporary spec은 공통 코어를 공유하되 정보 밀도는 달라야 한다**: temporary spec은 global spec을 복제하는 것이 아니라, 변경과 실행에 필요한 코어만 더 짧고 직접적으로 재서술해야 한다.
23. **temporary spec의 코어 재서술은 변경 관련 부분으로 제한해야 한다**: global background 전체를 반복하기보다 이번 변경에 영향을 주는 scope, guardrail, contract만 간략하게 다시 쓴다.
24. **temporary spec에는 코드 접점 정보가 필수다**: target files, hotspots, touchpoints는 실행 청사진에서 반드시 보여야 한다.
25. **implementation plan은 임시 스펙 안에 요약하고, 상세는 필요 시 별도 문서로 확장한다**: 대규모 구현을 위해 요약+링크형이 적합하다.
26. **validation plan은 contract/invariant delta와 직접 연결되어야 한다**: 변경된 약속과 불변조건이 어떤 방식으로 검증되는지 ID 수준에서 연결해야 한다.
27. **temporary spec에는 Risks / Open Questions가 필수다**: 실행 문서라면 남아 있는 불확실성과 위험을 감추지 말고 드러내야 한다.
28. **temporary spec의 canonical section set은 7섹션 압축형이 적합하다**: 과도한 분리보다 compact한 실행 문서가 더 잘 맞는다.
29. **delta 섹션은 `Contract/Invariant Delta`로 명시해야 한다**: invariant 변화는 contract 변화에 암묵적으로 숨기지 말고 이름에서 드러내야 한다.

## 결정 사항 (Decisions Made)

| # | 결정 | 근거 | 관련 논점 |
|---|------|------|----------|
| 1 | `whitepaper` 용어는 유지한다 | 기존 SDD 철학과 연속성을 유지하면서도 의미를 재정의할 수 있음 | 논점 5 |
| 2 | 사람용 지속 스펙은 `high-level concept + scope + non-goals + guardrails + key decisions` 중심으로 본다 | 사람은 모든 구현 디테일보다 방향성과 경계조건을 먼저 알아야 함 | 논점 2 |
| 3 | `scope`는 key feature 목록만이 아니라 책임 범위와 경계 선언을 함께 포함한다 | 사람과 LLM 모두 "무엇을 해야 하는가"뿐 아니라 "무엇을 하면 안 되는가"를 알아야 정렬됨 | 논점 3 |
| 4 | LLM용 지속 정보에는 `선택적 전략 지도`를 포함한다 | 코드 검색은 빠르지만, 숨은 엔트리포인트/핵심 경계/확장 포인트는 힌트가 있으면 탐색 품질이 올라감 | 논점 4 |
| 5 | 일반적인 구현 상세와 코드 전수 매핑은 main spec의 상시 유지 대상으로 보지 않는다 | 이는 codebase가 이미 보유한 정보와 중복되고 drift 비용이 큼 | 논점 4, 5 |
| 6 | [docs/SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md)의 `구현 근거와 코드 매핑` 개념은 `전략적 navigation hint` 수준으로 좁히는 것이 타당하다 | 현재 정의의 폭이 사람/LLM 모두에게 다소 과도함 | 논점 4, 6 |
| 7 | 이번 논의 결과를 SDD의 새 canonical model로 삼는다 | 이후 문서와 spec 관련 스킬을 순차적으로 이 정의에 맞게 재정렬할 예정 | 논점 6, 8 |
| 8 | 글로벌 스펙의 architecture/component 정보는 `decision-bearing structure`만 남긴다 | inventory성 구조 정보는 코드와 온디맨드 분석으로 대체 가능하지만, 구조적 경계와 핵심 판단은 지속 문서 가치가 높음 | 논점 7 |
| 9 | `Contract / Invariants / Verifiability`는 글로벌 스펙의 독립 필수 섹션으로 둔다 | 더 얇은 스펙에서도 executable spec 성격을 유지하려면 검증 기준이 문서에서 바로 보여야 함 | 논점 8 |
| 10 | temporary spec은 `변경 scope + contract delta + implementation plan + validation plan`을 묶은 실행 청사진으로 본다 | 구현용 화이트페이퍼를 실행 문서로 재정의해 global spec과 역할을 분명히 나눔 | 논점 9 |
| 11 | 전략적 code map은 글로벌 스펙 본문이 아니라 부록/후반부 보조 영역에 둔다 | 본문을 얇게 유지하면서도 탐색 힌트는 보존할 수 있음 | 논점 10 |
| 12 | `Contract / Invariants / Verifiability`는 한 섹션 아래 3블록 구조로 표준화한다 | 세 축의 역할을 분리하면서도 한 자리에서 계약-불변식-검증 연결을 볼 수 있음 | 논점 11 |
| 13 | `Contract` 블록의 기본 필드는 `Inputs/Outputs`, `Preconditions`, `Postconditions`, `Failure Guarantees`로 둔다 | executable spec이 되려면 입출력뿐 아니라 전제/사후/실패 보장까지 명시되어야 함 | 논점 12 |
| 14 | `Invariants` 블록에는 시스템/도메인 차원의 핵심 불변조건만 남긴다 | 로컬 구현 불변식까지 올리면 글로벌 스펙이 다시 구현 설명서로 비대해짐 | 논점 13 |
| 15 | `Verifiability` 블록은 각 contract/invariant를 검증 방법과 연결하는 매핑 표로 둔다 | 테스트, 리뷰 체크, 런타임 확인 가능성을 명시해야 검증 기준이 바로 작동함 | 논점 14 |
| 16 | Contract / Invariant / Verifiability 항목에는 고정 ID를 부여한다 | 예: C1, I1, V1. 추후 리뷰, 테스트, temporary spec delta에서 정확히 참조 가능 | 논점 15 |
| 17 | `Contract` 표의 canonical 컬럼은 `ID | Subject | Inputs/Outputs | Preconditions | Postconditions | Failure Guarantees`로 둔다 | 설명용 `Notes` 컬럼을 기본에서 제거해 규범성을 유지 | 논점 16 |
| 18 | `Invariants` 표의 canonical 컬럼은 `ID | Scope | Invariant | Why It Matters`로 둔다 | invariant 정의와 의미를 최소 컬럼으로 유지 | 논점 17 |
| 19 | `Verifiability` 표의 canonical 컬럼은 `ID | Targets | Verification Method | Evidence / Notes`로 둔다 | 추적성, 검증 수단, 근거 연결에 충분한 최소 구조 | 논점 18 |
| 20 | 표 셀 내용은 `짧은 규범 문장` 문체로 고정한다 | 키워드 단편보다 테스트/리뷰로 변환 가능한 판정 문장이 필요 | 논점 19 |
| 21 | `Verification Method`는 고정 enum을 사용하고 canonical set은 `test`, `review`, `runtime-check`, `manual-check`로 둔다 | 자유 텍스트보다 일관성, 검색성, 자동화 가능성이 높음 | 논점 20 |
| 22 | 다중 target 및 복합 검증 방법의 표면 표기법은 엄격히 표준화하지 않는다 | 의미 추적에 필요한 것은 ID와 enum이며, 표면 문법까지 고정하면 과규격화 위험이 큼 | 논점 21 |
| 23 | global spec과 temporary spec은 `공통 코어 + temporary 전용 실행 블록` 관계로 둔다 | 철학은 공유하되 목적과 정보 밀도는 다르게 설계하는 편이 맞음 | 논점 22 |
| 24 | temporary spec은 global spec의 전체 코어를 반복하지 않고, 변경 관련 코어만 간략하게 재서술한다 | 임시 스펙은 독립 백서가 아니라 실행 청사진이기 때문 | 논점 23 |
| 25 | temporary spec에는 `target files / hotspots / touchpoints`를 필수 섹션으로 둔다 | 실행 문서라면 어디를 건드리는지와 주의 지점을 명시해야 함 | 논점 24 |
| 26 | temporary spec의 `implementation plan`은 요약+링크형으로 둔다 | 실행 entry document를 유지하면서도 대규모 구현은 별도 plan으로 확장 가능 | 논점 25 |
| 27 | temporary spec의 `validation plan`은 contract/invariant delta ID와 직접 매핑한다 | 변경된 약속이 실제로 어떻게 검증되는지 추적 가능해야 함 | 논점 26 |
| 28 | temporary spec에 `Risks / Open Questions` 섹션을 필수로 둔다 | 실행 청사진이라면 남아 있는 불확실성과 위험을 드러내야 함 | 논점 27 |
| 29 | temporary spec의 canonical section set은 7섹션 압축형으로 둔다 | compact한 실행 문서가 목적에 더 부합함 | 논점 28 |
| 30 | 7섹션 구조의 delta 섹션 명칭은 `Contract/Invariant Delta`로 둔다 | invariant 변화도 1급 변경으로 드러나야 함 | 논점 29 |

## 미결 질문 (Open Questions)

- [ ] 전략적 code map의 유지 방식을 수동 curated로 할지, 도구 보조 생성으로 할지
- [ ] global spec과 temporary spec의 필수 섹션 차이를 템플릿 수준에서 어떻게 명시할지
- [ ] temporary spec의 `Contract/Invariant Delta`와 `Validation Plan`에서 ID 매핑 예시를 어떤 템플릿으로 보여줄지

## 실행 항목 (Action Items)

| # | 항목 | 우선순위 | 담당 |
|---|------|---------|------|
| 1 | [docs/SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md)에 `사람/LLM 소비자별 정보 밀도 차이`를 명시적으로 추가 | High | TBD |
| 2 | `구현 근거와 코드 매핑` 섹션을 `전략적 code map / navigation hint` 중심으로 재서술 | High | TBD |
| 3 | `Contract / Invariants / Verifiability`를 독립 필수 섹션으로 정의 문서와 템플릿에 반영 | High | TBD |
| 4 | 전략적 code map의 최소 스키마 정의: entrypoint, invariant hotspot, extension point, change hotspot | High | TBD |
| 5 | `Contract / Invariants / Verifiability`의 canonical 표 포맷과 ID 규칙 정의 | High | TBD |
| 6 | spec-create / spec-upgrade 템플릿이 과도한 구현 디테일을 본문에 요구하는지 점검 | High | TBD |
| 7 | global spec과 temporary spec의 필수 섹션 차이를 문서/스킬/템플릿에 동기화 | High | TBD |
| 8 | `Verification Method` enum과 셀 문체 규칙을 템플릿/가이드에 반영 | High | TBD |
| 9 | CIV 템플릿 가이드에 `ID/enum만 고정하고 표면 표기법은 유연하게 둔다`는 원칙 명시 | Medium | TBD |
| 10 | temporary spec 7섹션 canonical template 작성: `Change Summary`, `Scope Delta`, `Contract/Invariant Delta`, `Touchpoints`, `Implementation Plan`, `Validation Plan`, `Risks/Open Questions` | High | TBD |

## 리서치 결과 요약 (Research Findings)

- [docs/SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md)는 현재 스펙을 `문제, 동기, 핵심 설계, 기대 동작, 코드 근거를 함께 담는 화이트페이퍼형 Single Source of Truth`로 규정하고, 코드 매핑을 비교적 넓게 요구한다.
- [docs/SDD_CONCEPT.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_CONCEPT.md)와 [docs/SDD_WORKFLOW.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_WORKFLOW.md)는 SDD의 실제 목적을 `AI agent의 표류 제어`, `청사진 제공`, `drift 관리` 쪽에 더 강하게 둔다.
- [docs/sdd.md](/Users/hyunjoonlee/github/sdd_skills/docs/sdd.md)는 agent 시대의 핵심 문제를 interpretation drift, context loss, hallucination으로 규정하며, scope/contract/constraints의 중요성을 강조한다.
- 기존 토론 [discussion_spec_as_whitepaper.md](/Users/hyunjoonlee/github/sdd_skills/_sdd/discussion/discussion_spec_as_whitepaper.md)는 스펙을 더 논문적으로 풍부하게 만들자는 방향이었고, 이번 토론은 그 방향을 `LLM 소비 방식` 기준으로 다시 얇게 조정한 후속 논의다.

## 토론 흐름 (Discussion Flow)

Round 1: 사람용 서사와 LLM용 코드지도를 한 문서에서 어떻게 볼 것인가?  
→ 사용자 응답: 사람에게 필요한 것은 high-level concept와 introduction 수준, 그리고 scope. 나머지 디테일은 필요 시 LLM이 코드에서 빠르게 찾아 정리해 줄 수 있음.

Round 2: 지속적으로 유지할 스펙의 범위는 어디까지인가?  
→ 사용자 역질문: code map이 실제로 LLM 구현/탐색에 도움이 되는지가 먼저 판단되어야 함.

Round 3: code map이 도움이 된다면 어느 수준이 적절한가?  
→ 결정: 전수형 map이 아니라 `선택적 전략 지도`가 적절함.

Round 4: 이런 구조에서도 `whitepaper` 용어를 유지할 것인가?  
→ 결정: 용어는 유지하되 의미를 수정. 즉, SDD의 whitepaper는 얇은 서사 + 전략적 navigation hint를 담는 기준 문서로 본다.

Round 5: `scope`는 key feature 목록을 의미하는가?  
→ 결정: 아니다. scope는 핵심 기능을 포함하지만, 더 본질적으로는 프로젝트의 책임 범위와 out-of-scope 경계를 정의한다.

Round 6: 글로벌 스펙에서 architecture/component 관련 정보는 어느 수준까지 남길 것인가?  
→ 결정: 전수형 목록은 제거하고, 시스템 경계, ownership, cross-component contract, extension point, invariant hotspot 같은 `decision-bearing structure`만 남긴다.

Round 7: Contract / Invariants / Verifiability는 어떤 형태로 둘 것인가?  
→ 결정: 글로벌 스펙의 독립 필수 섹션으로 둔다.

Round 8: temporary spec의 중심 성격은 무엇인가?  
→ 결정: 변경 scope, contract delta, 구현 계획, 검증 계획을 묶은 `실행 청사진`으로 본다.

Round 9: 전략적 code map은 글로벌 스펙 어디에 둘 것인가?  
→ 결정: 본문이 아니라 부록/후반부 보조 영역에 둔다.

Round 10: `Contract / Invariants / Verifiability`는 어떤 큰 형태로 둘 것인가?  
→ 결정: 한 섹션 아래 `Contract`, `Invariants`, `Verifiability` 3블록 구조로 둔다.

Round 11: `Contract` 블록의 표준 필드는 어디까지 둘 것인가?  
→ 결정: `Inputs/Outputs`, `Preconditions`, `Postconditions`, `Failure Guarantees`를 기본 필드로 둔다.

Round 12: `Invariants` 블록에는 어느 수준의 invariant를 남길 것인가?  
→ 결정: 시스템/도메인 차원의 핵심 불변조건만 남기고, 로컬 구현 불변식은 제외한다.

Round 13: `Verifiability` 블록은 어떤 형식이 맞는가?  
→ 결정: 각 contract/invariant와 검증 방식을 연결하는 매핑 표로 둔다.

Round 14: Contract / Invariants / Verifiability 항목에 고정 ID를 붙일 것인가?  
→ 결정: 그렇다. `C1`, `I1`, `V1` 같은 식별자를 부여한다.

Round 15: `Contract` 표의 canonical 컬럼은 어느 수준으로 고정할 것인가?  
→ 결정: `ID | Subject | Inputs/Outputs | Preconditions | Postconditions | Failure Guarantees`의 6컬럼 기본형으로 둔다.

Round 16: `Invariants` 표의 canonical 컬럼은 어떻게 둘 것인가?  
→ 결정: `ID | Scope | Invariant | Why It Matters`의 4컬럼 기본형으로 둔다.

Round 17: `Verifiability` 표의 canonical 컬럼은 어떻게 둘 것인가?  
→ 결정: `ID | Targets | Verification Method | Evidence / Notes`의 4컬럼 기본형으로 둔다.

Round 18: Contract / Invariants / Verifiability 표의 셀 내용은 어떤 문체로 쓸 것인가?  
→ 결정: 각 셀은 `짧은 규범 문장`으로 쓴다.

Round 19: `Verification Method`는 어떤 값 집합으로 제한할 것인가?  
→ 결정: 고정 enum을 사용하고 canonical set은 `test`, `review`, `runtime-check`, `manual-check`로 둔다.

Round 20: `Targets`와 복합 검증 방법의 표기법까지 엄격히 정할 것인가?  
→ 결정: 아니다. `ID`와 `Verification Method` enum만 고정하고, 나머지 표면 문법은 LLM이 유연하게 작성하고 해석할 수 있도록 둔다.

Round 21: global spec과 temporary spec의 필수 섹션 관계는 어떻게 둘 것인가?  
→ 결정: `공통 코어 + temporary 전용 실행 블록` 구조로 둔다.

Round 22: temporary spec의 공통 코어는 어느 정도 직접 서술할 것인가?  
→ 결정: global spec 전체를 반복하지 않고, 변경과 직접 관련된 코어만 간략하게 재서술한다.

Round 23: temporary spec에 code touchpoints는 필수인가?  
→ 결정: 그렇다. target files, hotspots, touchpoints는 필수다.

Round 24: temporary spec의 implementation plan은 어느 수준까지 직접 담을 것인가?  
→ 결정: 요약+링크형으로 둔다.

Round 25: temporary spec의 validation plan은 contract delta와 얼마나 직접 연결될 것인가?  
→ 결정: 변경된 contract/invariant 항목과 ID 수준에서 직접 매핑한다.

Round 26: temporary spec에 `Risks / Open Questions` 섹션을 필수로 둘 것인가?  
→ 결정: 그렇다.

Round 27: temporary spec의 canonical section set은 어떤 형태로 고정할 것인가?  
→ 결정: 7섹션 압축형을 사용한다.

Round 28: delta 섹션에 invariant 변화는 어떻게 드러낼 것인가?  
→ 결정: `Contract Delta`로 숨기지 않고 `Contract/Invariant Delta`라는 이름으로 명시한다.

## Sources

- [docs/SDD_SPEC_DEFINITION.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_SPEC_DEFINITION.md)
- [docs/SDD_CONCEPT.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_CONCEPT.md)
- [docs/SDD_WORKFLOW.md](/Users/hyunjoonlee/github/sdd_skills/docs/SDD_WORKFLOW.md)
- [docs/sdd.md](/Users/hyunjoonlee/github/sdd_skills/docs/sdd.md)
- [discussion_spec_as_whitepaper.md](/Users/hyunjoonlee/github/sdd_skills/_sdd/discussion/discussion_spec_as_whitepaper.md)
- 사용자 입력 4라운드
