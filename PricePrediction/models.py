from django.db import models


class CropPricePredict(models.Model):
    crop = models.CharField(max_length=100)
    date = models.DateField()
    price = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'CropPricePredict'
        unique_together = ('crop', 'date')
        verbose_name = 'Crop Price Prediction'
        verbose_name_plural = 'Crop Price Predictions'

    def __str__(self):
        return f"{self.crop} - {self.date} - {self.price}"
