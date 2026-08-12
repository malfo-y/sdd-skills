---
name: feature-draft
description: This skill should be used when the user asks to "feature draft", "draft feature", "기능 초안", "기능 명세", "계획 잡아줘", or wants a feature spec for a change that fits in a single context — task breakdown with Target Files and falsifiable AC. Oversized changes are split into multiple features via a rolling split plan.
---

# Feature Draft

구현에 필요한 기능 명세 및 계획 작성. 단일 컨텍스트로 감당되는 변경의 기본 경로다. 산출물의 정의는 아래 Required Output이 전부다.

## 분할 규칙 (작성 전 판정 + 작성 중 상시 감시)

변경 요소(계약·수정 지점)와 task의 대응이 다대다로 얽혀 "모든 변경 요소가 어느 task에서 처리되는지"를 눈으로 검산할 수 없으면(**coverage 눈검산 불가**), 하나의 draft로 강행하지 않는다 — **분할한다**. 해소 수단은 더 큰 파이프라인이 아니라 분할이다.

새 contract/invariant(다른 코드·문서·미래 작업이 새로 의지하게 될 약속)가 생기는 것 자체는 분할 사유가 아니다 — 해당 task의 `Contracts`에 적는다.

**분할 방법 (롤링)**: 분할 필요 판정이면 이 draft 파일이 곧 분할 계획이다. Part 1 마커 내부에 분할 feature 목록(feature당 1줄 의도 + scope)을 적는다 — `spec-sync` 스킬이 마커 내부를 소비해 feature별 planned todo로 global spec에 고정한다. Part 2에는 **첫 feature의 task만** 작성한다. 나머지 feature는 각자 차례에 자기 draft를 새로 만든다.

**census형 sweep은 분할 대상이 아니라 검증 대상이다**: rename/전파류처럼 같은 대상의 변형 표기(kebab/underscore/공백/글롭)가 여러 파일에 흩어져 전수 열거 없이는 수정 잔존이 재발하는 변경은, Part 2 마지막에 read-only 검증 task(변형 표기 전수 grep census를 AC로, Target Files `없음 (read-only 검증)`)를 필수로 둔다.

판정 결과와 근거를 draft 상단에 1줄 기록한다 — 값은 "적격" 또는 "분할 필요 — 분할 계획 포함".

## Process

1. **맥락 수집**: 요구사항의 원천은 이번 대화다(메인 루프가 이미 보유). spec/코드 탐색은 Target Files와 AC를 실측으로 뒷받침할 만큼만 한다. 동일 change element가 둘 이상의 동기화 표면에 걸리는지 함께 식별한다.
2. **핵심 질문**
   - **발동**: 로컬 탐색으로 닫히지 않고 답이 아키텍처·범위·Target Files를 바꾸는 unknown만 묻는다.
   - **순서**: 한 번에 하나씩, 뒤늦은 답이 앞선 결정을 가장 많이 무효화하는 질문부터 묻는다.
   - **무인 실행**: 가장 합당한 해석을 택해 결정과 근거를 Open Questions에 기록한다.
3. **task 만들기** — 계획의 본체다. 아래 순서로 짓는다.
   - **열거**: 이번 변경이 만들거나 바꾸는 요소를 먼저 전수 열거한다 — 계약·수정 지점·1에서 식별한 동기화 표면. task부터 떠올리지 않는다. 열거가 끝나야 규모와 경계가 보인다.
   - **배정**: 각 요소에 owner task를 **정확히 하나** 배정한다. 한 task가 여러 요소를 가져도 되지만, 한 요소가 두 task에 걸치면 경계를 다시 긋는다. 의도가 두 문장이면 두 task로 쪼개고, 다른 task의 결과를 봐야 완료를 판정할 수 있어도 다시 긋는다.
   - **순서**: 산출물 의존으로만 정한다 — 뒤 task가 앞 task의 산출물을 쓰면 그 순서로 놓고, 그런 의존이 없으면 순서에 의미를 두지 않는다(구현이 병렬로 진행해도 좋다는 신호다).
4. **분할 판정**: 3의 요소↔task 대응을 눈으로 검산해 위 분할 규칙을 점검한다. 판정 근거 1줄 확정 (census형 신호가 있으면 검증 task를 Part 2 마지막에 예약).
5. **draft 작성**
   - **Template fidelity**: Required Output의 fenced template을 출발 skeleton으로 verbatim 복사하고 heading·marker·field order를 보존한다.
   - **허용 변형**: placeholder와 예시 값을 실제 값으로 치환하고, Propagation row·task block·AC·Target File row는 필요한 수만큼 반복한다. 조건이 성립하지 않는 `Propagation Surfaces`·`Open Questions` 섹션만 제거할 수 있다.
6. **surface**: 저장 후 Open Questions 중 사용자 확인이 필요한 항목만 채팅에 1줄씩 노출한다. 없으면 "사용자 확인이 필요한 항목 없음" 1줄.

## Required Output

파일: `_sdd/drafts/<YYYY-MM-DD>_feature_draft_<slug>.md` (`slug`는 소문자 snake_case)

아래 fenced template이 산출물 구조의 단일 소스다.

```markdown
# Feature Draft: [title]

> 규모 판정: [판정 근거 1줄 — 값은 "적격" 또는 "분할 필요 — 분할 계획 포함"]

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
[무엇이 왜 바뀌는가. **새 contract/invariant 약속이 생기면 여기 1줄씩 명시한다** — `spec-sync` 스킬이 이 마커 내부를 global spec 반영 입력으로 소비한다.]

## Scope
- **In**: ...
- **Out**: ...
<!-- spec-update-todo-input-end -->

# Propagation Surfaces
[동일 change element가 둘 이상의 동기화 표면(미러·등록·템플릿·문서 등)에 반영돼야 할 때만 작성하고, 없으면 섹션 생략.]

| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | ... | exact paths/patterns | read-only query + expected surface set | Task N |

# Part 2: Tasks

### Task 1: [action-oriented title]
[의도 1줄 — 비자명한 근거가 있으면 함께.]

**Contracts** (있을 때만): 이 task가 만드는/바꾸는 약속(인터페이스·불변식)의 정밀 서술.

**Acceptance Criteria**:
- [ ] AC1: ...

**Target Files**:
- [M] `path/to/file` -- 변경 이유
- [C] `path/to/new_file` -- 생성 이유
- ...

# Open Questions
[없으면 섹션 생략. 항목당 1-2줄: 내린 결정 + 사용자 확인 필요 여부.]
```

## 규칙

- **task의 정의**: task는 단일 의도를 가지고 자기 AC만으로 완료 판정이 닫히는 실행 단위다.
- **AC가 핵심이다**
  - **1등급**: 재현 가능한 test/check 출력으로 판정한다.
  - **2등급**: 명시 rubric + reviewer 판정 + 인용 근거로 판정한다.
  - **공통 기준**: 각 AC에 평가방법과 기대 evidence를 함께 쓰고, 이진 판정으로 닫으며, 외부 증거에 묶어 제3자가 반박 가능하게 한다.
- **Target Files는 실측**: 현재 코드 탐색으로 확인한 경로만 적는다. 확정 불가면 `[TBD] <사유>`. 마커는 `[C]` Create / `[M]` Modify / `[D]` Delete.
- **마커 보존**: `spec-update-todo-input` 마커 쌍을 유실하지 않는다 — `spec-sync` 입력 호환의 조건이다.
- **조건부 propagation 표**
  - 발동: 동일 change element가 둘 이상의 동기화 표면에 걸릴 때만 `Propagation Surfaces`를 만든다.
  - 필드: `Required surfaces`는 exact path/pattern, `Discovery evidence`는 read-only query와 기대 surface 집합을 적는다.
  - 소유·연접: 각 행은 정확히 하나의 owner task를 가지며, 그 task의 Target Files와 AC가 required surface의 실행·검증을 닫는다.
  - 비발동: 일반 다중파일 변경만으로는 표를 만들지 않는다.
  - census 예외: 변형 표기 전수 제거가 필요할 때만 별도의 census read-only 검증 task 규칙을 적용한다.
- **품질 게이트**: 작성 후 producer인 메인 루프가 `plan-review`를 호출해 finding을 직접 반영한다 — 각 호출은 **단일 패스**이고 reviewer와 사용자는 재호출·fix를 소유하지 않는다.
  - **gate 1 → fix 1** (항상): Critical/High/Medium은 반영하고, Low는 **저비용 AND 명백히 이득 AND 현재 draft scope 내** 셋을 모두 만족할 때만 반영하며 나머지는 advisory로 남긴다 (`현재 draft scope 내`가 scope 확장을 막는 load-bearing 조건).
  - **gate 2 → fix 2** (조건부): fix 전 raw 합산 finding이 Low 제외 **Critical+High ≥ 3 또는 Medium ≥ 5**면 같은 게이트를 한 번 더 호출하고 같은 fix 정책을 적용한다. 이후 gate 2 finding이 인용한 평가조건을 final draft에서 재확인하고 evidence와 미해소 finding을 남긴다. gate 3은 없다 — gate 2도 임계값이면 마감에서 후속 `plan-review` 1회 수동 실행을 권고한다.
  - 마감 메시지는 실행한 게이트의 severity·fix·검증 결과를 호출별로 구분해 보고한다.
- **실행 인계**: `implementation` 스킬(메인 루프 직접 RED→GREEN 구현)로 인계한다. 구현 작성을 여러 갈래로 나눠야 할 규모로 드러나면 분할 규칙으로 돌아간다.
- **Minimum-Code 기준**: task의 description과 AC는 요청 동작 또는 관측된 위험에 직접 추적되는 가장 작은 변경만 명세한다.

## Integration

- `plan-review`: draft 품질 게이트 — producer가 각 호출을 단일 패스로 실행하며, finding 규모에 따라 최대 두 번 호출한다 (위 규칙 참조).
- `implementation`: 실행 인계 대상 — Part 2 task를 RED→GREEN으로 구현한다.
- `spec-sync`: Part 1 마커 내부를 global spec 반영 입력으로 소비한다 (파일명이 기존 `*_feature_draft_*` glob에 매칭된다).
