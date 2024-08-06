from django.db import models
from Users.models import User


class DiseaseLog(models.Model):
    ID = models.AutoField(primary_key=True)
    farmName = models.CharField(max_length=100)
    disease = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'DiseaseLog'

    def __str__(self):
        return f"{self.ID} - {self.farmName} - {self.disease}"
