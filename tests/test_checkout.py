"""
test_checkout.py
==========================================================
Test suite for the SauceDemo Checkout flow.

Covers:
  - Successful end-to-end checkout
  - Missing first name / last name / postal code validation
  - Cancel checkout
==========================================================
"""

import pytest
import allure

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.checkout_complete_page import CheckoutCompletePage
from utilities.config_reader import config
from utilities.data_generator import DataGenerator

PRODUCT_ONE = "Sauce Labs Backpack"


@pytest.fixture
def cart_with_one_item(driver):
    """Fixture: logs in, adds one product, and navigates to the cart page."""
    login_page = LoginPage(driver).open()
    login_page.login(config.get_standard_username(), config.get_password())

    inventory_page = InventoryPage(driver)
    inventory_page.add_product_to_cart_by_name(PRODUCT_ONE)
    inventory_page.click_cart_icon()
    return CartPage(driver)


@allure.feature("Checkout")
class TestCheckout:

    @allure.story("Successful Checkout")
    @pytest.mark.smoke
    @pytest.mark.checkout
    def test_successful_checkout(self, driver, cart_with_one_item):
        """A user with valid checkout info should be able to complete an order end-to-end."""
        cart_page = cart_with_one_item
        user_info = DataGenerator.generate_checkout_info()

        with allure.step("Proceed to checkout"):
            cart_page.click_checkout()
            checkout_page = CheckoutPage(driver)

        with allure.step("Fill in valid checkout information and continue"):
            checkout_page.complete_checkout_step_one(
                user_info["first_name"], user_info["last_name"], user_info["postal_code"]
            )

        with allure.step("Assert on overview page with correct total calculation"):
            overview_page = CheckoutOverviewPage(driver)
            assert overview_page.is_checkout_overview_displayed()
            assert overview_page.is_total_calculated_correctly()

        with allure.step("Finish the order"):
            overview_page.click_finish()

        with allure.step("Assert order confirmation is displayed"):
            complete_page = CheckoutCompletePage(driver)
            assert complete_page.assert_true(
                complete_page.is_order_successful(),
                "Order confirmation header should read 'Thank you for your order!'",
            )

    @allure.story("Validation")
    @pytest.mark.regression
    @pytest.mark.checkout
    @pytest.mark.negative
    def test_missing_first_name(self, driver, cart_with_one_item):
        """Checkout should be blocked with an error when first name is missing."""
        cart_page = cart_with_one_item
        with allure.step("Proceed to checkout and submit without first name"):
            cart_page.click_checkout()
            checkout_page = CheckoutPage(driver)
            checkout_page.enter_last_name("Doe")
            checkout_page.enter_postal_code("12345")
            checkout_page.click_continue()

        with allure.step("Assert 'First Name is required' error is shown"):
            assert checkout_page.is_error_displayed()
            assert "first name is required" in checkout_page.get_error_message().lower()

    @allure.story("Validation")
    @pytest.mark.regression
    @pytest.mark.checkout
    @pytest.mark.negative
    def test_missing_last_name(self, driver, cart_with_one_item):
        """Checkout should be blocked with an error when last name is missing."""
        cart_page = cart_with_one_item
        with allure.step("Proceed to checkout and submit without last name"):
            cart_page.click_checkout()
            checkout_page = CheckoutPage(driver)
            checkout_page.enter_first_name("John")
            checkout_page.enter_postal_code("12345")
            checkout_page.click_continue()

        with allure.step("Assert 'Last Name is required' error is shown"):
            assert checkout_page.is_error_displayed()
            assert "last name is required" in checkout_page.get_error_message().lower()

    @allure.story("Validation")
    @pytest.mark.regression
    @pytest.mark.checkout
    @pytest.mark.negative
    def test_missing_postal_code(self, driver, cart_with_one_item):
        """Checkout should be blocked with an error when postal code is missing."""
        cart_page = cart_with_one_item
        with allure.step("Proceed to checkout and submit without postal code"):
            cart_page.click_checkout()
            checkout_page = CheckoutPage(driver)
            checkout_page.enter_first_name("John")
            checkout_page.enter_last_name("Doe")
            checkout_page.click_continue()

        with allure.step("Assert 'Postal Code is required' error is shown"):
            assert checkout_page.is_error_displayed()
            assert "postal code is required" in checkout_page.get_error_message().lower()

    @allure.story("Cancel Checkout")
    @pytest.mark.regression
    @pytest.mark.checkout
    def test_cancel_checkout(self, driver, cart_with_one_item):
        """Cancelling on the checkout info page should return the user to the cart."""
        cart_page = cart_with_one_item
        with allure.step("Proceed to checkout, then cancel"):
            cart_page.click_checkout()
            checkout_page = CheckoutPage(driver)
            checkout_page.click_cancel()

        with allure.step("Assert user is returned to the cart page"):
            returned_cart_page = CartPage(driver)
            assert returned_cart_page.is_cart_page_displayed()
