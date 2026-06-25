from api.clients.base_client import BaseAPIClient


class AuthClient(BaseAPIClient):
    """Auth calls against the SauceDemo Mock API."""

    def login(self, username: str, password: str):
        return self.post("/api/auth/login", json={
            "username": username,
            "password": password
        })
