import requests
import os 
backend_url = os.getenv("BACKEND_URL", "http://localhost:8001")
class APIClient:
    """
    A client for interacting with the local Django REST API.
    """
    BASE_URL = f"{backend_url}/api/auth"

    @staticmethod
    def signup(username, email, password, password_confirm):
        """
        Handles user signup by sending a POST request to the API.
        """
        response = requests.post(
            f"{APIClient.BASE_URL}/signup/",
            json={
                "username": username,
                "email": email,
                "password": password,
                "password_confirm": password_confirm,
            },
        )

        if response.status_code != 201:
            print(f"Error: {response.status_code}")
            print(f"Response body: {response.json()}")

        return response
