# Discussion Summary: Global Spec Reduction

**Date**: 2026-04-04
**Rounds**: 6
**Topic**: global spec을 더 과감하게 줄일지, 줄인다면 무엇을 global에서 내리고 feature-level surface나 README로 보낼지
**Language**: Korean

## 핵심 논점

1. global spec이 여전히 LLM과 사람의 공동 계약 문서여야 하는가, 아니면 상위 결정 메모로 더 얇아져야 하는가
2. `Contract / Invariants / Verifiability`를 global core에 둘지, feature-level 또는 temporary surface로 내려야 하는가
3. `usage-guide`, `expected results`, `reference information`을 `_sdd/spec/`에 둘지 README, docs, feature-level 문서로 옮길지
4. global에서 내려낸 feature-level 정보를 영속적으로 어디에 둘지
5. `spec-review`, `spec-summary` 같은 consumer가 global spec만 읽어도 되는지

## 결정 사항

1. **global spec은 더 얇은 `결정 메모`로 간다.**
   - 배경, scope, guardrails, 핵심 결정, decision-bearing structure 중심으로 남긴다.

2. **global spec의 CIV는 repo-wide invariant만 예외적으로 남긴다.**
   - feature-level contract, expected result, validation linkage는 global core에서 기본 제거 대상이다.

3. **usage / expected results / supporting reference는 `_sdd/spec/`보다 README나 feature-level surface가 더 적합하다.**
   - global spec에 repo-wide expected results는 별도로 둘 필요가 없다는 방향으로 정리했다.

4. **persistent feature spec layer를 새로 만들지 않는다.**
   - 필요할 때만 `guide-create`로 feature-level 문서를 생성한다.
   - 즉, `_sdd/guides/`는 상시 mandatory layer가 아니라 on-demand companion surface다.

5. **consumer는 global spec만 본다.**
   - `spec-review`, `spec-summary` 등은 global spec을 기준으로 판단한다.
   - feature-level guide는 필요할 때만 사람이 요청해서 생성/참조하는 부가 surface로 본다.

## 미결 질문

- `guide-create`라는 이름을 유지할지, 더 직접적인 이름으로 바꿀지는 아직 결정하지 않았다.
- global spec을 실제로 더 줄일 때, 현재 남아 있는 repo-wide invariant 중 어떤 항목까지 global에 남길지 구체적 pruning 기준은 별도 설계가 필요하다.

## 실행 항목

1. global spec diet를 실제 변경으로 옮기려면, 별도 follow-up discussion 또는 draft에서 "global에 남길 최소 항목 목록"을 먼저 고정한다.
2. 이후 변경을 진행한다면 `main.md` 중심 global spec 축소와 `components.md`/`usage-guide.md`의 추가 축소 또는 제거를 검토한다.
3. `guide-create`를 on-demand feature surface로 계속 쓸지, 이름과 contract를 재정의할지는 후속 논의로 분리한다.

## 리서치 결과 요약

- [docs/SDD_SPEC_DEFINITION.md](../../docs/SDD_SPEC_DEFINITION.md)는 현재 canonical model에서 global spec core에 `Contract / Invariants / Verifiability`, `사용 가이드 & 기대 결과`, `참조 정보`를 포함시키고 있다.
- [docs/SDD_CONCEPT.md](../../docs/SDD_CONCEPT.md)는 global spec을 장기 기준 문서, temporary spec을 실행 청사진으로 정의하고 있어, 현재 모델은 feature-level 지속 문서를 별도 mandatory layer로 두지 않는다.
- [main.md](../spec/main.md)는 이미 thin global spec 쪽으로 이동했지만, 여전히 CIV, usage 기준, reference surface를 global spec 안에 유지하고 있다.
- 저장소에는 `_sdd/spec/features/` 같은 persistent feature spec layer가 없고, `_sdd/guides/`는 `guide-create`가 만드는 optional companion document로만 정의돼 있다.

## Sources

- `docs/SDD_SPEC_DEFINITION.md`
- `docs/SDD_CONCEPT.md`
- `_sdd/spec/main.md`
- `.codex/skills/discussion/references/discussion-question-guide.md`
- `.codex/skills/guide-create/SKILL.md`
- `_sdd/spec/components.md`

## 토론 흐름

### Round 1
- 질문: global spec의 기본 역할을 `결정 메모`로 볼지, `공동 계약 문서`로 볼지
- 응답: `결정 메모`

### Round 2
- 질문: global spec의 CIV를 어디까지 남길지
- 응답: `전역 불변식만 유지`

### Round 3
- 질문: supporting surface를 `_sdd/spec/`에 둘지, README/feature 쪽으로 보낼지
- 응답: `README/feature로 이관`

### Round 4
- 질문: 논의를 어디까지 이어갈지
- 응답: `feature spec 정의`

### Round 5
- 질문: 내려낸 내용을 어디에 영속적으로 둘지
- 응답: `guide 승격`

### Round 6
- 질문: 여기서 정리할지, 후속 설계를 더 논의할지
- 응답: 자유 입력으로 보정
  - feature-level 문서는 사용자가 요구할 때만 `guide-create`로 생성
  - `spec-review`, `spec-summary` 등은 global spec만 고려
  - global spec에 repo-wide expected results는 필요 없음

## 결론

이번 토론의 결론은 분명하다.

> global spec은 현재 canonical model보다 더 얇은 상위 결정 메모로 줄이고, feature-level usage/contract/expected result는 global 기본 책임에서 내린다. 다만 그 정보는 상시 persistent feature spec layer를 새로 만드는 대신, 필요할 때 `guide-create`로 생성하는 on-demand companion surface로 다룬다.
