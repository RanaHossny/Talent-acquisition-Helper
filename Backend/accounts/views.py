from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView
from .serializers import LoginSerializer, SignupSerializer
from rest_framework.permissions import AllowAny
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from .models import UserCollection
from .serializers import UserCollectionSerializer

class UserCollectionRetrieveView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Get the authenticated user
        user = request.user

        try:
            # Get the user's collection
            collection = UserCollection.objects.get(user=user)
        except UserCollection.DoesNotExist:
            raise NotFound("Collection not found for this user.")

        # Serialize the collection and return the response
        serializer = UserCollectionSerializer(collection)
        return Response(serializer.data)

class SignUpView(CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]  # Ensuring the signup endpoint is publicly accessible

    def create(self, request, *args, **kwargs):
        # Validate user data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate the access token directly from the RefreshToken (no need to return refresh token)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Return the user data along with the access token (only)
        return Response({
            'user': SignupSerializer(user).data,  # Return the user data
            'access_token': access_token  # Return only the access token
        }, status=status.HTTP_201_CREATED)

class LoginView(GenericAPIView):
    permission_classes = [AllowAny]  # Allow anyone to access the login endpoint
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        # Validate login data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Authenticate user with the credentials
        user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        
        if user is None:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

        # Generate the access token from the RefreshToken (you don't need to return the refresh token)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Return the response with the access token (no need to send refresh token)
        return Response({
            'message': 'Login successful',
            'access_token': access_token  # Only return the access token
        }, status=status.HTTP_200_OK)