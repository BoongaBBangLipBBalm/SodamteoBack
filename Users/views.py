from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, Token
from .serializers import UserSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        refresh_token = TokenObtainPairSerializer.get_token(user)
        access_token = refresh_token.access_token
        verify_url = self.request.build_absolute_uri(reverse('verify-email', args=[str(access_token)]))
        send_mail(
            subject='Verify your email address',
            message=f'Click the following link to verify your email address: {verify_url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )


class VerifyEmail(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token, *args, **kwargs):
        try:
            user = User.objects.get(id=AccessToken(token).payload['id'])
            user.is_active = True
            user.save()
            return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.get(email=email)

        if user is None:
            return Response({'message': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(password):
            return Response({'message': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_active:
            return Response({'message': 'Email disabled'}, status=status.HTTP_400_BAD_REQUEST)

        print(user)

        token = TokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        response = Response({"message": "Logged in successfully",
                             "access_token": access_token,
                             "refresh_token": refresh_token}, status=status.HTTP_200_OK)

        return response


class Logout(APIView):
    def post(self, request):
        token = request.data.get('RefreshToken')
        refreshToken = RefreshToken(token)

        refreshToken.blacklist()

        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]


class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]
