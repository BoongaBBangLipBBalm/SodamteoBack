from django.db import models
from Users.models import User


class FarmProfile(models.Model):
    farmID = models.CharField(max_length=100, primary_key=True)
    userID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farms')
    crop = models.CharField(max_length=100)

    class Meta:
        db_table = 'FarmProfile'
        unique_together = (('farmID', 'userID'),)

    def __str__(self):
        return f"{self.farmID} - {self.crop}"
