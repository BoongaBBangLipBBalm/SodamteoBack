from django.urls import path
from .views import CropSelection, CropEnvironment

urlpatterns = [
    path('crop_selection/', CropSelection.as_view(), name='crop_selection'),
    path('current_environment/', CropEnvironment.as_view(), name='current_environment'),
]
