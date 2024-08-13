from rest_framework import serializers
from .models import DiseaseLog


class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseaseLog
        fields = [
            'id',
            'disease',
            'timestamp',
            'confidence'
        ]
