from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.response import status
from rest_framework.views import APIView
from Farm.serializers import FarmSerializer

from SodamteoBack import Manage
from SodamteoBack.CropSelection.views import CropSelection

# Create your views here.
class GetFarm(APIView):
    def get(self, request):
        farmName = request.data.get('farName')
        farm_status = CropSelection.objects.get(farmId=farmName)
        serializer = FarmSerializer(farm_status)
        return Response(serializer.data)

class Aircon(APIView):
    def get(self, request):
        farmName = request.data.get('farName')
        device = request.data.get('device')

        try:
            device_status = Manage.objects.get(farmName=farmName, device=device)
        except Manage.DoesNotExist:
            return Response({"error": "can't find Airconditioner status"}, status=status.HTTP_404_NOT_FOUND)

        serializer = FarmSerializer(device_status)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        farmName = request.data.get('farmName')
        device = request.data.get('device')
        temp_opt = request.get.data('tempOpt')
        manage = Manage.objects.get(farmName='farmName', device='device')
        serializer = FarmSerializer(manage)
        manage.status = temp_opt
        manage.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class Humid(APIView):
    def get(self, request):
        farmName = request.data.get('farName')
        device = request.data.get('device')

        try:
            device_status = Manage.objects.get(farmName=farmName, device=device)
        except Manage.DoesNotExist:
            return Response({"error": "can't find Humidifier status"}, status=status.HTTP_404_NOT_FOUND)

        serializer = FarmSerializer(device_status)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch(self, request):
        farmName = request.data.get('farName')
        device = request.data.get('device')
        humid_opt = request.data.get('humidOpt')
        manage = Manage.objects.get(farmName='farmName',device='device')
        serializer = FarmSerializer(manage)
        manage.status = humid_opt
        manage.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class Co2(APIView):
    def get(self, request):
        farmName = request.data.get('farName')
        device = request.data.get('device')

        try:
            device_status = Manage.objects.get(farmName=farmName, device=device)
        except Manage.DoesNotExist:
            return Response({"error": "can't find Co2 status"}, status=status.HTTP_404_NOT_FOUND)

        serializer = FarmSerializer(device_status)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self,request):
        farmName = request.data.get('farName')
        device = request.data.get('device')
        co2_opt = request.data.get('co2Opt')
        manage = Manage.objects.get(farmName='farmName',device='device')
        serializer = FarmSerializer(manage)
        manage.status = co2_opt
        manage.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)