"""
login_page.py
==========================================================
Page Object for the SauceDemo Login page (https://www.saucedemo.com/).
==========================================================
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utilities.config_reader import config


class LoginPage(BasePage):

    # ------------------------------------------------------------------
    # Locators
    # ------------------------------------------------------------------
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    ERROR_BUTTON_CLOSE = (By.CSS_SELECTOR, ".error-button")
    LOGO = (By.CLASS_NAME, "login_logo")

    def __init__(self, driver):
        super().__init__(driver)
        self.base_url = config.get_base_url()

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def open(self):
        self.open_url(self.base_url)
        return self

    def enter_username(self, username: str):
        self.type_text(self.USERNAME_INPUT, username, description="Username field")
        return self

    def enter_password(self, password: str):
        self.type_text(self.PASSWORD_INPUT, password, description="Password field")
        return self

    def click_login(self):
        self.click(self.LOGIN_BUTTON, description="Login button")
        return self

    def login(self, username: str, password: str):
        """Convenience method performing the full login flow."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self

    # ------------------------------------------------------------------
    # State / Assertions
    # ------------------------------------------------------------------
    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE, description="Login error message")

    def is_error_displayed(self) -> bool:
        return self.is_displayed(self.ERROR_MESSAGE)

    def is_login_page_displayed(self) -> bool:
        return self.is_displayed(self.LOGO)

    def is_login_successful(self) -> bool:
        """
        A successful login redirects to /inventory.html.
        Used as the primary assertion point in login tests.
        """
        return "inventory.html" in self.get_current_url()
