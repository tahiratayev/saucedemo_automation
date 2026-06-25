import allure
import pytest
from playwright.sync_api import Page, expect
from pytest_bdd import given, when, then, parsers, scenarios

from pages.login_page import LoginPage

scenarios("login.feature")


@pytest.fixture
def login_page(page: Page, base_url: str) -> LoginPage:
    return LoginPage(page, base_url)


# ---------------------------------------------------------------------------
# Background
# ---------------------------------------------------------------------------

@given("the user is on the Swag Labs login page")
def navigate_to_login_page(login_page: LoginPage) -> None:
    with allure.step("Navigate to the Swag Labs login page"):
        login_page.navigate()


# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------

@when(parsers.parse('the user enters username "{username}"'))
def enter_username(login_page: LoginPage, username: str) -> None:
    with allure.step(f"Enter username: {username}"):
        login_page.page.locator("[data-test='username']").fill(username)


@when(parsers.parse('the user enters password "{password}"'))
def enter_password(login_page: LoginPage, password: str) -> None:
    with allure.step(f"Enter password: {'*' * len(password)}"):
        login_page.page.locator("[data-test='password']").fill(password)


@when("the user clicks the login button")
def click_login_button(login_page: LoginPage) -> None:
    with allure.step("Click the login button"):
        login_page.page.locator("[data-test='login-button']").click()


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------

@then("the user should be redirected to the products page")
def verify_redirect_to_products(login_page: LoginPage) -> None:
    with allure.step("Verify the user is redirected to the products page"):
        expect(login_page.page).to_have_url("https://www.saucedemo.com/inventory.html")


@then("an error message should be displayed indicating incorrect credentials")
def verify_incorrect_credentials_error(login_page: LoginPage) -> None:
    with allure.step("Verify error message for incorrect credentials is displayed"):
        error_container = login_page.page.locator("[data-test='error']")
        expect(error_container).to_be_visible()
        expect(error_container).to_contain_text(
            "Username and password do not match any user in this service"
        )


@then("an error message should be displayed requiring a username")
def verify_username_required_error(login_page: LoginPage) -> None:
    with allure.step("Verify error message requiring a username is displayed"):
        error_container = login_page.page.locator("[data-test='error']")
        expect(error_container).to_be_visible()
        expect(error_container).to_contain_text("Username is required")


@then("an error message should be displayed requiring a password")
def verify_password_required_error(login_page: LoginPage) -> None:
    with allure.step("Verify error message requiring a password is displayed"):
        error_container = login_page.page.locator("[data-test='error']")
        expect(error_container).to_be_visible()
        expect(error_container).to_contain_text("Password is required")


@then("an error message should be displayed indicating the account is locked")
def verify_locked_account_error(login_page: LoginPage) -> None:
    with allure.step("Verify error message for a locked account is displayed"):
        error_container = login_page.page.locator("[data-test='error']")
        expect(error_container).to_be_visible()
        expect(error_container).to_contain_text(
            "Sorry, this user has been locked out"
        )
