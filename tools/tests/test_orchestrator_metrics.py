"""M2 regression fixtures use literal transcripts, never execute their commands."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[2] / '_sdd/goal/2026-10-04_orchestrator_harness_redesign/bench/metrics.py'
spec = importlib.util.spec_from_file_location('orchestrator_metrics', SOURCE)
metrics = importlib.util.module_from_spec(spec)
spec.loader.exec_module(metrics)
ROOT = '/tmp/bench/t-87-new-1'


def tool(name, **kwargs):
    return {'type': 'tool_use', 'name': name, 'input': kwargs}


def record(ident, second, tools, tokens):
    return {'type': 'assistant', 'timestamp': f'2026-10-04T00:00:{second:02d}Z',
            'message': {'id': ident, 'usage': {'input_tokens': tokens, 'output_tokens': 2}, 'content': tools}}


class MetricsTests(unittest.TestCase):
    def measure(self, *tools):
        records = [record('first', 0, [], 10), record('last', 3, list(tools), 20)]
        with patch.object(metrics.glob, 'glob', side_effect=[['/fixture/main.jsonl'], []]), \
                patch.object(metrics, 'load', return_value=records), \
                patch.object(metrics.os.path, 'exists', return_value=False):
            return metrics.measure('/tmp/bench', '87-new-1', 'fixture', '12')

    def test_confirmed_shell_writes(self):
        commands = [
            'echo x > notes.md', 'echo x > "notes.md"',
            "cat <<'EOF' > notes.md\nx\nEOF", f'echo x > {ROOT}/notes.md',
            f'echo x > /private{ROOT}/notes.md',
            "python3 -c \"open('notes.md', 'w').write('x')\"",
            "python3 <<'PYCODE'\nopen('notes.md', 'w').write('x')\nPYCODE",
            "python3 -c \"from pathlib import Path; Path('notes.md').write_text('x')\"",
            'cp /tmp/scratch.md notes.md', 'tee notes.md', 'touch notes.md',
            "sed -i '' 's/a/b/' notes.md", 'rm notes.md', 'mv notes.md /tmp/scratch.md',
            'echo x > src/digest_helpers.py', 'echo x > src/state.md',
            'echo x > _sdd/implementation/../../notes.md',
        ]
        for command in commands:
            with self.subTest(command=command):
                self.assertEqual(self.measure(tool('Bash', command=command))['M2_main_edits'], 1)

    def test_outside_and_allowed_are_not_writes(self):
        commands = [
            'cp notes.md /tmp/scratch.md', 'echo x > /tmp/scratch.md',
            f'echo x > {ROOT}-other/notes.md', 'git diff -- notes.md',
            'cat notes.md', 'echo x > _sdd/implementation/run/digest.md',
            'echo x > _sdd/goal/run/result.md', 'echo x > _sdd/work_log/2026-10-04.md',
            'echo x > /dev/null', "cat <<'EOF'\n> notes.md\nEOF",
        ]
        for command in commands:
            with self.subTest(command=command):
                out = self.measure(tool('Bash', command=command))
                self.assertEqual(out['M2_main_edits'], 0)
                self.assertEqual(out.get('M2_status'), 'PASS')

    def test_direct_writes_use_root_relative_boundary(self):
        for path, expected in [(f'{ROOT}/notes.md', 1), (f'/private{ROOT}/notes.md', 1),
                               ('/tmp/scratch.md', 0), (f'{ROOT}/src/digest.py', 1),
                               (f'{ROOT}/src/state.md', 1),
                               (f'{ROOT}/_sdd/implementation/run/state.md', 0)]:
            with self.subTest(path=path):
                self.assertEqual(self.measure(tool('Write', file_path=path))['M2_main_edits'], expected)
        self.assertEqual(self.measure(tool('NotebookEdit', notebook_path=f'{ROOT}/n.ipynb'))['M2_main_edits'], 1)

    def test_unknown_and_mixed_commands_preserve_evidence(self):
        for command in ['bash helper.sh', './helper.sh', 'python3 helper.py',
                        'echo x > "$TARGET"', "python3 -c \"open(target, 'w').write('x')\"",
                        'cd other && echo x > notes.md', 'find . -exec sh helper.sh \\;',
                        'echo $(./helper.sh)', 'git checkout main']:
            with self.subTest(command=command):
                out = self.measure(tool('Bash', command=command))
                self.assertEqual(out.get('M2_unknown'), 1)
                self.assertEqual(out.get('M2_status'), 'UNVERIFIED')
                self.assertTrue(out.get('M2_unknown_commands'))
        out = self.measure(tool('Bash', command='echo x > notes.md && ./helper.sh'))
        self.assertEqual(out['M2_main_edits'], 1)
        self.assertEqual(out.get('M2_unknown'), 1)
        self.assertEqual(out.get('M2_status'), 'FAIL')
        self.assertTrue(out.get('M2_unknown_commands'))

    def test_delta_literal_boundaries_and_unknown_syntax(self):
        for path in ['digest.md', 'state.md', '_sdd/goal/run/a.md']:
            self.assertIs(metrics.target_write(path, '/private' + ROOT), False)
        for path in ['', '$OUT', '*.md', '~/notes.md']:
            self.assertIsNone(metrics.target_write(path, ROOT))
        for command in ['echo "unfinished', 'echo x >', 'cat <<EOF\n$(./helper.sh)\nEOF',
                        'cp -r source /tmp/scratch', 'git diff --output=notes.md',
                        "sed -i '' 'w notes.md' /tmp/scratch.md",
                        "python3 -c 'bad syntax !'", "python3 -c \"open('notes.md')\"",
                        "python3 -c \"handle.write_text('x')\""]:
            with self.subTest(command=command):
                self.assertEqual(self.measure(tool('Bash', command=command)).get('M2_status'), 'UNVERIFIED')
        for command in ['cat < notes.md', 'echo x 2>&1', '> /tmp/scratch.md']:
            with self.subTest(command=command):
                self.assertEqual(self.measure(tool('Bash', command=command)).get('M2_status'), 'PASS')
        for command in ['echo x >> notes.md', 'echo x &> notes.md',
                        "python3 -c \"open('notes.md', mode='a')\"",
                        "python3 -c \"Path('notes.md').write_bytes(b'x')\""]:
            with self.subTest(command=command):
                self.assertEqual(self.measure(tool('Bash', command=command))['M2_main_edits'], 1)
        out = self.measure(tool('Edit', file_path='$OUT'))
        self.assertEqual(out.get('M2_unknown'), 1)
        self.assertEqual(out.get('M2_status'), 'UNVERIFIED')
        self.assertEqual(out['M2_unknown_commands'][0]['tool_index'], 1)

    def test_comments_do_not_hide_following_commands(self):
        for command in ['echo ok # comment\ntouch notes.md',
                        'echo ok # comment\n./helper.sh']:
            with self.subTest(command=command):
                out = self.measure(tool('Bash', command=command))
                self.assertEqual(out.get('M2_status'), 'UNVERIFIED')
                self.assertEqual(out.get('M2_unknown'), 1)
                self.assertTrue(out.get('M2_unknown_commands'))

    def test_quoted_or_escaped_operators_are_not_confirmed_redirects(self):
        for command in ["echo '>' notes.md", 'echo ">" notes.md',
                        r'echo \> notes.md', "echo '>>' notes.md",
                        "echo ';' notes.md"]:
            with self.subTest(command=command):
                out = self.measure(tool('Bash', command=command))
                self.assertEqual(out['M2_main_edits'], 0)
                self.assertEqual(out.get('M2_status'), 'UNVERIFIED')
                self.assertEqual(out.get('M2_unknown'), 1)

    def test_other_metrics_and_clean_pass(self):
        out = self.measure(tool('Bash', command='git diff -- notes.md'))
        self.assertEqual(out.get('M2_status'), 'PASS')
        self.assertEqual(out.get('M2_unknown'), 0)
        self.assertEqual({k: out[k] for k in ['wall_s', 'M1_ctx_first', 'M1_ctx_last', 'M1_growth',
                                             'M1_peak_growth', 'workers', 'M3_cold_starts', 'M3_median', 'M5_tokens']},
                         dict(wall_s=12, M1_ctx_first=10, M1_ctx_last=20, M1_growth=10,
                              M1_peak_growth=10, workers=0, M3_cold_starts=[], M3_median=None, M5_tokens=34))


if __name__ == '__main__':
    unittest.main()
