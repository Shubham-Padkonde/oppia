"""Record a real local pseudo-terminal stream with its original event timing."""
import argparse
import codecs
import fcntl
import json
import os
import pty
import struct
import termios
import time
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('script')
p.add_argument('output')
a = p.parse_args()
path = Path(a.output)
if path.exists():
    raise SystemExit('Refusing to overwrite a recording: ' + str(path))
started = time.monotonic()
pid, master = pty.fork()
if pid == 0:
    fcntl.ioctl(0, termios.TIOCSWINSZ, struct.pack('HHHH', 36, 130, 0, 0))
    os.environ.update(TERM='xterm-256color', COLUMNS='130', LINES='36')
    os.execv('/bin/bash', ['bash', a.script])
decoder = codecs.getincrementaldecoder('utf-8')('replace')
with path.open('w', encoding='utf-8') as out:
    out.write(json.dumps({'version': 2, 'width': 130, 'height': 36,
                         'timestamp': int(time.time()),
                         'title': 'Live local Oppia test run',
                         'env': {'TERM': 'xterm-256color'}}) + '\n')
    while True:
        try:
            data = os.read(master, 65536)
        except OSError:
            break
        if not data:
            break
        text = decoder.decode(data)
        out.write(json.dumps([time.monotonic() - started, 'o', text]) + '\n')
        out.flush()
        os.write(1, data)
    _, status = os.waitpid(pid, 0)
    code = os.waitstatus_to_exitcode(status)
Path(str(path) + '.result.json').write_text(json.dumps({
    'exit_code': code, 'duration_seconds': time.monotonic() - started,
    'script': str(Path(a.script).resolve()), 'recording': str(path.resolve())
}, indent=2), encoding='utf-8')
raise SystemExit(code)
