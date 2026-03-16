from urllib import request

from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import LoginSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all() 
    serializer_class = UserSerializer 
    permission_classes = [AllowAny] # Allow anyone to access this view for registration


class LoginView(APIView):

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = authenticate(username=username, password=password)

            if user:
                token, created = Token.objects.get_or_create(user=user)

                return Response({
                    "token": token.key,
                    "message": "Login successful"
                })

            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)