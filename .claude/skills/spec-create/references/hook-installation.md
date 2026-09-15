# Hook Installation Contract

> Authoring canonical: `.claude/skills/spec-create/references/hook-installation.md`. The copies under the other `spec-create`/`spec-upgrade` packages are exact distribution mirrors so each skill remains self-contained.

## Trigger and Inputs

Read and apply this whole reference when the skill creates or merges the `AGENTS.md` SDD-HARNESS block. Hook installation has the same trigger as the harness: install both Claude Code and Codex registrations together; it is not a separate opt-in.

Inputs:

- the four canonical scripts in the calling skill's local `references/hooks/`
- the consumer repo's `.claude/settings.json`, if present
- the consumer repo's `.codex/hooks.json`, if present
- the consumer repo root used by Codex commands

## Hook Asset Matrix

| Script | Purpose |
|---|---|
| `worklog-gate.sh` | Enforce the harness §5 work-log gate for Bash commands. |
| `agent-watchdog.sh` | Send a fail-open advisory nudge when a subagent runs beyond its threshold. |
| `worklog-context.sh` | Inject today's work-log state for every session-start source. |
| `harness-context.sh` | Re-inject the full `AGENTS.md` after context loss. `startup` follows the `CLAUDE.md` pointer; `resume` and `fork` restore context, so only `clear` and `compact` belong here. |

`worklog-gate.sh` rejects the session's first `git commit` when today's work log has no uncommitted change. `agent-watchdog.sh` measures from a subagent's first tool call, nudges after five minutes, preserves the original tool result, adds the nudge as additional context beside it, and fails open when it cannot decide.

## Verbatim Script Copy

Read these four local assets and write them under the same names in the consumer repo's `.claude/hooks/`:

- `references/hooks/worklog-gate.sh`
- `references/hooks/worklog-context.sh`
- `references/hooks/harness-context.sh`
- `references/hooks/agent-watchdog.sh`

Copy every script verbatim. Do not add, delete, reorder, summarize, or substitute lines or slots. The harness fixes `_sdd/work_log/<yyyy-mm-dd>.md`, and the harness asset itself fixes the `AGENTS.md` injection target. Do not reconstruct scripts from memory or from this prose. Overwrite an existing installed script with the current local canonical asset.

Use the shared `.claude/hooks/` installation for both runtimes. Do not create a second `.codex/hooks/` script copy and do not add a `chmod` step; every registered command invokes `bash <path>` directly.

## Idempotent Settings Merge

Treat `.claude/settings.json` and `.codex/hooks.json` as independent key-level idempotent merge units. Regardless of the calling runtime, attempt both files. The four scripts are independent registrations.

### Absent file

Create the file with only the four SDD hook groups from the matching complete runtime definition below.

### Existing file

Add the required groups to `hooks.PreToolUse`, `hooks.PostToolUse`, and `hooks.SessionStart`. If an existing `command` contains `.claude/hooks/<script>.sh`, replace the **whole outer group object** containing that handler with the matching canonical group. Replacing only the inner `{type, command}` cannot repair a stale event or matcher.

Preserve unrelated top-level keys, events, groups, and user hook handlers. Re-running the merge must not accumulate duplicate SDD handlers.

### Mixed group

1. Capture the original event and matcher before replacing the group.
2. Move only the SDD handler to its canonical runtime group.
3. Put all remaining non-SDD handlers together in a separate group under the original event and matcher.
4. Omit the matcher key if the original group had none, and preserve other group fields that belong to the user's handler contract.

### Malformed JSON

If one settings file cannot be parsed, preserve its bytes and skip registration for that runtime. Continue copying all four scripts and continue the merge for the other runtime. Record the skipped runtime and partial failure in the final report. Finish the other safe installation work, then return the partial result; do not retry the skipped registration until the input is corrected. A partial result is not a complete installation.

## Runtime Definitions

### Claude Code — `.claude/settings.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "bash \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/worklog-gate.sh" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "hooks": [
          { "type": "command", "command": "bash \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/agent-watchdog.sh" }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          { "type": "command", "command": "bash \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/worklog-context.sh" }
        ]
      },
      {
        "matcher": "clear|compact",
        "hooks": [
          { "type": "command", "command": "bash \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/harness-context.sh" }
        ]
      }
    ]
  }
}
```

### Codex — `.codex/hooks.json`

Codex hook commands run from the session working directory, so resolve the shared installation from the git root.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "bash \"$(git rev-parse --show-toplevel)/.claude/hooks/worklog-gate.sh\"" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "hooks": [
          { "type": "command", "command": "bash \"$(git rev-parse --show-toplevel)/.claude/hooks/agent-watchdog.sh\"" }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          { "type": "command", "command": "bash \"$(git rev-parse --show-toplevel)/.claude/hooks/worklog-context.sh\"" }
        ]
      },
      {
        "matcher": "clear|compact",
        "hooks": [
          { "type": "command", "command": "bash \"$(git rev-parse --show-toplevel)/.claude/hooks/harness-context.sh\"" }
        ]
      }
    ]
  }
}
```

## Codex Trust Boundary

Codex hooks require version 0.124.0+ and a trusted project `.codex/` layer. A non-managed exact definition does not run until the user reviews and trusts it through `/hooks`; changing the definition requires review again. Do not approve trust automatically, bypass trust, or modify user-global Codex settings. Without evidence that the current exact definition has been reviewed and trusted, runtime acceptance remains `pending user trust`; structural checks alone cannot complete acceptance. Finish document and registration preparation and safe verification before leaving `/hooks` review as the user’s remaining action.

## Verification and Report

### Verify

- Installed scripts are byte-identical to the four local assets.
- For each registered runtime, SDD hook groups exactly match its complete `Runtime Definition`, and a second merge produces no diff or duplicate SDD handler.
- For a skipped runtime, verify the original file remains byte-identical and report the parse failure instead of requiring registration checks.
- Existing unrelated keys and handlers remain, and mixed non-SDD handlers retain their original event/matcher.
- Assess runtime acceptance separately from installation checks. Apply `Codex Trust Boundary` to the current definition, and claim lifecycle execution only with observed evidence. Missing trust or execution evidence remains pending/unverified, without repeated installation attempts.

### Report

- Common:
  - script placement
  - each runtime's registration status: `created | replaced | already current | skipped`
  - installation verification results, parse failures, and any partial result
  - each runtime's acceptance evidence or remaining requirement; for Codex use `pending user trust` when the trust boundary is not satisfied
  - remaining user action for partial or pending acceptance; do not label either as complete acceptance
- Claude Code notices:
  - `.claude/settings.json` is committed project configuration
  - the gate applies to the session's first `git commit`, and `SDD_SKIP_WORKLOG=1` bypasses it
  - compact/clear re-injects the full `AGENTS.md`
  - SessionStart matcher support was observed in Claude Code 2.1.220; unsupported versions do not fire and do not report an error
  - a `[harness]` line after compact/clear confirms execution
- Codex notices:
  - version 0.124.0+ and project trust are required
  - `/hooks` review is required before a non-managed exact definition runs and again after its definition changes
  - trust was not auto-approved and no user-global setting was changed
