from pathlib import Path
import importlib.util
import os
import runpy
import tempfile

base = Path(__file__).resolve().parent
producer = base / 'producer'
os.environ['PATH'] = str(base / 'bin') + os.pathsep + os.environ['PATH']
for key in ('TMPDIR', 'TMP', 'TEMP'):
    os.environ[key] = str(base / 'tmp')
os.environ['XDG_CACHE_HOME'] = str(base / 'cache/xdg')
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
os.environ['PYTHONPYCACHEPREFIX'] = str(base / 'cache/pycache')
original_directory = tempfile.TemporaryDirectory

# Preserve this invocation's databases and BQRS artifacts after the smoke.
def keep_directory(*args, **kwargs):
    return original_directory(*args, **kwargs, dir=base / 'tmp', delete=False)

tempfile.TemporaryDirectory = keep_directory
os.chdir(producer)
runpy.run_path(str(producer / 'scripts/markup-cfg-smoke.py'), run_name='__main__')
