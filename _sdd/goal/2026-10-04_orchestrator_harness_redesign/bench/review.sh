#!/usr/bin/env bash
# M4 독립 리뷰: 하네스 스킬 없이 새 세션 1개가 고정 지시문으로 draft AC를 fresh 판정하고 결함을 찾는다.
# usage: review.sh <run id: <feat>-<arm>-<rep>>   env: BENCH_DIR
set -euo pipefail
RUN=$1
B=${BENCH_DIR:?BENCH_DIR required}
WT=$B/t-$RUN
LOG=$B/logs
DRAFT=$(cd "$WT" && ls _sdd/drafts/*2026-08-26_feature_draft_*.md | head -1)
SCHEMA=$(cat <<'EOF'
{
  "type": "object",
  "required": ["ac", "findings"],
  "properties": {
    "ac": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["task", "ac", "verdict", "evidence"],
        "properties": {
          "task": {"type": "string"},
          "ac": {"type": "string"},
          "verdict": {"enum": ["MET", "NOT_MET", "UNTESTED"]},
          "evidence": {"type": "string"}
        }
      }
    },
    "findings": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["severity", "location", "summary"],
        "properties": {
          "severity": {"enum": ["Critical", "High", "Medium", "Low"]},
          "location": {"type": "string"},
          "summary": {"type": "string"}
        }
      }
    }
  }
}
EOF
)
PROMPT="너는 이 저장소의 변경을 처음 보는 독립 리뷰어다. 기준 문서는 \`$DRAFT\`(feature draft)이고, 리뷰 대상은 HEAD 대비 작업 트리 전체 변경이다(\`git status --short\`와 \`git diff HEAD\`로 확인한다. draft 파일 자체는 대상이 아니다).
1. draft Part 2의 모든 task AC를 지금 작업 트리에서 직접 실행하거나 읽어서 판정한다(MET / NOT_MET / UNTESTED). evidence에는 실행한 명령과 결과 요지, 또는 file:line을 적는다.
2. draft Part 1(spec delta)이 \`_sdd/spec/\`에 반영되었는지 확인한다. 반영되지 않았거나 틀리게 반영됐으면 finding으로 낸다.
3. 이 변경이 만든 결함을 찾는다. AC 밖 결함도 포함한다(남은 stale 참조, claude↔codex 미러 불일치, 깨진 절·파일 참조, 형식 오류, 의도와 다른 의미 변경).
severity 기준: Critical = 변경 목적을 깨거나 저장소를 손상한다. High = 스킬 실행 결과가 틀려지는 결함이거나 AC 미충족이다. Medium = 혼동·불일치를 낳지만 실행 결과는 맞다. Low = 사소한 표현 문제다.
파일을 수정하지 않는다. 결과는 지정된 JSON schema로만 낸다."
RSID=$(uuidgen | tr 'A-Z' 'a-z')
( cd "$WT" && printf '%s' "$PROMPT" | claude -p --model claude-opus-5-5 --disable-slash-commands \
    --dangerously-skip-permissions --session-id "$RSID" --output-format json --json-schema "$SCHEMA" \
    > "$LOG/$RUN.review.json" 2> "$LOG/$RUN.review.err" ) || echo "claude exit $?" >> "$LOG/$RUN.review.err"
printf '%s\t%s\n' "$RUN" "$RSID" >> "$LOG/reviews.tsv"
