# Feature Draft: 오케스트레이터 경로를 기본으로 교체하고 구 직접 실행 단계 스킬 삭제 (Feature B)

> 규모 판정: 적격 — 변경 요소가 파일군 8개(오케스트레이터 자체·구 스킬 삭제+marketplace·pr-review·goal 계열·하네스 템플릿·spec 계열 스킬·README·docs)로 나뉘고 요소↔task가 1:1이라 눈검산 가능. 같은 대상의 변형 표기가 여러 파일에 흩어진 census형 sweep이므로 마지막에 read-only census task를 둔다. 선행 조건: goal R4 실측 합격(신 경로).

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
실측 합격에 따라 `sdd-orchestrator`를 SDD 체인(feature-draft → plan-review → implementation → implementation-review → spec-sync)의 기본이자 유일한 실행 경로로 만들고, 메인 루프가 단계 작업을 직접 수행하던 구 단계 스킬 5종(`feature-draft`·`plan-review`·`implementation`·`implementation-review`·`spec-sync`, Claude·Codex)을 삭제한다. 단계 이름은 오케스트레이터의 단계·worker 계약 이름으로 남는다(`references/workers/<단계>.md`).

새 contract/invariant:
- SDD 체인 단계 진입은 `sdd-orchestrator` 호출이다(Claude `sdd-skills:sdd-orchestrator`, Codex `$sdd-orchestrator`, 단계만 실행할 때는 단계를 지정). discussion은 `discussion` 스킬 그대로다.
- feature draft 산출물 구조의 단일 소스는 `sdd-orchestrator/references/workers/feature-draft.md`의 Required Output이다.
- simplicity 계약의 단일 소스는 `sdd-orchestrator/references/simplicity-contract.md`이고, `sdd-orchestrator`와 `pr-review`가 소비한다.
- 재개용 구현 기록은 implementation ledger가 아니라 오케스트레이터 state(`_sdd/implementation/<YYYY-MM-DD>_<slug>/state.md`)다.

표현 치환 규칙(모든 task 공통, 단계 개념 언급은 유지):
- "`<단계>` 스킬을 호출/실행/사용" → "`sdd-orchestrator`로 `<단계>` 단계를 실행"(명령 예시는 런타임별 prefix)
- "`feature-draft`(스킬)의 Required Output" → "`sdd-orchestrator/references/workers/feature-draft.md`의 Required Output"
- "producer 스킬(`feature-draft`·`implementation`)이 게이트 소유" → "`sdd-orchestrator`가 게이트 순서와 fix를 소유"
- "implementation ledger(`*_implementation_ledger_*`)" → "오케스트레이터 state(`_sdd/implementation/<YYYY-MM-DD>_<slug>/state.md`)" — 읽는 쪽은 legacy ledger를 fallback으로 계속 읽을 수 있다

## Scope
- **In**: `sdd-orchestrator`(양 runtime) 자체 정리, 구 단계 스킬 10개 디렉터리 삭제, `.claude-plugin/marketplace.json`, `pr-review`·`goal-init`·`sdd-autopilot`·`spec-create`·`spec-upgrade`(하네스 템플릿)·`spec-review`·`spec-rewrite`·`spec-upgrade`·`spec-summary`의 참조, repo `AGENTS.md`(self-host 하네스), `README.md`, `docs/`(AUTOPILOT_GUIDE·SDD_SPEC_DEFINITION·SDD_WORKFLOW ko/en — SDD_QUICK_START·SKILL_AUTHORING_NORMS는 단계 개념 언급뿐이라 무변경)
- **Out**: `docs/reviews/`(날짜가 붙은 과거 리뷰 기록 — 역사로 보존), `tools/uninstall-codex-skill-bundle.py`(legacy 목록으로 계속 유효), global spec(`_sdd/spec/`)은 `spec-sync` 단계 소관
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: sdd-orchestrator를 기본 경로로 정리하고 simplicity 계약을 옮긴다
오케스트레이터가 구 스킬을 전제한 문장을 지우고, simplicity 계약을 자기 reference로 가져온다. 구 단계 스킬이 하던 진입 트리거를 description이 받는다.

**Contracts**:
- `references/simplicity-contract.md` 신규(양 runtime 동일본): 구 `implementation-review/references/simplicity-contract.md` 내용을 옮기되, 소비자 서술을 `sdd-orchestrator`(simplicity worker가 경로를 읽음)·`pr-review`(prompt에 전문 포함)로 바꾸고, correctness 소관 서술을 "correctness 리뷰(호출 경로의 별도 수행자)"로 바꾼다.
- SKILL.md: simplicity 계약 경로를 `references/simplicity-contract.md`로, "단계와 이름이 같은 스킬 … 호출하지 않는다" 문장 삭제, description에 구 단계 스킬의 대표 트리거(기능 초안·계획, 구현 실행, 구현 리뷰, spec 동기화)를 흡수.
- worker 계약의 잔여 스킬 지칭 정리: `workers/feature-draft.md` 템플릿의 "`spec-sync` 스킬이" → "`spec-sync` 단계가", `workers/plan-review.md`의 "`feature-draft`로 draft를 먼저 작성하라" → "`sdd-orchestrator`로 계획 단계를 먼저 실행하라".

**Acceptance Criteria**:
- [ ] AC1 (1등급): `test -f` 양 runtime `sdd-orchestrator/references/simplicity-contract.md`, `grep -c 'implementation-review' ` 해당 파일 = 0, SKILL.md에 `references/simplicity-contract.md` 1건 이상, `grep -c '단계와 이름이 같은 스킬'` = 0.
- [ ] AC2 (1등급): `/usr/bin/diff -r` 양 runtime `references` 무출력, SKILL.md hunk 1개(Runtime 절 안).
- [ ] AC3 (1등급): SKILL.md frontmatter `description` 줄에 구 단계 스킬 트리거가 있다 — `grep -m1 '^description:' SKILL.md | grep -c -E '구현해줘|implement the plan'` = 1, 같은 줄에 `feature draft`·`spec sync`·`review implementation` 각 1건.

**Target Files**:
- [C] `.claude/skills/sdd-orchestrator/references/simplicity-contract.md` -- 계약 이동(구 위치는 Task 2에서 삭제)
- [C] `plugins/sdd-skills-codex/skills/sdd-orchestrator/references/simplicity-contract.md` -- 동일
- [M] `.claude/skills/sdd-orchestrator/SKILL.md`, `plugins/sdd-skills-codex/skills/sdd-orchestrator/SKILL.md` -- 경로·문장·description
- [M] `.claude/skills/sdd-orchestrator/references/workers/{feature-draft,plan-review}.md`, Codex 동일 -- 잔여 스킬 지칭

### Task 2: 구 단계 스킬 삭제와 marketplace 정리
Task 1이 simplicity 계약을 옮긴 뒤에 실행한다(선행 task: 1 — 삭제 대상 디렉터리에 Task 1의 입력이 있다).

**Acceptance Criteria**:
- [ ] AC1 (1등급): `for s in feature-draft plan-review implementation implementation-review spec-sync; do test ! -e .claude/skills/$s && test ! -e plugins/sdd-skills-codex/skills/$s; done` 성공, `jq -r '.plugins[0].skills[]' .claude-plugin/marketplace.json`에 다섯 이름 0건, `claude plugin validate .` → `Validation passed`.

**Target Files**:
- [D] `.claude/skills/{feature-draft,plan-review,implementation,implementation-review,spec-sync}/` -- 구 직접 실행 경로
- [D] `plugins/sdd-skills-codex/skills/{feature-draft,plan-review,implementation,implementation-review,spec-sync}/` -- 동일
- [M] `.claude-plugin/marketplace.json` -- skills 배열에서 5개 제거

### Task 3: pr-review의 simplicity 계약 포인터와 spec 반영 안내
**Acceptance Criteria**:
- [ ] AC1 (1등급): 양 runtime `pr-review/SKILL.md`·`examples/sample-review.md`에서 `implementation-review` 0건, `` `/spec-sync` ``·`$spec-sync` 0건, SKILL.md에 `sdd-orchestrator/references/simplicity-contract.md` 1건 이상.
- [ ] AC2 (1등급): claude↔codex hunk 수가 기준선과 같다(pr-review/SKILL.md 15, examples/sample-review.md 10).

**Target Files**:
- [M] `.claude/skills/pr-review/SKILL.md`, `.claude/skills/pr-review/examples/sample-review.md` -- 계약 포인터, spec 반영 안내
- [M] `plugins/sdd-skills-codex/skills/pr-review/SKILL.md`, `plugins/sdd-skills-codex/skills/pr-review/examples/sample-review.md` -- 동일

### Task 4: goal 계열의 SDD Loop Protocol과 setup 경계
**Contracts**: harness-templates.md SDD payload 2·3·4단계를 "그 feature를 `sdd-orchestrator`로 진행한다 — reviewed draft가 없으면 계획 단계부터, 있으면 구현 단계부터 게이트 결과까지 닫고, persistent 변경이 있으면 spec-sync 단계까지"로 바꾸고, 분할 시 smallest next unit·nested goal-init 금지 문장은 보존한다. 사전 승인 목록의 "`spec-sync` 실행"은 "`sdd-orchestrator` 실행(spec-sync 단계 포함)". goal-init·sdd-autopilot의 setup 경계 문장은 "setup 중 `sdd-orchestrator`나 initial feature를 실행하지 않는다".

**Acceptance Criteria**:
- [ ] AC1 (1등급): 양 runtime `goal-init/SKILL.md`·`goal-init/references/harness-templates.md`·`sdd-autopilot/SKILL.md`에서 다음 고정 문자열이 모두 0건(`grep -c -F`): `` `feature-draft`를 실행 `` / `` `implementation`으로 구현 `` / `` `spec-sync`를 실행 `` / `` `spec-sync` 실행 `` / `feature-draft·implementation·spec-sync` / `` `feature-draft`·`implementation`·`spec-sync` ``. harness-templates.md에 `sdd-orchestrator` 2건 이상, `nested` 1건 이상(보존).
- [ ] AC2 (1등급): 세 파일 짝의 claude↔codex `/usr/bin/diff` hunk 수가 변경 전 기준선과 같다(goal-init/SKILL.md 3, harness-templates.md 0, sdd-autopilot/SKILL.md 3).

**Target Files**:
- [M] `.claude/skills/goal-init/SKILL.md`, `.claude/skills/goal-init/references/harness-templates.md`, `.claude/skills/sdd-autopilot/SKILL.md` -- Loop Protocol·setup 경계
- [M] `plugins/sdd-skills-codex/skills/goal-init/SKILL.md`, `plugins/sdd-skills-codex/skills/goal-init/references/harness-templates.md`, `plugins/sdd-skills-codex/skills/sdd-autopilot/SKILL.md` -- 동일

### Task 5: 하네스 템플릿(AGENTS) §3과 self-host AGENTS.md
**Contracts**: §3의 단계 순서 줄은 유지한다. "동명의 SDD 스킬 … 그 스킬을 호출" → "discussion은 `discussion` 스킬, 나머지 단계는 `sdd-orchestrator` 스킬이 실행한다. 단계에 진입하면 그 스킬을 호출하고 로직을 직접 재구현하지 않는다". "`plan-review`·`implementation-review` 단계는 … 자기 품질 게이트로 내부 수행" → "`sdd-orchestrator`가 게이트로 수행하므로 별도로 호출하지 않는다". 진입 예시 "(discussion이나 feature-draft 등의 스킬 호출" → "(discussion이나 sdd-orchestrator 등의 스킬 호출". "`spec-sync`의 호출 여부" → "`sdd-orchestrator`의 spec-sync 단계 실행 여부". 4개 미러는 byte-identical을 유지하고, repo `AGENTS.md`의 `SDD-HARNESS` 마커 구간에 같은 문장을 반영한다.

**Acceptance Criteria**:
- [ ] AC1 (1등급): 4개 템플릿과 `AGENTS.md`에서 `동명의 SDD 스킬`·`자기 품질 게이트로 내부 수행`·`` `spec-sync`의 호출 `` 0건, `sdd-orchestrator` 각 2건 이상.
- [ ] AC2 (1등급): 4개 템플릿 쌍별 `/usr/bin/diff` 무출력(현재 byte-identical 유지).

**Target Files**:
- [M] `.claude/skills/spec-create/references/agents-harness-template.md`, `.claude/skills/spec-upgrade/references/agents-harness-template.md` -- §3
- [M] `plugins/sdd-skills-codex/skills/spec-create/references/agents-harness-template.md`, `plugins/sdd-skills-codex/skills/spec-upgrade/references/agents-harness-template.md` -- 동일
- [M] `AGENTS.md` -- self-host 하네스 §3

### Task 6: spec 계열 스킬의 draft 형식 포인터와 Integration
**Acceptance Criteria**:
- [ ] AC1 (1등급): 양 runtime `spec-review/SKILL.md`·`spec-rewrite/SKILL.md`·`spec-rewrite/references/{spec-format,rewrite-checklist}.md`·`spec-upgrade/SKILL.md`·`spec-summary/SKILL.md`에서 `skill catalog가 제공하는 `feature-draft``·`same-runtime `feature-draft``·`../feature-draft/SKILL.md`·`` `implementation-review` ``·`implementation_ledger` 0건, `workers/feature-draft.md` 합계 10건 이상(5 표면 × 2 runtime).
- [ ] AC2 (1등급): 각 파일 짝의 claude↔codex `/usr/bin/diff` hunk 수가 변경 전 기준선과 같다(6개 파일 모두 0).

**Target Files**:
- [M] `.claude/skills/spec-review/SKILL.md`, `.claude/skills/spec-rewrite/SKILL.md`, `.claude/skills/spec-rewrite/references/spec-format.md`, `.claude/skills/spec-rewrite/references/rewrite-checklist.md`, `.claude/skills/spec-upgrade/SKILL.md`, `.claude/skills/spec-summary/SKILL.md` -- 포인터·Integration·state 경로
- [M] `plugins/sdd-skills-codex/skills/` 의 같은 6개 파일 -- 동일

### Task 7: README
**Contracts**: 사용 예시·스킬 표·모델 override 안내를 `sdd-orchestrator` 기준으로 바꾸고, 스킬 수를 실제 디렉터리 수(Claude 16, Codex 14, 공통 14)로 맞춘다. `--model` 안내 중 구 `implementation-review` 전용 설명은 `pr-review`만 남긴다.

**Acceptance Criteria**:
- [ ] AC1 (1등급): `README.md`에서 `` `implementation-review` ``·`` `feature-draft`로 ``·`implementation 스킬로`·`spec-sync 스킬로` 0건, `sdd-orchestrator` 3건 이상, 표기된 스킬 수가 `ls .claude/skills | wc -l`(16)·`ls plugins/sdd-skills-codex/skills | wc -l`(14)과 일치.

**Target Files**:
- [M] `README.md` -- 사용 예시·스킬 표·스킬 수

### Task 8: docs(ko/en)
**Contracts**: 단계 개념 언급은 유지하고, 스킬 호출·스킬 역할 표·producer 게이트 소유·ledger 서술만 표현 치환 규칙대로 바꾼다. ko/en 짝은 같은 의미로 맞춘다.

**Acceptance Criteria**:
- [ ] AC1 (1등급): `docs/`(`docs/reviews/` 제외)에서 `implementation_ledger`·`` `feature-draft` 스킬의 ``·`the `feature-draft` skill`·`Producer ownership`·`producer-owned` 0건, `docs/AUTOPILOT_GUIDE.md`·`docs/en/AUTOPILOT_GUIDE.md`에 `sdd-orchestrator` 각 2건 이상.

**Target Files**:
- [M] `docs/AUTOPILOT_GUIDE.md`, `docs/en/AUTOPILOT_GUIDE.md` -- Loop 설명·관련 스킬·producer ownership·ledger
- [M] `docs/SDD_SPEC_DEFINITION.md`, `docs/en/SDD_SPEC_DEFINITION.md` -- draft 형식 단일 소스·ledger
- [M] `docs/SDD_WORKFLOW.md`, `docs/en/SDD_WORKFLOW.md` -- gate 소유·spec-sync 역할

### Task 9: 구 직접 실행 경로 census (read-only)
goal R2의 census 목록이다. 모든 리터럴은 `docs/reviews/`에 0건임을 확인하고 골랐다(과거 기록 보존과 충돌 없음).

**Acceptance Criteria**:
- [ ] AC1 (1등급): 다음 리터럴 각각 `grep -rn -F '<리터럴>' .claude plugins docs README.md AGENTS.md` 0건 — `동명의 SDD 스킬` / `$spec-sync` / `` `/spec-sync` `` / `producer인 메인 루프` / `자기 품질 게이트로 내부 수행` / `../implementation-review/references` / `implementation_ledger` / `` `implementation` 스킬 `` / `` `spec-sync` 스킬 `` / `` `implementation-review` 스킬 `` / `` `feature-draft` 스킬 `` / `` `spec-sync`의 호출 `` / ``same-runtime `feature-draft` `` / ``skill catalog가 제공하는 `feature-draft` ``.
- [ ] AC2 (1등급): Task 2 AC1의 디렉터리 부재·marketplace·validate 재확인, `git diff --check main...HEAD`·`git diff --check` 무출력.

**Target Files**:
- 없음 (read-only 검증)

# Open Questions
- `docs/reviews/2026-09-15-skill-instructions/`는 구 스킬 경로를 69줄 인용하지만 날짜가 붙은 과거 리뷰 기록이라 수정하지 않는다. census 리터럴은 그 폴더에 0건인 것만 골랐다. 사용자 확인 불필요(되돌리기 쉬움, 필요하면 후속 정리).
- 사용자가 `feature-draft`·`implementation` 등 구 스킬 이름으로 요청하면 `sdd-orchestrator` description의 트리거가 받는다. 구 이름의 별칭 스킬은 만들지 않는다(구 경로 삭제 결정). 사용자 확인 불필요.
