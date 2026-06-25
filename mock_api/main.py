"""
SauceDemo Mock API — FastAPI
Simulates the backend that SauceDemo doesn't expose publicly.
Used for API-layer tests without hitting a real service.
"""
import uuid
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from mock_api.models import (
    LoginRequest, LoginResponse,
    OrderRequest, OrderResponse,
    Product, OrderItem
)

app = FastAPI(
    title="SauceDemo Mock API",
    description="Mock backend for SauceDemo automation tests",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------
# In-memory data store
# ------------------------------------------------

USERS = {
    "standard_user":      {"id": 1, "password": "secret_sauce"},
    "locked_out_user":    {"id": 2, "password": "secret_sauce"},
    "problem_user":       {"id": 3, "password": "secret_sauce"},
    "performance_glitch_user": {"id": 4, "password": "secret_sauce"},
}

LOCKED_USERS = {"locked_out_user"}

PRODUCTS = [
    Product(id=1, name="Sauce Labs Backpack",
            description="carry.allTheThings() with the sleek, streamlined Sly Pack",
            price=29.99, image_url="/static/media/sauce-backpack-1200x1500.jpg"),
    Product(id=2, name="Sauce Labs Bike Light",
            description="A red light isn't the desired state in testing but it sure helps",
            price=9.99, image_url="/static/media/bike-light-1200x1500.jpg"),
    Product(id=3, name="Sauce Labs Bolt T-Shirt",
            description="Get your testing superhero on with the Sauce Labs bolt T-shirt",
            price=15.99, image_url="/static/media/bolt-shirt-1200x1500.jpg"),
    Product(id=4, name="Sauce Labs Fleece Jacket",
            description="It's not every day that you come across a midweight quarter-zip",
            price=49.99, image_url="/static/media/sauce-pullover-1200x1500.jpg"),
    Product(id=5, name="Sauce Labs Onesie",
            description="Rib snap infant onesie for the junior automation engineer",
            price=7.99, image_url="/static/media/red-onesie-1200x1500.jpg"),
    Product(id=6, name="Test.allTheThings() T-Shirt (Red)",
            description="This classic Sauce Labs t-shirt is perfect to wear at any testing conference",
            price=15.99, image_url="/static/media/red-tatt-1200x1500.jpg"),
]

ORDERS: dict = {}

TAX_RATE = 0.08


# ------------------------------------------------
# Auth endpoints
# ------------------------------------------------

@app.post("/api/auth/login", response_model=LoginResponse, status_code=200)
def login(request: LoginRequest):
    user = USERS.get(request.username)

    if not user or user["password"] != request.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    if request.username in LOCKED_USERS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sorry, this user has been locked out."
        )

    token = f"mock-token-{uuid.uuid4().hex[:16]}"
    return LoginResponse(token=token, user_id=user["id"], username=request.username)


# ------------------------------------------------
# Product endpoints
# ------------------------------------------------

@app.get("/api/products", response_model=list[Product])
def get_products():
    return PRODUCTS


@app.get("/api/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    product = next((p for p in PRODUCTS if p.id == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    return product


# ------------------------------------------------
# Order endpoints
# ------------------------------------------------

@app.post("/api/orders", response_model=OrderResponse, status_code=201)
def create_order(request: OrderRequest):
    if not request.items:
        raise HTTPException(status_code=400, detail="Order must contain at least one item")
    if not request.first_name or not request.last_name or not request.postal_code:
        raise HTTPException(status_code=400, detail="Customer info incomplete")

    subtotal = round(sum(item.price * item.quantity for item in request.items), 2)
    tax = round(subtotal * TAX_RATE, 2)
    total = round(subtotal + tax, 2)
    order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"

    order = OrderResponse(
        order_id=order_id,
        status="confirmed",
        subtotal=subtotal,
        tax=tax,
        total=total,
        items=request.items
    )
    ORDERS[order_id] = order
    return order


@app.get("/api/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: str):
    order = ORDERS.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    return order


# ------------------------------------------------
# Health check
# ------------------------------------------------

@app.get("/health")
def health():
    return {"status": "ok", "service": "saucedemo-mock-api"}
