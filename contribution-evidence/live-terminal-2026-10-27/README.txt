Fresh local Oppia terminal evidence — 2026-10-27

These recordings capture actual stdout/stderr from a local Bash pseudo-terminal
while the shown commands execute in Ubuntu on WSL. They are terminal-stream
recordings, not screenshots or desktop screen captures. The recorder saves each
output chunk and its monotonic elapsed timestamp as asciicast v2. No text was
retyped into the recordings and no output was substituted afterward.

The GIF and MP4 playback was generated with asciinema agg 1.9.0 and FFmpeg.
Inactive intervals are capped at two seconds in playback; the .cast files retain
the original event timestamps. Playback duration is not a performance measurement.
The recorder and all demonstration/runner scripts are included here.

#23034: mypy-live-2.cast, mypy-live.gif, mypy-live.mp4
Commit: 377edf70224180fcf2bf6a5702507a66467e67a5
The same temporary dependency/target fixture is checked with the targeted
command before and after adding --follow-imports=silent. It also verifies that
wrong imported argument types and explicitly requested dependency errors remain
reported. This compares the command flags; it does not check out a separate
baseline revision. The focused scripts.run_mypy_checks_test suite follows.

#22116: shared-live-1.cast, shared-live.gif, shared-live.mp4
Commit: 11cd2090e6d60f97552482a605d48d8203176c33
The checker runs on the actual requirements inputs, then on an in-memory fixture
changing development Pillow from 10.1.0 to 10.0.0. Repository requirements are
unchanged. The focused scripts.linters.other_files_linter_test suite follows.

Both runs use a separate checkout at /home/shubham12/gsoc-evidence/oppia, the
existing Python 3.12.13 environment, existing Oppia tools, and a symlink to the
installed third_party dependencies. The backend wrapper starts local Redis and
the Datastore emulator through Oppia's own test runner, using local-only test
configuration. The displayed untracked third_party entry is that dependency
symlink. No tracked implementation files were edited during these recordings.

Local reproduction scripts contain absolute paths for this environment; adjust
those paths when replaying the commands elsewhere. The full application suite
was not run. These recordings do not establish new coverage percentages.
