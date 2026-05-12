import logging
import sys
import types
from pathlib import Path
import importlib.util

logger = logging.getLogger('linuxsyncpy.run_preinstall_test')

ROOT = Path(__file__).resolve().parent
TEST_ROOT = Path.home() / 'Documents' / 'test scan'
PACKAGE_NAME = 'unique-test-package-12345'

# Prepare a fake package module to allow relative imports (linuxsyncpy.*)
pkg = types.ModuleType('linuxsyncpy')
pkg.__path__ = [str(ROOT)]
sys.modules['linuxsyncpy'] = pkg

# Helper to load a submodule from file into package namespace
def load_module(name, path):
    full_name = f'linuxsyncpy.{name}'
    spec = importlib.util.spec_from_file_location(full_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[full_name] = module
    spec.loader.exec_module(module)
    return module

# Load modules needed
load_module('utils', ROOT / 'utils.py')
load_module('scanner', ROOT / 'scanner.py')
load_module('installer', ROOT / 'installer.py')
load_module('git', ROOT / 'git.py')
load_module('index', ROOT / 'index.py')

# Run pre_install
# print suppressed
try:
    logger.debug('run_preinstall_test launching pre_install')
    sys.modules['linuxsyncpy.index'].pre_install(package_name=PACKAGE_NAME, root_dir=str(TEST_ROOT), dry_run=False)
    logger.debug('run_preinstall_test pre_install completed')
except Exception as e:
    logger.exception('run_preinstall_test failed')
    raise
