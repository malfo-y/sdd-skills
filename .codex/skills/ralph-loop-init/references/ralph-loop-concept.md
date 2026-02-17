# Ralph Loop: Architecture Reference

This document describes the architecture of a ralph loop -- a Codex-driven automated ML training debugger. Use this as a reference when generating project-specific `ralph/PROMPT.md` files.

---

## 1. Core Concept

```
while true:
    Phase 1: Codex reads state + results -> writes action.sh
    Phase 2: run.sh executes action.sh (training, validation — may take hours)
    repeat until phase = DONE
```

The Codex agent's job: Read state, diagnose, then output `ralph/action.sh` and update `ralph/state.md`. Exit immediately after.

The Codex agent must **never** run training or long commands itself. It writes them into `ralph/action.sh` instead.

---

## 2. Directory Structure

```
ralph/
├── PROMPT.md       <- Codex instruction document (state machine, log parsing guide)
├── config.sh       <- User-editable parameters (project-specific)
├── run.sh          <- Loop controller (Codex -> action.sh -> repeat)
├── action.sh       <- Codex-generated execution script (each iteration)
├── state.md        <- Current phase, iteration, errors, checkpoint path, notes
└── results/        <- Training/validation logs and outputs
    ├── training.log
    ├── last_exit_code
    ├── last_checkpoint_path
    ├── validation.log
    ├── validation_output/
    └── codex_iter{N}.json <- Codex JSONL event log (for debugging)
```

---

## 3. State Machine

```
SETUP -> TRAINING -> VALIDATING -> ANALYZING -> DONE
              \-> ADJUSTING ->/         ->/
                    ^ (retry)
```

| Phase | Role | action.sh | Next Phase |
|-------|------|-----------|------------|
| **SETUP** | Verify environment (dataset, scripts, GPU) | Not needed (Codex checks only) | TRAINING |
| **TRAINING** | Execute training | Training script + log capture | VALIDATING (success) / ADJUSTING (failure) |
| **VALIDATING** | Run validation/inference | Validation script | ANALYZING (success) / ADJUSTING (failure) |
| **ANALYZING** | Analyze results + summarize | Not needed (Codex analysis only) | DONE |
| **ADJUSTING** | Diagnose error + apply fix | Fix action (optional) | TRAINING / VALIDATING (retry) |
| **DONE** | Final summary | Not needed | — |

### Transition Rules

- **SETUP -> TRAINING**: Environment verified (dataset exists, training script exists, GPU available)
- **TRAINING -> VALIDATING**: exit code 0 + checkpoint exists
- **TRAINING -> ADJUSTING**: exit code != 0, or NaN detected, or training anomaly
- **VALIDATING -> ANALYZING**: Validation output files generated and non-trivial (>10KB)
- **VALIDATING -> ADJUSTING**: Validation failed
- **ANALYZING -> DONE**: Analysis complete, summary written
- **ADJUSTING -> TRAINING**: Fix applied, retry training
- **ADJUSTING -> VALIDATING**: Fix applied, retry validation

### Escalation Rules

- Same root cause fails **3 times** -> set phase to DONE with note "STUCK: {error description}. Human intervention needed."
- Error cannot be diagnosed (no traceback, no clear cause) -> set phase to DONE with note "UNKNOWN ERROR: {last 10 lines of log}. Human intervention needed."
- Error requires external action (API key, hardware change, data corruption) -> set phase to DONE with explanation

---

## 4. Eight-Step Iteration Protocol

Every iteration, the Codex agent must follow these steps in order:

1. Read `ralph/config.sh` (user-specified parameters)
2. Read `ralph/state.md` (current phase, errors, notes)
3. Read `ralph/results/last_exit_code` if it exists (was previous action successful?)
4. Read any result files relevant to the current phase
5. Decide what to do next
6. Write `ralph/action.sh` with the next action (or skip if agent-only iteration)
7. Update `ralph/state.md` (always increment iteration, update phase/notes)
8. Exit

---

## 5. action.sh Canonical Rules

Every `action.sh` must follow these 10 rules:

1. Always start with `#!/usr/bin/env bash` and `set -euo pipefail`
2. Always `source ralph/config.sh` to load user-specified parameters
3. Always `mkdir -p ralph/results` at the top
4. Always `export PYTHONUNBUFFERED=1` (flush output immediately, prevents lost logs on crash)
5. Always `export TQDM_DISABLE=1` for training scripts (suppress tqdm noise)
6. Use config variables (`${LEARNING_RATE}`, `${NUM_EPOCHS}`, etc.) — never hardcode values
7. Save all outputs to `ralph/results/` so Codex can read them next iteration
8. Use `2>&1 | tee ralph/results/<name>.log` to capture stdout+stderr
9. Keep it simple — one logical action per script
10. Use the correct Python command for the project (e.g., `uv run python`, `python3`, etc.)

---

## 6. state.md Canonical Format

```
phase: <SETUP|TRAINING|VALIDATING|ANALYZING|ADJUSTING|DONE>
iteration: <number>
errors: [<list of error descriptions>]
last_checkpoint: <path or null>
validation_results: <summary or null>
notes: <free-form notes from this iteration>
```

---

## 7. Common Error Patterns

| Symptom | Likely Cause | Typical Fix |
|---------|-------------|-------------|
| `CUDA out of memory` | GPU memory exceeded | Reduce batch size, image resolution, or add gradient accumulation |
| `loss=nan` or `event=nan_detected` | Learning rate too high or data issue | Reduce learning rate by 10x, enable gradient clipping |
| Loss increasing over epochs | Overfitting or LR too high | Reduce LR, add regularization |
| `ModuleNotFoundError` | Missing dependency | Install the package (`pip install` / `uv sync`) |
| `FileNotFoundError` | Wrong path in config | Check and fix path in config.sh or script |
| `RuntimeError: expected scalar type` | dtype mismatch | Check model dtype vs data dtype |
| `KeyError` in dataset loading | Missing field in metadata | Check metadata format matches code expectations |
| `Connection error` / `HTTP 403` | Model download failed | Check auth token, network, or use local path |
| Process killed without traceback | OOM killer (system level) | Reduce memory usage significantly |
| Training exits without final summary | Crash mid-training | Check last traceback in log |

---

## 8. PROMPT.md Anti-Recursion Warning

**CRITICAL**: Every generated PROMPT.md must include this warning near the top:

```
IMPORTANT: Do NOT invoke skills, modes, slash commands, or automation directives.
Do NOT start nested Codex sessions (`codex`, `codex exec`, etc.).
You are inside a standalone training automation loop, not an interactive session.
```

This prevents the model inside the ralph loop from recursively launching nested agent sessions, which would break the automation.

---

## 9. ADJUSTING Phase Protocol

When in ADJUSTING phase, Codex acts as a debugger:

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

**Step 3: Apply ONE fix**
- Change only one thing at a time (so you know what fixed it)
- Edit the relevant file (training script, config, source code)
- Write action.sh if an action is needed (e.g., install dependency, clear cache)
- Record in state.md: what the error was and what you changed

**Step 4: Retry**
- Set phase back to TRAINING (or VALIDATING if that's what failed)

---

## 10. Structured Logging (`[TRAIN]` Events)

If the training script emits structured `[TRAIN]` events, Codex can parse them for fast diagnostics:

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

If no structured logging exists, Codex should parse raw log output instead (look for loss values, error messages, progress indicators).
