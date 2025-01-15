import requests
import os
backend_url = os.getenv("BACKEND_URL", "http://localhost:8001")
class APIClient:
    """
    A client for interacting with the local Django REST API.
    """
    BASE_URL = f"{backend_url}/api/auth"
    @staticmethod
    def login(username, password):
        """
        Handles user login by sending a POST request to the API.
        """
        response = requests.post(
            f"{APIClient.BASE_URL}/login/",
            json={"username": username, "password": password},
        )
        return response
