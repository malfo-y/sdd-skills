# Feature Draft: sdd-autopilot을 goal-init SDD instance로 전환

> 규모 판정: 적격 — `goal-init` SDD preset → `sdd-autopilot` thin entrypoint → 사용자 문서 전파가 선형이고, 계약별 owner task와 10개 live surface를 눈으로 전수 대응할 수 있다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
`sdd-autopilot`을 기능 요청을 즉시 구현하는 독립 chain runner에서 기존 `goal-init`의 SDD 전용 instance/harness setup entrypoint로 재정의한다.

- `/sdd-autopilot`은 사용자 요청을 `goal-init(preset=sdd)`로 전달하고, 기존 Goal Intake → Divergence → Condition Crafting → Harness Setup → Handoff 5단계와 condition self-check, 4파일 형식을 그대로 재사용한다.
- setup 단계에서는 initial feature draft·implementation·spec-sync를 실행하지 않는다. native goal도 활성화하지 않고 현재 goal status를 조회·변경·clear·pause·replace하지 않는다.
- SDD preset의 `goal.md` `Loop Protocol`은 native goal 활성화 뒤 다음 6단계를 반복한다: 미충족 DONE WHEN 또는 실패한 integration proof gap에서 최소 next feature 선택 → reviewed draft가 없으면 `feature-draft`(분할이면 최소 next unit) → `implementation` → persistent 변경 시 `spec-sync` → evidence·완료 feature·남은 gap·next action 기록 → 모든 DONE WHEN과 integration proof 통과 시 종료.
- active SDD goal 안에서 draft가 분할돼도 nested `goal-init`을 만들지 않고 현재 goal loop가 다음 최소 feature를 계속 선택한다.
- 기존 `experiments.md`·`journal.md`·`report.md` 역할과 형식은 유지한다. formal Goal Contract, scope ID, Initial Feature Queue, status manifest, goal-level reviewer는 추가하지 않는다.
- Handoff는 조건 문자열과 runtime 실행법에 더해 “goal을 활성화하지 않았으며 기존 goal 상태도 변경하지 않았다”는 불변식을 항상 표시하고, 사용자가 검토 후 직접 활성화하도록 한다.

Global spec 반영은 구현 후 `spec-sync` 소관이다. `_sdd/spec/main.md`의 autopilot guardrail·오케스트레이션 결정, `_sdd/spec/components.md`의 `sdd-autopilot`·`goal-init` component/navigation 설명, `_sdd/spec/usage-guide.md`의 autopilot 시나리오를 새 setup/activation 계약으로 바꾸고, `decision_log.md`·`logs/changelog.md`에 독립 runner 결정을 supersede하는 이력을 append한다.

## Scope
- **In**: Claude/Codex `goal-init` SDD preset, 6단계 SDD Loop Protocol, Claude/Codex `sdd-autopilot` thin entrypoint, setup/activation 분리, active-goal status 비조회, nested goal-init 금지, 한·영 autopilot 가이드, README·env 정합, 후속 global spec sync.
- **Out**: generic `goal-init`의 5단계·4파일·condition self-check 변경, native `/goal` runtime 구현, `/goal` 자동 활성화·migration·merge, initial feature draft/queue, formal Goal Contract schema, producer skill·review gate 변경, marketplace 등록 구조 변경.
<!-- spec-update-todo-input-end -->

# Propagation Surfaces

| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | `goal-init(preset=sdd)`와 선택형 SDD Loop Protocol(template 전문 단일 소유) | `.claude/skills/goal-init/{SKILL.md,references/harness-templates.md}`; `.codex/skills/goal-init/{SKILL.md,references/harness-templates.md}` | `rg --hidden -l '^### Step 4: Harness Setup|^## 1\. `goal\.md` 템플릿' .claude/skills/goal-init .codex/skills/goal-init`에서 SKILL/template 짝 4파일 | Task 1 |
| P2 | 독립 runner 제거와 inert harness thin entrypoint | `.claude/skills/sdd-autopilot/SKILL.md`; `.codex/skills/sdd-autopilot/SKILL.md` | `rg --hidden -l '체인\(draft|Step 2: 체인|chain runner' .claude/skills/sdd-autopilot .codex/skills/sdd-autopilot`의 current owner 2파일 | Task 2 |
| P3 | setup/activation 사용자 모델과 obsolete pre-flight 제거 | `docs/AUTOPILOT_GUIDE.md`; `docs/en/AUTOPILOT_GUIDE.md`; `README.md`; `_sdd/env.md` | `rg -l -i 'sdd-autopilot|sdd autopilot' README.md docs _sdd/env.md`의 live 사용자-facing 집합 4파일 | Task 3 |

# Part 2: Tasks

### Task 1: goal-init에 SDD preset을 추가
generic 경로를 그대로 둔 채 `preset=sdd`일 때만 6단계 SDD Loop Protocol을 선택하도록 adapter와 template slot을 추가한다. 6단계 전문은 Claude/Codex `harness-templates.md`의 byte-identical payload 구간이 단일 소유하고, runtime별 실행법 슬롯 차이는 유지한다. 두 SKILL은 preset 선택·삽입 규칙과 template pointer만 가진다.

**Contracts**: `preset=sdd`는 기존 5단계·condition self-check·4파일 형식을 바꾸지 않는 HOW preset이다. setup은 initial draft와 코드를 만들지 않고 native goal도 발동하지 않는다. active goal 안의 split은 현재 loop의 next-feature 선택으로 처리하며 nested goal-init을 만들지 않는다.

**Acceptance Criteria**:
- [ ] AC1: Claude/Codex `goal-init`이 `preset=sdd` 입력을 명시적으로 인식하고 generic path의 Goal Intake → Divergence → Condition Crafting → Harness Setup → Handoff 5단계, evaluator self-check 3항목, 4파일 산출을 그대로 재사용한다. 평가: 두 SKILL의 preset adapter와 기존 단계 anchor를 인용한 rubric에서 삭제·우회·별도 6번째 setup 단계가 0건이면 PASS.
- [ ] AC2: SDD preset `Loop Protocol`에 순서가 고정된 6단계가 모두 있다: 미충족 DONE WHEN 또는 실패한 integration-proof gap에서 최소 next feature → draft 부재 시 `feature-draft`와 split 최소 unit → `implementation` → persistent 변경 시 `spec-sync` → evidence/완료 feature/남은 gap/next action 기록 → DONE WHEN+integration proof 종료. 평가: 두 template의 전문에서 단계 누락·순서 역전·integration-proof-only 교착 0건이고, 두 SKILL에는 `preset=sdd` 선택·template 삽입 규칙과 canonical pointer만 있으며 6단계 전문 복제가 0건이면 PASS.
- [ ] AC3: setup 전/중 initial `feature-draft`·`implementation`·`spec-sync` 호출이 0건이고, 실행 중 split은 nested `goal-init` 없이 현재 native goal loop에서 처리된다. 평가: 두 SKILL의 preset hard boundary와 protocol 문면을 인용하고, setup Process에 producer 호출 지시가 없으면 PASS.
- [ ] AC4: 기존 4파일 heading·역할과 generic Loop Protocol의 네 동작(pending 가설 선택 → 검증 출력 대화 surface → journal append → pending 고갈 시 새 가설 보충)이 보존되고 formal Goal Contract·scope ID·Initial Feature Queue·status manifest·goal-level reviewer가 추가되지 않는다. 평가: template fenced heading 집합이 `goal.md`/`experiments.md`/`journal.md`/`report.md` 기존 집합과 같고, 두 template의 generic 분기에서 네 동작 누락·변경 0건이며, 금지 schema scoped `rg` 출력이 비어 있으면 PASS.
- [ ] AC5: Handoff는 native goal 미활성·기존 goal 무변경 불변식을 항상 표시하고 사용자가 직접 활성화하도록 한다. 평가: 두 SKILL Step 5와 template 실행법 주변에 positive anchor가 있고 자동 `set`/발동 지시가 0건이면 PASS.
- [ ] AC6: Claude/Codex harness template의 `Loop Protocol preset payloads` 구간은 byte-identical이고, 기존 runtime별 실행법 슬롯 차이는 보존된다. goal-init SKILL 짝도 runtime invocation 차이를 제외해 의미가 같다. 평가: payload 구간 diff exit 0 + main 대비 실행법 슬롯 hunk 외 신규 runtime 불일치 0건 + SKILL의 preset 선택/비발동 anchor semantic rubric 누락 0건이면 PASS.

**Target Files**:
- [M] `.claude/skills/goal-init/SKILL.md` -- generic 계약을 재사용하는 SDD preset adapter와 handoff 불변식
- [M] `.codex/skills/goal-init/SKILL.md` -- Codex runtime의 동일 SDD preset adapter와 handoff 불변식
- [M] `.claude/skills/goal-init/references/harness-templates.md` -- generic/SDD 선택형 Loop Protocol template
- [M] `.codex/skills/goal-init/references/harness-templates.md` -- Claude template과 byte-identical mirror

### Task 2: sdd-autopilot을 thin setup entrypoint로 교체
기존 chain runner의 AC·Hard Rules·Process를 제거하고 `goal-init(preset=sdd)` 호출과 결과 relay만 소유하게 한다.

**Contracts**: `/sdd-autopilot`은 inert 4-file harness와 조건 문자열을 준비하는 entrypoint다. producer skills와 native goal runtime은 setup에서 호출하지 않으며, current goal status를 조회하거나 active goal 때문에 차단하지 않는다.

**Acceptance Criteria**:
- [ ] AC7: 두 `sdd-autopilot` SKILL의 description·Goal·Process가 end-to-end implementation runner가 아니라 `goal-init` SDD preset setup entrypoint임을 명시하고, 사용자 원문과 관련 context를 goal-init에 전달한다. 평가: positive anchor 존재 + 독립 Draft/구현/Spec sync 실행 단계 0건이면 PASS.
- [ ] AC8: setup에서 current native goal status 조회, `ACTIVE_GOAL_CONFLICT`, goal set/clear/pause/resume/replace, initial feature draft·implementation·spec-sync가 모두 금지된다. 평가: Hard Rules/AC에 비조회·비변경·비발동 anchor가 있고 실행 Process에 해당 호출 지시가 0건이면 PASS.
- [ ] AC9: 두 runtime 모두 goal-init의 5단계·4파일·self-check를 단일 소스로 가리키고 SDD Loop Protocol을 재서술하지 않는다. Claude는 plugin-prefixed invocation, Codex는 runtime-local skill loading 규약을 사용한다. 평가: thin entrypoint rubric에서 중복 protocol 단계 정의 0건과 runtime별 올바른 호출 anchor를 확인하면 PASS.
- [ ] AC10: Handoff가 조건 문자열·runtime 실행법·4파일 경로·“goal 미활성/기존 goal 무변경”을 relay하고 활성화 선택을 사용자에게 둔다. 평가: 두 SKILL Final Check/relay 목록의 4요소 누락 0건이면 PASS.

**Target Files**:
- [M] `.claude/skills/sdd-autopilot/SKILL.md` -- `sdd-skills:goal-init` SDD preset thin entrypoint
- [M] `.codex/skills/sdd-autopilot/SKILL.md` -- runtime-local `goal-init` SDD preset thin entrypoint

### Task 3: 사용자 문서와 환경 안내를 setup 모델로 전환
한·영 가이드와 README를 goal harness setup/사용자 activation 흐름으로 다시 쓰고 obsolete pre-flight 설명을 제거한다.

**Contracts**: 문서는 `/sdd-autopilot` 호출만으로 구현이 시작된다고 약속하지 않는다. setup 산출물은 4-file goal harness+condition이며, 실제 multiple SDD path 실행은 사용자가 native goal을 활성화한 뒤 6단계 loop가 수행한다.

**Acceptance Criteria**:
- [ ] AC11: 한·영 AUTOPILOT_GUIDE가 setup → 사용자 검토/activation → native goal의 repeated SDD loop를 같은 의미로 설명하고, 6단계 protocol·split continuation·producer-owned gates·final integration proof를 포함한다. 평가: ko/en section 대응표의 개념 누락·모순 0건이면 PASS.
- [ ] AC12: 가이드가 initial draft/implementation/spec-sync 0건, current goal status 비조회, native goal 비발동·기존 goal 무변경 handoff를 명시하며 formal Goal Contract/Initial Feature Queue를 사용자 개념으로 도입하지 않는다. 평가: positive/negative anchor scoped `rg`와 section 인용 rubric으로 PASS/FAIL 판정한다.
- [ ] AC13: AUTOPILOT_GUIDE 한·영 metadata는 breaking role change에 맞는 동일 버전 `3.0.0`과 날짜 `2026-08-10`을 사용하고, README 문서 설명도 “전체 파이프라인 자동화”가 아니라 SDD goal harness setup으로 바뀐다. 평가: metadata/README row 대조에서 차이·stale 문구 0건이면 PASS.
- [ ] AC14: `_sdd/env.md`의 `SDD-Autopilot Resources` pre-flight block 전체(상위 heading부터 `외부 서비스`·`환경 변수`·`테스트`·`빌드/배포` 하위 절과 본문까지)가 제거되고 나머지 environment guide는 보존된다. 평가: `git diff -- _sdd/env.md`의 hunk가 현행 block 전체 삭제만 포함하고, `rg -n 'SDD-Autopilot Resources|Pre-flight Check|파이프라인 요구사항|^### (외부 서비스|환경 변수|테스트|빌드/배포)$' _sdd/env.md` 출력이 비어 있으면 PASS.

**Target Files**:
- [M] `docs/AUTOPILOT_GUIDE.md` -- 한국어 setup/activation/loop 사용 가이드 3.0.0
- [M] `docs/en/AUTOPILOT_GUIDE.md` -- 영문 semantic mirror 3.0.0
- [M] `README.md` -- autopilot 문서 설명과 사용 시점 정정
- [M] `_sdd/env.md` -- obsolete autopilot pre-flight resource section 제거

### Task 4: 전파·미러·stale runner 계약을 전수 검증
작성 표면을 모두 닫은 뒤 독립 chain runner와 active-goal blocker가 live surface에 남지 않았는지 read-only census로 확인한다.

**Acceptance Criteria**:
- [ ] AC15: P1~P3의 required surface 10파일이 모두 변경되고, `.claude/skills/goal-init`·`.codex/skills/goal-init`의 sample 파일과 `.claude-plugin/marketplace.json`은 변경되지 않는다. 평가: `git diff --name-only main -- .claude/skills/goal-init/SKILL.md .claude/skills/goal-init/references/harness-templates.md .codex/skills/goal-init/SKILL.md .codex/skills/goal-init/references/harness-templates.md .claude/skills/sdd-autopilot/SKILL.md .codex/skills/sdd-autopilot/SKILL.md docs/AUTOPILOT_GUIDE.md docs/en/AUTOPILOT_GUIDE.md README.md _sdd/env.md` 출력 집합이 이 exact 10파일이고, `git diff --exit-code main -- .claude/skills/goal-init/examples .codex/skills/goal-init/examples .claude-plugin/marketplace.json`이 exit 0이면 PASS.
- [ ] AC16: implementation surface에서 old runner·active-goal blocker 의미가 0건이고, native goal 활성화 후 Loop Protocol의 정상 `feature-draft → implementation → spec-sync` 순서는 허용된다. 평가: exact 10파일에 `rg -n -i 'Step 2: 체인|Step 2: The Chain|무승인으로 끝까지 실행|runs? the SDD chain end-to-end without approval steps|기능 요청 하나를 받아 계획.*구현.*스펙 동기화|takes a single feature request and runs planning.*implementation.*spec synchronization to completion|ACTIVE_GOAL_CONFLICT|RUNNING 또는 PAUSED|RUNNING or PAUSED'`를 실행한 출력이 비어 있으면 PASS. 별도로 setup Process를 인용해 current goal status read/check 명령이 0건임을 확인하되, handoff의 `/goal status` 사용자 실행법과 negative invariant 문장은 허용한다.
- [ ] AC17: positive contract가 두 runtime skill과 한·영 docs에 모두 존재한다. 평가: 파일별 `goal-init`/SDD preset, 6단계 loop 또는 그 canonical pointer, 사용자 activation, initial producer 실행 0건 의미 anchor를 검사해 필수 surface 전부 PASS를 출력한다.
- [ ] AC18: generic goal-init 계약 보존을 확인한다. 평가: 두 SKILL에서 5개 Step heading, AC1~AC5, 4-file path, evaluator self-check 3항목이 유지되고, 두 template generic 분기의 pending 선택·검증 출력 surface·journal append·큐 보충 네 동작이 모두 존재하며, sample session 두 파일이 main 대비 변경 0건이면 PASS.
- [ ] AC19: Part 1 marker가 후속 global spec 반영 표면을 열거하고 Part 2 Target Files에는 `_sdd/spec/`가 없다. 평가: marker 내부 `main.md`·`components.md`·`usage-guide.md`·decision log·changelog anchor 존재 + `rg -n '^\- \[[MCD]\] `_sdd/spec/'` 출력 0건이면 PASS.
- [ ] AC20: `git diff --check`가 출력 없이 exit 0이고 두 template의 `Loop Protocol preset payloads` 구간 diff가 exit 0이다.

**Target Files**:
- 없음 (read-only 검증)
