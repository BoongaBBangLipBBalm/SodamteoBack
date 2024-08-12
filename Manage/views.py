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
        auth_token = request.header.get('Authorization').replace('Bearer ', '')
        payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])
        farmID = payload['farmID']

        device = request.data.get('device')
        targetValue = request.get.data('targetValue')

        deviceStatus = Device.objects.get(farmID=farmID, deviceID=device)

        if deviceStatus:
            deviceStatus.status = targetValue
            deviceStatus.save()
        else:
            deviceStatus = Device.objects.create(farmID=farmID, deviceID=device, status=targetValue)

        serializer = FarmSerializer(deviceStatus)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        auth_token = request.header.get('Authorization').replace('Bearer ', '')
        payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])
        farmID = payload['farmID']

        device = request.data.get('device')

        try:
            deviceStatus = Device.objects.get(farmID=farmID, deviceID=device)
        except Exception as e:
            return Response({"error": "No airconditioner status"}, status=status.HTTP_404_NOT_FOUND)

        serializer = FarmSerializer(deviceStatus)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Humidifier(APIView):
    def post(self, request):
        auth_token = request.header.get('Authorization').replace('Bearer ', '')
        payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])
        farmID = payload['farmID']

        device = request.data.get('device')
        targetValue = request.get.data('targetValue')

        deviceStatus = Device.objects.get(farmID=farmID, deviceID=device)

        if deviceStatus:
            deviceStatus.status = targetValue
            deviceStatus.save()
        else:
            deviceStatus = Device.objects.create(farmID=farmID, deviceID=device, status=targetValue)

        serializer = FarmSerializer(deviceStatus)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        auth_token = request.header.get('Authorization').replace('Bearer ', '')
        payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])
        farmID = payload['farmID']

        device = request.data.get('device')

        try:
            deviceStatus = Device.objects.get(farmID=farmID, deviceID=device)
        except Exception as e:
            return Response({"error": "No airconditioner status"}, status=status.HTTP_404_NOT_FOUND)

        serializer = FarmSerializer(deviceStatus)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CO2(APIView):
    def post(self, request):
        auth_token = request.header.get('Authorization').replace('Bearer ', '')
        payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])
        farmID = payload['farmID']

        device = request.data.get('device')
        targetValue = request.get.data('targetValue')

        deviceStatus = Device.objects.get(farmID=farmID, deviceID=device)

        if deviceStatus:
            deviceStatus.status = targetValue
            deviceStatus.save()
        else:
            deviceStatus = Device.objects.create(farmID=farmID, deviceID=device, status=targetValue)

        serializer = FarmSerializer(deviceStatus)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        auth_token = request.header.get('Authorization').replace('Bearer ', '')
        payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])
        farmID = payload['farmID']

        device = request.data.get('device')

        try:
            deviceStatus = Device.objects.get(farmID=farmID, deviceID=device)
        except Exception as e:
            return Response({"error": "No airconditioner status"}, status=status.HTTP_404_NOT_FOUND)

        serializer = FarmSerializer(deviceStatus)
        return Response(serializer.data, status=status.HTTP_200_OK)
