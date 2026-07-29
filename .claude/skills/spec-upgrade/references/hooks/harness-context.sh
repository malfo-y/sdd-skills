#!/usr/bin/env bash
# SDD 하네스 자산 — 컨텍스트 소실 후 하네스 재주입 (Claude Code SessionStart 훅, source=clear|compact).
#
# 정본 = `.claude/skills/spec-create/references/hooks/`.
# 나머지 3곳(`.codex/spec-create`, `.claude/spec-upgrade`, `.codex/spec-upgrade`의
# `references/hooks/`)은 미러다. 수정 시 4곳을 바이트 동일로 동기화한다.
#
# 차단하지 않는다. SessionStart 훅은 exit 0 의 stdout 이 그대로 모델 컨텍스트로 들어간다.
# compact/clear 로 컨텍스트가 날아가면 `CLAUDE.md` 포인터만 재주입되고 하네스 본문은 사라진다.
# 포인터를 따라 읽을지는 모델 재량이라 실제로 누락되므로, 지시가 아니라 전문을 직접 넣는다.
#
# 마커(`SDD-HARNESS`) 블록만이 아니라 `AGENTS.md` 전문을 넣는다 — 마커 밖 내용은 그 repo가
# 직접 쓴 작업 규약이고, 재주입의 목적에 정확히 해당한다.
set -uo pipefail

cd "${CLAUDE_PROJECT_DIR:-.}" 2>/dev/null || exit 0
[ -f AGENTS.md ] || exit 0

echo "[harness] 컨텍스트가 초기화됐다(compact/clear). 아래가 이 repo의 작업 하네스 AGENTS.md 전문이다 — 다시 Read 하지 말고 이대로 따른다."
cat AGENTS.md
