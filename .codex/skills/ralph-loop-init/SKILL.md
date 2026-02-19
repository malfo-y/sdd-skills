---
name: ralph-loop-init
description: Use this skill when the user asks to "init ralph", "ralph loop", "set up ralph loop", "training loop", "training debug loop", "create ralph", "set up training debug loop", "automated training loop", or wants to generate a `ralph/` directory for Codex-driven automated ML training debugging.
---

# Ralph Loop Initialization (Codex)

> **Security Notice**: The generated `run.sh` uses `codex exec --dangerously-bypass-approvals-and-sandbox` for unattended automation. This grants full filesystem and command execution access with no interactive confirmation. Only run ralph loops in trusted repositories inside isolated environments (container, VM, dedicated sandbox machine). Do not run on hosts with sensitive credentials or production access.

Generate a complete `ralph/` directory for Codex-driven automated ML training debugging.
The ralph loop is a `while true` automation: Codex reads state and results, writes `action.sh`, the script executes it, and the loop repeats until training is complete or escalation is required.

This skill discovers the project training pipeline, confirms findings with the user, and generates four project-specific files:
`config.sh`, `PROMPT.md`, `run.sh`, and `state.md`.

---

## Step 0: Read Project Specs

Check whether `_sdd/` exists in the project root.

If it exists:
1. Locate `_sdd/spec/**/*.md`.
2. If multiple candidates exist, ask the user directly which files define the training pipeline.
3. Read relevant spec files as the primary source of truth for architecture intent.
4. Extract key data: training entrypoint, dataset format, CLI args, loss, validation flow, hyperparameters, framework constraints.

If `_sdd/` does not exist, continue with code-only discovery.

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
```

Key rules:
- Keep `MAX_STEPS="10"` for the first run.
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
[... 8-step protocol from reference ...]

## Project Context
- Config: `ralph/config.sh`
- Python command: `<detected python command>`
- Validation script: `<path or none>`
- Results dir: `ralph/results/`

## State Machine
### SETUP
[... project checks ...]
### TRAINING
[... exact training command with config vars ...]
### VALIDATING
[... exact validation command or skipped ...]
### ANALYZING
[... project-specific metrics analysis ...]
[... write ralph/results/experiment_report.md per Section 11 of the reference ...]
### ADJUSTING
[... debugging protocol + project-specific error patterns ...]
### DONE
[... final summary format ...]
[... confirm experiment_report.md was written ...]

## action.sh Rules
[... 10 rules from reference, customized python command ...]

## state.md Format
[... canonical format from reference ...]
```

Required project-specific customizations:
- Exact training command using `config.sh` variables
- Exact validation command (or explicit skip)
- Log parsing instructions matching actual log format
- Project-specific error patterns

---

## Step 5: Generate `ralph/run.sh`

Find and read template by globbing:
- `**/.codex/skills/ralph-loop-init/examples/run.sh.example`

Copy nearly verbatim into `ralph/run.sh`.
Adjust only if `python3` is unavailable for the inline JSON parser.

The template uses `codex exec --json` and a retry-on-failure guard for Codex step failures.

Mark executable:
- `chmod +x ralph/run.sh`

---

## Step 6: Generate `ralph/state.md`

Find and read template by globbing:
- `**/.codex/skills/ralph-loop-init/examples/state.md.example`

Copy verbatim into `ralph/state.md`:

```yaml
phase: SETUP
iteration: 0
errors: []
last_checkpoint: null
validation_results: null
notes: Initial state. Ralph loop initialized.
```

---

## Step 7: Verify and Summarize

1. Verify files exist:
   - `ralph/config.sh`
   - `ralph/PROMPT.md`
   - `ralph/run.sh`
   - `ralph/state.md`
2. Ensure `ralph/results/` exists.
3. Print concise summary:
   - files created
   - `ralph/results/` directory (experiment_report.md auto-generated in ANALYZING)
   - run command: `bash ralph/run.sh`
   - phase flow: `SETUP -> TRAINING -> VALIDATING -> ANALYZING -> DONE`
4. Remind user `MAX_STEPS="10"` is only for first debug run.
