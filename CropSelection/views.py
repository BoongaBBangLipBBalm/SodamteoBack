import jwt
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from CropSelection.models import FarmEnvironment
from CropSelection.serializers import EnvironmentSerializer
from Farm.models import FarmProfile
from Sodamteo import settings

import os
import joblib
import sklearn
import numpy as np


class CropSelection(APIView):
    def post(self, request):
        model = joblib.load(os.path.join(settings.MEDIA_ROOT, 'models/Linear_Regression_Crop_Selection.pkl'))

        auth_token = request.headers.get('Authorization', None).replace('Bearer ', '')
        payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])
        farmID = payload['farmID']

        N = request.GET.get('N')
        P = request.GET.get('P')
        K = request.GET.get('K')
        temperature = request.GET.get('temperature')
        humidity = request.GET.get('humidity')
        ph = request.GET.get('ph')
        rainfall = request.GET.get('rainfall')

        environment = FarmEnvironment.objects.create(farmID=farmID, N=N, P=P, K=K, temperature=temperature,
                                                     humidity=humidity, ph=ph, rainfall=rainfall)
        serializer = EnvironmentSerializer(environment)

        results = model.predict_proba([[N, P, K, temperature, humidity, ph, rainfall]])

        sorted_indices = np.argsort(results[0])[::-1][:3]

        probs = results[0][sorted_indices]
        crops = model.classes_[sorted_indices]

        return Response({'crops': crops, 'probs': probs, 'init_env': serializer}, status=status.HTTP_201_CREATED)


class CropEnvironment(APIView):
    def post(self, request):
        auth_token = request.headers.get('Authorization', None).replace('Bearer ', '')
        payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])
        farmID = payload['farmID']

        N = request.data.get('N')
        P = request.data.get('P')
        K = request.data.get('K')
        temperature = request.data.get('temperature')
        humidity = request.data.get('humidity')
        ph = request.data.get('ph')
        rainfall = request.data.get('rainfall')

        FarmEnvironment.objects.create(farmID=farmID, N=N, P=P, K=K, temperature=temperature,
                                       humidity=humidity, ph=ph, rainfall=rainfall)

        response = Response(status=status.HTTP_201_CREATED)
        response['Authorization'] = 'Bearer ' + auth_token

        return response

    def get(self, request):
        auth_token = request.headers.get('Authorization', None).replace('Bearer ', '')
        payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])
        farmID = payload['farmID']

        try:
            environmentList = FarmEnvironment.objects.filter(farmID=farmID)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

        serializerList = []
        for environment in environmentList:
            serializer = EnvironmentSerializer(environment)
            serializerList.append(serializer.data)

        response = Response(serializerList, status.HTTP_200_OK)
        response['Authorization'] = 'Bearer ' + auth_token

        return response
