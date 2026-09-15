"""Run the source-native run.sh templates with isolated fake CLIs (no accounts/network)."""

import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "claude": ROOT / ".claude/skills/ralph-loop-init/SKILL.md",
    "codex": ROOT / "plugins/sdd-skills-codex/skills/ralph-loop-init/SKILL.md",
}

FAKE_CLI = '''
from pathlib import Path
import os
import sys

r = Path("ralph")
state = (r / "state.md").read_text()
with (r / "calls").open("a") as f:
    f.write(state.splitlines()[0] + "\\n")
calls = len((r / "calls").read_text().splitlines())
scenario = os.environ["RALPH_TEST_SCENARIO"]
(r / "state.md").write_text(state.replace(state.splitlines()[0], "phase: DONE", 1))
if scenario == "failure" or (scenario == "recover" and calls == 1):
    (r / "action.sh").write_text("echo unsafe > ralph/unsafe\\n")
    sys.exit(7)
if scenario == "action_report":
    (r / "action.sh").write_text(
        "echo action > ralph/action_ran\\n"
        "echo 'Final status: PASS' > ralph/results/final_report.md\\n"
    )
elif scenario != "missing_report":
    status = "PASS" if scenario == "bad_pass" else "STUCK"
    (r / "results/final_report.md").write_text("Final status: " + status + "\\n")
'''



class RalphTemplates(unittest.TestCase):
    def fixture(self, directory, runtime, scenario, max_iterations=4):
        root = Path(directory)
        ralph = root / "ralph"
        ralph.mkdir()
        (ralph / "results").mkdir()
        source = SOURCES[runtime].read_text()
        section = source.split("### Step 6:", 1)[1].split("### Step 7:", 1)[0]
        template = re.search(r"```bash\n(.*?)\n```", section, re.S).group(1) + "\n"
        (ralph / "run.sh").write_text(template)
        (ralph / "state.md").write_text("phase: SETUP\niteration: 0\nnotes: original\n")
        (ralph / "decisions.md").write_text("original decisions\n")
        (ralph / "PROMPT.md").write_text("fixture only\n")
        (ralph / "config.sh").write_text(
            "LLM_TIMEOUT_SECONDS=0\nMAX_LLM_FAILURES=3\nMAX_RUNTIME_MINUTES=1\n"
            f"MAX_ITERATIONS={max_iterations}\n"
        )
        (ralph / "verify.sh").write_text("test -f ralph/action_ran\n")
        binaries = root / "bin"
        binaries.mkdir()
        for cli in ("claude", "codex"):
            executable = binaries / cli
            executable.write_text(f"#!{sys.executable}\n" + FAKE_CLI)
            executable.chmod(0o755)
        sleeper = binaries / "sleep"
        sleeper.write_text("#!/bin/sh\nexit 0\n")
        sleeper.chmod(0o755)
        (binaries / "python3").symlink_to(sys.executable)
        env = dict(os.environ, PATH=f"{binaries}:/usr/bin:/bin", RALPH_TEST_SCENARIO=scenario)
        return root, ralph, env

    def run_loop(self, root, env, *args):
        return subprocess.run(
            ["/bin/bash", "ralph/run.sh", *args], cwd=root, env=env,
            capture_output=True, text=True, timeout=5,
        )

    def test_locked_reset_preserves_owner_artifacts(self):
        for runtime in SOURCES:
            with self.subTest(runtime=runtime), tempfile.TemporaryDirectory() as directory:
                root, ralph, env = self.fixture(directory, runtime, "recover")
                (ralph / "action.sh").write_text("pending action\n")
                (ralph / "results/keep.txt").write_text("owner result\n")
                before = {p.relative_to(ralph): p.read_bytes() for p in ralph.rglob("*") if p.is_file()}
                # The real lock check uses kill -0 and ps; keep a harmless owner alive.
                holder = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(20)", "run.sh"])
                try:
                    lock = ralph / ".ralph.lock.d"
                    lock.mkdir()
                    (lock / "pid").write_text(str(holder.pid))
                    result = self.run_loop(root, env, "--reset")
                    self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertIn("another ralph instance", result.stderr.lower())
                    after = {p: (ralph / p).read_bytes() if (ralph / p).exists() else None for p in before}
                    self.assertEqual(before, after)
                    self.assertEqual((lock / "pid").read_text(), str(holder.pid))
                finally:
                    holder.terminate()
                    holder.wait(timeout=2)

    def test_failed_done_restores_state_and_honors_failure_limit(self):
        for runtime in SOURCES:
            with self.subTest(runtime=runtime), tempfile.TemporaryDirectory() as directory:
                root, ralph, env = self.fixture(directory, runtime, "failure")
                result = self.run_loop(root, env)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertEqual((ralph / "calls").read_text().splitlines(), ["phase: SETUP"] * 3)
                self.assertIn("phase: SETUP", (ralph / "state.md").read_text())
                self.assertIn("iteration: 3", (ralph / "state.md").read_text())
                self.assertFalse((ralph / "action.sh").exists())
                self.assertFalse((ralph / "unsafe").exists())
                self.assertFalse((ralph / ".ralph.lock.d").exists())

    def test_backup_failure_stops_before_cli_and_preserves_current_state(self):
        for runtime in SOURCES:
            with self.subTest(runtime=runtime), tempfile.TemporaryDirectory() as directory:
                root, ralph, env = self.fixture(directory, runtime, "failure")
                stale = "phase: DONE\niteration: 99\nnotes: stale backup\n"
                (ralph / "results/state_backup.md").write_text(stale)
                copier = root / "bin/cp"
                copier.write_text(
                    '#!/bin/sh\n'
                    'if [ "$1" = "ralph/state.md" ] && [ "$2" = "ralph/results/state_backup.md" ]; then\n'
                    '  echo "fixture: backup write failed" >&2\n'
                    '  exit 73\n'
                    'fi\n'
                    'exec /bin/cp "$@"\n'
                )
                copier.chmod(0o755)
                result = self.run_loop(root, env)
                self.assertFalse((ralph / "calls").exists(), result.stdout + result.stderr)
                self.assertEqual(result.returncode, 73, result.stdout + result.stderr)
                self.assertIn("fixture: backup write failed", result.stderr)
                # The loop owns iteration and increments it before taking the backup.
                self.assertEqual(
                    (ralph / "state.md").read_text(),
                    "phase: SETUP\niteration: 1\nnotes: original\n",
                )
                self.assertEqual((ralph / "results/state_backup.md").read_text(), stale)
                self.assertFalse((ralph / ".ralph.lock.d").exists())

    def test_failed_action_is_not_carried_into_successful_retry(self):
        for runtime in SOURCES:
            with self.subTest(runtime=runtime), tempfile.TemporaryDirectory() as directory:
                root, ralph, env = self.fixture(directory, runtime, "recover")
                result = self.run_loop(root, env)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual((ralph / "calls").read_text().splitlines(), ["phase: SETUP"] * 2)
                self.assertTrue((ralph / "results/final_report.md").exists())
                self.assertFalse((ralph / "unsafe").exists())
                self.assertFalse((ralph / "action.sh").exists())

    def test_done_requires_report_and_pass_verification(self):
        for runtime in SOURCES:
            for scenario in ("missing_report", "bad_pass"):
                with self.subTest(runtime=runtime, scenario=scenario), tempfile.TemporaryDirectory() as directory:
                    root, ralph, env = self.fixture(directory, runtime, scenario, max_iterations=1)
                    result = self.run_loop(root, env)
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn("DONE rejected", result.stdout)
                    self.assertIn("phase: ADJUSTING", (ralph / "state.md").read_text())

    def test_action_runs_before_done_gate_and_done_restart_skips_cli(self):
        for runtime in SOURCES:
            with self.subTest(runtime=runtime), tempfile.TemporaryDirectory() as directory:
                root, ralph, env = self.fixture(directory, runtime, "action_report")
                result = self.run_loop(root, env)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertTrue((ralph / "action_ran").exists())
                self.assertTrue((ralph / "results/action_iter1.sh").exists())
                self.assertIn("phase: DONE", (ralph / "state.md").read_text())
                before = (ralph / "state.md").read_bytes()
                result = self.run_loop(root, env)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual((ralph / "calls").read_text().splitlines(), ["phase: SETUP"])
                self.assertEqual((ralph / "state.md").read_bytes(), before)

    def test_unlocked_reset_starts_fresh(self):
        for runtime in SOURCES:
            with self.subTest(runtime=runtime), tempfile.TemporaryDirectory() as directory:
                root, ralph, env = self.fixture(directory, runtime, "complete")
                (ralph / "state.md").write_text("phase: DONE\niteration: 99\n")
                (ralph / "results/old.txt").write_text("old result")
                (ralph / "action.sh").write_text("echo unsafe > ralph/unsafe\n")
                result = self.run_loop(root, env, "--reset")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertFalse((ralph / "results/old.txt").exists())
                self.assertFalse((ralph / "unsafe").exists())
                self.assertIn("iteration: 1", (ralph / "state.md").read_text())
                self.assertIn("Loop reset", (ralph / "decisions.md").read_text())


if __name__ == "__main__":
    unittest.main()
