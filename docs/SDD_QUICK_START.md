# SDD 빠른 시작 가이드

이 문서는 현재 SDD canonical model을 빠르게 시작하기 위한 최소 안내다.

관련 문서:
- [SDD_SPEC_DEFINITION.md](SDD_SPEC_DEFINITION.md)
- [SDD_CONCEPT.md](SDD_CONCEPT.md)
- [SDD_WORKFLOW.md](SDD_WORKFLOW.md)

---

## 1. 먼저 기억할 4가지

1. 글로벌 스펙은 얇은 기준 문서다.
2. temporary spec은 변경 실행 청사진이다.
3. `Contract / Invariants / Verifiability`는 공통 품질 게이트다.
4. canonical model 변경 시 순서는 `definition -> skills -> docs -> mirrors/examples`다.

---

## 2. 시작점 고르기

| 상황 | 시작 스킬 |
|------|-----------|
| 대부분의 기능 구현 | `/sdd-autopilot` |
| 요구사항/방향이 모호함 | `/discussion` |
| 스펙이 없음 | `/spec-create` |
| legacy spec을 현재 모델로 옮겨야 함 | `/spec-upgrade` |
| 현재 spec 상태를 빠르게 보고 싶음 | `/spec-summary` |

---

## 3. 글로벌 스펙과 temporary spec

### 글로벌 스펙

글로벌 스펙은 다음 축을 가진다.

- 배경 및 high-level concept
- Scope / Non-goals / Guardrails
- 핵심 설계와 주요 결정
- Contract / Invariants / Verifiability
- 사용 가이드 & 기대 결과
- Decision-bearing structure

필요할 때만 보조 영역을 추가한다.

- 데이터 모델 / API / 환경 및 설정
- Strategic Code Map appendix

### Temporary Spec

temporary spec은 아래 7섹션을 사용한다.

- Change Summary
- Scope Delta
- Contract/Invariant Delta
- Touchpoints
- Implementation Plan
- Validation Plan
- Risks / Open Questions

---

## 4. 가장 흔한 경로

### 기본 경로

```bash
/sdd-autopilot 이 기능 구현해줘: [기능 설명]
```

### 수동 경로

대규모:

```text
feature-draft -> spec-update-todo -> implementation-plan -> implementation -> implementation-review -> spec-update-done
```

중규모:

```text
feature-draft -> implementation -> spec-update-done
```

소규모:

```text
직접 구현 -> 필요 시 implementation-review / spec-update-done
```

---

## 5. 좋은 입력

최소한 아래 세 가지는 같이 준다.

- What: 무엇을 바꾸는가
- Why: 왜 필요한가
- Constraints: 어떤 제약이 있는가

예시:

```text
/feature-draft
사용자가 CSV를 업로드하면 자동 파싱 후 users 테이블에 bulk insert.
- 최대 10MB
- 컬럼 매핑은 UI에서 수동 지정
- 에러 행은 건너뛰고 리포트 생성
```

---

## 6. 어디를 보면 되나

- 스펙의 정의: [SDD_SPEC_DEFINITION.md](SDD_SPEC_DEFINITION.md)
- 두 단계 구조: [SDD_CONCEPT.md](SDD_CONCEPT.md)
- 전체 워크플로우: [SDD_WORKFLOW.md](SDD_WORKFLOW.md)
- 철학과 운영 모델: [sdd.md](sdd.md)
