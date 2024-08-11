from rest_framework.views import APIView
from rest_framework.response import Response

from Sodamteo import settings

import os
import joblib
import sklearn
import numpy as np


class CropSelection(APIView):
    def get(self, request):
        model = joblib.load(os.path.join(settings.MEDIA_ROOT, 'models/Linear_Regression_Crop_Selection.pkl'))

        # Serializer 만들기
        N = request.GET.get('N')
        P = request.GET.get('P')
        K = request.GET.get('K')
        temperature = request.GET.get('temperature')
        humidity = request.GET.get('humidity')
        ph = request.GET.get('ph')
        rainfall = request.GET.get('rainfall')

        results = model.predict_proba([[N, P, K, temperature, humidity, ph, rainfall]])

        sorted_indices = np.argsort(results[0])[::-1][:3]

        print(results, sorted_indices)

        probs = results[0][sorted_indices]
        crops = model.classes_[sorted_indices]

        return Response({'crops': crops, 'probs': probs})
