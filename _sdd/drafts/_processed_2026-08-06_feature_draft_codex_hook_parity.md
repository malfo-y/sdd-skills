# Feature Draft: SDD 하네스의 Codex hook parity — 공용 script 기반

> 규모 판정: 분할 필요 — 분할 계획 포함. script semantics, dual-setting 설치, 실제 lifecycle 수용 검증이 다대다로 연접해 3개 feature로 rolling split하며, Part 2는 첫 feature만 다룬다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

Codex가 stable project hook과 평문 context 주입을 지원하므로, “Codex에는 hook 메커니즘이 없어 Claude 자산만 설치한다”는 기존 플랫폼 비대칭 계약을 단계적으로 종료한다. 최종 상태에서는 어느 runtime에서 `spec-create`·`spec-upgrade`를 호출해도 공용 script 4개와 Claude/Codex 등록이 함께 설치되고, 네 lifecycle이 양 runtime에서 실제로 검증된다.

### Rolling Split Plan

1. **Feature 1 — 공용 hook script 기반 (이 draft의 Part 2)**: 기존 `.claude/hooks/` 소비 경로를 유지한 채 4개 script의 root resolution·설명·watchdog 반환을 dual-runtime contract로 전환하고 5-way mirror 및 payload fixture로 검증한다. 이 단계만으로 Codex hook 설치 parity를 선언하지 않는다.
2. **Feature 2 — dual-setting 설치 계약**: `spec-create`·`spec-upgrade`가 호출 runtime과 무관하게 `.claude/settings.json`과 `.codex/hooks.json`을 함께 독립·멱등 병합하도록 4개 SKILL mirror를 갱신하고, 이 repo에 `.codex/hooks.json`을 self-host 등록한다. dual-setting의 normative contract는 `spec-create` §3e 한 곳에 두고 `spec-upgrade`는 upgrade 고유 delta와 canonical 참조만 소유한다.
3. **Feature 3 — runtime acceptance와 spec convergence**: disposable fixture에서 두 설치 workflow의 재실행·사용자 key 보존·깨진 JSON 독립 실패를 검증하고, Codex 0.124.0+와 지원 Claude Code에서 네 lifecycle을 실제로 관찰한다. live 구현 census 후 `spec-sync`에 global spec·usage guide·superseding decision·changelog 반영 근거를 인계한다.

### 최종 상태의 새 contract / invariant

- **공용 실행 경로**: script 설치 경로는 호환성을 위해 `.claude/hooks/`로 유지한다. script가 `CLAUDE_PROJECT_DIR`와 git root를 순서대로 해석하므로 Claude Code와 Codex가 같은 bytes를 실행한다.
- **dual-setting 설치**: 하네스 생성·업그레이드는 `.claude/settings.json`과 `.codex/hooks.json`을 항상 함께 등록 대상으로 삼는다. 두 파일은 독립 파싱·key-level merge하며, 깨진 파일은 덮어쓰지 않고 해당 runtime만 skip한 뒤 부분 실패를 알린다.
- **watchdog 의미**: PostToolUse nudge는 top-level `decision: "block"`이 아니라 양 runtime의 공통 의미인 `hookSpecificOutput.additionalContext`를 사용해 원래 tool result를 보존한다.
- **Codex trust 경계**: project hook 등록을 설치 완료로 보되 Codex 0.124.0+와 `/hooks` exact-definition trust 필요를 announce한다. skill은 trust나 사용자 전역 Codex 설정을 자동 변경하지 않는다.
- **완료 게이트**: 구조 parity와 실제 runtime lifecycle 증거가 모두 있어야 전체 Codex hook parity를 완료로 선언한다. 공식 schema/behavior 불일치, `additionalContext`의 result 손실, 사용자 설정 보존과 멱등 merge의 양립 불가가 발견되면 강행하지 않고 재논의한다.

### Feature 1 착수 조건과 가정

- OpenAI Codex 0.124.0+ 공식 schema에서 PreToolUse input의 `session_id`·`tool_input.command`, PostToolUse input의 optional `agent_id`·`agent_type`, PostToolUse output의 `hookSpecificOutput.hookEventName`·`additionalContext`가 유효하다는 조사 결과를 착수 근거로 삼는다. 확신도는 높음(공식 문서·generated schema + 로컬 Codex 0.146.0 확인).
- 구현 시작 시 installed Codex schema를 다시 읽어 위 field와 event name을 확인한다. 하나라도 다르면 Task 1/2를 수정해 추측으로 맞추지 않고 구현을 중단해 재논의한다.
- SessionStart stdout의 developer-context 주입과 event matcher·trust는 Feature 3의 실제 lifecycle gate에서 닫는다. Feature 1은 script I/O contract와 fixture까지만 소유한다.

## Scope

- **전체 In**: 공용 script 4종 / 5-way mirror / dual-setting 설치·독립 병합·announce / project `.codex/hooks.json` / 실제 Claude·Codex lifecycle·설치 fixture / stale 비대칭 census / 후행 spec-sync.
- **현재 Feature 1 In**: `worklog-gate.sh`·`worklog-context.sh`·`harness-context.sh`의 dual-root resolution과 runtime-neutral 설명 / `agent-watchdog.sh`의 runtime-neutral 상태 경로·`additionalContext` 반환 / 4종 × 5 surface byte parity / payload·cwd fixture 검증.
- **Out**: `.claude/hooks/` 경로 이동 / plugin packaging / user-global Codex config·trust 변경 / hook별 opt-in / watchdog threshold·cooldown 조정 / 신규 lifecycle / historical decision·changelog 재작성. Feature 2 전에는 SKILL 설치 계약과 `.codex/hooks.json`을 수정하지 않고, Feature 3 전에는 전체 runtime parity 완료를 선언하거나 `_sdd/spec/*.md`를 직접 수정하지 않는다.
<!-- spec-update-todo-input-end -->

# Propagation Surfaces

| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | project-root resolver + runtime-neutral SessionStart/PreToolUse 설명 | `{.claude/hooks,.claude/skills/spec-create/references/hooks,.codex/skills/spec-create/references/hooks,.claude/skills/spec-upgrade/references/hooks,.codex/skills/spec-upgrade/references/hooks}/{worklog-gate,worklog-context,harness-context}.sh` (3종 × 5 = 15파일) | `for n in worklog-gate worklog-context harness-context; do find .claude/hooks .claude/skills/spec-create/references/hooks .codex/skills/spec-create/references/hooks .claude/skills/spec-upgrade/references/hooks .codex/skills/spec-upgrade/references/hooks -maxdepth 1 -name "$n.sh"; done`의 기대 집합은 각 이름별 위 5 directory 정확히 1개. 현재 15파일 모두 `CLAUDE_PROJECT_DIR` fallback이 `.`이고 header가 Claude Code 전용 | Task 1 |
| P2 | watchdog runtime-neutral state + PostToolUse `additionalContext` | `{.claude/hooks,.claude/skills/spec-create/references/hooks,.codex/skills/spec-create/references/hooks,.claude/skills/spec-upgrade/references/hooks,.codex/skills/spec-upgrade/references/hooks}/agent-watchdog.sh` (5파일) | `find`를 같은 5 directory에 `-name agent-watchdog.sh`로 실행한 기대 집합은 directory별 정확히 1개. 현재 5파일 hash는 동일하며 모두 `claude-agent-watchdog`와 `{"decision":"block","reason":...}`를 포함 | Task 2 |

# Part 2: Tasks

### Task 1: 세 root-relative hook을 dual-root로 전환

Claude Code의 기존 환경변수 경로를 우선 보존하면서, Codex처럼 환경변수가 없는 실행은 현재 git worktree root로 복구한다.

**Contracts**:
- root resolver 순서는 ① nonempty `CLAUDE_PROJECT_DIR`가 실제 directory면 그 경로 ② `git rev-parse --show-toplevel` 성공 경로 ③ 판정 불가다. ①이 nonempty지만 invalid여도 ②를 시도한다.
- resolver 성공 후 해당 root에서 기존 로직을 실행한다. 실패하면 `worklog-gate.sh`는 allow, 두 SessionStart script는 무출력 exit 0이다.
- `worklog-gate.sh`의 commit 탐지·deny JSON·session marker·우회와 두 SessionStart script의 stdout 내용은 root 해석 외에는 바꾸지 않는다.
- header와 root 설명은 Claude Code/Codex 공용 실행 자산임을 말하되, 정본/4 mirror 규율과 `.claude/hooks/` 설치 경로를 유지한다.
- script별 정본은 `.claude/skills/spec-create/references/hooks/`, 나머지 4 surface는 byte-identical 사본이다. 공통 resolver를 위한 새 helper file이나 단일 사용처 abstraction은 만들지 않는다.

**Acceptance Criteria**:
- [x] AC1: installed Codex 0.124.0+의 공식/generated PreToolUse schema에서 `session_id`와 `tool_input.command`를 착수 전에 확인하고 근거 URL/로컬 schema path를 work log에 남긴다. 예상과 다르면 구현을 중단한다.
- [x] AC2: 각 script를 `CLAUDE_PROJECT_DIR=<repo>`로 repo root와 `docs/` cwd에서 실행했을 때 root 실행과 같은 exit code·stdout·판정을 내 기존 Claude 경로가 유지된다.
- [x] AC3: `CLAUDE_PROJECT_DIR`를 unset한 채 repo root와 `docs/` cwd에서 실행해도 git-root fallback으로 AC2와 같은 결과를 낸다. 현재 구현의 `docs/` 실행(하네스 stdout 0 bytes)이 변경 후 root 실행과 byte-identical해지는 것으로 반증 가능하게 확인한다.
- [x] AC4: invalid `CLAUDE_PROJECT_DIR` + repo 하위 cwd는 git-root fallback으로 성공하고, invalid env + git repo가 아닌 빈 fixture는 출력 없이 exit 0 또는 gate allow다.
- [x] AC5: Claude/Codex 대표 PreToolUse payload로 ① 비-commit allow ② 오늘 work log 변경 없는 첫 commit deny ③ `SDD_SKIP_WORKLOG=1` allow를 관찰한다. deny JSON은 `hookSpecificOutput.permissionDecision == "deny"`이고 원래 reason text를 포함한다.
- [x] AC6: `worklog-context.sh` stdout은 기존 work log 상태·parser 경고 문구를 유지한다. `harness-context.sh`는 `[harness]` 다음 bytes가 marker 밖 문장을 포함한 fixture `AGENTS.md`와 동일하고, 파일이 없으면 무출력 exit 0이다.
- [x] AC7: P1의 15파일이 모두 `bash -n`을 통과하고 script 종류별 5개 hash가 1종이다.

**Target Files**:
- [M] `.claude/skills/spec-create/references/hooks/{worklog-gate,worklog-context,harness-context}.sh` -- 정본 3종
- [M] `.codex/skills/spec-create/references/hooks/{worklog-gate,worklog-context,harness-context}.sh` -- mirror 3종
- [M] `.claude/skills/spec-upgrade/references/hooks/{worklog-gate,worklog-context,harness-context}.sh` -- mirror 3종
- [M] `.codex/skills/spec-upgrade/references/hooks/{worklog-gate,worklog-context,harness-context}.sh` -- mirror 3종
- [M] `.claude/hooks/{worklog-gate,worklog-context,harness-context}.sh` -- dogfooding 사본 3종

---

### Task 2: watchdog을 공통 advisory output으로 전환

Claude에서 결과 보존용으로 쓰던 top-level block이 Codex에서는 결과를 대체하므로, 양 runtime이 공유하는 additional context 의미로 좁힌다.

**Contracts**:
- 상태 경로는 `${TMPDIR:-/tmp}/sdd-agent-watchdog/<session_id>/<agent_id>.*`로 runtime-neutral하게 바꾼다. 기존 `claude-agent-watchdog` 상태를 migrate하거나 읽지 않는다 — 임시 cooldown 상태이며 호환 자산이 아니다.
- `agent_id`가 있는 payload만 추적한다. 300초 threshold·300초 cooldown·jq→python3 fallback·모든 판정 불가의 fail-open은 유지한다.
- 발동 JSON은 `{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"<nudge>"}}`이며 top-level `decision`·`reason`은 없다. nudge의 자평·싼 경로 전환·최종 언급 3요소는 보존한다.
- header와 설명은 Claude Code/Codex 공용 PostToolUse advisory임을 말한다. 정본/4 mirror 규율은 Task 1과 같다.

**Acceptance Criteria**:
- [x] AC1: installed Codex 0.124.0+ 공식 generated PostToolUse input/output schema에서 optional `agent_id`·`agent_type`, `hookSpecificOutput.hookEventName`, `additionalContext`를 착수 전에 확인하고 work log에 근거를 남긴다. 예상과 다르면 구현을 중단한다.
- [x] AC2: fixture에서 ① `agent_id` 없음은 무출력 ② 최초 agent 호출은 neutral state file 생성·무출력 ③ start를 301초 과거로 바꾼 다음 호출은 parseable `hookSpecificOutput` 출력 ④ cooldown 내 다음 호출은 무출력이다.
- [x] AC3: 발동 payload의 `hookEventName`은 정확히 `PostToolUse`, `additionalContext`는 nonempty이고 자평·전환·최종 언급 3요소를 포함한다. 출력 전체에 top-level `decision`·`reason` key가 없다.
- [x] AC4: jq 우선과 jq 부재 python3 fallback에서 AC2·AC3이 같고, 둘 다 없거나 JSON 파싱 실패·상태 기록 실패에서는 무출력 exit 0이다.
- [x] AC5: P2의 5파일이 모두 `bash -n`을 통과하고 hash가 1종이다. `rg 'Claude Code PostToolUse|claude-agent-watchdog|"decision":"block"'` 잔존이 0건이다.

**Target Files**:
- [M] `.claude/skills/spec-create/references/hooks/agent-watchdog.sh` -- 정본
- [M] `.codex/skills/spec-create/references/hooks/agent-watchdog.sh` -- mirror
- [M] `.claude/skills/spec-upgrade/references/hooks/agent-watchdog.sh` -- mirror
- [M] `.codex/skills/spec-upgrade/references/hooks/agent-watchdog.sh` -- mirror
- [M] `.claude/hooks/agent-watchdog.sh` -- dogfooding 사본

---

### Task 3: Feature 1 mirror·scope census를 검증 (read-only, 마지막)

두 구현 task가 같은 5 surface 규율을 공유하므로 누락·예상 밖 수정을 omission 표와 diff로 마감한다.

**Contracts**: 없음 (read-only 검증)

**Acceptance Criteria**:
- [x] AC1: P1·P2의 exact `find` query로 4 script × 5 directory 표를 만들고, 각 cell이 정확히 한 파일이며 script별 hash가 1종이다. 단순 총 hit count로 대체하지 않는다.
- [x] AC2: 20파일 전체 `bash -n`이 통과하고, `rg 'Claude Code (PreToolUse|PostToolUse|SessionStart) 훅|claude-agent-watchdog|"decision":"block"'`의 stale hit가 0건이다. runtime 비교 설명의 `Claude Code`는 false positive 목록으로 분리해 계약 모순 여부를 확인한다.
- [x] AC3: `git diff --name-only`의 feature 소유 변경은 P1·P2의 20파일과 해당일 work log뿐이다. SKILL 본문, `.claude/settings.json`, `.codex/hooks.json`, `_sdd/spec/` 변경은 0건이다.
- [x] AC4: `git diff --check` 무출력이고 Task 1·2 fixture 명령, schema source, 관찰 결과를 해당일 work log에 남긴다.

**Target Files**:
- [TBD] `_sdd/work_log/<implementation-date>.md` -- 구현일의 schema·fixture·census 증거 기록(구현 날짜가 아직 정해지지 않아 파일명 미확정)

# Open Questions

- 사용자 확인이 필요한 in-scope 항목은 없다. Feature 1 schema 착수 조건이 어긋나면 AC를 완화하거나 추측 구현하지 않고 형님께 재논의를 요청한다.
