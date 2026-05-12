"""Module entrypoint for `python -m linuxsyncpy`.

This routes directly to the CLI preinstall workflow.
"""

import logging

from .cli import main

logger = logging.getLogger('linuxsyncpy.__main__')

if __name__ == "__main__":
    logger.debug('running package entrypoint __main__')
    raise SystemExit(main())
