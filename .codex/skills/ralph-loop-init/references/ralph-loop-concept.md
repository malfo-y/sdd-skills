# Ralph Loop: Architecture Reference

This document describes the architecture of a ralph loop — an LLM-driven automated ML training debugger. Use this as a reference when generating project-specific `ralph/PROMPT.md` files.

---

## 1. Core Concept

```
while true:
    Phase 1: LLM reads state + results -> writes action.sh
    Phase 2: run.sh executes action.sh (training, validation — may take hours)
    repeat until phase = DONE
```

The LLM's job: Read state, diagnose, then output `ralph/action.sh` and update `ralph/state.md`. Exit immediately after.

The LLM must **never** run training or long commands itself. It writes them into `ralph/action.sh` instead.

`run.sh` archives each executed `ralph/action.sh` to `ralph/results/action_iter{N}.sh`; therefore, the next iteration may start with no `ralph/action.sh`, which is normal.
`run.sh` should enforce a per-turn timeout using `LLM_TIMEOUT_SECONDS` from `ralph/config.sh` so a hung LLM turn cannot block the loop forever.

---

## 2. Directory Structure

```
ralph/
├── PROMPT.md       <- LLM instruction document (state machine, log parsing guide)
├── config.sh       <- User-editable parameters (project-specific)
├── run.sh          <- Loop controller (LLM -> action.sh -> repeat)
├── action.sh       <- LLM-generated execution script (each iteration)
├── state.md        <- Current phase, iteration, errors, checkpoint path, notes
└── results/        <- Training/validation logs and outputs
    ├── decisions.md        <- Accumulated LLM decision summaries per iteration
    ├── training.log
    ├── last_exit_code
    ├── last_checkpoint_path
    ├── validation.log
    ├── validation_output/
    ├── action_iter{N}.sh  <- Archived action script from each completed execution
    ├── llm_iter{N}.json   <- LLM stream-json log (for debugging)
    └── experiment_report.md  <- Experiment report for production runs
```

---

## 3. State Machine

```
SETUP -> SMOKE_TEST -> TRAINING -> VALIDATING -> ANALYZING -> DONE
                \-> ADJUSTING -> SMOKE_TEST (if smoke-test failure)
                          \----> TRAINING / VALIDATING (other fixes)
```

| Phase | Role | action.sh | Next Phase |
|-------|------|-----------|------------|
| **SETUP** | Verify environment (dataset, scripts, GPU) | Not needed (LLM checks only) | SMOKE_TEST |
| **SMOKE_TEST** | Run 1 training step to verify pipeline works | Training with `MAX_STEPS=1` | TRAINING (pass) / ADJUSTING (fail) |
| **TRAINING** | Execute training | Training script + log capture | VALIDATING (success) / ADJUSTING (failure) |
| **VALIDATING** | Run validation/inference | Validation script | ANALYZING (success) / ADJUSTING (failure) |
| **ANALYZING** | Analyze results + write experiment report | Not needed (LLM analysis only) | DONE |
| **ADJUSTING** | Diagnose error + apply fix | Fix action (optional) | SMOKE_TEST / TRAINING / VALIDATING (retry) |
| **DONE** | Final summary + verify experiment report | Not needed | — |

### Transition Rules

- **SETUP -> SMOKE_TEST**: Environment verified (dataset exists, training script exists, GPU available)
- **SMOKE_TEST -> TRAINING**: exit code 0 AND log contains ≥1 step completion indicator
- **SMOKE_TEST -> ADJUSTING**: exit code != 0, or no step logged
- **TRAINING -> VALIDATING**: exit code 0 + checkpoint exists
- **TRAINING -> ADJUSTING**: exit code != 0, or NaN detected, or training anomaly
- **VALIDATING -> ANALYZING**: Validation output files generated and non-trivial (>10KB)
- **VALIDATING -> ADJUSTING**: Validation failed
- **VALIDATING -> ADJUSTING**: Validation action reported success (`last_exit_code=0`) but expected validation output file is still missing (indicates broken action script/runner)
- **ANALYZING -> DONE**: Analysis complete, summary written, experiment_report.md generated
- **ADJUSTING -> SMOKE_TEST**: If the failure being fixed originated in SMOKE_TEST, rerun the smoke gate before allowing full training
- **ADJUSTING -> TRAINING**: Fix applied, retry training
- **ADJUSTING -> VALIDATING**: Fix applied, retry validation

**Note**: SMOKE_TEST uses `MAX_STEPS=1` hardcoded in action.sh — it does not read `${MAX_STEPS}` from config.sh. This ensures the smoke test is always fast (seconds to minutes) regardless of the configured training length.

### Escalation Rules

- Same root cause fails **3 times** -> set phase to DONE with note "STUCK: {error description}. Human intervention needed."
- Error cannot be diagnosed (no traceback, no clear cause) -> set phase to DONE with note "UNKNOWN ERROR: {last 10 lines of log}. Human intervention needed."
- Error requires external action (API key, hardware change, data corruption) -> set phase to DONE with explanation

### ANALYZING Phase Protocol

After writing the summary to state.md, the LLM **must** generate `ralph/results/experiment_report.md` following the template in Section 11. This document captures everything needed to reproduce the experiment at production scale.

---

## 4. Iteration Protocol (11 Steps)

Every iteration, the LLM must follow these steps in order:

1. Read `ralph/config.sh` (user-specified parameters)
2. Read `ralph/state.md` (current phase, errors, notes)
3. Read the most recent 15 entries from `ralph/results/decisions.md` if it exists (prior iteration decisions — see Section 13). If fewer than 15 exist, read all.
4. Read `ralph/results/last_exit_code` if it exists (was previous action successful?)
5. Read any result files relevant to the current phase
6. Read `_sdd/env.md` if it exists (Python environment, required env variables, runtime configuration)
7. Decide what to do next
8. Write `ralph/action.sh` with the next action (or skip if LLM-only iteration)
9. Update `ralph/state.md` (always increment iteration, update phase/notes)
10. Append this iteration's decision entry to `ralph/results/decisions.md` (see Section 13)
11. Exit

---

## 5. action.sh Canonical Rules

Every `action.sh` must follow these rules:

1. Always start with `#!/usr/bin/env bash` and `set -euo pipefail`
2. Always `source ralph/config.sh` to load user-specified parameters
3. Always `mkdir -p ralph/results` at the top
4. Always `export PYTHONUNBUFFERED=1` (flush output immediately, prevents lost logs on crash)
5. Always `export TQDM_DISABLE=1` for training scripts (suppress tqdm noise)
6. Use config variables (`${LEARNING_RATE}`, `${NUM_EPOCHS}`, etc.) — never hardcode values, except SMOKE_TEST's intentional `MAX_STEPS=1` override
7. Save all outputs to `ralph/results/` so LLM can read them next iteration
8. Use `2>&1 | tee ralph/results/<name>.log` to capture stdout+stderr
9. Keep it simple — one logical action per script
10. Use the correct Python command for the project (e.g., `uv run python`, `python3`, etc.)
11. If the Python command includes `conda run`, do **not** execute inline heredoc Python (`${PYTHON_CMD} - <<'PY'`); write a runner `.py` file and execute it.
12. Do not blindly copy archived `ralph/results/action_iter*.sh`; regenerate a fresh action script from current state/results.

---

## 6. state.md Canonical Format

```
phase: <SETUP|SMOKE_TEST|TRAINING|VALIDATING|ANALYZING|ADJUSTING|DONE>
iteration: <number>
initialized_at: <ISO-8601 UTC timestamp of initial state creation/reset>
errors: [<list of error descriptions>]
last_checkpoint: <path or null>
validation_results: <summary or null>
notes: <free-form notes from this iteration>
```

`initialized_at` is set when `state.md` is first created (or reset) and should remain unchanged across later iterations.

---

## 7. Common Error Patterns

| Symptom | Likely Cause | Typical Fix |
|---------|-------------|-------------|
| `CUDA out of memory` | GPU memory exceeded | Reduce batch size, image resolution, or add gradient accumulation |
| `loss=nan` or `event=nan_detected` | Learning rate too high or data issue | Reduce learning rate by 10x, enable gradient clipping |
| Loss increasing over epochs | Overfitting or LR too high | Reduce LR, add regularization |
| `ModuleNotFoundError` | Missing dependency or PYTHONPATH not set | Install (`pip install` / `uv sync`) or add `export PYTHONPATH=$(pwd)` |
| `FileNotFoundError` | Wrong path in config | Check and fix path in config.sh or script |
| `RuntimeError: expected scalar type` | dtype mismatch | Check model dtype vs data dtype |
| `KeyError` in dataset loading | Missing field in metadata | Check metadata format matches code expectations |
| `Connection error` / `HTTP 403` | Model download failed | Check auth token, network, or use local path |
| Process killed without traceback | OOM killer (system level) | Reduce memory usage significantly |
| Training exits without final summary | Crash mid-training | Check last traceback in log |
| `timeout: command not found` | macOS — no GNU `timeout` | Use background process + kill pattern (see Section 12) |

---

## 8. PROMPT.md Anti-Recursion Warning

**CRITICAL**: Every generated PROMPT.md must include this warning near the top:

```
IMPORTANT: Do NOT invoke any skills, modes, or slash commands. Do NOT use the Skill tool.
You are inside a standalone training automation loop — not an interactive session.
```

This prevents the LLM inside the ralph loop from recursively invoking skills or entering interactive modes, which would break the automation.

---

## 9. ADJUSTING Phase Protocol

When in ADJUSTING phase, the LLM acts as a debugger:

**Step 0: Check Known Errors first**
- Before reading any log files, scan the `## Known Errors` section of this PROMPT.md
- If the symptom matches a known error → apply the documented fix immediately, skip Steps 1–2
- This prevents re-investigating already-solved problems and saves iteration turns

**Step 1: Gather evidence**
- Read the FULL error from training.log or validation.log
- Focus on the **last traceback** — the final `Traceback (most recent call last):` block
- Read the **last 50 lines** of the log for context
- Check `ralph/results/last_exit_code` (non-zero = crash)

**Step 2: Identify root cause**
- Read the actual error message, not just the exception type
- Trace back through the call stack to find **where** it originated
- If error is in project code -> fix it directly
- If error is in a library -> check version, args, or environment

**Step 2.5: Check if root cause is in PROMPT.md** (see Section 14)
- If the error is caused by a missing/incorrect template **in PROMPT.md itself**:
  - AND this is the 2nd+ occurrence of the same root cause
  - → Apply targeted fix to `ralph/PROMPT.md` directly (edit the specific template)
  - → Add the error to `## Known Errors` section of PROMPT.md
  - Record: `"iterN PROMPT_FIX: <phase> — <description>"`
  - No action.sh needed for this iteration — the PROMPT.md fix is the action
  - Set phase back to the failed phase for retry
  - Skip Steps 3–4

**Step 3: Apply ONE fix**
- Change only one thing at a time (so you know what fixed it)
- Edit the relevant file (training script, config, source code)
- Write action.sh if an action is needed (e.g., install dependency, clear cache)
- Record in state.md: what the error was and what you changed

**Step 4: Retry**
- If failure originated in SMOKE_TEST, set phase back to SMOKE_TEST (repeat gate)
- Otherwise set phase back to TRAINING (or VALIDATING if that's what failed)

---

## 10. Structured Logging (`[TRAIN]` Events)

If the training script emits structured `[TRAIN]` events, the LLM can parse them for fast diagnostics:

```bash
# Extract structured logs
grep "^\[TRAIN\]" ralph/results/training.log | tail -20

# Key events:
# - event=start: hyperparameters (learning_rate, num_epochs, etc.)
# - event=step: per-step loss and metrics
# - event=epoch_end: per-epoch average loss
# - event=nan_detected: NaN loss detected
# - event=checkpoint: checkpoint saved
# - event=end: final metrics (total_steps, total_time)
```

If no structured logging exists, the LLM should parse raw log output instead (look for loss values, error messages, progress indicators).

---

## 11. Experiment Report (`ralph/results/experiment_report.md`)

During the ANALYZING phase, after writing the summary to state.md, the LLM must generate `ralph/results/experiment_report.md`. The purpose of this document is to record all information needed to reproduce the same experiment at production scale.

### Template

```markdown
# Experiment Report

## Execution Command
(Copy the full execution command from the last successful training action.sh verbatim)

## Key Parameters
| Category | Parameter | Value |
|----------|-----------|-------|
(List all key parameters from config.sh, organized by category)

## Training Results
- Final avg loss, total steps, duration
- NaN/instability occurrences
- Checkpoint path

## Validation Results
- Project-specific validation metric summary
- Validation failure items

## Production Run Guide
- Values to change in config.sh (e.g., set MAX_STEPS="" for unlimited, increase NUM_EPOCHS)
- Ready-to-run command: `bash ralph/run.sh`
```

This template is project-agnostic. The generated PROMPT.md should customize it with project-specific metrics and parameters.

---

## 12. Known Errors Pattern

### What It Is

A `## Known Errors` section in PROMPT.md that documents errors **already confirmed and fixed** during previous iterations. The LLM checks this section first in ADJUSTING phase (Step 0) before any investigation.

### Why It Matters

Without a Known Errors section, the LLM re-investigates the same error every time it recurs — reading logs, checking schemas, searching source files — consuming many turns and risking timeout. With it, a recurring error is fixed in 1 turn.

### Format (include in generated PROMPT.md)

```markdown
## Known Errors (Confirmed + Fixed)

These errors have been observed and resolved. Apply the fix immediately without further investigation.

### E1: `<error message snippet>`
- **Where**: Which command / phase triggers it
- **Cause**: Root cause in one sentence
- **Fix**: Exact fix (command, code change, env var)
- **Status**: ✅ Fixed / ⚠️ Workaround

### E2: ...
```

### macOS Timeout Pattern (always include)

macOS does not ship the GNU `timeout` command. Any action.sh that uses `timeout N cmd` will fail with `timeout: command not found`. Use the background process + kill pattern instead:

```bash
# Instead of: timeout ${TIMEOUT} uv run some-long-command
uv run some-long-command 2>&1 | tee ralph/results/output.log &
CMD_PID=$!
ELAPSED=0; INTERVAL=15
while kill -0 $CMD_PID 2>/dev/null; do
    sleep $INTERVAL
    ELAPSED=$((ELAPSED + INTERVAL))
    if [ $ELAPSED -ge ${TIMEOUT} ]; then
        kill $CMD_PID 2>/dev/null || true
        echo "[timeout] Killed after ${TIMEOUT}s" >> ralph/results/output.log
        break
    fi
done
wait $CMD_PID 2>/dev/null || true
```

Include this as E1 in the Known Errors section of every generated PROMPT.md when the platform may be macOS.

---

## 13. Decision Log (`ralph/results/decisions.md`)

### Purpose

An accumulating log where each iteration appends a structured summary of what was observed, decided, and why. The LLM reads this at the start of every iteration (Step 3 of the iteration protocol) to maintain continuity across iterations — preventing repeated failed approaches and preserving context on what was already tried.

### Location

`ralph/results/decisions.md` — lives in `results/` so it is cleared on `--reset` along with other loop artifacts.

### Entry Format

Each iteration appends one entry:

```markdown
## Iteration {N} — {PHASE}
- **Observed**: {what the LLM saw — key facts from logs, exit codes, state}
- **Decision**: {what action/transition was chosen}
- **Reason**: {why this decision, not alternatives}
- **Evidence**: {must cite concrete artifacts, including exit code and log/artifact path}
- **Action**: {action.sh summary or "LLM-only iteration (no action.sh)"}
```

### Rules

1. **Read before decide**: At the start of every iteration (after reading state.md), read the most recent 15 entries from `decisions.md`. If fewer than 15 exist, read all.
2. **Keyword search fallback**: If repeated failure patterns are suspected and not explained by the recent 15, search older decision entries by keyword before choosing the next action.
3. **Append-only**: Read existing content, then write back with the new entry added at the end
4. **One entry per iteration**: Every iteration must append exactly one entry, even for LLM-only iterations (SETUP, ANALYZING, DONE)
5. **Cleared on `--reset`**: Since the file lives in `ralph/results/`, it is automatically removed when `run.sh --reset` clears the results directory
6. **Concise entries**: Each field should be 1–2 sentences. The log must remain scannable across many iterations
7. **Evidence requirement**: The Evidence field must cite concrete artifacts — at minimum the exit code and the path to the relevant log or artifact file

---

## 14. PROMPT.md Self-Correction Protocol

### Problem

PROMPT.md templates are generated before the loop starts, based on code discovery and specs. Some templates may contain errors (missing environment variables, wrong paths, incomplete phase transition instructions) that only surface at runtime. Without self-correction, the LLM inside the loop cannot fix these template errors — it can only retry with the same broken template, causing repeated failures until a human intervenes.

### Solution: Allow Targeted PROMPT.md Edits

When the LLM detects that a recurring error is caused by an incorrect or incomplete template **in PROMPT.md itself**, it may edit PROMPT.md to fix the template.

### Trigger Conditions

The LLM should modify PROMPT.md when **ALL** of these conditions are true:
1. The same root cause has appeared **2 or more times** (checked via `state.md` errors list)
2. The root cause traces back to a **template or instruction in PROMPT.md** (not external code, data, or infrastructure)
3. The fix is a **targeted edit** to the specific phase template (not a structural redesign)

### Allowed Modifications

| Allowed | Not Allowed |
|---------|-------------|
| Fix missing env vars in templates (`export PYTHONPATH=...`) | Change state machine structure or add new phases |
| Fix incorrect paths or variable names | Rewrite core iteration protocol |
| Add missing instructions to phase transitions | Remove anti-recursion warning |
| Add new entries to `## Known Errors` section | Change `action.sh` canonical rules |
| Fix incorrect schema field references | Restructure the overall document |
| Add fallback logic to templates | Remove existing phases |

### Procedure

1. In ADJUSTING Step 2.5, identify that the root cause is a PROMPT.md template error
2. Apply the targeted fix to `ralph/PROMPT.md` using the Edit tool
3. If the error is likely to recur in future runs, also add it to the `## Known Errors` section
4. Record in `state.md` errors: `"iterN PROMPT_FIX: <phase> — <what was changed>"`
5. Set phase back to the fixed phase for retry
6. Do NOT write an `action.sh` for this iteration — the PROMPT.md fix is the action

### Examples from Real Loops

**Example 1**: RETRIEVE template missing `export PYTHONPATH=$(pwd)` — LLM failed at RETRIEVE_TC, then again at RETRIEVE_T2C with the same `ModuleNotFoundError`. On the 2nd occurrence, LLM should fix ALL RETRIEVE templates in PROMPT.md, not just the current one.

**Example 2**: POLL_T2C transition says "write job_id to state.md" but omits "also write job_id file for next phase's `cat` command". LLM fails at RETRIEVE_T2C because the file doesn't exist. LLM should add the missing file-write instruction AND a fallback (`state.md` grep) to the RETRIEVE template.

### Known Errors Accumulation

When the LLM adds a new entry to `## Known Errors`, it persists across iterations. If the loop is later restarted with `--reset`, the accumulated Known Errors remain in PROMPT.md because `--reset` only clears `ralph/results/` and `ralph/state.md`, not `ralph/PROMPT.md`. This means future runs benefit from past debugging experience.
