"""
checkout_complete_page.py
==========================================================
Page Object for the SauceDemo Checkout: Complete page
(Step Three / order confirmation) - checkout-complete.html
==========================================================
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutCompletePage(BasePage):

    # ------------------------------------------------------------------
    # Locators
    # ------------------------------------------------------------------
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")
    PONY_EXPRESS_IMAGE = (By.CLASS_NAME, "pony_express")

    EXPECTED_HEADER_TEXT = "Thank you for your order!"

    def __init__(self, driver):
        super().__init__(driver)

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def click_back_home(self):
        self.click(self.BACK_HOME_BUTTON, description="Back Home button")
        return self

    # ------------------------------------------------------------------
    # State / Getters
    # ------------------------------------------------------------------
    def get_confirmation_header(self) -> str:
        return self.get_text(self.COMPLETE_HEADER, description="Order confirmation header")

    def is_order_successful(self) -> bool:
        return (
            "checkout-complete.html" in self.get_current_url()
            and self.get_confirmation_header() == self.EXPECTED_HEADER_TEXT
        )

    def is_checkout_complete_page_displayed(self) -> bool:
        return "checkout-complete.html" in self.get_current_url()
