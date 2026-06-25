import pytest
import allure
from pytest_bdd import given, when, then, scenario, parsers
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


# ------------------------------------------------
# Scenarios
# ------------------------------------------------

@allure.feature("Inventory")
@allure.story("Page Load")
@scenario("../features/inventory.feature", "Inventory page loads with products")
def test_inventory_loads():
    pass

@allure.feature("Inventory")
@allure.story("Cart")
@scenario("../features/inventory.feature", "Add product to cart")
def test_add_to_cart():
    pass

@allure.feature("Inventory")
@allure.story("Sorting")
@scenario("../features/inventory.feature", "Sort products by price low to high")
def test_sort_by_price():
    pass

@allure.feature("Inventory")
@allure.story("Sorting")
@scenario("../features/inventory.feature", "Sort products by name Z to A")
def test_sort_by_name_za():
    pass


# ------------------------------------------------
# Steps
# ------------------------------------------------

@given("I am logged in as a standard user")
def login_as_standard_user(page, base_url):
    with allure.step("Login with valid credentials"):
        LoginPage(page, base_url).login("standard_user", "secret_sauce")


@then("I should see the inventory page")
def verify_inventory_page_loaded(page):
    with allure.step("Verify inventory page is loaded"):
        inventory = InventoryPage(page)
        assert inventory.is_loaded(), f"Expected inventory page, got: {page.url}"
        assert inventory.get_page_title() == "Products"


@then("the page should display 6 products")
def verify_product_count(page):
    with allure.step("Verify 6 products are displayed"):
        count = InventoryPage(page).get_product_count()
        assert count == 6, f"Expected 6 products but got {count}"


@when("I add the first product to the cart")
def add_first_product(page):
    with allure.step("Click Add to cart on first product"):
        InventoryPage(page).add_first_item_to_cart()


@then("the cart badge should show 1")
def verify_cart_badge(page):
    with allure.step("Verify cart badge shows 1"):
        count = InventoryPage(page).get_cart_count()
        assert count == 1, f"Expected cart count 1 but got {count}"


@when("I sort products by price low to high")
def sort_price_low_high(page):
    with allure.step("Sort by price: low to high"):
        InventoryPage(page).sort_by("lohi")


@then("products should be sorted by ascending price")
def verify_price_ascending(page):
    with allure.step("Verify prices are in ascending order"):
        prices = InventoryPage(page).get_product_prices()
        assert prices == sorted(prices), \
            f"Prices not sorted ascending: {prices}"


@when("I sort products by name Z to A")
def sort_name_za(page):
    with allure.step("Sort by name: Z to A"):
        InventoryPage(page).sort_by("za")


@then("products should be sorted in reverse alphabetical order")
def verify_name_za(page):
    with allure.step("Verify names are in Z to A order"):
        names = InventoryPage(page).get_product_names()
        assert names == sorted(names, reverse=True), \
            f"Names not sorted Z to A: {names}"
