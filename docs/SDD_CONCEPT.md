# SDD 핵심 컨셉: 글로벌 스펙과 Temporary Spec

이 문서는 SDD의 두 단계 스펙 구조를 설명한다. 핵심은 문서 수를 늘리는 것이 아니라, 장기 기준과 변경 청사진을 분리하는 것이다.

관련 문서:
- [SDD_SPEC_DEFINITION.md](SDD_SPEC_DEFINITION.md)
- [SDD_WORKFLOW.md](SDD_WORKFLOW.md)
- [sdd.md](sdd.md)

---

## 1. 글로벌 스펙은 무엇인가

글로벌 스펙은 프로젝트의 Single Source of Truth다. 하지만 예전처럼 모든 구현 상세를 전수 기록하는 inventory 문서는 아니다.

글로벌 스펙의 역할:
- 프로젝트의 문제와 high-level concept를 고정한다.
- scope, non-goals, guardrails를 고정한다.
- 핵심 설계와 주요 결정을 고정한다.
- `Contract / Invariants / Verifiability`를 통해 검증 가능한 약속을 남긴다.
- decision-bearing structure와 전략적 code navigation hint를 남긴다.

즉, 글로벌 스펙은 "코드에 뭐가 어디 있는지 전부 적는 문서"가 아니라, 사람과 AI가 같은 경계와 계약으로 판단하게 만드는 기준 문서다.

### 글로벌 스펙에 남길 것과 남기지 않을 것

| 남길 것 | 기본 본문에서 강제하지 않을 것 |
|--------|-----------------------------|
| high-level concept | 전체 implementation inventory |
| scope / non-goals / guardrails | 컴포넌트 전수 설명 |
| key decisions | 코드 그대로 옮겨 적은 매뉴얼 |
| CIV | local implementation detail |
| decision-bearing structure | 탐색 가치가 낮은 파일 목록 |

---

## 2. Temporary Spec은 무엇인가

temporary spec은 글로벌 스펙의 요약본이 아니다. 변경을 구현하기 위한 실행 청사진이다.

temporary spec의 canonical 7섹션:
- Change Summary
- Scope Delta
- Contract/Invariant Delta
- Touchpoints
- Implementation Plan
- Validation Plan
- Risks / Open Questions

temporary spec의 역할:
- 이번 변경의 범위를 글로벌 스펙과 구분해서 고정한다.
- 바뀌는 contract와 invariant를 명시한다.
- 실제 코드 접점과 구현 순서를 드러낸다.
- 검증 계획을 delta ID와 연결한다.

따라서 temporary spec은 "나중에 병합될 문서 조각"이 아니라, 구현과 검증을 이끄는 작업 청사진이다.

---

## 3. 두 문서는 왜 비대칭인가

사람과 AI는 같은 문서를 읽어도 필요한 정보 밀도가 다르다.

- 사람은 개념, 배경, scope, non-goals, guardrails를 먼저 이해해야 한다.
- AI는 필요한 순간 코드 탐색을 빠르게 할 수 있으므로, 장기 문서에 모든 구현 해설을 적어 둘 필요가 없다.
- 대신 AI에게도 contract, invariant, verification, strategic code map 같은 고신호 정보는 지속적으로 가치가 있다.

그래서 SDD는 다음 비대칭을 채택한다.

- 글로벌 스펙: 얇고 지속적인 기준 문서
- temporary spec: delta와 execution 중심의 직접적인 청사진

---

## 4. 생명주기

### 중규모 경로

```text
feature-draft -> implementation -> spec-update-done
```

- `feature-draft`가 temporary spec과 구현 계획을 함께 만든다.
- 구현 후 `spec-update-done`이 persistent truth만 글로벌 스펙에 반영한다.

### 대규모 경로

```text
feature-draft -> spec-update-todo -> implementation-plan -> implementation -> implementation-review -> spec-update-done
```

- 장기 작업에서는 `spec-update-todo`로 planned persistent information을 먼저 글로벌 스펙에 반영할 수 있다.
- `implementation-plan`은 delta와 validation linkage를 phase/task 수준으로 풀어 준다.
- `implementation-review`는 plan 대비 구현과 acceptance criteria를 검증한다.

---

## 5. 아티팩트 구분

### 지속 문서

| 위치 | 역할 |
|------|------|
| `_sdd/spec/` | 글로벌 스펙과 supporting spec |
| `_sdd/env.md` | 환경과 검증 힌트 |
| `_sdd/spec/decision_log.md` | 주요 결정 기록 |

### 실행 중간 산출물

| 위치 | 역할 |
|------|------|
| `_sdd/drafts/` | temporary spec draft |
| `_sdd/implementation/` | 구현 계획, 진행 상황, 구현 리포트, 구현 리뷰 |
| `_sdd/discussion/` | 논의 handoff |
| `_sdd/guides/` | 기능별 guide |

운영 원칙:
- 글로벌 스펙은 ad-hoc 수정보다 skillchain을 통한 sync를 기본으로 한다.
- temporary spec과 계획 문서는 실행이 끝나면 아카이브되거나 후속 단계 입력으로 흡수된다.

---

## 6. 요약

한 문장으로 요약하면 이렇다.

> 글로벌 스펙은 장기 기준을 고정하고, temporary spec은 이번 변경의 실행 청사진을 고정한다.

이 비대칭 구조 덕분에 SDD는 문서를 두껍게 만드는 대신, 기준과 실행을 분리해서 drift를 줄인다.
