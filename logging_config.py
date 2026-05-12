"""Centralized logging configuration for the linuxsyncpy package."""
from pathlib import Path
import logging
import os


LOG_FILE_NAME = 'linuxsyncpy_run.log'
DEBUG_ENV_VAR = 'LINUXSYNCPY_DEBUG'
DEBUG_ENABLED = False


def configure_logging(debug: bool | None = None) -> None:
    global DEBUG_ENABLED
    if debug is None:
        debug = os.environ.get(DEBUG_ENV_VAR, '').strip().lower() in {'1', 'true', 'yes', 'on'}
    DEBUG_ENABLED = bool(debug)

    root = Path(__file__).resolve().parent
    log_file = root / LOG_FILE_NAME

    handlers = [logging.StreamHandler()]
    try:
        fh = logging.FileHandler(log_file, encoding='utf-8')
        handlers.append(fh)
    except Exception:
        # if file handler cannot be created, just use stream handler
        pass

    level = logging.DEBUG if DEBUG_ENABLED else logging.INFO
    logging.basicConfig(
        level=level,
        format='[%(asctime)s] %(levelname)s %(name)s: %(message)s',
        handlers=handlers,
    )


def set_debug(enabled: bool) -> None:
    global DEBUG_ENABLED
    DEBUG_ENABLED = bool(enabled)
    root_logger = logging.getLogger()
    level = logging.DEBUG if DEBUG_ENABLED else logging.INFO
    root_logger.setLevel(level)
    for handler in root_logger.handlers:
        handler.setLevel(level)
    root_logger.debug(f'set_debug enabled={DEBUG_ENABLED}')


def is_debug_enabled() -> bool:
    return DEBUG_ENABLED


# Configure immediately on import
configure_logging()
