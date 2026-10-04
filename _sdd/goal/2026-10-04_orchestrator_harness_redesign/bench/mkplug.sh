#!/usr/bin/env bash
# --plugin-dir용 래퍼를 만든다. marketplace 루트(plugin.json 없음)를 --plugin-dir로 주면 설치된 sdd-skills를 덮어쓰지 못하므로,
# plugin.json(name=sdd-skills) + skills/<이름> symlink 구조로 감싼다.
# usage: mkplug.sh <repo checkout> <out dir>
set -euo pipefail
SRC=$(cd "$1" && pwd); OUT=$2
rm -rf "$OUT"; mkdir -p "$OUT/.claude-plugin" "$OUT/skills"
printf '{"name":"sdd-skills","version":"0.0.0-bench","description":"bench harness from %s"}\n' "$SRC" > "$OUT/.claude-plugin/plugin.json"
for s in $(jq -r '.plugins[0].skills[]' "$SRC/.claude-plugin/marketplace.json"); do
  ln -s "$SRC/${s#./}" "$OUT/skills/$(basename "$s")"
done
