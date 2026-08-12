"""
inventory_page.py
==========================================================
Page Object for the SauceDemo Inventory / Products page.
==========================================================
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InventoryPage(BasePage):

    # ------------------------------------------------------------------
    # Locators
    # ------------------------------------------------------------------
    PAGE_TITLE = (By.CLASS_NAME, "title")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    ITEM_IMAGES = (By.CSS_SELECTOR, ".inventory_item_img img")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button[id^='add-to-cart-']")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[id^='remove-']")
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    BURGER_MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    MENU_CLOSE_BUTTON = (By.ID, "react-burger-cross-btn")

    # Sort dropdown values (as defined by the SauceDemo <select> element)
    SORT_NAME_A_TO_Z = "az"
    SORT_NAME_Z_TO_A = "za"
    SORT_PRICE_LOW_TO_HIGH = "lohi"
    SORT_PRICE_HIGH_TO_LOW = "hilo"

    def __init__(self, driver):
        super().__init__(driver)

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def add_product_to_cart_by_name(self, product_name: str):
        """Adds a product to the cart by matching its visible name."""
        items = self.find_elements(self.INVENTORY_ITEMS)
        for item in items:
            name = item.find_element(By.CLASS_NAME, "inventory_item_name").text.strip()
            if name == product_name:
                button = item.find_element(By.CSS_SELECTOR, "button[id^='add-to-cart-']")
                button.click()
                self.logger.info(f"Added product to cart: {product_name}")
                return self
        raise ValueError(f"Product '{product_name}' not found on inventory page")

    def add_product_to_cart_by_index(self, index: int = 0):
        buttons = self.find_elements(self.ADD_TO_CART_BUTTONS)
        buttons[index].click()
        self.logger.info(f"Added product at index {index} to cart")
        return self

    def add_all_products_to_cart(self):
        buttons = self.find_elements(self.ADD_TO_CART_BUTTONS)
        count = len(buttons)
        for i in range(count):
            # Re-fetch each time; DOM updates after each click (button becomes "Remove")
            buttons = self.find_elements(self.ADD_TO_CART_BUTTONS)
            if buttons:
                buttons[0].click()
        self.logger.info(f"Added {count} product(s) to cart")
        return self

    def remove_product_by_name(self, product_name: str):
        items = self.find_elements(self.INVENTORY_ITEMS)
        for item in items:
            name = item.find_element(By.CLASS_NAME, "inventory_item_name").text.strip()
            if name == product_name:
                button = item.find_element(By.CSS_SELECTOR, "button[id^='remove-']")
                button.click()
                self.logger.info(f"Removed product from cart: {product_name}")
                return self
        raise ValueError(f"Product '{product_name}' not found on inventory page")

    def click_cart_icon(self):
        self.click(self.CART_ICON, description="Cart icon")
        return self

    def sort_products(self, sort_value: str):
        self.select_dropdown_by_value(self.SORT_DROPDOWN, sort_value, description="Sort dropdown")
        return self

    def open_menu(self):
        self.click(self.BURGER_MENU_BUTTON, description="Burger menu button")
        return self

    def logout(self):
        self.open_menu()
        self.wait.wait_for_visible(self.LOGOUT_LINK)
        self.click(self.LOGOUT_LINK, description="Logout link")
        return self

    # ------------------------------------------------------------------
    # State / Getters
    # ------------------------------------------------------------------
    def get_product_count(self) -> int:
        return len(self.find_elements(self.INVENTORY_ITEMS))

    def get_all_product_names(self) -> list:
        elements = self.find_elements(self.ITEM_NAMES)
        return [el.text.strip() for el in elements]

    def get_all_product_prices(self) -> list:
        """Returns prices as floats, e.g. [29.99, 9.99, ...]"""
        elements = self.find_elements(self.ITEM_PRICES)
        return [float(el.text.replace("$", "").strip()) for el in elements]

    def get_all_product_image_srcs(self) -> list:
        elements = self.find_elements(self.ITEM_IMAGES)
        return [el.get_attribute("src") for el in elements]

    def get_cart_badge_count(self) -> int:
        if self.is_displayed(self.CART_BADGE):
            return int(self.get_text(self.CART_BADGE, description="Cart badge"))
        return 0

    def is_inventory_page_displayed(self) -> bool:
        return "inventory.html" in self.get_current_url()

    def is_cart_badge_displayed(self) -> bool:
        return self.is_displayed(self.CART_BADGE)
