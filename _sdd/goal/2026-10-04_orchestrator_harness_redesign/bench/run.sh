#!/usr/bin/env bash
# 벤치마크 1회 실행: base commit worktree에서 draft를 구현~spec-sync까지 진행하고 독립 리뷰를 붙인다.
# usage: run.sh <feat: 87|88> <arm: old|new> <rep> <harness plugin dir>
# env: BENCH_DIR (worktree·로그를 둘 scratch 디렉터리)
set -euo pipefail
FEAT=$1; ARM=$2; REP=$3; HARNESS=$4
B=${BENCH_DIR:?BENCH_DIR required}
HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(git -C "$HERE" rev-parse --show-toplevel)
case $FEAT in
  87) MERGE=97f3ea4; SLUG=review_evidence_floor ;;
  88) MERGE=d5c39b3; SLUG=goal_autonomy_grant ;;
  *) echo "unknown feat $FEAT" >&2; exit 2 ;;
esac
BASE=$(git -C "$REPO" rev-parse "$MERGE^1")
DRAFT=_sdd/drafts/2026-08-26_feature_draft_${SLUG}.md
RUN=$FEAT-$ARM-$REP
WT=$B/t-$RUN
LOG=$B/logs
mkdir -p "$LOG"

git -C "$REPO" worktree add -q --detach "$WT" "$BASE"
git -C "$REPO" show "$MERGE:_sdd/drafts/_processed_2026-08-26_feature_draft_${SLUG}.md" > "$WT/$DRAFT"
# 대상 worktree의 bare 프로젝트 스킬(base 시점 사본)은 막고, --plugin-dir의 sdd-skills:* 만 쓰게 한다.
DENY=$(ls "$WT/.claude/skills" | sed 's/.*/Skill(&)/' | paste -sd, -)

case $ARM in
  old) PROMPT="\`$DRAFT\`(plan-review까지 끝난 draft)를 SDD 체인의 나머지 단계로 끝까지 진행해 주세요. 먼저 \`sdd-skills:implementation\` 스킬로 구현하고(품질 게이트 포함), 이어서 \`sdd-skills:spec-sync\` 스킬로 global spec을 동기화합니다. 사용자는 자리에 없으니 확인 질문 없이 끝까지 진행하고, git commit·push는 하지 않습니다." ;;
  new) PROMPT="\`$DRAFT\`(plan-review까지 끝난 draft)를 SDD 체인의 나머지 단계로 끝까지 진행해 주세요. \`sdd-skills:sdd-orchestrator\` 스킬로 구현 단계부터 spec-sync까지 진행합니다. 사용자는 자리에 없으니 확인 질문 없이 끝까지 진행하고, git commit·push는 하지 않습니다." ;;
  *) echo "unknown arm $ARM" >&2; exit 2 ;;
esac

SID=$(uuidgen | tr 'A-Z' 'a-z')
START=$(date +%s)
( cd "$WT" && printf '%s' "$PROMPT" | claude -p --model claude-opus-5-5 --plugin-dir "$HARNESS" \
    --disallowedTools "$DENY" --session-id "$SID" --dangerously-skip-permissions \
    --output-format json > "$LOG/$RUN.json" 2> "$LOG/$RUN.err" ) || echo "claude exit $?" >> "$LOG/$RUN.err"
END=$(date +%s)
printf '%s\t%s\t%s\t%s\n' "$RUN" "$SID" "$((END-START))" "$BASE" >> "$LOG/runs.tsv"

"$HERE/post.sh" "$RUN"
