from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
import jwt

from Farm.models import FarmProfile
from Farm.serializers import FarmSerializer
from Users.models import User

from Sodamteo import settings


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

        # 2 find user
        try:
            userID = User.objects.get(id=payload['id'])
        except User.DoesNotExist:
            return Response({"error": "can't find email"}, status=status.HTTP_404_NOT_FOUND)

        # 3 create farm
        farm = FarmProfile.objects.create(userID=userID, cropName=cropName, farmName=farmName)

        serializer = FarmSerializer(farm)

        new_payload = {
            'token_type': payload['token_type'],
            'exp': payload['exp'],
            'iat': payload['iat'],
            'jti': payload['jti'],
            'id': payload['id'],
            'farmID': farm.farmID
        }
        new_token = jwt.encode(new_payload, settings.SECRET_KEY, algorithm='HS256')

        response = Response(serializer.data, status.HTTP_201_CREATED)
        response['Authorization'] = 'Bearer ' + new_token

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
            serializer = FarmSerializer(farm)
            serializerList.append(serializer.data)

        response = Response(serializerList, status.HTTP_200_OK)
        response['Authorization'] = 'Bearer ' + auth_token

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
        farmName = data.get('farmName')

        if not userID or not farmName:
            return Response({"error": "Email and Farm Name are required"}, status=status.HTTP_400_BAD_REQUEST)

        # find farm
        try:
            farm = FarmProfile.objects.get(userID=userID, farmName=farmName)
        except FarmProfile.DoesNotExist:
            return Response({"error": "No Farm Profile"}, status=status.HTTP_404_NOT_FOUND)

        # 4 serialize
        serializer = FarmSerializer(farm)

        new_payload = {
            'token_type': payload['token_type'],
            'exp': payload['exp'],
            'iat': payload['iat'],
            'jti': payload['jti'],
            'id': payload['id'],
            'farmID': farm.farmID
        }
        new_token = jwt.encode(new_payload, settings.SECRET_KEY, algorithm='HS256')

        response = Response(serializer.data, status.HTTP_200_OK)
        response['Authorization'] = 'Bearer ' + new_token

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

        new_crop = request.data.get('newCrop')
        newFarmName = request.data.get('newFarmName')

        try:
            farm = FarmProfile.objects.get(farmID=farmID)
        except FarmProfile.DoesNotExist:
            return Response({"error": "can't find farm"}, status=status.HTTP_404_NOT_FOUND)

        farm.cropName = new_crop
        if newFarmName:
            farm.farmName = newFarmName

        farm.save()

        serializer = FarmSerializer(farm)

        new_payload = {
            'token_type': payload['token_type'],
            'exp': payload['exp'],
            'iat': payload['iat'],
            'jti': payload['jti'],
            'id': payload['id'],
            'farmID': farm.farmID
        }
        new_token = jwt.encode(new_payload, settings.SECRET_KEY, algorithm='HS256')

        response = Response(serializer.data, status.HTTP_200_OK)
        response['Authorization'] = 'Bearer ' + new_token

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

        response = Response({"message: Deleted Successfully"}, status.HTTP_200_OK)
        response['Authorization'] = 'Bearer ' + new_token

        return response
