from django.db import models


class FoodIngredient(models.Model):

    id = models.AutoField(primary_key=True)
    ingredient = models.ForeignKey('food.Ingredient', on_delete=models.CASCADE, related_name='ingredient')
    food = models.ForeignKey('food.Food', on_delete=models.CASCADE, related_name='food')
    ingredient_percent = models.FloatField(default=0)
    top_ingredient = models.PositiveSmallIntegerField(default=0)
    dehydrated_percent = models.FloatField(default=0)

    class Meta:
        ordering=['id']
