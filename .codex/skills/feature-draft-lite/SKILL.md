---
name: feature-draft-lite
description: This skill should be used when the user asks for "feature draft lite", "lite draft", "draft lite", "라이트 초안", "경량 기능 초안", "간단 draft", "가볍게 계획", or wants a lightweight feature draft for a change that fits in a single context — task breakdown with Target Files and AC, without the full coverage-index/validation ceremony. For scale-proven changes use feature-draft (full) instead.
version: 1.0.0
---

# Feature Draft Lite

구현에 필요한 기능 명세 및 계획 작성. 단일 컨텍스트로 감당되는 변경의 기본 경로다. 산출물의 정의는 아래 Required Output이 전부다.

## 승격 규칙 (작성 전 판정 + 작성 중 상시 감시)

셋 중 하나에 해당하면 이 스킬로 강행하지 않는다 — 사용자에게 `feature-draft`(full: 병렬·대규모 실행용 coverage 장부와 검증 매핑을 갖춘 draft 스킬) 전환을 안내하고, 작성 중 발견 시 진행분을 전환 입력으로 넘긴다.

1. **coverage 눈검산 불가**: 변경 요소(계약·수정 지점)와 task의 대응이 다대다로 얽혀 "모든 변경 요소가 어느 task에서 처리되는지"를 눈으로 검산할 수 없다.
2. **단일 컨텍스트 초과**: 작업 총량이 한 세션에서 품질 저하 없이 끝날 규모를 넘는다.
3. **census형 sweep**: rename/전파류처럼 같은 대상의 변형 표기(kebab/underscore/공백/글롭)가 여러 파일에 흩어져 있어, 전수 열거 없이는 수정 잔존이 재발하는 변경이다.

리트머스: **"머리 하나에 다 안 담기는가?"** 담기면 lite, 안 담기면 full. 새 contract/invariant(다른 코드·문서·미래 작업이 새로 의지하게 될 약속)가 생겨도, 소수이고 눈검산 가능하면 lite 적격이다 — 해당 task의 `Contracts`에 적는다.

판정 결과와 근거를 draft 상단에 1줄 기록한다.

## Process

1. **맥락 수집**: 요구사항의 원천은 이번 대화다(메인 루프가 이미 보유). spec/코드 탐색은 Target Files와 AC를 실측으로 뒷받침할 만큼만 한다.
2. **승격 판정**: 위 규칙 3개 점검. 통과 시 근거 1줄 확정.
3. **draft 작성**: Required Output 구조로 작성한다. **task는 단일 의도를 가지고 자기 AC만으로 완료 판정이 닫히는 실행 단위다** — 의도가 두 문장이면 두 task로 쪼개고, 다른 task의 결과를 봐야 완료를 판정할 수 있으면 경계를 다시 긋는다.
4. **surface**: 저장 후 Open Questions 중 사용자 확인이 필요한 항목만 채팅에 1줄씩 노출한다. 없으면 "사용자 확인이 필요한 항목 없음" 1줄.

## Required Output

파일: `_sdd/drafts/<YYYY-MM-DD>_feature_draft_lite_<slug>.md` (`slug`는 소문자 snake_case)

```markdown
# Feature Draft (Lite): [title]

> Lite 적격: [승격 규칙 3개를 통과한 근거 1줄]

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

# Open Questions
[없으면 섹션 생략. 항목당 1-2줄: 내린 결정 + 사용자 확인 필요 여부.]
```

## 규칙

- **AC가 핵심이다**: 각 AC는 falsifiable해야 한다 — "미충족"이라 말할 수 있는 관찰/증거가 정의되지 않는 AC는 다시 쓴다.
- **Target Files는 실측**: 현재 코드 탐색으로 확인한 경로만 적는다. 확정 불가면 `[TBD] <사유>`. 마커는 `[C]` Create / `[M]` Modify / `[D]` Delete.
- **마커 보존**: `spec-update-todo-input` 마커 쌍을 유실하지 않는다 — `spec-sync` 입력 호환의 조건이다.
- **품질 게이트**: 작성 후 `plan-review` 스킬 1회로 draft를 점검한다 — **단일 패스**로, review loop는 돌리지 않고 finding은 작성자인 메인 루프가 직접 반영한다.
- **실행 인계**: 기본은 `implementation-lite` 스킬(메인 루프 직접 RED→GREEN 구현)이다. `implementation`(full) 스킬로 인계할 수도 있다 — Part 2가 task별 AC·Target Files를 갖춘 flat task-set이라 그대로 입력이 된다. 구현 작성을 여러 sub-agent로 나눠야 할 규모면 승격 규칙으로 돌아간다.
- **출력 절약**: 산출물에 작성 과정·검증 내레이션을 남기지 않는다.

## Integration

- `plan-review`: draft 품질 게이트 — 작성 후 단일 패스 점검 (위 규칙 참조).
- `implementation-lite`: 기본 실행 인계 대상 — Part 2 task를 RED→GREEN으로 구현한다.
- `implementation` (full): 대안 실행 인계 대상 — Part 2를 flat task-set 입력으로 소비한다 (task별 AC·Target Files 보유, 검증 상세는 실행 측이 AC에서 도출).
- `spec-sync`: Part 1 마커 내부를 global spec 반영 입력으로 소비한다 (파일명이 기존 `*_feature_draft_*` glob에 매칭된다).
- `feature-draft` (full): 승격 대상 — 승격 시 이 draft 내용과 대화 맥락을 호출 입력으로 전달한다.
