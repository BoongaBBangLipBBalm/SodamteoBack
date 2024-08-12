from django.urls import path

from .views import Airconditioner, Humidifier, CO2

urlpatterns = [
    path('airconditioner/', Airconditioner.as_view(), name='airconditioner'),
    path('humidifier/', Humidifier.as_view(), name='humidifier'),
    path('co2/', CO2.as_view(), name='co2'),
]