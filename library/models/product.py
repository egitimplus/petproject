from django.db import models


class ProductLink(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    food_type = models.CharField(max_length=255)
    url = models.URLField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    active = models.BooleanField(default=1)
    down = models.BooleanField(default=0)
    food = models.ForeignKey('food.Food', on_delete=models.SET_NULL, null=True, blank=True, related_name='productlink')
    petshop = models.ForeignKey('company.PetShop', on_delete=models.SET_NULL, null=True, blank=True, related_name='productlink')

    def __str__(self):
        return '%s - %s' % (self.brand, self.name)

