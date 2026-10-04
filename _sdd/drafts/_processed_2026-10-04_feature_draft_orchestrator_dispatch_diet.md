# Feature Draft: worker dispatch 다이어트 — foreground 실행과 공통 경계 파일 (Feature A3)

> 규모 판정: 적격 — 변경 요소 2개(Claude Runtime 절의 실행 방식, dispatch 템플릿의 공통 경계 블록 → reference 파일)와 Codex 미러 복사, task 2개로 눈검산 가능.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
F5 2회차(v2, b83fbcd)에서 87은 M1 59.0k·62.1k(합격선 73k)로 여유가 있으나 88은 87.9k(합격선 88.5k)로 여유가 0.6k뿐이고, fix가 많은 run(88-new-4, worker 14개 이상)은 넘을 수 있다. 88-new-3 transcript 분해에서 오케스트레이터 맥락의 큰 비중이 worker 결과가 아닌 포장에서 나왔다: Claude에서 worker를 `run_in_background: true`로 띄워 dispatch마다 "Async agent launched" 안내문 약 1.2k자와 완료 알림 포장이 쌓였고(12회 약 18k자), dispatch prompt마다 공통 경계 5줄(약 550자)이 반복됐다(12회 약 6.6k자, 오케스트레이터 출력이라 벽시계도 늘림).

새 contract/invariant: worker 공통 경계의 단일 소스는 `sdd-orchestrator/references/worker-boundary.md`다(dispatch prompt는 경로만 준다).

## Scope
- **In**: `sdd-orchestrator` SKILL.md(Worker dispatch 템플릿, Claude Runtime 절), `references/worker-boundary.md` 신규, Codex 미러(Runtime 절 밖 동일 반영 + reference 복사)
- **Out**: worker 계약 본문, 게이트 정책, Codex spawn 방식
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: 공통 경계를 reference 파일로 옮긴다
**Contracts**: `references/worker-boundary.md`는 지금 템플릿의 공통 경계 5줄(사용자 질문 금지·BLOCKED, git 쓰기 금지, 대상 밖 수정 금지, state.md·digest 쓰기 금지 + 리뷰 worker(plan-review·implementation-review·simplicity)는 state.md 읽기도 금지, 하위 worker 금지)과 반환 규칙(계약의 반환 형식 + `digest 변경분` 블록, 계약 항목만 짧게)을 담는다. 템플릿은 `공통 경계: <worker-boundary.md 절대 경로>` 한 줄과 시작 줄(계약·공통 경계·digest·입력 문서를 한 메시지에서 함께 읽는다)로 줄인다.

**Acceptance Criteria**:
- [ ] AC1 (1등급): `test -f` 양 runtime `references/worker-boundary.md`, 그 파일에 `BLOCKED`·`git 쓰기`·`state.md`·`digest 변경분` 각 1건 이상.
- [ ] AC2 (1등급): SKILL.md `Worker dispatch` fenced 템플릿 구간에 `worker-boundary.md` 1건, `git 쓰기` 0건, `한 메시지에서 함께 읽는다` 1건.

**Target Files**:
- [C] `.claude/skills/sdd-orchestrator/references/worker-boundary.md` -- 공통 경계 단일 소스(dispatch마다 반복 출력하지 않기 위해 파일로 분리)
- [M] `.claude/skills/sdd-orchestrator/SKILL.md` -- 템플릿 축소

### Task 2: Claude worker를 foreground로 띄운다
**Contracts**: Runtime 절(Claude)은 `Agent`를 `run_in_background: false`로 띄우고, 동시에 띄울 worker는 한 메시지에 여러 호출로 내서 함께 실행하고 결과를 한 번에 받는다고 쓴다. 백그라운드 완료 알림 대기 문장은 지운다. Codex Runtime 절은 바꾸지 않는다.

**Acceptance Criteria**:
- [ ] AC1 (1등급): Claude SKILL.md Runtime 절에 `run_in_background: false` 1건, `완료 알림` 0건.
- [ ] AC2 (1등급, Task 1·2 공통): claude↔codex SKILL.md hunk 1개(Runtime 절 안), `/usr/bin/diff -r` references 무출력, `git diff --check` 무출력, Feature A structural check 42개 회귀 PASS, A2 check는 `T2.brief`(`진행 서술`)만 `references/worker-boundary.md`에서 판정하고 나머지는 그대로 PASS.

**Target Files**:
- [M] `.claude/skills/sdd-orchestrator/SKILL.md` -- Runtime 절
- [M] `plugins/sdd-skills-codex/skills/sdd-orchestrator/SKILL.md` -- Runtime 절 밖 동일 반영
- [C] `plugins/sdd-skills-codex/skills/sdd-orchestrator/references/worker-boundary.md` -- 동일 복사

# Open Questions
- 효과는 F5 3회차(v3) 실측으로 판정한다(신 경로 87·88 각 2회 재실행 — 최종 하네스 기준). 사용자 확인 불필요.
