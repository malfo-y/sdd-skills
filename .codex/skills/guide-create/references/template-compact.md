# SDD Guide Generation Template (Compact)

> Canonical generation template for SDD guide documents. guide-create skill references this template for consistent §1-§5 structure with What/Why/How triad enforcement. Guide는 프로젝트 전체가 아닌 단일 기능 deep-dive이므로, spec의 §1-§8을 그대로 쓰지 않고 guide 고유 §1-§5 구조를 사용하되 § numbering과 Writing Rules를 공유한다.

---

## Writing Rules

> 아래 규칙은 모든 섹션에 적용된다. spec-create의 Writing Rules와 동일한 규칙을 공유한다.

**Document Metadata** — 가이드 상단에 포함:
- **Title**: 기능 기술 보고서: <feature name>
- **Version**: X.Y.Z
- **Status**: Draft | In Review | Approved | Deprecated
- **Last Updated**: YYYY-MM-DD
- **Input Source**: conversation / spec / code / mixed
- **Target Feature**: <feature name>
- **Confidence**: High / Medium / Low

**Code Excerpt Rules**:
- ≤30줄 함수 → 전문(full body) 발췌
- >30줄 함수 → 시그니처 + 핵심 로직만
- 코드 블록 시작에 `# [filepath:functionName]` 헤더 부착

**Inline Citation**:
- 본문에서 코드 참조 시 `[filepath:functionName]` 형식 사용
- 예: "검증 단계 `[src/validator.py:validate]`에서 데이터 무결성을 확인한다."

**What/Why/How Triad** — 컴포넌트, 설계 결정, 의존성에 필수:
- **What**: 무엇을 하는가 (Purpose, description)
- **Why**: 왜 이렇게 하는가 (Rationale, alternatives considered)
- **How**: 어떻게 구현하는가 (Implementation approach, code references)

**Source Field**:
- 형식: `<path>`: ClassName, function_name()
- 코드베이스가 존재할 때만 포함. 그린필드 프로젝트는 생략.

**Component Why Style**:
- 자연스러운 산문체로 작성: "인증 로직을 API 레이어에서 분리하여 독립 테스트와 재사용이 가능하도록 했다"
- 레이블 패턴 금지: "~의 이유: ..." 형태 사용 금지

---

## Section-to-Spec Mapping

| Guide | Spec | 비고 |
|-------|------|------|
| §1 Background & Motivation | spec §1 | 직접 대응 |
| §2 Core Design | spec §2 | 직접 대응 |
| §3 Usage Scenario Guide | spec §5 확장 | guide 특화 |
| §4 API Reference | spec §6 확장 | guide 특화 |
| §5 Implementation Guide | guide 고유 | 체크리스트/안티패턴 |
| Appendix | spec §8 패턴 | 동일 패턴 |

---

## §1 Background & Motivation

*이 섹션에서는 기능이 해결하는 문제, 이 접근법을 선택한 이유를 서술한다.*

### Problem Statement [What]

[이 기능이 해결하는 문제와 사용자/시스템 관점의 고통점]

### Why This Approach [Why]

[대안 비교를 통해 이 접근법이 선택된 이유. 스펙에서 확인 가능한 경우 명시.]

### Core Value

[핵심 가치와 기능의 동기/맥락]

---

## §2 Core Design

*이 섹션에서는 기능의 핵심 설계 아이디어와 알고리즘을 서사 형식으로 서술한다.*

### Key Idea [What]

[핵심 설계 아이디어를 내러티브 형식으로 서술]

### Algorithm / Logic Flow [How]

[주요 알고리즘 또는 처리 흐름. 실제 코드 발췌를 포함한다.]

```python
# [src/core/processor.py:process_data]
def process_data(input):
    validated = validate(input)
    return transform(validated)
```

> 30줄 규칙 적용: ≤30줄 함수는 전문, >30줄 함수는 시그니처+핵심 로직만 발췌.

### Design Rationale [Why]

| Choice | Rationale | Alternatives |
|--------|-----------|-------------|
| ... | Why chosen | What else considered |

---

## §3 Usage Scenario Guide

*이 섹션이 가이드의 핵심이다. 가능한 한 구체적이고 자세하게 작성한다.*

### Scenario: [Name]

**전제 조건**: 이 시나리오가 성립하는 초기 상태

**입력**: 구체적 데이터 예시 포함

**처리 흐름**: 단계별 동작 설명. 각 단계에서 호출되는 함수/메서드를 인라인 citation으로 참조.
- 예: "`[src/payments/payment_service.ts:confirmPayment]`에서 상태를 검증한다"

**기대 결과**: 성공/실패 시 예상 출력

> 최소 요구사항: 정상 시나리오 1개 + 예외/에러 시나리오 1개 이상.
> 권장 시나리오 유형: 기본 정상 흐름, 엣지 케이스, 에러/실패, 동시성/멱등성.

---

## §4 API Reference

*이 섹션은 개별 인터페이스별 reference로 작성한다. 가능한 한 구체적이고 자세하게 작성한다.*

### [Endpoint / Function / Interface]

**구현 소스**: `[filepath:handler/service]` (인라인 citation)

**시그니처**: 엔드포인트 URL, 함수 시그니처, 또는 인터페이스 정의

**파라미터**:

| 이름 | 타입 | 필수/선택 | 설명 |
|------|------|----------|------|
| ... | ... | ... | ... |

**리턴값/응답**: 성공 응답 구조와 필드 설명

**에러 코드**: 에러 상황별 코드/메시지

| HTTP 상태 | 에러 코드 | 상황 |
|-----------|----------|------|
| ... | ... | ... |

**코드 예시**: 요청/응답 JSON 또는 함수 호출 예시

> API가 없는 기능(내부 로직, UI 컴포넌트 등)인 경우 함수/메서드 인터페이스를 동일 구조로 문서화.

---

## §5 Implementation Guide

*이 섹션에서는 핵심 구현 규칙, 체크리스트, 안티패턴을 서술한다.*

### Key Rules

[구현 시 반드시 지켜야 할 규칙과 제약]
- 상태 변화 규칙
- 에러 처리 규칙
- 데이터 검증/저장 규칙

### Checklist

**구현 전**:
- [ ] ...

**구현 중**:
- [ ] ...

**완료/리뷰 전**:
- [ ] ...

### Anti-patterns

[피해야 할 구현 방식을 근거와 함께 기술]

---

## Appendix (Optional)

### 관련 스펙 레퍼런스

- 파일 경로 + 섹션명: `_sdd/spec/xxx.md` → `섹션명`

### 관련 코드 레퍼런스

- 파일 경로 + 심볼: `src/xxx.ts` → `functionName`

### 가정 및 미확정 사항

- 근거가 부족한 부분을 숨기지 말고 명시
