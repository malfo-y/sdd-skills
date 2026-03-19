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

프로젝트를 분석하여 자동 디버깅 대상 프로세스를 식별한다. 사용자 요청과 프로젝트 구조에 따라 탐색 전략을 자율적으로 결정한다.

아래 5가지 항목을 파악한다:

| # | 항목 | 목표 | 미발견 시 |
|---|------|------|----------|
| 1 | **Entry Point** | 메인 진입점 (스크립트, 명령, 설정 파일) | → 스킬 종료 |
| 2 | **Verification Step** | 성공 검증 방법 | → CHECKING phase 생략 |
| 3 | **Input/Data Dependencies** | 필요한 입력, 데이터, 외부 의존성 | → 기록 후 진행 |
| 4 | **Output Parsing** | 출력에서 상태 추출 방법 (구조화 로깅 여부) | → raw log 파싱 |
| 5 | **Runtime Environment** | 실행 환경과 명령 (`_sdd/env.md` 우선) | → 프로젝트 파일에서 추론 |

진입점을 읽고 실행 인터페이스(CLI args, config files, env vars)를 파악한다. Step 0에서 읽은 spec이 있으면 코드 탐색 결과와 교차 검증한다.

**Decision Gate 1->2**:
```
entry_point_found = 대상 프로세스 진입점 1개 이상 식별
process_understood = 실행 방법과 검증 방법을 이해함

IF entry_point_found AND process_understood -> Step 2
ELSE IF NOT entry_point_found -> 오류 보고 → 스킬 종료
ELSE -> 부분 탐색 결과로 Step 2 진행, 미확인 항목 표시
```

#### Context Management

| 크기 | 전략 |
|------|------|
| Spec < 500줄 / 코드 < 50파일 | 전체 읽기 |
| Spec 500+ / 코드 50-200 | TOC/Glob 먼저, 타겟만 Read |
| Spec 1000+ / 코드 200+ | 인덱스만, 최대 3개 섹션 |

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

`ralph/` 디렉토리를 생성하고 `ralph/CHECKS.md`를 작성한다. Step 7에서 프로그래밍적으로 검증할 체크리스트다.

```
# Ralph Loop: Acceptance Criteria
Generated: <current UTC timestamp>
Project: <project name>

## config.sh
- [ ] No `<placeholder>` strings remain
- [ ] `LLM_TIMEOUT_SECONDS` and `MAX_LLM_FAILURES` defined
- [ ] PROMPT.md에서 참조하는 모든 변수가 정의됨

## PROMPT.md
- [ ] Anti-recursion warning present
- [ ] SMOKE_TEST phase with repeat gate (ADJUSTING → SMOKE_TEST)
- [ ] Core phases present (reference names or custom names)
- [ ] Main execution command using config.sh variables
- [ ] Known Errors section present
- [ ] action.sh Rules section present
- [ ] Decision log read/write instructions present
- [ ] Self-correction protocol present

## run.sh
- [ ] `--reset` flag, `LLM_TIMEOUT_SECONDS`, DONE detection present

## state.md
- [ ] `phase: SETUP`, `iteration: 0`, valid `initialized_at` timestamp
```

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

### 4.1 Read the Reference

`ralph-loop-concept.md`를 Glob(`**/.claude/skills/ralph-loop-init/references/ralph-loop-concept.md`)으로 찾아 읽는다. State machine, action.sh rules, iteration protocol, error patterns, anti-recursion warning의 원본이다.

> `ralph-loop-concept.md`는 ML 예시 기반이지만 패턴은 범용적이다. 프로젝트에 맞게 phase 이름, 명령, 에러 패턴을 변환하여 활용한다.

### 4.2 Generate the PROMPT.md

레퍼런스의 구조를 기반으로 프로젝트에 맞는 PROMPT.md를 생성한다. LLM이 프로젝트 분석 결과에 따라 내용을 자유롭게 구성하되, 아래 필수 요소를 포함해야 한다:

**필수 요소:**
1. Anti-recursion warning (스킬/슬래시 커맨드 호출 금지)
2. Project Context (config 경로, runtime 명령, verification 경로, results dir)
3. Phase hint block:
   ```
   > Reference phases: SETUP / SMOKE_TEST / EXECUTING / CHECKING / ANALYZING / ADJUSTING / DONE
   > 프로젝트에 맞게 phase 이름 변경/추가/제거 가능
   ```
4. 각 phase별 프로젝트 고유 명령 (config.sh 변수 사용)
5. SMOKE_TEST repeat gate (실패 시 ADJUSTING → SMOKE_TEST 반복)
6. Known Errors section (E1 macOS timeout + Step 1에서 발견한 프로젝트 에러)
7. action.sh Rules (레퍼런스 참조)
8. Decision Log read/write protocol (레퍼런스 참조)
9. Self-correction protocol (PROMPT.md 자체 수정 규칙)

### 4.3 Known Errors

`uname -s`로 플랫폼 감지. Darwin이면 E1(macOS timeout) 포함. Step 1에서 발견한 프로젝트 고유 에러도 추가한다.

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

### 7.1 Verify

`ralph/CHECKS.md`의 각 항목을 `Grep`/`Read`로 검증한다. 각 체크를 ✅ (pass) 또는 ❌ (fail)로 표시하고, 실패 항목은 해당 파일을 수정한 후 재검증한다 (최대 2회).

### 7.2 Update CHECKS.md

검증 완료 후 `ralph/CHECKS.md`의 `[ ]`를 `[x]` (통과) 또는 `[!]` (수정 후 통과)로 업데이트한다.

### 7.3 Summarize

`ralph/results/` 디렉토리를 생성하고(mkdir -p), 사용자에게 요약을 출력한다:

```
Ralph loop initialized (TDD verified)!

Files created:
  ralph/CHECKS.md    — Acceptance criteria (verified ✅)
  ralph/config.sh    — Process configuration (edit before running)
  ralph/PROMPT.md    — LLM instructions for the automation loop
  ralph/run.sh       — Loop controller script
  ralph/state.md     — Initial state (SETUP, iteration 0)
  ralph/results/     — Output directory

Loop phases: SETUP -> SMOKE_TEST -> [execution] -> [checking] -> ANALYZING -> DONE

Next steps:
  1. Review and edit ralph/config.sh
  2. Run: bash ralph/run.sh
  3. Fresh restart: bash ralph/run.sh --reset
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
