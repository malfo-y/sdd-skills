# Feature Draft: resume-only implementation ledger

> 규모 판정: 적격 — 변경 요소 3개(ledger 계약 본문·증거 기록처 서술·산출물 목록)가 task 3개에 1:1 대응하고 총 6파일로 단일 컨텍스트에 담긴다. 추가형 변경이라 변형 표기 전수 제거(census형) 신호 없음.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

모든 `implementation` 실행이 `_sdd/implementation/<YYYY-MM-DD>_implementation_ledger_<slug>.md` 단일 로컬 ledger를 생성·갱신한다. 목적은 감사가 아니라 **compact/세션 재개 후 다음 행동을 결정하는 resume pointer**다. 근거: 2026-08-05 토론(producer_review_alignment_and_ledger) 결정 6~9 + 사용자 승인 조정 2건.

**새 contract/invariant**:
- 같은 slug의 기존 ledger가 있으면 새로 만들지 않고 그 파일을 이어쓴다 — 날짜가 바뀐 재개에서도 ledger를 분열시키지 않는다.
- ledger는 task당 4상태 `READY → RED_CONFIRMED → GREEN_CONFIRMED → DELTA_CLOSED`만 사용한다. (c) test-free task는 RED/GREEN 단계가 없으므로 커버리지 델타를 닫으면 `READY → DELTA_CLOSED`로 직행한다.
- 기록 기준: **재실행으로 복원할 수 없는 사실만** 기록한다(triage 분류·근거, RED/GREEN 명령과 판정 신호 1줄, 계약 오류 선언 횟수, target 밖 수정, coverage delta 항목 수·처리). 명령 출력 전문·서술형 진행기는 금지한다.
- 마감 통합(조정 1): 마감의 AC→증거 테이블은 별도 산출물이 아니라 **ledger에 완성해 쓰고 채팅에 동일 표를 노출**한다 — ledger가 증거 테이블의 점진 작성본이며 기록처다(이중 작성 없음). 게이트 fix는 마지막 `Review fix delta` 블록 하나로 기록한다.
- 재개 규칙(조정 2): ledger로 상태를 복원할 때 **미완료(비 DELTA_CLOSED) task는 상태를 신뢰하지 않고 그 task의 테스트/check를 fresh 실행해 재판정**한다. DELTA_CLOSED task는 ledger를 신뢰하되 현재 diff와 모순이 보이면 fresh 실행으로 재확인한다.
- 도입 관측 exit 조건(스킬 계약 아님, decision_log 기록 대상): 도입 후 수 회의 구현에서 ledger가 실제 재개에 읽힌 적이 있는지 관측하고, 전혀 사용되지 않으면 회수를 재검토한다.

## Scope
- **In**: `implementation` SKILL 2벌의 ledger 계약 추가와 마감 절 기록처 수정, SDD_SPEC_DEFINITION 한·영의 증거 기록처 문장 갱신, AUTOPILOT_GUIDE 한·영의 산출물 목록 갱신.
- **Out**: reviewer들의 ledger 소비(fresh verification 원칙 불변 — implementation-review·simplicity·spec-sync agent 무변경), RED→GREEN·커버리지 델타 의미론, 단일 패스+fix 1회 계약, sdd-autopilot SKILL(증거 테이블의 채팅 노출이 유지되므로 relay 계약 무변경), AGENTS.md·하네스 템플릿(`_sdd/implementation/` 읽기 서술이 ledger를 이미 포괄), 실제 finding 감소 효과 측정.
<!-- spec-update-todo-input-end -->

# Propagation Surfaces

| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | ledger 계약 본문(4상태·기록 기준·재개 규칙·마감 통합) | `.claude/skills/implementation/SKILL.md`, `.codex/skills/implementation/SKILL.md` | `grep -l 'Implementation Ledger' <두 파일>` → 현재 0파일, 완료 후 2파일. 두 파일은 byte-identical 미러(`diff -q` 무출력 실측) | Task 1 |
| P2 | 증거 기록처 서술(구현 증거 테이블의 기록처 = ledger 파일) | `docs/SDD_SPEC_DEFINITION.md:171`, `docs/en/SDD_SPEC_DEFINITION.md:171` | `grep -c 'implementation ledger' <두 파일>` → 현재 각 0, 완료 후 각 1 이상 (현행 문장 앵커: ko "AC→증거 테이블과 리뷰의 verification ledger가 그 기록처다" / en "AC→evidence table and the review's verification ledger") | Task 2 |
| P3 | autopilot 산출물 목록(ledger 파일 추가) | `docs/AUTOPILOT_GUIDE.md`(28행 경량 반환 문장·69행 산출물 표), `docs/en/AUTOPILOT_GUIDE.md`(28행·69행 동형) | `grep -c 'ledger' <두 파일>` → 현재 각 0, 완료 후 각 2 이상 (앵커: ko 28행 "갱신된 spec뿐입니다"·69행 표 행 `AC→증거 테이블 | 최종 응답 (채팅)` / en 28행 "and the updated spec"·69행 `AC→evidence table | final response (chat)`) | Task 3 |

# Part 2: Tasks

### Task 1: implementation SKILL 2벌에 ledger 계약 추가

resume pointer 계약을 `## Process` 앞 독립 절로 추가하고, 마감 2(AC→증거 테이블)의 기록처를 ledger로 지정한다. 산문 규칙 우선(의사코드 금지), byte-identical 미러 유지.

**Contracts**: Part 1의 새 contract 4항(4상태·기록 기준·마감 통합·재개 규칙)에 더해 이 task가 확정하는 신규 정보 — 파일명 `_sdd/implementation/<YYYY-MM-DD>_implementation_ledger_<slug>.md`(slug는 draft slug 재사용, draft 없으면 요청 요약 snake_case), 헤더 구성(source·시작 시점 dirty paths·전체 status), 갱신 시점(각 단계 성공 직후 해당 task 행만).

**Acceptance Criteria**:
- [ ] AC1: 두 파일에 `## Implementation Ledger` 절이 있고 상태 사슬 리터럴 `READY → RED_CONFIRMED → GREEN_CONFIRMED → DELTA_CLOSED`가 존재하며, (c) task의 `READY → DELTA_CLOSED` 직행 규칙이 명시돼 있다.
- [ ] AC2: 두 파일에 기록 기준 리터럴 "재실행으로 복원할 수 없는 사실만"과 금지 리터럴("출력 전문"·"서술형 진행기")이 존재한다.
- [ ] AC3: 두 파일의 재개 규칙에 미완료 task fresh 재판정("신뢰하지 않고"+"fresh 실행")과 DELTA_CLOSED의 diff 모순 시 재확인이 모두 존재한다.
- [ ] AC4: 두 파일에서 `AC→증거 테이블`을 포함한 마감 2 문장 자체(현행 88행 앵커)에 `ledger` 리터럴이 존재한다(절-범위 아닌 문장-범위 판정) — "채팅에 노출" 문구는 유지된다.
- [ ] AC5: 두 파일이 byte-identical이다(`diff -q` 무출력).

**Target Files**:
- [M] `.claude/skills/implementation/SKILL.md` -- ledger 절 추가 + 마감 2 기록처 수정
- [M] `.codex/skills/implementation/SKILL.md` -- 동일 (byte-identical 미러)

### Task 2: SDD_SPEC_DEFINITION 한·영 증거 기록처 갱신

§6 증거 기반 결과 문장에서 구현 측 기록처를 ledger 파일로 명시한다(리뷰 측 verification ledger 서술은 무변경).

**Acceptance Criteria**:
- [ ] AC1: ko 171행 문장이 구현의 AC→증거 테이블 기록처로 `implementation ledger`를 언급하고, "리뷰의 verification ledger" 문구는 그대로 잔존한다.
- [ ] AC2: en 171행 동형 — `implementation ledger` 언급 + "the review's verification ledger" 잔존.

**Target Files**:
- [M] `docs/SDD_SPEC_DEFINITION.md` -- §6 기록처 문장 1곳
- [M] `docs/en/SDD_SPEC_DEFINITION.md` -- 동일 (영문)

### Task 3: AUTOPILOT_GUIDE 한·영 산출물 목록 갱신

경량 반환 문장(28행)과 산출물 표(69행)에 ledger 파일을 추가해 "산출물 전수" 서술이 참이 되게 한다.

**Acceptance Criteria**:
- [ ] AC1: ko — 28행 문장과 69행 표에 각각 ledger가 추가돼 `grep -c 'ledger'` ≥ 2이고, 표의 ledger 행이 `_sdd/implementation/` 경로를 지정한다.
- [ ] AC2: en — 동형(28행 문장·69행 표, `grep -c 'ledger'` ≥ 2).

**Target Files**:
- [M] `docs/AUTOPILOT_GUIDE.md` -- 경량 반환 문장 + 산출물 표
- [M] `docs/en/AUTOPILOT_GUIDE.md` -- 동일 (영문)

# Open Questions
[없음 — 방향·조정 2건(증거 테이블 통합·활성 task fresh 재판정)·exit 관측 조건은 사용자가 대화에서 확정.]
