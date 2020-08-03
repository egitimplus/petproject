from django.db import models


class Site(models.Model):

    id = models.AutoField(primary_key=True)
    brand = models.ForeignKey('company.Brand', on_delete=models.CASCADE, related_name='site')
    company = models.ForeignKey('company.PetShop', on_delete=models.CASCADE, related_name='site')
    size = models.ForeignKey('food.FoodSize', on_delete=models.CASCADE, related_name='site')
    url = models.URLField()
    price = models.FloatField(default=0)
    stock = models.BooleanField(default=False)
    top_site = models.PositiveSmallIntegerField(default=0)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return '%s - %s' % (self.company.name, self.brand.name)
