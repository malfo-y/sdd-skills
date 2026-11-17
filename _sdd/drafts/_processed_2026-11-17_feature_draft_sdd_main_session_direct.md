# SDD 체인을 메인 세션 직접 실행으로 간략화

<!-- spec-update-todo-input-start -->
## Spec Delta

- SDD 체인의 실행 주체가 바뀐다. 메인 세션이 계획 → 계획 리뷰 → 테스트 먼저 구현 → 구현 리뷰 → spec 반영을 직접 한다. 단계 worker, 리뷰 전용 agent, 인계 파일(digest·state), gate 2, 병렬 dispatch, 단계별 worker 모델 옵션은 없어진다.
- `sdd-orchestrator` 스킬은 순서와 저장소 규약(계획 파일 경로와 마커, 사용자 결정 처리, 증거 없는 충족 금지, spec 반영 규약)만 가진다. 단계의 방법·깊이·검증 강도는 모델이 정한다.
- 계획과 진행 상태는 계획 파일 하나(`_sdd/drafts/<날짜>_feature_draft_<slug>.md`)가 가진다. `_sdd/implementation/<날짜>_<slug>/`는 새로 만들지 않는다.
- 독립 리뷰는 PR 시점의 `pr-review`로만 남는다(선택).
- 근거: 같은 기능(dancedmd IB 여러 노드 LoRA)을 같은 base 커밋에서 다시 구현한 실측. worker 9개 44.2분 → 한 세션 15.2분, CPU 계약 통과, 독립 리뷰가 잡던 High 자리도 스스로 처리.

범위 In: `sdd-orchestrator` 본체(Claude·Codex), 별칭 스킬 5종, 삭제되는 파일을 가리키는 의존 스킬 참조, 문서, spec.
범위 Out: `pr-review`·`spec-create` 등 다른 스킬 자체의 간략화, 스킬 개명.
<!-- spec-update-todo-input-end -->

## 계획

작업은 세 묶음이고 순서대로 한다.

1. **스킬 본체**: 새 `SKILL.md`, `references/spec-sync.md`(spec 규약만). `references/workers/`, `worker-boundary.md`, `handoff-templates.md` 삭제. Codex 미러(`plugins/sdd-skills-codex/skills/sdd-orchestrator/`)는 같은 내용으로 둔다. 별칭 스킬 5종 × 2 런타임에서 `--model` 전달 문구를 뺀다. `spec-review`·`spec-rewrite`가 읽는 `workers/feature-draft.md`의 `Required Output` 참조를 새 SKILL의 `계획 파일` 절로 바꾼다.
2. **의존 스킬**: `pr-review`가 읽는 `simplicity-contract.md`를 `pr-review/references/`로 옮긴다. `goal-init`·`sdd-autopilot` 문구, `spec-create`·`spec-upgrade`의 worker 모델 기본값 표(단계 5행 삭제, `pr-review` 행 유지), `_sdd/env.md`.
3. **문서와 spec**: `docs/SDD_WORKFLOW.md`·`AUTOPILOT_GUIDE.md`·`SDD_SPEC_DEFINITION.md`(영문 미러 포함), `README.md`, `AGENTS.md`, `_sdd/spec/`(main·components·usage-guide, decision_log·changelog 신규 entry).

끝나는 조건:

- C1: `sdd-orchestrator` 디렉터리가 두 런타임 모두 `SKILL.md`, `references/spec-sync.md`(+ 묶음 2 전까지 `simplicity-contract.md`)만 가진다. 판정: `find` 출력.
- C2: 두 런타임의 `sdd-orchestrator` 파일이 같다. 판정: `/usr/bin/diff -r` hunk 0.
- C3: 삭제한 경로(`references/workers/`, `worker-boundary`, `handoff-templates`)를 가리키는 문자열이 스킬·문서·spec 현재 본문에 없다. 판정: `/usr/bin/grep -rE` 0건(기록 파일 `decision_log.md`·`logs/`·`_sdd/work_log`·`_sdd/drafts`·`_sdd/goal`·`docs/reviews` 제외).
- C4: 별칭 5종이 가리키는 `단계와 진입`의 `호출 이름` 표가 새 SKILL에 있고 다섯 이름이 모두 행으로 있다. 판정: grep.
- C5: 새 스킬로 실제 작업 하나를 끝까지 돌려 계획 파일·검사·spec 반영이 나온다. 판정: 이 개편 자체가 그 실행이다(계획 파일 = 이 파일).
- C6: `claude plugin validate .` 통과, `git diff --check` 통과, 새 파일 끝 공백 0.

계획이 기대는 외부 사실(확인함):

- Codex 미러 `SKILL.md`는 현재 `Runtime: worker dispatch` 절만 다르다 → dispatch가 없어지면 같은 파일로 둘 수 있다.
- 별칭 스킬은 `../sdd-orchestrator/SKILL.md`의 `단계와 진입` 호출 이름 표를 따른다고 쓴다 → 절 이름과 표를 유지한다.
- `spec-review` L63, `spec-rewrite` L105, `rewrite-checklist.md` L21, `spec-format.md` L27이 `workers/feature-draft.md`의 `Required Output`을 읽는다.
- `pr-review`는 `../sdd-orchestrator/references/simplicity-contract.md`를 읽는다 → 묶음 2에서 옮기기 전까지 그 자리에 둔다.
- spec `main.md` §2 Guardrails에 worker 구조를 전제한 항목이 다수 있다(L59–L111) → 묶음 3에서 다시 쓴다.
- 스킬 편집은 커밋·푸시·플러그인 갱신 전에는 설치본에 발효되지 않는다.

## 진행

현재 단계: 마감(세 묶음 모두 완료, spec 반영 v5.0.0). 커밋은 하지 않았다.

조건별 판정:

- C1 충족: `find` 출력이 두 runtime 모두 `SKILL.md`, `references/spec-sync.md` 2파일이다(묶음 2에서 `simplicity-contract.md`를 `pr-review/references/`로 옮김).
- C2 충족: `/usr/bin/diff -r .claude/skills/sdd-orchestrator plugins/sdd-skills-codex/skills/sdd-orchestrator` 출력 없음.
- C3 충족: 삭제 경로와 폐지 용어(`references/workers`, `worker-boundary`·`handoff-templates` 변형 표기, `Worker dispatch`, `DELTA_CLOSED`, `gate 2`, `digest 변경분`, `호출자 차원 한정`)의 `/usr/bin/grep -rnE` 결과가 기록 파일을 뺀 현재 본문에서 0건이다.
- C4 충족: 새 SKILL `### 호출 이름` 표에 다섯 이름 행이 모두 있다(grep 5건).
- C5 충족: 이 개편을 새 순서(계획 → 계획 리뷰 → 구현 → 구현 리뷰 → spec 반영)로 직접 수행했고 계획 파일·검사·spec 반영이 나왔다.
- C6 충족: `claude plugin validate .` 통과, `git diff --check` 출력 없음, 새 파일 끝 공백 0, 권한 0644.

계획과 달라진 결정:

- 계획 리뷰가 놓친 수정 지점 3종을 구현 중 census로 찾아 고쳤다: `spec-upgrade/SKILL.md`의 `workers/feature-draft.md` 참조, `spec-summary`의 오케스트레이터 state 문구, `spec-review`·`spec-rewrite`의 task 형식 전제 rubric 문구.
- simplicity 계약의 `호출자 차원 한정` 절을 지웠다. 차원을 한정하던 호출자(구현 게이트)가 없어져 죽은 규칙이 됐다.
- 하네스 §3의 "게이트로 수행" 문구를 "순서 안에서 직접 수행"으로 바꿨다(`AGENTS.md` + 템플릿 4미러). `goal-init` Loop Protocol 3번도 "구현 리뷰까지"로 바꿨다.
- spec `🚧 Planned` 2건(reviewer 반환 다이어트 효과 판정, 게이트 2 임계 비례화)을 닫았다. 관측 표면이던 구현 게이트가 없어졌다.

구현 리뷰에서 찾아 고친 것:

- spec Guardrail의 30초 시간 규약이 SDD 체인 규칙처럼 서술돼 있었는데 그 문면을 가진 worker 계약이 삭제됐다. 소유자를 사실대로 고쳤다(하네스 §2가 공통, 30초 예산은 `pr-review` correctness 계약).
- spec 실행 경제 불릿에 task 병렬 전제 문장이 남아 있어 지웠다.
- changelog의 크기 수치를 실측으로 고쳤다(SKILL 20KB → 8KB, 스킬 전체 82KB → 14KB).

실행으로 확인하지 못한 것:

- 설치본에서 `/sdd-orchestrator`와 별칭 5종을 실제 호출한 동작. 스킬 편집은 커밋·푸시·플러그인 갱신 뒤에 발효된다.
- Codex runtime에서의 동작.
- 기존 소비 repo의 `_sdd/env.md`에 남은 단계 행과 예전 형식 draft·state를 새 스킬이 받는 동작(문면으로만 호환을 적었다).
