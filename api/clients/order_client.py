from api.clients.base_client import BaseAPIClient


class OrderClient(BaseAPIClient):
    """Order calls against the SauceDemo Mock API."""

    def create_order(self, payload: dict):
        return self.post("/api/orders", json=payload)

    def get_order(self, order_id: str):
        return self.get(f"/api/orders/{order_id}")
