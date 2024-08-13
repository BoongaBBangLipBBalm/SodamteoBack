from django.db import models
from Farm.models import FarmProfile


class FarmEnvironment(models.Model):
    farmID = models.ForeignKey(FarmProfile, on_delete=models.CASCADE, related_name='farm_environment')
    timestamp = models.DateTimeField(auto_now_add=True)
    N = models.FloatField(null=True)
    P = models.FloatField(null=True)
    K = models.FloatField(null=True)
    temperature = models.FloatField(null=True)
    humidity = models.FloatField(null=True)
    ph = models.FloatField(null=True)
    rainfall = models.FloatField(null=True)

    class Meta:
        db_table = 'EnvironmentLog'

    def __str__(self):
        return (f"{self.timestamp} - {self.farmID}: N({self.N}), P({self.P}), K({self.K}), "
                f"Temperature({self.temperature}), Humidity({self.humidity}), pH({self.ph}), Rainfall({self.rainfall})")


class DefaultEnvironment(models.Model):
    cropName = models.CharField(primary_key=True, max_length=100)
    N = models.FloatField(null=True)
    P = models.FloatField(null=True)
    K = models.FloatField(null=True)
    temperature = models.FloatField(null=True)
    humidity = models.FloatField(null=True)
    ph = models.FloatField(null=True)
    rainfall = models.FloatField(null=True)

    class Meta:
        db_table = 'DefaultEnvironment'

    def __str__(self):
        return (f"{self.cropName}: N({self.N}), P({self.P}), K({self.K}), "
                f"Temperature({self.temperature}), Humidity({self.humidity}), pH({self.ph}), Rainfall({self.rainfall})")
