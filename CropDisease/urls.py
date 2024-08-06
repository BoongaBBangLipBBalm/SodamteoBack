from django.urls import path
from .views import DiseaseDetection, GetFarmDisease

urlpatterns = [
    path("detect_disease/", DiseaseDetection.as_view(), name="disease_detection"),
    path("get_farm_disease/", GetFarmDisease.as_view(), name="get_farm_disease"),
]
