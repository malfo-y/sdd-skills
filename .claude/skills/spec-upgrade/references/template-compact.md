# SDD Spec Generation Template (Compact)

> Canonical generation template for SDD spec documents. All spec-related skills (spec-create, spec-upgrade, spec-rewrite) reference this template for consistent §1-§8 structure with What/Why/How triad enforcement.

---

## Writing Rules

> 아래 규칙은 모든 섹션에 적용된다.

**Document Metadata** — 스펙 상단에 포함:
- **Title**: 프로젝트 이름
- **Version**: X.Y.Z
- **Status**: Draft | In Review | Approved | Deprecated
- **Last Updated**: YYYY-MM-DD

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

## §1 Background & Motivation

*이 섹션에서는 프로젝트가 해결하는 문제, 이 접근법을 선택한 이유, 핵심 가치 제안을 서술한다.*

### Problem Statement [What]

[이 프로젝트가 해결하는 문제와 기존 상태의 고통점]

### Why This Approach [Why]

[대안 비교를 통해 이 접근법이 선택된 이유]

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| This project | ... | ... | **Chosen** |
| Alternative A | ... | ... | Rejected: ... |

### Core Value Proposition / Key Features / Target Users

[핵심 가치, 주요 기능, 대상 사용자를 간결하게 서술]

### Success Criteria / Non-Goals

- [ ] Criterion 1
- Non-goal 1

---

## §2 Core Design

*이 섹션에서는 프로젝트의 핵심 설계 아이디어와 알고리즘을 서사 형식으로 서술한다.*

### Key Idea [What]

[핵심 설계 아이디어를 내러티브 형식으로 서술. 어떤 문제를 만났고, 어떤 해결책을 고안했으며, 왜 작동하는지.]

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

## §3 Architecture Overview

*이 섹션에서는 시스템의 전체 구조를 다이어그램과 테이블로 제시한다.*

### System Diagram (ASCII)

```
[시스템 아키텍처 ASCII 다이어그램]
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| ... | ... | ... |

### Design Decisions

| Decision | Rationale | Alternatives |
|----------|-----------|-------------|
| ... | ... | ... |

---

## §4 Component Details

*이 섹션은 주요 컴포넌트마다 반복한다. 각 컴포넌트에 What/Why/How 트라이어드를 테이블 컬럼으로 강제한다.*

### [Component Name]

| Aspect | Description |
|--------|-------------|
| **Purpose** [What] | 이 컴포넌트가 하는 일 |
| **Why** | 이 컴포넌트가 존재하는 이유 — 산문체 (Writing Rules 참조) |
| **Input** | 입력 형식과 데이터 |
| **Output** | 출력 형식과 데이터 |
| **Dependencies** [Why] | 의존성과 이유: "X에 의존 — Y 때문" |
| **Source** | _(코드베이스 존재 시)_ `<path>`: Class, function() |

**Architecture Details [How]**:
- 구현 접근 방식과 선택 이유
- 핵심 클래스/함수
- 사용된 디자인 패턴

**How to Use**:
- API/인터페이스 예시
- 설정 옵션

**Known Issues**:
- 현재 제한사항과 개선 계획

---

## §5 Usage Guide & Expected Results

*이 섹션에서는 시나리오 기반 사용법과 기대 결과를 서술한다.*

### Scenario: [Name]

**Setup**: 전제 조건 및 준비 단계

**Action**: 사용자가 수행하는 작업

**Expected Result**: 관찰 가능한 결과 (구체적 값/동작 포함)

---

## §6 Data Models / API Reference (조건부)

*데이터 모델이나 API가 있는 경우에만 포함한다.*

### Data Models

[엔티티 정의, 제약 조건, 관계]

### API Reference

[엔드포인트, 요청/응답 스키마, 에러 코드]

---

## §7 Environment & Dependencies

*이 섹션에서는 프로젝트 실행 환경과 의존성을 서술한다.*

### Directory Structure

```
project/
├── src/
├── tests/
└── ...
```

### Dependencies

- Runtime / Development 의존성

### Configuration

- 환경 변수
- 설정 파일
- 필수 인증 정보

---

## §8 Identified Issues & Appendix

*이 섹션에서는 알려진 이슈와 코드 참조 인덱스를 정리한다.*

### Issues

- [ ] Critical bugs
- [ ] Code quality issues
- [ ] Missing features

### Appendix: Code Reference Index

| File | Functions / Classes | Referenced In |
|------|---------------------|---------------|
| `src/...` | function(), Class | §2, §4 |

---

## Modular Spec Guide

*프로젝트 규모에 따라 스펙 파일 구조를 결정한다.*

### Scale Criteria

| 규모 | 줄 수 | 구조 |
|------|-------|------|
| 소규모 | ~500줄 이하 | 단일 `main.md` |
| 중규모 | 500–1500줄 | `main.md` (인덱스) + `<component>.md` 파일 |
| 대규모 | 1500줄 초과 | `main.md` (인덱스) + `<component>/` 서브디렉토리 |

### 소규모 — 단일 파일

```
_sdd/spec/
└── main.md
```

### 중규모 — 인덱스 + 컴포넌트 파일

```
_sdd/spec/
├── main.md              # 인덱스: §1-§3 인라인, §4 컴포넌트 링크
├── api.md
├── database.md
└── frontend.md
```

### 대규모 — 인덱스 + 컴포넌트 서브디렉토리

```
_sdd/spec/
├── main.md              # 인덱스: §1-§3 인라인, §4 서브디렉토리 링크
├── api/
│   ├── overview.md
│   └── endpoints.md
└── database/
    ├── overview.md
    └── schema.md
```

### main.md 인덱스 형식

- §1-§3은 `main.md`에 인라인으로 유지
- §4 컴포넌트는 링크로 분리: `See [Component Name](./component.md)`
- §5-§8은 길이에 따라 인라인 또는 링크

### 서브 스펙 파일 형식

각 서브 스펙 파일도 동일한 What/Why/How 구조를 준수한다:
- 컴포넌트 레벨 Purpose/Why/How 테이블
- Architecture Details + 코드 발췌
- Source 필드 매핑
- 해당 컴포넌트의 Known Issues
