import requests

class APIClient:
    """
    A client for interacting with the local Django REST API.
    """
    BASE_URL = "http://127.0.0.1:8000/api/auth"

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
        return response
