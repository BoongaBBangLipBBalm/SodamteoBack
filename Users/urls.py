from django.urls import path
from .views import UserCreate, Login, Logout, CustomTokenObtainPairView, CustomTokenRefreshView, VerifyEmail

urlpatterns = [
    path('register/', UserCreate.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('verify-email/<str:token>/', VerifyEmail.as_view(), name='verify-email'),
]
