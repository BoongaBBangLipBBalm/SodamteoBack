from rest_framework import serializers
from .models import FarmEnvironment, DefaultEnvironment


class CurrEnvSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmEnvironment
        fields = ['timestamp', 'N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']


class OptEnvSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultEnvironment
        fields = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
