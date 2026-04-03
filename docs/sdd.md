# Spec-Driven Development (SDD)

AI agent 시대의 개발은 "코드를 더 빨리 쓰는 것"만으로는 안정해지지 않는다. 중요한 것은 사람과 에이전트가 같은 기준으로 판단하도록 만드는 것이다. SDD는 그 기준을 spec으로 고정한다.

관련 문서:
- [SDD_SPEC_DEFINITION.md](SDD_SPEC_DEFINITION.md)
- [SDD_CONCEPT.md](SDD_CONCEPT.md)
- [SDD_WORKFLOW.md](SDD_WORKFLOW.md)

---

## 1. 왜 SDD인가

AI agent와 함께 개발할 때 반복되는 문제는 대체로 세 가지다.

### 해석의 표류

같은 요구를 여러 번 던지면 구현 결정이 흔들린다. 누가 구현하느냐, 어느 날 구현하느냐에 따라 결과가 달라진다.

### 컨텍스트 압축 실패

코드베이스가 커질수록 에이전트는 기존 패턴, 제약, 중요한 경계를 놓치기 쉽다. 이미 있는 구조를 무시하고 중복 구현을 만들기도 한다.

### 환각과 거짓 계약

존재하지 않는 API, 잘못된 입출력, 애매한 실패 보장을 "그럴듯하게" 만들어 낸다. 코드가 있어 보여도 계약이 틀리면 시스템은 흔들린다.

SDD는 이 문제를 "프롬프트를 더 잘 쓰자"로 해결하지 않는다. 기준과 계약을 spec으로 외부화해 drift를 줄인다.

---

## 2. SDD에서 spec은 무엇을 고정하는가

SDD의 spec은 단순 문서가 아니라 제어면(control plane)이다. 특히 아래 항목을 고정한다.

- high-level concept
- scope / non-goals / guardrails
- 핵심 설계와 주요 결정
- Contract / Invariants / Verifiability
- expected results
- decision-bearing structure

여기서 중요한 점은 "모든 구현 상세"를 문서화하는 것이 아니라, 다음 판단에 계속 필요한 정보만 남긴다는 것이다.

---

## 3. CIV가 중요한 이유

`Contract / Invariants / Verifiability`는 SDD의 핵심 품질 게이트다.

### Contract

무엇을 입력으로 받고 무엇을 출력하는지, 어떤 전제조건과 사후조건이 있는지, 실패 시 무엇을 보장하는지를 명시한다.

### Invariants

다음 변경에서도 깨지면 안 되는 시스템/도메인 규칙을 남긴다.

### Verifiability

각 contract와 invariant를 무엇으로 검증할지 연결한다. 중요한 것은 추상적 구호가 아니라, 실제 검증 경로가 명시되어야 한다는 점이다.

이 구조 덕분에 리뷰 질문이 "그럴듯한가?"에서 "계약을 지키는가?"로 바뀐다.

---

## 4. 사람과 LLM이 같은 문서를 다르게 읽는 이유

사람은 먼저 문맥을 이해해야 한다.

- 왜 이 프로젝트가 존재하는가
- 어디까지가 책임 범위인가
- 무엇을 하지 않는가
- 어떤 결정은 건드리면 안 되는가

반면 LLM은 코드를 빠르게 탐색할 수 있다. 그래서 장기 문서에 구현 inventory를 전부 적어 두는 것은 비용 대비 가치가 낮다.

그래서 SDD의 글로벌 스펙은 다음 성격을 가진다.

- 사람에게는 방향과 경계를 주는 문서
- AI에게는 추측을 줄이기 위한 계약과 탐색 힌트를 주는 문서

이때 전략적 code map은 전체 파일 목록이 아니라 entrypoint, invariant hotspot, extension point, change hotspot 같은 고신호 힌트만 남긴다.

---

## 5. 글로벌 스펙과 Temporary Spec

### 글로벌 스펙

글로벌 스펙은 얇은 기준 문서다.

- 배경 및 high-level concept
- Scope / Non-goals / Guardrails
- 핵심 설계와 주요 결정
- Contract / Invariants / Verifiability
- 사용 가이드 & 기대 결과
- Decision-bearing structure

필요할 때만 참조 정보와 appendix를 붙인다.

### Temporary Spec

temporary spec은 변경 실행 청사진이다.

- Change Summary
- Scope Delta
- Contract/Invariant Delta
- Touchpoints
- Implementation Plan
- Validation Plan
- Risks / Open Questions

이 두 문서는 공통 코어를 공유하지만, 정보 밀도와 역할은 의도적으로 다르다.

---

## 6. 운영 루프

SDD의 기본 루프는 아래처럼 돌아간다.

```text
requirements -> temporary spec / plan -> implementation -> verification -> global spec sync
```

규모가 크면:

```text
feature-draft -> spec-update-todo -> implementation-plan -> implementation -> implementation-review -> spec-update-done
```

규모가 중간이면:

```text
feature-draft -> implementation -> spec-update-done
```

대부분의 실전에서는 `/sdd-autopilot`이 이 흐름을 자동으로 조합한다.

---

## 7. 도입 원칙

SDD를 도입할 때 핵심은 "문서를 많이 쓰자"가 아니다.

- 글로벌 스펙을 얇게 유지한다.
- CIV를 명시적으로 복구한다.
- temporary spec을 실행 청사진으로 다룬다.
- skill behavior와 docs를 분리하지 않는다.
- definition 변경 시 `definition -> skills -> docs -> mirrors/examples` 순서를 지킨다.

즉, SDD는 문서 양을 늘리는 방법론이 아니라, 사람과 AI가 같은 계약 아래에서 반복적으로 일하게 만드는 운영 모델이다.
