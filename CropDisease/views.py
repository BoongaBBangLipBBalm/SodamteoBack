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

        diseases = DiseaseLog.objects.filter(farmName=farm_name).values('disease', 'timestamp')

        result = [{"disease": disease['disease'], "timestamp": disease['timestamp']} for disease in diseases]

        return Response({"diseases": result}, status=status.HTTP_200_OK)


class DeleteDiseaseLog(APIView):
    """
    질병 로그 삭제
    """

    def delete(self, request):
        farm_name = request.data.get('farmName')
        disease = request.data.get('disease')
        timestamp = request.data.get('timestamp')

        if not farm_name or not disease:
            return Response({"error": "Farm name and disease are required"}, status=status.HTTP_400_BAD_REQUEST)

        DiseaseLog.objects.filter(farmName=farm_name, disease=disease, timestamp=timestamp).delete()

        return Response({"message": "Disease log deleted successfully"}, status=status.HTTP_200_OK)
