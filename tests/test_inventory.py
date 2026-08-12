"""
test_inventory.py
==========================================================
Test suite for the SauceDemo Inventory / Products page.

Covers:
  - Product count
  - Product name / image / price presence
  - Sorting: A-Z, Z-A, Price Low-High, Price High-Low
==========================================================
"""

import pytest
import allure

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utilities.config_reader import config

EXPECTED_PRODUCT_COUNT = 6


@pytest.fixture
def logged_in_inventory_page(driver):
    """Fixture: logs in as standard_user and returns an InventoryPage instance."""
    login_page = LoginPage(driver).open()
    login_page.login(config.get_standard_username(), config.get_password())
    return InventoryPage(driver)


@allure.feature("Inventory")
class TestInventory:

    @allure.story("Product Count")
    @pytest.mark.smoke
    @pytest.mark.inventory
    def test_product_count(self, logged_in_inventory_page):
        """Inventory page should display exactly 6 products for the standard user."""
        inventory_page = logged_in_inventory_page
        with allure.step("Assert product count is correct"):
            count = inventory_page.get_product_count()
            assert inventory_page.assert_true(
                count == EXPECTED_PRODUCT_COUNT,
                f"Expected {EXPECTED_PRODUCT_COUNT} products, found {count}",
            )

    @allure.story("Product Name")
    @pytest.mark.regression
    @pytest.mark.inventory
    def test_product_names_are_not_empty(self, logged_in_inventory_page):
        """Every product must have a non-empty display name."""
        inventory_page = logged_in_inventory_page
        with allure.step("Assert all product names are populated"):
            names = inventory_page.get_all_product_names()
            assert len(names) == EXPECTED_PRODUCT_COUNT
            assert all(name.strip() != "" for name in names)

    @allure.story("Product Image")
    @pytest.mark.regression
    @pytest.mark.inventory
    def test_product_images_are_present(self, logged_in_inventory_page):
        """Every product must have a valid (non-empty) image source."""
        inventory_page = logged_in_inventory_page
        with allure.step("Assert all product images have a valid src"):
            image_srcs = inventory_page.get_all_product_image_srcs()
            assert len(image_srcs) == EXPECTED_PRODUCT_COUNT
            assert all(src and src.strip() != "" for src in image_srcs)

    @allure.story("Product Price")
    @pytest.mark.regression
    @pytest.mark.inventory
    def test_product_prices_are_valid(self, logged_in_inventory_page):
        """Every product must have a positive numeric price."""
        inventory_page = logged_in_inventory_page
        with allure.step("Assert all product prices are valid positive numbers"):
            prices = inventory_page.get_all_product_prices()
            assert len(prices) == EXPECTED_PRODUCT_COUNT
            assert all(price > 0 for price in prices)

    @allure.story("Sorting")
    @pytest.mark.regression
    @pytest.mark.inventory
    def test_sort_name_a_to_z(self, logged_in_inventory_page):
        """Sorting by 'Name (A to Z)' should return alphabetically ascending names."""
        inventory_page = logged_in_inventory_page
        with allure.step("Sort by Name A-Z and assert order"):
            inventory_page.sort_products(InventoryPage.SORT_NAME_A_TO_Z)
            names = inventory_page.get_all_product_names()
            assert names == sorted(names)

    @allure.story("Sorting")
    @pytest.mark.regression
    @pytest.mark.inventory
    def test_sort_name_z_to_a(self, logged_in_inventory_page):
        """Sorting by 'Name (Z to A)' should return alphabetically descending names."""
        inventory_page = logged_in_inventory_page
        with allure.step("Sort by Name Z-A and assert order"):
            inventory_page.sort_products(InventoryPage.SORT_NAME_Z_TO_A)
            names = inventory_page.get_all_product_names()
            assert names == sorted(names, reverse=True)

    @allure.story("Sorting")
    @pytest.mark.regression
    @pytest.mark.inventory
    def test_sort_price_low_to_high(self, logged_in_inventory_page):
        """Sorting by 'Price (low to high)' should return ascending prices."""
        inventory_page = logged_in_inventory_page
        with allure.step("Sort by Price Low-High and assert order"):
            inventory_page.sort_products(InventoryPage.SORT_PRICE_LOW_TO_HIGH)
            prices = inventory_page.get_all_product_prices()
            assert prices == sorted(prices)

    @allure.story("Sorting")
    @pytest.mark.regression
    @pytest.mark.inventory
    def test_sort_price_high_to_low(self, logged_in_inventory_page):
        """Sorting by 'Price (high to low)' should return descending prices."""
        inventory_page = logged_in_inventory_page
        with allure.step("Sort by Price High-Low and assert order"):
            inventory_page.sort_products(InventoryPage.SORT_PRICE_HIGH_TO_LOW)
            prices = inventory_page.get_all_product_prices()
            assert prices == sorted(prices, reverse=True)
