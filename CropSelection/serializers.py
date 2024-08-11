from rest_framework import serializers
from .models import FarmEnvironment


class EnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmEnvironment
        fields = '__all__'
