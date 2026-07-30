# Feature Draft: implementation 커버리지 델타 단계

> 규모 판정: 적격 — 변경 요소는 `implementation` SKILL.md 미러 2개의 Process 절 1개 추가이고, 변경 요소↔task 대응이 1:1로 눈검산된다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

`implementation` 스킬의 test-first 규율에 **커버리지 델타** 단계를 추가한다. 기존 규율에서 테스트 집합은 AC의 함수였다 — RED는 "AC가 요구하는 동작의 미충족"만 관찰하고, GREEN에서 코드가 AC보다 넓어진 부분(분기·경계값·에러 경로·기존 호출부 적응)은 어떤 테스트도 고정하지 않은 채 남았다. 마감 증거 테이블도 AC 단위라 그 확장분은 등장조차 하지 않고, `implementation-review-agent`는 AC verdict ledger 기반 + 읽기 범위 계단(AC 밖 탐색적 읽기 금지)이라 구조적 사각지대였다.

- **새 contract**: task별 GREEN 통과 직후, 그 task에서 변경한 파일의 **diff를 실제로 실행해 읽고**, 그 출력을 기준으로 방금 통과시킨 테스트/check가 도달하지 않는 동작을 열거한다(기억 기반 회상 금지). 열거된 각 항목은 기존 §1 Triage 기준을 그대로 적용해 닫는다((a)/(b)는 테스트 추가, (c)는 근거 1줄).
- **새 contract**: 델타로 추가하는 테스트는 코드가 이미 존재하므로 RED를 관찰할 수 없다. 대신 **변이 확인**(대상 동작을 일시적으로 깨서 실패 관찰 → 복구 → 해당 테스트 재실행으로 통과 재확인)으로 판별력을 증명한다 — 이것이 없으면 델타 테스트는 코드를 보고 짜맞춘 무조건 통과 테스트로 퇴화한다.
- **새 contract**: 변이 확인을 통과한 델타 테스트에도 테스트 불변 규칙(약화·수정 금지)이 동일하게 적용된다 — 불변 규칙의 트리거는 "RED 관찰 후"였고 델타 테스트는 정의상 RED가 없어 문면상 보호 밖이었다.
- **새 contract**: 델타 처리 결과는 마감 증거 테이블에 AC 유래 행과 같은 형식으로 실린다(테이블 스키마 무변경). **델타가 없으면 아무것도 적지 않는다** — "델타 없음" 같은 통과 문구는 두지 않는다(형식적 통과 문구로 전락할 표면 자체를 만들지 않는다).
- test-first canonical surface의 순서 서술이 `triage → RED → GREEN → 마감`에서 `triage → RED → GREEN → 커버리지 델타 → 마감`으로 바뀐다. 대상 표면: `_sdd/spec/main.md` Guardrails의 `implementation` test-first 항목 · `_sdd/spec/main.md` §3 주요 결정 표 `implementation test-first` 행 · `_sdd/spec/components.md`의 `implementation` 컴포넌트 행 · `_sdd/spec/components.md` Strategic Code Map의 `Implementation contract` 행(triage·RED·불변 규칙·마감을 전수 열거하므로 델타 추가 시 불완전해진다).

## Scope

- **In**: `.claude/skills/implementation/SKILL.md` · `.codex/skills/implementation/SKILL.md` Process 절에 커버리지 델타 단계 추가(미러 identical 유지), 후속 절 번호 이동.
- **Out**:
  - `## 마감` 절은 건드리지 않는다 — 증거 테이블 스키마가 그대로이므로 델타 행 수용은 신설 절 안의 1문장으로 처리한다(편집 표면 최소화).
  - 중단·분할 규칙에 "델타가 반복적으로 크다 = 계획 문제" 신호를 추가하지 않는다 — 아직 관측되지 않은 실패 모드이고, 기존 규칙 2(계약 오류 반복)로 이미 계획 문제를 잡는다(YAGNI).
  - `implementation-review` / reviewer agent 변경 없음 — 델타는 구현 시점에 닫히므로 리뷰 렌즈를 넓히지 않는다(읽기 범위 계단 원칙 유지).
  - 새 agent·새 파일·새 artifact 없음.
  - `feature-draft`·`sdd-autopilot`·`docs/AUTOPILOT_GUIDE.md`(ko·en)·`usage-guide.md`의 `RED→GREEN` 축약 표기는 변경하지 않는다 — 델타 추가 후에도 그 축약은 여전히 참이다.
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: implementation SKILL.md에 커버리지 델타 단계 추가 (미러 2개 대칭)

GREEN 직후 지점에 Process 절 하나를 신설한다. 지점이 GREEN 직후여야 하는 이유는 마감으로 미루면 전체 GREEN 통과 후라 코드를 보고 짜맞춘 테스트가 되고, 리뷰로 미루면 fix 1회 타이밍이라 늦기 때문이다.

**Contracts**:
- 신설 절은 Process의 **4번**이고, 기존 `### 4. 테스트 불변 규칙`은 **5번**으로 번호만 이동한다(본문 무변경).
- 절 본문은 다음 5요소를 담는다 — (i) **diff를 실제로 실행해 읽으라는 행위 지시**(근거 규정이 아니라 행위 의무), (ii) 열거 항목의 처리 분류는 **§1 Triage 기준 재사용**(기준을 재정의하지 않는다), (iii) 델타 테스트는 RED 대신 **변이 확인**(파괴 → 실패 관찰 → 복구 → 재실행 통과 재확인)으로 판별력 증명, (iv) 델타 테스트에도 **§5 테스트 불변 규칙이 동일 적용**됨을 명시, (v) **델타가 없으면 무출력**(통과 문구 없음).
- 델타로 추가한 테스트는 마감 증거 테이블에 AC 유래 행과 같은 형식으로 싣는다(테이블 스키마는 바꾸지 않는다).

**Acceptance Criteria**:
- [ ] AC1: `.claude/skills/implementation/SKILL.md`의 Process 절 헤딩이 위에서부터 `### 1. Triage` → `### 2. RED` → `### 3. GREEN` → `### 4. <커버리지 델타 절>` → `### 5. 테스트 불변 규칙` 순서로 나타난다 (`grep -n '^### '` 출력으로 판정).
- [ ] AC2: 신설 절 본문에서 Contracts의 5요소가 각각 문장으로 확인된다 — (i)은 "diff 실측이 근거다" 같은 명사형이 아니라 **diff 실행을 지시하는 동사형 문장**이어야 충족이다. 5개 중 하나라도 없거나 (i)이 명사형이면 미충족 (절 본문 인용으로 판정).
- [ ] AC3: 기존 `테스트 불변 규칙` 절의 본문(헤딩 줄 제외)이 변경 전과 문자 단위로 동일하다 (`git diff` 상 해당 절에서 헤딩 줄 1개 외 변경 없음).
- [ ] AC4: `diff .claude/skills/implementation/SKILL.md .codex/skills/implementation/SKILL.md`의 exit code가 0이다.

**Target Files**:
- [M] `.claude/skills/implementation/SKILL.md` -- Process 절 신설 + 후속 절 번호 이동
- [M] `.codex/skills/implementation/SKILL.md` -- 위와 identical 미러

### Task 2: 신설 절을 완료된 실제 task에 회고 적용해 실효 1회 관찰 (read-only)

Task 1의 AC는 텍스트 속성만 판정하므로, 절 문면이 실제로 "AC 유래 테스트가 도달하지 않은 동작"을 끌어내는지는 관찰되지 않는다. 이미 끝난 task 1건에 절차를 그대로 돌려 그 공백을 메운다. 코드/문서를 수정하지 않는다.

**Acceptance Criteria**:
- [ ] AC1: `_sdd/work_log/`에 기록된 완료 task 중 **AC 유래 테스트 또는 structural-check가 실제로 존재했던 task 1건**을 지정하고, 그 task의 커밋 diff를 실행해 읽은 뒤 신설 절 절차대로 델타 항목을 열거한다. 증거는 (지정한 task·커밋 해시, diff 명령 출력, 열거 항목별 근거 hunk)다.
- [ ] AC2: 열거 결과가 0건이면 "왜 0건인가"(그 task의 구현이 AC 범위를 넘지 않았음)를 diff 근거로 1줄 판정해 남긴다 — 0건 자체는 미충족이 아니지만 근거 없는 0건은 미충족이다.

**Target Files**:
- 없음 (read-only 검증)

### Task 3: Process 절 순서를 열거하는 표면 census (read-only 검증)

절 하나가 늘어나면서 stale해질 표면을 전수 확인한다. 축약 표기(`RED→GREEN`)는 여전히 참이므로 대상이 아니고, **순서·구성요소를 열거하는** 서술만 대상이다.

**Acceptance Criteria**:
- [ ] AC1: `.claude/`·`.codex/`·`docs/`·`README.md`·`AGENTS.md`·`_sdd/spec/`(단 `_sdd/spec/prev/` 제외) 범위에서 `RED`·`GREEN`·`Triage`·`test-free`·`structural-check` 변형을 grep하고, 출력 전량을 "순서/구성요소 열거" 대 "축약 표기"로 분류한다.
- [ ] AC2: live 표면(`.claude/`·`.codex/`·`docs/`·`README.md`·`AGENTS.md`) 중 열거형 서술을 가진 파일이 `implementation` SKILL.md 미러 2개뿐임을 AC1 분류 결과로 확인한다. 추가 표면이 발견되면 그 목록과 함께 미충족으로 보고한다(이 draft 범위 밖 처리).
- [ ] AC3: `_sdd/spec/` 안의 열거형 서술을 파일·행 번호로 열거해 `spec-sync` 인계 목록으로 남긴다. 목록은 Part 1이 명시한 4개 표면을 최소한 포함해야 한다 — 누락되면 미충족. 이 task는 spec을 수정하지 않는다.

**Target Files**:
- 없음 (read-only 검증)

# Open Questions

- **변이 확인의 작업 트리 오염**: 구현 파일을 일시적으로 깨는 행위라 되돌림 실패 위험이 있다. 완화로 "복구 후 해당 테스트 재실행 통과 재확인"을 절차에 넣었다. 대안(무조건 통과 테스트 허용)이 이 feature의 목적을 무력화하므로 채택했다. 사용자 확인 불요.
- **accepted trade-off — 무출력의 대가**: 델타 0건일 때 무출력이므로 이 단계의 **스킵과 0건은 사후 구분되지 않는다**(RED의 실패 출력 캡처, 계약 오류의 선언 아티팩트와 달리 수행 흔적이 없다). `implementation-review`도 AC verdict ledger 기반이라 수행 여부를 볼 수 없다. 강제력은 (i) diff 실행 행위 의무와 (ii) 델타 발견 시 증거 테이블 노출에만 의존한다. 통과 문구를 되살리는 대신 이 한계를 명시 수용한다. 사용자 확인 불요.
- **advisory (미반영)**: Part 1 Change Summary와 Task 1 Contracts가 같은 요소를 두 번 서술한다(plan-review Low). Part 1은 spec-sync 입력이라 독립적으로 읽혀야 하고 Task 1 Contracts는 AC2의 판정 대상이라, 양쪽 모두 필요하다고 판단해 유지했다.
