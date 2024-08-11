from django.http import JsonResponse
from rest_framework.views import APIView
from .models import CropPricePredict
from .price_perdict import price_prediction


def run_price_prediction_view(request):
    if request.method == 'GET':
        price_prediction()
        return JsonResponse({'status': 'success'})


class GetPredict(APIView):
    def get(self, request):
        crop = request.GET.get('crop')
        if not crop:
            return JsonResponse({'error': 'crop is required'}, status=400)
        prices = CropPricePredict.objects.filter(crop=crop).values('date', 'price')

        return JsonResponse({'crop': crop, 'predictions': list(prices)}, status=200)
