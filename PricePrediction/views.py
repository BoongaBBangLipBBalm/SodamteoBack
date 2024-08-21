from .price_predict import price_prediction
from django.http import JsonResponse
from rest_framework.views import APIView
import pandas as pd
import os
from django.conf import settings
from datetime import datetime, timedelta
from .models import CropPricePredict


def run_price_prediction_view(request):
    if request.method == 'GET':
        price_prediction()
        return JsonResponse({'status': 'success'})




class GetPredict(APIView):
    def get(self, request):
        crop = request.GET.get('crop')
        if not crop:
            return JsonResponse({'error': 'crop is required'}, status=400)

        predictions = CropPricePredict.objects.filter(crop=crop).values('date', 'price')

        # CSV 파일 로드
        csv_path = os.path.join(settings.MEDIA_ROOT, 'Rice_Price_data.csv')
        data_df = pd.read_csv(csv_path)

        recent_data = data_df.tail(12)

        # 응답 데이터 포매팅
        recent_data = recent_data[['date', 'price']]
        recent_data_json = recent_data.to_dict(orient='records')

        return JsonResponse({
            'crop': crop,
            'predictions': list(predictions),
            'recent_data': recent_data_json
        }, status=200)

