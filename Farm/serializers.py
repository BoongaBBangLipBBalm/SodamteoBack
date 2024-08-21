from rest_framework import serializers

from CropSelection.serializers import CurrEnvSerializer
from .models import FarmProfile


class OnlyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmProfile
        fields = ['farmName', 'cropName']


class AllFarmSerializer(serializers.ModelSerializer):
    farm_environment = serializers.SerializerMethodField()

    class Meta:
        model = FarmProfile
        fields = ['farmID', 'farmName', 'cropName', 'farm_environment']

    def get_farm_environment(self, obj):
        latest = obj.farm_environment.order_by('-timestamp').last()
        if latest:
            return CurrEnvSerializer(latest).data
        return None


class SingleFarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmProfile
        fields = ['farmID', 'farmName', 'cropName']
