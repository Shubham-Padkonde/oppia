"""Run Oppia's test runner with a separate Redis listener for this checkout."""
import os
import socket
import sys
from pathlib import Path

repo = Path('/home/shubham12/gsoc-evidence/oppia')
scratch = Path(__file__).resolve().parent
os.chdir(repo)
sys.path.insert(0, str(repo))
os.environ['REDIS_HOST'] = '127.0.0.1'
os.environ['CLOUDSDK_CONFIG'] = '/tmp/codex-oppia-gcloud-config'
os.environ['CLOUDSDK_PYTHON'] = sys.executable
os.environ['CLOUDSDK_CORE_DISABLE_USAGE_REPORTING'] = 'true'

with socket.socket() as probe:
    if probe.connect_ex(('127.0.0.1', 6379)) == 0:
        raise RuntimeError('The dedicated Redis endpoint is already in use.')

from scripts import common, run_backend_tests

data_dir = scratch / 'oppia-redis-data'
data_dir.mkdir(exist_ok=True)
redis_config = scratch / 'oppia-test-redis.conf'
redis_config.write_text(
    'bind 127.0.0.1\nport 6379\ndaemonize no\nsave ""\nappendonly no\n'
    f'dir {data_dir}\n', encoding='utf-8'
)
redis_cli = scratch / 'oppia-redis-cli.sh'
redis_cli.write_text(
    f'#!/bin/sh\nexec "{common.REDIS_CLI_PATH}" -h 127.0.0.1 "$@"\n',
    encoding='utf-8'
)
redis_cli.chmod(0o755)
common.REDIS_CONF_PATH = str(redis_config)
common.REDIS_CLI_PATH = str(redis_cli)
common.REDIS_DUMP_PATH = str(data_dir / 'dump.rdb')
run_backend_tests.main(sys.argv[1:])
