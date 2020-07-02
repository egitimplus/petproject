from django.db import models


class Calorie(models.Model):

    food = models.OneToOneField('food.Food', related_name='calorie', on_delete=models.CASCADE, primary_key=True)
    protein = models.FloatField()
    carbs = models.FloatField()
    fat = models.FloatField()
    total = models.FloatField()
