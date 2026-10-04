#!/usr/bin/env bash
# run 종료 후 처리: 결과물 patch 스냅샷(untracked 포함, draft 제외) + 독립 리뷰.
# usage: post.sh <run id>   env: BENCH_DIR
set -euo pipefail
RUN=$1
B=${BENCH_DIR:?BENCH_DIR required}
HERE=$(cd "$(dirname "$0")" && pwd)
WT=$B/t-$RUN
DRAFT=$(cd "$WT" && ls _sdd/drafts/*2026-08-26_feature_draft_*.md | head -1)
git -C "$WT" add -N -- . ":(exclude)$DRAFT"
git -C "$WT" diff HEAD -- . ":(exclude)$DRAFT" > "$B/logs/$RUN.patch"
"$HERE/review.sh" "$RUN"
