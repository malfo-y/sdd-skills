---
name: implementation-lite
description: This skill should be used when the user asks for "implementation lite", "lite implementation", "implement lite draft", "라이트 구현", "경량 구현", "간단히 구현", "lite draft 구현", or wants to execute a small task set (typically a lite feature draft) with RED→GREEN test-first where the main loop itself writes all code and tests (read-only helper agents allowed; independent tasks may be batched in parallel). When implementation writing itself must fan out to multiple agents, use implementation (full) instead.
version: 1.0.0
---

# Implementation Lite

TDD 기반 구현 실행 스킬. Task마다 test-first 순서를 지킨다 — **실패를 먼저 관찰하고(RED), 최소 구현으로 통과시킨다(GREEN)**. 테스트는 필요한 task에만 만든다(아래 Triage).

**작성자 불변식**: 코드와 테스트는 메인 루프가 직접 작성한다. 탐색·조사 같은 read-only 보조 agent는 필요하면 자유롭게 쓴다 — 경계는 "작성의 위임"이다. 구현 작성 자체를 여러 sub-agent로 나눠야 할 규모면 승격 규칙을 따른다.

## 입력

우선순위:

1. 사용자 지정 경로의 lite feature draft (`_sdd/drafts/*_feature_draft_lite_*.md`) — Part 2 task들을 하나씩 실행한다.
2. 대화에서 직접 받은 inline task 목록 — 각 task에 AC(충족/미충족을 증거로 판정할 수 있는 완료 조건)와 대상 파일이 없으면 시작 전에 보완한다. 대상 파일 경로는 코드 탐색으로 실측 확인한다.

- 명백한 의존(뒤 task가 앞 task의 산출물을 사용)이 문서 순서와 어긋나면 순서만 인라인으로 조정한다.
- 서로 독립인 task들은 tool call을 배칭해 병렬로 실행해도 된다. 병렬로 진행해도 **각 task 안에서는 RED→GREEN 순서를 지킨다**.

## 승격 규칙 (시작 전 판정 + 실행 중 상시)

하나라도 해당하면 이 스킬로 강행하지 않는다 — 사용자에게 `implementation` 스킬(full: 병렬 dispatch와 리뷰 게이트를 갖춘 실행 orchestrator) 전환을 안내하고, 진행분과 잔여 task를 전환 입력으로 넘긴다.

1. **단일 세션 초과**: 작업 총량이 한 세션에서 품질 저하 없이 끝날 규모를 넘는다.
2. **계약 오류 반복**: 같은 task에서 아래 "테스트 불변 규칙"의 계약 오류 선언이 2회 이상 발생한다 — 계약 자체가 흔들리는 신호로, 테스트 작성자와 구현자가 분리된 full의 구조가 필요하다.

## Process — task 단위로

### 1. Triage: 테스트가 필요한가

각 task를 셋 중 하나로 분류한다. 기준은 구현 난이도가 아니다 — "간단한 구현이라서"는 (c) 자격이 아니다.

- **(a) test**: 테스트 프레임워크로 실패하는 테스트를 쓸 수 있는 task.
- **(b) structural-check**: 프레임워크 없는 자산(문서·설정 등)이지만, grep·diff·명령 exit code로 충족 여부를 판정하는 check를 만들 수 있는 task.
- **(c) test-free**: 가능한 check가 "파일/문구가 존재한다" 수준의 동어반복뿐이라 판정 가치가 없는 task — 테스트 없이 구현하고, AC 검증은 마감 증거 테이블에서 닫는다. 분류 근거를 1줄 기록한다.

경계 판정이 애매하면 (b) 쪽으로 보수적으로 분류하고 판단 근거를 1줄 기록한다.

### 2. RED: 실패를 먼저 관찰

(a)/(b) task는 구현 전에 테스트/check를 작성하고 **실제 실행해 실패를 관찰한다**.

- 실패는 AC가 요구하는 동작의 미충족(assertion/check 단계 실패)이어야 한다. import·문법 오류로만 실패하면 동작 검증에 도달하도록 테스트를 고쳐 다시 관찰한다.
- 실패 출력을 캡처해 둔다 — 마감 증거 테이블의 재료다.
- **RED를 관찰하기 전에는 구현을 시작하지 않는다.**

### 3. GREEN: 최소 구현으로 통과

- AC가 요구하는 동작을 만드는 최소 코드만 작성한다. 요청되지 않은 옵션·설정·추상화·에러 처리를 추가하지 않는다.
- 테스트/check를 다시 실행해 통과를 확인하고 출력을 캡처한다.
- task의 대상 파일 밖 수정이 필요해지면, 수정 전에 그 파일과 이유를 기록한다(마감 요약에 포함).

### 4. 테스트 불변 규칙

RED 관찰 후에는 테스트를 통과시키기 위해 테스트를 약화·수정하지 않는다. 테스트가 가정한 계약이 틀렸다고 판단되면:

1. 어떤 가정이 왜 틀렸는지 **선언**을 남긴다 (채팅 + 마감 요약).
2. 테스트를 고치고 RED를 다시 관찰한 뒤 구현으로 돌아간다.

선언 없는 테스트 수정은 없다. 같은 task에서 선언이 반복되면 승격 규칙 2에 해당한다.

## 마감

1. **회귀 1회**: 전체 테스트 suite가 있으면 실행한다. 이번 변경과 무관한 실패를 발견하면 사용자에게 보고한다 — 몰래 고치지 않는다.
2. **AC→증거 테이블**을 채팅에 노출한다. 증거는 외부에 남는 형태(명령 출력·diff·grep 결과)로 적는다. **증거를 못 대는 AC는 "충족"이라 적지 않는다** — 미충족/보류로 남기고 보고한다.

   | Task | AC | 판정 | 증거 |
   |------|----|------|------|

3. 계약 오류 선언·대상 파일 밖 수정이 있었으면 함께 요약한다.
4. 추가 검증이 필요하면(사용자 요청 시) `implementation-review` 스킬 1회를 후속으로 쓴다 — 기본은 증거 테이블로 닫는다.

## Integration

- `feature-draft-lite`: 주 입력 — lite draft Part 2의 task를 소비한다.
- `implementation` (full): 승격 대상 — 진행분·잔여 task를 전환 입력으로 전달한다.
- `implementation-review`: 선택적 후속 검증 (단일 패스).
- `spec-sync`: 구현이 spec에 반영될 변경이면, draft Part 1 마커 내용과 실제 변경을 입력으로 global spec을 동기화한다.
