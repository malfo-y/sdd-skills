#!/usr/bin/env python3
"""Install the Codex skill bundle (skills + agents + config) from a GitHub repo."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import os
import re
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
DEFAULT_CONFIG_PATH = ".codex/config.toml"


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


@dataclass
class Source:
    owner: str
    repo: str
    ref: str
    skills_root: str
    agents_root: str
    config_path: str


@dataclass
class Destinations:
    codex_home: str
    skills_root: str
    agents_root: str
    config_path: str


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
    sparse_paths = [source.skills_root, source.agents_root, source.config_path]
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
            config_path=_validate_relative_path(DEFAULT_CONFIG_PATH),
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
        config_path=_validate_relative_path(DEFAULT_CONFIG_PATH),
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
        config_path=os.path.join(codex_home, "config.toml"),
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


def _install_skill(
    skill_name: str,
    skill_dir: str,
    dest_root: str,
    force: bool,
    dry_run: bool,
) -> str:
    dest_dir = os.path.join(dest_root, skill_name)
    existed_before = os.path.exists(dest_dir)
    if existed_before:
        if not force:
            return "skipped"
        if not dry_run:
            shutil.rmtree(dest_dir)
    if dry_run:
        if existed_before and force:
            return "would replace"
        return "would install"
    os.makedirs(dest_root, exist_ok=True)
    shutil.copytree(skill_dir, dest_dir)
    if existed_before and force:
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
    if existed_before and not force:
        return "skipped"
    if dry_run:
        if existed_before and force:
            return "would replace"
        return "would install"
    os.makedirs(dest_root, exist_ok=True)
    if existed_before:
        os.remove(dest_path)
    shutil.copy2(agent_path, dest_path)
    if existed_before and force:
        return "replaced"
    return "installed"


def _extract_agents_section(config_text: str) -> dict[str, int]:
    match = re.search(r"(?ms)^\[agents\]\s*(.*?)(?=^\[|\Z)", config_text)
    if not match:
        return {}
    body = match.group(1)
    values: dict[str, int] = {}
    for key in ("max_threads", "max_depth"):
        key_match = re.search(rf"(?m)^{key}\s*=\s*(\d+)\s*$", body)
        if key_match:
            values[key] = int(key_match.group(1))
    return values


def _merge_config(existing_text: str | None, incoming_text: str) -> tuple[str, str]:
    incoming_agents = _extract_agents_section(incoming_text)
    if not incoming_agents:
        raise InstallError("Incoming config.toml is missing an [agents] section.")

    if not existing_text:
        return incoming_text, "installed"

    existing_agents = _extract_agents_section(existing_text)
    merged_agents = dict(existing_agents)
    changed = False
    for key, value in incoming_agents.items():
        if existing_agents.get(key) != value:
            merged_agents[key] = value
            changed = True

    if not existing_agents:
        block_lines = ["[agents]"] + [f"{key} = {merged_agents[key]}" for key in sorted(merged_agents)]
        suffix = "" if existing_text.endswith("\n") or not existing_text else "\n"
        merged_text = existing_text + suffix + "\n".join(block_lines) + "\n"
        return merged_text, "updated" if changed else "unchanged"

    def repl(match: re.Match[str]) -> str:
        body = "\n".join(f"{key} = {merged_agents[key]}" for key in sorted(merged_agents))
        return f"[agents]\n{body}\n\n"

    merged_text = re.sub(r"(?ms)^\[agents\]\s*.*?(?=^\[|\Z)", repl, existing_text, count=1)
    return merged_text, "updated" if changed else "unchanged"


def _install_config(
    config_path: str,
    dest_path: str,
    dry_run: bool,
) -> str:
    incoming_text = open(config_path, "r", encoding="utf-8").read()
    existing_text = None
    if os.path.exists(dest_path):
        existing_text = open(dest_path, "r", encoding="utf-8").read()
    merged_text, status = _merge_config(existing_text, incoming_text)
    if dry_run:
        if status == "installed":
            return "would install"
        if status == "updated":
            return "would update"
        return "unchanged"
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as handle:
        handle.write(merged_text)
    return status


def _print_summary(
    skill_results: list[tuple[str, str]],
    agent_results: list[tuple[str, str]],
    config_result: tuple[str, str],
    destinations: Destinations,
    dry_run: bool,
) -> None:
    action_word = "Planned" if dry_run else "Completed"
    print(f"{action_word} bundle install into {destinations.codex_home}")
    print(f"Skills root: {destinations.skills_root}")
    for skill_name, status in skill_results:
        print(f"- {skill_name}: {status}")
    print(f"Agents root: {destinations.agents_root}")
    for agent_name, status in agent_results:
        print(f"- {agent_name}: {status}")
    label, status = config_result
    print(f"Config: {destinations.config_path}")
    print(f"- {label}: {status}")


def _parse_args(argv: list[str]) -> Args:
    parser = argparse.ArgumentParser(
        description="Install the Codex skill bundle (skills + agents + config) into CODEX_HOME."
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
        help="Replace already installed skills instead of skipping them",
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
            config_source = os.path.join(repo_root, source.config_path)
            if not os.path.isfile(config_source):
                raise InstallError(f"Config file not found: {source.config_path}")
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
            config_result = (
                os.path.basename(destinations.config_path),
                _install_config(
                    config_path=config_source,
                    dest_path=destinations.config_path,
                    dry_run=args.dry_run,
                ),
            )
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)
        _print_summary(skill_results, agent_results, config_result, destinations, args.dry_run)
        if not args.dry_run:
            print("Restart Codex to pick up new skills.")
        return 0
    except InstallError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
