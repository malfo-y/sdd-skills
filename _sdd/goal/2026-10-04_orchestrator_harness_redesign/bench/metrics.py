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
# Only literal targets are resolved (plus simple literal assignments); no shell execution or general dataflow.
ALLOWED_DIRS = ("_sdd/goal/", "_sdd/implementation/", "_sdd/work_log/")
# Commands that never write files by themselves (argument checks for the risky ones are in bash_writes).
READ_ONLY = {"cat", "echo", "printf", "pwd", "head", "tail", "wc", "ls", "true", "false", "test", "[",
             "grep", "rg", "jq", "cut", "tr", "diff", "cmp", "date", "basename", "dirname", "stat",
             "file", "du", "mkdir", "type", "which", "uuidgen", "nl", "comm", "sort", "uniq", "find", "sed"}
FIND_ACTIONS = ("-exec", "-execdir", "-ok", "-okdir", "-delete", "-fprint", "-fprint0", "-fprintf", "-fls")
SED_WRITE = re.compile(r"\b[we](\s|$)")
SAFE_PY_CALLS = {"open", "print", "len", "str", "int", "list", "dict", "set", "tuple", "sorted", "enumerate",
                 "range", "min", "max", "sum", "any", "all", "zip", "isinstance", "repr", "Path"}
SAFE_PY_METHODS = {"read", "write", "readlines", "splitlines", "split", "rsplit", "join", "strip", "rstrip",
                   "lstrip", "replace", "startswith", "endswith", "count", "find", "index", "format", "encode",
                   "decode", "lower", "upper", "get", "items", "keys", "values", "append", "extend", "insert",
                   "pop", "update", "sub", "subn", "search", "match", "fullmatch", "findall", "finditer", "group",
                   "groups", "partition", "rpartition", "close", "loads", "dumps", "load", "dump", "compile",
                   "rfind", "setdefault", "sort", "copy", "exit", "exists", "isfile", "isdir", "basename",
                   "dirname", "abspath"}
PATH_METHODS = {"read_text", "read_bytes", "write_text", "write_bytes", "exists", "is_file"}
HEREDOC = re.compile(r"<<(-?)\s*(['\"]?)(\w+)\2([^\n]*)\n(.*?)\n\3(?:\n|$)", re.S)
ASSIGN = re.compile(r"(?:^|[;&|\s])([A-Za-z_]\w*)=(?:'([^']*)'|\"([^\"$`]*)\"|([^\s;&|$`'\"()]+))")


def target_write(target, root):
    """True: target write, False: outside/allowed, None: unresolved literal path."""
    if not target or re.search(r"[$`~]", target):
        return None
    if re.search(r"[*?{}\[\]]", target):
        # A glob can only match inside its literal directory prefix.
        prefix = re.split(r"[*?{}\[\]]", target, maxsplit=1)[0]
        prefix = prefix[:prefix.rfind("/") + 1]
        return False if prefix and target_write(prefix + "x", root) is False else None
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
    """Return (write targets, statically safe). A target is None when unresolved.

    Safe means every call is on a small allowlist, so the only file writes are the extracted ones.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return [], False
    strings, paths = {}, {}

    def literal(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        if isinstance(node, ast.Name):
            return strings.get(node.id)
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            left, right = literal(node.left), literal(node.right)
            return None if left is None or right is None else left + right
        if isinstance(node, ast.JoinedStr):
            plain = lambda v: isinstance(v, ast.FormattedValue) and v.conversion == -1 and not v.format_spec
            parts = [literal(v.value if plain(v) else v) for v in node.values]
            return None if None in parts else "".join(parts)
        return None

    # Single-name assignments in source order: string literals (incl. concatenation) and Path(...) objects.
    for node in sorted((n for n in ast.walk(tree) if isinstance(n, ast.Assign)), key=lambda n: (n.lineno, n.col_offset)):
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            value, name = node.value, node.targets[0].id
            strings.pop(name, None)
            if literal(value) is not None:
                strings[name] = literal(value)
            elif isinstance(value, ast.Call) and isinstance(value.func, ast.Name) and value.func.id == "Path":
                paths[name] = value

    def path_call(receiver):
        if isinstance(receiver, ast.Name):
            receiver = paths.get(receiver.id)
        return receiver if isinstance(receiver, ast.Call) and isinstance(receiver.func, ast.Name) and receiver.func.id == "Path" else None

    def chain_root(node):
        names = []
        while isinstance(node, ast.Attribute):
            names.append(node.attr)
            node = node.value
        return (node.id if isinstance(node, ast.Name) else None), names[::-1]

    targets, safe = [], True
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name):
            safe &= func.id in SAFE_PY_CALLS
            if func.id == "open":
                mode = node.args[1] if len(node.args) > 1 else next(
                    (k.value for k in node.keywords if k.arg == "mode"), None)
                if isinstance(mode, ast.Constant) and isinstance(mode.value, str) and any(c in mode.value for c in "wax+"):
                    targets.append(literal(node.args[0]) if node.args else None)
        elif isinstance(func, ast.Attribute):
            receiver = path_call(func.value)
            if receiver is not None or func.attr in ("write_text", "write_bytes"):
                safe &= func.attr in PATH_METHODS
                if func.attr in ("write_text", "write_bytes"):
                    targets.append(literal(receiver.args[0]) if receiver is not None and receiver.args else None)
                continue
            root, names = chain_root(func.value)
            safe &= func.attr in SAFE_PY_METHODS and root not in ("shutil", "subprocess") and \
                (root != "os" or names[:1] == ["path"])
        else:
            safe = False
    return targets, safe


def _scan(raw):
    """Quote-aware shell flags that shlex cannot report: comment start, escaped operator, expansion."""
    flags, quote, prev, i = set(), None, " ", 0
    while i < len(raw):
        c, nxt = raw[i], raw[i + 1:i + 2]
        if quote == "'":
            quote = None if c == "'" else quote
        elif c == "\\":
            if quote is None and nxt and nxt in ";&|<>":
                flags.add("quoted or escaped shell operator is unverified")
            prev, i = "x", i + 2
            continue
        elif c == '"':
            quote = None if quote else '"'
        elif c == "'" and quote is None:
            quote = "'"
        elif c == "`" or (c == "$" and nxt == "("):
            # Parameter expansion only matters in a command word or write target, which stay unresolved.
            flags.add("shell expansion or substitution")
        elif c == "#" and quote is None and prev in " \t\n;&|(":
            flags.add("shell comment boundary is unverified")
        prev, i = c, i + 1
    return flags


def bash_writes(tool, root):
    """Return (confirmed write, unknown reasons) for one Bash tool call.

    shlex only tokenizes. Unsupported execution/syntax is unknown, never a PASS.
    """
    raw = tool["input"].get("command", "")
    reasons, targets = [], []
    # Simple heredocs: preserve each command header, remove only the bodies. Python reads the body
    # of the heredoc on its own line.
    bodies = []
    while heredoc := HEREDOC.search(raw):
        header, body = raw[raw.rfind("\n", 0, heredoc.start()) + 1:heredoc.start()], heredoc.group(5)
        bodies.append((header, body))
        if not heredoc.group(2) and ("$(" in body or "`" in body):
            reasons.append("unquoted heredoc expansion")
        raw = raw[:heredoc.start()] + heredoc.group(4) + "\n" + raw[heredoc.end():]
    body = next((b for h, b in bodies if "python" in h), bodies[0][1] if bodies else None)
    # Simple literal assignments (NAME=value) are substituted; anything still expanding stays unknown.
    for _ in range(3):
        for m in ASSIGN.finditer(raw):
            value = next(g for g in m.groups()[1:] if g is not None)
            raw = re.sub(r"\$(?:\{" + m.group(1) + r"\}|" + m.group(1) + r"\b)", lambda _m: value, raw)
    flags = _scan(raw)
    # shlex loses quoted-operator provenance and comment boundaries: keep these forms unverified.
    for flag in ("shell comment boundary is unverified", "quoted or escaped shell operator is unverified"):
        if flag in flags:
            return False, [flag]
    if re.search(r"(['\"])[;&|<>]+\1", raw):
        return False, ["quoted or escaped shell operator is unverified"]
    reasons += flags
    try:
        lexer = shlex.shlex(raw, posix=True, punctuation_chars=";&|<>\n")
        lexer.whitespace = " \t\r"
        lexer.whitespace_split = True
        lexer.commenters = ""
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
    cwd = root
    for segment in segments:
        words, i = [], 0
        while i < len(segment):
            token = segment[i]
            if token in (">", ">>", "<", ">&", "&>") and i + 1 < len(segment):
                destination = segment[i + 1]
                if token != "<" and not (token == ">&" and destination.isdigit()):
                    targets.append((cwd, destination))
                i += 2
            else:
                words.append(token)
                i += 1
        while words and re.match(r"[A-Za-z_]\w*=", words[0]):
            words = words[1:]
        if not words:
            continue
        if words[0] == "command" and len(words) > 1 and not words[1].startswith("-"):
            words = words[1:]
        command, args = words[0], words[1:]
        if command.startswith("/"):
            command = os.path.basename(command)
        options = [a for a in args if a.startswith("-")]
        if command == "cd":
            cwd = args[0] if len(args) == 1 and os.path.isabs(args[0]) else None
        elif command in ("python", "python3"):
            source = args[1] if len(args) == 2 and args[0] == "-c" else body if args in ([], ["-"]) else None
            found, safe = python_targets(source) if source is not None else ([], False)
            targets += [(cwd, t) for t in found]
            if not safe:
                reasons.append("Python execution beyond literal write targets")
        elif command in ("cp", "mv") and len(args) == 2 and not options:
            targets += [(cwd, a) for a in (args if command == "mv" else args[-1:])]
        elif command in ("tee", "touch", "rm") and args and not options:
            targets += [(cwd, a) for a in args]
        elif command == "sed" and args[:2] == ["-i", ""]:
            rest, scripts, files = args[2:], [], []
            while rest and (rest[0] == "-e" and len(rest) > 1 or not rest[0].startswith("-")):
                if rest[0] == "-e":
                    scripts.append(rest[1])
                    rest = rest[2:]
                else:
                    (files if scripts else scripts).append(rest.pop(0))
            targets += [(cwd, a) for a in files]
            if rest or not files:
                reasons.append("unsupported command or arguments")
            if any(SED_WRITE.search(x) for x in scripts):
                reasons.append("sed script effects beyond literal target")
        elif command == "chmod" and len(args) >= 2 and not options:
            targets += [(cwd, a) for a in args[1:]]
        elif command == "command" and args[:1] in (["-v"], ["-V"]) or command == "git" and args == ["branch", "--show-current"]:
            pass
        elif command == "git" and args and args[0] in ("diff", "status", "show", "log", "rev-parse", "ls-files", "grep", "cat-file", "check-ignore") and not any(a.startswith(("--output", "--ext-diff", "--textconv")) for a in args):
            pass
        elif command in READ_ONLY and not (
                (command == "find" and any(a in FIND_ACTIONS for a in args))
                or (command == "sed" and (any(a.startswith(("-i", "--in-place")) for a in options)
                                          or any(SED_WRITE.search(a) for a in args if not a.startswith("-"))))
                or (command == "sort" and any(a.startswith(("-o", "--output")) for a in options))
                or (command == "uniq" and len(args) - len(options) > 1)):
            pass
        else:
            reasons.append("unsupported command or arguments")
        if any(t and all(c in ";&|<>\n" for c in t) for t in words):
            reasons.append("unsupported shell operator")
    confirmed = False
    for base, target in targets:
        if target and not os.path.isabs(target):
            target = None if base is None else os.path.join(base, target)
        result = target_write(target, root)
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
