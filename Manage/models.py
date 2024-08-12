from django.db import models
from Farm.models import FarmProfile


class Device(models.Model):
    farmID = models.ForeignKey(FarmProfile, on_delete=models.CASCADE, related_name='farm_devices')
    device = models.CharField(max_length=100)
    status = models.FloatField()

    class Meta:
        db_table = 'Device'

    def __str__(self):
        return f"{self.device} is now {self.status}"
