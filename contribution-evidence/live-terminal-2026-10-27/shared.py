"""Run the dependency-version check on repository and mismatch inputs."""
import os
from pathlib import Path
import sys

scratch = Path(__file__).resolve().parent
repo = Path('/home/shubham12/gsoc-evidence/oppia')
os.chdir(repo)
sys.path.insert(0, str(repo))
from scripts.linters import other_files_linter


class Cache:
    def __init__(self, overrides=None):
        self.overrides = overrides or {}

    def readlines(self, filename):
        return self.overrides.get(filename, (repo / filename).read_text().splitlines())


lines = ['Oppia #22116: shared Python dependency version check',
         'Captured output from the new linter on real and modified inputs.', '']
check = other_files_linter.CustomLintChecksManager(Cache())
result = check.check_shared_python_dependency_versions()
assert not result.failed
lines.extend(['Current repository inputs:', *result.get_report(), ''])
dev_requirements = (repo / 'requirements_dev.in').read_text()
assert 'Pillow==10.1.0' in dev_requirements
dev_requirements = dev_requirements.replace('Pillow==10.1.0', 'Pillow==10.0.0')
check = other_files_linter.CustomLintChecksManager(Cache({
    'requirements_dev.in': dev_requirements.splitlines(),
}))
result = check.check_shared_python_dependency_versions()
assert result.failed
assert any('pillow:' in line for line in result.get_report())
lines.extend(['In-memory fixture: change only development Pillow to 10.0.0:',
              *result.get_report(), '',
              'Repository requirements files were not modified.',
              'This checks declared shared version specifiers; it is not a dependency resolver.'])
text = '\n'.join(lines)
(scratch / 'oppia-shared-dependencies-evidence.txt').write_text(text, encoding='utf-8')
print(text)
