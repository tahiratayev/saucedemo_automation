from pydantic import BaseModel, EmailStr
from typing import Optional


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    token: str
    user_id: int
    username: str


class OrderItem(BaseModel):
    product_id: int
    name: str
    price: float
    quantity: int


class OrderRequest(BaseModel):
    user_id: int
    items: list[OrderItem]
    first_name: str
    last_name: str
    postal_code: str


class OrderResponse(BaseModel):
    order_id: str
    status: str
    subtotal: float
    tax: float
    total: float
    items: list[OrderItem]


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image_url: str
