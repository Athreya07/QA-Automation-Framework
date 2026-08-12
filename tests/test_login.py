"""
test_login.py
==========================================================
Test suite for the SauceDemo Login page.

Covers:
  - Valid login
  - Invalid login (wrong username/password)
  - Empty username / empty password
  - Locked out user
  - SQL Injection / XSS input handling
  - Data-driven login via Excel (login_data.xlsx)
==========================================================
"""

import pytest
import allure

from pages.login_page import LoginPage
from utilities.config_reader import config
from utilities.excel_utils import ExcelUtils
from utilities.logger import get_logger

logger = get_logger("TestLogin")


@allure.feature("Login")
class TestLogin:

    @allure.story("Valid Login")
    @pytest.mark.smoke
    @pytest.mark.login
    def test_valid_login(self, driver):
        """A user with valid credentials should reach the Inventory page."""
        with allure.step("Open login page"):
            login_page = LoginPage(driver).open()

        with allure.step("Login with valid standard_user credentials"):
            login_page.login(config.get_standard_username(), config.get_password())

        with allure.step("Assert redirected to inventory page"):
            assert login_page.assert_true(
                login_page.is_login_successful(),
                "User should be redirected to inventory.html after valid login",
            )

    @allure.story("Invalid Login")
    @pytest.mark.regression
    @pytest.mark.login
    @pytest.mark.negative
    def test_invalid_login_wrong_password(self, driver):
        """Login with a valid username but wrong password should fail with an error."""
        with allure.step("Open login page and attempt login with wrong password"):
            login_page = LoginPage(driver).open()
            login_page.login(config.get_standard_username(), "wrong_password_123")

        with allure.step("Assert error message is displayed"):
            assert login_page.assert_true(
                login_page.is_error_displayed(),
                "Error message should be displayed for wrong password",
            )
            assert "do not match" in login_page.get_error_message().lower()

    @allure.story("Invalid Login")
    @pytest.mark.regression
    @pytest.mark.login
    @pytest.mark.negative
    def test_invalid_login_unknown_user(self, driver):
        """Login with a completely unknown username should fail."""
        with allure.step("Attempt login with unknown user"):
            login_page = LoginPage(driver).open()
            login_page.login("nonexistent_user_007", config.get_password())

        with allure.step("Assert error message is displayed"):
            assert login_page.assert_true(
                login_page.is_error_displayed(),
                "Error message should be displayed for unknown username",
            )

    @allure.story("Empty Fields")
    @pytest.mark.regression
    @pytest.mark.login
    @pytest.mark.negative
    def test_empty_username(self, driver):
        """Submitting the form with an empty username should show an error."""
        with allure.step("Attempt login with empty username"):
            login_page = LoginPage(driver).open()
            login_page.enter_password(config.get_password())
            login_page.click_login()

        with allure.step("Assert username-required error is shown"):
            assert login_page.assert_true(
                login_page.is_error_displayed(),
                "Error message should be displayed for empty username",
            )
            assert "username is required" in login_page.get_error_message().lower()

    @allure.story("Empty Fields")
    @pytest.mark.regression
    @pytest.mark.login
    @pytest.mark.negative
    def test_empty_password(self, driver):
        """Submitting the form with an empty password should show an error."""
        with allure.step("Attempt login with empty password"):
            login_page = LoginPage(driver).open()
            login_page.enter_username(config.get_standard_username())
            login_page.click_login()

        with allure.step("Assert password-required error is shown"):
            assert login_page.assert_true(
                login_page.is_error_displayed(),
                "Error message should be displayed for empty password",
            )
            assert "password is required" in login_page.get_error_message().lower()

    @allure.story("Locked User")
    @pytest.mark.regression
    @pytest.mark.login
    @pytest.mark.negative
    def test_locked_out_user(self, driver):
        """A locked-out user should be blocked from logging in with a clear error."""
        with allure.step("Attempt login with locked_out_user"):
            login_page = LoginPage(driver).open()
            login_page.login(config.get_locked_out_username(), config.get_password())

        with allure.step("Assert locked-out error is shown"):
            assert login_page.assert_true(
                login_page.is_error_displayed(),
                "Error message should be displayed for locked out user",
            )
            assert "locked out" in login_page.get_error_message().lower()

    @allure.story("Security")
    @pytest.mark.regression
    @pytest.mark.login
    @pytest.mark.security
    def test_sql_injection_input(self, driver):
        """SQL injection payloads in the login form must not bypass authentication."""
        with allure.step("Attempt login with SQL injection payload"):
            login_page = LoginPage(driver).open()
            login_page.login("' OR '1'='1", "' OR '1'='1")

        with allure.step("Assert login is rejected (no auth bypass)"):
            assert login_page.assert_true(
                not login_page.is_login_successful(),
                "SQL injection payload must NOT result in a successful login",
            )
            assert login_page.is_error_displayed()

    @allure.story("Security")
    @pytest.mark.regression
    @pytest.mark.login
    @pytest.mark.security
    def test_xss_input(self, driver):
        """XSS payloads in the login form must be handled safely (no script execution, login rejected)."""
        xss_payload = "<script>alert('xss')</script>"
        with allure.step("Attempt login with XSS payload"):
            login_page = LoginPage(driver).open()
            login_page.login(xss_payload, xss_payload)

        with allure.step("Assert login is rejected and no JS alert fired"):
            assert login_page.assert_true(
                not login_page.is_login_successful(),
                "XSS payload must NOT result in a successful login",
            )
            # If an alert() had actually executed, this would raise/hang;
            # reaching this point confirms no script execution occurred.
            assert login_page.is_error_displayed()

    @allure.story("Data-Driven Login")
    @pytest.mark.regression
    @pytest.mark.login
    @pytest.mark.parametrize(
        "username,password,expected_result", ExcelUtils.get_login_test_data()
    )
    def test_login_data_driven(self, driver, username, password, expected_result):
        """
        Data-driven login test sourced from testdata/login_data.xlsx.
        Validates each row's expected outcome: success | failure | locked.
        """
        with allure.step(f"Attempt login with username='{username}'"):
            login_page = LoginPage(driver).open()
            login_page.login(username or "", password or "")

        if expected_result == "success":
            with allure.step("Assert login succeeded"):
                assert login_page.assert_true(
                    login_page.is_login_successful(),
                    f"Expected successful login for user '{username}'",
                )
        elif expected_result == "locked":
            with allure.step("Assert locked-out error shown"):
                assert login_page.is_error_displayed()
                assert "locked out" in login_page.get_error_message().lower()
        else:  # failure
            with allure.step("Assert login failed with an error message"):
                assert login_page.assert_true(
                    login_page.is_error_displayed(),
                    f"Expected login failure for user '{username}'",
                )
