import pytest
import allure
from pytest_bdd import given, when, then, scenario, parsers
from pages.login_page import LoginPage


# ------------------------------------------------
# Scenarios
# ------------------------------------------------

@allure.feature("Login")
@allure.story("Successful Login")
@scenario("../features/login.feature", "Successful login with valid credentials")
def test_successful_login():
    pass

@allure.feature("Login")
@allure.story("Failed Login")
@scenario("../features/login.feature", "Login fails with invalid password")
def test_invalid_password():
    pass

@allure.feature("Login")
@allure.story("Failed Login")
@scenario("../features/login.feature", "Login fails with locked out user")
def test_locked_out_user():
    pass

@allure.feature("Login")
@allure.story("Failed Login")
@scenario("../features/login.feature", "Login fails with empty credentials")
def test_empty_credentials():
    pass  # FIX: removed duplicate scenario decorator


# ------------------------------------------------
# Steps
# ------------------------------------------------

@given("I am on the login page")
def navigate_to_login(page, base_url):
    with allure.step("Navigate to login page"):
        LoginPage(page, base_url).navigate()


@when(parsers.parse('I login with username "{username}" and password "{password}"'))
def perform_login(page, base_url, username, password):
    with allure.step(f"Login with username='{username}'"):
        login_page = LoginPage(page, base_url)
        login_page.navigate()
        login_page.enter_username(username)
        login_page.enter_password(password)
        login_page.click_login()


@then("I should be redirected to the inventory page")
def verify_inventory_page(page):
    with allure.step("Verify redirect to inventory page"):
        assert "/inventory.html" in page.url, \
            f"Expected inventory page but got: {page.url}"


@then("I should see an error message")
def verify_error_message(page):
    with allure.step("Verify error message is visible"):
        from pages.login_page import LoginPageLocators
        error = page.locator(LoginPageLocators.ERROR_MESSAGE)
        assert error.is_visible(), "Expected error message but it was not visible"


@when("I submit login with empty credentials")
def submit_empty_credentials(page, base_url):
    with allure.step("Click login with empty fields"):
        login_page = LoginPage(page, base_url)
        login_page.navigate()
        login_page.click_login()
