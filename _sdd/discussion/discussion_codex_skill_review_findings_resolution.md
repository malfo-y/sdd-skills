# Discussion: Codex Skill Review Findings Resolution

**Date**: 2026-04-04
**Topic**: `_sdd/spec/logs/skill_review_codex_sdd_pipeline_2026-04-04.md`의 findings에 대한 결정 정리
**Participants**: User, Codex

---

## Scope

이번 discussion의 목적은 Codex SDD skillchain에 대한 사용자 관점 리뷰에서 나온 핵심 findings를 decision backlog로 보고, 실제 운영 정책을 하나씩 확정하는 것이다.

대상 findings:

1. `_sdd/` path contract
2. `sdd-autopilot` top-level entrypoint 역할
3. ambiguity 처리 기본 정책
4. review artifact 언어 정책
5. skill/agent mirror 유지 방식

---

## Decisions

### 1. `_sdd/` path policy

**Decision**: `lowercase canonical`

앞으로 `_sdd/` artifact path는 lowercase를 canonical로 본다. 기존 uppercase artifact는 transition 대상이며, 점진적으로 정리한다.

의미:
- skillchain 설계 기준은 lowercase
- legacy uppercase artifact는 필요한 경우에만 fallback
- path drift는 이후 정리 대상

### 2. `sdd-autopilot` entrypoint policy

**Decision**: spec 부재 시에도 진행하는 `code-first fallback entrypoint`

사용자 의견:
> 스펙이 없으면 없는대로 코드만 보고 진행할 수 있지 않을까? 중간 결과 저장용으로 `_sdd` 디렉토리는 만들고. 그 다음 가능하면 스펙을 만들라고 사용자에게 권고.

정리:
- `sdd-autopilot`은 spec이 없어도 중단하지 않는다.
- `_sdd/` artifact workspace는 필요 시 부트스트랩한다.
- 코드를 기준으로 draft/plan/implementation/review를 진행할 수 있다.
- 종료 시 또는 적절한 지점에 `spec-create`를 권고한다.

즉 `sdd-autopilot`은 spec-ready repo 전용이 아니라, spec-less repo에서도 동작하는 최상위 entrypoint로 본다.

### 3. ambiguity policy

**Decision**: `One Extra Question`

원칙:
- 결과 품질이나 방향을 실질적으로 바꾸는 ambiguity면 질문 1회를 추가한다.
- 그 외 ambiguity는 best-effort로 진행한다.
- 불확실성은 artifact에 남긴다.

이 결정은 속도와 정확도의 균형을 위한 기준이다.

### 4. review artifact language policy

**Decision**: `User Language First`

원칙:
- review artifact는 현재 사용자 언어를 우선한다.
- 사용자 언어 신호가 약하면 기존 review 문서 언어를 fallback으로 사용한다.
- `implementation-review`의 한국어 고정 정책은 완화 대상이다.

### 5. skill/agent mirror maintenance policy

**Decision**: `Manual Sync`

현재는 skill/agent mirror를 생성 기반 또는 자동 audit 기반으로 바꾸지 않고, 사람이 함께 수정하는 방식으로 유지한다.

의미:
- mirror notice 유지 가능
- 수정 시 pair를 함께 건드리는 운영 discipline을 전제로 함
- 자동 검사나 one-source generation은 당장 채택하지 않음

---

## Tension Notes

### Manual Sync에 대한 caveat

이 결정은 현재 운영 단순성에는 유리하지만, 다시 drift가 생길 가능성은 남긴다.

특히 아래 상황에서 리스크가 있다.

- canonical model이 다시 바뀔 때
- docs/skills/agents를 한 번에 대규모로 수정할 때
- Codex/Claude parity sync가 동시에 필요할 때

즉, 이번 결정은 "manual sync를 유지하되 drift 비용을 감수한다"는 선택이다.

---

## Consolidated Outcome

이번 discussion으로 확정된 운영 방향은 아래와 같다.

- `_sdd/` 경로는 lowercase canonical
- `sdd-autopilot`은 spec-less repo에서도 작동하는 code-first fallback entrypoint
- ambiguity는 핵심 분기일 때만 질문 1회 추가
- review artifact는 user language first
- skill/agent mirror는 manual sync 유지

---

## Suggested Next Step

다음 작업은 위 결정을 실제 skill/agent/docs surface에 반영하는 patch planning이다.

우선순위 권장:

1. `_sdd/` path canonicalization
2. `sdd-autopilot` spec-less fallback 설계
3. ambiguity threshold 규칙 반영
4. `implementation-review` 언어 정책 완화
5. mirror manual-sync caveat를 문서화
