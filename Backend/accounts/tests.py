from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import UserCollection
from rest_framework_simplejwt.tokens import RefreshToken

class UserCollectionRetrieveViewTestCase(APITestCase):
    """
    Test cases for UserCollectionRetrieveView.
    """

    def setUp(self):
        """
        Set up the test environment.
        """
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.collection = UserCollection.objects.create(user=self.user)  
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

    def test_get_collection_authenticated_user(self):
        """
        Test that an authenticated user can retrieve their collection.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get('/api/collection/')  

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.collection.name)

    def test_get_collection_unauthenticated_user(self):
        """
        Test that an unauthenticated user cannot retrieve a collection.
        """
        response = self.client.get('/api/collection/') 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class SignUpViewTestCase(APITestCase):
    """
    Test cases for SignUpView.
    """

    def test_signup_success(self):
        """
        Test that a new user can sign up successfully.
        """
        data = {
            "username": "newuser",
            "password": "bafbfrwbftfajfbdajfb",
            "password_confirm": "bafbfrwbftfajfbdajfb",
            "email": "newuser@example.com"

        }

        response = self.client.post('/api/auth/signup/', data, format='json')  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access_token', response.data)
        self.assertEqual(response.data['user']['username'], "newuser")

    def test_signup_missing_fields(self):
        """
        Test that missing fields in the signup request return an error.
        """
        data = {
            "username": "newuser",
            "password": "newpassword"
        }

        response = self.client.post('/api/auth/signup/', data, format='json')  
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTestCase(APITestCase):
    """
    Test cases for LoginView.
    """

    def setUp(self):
        """
        Set up the test environment by creating a user.
        """
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_login_success(self):
        """
        Test that a user can log in successfully with valid credentials.
        """
        data = {
            "username": "testuser",
            "password": "testpassword"
        }

        response = self.client.post('/api/auth/login/', data, format='json')  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)

    def test_login_invalid_credentials(self):
        """
        Test that invalid credentials return an error.
        """
        data = {
            "username": "testuser",
            "password": "wrongpassword"
        }

        response = self.client.post('/api/auth/login/', data, format='json')  
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], "Invalid credentials.")
