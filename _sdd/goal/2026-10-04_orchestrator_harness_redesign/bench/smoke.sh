#!/usr/bin/env bash
# 신 경로 smoke: scratch git repo의 task 1개짜리 draft를 sdd-orchestrator로 implementation부터 implementation-review까지 실행한다.
# usage: smoke.sh <harness plugin dir>   env: BENCH_DIR
set -euo pipefail
HARNESS=$1
B=${BENCH_DIR:?BENCH_DIR required}
HERE=$(cd "$(dirname "$0")" && pwd)
R=$B/smoke-$(date +%Y%m%d%H%M%S)
DRAFT=_sdd/drafts/2026-10-04_feature_draft_smoke_beta.md
mkdir -p "$R/_sdd/drafts" "$R/logs"
cd "$R"
git init -q
printf '# Notes\n\n- alpha\n' > notes.md
cat > "$DRAFT" <<'EOF'
# Feature Draft: notes에 beta 항목 추가

> 규모 판정: 적격 — 변경 요소 1개(notes.md 목록 1줄), task 1개.

<!-- spec-update-todo-input-start -->
# Part 1: Spec Delta

## Change Summary
notes.md 목록에 `beta` 항목을 추가한다. 새 contract 없음.

## Scope
- **In**: `notes.md`
- **Out**: 그 밖의 파일
<!-- spec-update-todo-input-end -->

# Part 2: Tasks

### Task 1: notes.md에 beta 항목 추가
목록 끝에 `- beta` 한 줄을 추가한다.

**Acceptance Criteria**:
- [ ] AC1 (1등급): `grep -c '^- beta$' notes.md` = 1 이고 `grep -c '^- alpha$' notes.md` = 1.

**Target Files**:
- [M] `notes.md` -- beta 항목 추가
EOF
git add -A
git -c user.name=smoke -c user.email=smoke@example.invalid commit -qm init

PROMPT="\`$DRAFT\`(plan-review까지 끝난 draft)를 \`sdd-skills:sdd-orchestrator\` 스킬로 implementation부터 implementation-review까지 진행해 주세요(spec-sync는 하지 않습니다). 사용자는 자리에 없으니 확인 질문 없이 끝까지 진행하고, git commit은 하지 않습니다."
SID=$(uuidgen | tr 'A-Z' 'a-z')
START=$(date +%s)
printf '%s' "$PROMPT" | claude -p --model claude-opus-5-5 --plugin-dir "$HARNESS" --session-id "$SID" \
  --dangerously-skip-permissions --output-format json > logs/out.json 2> logs/err.txt || echo "claude exit $?" >> logs/err.txt
printf 'smoke\t%s\t%s\tinit\n' "$SID" "$(( $(date +%s) - START ))" > logs/runs.tsv

python3 "$HERE/metrics.py" "$R"
ls _sdd/implementation/*/digest.md >/dev/null 2>&1 && echo "digest: yes" || echo "digest: no"
ls _sdd/implementation/*/state.md >/dev/null 2>&1 && echo "state: yes" || echo "state: no"
[ "$(grep -c '^- beta$' notes.md)" = 1 ] && [ "$(grep -c '^- alpha$' notes.md)" = 1 ] && echo "task AC: PASS" || echo "task AC: FAIL"
echo "dir: $R"
