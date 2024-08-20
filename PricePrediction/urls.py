from django.urls import path
from .views import run_price_prediction_view, GetPredict

urlpatterns = [
    path('predict-price/', run_price_prediction_view, name='predict-price'),
    path('getpredict/', GetPredict.as_view(), name='get-predict'),
]
