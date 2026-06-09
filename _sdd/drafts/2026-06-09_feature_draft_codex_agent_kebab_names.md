# Feature Draft: Codex custom agent names to kebab-case

<!-- spec-update-todo-input-start -->
# Part 1: Temporary Spec Draft

## Change Summary

Codex custom agent의 TOML `name` 필드와 모든 Codex `spawn_agent(agent_type=...)` 호출 참조를 underscore style에서 kebab-case로 바꾼다. 현재 `.codex/agents/*.toml` 파일명은 이미 kebab-case인데 `name`과 호출값은 `feature_draft_agent` 같은 underscore style이라, 파일명과 호출 ID가 섞여 invocation confusion을 만든다.

검증된 runtime 사실:

- 현재 열린 Codex 세션의 tool schema는 기존 underscore role을 노출한다: `feature_draft_agent`, `implementation_agent`, `implementation_plan_agent`, `implementation_review_agent`, `plan_review_agent`, `ralph_loop_init_agent`, `spec_review_agent`, `spec_update_done_agent`, `spec_update_todo_agent`.
- 같은 현재 세션에서 `spawn_agent(agent_type="feature-draft-agent")`는 실패했다. 현재 세션의 registry는 agent 파일 변경을 hot-reload하지 않는다.
- 임시 `kebab-pilot-agent.toml` 파일을 추가한 뒤 같은 세션에서는 실패했지만, fresh `codex exec` 프로세스에서는 `agent_type="kebab-pilot-agent"`가 성공했다.
- 따라서 Codex는 kebab-case custom agent `name`을 지원하지만, validation은 새 세션 또는 fresh `codex exec` 프로세스에서 해야 한다.

대상 mapping:

| Current Codex `name` / `agent_type` | New Codex `name` / `agent_type` |
|-------------------------------------|---------------------------------|
| `feature_draft_agent` | `feature-draft-agent` |
| `implementation_plan_agent` | `implementation-plan-agent` |
| `plan_review_agent` | `plan-review-agent` |
| `implementation_agent` | `implementation-agent` |
| `implementation_review_agent` | `implementation-review-agent` |
| `spec_update_todo_agent` | `spec-update-todo-agent` |
| `spec_update_done_agent` | `spec-update-done-agent` |
| `spec_review_agent` | `spec-review-agent` |
| `ralph_loop_init_agent` | `ralph-loop-init-agent` |

Built-in roles stay unchanged: `explorer`, `worker`, `default`.

## Scope Delta

**In-scope**

- Codex custom agent TOML `name` fields and self descriptions in `.codex/agents/*.toml`.
- Codex wrapper/orchestrator skill text that calls custom agents through `spawn_agent(agent_type=...)`.
- Codex `sdd-autopilot` generated-orchestrator contract, sample, profile, and reasoning references that define or emit Codex custom agent IDs.
- Current global spec/docs surfaces that state the Codex custom agent naming contract.
- One Claude-side cross-platform note that documents a Codex `spawn_agent(agent_type="implementation_agent")` call.

**Out-of-scope**

- Claude agent names and Claude `subagent_type` values. Claude is already kebab-case and is parity reference only.
- Skill names and skill folder names such as `.codex/skills/feature-draft/`.
- Artifact/path slug conventions such as `_sdd/drafts/<date>_feature_draft_<slug>.md`, `_sdd/implementation/<date>_implementation_plan_<slug>.md`, `_sdd/implementation/<date>_plan_review_<slug>.md`.
- Historical artifacts under `_sdd/drafts/`, `_sdd/implementation/`, `_sdd/discussion/`, and `_sdd/spec/prev/`.
- Removed-agent historical note in `.codex/skills/investigate/SKILL.md` that says old `investigate_agent` was removed. No current `.codex/agents/investigate-agent.toml` exists, and the live note explains why this skill owns investigation inline instead of spawning a custom leaf.
- Runtime hot-reload support. Existing open sessions may continue to expose old names until restart/reload.

**Guardrail delta**

- No blind global rename. Only replace the exact old Codex custom agent ID tokens listed in the mapping table.
- Preserve artifact slugs that contain words like `feature_draft` or `implementation_plan` when they are file naming conventions, not agent IDs.
- Do not add alias normalization from underscore to kebab. Old names should fail after reload, so stale references are caught.

## Contract/Invariant Delta

| ID | Type | Change | Why |
|----|------|--------|-----|
| C1 | Modify | Codex custom agent TOML `name` values use kebab-case and match existing kebab-case filenames. | Removes mixed filename/call ID convention that causes invocation confusion. |
| C2 | Modify | All Codex custom-agent `spawn_agent(agent_type=...)` references use kebab-case IDs from the mapping table. | Runtime calls must match TOML `name` values. |
| C3 | Keep | Built-in Codex roles `explorer`, `worker`, and `default` are unchanged. | Built-ins are not custom agent TOML names and are outside this rename. |
| I1 | Add | No live Codex runtime/config/skill/autopilot surface may contain the nine mapped old underscore custom agent IDs after implementation. | Stale current-agent IDs will fail after registry reload and recreate confusion. |
| I2 | Add | Artifact naming slugs such as `_feature_draft_`, `_implementation_plan_`, and `_plan_review_` remain unchanged. | These are file naming contracts, not agent invocation IDs. |
| I3 | Add | Validation of kebab-case custom agent resolution must run in a fresh Codex process or new session. | Current sessions do not hot-reload custom agent registry changes. |
| I4 | Keep | The live `.codex/skills/investigate/SKILL.md` note may keep `investigate_agent` only as a removed-agent historical note, not as a current custom agent ID or spawn target. | No current investigate custom agent TOML exists, and the note documents intentional inline ownership. |

## Touchpoints

All touchpoints below were reverified against the current code on 2026-06-09 using `rg` and direct file reads. The Strategic Code Map in `_sdd/spec/components.md` was used only as a starting hint; Target Files below come from current code search.

### 1. Required live runtime/config docs and agent/skill files to modify

**Codex agent TOML files**

- `.codex/agents/feature-draft-agent.toml`: line 1 `name`, line 2 self description, line 286 `plan_review_agent` review report reference, line 335 Source Pointer.
- `.codex/agents/implementation-agent.toml`: line 1 `name`, line 2 self description.
- `.codex/agents/implementation-plan-agent.toml`: line 1 `name`, line 2 self description, line 311 `plan_review_agent` review report reference, line 362 Source Pointer.
- `.codex/agents/implementation-review-agent.toml`: line 1 `name`, line 2 self description.
- `.codex/agents/plan-review-agent.toml`: line 1 `name`, line 2 self description.
- `.codex/agents/ralph-loop-init-agent.toml`: line 1 `name`, line 2 self description.
- `.codex/agents/spec-review-agent.toml`: line 1 `name`, line 2 self description.
- `.codex/agents/spec-update-done-agent.toml`: line 1 `name`, line 2 self description.
- `.codex/agents/spec-update-todo-agent.toml`: line 1 `name`, line 2 self description.

**Codex agent README**

- `.codex/agents/README.md`: Naming section currently says filename kebab + `name` snake; Agent Set currently lists underscore-style stems; Inline Writing lines 36-40 also list underscore-style helper stems (`feature_draft`, `implementation_plan`, `plan_review`, `implementation_review`, `spec_review`) that must be updated or removed consistently with the custom agent ID contract.

**Codex skill wrappers/orchestrators**

- `.codex/skills/feature-draft/SKILL.md`: lines 9, 24, 38-40, 51-54.
- `.codex/skills/implementation-plan/SKILL.md`: lines 9, 21, 35-37, 46-49.
- `.codex/skills/implementation/SKILL.md`: lines 9, 17, 26, 131, 143, 182, 196-198, 249.
- `.codex/skills/implementation-review/SKILL.md`: lines 9, 19.
- `.codex/skills/plan-review/SKILL.md`: lines 9, 14.
- `.codex/skills/ralph-loop-init/SKILL.md`: lines 9, 16.
- `.codex/skills/spec-review/SKILL.md`: lines 9, 14.
- `.codex/skills/spec-update-done/SKILL.md`: lines 9, 14.
- `.codex/skills/spec-update-todo/SKILL.md`: lines 9, 14.
- `.codex/skills/investigate/SKILL.md`: line 83 contains a live removed-agent historical note, `구 investigate_agent는 제거됨`. Keep it as an allowed historical note/non-goal unless implementation finds a current `.codex/agents/investigate-agent.toml`.

**Cross-platform note with Codex invocation**

- `.claude/skills/implementation/SKILL.md`: line 144 documents Codex `spawn_agent(agent_type="implementation_agent")`; update this documentation only. Do not change Claude agent names.

### 2. Required `sdd-autopilot` contract/sample/profile files

- `.codex/skills/sdd-autopilot/SKILL.md`: lines 179, 183-185, 202, 206, 209, 274, 281, 285, 287, 295, 297, 301.
- `.codex/skills/sdd-autopilot/references/orchestrator-contract.md`: lines 68-81 allowed-list and legacy-alias policy, lines 103-118 implementation/planning producer rules, lines 152 and 158-163 review-fix mapping, lines 229-244 step labels for spec update agents.
- `.codex/skills/sdd-autopilot/references/execution-profile-policy.md`: lines 12-20 profile table.
- `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md`: all Codex `agent_type`, profile mapping, review/fix/re-review mapping, execution sequence, and retry references found at current lines 5, 30-45, 50, 61, 71, 74, 91, 99-114, 118, 176-194, 199, 209, 212, 220-225, 234, 237, 246, 249, 260, 263, 277, 297-324, 354.
- `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md`: line 137 review-fix loop mapping.

### 3. Required global spec/docs sync files

- `_sdd/spec/main.md`: lines 64-65, 100, 112 currently state underscore Codex custom agent names as current contract. Line 65 is the generic current-contract statement that says Codex uses `_agent` suffix names as canonical; validation must catch it even though it is not one of the nine exact old IDs.
- `_sdd/spec/components.md`: line 13 currently says Codex generated orchestrator treats `implementation_agent` as the dispatch controller.
- `_sdd/spec/DECISION_LOG.md`: add a new 2026-06-09 entry that supersedes the prior underscore Codex-name decision. Do not rewrite older historical entries except if a top current summary is explicitly maintained.
- `_sdd/spec/logs/changelog.md`: add a new 2026-06-09 changelog entry. Do not rewrite older historical entries.
- `.claude/skills/implementation/SKILL.md`: line 144 is cross-platform documentation of Codex invocation and should be updated with the docs sync, even though it is under `.claude/`.

Verified no current old underscore agent-ID matches in `docs/AUTOPILOT_GUIDE.md`, `docs/en/AUTOPILOT_GUIDE.md`, `README.md`, `docs/SDD_WORKFLOW.md`, or `docs/en/SDD_WORKFLOW.md` as of 2026-06-09. These are not target files unless implementation adds a new explanatory note.

### 4. Non-goals / historical files not to edit

- `_sdd/drafts/**`, including `_sdd/drafts/2026-06-02_feature_draft_agent_identifier_rename.md`.
- `_sdd/implementation/**`, including prior reports that documented the older underscore Codex convention.
- `_sdd/discussion/**`.
- `_sdd/spec/prev/**`.
- Historical lines inside `_sdd/spec/DECISION_LOG.md` and `_sdd/spec/logs/changelog.md` that describe completed past work; add new entries instead of rewriting history.
- `.claude/agents/**` and `.claude/skills/**` except `.claude/skills/implementation/SKILL.md` line 144.
- `.codex/skills/investigate/SKILL.md` line 83 old `investigate_agent` mention remains allowed only as a removed-agent historical note; do not add `.codex/agents/investigate-agent.toml`.
- Artifact/path slugs: `_feature_draft_`, `_implementation_plan_`, `_implementation_review_`, `_plan_review_`, `_spec_update_todo_`, `_spec_update_done_`, `_spec_review_`, `_ralph_loop_init_`.

## Implementation Plan

1. Update the nine `.codex/agents/*.toml` `name` fields to kebab-case and align their self descriptions and internal Codex review/Source Pointer references.
2. Update `.codex/agents/README.md` so it states filename and `name` are both kebab-case, and update both Agent Set and Inline Writing inventories to avoid underscore custom-agent stems.
3. Update Codex skill wrappers/orchestrators to call `spawn_agent(agent_type="<kebab-agent>")`.
4. Update Codex `sdd-autopilot` contract, profile policy, sample orchestrator, and reasoning references so generated orchestrators emit kebab-case IDs and reject underscore custom agent IDs as stale.
5. Update current global spec/docs sync surfaces and the one Claude-side cross-platform Codex invocation note.
6. Run static validation in the current worktree, including narrow checks for generic `_agent` current-contract text, README underscore stem inventories, and the allowed removed `investigate_agent` note. Then run resolution-only smoke validation in a fresh Codex process/new session because current sessions do not hot-reload the custom agent registry.

## Validation Plan

| ID | Targets | Verification Method | Evidence / Notes |
|----|---------|---------------------|------------------|
| V1 | C1, I1 | grep/static | `rg -n '^name = ".*_agent"' .codex/agents` returns no matches; each `.codex/agents/*-agent.toml` has the matching kebab `name`. |
| V2 | C2, I1 | grep/static | `rg -n 'feature_draft_agent|implementation_plan_agent|plan_review_agent|implementation_agent|implementation_review_agent|spec_update_todo_agent|spec_update_done_agent|spec_review_agent|ralph_loop_init_agent' .codex .claude/skills/implementation/SKILL.md _sdd/spec/main.md _sdd/spec/components.md docs README.md` returns no live matches, excluding historical `_sdd` artifacts and old log entries. |
| V3 | C3 | grep/static | `rg -n 'agent_type="(explorer|worker|default)"|agent_type:.*(explorer|worker|default)' .codex/skills .codex/agents` still shows built-ins only where intended; no built-in rename attempted. |
| V4 | I2 | grep/static | `rg -n '_feature_draft_|_implementation_plan_|_implementation_review_|_plan_review_|_spec_update_todo_|_spec_update_done_|_spec_review_|_ralph_loop_init_' _sdd .codex` confirms artifact slug occurrences remain valid and were not mass-renamed. |
| V5 | I3, C1, C2 | smoke/fresh process | Fresh `codex exec` or new thread can spawn at least `feature-draft-agent` and one non-pilot agent such as `implementation-agent`; same current-session schema may still show old names and is not valid evidence of failure. |
| V6 | C2, I1 | manual review | `sdd-autopilot` sample/contract/profile files emit kebab `agent_type` values and describe underscore names as stale unsupported aliases, not canonical names. |
| V7 | I1, I4 | grep/static + manual review | Narrow current-contract check for both `_agent suffix` and backticked `` `_agent` suffix `` text, plus underscore helper stems in `_sdd/spec/main.md` and `.codex/agents/README.md`, returns no stale current-contract matches. `investigate_agent` is allowed only in `.codex/skills/investigate/SKILL.md` as the removed-agent historical note and is excluded from the nine-agent rename mapping. |

Suggested validation commands:

```bash
rg -n '^name = ".*_agent"' .codex/agents
rg -n 'feature_draft_agent|implementation_plan_agent|plan_review_agent|implementation_agent|implementation_review_agent|spec_update_todo_agent|spec_update_done_agent|spec_review_agent|ralph_loop_init_agent' .codex .claude/skills/implementation/SKILL.md _sdd/spec/main.md _sdd/spec/components.md docs README.md
rg -n '`?_agent`? suffix|feature_draft|implementation_plan|plan_review|implementation_review|spec_review|spec_update_todo|spec_update_done|ralph_loop_init' .codex/agents/README.md _sdd/spec/main.md
rg -n 'investigate_agent' .codex/skills/investigate/SKILL.md
rg -n 'agent_type="(feature-draft-agent|implementation-plan-agent|plan-review-agent|implementation-agent|implementation-review-agent|spec-update-todo-agent|spec-update-done-agent|spec-review-agent|ralph-loop-init-agent)"' .codex/skills .codex/agents
codex exec --cd /Users/hyunjoonlee/github/sdd_skills 'Use spawn_agent(agent_type="feature-draft-agent") only to verify the agent type resolves. Do not ask the spawned agent to read files, write files, or run commands. Report resolution success/failure only.'
codex exec --cd /Users/hyunjoonlee/github/sdd_skills 'Use spawn_agent(agent_type="implementation-agent") only to verify the agent type resolves. Do not ask the spawned agent to read files, write files, or run commands. Report resolution success/failure only.'
```

## Risks / Open Questions

### Q1. Current open Codex sessions may still expose old underscore names after the files are changed.
- **Decision taken**: Treat current-session failures for kebab names as expected cache behavior. Runtime validation must use a new thread or fresh `codex exec` process.
- **Alternatives considered**: Validate in the same session only; rejected because the pilot already showed registry is not hot-reloaded. Add hot-reload support; rejected as outside scope.
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q2. Whether to update historical `_sdd` artifacts and old decision log/changelog lines containing underscore names.
- **Decision taken**: Do not edit historical artifacts or old historical log lines. Add new current spec/changelog/decision entries and update current canonical spec statements.
- **Alternatives considered**: Rewrite all history to remove old names; rejected because it destroys evidence of prior decisions. Leave current spec unchanged; rejected because current canonical contract would conflict with implementation.
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q3. Whether Claude files should be modified for parity.
- **Decision taken**: Do not modify Claude agent names. Update only `.claude/skills/implementation/SKILL.md` line 144 because it explicitly documents a Codex `spawn_agent(agent_type="implementation_agent")` call.
- **Alternatives considered**: Skip `.claude/**` entirely; rejected because the Codex invocation note would remain stale. Update Claude agent names; rejected because they are already kebab-case and outside scope.
- **Confidence**: HIGH
- **User confirmation needed**: No

### Q4. Whether to preserve underscore names as aliases for backward compatibility.
- **Decision taken**: Do not preserve aliases. `sdd-autopilot` contract should reject/regenerate stale underscore custom agent IDs.
- **Alternatives considered**: Normalize underscore to kebab at generation or execution time; rejected because it keeps two conventions alive and hides stale references. Document both as accepted; rejected for the same reason.
- **Confidence**: MEDIUM
- **User confirmation needed**: No

### Q5. Whether to remove the live `.codex/skills/investigate/SKILL.md` `investigate_agent` note.
- **Decision taken**: Keep it as an allowed removed-agent historical note/non-goal and exclude it from the nine-agent rename mapping. Validation should confirm it is not a current TOML `name` or `spawn_agent(agent_type=...)` target.
- **Alternatives considered**: Rewrite the note to avoid the underscore ID; rejected because the current wording explains the removal directly. Add `investigate-agent` as a target; rejected because no current `.codex/agents/investigate-agent.toml` exists.
- **Confidence**: HIGH
- **User confirmation needed**: No
<!-- spec-update-todo-input-end -->

# Part 2: Implementation Plan

## Overview

This implementation renames Codex custom agent invocation IDs from underscore style to kebab-case. "Codex custom agent ID" means the `.codex/agents/*.toml` `name` field and the value passed to Codex `spawn_agent(agent_type=...)`. It does not mean skill names, folder names, or `_sdd` artifact filename slugs.

The current code already uses kebab-case filenames such as `.codex/agents/feature-draft-agent.toml`. The implementation should align `name = "feature-draft-agent"` and all `spawn_agent(agent_type="feature-draft-agent")` references with those filenames.

Execution should be sequential by phase. The same old IDs appear in shared `sdd-autopilot` files and in multiple skill wrappers; parallel edits would create avoidable file conflicts. Minimum-code mandate: only exact old custom agent ID tokens are renamed, plus directly attached explanatory text that states the naming contract.

## Scope

In scope:

- `.codex/agents/*.toml` custom agent `name` and self-reference text.
- `.codex/skills/**/SKILL.md` Codex custom agent dispatch references.
- `.codex/skills/sdd-autopilot/**` Codex generated-orchestrator contracts, examples, profile tables, and reasoning references.
- Current canonical spec/docs surfaces that state current Codex custom agent names.
- `.claude/skills/implementation/SKILL.md` line 144 because it documents Codex invocation syntax.

Out of scope:

- Claude `subagent_type` values and `.claude/agents/**`.
- Built-in Codex roles `explorer`, `worker`, `default`.
- `_sdd` historical artifacts and artifact filename slug conventions.
- Compatibility aliases or runtime hot-reload behavior.
- `.codex/skills/investigate/SKILL.md` line 83 removed-agent note `구 investigate_agent는 제거됨`; this remains allowed because no current `.codex/agents/investigate-agent.toml` exists and the note explains inline ownership.

## Components

| Component | Definition | Change |
|-----------|------------|--------|
| Codex agent TOML | `.codex/agents/*-agent.toml` files that define custom agent `name` values. | Rename `name` values from underscore to kebab and update adjacent self-description text. |
| Codex wrapper/orchestrator skills | `.codex/skills/*/SKILL.md` files that instruct the main loop to call `spawn_agent`. | Replace old custom agent IDs in `spawn_agent(agent_type=...)` and role prose. |
| Codex autopilot contract | `.codex/skills/sdd-autopilot/**` files that generate or validate orchestrator agent calls. | Emit/allow kebab IDs and classify underscore IDs as stale unsupported aliases. |
| Global spec/docs sync | `_sdd/spec/main.md`, `_sdd/spec/components.md`, `_sdd/spec/DECISION_LOG.md`, `_sdd/spec/logs/changelog.md`, plus one Claude cross-platform note. | Align exact current-name statements and the generic `_agent` canonical statement with the new kebab contract, then append history entries. |
| Codex agent README | `.codex/agents/README.md` custom agent naming, Agent Set, and Inline Writing inventories. | Replace underscore-style custom agent stems with kebab-case agent IDs where those lists describe current custom agents. |
| Validation | Static grep plus fresh-process smoke. | Prove old live IDs and current-contract stem remnants are gone, preserve the allowed removed `investigate_agent` note, and confirm fresh Codex process resolves kebab IDs. |

## Contract/Invariant Delta Coverage

| Delta | Covered By | Validation |
|-------|------------|------------|
| C1: TOML `name` values become kebab-case | T1 | V1, V5 |
| C2: Codex `spawn_agent(agent_type=...)` references become kebab-case | T2, T3, T4 | V2, V5, V6 |
| C3: built-ins unchanged | T3, T6 | V3 |
| I1: no mapped old live underscore custom agent IDs | T1-T6 | V1, V2, V6, V7 |
| I2: artifact slugs unchanged | T4, T5, T6 | V4 |
| I3: fresh process required for runtime validation | T6 | V5 |
| I4: removed `investigate_agent` live note is allowed only as history | T2, T6 | V7 |

## Implementation Phases

| Phase | Tasks | Dependency | Parallelism |
|-------|-------|------------|-------------|
| Phase 1 | T1 | None | Single task; all agent TOMLs are touched in one controlled pass. |
| Phase 2 | T2 | T1 | Single task; wrapper references depend on new TOML names. |
| Phase 3 | T3 | T1, T2 | Single task; shared autopilot files require sequential editing. |
| Phase 4 | T4 -> T5 | T3 | Sequential; spec/docs should reflect final runtime contract before the README summarizes it. |
| Phase 5 | T6 | T1-T5 | Verification only. |

## Task Details

### Task T1: Rename Codex agent TOML `name` fields
**Component**: Codex agent TOML
**Priority**: P0
**Type**: Refactor

**Description**: Update the nine current `.codex/agents/*-agent.toml` files so each `name` field is the kebab-case ID matching its filename. Update only adjacent self-description and internal review/Source Pointer text that names Codex custom agent IDs.

**Acceptance Criteria**:
- [ ] Each `.codex/agents/*-agent.toml` has `name = "<matching-kebab-file-stem>"`.
- [ ] Line 2 descriptions use `spawn_agent(agent_type="<kebab-agent>")`.
- [ ] `feature-draft-agent.toml` and `implementation-plan-agent.toml` internal `plan_review_agent` references become `plan-review-agent`.
- [ ] No TOML `name` value ends in `_agent`.

**Target Files**:
- [M] `.codex/agents/feature-draft-agent.toml` -- `feature_draft_agent` to `feature-draft-agent`; internal `plan_review_agent` references to `plan-review-agent`.
- [M] `.codex/agents/implementation-agent.toml` -- `implementation_agent` to `implementation-agent`.
- [M] `.codex/agents/implementation-plan-agent.toml` -- `implementation_plan_agent` to `implementation-plan-agent`; internal `plan_review_agent` references to `plan-review-agent`.
- [M] `.codex/agents/implementation-review-agent.toml` -- `implementation_review_agent` to `implementation-review-agent`.
- [M] `.codex/agents/plan-review-agent.toml` -- `plan_review_agent` to `plan-review-agent`.
- [M] `.codex/agents/ralph-loop-init-agent.toml` -- `ralph_loop_init_agent` to `ralph-loop-init-agent`.
- [M] `.codex/agents/spec-review-agent.toml` -- `spec_review_agent` to `spec-review-agent`.
- [M] `.codex/agents/spec-update-done-agent.toml` -- `spec_update_done_agent` to `spec-update-done-agent`.
- [M] `.codex/agents/spec-update-todo-agent.toml` -- `spec_update_todo_agent` to `spec-update-todo-agent`.

**Technical Notes**: Covers C1 and I1, validated by V1 and V2. Do not rename files; filenames are already kebab-case.
**Dependencies**: None

### Task T2: Update Codex skill wrapper dispatch references
**Component**: Codex wrapper/orchestrator skills
**Priority**: P0
**Type**: Refactor

**Description**: Replace old underscore custom agent IDs in Codex skill dispatch instructions with kebab-case IDs. Keep skill names and folder names unchanged.

**Acceptance Criteria**:
- [ ] Every `spawn_agent(agent_type="...")` custom agent reference in Codex skill wrappers uses the kebab-case ID from the mapping table.
- [ ] Role Pointer and Source text names the kebab custom agent ID when it refers to Codex `agent_type`.
- [ ] Built-in `explorer`, `worker`, and `default` references remain unchanged.
- [ ] `.codex/skills/investigate/SKILL.md` line 83 is not edited into a new custom agent target; its old `investigate_agent` text is treated only as the allowed removed-agent historical note covered by I4/V7.

**Target Files**:
- [M] `.codex/skills/feature-draft/SKILL.md` -- producer and reviewer `agent_type` names.
- [M] `.codex/skills/implementation-plan/SKILL.md` -- producer and reviewer `agent_type` names.
- [M] `.codex/skills/implementation/SKILL.md` -- implementation leaf and implementation review/fix/re-review `agent_type` names.
- [M] `.codex/skills/implementation-review/SKILL.md` -- reviewer `agent_type` name.
- [M] `.codex/skills/plan-review/SKILL.md` -- reviewer `agent_type` name.
- [M] `.codex/skills/ralph-loop-init/SKILL.md` -- ralph init `agent_type` name.
- [M] `.codex/skills/spec-review/SKILL.md` -- spec reviewer `agent_type` name.
- [M] `.codex/skills/spec-update-done/SKILL.md` -- done sync `agent_type` name.
- [M] `.codex/skills/spec-update-todo/SKILL.md` -- todo sync `agent_type` name.

**Technical Notes**: Covers C2, I1, and I4, validated by V2 and V7. Do not edit `.codex/skills/*/skill.json` unless a direct old custom agent ID is found there; current search found none. Do not add `.codex/agents/investigate-agent.toml` because the only `investigate_agent` surface is a removed-agent historical note, not a current invocation ID.
**Dependencies**: T1

### Task T3: Update Codex sdd-autopilot contract and examples
**Component**: Codex autopilot contract
**Priority**: P0
**Type**: Refactor

**Description**: Update `sdd-autopilot` Codex contract surfaces so generated orchestrators allow and emit kebab-case custom agent IDs. Change old underscore custom agent names from canonical to stale unsupported aliases. Keep built-in roles unchanged.

**Acceptance Criteria**:
- [ ] Allowed custom agent list uses the nine kebab-case IDs.
- [ ] Legacy/alias policy says underscore custom agent IDs are unsupported stale aliases and must be reject/regenerate targets.
- [ ] Implementation dispatch controller text uses `implementation-agent`.
- [ ] Planning producer gate text uses `feature-draft-agent`, `implementation-plan-agent`, and `plan-review-agent`.
- [ ] Review-fix mappings use `implementation-review-agent`, `implementation-agent`, `implementation-review-agent`.
- [ ] Profile tables and sample orchestrator Codex `agent_type` values use kebab-case.

**Target Files**:
- [M] `.codex/skills/sdd-autopilot/SKILL.md` -- runtime generation/verification/execution rules.
- [M] `.codex/skills/sdd-autopilot/references/orchestrator-contract.md` -- allowed IDs, legacy policy, producer/review/fix mappings, spec update step labels.
- [M] `.codex/skills/sdd-autopilot/references/execution-profile-policy.md` -- profile key table.
- [M] `.codex/skills/sdd-autopilot/examples/sample-orchestrator.md` -- sample `agent_type`, profile, mapping, sequence, retry references.
- [M] `.codex/skills/sdd-autopilot/references/sdd-reasoning-reference.md` -- fixed review/fix/re-review role mapping.

**Technical Notes**: Covers C2, C3, I1, and I3, validated by V2, V3, V5, V6. This task is sequential because all generated-orchestrator semantics converge in shared files.
**Dependencies**: T1, T2

### Task T4: Update current global spec and cross-platform docs sync
**Component**: Global spec/docs sync
**Priority**: P1
**Type**: Refactor

**Description**: Align current canonical spec statements with the new Codex kebab custom agent naming contract. Add new append-only history entries for the decision and changelog. Update the single Claude-side cross-platform Codex invocation note.

**Acceptance Criteria**:
- [ ] `_sdd/spec/main.md` no longer states underscore Codex custom agent IDs as current contract, including line 65's generic statement that Codex uses `_agent` suffix names as canonical.
- [ ] `_sdd/spec/components.md` describes Codex `implementation-agent` as the generated-orchestrator dispatch controller.
- [ ] `_sdd/spec/DECISION_LOG.md` has a new 2026-06-09 decision entry that records the kebab-case Codex custom agent ID decision and fresh-process validation requirement.
- [ ] `_sdd/spec/logs/changelog.md` has a new 2026-06-09 changelog entry.
- [ ] `.claude/skills/implementation/SKILL.md` line 144 Codex invocation example uses `implementation-agent`.

**Target Files**:
- [M] `_sdd/spec/main.md` -- current guardrails/decisions for Codex custom agent names.
- [M] `_sdd/spec/components.md` -- `sdd-autopilot` note for Codex implementation dispatch controller.
- [M] `_sdd/spec/DECISION_LOG.md` -- append-only decision entry.
- [M] `_sdd/spec/logs/changelog.md` -- append-only changelog entry.
- [M] `.claude/skills/implementation/SKILL.md` -- cross-platform Codex invocation note only.

**Technical Notes**: Covers I1 and I2, validated by V2, V4, and V7. Historical old log lines can remain as history; the new entry must make the current contract clear.
**Dependencies**: T3

### Task T5: Update Codex agent README naming contract
**Component**: Codex agent README
**Priority**: P1
**Type**: Refactor

**Description**: Update `.codex/agents/README.md` so it no longer says `name` uses snake_case. List the custom agent set as the actual kebab-case `agent_type` values. Keep built-in role guidance unchanged.

**Acceptance Criteria**:
- [ ] Naming section states both filename and TOML `name` use kebab-case for custom agents.
- [ ] Agent Set lists `feature-draft-agent`, `implementation-plan-agent`, `implementation-agent`, `plan-review-agent`, `implementation-review-agent`, `spec-update-todo-agent`, `spec-update-done-agent`, `spec-review-agent`, `ralph-loop-init-agent`.
- [ ] Inline Writing lines 36-40 no longer list underscore helper stems such as `feature_draft`, `implementation_plan`, `plan_review`, `implementation_review`, or `spec_review` as current custom-agent inventory.
- [ ] Built-in role examples `explorer`, `worker`, `default` are unchanged.

**Target Files**:
- [M] `.codex/agents/README.md` -- custom agent naming and inventory documentation.

**Technical Notes**: Covers C1, C3, and I1, validated by V2, V3, and V7.
**Dependencies**: T4

### Task T6: Run static and fresh-process validation
**Component**: Validation
**Priority**: P0
**Type**: Test

**Description**: Run static grep checks in the current worktree and runtime smoke checks in fresh Codex processes or a new session. Do not treat current-session tool schema as failure evidence because it may still expose the pre-change registry.

**Acceptance Criteria**:
- [ ] V1 static check finds no `.codex/agents` TOML `name` ending in `_agent`.
- [ ] V2 static check finds no mapped old underscore custom agent IDs in live Codex/runtime/spec surfaces, excluding historical `_sdd` artifacts and old log lines.
- [ ] V3 confirms built-in roles remain unchanged.
- [ ] V4 confirms artifact slug conventions were not renamed.
- [ ] V5 fresh-process smoke resolves `feature-draft-agent` and `implementation-agent` with resolution-only prompts that instruct the spawned agent not to read files, write files, or run commands.
- [ ] V6 manual review confirms `sdd-autopilot` contract/sample/profile emits kebab-case IDs and rejects underscore IDs.
- [ ] V7 confirms `_sdd/spec/main.md` generic `_agent` canonical text and `.codex/agents/README.md` underscore stem inventories are gone, while `.codex/skills/investigate/SKILL.md` keeps `investigate_agent` only as the removed-agent historical note.

**Target Files**:
- [TBD] No file modification expected -- validation only; if results are recorded, use the implementation report/progress artifact chosen by the implementation skill.

**Technical Notes**: Covers V1-V7, I3, and I4. Use fresh `codex exec` or a new thread for runtime smoke; same-session failures are expected after registry changes. The smoke prompt is a no-op resolution check and must not ask spawned agents to inspect the repository.
**Dependencies**: T1, T2, T3, T4, T5

## Parallel Execution Summary

No task should run in parallel with another task that writes files. The same old IDs are shared across agent TOMLs, wrapper skills, `sdd-autopilot` contract files, and spec/docs. Sequential execution keeps the rename atomic and reduces false positives from partial grep states.

Potential read-only validation can run in parallel after T1-T5 are complete, but T6 should report one integrated result because V2/V4 require interpreting allowed historical exceptions.

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Current session still exposes old underscore roles. | Run V5 in fresh `codex exec` or a new session; record current-session schema as stale cache only. |
| Artifact slugs are accidentally renamed. | V4 explicitly checks `_feature_draft_`, `_implementation_plan_`, `_plan_review_`, and related slugs. |
| Historical logs keep old names and confuse grep. | V2 excludes historical artifacts and old log lines; T4 adds new current entries instead of rewriting history. |
| Built-in roles are accidentally touched. | T3/T5 keep built-in examples unchanged; V3 checks `explorer`, `worker`, `default`. |
| Alias policy keeps both conventions alive. | T3 updates `sdd-autopilot` to reject/regenerate underscore custom agent IDs instead of normalizing them. |
| Removed `investigate_agent` note is mistaken for a current target. | T2 and V7 classify `.codex/skills/investigate/SKILL.md` line 83 as an allowed removed-agent historical note and forbid adding an `investigate-agent` TOML target. |

## Open Questions

- None requiring user confirmation. Q4 in Part 1 has MEDIUM confidence because alias-free migration can break stale external references, but it matches the stated goal of removing invocation confusion and the current `sdd-autopilot` reject/regenerate style. Q5 classifies the live `investigate_agent` text as an allowed removed-agent historical note, not an implementation target.

## Self-Containment Check

- 검토 섹션 수: 9 (`Overview`, `Scope`, `Components`, `Contract/Invariant Delta Coverage`, `Implementation Phases`, `Task Details`, `Parallel Execution Summary`, `Risks and Mitigations`, `Open Questions`)
- Pass 1 발견 갭 및 보완:
  - `Overview`: 처음에는 "custom agent ID"가 external context에 의존했다. 보완: `.codex/agents/*.toml` `name`과 `spawn_agent(agent_type=...)` 값이라는 정의를 추가했다.
  - `Task Details T4`: `_sdd/spec/DECISION_LOG.md`와 changelog의 historical old names 처리 기준이 불분명했다. 보완: append-only entry를 추가하고 older historical lines는 유지한다고 명시했다.
  - `Task Details T6`: fresh-process smoke가 왜 필요한지 대화 맥락에 의존했다. 보완: current-session registry hot-reload failure와 fresh `codex exec` requirement를 description/technical notes에 명시했다.
  - `Task Details T2/T6`: `investigate_agent`가 current custom agent인지 removed historical note인지 불분명했다. 보완: `.codex/skills/investigate/SKILL.md` line 83을 allowed removed-agent historical note로 분류하고 V7 검증 예외를 추가했다.
  - `Task Details T4/T5`: `_sdd/spec/main.md` generic `_agent` canonical statement와 `.codex/agents/README.md` Inline Writing stem inventory가 bare path 수준으로만 남을 수 있었다. 보완: 각 AC와 V7에 line/surface purpose를 명시했다.
- Pass 2 발견 갭 및 보완:
  - `Components`: built-in role과 custom agent의 차이를 reader가 모를 수 있었다. 보완: built-ins are unchanged and not TOML custom names라는 scope/component 문장을 추가했다.
  - `Implementation Phases`: 왜 병렬화하지 않는지 파일 충돌 기준이 부족했다. 보완: shared `sdd-autopilot` files and grep partial-state risk 때문에 sequential이라고 명시했다.
  - `Open Questions`: MEDIUM confidence Q4가 사용자 확인 필요로 오해될 수 있었다. 보완: stated goal and existing reject/regenerate style에 근거해 confirmation이 필요 없다고 설명했다.
  - `Validation`: fresh `codex exec` smoke가 no-op의 의미를 reader가 다르게 해석할 수 있었다. 보완: spawned agent에게 file read/write/command execution을 시키지 않는 resolution-only prompt라고 명시했다.
- 보완 완료: Yes
