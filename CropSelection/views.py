from datetime import datetime, timedelta
import random

import jwt
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from CropSelection.models import FarmEnvironment, DefaultEnvironment
from CropSelection.serializers import CurrEnvSerializer, OptEnvSerializer
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

        N = float(request.data.get('N'))
        P = float(request.data.get('P'))
        K = float(request.data.get('K'))
        temperature = float(request.data.get('temperature'))
        humidity = float(request.data.get('humidity'))
        ph = float(request.data.get('ph'))
        rainfall = float(request.data.get('rainfall'))

        # try:
        #     farm = FarmProfile.objects.get(farmID=farmID)
        # except Exception as e:
        #     return Response({'error': "No such farm"}, status=status.HTTP_404_NOT_FOUND)

        # environment = FarmEnvironment.objects.create(farmID=farm, N=N, P=P, K=K, temperature=temperature,
        #                                              humidity=humidity, ph=ph, rainfall=rainfall)
        # serializer = CurrEnvSerializer(environment)

        results = model.predict_proba([[N, P, K, temperature, humidity, ph, rainfall]])

        sorted_indices = np.argsort(results[0])[::-1][:3]

        probs = results[0][sorted_indices]
        crops = model.classes_[sorted_indices]

        data = {}
        for c, p in zip(crops, probs):
            data[c] = p

        # response = Response({'crops': crops, 'probs': probs, 'init_env': serializer}, status=status.HTTP_201_CREATED)
        response = Response(data, status=status.HTTP_201_CREATED)
        response['Authorization'] = auth_token

        return response


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

        try:
            farm = FarmProfile.objects.get(farmID=farmID)
        except Exception as e:
            return Response({'error': "No such farm"}, status=status.HTTP_404_NOT_FOUND)

        FarmEnvironment.objects.create(farmID=farm, N=N, P=P, K=K, temperature=temperature,
                                       humidity=humidity, ph=ph, rainfall=rainfall)

        response = Response(status=status.HTTP_201_CREATED)
        response['Authorization'] = auth_token

        return response

    def get(self, request):
        auth_token = request.headers.get('Authorization', None).replace('Bearer ', '')
        payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])
        farmID = payload['farmID']

        try:
            cropName = FarmProfile.objects.get(farmID=farmID).cropName
        except Exception as e:
            return Response({'error': "No such farm"}, status=status.HTTP_404_NOT_FOUND)

        try:
            defEnv = DefaultEnvironment.objects.get(cropName=cropName)
        except Exception as e:
            return Response({'error': f"No info for {cropName}"}, status=status.HTTP_404_NOT_FOUND)

        try:
            environmentList = FarmEnvironment.objects.filter(farmID=farmID).order_by('-timestamp')
        except Exception as e:
            return Response({'error': "Nothing to load"}, status=status.HTTP_404_NOT_FOUND)

        currEnvSerializers = []
        cnt = 0
        for environment in environmentList:
            serializer = CurrEnvSerializer(environment)
            currEnvSerializers.append(serializer.data)
            cnt += 1
            if cnt == 5: break

        optEnvSerializer = OptEnvSerializer(defEnv)

        response = Response({"Current": currEnvSerializers,
                             "Opt": optEnvSerializer.data}, status.HTTP_200_OK)
        response['Authorization'] = auth_token

        return response
