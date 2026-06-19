#!/usr/bin/env python3
"""Install the Codex skill bundle (skills + agents) from a GitHub repo."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import zipfile

DEFAULT_REF = "main"
DEFAULT_REPO = "malfo-y/sdd-skills"
DEFAULT_SKILLS_ROOT = ".codex/skills"
DEFAULT_AGENTS_ROOT = ".codex/agents"
MANIFEST_NAME = ".sdd-skill-bundle-manifest.json"
# "sdd" substring도 "_sdd"를 포섭
PRUNE_KEYWORDS = ("sdd",)


@dataclass
class Args:
    repo: str | None = None
    url: str | None = None
    skills_root: str | None = None
    ref: str = DEFAULT_REF
    dest: str | None = None
    method: str = "auto"
    force: bool = False
    include_hidden: bool = False
    dry_run: bool = False
    prune: bool = True
    prune_yes: bool = False


@dataclass
class Source:
    owner: str
    repo: str
    ref: str
    skills_root: str
    agents_root: str


@dataclass
class Destinations:
    codex_home: str
    skills_root: str
    agents_root: str


class InstallError(Exception):
    pass


def _codex_home() -> str:
    return os.environ.get("CODEX_HOME", os.path.expanduser("~/.codex"))


def _default_dest() -> str:
    return os.path.join(_codex_home(), "skills")


def _tmp_root() -> str:
    base = os.path.join(tempfile.gettempdir(), "codex")
    os.makedirs(base, exist_ok=True)
    return base


def _github_headers(user_agent: str) -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": user_agent,
    }
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _request(url: str, user_agent: str) -> bytes:
    request = urllib.request.Request(url, headers=_github_headers(user_agent))
    with urllib.request.urlopen(request) as response:
        return response.read()


def _parse_github_url(url: str, default_ref: str) -> tuple[str, str, str, str | None]:
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc != "github.com":
        raise InstallError("Only GitHub URLs are supported.")
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2:
        raise InstallError("Invalid GitHub URL.")
    owner, repo = parts[0], parts[1]
    ref = default_ref
    subpath = ""
    if len(parts) > 2:
        if parts[2] in ("tree", "blob"):
            if len(parts) < 4:
                raise InstallError("GitHub URL missing ref or path.")
            ref = parts[3]
            subpath = "/".join(parts[4:])
        else:
            subpath = "/".join(parts[2:])
    return owner, repo, ref, subpath or None


def _validate_relative_path(path: str) -> str:
    normalized = os.path.normpath(path).strip()
    if not normalized or normalized == ".":
        raise InstallError("Path must not be empty.")
    if os.path.isabs(normalized) or normalized.startswith(".."):
        raise InstallError("Path must stay inside the repository.")
    return normalized


def _build_repo_url(owner: str, repo: str) -> str:
    return f"https://github.com/{owner}/{repo}.git"


def _build_repo_ssh(owner: str, repo: str) -> str:
    return f"git@github.com:{owner}/{repo}.git"


def _run_git(args: list[str]) -> None:
    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise InstallError(result.stderr.strip() or "Git command failed.")


def _safe_extract_zip(zip_file: zipfile.ZipFile, dest_dir: str) -> None:
    dest_root = os.path.realpath(dest_dir)
    for info in zip_file.infolist():
        extracted_path = os.path.realpath(os.path.join(dest_dir, info.filename))
        if extracted_path == dest_root or extracted_path.startswith(dest_root + os.sep):
            continue
        raise InstallError("Archive contains files outside the destination.")
    zip_file.extractall(dest_dir)


def _download_repo_zip(owner: str, repo: str, ref: str, dest_dir: str) -> str:
    zip_url = f"https://codeload.github.com/{owner}/{repo}/zip/{ref}"
    zip_path = os.path.join(dest_dir, "repo.zip")
    try:
        payload = _request(zip_url, "codex-skill-bundle-install")
    except urllib.error.HTTPError as exc:
        raise InstallError(f"Download failed: HTTP {exc.code}") from exc
    with open(zip_path, "wb") as handle:
        handle.write(payload)
    with zipfile.ZipFile(zip_path, "r") as zip_file:
        _safe_extract_zip(zip_file, dest_dir)
        top_levels = {name.split("/")[0] for name in zip_file.namelist() if name}
    if not top_levels:
        raise InstallError("Downloaded archive was empty.")
    if len(top_levels) != 1:
        raise InstallError("Unexpected archive layout.")
    return os.path.join(dest_dir, next(iter(top_levels)))


def _git_sparse_checkout(repo_url: str, ref: str, sparse_paths: list[str], dest_dir: str) -> str:
    repo_dir = os.path.join(dest_dir, "repo")
    clone_cmd = [
        "git",
        "clone",
        "--filter=blob:none",
        "--depth",
        "1",
        "--sparse",
        "--single-branch",
        "--branch",
        ref,
        repo_url,
        repo_dir,
    ]
    try:
        _run_git(clone_cmd)
    except InstallError:
        _run_git(
            [
                "git",
                "clone",
                "--filter=blob:none",
                "--depth",
                "1",
                "--sparse",
                "--single-branch",
                repo_url,
                repo_dir,
            ]
        )
    _run_git(["git", "-C", repo_dir, "sparse-checkout", "set", *sparse_paths])
    _run_git(["git", "-C", repo_dir, "checkout", ref])
    return repo_dir


def _prepare_repo(source: Source, method: str, tmp_dir: str) -> str:
    sparse_paths = [source.skills_root, source.agents_root]
    if method in ("download", "auto"):
        try:
            return _download_repo_zip(source.owner, source.repo, source.ref, tmp_dir)
        except InstallError as exc:
            if method == "download":
                raise
            err_msg = str(exc)
            if "HTTP 401" not in err_msg and "HTTP 403" not in err_msg and "HTTP 404" not in err_msg:
                raise
    if method in ("git", "auto"):
        try:
            return _git_sparse_checkout(
                _build_repo_url(source.owner, source.repo),
                source.ref,
                sparse_paths,
                tmp_dir,
            )
        except InstallError:
            return _git_sparse_checkout(
                _build_repo_ssh(source.owner, source.repo),
                source.ref,
                sparse_paths,
                tmp_dir,
            )
    raise InstallError("Unsupported method.")


def _resolve_source(args: Args) -> Source:
    skills_root = args.skills_root
    if args.url:
        owner, repo, ref, url_path = _parse_github_url(args.url, args.ref)
        skills_root = skills_root or url_path or DEFAULT_SKILLS_ROOT
        return Source(
            owner=owner,
            repo=repo,
            ref=ref,
            skills_root=_validate_relative_path(skills_root),
            agents_root=_validate_relative_path(DEFAULT_AGENTS_ROOT),
        )
    repo = args.repo or DEFAULT_REPO
    repo_parts = [part for part in repo.split("/") if part]
    if len(repo_parts) != 2:
        raise InstallError("--repo must be in owner/repo format.")
    return Source(
        owner=repo_parts[0],
        repo=repo_parts[1],
        ref=args.ref,
        skills_root=_validate_relative_path(skills_root or DEFAULT_SKILLS_ROOT),
        agents_root=_validate_relative_path(DEFAULT_AGENTS_ROOT),
    )


def _resolve_destinations(dest: str | None) -> Destinations:
    skills_root = os.path.expanduser(dest or _default_dest())
    normalized = os.path.normpath(skills_root)
    if os.path.basename(normalized) == "skills":
        codex_home = os.path.dirname(normalized)
    else:
        codex_home = normalized
        skills_root = os.path.join(codex_home, "skills")
    return Destinations(
        codex_home=codex_home,
        skills_root=skills_root,
        agents_root=os.path.join(codex_home, "agents"),
    )


def _discover_skills(repo_root: str, skills_root: str, include_hidden: bool) -> list[tuple[str, str]]:
    root_dir = os.path.join(repo_root, skills_root)
    if not os.path.isdir(root_dir):
        raise InstallError(f"Skills root not found: {skills_root}")
    discovered = []
    for entry in sorted(os.listdir(root_dir)):
        if not include_hidden and entry.startswith("."):
            continue
        skill_dir = os.path.join(root_dir, entry)
        if not os.path.isdir(skill_dir):
            continue
        if not os.path.isfile(os.path.join(skill_dir, "SKILL.md")):
            continue
        discovered.append((entry, skill_dir))
    if not discovered:
        raise InstallError(f"No skills found under: {skills_root}")
    return discovered


def _discover_agents(repo_root: str, agents_root: str) -> list[tuple[str, str]]:
    root_dir = os.path.join(repo_root, agents_root)
    if not os.path.isdir(root_dir):
        raise InstallError(f"Agents root not found: {agents_root}")
    discovered = []
    for entry in sorted(os.listdir(root_dir)):
        agent_path = os.path.join(root_dir, entry)
        if os.path.isdir(agent_path):
            continue
        if not entry.endswith(".toml"):
            continue
        discovered.append((entry, agent_path))
    if not discovered:
        raise InstallError(f"No agents found under: {agents_root}")
    return discovered


def _sha256_file(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _dir_signature(root: str) -> list[tuple[str, ...]]:
    signature: list[tuple[str, ...]] = []
    for current_root, dirnames, filenames in os.walk(root):
        dirnames.sort()
        filenames.sort()
        rel_root = os.path.relpath(current_root, root)
        if rel_root == ".":
            rel_root = ""
        signature.append(("dir", rel_root))
        for filename in filenames:
            abs_path = os.path.join(current_root, filename)
            rel_path = os.path.join(rel_root, filename) if rel_root else filename
            signature.append(("file", rel_path, _sha256_file(abs_path)))
    return signature


def _same_skill_dir(src_dir: str, dest_dir: str) -> bool:
    if not os.path.isdir(dest_dir):
        return False
    return _dir_signature(src_dir) == _dir_signature(dest_dir)


def _same_file(src_path: str, dest_path: str) -> bool:
    if not os.path.isfile(dest_path):
        return False
    if os.path.getsize(src_path) != os.path.getsize(dest_path):
        return False
    return _sha256_file(src_path) == _sha256_file(dest_path)


def _remove_existing_path(path: str) -> None:
    if os.path.isdir(path) and not os.path.islink(path):
        shutil.rmtree(path)
        return
    os.remove(path)


def _manifest_path(codex_home: str) -> str:
    return os.path.join(codex_home, MANIFEST_NAME)


def _load_manifest(codex_home: str) -> dict[str, list[str]] | None:
    path = _manifest_path(codex_home)
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (json.JSONDecodeError, OSError):
        return None
    skills = data.get("skills") if isinstance(data, dict) else None
    agents = data.get("agents") if isinstance(data, dict) else None
    return {
        "skills": list(skills) if isinstance(skills, list) else [],
        "agents": list(agents) if isinstance(agents, list) else [],
    }


def _write_manifest(codex_home: str, skill_names: list[str], agent_names: list[str]) -> None:
    os.makedirs(codex_home, exist_ok=True)
    payload = {"skills": sorted(skill_names), "agents": sorted(agent_names)}
    with open(_manifest_path(codex_home), "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")


def _contains_keyword(text: str) -> bool:
    lowered = text.lower()
    return any(keyword in lowered for keyword in PRUNE_KEYWORDS)


def _file_has_keyword(path: str) -> bool:
    if not os.path.isfile(path):
        return False
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as handle:
            return _contains_keyword(handle.read())
    except OSError:
        return False


def _find_skill_orphans(
    skills_root: str,
    source_names: set[str],
    manifest: dict[str, list[str]] | None,
) -> list[str]:
    if not os.path.isdir(skills_root):
        return []
    orphans: list[str] = []
    for entry in sorted(os.listdir(skills_root)):
        path = os.path.join(skills_root, entry)
        if not os.path.isdir(path):
            continue
        if entry in source_names:
            continue
        if manifest is not None:
            if entry in manifest["skills"]:
                orphans.append(entry)
        elif _file_has_keyword(os.path.join(path, "SKILL.md")):
            orphans.append(entry)
    return orphans


def _find_agent_orphans(
    agents_root: str,
    source_names: set[str],
    manifest: dict[str, list[str]] | None,
) -> list[str]:
    if not os.path.isdir(agents_root):
        return []
    orphans: list[str] = []
    for entry in sorted(os.listdir(agents_root)):
        path = os.path.join(agents_root, entry)
        if os.path.isdir(path) or not entry.endswith(".toml"):
            continue
        if entry in source_names:
            continue
        if manifest is not None:
            if entry in manifest["agents"]:
                orphans.append(entry)
        elif _file_has_keyword(path):
            orphans.append(entry)
    return orphans


def _install_skill(
    skill_name: str,
    skill_dir: str,
    dest_root: str,
    force: bool,
    dry_run: bool,
) -> str:
    dest_dir = os.path.join(dest_root, skill_name)
    existed_before = os.path.exists(dest_dir)
    identical = existed_before and _same_skill_dir(skill_dir, dest_dir)
    if existed_before:
        if identical and not force:
            return "unchanged"
        if dry_run:
            return "would replace"
        _remove_existing_path(dest_dir)
    if dry_run:
        return "would install"
    os.makedirs(dest_root, exist_ok=True)
    shutil.copytree(skill_dir, dest_dir)
    if existed_before:
        return "replaced"
    return "installed"


def _install_agent(
    agent_name: str,
    agent_path: str,
    dest_root: str,
    force: bool,
    dry_run: bool,
) -> str:
    dest_path = os.path.join(dest_root, agent_name)
    existed_before = os.path.exists(dest_path)
    identical = existed_before and _same_file(agent_path, dest_path)
    if existed_before and identical and not force:
        return "unchanged"
    if dry_run:
        if existed_before:
            return "would replace"
        return "would install"
    os.makedirs(dest_root, exist_ok=True)
    if existed_before:
        _remove_existing_path(dest_path)
    shutil.copy2(agent_path, dest_path)
    if existed_before:
        return "replaced"
    return "installed"


def _confirm_prune() -> bool:
    answer = input("Prune these orphaned entries? [y/N] ").strip().lower()
    return answer in ("y", "yes")


def _prune_orphans(
    destinations: Destinations,
    source_skill_names: set[str],
    source_agent_names: set[str],
    args: Args,
) -> dict[str, object]:
    manifest = _load_manifest(destinations.codex_home)
    skill_orphans = _find_skill_orphans(destinations.skills_root, source_skill_names, manifest)
    agent_orphans = _find_agent_orphans(destinations.agents_root, source_agent_names, manifest)
    candidates = skill_orphans + agent_orphans
    result: dict[str, object] = {
        "skills": skill_orphans,
        "agents": agent_orphans,
        "pruned": [],
        "status": "none",
    }
    if not candidates:
        return result
    if args.dry_run:
        result["status"] = "would-prune"
        return result
    proceed: bool
    if sys.stdin.isatty():
        for name in candidates:
            print(f"Orphan candidate: {name}")
        proceed = _confirm_prune()
    elif args.prune_yes:
        proceed = True
    else:
        result["status"] = "held-non-tty"
        return result
    if not proceed:
        result["status"] = "declined"
        return result
    for name in skill_orphans:
        _remove_existing_path(os.path.join(destinations.skills_root, name))
    for name in agent_orphans:
        _remove_existing_path(os.path.join(destinations.agents_root, name))
    result["pruned"] = candidates
    result["status"] = "pruned"
    return result


def _print_summary(
    skill_results: list[tuple[str, str]],
    agent_results: list[tuple[str, str]],
    destinations: Destinations,
    dry_run: bool,
    prune_result: dict[str, object] | None = None,
) -> None:
    action_word = "Planned" if dry_run else "Completed"
    print(f"{action_word} bundle install into {destinations.codex_home}")
    print(f"Skills root: {destinations.skills_root}")
    for skill_name, status in skill_results:
        print(f"- {skill_name}: {status}")
    print(f"Agents root: {destinations.agents_root}")
    for agent_name, status in agent_results:
        print(f"- {agent_name}: {status}")
    if prune_result is not None:
        _print_prune_result(prune_result)


def _print_prune_result(prune_result: dict[str, object]) -> None:
    status = prune_result["status"]
    candidates = list(prune_result["skills"]) + list(prune_result["agents"])
    print("Prune:")
    if status == "none":
        print("- no orphaned entries")
        return
    if status == "would-prune":
        for name in candidates:
            print(f"- would prune: {name}")
        return
    if status == "held-non-tty":
        print("- held: non-interactive shell; pass --prune-yes to prune")
        for name in candidates:
            print(f"- candidate: {name}")
        return
    if status == "declined":
        print("- declined by user")
        for name in candidates:
            print(f"- candidate: {name}")
        return
    for name in prune_result["pruned"]:
        print(f"- pruned: {name}")


def _parse_args(argv: list[str]) -> Args:
    parser = argparse.ArgumentParser(
        description="Install the Codex skill bundle (skills + agents) into CODEX_HOME."
    )
    parser.add_argument(
        "--repo",
        default=DEFAULT_REPO,
        help=f"owner/repo (default: {DEFAULT_REPO})",
    )
    parser.add_argument("--url", help="https://github.com/owner/repo[/tree/ref/path]")
    parser.add_argument(
        "--skills-root",
        help=(
            "Repo path that contains skill directories "
            f"(default: {DEFAULT_SKILLS_ROOT}; URL path is used when present)"
        ),
    )
    parser.add_argument("--ref", default=DEFAULT_REF, help=f"Git ref (default: {DEFAULT_REF})")
    parser.add_argument(
        "--dest",
        default=_default_dest(),
        help="Destination skill root or CODEX_HOME root (default: ~/.codex/skills)",
    )
    parser.add_argument(
        "--method",
        choices=["auto", "download", "git"],
        default="auto",
        help="Repo fetch strategy",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace existing skills and agents even when contents are identical",
    )
    parser.add_argument(
        "--include-hidden",
        action="store_true",
        help="Also install skill directories whose names start with '.'",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be installed without copying files",
    )
    parser.add_argument(
        "--prune",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Remove orphaned bundle skills/agents no longer in the source (default: on)",
    )
    parser.add_argument(
        "--prune-yes",
        action="store_true",
        help="Prune orphans without confirmation in non-interactive shells",
    )
    return parser.parse_args(argv, namespace=Args())


def main(argv: list[str]) -> int:
    args = _parse_args(argv)
    try:
        source = _resolve_source(args)
        destinations = _resolve_destinations(args.dest)
        tmp_dir = tempfile.mkdtemp(prefix="skill-bundle-", dir=_tmp_root())
        try:
            repo_root = _prepare_repo(source, args.method, tmp_dir)
            discovered = _discover_skills(repo_root, source.skills_root, args.include_hidden)
            discovered_agents = _discover_agents(repo_root, source.agents_root)
            skill_results: list[tuple[str, str]] = []
            for skill_name, skill_dir in discovered:
                status = _install_skill(
                    skill_name=skill_name,
                    skill_dir=skill_dir,
                    dest_root=destinations.skills_root,
                    force=args.force,
                    dry_run=args.dry_run,
                )
                skill_results.append((skill_name, status))
            agent_results: list[tuple[str, str]] = []
            for agent_name, agent_path in discovered_agents:
                status = _install_agent(
                    agent_name=agent_name,
                    agent_path=agent_path,
                    dest_root=destinations.agents_root,
                    force=args.force,
                    dry_run=args.dry_run,
                )
                agent_results.append((agent_name, status))
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)
        source_skill_names = {name for name, _ in discovered}
        source_agent_names = {name for name, _ in discovered_agents}
        prune_result: dict[str, object] | None = None
        if args.prune:
            prune_result = _prune_orphans(
                destinations,
                source_skill_names,
                source_agent_names,
                args,
            )
        if not args.dry_run:
            manifest_skills = set(source_skill_names)
            manifest_agents = set(source_agent_names)
            if prune_result is not None:
                pruned = set(prune_result["pruned"])
                manifest_skills |= {n for n in prune_result["skills"] if n not in pruned}
                manifest_agents |= {n for n in prune_result["agents"] if n not in pruned}
            else:
                prev = _load_manifest(destinations.codex_home) or {"skills": [], "agents": []}
                manifest_skills |= {
                    n for n in prev["skills"]
                    if n not in source_skill_names
                    and os.path.isdir(os.path.join(destinations.skills_root, n))
                }
                manifest_agents |= {
                    n for n in prev["agents"]
                    if n not in source_agent_names
                    and os.path.isfile(os.path.join(destinations.agents_root, n))
                }
            _write_manifest(
                destinations.codex_home,
                sorted(manifest_skills),
                sorted(manifest_agents),
            )
        _print_summary(
            skill_results,
            agent_results,
            destinations,
            args.dry_run,
            prune_result,
        )
        if not args.dry_run:
            print("Restart Codex to pick up new skills.")
        return 0
    except InstallError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
