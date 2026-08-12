"""
cart_page.py
==========================================================
Page Object for the SauceDemo Shopping Cart page.
==========================================================
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):

    # ------------------------------------------------------------------
    # Locators
    # ------------------------------------------------------------------
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[id^='remove-']")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CART_QUANTITY = (By.CLASS_NAME, "cart_quantity")
    PAGE_TITLE = (By.CLASS_NAME, "title")

    def __init__(self, driver):
        super().__init__(driver)

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def remove_product_by_name(self, product_name: str):
        items = self.find_elements(self.CART_ITEMS)
        for item in items:
            name = item.find_element(By.CLASS_NAME, "inventory_item_name").text.strip()
            if name == product_name:
                button = item.find_element(By.CSS_SELECTOR, "button[id^='remove-']")
                button.click()
                self.logger.info(f"Removed '{product_name}' from cart page")
                return self
        raise ValueError(f"Product '{product_name}' not found in cart")

    def click_continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING_BUTTON, description="Continue Shopping button")
        return self

    def click_checkout(self):
        self.click(self.CHECKOUT_BUTTON, description="Checkout button")
        return self

    # ------------------------------------------------------------------
    # State / Getters
    # ------------------------------------------------------------------
    def get_cart_item_count(self) -> int:
        return len(self.find_elements(self.CART_ITEMS))

    def get_cart_product_names(self) -> list:
        elements = self.find_elements(self.ITEM_NAMES)
        return [el.text.strip() for el in elements]

    def is_product_in_cart(self, product_name: str) -> bool:
        return product_name in self.get_cart_product_names()

    def is_cart_page_displayed(self) -> bool:
        return "cart.html" in self.get_current_url()

    def is_cart_empty(self) -> bool:
        return self.get_cart_item_count() == 0
