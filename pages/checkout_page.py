"""
checkout_page.py
==========================================================
Page Object for the SauceDemo Checkout: Your Information
page (Step One) - checkout-step-one.html
==========================================================
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutPage(BasePage):

    # ------------------------------------------------------------------
    # Locators
    # ------------------------------------------------------------------
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    PAGE_TITLE = (By.CLASS_NAME, "title")

    def __init__(self, driver):
        super().__init__(driver)

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def enter_first_name(self, first_name: str):
        self.type_text(self.FIRST_NAME_INPUT, first_name, description="First name field")
        return self

    def enter_last_name(self, last_name: str):
        self.type_text(self.LAST_NAME_INPUT, last_name, description="Last name field")
        return self

    def enter_postal_code(self, postal_code: str):
        self.type_text(self.POSTAL_CODE_INPUT, postal_code, description="Postal code field")
        return self

    def fill_checkout_info(self, first_name: str, last_name: str, postal_code: str):
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)
        return self

    def click_continue(self):
        self.click(self.CONTINUE_BUTTON, description="Continue button")
        return self

    def click_cancel(self):
        self.click(self.CANCEL_BUTTON, description="Cancel button")
        return self

    def complete_checkout_step_one(self, first_name: str, last_name: str, postal_code: str):
        self.fill_checkout_info(first_name, last_name, postal_code)
        self.click_continue()
        return self

    # ------------------------------------------------------------------
    # State / Getters
    # ------------------------------------------------------------------
    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE, description="Checkout error message")

    def is_error_displayed(self) -> bool:
        return self.is_displayed(self.ERROR_MESSAGE)

    def is_checkout_step_one_displayed(self) -> bool:
        return "checkout-step-one.html" in self.get_current_url()
