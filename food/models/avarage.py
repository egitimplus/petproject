from django.db import models


class Avarage(models.Model):
    name = models.CharField(max_length=255, unique=True)
    avarage = models.FloatField(default=0)
    recommend = models.FloatField(default=0)
    max_value = models.FloatField(default=0)
    min_value = models.FloatField(default=0)

    def __str__(self):
        return self.food.name

