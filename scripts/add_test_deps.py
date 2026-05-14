"""Add unique test dependencies to test_install and run installers.

This script uses the installed `linuxsyncpy` package to append a pip and npm
dependency to the `test_install` folder and attempts to install them.
"""
import logging
from pathlib import Path

logging.basicConfig(level=logging.DEBUG)

try:
    from linuxsyncpy import installer
except Exception as exc:
    print('Failed to import linuxsyncpy.installer:', exc)
    raise


def main():
    base = Path(__file__).resolve().parent.parent / 'test_install'
    req = base / 'requirements.txt'
    pkg = base / 'package.json'

    print('Adding pip package colorama==0.4.6 to', req)
    try:
        installer.install_pip_with_package(str(req), 'colorama==0.4.6', dry_run=False)
    except Exception as exc:
        print('pip install step failed:', exc)

    print('Adding npm package axios to', pkg)
    try:
        installer.install_npm_with_package(str(pkg), 'axios', version='^1.4.0', dry_run=False)
    except Exception as exc:
        print('npm install step failed:', exc)


if __name__ == '__main__':
    main()
