#!/usr/bin/env python3
"""벤치마크 run의 transcript를 계측해 M1~M5를 낸다 (goal.md 검증 레시피 R4).

usage: metrics.py <BENCH_DIR> [run id ...]   (run id 생략 시 runs.tsv 전체)
"""
import ast
import glob
import json
import os
import re
import shlex
import statistics
import sys
from datetime import datetime

HANDOFF = re.compile(r"digest|state\.md|_feature_draft_|/references/|SKILL\.md|/workers/")
READ_CMD = re.compile(r"^\s*(cat|sed|head|tail|less|wc)\b")
# Only literal targets are resolved; no shell execution or variable/dataflow evaluation.
ALLOWED_DIRS = ("_sdd/goal/", "_sdd/implementation/", "_sdd/work_log/")


def target_write(target, root):
    """True: target write, False: outside/allowed, None: unresolved literal path."""
    if not target or re.search(r"[$`*?{}\[\]~]", target):
        return None
    def normalize(path):
        path = os.path.normpath(path)
        return path[8:] if path.startswith("/private/tmp/") else path
    root = normalize(os.path.abspath(root))
    path = normalize(os.path.join(root, target))
    relative = os.path.relpath(path, root)
    if relative == ".." or relative.startswith("../"):
        return False
    return not (relative in ("digest.md", "state.md") or relative.startswith(ALLOWED_DIRS))


def python_targets(source):
    """Extract literal open/Path writes; arbitrary Python remains unverified."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    targets = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name) and node.func.id == "open":
            mode = node.args[1] if len(node.args) > 1 else next(
                (k.value for k in node.keywords if k.arg == "mode"), None)
            if not isinstance(mode, ast.Constant) or not isinstance(mode.value, str) or not any(c in mode.value for c in "wax+"):
                continue
            path = node.args[0] if node.args else None
        elif isinstance(node.func, ast.Attribute) and node.func.attr in ("write_text", "write_bytes"):
            receiver = node.func.value
            if not (isinstance(receiver, ast.Call) and isinstance(receiver.func, ast.Name) and receiver.func.id == "Path"):
                continue
            path = receiver.args[0] if receiver.args else None
        else:
            continue
        targets.append(path.value if isinstance(path, ast.Constant) and isinstance(path.value, str) else None)
    return targets


def bash_writes(tool, root):
    """Return (confirmed write, unknown reasons) for one Bash tool call.

    shlex only tokenizes. Unsupported execution/syntax is unknown, never a PASS.
    """
    raw = tool["input"].get("command", "")
    reasons, targets = [], []
    # One simple heredoc: preserve its command header, remove only its body.
    heredoc = re.search(r"<<(-?)\s*(['\"]?)(\w+)\2([^\n]*)\n(.*?)\n\3(?:\n|$)", raw, re.S)
    body = None
    if heredoc:
        body = heredoc.group(5)
        if not heredoc.group(2) and ("$" in body or "`" in body):
            reasons.append("unquoted heredoc expansion")
        raw = raw[:heredoc.start()] + heredoc.group(4) + "\n" + raw[heredoc.end():]
    # shlex loses quoted-operator provenance and consumes comment newlines.
    # Keep these forms unverified instead of attempting a shell grammar.
    if "#" in raw:
        return False, ["shell comment boundary is unverified"]
    if re.search(r"(['\"])[;&|<>]+\1|\\[;&|<>]", raw):
        return False, ["quoted or escaped shell operator is unverified"]
    if "$" in raw or "`" in raw:
        reasons.append("shell expansion or substitution")
    try:
        lexer = shlex.shlex(raw, posix=True, punctuation_chars=";&|<>\n")
        lexer.whitespace = " \t\r"
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return False, ["unsupported shell quoting"]
    segments, segment = [], []
    for token in tokens + [";"]:
        if token in (";", "&&", "||", "|", "\n"):
            segments.append(segment)
            segment = []
        else:
            segment.append(token)
    cwd_unknown = any(seg and seg[0] == "cd" for seg in segments)
    for segment in segments:
        words, i = [], 0
        while i < len(segment):
            token = segment[i]
            if token in (">", ">>", "<", ">&", "&>") and i + 1 < len(segment):
                destination = segment[i + 1]
                if token != "<" and not (token == ">&" and destination.isdigit()):
                    targets.append(destination)
                i += 2
            else:
                words.append(token)
                i += 1
        if not words:
            continue
        command, args = words[0], words[1:]
        if command in ("python", "python3"):
            reasons.append("Python execution beyond literal write targets")
            source = args[1] if len(args) == 2 and args[0] == "-c" else body
            if source is not None:
                targets.extend(python_targets(source))
        elif command in ("cp", "mv") and len(args) == 2 and not any(a.startswith("-") for a in args):
            targets.extend(args if command == "mv" else args[-1:])
        elif command in ("tee", "touch", "rm") and args and not any(a.startswith("-") for a in args):
            targets.extend(args)
        elif command == "sed" and len(args) == 4 and args[:2] == ["-i", ""]:
            targets.append(args[-1])
            reasons.append("sed script effects beyond literal target")
        elif command == "git" and args and args[0] in ("diff", "status", "show", "log", "rev-parse") and not any(a.startswith(("--output", "--ext-diff", "--textconv")) for a in args):
            pass
        elif command in ("cat", "echo", "printf", "pwd", "head", "tail", "wc", "ls", "true", "false", "test", "["):
            pass
        else:
            reasons.append("unsupported command or arguments")
        if any(t and all(c in ";&|<>\n" for c in t) for t in words):
            reasons.append("unsupported shell operator")
    confirmed = False
    for target in targets:
        result = None if cwd_unknown and target and not os.path.isabs(target) else target_write(target, root)
        if result is None:
            reasons.append("unresolved write target or working directory")
        confirmed |= result is True
    return confirmed, sorted(set(reasons))


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
    root = os.path.join(bench, f"t-{run}")
    edits, bash_w, unknown = [], [], []
    for index, tool in enumerate((t for m in msgs for t in m["tools"]), 1):
        name, inputs = tool["name"], tool["input"]
        if name in ("Edit", "Write", "NotebookEdit"):
            path = inputs.get("file_path", inputs.get("notebook_path", ""))
            result = target_write(path, root)
            if result is True:
                edits.append(path)
            elif result is None:
                unknown.append({"tool_index": index, "tool": name, "reasons": ["unresolved write target"]})
        elif name == "Bash":
            written, reasons = bash_writes(tool, root)
            # Transcript index locates evidence without copying command payloads/secrets.
            if written:
                bash_w.append({"tool_index": index})
            if reasons:
                unknown.append({"tool_index": index, "tool": name, "reasons": reasons})
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
        "M2_unknown": len(unknown),
        "M2_unknown_commands": unknown,
        "M2_status": "FAIL" if edits or bash_w else "UNVERIFIED" if unknown else "PASS",
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
