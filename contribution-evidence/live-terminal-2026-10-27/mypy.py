"""Capture actual MyPy behavior on a small reproducible import example."""
import os
import shlex
from pathlib import Path
import subprocess
import sys
import tempfile

scratch = Path(__file__).resolve().parent
repo = Path('/home/shubham12/gsoc-evidence/oppia')
os.chdir(repo)
sys.path.insert(0, str(repo))
from scripts import run_mypy_checks

lines = ['Oppia #23034: targeted MyPy diagnostics',
         'Captured output from real MyPy invocations on temporary fixtures.', '']
with tempfile.TemporaryDirectory() as directory:
    fixture = Path(directory)
    dependency = fixture / 'dependency.py'
    target = fixture / 'target.py'
    config = fixture / 'mypy.ini'
    config.write_text('[mypy]\nstrict = True\ncache_dir = ' + str(fixture / 'cache') + '\n')
    dependency.write_text('unrelated_error: int = "wrong"\ndef increment(value: int) -> int:\n    return value + 1\n')
    target.write_text('from dependency import increment\nresult: int = increment(1)\n')
    run_mypy_checks.CONFIG_FILE_PATH = str(config)
    command = run_mypy_checks.get_mypy_cmd([str(target)])

    def capture(label, args, expected):
        print(label, flush=True)
        print(shlex.join(args), flush=True)
        result = subprocess.run(args, text=True, capture_output=True, cwd=repo)
        print(result.stdout + result.stderr, end='', flush=True)
        print('Exit code:', result.returncode, flush=True)
        assert result.returncode == expected, result.stdout + result.stderr
        lines.extend([label, (result.stdout + result.stderr).replace(str(fixture) + '/', ''), 'Exit code: ' + str(result.returncode), ''])

    capture('Before: a correct target reports an unrelated imported-file error',
            [arg for arg in command if arg != '--follow-imports=silent'], 1)
    capture('After: the same correct target passes', command, 0)
    target.write_text('from dependency import increment\nresult: int = increment("wrong")\n')
    capture('After: a wrong argument still fails against the imported signature', command, 1)
    capture('After: explicitly requested dependency errors remain visible',
            run_mypy_checks.get_mypy_cmd([str(target), str(dependency)]), 1)

lines.extend(['Full-repository checks keep the existing import behavior.',
              'This demonstrates diagnostic scope, not a performance improvement.'])
(scratch / 'oppia-scoped-mypy-evidence.txt').write_text('\n'.join(lines), encoding='utf-8')
