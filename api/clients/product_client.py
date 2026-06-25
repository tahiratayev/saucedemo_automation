from api.clients.base_client import BaseAPIClient


class ProductClient(BaseAPIClient):
    """Product calls against the SauceDemo Mock API."""

    def get_products(self):
        return self.get("/api/products")

    def get_product(self, product_id: int):
        return self.get(f"/api/products/{product_id}")
