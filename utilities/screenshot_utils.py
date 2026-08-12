"""
screenshot_utils.py
==========================================================
Utility for capturing screenshots, primarily used to
automatically capture the browser state whenever a test
fails (wired up via conftest.py's pytest_runtest_makereport
hook).

Filename format: <TestName>_<YYYY-MM-DD>_<HH-MM-SS>.png
==========================================================
"""

import os
import re
from datetime import datetime
from pathlib import Path

from utilities.config_reader import config
from utilities.logger import get_logger

logger = get_logger("ScreenshotUtils")

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class ScreenshotUtils:

    @staticmethod
    def _sanitize_name(name: str) -> str:
        """Remove characters that are unsafe for filenames."""
        return re.sub(r"[^A-Za-z0-9_\-]", "_", name)

    @staticmethod
    def capture_screenshot(driver, test_name: str) -> str:
        """
        Captures a screenshot and saves it under screenshots/.

        Args:
            driver: active Selenium WebDriver instance.
            test_name: logical name of the test (used in filename).

        Returns:
            Absolute path to the saved screenshot, or None on failure.
        """
        try:
            screenshot_dir = PROJECT_ROOT / config.get_report_dir("screenshot")
            screenshot_dir.mkdir(parents=True, exist_ok=True)

            safe_name = ScreenshotUtils._sanitize_name(test_name)
            date_str = datetime.now().strftime("%Y-%m-%d")
            time_str = datetime.now().strftime("%H-%M-%S")
            filename = f"{safe_name}_{date_str}_{time_str}.png"

            filepath = screenshot_dir / filename
            driver.save_screenshot(str(filepath))

            logger.info(f"Screenshot captured: {filepath}")
            return str(filepath)

        except Exception as exc:
            logger.error(f"Failed to capture screenshot for '{test_name}': {exc}")
            return None

    @staticmethod
    def cleanup_old_screenshots(days: int = 7) -> None:
        """
        Nice-to-have: deletes screenshots older than N days to
        keep the repository clean over time.
        """
        screenshot_dir = PROJECT_ROOT / config.get_report_dir("screenshot")
        if not screenshot_dir.exists():
            return

        cutoff = datetime.now().timestamp() - (days * 86400)
        removed = 0
        for file in screenshot_dir.glob("*.png"):
            if file.stat().st_mtime < cutoff:
                file.unlink()
                removed += 1

        if removed:
            logger.info(f"Cleaned up {removed} screenshot(s) older than {days} days")
