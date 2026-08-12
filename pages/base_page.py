"""
base_page.py
==========================================================
BasePage - parent class for every Page Object in the
framework. Centralizes common Selenium interactions
(click, type, get text, etc.) so that:

  1. No raw Selenium calls are scattered across page classes.
  2. Every interaction is automatically logged.
  3. Every interaction goes through explicit waits (WaitUtils).
  4. Exceptions are caught, logged, and re-raised consistently.
==========================================================
"""

from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
)

from utilities.wait_utils import WaitUtils
from utilities.logger import get_logger, log_click, log_assertion, log_exception


class BasePage:
    """Parent class providing reusable, logged Selenium actions."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WaitUtils(driver)
        self.logger = get_logger(self.__class__.__name__)

    # ------------------------------------------------------------------
    # Core interactions
    # ------------------------------------------------------------------
    def open_url(self, url: str) -> None:
        try:
            self.logger.info(f"Navigating to URL: {url}")
            self.driver.get(url)
        except Exception as exc:
            log_exception(self.logger, f"Failed to open URL: {url}", exc)
            raise

    def click(self, locator: tuple, description: str = None) -> None:
        """Wait for element to be clickable, then click it."""
        desc = description or str(locator)
        try:
            element = self.wait.wait_for_clickable(locator)
            element.click()
            log_click(self.logger, desc)
        except (ElementClickInterceptedException, StaleElementReferenceException) as exc:
            # Retry once with JS click as a resilience fallback
            self.logger.warning(f"Standard click failed for '{desc}', retrying via JS click")
            try:
                element = self.wait.wait_for_present(locator)
                self.driver.execute_script("arguments[0].click();", element)
                log_click(self.logger, f"{desc} (JS fallback)")
            except Exception as inner_exc:
                log_exception(self.logger, f"JS click fallback failed for '{desc}'", inner_exc)
                raise
        except Exception as exc:
            log_exception(self.logger, f"Failed to click element: {desc}", exc)
            raise

    def type_text(self, locator: tuple, text: str, description: str = None) -> None:
        """Wait for element to be visible, clear it, then send keys."""
        desc = description or str(locator)
        try:
            element = self.wait.wait_for_visible(locator)
            element.clear()
            element.send_keys(text)
            self.logger.info(f"TYPE -> '{desc}' <- '{text if 'password' not in desc.lower() else '****'}'")
        except Exception as exc:
            log_exception(self.logger, f"Failed to type into element: {desc}", exc)
            raise

    def get_text(self, locator: tuple, description: str = None) -> str:
        desc = description or str(locator)
        try:
            element = self.wait.wait_for_visible(locator)
            text = element.text.strip()
            self.logger.info(f"GET TEXT -> '{desc}' = '{text}'")
            return text
        except Exception as exc:
            log_exception(self.logger, f"Failed to get text from element: {desc}", exc)
            raise

    def get_attribute(self, locator: tuple, attribute: str) -> str:
        try:
            element = self.wait.wait_for_present(locator)
            return element.get_attribute(attribute)
        except Exception as exc:
            log_exception(self.logger, f"Failed to get attribute '{attribute}' from {locator}", exc)
            raise

    def is_displayed(self, locator: tuple) -> bool:
        """Non-throwing visibility check - returns False instead of raising."""
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except (NoSuchElementException, StaleElementReferenceException):
            return False

    def is_element_present(self, locator: tuple) -> bool:
        return len(self.driver.find_elements(*locator)) > 0

    def find_elements(self, locator: tuple) -> list:
        try:
            self.wait.wait_for_present(locator)
            return self.driver.find_elements(*locator)
        except Exception:
            return self.driver.find_elements(*locator)

    def select_dropdown_by_value(self, locator: tuple, value: str, description: str = None) -> None:
        from selenium.webdriver.support.ui import Select
        desc = description or str(locator)
        try:
            element = self.wait.wait_for_visible(locator)
            Select(element).select_by_value(value)
            self.logger.info(f"SELECT -> '{desc}' -> value='{value}'")
        except Exception as exc:
            log_exception(self.logger, f"Failed to select dropdown option: {desc}", exc)
            raise

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_title(self) -> str:
        return self.driver.title

    def scroll_to_element(self, locator: tuple) -> None:
        try:
            element = self.wait.wait_for_present(locator)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        except Exception as exc:
            log_exception(self.logger, f"Failed to scroll to element: {locator}", exc)
            raise

    def go_back(self) -> None:
        self.logger.info("BROWSER BACK -> navigating to previous page")
        self.driver.back()

    def refresh(self) -> None:
        self.logger.info("BROWSER REFRESH")
        self.driver.refresh()

    # ------------------------------------------------------------------
    # Assertion-friendly helpers (used by tests, e.g. assert page.is_x())
    # ------------------------------------------------------------------
    def assert_true(self, condition: bool, description: str) -> bool:
        log_assertion(self.logger, description, condition)
        return condition
