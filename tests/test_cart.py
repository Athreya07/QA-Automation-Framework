"""
test_cart.py
==========================================================
Test suite for the SauceDemo Shopping Cart.

Covers:
  - Add single product
  - Remove product
  - Add multiple products
  - Cart badge accuracy
  - Cart persistence across navigation
==========================================================
"""

import pytest
import allure

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utilities.config_reader import config

PRODUCT_ONE = "Sauce Labs Backpack"
PRODUCT_TWO = "Sauce Labs Bike Light"
PRODUCT_THREE = "Sauce Labs Bolt T-Shirt"


@pytest.fixture
def logged_in_inventory_page(driver):
    login_page = LoginPage(driver).open()
    login_page.login(config.get_standard_username(), config.get_password())
    return InventoryPage(driver)


@allure.feature("Cart")
class TestCart:

    @allure.story("Add Product")
    @pytest.mark.smoke
    @pytest.mark.cart
    def test_add_single_product_to_cart(self, driver, logged_in_inventory_page):
        """Adding a single product should update the cart badge to 1."""
        inventory_page = logged_in_inventory_page
        with allure.step(f"Add '{PRODUCT_ONE}' to cart"):
            inventory_page.add_product_to_cart_by_name(PRODUCT_ONE)

        with allure.step("Assert cart badge shows 1"):
            assert inventory_page.assert_true(
                inventory_page.get_cart_badge_count() == 1,
                "Cart badge should display 1 after adding one product",
            )

    @allure.story("Remove Product")
    @pytest.mark.regression
    @pytest.mark.cart
    def test_remove_product_from_cart(self, driver, logged_in_inventory_page):
        """Removing a product from the inventory page should clear the cart badge."""
        inventory_page = logged_in_inventory_page
        with allure.step(f"Add then remove '{PRODUCT_ONE}'"):
            inventory_page.add_product_to_cart_by_name(PRODUCT_ONE)
            inventory_page.remove_product_by_name(PRODUCT_ONE)

        with allure.step("Assert cart badge is no longer displayed"):
            assert inventory_page.assert_true(
                not inventory_page.is_cart_badge_displayed(),
                "Cart badge should disappear after removing the only product",
            )

    @allure.story("Add Multiple Products")
    @pytest.mark.regression
    @pytest.mark.cart
    def test_add_multiple_products_to_cart(self, driver, logged_in_inventory_page):
        """Adding multiple products should reflect the correct count in the cart badge and cart page."""
        inventory_page = logged_in_inventory_page
        with allure.step("Add three products to cart"):
            inventory_page.add_product_to_cart_by_name(PRODUCT_ONE)
            inventory_page.add_product_to_cart_by_name(PRODUCT_TWO)
            inventory_page.add_product_to_cart_by_name(PRODUCT_THREE)

        with allure.step("Assert cart badge shows 3"):
            assert inventory_page.get_cart_badge_count() == 3

        with allure.step("Navigate to cart and assert all 3 products are listed"):
            inventory_page.click_cart_icon()
            cart_page = CartPage(driver)
            assert cart_page.get_cart_item_count() == 3
            product_names = cart_page.get_cart_product_names()
            assert PRODUCT_ONE in product_names
            assert PRODUCT_TWO in product_names
            assert PRODUCT_THREE in product_names

    @allure.story("Cart Badge")
    @pytest.mark.regression
    @pytest.mark.cart
    def test_cart_badge_updates_dynamically(self, driver, logged_in_inventory_page):
        """Cart badge count should increment/decrement correctly as items are added/removed."""
        inventory_page = logged_in_inventory_page
        with allure.step("Add two products and verify badge = 2"):
            inventory_page.add_product_to_cart_by_name(PRODUCT_ONE)
            inventory_page.add_product_to_cart_by_name(PRODUCT_TWO)
            assert inventory_page.get_cart_badge_count() == 2

        with allure.step("Remove one product and verify badge = 1"):
            inventory_page.remove_product_by_name(PRODUCT_ONE)
            assert inventory_page.get_cart_badge_count() == 1

    @allure.story("Cart Persistence")
    @pytest.mark.regression
    @pytest.mark.cart
    def test_cart_persists_across_navigation(self, driver, logged_in_inventory_page):
        """Cart contents should persist when navigating to the cart page and back."""
        inventory_page = logged_in_inventory_page
        with allure.step("Add a product, navigate to cart, then go back"):
            inventory_page.add_product_to_cart_by_name(PRODUCT_ONE)
            inventory_page.click_cart_icon()

            cart_page = CartPage(driver)
            assert cart_page.is_product_in_cart(PRODUCT_ONE)

            cart_page.click_continue_shopping()

        with allure.step("Assert cart badge still shows 1 after returning to inventory"):
            assert inventory_page.get_cart_badge_count() == 1
