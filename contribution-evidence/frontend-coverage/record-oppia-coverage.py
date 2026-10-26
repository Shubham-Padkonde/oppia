"""Record real checker output and render that terminal transcript to video."""
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import textwrap
import time

root = Path(__file__).resolve().parents[2]
repo = root
scratch = Path(__file__).resolve().parent
fixture = scratch / 'example.info'

if len(sys.argv) > 1:
    baseline = subprocess.check_output(
        ['git', 'show', '70b81c3901058b87a69ebbe372d3bcb6e6dcdaef:scripts/check_frontend_test_coverage.py'], cwd=repo
    )
    (scratch / 'oppia-coverage-baseline.py').write_bytes(baseline)
    os.chdir(repo)
    sys.path.insert(0, str(repo))
    if sys.argv[1] == 'before':
        spec = importlib.util.spec_from_file_location(
            'baseline_checker', scratch / 'oppia-coverage-baseline.py'
        )
        checker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(checker)
    else:
        from scripts import check_frontend_test_coverage as checker
    checker.LCOV_FILE_PATH = str(fixture)
    checker.check_coverage_changes(['core/templates/example.ts'])
    raise SystemExit(0)

from PIL import Image, ImageDraw, ImageFont

baseline = subprocess.check_output(
    ['git', 'show', '70b81c3901058b87a69ebbe372d3bcb6e6dcdaef:scripts/check_frontend_test_coverage.py'],
    cwd=repo
)
(scratch / 'oppia-coverage-baseline.py').write_bytes(baseline)
events = []
clock = 0.0
events.append([clock, 'o', 'Oppia #22583 | Local LCOV fixture\r\n'
               'Actual command output; both runs should exit 1.\r\n'
               'Fixture: covered line 2; uncovered lines 7 and 12.\r\n\r\n'])
for state in ('before', 'after'):
    clock += 1
    events.append([clock, 'o', f'$ python record-oppia-coverage.py {state}\r\n'])
    started = time.monotonic()
    result = subprocess.run(
        [sys.executable, str(Path(__file__).resolve()), state],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=repo
    )
    clock += time.monotonic() - started
    output = re.sub(r'\x1b\[[0-9;]*m', '', result.stdout.decode())
    events.append([clock, 'o', output.replace('\n', '\r\n')])
    events.append([clock + .1, 'o', f'[exit {result.returncode}]\r\n\r\n'])
    if result.returncode != 1:
        raise RuntimeError(f'Unexpected exit code for {state}')
    clock += 4

cast_path = scratch / 'demo.cast'
header = {'version': 2, 'width': 106, 'height': 30, 'timestamp': int(time.time()),
          'title': 'Oppia frontend coverage: actual before/after output'}
cast_path.write_text('\n'.join(json.dumps(x) for x in [header, *events]) + '\n')
width, height, fps = 1440, 900, 5
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 21)
output_path = scratch / 'demo.mp4'
encoder = subprocess.Popen([
    'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'rawvideo',
    '-pix_fmt', 'rgb24', '-s', f'{width}x{height}', '-r', str(fps), '-i', '-',
    '-an', '-c:v', 'libx264', '-crf', '22', '-pix_fmt', 'yuv420p',
    '-movflags', '+faststart', str(output_path)
], stdin=subprocess.PIPE)
for frame in range(int((clock + 2) * fps)):
    current = frame / fps
    transcript = ''.join(event[2] for event in events if event[0] <= current)
    lines = []
    for line in transcript.replace('\r', '').split('\n'):
        lines.extend(textwrap.wrap(line, width=105, replace_whitespace=False) or [''])
    canvas = Image.new('RGB', (width, height), '#111827')
    draw = ImageDraw.Draw(canvas)
    for index, line in enumerate(lines[-30:]):
        color = '#86efac' if line.startswith('Uncovered lines:') else '#e5e7eb'
        draw.text((32, 32 + index * 28), line, font=font, fill=color)
    encoder.stdin.write(canvas.tobytes())
encoder.stdin.close()
if encoder.wait() != 0:
    raise RuntimeError('Video rendering failed')
print(f'Recorded real before/after output: {output_path}')
