from api.clients.base_client import BaseAPIClient


class UserClient(BaseAPIClient):
    """
    Handles user-related API calls.
    """

    def get_user(self, user_id: int) -> dict:
        """GET /api/users/{id} — fetch a single user"""
        response = self.get(f"/api/users/{user_id}")
        return response.json()

    def get_users(self, page: int = 1) -> dict:
        """GET /api/users?page={n} — fetch paginated users"""
        response = self.get("/api/users", params={"page": page})
        return response.json()
