# Feature Draft: Codex hook runtime acceptance

> 규모 판정: 적격 — 실제 skill 설치 검증 2개와 runtime lifecycle 검증 2개가 서로 독립된 Task 1~4에 1:1 대응한다. acceptance 중 runtime contract 결함이 드러나면 공용 hook bundle의 최소 호환 수정과 전파 검증까지 같은 feature에서 닫는다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

- **새 acceptance invariant — dual-setting parity 완료는 문서·schema 일치만으로 선언하지 않는다.** Codex에서 `spec-create`와 `spec-upgrade`를 실제 호출한 disposable fixture가 두 runtime 설정을 만들고, 멱등성·사용자 handler 보존·broken JSON의 runtime별 독립 실패를 관찰해야 한다.
- **새 lifecycle evidence contract**: Codex 0.124.0+ trusted project에서 SessionStart context, PreToolUse gate, `clear|compact` context reinjection, PostToolUse subagent watchdog `additionalContext`를 실제 lifecycle로 관찰한다. Claude Code 지원 버전에서도 동일 script bundle의 핵심 SessionStart/PreToolUse smoke를 유지한다.
- **SessionStart stdout contract**: 공용 context hook은 Codex가 요구하는 `hookSpecificOutput.hookEventName=SessionStart`와 `additionalContext` JSON envelope를 출력한다. 같은 envelope가 Claude Code에서도 context로 소비돼야 하며, `jq` 또는 `python3`가 없으면 fail-open한다.
- **trust boundary는 acceptance 일부다.** project definition이 미신뢰이면 `/hooks`의 사용자-visible 검토·신뢰 없이는 lifecycle PASS를 선언하지 않는다. 자동 trust, undocumented trust store 수정, `--dangerously-bypass-hook-trust`는 사용하지 않는다.
- runtime acceptance는 영구 fixture나 새 테스트 프레임워크를 만들지 않는다. 실행 증거·명령·결과는 ignored implementation ledger와 오늘 work log에 기록하고, 최종 live census 후 `spec-sync`로 discussion의 결정과 Feature 1~3 완료 상태를 global spec에 반영한다.

## Decisions and Assumptions

- 구현 전 probe에서 Codex `0.146.0`, `hooks stable true`, Claude Code `2.1.223`을 확인했다. 현재 repo의 새 `codex exec`는 trust bypass 없이 정상 시작했고 SessionStart hook stdout이 추가 입력으로 소비되는 징후(`Reading additional input from stdin...`)가 있었다. 이는 착수 조건일 뿐 각 lifecycle AC의 PASS 증거를 대체하지 않는다.
- 실제 skill invocation은 현재 mirror의 Codex skill을 disposable git repo의 `.codex/skills/`에 설치해 `$spec-create`/`$spec-upgrade`로 호출한다. fixture가 만드는 산출물만 판정하며 다른 global skill이나 user-global config를 변경하지 않는다.
- macOS의 `/tmp`→`/private/tmp` alias가 Codex sandbox 경계와 patch 대상 경로를 갈라놓을 수 있으므로, fixture root는 생성 즉시 `pwd -P`/`realpath`로 canonicalize하고 이후 `codex -C`, prompt의 절대 경로, evidence에 그 한 경로만 사용한다. actual invocation은 `.codex/hooks.json` project-control path 쓰기까지 필요한 `--sandbox danger-full-access` mode를 **disposable canonical fixture에만** 한정한다. 각 fixture는 read-only auth symlink만 공유하는 별도 disposable `CODEX_HOME`을 사용해 Codex의 project trust/state/config write도 fixture 안에 격리한다. `--dangerously-bypass-approvals-and-sandbox`, hook trust bypass, repo 밖 쓰기는 금지하고 user-global config hash를 invocation마다 전후 비교한다.
- watchdog 5분 경계는 실제로 5분을 대기하지 않고, 같은 subagent session의 첫 tool call이 만든 runtime state의 timestamp만 해당 disposable probe 안에서 301초 전으로 조정한 뒤 다음 PostToolUse 결과의 `additionalContext`를 관찰한다. script를 수정하거나 threshold를 낮추지 않는다.

## Scope

- **In**: disposable Codex `spec-create`/`spec-upgrade` 실제 호출 / absent·existing mixed group·partial/old install·broken JSON·idempotency fixture / 현재 repo의 trusted Codex SessionStart·PreToolUse·compact/clear·subagent PostToolUse lifecycle / Claude Code SessionStart·PreToolUse smoke / 발견된 공용 SessionStart 출력 계약의 최소 호환 수정과 5면 전파 / command·version·trust·result ledger / Feature 1~3 final census와 spec-sync handoff.
- **Out**: 새 hook 종류·threshold·SKILL 동작 변경 / 영구 fixture·테스트 framework / trust 자동 승인·bypass / undocumented trust file 수정 / 승인되지 않은 user-global Codex·Claude 설정 수정 / plugin packaging / 이 feature에서 `_sdd/spec/` 직접 수정.
<!-- spec-update-todo-input-end -->

# Propagation Surfaces

| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | spec-create 실제 dual-setting 설치 | 각 disposable fixture의 `.claude/hooks/{worklog-gate,worklog-context,harness-context,agent-watchdog}.sh`, `.claude/settings.json`, `.codex/hooks.json` | `find .claude/hooks -maxdepth 1 -type f -name '*.sh' -print \| sort` → 정확히 4 path; `jq -S '.hooks' .claude/settings.json .codex/hooks.json` → PreToolUse/Bash·PostToolUse/none·SessionStart/none·SessionStart/clear\|compact; `sha256sum` → current reference와 일치 | Task 1 |
| P2 | spec-upgrade partial/broken 보완 | 각 disposable fixture의 같은 script 4개와 JSON 2개, `_sdd/spec/` upgrade inventory | P1의 `find`·`jq`·`sha256sum` query + `find _sdd/spec -maxdepth 1 -type f -print \| sort` → current spec-upgrade Output Contract inventory | Task 2 |
| P3 | Codex lifecycle 4종 | 현재 repo와 독립 deny fixture의 `.codex/hooks.json`, `.claude/hooks/*.sh` | `jq -r '.hooks \| to_entries[] as $e \| $e.value[] \| [$e.key, (.matcher // "none"), .hooks[].command] \| @tsv' .codex/hooks.json` → exact 4-map; `codex --version` 0.124.0+; `codex features list \| rg '^hooks\\s+stable\\s+true'` | Task 3 |
| P4 | Claude lifecycle smoke | 독립 fixture의 `.claude/settings.json`, `.claude/hooks/*.sh` | `jq`의 P3 동형 query를 `.claude/settings.json`에 실행 → exact 4-map; `claude --version` → 2.1.220+; script `sha256sum` → current reference와 일치 | Task 4 |

# Part 2: Tasks

### Task 1: Codex에서 `spec-create` dual-setting 설치를 실제 수용 검증

현재 Codex mirror skill을 disposable git repo에서 실제 호출해 canonical 설치 계약이 실행 가능한지 검증한다.

**Contracts**:
- fixture는 실행마다 새 임시 git repo이고 현재 repo·user-global 설정을 수정하지 않는다. current `.codex/skills/spec-create/`와 reference asset을 project-local skill로 설치한 뒤 `$spec-create`를 명시 호출한다.
- 각 fixture는 canonical physical path로 만든 뒤 `CODEX_HOME=<fixture-isolated-home> codex exec --sandbox danger-full-access -m gpt-5.6-sol -C <canonical-fixture>`에서 호출한다. 격리 홈에는 user-global `auth.json`의 read-only symlink만 두며 global `config.toml`은 읽거나 쓰지 않는다. 기본 read-only/workspace-write가 `.codex` control path까지 쓸 것이라 가정하거나 `/tmp` alias를 혼용하지 않는다. prompt도 현재 physical fixture 밖 쓰기와 user-global 수정을 금지한다.
- absent fixture, valid-existing fixture, broken-one-runtime fixture를 각각 사용한다. valid-existing에는 다른 top-level key/event와 SDD handler가 사용자 handler와 섞인 non-canonical matcher group을 둔다.
- second invocation 전후 deterministic product surface(`.claude/hooks/`, 두 JSON, 하네스/spec 문서)의 content manifest가 동일해야 한다. append-only evidence surface인 `_sdd/work_log/`는 허용 delta로 분리해 append 외 rewrite가 없는지만 검사하고, timestamp와 Codex session artifact는 manifest에서 제외한다.

**Acceptance Criteria**:
- [x] AC1: 세 fixture 모두 실제 `codex exec` transcript가 `$spec-create` 사용과 성공/partial report를 남기며, 공용 script 4개가 current reference와 byte-identical이고 두 JSON의 SDD map이 canonical과 일치한다(깨진 runtime은 제외).
- [x] AC2: absent fixture는 두 JSON을 생성한다. valid-existing fixture는 SDD group만 canonical로 바꾸고 모든 non-SDD handler의 원래 event+matcher, 다른 top-level key/event를 보존한다.
- [x] AC3: broken-one-runtime fixture에서 깨진 파일의 pre/post bytes가 같고 반대 runtime JSON과 script 4개는 정상 설치된다. report가 runtime별 skip/성공을 구분한다.
- [x] AC4: 각 fixture의 두 번째 실제 invocation 뒤 deterministic product manifest diff가 0이고 SDD command는 script별/runtime별 정확히 1개다. `_sdd/work_log/`는 새 항목 append만 허용하며 기존 bytes가 prefix로 보존된다.

**Target Files**:
- [C] `_sdd/implementation/2026-08-06_implementation_ledger_codex_hook_runtime_acceptance.md` -- Feature 1/2 구조 증거와 분리된 실제 invocation·lifecycle transcript/fixture evidence

---

### Task 2: Codex에서 `spec-upgrade` partial/broken 설치를 실제 수용 검증

upgrade 고유 delta가 Claude-only·Codex-only·old group을 dual-setting canonical로 보완하는지 실제 호출한다.

**Contracts**:
- 새 fixture에 current `.codex/skills/spec-upgrade/`와 canonical 참조용 `spec-create`를 project-local로 설치한다.
- Task 1과 같은 canonical physical path + fixture별 isolated `CODEX_HOME` + fixture 한정 `danger-full-access` invocation + global hash 불변 contract를 적용한다.
- partial fixture는 Claude-only SDD group, Codex-only SDD group, old command/matcher와 보존해야 할 사용자 handler/top-level key를 함께 둔다. broken fixture는 한 runtime JSON만 invalid bytes로 둔다.
- upgrade가 스펙 자체를 불필요하게 재작성했는지는 fixture의 사전 최소 old-format spec과 결과 inventory로 별도 기록한다.

**Acceptance Criteria**:
- [x] AC1: 실제 `$spec-upgrade` transcript가 partial/old 상태를 진단하고 두 runtime map을 canonical로 보완하며 공용 script 4개를 current reference와 byte-identical하게 설치한다.
- [x] AC2: partial fixture의 non-SDD handler는 원래 event+matcher와 bytes-equivalent command를 유지하고 다른 top-level key/event가 보존된다. SDD command는 script별/runtime별 1개다.
- [x] AC3: broken fixture의 invalid file bytes는 같고 반대 runtime과 script 설치는 성공하며 report가 runtime별 partial failure를 명시한다.
- [x] AC4: 두 번째 실제 invocation 뒤 hook/script/settings manifest diff가 0이고, old-format spec upgrade 산출물은 현재 spec-upgrade Output Contract의 inventory를 만족한다.

**Target Files**:
- [M] `_sdd/implementation/2026-08-06_implementation_ledger_codex_hook_runtime_acceptance.md` -- upgrade fixture·멱등·partial failure evidence

---

### Task 3: trusted Codex에서 네 lifecycle을 실제 관찰

현재 repo의 exact self-host definition을 trust bypass 없이 새 Codex session에서 실행해 구조 검증을 lifecycle evidence로 승격한다.

**Contracts**:
- `--dangerously-bypass-hook-trust`, trust store 직접 수정은 금지한다. 미신뢰 경고가 나오면 `/hooks`에서 사용자 검토·신뢰가 이 task의 유일한 unblock 경로이며, 그 명시적 사용자 승인이 Codex의 documented trust state를 갱신하는 것은 허용된 delta로 기록한다.
- SessionStart·compact·watchdog은 현재 repo에서 관찰한다. PreToolUse deny는 current exact `.codex/hooks.json`과 byte-identical `.claude/hooks/`를 복사한 **독립 disposable git root**에서 `codex -C <fixture>`로 관찰한다. 시작 work log는 부재하고 initial HEAD를 만든 뒤 empty commit을 시도하며, commit이 생성되지 않았음을 확인한다. allow path는 같은 독립 root의 non-commit Bash tool 결과가 보존되는지 본다.
- watchdog은 같은 subagent가 첫 tool로 state를 만든 뒤 자기 session의 start timestamp만 301초 전으로 바꾸고, 바로 그 PostToolUse 결과에서 3요소 nudge를 받는지 확인한다.

**Acceptance Criteria**:
- [x] AC1: trust bypass 없는 새 session의 transcript가 SessionStart `[work log]` prefix와 해당 hook의 고유 문구를 모델 입력에서 식별하고 원래 user prompt의 답을 보존한다.
- [x] AC2: current definition/script와 byte-identical한 독립 root에서 non-commit Bash tool 결과가 보존되고, work log가 없는 상태의 commit attempt는 PreToolUse가 deny하며 `git rev-parse HEAD`가 initial HEAD와 같다.
- [x] AC3: interactive `/compact` 또는 `/clear` 직후 `[harness]`와 `AGENTS.md` 본문 고유 anchor가 재주입됐음을 다음 model turn이 식별한다.
- [x] AC4: 실제 subagent PostToolUse transcript가 state first-call silent 후 301초 probe에서 `additionalContext`의 진행 요약·요구사항 재확인·접근 조정 3요소를 식별하고, 직전 tool result도 보존한다.
- [x] AC5: transcript/명령 census에 hook trust bypass·undocumented trust write가 0이다. `/hooks` 수동 승인이 필요했다면 사용자 승인 사실, 승인으로 추가된 exact 4개 definition hash, 승인 직후 baseline을 기록하고 이후 실행에서 그 baseline hash가 유지된다.

**Target Files**:
- [M] `_sdd/implementation/2026-08-06_implementation_ledger_codex_hook_runtime_acceptance.md` -- Codex trust·SessionStart·PreToolUse·compact·watchdog evidence
- [M] `.claude/hooks/{worklog-context,harness-context,agent-watchdog}.sh` -- self-host runtime output contract와 review-fix watchdog 문구
- [M] `.claude/skills/spec-create/references/hooks/{worklog-context,harness-context,agent-watchdog}.sh`
- [M] `.codex/skills/spec-create/references/hooks/{worklog-context,harness-context,agent-watchdog}.sh`
- [M] `.claude/skills/spec-upgrade/references/hooks/{worklog-context,harness-context,agent-watchdog}.sh`
- [M] `.codex/skills/spec-upgrade/references/hooks/{worklog-context,harness-context,agent-watchdog}.sh`

---

### Task 4: Claude smoke와 Feature 1~3 final census

같은 script bundle이 지원 Claude Code에서도 핵심 lifecycle을 유지하는지 smoke하고, 전체 목표의 누락을 마지막으로 닫는다.

**Contracts**:
- Claude smoke는 project-local `.claude/settings.json`/script를 둔 disposable fixture에서 수행한다. user-global 설정을 수정하지 않는다.
- final census는 discussion decision, Feature 1 script 20면, Feature 2 SKILL 4면+self-host, Feature 3 runtime evidence를 한 표로 대조한다. 구조 PASS를 lifecycle PASS로 대체해 기록하지 않는다.

**Acceptance Criteria**:
- [x] AC1: Claude Code 2.1.220+ 실제 session이 SessionStart work-log context를 식별하고 non-commit Bash 결과를 보존한다. work log 없는 fixture commit은 PreToolUse가 deny하고 commit이 생성되지 않는다.
- [x] AC2: Feature 1의 4×5 script가 종류별 byte-identical·`bash -n`을 유지하고 Feature 2의 mirror 2쌍·Codex map 3면·JSON parse·stale 0을 유지한다.
- [x] AC3: discussion의 확정 결정(공용 경로, dual install, independent merge, broken-file partial, trust boundary, watchdog additionalContext, Claude smoke) 각각에 structural evidence와 runtime evidence 또는 명시적 blocker가 1개 이상 연결된다.
- [x] AC4: `git diff --check` clean, 공용 SessionStart 호환 수정 2종×5면과 watchdog review fix 1종×5면 외 task 범위 밖 source/settings 변경 0, global config는 사용자 승인된 exact trust delta 외 변경 0, implementation ledger·오늘 work log에 version·command class·fixture/result·review evidence가 있고 `spec-sync` 입력으로 Feature 1~3 draft가 준비됐다.

**Target Files**:
- [M] `_sdd/work_log/2026-08-06.md` -- runtime acceptance와 final census 요약
- [M] `_sdd/implementation/2026-08-06_implementation_ledger_codex_hook_runtime_acceptance.md` -- Claude smoke·최종 decision/evidence census

# Open Questions

- 현재 repo exact definition이 이미 trusted인지 lifecycle transcript로 확인한다. 미신뢰이면 자동 우회하지 않고 형님의 `/hooks` 사용자 승인만 요청한다. 그 전에도 Task 1·2와 Claude smoke·구조 census는 계속 진행한다.
