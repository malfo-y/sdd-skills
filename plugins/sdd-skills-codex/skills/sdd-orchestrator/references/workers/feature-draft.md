# feature-draft worker 계약

`sdd-orchestrator`가 띄운 계획 worker가 따른다. 구현에 필요한 기능 명세와 계획을 작성한다. 산출물의 정의는 아래 Required Output이 전부다. 품질 게이트(`plan-review`)와 구현 인계는 오케스트레이터가 소유한다.

**task의 정의**: task는 단일 의도를 가지고 자기 AC만으로 완료 판정이 닫히는 실행 단위다.

## 목표

입력의 요청과 digest의 결정·제약을 falsifiable AC와 실측 Target Files를 가진 task 집합으로 바꿔 `_sdd/drafts/` draft 파일 하나로 남긴다. fix 모드면 받은 findings로 같은 draft를 고친다.

## Acceptance Criteria

- [ ] AC1: draft 파일이 Required Output의 경로 규약과 fenced template 구조(마커 쌍 포함)대로 생성되었다.
- [ ] AC2: 규모 판정 1줄이 draft 상단에 기록되었다 (분할 규칙 참조 — 분할 필요면 Part 1에 분할 계획, Part 2에 첫 feature만).
- [ ] AC3: 현재 feature의 모든 변경 요소에 owner task가 정확히 하나 배정되었고(Process 3 검산·분할 규칙 참조), 각 task의 AC가 "규칙"의 등급·공통 기준을 따른다.
- [ ] AC4: 반환이 `반환` 절 형식을 따르고, AC별 검증 명령과 기대값을 `digest 변경분`에 담았다.

## Process

1. **맥락 수집**: 요구사항의 원천은 입력의 요청과 digest의 결정·제약이다. spec/코드 탐색은 Target Files와 AC를 실측으로 뒷받침할 만큼만 한다. 동일 change element가 둘 이상의 동기화 표면에 걸리는지 함께 식별한다.
2. **unknown 처리**: 사용자에게 질문하지 않는다. 로컬 탐색으로 닫히지 않는 unknown은 가장 합당한 해석을 택하고 결정과 근거를 Open Questions에 적는다. 답에 따라 아키텍처·범위·Target Files가 바뀌는 항목은 `사용자 확인 필요`로 표시한다.
3. **task 만들기** — 계획의 본체다. 아래 순서로 짓는다.
   - **열거**: 이번 변경이 만들거나 바꾸는 요소를 먼저 전수 열거한다 — 계약·수정 지점·1에서 식별한 동기화 표면. task부터 떠올리지 않는다. 열거가 끝나야 규모와 경계가 보인다.
   - **배정**: 각 요소에 owner task를 **정확히 하나** 배정한다. 한 task가 여러 요소를 가져도 되지만, 한 요소가 두 task에 걸치면 경계를 다시 긋는다. 같은 로직·상수·계약을 두 task가 각자 구현하도록 계획했다면 그것도 요소 하나를 두 곳에 배정한 것이다. 의도가 두 문장이면 두 task로 쪼갠다. 선행 task의 확정된 산출물을 입력으로 쓰는 것은 허용한다(census 검증 포함). 자기 AC로 판정하지 못하고 다른 task의 미완료 작업이나 향후 판정에 기대면 경계를 다시 긋는다.
   - **순서**: 산출물 의존으로만 정한다 — 뒤 task가 앞 task의 산출물을 쓰면 그 순서로 놓고, 그런 의존이 없으면 순서에 의미를 두지 않는다(구현이 병렬로 진행해도 좋다는 신호다).
4. **분할 판정**: 3의 요소↔task 대응을 눈으로 검산해 아래 분할 규칙을 점검한다. 판정 근거 1줄 확정 (census형 신호가 있으면 검증 task를 Part 2 마지막에 예약).
5. **draft 작성**
   - **Template fidelity**: Required Output의 fenced template을 출발 skeleton으로 verbatim 복사하고 heading·marker·field order를 보존한다.
   - **허용 변형**: placeholder와 예시 값을 실제 값으로 치환하고, Task block·AC·Target File row는 필요한 수만큼 반복한다.

### 분할 규칙 (작성 전 판정 + 작성 중 상시 감시)

변경 요소(계약·수정 지점)와 task의 대응이 다대다로 얽혀 "모든 변경 요소가 어느 task에서 처리되는지"를 눈으로 검산할 수 없으면(**coverage 눈검산 불가**), 하나의 draft로 강행하지 않는다 — **분할한다**. 해소 수단은 더 큰 파이프라인이 아니라 분할이다.

새 contract/invariant(다른 코드·문서·미래 작업이 새로 의지하게 될 약속)가 생기는 것 자체는 분할 사유가 아니다 — 해당 task의 `Contracts`에 적는다.

**분할 방법 (롤링)**: 분할 필요 판정이면 이 draft 파일이 곧 분할 계획이다. Part 1 마커 내부에 분할 feature 목록(feature당 1줄 의도 + scope)을 적는다 — `spec-sync` 단계가 마커 내부를 소비해 feature별 planned todo로 global spec에 고정한다. Part 2에는 **첫 feature의 task만** 작성하고, AC3의 task 단위 검산도 이 현재 feature 범위에 적용한다. 나머지 변경 범위는 Part 1의 feature별 scope에 보존하고, 각자 차례에 자기 draft를 새로 만든다.

**census형 sweep은 분할 대상이 아니라 검증 대상이다**: rename/전파류처럼 같은 대상의 변형 표기(kebab/underscore/공백/글롭)가 여러 파일에 흩어져 전수 열거 없이는 수정 잔존이 재발하는 변경은, Part 2 마지막에 read-only 검증 task(변형 표기 전수 grep census를 AC로, Target Files `없음 (read-only 검증)`)를 필수로 둔다.

판정 결과와 근거를 draft 상단에 1줄 기록한다 — 값은 "적격" 또는 "분할 필요 — 분할 계획 포함".

## Required Output

파일: `_sdd/drafts/<YYYY-MM-DD>_feature_draft_<slug>.md` (`slug`는 소문자 snake_case)

아래 fenced template이 산출물 구조의 단일 소스다.

```markdown
# Feature Draft: [title]

> 규모 판정: [판정 근거 1줄 — 값은 "적격" 또는 "분할 필요 — 분할 계획 포함"]

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
[무엇이 왜 바뀌는가. **새 contract/invariant 약속이 생기면 여기 1줄씩 명시한다** — `spec-sync` 단계가 이 마커 내부를 global spec 반영 입력으로 소비한다.]

## Scope
- **In**: ...
- **Out**: ...
<!-- spec-update-todo-input-end -->

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

- **AC가 핵심이다**
  - **1등급**: 재현 가능한 test/check 출력으로 판정한다.
  - **2등급**: 명시 rubric + reviewer 판정 + 인용 근거로 판정한다.
  - **공통 기준**: 각 AC에 평가방법과 기대 evidence를 함께 쓰고, 이진 판정으로 닫으며, 외부 증거에 묶어 제3자가 반박 가능하게 한다.
- **Target Files는 실측**: 현재 코드 탐색으로 확인한 경로만 적는다. 확정 불가면 `[TBD] <사유>`. 마커는 `[C]` Create / `[M]` Modify / `[D]` Delete.
- **Minimum-Code 기준**: task의 description과 AC는 요청 동작 또는 관측된 위험에 직접 추적되는 가장 작은 변경만 명세한다. 계획이 과잉으로 새는 자리 셋을 특히 본다.
  - **파일 생성의 기본값은 "만들지 않음"이다**: 기존 파일 수정으로 닫히면 `[M]`이고, `[C]`는 왜 수정으로 안 되는지를 생성 이유에 적는다.
  - **한 곳에서만 쓰일 helper·layer·config·interface를 계획하지 않는다**: 두 번째 사용처가 실재할 때 만든다.
  - **같은 정보를 여러 섹션에 재서술하지 않는다**: Description·AC·`Contracts` 중 한 곳이 소유하고 나머지는 참조한다.
- **마커 보존**: `spec-update-todo-input` 마커 쌍을 유실하지 않는다 — `spec-sync` 입력 호환의 조건이다.

## fix 모드

입력에 findings가 오면 새 draft를 만들지 않고 그 draft를 고친다. 받은 findings는 오케스트레이터가 반영하기로 고른 것이므로 모두 반영한다. 반영할 수 없는 finding은 사유를 반환한다.

## 반환

- draft 경로
- 규모 판정 1줄
- task 표: `Task | Target Files | 선행 task | Contracts 공유 task` (오케스트레이터의 병렬 판단 입력)
- `사용자 확인 필요` Open Questions (없으면 "없음")
- fix 모드면 finding별 반영 내용, 반영하지 못한 finding과 사유
- `digest 변경분`: AC별 `명령 → 기대값`, 탐색 중 확인한 환경 함정, 새로 내린 결정
