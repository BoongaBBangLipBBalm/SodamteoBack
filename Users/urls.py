from django.urls import path
from .views import UserCreate, CustomTokenObtainPairView, CustomTokenRefreshView, VerifyEmail

urlpatterns = [
    path('register/', UserCreate.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('verify-email/<str:token>/', VerifyEmail.as_view(), name='verify-email'),
]
