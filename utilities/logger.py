"""
logger.py
==========================================================
Centralized logging utility for the QA Automation Framework.

- Writes to both console and a timestamped log file inside logs/
- One log file per test execution session
- Provides a get_logger(name) factory so every module/page/test
  gets a properly namespaced logger (e.g. "pages.LoginPage")
==========================================================
"""

import logging
import os
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

# One log file per execution run (session-level), shared across all loggers
_SESSION_TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
LOG_FILE_PATH = LOG_DIR / f"execution_{_SESSION_TIMESTAMP}.log"

_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)-30s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_configured_loggers = {}


def get_logger(name: str = "QAFramework") -> logging.Logger:
    """
    Returns a configured logger instance.

    Args:
        name: Logical name for the logger, typically __name__ or
              a descriptive tag such as "DriverFactory", "LoginPage".

    Returns:
        logging.Logger instance writing to both console and the
        shared session log file under logs/.
    """
    if name in _configured_loggers:
        return _configured_loggers[name]

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False  # avoid duplicate logs via root logger

    if not logger.handlers:
        formatter = logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT)

        # File handler - captures everything (DEBUG+)
        file_handler = logging.FileHandler(LOG_FILE_PATH, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        # Console handler - INFO+ to keep console readable
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    _configured_loggers[name] = logger
    return logger


# ------------------------------------------------------------------
# Convenience helpers for common structured log events
# ------------------------------------------------------------------
def log_test_start(logger: logging.Logger, test_name: str) -> None:
    logger.info("=" * 70)
    logger.info(f"TEST START -> {test_name}")
    logger.info("=" * 70)


def log_test_end(logger: logging.Logger, test_name: str, status: str) -> None:
    logger.info("-" * 70)
    logger.info(f"TEST END   -> {test_name} | STATUS: {status}")
    logger.info("-" * 70)


def log_browser_launch(logger: logging.Logger, browser: str) -> None:
    logger.info(f"BROWSER LAUNCH -> {browser.upper()} driver initialized")


def log_click(logger: logging.Logger, element_desc: str) -> None:
    logger.info(f"CLICK -> {element_desc}")


def log_assertion(logger: logging.Logger, description: str, result: bool) -> None:
    status = "PASSED" if result else "FAILED"
    logger.info(f"ASSERTION [{status}] -> {description}")


def log_exception(logger: logging.Logger, message: str, exc: Exception) -> None:
    logger.error(f"EXCEPTION -> {message} | {type(exc).__name__}: {exc}", exc_info=True)
