---
name: implementation
description: Use this skill when the user asks to "implement the plan", "start implementation", "execute the plan", "구현해줘", "구현 실행", or wants to execute a task set (typically a feature draft) with RED→GREEN test-first where the main loop itself writes all code and tests (read-only helper agents allowed; independent tasks may be batched in parallel). Oversized work is closed at a feasible boundary and the remainder split into follow-up features.
---

# Implementation

TDD 기반 구현 실행 스킬. Task마다 test-first 순서를 지킨다 — **실패를 먼저 관찰하고(RED), 최소 구현으로 통과시킨다(GREEN)**. 테스트는 필요한 task에만 만든다(아래 Triage).

**작성자 불변식**: 코드와 테스트는 메인 루프가 직접 작성한다. 탐색·조사 같은 read-only 보조 agent는 필요하면 자유롭게 쓴다 — 경계는 "작성의 위임"이다. 구현 작성 자체를 여러 갈래로 나눠야 할 규모면 중단·분할 규칙을 따른다.

## Goal

입력 task 집합을 task마다 Triage→RED→GREEN→커버리지 델타로 실행하고, 마감 4단계까지 닫아 모든 AC 판정이 외부 증거에 묶인 상태로 종료한다.

## Acceptance Criteria

> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] AC1: ledger가 생성(재개면 이어쓰기)되어 task별 최종 상태를 반영한다 (Implementation Ledger 참조).
- [ ] AC2: 각 task가 Triage 분류를 거쳤고, (a)/(b) task는 RED 실패를 관찰한 뒤에만 구현을 시작했으며 GREEN 통과 출력을 캡처했다.
- [ ] AC3: 각 task의 커버리지 델타(§4)를 diff 실측으로 닫았다 — (c) task 포함.
- [ ] AC4: 마감 1~4를 순서대로 수행했다 — 회귀 1회, AC→증거 테이블(증거 없는 "충족" 없음), `implementation-review` 게이트+fix, 마감 요약.
- [ ] AC5: 코드·테스트 작성을 위임하지 않았다 (작성자 불변식).
- [ ] AC6: 중단·분할 규칙 발동 시 강행하지 않고 해당 규칙의 마감·반환·인계를 따랐다.

## 입력

우선순위:

1. 사용자 지정 경로의 feature draft (`_sdd/drafts/*_feature_draft_*.md`) — Part 2 task들을 하나씩 실행한다.
2. 대화에서 직접 받은 inline task 목록 — 각 task에 AC(충족/미충족을 증거로 판정할 수 있는 완료 조건)와 대상 파일이 없으면 시작 전에 보완한다. 대상 파일 경로는 코드 탐색으로 실측 확인한다.

- 명백한 의존(뒤 task가 앞 task의 산출물을 사용)이 문서 순서와 어긋나면 순서만 인라인으로 조정한다.
- 서로 의존하지 않는 read-only 호출(파일 읽기·검색·조회 명령)은 한 메시지에서 함께 낸다 — 앞 호출의 결과를 봐야 대상이 정해지는 호출만 다음 턴으로 미룬다. 파일을 쓰거나 상태를 바꾸는 호출은 배칭하지 않는다.
- 서로 독립인 task들은 병렬로 진행해도 된다. 병렬로 진행해도 **각 task 안에서는 RED→GREEN 순서를 지킨다**.

## 중단·분할 규칙 (시작 전 판정 + 실행 중 상시)

하나라도 해당하면 이 스킬로 강행하지 않는다:

1. **단일 세션 초과**
   - 발동: 작업 총량이 한 세션에서 품질 저하 없이 끝날 규모를 넘는다.
   - 마감: 현재 task를 닫을 수 있는 경계까지 완료한다.
   - 반환: 분할 사유·닫힌 task 경계·잔여 scope.
   - 인계: `feature-draft`의 `분할 방법 (롤링)`으로 복귀한다.
2. **계약 오류 반복**: 같은 task에서 아래 "테스트 불변 규칙"의 계약 오류 선언이 2회 이상 발생한다 — 계약 자체가 흔들리는 신호이며, 이는 구현이 아니라 계획의 문제다. 구현을 중단하고 draft로 복귀해 해당 task의 계약을 재설계한다(필요시 분할).

## Implementation Ledger (resume pointer)

모든 실행은 시작 시 `_sdd/implementation/<YYYY-MM-DD>_implementation_ledger_<slug>.md` 하나를 생성한다 — slug는 draft slug를 재사용하고, draft 없는 inline 실행이면 요청 요약 snake_case를 쓴다. 같은 slug의 기존 ledger가 있으면 새로 만들지 않고 그 파일을 이어쓴다(날짜가 바뀐 재개에서도 ledger를 분열시키지 않는다). 목적은 감사 로그가 아니라 **compact/세션 재개 후 다음 행동을 결정하는 resume pointer**다.

- **기록 기준**: 재실행으로 복원할 수 없는 사실만 기록한다.
  - 헤더: source(draft 경로 또는 inline 요청 요약)·시작 시점 dirty paths(`git status` 요약)·전체 status.
  - task별 1행: 상태·triage 분류와 근거 1줄·RED/GREEN 명령과 판정 신호 1줄·계약 오류 선언 횟수·계획 이탈·발견·대상 파일 밖 수정·커버리지 델타 항목 수와 처리.
  - **계획 이탈·발견**
    - 대상: source draft/inline task에서 달라진 판단 또는 새 edge case.
    - 형식: `건수; 내용 → 이유 → 처리`.
    - 없음: `0`.
    - 제외: 테스트/check 가정 오류는 `계약 오류 선언 횟수`에 기록한다.
  - 명령 출력 전문과 서술형 진행기는 기록하지 않는다 — 재실행으로 알 수 있는 것은 ledger의 몫이 아니다.
- **상태**: task당 `READY → RED_CONFIRMED → GREEN_CONFIRMED → DELTA_CLOSED` 네 단계만 쓴다. (c) test-free task는 RED/GREEN 단계가 없으므로 커버리지 델타를 닫으면 `READY → DELTA_CLOSED`로 직행한다. 각 단계 성공 직후 해당 task 행만 갱신한다.
- **재개 규칙**: ledger로 상태를 복원할 때, 미완료(비 DELTA_CLOSED) task는 상태를 신뢰하지 않고 그 task의 테스트/check를 fresh 실행해 재판정한다. DELTA_CLOSED task는 ledger를 신뢰하되 현재 diff와 모순이 보이면 같은 방식으로 fresh 실행해 재확인한다.
- **마감 통합**: 품질 게이트 fix가 있었으면 마지막에 `Review fix delta` 블록 하나로 기록한다 — AC→증거 테이블의 기록처 규칙은 마감 2가 소유한다.

## Process — task 단위로

다음 제한은 RED·GREEN·회귀를 포함한 모든 test/check 실행에 공통 적용한다.

- 표적 test/check는 30초가 지나면 중단한다.
- Timeout 후에는 test target, fixture, 또는 관련 구현이 바뀌기 전까지 같은 명령을 다시 실행하지 않는다.
- 느리다고 알려진 test는 repo 또는 사용자가 명시한 checkpoint에서만 실행한다.
- 실행 중 무겁게 드러난 테스트(무겁지 않다고 봤던 것 포함)는 그 사실을 보고하고, slow 분류로 숨기기 전에 **테스트 분리·리팩토링(fixture·suite 분할 등)을 사용자에게 적극 권고한다** — 본질적으로 느리다는 근거가 있을 때만 checkpoint 한정 실행으로 등록한다.

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

### 4. 커버리지 델타: 구현이 AC보다 넓어졌는가

GREEN 통과 직후, **이번 task에서 변경한 파일의 diff를 실제로 실행해 읽는다**(신규 파일은 전문).

- 기준점은 이번 task 시작 시점이다. 커밋 경계가 없으면 이번 task가 만진 hunk로 한정한다.
- 그 출력에서, 방금 통과시킨 테스트/check가 도달하지 않는 동작을 열거한다. 근거는 diff 출력이지 기억이나 AC 재독이 아니다.
- 전형적 델타: AC가 요구하지 않았는데 구현하며 생긴 분기·경계값·에러 경로·기존 호출부 적응.
- §1에서 (c)로 분류한 task도 이 단계를 건너뛰지 않는다 — 도달하는 테스트/check가 0개이므로 diff의 동작 전량이 열거 대상이다.

열거 항목이 AC도 요구하지 않고 기존 동작 유지에도 불필요하면 **삭제가 1순위다**(§3 최소성).

- 삭제했으면 (a)/(b) task는 §3에서 통과시킨 그 task의 테스트/check를 다시 실행해 통과를 재확인하고 출력을 갱신 캡처한다 — 증거 테이블에 싣는 GREEN 증거는 삭제 이후 출력이다. 재확인이 실패하면 그 항목은 불필요분이 아니므로 삭제를 되돌리고 남기기 경로로 닫는다.
- 남기기로 한 항목만 §1 Triage 기준을 그대로 적용해 닫는다 — (a)/(b)면 테스트/check를 추가하고, (c)면 근거를 1줄 남긴다.

델타 테스트는 코드가 이미 있어 RED를 관찰할 수 없다. 대신 **변이 확인**으로 판별력을 증명한다: 대상 동작을 일시적으로 깨서 그 테스트의 실패를 관찰하고, 되돌린 뒤 다시 실행해 통과를 재확인한다. 변이 확인 없는 델타 테스트는 코드를 보고 짜맞춘 무조건 통과 테스트다. 델타 테스트에도 아래 §5 테스트 불변 규칙이 동일하게 적용되며, §5 2단계의 "RED 재관찰"은 변이 확인 재수행으로 대체한다.

델타로 추가한 테스트는 마감 증거 테이블에 AC 유래 행과 같은 형식으로 싣는다. 델타가 없으면 아무것도 적지 않는다 — "델타 없음" 같은 통과 문구는 두지 않는다.

이 단계는 마감의 품질 게이트 fix로 구현이 바뀌었을 때도 그 fix diff에 적용한다. fix 산출물은 AC가 정해진 뒤에 태어나 AC 유래 테스트가 구조적으로 없는 부류다.

### 5. 테스트 불변 규칙

RED 관찰 후에는 테스트를 통과시키기 위해 테스트를 약화·수정하지 않는다. 테스트가 가정한 계약이 틀렸다고 판단되면:

1. 어떤 가정이 왜 틀렸는지 **선언**을 남긴다 (채팅 + 마감 요약).
2. 테스트를 고치고 RED를 다시 관찰한 뒤 구현으로 돌아간다.

선언 없는 테스트 수정은 없다. 같은 task에서 선언이 반복되면 중단·분할 규칙 2에 해당한다.

## 마감

1. **회귀 1회**: 이번 변경 관련 표적 test/check + fast 회귀(무거운 test 제외)만 실행한다. 이번 변경과 무관한 실패를 발견하면 사용자에게 보고한다 — 몰래 고치지 않는다.
2. **AC→증거 테이블**을 ledger에 완성해 쓰고, 같은 표를 채팅에 노출한다. 증거는 외부에 남는 형태(명령 출력·diff·grep 결과)로 적는다. **증거를 못 대는 AC는 "충족"이라 적지 않는다** — 미충족/보류로 남기고 보고한다.

   | Task | AC | 판정 | 증거 |
   |------|----|------|------|

3. **품질 게이트**: producer인 메인 루프가 `implementation-review`를 호출하고 finding을 직접 반영한다. 각 gate 호출 내부는 **단일 패스**이며 reviewer와 사용자는 gate 재호출이나 fix를 소유하지 않는다. 게이트 반환은 중간 산출물이며 사용자 입력 대기 지점이 아니다 — 반환 직후 같은 흐름에서 fix를 시작하고, 조건 판정과 gate 2 실행도 묻지 않고 이어서 수행한 뒤 마감 요약으로만 닫는다.
    1. **gate 1 → fix 1**: 첫 gate를 항상 호출한다. 반환된 Critical/High/Medium을 직접 반영한다. Low는 렌즈별 기존 정책을 적용한다.
        - **correctness 렌즈 Low**: **저비용 AND 명백히 이득 AND 현재 change scope 내** 세 조건을 모두 만족하는 것만 fix하고, 나머지는 마감 요약에 advisory로 남긴다. `현재 change scope 내`가 scope 확장을 막는 load-bearing 조건이다.
        - **simplicity 렌즈 Low**(주관적 취향): fix 대상이 아니며 advisory로만 남긴다.
    2. **조건 판정**: fix 전 gate 1의 raw 합산 finding(직접 correctness finding + simplicity 반환)을 dedup하지 않고, Low를 제외해 **Critical+High ≥ 3 또는 Medium ≥ 5**인지 판정한다.
    3. **gate 2 → fix 2**: 임계값에 도달한 경우에만 같은 `implementation-review`를 두 번째 호출한다. Critical/High/Medium을 직접 반영하고 Low에는 gate 1과 동일한 렌즈별 정책을 적용한다.
    4. **fix 검증 후 종료**: 각 fix는 **§4 커버리지 델타 → 회귀 재실행 → 변경된 AC 증거 갱신** 순서로 닫는다. fix 2 뒤에는 gate 2 finding별 표적 검증까지 수행하고, 해소되지 않은 finding을 남긴 채 종료한다. 세 번째 gate는 호출하지 않는다. gate 2의 fix 전 raw 합산 finding도 같은 임계값에 도달하면 마감 요약에서 후속 `implementation-review` 1회 수동 실행을 권고한다.
4. **마감 요약**: 계약 오류 선언·대상 파일 밖 수정이 있었으면 요약한다. gate 2를 실행했으면 호출 1/2의 severity·fix·검증과 해소되지 않은 finding을 구분하고, 실행하지 않았으면 gate 1 결과만 보고한다.

## Integration

- `feature-draft`: 주 입력 — draft Part 2의 task를 소비한다. 계약 오류 반복 시 복귀 대상이기도 하다.
- `implementation-review`: 마감 품질 게이트 — 이 스킬이 소유한다 (마감 3 참조).
- `spec-sync`: 구현이 spec에 반영될 변경이면, draft Part 1 마커 내용과 실제 변경을 입력으로 global spec을 동기화한다.
