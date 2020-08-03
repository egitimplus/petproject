from django.db import models


class FoodSite(models.Model):

    id = models.AutoField(primary_key=True)
    food = models.ForeignKey('food.Food', on_delete=models.CASCADE, related_name='foodsite')
    company = models.ForeignKey('company.PetShop', on_delete=models.CASCADE, related_name='foodsite')
    size = models.ForeignKey('food.FoodSize', on_delete=models.CASCADE, related_name='foodsite')
    url = models.URLField()
    price = models.FloatField(default=0)
    stock = models.BooleanField(default=False)
    top_site = models.PositiveSmallIntegerField(default=0)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return '%s - %s'. % (self.company.name, self.food.name)
