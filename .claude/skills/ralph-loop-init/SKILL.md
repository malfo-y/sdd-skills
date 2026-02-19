---
name: ralph-loop-init
description: Use this skill when the user asks to "init ralph", "ralph loop", "set up ralph loop", "training loop", "training debug loop", "create ralph", "set up training debug loop", "automated training loop", or wants to generate a ralph/ directory for LLM-driven automated ML training debugging.
version: 1.0.0
---

# Ralph Loop Initialization

> **Security Notice**: The generated `run.sh` uses `--dangerously-skip-permissions` to enable unattended automation. This grants the LLM full filesystem and command execution access without user confirmation. **Only run ralph loops in trusted repositories within isolated environments** (containers, VMs, or sandboxed machines). Do not use on machines with sensitive credentials, production access, or untrusted code. Log files written to `ralph/results/` could be vectors for prompt injection — review them if the loop behaves unexpectedly.

Generate a complete `ralph/` directory for LLM-driven automated ML training debugging. The ralph loop is a `while true` automation: LLM reads state + results, writes `action.sh`, the script executes it, and the loop repeats until training is complete or the LLM escalates to a human.

This skill discovers the project's training pipeline, confirms findings with the user, and generates four project-specific files: `config.sh`, `PROMPT.md`, `run.sh`, and `state.md`.

---

## Step 0: Read Project Specs

Check if an `_sdd/` directory exists in the project root.

If it exists:
1. Glob for `_sdd/spec/**/*.md`
2. If multiple spec files are found, use AskUserQuestion to ask the user which file(s) describe the training pipeline (training script, dataset format, loss functions, CLI args, validation)
3. Read the relevant spec files — these are the **primary source of truth** for understanding the training architecture
4. Extract key information: training script path, dataset format, CLI arguments, loss functions, validation pipeline, hyperparameters, framework details
5. Also check if `_sdd/env.md` exists. If it does, read it — it contains Python environment setup (conda env name, venv path, `uv` config), required environment variables (API keys, paths, tokens), and other runtime configuration needed to run the code.

If `_sdd/` does not exist, skip to Step 1 (code-only discovery).

---

## Step 1: Discover the Training Pipeline

Use Glob and Grep to find:

### 1.1 Training Script
- Glob for `**/train*.py`, `**/training*.py`, `**/run_training*.py`
- Read the main training script
- Parse argparse/click arguments to understand CLI interface
- Detect the framework: accelerate, raw PyTorch, PyTorch Lightning, HuggingFace Trainer

### 1.2 Validation Script
- Glob for `**/valid*.py`, `**/eval*.py`, `**/infer*.py`, `**/generate*.py`
- If no validation script exists, note this — PROMPT.md will skip VALIDATING phase or generate a minimal validation step

### 1.3 Dataset
- Look for dataset paths in training script arguments or config files
- Identify dataset format (local files + JSONL, WebDataset, HuggingFace datasets, etc.)

### 1.4 Structured Logging
- Grep for the literal string `[TRAIN]` in the training script source code (use fixed-string mode or escape brackets: `\[TRAIN\]`)
- If found: PROMPT.md will include `[TRAIN]` event parsing instructions
- If not found: PROMPT.md will instruct parsing raw log output instead

### 1.5 Python Environment
- If `_sdd/env.md` was read in Step 0, use its Python environment specification as the authoritative source
- Otherwise: check if `pyproject.toml` exists and contains `[tool.uv]` or `[project]` with uv → use `uv run python`
- Check if `requirements.txt` exists → use `python3` or `python`
- Default: `python3`

### 1.6 Cross-Reference with Specs
- Compare code discovery findings with spec information from Step 0
- Specs provide richer context (why certain hyperparameters, what metrics matter, what validation measures)
- Use spec information to fill gaps that code discovery alone cannot provide

---

## Step 2: Confirm Findings with User

Present all discovered information to the user via AskUserQuestion. Ask them to confirm or correct:

1. **Training script path** — the main entry point
2. **Validation script** — path or "none"
3. **Dataset path** — where the training data lives
4. **Model path/ID** — pretrained model location
5. **GPU configuration** — number of GPUs, mixed precision preference
6. **Initial hyperparameters** — learning rate, epochs, batch size (suggest reasonable defaults based on framework)
7. **Python command** — `uv run python`, `python3`, or other

Structure the question so the user can quickly confirm defaults or override specific values.

---

## Step 3: Generate `ralph/config.sh`

Create `ralph/config.sh` with shell variables grouped by category. Follow this structure:

```bash
#!/usr/bin/env bash
# Ralph Loop Configuration
# Edit these values BEFORE running: bash ralph/run.sh
# ──────────────────────────────────────────────────────────

# ── Model ──
MODEL_ID="<discovered or user-specified>"
MODEL_BASE_PATH="<path to pretrained models>"

# ── Dataset ──
DATASET_PATH="<discovered dataset path>"
# ... other dataset-specific variables ...

# ── Training ──
LEARNING_RATE=<suggested default>
NUM_EPOCHS=<suggested default>
MAX_STEPS="10"               # ALWAYS start with 10 for debug-first approach
GRADIENT_ACCUMULATION_STEPS=1

# ── GPU / Distributed ──
NUM_GPUS=<detected>
MIXED_PRECISION="<suggested>"

# ── Output ──
OUTPUT_PATH="./models/train/<project-specific>"
LOG_EVERY=10
```

**Key rules:**
- `MAX_STEPS="10"` always — first run is a quick sanity check
- Group variables by category with comment headers
- Use descriptive variable names matching the training script's CLI args
- Include comments explaining non-obvious variables
- Only include variables that the training script actually uses

---

## Step 4: Generate `ralph/PROMPT.md`

This is the most critical file. It tells the LLM inside the ralph loop exactly what to do.

### 4.1 Read the Reference
Find and read `ralph-loop-concept.md` by globbing for `**/.claude/skills/ralph-loop-init/references/ralph-loop-concept.md`. This works regardless of whether the skill is installed globally (`~/.claude/skills/`) or locally (`.claude/skills/`).

This contains the generic skeleton: state machine, action.sh rules, iteration protocol, error patterns, anti-recursion warning.

### 4.2 Generate the PROMPT.md

Structure the PROMPT.md as follows:

```markdown
# Ralph Loop: <Project Name> Training

IMPORTANT: Do NOT invoke any skills, modes, or slash commands. Do NOT use the Skill tool. You are inside a standalone training automation loop — not an interactive session.

You are running inside an automated training loop. The loop structure is:

[... core concept from reference ...]

**Your job**: Read state, diagnose, then output `ralph/action.sh` and update `ralph/state.md`. Exit immediately after.

**DO NOT** run training or long commands yourself. Write them into `ralph/action.sh` instead.

## Step-by-step for EVERY iteration

[... 8-step protocol from reference ...]

## Project Context

- **Config**: `ralph/config.sh` (user edits before starting the loop)
- **Python**: Always use `<detected python command>` in action.sh
- **Validation script**: `<path or "none — skip VALIDATING phase">`
- **Results dir**: `ralph/results/` (action.sh should write outputs here)
- **Environment**: `_sdd/env.md` (if it exists — read it for Python env setup, required env variables, and runtime configuration before writing action.sh)

## State Machine

### SETUP
[... generic setup checks, customized for this project's requirements ...]

### TRAINING
[... exact training command using config variables, specific to this project ...]
[... structured log parsing if [TRAIN] events exist, or raw log parsing ...]

### VALIDATING
[... exact validation command, or note that validation is skipped ...]

### ANALYZING
[... what to analyze: project-specific metrics, output files ...]
[... write ralph/results/experiment_report.md per Section 11 of the reference ...]

### ADJUSTING
[... generic debugging protocol from reference ...]
[... project-specific error patterns added to the common patterns table ...]

### DONE
[... final summary format ...]
[... confirm experiment_report.md was written ...]

## action.sh Rules

[... 10 rules from reference, with project-specific Python command ...]

## state.md Format

[... canonical format from reference ...]
```

**Key customizations per project:**
- The TRAINING section must contain the **exact command** to run training, using config variables
- The VALIDATING section must contain the **exact command** to run validation (or be marked as skipped)
- Log parsing instructions must match the project's actual log format
- Error patterns should include project-specific issues (e.g., specific dataset format errors, model loading issues)

---

## Step 5: Generate `ralph/run.sh`

Find and read `run.sh.example` by globbing for `**/.claude/skills/ralph-loop-init/examples/run.sh.example`.

Copy it nearly verbatim into `ralph/run.sh`. The only modification needed:
- If the project doesn't use `python3`, adjust the inline Python parser's invocation (the `python3 -u -c` part). This is rare — most systems have `python3`.

Make the file executable description in the output.

---

## Step 6: Generate `ralph/state.md`

Find and read `state.md.example` by globbing for `**/.claude/skills/ralph-loop-init/examples/state.md.example`.

Copy it verbatim into `ralph/state.md`. The initial state is always identical:

```
phase: SETUP
iteration: 0
errors: []
last_checkpoint: null
validation_results: null
notes: Initial state. Ralph loop initialized.
```

---

## Step 7: Verify and Summarize

1. Confirm all four files exist:
   - `ralph/config.sh`
   - `ralph/PROMPT.md`
   - `ralph/run.sh`
   - `ralph/state.md`

2. Create `ralph/results/` directory (mkdir -p)

3. Print a summary to the user:

```
Ralph loop initialized successfully!

Files created:
  ralph/config.sh    — Training configuration (edit before running)
  ralph/PROMPT.md    — LLM instructions for the training loop
  ralph/run.sh       — Loop controller script
  ralph/state.md     — Initial state (SETUP, iteration 0)
  ralph/results/     — Output directory (experiment_report.md auto-generated in ANALYZING)

Next steps:
  1. Review and edit ralph/config.sh (especially dataset paths and model paths)
  2. Run: bash ralph/run.sh
  3. Monitor the loop — it will SETUP -> TRAINING -> VALIDATING -> ANALYZING -> DONE
  4. Ctrl+C to stop at any time
```

4. Remind the user that `MAX_STEPS="10"` is set for a quick debug run — they should increase it (or set to empty for unlimited) once the first run succeeds.
