import pytest
import allure
from pytest_bdd import given, when, then, scenario, parsers
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutStepOnePage, CheckoutStepTwoPage, CheckoutCompletePage


# ------------------------------------------------
# Scenarios
# ------------------------------------------------

@allure.feature("Checkout")
@allure.story("Happy Path")
@scenario("../features/checkout.feature", "Complete a full checkout successfully")
def test_full_checkout():
    pass

@allure.feature("Checkout")
@allure.story("Validation")
@scenario("../features/checkout.feature", "Checkout fails with missing first name")
def test_missing_first_name():
    pass

@allure.feature("Checkout")
@allure.story("Validation")
@scenario("../features/checkout.feature", "Checkout fails with missing last name")
def test_missing_last_name():
    pass

@allure.feature("Checkout")
@allure.story("Validation")
@scenario("../features/checkout.feature", "Checkout fails with missing postal code")
def test_missing_postal_code():
    pass

@allure.feature("Checkout")
@allure.story("Price Calculation")
@scenario("../features/checkout.feature", "Order total matches subtotal plus tax")
def test_total_calculation():
    pass

@allure.feature("Checkout")
@allure.story("Navigation")
@scenario("../features/checkout.feature", "Cancel checkout returns to cart")
def test_cancel_checkout():
    pass


# ------------------------------------------------
# Steps
# ------------------------------------------------

@given("I am logged in and have added a product to the cart")
def logged_in_with_product(page, base_url):
    with allure.step("Login and add first product to cart"):
        LoginPage(page, base_url).login("standard_user", "secret_sauce")
        InventoryPage(page).add_first_item_to_cart()

@given("I am on the cart page")
def navigate_to_cart(page):
    with allure.step("Navigate to cart"):
        InventoryPage(page).go_to_cart()
        assert CartPage(page).is_loaded(), "Expected cart page"

@when("I proceed to checkout")
def proceed_to_checkout(page):
    with allure.step("Click checkout button"):
        CartPage(page).proceed_to_checkout()
        assert CheckoutStepOnePage(page).is_loaded(), "Expected checkout step 1"

@when(parsers.parse('I fill in my details with first name "{first}" last name "{last}" and postal code "{postal}"'))
def fill_checkout_info(page, first, last, postal):
    with allure.step(f"Fill info: {first} {last}, {postal}"):
        step_one = CheckoutStepOnePage(page)
        step_one.fill_info(first, last, postal)

@when("I continue to order overview")
def continue_to_overview(page):
    with allure.step("Click continue to step 2"):
        CheckoutStepOnePage(page).continue_checkout()
        assert CheckoutStepTwoPage(page).is_loaded(), "Expected checkout step 2"

@when("I finish the order")
def finish_order(page):
    with allure.step("Click finish"):
        CheckoutStepTwoPage(page).finish_order()

@when("I submit checkout info with empty first name")
def submit_empty_first_name(page):
    with allure.step("Submit with empty first name"):
        CheckoutStepOnePage(page).fill_info("", "Doe", "12345")
        CheckoutStepOnePage(page).continue_checkout()

@when("I submit checkout info with empty last name")
def submit_empty_last_name(page):
    with allure.step("Submit with empty last name"):
        CheckoutStepOnePage(page).fill_info("John", "", "12345")
        CheckoutStepOnePage(page).continue_checkout()

@when("I submit checkout info with empty postal code")
def submit_empty_postal(page):
    with allure.step("Submit with empty postal code"):
        CheckoutStepOnePage(page).fill_info("John", "Doe", "")
        CheckoutStepOnePage(page).continue_checkout()

@when("I cancel checkout")
def cancel_checkout(page):
    with allure.step("Click cancel on checkout step 1"):
        CheckoutStepOnePage(page).cancel()

@then("I should see the order confirmation page")
def verify_confirmation_page(page):
    with allure.step("Verify checkout-complete URL"):
        assert CheckoutCompletePage(page).is_loaded(), \
            f"Expected confirmation page, got: {page.url}"

@then(parsers.parse('the confirmation header should say "{expected_header}"'))
def verify_confirmation_header(page, expected_header):
    with allure.step(f"Verify header text: {expected_header}"):
        actual = CheckoutCompletePage(page).get_header()
        assert actual == expected_header, \
            f"Expected '{expected_header}' but got '{actual}'"

@then("I should see a checkout error message")
def verify_checkout_error(page):
    with allure.step("Verify error message is visible"):
        step_one = CheckoutStepOnePage(page)
        assert step_one.is_error_visible(), "Expected error message but none visible"

@then("the order total should equal subtotal plus tax")
def verify_total_calculation(page):
    with allure.step("Verify total = subtotal + tax"):
        step_two = CheckoutStepTwoPage(page)
        subtotal = step_two.get_subtotal()
        tax = step_two.get_tax()
        total = step_two.get_total()
        expected = round(subtotal + tax, 2)
        assert round(total, 2) == expected, \
            f"Total {total} != subtotal {subtotal} + tax {tax} = {expected}"

@then("I should be back on the cart page")
def verify_back_on_cart(page):
    with allure.step("Verify cart page URL"):
        assert CartPage(page).is_loaded(), \
            f"Expected cart page, got: {page.url}"
