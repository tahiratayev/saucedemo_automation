"""
API tests against the SauceDemo Mock API (FastAPI).
Run with: pytest -m api
Requires: uvicorn running on localhost:8000
          or use the pytest fixture below that spins it up automatically.
"""
import pytest
import allure
import threading
import time
from jsonschema import validate
import requests
from api.clients.auth_client import AuthClient
from api.clients.product_client import ProductClient
from api.clients.order_client import OrderClient
from api.schemas.schemas import LOGIN_SUCCESS_SCHEMA, PRODUCT_SCHEMA, ORDER_SCHEMA


# ------------------------------------------------
# Fixtures — spin up mock server for tests
# ------------------------------------------------

@pytest.fixture(scope="session", autouse=False)
def mock_api_server():
    """Start FastAPI mock server in a background thread for the test session."""
    import uvicorn
    from mock_api.main import app

    config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="error")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    # Wait for server to be ready
    for _ in range(20):
        try:
            requests.get("http://127.0.0.1:8000/health", timeout=1)
            break
        except Exception:
            time.sleep(0.3)

    yield "http://127.0.0.1:8000"
    server.should_exit = True


@pytest.fixture(scope="module")
def auth_client(mock_api_server):
    client = AuthClient(base_url=mock_api_server)
    yield client
    client.close()


@pytest.fixture(scope="module")
def product_client(mock_api_server):
    client = ProductClient(base_url=mock_api_server)
    yield client
    client.close()


@pytest.fixture(scope="module")
def order_client(mock_api_server):
    client = OrderClient(base_url=mock_api_server)
    yield client
    client.close()


# ------------------------------------------------
# Auth tests
# ------------------------------------------------

@allure.feature("API — Auth")
@allure.story("Login")
@pytest.mark.api
def test_login_success(auth_client):
    """Valid credentials return token + user info."""
    with allure.step("POST /api/auth/login with valid credentials"):
        response = auth_client.login("standard_user", "secret_sauce")

    with allure.step("Verify 200 status"):
        assert response.status_code == 200

    with allure.step("Verify response schema"):
        validate(instance=response.json(), schema=LOGIN_SUCCESS_SCHEMA)

    with allure.step("Verify token is non-empty"):
        assert response.json()["token"]


@allure.feature("API — Auth")
@allure.story("Login")
@pytest.mark.api
def test_login_invalid_password(auth_client):
    """Wrong password returns 401."""
    with allure.step("POST with wrong password"):
        with pytest.raises(Exception) as exc:
            auth_client.login("standard_user", "wrong_password")
        assert "401" in str(exc.value)


@allure.feature("API — Auth")
@allure.story("Login")
@pytest.mark.api
def test_login_locked_user(auth_client):
    """Locked user returns 403."""
    with allure.step("POST with locked_out_user"):
        with pytest.raises(Exception) as exc:
            auth_client.login("locked_out_user", "secret_sauce")
        assert "403" in str(exc.value)


# ------------------------------------------------
# Product tests
# ------------------------------------------------

@allure.feature("API — Products")
@allure.story("Catalog")
@pytest.mark.api
def test_get_all_products(product_client):
    """GET /api/products returns 6 products."""
    with allure.step("GET /api/products"):
        response = product_client.get_products()

    with allure.step("Verify 6 products returned"):
        products = response.json()
        assert len(products) == 6

    with allure.step("Verify schema of first product"):
        validate(instance=products[0], schema=PRODUCT_SCHEMA)


@allure.feature("API — Products")
@allure.story("Catalog")
@pytest.mark.api
def test_get_single_product(product_client):
    """GET /api/products/1 returns correct product."""
    with allure.step("GET /api/products/1"):
        response = product_client.get_product(1)

    with allure.step("Verify product name"):
        product = response.json()
        assert product["name"] == "Sauce Labs Backpack"
        assert product["price"] == 29.99


@allure.feature("API — Products")
@allure.story("Catalog")
@pytest.mark.api
def test_get_nonexistent_product(product_client):
    """GET /api/products/999 returns 404."""
    with allure.step("GET /api/products/999"):
        with pytest.raises(Exception) as exc:
            product_client.get_product(999)
        assert "404" in str(exc.value)


# ------------------------------------------------
# Order tests
# ------------------------------------------------

@allure.feature("API — Orders")
@allure.story("Create Order")
@pytest.mark.api
def test_create_order_success(order_client):
    """Valid order returns confirmed status with correct totals."""
    payload = {
        "user_id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "postal_code": "12345",
        "items": [
            {"product_id": 1, "name": "Sauce Labs Backpack", "price": 29.99, "quantity": 1}
        ]
    }
    with allure.step("POST /api/orders"):
        response = order_client.create_order(payload)

    with allure.step("Verify 201 status"):
        assert response.status_code == 201

    with allure.step("Verify schema"):
        validate(instance=response.json(), schema=ORDER_SCHEMA)

    with allure.step("Verify totals"):
        order = response.json()
        assert order["status"] == "confirmed"
        assert order["subtotal"] == 29.99
        assert round(order["total"], 2) == round(29.99 * 1.08, 2)


@allure.feature("API — Orders")
@allure.story("Create Order")
@pytest.mark.api
def test_create_order_missing_info(order_client):
    """Order with missing customer info returns 400."""
    payload = {
        "user_id": 1,
        "first_name": "",
        "last_name": "Doe",
        "postal_code": "12345",
        "items": [
            {"product_id": 1, "name": "Sauce Labs Backpack", "price": 29.99, "quantity": 1}
        ]
    }
    with allure.step("POST with empty first_name"):
        with pytest.raises(Exception) as exc:
            order_client.create_order(payload)
        assert "400" in str(exc.value)


@allure.feature("API — Orders")
@allure.story("Create Order")
@pytest.mark.api
def test_create_order_multi_item_total(order_client):
    """Multi-item order calculates correct subtotal."""
    payload = {
        "user_id": 1,
        "first_name": "Jane",
        "last_name": "Smith",
        "postal_code": "99999",
        "items": [
            {"product_id": 1, "name": "Sauce Labs Backpack",  "price": 29.99, "quantity": 1},
            {"product_id": 2, "name": "Sauce Labs Bike Light", "price": 9.99,  "quantity": 2},
        ]
    }
    with allure.step("POST multi-item order"):
        response = order_client.create_order(payload)

    with allure.step("Verify subtotal = 29.99 + 9.99*2"):
        order = response.json()
        assert order["subtotal"] == round(29.99 + 9.99 * 2, 2)
        assert round(order["total"], 2) == round(order["subtotal"] * 1.08, 2)
