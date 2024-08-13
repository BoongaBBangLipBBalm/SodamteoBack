from django.urls import path

from .views import DeviceManager

urlpatterns = [
    path('control/', DeviceManager.as_view(), name='control'),
]