from rest_framework import serializers
from .models import FarmEnvironment, DefaultEnvironment
from Farm.serializers import FarmSerializer


class CurrEnvSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmEnvironment
        fields = '__all__'


class OptEnvSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultEnvironment
        fields = '__all__'
