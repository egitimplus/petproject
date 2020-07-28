from django.db import models


class Avarage(models.Model):
    name = models.CharField(max_length=255, unique=True)
    avarage = models.FloatField(default=0)

    def __str__(self):
        return self.food.name

