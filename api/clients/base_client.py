import requests
import os


class BaseAPIClient:
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv("API_BASE_URL", "http://localhost:8000")
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def get(self, endpoint: str, **kwargs):
        response = self.session.get(f"{self.base_url}{endpoint}", **kwargs)
        response.raise_for_status()
        return response

    def post(self, endpoint: str, **kwargs):
        response = self.session.post(f"{self.base_url}{endpoint}", **kwargs)
        response.raise_for_status()  # FIX: consistent error handling for POST too
        return response

    def close(self):
        self.session.close()
