from django.db import models


class DryMatter(models.Model):

    food = models.OneToOneField('food.Food', related_name='drymatter', on_delete=models.CASCADE, primary_key=True)
    protein = models.FloatField()
    carbs = models.FloatField()
    fat = models.FloatField()
    fiber = models.FloatField()
    ash = models.FloatField()
