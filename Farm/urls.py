from django.urls import path
from .views import GetFarm, CreateFarm, UpdateFarm, DeleteFarm, GetFarmList

urlpatterns = [
    path("getallfarms/", GetFarmList.as_view(), name="getallfarm"),
    path("getfarm/", GetFarm.as_view(), name="getfarm"),
    path("createfarm/", CreateFarm.as_view(), name="createfarm"),
    path("updatefarm/", UpdateFarm.as_view(), name="updatefarm"),
    path("deletefarm/", DeleteFarm.as_view(), name="deletefarm"),
]
