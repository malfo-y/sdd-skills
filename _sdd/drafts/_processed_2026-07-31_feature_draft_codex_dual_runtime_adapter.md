# Feature Draft: Codex dual-runtime multi-agent adapter

> 규모 판정: 적격 — 동일한 lifecycle 계약을 Codex 12개 표면에 전파하는 census형 문서 변경이며, 세 task와 전수 grep으로 대응을 눈검산할 수 있다.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary

Codex agent dispatch는 활성 tool schema를 먼저 판별하고 mailbox contract와 target/close legacy contract 중 정확히 하나를 사용한다. Desktop과 현재 CLI 0.146.0이 노출한 mailbox schema는 `task_name`·제한된 `fork_turns`·target 없는 `wait_agent`를 사용하고, legacy target schema가 노출된 환경만 target형 `wait_agent`와 `close_agent` lifecycle을 사용한다. 실행 surface 이름이 아니라 schema로 선택하며, 존재하지 않는 lifecycle tool을 검색하거나 두 schema의 필드를 한 호출에 섞지 않는다.

## Scope

- **In**: `.codex`의 mandatory review/spec-sync orchestrator, conditional helper dispatch, autopilot lifecycle 설명, agent README와 PR review example의 dual-runtime 정합
- **Out**: model/effort allowlist 갱신, installer prune, agent census/ownership 문서, investigate diagnose-only 정책, Claude skill/agent 본문
<!-- spec-update-todo-input-end -->

## Decisions and Assumptions

- **Self-contained execution**: fresh bundle installer는 agent README를 설치하지 않으므로, executable SKILL은 자기 runtime adapter를 직접 보유한다. `.codex/agents/README.md`는 유지보수자용 요약이며 runtime dependency가 아니다. 반복 비용은 Task 3 census로 통제한다.
- **Schema selection**: `task_name`/`fork_turns`가 필요하거나 `wait_agent`가 `targets`를 받지 않으면 mailbox contract를 선택한다. target형 `wait_agent`와 `close_agent`가 함께 노출되면 target/close contract를 선택한다. 두 조건이 모두 성립하거나 어느 쪽도 완결되지 않으면 dispatch하지 않고 schema blocker를 보고한다. Desktop/CLI라는 surface 이름은 선택 근거가 아니다.
- **Confidence / confirmation**: 현재 Desktop tool schema와 CLI 0.146.0 실측에 근거한 high-confidence 결정이며, 기존 CLI 지원을 보존하는 범위라 추가 사용자 확인은 필요하지 않다.

# Part 2: Tasks

### Task 1: Make mandatory orchestrators schema-adaptive

`plan-review`, `implementation-review`, `pr-review`, `spec-sync`의 dispatch와 수거 절차가 Desktop/CLI에서 각각 유효한 호출만 만들게 한다.

**Contracts**: 활성 `spawn_agent`/`wait_agent` schema가 adapter 선택의 단일 근거다. mailbox 경로는 invocation별 `run_id`를 포함해 parent tree 재실행까지 고유한 `task_name`, `fork_turns: "none"`, `message`를 사용하고 mailbox final을 remaining set으로 수거하며 완료 agent를 별도 close하지 않는다. target/close 경로는 기존 `agent_type`/`message`, target형 wait, 노출된 `close_agent`를 사용한다. model/effort field는 선택된 schema가 허용할 때만 추가하며, 요청된 override field가 없으면 blocker로 종료한다.

**Acceptance Criteria**:
- [ ] AC1: 네 orchestrator 모두 mailbox와 target/close 선택 조건, spawn, wait, cleanup 차이를 명시하고 두 schema를 섞지 않는다.
- [ ] AC2: mailbox 예시는 invocation별 `run_id`가 들어간 parent-tree 고유 `task_name` + `fork_turns: "none"`를 포함하고 `wait_agent({timeout_ms: ...})`만 사용한다.
- [ ] AC3: target/close 예시는 target형 wait를 유지하고, `close_agent`는 active tool로 노출된 경로에서만 사용한다.
- [ ] AC4: 네 orchestrator의 기존 shard/lens 병렬성, framed payload, timeout 미완료 규칙, 반환 병합 계약은 보존된다.

**Target Files**:
- [M] `.codex/skills/plan-review/SKILL.md` -- 2-lens dual-runtime dispatch
- [M] `.codex/skills/implementation-review/SKILL.md` -- N+2 dual-runtime dispatch
- [M] `.codex/skills/pr-review/SKILL.md` -- correctness/simplicity dual-runtime dispatch
- [M] `.codex/skills/spec-sync/SKILL.md` -- body/record writer dual-runtime dispatch

### Task 2: Align optional helpers and lifecycle documentation

조건부 helper 경로와 상위 lifecycle 설명이 같은 adapter 선택 규칙을 사용하게 한다.

**Contracts**: helper가 실제로 spawn될 때만 schema를 선택한다. mailbox contract는 final 수거 후 종료된 agent를 close하지 않고, target/close contract는 final 결과 기록 후 노출된 close를 수행한다. 없는 tool을 `tool_search`로 복구하려 하지 않는다.

**Acceptance Criteria**:
- [ ] AC1: 다섯 optional-helper skill이 mailbox/target-close별 최소 유효 lifecycle을 설명한다.
- [ ] AC2: `sdd-autopilot`은 하위 skill이 선택한 runtime lifecycle을 재정의하지 않고 final 수거 완료만 검증한다.
- [ ] AC3: agent README와 PR review example이 dual-runtime contract를 정확히 반영한다.
- [ ] AC4: optional helper를 쓰지 않는 기본 inline path와 각 skill의 기존 사용자-facing behavior는 바뀌지 않는다.

**Target Files**:
- [M] `.codex/skills/investigate/SKILL.md` -- conditional explorer lifecycle
- [M] `.codex/skills/write-phased/SKILL.md` -- conditional worker lifecycle
- [M] `.codex/skills/guide-create/SKILL.md` -- optional helper error handling
- [M] `.codex/skills/spec-snapshot/SKILL.md` -- optional helper finalization
- [M] `.codex/skills/spec-summary/SKILL.md` -- large-document helper fallback
- [M] `.codex/skills/sdd-autopilot/SKILL.md` -- lifecycle invariant relay
- [M] `.codex/skills/pr-review/examples/sample-review.md` -- dual-runtime example
- [M] `.codex/agents/README.md` -- current Codex invocation contract

### Task 3: Prove the stale contract is gone without erasing CLI support

변형 표기 전수 census와 runtime smoke로 Desktop 회귀 제거와 CLI 보존을 함께 검증한다.

**Acceptance Criteria**:
- [ ] AC1: live `.codex` surface에서 무조건형 `close_agent`, `send_input`, `multi_tool_use.parallel`, mailbox 문맥의 target형 wait 잔존이 0이다.
- [ ] AC2: 모든 명시적 mailbox `spawn_agent` 예시가 `task_name`과 제한된 `fork_turns`를 포함한다.
- [ ] AC3: Desktop에서 representative `plan-review`가 두 reviewer를 mailbox contract로 spawn·수거·병합하고 close 없이 완료한다.
- [ ] AC4: `codex-cli 0.146.0`에서 representative `plan-review`가 현재 mailbox schema를 선택해 두 reviewer를 spawn·수거하고 unsupported-model startup rejection 없이 완료한다.
- [ ] AC5: `git diff --check`가 clean이고, `.codex` Markdown local link broken 0·SKILL 직접 상대 참조 missing 0이며, agent TOML 5/5 parse + filename/name uniqueness가 통과한다.

**Target Files**:
- 없음 (read-only 검증)
