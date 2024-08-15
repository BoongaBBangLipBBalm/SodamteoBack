import jwt
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import Device
from .serializers import DeviceSerializer
from Farm.models import FarmProfile

from Sodamteo import settings


class DeviceManager(APIView):
    def post(self, request):
        auth_token = request.headers.get('Authorization', None).replace('Bearer ', '')
        payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms='HS256')
        farmID = payload['farmID']

        device = request.data.get('device')

        try:
            farm = FarmProfile.objects.get(farmID=farmID)
        except Exception as e:
            return Response({"error": 'Farm not found'}, status=status.HTTP_404_NOT_FOUND)

        deviceStatus, created = Device.objects.get_or_create(
            farmID=farm,
            device=device,
            status=0.
        )

        if not created:
            return Response({"message": "Device already exists"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = DeviceSerializer(deviceStatus)

        response = Response(serializer.data, status=status.HTTP_200_OK)
        response['Authorization'] = 'Bearer ' + auth_token

        return response

    def get(self, request):
        auth_token = request.headers.get('Authorization', None).replace('Bearer ', '')
        payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms='HS256')
        farmID = payload['farmID']

        device = request.data.get('device')

        try:
            deviceStatus = Device.objects.filter(farmID=farmID)
        except Exception as e:
            return Response({"error": "No airconditioner status"}, status=status.HTTP_404_NOT_FOUND)

        serializerList = []
        for device in deviceStatus:
            serializer = DeviceSerializer(device)
            serializerList.append(serializer.data)

        response = Response(serializerList, status=status.HTTP_200_OK)
        response['Authorization'] = 'Bearer ' + auth_token

        return response

    def patch(self, request):
        auth_token = request.headers.get('Authorization', None).replace('Bearer ', '')
        payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms='HS256')
        farmID = payload['farmID']
        device = request.data.get('device')
        targetValue = request.data.get('targetValue')

        try:
            deviceStatus = Device.objects.get(farmID=farmID, device=device)
        except Exception as e:
            return Response({"error": f"No {device} status"}, status=status.HTTP_404_NOT_FOUND)

        deviceStatus.status = targetValue
        deviceStatus.save()

        serializer = DeviceSerializer(deviceStatus)

        response = Response(serializer.data, status=status.HTTP_200_OK)
        response['Authorization'] = 'Bearer ' + auth_token

        return response
