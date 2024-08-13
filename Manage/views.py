import jwt
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from Farm.serializers import FarmSerializer

from .models import Device
from Sodamteo import settings


class Airconditioner(APIView):
    def post(self, request):
        auth_token = request.headers.get('Authorization', None).replace('Bearer ', '')
        payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms='HS256')
        farmID = payload['farmID']

        device = request.data.get('device')
        targetValue = request.data.get('targetValue')

        deviceStatus, created = Device.objects.get_or_create(
            farmID=farmID,
            device=device,
            defaults={'status': targetValue}
        )

        if not created:
            deviceStatus.status = targetValue
            deviceStatus.save()

        serializer = FarmSerializer(deviceStatus)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        auth_token = request.headers.get('Authorization', None).replace('Bearer ', '')
        payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms='HS256')
        farmID = payload['farmID']

        device = request.data.get('device')

        try:
            deviceStatus = Device.objects.get(farmID=farmID, device=device)
        except Exception as e:
            return Response({"error": "No airconditioner status"}, status=status.HTTP_404_NOT_FOUND)

        serializer = FarmSerializer(deviceStatus)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Humidifier(APIView):
    def post(self, request):
        auth_token = request.headers.get('Authorization', None).replace('Bearer ', '')
        payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms='HS256')
        farmID = payload['farmID']

        device = request.data.get('device')
        targetValue = request.data.get('targetValue')

        deviceStatus, created = Device.objects.get_or_create(
            farmID=farmID,
            device=device,
            defaults={'status': targetValue}
        )

        if not created:
            deviceStatus.status = targetValue
            deviceStatus.save()

        serializer = FarmSerializer(deviceStatus)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        auth_token = request.headers.get('Authorization', None).replace('Bearer ', '')
        payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms='HS256')
        farmID = payload['farmID']

        device = request.data.get('device')

        try:
            deviceStatus = Device.objects.get(farmID=farmID, device=device)
        except Exception as e:
            return Response({"error": "No airconditioner status"}, status=status.HTTP_404_NOT_FOUND)

        serializer = FarmSerializer(deviceStatus)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Fertilizer(APIView):
    def post(self, request):
        auth_token = request.headers.get('Authorization', None).replace('Bearer ', '')
        payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms='HS256')
        farmID = payload['farmID']

        device = request.data.get('device')
        targetValue = request.data.get('targetValue')

        deviceStatus, created = Device.objects.get_or_create(
            farmID=farmID,
            device=device,
            defaults={'status': targetValue}
        )
        if not created:
            deviceStatus.status = targetValue
            deviceStatus.save()

        serializer = FarmSerializer(deviceStatus)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        auth_token = request.headers.get('Authorization', None).replace('Bearer ', '')
        payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms='HS256')
        farmID = payload['farmID']

        device = request.data.get('device')

        try:
            deviceStatus = Device.objects.get(farmID=farmID, device=device)
        except Exception as e:
            return Response({"error": "No airconditioner status"}, status=status.HTTP_404_NOT_FOUND)

        serializer = FarmSerializer(deviceStatus)
        return Response(serializer.data, status=status.HTTP_200_OK)
