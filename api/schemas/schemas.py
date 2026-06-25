LOGIN_SUCCESS_SCHEMA = {
    "type": "object",
    "required": ["token", "user_id", "username"],
    "properties": {
        "token":    {"type": "string"},
        "user_id":  {"type": "integer"},
        "username": {"type": "string"},
    },
    "additionalProperties": False
}

PRODUCT_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "description", "price", "image_url"],
    "properties": {
        "id":          {"type": "integer"},
        "name":        {"type": "string"},
        "description": {"type": "string"},
        "price":       {"type": "number"},
        "image_url":   {"type": "string"},
    }
}

ORDER_SCHEMA = {
    "type": "object",
    "required": ["order_id", "status", "subtotal", "tax", "total", "items"],
    "properties": {
        "order_id": {"type": "string"},
        "status":   {"type": "string"},
        "subtotal": {"type": "number"},
        "tax":      {"type": "number"},
        "total":    {"type": "number"},
        "items":    {"type": "array"},
    }
}
