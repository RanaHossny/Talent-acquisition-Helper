import requests

class APIClient:
    """
    A client for interacting with the local Django REST API.
    """
    BASE_URL = "http://127.0.0.1:8000/api/auth"

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
