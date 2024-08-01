from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from Farm.models import FarmProfile
from Farm.serializers import FarmSerializer
from Users.models import User
import json


# Create your views here.

class CreateFarm(APIView):
    """
    농장 생성
    """

    def post(self, request):

        # 1 input data
        user = request.data.get('email')
        crop = request.data.get('crop')

        # 2 find user
        try:
            user = User.objects.get(email=user)
        except User.DoesNotExist:
            if "@" not in user:
                return Response({"error": "can't find email"}, status=status.HTTP_404_NOT_FOUND)

        # 3 create farm
        farm = FarmProfile.objects.create(userID=user, crop=crop, farmID=user.email + crop)

        serializer = FarmSerializer(farm)

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetFarm(APIView):
    """
    농장 조회
    """

    def get(self, request):
        # 1 input data
        # 원본 코드:
        # email = request.data.get('email')
        # crop = request.data.get('crop')

        # 수정된 코드:
        email = request.query_params.get('email')
        crop = request.query_params.get('crop')

        if not email or not crop:
            return Response({"error": "Email and crop are required"}, status=status.HTTP_400_BAD_REQUEST)

        # 2 find user
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            if "@" not in email:
                return Response({"error": "can't find email"}, status=status.HTTP_404_NOT_FOUND)

        # farmID 생성 위치 수정
        farmID = email + crop

        # 3 find farm
        try:
            farm = FarmProfile.objects.get(farmID=farmID)
        except FarmProfile.DoesNotExist:
            return Response({"error": "can't find farm"}, status=status.HTTP_404_NOT_FOUND)

        # 4 serialize
        serializer = FarmSerializer(farm)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateFarm(APIView):
    """
    농장 수정
    """

    def patch(self, request):
        # 1 input data
        email = request.data.get('email')
        crop = request.data.get('crop')
        new_crop = request.data.get('new_crop')

        # 2 find user
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            if "@" not in email:
                return Response({"error": "can't find email"}, status=status.HTTP_404_NOT_FOUND)
        farmID = email + crop
        # 3 find farm
        try:
            farm = FarmProfile.objects.get(farmID=farmID)
        except FarmProfile.DoesNotExist:
            return Response({"error": "can't find farm"}, status=status.HTTP_404_NOT_FOUND)

        # 4 update farm
        farm.crop = new_crop
        farm.farmID = email + new_crop
        farm.save()

        serializer = FarmSerializer(farm)

        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteFarm(APIView):
    """
    농장 삭제
    """

    def delete(self, request):
        # 1 input data
        email = request.data.get('email')
        crop = request.data.get('crop')

        # 2 find user
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            if "@" not in email:
                return Response({"error": "can't find email"}, status=status.HTTP_404_NOT_FOUND)

        farmID = email + crop
        # 3 find farm
        try:
            farm = FarmProfile.objects.get(farmID=farmID)
        except FarmProfile.DoesNotExist:
            return Response({"error": "can't find farm"}, status=status.HTTP_404_NOT_FOUND)

        # 4 delete farm
        farm.delete()

        return Response({"success": "farm deleted"}, status=status.HTTP_200_OK)
