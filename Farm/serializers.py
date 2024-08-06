from rest_framework import serializers
from .models import FarmProfile


class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmProfile
        fields = '__all__'
