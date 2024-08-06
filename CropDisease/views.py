import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from Sodamteo import settings
from .models import DiseaseLog
from .detect_disease import detect_disease


class DiseaseDetection(APIView):
    """
    질병 탐지
    """

    def post(self, request):
        # 이미지 파일을 입력받음
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

        # 질병 탐지 결과를 로그로 저장
        farm_name = request.data.get('farmName')
        if not farm_name:
            return Response({"error": "Farm name is required"}, status=status.HTTP_400_BAD_REQUEST)

        DiseaseLog.objects.create(farmName=farm_name, disease=disease)

        # 임시 파일 삭제
        os.remove(temp_image_path)

        return Response({
            "disease": disease,
            "confidence": f"{confidence:.2f}%",
            "message": "Disease detection successful"
        }, status=status.HTTP_200_OK)


class GetFarmDisease(APIView):
    """
    농장 질병 조회
    """

    def get(self, request):
        farm_name = request.GET.get('farmName')

        if not farm_name:
            return Response({"error": "Farm name is required"}, status=status.HTTP_400_BAD_REQUEST)

        diseases = DiseaseLog.objects.filter(farmName=farm_name).values_list('disease', flat=True)
        return Response({"diseases": list(diseases)}, status=status.HTTP_200_OK)
