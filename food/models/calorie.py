from django.db import models


class Calorie(models.Model):
    food = models.OneToOneField('food.Food', on_delete=models.CASCADE, related_name='calorie', primary_key=True)
    protein = models.FloatField(default=0)
    fat = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    total = models.FloatField(default=0)

    def __str__(self):
        return self.food.name

