from django.urls import path

from SodamteoBack.Manage.views import Aircon, Humid, Co2, GetFarm

urlpatterns = [
    path('check/', GetFarm.as_view(), name='check_farm'),

    path('check/device/aircon', Aircon.as_view(), name='get_airconditioner'),
    path('check/device/humid', Humid.as_view(), name='get_humidifier'),
    path('check/device/co2', Co2.as_view(), name='get_co2'),

    path('check/device/manage/aircon', Aircon.as_view(), name='patch_airconditioner'),
    path('check/device/manage/humid', Humid.as_view(), name='patch_humidifier'),
    path('check/device/manage/co2', Co2.as_view(), name='patch_co2'),
]