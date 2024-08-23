import re

from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
import jwt
import json

from CropSelection.serializers import CurrEnvSerializer
from Farm.models import FarmProfile
from Farm.serializers import AllFarmSerializer, SingleFarmSerializer, OnlyProfileSerializer
from Manage.serializers import DeviceSerializer
from Users.models import User
from Manage.models import Device

from Sodamteo import settings
from media.false import saveFalseData


class CreateFarm(APIView):
    """
    농장 생성
    """

    def post(self, request):
        # 1 input data
        auth_token = request.headers.get('Authorization', None).replace('Bearer ', '')
        payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms='HS256')

        cropName = request.data.get('cropName')
        farmName = request.data.get('farmName')
        devices = (request.data.get('devices'))
        devices = re.sub(r'\[|]$', '', devices).replace(' ', '').split(',')

        # 2 find user
        try:
            userID = User.objects.get(id=payload['id'])
        except User.DoesNotExist:
            return Response({"error": "can't find email"}, status=status.HTTP_404_NOT_FOUND)

        # 3 create farm
        farm = FarmProfile.objects.create(userID=userID, cropName=cropName, farmName=farmName)

        for device in devices:
            if not device: break
            Device.objects.create(farmID=farm, device=device, status=0, isAuto=False)

        devices = farm.farm_devices.all()
        if devices:
            deviceSerializers = DeviceSerializer(devices, many=True).data
        else:
            deviceSerializers = "No Devices Yet"

        serializer = AllFarmSerializer(farm)

        new_payload = {
            'token_type': payload['token_type'],
            'exp': payload['exp'],
            'iat': payload['iat'],
            'jti': payload['jti'],
            'id': payload['id'],
            'farmID': farm.farmID
        }
        new_token = jwt.encode(new_payload, settings.SECRET_KEY, algorithm='HS256')

        response = Response({"message": "New Token Arrived",
                             "farmInfo": serializer.data,
                             "device": deviceSerializers}, status.HTTP_201_CREATED)
        response['Authorization'] = new_token

        return response


class GetFarmList(APIView):
    '''
    사용자의 모든 Farm Profile 조회
    '''
    def get(self, request):
        auth_token = request.headers.get('Authorization', None).replace('Bearer ', '')
        payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms='HS256')

        userID = payload['id']

        try:
            farmList = FarmProfile.objects.filter(userID=userID)
        except FarmProfile.DoesNotExist:
            return Response({"error": "No Farm Profile Yet"}, status=status.HTTP_404_NOT_FOUND)

        serializerList = []
        for farm in farmList:
            saveFalseData(farm.farmID) #################### 가짜 데이터 save하므로 나중에 지우기
            serializer = AllFarmSerializer(farm)
            serializerList.append(serializer.data)

        response = Response(serializerList, status.HTTP_200_OK)
        response['Authorization'] = auth_token

        return response


class GetFarm(APIView):
    """
    농장 조회
    """
    def get(self, request):
        # 1 input data
        data = request.GET

        auth_token = request.headers.get('Authorization', None).replace('Bearer ', '')
        payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])

        userID = payload['id']
        farmID = data.get('farmID')

        if not userID or not farmID:
            return Response({"error": "Email and Farm Name are required"}, status=status.HTTP_400_BAD_REQUEST)

        # find farm
        try:
            farm = FarmProfile.objects.get(farmID=farmID)
        except FarmProfile.DoesNotExist:
            return Response({"error": "No Farm Profile"}, status=status.HTTP_404_NOT_FOUND)

        # 4 serialize
        serializer = OnlyProfileSerializer(farm)

        environmentList = farm.farm_environment.all()
        currEnvSerializers = []
        cnt = 0
        for environment in environmentList:
            currEnv = CurrEnvSerializer(environment)
            currEnvSerializers.append(currEnv.data)
            cnt += 1
            if cnt == 5: break

        devices = farm.farm_devices.all()
        if devices:
            deviceSerializers = DeviceSerializer(devices, many=True).data
        else:
            deviceSerializers = "No Devices Yet"

        new_payload = {
            'token_type': payload['token_type'],
            'exp': payload['exp'],
            'iat': payload['iat'],
            'jti': payload['jti'],
            'id': payload['id'],
            'farmID': farmID
        }
        new_token = jwt.encode(new_payload, settings.SECRET_KEY, algorithm='HS256')

        response = Response({"FarmInfo": serializer.data, "environment": currEnvSerializers, "device": deviceSerializers,
                             "message": "New Token Arrived"}, status.HTTP_200_OK)
        response['Authorization'] = new_token

        return response


class UpdateFarm(APIView):
    """
    농장 수정
    """
    def patch(self, request):
        # 1 input data
        token = request.headers.get('Authorization', None).replace('Bearer ', '')
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        farmID = payload['farmID']

        newFarmName = request.data.get('newFarmName')

        try:
            farm = FarmProfile.objects.get(farmID=farmID)
        except FarmProfile.DoesNotExist:
            return Response({"error": "can't find farm"}, status=status.HTTP_404_NOT_FOUND)

        if newFarmName:
            farm.farmName = newFarmName

        farm.save()

        serializer = SingleFarmSerializer(farm)

        response = Response({"FarmInfo": serializer.data}, status.HTTP_200_OK)
        response['Authorization'] = token

        return response


class DeleteFarm(APIView):
    """
    농장 삭제
    """
    def delete(self, request):
        # 1 input data
        token = request.headers.get('Authorization', None).replace('Bearer ', '')
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        farmID = payload['farmID']

        # 3 find farm
        try:
            farm = FarmProfile.objects.get(farmID=farmID)
        except FarmProfile.DoesNotExist:
            return Response({"error": "can't find farm"}, status=status.HTTP_404_NOT_FOUND)

        # 4 delete farm
        farm.delete()

        new_payload = {
            'token_type': payload['token_type'],
            'exp': payload['exp'],
            'iat': payload['iat'],
            'jti': payload['jti'],
            'id': payload['id']
        }
        new_token = jwt.encode(new_payload, settings.SECRET_KEY, algorithm='HS256')

        response = Response({"message": "Deleted Successfully and New Token Arrived"}, status.HTTP_200_OK)
        response['Authorization'] = new_token

        return response
