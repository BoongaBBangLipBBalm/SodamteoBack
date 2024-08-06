from django.urls import path
from .views import run_price_prediction_view

urlpatterns = [
    path('predict-price/', run_price_prediction_view, name='predict-price'),
]
