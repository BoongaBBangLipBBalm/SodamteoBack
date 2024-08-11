from django.db import models
from Users.models import User


class FarmProfile(models.Model):
    farmID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farm_profile')
    farmName = models.CharField(max_length=100)
    cropName = models.CharField(max_length=100)

    class Meta:
        db_table = 'FarmProfile'

    def __str__(self):
        return f"{self.farmName} - {self.cropName}"
