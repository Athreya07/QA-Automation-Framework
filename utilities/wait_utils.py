"""
wait_utils.py
==========================================================
Reusable Explicit Wait helpers built on Selenium's
WebDriverWait + expected_conditions (EC).

Goal: eliminate time.sleep() usage throughout the framework
by centralizing all synchronization logic here.
==========================================================
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from utilities.config_reader import config
from utilities.logger import get_logger

logger = get_logger("WaitUtils")


class WaitUtils:
    """Wraps WebDriverWait with reusable, descriptive wait methods."""

    def __init__(self, driver, timeout: int = None):
        self.driver = driver
        self.timeout = timeout or config.get_explicit_wait()
        self.wait = WebDriverWait(self.driver, self.timeout)

    def wait_for_visible(self, locator: tuple):
        """Wait until element is present AND visible on the DOM."""
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            logger.error(f"Timeout waiting for element to be VISIBLE: {locator}")
            raise

    def wait_for_clickable(self, locator: tuple):
        """Wait until element is visible and enabled for click."""
        try:
            return self.wait.until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            logger.error(f"Timeout waiting for element to be CLICKABLE: {locator}")
            raise

    def wait_for_present(self, locator: tuple):
        """Wait until element exists in the DOM (not necessarily visible)."""
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            logger.error(f"Timeout waiting for element to be PRESENT: {locator}")
            raise

    def wait_for_all_present(self, locator: tuple):
        """Wait until all matching elements exist in the DOM."""
        try:
            return self.wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            logger.error(f"Timeout waiting for elements to be PRESENT: {locator}")
            raise

    def wait_for_invisible(self, locator: tuple):
        """Wait until an element becomes invisible or is removed from DOM."""
        try:
            return self.wait.until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            logger.error(f"Timeout waiting for element to become INVISIBLE: {locator}")
            raise

    def wait_for_text_present(self, locator: tuple, text: str):
        """Wait until specific text appears within the given element."""
        try:
            return self.wait.until(EC.text_to_be_present_in_element(locator, text))
        except TimeoutException:
            logger.error(f"Timeout waiting for text '{text}' in element: {locator}")
            raise

    def wait_for_url_contains(self, partial_url: str):
        """Wait until current URL contains the given substring."""
        try:
            return self.wait.until(EC.url_contains(partial_url))
        except TimeoutException:
            logger.error(f"Timeout waiting for URL to contain: {partial_url}")
            raise

    def wait_for_title_contains(self, partial_title: str):
        """Wait until page title contains the given substring."""
        try:
            return self.wait.until(EC.title_contains(partial_title))
        except TimeoutException:
            logger.error(f"Timeout waiting for title to contain: {partial_title}")
            raise

    def wait_for_alert(self):
        """Wait for a JS alert/confirm/prompt to appear and return it."""
        try:
            return self.wait.until(EC.alert_is_present())
        except TimeoutException:
            logger.error("Timeout waiting for alert to be present")
            raise
