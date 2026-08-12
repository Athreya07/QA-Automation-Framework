"""
checkout_overview_page.py
==========================================================
Page Object for the SauceDemo Checkout: Overview page
(Step Two) - checkout-step-two.html
==========================================================
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutOverviewPage(BasePage):

    # ------------------------------------------------------------------
    # Locators
    # ------------------------------------------------------------------
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    ITEM_TOTAL_LABEL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX_LABEL = (By.CLASS_NAME, "summary_tax_label")
    TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")
    CANCEL_BUTTON = (By.ID, "cancel")
    PAGE_TITLE = (By.CLASS_NAME, "title")
    PAYMENT_INFO = (By.CSS_SELECTOR, ".summary_info .summary_value_label")

    def __init__(self, driver):
        super().__init__(driver)

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def click_finish(self):
        self.click(self.FINISH_BUTTON, description="Finish button")
        return self

    def click_cancel(self):
        self.click(self.CANCEL_BUTTON, description="Cancel button")
        return self

    # ------------------------------------------------------------------
    # State / Getters
    # ------------------------------------------------------------------
    def get_item_total(self) -> float:
        text = self.get_text(self.ITEM_TOTAL_LABEL, description="Item total label")
        return float(text.split("$")[-1])

    def get_tax(self) -> float:
        text = self.get_text(self.TAX_LABEL, description="Tax label")
        return float(text.split("$")[-1])

    def get_total(self) -> float:
        text = self.get_text(self.TOTAL_LABEL, description="Total label")
        return float(text.split("$")[-1])

    def get_order_product_names(self) -> list:
        elements = self.find_elements(self.ITEM_NAMES)
        return [el.text.strip() for el in elements]

    def is_checkout_overview_displayed(self) -> bool:
        return "checkout-step-two.html" in self.get_current_url()

    def is_total_calculated_correctly(self) -> bool:
        """Validates that item_total + tax == total (within floating point tolerance)."""
        return abs((self.get_item_total() + self.get_tax()) - self.get_total()) < 0.01
