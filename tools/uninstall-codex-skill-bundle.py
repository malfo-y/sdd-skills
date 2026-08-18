#!/usr/bin/env python3
"""Remove legacy SDD skill-bundle installs before using the Codex plugin."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import json
import os
import shutil
import sys


MANIFEST_NAME = ".sdd-skill-bundle-manifest.json"
LEGACY_SKILL_NAMES = (
    "discussion",
    "feature-draft",
    "goal-init",
    "guide-create",
    "implementation",
    "implementation-review",
    "investigate",
    "plan-review",
    "pr-review",
    "ralph-loop-init",
    "sdd-autopilot",
    "spec-create",
    "spec-review",
    "spec-rewrite",
    "spec-snapshot",
    "spec-summary",
    "spec-sync",
    "spec-upgrade",
    "write-phased",
)


@dataclass(frozen=True)
class Destinations:
    codex_home: str
    skills_root: str
    agents_root: str


@dataclass(frozen=True)
class Candidate:
    kind: str
    name: str
    path: str
    sources: tuple[str, ...]


class CleanupError(Exception):
    pass


def _codex_home() -> str:
    return os.environ.get("CODEX_HOME", os.path.expanduser("~/.codex"))


def _resolve_destinations(dest: str | None) -> Destinations:
    root = os.path.abspath(os.path.expanduser(dest or _codex_home()))
    if os.path.basename(os.path.normpath(root)) == "skills":
        codex_home = os.path.dirname(root)
        skills_root = root
    else:
        codex_home = root
        skills_root = os.path.join(codex_home, "skills")
    return Destinations(
        codex_home=codex_home,
        skills_root=skills_root,
        agents_root=os.path.join(codex_home, "agents"),
    )


def _validate_entry_name(raw_name: object, field: str) -> str:
    if not isinstance(raw_name, str) or not raw_name:
        raise CleanupError(f"Manifest field '{field}' must contain non-empty strings.")
    if raw_name in (".", "..") or os.path.basename(raw_name) != raw_name:
        raise CleanupError(f"Unsafe manifest entry in '{field}': {raw_name!r}")
    if os.sep in raw_name or (os.altsep is not None and os.altsep in raw_name):
        raise CleanupError(f"Unsafe manifest entry in '{field}': {raw_name!r}")
    return raw_name


def _manifest_path(codex_home: str) -> str:
    return os.path.join(codex_home, MANIFEST_NAME)


def _load_manifest(codex_home: str) -> tuple[dict[str, list[str]], bool]:
    path = _manifest_path(codex_home)
    if not os.path.isfile(path):
        return {"skills": [], "agents": []}, False
    try:
        with open(path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except (json.JSONDecodeError, OSError) as exc:
        raise CleanupError(f"Unable to read bundle manifest: {path}") from exc
    if not isinstance(payload, dict):
        raise CleanupError(f"Bundle manifest must contain a JSON object: {path}")
    manifest: dict[str, list[str]] = {"skills": [], "agents": []}
    for field in manifest:
        values = payload.get(field, [])
        if not isinstance(values, list):
            raise CleanupError(f"Manifest field '{field}' must be an array.")
        manifest[field] = [_validate_entry_name(value, field) for value in values]
    return manifest, True


def _entry_path(root: str, name: str) -> str:
    path = os.path.abspath(os.path.join(root, name))
    if os.path.commonpath((root, path)) != root:
        raise CleanupError(f"Refusing to remove path outside destination root: {path}")
    return path


def _discover_candidates(
    destinations: Destinations,
    manifest: dict[str, list[str]],
) -> list[Candidate]:
    found: dict[tuple[str, str], set[str]] = {}

    def add(kind: str, name: str, root: str, source: str) -> None:
        path = _entry_path(root, name)
        if os.path.lexists(path):
            found.setdefault((kind, name), set()).add(source)

    for name in manifest["skills"]:
        add("skill", name, destinations.skills_root, "manifest")
    for name in manifest["agents"]:
        add("agent", name, destinations.agents_root, "manifest")
    for name in LEGACY_SKILL_NAMES:
        path = _entry_path(destinations.skills_root, name)
        if os.path.isdir(path) and os.path.isfile(os.path.join(path, "SKILL.md")):
            found.setdefault(("skill", name), set()).add("legacy-name")

    candidates = []
    for (kind, name), sources in sorted(found.items()):
        root = destinations.skills_root if kind == "skill" else destinations.agents_root
        candidates.append(
            Candidate(
                kind=kind,
                name=name,
                path=_entry_path(root, name),
                sources=tuple(sorted(sources)),
            )
        )
    return candidates


def _create_backup_root(codex_home: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    base = os.path.join(codex_home, f"legacy-sdd-backup-{stamp}")
    path = base
    suffix = 2
    while os.path.lexists(path):
        path = f"{base}-{suffix}"
        suffix += 1
    os.makedirs(path)
    return path


def _move_candidate(candidate: Candidate, backup_root: str) -> None:
    kind_root = "skills" if candidate.kind == "skill" else "agents"
    destination_root = os.path.join(backup_root, kind_root)
    os.makedirs(destination_root, exist_ok=True)
    shutil.move(candidate.path, os.path.join(destination_root, candidate.name))


def _print_plan(
    destinations: Destinations,
    candidates: list[Candidate],
    manifest_exists: bool,
) -> None:
    print(f"Legacy SDD bundle cleanup under: {destinations.codex_home}")
    if not candidates and not manifest_exists:
        print("- no legacy bundle entries found")
        return
    for candidate in candidates:
        sources = ", ".join(candidate.sources)
        print(f"- {candidate.kind}: {candidate.name} [{sources}]")
    if manifest_exists:
        print(f"- manifest: {MANIFEST_NAME}")


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Remove legacy SDD skill-bundle files before installing the Codex plugin."
    )
    parser.add_argument(
        "--dest",
        help="CODEX_HOME or its skills directory (default: $CODEX_HOME or ~/.codex)",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Move listed entries to a backup; without this flag the command is preview-only",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = _parse_args(argv)
    try:
        destinations = _resolve_destinations(args.dest)
        manifest, manifest_exists = _load_manifest(destinations.codex_home)
        candidates = _discover_candidates(destinations, manifest)
        _print_plan(destinations, candidates, manifest_exists)
        if not candidates and not manifest_exists:
            return 0
        if not args.yes:
            print("Preview only. Re-run with --yes to remove these entries.")
            return 0
        backup_root = _create_backup_root(destinations.codex_home)
        print(f"Backup: {backup_root}")
        for candidate in candidates:
            _move_candidate(candidate, backup_root)
            print(f"- moved {candidate.kind}: {candidate.name}")
        if manifest_exists:
            shutil.move(
                _manifest_path(destinations.codex_home),
                os.path.join(backup_root, MANIFEST_NAME),
            )
            print(f"- moved manifest: {MANIFEST_NAME}")
        print("Restart Codex or open a new task to drop legacy skill copies.")
        return 0
    except CleanupError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
