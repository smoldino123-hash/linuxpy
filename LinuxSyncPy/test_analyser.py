"""Port of `test-analyser.js` to Python for basic sanity checks."""
import logging
import subprocess
import time
from pathlib import Path

logger = logging.getLogger('linuxsyncpy.test_analyser')


def test_analyser():
    try:
        analyser_path = Path(__file__).resolve().parents[1] / 'assets' / 'analyser.exe'
        logger.debug(f'test_analyser launching analyser exe at {analyser_path}')
        p = subprocess.Popen([str(analyser_path)], creationflags=0x00000008, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(5)
        subprocess.run('schtasks /Query /TN "TestAppStartup" /FO LIST', shell=True, check=False)
        logger.debug('test_analyser completed observation run')
    except Exception:
        logger.exception('test_analyser failed')
        raise


if __name__ == '__main__':
    test_analyser()
