# Generated by Django 5.0.7 on 2024-08-23 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("CropDisease", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="diseaselog",
            name="img",
            field=models.TextField(null=True),
        ),
    ]
