from django.shortcuts import render

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer
from .tokens import CustomTokenObtainPairSerializer
from lms_project.api import success, error

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """Public endpoint to register a new user."""

    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.instance
        refresh = RefreshToken.for_user(user)
        tokens = {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "is_admin": getattr(user, "is_admin", False),
                "is_student": getattr(user, "is_student", False),
            },
        }
        headers = self.get_success_headers(serializer.data)
        return success(result=tokens, message="User created", code=201, headers=headers)


class CustomLoginView(TokenObtainPairView):
    """JWT login using email instead of username."""

    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return success(result=response.data, code=response.status_code)


class LogoutView(APIView):
    """Invalidate a refresh token to log the user out."""

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            token = RefreshToken(request.data["refresh"])
            token.blacklist()
            return success(message="Logged out", code=200, result=None)
        except Exception:
            return error(message="Invalid refresh token", code=400)


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return success(result=response.data, code=response.status_code)
