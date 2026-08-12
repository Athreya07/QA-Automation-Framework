"""
config_reader.py
==========================================================
Centralized, dynamic config reader for the QA Automation
Framework. Reads config/config.ini and exposes typed
accessors. Supports environment switching via the
[ENV] -> active_env key, and allows values to be
overridden at runtime (e.g. from CLI args in conftest.py).
==========================================================
"""

import configparser
import os
from pathlib import Path
from typing import Optional

# Project root = one level up from this file's directory (utilities/..)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE_PATH = PROJECT_ROOT / "config" / "config.ini"


class ConfigReader:
    """
    Reads and exposes configuration values from config.ini.

    Usage:
        config = ConfigReader()
        url = config.get_base_url()
        browser = config.get_browser()
    """

    _instance = None
    _parser: Optional[configparser.ConfigParser] = None

    def __new__(cls, *args, **kwargs):
        # Singleton pattern - avoid re-parsing the ini file repeatedly
        if cls._instance is None:
            cls._instance = super(ConfigReader, cls).__new__(cls)
        return cls._instance

    def __init__(self, config_path: Path = CONFIG_FILE_PATH):
        if self._parser is not None:
            return  # already initialized (singleton)

        if not config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found at: {config_path}"
            )

        self._parser = configparser.ConfigParser()
        self._parser.read(config_path)
        self._overrides = {}

    # ------------------------------------------------------------------
    # Override support (used when user passes --browser / --url via CLI)
    # ------------------------------------------------------------------
    def set_override(self, key: str, value: str) -> None:
        """Allow CLI args (see conftest.py) to override config.ini values."""
        if value is not None:
            self._overrides[key.lower()] = value

    def _get(self, section: str, key: str, fallback=None):
        override_val = self._overrides.get(key.lower())
        if override_val is not None:
            return override_val
        return self._parser.get(section, key, fallback=fallback)

    # ------------------------------------------------------------------
    # Environment resolution
    # ------------------------------------------------------------------
    def get_active_env(self) -> str:
        return self._overrides.get("env") or self._parser.get(
            "ENV", "active_env", fallback="qa"
        )

    # ------------------------------------------------------------------
    # Public accessors
    # ------------------------------------------------------------------
    def get_base_url(self) -> str:
        env = self.get_active_env()
        return self._get(env, "base_url")

    def get_browser(self) -> str:
        env = self.get_active_env()
        return self._get(env, "browser", fallback="chrome").lower()

    def is_headless(self) -> bool:
        env = self.get_active_env()
        val = self._get(env, "headless", fallback="false")
        return str(val).strip().lower() == "true"

    def get_implicit_wait(self) -> int:
        env = self.get_active_env()
        return int(self._get(env, "implicit_wait", fallback="10"))

    def get_explicit_wait(self) -> int:
        env = self.get_active_env()
        return int(self._get(env, "explicit_wait", fallback="15"))

    def get_page_load_timeout(self) -> int:
        env = self.get_active_env()
        return int(self._get(env, "page_load_timeout", fallback="30"))

    def get_credential(self, key: str) -> str:
        return self._parser.get("CREDENTIALS", key)

    def get_standard_username(self) -> str:
        return self.get_credential("standard_user")

    def get_password(self) -> str:
        return self.get_credential("password")

    def get_locked_out_username(self) -> str:
        return self.get_credential("locked_out_user")

    def get_problem_username(self) -> str:
        return self.get_credential("problem_user")

    def get_report_dir(self, report_type: str) -> str:
        mapping = {
            "allure_results": "allure_results_dir",
            "allure_report": "allure_report_dir",
            "html_report": "html_report_dir",
            "screenshot": "screenshot_dir",
            "log": "log_dir",
        }
        key = mapping.get(report_type)
        if not key:
            raise ValueError(f"Unknown report_type: {report_type}")
        return self._parser.get("REPORTING", key)

    def get_window_size(self) -> tuple:
        width = self._parser.getint("EXECUTION", "window_width", fallback=1920)
        height = self._parser.getint("EXECUTION", "window_height", fallback=1080)
        return width, height

    def get_parallel_workers(self) -> str:
        return self._parser.get("EXECUTION", "parallel_workers", fallback="auto")


# Convenience module-level singleton instance
config = ConfigReader()


if __name__ == "__main__":
    # Quick manual sanity check: `python utilities/config_reader.py`
    c = ConfigReader()
    print("Active Env      :", c.get_active_env())
    print("Base URL        :", c.get_base_url())
    print("Browser         :", c.get_browser())
    print("Headless        :", c.is_headless())
    print("Implicit Wait   :", c.get_implicit_wait())
    print("Standard User   :", c.get_standard_username())
    print("Password        :", c.get_password())
