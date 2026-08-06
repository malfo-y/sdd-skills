# Feature Draft: Codex hook dual-setting 설치 계약

> 규모 판정: 적격 — normative 설치 계약(spec-create), upgrade delta(spec-upgrade), self-host 등록이 Task 1~3에 1:1 대응하고 마지막 census로 전파 누락을 닫을 수 있어 단일 컨텍스트에서 눈검산 가능하다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

- **새 contract — hook bundle은 호출 runtime과 무관한 dual-setting 산출물이다.** `spec-create`·`spec-upgrade`가 하네스를 설치하면 공용 script 4개를 기존 `.claude/hooks/`에 verbatim 배치하고 `.claude/settings.json`과 `.codex/hooks.json`을 항상 함께 등록 대상으로 삼는다.
- **normative contract는 `spec-create` §3e 한 곳이 소유한다.** 두 설정의 event/matcher/command, 독립 병합, 사용자 항목 보존, 파싱 실패, announce 규칙은 §3e가 canonical이다. `spec-upgrade` Step 6은 canonical 참조와 old/partial 설치를 보완하는 upgrade 고유 delta, 그리고 spec-create 부재 환경의 최소 complete fallback만 가진다.
- **Codex 등록 형태**: `<repo>/.codex/hooks.json`에 PreToolUse(`matcher: "Bash"`), PostToolUse(matcher 없음), SessionStart(matcher 없음 / `clear|compact`) 그룹을 등록한다. command는 공식 권장대로 session cwd에 기대지 않고 `bash "$(git rev-parse --show-toplevel)/.claude/hooks/<script>.sh"`로 공용 설치본을 찾는다.
- **독립 merge invariant**: 두 JSON은 각각 별도 parse/merge unit다. script path를 포함하는 기존 command의 outer group을 계약 형태로 교체하고, mixed group의 사용자 command·다른 hook·다른 top-level key는 보존한다. 한 파일이 깨졌으면 원본을 덮어쓰지 않고 그 runtime 등록만 skip하며 다른 파일과 script 설치는 계속한다.
- **Codex activation boundary**: 설치 보고는 Codex hooks stable 기준 0.124.0+, project `.codex/` layer trust, exact hook definition을 `/hooks`에서 검토·신뢰하기 전 무발동, definition 변경 시 재검토 가능성을 명시한다. skill은 trust를 자동 승인하거나 `~/.codex/config.toml` 등 user-global 상태를 수정하지 않는다.
- 이 feature는 계약·self-host 구조까지만 소유한다. 실제 `spec-create`/`spec-upgrade` 재실행·깨진 JSON fixture와 Claude/Codex lifecycle 수용 증거는 후속 runtime acceptance feature가 닫기 전까지 전체 parity 완료 근거로 사용하지 않는다.

## Decisions and Assumptions

- **공용 script 경로는 `.claude/hooks/` 유지**(확신도 높음, 사용자 추가 확인 불필요): Feature 1이 이미 이 경로의 dogfooding 사본과 네 reference mirror를 byte-identical 공용 자산으로 만들었고 기존 소비 repo도 이 경로를 계약으로 가진다. `.codex/hooks/`에 같은 bytes를 한 벌 더 복제하면 동기화 surface만 늘고, runtime-neutral 경로로 이동하면 기존 Claude command와 소비 repo를 깨므로 둘 다 기각한다.
- **trust persistence의 내부 저장 경로는 이 feature가 가정하지 않는다**: 공식 계약은 `/hooks`의 exact-definition trust까지다. 저장 구현은 바뀔 수 있으므로 self-host task는 확인 가능한 `~/.codex/config.toml` 사전·사후 불변과 trust 변경 명령 미실행만 검증하고, 실제 trust 상태는 Feature 3 lifecycle 수용에서 사용자-visible `/hooks` 상태로 확인한다.
- **Feature 2 diff baseline**: Feature 1의 tracked script 20개와 discussion/draft/work-log dirty state가 이미 존재한다. 구현 시작 ledger에 `git status --short`, tracked diff path set, 기존 untracked artifact의 hash를 기록하고 Feature 2 추가 변경만 그 baseline과 집합·hash delta로 판정한다.

## Scope

- **In**: Claude·Codex `spec-create` SKILL 2파일의 dual-setting normative contract / `spec-upgrade` SKILL 2파일의 upgrade delta·fallback / checklist·validation·Output Contract·announce 전파 / 이 repo `.codex/hooks.json` self-host 등록 / JSON example parse·event/matcher/command·mirror·stale census.
- **Out**: 공용 script 변경(Feature 1 완료) / `.claude/settings.json` 동작 변경 / 실제 skill invocation·사용자 설정 fixture·lifecycle 관찰(Feature 3) / trust 자동 승인·dangerous bypass 권장 / user-global config / plugin packaging / `_sdd/spec/*.md` 직접 수정.
<!-- spec-update-todo-input-end -->

# Propagation Surfaces

| ID | Change element | Required surfaces | Discovery evidence | Owner task |
|---|---|---|---|---|
| P1 | spec-create dual-setting normative contract(checklist·Hard Rules·Step 3/3e·validation·Output Contract·announce) | `.claude/skills/spec-create/SKILL.md`, `.codex/skills/spec-create/SKILL.md` | `cmp -s` 현재 동일. `rg -n '\.claude/hooks/|\.claude/settings\.json|Claude Code가 직접 실행'` 결과가 두 파일 각각 checklist 26, Hard Rule 74, Step 3 158, §3e 214+, validation 309, output 329~331에 있고 `.codex/hooks.json` hit는 0 | Task 1 |
| P2 | spec-upgrade dual-setting upgrade delta·fallback·validation·announce | `.claude/skills/spec-upgrade/SKILL.md`, `.codex/skills/spec-upgrade/SKILL.md` | `cmp -s` 현재 동일. 같은 `rg`가 checklist 28, Step 6 155+, validation 180, output 192에 Claude-only 계약을 반환하고 `.codex/hooks.json` hit는 0 | Task 2 |
| P3 | repo self-host Codex hook definition | `.codex/hooks.json` | `test -e .codex/hooks.json`은 false, `.claude/settings.json`에는 script 4종의 동일 event/matcher group이 존재. 공식 Codex docs는 `<repo>/.codex/hooks.json`과 git-root command를 명시 | Task 3 |

# Part 2: Tasks

### Task 1: `spec-create` §3e를 dual-setting canonical으로 확장

하네스 설치의 단일 normative contract가 두 runtime 설정을 결정하도록 checklist부터 output까지 같은 의미로 전파한다.

**Contracts**:
- script 4개는 기존대로 `.claude/hooks/`에 verbatim 설치한다. 새 `.codex/hooks/` script 사본이나 chmod 단계는 만들지 않는다.
- `.claude/settings.json`의 기존 4 group·command는 그대로 유지하고, `.codex/hooks.json`에는 같은 event/matcher set과 git-root command 4개를 둔다.
- 각 JSON은 독립적으로 key-level idempotent merge한다. 파일 부재는 해당 runtime 4 group만으로 생성한다. 파일 존재 시 command가 `.claude/hooks/<script>.sh`를 포함하는 group을 script별로 찾아 outer group 전체를 계약 형태로 교체한다.
- 교체 group에 사용자 command가 섞여 있으면 사용자 handler를 별도 matcher group으로 보존한다. 다른 event group, `permissions`·`description` 등 top-level key, 사용자 hook handler는 보존한다.
- 파싱 불가 file은 byte-preserved하고 그 runtime 등록만 skip한다. 반대 runtime merge와 script copy는 계속하며 최종 보고에 Claude/Codex 각각 생성·교체·skip 상태를 적는다.
- Codex announce는 0.124.0+, project layer trust, `/hooks` exact-definition 검토·신뢰 전 무발동, 변경 시 재검토를 포함한다. 자동 trust와 user-global config 변경은 금지한다. 기존 Claude announce와 gate/context 설명은 보존한다.

**Acceptance Criteria**:
- [x] AC1: checklist·Hard Rules·Step 3·§3e·Step 5 validation·Output Contract에서 `.claude/settings.json`과 `.codex/hooks.json`이 모두 설치 대상으로 일관되게 등장하고, `.claude/hooks/`만 script 배치 경로로 남는다.
- [x] AC2: §3e에 두 JSON example이 각각 하나 있고 모두 parser를 통과한다. 각 example의 script→(event, matcher, command) map은 4종 정확히 1회이며, Codex command는 모두 `$(git rev-parse --show-toplevel)/.claude/hooks/<script>.sh`를 포함하고 `$CLAUDE_PROJECT_DIR`를 포함하지 않는다.
- [x] AC3: §3e가 두 JSON의 독립 parse/merge, outer-group 교체, mixed-group 사용자 handler 분리 보존, 다른 top-level/event 보존, runtime별 broken-file skip·partial report를 명시한다.
- [x] AC4: Output Contract에 두 설정 파일과 runtime별 merge 결과가 있고, announce에 Codex 0.124.0+·project trust·`/hooks`·exact definition 변경 시 재검토·무발동이 모두 있다. `--dangerously-bypass-hook-trust`나 user-global 수정 권장은 0건이다.
- [x] AC5: `.claude/skills/spec-create/SKILL.md`와 `.codex/skills/spec-create/SKILL.md`가 byte-identical이며, hook 관련 문맥에서 `.claude/settings.json`만을 유일한 등록 대상으로 말하는 omission이 0건이다.

**Target Files**:
- [M] `.claude/skills/spec-create/SKILL.md` -- dual-setting normative contract
- [M] `.codex/skills/spec-create/SKILL.md` -- byte-identical mirror

---

### Task 2: `spec-upgrade`에 dual-setting upgrade delta를 반영

canonical prose를 복제하지 않고, old/partial 설치를 현재 dual-setting 상태로 보완하는 upgrade 고유 책임과 spec-create 부재 fallback만 둔다.

**Contracts**:
- Step 6은 설치 계약의 canonical이 `spec-create` §3e임을 명시한다. spec-create가 있으면 그 계약을 읽어 적용한다.
- upgrade delta는 기존 repo가 `.claude/settings.json`만, `.codex/hooks.json`만, 또는 old command/matcher를 가진 상태에서 두 runtime 계약을 보완하고 재실행 diff가 없도록 하는 것이다.
- spec-create가 없는 환경의 fallback은 두 파일의 exact 4-group event/matcher/command map, 독립 merge·broken-file skip·사용자 보존, runtime별 report와 Codex announce를 빠짐없이 제공한다. spec-create의 설계 rationale를 반복하지 않는다.

**Acceptance Criteria**:
- [x] AC1: checklist·Step 6·Step 7 validation·Output Contract가 두 설정 파일과 script 4종을 모두 명시하며, Step 6이 `spec-create` §3e를 canonical로 가리킨다.
- [x] AC2: Step 6 fallback의 Claude/Codex 4-group map을 구조화해 추출하면 Task 1 §3e examples와 event/matcher/command가 정확히 일치한다.
- [x] AC3: Step 6이 partial install 3종(Claude-only, Codex-only, old group)의 보완·재실행 멱등, 두 파일 독립 처리, broken-file byte preservation, 사용자 key/hook 보존을 명시한다.
- [x] AC4: Output Contract/announce가 runtime별 merge 결과와 Codex 0.124.0+·project trust·`/hooks` 무발동 경계를 포함하고, user-global config·trust 자동 변경을 지시하지 않는다.
- [x] AC5: `.claude/skills/spec-upgrade/SKILL.md`와 `.codex/skills/spec-upgrade/SKILL.md`가 byte-identical이며 Claude-only 설치 omission이 0건이다.

**Target Files**:
- [M] `.claude/skills/spec-upgrade/SKILL.md` -- upgrade delta와 fallback
- [M] `.codex/skills/spec-upgrade/SKILL.md` -- byte-identical mirror

---

### Task 3: project `.codex/hooks.json`을 self-host 등록

이 repo가 후속 runtime acceptance에서 소비 repo와 동일한 exact hook definition을 실행하도록 canonical Codex example을 dogfooding한다.

**Contracts**:
- SDD 소유 group은 PreToolUse `Bash`, PostToolUse matcher 없음, SessionStart matcher 없음/`clear|compact` 네 개다.
- command 4개는 `bash "$(git rev-parse --show-toplevel)/.claude/hooks/<script>.sh"`이고 `.claude/hooks/`의 Feature 1 사본을 실행한다.
- `.claude/settings.json`과 user-global config는 수정하지 않고, `/hooks`·trust bypass 등 persisted trust를 바꾸는 명령을 실행하지 않는다. trust 내부 저장 경로는 추측하지 않는다.

**Acceptance Criteria**:
- [x] AC1: `.codex/hooks.json`이 parser를 통과하고 script→(event, matcher, command) map이 Task 1의 Codex example과 정확히 같다. script별 command는 1개다.
- [x] AC2: repo root와 `docs/` cwd에서 네 command를 shell-expand했을 때 모두 같은 repo의 `.claude/hooks/<script>.sh`를 찾고 `bash -n`을 통과한다.
- [x] AC3: `.claude/settings.json`의 Feature 2 baseline 대비 hash/diff가 같고, `~/.codex/config.toml`의 사전·사후 existence+hash가 같다. 구현 명령 기록에 `/hooks` 실행·trust 승인·`--dangerously-bypass-hook-trust`가 0건이다. repo 밖 path를 git pathspec으로 검사하거나 undocumented trust file 경로를 가정하지 않는다.

**Target Files**:
- [C] `.codex/hooks.json` -- project-local Codex hook definition

---

### Task 4: dual-installation contract census (read-only, 마지막)

Claude-only 설치 문맥과 example/validation/output omission을 전수 대조해 다중 mirror 전파를 닫는다.

**Contracts**: 없음 (read-only 검증)

**Acceptance Criteria**:
- [x] AC1: 두 spec-create 파일과 두 spec-upgrade 파일의 hook 설치 문맥(checklist, Hard Rules/Step 6, 설치 본문, validation, Output Contract, announce)을 표로 열거하고 각 문맥에 dual-setting 또는 명시적 runtime 한정이 있어 omission 0이다.
- [x] AC2: live SKILL 범위에서 `Claude Code가 직접 실행|\.claude/settings\.json` hit를 전수 분류해 Codex hook 부재/Claude-only bundle을 현재 사실로 단정하는 stale 문장이 0건이다. runtime별 command·announce 설명은 허용 근거를 표에 남긴다.
- [x] AC3: spec-create pair와 spec-upgrade pair가 각각 byte-identical이고, 세 파일의 Codex event/matcher/command map(§3e example, Step 6 fallback, `.codex/hooks.json`)이 동일하다.
- [x] AC4: 구현 시작 ledger에 Feature 1 tracked path set과 기존 untracked artifact hash baseline이 있다. 종료 snapshot과 비교했을 때 Feature 2가 추가한 tracked/untracked 변경은 Task 1~3의 5 구현 파일 + 오늘 work log/ignored ledger뿐이고, baseline의 Feature 1 files·기존 artifact는 Feature 2 task에 의해 예상 밖으로 바뀌지 않았다. `git diff --check` 무출력, `_sdd/spec/` 변경 0건이다.

**Target Files**:
- [TBD] `_sdd/work_log/<implementation-date>.md` -- 구현일의 JSON parse/map/census·review 증거(구현 날짜 미확정)

# Open Questions

- 사용자 확인이 필요한 in-scope 항목은 없다. 실제 skill invocation과 lifecycle 수용 검증은 Feature 3에서 수행하며, 이 feature의 구조 검증만으로 전체 parity를 완료 처리하지 않는다.
