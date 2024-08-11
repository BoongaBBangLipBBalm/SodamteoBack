from django.urls import path
from .views import CropSelection

urlpatterns = [
    path('crop_selection/', CropSelection.as_view(), name='crop_selection'),
]
