from django.urls import path
from .views import UserCreate, Login, CustomTokenObtainPairView, CustomTokenRefreshView, VerifyEmail

urlpatterns = [
    path('register/', UserCreate.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('verify-email/<str:token>/', VerifyEmail.as_view(), name='verify-email'),
]
