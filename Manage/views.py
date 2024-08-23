import jwt
import yaml
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from CropSelection.models import DefaultEnvironment
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

        exist = farm.farm_devices.filter(device=device)
        if not exist:
            deviceStatus = Device.objects.create(farmID=farm, device=device, status=0.)
        else:
            return Response({"message": "Device already exists"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = DeviceSerializer(deviceStatus)

        response = Response(serializer.data, status=status.HTTP_200_OK)
        response['Authorization'] = auth_token

        return response

    def get(self, request):
        auth_token = request.headers.get('Authorization', None).replace('Bearer ', '')
        payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms='HS256')
        farmID = payload['farmID']

        try:
            deviceStatus = Device.objects.filter(farmID=farmID)
        except Exception as e:
            return Response({"error": "No airconditioner status"}, status=status.HTTP_404_NOT_FOUND)

        serializerList = []
        for device in deviceStatus:
            serializer = DeviceSerializer(device)
            serializerList.append(serializer.data)

        response = Response(serializerList, status=status.HTTP_200_OK)
        response['Authorization'] = auth_token

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
        response['Authorization'] = auth_token

        return response

    def delete(self, request):
        auth_token = request.headers.get('Authorization', None).replace('Bearer ', '')
        payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms='HS256')
        farmID = payload['farmID']
        device = request.data.get('device')

        try:
            farm = FarmProfile.objects.get(farmID=farmID)
        except Exception as e:
            return Response({"error": "Farm not found"}, status=status.HTTP_404_NOT_FOUND)

        if farm.farm_devices.filter(device=device).exists():
            farm.farm_devices.filter(device=device).delete()
            response = Response({"message": f"{device} deleted successfully"}, status=status.HTTP_200_OK)
        else:
            response = Response({"message": f"{device} not found"}, status=status.HTTP_404_NOT_FOUND)

        response['Authorization'] = auth_token
        return response


class autoManage(APIView):
    def patch(self, request):
        auth_token = request.headers.get('Authorization', None).replace('Bearer ', '')
        payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms='HS256')
        farmID = payload['farmID']
        device = request.data.get('device')
        auto = request.data.get('isAuto')

        try:
            deviceStatus = Device.objects.get(farmID=farmID, device=device)
        except Exception as e:
            return Response({"error": f"No {device} status"}, status=status.HTTP_404_NOT_FOUND)

        if auto:
            crop = FarmProfile.objects.get(farmID=farmID).cropName
            default = DefaultEnvironment.objects.filter(cropName=crop).first()

            if not default:
                return Response({"error": "Default environment settings not found for this crop"},
                                status=status.HTTP_404_NOT_FOUND)

            if device == "Airconditioner":
                new_status = default.temperature
            elif device == "Humidifier":
                new_status = default.humidity
            elif device == "Fertilizer":
                # N, P, K, pH의 평균값 계산
                new_status = (default.N + default.P + default.K + default.ph) / 4
            else:
                return Response({"error": "Unsupported device"}, status=status.HTTP_400_BAD_REQUEST)

            deviceStatus.status = new_status
            deviceStatus.isAuto = auto
            deviceStatus.save()

        else:
            deviceStatus.isAuto = auto
            deviceStatus.save()

        deviceSerializer = DeviceSerializer(deviceStatus)
        return Response({
            "message": "Auto mode updated",
            "device": deviceSerializer.data
        }, status=status.HTTP_200_OK)