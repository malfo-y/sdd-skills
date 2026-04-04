# Discussion Summary: Global Definition and Codex Skill Diet

**Date**: 2026-04-04
**Rounds**: 7
**Topic**: `docs/SDD_SPEC_DEFINITION.md`를 더 얇은 global spec 모델로 재정의하고, 현재 Codex skill들을 그 기준에 맞게 어떻게 업데이트할지
**Language**: Korean

## 핵심 논점

1. 이번 변경의 대상은 현재 repo의 active global spec이 아니라, `docs/SDD_SPEC_DEFINITION.md`와 이를 소비하는 Codex skillchain인가
2. 새 definition에서 global spec의 mandatory core를 어디까지로 줄일 것인가
3. `Contract / Invariants / Verifiability`, `사용 가이드 & 기대 결과`, `참조 정보`, `Strategic Code Map`을 global mandatory core에서 내릴 것인가
4. repo-wide invariant는 완전히 제거할지, 남긴다면 어떤 형태로 남길지
5. 새 definition이 Codex skill에 미치는 영향은 어떤 순서로 잠그는 것이 안전한가

## 결정 사항

1. **이번 논의의 대상은 `docs/SDD_SPEC_DEFINITION.md`와 Codex skillchain이다.**
   - 당장 `_sdd/spec/main.md`를 다시 줄이는 작업을 논의하는 것이 아니다.

2. **새 global mandatory core는 더 얇게 간다.**
   - 남길 것: 배경 및 high-level concept, scope / non-goals / guardrails, 핵심 설계와 주요 결정
   - current canonical model보다 훨씬 더 얇은 decision memo 성격으로 간다.

3. **global mandatory core에서 다음을 뺀다.**
   - `사용 가이드 & 기대 결과`
   - `참조 정보`
   - `Strategic Code Map`
   - 현재 형태의 `Contract / Invariants / Verifiability`

4. **repo-wide invariant가 필요하면 별도 CIV 표가 아니라 guardrails에 흡수한다.**
   - 즉, feature-level CIV를 global에 두지 않고
   - 정말 필요한 repo-level operating invariant만 guardrails나 key decisions 문장으로 남긴다.

5. **Codex skill 영향도 논의는 consumer를 먼저 잠근다.**
   - `spec-review`, `spec-summary`, `spec-rewrite`가 새 global minimum을 어떻게 읽을지 먼저 고정한다.
   - 그 다음 generator/transformer와 planner/update/orchestrator 계열을 맞추는 편이 drift가 적다.

## 내 의견

1. 이 방향은 타당하다.
   - global spec을 “공동 계약 문서”에서 “상위 결정 메모”로 더 줄이려는 목적과 일관된다.

2. 다만 repo-wide invariant를 완전 제거하는 것은 반대다.
   - LLM이 코드만 보고도 재구성하기 어려운 repo-level operating rule은 남겨야 한다.
   - 하지만 그것을 현재처럼 독립 CIV 표로 둘 필요는 없다.

3. 그래서 가장 안정적인 목표 형태는 아래와 같다.
   - global spec = 배경/개념 + 경계 + 핵심 결정 + 아주 얇은 guardrail
   - feature-level usage/contract/validation = global 밖
   - consumer skill = global spec에는 그 이상을 기대하지 않음

## 미결 질문

1. `spec-review`는 global spec에서 무엇이 빠져 있어도 정상으로 볼 것인가
2. `spec-summary`는 새 global minimum을 어떤 outline으로 요약할 것인가
3. `spec-rewrite`는 “too heavy”와 “good thin global spec”을 어떤 rubric으로 판정할 것인가
4. planner/update 계열 (`feature-draft`, `implementation-plan`, `spec-update-*`, `sdd-autopilot`)이 feature-level usage/CIV를 temporary spec만으로 처리할지, 필요 시 guide 생성까지 contract에 포함할지

## 실행 항목

1. `docs/SDD_SPEC_DEFINITION.md`를 새 global minimum 기준으로 재작성한다.
2. Codex consumer skill 3종을 우선 업데이트한다.
   - `.codex/skills/spec-review/SKILL.md`
   - `.codex/skills/spec-summary/SKILL.md`
   - `.codex/skills/spec-rewrite/SKILL.md`
3. 그 다음 Codex generator/transformer를 맞춘다.
   - `.codex/skills/spec-create/`
   - `.codex/skills/spec-upgrade/`
4. 마지막으로 planner/update/orchestrator 계열 read/write contract를 맞춘다.
   - `.codex/skills/feature-draft/`
   - `.codex/skills/implementation-plan/`
   - `.codex/skills/spec-update-todo/`
   - `.codex/skills/spec-update-done/`
   - `.codex/skills/sdd-autopilot/`

## 리서치 결과 요약

- [docs/SDD_SPEC_DEFINITION.md](../../docs/SDD_SPEC_DEFINITION.md)는 현재 global spec core에 `Contract / Invariants / Verifiability`, `사용 가이드 & 기대 결과`, `참조 정보`, `Strategic Code Map`을 포함시키는 모델이다.
- [docs/SDD_CONCEPT.md](../../docs/SDD_CONCEPT.md)는 global/temporary two-level model을 설명하지만, 지금 논의하는 더 공격적인 global diet는 아직 반영하지 않는다.
- [main.md](../spec/main.md)는 이미 thin global spec 쪽으로 이동했지만, 현재 definition보다는 좁고 이번 논의 목표보다는 아직 넓다.
- 로컬 구조상 Codex skillchain은 consumer, generator/transformer, planner/update/orchestrator로 나누어 읽기/쓰기 계약을 재설계할 수 있다.

## Sources

- `docs/SDD_SPEC_DEFINITION.md`
- `docs/SDD_CONCEPT.md`
- `_sdd/spec/main.md`
- `.codex/skills/discussion/references/discussion-question-guide.md`
- `.codex/skills/spec-review/SKILL.md`
- `.codex/skills/spec-summary/SKILL.md`
- `.codex/skills/spec-rewrite/SKILL.md`
- `.codex/skills/spec-create/SKILL.md`
- `.codex/skills/spec-upgrade/SKILL.md`

## 토론 흐름

### Round 1
- 질문: 새 기준에서 가장 먼저 고정할 축은 무엇인가
- 응답: global 최소 코어

### Round 2
- 질문: global mandatory core를 어디까지로 볼 것인가
- 응답: 배경+경계+결정+전역 불변식

### Round 3
- 질문: global mandatory core에서 우선 뺄 것은 무엇인가
- 응답: usage/reference뿐 아니라 CIV도 같이 내림

### Round 4
- 질문: repo-wide invariant는 어떤 형태로 남길 것인가
- 응답: guardrails에 흡수

### Round 5
- 질문: 다음으로 어디까지 논의할 것인가
- 응답: Codex 스킬 영향도

### Round 6
- 질문: 어떤 skill family부터 잠글 것인가
- 응답: consumer 먼저

### Round 7
- 질문: 여기서 정리할지, consumer 상세를 더 팔지
- 응답: 여기서 정리

## 결론

> `docs/SDD_SPEC_DEFINITION.md`의 global spec 정의는 지금보다 더 얇아져야 한다. 새 global mandatory core는 배경/개념, 경계, 핵심 결정 중심으로 축소하고, usage/reference/current-form CIV는 global core에서 내린다. repo-wide invariant가 필요하면 별도 CIV 표가 아니라 guardrails 안에 흡수한다. Codex skillchain 개편은 consumer 계열부터 잠그는 것이 가장 안전하다.
