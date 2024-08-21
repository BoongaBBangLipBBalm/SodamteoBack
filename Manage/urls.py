from django.urls import path

from .views import DeviceManager, autoManage

urlpatterns = [
    path('control', DeviceManager.as_view(), name='control'),
    path('auto', autoManage.as_view(), name='auto'),
]