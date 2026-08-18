#!/usr/bin/env bash
# SDD 하네스 자산 — work log 세션 컨텍스트 주입 (Claude Code/Codex SessionStart 훅).
#
# 정본 = `.claude/skills/spec-create/references/hooks/`.
# 나머지 4곳(`.codex/spec-create`, `.claude/spec-upgrade`, `.codex/spec-upgrade`의
# `references/hooks/` + `.claude/hooks/`)은 미러다. 수정 시 5곳을 바이트 동일로 동기화한다.
#
# 차단하지 않는다. Claude Code와 Codex가 함께 해석하는 SessionStart JSON envelope의
# additionalContext로 stdout을 전달한다. JSON 인코더가 없으면 invalid JSON을 내지 않고 fail-open한다.
set -uo pipefail

emit_session_context() {
  if command -v jq >/dev/null 2>&1; then
    jq -cn --arg context "$1" '{hookSpecificOutput:{hookEventName:"SessionStart",additionalContext:$context}}'
  elif command -v python3 >/dev/null 2>&1; then
    printf '%s' "$1" | python3 -c 'import json, sys
print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": sys.stdin.read()}}, ensure_ascii=False))'
  fi
}

project_root=$(
  if [ -n "${CLAUDE_PROJECT_DIR:-}" ] && [ -d "$CLAUDE_PROJECT_DIR" ]; then
    printf '%s\n' "$CLAUDE_PROJECT_DIR"
  else
    git rev-parse --show-toplevel 2>/dev/null
  fi
) || exit 0
cd "$project_root" 2>/dev/null || exit 0

log="_sdd/work_log/$(date +%F).md"

context=$(
  if [ -f "$log" ]; then
    last=$(grep -E '^## ' "$log" 2>/dev/null | tail -1)
    echo "[work log] 오늘 파일: ${log} (존재). 마지막 항목: ${last:-(항목 없음)}"
  else
    echo "[work log] 오늘 파일: ${log} (아직 없음 — 첫 작업 단위 종료 시 생성)"
  fi

  echo "[work log] 작업 단위(SDD 단계 종료 또는 독립 커밋)를 닫기 전 이 파일에 항목을 append한다 — AGENTS.md §5. 과거 로그 읽기는 on-demand(포렌식)일 때만."

  if command -v jq >/dev/null 2>&1 || command -v python3 >/dev/null 2>&1; then
    echo "[work log] git commit 은 훅으로 게이트되어 있다: 오늘 로그에 미커밋 변경이 없으면 세션 첫 커밋이 거부된다(우회: SDD_SKIP_WORKLOG=1)."
  else
    echo "[work log] ⚠️ 커밋 게이트 비활성 — JSON 파서(jq 또는 python3)가 없어 worklog-gate.sh 가 판정을 못 하고 모든 커밋을 통과시킨다. work log 기록은 규약(AGENTS.md §5)으로만 유지된다."
  fi
)

emit_session_context "$context"
