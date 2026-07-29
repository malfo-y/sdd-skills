# Feature Draft: work log 훅을 하네스 자산으로 승격 (spec-create/spec-upgrade 설치)

> 규모 판정: 적격 — 변경 요소가 "훅 자산 2 + 설치 지시 2스킬 + 템플릿 1줄 + dogfooding"으로 열거되고 각 요소가 task와 1:1로 대응해 눈검산이 닫힌다. 미러 전파(4벌·2벌)는 census형 sweep이므로 마지막에 read-only 검증 task를 둔다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

SDD 하네스가 지금까지 배포하던 것은 **산문 규약**(`AGENTS.md` §5 "작업 단위 종료 시 예외 없이 work log append")뿐이라, 규약 준수가 모델 재량에 달려 있고 실제로 누락된다. 훅은 하네스(Claude Code)가 직접 실행하는 셸 명령이라 모델이 건너뛸 수 없다 — 이 차이를 이용해 §5를 **실행되는 게이트**로 승격한다.

`spec-create`·`spec-upgrade`가 소비 repo에 설치하는 하네스 산출물에 훅 자산을 추가한다. 기존 산출물은 `AGENTS.md`(하네스) / `CLAUDE.md`(포인터) / `.gitignore`(`SDD-WORKSPACE` 마커) 3종이고, 여기에 `.claude/hooks/worklog-gate.sh` · `.claude/hooks/worklog-context.sh` · `.claude/settings.json` 훅 등록이 4번째 산출물군으로 들어간다.

**새 contract/invariant**:

- **하네스 산출물 계약 확장**: 하네스 설치(= `AGENTS.md` 마커 블록 생성/병합)를 수행하면 훅 자산도 **항상 함께** 설치한다. 훅은 별도 opt-in이 아니며, 하네스 설치와 동일 조건에 묶인다. 설치 사실은 스킬 최종 보고에 명시한다(announce).
- **훅 자산 정본 위치**: 정본은 `.claude/skills/spec-create/references/hooks/`이고 나머지 3곳(`.codex/spec-create`, `.claude/spec-upgrade`, `.codex/spec-upgrade`의 `references/hooks/`)은 미러다. 4벌 바이트 동일을 유지한다 — 기존 `agents-harness-template.md` 4벌 동일 규율과 같다.
- **훅 등록 형태 고정**: PreToolUse 항목은 `matcher: "Bash"`, SessionStart 항목은 matcher 없음. command는 `bash "$CLAUDE_PROJECT_DIR"/.claude/hooks/<script>` — 복사된 스크립트에 실행 권한이 없을 수 있으므로 exec bit에 의존하지 않으며, 별도 `chmod` 단계를 두지 않기 위한 결정이다. matcher가 빠지면 모든 도구 호출에 훅이 붙고, 잘못 지정되면 게이트가 침묵 무력화되므로 등록 형태 자체가 계약이다.
- **셸 스크립트는 verbatim 복사, `settings.json`은 키 수준 멱등 병합**: JSON에는 `SDD-HARNESS` 같은 마커 주석을 넣을 수 없다. 멱등 판정 키는 "`hooks.<event>[].hooks[].command` 문자열이 해당 훅 스크립트 경로를 포함하는 항목"이며, 그 항목만 교체하고 사용자의 다른 훅·`permissions` 등 나머지 키는 보존한다.
- **대상은 커밋되는 `.claude/settings.json`이다**(개인용 `settings.local.json` 아님). 근거: 하네스는 repo 규약이고 팀 전체에 적용되어야 한다. **부수 효과**: 소비 repo의 모든 Claude Code 사용자(SDD를 쓰지 않는 기여자 포함)가 커밋 게이트를 받는다 — announce 문구에 이 사실을 포함한다. 확신도: 중.
- **조용한 무력화 금지**: 게이트는 JSON 파서(`jq` → `python3` 순)로 stdin payload를 읽는다. 둘 다 없으면 게이트는 통과시키되(fail-open), SessionStart 훅이 "게이트 비활성" 경고를 컨텍스트에 출력한다. 파서 부재가 침묵으로 이어지면 안 된다.
- **두 스크립트 모두 프로젝트 루트를 고정한다**: 시작 시 `cd "${CLAUDE_PROJECT_DIR:-.}"`. 게이트는 `git status --porcelain -- _sdd/work_log/<today>.md`를 상대경로로 평가하므로 훅 cwd가 repo 루트가 아니면 로그를 썼는데도 매칭 0건 → 오탐 차단이 된다.
- **Codex 비대칭 수용**: Codex에는 훅 메커니즘이 없어 `.codex/` 레인 스킬도 동일하게 `.claude/hooks/`를 설치하지만 Codex 자신은 게이트의 강제를 받지 않는다. 산출물은 대상 repo의 것이고 그 repo는 Claude Code로도 열린다는 근거로 이 비대칭을 수용한다.
- **자산 형식 제약 없음(실측 확정)**: `tools/install-codex-skill-bundle.py`는 `SKILL.md` 존재만 확인하고(`:284`) 스킬 디렉토리를 `shutil.copytree`로 통째 복사하며(`:461`) 파일 형식 검증기가 없다. `.claude-plugin/marketplace.json`은 스킬을 디렉토리 경로로 등록한다. 따라서 `references/hooks/*.sh`를 `.md` 코드블록으로 감쌀 필요가 없다.

## Scope

- **In**: 훅 자산 정본 2파일 작성 + 4벌 미러 배포 / `spec-create`·`spec-upgrade` SKILL.md에 설치 지시·산출물 목록·체크리스트·검증 항목·최종 보고 항목 추가(각 claude·codex 2벌) / 하네스 템플릿 §5에 게이트 존재 1줄 추가(4벌) / 이 repo 프로토타입 3파일을 정본 산출물과 일치(dogfooding) / 미러·리터럴 전수 census + omission 대조 검증
- **Out**: Stop 훅(턴 종료 차단, 이전 논의의 B안) — 커밋 없는 SDD 단계 누락 실측이 나올 때까지 보류 / work log **내용 품질** 검사(항목 형식·충실도 판정) — 게이트는 "기록했는가"만 본다 / Codex용 등가 강제 메커니즘 탐색 / **이 repo의 spec·docs 본문 반영** — `_sdd/spec/usage-guide.md`(소비 repo 산출물 세트 열거)와 `docs/SDD_CONCEPT.md`(하네스를 문서 규약 레이어로 서술; 실행 자산 편입으로 후행 갱신 대상)는 이 feature에서 건드리지 않고 후속 `spec-sync` 단계에서 판정한다
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: 훅 자산 정본 2파일 작성 + 4벌 미러 배포

이 repo에 설치된 프로토타입(`.claude/hooks/*.sh`)은 `jq` 전용이고, 실행 권한에 의존하며, 게이트에 프로젝트 루트 고정이 빠져 있다. 배포하려면 세 전제를 다 걷어내야 한다. 게이트 판정 로직 자체(명령 경계 `git commit` 판별, `git status --porcelain` 통과 조건, 세션 마커, `--amend`/`SDD_SKIP_WORKLOG=1`/rebase·merge·cherry-pick 예외)는 프로토타입에서 12 케이스로 검증된 설계를 그대로 옮긴다. 정본만 있고 미러가 없는 중간 상태는 4벌 동일 규율이 깨진 상태라 독립 가치가 없으므로 배포까지 한 task로 닫는다.

**Contracts**:
- `worklog-gate.sh`: stdin으로 PreToolUse payload(JSON)를 받아 `.tool_input.command`·`.session_id`를 읽는다. 차단 시 `permissionDecision: "deny"` + `permissionDecisionReason`(한국어, 항목 형식·우회법 포함) JSON을 stdout에 쓰고 exit 0. 통과 시 무출력 exit 0.
- `worklog-context.sh`: SessionStart에서 실행되어 오늘 로그 경로·존재 여부·마지막 `## ` 헤더를 stdout에 쓴다(exit 0 stdout이 컨텍스트로 주입됨). JSON 파서가 하나도 없으면 "게이트 비활성" 경고 줄을 추가로 출력한다.
- 두 스크립트 모두 시작 시 `cd "${CLAUDE_PROJECT_DIR:-.}"`로 루트를 고정한다.
- 대상 경로는 `_sdd/work_log/$(date +%F).md` 고정 — 하네스 템플릿 §5가 이 경로를 규정하므로 슬롯 치환 대상이 아니다.
- 세션 마커(`.git/sdd-worklog-ok/<session_id>`)는 **정리하지 않는다(의도적)** — `.git/` 내부라 무해하고, 정리 로직은 게이트가 감당할 책임이 아니다.

**Acceptance Criteria**:
- [ ] AC1: 12 케이스를 **`jq` 경로와 `python3` 경로 양쪽에서** 실행해 24판정이 모두 동일하다. 통과: `grep "git commit" <file>` / `git log --oneline` / `git status` / `git commit --amend --no-edit` / `SDD_SKIP_WORKLOG=1 git commit -m x` / 비-git 명령, 차단: `git commit -m x` / `git add -A && git commit -m x` / `git -C . commit -m x` / `git -c user.name=x commit -m y` / `GIT_EDITOR=true git commit` / `cd /tmp; git commit -m x`. (파서 강제 방법 = PATH에서 `jq`를 가린 사본 실행)
- [ ] AC2: 두 경로가 만든 deny JSON을 각각 파싱했을 때 `permissionDecisionReason` 문자열이 **바이트 동일**하다(python3 경로의 JSON 이스케이프 대칭성 증명).
- [ ] AC3: `jq`·`python3`를 모두 가린 상태에서 차단 대상 payload를 주면 게이트는 무출력 exit 0(fail-open)이고, 같은 조건에서 `worklog-context.sh` 출력에 "게이트 비활성" 경고 줄이 포함된다.
- [ ] AC4: 실행 권한이 없는 사본(`chmod -x`)을 `bash <path>` 로 호출해도 AC1의 판정이 동일하다.
- [ ] AC5: 오늘 로그에 미커밋 변경이 있으면 통과하고 `.git/sdd-worklog-ok/<session_id>` 마커가 생성되며, 마커 존재 시 로그가 없어도 같은 세션의 후속 `git commit`이 통과한다.
- [ ] AC6: **repo 하위 디렉토리를 cwd로** 두고 실행해도 AC5의 통과 판정이 동일하다(루트 고정 증명).
- [ ] AC7: `worklog-gate.sh` 4벌의 md5가 모두 동일하고 `worklog-context.sh` 4벌도 동일하다.
- [ ] AC8: 두 정본 파일 상단 주석에 "정본 = `.claude/skills/spec-create/references/hooks/`, 나머지 3곳은 미러, 수정 시 4곳 동기화" 취지의 문장이 있다.

**Target Files**:
- [C] `.claude/skills/spec-create/references/hooks/worklog-gate.sh` -- 훅 자산 정본(게이트)
- [C] `.claude/skills/spec-create/references/hooks/worklog-context.sh` -- 훅 자산 정본(세션 컨텍스트)
- [C] `.codex/skills/spec-create/references/hooks/worklog-gate.sh` -- 미러
- [C] `.codex/skills/spec-create/references/hooks/worklog-context.sh` -- 미러
- [C] `.claude/skills/spec-upgrade/references/hooks/worklog-gate.sh` -- 미러
- [C] `.claude/skills/spec-upgrade/references/hooks/worklog-context.sh` -- 미러
- [C] `.codex/skills/spec-upgrade/references/hooks/worklog-gate.sh` -- 미러
- [C] `.codex/skills/spec-upgrade/references/hooks/worklog-context.sh` -- 미러

---

### Task 2: 하네스 템플릿 §5에 게이트 존재 1줄 추가 (4벌)

소비 repo의 `AGENTS.md`를 읽는 사람/모델이 "이 규약은 강제된다"는 사실과 우회법을 알아야 한다. **새 § 섹션을 만들지 않고 §5 안에 불릿 1줄만 추가한다** — § 범위가 바뀌면 두 SKILL.md와 `_sdd/spec/usage-guide.md`의 "§0~§5" 리터럴이 전부 따라 바뀌어야 하고 그 전파가 과거에 실측으로 샜다.

**Acceptance Criteria**:
- [ ] AC1: 4벌 `agents-harness-template.md` §5에 게이트 존재·발동 시점(세션 첫 커밋)·우회법(`SDD_SKIP_WORKLOG=1`)을 담은 불릿이 추가되어 있고 4벌 md5가 동일하다.
- [ ] AC2: 템플릿의 `## ` 섹션 번호는 여전히 §0~§5이며, `grep -rn '§0~§5' .claude .codex _sdd/spec docs` 의 히트 수가 변경 전과 같다.

**Target Files**:
- [M] `.claude/skills/spec-create/references/agents-harness-template.md` -- §5 불릿 추가(정본)
- [M] `.codex/skills/spec-create/references/agents-harness-template.md` -- 미러 동기화
- [M] `.claude/skills/spec-upgrade/references/agents-harness-template.md` -- 미러 동기화
- [M] `.codex/skills/spec-upgrade/references/agents-harness-template.md` -- 미러 동기화

---

### Task 3: `spec-create`에 훅 설치 지시 추가 (claude·codex 2벌)

`Step 3`의 부트스트랩 파일 목록과 `3a~3d` 옆에 훅 설치 하위 절차(`3e`)를 추가하고, 자산 목록·체크리스트·검증·산출물 계약까지 같은 사실을 반영한다. 지시는 기존 3a와 동일한 **"Read + verbatim 복사"** 기계적 명령으로 쓴다 — "생성한다/사용한다"로 쓰면 모델이 재구성해 자산 변경이 산출물에 누락된다(실측).

**Contracts**: `settings.json` 병합 규칙 — 파일 부재면 훅 2개만 담아 생성. 존재하면 `hooks.PreToolUse`·`hooks.SessionStart` 배열에 항목을 추가하되, `command` 문자열이 해당 스크립트 경로를 포함하는 기존 항목이 있으면 **그 항목만 교체**한다(멱등). `permissions` 등 다른 최상위 키와 사용자의 다른 훅 항목은 보존한다. 등록 형태는 PreToolUse = `matcher: "Bash"` + `bash "$CLAUDE_PROJECT_DIR"/.claude/hooks/worklog-gate.sh`, SessionStart = matcher 없음 + `bash "$CLAUDE_PROJECT_DIR"/.claude/hooks/worklog-context.sh`.

**Acceptance Criteria**:
- [ ] AC1: `3e` 하위 절차가 존재하고, 두 `.sh`를 `references/hooks/`에서 **Read → verbatim 복사**하라고 지시하며 "재구성하지 않는다" 경고를 포함한다.
- [ ] AC2: `settings.json` 병합 규칙이 위 Contracts 전 항목(부재 생성 / 배열 추가 / command 경로 기준 항목만 교체 / 타 키 보존 / PreToolUse matcher `"Bash"` / SessionStart matcher 없음)을 모두 명시한다.
- [ ] AC3: 훅 설치가 `AGENTS.md` 하네스 설치와 **동일 조건**에 묶인다고 명시되어 있다(별도 opt-in 아님).
- [ ] AC4: 아래 **5개 섹션 각각의 본문**에 리터럴 `references/hooks/` 또는 `.claude/hooks/` 가 1회 이상 등장한다(섹션 경계는 `## `/`### ` 헤더 기준) — `## Acceptance Criteria`(체크리스트), `## Companion Assets`, `### Step 3: Bootstrap Workspace Guidance`(파일 목록), `### Step 5: Validate and Save`, `## Output Contract`.
- [ ] AC5: Hard Rules의 파일 생성/병합 규칙 항목(현재 `AGENTS.md`·`CLAUDE.md`·`_sdd/env.md`를 열거하는 4번)에 훅 자산 반영 여부를 판정해 기록했다 — 반영했거나, 하지 않았다면 그 근거가 draft 실행 기록에 남는다.
- [ ] AC6: `Output Contract`에 설치 사실을 최종 보고에 명시하라는 announce 요구가 있고, 그 문구가 "커밋되는 `settings.json`이라 이 repo의 모든 Claude Code 사용자에게 적용된다"는 고지를 포함한다.
- [ ] AC7: `.claude`·`.codex` 2벌 `spec-create/SKILL.md`가 바이트 동일하다.

**Target Files**:
- [M] `.claude/skills/spec-create/SKILL.md` -- 3e 신설 + 5개 섹션 반영
- [M] `.codex/skills/spec-create/SKILL.md` -- 미러 동기화

---

### Task 4: `spec-upgrade`에 훅 설치 지시 추가 (claude·codex 2벌)

`Step 6: Harness Merge`의 제목·본문에 훅 병합 규칙을 추가하고, 자산 목록·체크리스트·검증·최종 보고에 반영한다. 병합 규칙 본문은 Task 3과 **동일한 계약**을 쓴다(두 스킬이 같은 산출물을 만들어야 하므로).

**Acceptance Criteria**:
- [ ] AC1: `Step 6` 제목이 훅 자산을 포함하도록 갱신되고, 본문에 Task 3 Contracts와 **동일한** `settings.json` 병합 규칙(matcher 규정 포함) + `.sh` verbatim 복사 지시가 있다.
- [ ] AC2: 아래 **4개 섹션 각각의 본문**에 리터럴 `references/hooks/` 또는 `.claude/hooks/` 가 1회 이상 등장한다(섹션 경계는 `## `/`### ` 헤더 기준) — `## Acceptance Criteria`(체크리스트), `## Companion Assets`, `### Step 7: Validate`, `## Output Contract`.
- [ ] AC3: `Output Contract` 최종 보고 항목에 훅 설치 결과와 Task 3 AC6과 동일한 announce 고지 요구가 있다.
- [ ] AC4: `.claude`·`.codex` 2벌 `spec-upgrade/SKILL.md`가 바이트 동일하다.

**Target Files**:
- [M] `.claude/skills/spec-upgrade/SKILL.md` -- Step 6 확장 + 4개 섹션 반영
- [M] `.codex/skills/spec-upgrade/SKILL.md` -- 미러 동기화

---

### Task 5: dogfooding — 이 repo의 훅 3파일을 정본 산출물과 일치시킴

프로토타입은 체인의 입력일 뿐이다. 이 repo가 자기 스킬의 산출물과 다른 상태로 남으면 정본이 둘이 된다. `spec-create` 3e 절차를 이 repo에 실제로 적용해 산출물을 재생성한다 — 절차 자체의 실행 검증도 겸한다.

**Acceptance Criteria**:
- [ ] AC1: `.claude/hooks/worklog-gate.sh`·`worklog-context.sh`가 각 정본과 바이트 동일하다(md5 대조).
- [ ] AC2: `.claude/settings.json`의 PreToolUse 항목이 `matcher: "Bash"` + `bash "$CLAUDE_PROJECT_DIR"/.claude/hooks/worklog-gate.sh`이고, SessionStart 항목은 matcher 없이 `bash "$CLAUDE_PROJECT_DIR"/.claude/hooks/worklog-context.sh`이며, `settings.local.json`의 `permissions`는 변경되지 않았다.
- [ ] AC3: 이 repo의 `AGENTS.md` §5가 갱신된 하네스 템플릿 §5와 일치한다(마커 블록 내부 대조).
- [ ] AC4: 3e 절차를 한 번 더 적용해도 `.claude/hooks/`·`.claude/settings.json`에 변경이 발생하지 않는다(멱등 실증, `git status --porcelain -- .claude/hooks .claude/settings.json` 무출력).

**Target Files**:
- [M] `.claude/hooks/worklog-gate.sh` -- 정본 산출물로 교체
- [M] `.claude/hooks/worklog-context.sh` -- 정본 산출물로 교체
- [M] `.claude/settings.json` -- matcher + `bash <path>` 등록 형태로 교체
- [M] `AGENTS.md` -- §5 하네스 마커 블록 동기화

---

### Task 6: 전파 census + omission 대조 검증 (read-only)

하네스 표면 변경은 미러·리터럴 누락이 매 라운드 재발한다(실측). pair/orphan census만으로는 "4벌 모두에서 빠진" 누락을 구조적으로 못 잡으므로, **기존 자산의 등장 표면을 신규 자산의 최소 등장 표면으로 삼는 1:1 대조**를 함께 둔다.

**Acceptance Criteria**:
- [ ] AC1 (omission 대조): `spec-create/SKILL.md`·`spec-upgrade/SKILL.md`에서 기존 자산 리터럴 `agents-harness-template.md`가 등장하는 모든 섹션을 열거하고, 각 섹션에 `references/hooks/` 대응 항목이 있는지 1:1로 대조해 미대응 섹션이 0건이다(대응 불필요면 사유를 기록).
- [ ] AC2 (변형 표기 census): `worklog-gate`·`worklog-context`·`worklog_gate`·`worklog_context`·`sdd-worklog-ok`·`SDD_SKIP_WORKLOG`·`references/hooks`·`.claude/hooks` 각 표기를 `.claude`·`.codex`·`docs`·`README.md`·`AGENTS.md`·`.claude-plugin`·`_sdd/spec` 전체에 grep해 claude·codex 짝이 모두 맞고 고아 참조가 0건이다.
- [ ] AC3 (회귀): `tools/install-codex-skill-bundle.py`가 여전히 `shutil.copytree`로 스킬 디렉토리를 통째 복사하고(`:461` 부근) 파일 형식 검증기를 도입하지 않았다 — 유지되면 `references/hooks/`가 codex 번들로 함께 이동한다.
- [ ] AC4 (회귀): `.claude-plugin/marketplace.json`이 스킬을 디렉토리 경로로 등록하는 방식을 유지한다(파일 단위 등록이면 훅 자산 누락이므로 결함으로 보고).
- [ ] AC5: `git diff --check` 무출력.

**Target Files**:
- 없음 (read-only 검증)

# Open Questions

사용자 확인이 필요한 항목 없음.

(리뷰에서 제기된 late-binding 결정 1건은 실측으로 해소해 Part 1에 확정 기록했다 — codex 번들 installer가 `copytree` + 형식 검증기 부재이고 marketplace가 디렉토리 등록이므로, 훅 자산을 `.sh` 원본 그대로 `references/hooks/`에 둔다. `.md` 코드블록 래핑 대안은 폐기.)
