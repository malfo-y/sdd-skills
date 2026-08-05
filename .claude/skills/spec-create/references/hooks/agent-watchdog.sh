#!/usr/bin/env bash
# SDD 하네스 자산 — subagent 장기실행 watchdog (Claude Code PostToolUse 훅).
#
# 정본 = `.claude/skills/spec-create/references/hooks/`.
# 나머지 3곳(`.codex/spec-create`, `.claude/spec-upgrade`, `.codex/spec-upgrade`의
# `references/hooks/`)은 미러다. 수정 시 4곳을 바이트 동일로 동기화한다.
#
# subagent가 첫 tool call 이후 THRESHOLD초 이상 돌면 tool 결과에 자기점검 nudge를
# 끼워 넣는다 — 시간 도둑(반복 환경 재설치 등) 자평 + 캐시/재사용 전환 유도.
# COOLDOWN초마다 최대 1회 재발동한다. 메인 루프 호출(payload에 agent_id 없음)은 대상이 아니다.
#
# advisory 자산이다(게이트 아님) — 파서 부재·파싱 실패·상태 기록 실패 등 판정 불가는
# 전부 조용히 fail-open(exit 0) 한다. nudge 부재는 기능 상실이지 규약 붕괴가 아니다.
#
# 알려진 한계: nudge는 tool call 경계에서만 전달된다 — 단일 장시간 명령의 중간에는 개입하지 못한다.
set -uo pipefail

allow() { exit 0; }

THRESHOLD=300
COOLDOWN=300

payload=$(cat)

# JSON 파서: jq → python3. 둘 다 없으면 판정 불가(fail-open).
parse_payload() {
  if command -v jq >/dev/null 2>&1; then
    printf '%s' "$payload" | jq -r '(.session_id // "unknown"), (.agent_id // "")' 2>/dev/null
  elif command -v python3 >/dev/null 2>&1; then
    printf '%s' "$payload" | python3 -c 'import sys, json
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(1)
print(d.get("session_id") or "unknown")
print(d.get("agent_id") or "")' 2>/dev/null
  else
    return 1
  fi
}

parsed=$(parse_payload) || allow
[ -n "$parsed" ] || allow
session=$(printf '%s\n' "$parsed" | sed -n '1p')
agent=$(printf '%s\n' "$parsed" | sed -n '2p')
[ -n "$agent" ] || allow

# 상태는 세션·agent 단위 파일로만 둔다. 디렉토리 생성 실패(공유 /tmp 소유권 등)는 fail-open.
dir="${TMPDIR:-/tmp}/claude-agent-watchdog/$session"
mkdir -p "$dir" 2>/dev/null || allow
now=$(date +%s)
start_file="$dir/$agent.start"
nudge_file="$dir/$agent.nudge"

if [ ! -f "$start_file" ]; then
  printf '%s' "$now" > "$start_file" 2>/dev/null
  allow
fi

start=$(cat "$start_file" 2>/dev/null) || allow
case "$start" in (''|*[!0-9]*) allow ;; esac
elapsed=$(( now - start ))
[ "$elapsed" -ge "$THRESHOLD" ] || allow

last=$(cat "$nudge_file" 2>/dev/null || echo 0)
case "$last" in (''|*[!0-9]*) last=0 ;; esac
[ $(( now - last )) -ge "$COOLDOWN" ] || allow
printf '%s' "$now" > "$nudge_file" 2>/dev/null

# ⚠️ reason 에는 " 와 \ 와 줄바꿈이 없어야 한다(문구를 고칠 때도 넣지 말 것 — 단일 라인 리터럴 유지).
reason="[agent-watchdog] 이 agent는 첫 tool call 이후 ${elapsed}초째 실행 중입니다. (1) 지금 하는 작업이 시간을 과도하게 먹고 있는지 1문장으로 자평하세요. (2) 반복 실행하는 명령에 캐시/재사용 여지가 있으면 그 방법으로 전환하세요 — 예: 매번 환경을 재설치하는 실행(uv run --with, pip install 반복) 대신 venv를 한 번 만들어 재사용. (3) 이 메시지로 접근을 바꿨다면 최종 응답에 한 줄로 언급하세요."

printf '{"decision":"block","reason":"%s"}\n' "$reason"
exit 0
