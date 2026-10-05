# Feature Draft: 오케스트레이터 기반 multi-agent 하네스 — 신 경로 추가 (Feature A)

> 규모 판정: 분할 필요 — 분할 계획 포함. 재편 전체(신 경로 추가 + 실측 + 기본 경로 교체·구 경로 삭제·참조 sweep·spec 재작성)는 요소↔task 대응을 한 draft로 눈검산할 수 없고, 교체는 실측 합격(goal R4)이 선행 조건이라 시점도 다르다. 이 draft의 Part 2는 Feature A(신 경로를 구 경로 옆에 추가)만 다룬다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
SDD 체인(feature-draft → plan-review → implementation → implementation-review → spec-sync)을 오케스트레이터 스킬 `sdd-orchestrator`가 지휘하는 multi-agent 경로를 추가한다. 동기는 메인 맥락 보호와 병렬 벽시계 단축이고, 과거 agent 경로의 폐지 원인(맥락을 다시 파악하는 비용)은 레시피형 digest로 해소됐다(2026-10-04 cold start 실측). 결정 출처는 `_sdd/discussion/2026-10-04_discussion_orchestrator_harness_redesign.md`(결정 1~6)다.

새 contract/invariant:
- 오케스트레이터(메인 루프)는 단계 순서·게이트 루프·병렬 판단·사용자 질문을 소유하고, 대상 파일(코드·테스트·draft·spec)을 직접 수정하지 않는다. 쓰는 파일은 digest·state·work log뿐이다.
- 단계 작업은 worker가 `sdd-orchestrator/references/workers/<단계>.md` 계약을 읽고 수행한다. worker는 사용자에게 질문하지 않고, git 쓰기를 하지 않으며, 하위 worker를 띄우지 않는다.
- 인계는 2파일이다. digest(방법·이유: 결정·환경 함정·검증 레시피)는 모든 worker가 읽는다. state(단계·task 상태·RED/GREEN 신호·게이트 결과·AC→증거)는 오케스트레이터 재개용이고 리뷰 worker에게 주지 않는다. 둘 다 오케스트레이터가 단일 작성자이며 worker는 반환의 `digest 변경분`으로만 바꾼다. 위치는 `_sdd/implementation/<YYYY-MM-DD>_<slug>/{digest.md,state.md}`이고, 기존 implementation ledger의 역할을 state가 흡수한다.
- 구현은 task별 worker다. Target Files가 서로소이고 `Contracts`를 공유하지 않으며 산출물 의존이 없는 task만 같은 작업 트리에서 병렬로 띄운다. 병렬 상한은 두지 않고 런타임에 맡긴다.
- 리뷰 worker는 작성 worker와 분리된 새 worker다. 전체 회귀는 리뷰 worker가 digest 검증 레시피를 fresh 실행해 대신한다. 게이트 정책(gate 1+fix 1, fix 전 raw `Critical+High ≥ 3 또는 Medium ≥ 5`면 gate 2+fix 2, gate 3 없음)은 구 경로와 같고 소유자만 오케스트레이터로 옮긴다.
- Feature A 동안 신 경로는 구 경로 옆에 있는 실험 경로다. 구 단계 스킬의 동작은 바꾸지 않는다.

분할 계획(롤링):
- **Feature A — 신 경로 추가** (이 draft): `sdd-orchestrator` 스킬(Claude·Codex)과 handoff 템플릿, 단계별 worker 계약 5종, Claude marketplace 등록, smoke 검증. 구 경로 불변.
- **Feature B — 교체와 구 경로 삭제** (goal R4 실측 합격 후): `sdd-orchestrator`를 SDD 체인의 기본 진입점으로 만들고, 구 직접 실행 단계 스킬(`feature-draft`·`plan-review`·`implementation`·`implementation-review`·`spec-sync`, 양 런타임)을 삭제한다. simplicity 계약 reference를 `sdd-orchestrator`로 옮기고 `pr-review` 포인터를 갱신한다. 하네스 템플릿(AGENTS ×4 미러)·goal-init SDD Loop Protocol·sdd-autopilot·spec 계열 스킬·docs·README·AGENTS.md의 참조를 census로 정리한다. spec Guardrails·결정을 새 하네스 기준으로 다시 쓴다(goal R5 census 포함).

## Scope
- **In**: `.claude/skills/sdd-orchestrator/`·`plugins/sdd-skills-codex/skills/sdd-orchestrator/` 신규(SKILL.md, `references/handoff-templates.md`, `references/workers/` 5종), `.claude-plugin/marketplace.json` 등록, goal 벤치마크용 smoke 스크립트
- **Out**: 구 단계 스킬 수정·삭제와 참조 sweep(Feature B), spec Guardrails 재작성(Feature B의 spec-sync), Codex 실측(정적 검사만), discussion 스킬(오케스트레이터가 직접 수행하는 기존 경로 유지), `pr-review`
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: 오케스트레이터 스킬과 handoff 템플릿 (Claude)
메인 루프가 지휘만 하고 단계 작업은 worker에게 맡기는 진입 스킬을 만든다. 역할 경계·dispatch 형식·게이트 루프·병렬 규칙·재개가 이 파일 하나에 있다.

**Contracts**:
- 진입: 요청만 있으면 feature-draft부터, draft 경로가 있으면 state나 사용자 말로 plan-review 완료가 확인될 때 implementation부터(아니면 plan-review부터), 사용자가 단계만 지정하면(예: "spec-sync만", "리뷰만") 그 단계만 실행한다. 기본 종점은 spec-sync 완료이고, 사용자가 종점을 지정하면 그 단계에서 멈춘다. discussion은 이 스킬 밖(기존 스킬)이며, discussion 파일은 입력 포인터로만 쓴다.
- 오케스트레이터가 직접 하는 일: 사용자 질문(아키텍처·범위·Target Files를 바꾸는 unknown만, 계획 worker를 띄우기 전), digest·state 작성, 단계·게이트 순서와 병렬 판단, worker 반환 집계, work log append, 마감 보고. 하지 않는 일: 대상 파일 수정, worker 일의 대리 수행(실패해도 대신 고치지 않는다), git 쓰기(사용자가 따로 요청할 때만).
- digest 초기화: 계획 단계를 거치면 feature-draft worker 반환의 `digest 변경분`으로 만든다. draft로 진입하면 draft AC의 검증 명령, `_sdd/env.md`, 대화에서만 나온 결정으로 오케스트레이터가 만든다. 이때 대상 파일을 탐색하지 않는다.
- 병렬 규칙: task worker는 task당 1개다. Target Files가 서로소이고, `Contracts`를 공유하지 않고, 산출물 의존(선행 task)이 없는 task들만 한 번에 동시에 띄운다. 나머지는 의존 순서대로 띄운다. 동시 실행 수 상한은 두지 않고 런타임에 맡긴다.
- dispatch prompt 형식(모든 worker 공통, SKILL.md가 단일 소스): ① 역할 1줄(`너는 sdd-orchestrator가 띄운 <단계> worker다`) ② 계약 파일 절대 경로(Read해서 따른다) ③ digest 절대 경로 ④ 입력(draft 경로·task ID·리뷰 범위·fix할 findings 등) ⑤ 공통 경계 5줄 — 사용자 질문 금지(필요한 결정은 합당한 해석+반환에 기록, 진행 불가면 BLOCKED 반환) / git 쓰기 금지 / 지정 대상 밖 파일 수정 금지(동시 실행 중인 다른 worker의 Target Files를 함께 알려 준다) / state.md·digest 쓰기 금지(리뷰 worker — plan-review·implementation-review·simplicity — 는 state.md 읽기도 금지) / 하위 worker 금지 ⑥ 반환은 계약의 `반환` 형식 + 끝에 `digest 변경분` 블록(없으면 "없음").
- 게이트 루프: 계획 = feature-draft worker → plan-review worker(별도 새 worker) → fix는 feature-draft worker를 findings와 함께 다시 띄운다. 구현 = task worker들 → implementation-review(correctness worker 1 + simplicity worker 2묶음, 동시) → fix는 해당 파일을 가진 task worker를 findings와 함께 다시 띄운다. simplicity worker도 다른 worker처럼 계약 파일(`implementation-review/references/simplicity-contract.md`) 경로를 Read하고, 입력으로 차원 묶음 한정(참조 ∥ 국소)을 받는다. fix 정책·gate 2 임계·gate 3 없음은 Change Summary와 같다. 임계 판정은 오케스트레이터가 fix 전 raw 수치로 한다.
- 실패: worker가 실패·무응답이면 같은 입력으로 1회 다시 띄우고, 또 실패하면 멈추고 보고한다. task worker가 계약 오류를 2회 선언(BLOCKED)하면 그 task를 계획 단계로 되돌린다.
- 재개: state를 읽어 다음 행동을 정한다. DELTA_CLOSED가 아닌 task는 state를 믿지 않고 worker가 fresh 재판정한다.
- 마감: AC→증거(리뷰 worker의 fresh verdict 포인터)를 state에 쓰고, 게이트 호출별 severity·fix·검증과 사용자 확인 필요 항목만 채팅에 보고한다.
- 런타임 차이(dispatch 도구 이름·동시 실행·완료 수거)는 `## Runtime: worker dispatch` 절 하나에만 둔다(Task 4의 미러 기준선 근거).
- handoff 템플릿: `# Digest:`(출처 포인터 / 결정·제약 / 환경 함정 / 검증 레시피 `AC → 명령 → 기대값`; 상태·통과 주장·이력 없음)과 `# State:`(출처·base commit·시작 시 dirty 범위·현재 단계 / task 표 `Task | 담당 | 상태 | triage | RED·GREEN 명령과 신호 | 계약 오류 선언` / 게이트 표 / 계획 이탈·발견 `내용 → 이유 → 처리` / AC→증거 표) fenced template 두 개.

**Acceptance Criteria**:
- [ ] AC1 (1등급): `test -f` 로 `.claude/skills/sdd-orchestrator/SKILL.md`·`references/handoff-templates.md` 존재, `grep -c '^name: sdd-orchestrator$' SKILL.md` = 1, `grep -n '^## Runtime: worker dispatch$' SKILL.md` 1건.
- [ ] AC2 (1등급): handoff-templates.md에 fenced template 두 개의 첫 줄 `# Digest:`·`# State:`가 각 1건이고, Digest 템플릿 구간(`# Digest:`~다음 fence)의 필드 머리(`^#` heading 줄과 `^|` 표 줄)에 `상태`·`MET`·`PASS`가 0건이다(`awk`로 구간 추출 → `grep -E '^(#|\|)'` → `grep -c`).
- [ ] AC3 (2등급): reviewer가 SKILL.md를 위 Contracts의 9개 항목(진입과 종점·직접 하는 일/하지 않는 일·digest 초기화·병렬 규칙·dispatch 형식 6요소·게이트 루프·실패·재개·마감)과 대조해 항목마다 해당 문장의 인용(content anchor)을 댈 수 있다. 하나라도 없으면 FAIL.

**Target Files**:
- [C] `.claude/skills/sdd-orchestrator/SKILL.md` -- 새 진입 스킬(기존 스킬 수정으로는 구 경로 불변 제약을 지킬 수 없다)
- [C] `.claude/skills/sdd-orchestrator/references/handoff-templates.md` -- 오케스트레이터가 작성 직전에 읽는 digest·state 템플릿(SKILL.md 본문에 두면 매 호출 맥락에 실린다)

### Task 2: 계획 단계 worker 계약 2종 (Claude)
기존 `feature-draft`·`plan-review` SKILL.md를 worker 계약으로 옮긴다. 철학 규칙(falsifiable AC 2등급, Target Files 실측, Minimum-Code, 분할 규칙, 5-smell rubric, 외부 사실 대조 바닥)은 그대로 두고, 메인 루프·사용자 대화·게이트 소유 문장만 바꾼다.

**Contracts**:
- `workers/feature-draft.md`: 원본에서 Process 1·3·4·5, 분할 규칙, Required Output fenced template(verbatim), 규칙(AC·Target Files·Minimum-Code·마커 보존)을 유지한다. `핵심 질문`(사용자 질문)은 "질문하지 않고 합당한 해석을 택해 Open Questions에 결정과 `사용자 확인 필요` 여부를 적는다"로 바꾼다. `품질 게이트`·`실행 인계`·`Integration`은 삭제한다(오케스트레이터 소유). fix 모드: 입력에 findings가 오면 같은 draft를 고치고 반영·미반영 사유를 반환한다. 반환 = draft 경로 / 규모 판정 / task 표(`Task | Target Files | 선행 task | Contracts 공유 여부`) / 사용자 확인 필요 Open Questions / `digest 변경분`(AC별 검증 명령과 기대값, 확인한 환경 함정).
- `workers/plan-review.md`: 원본의 Input·읽기 지침·5-smell rubric·Severity·Blocker Policy·반환을 유지한다. "메인 루프가 직접 수행"을 worker 수행으로 바꾸고 `Integration`을 삭제한다. state.md를 읽지 않는다.

**Acceptance Criteria**:
- [ ] AC1 (1등급): 두 파일에서 `grep -c '메인 루프'` = 0, `grep -c 'AskUserQuestion\|사용자에게 묻\|한 번에 하나씩'` = 0, feature-draft.md에 `spec-update-todo-input-start` 1건 이상, plan-review.md에 `외부 사실` 1건 이상.
- [ ] AC2 (1등급): feature-draft.md의 Required Output fenced template이 원본(`.claude/skills/feature-draft/SKILL.md`)의 것과 같다 — 두 파일에서 fence 구간을 추출해 `/usr/bin/diff` 무출력.
- [ ] AC3 (1등급): 두 파일 모두 `## 반환` 절이 있고 feature-draft.md 반환에 `digest 변경분`이 있다(`grep -n`).

**Target Files**:
- [C] `.claude/skills/sdd-orchestrator/references/workers/feature-draft.md` -- 계획 worker 계약
- [C] `.claude/skills/sdd-orchestrator/references/workers/plan-review.md` -- 계획 리뷰 worker 계약

### Task 3: 구현·리뷰·sync 단계 worker 계약 3종 (Claude)
기존 `implementation`·`implementation-review`·`spec-sync` SKILL.md를 worker 계약으로 옮긴다. TDD 규율(Triage·RED·GREEN·커버리지 델타·테스트 불변·시간 제한·read-only 검증 경로), fresh verification·읽기 계단·severity, spec-sync routing은 그대로 둔다.

**Contracts**:
- `workers/implementation.md`: 범위는 입력으로 받은 task 하나(또는 fix할 findings)다. 원본의 Process(시간 제한, read-only 검증 task, §1~§5)를 유지한다. 작성자 불변식("메인 루프가 직접 작성")·Implementation Ledger·마감(회귀·AC 표·게이트·요약)·중단·분할 규칙 1·Integration을 삭제한다. 계약 오류 선언이 같은 task에서 2회면 멈추고 BLOCKED로 반환한다. fix 모드: findings 반영 → §4 커버리지 델타 → 표적 test/check 재실행. 반환 = task별 `상태(DELTA_CLOSED|BLOCKED|READY+사유) | triage와 근거 | RED 명령·신호 | GREEN 명령·신호 | 델타 처리 | 계약 오류 선언 | 대상 밖 수정 필요` + `digest 변경분`.
- `workers/implementation-review.md`: correctness 렌즈만 담는다. 원본의 기준 문서 적응·읽기 범위 3단 계단·Fresh Verification(+ digest 검증 레시피 전체 fresh 실행으로 회귀 대신)·Findings 분류·보고(simplicity 항목 제외)를 유지한다. simplicity dispatch·`--model`·Integration을 삭제한다. state.md와 구현 worker의 통과 주장을 읽지 않는다. simplicity는 오케스트레이터가 기존 `implementation-review/references/simplicity-contract.md`로 따로 띄운다(Feature B에서 이동).
- `workers/spec-sync.md`: 원본 전체를 유지하고 "메인 루프가 직접 수행"만 worker 수행으로 바꾼다. Input Sources에 `_sdd/implementation/<YYYY-MM-DD>_<slug>/state.md`를 구현 증거로 추가한다. 반환 = 바뀐 spec 파일 / 새 Spec Version / routing 요약(승격·Planned·보류 수) / Open Questions / rename한 입력 파일.

**Acceptance Criteria**:
- [ ] AC1 (1등급): 세 파일에서 `grep -c '메인 루프'` = 0. implementation.md에 `RED`·`커버리지 델타`·`변이 확인`·`BLOCKED` 각 1건 이상, `ledger` 0건.
- [ ] AC2 (1등급): implementation-review.md에 `state.md` 문장(읽지 않는다)이 있고 `simplicity-contract`·`--model` 0건, `MET — ` 1건 이상.
- [ ] AC3 (1등급): spec-sync.md에 `state.md` 1건 이상, `Repo-wide Invariant Test`·`🚧 Planned` 각 1건 이상.
- [ ] AC4 (1등급): 세 파일 모두 `## 반환` 절이 있고 implementation.md 반환에 `digest 변경분`이 있다.

**Target Files**:
- [C] `.claude/skills/sdd-orchestrator/references/workers/implementation.md` -- task worker 계약
- [C] `.claude/skills/sdd-orchestrator/references/workers/implementation-review.md` -- correctness 리뷰 worker 계약
- [C] `.claude/skills/sdd-orchestrator/references/workers/spec-sync.md` -- spec-sync worker 계약

### Task 4: Codex 미러
Claude 쪽 `sdd-orchestrator` 전체를 Codex 플러그인에 미러한다. worker 계약과 템플릿은 런타임 중립 어휘로 쓰여 그대로 복사하고, SKILL.md는 `## Runtime: worker dispatch` 절만 Codex spawn 방식(기존 implementation-review Codex 미러의 Mailbox / Target-close 두 contract, `fork_turns: "none"`, 동시 상한에 걸리면 끝난 worker 뒤에 이어서 띄움)으로 바꾼다.

**Acceptance Criteria**:
- [ ] AC1 (1등급): `/usr/bin/diff -r .claude/skills/sdd-orchestrator/references plugins/sdd-skills-codex/skills/sdd-orchestrator/references` 무출력.
- [ ] AC2 (1등급): 두 SKILL.md의 `/usr/bin/diff` hunk 수(`grep -c '^[0-9]'`) = 1이고, 그 hunk의 claude 쪽 줄 범위가 `## Runtime: worker dispatch` 절 안에 있다.
- [ ] AC3 (1등급): Codex SKILL.md의 Runtime 절에 `fork_turns` 1건 이상, `Agent(` 0건.

**Target Files**:
- [C] `plugins/sdd-skills-codex/skills/sdd-orchestrator/SKILL.md` -- Codex 진입 스킬
- [C] `plugins/sdd-skills-codex/skills/sdd-orchestrator/references/handoff-templates.md` -- 동일 복사
- [C] `plugins/sdd-skills-codex/skills/sdd-orchestrator/references/workers/{feature-draft,plan-review,implementation,implementation-review,spec-sync}.md` -- 동일 복사

### Task 5: Claude marketplace 등록
Claude 플러그인은 `marketplace.json`의 skills 배열에 명시된 스킬만 로드한다(Codex는 `skills/` 디렉터리 자동 탐색이라 변경 없음).

**Acceptance Criteria**:
- [ ] AC1 (1등급): `jq -r '.plugins[0].skills[]' .claude-plugin/marketplace.json | grep -c '^./.claude/skills/sdd-orchestrator$'` = 1, `claude plugin validate .` 출력에 `Validation passed`.

**Target Files**:
- [M] `.claude-plugin/marketplace.json` -- skills 배열에 `./.claude/skills/sdd-orchestrator` 추가

### Task 6: headless smoke 검증
신 경로가 실제로 worker를 띄우고 오케스트레이터가 대상 파일을 직접 고치지 않는지, 비싼 벤치마크 전에 작은 고정 과제로 확인한다. 이 스크립트는 goal 벤치마크 도구라 goal 디렉터리에 둔다.

**Contracts**: `smoke.sh <harness plugin dir>`는 scratch git repo(파일 1개 + task 1개짜리 draft, AC는 `grep` 1줄)를 만들고 `claude -p --plugin-dir <harness>`로 `sdd-skills:sdd-orchestrator`를 implementation부터 spec-sync 없이(종점=implementation-review) 실행한다. 출력은 `metrics.py`와 같은 형식의 한 줄 JSON + digest·state 존재 여부 + AC grep 결과다.

**Acceptance Criteria**:
- [ ] AC1 (1등급, 느린 검증 — 마감 checkpoint에서 1회): `smoke.sh <브랜치 스냅샷>` 결과에서 `_sdd/implementation/*/digest.md`·`state.md` 존재, `workers` ≥ 2(task worker + 리뷰 worker), `M2_main_edits` = 0, 과제 AC grep 통과.

**Target Files**:
- [C] `_sdd/goal/2026-10-04_orchestrator_harness_redesign/bench/smoke.sh` -- smoke 실행기

### Task 7: 구 경로 불변·정적 검사 census (read-only)
Feature A가 구 경로를 건드리지 않았고 정적 검사가 깨끗한지 전수로 닫는다.

**Acceptance Criteria**:
- [ ] AC1 (1등급): `git diff main -- .claude/skills/{feature-draft,plan-review,implementation,implementation-review,spec-sync} plugins/sdd-skills-codex/skills/{feature-draft,plan-review,implementation,implementation-review,spec-sync}` 무출력.
- [ ] AC2 (1등급): `git diff --check main...HEAD` 와 `git diff --check` 무출력.

**Target Files**:
- 없음 (read-only 검증)

# Open Questions
- 스킬 이름은 `sdd-orchestrator`로 정했다(기존 `sdd-autopilot`과 같은 접두, 역할이 이름에 드러남). 사용자 확인 불필요.
- worker 계약을 단계 스킬과 같은 이름(`workers/<단계>.md`)으로 둬서 docs의 단계 이름 언급("spec-sync 단계")이 Feature B 뒤에도 유효하게 했다. 사용자 확인 불필요.
- 토론의 "단계 경계에서 오케스트레이터가 커밋" 기본값은 따르지 않는다. 커밋은 사용자 요청 시에만이라는 전역 규범과 구 경로 동작(커밋 없음)에 맞췄고, worker git 쓰기 금지는 유지한다. 사용자 확인 불필요(되돌리기 쉬움).
- simplicity 리뷰는 Feature A에서 기존 `implementation-review/references/simplicity-contract.md`를 그대로 가리킨다. 복사본을 만들지 않고 Feature B에서 옮긴다. 사용자 확인 불필요.
