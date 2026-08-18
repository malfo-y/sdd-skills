from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "uninstall-codex-skill-bundle.py"
REPO_ROOT = SCRIPT.parents[1]


def load_uninstaller():
    spec = importlib.util.spec_from_file_location("uninstall_codex_skill_bundle", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class UninstallCodexSkillBundleTest(unittest.TestCase):
    def run_script(self, codex_home: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--dest", str(codex_home), *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    @staticmethod
    def make_skill(codex_home: Path, name: str) -> Path:
        skill_dir = codex_home / "skills" / name
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(f"---\nname: {name}\n---\n", encoding="utf-8")
        return skill_dir

    def test_default_is_preview_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = Path(tmp)
            legacy = self.make_skill(codex_home, "spec-sync")
            custom = self.make_skill(codex_home, "custom-skill")

            result = self.run_script(codex_home)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Preview only", result.stdout)
            self.assertTrue(legacy.exists())
            self.assertTrue(custom.exists())

    def test_yes_removes_known_legacy_skill_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = Path(tmp)
            legacy = self.make_skill(codex_home, "spec-sync")
            custom = self.make_skill(codex_home, "custom-skill")

            result = self.run_script(codex_home, "--yes")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(legacy.exists())
            self.assertTrue(custom.exists())
            backups = list(codex_home.glob("legacy-sdd-backup-*"))
            self.assertEqual(len(backups), 1)
            self.assertTrue((backups[0] / "skills" / "spec-sync" / "SKILL.md").is_file())

    def test_manifest_removes_managed_skill_agent_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = Path(tmp)
            managed = self.make_skill(codex_home, "retired-sdd-skill")
            custom = self.make_skill(codex_home, "custom-skill")
            agent = codex_home / "agents" / "retired-sdd-agent.toml"
            agent.parent.mkdir(parents=True)
            agent.write_text("name = 'retired-sdd-agent'\n", encoding="utf-8")
            manifest = codex_home / ".sdd-skill-bundle-manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "skills": ["retired-sdd-skill"],
                        "agents": ["retired-sdd-agent.toml"],
                    }
                ),
                encoding="utf-8",
            )

            result = self.run_script(codex_home, "--yes")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(managed.exists())
            self.assertFalse(agent.exists())
            self.assertFalse(manifest.exists())
            self.assertTrue(custom.exists())
            backups = list(codex_home.glob("legacy-sdd-backup-*"))
            self.assertEqual(len(backups), 1)
            self.assertTrue(
                (backups[0] / "skills" / "retired-sdd-skill" / "SKILL.md").is_file()
            )
            self.assertTrue((backups[0] / "agents" / "retired-sdd-agent.toml").is_file())
            self.assertTrue((backups[0] / ".sdd-skill-bundle-manifest.json").is_file())

    def test_unsafe_manifest_entry_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = Path(tmp)
            outside = codex_home.parent / f"{codex_home.name}-outside-skill"
            manifest = codex_home / ".sdd-skill-bundle-manifest.json"
            manifest.write_text(
                json.dumps({"skills": [f"../{outside.name}"], "agents": []}),
                encoding="utf-8",
            )

            result = self.run_script(codex_home, "--yes")

            self.assertEqual(result.returncode, 1)
            self.assertIn("Unsafe manifest entry", result.stderr)
            self.assertTrue(manifest.exists())
            self.assertFalse(outside.exists())

    def test_legacy_names_match_current_plugin_bundle(self) -> None:
        module = load_uninstaller()
        skills_root = REPO_ROOT / "plugins" / "sdd-skills-codex" / "skills"
        plugin_names = {
            path.name
            for path in skills_root.iterdir()
            if path.is_dir() and (path / "SKILL.md").is_file()
        }

        self.assertEqual(set(module.LEGACY_SKILL_NAMES), plugin_names)


if __name__ == "__main__":
    unittest.main()
