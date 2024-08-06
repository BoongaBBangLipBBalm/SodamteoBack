from django.urls import path
from .views import DiseaseDetection, GetFarmDisease, DeleteDiseaseLog

urlpatterns = [
    path("detect_disease/", DiseaseDetection.as_view(), name="disease_detection"),
    path("get_farm_disease/", GetFarmDisease.as_view(), name="get_farm_disease"),
    path("delete_disease_log/", DeleteDiseaseLog.as_view(), name="delete_disease_log"),
]
