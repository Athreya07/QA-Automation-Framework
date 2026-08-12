"""
test_logout.py
==========================================================
Test suite for Logout and session handling.

Covers:
  - Successful logout
  - Session validation (direct URL access after logout)
  - Browser back button behavior after logout
==========================================================
"""

import pytest
import allure

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utilities.config_reader import config


@pytest.fixture
def logged_in_inventory_page(driver):
    login_page = LoginPage(driver).open()
    login_page.login(config.get_standard_username(), config.get_password())
    return InventoryPage(driver)


@allure.feature("Logout")
class TestLogout:

    @allure.story("Logout Successfully")
    @pytest.mark.smoke
    @pytest.mark.logout
    def test_logout_successfully(self, driver, logged_in_inventory_page):
        """Logging out should return the user to the login page."""
        inventory_page = logged_in_inventory_page
        with allure.step("Logout via burger menu"):
            inventory_page.logout()

        with allure.step("Assert redirected to login page"):
            login_page = LoginPage(driver)
            assert login_page.assert_true(
                login_page.is_login_page_displayed(),
                "User should be redirected to the login page after logout",
            )

    @allure.story("Session Validation")
    @pytest.mark.regression
    @pytest.mark.logout
    @pytest.mark.security
    def test_session_invalid_after_logout(self, driver, logged_in_inventory_page):
        """
        After logout, directly navigating to /inventory.html should NOT
        display the inventory page (session must be invalidated).
        """
        inventory_page = logged_in_inventory_page
        with allure.step("Logout, then attempt direct navigation to inventory.html"):
            inventory_page.logout()
            inventory_page.open_url(f"{config.get_base_url()}inventory.html")

        with allure.step("Assert user is NOT on the inventory page (redirected/blocked)"):
            login_page = LoginPage(driver)
            assert inventory_page.assert_true(
                not inventory_page.is_inventory_page_displayed() or login_page.is_error_displayed(),
                "Direct access to inventory.html after logout should be blocked",
            )

    @allure.story("Browser Back Button")
    @pytest.mark.regression
    @pytest.mark.logout
    def test_back_button_after_logout(self, driver, logged_in_inventory_page):
        """Using the browser back button after logout should not restore an authenticated session view."""
        inventory_page = logged_in_inventory_page
        with allure.step("Logout, then click browser back button"):
            inventory_page.logout()
            login_page = LoginPage(driver)
            login_page.go_back()

        with allure.step("Assert still on / redirected to login page (no cached authenticated state)"):
            assert login_page.assert_true(
                login_page.is_login_page_displayed(),
                "Browser back navigation after logout should not restore an authenticated session",
            )
