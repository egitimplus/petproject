from django.db import models


class Dry(models.Model):
    food = models.OneToOneField('food.Food', on_delete=models.CASCADE, related_name='dry', primary_key=True)
    protein = models.FloatField(default=0)
    fat = models.FloatField(default=0)
    fibre = models.FloatField(default=0)
    ash = models.FloatField(default=0)
    calcium = models.FloatField(default=0)
    phosphorus = models.FloatField(default=0)
    magnesium = models.FloatField(default=0)
    taurine = models.FloatField(default=0)
    omega3 = models.FloatField(default=0)
    omega6 = models.FloatField(default=0)
    dha = models.FloatField(default=0)
    epa = models.FloatField(default=0)
    carbs = models.FloatField(default=0)

    def __str__(self):
        return self.food.name

