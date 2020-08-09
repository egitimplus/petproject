from django.db import models


class FoodSite(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    food = models.ForeignKey('food.Food', on_delete=models.CASCADE, related_name='foodsite')
    petshop = models.ForeignKey('company.PetShop', on_delete=models.CASCADE, related_name='foodsite')
    size = models.ForeignKey('food.FoodSize', on_delete=models.SET_NULL, null=True, blank=True, related_name='foodsite')
    url = models.URLField()
    old_price = models.FloatField(default=0)
    price = models.FloatField(default=0)
    stock = models.BooleanField(default=False)
    cargo = models.BooleanField(default=False)
    best_before = models.DateField(null=True, blank=True)
    top_site = models.PositiveSmallIntegerField(default=0)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    code = models.CharField(max_length=255)

    def __str__(self):
        return '%s - %s' % (self.company.name, self.name)
