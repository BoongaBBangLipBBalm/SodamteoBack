from django.db import models
from django.db.models import ImageField

from Farm.models import FarmProfile


class DiseaseLog(models.Model):
    id = models.AutoField(primary_key=True)
    farmID = models.ForeignKey(FarmProfile, on_delete=models.CASCADE, related_name='disease')
    image = models.TextField(blank=True, null=True)
    disease = models.CharField(max_length=100)
    confidence = models.FloatField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    img = models.TextField(null=True)

    class Meta:
        db_table = 'DiseaseLog'

    def __str__(self):
        return f"{self.timestamp} - {self.disease}({self.confidence})"
