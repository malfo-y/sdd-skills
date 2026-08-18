#!/usr/bin/env bash
# SDD 하네스 자산 — work log 커밋 게이트 (Claude Code/Codex PreToolUse 훅).
#
# 정본 = `.claude/skills/spec-create/references/hooks/`.
# 나머지 4곳(`.codex/spec-create`, `.claude/spec-upgrade`, `.codex/spec-upgrade`의
# `references/hooks/` + `.claude/hooks/`)은 미러다. 수정 시 5곳을 바이트 동일로 동기화한다.
#
# AGENTS.md §5("작업 단위 종료 시 예외 없이 work log 기록")를 하네스 차원에서 강제한다.
# 통과 조건 (하나라도 만족하면 allow):
#   - git commit 호출이 아님
#   - --amend, 또는 SDD_SKIP_WORKLOG=1 명시
#   - rebase / merge / cherry-pick 진행 중
#   - 이번 세션에서 이미 한 번 통과함 (마커)
#   - 오늘 work log에 미커밋 변경(신규/수정)이 있음  ← 실제 판정
#
# 판정이 불가능한 상황(JSON 파서 부재, git repo 아님 등)에서는 fail-open 한다.
# 파서 부재는 침묵하지 않는다 — worklog-context.sh 가 세션 시작 시 "게이트 비활성"을 알린다.
#
# 알려진 한계 — 전부 통과(fail-open) 방향이다:
#   - `sudo git commit`, `bash -c "git commit …"` 같은 중첩 호출은 감지하지 못한다.
#   - `git -C "/path with space" commit` 처럼 전역 옵션 값에 공백이 있으면 감지하지 못한다.
#   - 백슬래시 줄바꿈으로 `git` 과 `commit` 이 다른 줄에 있으면 감지하지 못한다.
set -uo pipefail

allow() { exit 0; }

# Claude Code는 CLAUDE_PROJECT_DIR를 주지만 Codex는 주지 않는다. 유효한 환경변수를
# 우선하고, 없거나 잘못됐으면 현재 worktree의 git root로 복구한다.
project_root=$(
  if [ -n "${CLAUDE_PROJECT_DIR:-}" ] && [ -d "$CLAUDE_PROJECT_DIR" ]; then
    printf '%s\n' "$CLAUDE_PROJECT_DIR"
  else
    git rev-parse --show-toplevel 2>/dev/null
  fi
) || allow
cd "$project_root" 2>/dev/null || allow

payload=$(cat)

# JSON 파서: jq → python3. 둘 다 없으면 판정 불가.
# session_id 를 먼저 출력한다 — command 는 여러 줄일 수 있어 마지막에 와야 안전하다.
parse_payload() {
  if command -v jq >/dev/null 2>&1; then
    printf '%s' "$payload" | jq -r '(.session_id // "unknown"), (.tool_input.command // "")' 2>/dev/null
  elif command -v python3 >/dev/null 2>&1; then
    printf '%s' "$payload" | python3 -c 'import sys, json
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(1)
print(d.get("session_id") or "unknown")
print((d.get("tool_input") or {}).get("command") or "")' 2>/dev/null
  else
    return 1
  fi
}

parsed=$(parse_payload) || allow
[ -n "$parsed" ] || allow
session=$(printf '%s\n' "$parsed" | sed -n '1p')
cmd=$(printf '%s\n' "$parsed" | sed -n '2,$p')

# 인용부호 안의 내용은 명령이 아니라 데이터다. 판별 전에 걷어낸다 —
# 그러지 않으면 커밋 메시지에 들어간 `--amend` 한 조각으로 게이트가 조용히 뚫린다.
cmd=$(printf '%s' "$cmd" | sed -e "s/'[^']*'//g" -e 's/"[^"]*"//g')

# 명령 경계 = 문자열 시작 또는 ; & | ( ` { 뒤. 이 경계에서 시작하는 git 만 본다 —
# 그래야 `grep "git commit" file` 처럼 인자에 들어간 텍스트를 커밋으로 오인하지 않는다.
# `git -C <path> commit` 처럼 값을 받는 전역 옵션은 건너뛴다.
cmd_boundary='(^|[;&|(`{])[[:space:]]*'
env_prefix='([A-Za-z_][A-Za-z0-9_]*=[^[:space:]]*[[:space:]]+)*'

# git commit 호출이 아니면 관심 없음.
git_commit_re="${cmd_boundary}${env_prefix}"'git([[:space:]]+(-[Cc][[:space:]]+[^[:space:]]+|-[^[:space:]]+))*[[:space:]]+commit([[:space:]]|$)'
printf '%s' "$cmd" | grep -Eq "$git_commit_re" || allow

# 명시적 예외. 예외 판별도 경계를 맞춘다 — 문자열 전체를 훑으면
# 커밋 메시지에 들어간 우회 토큰만으로 게이트가 조용히 뚫린다.
skip_re="${cmd_boundary}${env_prefix}"'SDD_SKIP_WORKLOG=1([[:space:]]|$)'
printf '%s' "$cmd" | grep -Eq "$skip_re" && allow
printf '%s' "$cmd" | grep -Eq '(^|[[:space:]])--amend([[:space:]]|$)' && allow

git_dir=$(git rev-parse --git-dir 2>/dev/null) || allow

# 진행 중인 rebase/merge/cherry-pick 의 커밋은 새 작업 단위가 아니다
for f in rebase-merge rebase-apply MERGE_HEAD CHERRY_PICK_HEAD; do
  [ -e "$git_dir/$f" ] && allow
done

# 세션 마커: 이번 세션에서 이미 통과했으면 이후 커밋은 막지 않는다.
# (커밋을 여러 개로 분할하는 워크플로우에서 2번째 커밋부터 오탐으로 막히는 것을 방지)
# 마커는 정리하지 않는다(의도적) — .git/ 내부라 무해하고, 정리는 게이트의 책임이 아니다.
marker_dir="$git_dir/sdd-worklog-ok"
marker="$marker_dir/$session"
[ -f "$marker" ] && allow

log_rel="_sdd/work_log/$(date +%F).md"

# 오늘 로그에 미커밋 변경이 있으면 = 이번 작업 단위를 기록했다
if [ -n "$(git status --porcelain -- "$log_rel" 2>/dev/null)" ]; then
  mkdir -p "$marker_dir" 2>/dev/null && : > "$marker" 2>/dev/null
  allow
fi

reason="AGENTS.md §5 — 작업 단위를 닫기 전 work log 기록이 필요합니다.
오늘 로그 \`${log_rel}\` 에 미커밋 변경이 없습니다(아직 안 썼거나 이미 커밋된 상태).

이번 작업 단위 항목을 append한 뒤 다시 커밋하세요:
  ## <순번/HH:MM> <제목>
  무엇/왜 · 결과 · 포인터(관련 커밋·문서·decision log) · 요약(따로 남은 게 없을 때만)

예외가 필요하면 \`SDD_SKIP_WORKLOG=1 git commit ...\` 로 우회할 수 있습니다.
(이 게이트는 세션당 1회만 발동합니다 — 통과 후의 분할 커밋은 막지 않습니다.)"

# 읽는 쪽과 달리 쓰는 쪽은 파서가 필요 없다 — 구조가 고정이고 삽입값은 reason 하나다.
# ⚠️ reason 에는 " 와 \ 가 없어야 한다(위 메시지를 고칠 때도 넣지 말 것). 줄바꿈만 이스케이프한다.
printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"%s"}}\n' "${reason//$'\n'/\\n}"
exit 0
