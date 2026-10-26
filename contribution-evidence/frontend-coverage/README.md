# Frontend coverage diagnostics: local evidence

Evidence for [Oppia issue 22583](https://github.com/oppia/oppia/issues/22583).
The proposed source change is on `fix/frontend-uncovered-line-diagnostics`
(commit `09c508b`). This evidence branch is for the fork only.

[Download the video](demo.mp4?raw=true), or play the captured terminal output
with `asciinema play demo.cast`.

The video renders actual local command output captured before and after the
change. It demonstrates the coverage checker with the included LCOV fixture;
it does not represent a browser session or a full frontend test run. Line 2
is covered; lines 7 and 12 have zero hits. Both runs correctly exit 1, and
the patched checker additionally prints `Uncovered lines: 7, 12`.

To reproduce with Oppia's Python dependencies installed, run these commands
from this checkout's root:

```sh
python contribution-evidence/frontend-coverage/record-oppia-coverage.py before
python contribution-evidence/frontend-coverage/record-oppia-coverage.py after
```

Both commands intentionally exit 1 because the fixture has uncovered lines.
The baseline is commit `70b81c3901058b87a69ebbe372d3bcb6e6dcdaef`.
To capture fresh output and render the video, run the same script without
arguments on Linux with Pillow, ffmpeg and DejaVu Sans Mono installed.

Validation of the proposed change:

- All 21 tests in `scripts.check_frontend_test_coverage_test` passed using
  Oppia's backend runner with Python 3.12.13. Local Redis was isolated from
  the existing service.
- The changed checker has 100% line and branch coverage: 93 statements,
  42 branches, no misses or partial branches.
- Pylint, pycodestyle and Black passed for both changed files. Oppia's mypy
  runner passed for `scripts/check_frontend_test_coverage.py`.
- The full application test suite was not run. The targeted backend run's
  aggregate application coverage gate failed because it also measures other
  imported modules; the focused checker coverage report passed at 100%.
