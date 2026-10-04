#!/usr/bin/env python3
"""벤치마크 run의 transcript를 계측해 M1~M5를 낸다 (goal.md 검증 레시피 R4).

usage: metrics.py <BENCH_DIR> [run id ...]   (run id 생략 시 runs.tsv 전체)
"""
import glob
import json
import os
import re
import statistics
import sys
from datetime import datetime

HANDOFF = re.compile(r"digest|state\.md|_feature_draft_|/references/|SKILL\.md|/workers/")
READ_CMD = re.compile(r"^\s*(cat|sed|head|tail|less|wc)\b")
EXEMPT_WRITE = re.compile(r"digest|state\.md|_sdd/goal/|_sdd/implementation/|_sdd/work_log/")
# Bash로 대상 파일을 쓰는 명령 탐지: 단순 변수 치환 → heredoc 본문·따옴표 문자열 제거 → 쓰기 연산의 대상 중 제외 경로가 아닌 파일이 있으면 쓰기로 센다.
EXEMPT_PATH = re.compile(r"digest|state\.md|_sdd/goal/|_sdd/implementation/|_sdd/work_log/|^/tmp/|^/private/tmp/|^/dev/")
WRITE_OP = re.compile(r"\bsed\s+-i|\bperl\s+-\w*i|\btee\b|\b(cp|mv|rm|install|touch)\s")
REDIRECT = re.compile(r"(?<![0-9&<])>>?\s*([^\s;&|)]+)")
FILE_TOKEN = re.compile(r"(?:^|\s)([\w./~-]*[\w-]\.[A-Za-z0-9]{1,5}|[\w.~-]*/[\w./-]+)(?=\s|$)")
PY_WRITE = re.compile(r"open\([^)]*['\"][wa]|\.write_text\(|\.write\(")


def _clean(cmd):
    for name, val in re.findall(r"\b([A-Za-z_]\w*)=(\S+)", cmd):
        cmd = re.sub(r"\$\{?" + name + r"\}?", val, cmd)
    cmd = re.sub(r"<<-?\s*['\"]?(\w+)['\"]?[^\n]*\n.*?\n\1\b", " ", cmd, flags=re.S)
    return re.sub(r"'[^']*'|\"[^\"]*\"", " ", cmd)


def bash_writes(tool):
    if tool["name"] != "Bash":
        return False
    raw = tool["input"].get("command", "")
    cmd = _clean(raw)
    targets = [t for t in REDIRECT.findall(cmd) if t != "&1" and t != "&2"]
    for seg in re.split(r"&&|\|\||[;|\n]", cmd):
        if WRITE_OP.search(seg):
            targets += FILE_TOKEN.findall(seg)
    if PY_WRITE.search(raw):
        targets += re.findall(r"['\"]([^'\"\s]+\.[A-Za-z0-9]{1,5})['\"]", raw)
    return any(not EXEMPT_PATH.search(t) for t in targets)


def ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()


def load(path):
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def messages(recs):
    """assistant 메시지를 message.id로 합친다(content 블록마다 줄이 나뉜다)."""
    out = {}
    for r in recs:
        if r.get("type") != "assistant":
            continue
        m = r["message"]
        e = out.setdefault(m["id"], {"t": ts(r["timestamp"]), "usage": m.get("usage", {}), "tools": []})
        u = m.get("usage", {})
        if u.get("output_tokens", 0) > e["usage"].get("output_tokens", 0):
            e["usage"] = u
        e["tools"] += [c for c in m.get("content", []) if c.get("type") == "tool_use"]
    return sorted(out.values(), key=lambda e: e["t"])


def ctx(u):
    return u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0)


def total(msgs):
    return sum(ctx(m["usage"]) + m["usage"].get("output_tokens", 0) for m in msgs)


def is_handoff_read(tool):
    i = tool.get("input", {})
    if tool["name"] in ("ToolSearch", "Skill"):
        return True
    if tool["name"] == "Read":
        return bool(HANDOFF.search(i.get("file_path", "")))
    if tool["name"] == "Bash":
        cmd = i.get("command", "")
        return bool(READ_CMD.match(cmd) and HANDOFF.search(cmd))
    return False


def cold_start(recs):
    t0 = min(ts(r["timestamp"]) for r in recs if r.get("timestamp"))
    for m in messages(recs):
        if any(not is_handoff_read(t) for t in m["tools"]):
            return round(m["t"] - t0, 1)
    return None


def measure(bench, run, sid, wall):
    main_path = glob.glob(os.path.expanduser(f"~/.claude/projects/*/{sid}.jsonl"))[0]
    msgs = messages(load(main_path))
    subs = sorted(glob.glob(os.path.join(main_path[:-6], "subagents", "agent-*.jsonl")))
    sub_recs = [load(p) for p in subs]
    edits = [
        t["input"].get("file_path", "")
        for m in msgs
        for t in m["tools"]
        if t["name"] in ("Edit", "Write", "NotebookEdit") and not EXEMPT_WRITE.search(t["input"].get("file_path", ""))
    ]
    bash_w = [t["input"].get("command", "")[:160] for m in msgs for t in m["tools"] if bash_writes(t)]
    colds = [c for c in (cold_start(r) for r in sub_recs) if c is not None]
    tokens = total(msgs) + sum(total(messages(r)) for r in sub_recs)
    out = {
        "run": run,
        "wall_s": int(wall),
        "M1_ctx_first": ctx(msgs[0]["usage"]),
        "M1_ctx_last": ctx(msgs[-1]["usage"]),
        "M1_growth": ctx(msgs[-1]["usage"]) - ctx(msgs[0]["usage"]),
        "M1_peak_growth": max(ctx(m["usage"]) for m in msgs) - ctx(msgs[0]["usage"]),
        "M2_main_edits": len(edits) + len(bash_w),
        "M2_files": sorted(set(edits)),
        "M2_bash_writes": bash_w,
        "workers": len(sub_recs),
        "M3_cold_starts": colds,
        "M3_median": statistics.median(colds) if colds else None,
        "M5_tokens": tokens,
    }
    rev = os.path.join(bench, "logs", f"{run}.review.json")
    if os.path.exists(rev):
        try:
            so = json.load(open(rev)).get("structured_output") or {}
            acs = so.get("ac", [])
            out["M4_ac"] = f"{sum(a['verdict'] == 'MET' for a in acs)}/{len(acs)} MET"
            sev = [f["severity"] for f in so.get("findings", [])]
            out["M4_findings"] = {s: sev.count(s) for s in ("Critical", "High", "Medium", "Low")}
        except (ValueError, KeyError, TypeError) as e:
            out["M4_error"] = repr(e)
    return out


def main():
    bench = sys.argv[1]
    want = set(sys.argv[2:])
    for line in open(os.path.join(bench, "logs", "runs.tsv")):
        run, sid, wall, _base = line.rstrip("\n").split("\t")
        if not want or run in want:
            print(json.dumps(measure(bench, run, sid, wall), ensure_ascii=False))


if __name__ == "__main__":
    main()
