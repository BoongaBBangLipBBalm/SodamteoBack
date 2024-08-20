from django.http import JsonResponse
from rest_framework.views import APIView

from .price_predict import price_prediction
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

        return JsonResponse({'crop': crop, 'predictions': list(predictions)}, status=200)
