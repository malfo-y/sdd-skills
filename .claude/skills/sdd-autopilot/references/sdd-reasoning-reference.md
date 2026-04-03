# SDD Reasoning Reference

## Part 1: SDD 철학

### 1.1 핵심 원칙

1. **Spec is Source of Truth**: 코드는 결과물이고, global spec은 장기적 의도를 고정한다.
2. **Global spec과 temporary spec은 역할이 다르다**: global spec은 지속 정보, temporary spec은 실행 청사진이다.
3. **검증 기준도 spec에 둔다**: 리뷰/테스트의 질문이 "그럴듯한가?"가 아니라 "계약과 invariant를 지키는가?"가 되도록 만든다.

운영 대원칙: **AI가 만든 spec도 사람 승인 없이는 확정하지 않는다.**

### 1.2 사람과 LLM이 spec에서 필요로 하는 것

- 사람은 high-level concept, scope, non-goals, guardrails, key decisions가 먼저 필요하다.
- LLM은 코드를 빠르게 탐색할 수 있으므로 구현 inventory보다 전략적 navigation hint가 더 유용하다.
- 따라서 global spec은 두꺼운 구현 해설서가 아니라 얇은 constitutional document여야 한다.
- 상세 implementation inventory는 코드와 on-demand analysis에 맡기고, spec에는 decision-bearing structure만 남긴다.

### 1.3 핵심 용어

| 용어 | 의미 |
|------|------|
| **Global Spec** | 장기적 SoT. 문제 framing, scope, CIV, key decisions, decision-bearing structure를 유지하는 문서 |
| **Temporary Spec** | 변경 하나를 실행하기 위한 청사진. delta, touchpoints, plan, validation을 담는 문서 |
| **CIV** | `Contract / Invariants / Verifiability`. global spec의 필수 섹션 |
| **Decision-Bearing Structure** | 시스템 경계, ownership, cross-component contract, extension point, invariant hotspot |
| **Strategic Code Map** | appendix-level manual curated navigation hint. entrypoint, invariant hotspot, extension point, change hotspot 위주 |

### 1.4 Global Spec Canonical Shape

global spec core는 아래 순서를 유지한다.

1. `배경 및 high-level concept`
2. `Scope / Non-goals / Guardrails`
3. `핵심 설계와 주요 결정`
4. `Contract / Invariants / Verifiability`
5. `사용 가이드 & 기대 결과`
6. `Decision-bearing structure`

선택 섹션:

- `참조 정보`
- `Appendix A. Strategic Code Map`
- `Appendix B. Related Docs & Code References`

global spec 규칙:

- scope는 key feature 목록만이 아니라 책임 범위와 out-of-scope를 함께 고정한다.
- CIV는 필수다.
- strategic code map은 appendix-level manual curated hint다.
- architecture/component inventory를 본문 필수로 강제하지 않는다.

### 1.5 CIV 규칙

`Contract / Invariants / Verifiability`는 global spec의 독립 필수 섹션이다.

```markdown
### Contract
| ID | Subject | Inputs/Outputs | Preconditions | Postconditions | Failure Guarantees |

### Invariants
| ID | Scope | Invariant | Why It Matters |

### Verifiability
| ID | Targets | Verification Method | Evidence / Notes |
```

규칙:

- Contract ID는 `C1`, Invariant ID는 `I1`, Verifiability ID는 `V1`
- `Verification Method` enum은 `test`, `review`, `runtime-check`, `manual-check`
- 표면 문법은 유연하게 두되, 의미론과 traceability는 고정한다

### 1.6 Temporary Spec Canonical Shape

temporary spec은 global spec의 축약 복사본이 아니다. 변경 작업을 위한 실행 청사진이다.

canonical 7섹션:

1. `Change Summary`
2. `Scope Delta`
3. `Contract/Invariant Delta`
4. `Touchpoints`
5. `Implementation Plan`
6. `Validation Plan`
7. `Risks / Open Questions`

핵심 규칙:

- `Contract/Invariant Delta`는 `C*`, `I*` ID를 사용한다.
- `Validation Plan`은 `V*` ID를 사용하고 delta ID를 `Targets`로 연결한다.
- `Touchpoints`는 전수형 파일 목록이 아니라 전략적 change hotspot이다.
- temporary spec의 실행 정보는 global spec에 그대로 병합하지 않는다.

compact example:

```markdown
## Contract/Invariant Delta

| ID | Type | Change | Why |
|----|------|--------|-----|
| C1 | Modify | output must include CIV section | canonical rollout 유지 |
| I1 | Add | delta-to-validation traceability must survive rewrites | drift 방지 |

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, I1 | review, test | verify generated draft structure and template output |
```

### 1.7 spec-update-todo / done의 역할

- `spec-update-todo`: temporary spec이나 user input을 읽고, global spec에 남아야 할 **planned persistent information**만 올린다.
- `spec-update-done`: 실제 구현과 validation evidence를 읽고, global spec에 남아야 할 **implemented persistent information**만 올린다.

즉:

- temporary spec의 task breakdown, validation 실행 메모, transient risk log는 global spec 본문으로 가지 않는다.
- global spec으로 올라가는 것은 scope, decisions, CIV, usage impact, decision-bearing structure 변화다.

### 1.8 파이프라인 구성 원칙

1. **Spec-first**: global spec이 없으면 구현 전에 `spec-create` 선행.
2. **Delta-first for non-trivial changes**: 중규모 이상 변경은 temporary spec 또는 `feature-draft`를 선행.
3. **Review-fix 필수**: review만 하고 끝나지 않는다.
4. **Execute -> Verify**: 에이전트 호출 != 완료. evidence까지 확인해야 한다.
5. **파일 기반 handoff**: 상태 전달은 artifact 파일 경로 중심.
6. **Global spec 직접 수정 금지**: spec 변경은 `spec-update-todo` / `spec-update-done`에 위임.

---

## Part 2: 스킬 카탈로그

### 2.1 스킬 의존성 그래프

```text
spec-create -> feature-draft -> spec-update-todo -> implementation-plan -> implementation -> implementation-review -> spec-update-done
                                                                                             |  (review-fix loop)
                                                                                   ralph-loop-init (장시간 테스트)
```

`spec-review`는 파이프라인 끝이나 중간의 감사 단계로 선택적으로 추가한다.
`spec-summary`와 `spec-rewrite`는 비오케스트레이션 보조 스킬이다.

### 2.2 오케스트레이션 대상 스킬

#### feature-draft

- **`Agent(subagent_type="feature-draft")`**
- **Role**: temporary spec draft + implementation plan 통합 생성
- **Input**: 사용자 요청 + global spec
- **Output**: `_sdd/drafts/feature_draft_<topic>.md`
- **Reasoning note**: 중규모 이상 기능의 시작점. delta, touchpoints, validation linkage를 먼저 고정한다.

#### spec-update-todo

- **`Agent(subagent_type="spec-update-todo")`**
- **Role**: planned delta를 global spec에 사전 반영
- **Input**: feature draft Part 1 + global spec
- **Output**: global spec 업데이트
- **Reasoning note**: 장기 구현 중 drift 방지. temporary spec 전체를 복사하지 않는다.

#### implementation-plan

- **`Agent(subagent_type="implementation-plan")`**
- **Role**: temporary spec delta를 phase/task 중심 계획으로 세분화
- **Input**: feature draft 또는 temporary spec + global spec
- **Output**: `_sdd/implementation/implementation_plan.md`
- **Reasoning note**: large 변경에서 delta coverage와 validation linkage를 task로 풀어낸다.

#### implementation

- **`Agent(subagent_type="implementation")`**
- **Role**: TDD 기반 코드 구현
- **Input**: implementation plan 또는 feature draft
- **Output**: 코드 변경 + implementation artifact
- **Reasoning note**: actual code generation/modification 단계

#### implementation-review

- **`Agent(subagent_type="implementation-review")`**
- **Role**: 구현 결과를 계획/스펙 대비 리뷰
- **Input**: implementation artifact + 코드 + 필요 시 spec
- **Output**: 리뷰 리포트
- **Reasoning note**: review-fix loop의 핵심

#### spec-update-done

- **`Agent(subagent_type="spec-update-done")`**
- **Role**: 구현/검증 완료 후 global spec 동기화
- **Input**: global spec + temporary spec + implementation artifact + 코드
- **Output**: global spec 업데이트
- **Reasoning note**: temporary execution detail은 버리고 persistent truth만 남긴다.

#### spec-review

- **`Agent(subagent_type="spec-review")`**
- **Role**: global/temporary spec 품질 및 drift 감사
- **Input**: spec + 코드/implementation artifact
- **Output**: 리뷰 리포트
- **Reasoning note**: canonical model 기준으로 품질을 검증한다.

#### ralph-loop-init

- **`Agent(subagent_type="ralph-loop-init")`**
- **Role**: 장시간 반복 검증 루프 생성 및 실행 지원
- **Input**: 코드 파일 + 장시간 테스트/학습 명령
- **Output**: `ralph/` 디렉토리
- **Reasoning note**: 인라인 테스트로 부족한 long-running verification 전용

### 2.3 비오케스트레이션 스킬

| 스킬 | 용도 |
|------|------|
| spec-create | global spec 최초 생성 |
| discussion | 방향성과 개념 토론 |
| guide-create | 구현/리뷰 가이드 생성 |
| write-phased | inline phased writing helper |
| spec-summary | global/temporary spec 요약 |
| spec-rewrite | canonical model에 맞춰 spec 구조 재정리 |
| spec-upgrade | 구형 spec을 current canonical model로 변환 |

### 2.4 파이프라인 구성 가이드라인

#### 소규모

```text
implementation -> inline test
```

- 영향 파일 1-3개, 신규 컴포넌트 거의 없음
- global spec 변경이 없거나 매우 경미함

#### 중규모

```text
feature-draft -> implementation -> review-fix -> inline test -> spec-update-done
```

- feature-draft가 temporary spec과 기본 implementation plan을 함께 제공
- global spec planned update는 필요 시만 `spec-update-todo` 추가

#### 대규모

```text
feature-draft -> spec-update-todo -> implementation-plan -> implementation -> review-fix -> test -> spec-update-done
```

- multi-phase 변경
- large delta, 높은 리스크, 지속 spec 영향이 큼
- `spec-update-todo`로 global spec drift를 선제 관리

#### 특수 패턴

- **스펙 없음**: `spec-create` 선행
- **방향 불확실**: discussion 선행
- **장시간 검증 필요**: `ralph-loop-init` 포함
