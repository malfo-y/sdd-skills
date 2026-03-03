---
name: ralph-loop-init
description: Use this skill when the user asks to "init ralph", "ralph loop", "set up ralph loop", "training loop", "training debug loop", "create ralph", "set up training debug loop", "automated training loop", or wants to generate a `ralph/` directory for Codex-driven automated ML training debugging.
---

# Ralph Loop Initialization (Codex)

> **Security Notice**: The generated `run.sh` uses `codex exec --dangerously-bypass-approvals-and-sandbox` for unattended automation. This grants full filesystem and command execution access with no interactive confirmation. Only run ralph loops in trusted repositories inside isolated environments (container, VM, dedicated sandbox machine). Do not run on hosts with sensitive credentials or production access.

Generate a complete `ralph/` directory for Codex-driven automated ML training debugging.
The ralph loop is a `while true` automation: Codex reads state and results, writes `action.sh`, the script executes it, and the loop repeats until training is complete or escalation is required.

This skill discovers the project training pipeline, confirms findings with the user, and generates five project-specific files:
`CHECKS.md`, `config.sh`, `PROMPT.md`, `run.sh`, and `state.md`.

---

## Step 0: Read Project Specs

Check whether `_sdd/` exists in the project root.

If it exists:
1. Locate `_sdd/spec/**/*.md`.
2. If multiple candidates exist, ask the user directly which files define the training pipeline.
3. Read relevant spec files as the primary source of truth for architecture intent.
4. Extract key data: training entrypoint, dataset format, CLI args, loss, validation flow, hyperparameters, framework constraints.

If `_sdd/` does not exist, continue with code-only discovery.

Environment context rule:
- If `_sdd/env.md` exists, read it and extract only runtime setup hints
  (e.g., conda env name, required env var names).
- Never copy secret values from `_sdd/env.md` into generated files, logs, or chat output.
- Reflect this in generated `ralph/PROMPT.md` as an environment setup reference.

---

## Step 1: Discover the Training Pipeline

Use file discovery and source inspection (prefer `rg`-based search) to identify:

### 1.1 Training Script
- Search candidates such as `**/train*.py`, `**/training*.py`, `**/run_training*.py`.
- Read the main script.
- Parse argparse/click options to map CLI surface.
- Detect framework (accelerate, raw PyTorch, PyTorch Lightning, HuggingFace Trainer).

### 1.2 Validation Script
- Search `**/valid*.py`, `**/eval*.py`, `**/infer*.py`, `**/generate*.py`.
- If none exists, mark validation as skipped/minimal in generated prompt.

### 1.3 Dataset
- Extract dataset-related paths from args/config files.
- Identify format (JSONL files, WebDataset, HuggingFace datasets, etc.).

### 1.4 Structured Logging
- Search for the literal token `[TRAIN]` in training source (use fixed-string mode or escaped brackets: `\[TRAIN\]`).
- If found, include structured event parsing instructions.
- Otherwise, use raw log parsing instructions.

### 1.5 Python Command
- If `pyproject.toml` indicates `uv` workflow, use `uv run python`.
- If only `requirements.txt`-style setup is present, use `python3` (or `python` if needed).
- Default to `python3`.

### 1.6 Cross-check With Spec
- Compare code findings with Step 0 spec findings.
- Use spec context to fill intent-level gaps (metric priorities, tuning strategy, validation goals).

---

## Step 2: Confirm Findings With User

Ask the user directly to confirm or correct:

1. Training script path
2. Validation script path (or "none")
3. Dataset path
4. Model path/ID
5. GPU setup (count, precision)
6. Initial hyperparameters (learning rate, epochs, batch size)
7. Python command (`uv run python`, `python3`, or other)

Ask in a compact checklist format so the user can accept defaults quickly.

---

## Step 2.5: Write `ralph/CHECKS.md`

Before generating any files, create `ralph/` directory and write `ralph/CHECKS.md`.
This document defines acceptance criteria for each generated file and is written first so generation targets are explicit before output is produced.

Content to write:

---
```
# Ralph Loop: Acceptance Criteria
Generated: <current UTC timestamp>
Project: <project name>

## config.sh
- [ ] No `<placeholder>` strings remain (no `<...>` literals)
- [ ] `MAX_STEPS="10"` is set for debug-first approach
- [ ] `LLM_TIMEOUT_SECONDS` is defined
- [ ] Every variable referenced in PROMPT.md's training command is defined here
- [ ] Variable names match the training script's actual CLI argument names

## PROMPT.md
- [ ] Anti-recursion warning present near the top
- [ ] `SMOKE_TEST` phase defined between `SETUP` and `TRAINING`
  - [ ] `SMOKE_TEST` runs training with `MAX_STEPS=1` (hardcoded, overrides config)
  - [ ] Pass criteria stated: exit code 0 AND log contains ≥1 step indicator
  - [ ] On PASS -> transitions to `TRAINING`
  - [ ] On FAIL -> transitions to `ADJUSTING` with "SMOKE_TEST failed: <error>"
  - [ ] If failure originated in SMOKE_TEST, ADJUSTING sends phase back to `SMOKE_TEST` (repeat gate)
- [ ] All phases present: SETUP, SMOKE_TEST, TRAINING, VALIDATING, ANALYZING, ADJUSTING, DONE
- [ ] TRAINING section contains exact command using `config.sh` variables
- [ ] VALIDATING section contains exact command or explicit skip notice
- [ ] `## Known Errors` section present (E1 macOS timeout included if applicable)
- [ ] `## action.sh Rules` section present
- [ ] `SMOKE_TEST` explicitly states `MAX_STEPS=1` is the only allowed hardcoded exception
- [ ] PROMPT.md self-correction protocol present in ADJUSTING section (Step 2.5 or dedicated subsection)

## decisions.md
- [ ] PROMPT.md instructs Codex to read the most recent 15 entries from `ralph/results/decisions.md` each iteration (after state.md)
- [ ] PROMPT.md instructs Codex to append to `ralph/results/decisions.md` each iteration (after updating state.md)
- [ ] Decision entry format is specified in PROMPT.md (Iteration N, Observed, Decision, Reason, Evidence, Action)
- [ ] Decision Evidence rule requires concrete artifacts (`exit code` and `log/artifact path`)

## run.sh
- [ ] `--reset` flag behavior present (clears `ralph/results/`, rewrites `state.md`)
- [ ] `LLM_TIMEOUT_SECONDS` sourced from `config.sh`
- [ ] DONE phase detection present (loop exits when `phase: DONE`)

## state.md
- [ ] `phase: SETUP`
- [ ] `iteration: 0`
- [ ] `initialized_at` set to current UTC timestamp (no `__INITIALIZED_AT_UTC__` placeholder)
```
---

---

## Step 3: Generate `ralph/config.sh`

Create `ralph/config.sh` with grouped variables:

```bash
#!/usr/bin/env bash
# Ralph Loop Configuration
# Edit these values BEFORE running: bash ralph/run.sh

# -- Model --
MODEL_ID="<discovered or user-specified>"
MODEL_BASE_PATH="<path to pretrained models>"

# -- Dataset --
DATASET_PATH="<discovered dataset path>"

# -- Training --
LEARNING_RATE=<suggested default>
NUM_EPOCHS=<suggested default>
MAX_STEPS="10"  # debug-first sanity run
GRADIENT_ACCUMULATION_STEPS=1

# -- GPU / Distributed --
NUM_GPUS=<detected>
MIXED_PRECISION="<suggested>"

# -- Output --
OUTPUT_PATH="./models/train/<project-specific>"
LOG_EVERY=10

# -- Loop Safety --
LLM_TIMEOUT_SECONDS=600  # max seconds for one Codex turn (0 disables timeout)
```

Key rules:
- Keep `MAX_STEPS="10"` for the first run.
- Set `LLM_TIMEOUT_SECONDS` to bound a single Codex turn and avoid indefinite hangs.
- Use variable names aligned with real CLI arguments.
- Include only variables that are actually consumed by the training pipeline.
- Add brief comments only where needed.

---

## Step 4: Generate `ralph/PROMPT.md`

### 4.1 Read the Reference
Find and read `ralph-loop-concept.md` by globbing:
- `**/.codex/skills/ralph-loop-init/references/ralph-loop-concept.md`

This supports both global (`~/.codex/skills/`) and repo-local (`.codex/skills/`) skill installs.

### 4.2 Build Project-Specific Prompt
Generate `ralph/PROMPT.md` with this structure:

```markdown
# Ralph Loop: <Project Name> Training

IMPORTANT: Do NOT invoke skills, modes, slash commands, or automation directives.
Do NOT start nested Codex sessions (`codex`, `codex exec`, etc.).
You are inside a standalone training automation loop, not an interactive assistant session.

You are running inside an automated training loop.

[... core concept from reference ...]

**Your job**: Read state, diagnose, write `ralph/action.sh`, update `ralph/state.md`, then exit.

**DO NOT** run long training/validation commands directly. Put them into `ralph/action.sh`.

## Step-by-step for EVERY iteration
[... iteration protocol from reference, including reading the most recent 15 decisions from decisions.md after state.md and appending a new decision entry after updating state.md ...]

## Project Context
- Config: `ralph/config.sh`
- Python command: `<detected python command>`
- Validation script: `<path or none>`
- Results dir: `ralph/results/`
- Environment setup reference: `_sdd/env.md` (if present)
- `run.sh` archives executed `ralph/action.sh` to `ralph/results/action_iter{N}.sh`; missing `ralph/action.sh` next iteration is expected.
- If Python command contains `conda run`, never use `${PYTHON_CMD} - <<'PY'`; write runner files under `ralph/results/*.py` and execute `${PYTHON_CMD} <runner.py>`.

## State Machine
### SETUP
[... project checks ...]
- If a required env var is missing, check `_sdd/env.md` first and attempt shell/env loading before declaring STUCK.
### SMOKE_TEST
**Purpose**: Verify the training pipeline runs end-to-end before committing to full training.
- Write `action.sh` to run the training command with `MAX_STEPS=1` (hardcode this value; do not use `${MAX_STEPS}`).
- Save output to `ralph/results/smoke_test.log` (`2>&1 | tee`).
- After execution, grep the log for at least one step/loss indicator:
  - Structured logs: `[TRAIN] event=step`
  - Raw logs: `loss=` or `step 1` (or project-equivalent)
- Acceptance criteria (both): exit code `0` and at least one step indicator in `smoke_test.log`.
- On PASS: set `phase: TRAINING` with note `Smoke test passed (1 step).`
- On FAIL: set `phase: ADJUSTING` with note `SMOKE_TEST failed: <first error from log>`.
**Repeat gate rule**:
- If ADJUSTING fixes a failure that originated in SMOKE_TEST, set phase back to `SMOKE_TEST` and rerun the 1-step smoke test.
- Do not transition to `TRAINING` until SMOKE_TEST passes.
[Note: `MAX_STEPS=1` in SMOKE_TEST is hardcoded intentionally and is the only exception to the general config-variable/no-hardcoding rule.]
### TRAINING
[... exact training command with config vars ...]
### VALIDATING
[... exact validation command or skipped ...]
- Before generating a new validation action, check if existing validation output already determines pass/fail.
- If validation action exit code is `0` but required validation output file is still missing, transition to `ADJUSTING` (root cause: output-not-produced) instead of repeating the same validation action indefinitely.
### ANALYZING
[... project-specific metrics analysis ...]
[... write ralph/results/experiment_report.md per Section 11 of the reference ...]
### ADJUSTING
[... debugging protocol + project-specific error patterns ...]

### PROMPT.md Self-Correction (Section 14 of reference)
When a recurring error (2+ occurrences) traces back to an incorrect template in this PROMPT.md:
1. Fix the template directly using the Edit tool.
2. Add the error to `## Known Errors`.
3. Record `"iterN PROMPT_FIX: <phase> - <description>"` in `state.md` errors.
4. No `action.sh` needed; set phase back to the failed phase for retry.

Allowed: env vars, paths, variable names, phase transition instructions, Known Errors additions.
Not allowed: changing state machine structure, removing phases, rewriting core protocol.

### DONE
[... final summary format ...]
[... confirm experiment_report.md was written ...]

## action.sh Rules
[... 10 rules from reference, customized python command ...]
- Include the "no heredoc with `conda run`" and "no blind reuse of archived action_iter scripts" constraints from the reference.

## Decision Log
After updating `ralph/state.md`, append one decision entry to `ralph/results/decisions.md`.

### Format
Each iteration, append exactly one entry:

    ## Iteration {N} - {PHASE}
    - **Observed**: {key facts from logs, exit codes, and state}
    - **Decision**: {action/transition selected}
    - **Reason**: {why this decision over alternatives}
    - **Evidence**: {must cite concrete artifacts, including exit code and log/artifact path}
    - **Action**: {action.sh summary or "Codex-only iteration (no action.sh)"}

### Rules
- At the start of each iteration (after reading `state.md`), read the most recent 15 entries from `ralph/results/decisions.md` (if fewer than 15, read all).
- If a repeated failure pattern is suspected and not explained by the recent 15 entries, search older decision entries by keyword before deciding.
- Append-only: never overwrite prior entries.
- One entry per iteration, including Codex-only iterations (SETUP, ANALYZING, DONE).
- Keep each field to 1-2 sentences.

## state.md Format
[... canonical format from reference ...]
```

Required project-specific customizations:
- SMOKE_TEST grep pattern must match the project's actual log format (structured `[TRAIN] event=step` or raw `loss=`/`step 1`).
- SMOKE_TEST must enforce repeat-gate behavior (`ADJUSTING -> SMOKE_TEST` for smoke-origin failures).
- SMOKE_TEST must call out `MAX_STEPS=1` as an explicit exception to the no-hardcoding rule.
- Exact training command using `config.sh` variables
- Exact validation command (or explicit skip)
- Log parsing instructions matching actual log format
- Project-specific error patterns
- Environment setup guidance referencing `_sdd/env.md` when available
- Python execution style that is safe for the detected command (especially `conda run` stdin/heredoc caveat)
- Artifact-driven phase transitions that prevent VALIDATING/ADJUSTING infinite loops
- Decision Log section with recent-15 read rule and Evidence requirement
- PROMPT.md self-correction protocol (`PROMPT_FIX` record + retry)

### 4.3 Generate `## Known Errors` Section in PROMPT.md

After the ADJUSTING section, add a `## Known Errors (Confirmed + Fixed)` section following the format in Section 12 of the reference.

Always include E1 (macOS timeout) if the environment is or may be macOS:

```markdown
### E1: `timeout: command not found`
- **Where**: Any action.sh using `timeout N cmd`
- **Cause**: macOS does not ship GNU `timeout`
- **Fix**: Use background process + kill pattern (see reference Section 12)
- **Status**: ✅ Use pattern from Section 12 whenever timeout is needed
```

Add project-specific errors discovered during Step 1 (code discovery):
- If the project imports packages from sibling directories (not in the venv), add a PYTHONPATH error entry.
- If the project requires specific directories to exist at runtime (for example `./data/`, `./outputs/`), add a missing-directory entry.
- If there are known schema or API compatibility issues from spec/README, add them.

Codex in the ralph loop checks this section first in ADJUSTING (Step 0 of the ADJUSTING protocol), so pre-populating anticipated errors reduces investigation turns.

---

## Step 5: Generate `ralph/run.sh`

Find and read template by globbing:
- `**/.codex/skills/ralph-loop-init/examples/run.sh.example`

Copy nearly verbatim into `ralph/run.sh`.
Adjust only if `python3` is unavailable for the inline JSON parser.

The template uses `codex exec --json` and a retry-on-failure guard for Codex step failures.
Keep the template's CLI behavior:
- `bash ralph/run.sh` resumes from current `state.md`/`results`.
- `bash ralph/run.sh --reset` clears prior loop artifacts (`ralph/results/`, stale `ralph/action.sh`) and rewrites `ralph/state.md` to the initial SETUP state with a fresh `initialized_at` UTC timestamp before starting.
- Source `ralph/config.sh` and apply `LLM_TIMEOUT_SECONDS` to each Codex planning turn (default 600 seconds, `0` disables timeout).

Mark executable:
- `chmod +x ralph/run.sh`

---

## Step 6: Generate `ralph/state.md`

Find and read template by globbing:
- `**/.codex/skills/ralph-loop-init/examples/state.md.example`

Copy the template into `ralph/state.md`, then replace `__INITIALIZED_AT_UTC__` with the current UTC timestamp (`date -u '+%Y-%m-%dT%H:%M:%SZ'`):

```yaml
phase: SETUP
iteration: 0
initialized_at: __INITIALIZED_AT_UTC__
errors: []
last_checkpoint: null
validation_results: null
notes: Initial state. Ralph loop initialized.
```

---

## Step 7: Verify Against CHECKS.md and Summarize

### 7.1 Verify Each File Against Its Criteria

For each criterion in `ralph/CHECKS.md`, perform a targeted check:

**config.sh**:
- Check for remaining placeholders: count occurrences of `<` in the file (expect 0).
- Check `MAX_STEPS="10"` is present.
- Check `LLM_TIMEOUT_SECONDS` is defined.
- Check every variable referenced in PROMPT.md's TRAINING command is defined in config.sh.
- Check variable names align with training script CLI argument names.

**PROMPT.md**:
- Check anti-recursion warning: grep for `Do NOT invoke`.
- Check SMOKE_TEST phase: grep for `SMOKE_TEST`.
- Check SMOKE_TEST hardcoded rule: grep for `MAX_STEPS=1` and confirm it does not use `${MAX_STEPS}`.
- Check SMOKE_TEST pass criteria: grep for both `Exit code = 0` and `step completion indicator`.
- Check SMOKE_TEST repeat gate: confirm `ADJUSTING -> SMOKE_TEST` behavior is written.
- Check all phases present: SETUP, SMOKE_TEST, TRAINING, VALIDATING, ANALYZING, ADJUSTING, DONE.
- Check TRAINING section includes exact command using config variables.
- Check VALIDATING section includes exact command or explicit skip.
- Check Known Errors section: grep for `## Known Errors`.
- Check action.sh Rules section: grep for `## action.sh Rules`.
- Check PROMPT.md self-correction: grep for `PROMPT_FIX` or `Self-Correction` or `self-correction`.
- Check decision log reading instruction includes recent-15 scope: grep for `most recent 15` and `decisions.md`.
- Check decision log writing/append instruction: grep for `append` and `decisions.md`.
- Check decision format includes Evidence artifacts: grep for `**Evidence**`, `exit code`, and `log/artifact path`.

**run.sh**:
- Check `--reset` flag: grep for `--reset`.
- Check `LLM_TIMEOUT_SECONDS`: grep for `LLM_TIMEOUT_SECONDS`.
- Check DONE phase detection: grep for `phase: DONE` or equivalent.

**state.md**:
- Check phase: grep for `^phase: SETUP`.
- Check iteration: grep for `^iteration: 0`.
- Check no placeholder: confirm `__INITIALIZED_AT_UTC__` is NOT in the file.

Mark each check as ✅ pass or ❌ fail in output. If any criterion fails, fix the generated file before proceeding.

### 7.2 Update CHECKS.md with Results

After verification, update `ralph/CHECKS.md`:
- Replace `[ ]` with `[x]` for passing criteria.
- Replace `[ ]` with `[!]` for failing criteria and add a note on what was wrong/how it was fixed.

### 7.3 Create results directory and Summarize

Create `ralph/results/` directory (`mkdir -p`), then print summary:

```
Ralph loop initialized (TDD verified)!

Files created:
  ralph/CHECKS.md    — Acceptance criteria (all criteria verified ✅)
  ralph/config.sh    — Training configuration (edit before running)
  ralph/PROMPT.md    — Codex instructions for the training loop
  ralph/run.sh       — Loop controller script
  ralph/state.md     — Initial state (SETUP, iteration 0)
  ralph/results/     — Output directory

Loop phases: SETUP -> SMOKE_TEST -> TRAINING -> VALIDATING -> ANALYZING -> DONE

Next steps:
  1. Review and edit ralph/config.sh (especially dataset/model paths)
  2. Resume run: bash ralph/run.sh
  3. Fresh restart (clear old outputs): bash ralph/run.sh --reset
  4. The loop will SMOKE_TEST (1 step) before TRAINING (MAX_STEPS=10)
  5. Ctrl+C to stop at any time
```

Remind user that `MAX_STEPS="10"` is for the debug training run after smoke test passes; increase it (or set empty for unlimited) once the first full run succeeds.
