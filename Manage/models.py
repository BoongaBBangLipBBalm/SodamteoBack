from django.db import models
from CropSelection.models import FarmEnvironment
from Farm.models import Farm

class Device(models.Model):
    farmName = models.ForeignKey(Farm, on_delete=models.CASCADE)
    device = models.CharField(max_length=10)
    status = models.FloatField()

    class Meta:
        db_table = 'Device'
        # 이 두 필드를 합쳐서 고유하게 만들어 primary key 역할을 하도록 함
        constraints = [
            models.UniqueConstraint(fields=['farm', 'device'], name='unique_farm_device')
        ]

    def __str__(self):
        return f"{self.farmName}-{self.device} - {self.status}"