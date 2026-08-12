"""
conftest.py
==========================================================
Central PyTest configuration for the QA Automation Framework.

Provides:
  - CLI options: --browser, --headless, --env, --url
  - `driver` fixture: yields a ready-to-use WebDriver, quits
    it automatically after each test
  - Automatic screenshot capture on test failure
    (via pytest_runtest_makereport hook)
  - Allure environment + attachment integration
  - Structured test start/end logging
  - Execution summary printed at the end of the session
==========================================================
"""

import time
import pytest
import allure

from utilities.driver_factory import DriverFactory
from utilities.config_reader import config as app_config
from utilities.logger import get_logger, log_test_start, log_test_end
from utilities.screenshot_utils import ScreenshotUtils

logger = get_logger("Conftest")


# ======================================================================
# CLI OPTIONS - allow overriding config.ini values at runtime
# e.g.:  pytest --browser=firefox --headless=true --url=https://... 
# ======================================================================
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default=None,
                      help="Browser to run tests on: chrome | firefox | edge")
    parser.addoption("--headless", action="store", default=None,
                      help="Run browser in headless mode: true | false")
    parser.addoption("--env", action="store", default=None,
                      help="Environment to run against: qa | staging | prod")
    parser.addoption("--url", action="store", default=None,
                      help="Override the base URL from config.ini")


def pytest_configure(config):
    # Register custom marks defensively (also declared in pytest.ini)
    # NOTE: parameter must be named "config" to satisfy pytest's hookspec -
    # this is PyTest's own Config object, unrelated to our ConfigReader (app_config).
    config.addinivalue_line("markers", "smoke: quick smoke test")
    config.addinivalue_line("markers", "regression: full regression suite")


@pytest.fixture(scope="session", autouse=True)
def apply_cli_overrides(request):
    """Applies --browser / --headless / --env / --url overrides to ConfigReader."""
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    env = request.config.getoption("--env")
    url = request.config.getoption("--url")

    if browser:
        app_config.set_override("browser", browser)
    if headless:
        app_config.set_override("headless", headless)
    if env:
        app_config.set_override("env", env)
    if url:
        app_config.set_override("base_url", url)

    logger.info(
        f"Session config -> browser={app_config.get_browser()}, "
        f"headless={app_config.is_headless()}, env={app_config.get_active_env()}, "
        f"url={app_config.get_base_url()}"
    )


# ======================================================================
# DRIVER FIXTURE
# ======================================================================
@pytest.fixture(scope="function")
def driver(request):
    """
    Function-scoped WebDriver fixture.

    - Creates a fresh browser session per test (test isolation).
    - Logs test start/end.
    - Automatically quits the driver after the test, even on failure.
    """
    test_name = request.node.name
    log_test_start(logger, test_name)

    web_driver = DriverFactory.get_driver()
    request.node.driver = web_driver  # expose for the failure-screenshot hook

    yield web_driver

    status = "PASSED"
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        status = "FAILED"
    elif hasattr(request.node, "rep_call") and request.node.rep_call.skipped:
        status = "SKIPPED"

    log_test_end(logger, test_name, status)

    try:
        web_driver.quit()
    except Exception as exc:
        logger.warning(f"Error while quitting driver: {exc}")


# ======================================================================
# SCREENSHOT-ON-FAILURE + ALLURE ATTACHMENT HOOK
# ======================================================================
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook into PyTest's reporting pipeline to:
      1. Store the test result on the item (rep_setup/rep_call/rep_teardown)
         so the `driver` fixture can inspect pass/fail status.
      2. Capture a screenshot automatically when a test fails during
         the "call" phase, and attach it to both the filesystem
         (screenshots/) and the Allure report.
    """
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    if report.when == "call" and report.failed:
        driver = getattr(item, "driver", None)
        if driver is not None:
            screenshot_path = ScreenshotUtils.capture_screenshot(driver, item.name)
            if screenshot_path:
                try:
                    allure.attach.file(
                        screenshot_path,
                        name=f"{item.name}_failure_screenshot",
                        attachment_type=allure.attachment_type.PNG,
                    )
                except Exception as exc:
                    logger.warning(f"Could not attach screenshot to Allure: {exc}")


# ======================================================================
# ALLURE ENVIRONMENT INFO
# ======================================================================
@pytest.fixture(scope="session", autouse=True)
def write_allure_environment():
    """Writes environment.properties into allure-results for the Allure report's Environment tab."""
    import os
    results_dir = app_config.get_report_dir("allure_results")
    os.makedirs(results_dir, exist_ok=True)
    env_file = os.path.join(results_dir, "environment.properties")
    with open(env_file, "w") as f:
        f.write(f"Browser={app_config.get_browser()}\n")
        f.write(f"Environment={app_config.get_active_env()}\n")
        f.write(f"Base_URL={app_config.get_base_url()}\n")
        f.write(f"Headless={app_config.is_headless()}\n")
    yield


# ======================================================================
# EXECUTION SUMMARY (Nice-to-have: Execution Time Summary / Test Statistics)
# ======================================================================
_session_start_time = None
_stats = {"passed": 0, "failed": 0, "skipped": 0, "total": 0}


def pytest_sessionstart(session):
    global _session_start_time
    _session_start_time = time.time()


def pytest_runtest_logreport(report):
    if report.when == "call":
        _stats["total"] += 1
        if report.passed:
            _stats["passed"] += 1
        elif report.failed:
            _stats["failed"] += 1
    elif report.when == "setup" and report.skipped:
        _stats["total"] += 1
        _stats["skipped"] += 1


def pytest_sessionfinish(session, exitstatus):
    duration = time.time() - _session_start_time
    total = _stats["total"] or 1
    pass_pct = (_stats["passed"] / total) * 100

    summary = (
        "\n" + "=" * 60 + "\n"
        "EXECUTION SUMMARY\n" + "=" * 60 + "\n"
        f"Total Tests     : {_stats['total']}\n"
        f"Passed          : {_stats['passed']}\n"
        f"Failed          : {_stats['failed']}\n"
        f"Skipped         : {_stats['skipped']}\n"
        f"Pass Percentage : {pass_pct:.2f}%\n"
        f"Execution Time  : {duration:.2f}s\n" + "=" * 60
    )
    logger.info(summary)
    print(summary)

    # Persist stats as JSON for the custom HTML dashboard (see Step 5)
    import json, os
    os.makedirs("reports", exist_ok=True)
    with open("reports/execution_summary.json", "w") as f:
        json.dump({
            "total": _stats["total"],
            "passed": _stats["passed"],
            "failed": _stats["failed"],
            "skipped": _stats["skipped"],
            "pass_percentage": round(pass_pct, 2),
            "execution_time_seconds": round(duration, 2),
        }, f, indent=4)
