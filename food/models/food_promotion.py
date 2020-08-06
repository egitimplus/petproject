from django.db import models


class FoodPromotion(models.Model):
    site = models.OneToOneField('food.FoodSite', on_delete=models.CASCADE, related_name='foodpromotion', primary_key=True)
    food = models.ForeignKey('food.Food', on_delete=models.CASCADE, related_name='foodpromotion')
    name = models.CharField(max_length=255)
