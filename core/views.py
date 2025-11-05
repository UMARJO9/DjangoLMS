from django.shortcuts import render

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .tokens import CustomTokenObtainPairSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """Public endpoint to register a new user."""

    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class CustomLoginView(TokenObtainPairView):
    """JWT login using email instead of username."""

    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(APIView):
    """Invalidate a refresh token to log the user out."""

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            token = RefreshToken(request.data["refresh"])
            token.blacklist()
            return Response({"detail": "Logged out successfully."})
        except Exception:
            return Response({"error": "Invalid refresh token."}, status=400)

