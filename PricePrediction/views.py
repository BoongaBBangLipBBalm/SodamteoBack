from django.http import JsonResponse

from .price_perdict import price_prediction


def run_price_prediction_view(request):
    if request.method == 'GET':
        price_prediction()
        return JsonResponse({'status': 'success'})
