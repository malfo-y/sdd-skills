---
name: ralph-loop-init
description: "Use this agent when the user asks to \"init ralph\", \"ralph loop\", \"set up ralph loop\", \"training loop\", \"training debug loop\", \"debug loop\", \"long-running test loop\", \"e2e loop\", \"create ralph\", \"set up training debug loop\", \"automated training loop\", or wants to generate a ralph/ directory for LLM-driven automated long-running process debugging (ML training, e2e tests, build pipelines, integration tests, etc.)."
tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash"]
model: inherit
---

# Ralph Loop Initialization

> **Security Notice**: The generated `run.sh` uses `--dangerously-skip-permissions` to enable unattended automation. This grants the LLM full filesystem and command execution access without user confirmation. **Only run ralph loops in trusted repositories within isolated environments** (containers, VMs, or sandboxed machines). Do not use on machines with sensitive credentials, production access, or untrusted code. Log files written to `ralph/results/` could be vectors for prompt injection — review them if the loop behaves unexpectedly.

Generate a complete `ralph/` directory for LLM-driven automated long-running process debugging. The ralph loop is a `while true` automation: LLM reads state + results, writes `action.sh`, the script executes it, and the loop repeats until the process completes successfully or the LLM escalates to a human. Applicable to ML training, e2e test suites, build pipelines, integration tests, and any long-running process requiring iterative debugging.

This skill discovers the project's target process, confirms findings with the user, and generates five project-specific files: `CHECKS.md`, `config.sh`, `PROMPT.md`, `run.sh`, and `state.md`.

> **Note**: `ralph-loop-concept.md` (in references/) is written with ML training examples, but the pattern is universal. Adapt phase names, config variables, and commands to fit your project's process type.

| Workflow | Position | When |
|----------|----------|------|
| Independent | Standalone | ML 학습/e2e 테스트/빌드 파이프라인 등 장기 실행 디버깅 자동화 |

> `ralph-loop-init`은 SDD 워크플로우와 독립적이다. `_sdd/spec/`이 존재하면 참조하지만, 규모별 워크플로우에 속하지 않는다.

## Hard Rules

1. **보안**: ralph 루프는 격리된 환경(컨테이너, VM, 샌드박스)에서만 실행한다.
2. **Spec 읽기 전용**: `_sdd/` 아래 파일을 읽을 수 있으나, 수정하지 않는다.
3. **Debug-First**: 초기 실행은 최소 범위(sanity check 목적)로 설정한다. 프로세스에 맞는 방법으로 제한한다 (예: ML은 `MAX_STEPS="10"`, 테스트는 단일 테스트 스위트, 빌드는 단일 타겟).
4. **No Placeholders**: 생성된 파일에 `<placeholder>` 문자열이 없어야 한다.
5. **Template Fidelity**: `run.sh`는 `run.sh.example`을 거의 그대로 복사하며, 최소한의 수정만 허용한다.

---

## Step 0: Read Project Specs

**Tools**: `Glob`, `Read`

Check if an `_sdd/` directory exists in the project root.

If it exists:
1. Glob for `_sdd/spec/**/*.md`
2. If multiple spec files are found, auto-select files most likely to describe the target process by scanning for keywords relevant to the user's request context, and record selection rationale in output
3. Read the relevant spec files — these are the **primary source of truth** for understanding the target process architecture
4. Extract key information: entry point scripts, input/data format, CLI arguments, verification criteria, key configuration, runtime details
5. Also check if `_sdd/env.md` exists. If it does, read it — it contains runtime environment setup (Python env, Node version, Docker config, etc.), required environment variables (API keys, paths, tokens), and other runtime configuration needed to run the code.

If `_sdd/` does not exist, skip to Step 1 (code-only discovery).

**Decision Gate 0→1**:
```
sdd_exists = Glob("_sdd/") 존재 여부
spec_files = Glob("_sdd/spec/**/*.md") 결과

IF sdd_exists AND spec_files → spec 읽기 후 Step 1 진행
ELSE IF sdd_exists AND NOT spec_files → 경고 출력, Step 1 (코드 기반 탐색)
ELSE → Step 1 (코드 기반 탐색)
```

---

## Step 1: Discover the Target Process

**Tools**: `Glob`, `Grep`, `Read`

Analyze the project to identify the target process that needs automated debugging. The LLM should determine the appropriate discovery strategy based on the user's request and project structure.

### 1.1 Entry Point

Identify the main entry point for the target process:
- **ML training**: `train*.py`, `training*.py`, `run_training*.py`
- **E2E/integration tests**: test config files, `Makefile`, `package.json` scripts, `pytest.ini`
- **Build pipelines**: `Dockerfile`, `Makefile`, build scripts, CI config
- **Other**: Analyze project structure and user context to find the appropriate entry point

Read the main entry point script/config and understand the execution interface (CLI args, config files, environment variables).

### 1.2 Verification Step

Identify how to verify the process succeeded:
- **ML training**: validation/evaluation scripts (`valid*.py`, `eval*.py`, `infer*.py`)
- **E2E tests**: assertion results, test reports
- **Build pipelines**: artifact existence, build logs
- **Other**: Process-specific success criteria

If no verification step exists, note this — PROMPT.md will skip CHECKING phase or generate a minimal verification step.

### 1.3 Input/Data Dependencies

Identify inputs and data dependencies:
- **ML training**: dataset paths, data format (JSONL, WebDataset, HuggingFace datasets, etc.)
- **E2E tests**: test fixtures, seed data, external service dependencies
- **Build pipelines**: source files, dependency manifests, base images
- **Other**: Any required input files, data, or resources

### 1.4 Output Parsing

Determine how to parse process output for status monitoring:
- Check for structured logging (e.g., `[TRAIN] event=step` for ML, JSON test reports for tests)
- If structured logging found: PROMPT.md will include specific parsing instructions
- If not found: PROMPT.md will instruct parsing raw log output

### 1.5 Runtime Environment

**Tools**: `Glob`, `Read`

- If `_sdd/env.md` was read in Step 0, use its environment specification as the authoritative source
- **Python**: check `pyproject.toml` for `[tool.uv]` → `uv run python`; `requirements.txt` → `python3`
- **Node.js**: check `package.json` for scripts; use `npm`, `yarn`, or `pnpm` accordingly
- **Go**: check `go.mod`; use `go run` or `go build`
- **Rust**: check `Cargo.toml`; use `cargo run` or `cargo build`
- **Docker/Make**: check for `Dockerfile`, `Makefile`, `docker-compose.yml`
- Default: infer from project structure

### 1.6 Cross-Reference with Specs
- Compare code discovery findings with spec information from Step 0
- Specs provide richer context (why certain configurations, what metrics matter, what verification criteria apply)
- Use spec information to fill gaps that code discovery alone cannot provide

**Decision Gate 1->2**:
```
entry_point_found = 대상 프로세스 진입점 1개 이상 식별
process_understood = 프로세스의 실행 방법과 검증 방법을 이해함

IF entry_point_found AND process_understood -> Step 2
ELSE IF NOT entry_point_found -> 오류 보고: "대상 프로세스의 진입점을 찾을 수 없습니다. 실행 가능한 스크립트/명령을 확인하세요." → 스킬 종료
ELSE -> 부분 탐색 결과로 Step 2 진행, 미확인 항목 표시
```

#### Context Management

| Spec 크기 | 전략 | 구체적 방법 |
|-----------|------|-------------|
| < 200줄 | 전체 읽기 | `Read`로 전체 파일 읽기 |
| 200-500줄 | 전체 읽기 가능 | `Read`로 전체 읽기, 필요 시 섹션별 |
| 500-1000줄 | TOC 먼저, 관련 섹션만 | 상위 50줄(TOC) 읽기 -> 관련 섹션만 `Read(offset, limit)` |
| > 1000줄 | 인덱스만, 타겟 최대 3개 | 인덱스/TOC만 읽기 -> 타겟 섹션 최대 3개 선택적 읽기 |

| 코드베이스 크기 | 전략 | 구체적 방법 |
|----------------|------|-------------|
| < 50 파일 | 자유 탐색 | `Glob` + `Read` 자유롭게 사용 |
| 50-200 파일 | 타겟 탐색 | `Grep`/`Glob`으로 후보 식별 -> 타겟 `Read` |
| > 200 파일 | 타겟 탐색 | `Grep`/`Glob` 위주 -> 최소한의 `Read` |

---

## Step 2: Present Findings and Auto-Proceed

**Tools**: — (요약 제시, 도구 불필요)

Present all discovered information to the user as a summary table and auto-proceed with discovered values.

분석 결과 요약 테이블을 제시:
| 항목 | 파악 내용 | 상태 |
|------|----------|------|
| 진입점 (Entry Point) | &lt;discovered script/command&gt; | confirmed |
| 검증 단계 (Verification) | &lt;discovered or "미발견"&gt; | confirmed / input needed |
| 입력/데이터 | &lt;discovered inputs&gt; | confirmed |
| 핵심 설정 | &lt;key configuration&gt; | confirmed |
| 런타임 환경 | &lt;detected runtime&gt; | confirmed |
| 초기 파라미터 | &lt;suggested initial params&gt; | confirmed |
| 실행 명령 | &lt;execution command&gt; | confirmed |

Ask the user to confirm or correct:

1. **Entry point** — the main execution script/command
2. **Verification step** — how to verify success, or "none"
3. **Input/data path** — where input data or dependencies live
4. **Key configuration** — essential config values for the process
5. **Runtime environment** — runtime, package manager, etc.
6. **Initial parameters** — conservative initial values for debug-first run (suggest reasonable defaults)
7. **Execution command** — the full command to run the process

Structure the question so the user can quickly confirm defaults or override specific values.

**Decision Gate 2->2.5**:
```
findings_presented = 분석 결과 요약 테이블 제시 완료

IF findings_presented -> Step 2.5 진행 (사용자 확인을 기다리지 않는다)
```

---

## Step 2.5: Write `ralph/CHECKS.md`

**Tools**: `Bash (mkdir -p)`, `Write`

Before generating any files, create `ralph/` directory and write `ralph/CHECKS.md`.
This document defines acceptance criteria for each generated file — 자동 검증용 체크리스트로, Step 7에서 프로그래밍적으로 검증한다.
It is written first so generation targets are explicit before code is produced.

Content to write:

---
```
# Ralph Loop: Acceptance Criteria
Generated: <current UTC timestamp>
Project: <project name>

## config.sh
- [ ] No `<placeholder>` strings remain (no `<...>` literals)
- [ ] `LLM_TIMEOUT_SECONDS` is defined
- [ ] `MAX_LLM_FAILURES` is defined
- [ ] Every variable referenced in PROMPT.md's execution command is defined here
- [ ] Variable names match the project's actual configuration names

## PROMPT.md
- [ ] Anti-recursion warning present near the top
- [ ] `SMOKE_TEST` phase defined between `SETUP` and the main execution phase
  - [ ] `SMOKE_TEST` runs a minimal/quick version of the target process
  - [ ] Pass criteria stated: exit code 0 AND output contains expected indicator
  - [ ] On PASS → transitions to main execution phase
  - [ ] On FAIL → transitions to `ADJUSTING` with "SMOKE_TEST failed: <error>"
  - [ ] If failure originated in SMOKE_TEST, ADJUSTING sends phase back to `SMOKE_TEST` (repeat gate)
- [ ] Core phases present (reference names or project-appropriate custom names)
- [ ] Main execution section contains exact command using `config.sh` variables
- [ ] Verification/checking section contains exact command or explicit skip notice
- [ ] `## Known Errors` section present (E1 macOS timeout included if applicable)
- [ ] `## action.sh Rules` section present
- [ ] `SMOKE_TEST` explicitly states minimal execution as the only allowed hardcoded exception
- [ ] PROMPT.md self-correction protocol present in ADJUSTING section (Step 2.5 or dedicated subsection)

## decisions.md
- [ ] PROMPT.md instructs LLM to read the most recent 15 entries from `ralph/results/decisions.md` each iteration (after state.md)
- [ ] PROMPT.md instructs LLM to append to `ralph/results/decisions.md` each iteration (after updating state.md)
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

**Tools**: `Read`, `Write`

Create `ralph/config.sh` with shell variables grouped by category. The LLM generates project-appropriate variables based on the target process type.

**Fixed variables** (always present):
```bash
#!/usr/bin/env bash
# Ralph Loop Configuration
# Edit these values BEFORE running: bash ralph/run.sh
# ──────────────────────────────────────────────────────────

# ── Loop Safety (fixed) ──
LLM_TIMEOUT_SECONDS=600  # max seconds for one LLM turn (0 disables timeout)
MAX_LLM_FAILURES=3       # consecutive LLM failures before abort
```

**Project-specific variables** (LLM generates based on discovered process):

The LLM should add variables appropriate for the project type. Examples:

```bash
# ── ML Training Example ──
# MODEL_ID="<model name>"
# DATASET_PATH="<dataset path>"
# LEARNING_RATE=5e-5
# NUM_EPOCHS=3
# MAX_STEPS="10"                # debug-first: start small
# GRADIENT_ACCUMULATION_STEPS=1
# NUM_GPUS=1
# MIXED_PRECISION="fp16"
# OUTPUT_PATH="./models/train/<project>"

# ── E2E Test Example ──
# TEST_SUITE="<test suite path>"
# TEST_CONFIG="<config path>"
# PARALLEL_WORKERS=1            # debug-first: single worker
# TIMEOUT_PER_TEST=60

# ── Build Pipeline Example ──
# BUILD_TARGET="<target>"
# BUILD_CONFIG="debug"          # debug-first: debug build
# ARTIFACT_PATH="./build/output"
```

**Key rules:**
- `LLM_TIMEOUT_SECONDS` and `MAX_LLM_FAILURES` are always present
- Set initial parameters conservatively for debug-first approach
- Group variables by category with comment headers
- Use descriptive variable names matching the project's actual configuration
- Include comments explaining non-obvious variables
- Only include variables that the target process actually uses

---

## Step 4: Generate `ralph/PROMPT.md`

**Tools**: `Glob`, `Read`, `Write`

This is the most critical file. It tells the LLM inside the ralph loop exactly what to do.

### 4.1 Read the Reference
Find and read `ralph-loop-concept.md` by globbing for `**/.claude/skills/ralph-loop-init/references/ralph-loop-concept.md`. This works regardless of whether the skill is installed globally (`~/.claude/skills/`) or locally (`.claude/skills/`).

This contains the generic skeleton: state machine, action.sh rules, iteration protocol, error patterns, anti-recursion warning.

> **Note**: `ralph-loop-concept.md` uses ML training examples, but the pattern applies to any long-running process. Adapt phase names, commands, and error patterns to fit the project's process type.

### 4.2 Generate the PROMPT.md

Structure the PROMPT.md as follows:

```markdown
# Ralph Loop: <Project Name>

IMPORTANT: Do NOT invoke any skills, modes, or slash commands. Do NOT use the Skill tool. You are inside a standalone automation loop — not an interactive session.

You are running inside an automated process debugging loop. The loop structure is:

[... core concept from reference ...]

**Your job**: Read state, diagnose, then output `ralph/action.sh` and update `ralph/state.md`. Exit immediately after.

**DO NOT** run long commands yourself. Write them into `ralph/action.sh` instead.

## Step-by-step for EVERY iteration

[... iteration protocol from reference, including reading the most recent 15 entries from decisions.md after state.md and appending to decisions.md after updating state.md ...]

## Project Context

- **Config**: `ralph/config.sh` (user edits before starting the loop)
- **Runtime**: Always use `<detected runtime command>` in action.sh
- **Verification**: `<path or "none — skip CHECKING phase">`
- **Results dir**: `ralph/results/` (action.sh should write outputs here)
- **Environment**: `_sdd/env.md` (if it exists — read it for runtime env setup, required env variables, and runtime configuration before writing action.sh)

## State Machine

> Reference phases: SETUP / SMOKE_TEST / EXECUTING / CHECKING / ANALYZING / ADJUSTING / DONE
> EXECUTING = main process (training, testing, building, etc.)
> CHECKING = result verification (validation, assertion, artifact checking)
> Customize phase names to fit your project (e.g., TRAINING instead of EXECUTING, VALIDATING instead of CHECKING).

### SETUP
[... generic setup checks, customized for this project's requirements ...]

### SMOKE_TEST

**Purpose**: Verify the target process runs end-to-end before committing to full execution.

Write `action.sh` to:
1. Run a minimal/quick version of the target process (e.g., ML: 1 training step; tests: single test; build: minimal target)
2. Save output to `ralph/results/smoke_test.log` (use `2>&1 | tee`)
3. After the run, check the log for a success indicator appropriate to the process type

**Acceptance criteria** (BOTH must pass):
- Exit code = 0
- `ralph/results/smoke_test.log` contains at least one expected output indicator

On PASS → set phase to the main execution phase in state.md
On FAIL → set `phase: ADJUSTING` in state.md, note "SMOKE_TEST failed: <first error from log>"

**Repeat gate rule**:
- If ADJUSTING fixes a failure that originated in SMOKE_TEST, set phase back to `SMOKE_TEST` and rerun the smoke test.
- Do not transition to the main execution phase until SMOKE_TEST passes.

[Note: The minimal execution in SMOKE_TEST is hardcoded in action.sh — it does not use the full-scale parameters from config.sh. This is the only intentional hardcoded-value exception to the general config-variable rule. SMOKE_TEST is a repeat gate: after ADJUSTING fixes a smoke failure, return to SMOKE_TEST until it passes.]

### <Main Execution Phase> (e.g., TRAINING, EXECUTING, TESTING, BUILDING)
[... exact execution command using config variables, specific to this project ...]
[... structured log parsing if available, or raw log parsing ...]

### <Verification Phase> (e.g., VALIDATING, CHECKING)
[... exact verification command, or note that verification is skipped ...]
- Before generating a new verification action, check if existing output already determines pass/fail.
- If verification action exit code is `0` but required output is still missing, transition to `ADJUSTING` (root cause: output-not-produced) instead of repeating the same action indefinitely.

### ANALYZING
[... what to analyze: project-specific metrics, output files ...]
[... write ralph/results/experiment_report.md per Section 11 of the reference ...]

### ADJUSTING
[... generic debugging protocol from reference, including Step 2.5 for PROMPT.md self-correction ...]
[... project-specific error patterns added to the common patterns table ...]

### PROMPT.md Self-Correction (Section 14 of reference)

When a recurring error (2+ occurrences) traces back to an incorrect template in this PROMPT.md:
1. Fix the template directly using the Edit tool
2. Add the error to `## Known Errors` section
3. Record `"iterN PROMPT_FIX: <phase> — <description>"` in state.md errors
4. No action.sh needed — set phase back to the failed phase for retry

Allowed: fix env vars, paths, variable names, phase transition instructions, add Known Errors.
Not allowed: change state machine structure, remove phases, rewrite core protocol.

### DONE
[... final summary format ...]
[... confirm experiment_report.md was written ...]

## action.sh Rules

[... 10 rules from reference, with project-specific runtime command ...]

## Decision Log

After updating `ralph/state.md`, append a decision entry to `ralph/results/decisions.md`.

### Format

Each iteration, append exactly one entry:

    ## Iteration {N} — {PHASE}
    - **Observed**: {what you saw — key facts from logs, exit codes, state}
    - **Decision**: {what action/transition you chose}
    - **Reason**: {why this decision, not alternatives}
    - **Evidence**: {must cite concrete artifacts, including exit code and log/artifact path}
    - **Action**: {action.sh summary or "LLM-only iteration (no action.sh)"}

### Rules
- Read the most recent 15 entries from `ralph/results/decisions.md` at the start of every iteration (after state.md). If fewer than 15 exist, read all.
- If repeated failure patterns are suspected and not explained by the recent 15, search older decision entries by keyword before choosing the next action.
- Append-only: read existing content, write back with new entry at the end
- One entry per iteration, even for LLM-only iterations (SETUP, ANALYZING, DONE)
- Keep each field to 1–2 sentences

## state.md Format

[... canonical format from reference ...]
```

**Key customizations per project:**
- The SMOKE_TEST section must enforce repeat-gate behavior (`ADJUSTING -> SMOKE_TEST` for smoke-origin failures)
- The SMOKE_TEST section must call out the minimal execution as an explicit exception to the no-hardcoding rule
- The main execution section must contain the **exact command** to run the process, using config variables
- The verification section must contain the **exact command** to verify results (or be marked as skipped), plus artifact-driven transition rules to prevent infinite loops
- Log/output parsing instructions must match the project's actual output format
- Error patterns should include project-specific issues

### 4.3 Generate `## Known Errors` Section in PROMPT.md

After the ADJUSTING section, add a `## Known Errors (Confirmed + Fixed)` section following the format in Section 12 of the reference.

**플랫폼 감지**: `uname -s` 결과 확인. Darwin이면 E1을 포함하고, Linux면 E1을 reference only로 포함한다.

**Always include E1 (macOS timeout)** if the environment is or may be macOS (Darwin):

```markdown
### E1: `timeout: command not found`
- **Where**: Any action.sh using `timeout N cmd`
- **Cause**: macOS does not ship GNU `timeout`
- **Fix**: Use background process + kill pattern (see reference Section 12)
- **Status**: ✅ Use pattern from Section 12 whenever timeout is needed
```

**Add project-specific errors** discovered during Step 1 (code discovery):
- If the project imports packages from sibling directories (not in the runtime environment), add a path/import error entry
- If the project requires specific directories to exist at runtime, add a missing-directory entry
- If there are known schema or API compatibility issues from spec/README, add them

The LLM inside the ralph loop checks this section first in ADJUSTING (Step 0 of the ADJUSTING protocol), so pre-populating it with anticipated errors reduces investigation turns significantly.

---

## Step 5: Generate `ralph/run.sh`

**Tools**: `Read`, `Write`, `Bash (chmod +x)`

Find and read `run.sh.example` by globbing for `**/.claude/skills/ralph-loop-init/examples/run.sh.example`.

Copy it nearly verbatim into `ralph/run.sh`. The only modification needed:
- If the project doesn't use `python3`, adjust the inline Python parser's invocation (the `python3 -u -c` part). This is rare — most systems have `python3`.

Keep the template's CLI behavior:
- `bash ralph/run.sh` resumes from current `state.md`/`results`.
- `bash ralph/run.sh --reset` clears prior loop artifacts (`ralph/results/`, stale `ralph/action.sh`) and rewrites `ralph/state.md` to the initial SETUP state with a fresh `initialized_at` UTC timestamp before starting.
- Source `ralph/config.sh` and apply `LLM_TIMEOUT_SECONDS` to each LLM planning turn (default 600 seconds, `0` disables timeout).

Make the file executable description in the output.

---

### Step 5.5: 핵심 파일 확인 (Checkpoint)

**Tools**: — (요약 제시, 도구 불필요)

config.sh, PROMPT.md, run.sh 생성 후 요약 테이블을 제시하고 바로 Step 6으로 진행한다 (사용자 확인을 기다리지 않는다):

| 항목 | 내용 |
|------|------|
| config.sh 변수 | N개 설정 |
| PROMPT.md 섹션 | Known Errors, Phases, ... |
| run.sh 구조 | 루프 + LLM 호출 + 검증 |

---

## Step 6: Generate `ralph/state.md`

**Tools**: `Write`, `Bash (date -u)`

Find and read `state.md.example` by globbing for `**/.claude/skills/ralph-loop-init/examples/state.md.example`.

Copy it into `ralph/state.md`, then replace `__INITIALIZED_AT_UTC__` with the current UTC timestamp (`date -u '+%Y-%m-%dT%H:%M:%SZ'`). The initial structure is:

```
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

**Tools**: `Grep`, `Read`, `Edit`

### 7.1 Verify Each File Against Its Criteria

For each criterion in `ralph/CHECKS.md`, perform a targeted check:

**config.sh**:
- Check for remaining placeholders: `<[a-zA-Z_][a-zA-Z0-9_]*>` 패턴 매칭 — expect 0 occurrences
- Check `LLM_TIMEOUT_SECONDS` is defined
- Check `MAX_LLM_FAILURES` is defined
- Check every variable referenced in PROMPT.md's execution command is defined in config.sh
- Check variable names align with project configuration names

**PROMPT.md**:
- Check anti-recursion warning: grep for `Do NOT invoke`
- Check SMOKE_TEST phase: grep for `SMOKE_TEST`
- Check SMOKE_TEST minimal execution rule: confirm smoke test uses a minimal/quick execution
- Check SMOKE_TEST pass criteria: grep for both `Exit code = 0` and expected output indicator
- Check SMOKE_TEST repeat gate: confirm `ADJUSTING -> SMOKE_TEST` behavior is written
- Check core phases present: confirm SETUP, SMOKE_TEST, a main execution phase, ANALYZING, ADJUSTING, DONE exist (using reference names or project-appropriate custom names)
- Check main execution section includes exact command using config variables
- Check verification section includes exact command or explicit skip
- Check Known Errors section: grep for `## Known Errors`
- Check action.sh Rules section: grep for `## action.sh Rules`
- Check PROMPT.md self-correction: grep for `PROMPT_FIX` or `Self-Correction` or `self-correction`
- Check PROMPT.md contains decision log reading instruction with recent-15 scope: grep for `most recent 15` and `decisions.md`
- Check PROMPT.md contains decision log writing/append instruction: grep for `decisions.md` in the post-state-update steps
- Check decision format includes evidence artifacts: grep for `**Evidence**`, `exit code`, and `log/artifact path`

**run.sh**:
- Check `--reset` flag: grep for `--reset`
- Check `LLM_TIMEOUT_SECONDS`: grep for `LLM_TIMEOUT_SECONDS`
- Check DONE phase detection: grep for `phase: DONE` or equivalent

**state.md**:
- Check phase: grep for `^phase: SETUP`
- Check iteration: grep for `^iteration: 0`
- Check no placeholder: confirm `__INITIALIZED_AT_UTC__` is NOT in the file

Mark each check ✅ (pass) or ❌ (fail) in the output. If any criterion fails, fix the
generated file before proceeding.

### 7.2 Update CHECKS.md with Results

After verification, update `ralph/CHECKS.md` — replace `[ ]` with `[x]` for passing
criteria and `[!]` for failing ones (with a note on what was wrong and how it was fixed).

### 7.3 Create results directory and Summarize

Create `ralph/results/` directory (mkdir -p), then print summary to user:

```
Ralph loop initialized (TDD verified)!

Files created:
  ralph/CHECKS.md    — Acceptance criteria (all criteria verified ✅)
  ralph/config.sh    — Process configuration (edit before running)
  ralph/PROMPT.md    — LLM instructions for the automation loop
  ralph/run.sh       — Loop controller script
  ralph/state.md     — Initial state (SETUP, iteration 0)
  ralph/results/     — Output directory

Loop phases: SETUP -> SMOKE_TEST -> [execution] -> [checking] -> ANALYZING -> DONE

Next steps:
  1. Review and edit ralph/config.sh (especially paths and key parameters)
  2. Resume run: bash ralph/run.sh
  3. Fresh restart (clear old outputs): bash ralph/run.sh --reset
  4. The loop will SMOKE_TEST (minimal run) before full execution
  5. Ctrl+C to stop at any time
```

---

## Progressive Disclosure (완료 시)

```
완료 요약 테이블과 함께 전체 정보를 바로 출력한다 (사용자 확인을 기다리지 않는다):

1. 완료 요약 테이블 제시:
   | 항목 | 내용 |
   |------|------|
   | 생성 파일 | 5개 + results/ |
   | CHECKS.md 상태 | N/N 통과 |
   | 프로세스 타입 | <detected type> |
   | Phase 구성 | SETUP -> SMOKE_TEST -> [execution] -> ... -> DONE |

2. PROMPT.md 핵심 섹션 요약 출력

3. config.sh 변수 목록 출력
```

---

## Error Handling

| 상황 | 대응 |
|------|------|
| 대상 프로세스 진입점 미발견 | 오류 보고 후 스킬 종료 (실행 가능한 스크립트/명령 확인 안내) |
| `_sdd/spec` 디렉토리 미존재 | 코드 기반 탐색으로 진행, 사용자에게 경고 |
| `ralph-loop-concept.md` 참조 파일 미발견 | 오류: 스킬 설치 불완전, 메시지와 함께 중단 |
| `run.sh.example` 참조 파일 미발견 | 오류: 스킬 설치 불완전, 메시지와 함께 중단 |
| 사용자 미확인 (2+ 라운드) | 부분 탐색 결과 저장, 수동 설정 안내 |
| CHECKS.md 검증 실패 (Step 7) | 실패 파일 수정, 재검증 (최대 2라운드) |
| 복수 진입점 발견 | 가장 유력한 진입점 자동 선택 (파일명/구조 분석 기반), 판단 근거를 출력에 기록 |
| 프로세스 타입 감지 모호 | 사용자 요청 컨텍스트와 프로젝트 구조 분석으로 자동 선택, 판단 근거를 출력에 기록 |
