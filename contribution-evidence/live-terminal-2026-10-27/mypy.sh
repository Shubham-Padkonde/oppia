#!/bin/bash
set -euo pipefail
export PATH=/mnt/c/Users/padko/Documents/Codex/2026-10-26/he/work/gsoc-2027/oppia-env/bin:$PATH
cd /home/shubham12/gsoc-evidence/oppia
test "$(git rev-parse HEAD)" = 377edf70224180fcf2bf6a5702507a66467e67a5
PS4='+ '
set -x
whoami
date -u
git rev-parse --short HEAD
python --version
python /mnt/c/Users/padko/Documents/Codex/2026-10-26/he/outputs/oppia-terminal-proof/mypy.py
python /mnt/c/Users/padko/Documents/Codex/2026-10-26/he/outputs/oppia-terminal-proof/backend.py --test_targets scripts.run_mypy_checks_test --skip_install
git status --short
set +x
printf '\nRun finished successfully. Full application suite was not run.\n'
