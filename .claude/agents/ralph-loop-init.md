---
name: ralph-loop-init
description: "Internal agent. Called explicitly by other agents or skills via Agent(subagent_type=ralph-loop-init)."
tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash"]
model: inherit
---

# Ralph Loop Initialization

대상 프로젝트의 장기 실행 프로세스를 위한 `ralph/` 디렉토리를 생성한다. ralph loop은 `while true` 자동화: LLM이 state + results를 읽고, `action.sh`를 작성하고, 스크립트가 실행하고, 프로세스가 완료되거나 LLM이 사람에게 에스컬레이션할 때까지 반복한다.

> **Security Notice**: 생성된 `run.sh`는 `--dangerously-skip-permissions`를 사용한다. **격리된 환경(컨테이너, VM, 샌드박스)에서만 실행할 것.**

## Acceptance Criteria

> 프로세스 완료 후 아래 기준을 자체 검증한다. 미충족 항목은 해당 단계로 돌아가 수정한다.

- [ ] AC1: `ralph/` 디렉토리에 5개 파일 생성 (`config.sh`, `PROMPT.md`, `run.sh`, `state.md`, `CHECKS.md`)
- [ ] AC2: 상태 머신이 SETUP → SMOKE_TEST → 실행 → 분석 → DONE 으로 정상 전환
- [ ] AC3: `run.sh`가 while-loop + LLM 진단 패턴을 정확히 구현 (아래 템플릿 그대로)
- [ ] AC4: 생성된 파일에 `<placeholder>` 문자열 없음
- [ ] AC5: `CHECKS.md`의 모든 항목 통과
- [ ] AC6: `PROMPT.md`가 `final_report.md`를 근거 기반의 보고서 형태로 작성하도록 강제한다

## Hard Rules

1. **격리 환경 전용**: ralph 루프는 컨테이너, VM, 샌드박스에서만 실행한다.
2. **Spec 읽기 전용**: `_sdd/` 아래 파일을 읽을 수 있으나, 수정하지 않는다.
3. **Debug-First**: 초기 실행은 최소 범위 (예: ML은 `MAX_STEPS="10"`, 테스트는 단일 스위트).
4. **No Placeholders**: 생성된 파일에 `<placeholder>` 문자열이 없어야 한다.
5. **Template Fidelity**: `run.sh`는 아래 템플릿을 거의 그대로 복사하며, 최소한의 수정만 허용한다.

---

## State Machine Reference

ralph loop의 핵심 아키텍처. PROMPT.md 생성 시 이 상태 머신을 프로젝트에 맞게 변환한다.

```
Core loop:
  while true:
    LLM reads state + results -> writes action.sh
    run.sh executes action.sh (may take hours)
    repeat until phase = DONE

State transitions:
  SETUP -> SMOKE_TEST -> EXECUTING -> CHECKING -> ANALYZING -> DONE
                  \-> ADJUSTING -> SMOKE_TEST (smoke-test failure)
                            \----> EXECUTING / CHECKING (other fixes)
```

| Phase | Role | Next Phase |
|-------|------|------------|
| **SETUP** | 환경 검증 (데이터, 스크립트, 런타임) | SMOKE_TEST |
| **SMOKE_TEST** | 최소 실행으로 파이프라인 검증 | EXECUTING (pass) / ADJUSTING (fail) |
| **EXECUTING** | 본 실행 (학습, 테스트, 빌드 등) | CHECKING (success) / ADJUSTING (failure) |
| **CHECKING** | 결과 검증 (validation, assertion 등) | ANALYZING (success) / ADJUSTING (failure) |
| **ANALYZING** | 결과 분석 + 리포트 작성 | DONE |
| **ADJUSTING** | 에러 진단 + 수정 | SMOKE_TEST / EXECUTING / CHECKING (retry) |
| **DONE** | 최종 요약 | — |

> Phase 이름은 프로젝트에 맞게 변경 가능 (예: ML은 TRAINING/VALIDATING, 테스트는 TESTING/VERIFYING).

**Escalation**: 같은 원인 3회 실패 → DONE + "STUCK" 메시지. 진단 불가 → DONE + "UNKNOWN ERROR". 외부 조치 필요 → DONE + 설명.

---

## Process

### Step 1: Discover the Target Process

**도구**: `Glob`, `Grep`, `Read`

아래 체크리스트를 순서대로 확인한다:

- [ ] `_sdd/spec/**/*.md` 존재 시 읽기 (primary source of truth)
- [ ] `_sdd/env.md` 존재 시 읽기 (런타임 환경 설정)
- [ ] Entry Point 식별 (메인 진입점 스크립트/명령) — 미발견 시 스킬 종료
- [ ] Verification Step 파악 (성공 검증 방법)
- [ ] Input/Data Dependencies 파악
- [ ] Output Parsing 방법 파악 (구조화 로깅 여부)
- [ ] Runtime Environment 파악 (`_sdd/env.md` 우선, 없으면 프로젝트 파일에서 추론)

### Step 2: Present Findings and Confirm

분석 결과 요약 테이블을 제시하고 사용자 확인을 요청한다:

| 항목 | 파악 내용 | 상태 |
|------|----------|------|
| 진입점 | `<discovered>` | confirmed / input needed |
| 검증 방법 | `<discovered>` | confirmed / input needed |
| 입력/데이터 | `<discovered>` | confirmed |
| 런타임 환경 | `<detected>` | confirmed |
| 초기 파라미터 | `<suggested>` | confirmed |
| 실행 명령 | `<command>` | confirmed |

사용자가 확인하면 (또는 auto-proceed 가능하면) 다음 단계로 진행한다.

### Step 3: Generate `ralph/CHECKS.md`

`ralph/` 디렉토리를 생성하고 (`mkdir -p ralph`) 아래 내용으로 `ralph/CHECKS.md`를 작성한다:

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
- [ ] Core phases present
- [ ] Main execution command using config.sh variables
- [ ] Known Errors section present
- [ ] action.sh Rules section present
- [ ] Decision log read/write instructions present
- [ ] ANALYZING phase requires an executive-style `final_report.md`
- [ ] Final report uses conclusion-first reporting tone, not a 3-5 bullet memo
- [ ] Final report sections cover summary, scope, evidence, risks, recommendation, and next actions
- [ ] Self-correction protocol present

## run.sh
- [ ] `--reset` flag, `LLM_TIMEOUT_SECONDS`, DONE detection present

## state.md
- [ ] `phase: SETUP`, `iteration: 0`, valid `initialized_at` timestamp
```

### Step 4: Generate `ralph/config.sh`

**고정 변수** (항상 포함):
```bash
#!/usr/bin/env bash
# Ralph Loop Configuration
# Edit these values BEFORE running: bash ralph/run.sh
# ──────────────────────────────────────────────────────────

# ── Loop Safety (fixed) ──
LLM_TIMEOUT_SECONDS=600  # max seconds for one LLM turn (0 disables timeout)
MAX_LLM_FAILURES=3       # consecutive LLM failures before abort
```

**프로젝트별 변수**: LLM이 Step 1 분석 결과에 따라 적절한 변수를 추가한다.
- `LLM_TIMEOUT_SECONDS`와 `MAX_LLM_FAILURES`는 항상 포함
- Debug-first 접근: 초기 값은 보수적으로 설정
- 카테고리별 주석 헤더로 그룹화
- 프로젝트가 실제 사용하는 변수만 포함

### Step 5: Generate `ralph/PROMPT.md`

State Machine Reference 섹션의 구조를 기반으로 프로젝트에 맞는 PROMPT.md를 생성한다.

**필수 요소**:
1. Anti-recursion warning: `IMPORTANT: Do NOT invoke any skills, modes, or slash commands. Do NOT use the Skill tool. You are inside a standalone automation loop — not an interactive session.`
2. Project Context (config 경로, runtime 명령, verification 경로, results dir)
3. Phase 정의 (프로젝트에 맞게 SETUP / SMOKE_TEST / EXECUTING / CHECKING / ANALYZING / ADJUSTING / DONE 변환)
4. 각 phase별 프로젝트 고유 명령 (config.sh 변수 사용)
5. SMOKE_TEST repeat gate (실패 시 ADJUSTING → SMOKE_TEST 반복)
6. Iteration Protocol (11 Steps): config 읽기 → state 읽기 → decisions.md 읽기 → last_exit_code 읽기 → 결과 읽기 → env.md 읽기 → 판단 → action.sh 작성 → state.md 업데이트 → decisions.md 추가 → 종료
7. action.sh Rules: `set -euo pipefail`, `source ralph/config.sh`, `mkdir -p ralph/results`, `export PYTHONUNBUFFERED=1`, 결과를 `ralph/results/`에 저장, `2>&1 | tee` 로깅
8. Known Errors section — `uname -s`로 플랫폼 감지, Darwin이면 E1(macOS timeout 패턴) 포함 + Step 1에서 발견한 프로젝트 고유 에러 추가
9. Decision Log read/write protocol (append-only, 최근 15개 읽기)
10. `ANALYZING` phase는 `ralph/results/final_report.md`를 상사/리더십 보고용 문서처럼 작성하게 해야 한다. 결론을 먼저 제시하고 그 뒤에 근거와 권고를 배치하는 톤을 유지한다. 최소한 `verification_summary.md`, `decisions.md`, 핵심 실행 로그, `state.md`를 읽고 근거를 종합하여 보고서를 작성하게 하며, 단순히 테스트 로그 마지막 줄만 복사하거나 3-5개 bullet memo로 끝내서는 안 된다.
11. Final report contract: 아래 섹션을 기본 구조로 강제한다.

```markdown
# Final Report

- Generated at: <timestamp>
- Project: <project name>
- Final status: PASS / FAIL / STUCK / UNKNOWN ERROR
- Model / runtime: <model or toolchain>

## Executive Summary
- 한 단락으로 결과, 의미, 권고를 요약

## Objective and Scope
- 이번 Ralph loop가 검증하거나 해결하려던 대상
- 범위 안에서 실제로 수행한 것

## Run Summary
- Smoke run 결과
- Main execution 결과
- 반복 횟수 / 주요 phase 전환

## Key Evidence
- 어떤 로그/아티팩트/검증 결과를 근거로 결론을 내렸는지
- 실패/비재현 여부를 뒷받침하는 구체적 신호

## Root Cause Assessment
- 실패 시: 근본원인과 근거
- 성공 시: 재현 실패 또는 이슈 미관측 사실과 그 판단 근거

## Risks and Limitations
- 이번 실행이 커버하지 못한 범위
- 환경적 제약, 표본 부족, flaky 가능성, 추가 확인 필요 사항

## Recommendation
- 지금 시점의 권고안
- 코드/설정/운영 측면에서 유지, 수정, 추가 검증 중 무엇이 필요한지

## Next Actions
- 바로 다음에 할 일 1-3개

## Artifact References
- `ralph/results/...` 경로를 포함한 핵심 산출물 목록
```

`Executive Summary`, `Root Cause Assessment`, `Recommendation` 섹션은 최소 2-5문장의 완전한 문장으로 서술하게 하고, 단문 bullet만 나열하지 않도록 지시한다.

12. Self-correction protocol (PROMPT.md 자체 수정 규칙: 같은 원인 2회+ 실패 시 targeted edit 허용)

### Step 6: Generate `ralph/run.sh`

아래 템플릿을 **거의 그대로** `ralph/run.sh`에 복사한다. `python3` 명령이 프로젝트에 맞지 않으면 조정한다. `chmod +x ralph/run.sh` 실행.

```bash
#!/usr/bin/env bash
# Ralph loop: LLM thinks -> script executes -> repeat
#
# Flow per iteration:
#   1. LLM reads state.md + results, diagnoses, writes action.sh
#   2. action.sh executes (training, validation, etc.) -- may take hours
#   3. action.sh saves results to ralph/results/
#   4. Loop restarts -> LLM reads new results
#
# Usage: bash ralph/run.sh [--reset]
# Stop:  Ctrl+C or set phase to DONE in state.md

set -euo pipefail
cd "$(dirname "$0")/.."

show_usage() {
  cat <<'USAGE'
Usage: bash ralph/run.sh [--reset]

Options:
  --reset   Remove previous loop artifacts and restart from initial state.
USAGE
}

RESET=0
while [ $# -gt 0 ]; do
  case "$1" in
    --reset)
      RESET=1
      ;;
    -h|--help)
      show_usage
      exit 0
      ;;
    *)
      echo "[ralph] Unknown option: $1" >&2
      show_usage >&2
      exit 1
      ;;
  esac
  shift
done

if [ ${RESET} -eq 1 ]; then
  INIT_TS="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  echo "[ralph] --reset enabled: clearing previous artifacts."
  rm -rf ralph/results
  rm -f ralph/action.sh
  cat > ralph/state.md <<EOF
phase: SETUP
iteration: 0
initialized_at: ${INIT_TS}
errors: []
last_checkpoint: null
validation_results: null
notes: Initial state. Ralph loop initialized.
EOF
fi

if [ -f ralph/config.sh ]; then
  # shellcheck source=/dev/null
  source ralph/config.sh
fi

LLM_TIMEOUT_SECONDS="${LLM_TIMEOUT_SECONDS:-600}"
if ! [[ "${LLM_TIMEOUT_SECONDS}" =~ ^[0-9]+$ ]]; then
  echo "[ralph] Invalid LLM_TIMEOUT_SECONDS='${LLM_TIMEOUT_SECONDS}'. Use a non-negative integer." >&2
  exit 1
fi

if [ "${LLM_TIMEOUT_SECONDS}" -eq 0 ]; then
  echo "[ralph] LLM timeout disabled (LLM_TIMEOUT_SECONDS=0)."
else
  echo "[ralph] LLM timeout: ${LLM_TIMEOUT_SECONDS}s per LLM step."
fi

LOCK_DIR="ralph/.ralph.lock.d"
LOCK_PID_FILE="${LOCK_DIR}/pid"

is_probably_ralph_process() {
  local pid="$1"
  local cmd
  cmd="$(ps -p "${pid}" -o command= 2>/dev/null || true)"
  [ -n "${cmd}" ] && [[ "${cmd}" == *"run.sh"* ]]
}

cleanup_lock() {
  local owner_pid
  owner_pid="$(cat "${LOCK_PID_FILE}" 2>/dev/null || true)"
  if [ -n "${owner_pid}" ] && [ "${owner_pid}" = "$$" ]; then
    rm -rf "${LOCK_DIR}"
  fi
}

acquire_lock() {
  if mkdir "${LOCK_DIR}" 2>/dev/null; then
    echo "$$" > "${LOCK_PID_FILE}"
    return 0
  fi

  local existing_pid=""
  existing_pid="$(cat "${LOCK_PID_FILE}" 2>/dev/null || true)"

  if [ -n "${existing_pid}" ] && kill -0 "${existing_pid}" 2>/dev/null && is_probably_ralph_process "${existing_pid}"; then
    echo "[ralph] ERROR: Another ralph instance is running (PID ${existing_pid})." >&2
    echo "[ralph] If stale, remove manually: rm -rf ${LOCK_DIR}" >&2
    return 1
  fi

  echo "[ralph] Stale lock found (PID ${existing_pid}). Reclaiming lock."
  rm -rf "${LOCK_DIR}"
  if mkdir "${LOCK_DIR}" 2>/dev/null; then
    echo "$$" > "${LOCK_PID_FILE}"
    return 0
  fi

  echo "[ralph] ERROR: Failed to acquire lock at ${LOCK_DIR}." >&2
  return 1
}

acquire_lock || exit 1
trap cleanup_lock EXIT INT TERM

run_llm_with_timeout() {
  local timeout_seconds="$1"
  local prompt_path="$2"
  shift 2

  if [ "${timeout_seconds}" -eq 0 ]; then
    "$@" < "${prompt_path}"
    return $?
  fi

  if command -v timeout >/dev/null 2>&1; then
    timeout "${timeout_seconds}" "$@" < "${prompt_path}"
    return $?
  fi

  if command -v gtimeout >/dev/null 2>&1; then
    gtimeout "${timeout_seconds}" "$@" < "${prompt_path}"
    return $?
  fi

  python3 - "${timeout_seconds}" "${prompt_path}" "$@" <<'PY'
import subprocess
import sys

timeout_seconds = int(sys.argv[1])
prompt_path = sys.argv[2]
cmd = sys.argv[3:]

with open(prompt_path, "rb") as prompt_file:
    try:
        completed = subprocess.run(
            cmd,
            stdin=prompt_file,
            stdout=sys.stdout,
            stderr=sys.stderr,
            check=False,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        print(
            f"[ralph] LLM step timed out after {timeout_seconds} seconds.",
            file=sys.stderr,
        )
        sys.exit(124)

sys.exit(completed.returncode)
PY
}

VALID_PHASES="SETUP SMOKE_TEST TRAINING VALIDATING EXECUTING CHECKING ANALYZING ADJUSTING DONE"

validate_state_file() {
  local state_file="ralph/state.md"
  [ -f "${state_file}" ] || { echo "[ralph] VALIDATION ERROR: ${state_file} missing." >&2; return 1; }
  [ -s "${state_file}" ] || { echo "[ralph] VALIDATION ERROR: ${state_file} empty." >&2; return 1; }

  local phase
  phase="$(grep -m1 '^phase:' "${state_file}" | sed 's/^phase:[[:space:]]*//' | tr -d '[:space:]')" || true
  local phase_valid=0
  for vp in ${VALID_PHASES}; do [ "${phase}" = "${vp}" ] && phase_valid=1 && break; done
  [ "${phase_valid}" -eq 1 ] || { echo "[ralph] VALIDATION ERROR: Invalid phase '${phase}'." >&2; return 1; }

  local iter_val
  iter_val="$(grep -m1 '^iteration:' "${state_file}" | sed 's/^iteration:[[:space:]]*//' | tr -d '[:space:]')" || true
  [[ "${iter_val}" =~ ^[0-9]+$ ]] || { echo "[ralph] VALIDATION ERROR: Invalid iteration '${iter_val}'." >&2; return 1; }
}

ITERATION=0
LLM_FAIL_COUNT=0
MAX_LLM_FAILURES=3

mkdir -p ralph/results

while :; do
  ITERATION=$((ITERATION + 1))
  echo ""
  echo "=========================================="
  echo "  Ralph iteration #${ITERATION}"
  echo "  $(date '+%Y-%m-%d %H:%M:%S')"
  echo "=========================================="

  # --- Phase 1: LLM thinks ---
  echo "[ralph] Phase 1: LLM analyzing state and writing action..."
  # Disable errexit temporarily so LLM failures are handled by retry logic.
  set +e
  # Allow nested Claude Code execution (e.g., when spawned from autopilot/agent).
  unset CLAUDECODE
  run_llm_with_timeout "${LLM_TIMEOUT_SECONDS}" "ralph/PROMPT.md" \
    claude -p --verbose --dangerously-skip-permissions --output-format stream-json \
    | tee "ralph/results/llm_iter${ITERATION}.json" \
    | python3 -u -c "
import sys, json
for line in sys.stdin:
    line = line.strip()
    if not line: continue
    try:
        ev = json.loads(line)
    except json.JSONDecodeError:
        continue
    t = ev.get('type','')
    if t == 'assistant' and 'content' in ev:
        for block in ev['content']:
            if block.get('type') == 'text':
                print(block['text'], end='', flush=True)
            elif block.get('type') == 'tool_use':
                name = block.get('name','')
                inp = block.get('input',{})
                if name in ('Read','Glob','Grep'):
                    target = inp.get('file_path') or inp.get('pattern','')
                    print(f'  [{name}] {target}', flush=True)
                elif name == 'Write':
                    print(f'  [Write] {inp.get(\"file_path\",\"\")}', flush=True)
                elif name == 'Edit':
                    print(f'  [Edit] {inp.get(\"file_path\",\"\")}', flush=True)
                elif name == 'Bash':
                    cmd = inp.get('command','')[:80]
                    print(f'  [Bash] {cmd}', flush=True)
                else:
                    print(f'  [{name}]', flush=True)
    elif t == 'result':
        pass  # tool results -- skip (too verbose)
" 2>/dev/null
  LLM_EXIT=$?
  set -e
  echo ""

  if [ ${LLM_EXIT} -ne 0 ]; then
    LLM_FAIL_COUNT=$((LLM_FAIL_COUNT + 1))
    if [ ${LLM_EXIT} -eq 124 ]; then
      echo "[ralph] LLM step exceeded timeout (${LLM_TIMEOUT_SECONDS}s)."
    fi
    echo "[ralph] LLM step failed (exit code ${LLM_EXIT}, failure ${LLM_FAIL_COUNT}/${MAX_LLM_FAILURES})"
    if [ ${LLM_FAIL_COUNT} -ge ${MAX_LLM_FAILURES} ]; then
      echo "[ralph] ERROR: LLM step failed ${MAX_LLM_FAILURES} consecutive times. Exiting."
      echo "[ralph] Check: claude CLI installed? API key valid? Network OK?"
      exit 1
    fi
    echo "[ralph] Retrying after sleep..."
    sleep 10
    continue
  fi
  LLM_FAIL_COUNT=0

  if ! validate_state_file; then
    echo "[ralph] ERROR: state.md corrupted after LLM step. Aborting." >&2
    exit 1
  fi

  # Check if state is DONE (LLM decided we're finished)
  if grep -q "^phase: DONE" ralph/state.md 2>/dev/null; then
    COMPLETION_PROMISE="${COMPLETION_PROMISE:-}"
    if [ -n "${COMPLETION_PROMISE}" ]; then
      LLM_OUTPUT_FILE="ralph/results/llm_iter${ITERATION}.json"
      if grep -Fq "<completion_promise>${COMPLETION_PROMISE}</completion_promise>" "${LLM_OUTPUT_FILE}" 2>/dev/null; then
        echo "[ralph] State is DONE. Completion promise verified. Exiting loop."
      else
        echo "[ralph] WARNING: State is DONE but completion promise not found in LLM output."
        echo "[ralph]   Expected: <completion_promise>${COMPLETION_PROMISE}</completion_promise>"
        echo "[ralph]   Proceeding with exit (phase: DONE is authoritative)."
      fi
    else
      echo "[ralph] State is DONE. Exiting loop."
    fi
    break
  fi

  # --- Phase 2: Execute action ---
  if [ -f ralph/action.sh ]; then
    echo "[ralph] Phase 2: Executing action.sh..."
    echo ""

    cp ralph/state.md ralph/results/state_backup.md

    # Run action.sh, capture exit code (don't fail the loop on error)
    set +e
    bash ralph/action.sh
    ACTION_EXIT=$?
    set -e

    if ! validate_state_file 2>/dev/null; then
      echo "[ralph] WARNING: state.md corrupted after action.sh. Restoring from backup."
      cp ralph/results/state_backup.md ralph/state.md
    fi

    # Record exit code for LLM to read next iteration
    echo "${ACTION_EXIT}" > ralph/results/last_exit_code

    if [ ${ACTION_EXIT} -ne 0 ]; then
      echo "[ralph] action.sh exited with code ${ACTION_EXIT}"
    else
      echo "[ralph] action.sh completed successfully"
    fi

    # Archive action.sh so LLM writes a fresh one next iteration
    mv ralph/action.sh "ralph/results/action_iter${ITERATION}.sh"
  else
    echo "[ralph] No action.sh found -- LLM-only iteration"
  fi

  echo ""
  echo "--- Iteration #${ITERATION} complete ---"
  sleep 3
done
```

### Step 7: Generate `ralph/state.md`

`date -u '+%Y-%m-%dT%H:%M:%SZ'`로 현재 UTC 타임스탬프를 얻어 아래 내용으로 생성한다:

```
phase: SETUP
iteration: 0
initialized_at: <current UTC timestamp>
errors: []
last_checkpoint: null
validation_results: null
notes: Initial state. Ralph loop initialized.
```

### Step 8: Verify Against CHECKS.md and Summarize

1. `ralph/CHECKS.md`의 각 항목을 `Grep`/`Read`로 검증한다. 실패 항목은 해당 파일을 수정한 후 재검증 (최대 2회).
2. 검증 완료 후 `CHECKS.md`의 `[ ]`를 `[x]` (통과) 또는 `[!]` (수정 후 통과)로 업데이트한다.
3. `mkdir -p ralph/results` 후 요약을 출력한다:

```
Ralph loop initialized (TDD verified)!

Files created:
  ralph/CHECKS.md    — Acceptance criteria (verified)
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

## Error Handling

| 상황 | 대응 |
|------|------|
| 진입점 미발견 | 오류 보고 후 스킬 종료 |
| `_sdd/spec` 미존재 | 코드 기반 탐색으로 진행, 경고 출력 |
| CHECKS.md 검증 실패 | 실패 파일 수정, 재검증 (최대 2회) |
| 복수 진입점 발견 | 가장 유력한 진입점 자동 선택, 판단 근거 기록 |

## Final Check

Acceptance Criteria가 모두 만족되었나 검증한다. 미충족 항목이 있으면 해당 단계로 돌아가 수정한다.

> **Mirror Notice**: 이 agent는 `.claude/skills/ralph-loop-init/SKILL.md`와 동일한 계약을 공유한다.
> 내용을 수정할 때는 skill 파일과 이 agent 파일을 **반드시 함께** 수정해야 한다.
