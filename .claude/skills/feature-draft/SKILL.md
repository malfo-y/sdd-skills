---
name: feature-draft
description: This skill should be used when the user asks to "feature draft", "draft feature", "기능 초안", "기능 명세", "계획 잡아줘", or wants a feature spec for a change that fits in a single context — task breakdown with Target Files and falsifiable AC. Oversized changes are split into multiple features via a rolling split plan.
version: 2.0.1
---

# Feature Draft

구현에 필요한 기능 명세 및 계획 작성. 단일 컨텍스트로 감당되는 변경의 기본 경로다. 산출물의 정의는 아래 Required Output이 전부다.

## 분할 규칙 (작성 전 판정 + 작성 중 상시 감시)

둘 중 하나에 해당하면 하나의 draft로 강행하지 않는다 — **분할한다**. 규모 초과의 해소 수단은 더 큰 파이프라인이 아니라 분할이다.

1. **coverage 눈검산 불가**: 변경 요소(계약·수정 지점)와 task의 대응이 다대다로 얽혀 "모든 변경 요소가 어느 task에서 처리되는지"를 눈으로 검산할 수 없다.
2. **단일 컨텍스트 초과**: 작업 총량이 한 세션에서 품질 저하 없이 끝날 규모를 넘는다.

리트머스: **"머리 하나에 다 안 담기는가?"** 담기면 단일 draft, 안 담기면 쪼갠다. 새 contract/invariant(다른 코드·문서·미래 작업이 새로 의지하게 될 약속)가 생겨도, 소수이고 눈검산 가능하면 단일 draft 적격이다 — 해당 task의 `Contracts`에 적는다.

**분할 방법 (롤링)**: 분할 필요 판정이면 이 draft 파일이 곧 분할 계획이다. Part 1 마커 내부에 분할 feature 목록(feature당 1줄 의도 + scope)을 적는다 — `spec-sync` 스킬이 마커 내부를 소비해 feature별 planned todo로 global spec에 고정한다. Part 2에는 **첫 feature의 task만** 작성한다. 나머지 feature는 각자 차례에 자기 draft를 새로 만든다.

**census형 sweep은 분할 대상이 아니라 검증 대상이다**: rename/전파류처럼 같은 대상의 변형 표기(kebab/underscore/공백/글롭)가 여러 파일에 흩어져 전수 열거 없이는 수정 잔존이 재발하는 변경은, Part 2 마지막에 read-only 검증 task(변형 표기 전수 grep census를 AC로, Target Files `없음 (read-only 검증)`)를 필수로 둔다.

판정 결과와 근거를 draft 상단에 1줄 기록한다 — 값은 "적격" 또는 "분할 필요 — 분할 계획 포함".

## Process

1. **맥락 수집**: 요구사항의 원천은 이번 대화다(메인 루프가 이미 보유). spec/코드 탐색은 Target Files와 AC를 실측으로 뒷받침할 만큼만 한다.
2. **분할 판정**: 위 분할 규칙 점검. 판정 근거 1줄 확정 (census형 신호가 있으면 검증 task를 Part 2 마지막에 예약).
3. **draft 작성**: Required Output 구조로 작성한다. **task는 단일 의도를 가지고 자기 AC만으로 완료 판정이 닫히는 실행 단위다** — 의도가 두 문장이면 두 task로 쪼개고, 다른 task의 결과를 봐야 완료를 판정할 수 있으면 경계를 다시 긋는다.
4. **surface**: 저장 후 Open Questions 중 사용자 확인이 필요한 항목만 채팅에 1줄씩 노출한다. 없으면 "사용자 확인이 필요한 항목 없음" 1줄.

## Required Output

파일: `_sdd/drafts/<YYYY-MM-DD>_feature_draft_<slug>.md` (`slug`는 소문자 snake_case)

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

- **AC가 핵심이다**: 각 AC는 falsifiable해야 한다 — "미충족"이라 말할 수 있는 관찰/증거가 정의되지 않는 AC는 다시 쓴다.
- **Target Files는 실측**: 현재 코드 탐색으로 확인한 경로만 적는다. 확정 불가면 `[TBD] <사유>`. 마커는 `[C]` Create / `[M]` Modify / `[D]` Delete.
- **마커 보존**: `spec-update-todo-input` 마커 쌍을 유실하지 않는다 — `spec-sync` 입력 호환의 조건이다.
- **품질 게이트**: 작성 후 `plan-review` 스킬 1회로 draft를 점검한다 — **단일 패스**로, review loop는 돌리지 않고 finding은 작성자인 메인 루프가 직접 반영한다.
- **실행 인계**: `implementation` 스킬(메인 루프 직접 RED→GREEN 구현)로 인계한다. 구현 작성을 여러 갈래로 나눠야 할 규모로 드러나면 분할 규칙으로 돌아간다.
- **Minimum-Code Mandate**: task의 description과 AC는 요청된 동작을 만드는 최소 코드만 명세한다. 요청되지 않은 기능·옵션·설정 가능성, 단일 사용처 추상화, 발생할 수 없는 시나리오의 에러 처리를 계획에 넣지 않는다.

## Integration

- `plan-review`: draft 품질 게이트 — 작성 후 단일 패스 점검 (위 규칙 참조).
- `implementation`: 실행 인계 대상 — Part 2 task를 RED→GREEN으로 구현한다.
- `spec-sync`: Part 1 마커 내부를 global spec 반영 입력으로 소비한다 (파일명이 기존 `*_feature_draft_*` glob에 매칭된다).
