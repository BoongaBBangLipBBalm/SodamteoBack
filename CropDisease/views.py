import base64
import os

import cv2
import jwt
import numpy as np
from django.core.files.base import ContentFile

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from Farm.models import FarmProfile
from Sodamteo import settings
from .models import DiseaseLog
from .detect_disease import detect_disease

import os

from .serializers import DiseaseSerializer

SECRET_KEY = settings.SECRET_KEY


class DiseaseDetection(APIView):
    """
    질병 탐지 및 로그 저장
    """
    def post(self, request):
        auth_token = request.headers.get('Authorization', None).replace('Bearer ', '')
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms='HS256')

        farmID = payload['farmID']

        try:
            farm = FarmProfile.objects.get(farmID=farmID)
        except FarmProfile.DoesNotExist:
            return Response({"error": "No Farm Profile"}, status=status.HTTP_404_NOT_FOUND)

        ################################################
        raw_data = request.data.get('image')
        fmt, imgStr = raw_data.split(';base64,')
        ext = fmt.split('/')[-1]

        img_data = base64.b64decode(imgStr)

        imgArr = np.frombuffer(img_data, dtype=np.uint8)
        img = cv2.imdecode(imgArr, cv2.IMREAD_COLOR)

        # image_file = ContentFile(img_data, name=f'image.{ext}')
        ################################################

        disease, confidence = detect_disease(np.array(img))

        DiseaseLog.objects.create(farmID=farm, image=raw_data, disease=disease, confidence=confidence)

        response = Response({
            "disease": disease,
            "confidence": f"{confidence:.2f}%",
            "message": "Successful Disease Detection"
        }, status=status.HTTP_201_CREATED)

        response['Authorization'] = auth_token

        return response


class GetFarmDisease(APIView):
    """
    농장 질병 조회
    """
    def get(self, request):
        auth_token = request.headers.get('Authorization', None).replace('Bearer ', '')
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms='HS256')

        farmID = payload['farmID']

        diseases = DiseaseLog.objects.filter(farmID=farmID)

        serializerList = []
        for disease in diseases:
            serializer = DiseaseSerializer(disease)
            serializerList.append(serializer.data)

        response = Response(serializerList, status=status.HTTP_200_OK)
        response['Authorization'] = auth_token

        return response


class DeleteDiseaseLog(APIView):
    """
    질병 로그 삭제
    """
    def delete(self, request):
        auth_token = request.headers.get('Authorization', None).replace('Bearer ', '')
        diseaseID = request.data.get('diseaseID')

        DiseaseLog.objects.get(id=diseaseID).delete()

        response = Response({"message": "Disease log deleted successfully"},
                            status=status.HTTP_200_OK)
        response['Authorization'] = auth_token

        return response
