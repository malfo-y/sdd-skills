# Feature Draft: 오케스트레이터 맥락 다이어트와 worker 시작 묶음 읽기 (Feature A2)

> 규모 판정: 적격 — 변경 요소 5개(역할 경계 읽기 범위 2문장·dispatch 템플릿 2줄·state 갱신 규칙 1문장·spec-sync 입력 1문장)가 `sdd-orchestrator` SKILL.md 한 파일(+Codex 미러 복사)에 모이고 task 2개로 눈검산 가능.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
F5 실측(신 경로 1회차)에서 M2(메인 루프 대상 쓰기 0)·M3(cold start 중앙값 ≤10s)·M4(독립 리뷰)는 합격했으나 M1(오케스트레이터 맥락 증가 ≤ 구 × 0.5)이 87 77.3k(합격선 73k)·88 91.9k(88.5k)로 근소하게 불합격했다. transcript 분해에서 줄일 수 있는 소비가 드러났다: 메인 루프가 worker 계약(`references/workers/`)을 직접 읽음(87: 약 11.7k자), 환경을 직접 탐색함, worker 반환이 평균 약 3k자로 서술을 포함함, digest·state를 heredoc으로 통째 다시 씀. 또한 worker는 계약·digest·draft를 턴마다 하나씩 읽어 시작이 7~16초 걸렸고, spec-sync worker는 구현이 끝난 draft를 `_processed_`로 rename하지 않았다(구 경로는 rename).

새 contract/invariant: 없음(기존 "메인 루프는 지휘만 한다"의 집행 세부).

## Scope
- **In**: `.claude/skills/sdd-orchestrator/SKILL.md`(역할 경계·인계 파일·Worker dispatch 절), Codex 미러 SKILL.md(Runtime 절 밖 동일 반영)
- **Out**: worker 계약 파일 변경, 게이트 정책, 구 경로
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: 메인 루프 읽기·쓰기 범위 축소와 spec-sync rename 입력
메인 루프가 worker 계약을 읽거나 환경을 탐색하지 않게 하고, state는 바뀐 부분만 고치게 하며, draft를 다 구현했으면 spec-sync worker에게 rename 대상임을 넘긴다.

**Contracts**:
- 역할 경계 "하지 않는 일"의 읽기 항목: 읽어도 되는 것은 `references/handoff-templates.md`, draft, `_sdd/env.md`, digest·state뿐이다. `references/workers/`의 계약은 worker가 읽는 문서라 메인 루프가 읽지 않는다. 환경(명령·도구·셸 동작)을 직접 탐색하지 않는다 — 환경 함정은 `_sdd/env.md`와 worker 반환의 `digest 변경분`으로 쌓는다.
- 인계 파일: digest·state는 처음 만든 뒤 바뀐 행·항목만 고친다(파일 전체를 다시 쓰지 않는다).
- spec-sync 입력: draft의 Part 2 task가 모두 닫혔고 분할 계획(남은 feature)이 없으면, spec-sync worker 입력에 "이 draft는 소비 완료 — `_processed_` rename 대상"을 넣는다.

**Acceptance Criteria**:
- [ ] AC1 (1등급): SKILL.md에서 `grep -c 'references/workers/.*읽지 않는다'` ≥ 1, `grep -c '직접 탐색'` ≥ 1, `grep -c '바뀐 행'` ≥ 1, `grep -c '_processed_'` ≥ 1.

**Target Files**:
- [M] `.claude/skills/sdd-orchestrator/SKILL.md` -- 역할 경계·인계 파일·단계와 진입 표(spec-sync 입력)

### Task 2: dispatch 템플릿에 시작 묶음 읽기와 반환 길이 규칙
worker가 계약·digest·입력 문서를 한 메시지에서 함께 읽고, 반환은 계약의 반환 항목만 짧게 쓰게 한다.

**Contracts**: `Worker dispatch` 템플릿에 두 줄을 더한다. ① `시작: 계약·digest·입력 문서를 한 메시지에서 함께 읽는다.` ② 반환 줄에 `반환 항목만 짧게 쓴다 — 진행 서술·요약·문제없이 확인한 항목은 쓰지 않는다.`

**Acceptance Criteria**:
- [ ] AC1 (1등급): SKILL.md의 `Worker dispatch` fenced 템플릿 구간(`awk`로 추출)에 `한 메시지에서 함께 읽는다` 1건, `진행 서술` 1건.
- [ ] AC2 (1등급, Task 1·2 공통): `/usr/bin/diff` claude↔codex SKILL.md hunk 1개(Runtime 절 안), `/usr/bin/diff -r` references 무출력, `git diff --check` 무출력.

**Target Files**:
- [M] `.claude/skills/sdd-orchestrator/SKILL.md` -- Worker dispatch 템플릿
- [M] `plugins/sdd-skills-codex/skills/sdd-orchestrator/SKILL.md` -- Runtime 절 밖 동일 반영

# Open Questions
- 효과는 F5 재실측(신 경로 4회)으로 판정한다. 사용자 확인 불필요.
- Task 1·2가 같은 파일을 고쳐 Target Files가 서로소가 아니므로 순서대로 구현한다. 사용자 확인 불필요.
