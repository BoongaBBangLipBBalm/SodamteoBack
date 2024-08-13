import os
import jwt

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

        # 이미지 파일을 입력 받음
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)

        # 이미지 파일을 서버에 임시로 저장
        temp_image_path = os.path.join(settings.MEDIA_ROOT, image_file.name)
        with open(temp_image_path, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)

        # 질병 탐지
        disease, confidence = detect_disease(temp_image_path)

        DiseaseLog.objects.create(farmID=farm, disease=disease, confidence=confidence)

        # 임시 파일 삭제
        os.remove(temp_image_path)

        response = Response({
            "disease": disease,
            "confidence": f"{confidence:.2f}%",
            "message": "Successful Disease Detection"
        }, status=status.HTTP_201_CREATED)

        response['Authorization'] = 'Bearer ' + auth_token

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
        response['Authorization'] = 'Bearer ' + auth_token

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
        response['Authorization'] = 'Bearer ' + auth_token

        return response
